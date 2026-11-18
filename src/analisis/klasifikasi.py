"""Tahap 3: kategori calon anomali (outlier asli / patahan / galat input), perbaikan galat input, deduplikasi.

Aturan: hanya GALAT INPUT yang boleh diperbaiki, dan hanya bila terbukti oleh identitas independen
(gerbang bukti). Outlier asli dan patahan ditandai dan dijelaskan, nilainya tidak diubah.
Silver asli tidak ditimpa: hasil perbaikan ditulis ke data/silver/silver_bersih.parquet dengan kolom
`nilai_asal` dan `perbaikan`.

    python -m src.analisis.klasifikasi
    python -m src.analisis.klasifikasi --terapkan
    python -m src.analisis.klasifikasi --terapkan --catat-log
"""
import csv
import sys
from datetime import date
from pathlib import Path
import numpy as np
import pandas as pd

from src.analisis import grid as G

ANOMALI = Path("reports/tabel/calon_anomali.csv")
OUT_TABEL = G.OUT_TABEL
OUT_LAPORAN = Path("reports/klasifikasi_anomali.md")
OUT_BERSIH = Path("data/silver/silver_bersih.parquet")
LUAS = "tabel:sdg15_tutupan_hutan:luas_ribu_ha"
PERSEN = "tabel:sdg15_tutupan_hutan:persen"
KAWASAN = "var1304"
TOL_JUMLAH, TOL_PERSEN, TOL_TOTAL = 0.25, 0.2, 0.15
# patahan serentak: share provinsi yang berubah > ambang dan searah
PANGKAT, AMBANG_MIN, SHARE_MIN, SIGN_MIN, MIN_PROV = 3.0, 5.0, 0.5, 0.8, 20
PEMEKARAN_PAPUA = {9100, 9200, 9400, 9500, 9600, 9700}

RINCIAN_SILVER = {  # label Tahap 2 -> label Silver
    "jumlah": "total", "di luar kawasan hutan/areal penggunaan lain (apl)": "apl",
    "kawasan hutan": "kawasan_hutan", "kritis": "kritis", "sangat kritis": "sangat_kritis",
    "indeks kualitas air": "kualitas_air", "indeks kualitas air laut (ikal)": "kualitas_air_laut",
    "indeks kualitas ekosistem gambut (ikeg)": "kualitas_ekosistem_gambut",
    "indeks kualitas lahan (ikl)": "kualitas_lahan", "indeks kualitas tutupan lahan (iktl)": "kualitas_tutupan_lahan",
    "indeks kualitas udara": "kualitas_udara"}


def peta_rincian(x, ada: set):
    if x in ada:
        return x
    return RINCIAN_SILVER.get(str(x).strip().lower(), x)


# ---------------------------------------------------------------- deduplikasi
def cek_duplikat(s: pd.DataFrame) -> pd.DataFrame:
    """Aturan: kunci yang sama dari berkas/snapshot berbeda dengan nilai SAMA bukan duplikat yang salah
    (satu dipertahankan, lineage dicatat); nilai BEDA adalah revisi (keduanya dipertahankan, dibedakan
    oleh _berkas_raw, tidak dirata-rata)."""
    k = ["sumber", "seri_kode", "wilayah_kode", "periode", "rincian"]
    d = s[s.duplicated(k, keep=False)]
    if d.empty:
        return pd.DataFrame(columns=k + ["n_berkas", "n_nilai", "jenis"])
    g = d.groupby(k).agg(n_berkas=("_berkas_raw", "nunique"), n_nilai=("nilai", "nunique")).reset_index()
    g["jenis"] = np.where(g["n_nilai"] == 1, "sama (bukan duplikat salah)", "beda (revisi)")
    return g


# ---------------------------------------------------------------- usulan perbaikan galat input
def _w(s, seri, kolom="rincian"):
    x = s[(s["seri_kode"] == seri) & s["wilayah_kode"].isin(G.PROV38)]
    return x.pivot_table(index=["wilayah_kode", "tahun"], columns=kolom, values="nilai", aggfunc="first")


def _siklus(owner: dict) -> list:
    sisa, hasil = set(owner), []
    while sisa:
        a = next(iter(sisa))
        sik, x = [a], owner[a]
        while x != a and x in owner and x not in sik:
            sik.append(x)
            x = owner[x]
        if x == a:
            hasil.append(sik)
        sisa -= set(sik)
    return hasil


def usul_pertukaran(s: pd.DataFrame) -> list:
    """A1: blok hutan/non_hutan/persen berada di provinsi yang salah (total tetap di tempatnya)."""
    L, P = _w(s, LUAS), _w(s, PERSEN)
    usul = []
    for tahun in sorted(L.index.get_level_values("tahun").unique()):
        g = L.xs(tahun, level="tahun")
        p = P.xs(tahun, level="tahun") if tahun in P.index.get_level_values("tahun") else None
        if p is None or not {"hutan", "non_hutan", "total"} <= set(g.columns):
            continue
        hn = g["hutan"] + g["non_hutan"]
        salah = g[(hn - g["total"]).abs() > TOL_JUMLAH].index
        owner = {}
        for k in salah:
            cocok = [q for q in g.index if q != k and abs(g.at[q, "total"] - hn[k]) <= TOL_TOTAL]
            if len(cocok) == 1:
                owner[k] = cocok[0]
        if len(set(owner.values())) != len(owner):
            continue
        for sik in _siklus(owner):
            baru = {}                       # provinsi Q menerima blok dari baris P yang pemiliknya Q
            for pk in sik:
                q = owner[pk]
                baru[q] = {"hutan": g.at[pk, "hutan"], "non_hutan": g.at[pk, "non_hutan"],
                           "ph": p.at[pk, "hutan"], "pn": p.at[pk, "non_hutan"]}
            ok = True
            for q, b in baru.items():       # gerbang bukti
                ok &= abs(b["hutan"] + b["non_hutan"] - g.at[q, "total"]) <= TOL_JUMLAH
                ok &= abs(b["ph"] - b["hutan"] / g.at[q, "total"] * 100) <= TOL_PERSEN
                ok &= abs(b["ph"] + b["pn"] - 100) <= TOL_TOTAL
            if not ok:
                continue
            bukti = (f"hutan+non_hutan di baris asal sama dengan total {sik}-pemilik; dalam siklus {len(sik)} provinsi; "
                     "setelah dipindah jumlah rincian = total dan persen = luas/total; jumlah nasional tidak berubah")
            for q, b in baru.items():
                for seri, rinc, lama, nilai in [(LUAS, "hutan", g.at[q, "hutan"], b["hutan"]),
                                                (LUAS, "non_hutan", g.at[q, "non_hutan"], b["non_hutan"]),
                                                (PERSEN, "hutan", p.at[q, "hutan"], b["ph"]),
                                                (PERSEN, "non_hutan", p.at[q, "non_hutan"], b["pn"])]:
                    usul.append({"seri_kode": seri, "rincian": rinc, "wilayah_kode": q, "tahun": int(tahun),
                                 "nilai_asal": lama, "nilai_baru": nilai, "aturan": "A1_pertukaran_antarprovinsi",
                                 "bukti": bukti})
    return usul


def usul_geser_desimal_total(s: pd.DataFrame, sudah: set) -> list:
    """A2: total = 10x atau 0,1x jumlah komponen, sedangkan komponen sama dengan total biasa provinsi itu."""
    usul = []
    for seri, komp in [(LUAS, ["hutan", "non_hutan"]), (KAWASAN, ["kawasan_hutan", "apl"])]:
        w = _w(s, seri)
        if not set(komp + ["total"]) <= set(w.columns):
            continue
        jml = w[komp].sum(axis=1, min_count=len(komp))
        modal = w["total"].groupby(level="wilayah_kode").agg(lambda v: v.round(1).mode().iloc[0])
        for (k, t), tot in w["total"].items():
            if (seri, k, t) in sudah or pd.isna(jml[(k, t)]) or abs(jml[(k, t)] - tot) <= TOL_JUMLAH:
                continue
            r = tot / jml[(k, t)] if jml[(k, t)] else np.nan
            if (abs(r - 10) < 0.2 or abs(r - 0.1) < 0.01) and abs(jml[(k, t)] - modal[k]) <= TOL_TOTAL:
                usul.append({"seri_kode": seri, "rincian": "total", "wilayah_kode": k, "tahun": int(t),
                             "nilai_asal": tot, "nilai_baru": round(float(jml[(k, t)]), 1),
                             "aturan": "A2_geser_desimal_pada_total",
                             "bukti": f"total = {r:.1f} x jumlah komponen; jumlah komponen sama dengan total biasa provinsi ini ({modal[k]})"})
    return usul


def usul_persen_selisih(s: pd.DataFrame, sudah: set) -> list:
    """A3: persen hutan + non_hutan != 100; satu sisi cocok dengan luas/total, sisi lain diganti 100 - sisi cocok."""
    L, P = _w(s, LUAS), _w(s, PERSEN)
    if not ({"hutan", "non_hutan", "total"} <= set(L.columns) and {"hutan", "non_hutan"} <= set(P.columns)):
        return []
    x = L.join(P, rsuffix="_p", how="inner").dropna()
    usul = []
    for (k, t), r in x.iterrows():
        if (PERSEN, k, t) in sudah or abs(r["hutan_p"] + r["non_hutan_p"] - 100) <= TOL_TOTAL:
            continue
        ch, cn = r["hutan"] / r["total"] * 100, r["non_hutan"] / r["total"] * 100
        oh, on = abs(r["hutan_p"] - ch) <= TOL_TOTAL, abs(r["non_hutan_p"] - cn) <= TOL_TOTAL
        if oh != on:
            rinc, lama, baru = ("non_hutan", r["non_hutan_p"], round(100 - r["hutan_p"], 1)) if oh else \
                               ("hutan", r["hutan_p"], round(100 - r["non_hutan_p"], 1))
            if abs(baru - (cn if oh else ch)) <= TOL_TOTAL:
                usul.append({"seri_kode": PERSEN, "rincian": rinc, "wilayah_kode": k, "tahun": int(t),
                             "nilai_asal": lama, "nilai_baru": baru, "aturan": "A3_persen_tidak_berjumlah_100",
                             "bukti": f"persen hutan + non_hutan = {r['hutan_p'] + r['non_hutan_p']:.1f}; sisi lain cocok dengan luas/total; "
                                      f"nilai baru = 100 - sisi cocok = luas/total (selisih <= {TOL_TOTAL})"})
    return usul


def usulan(s: pd.DataFrame) -> pd.DataFrame:
    a1 = usul_pertukaran(s)
    sudah = {(u["seri_kode"], u["wilayah_kode"], u["tahun"]) for u in a1}
    sudah |= {(LUAS, u["wilayah_kode"], u["tahun"]) for u in a1}
    a2 = usul_geser_desimal_total(s, sudah)
    a3 = usul_persen_selisih(s, sudah)
    u = pd.DataFrame(a1 + a2 + a3, columns=["seri_kode", "rincian", "wilayah_kode", "tahun", "nilai_asal", "nilai_baru", "aturan", "bukti"])
    u["nama_wilayah"] = u["wilayah_kode"].map(G.PROV38)
    return u


def terapkan(s: pd.DataFrame, u: pd.DataFrame) -> pd.DataFrame:
    b = s.copy()
    b["nilai_asal"], b["perbaikan"] = np.nan, ""
    idx = b.set_index(["seri_kode", "rincian", "wilayah_kode", "tahun"]).index
    for r in u.itertuples(index=False):
        m = np.asarray(idx == (r.seri_kode, r.rincian, r.wilayah_kode, r.tahun))
        if m.sum() != 1:
            raise ValueError(f"sel perbaikan tidak unik/ada: {r}")
        b.loc[m, "nilai_asal"] = r.nilai_asal
        b.loc[m, "nilai"] = r.nilai_baru
        b.loc[m, "perbaikan"] = r.aturan
    return b


# ---------------------------------------------------------------- patahan serentak
def _ubah(s: pd.DataFrame) -> pd.DataFrame:
    x = s[s["wilayah_kode"].isin(G.PROV38)].sort_values(["seri_kode", "rincian", "wilayah_kode", "tahun"]).copy()
    g = x.groupby(["seri_kode", "rincian", "wilayah_kode"])
    x["v0"], x["t0"] = g["nilai"].shift(), g["tahun"].shift()
    x = x.dropna(subset=["v0"])
    x = x[x["v0"] != 0]
    x["ubah"] = (x["nilai"] - x["v0"]) / x["v0"].abs() * 100 / (x["tahun"] - x["t0"])
    return x


def patahan_serentak(s: pd.DataFrame) -> pd.DataFrame:
    baris = []
    for (seri, rinc), g in _ubah(s).groupby(["seri_kode", "rincian"]):
        skala = g["ubah"].abs().median()
        ambang = max(PANGKAT * skala, AMBANG_MIN)
        for t, h in g.groupby("tahun"):
            if len(h) < MIN_PROV:
                continue
            lewat = h[h["ubah"].abs() > ambang]
            share = len(lewat) / len(h)
            sign = max((lewat["ubah"] > 0).mean(), (lewat["ubah"] < 0).mean()) if len(lewat) else 0.0
            baris.append({"seri_kode": seri, "rincian": rinc, "periode": int(t), "n_provinsi": len(h),
                          "ambang_persen_per_tahun": round(ambang, 2), "share_melewati": round(share, 2),
                          "share_searah": round(sign, 2), "median_perubahan": round(h["ubah"].median(), 2),
                          "patahan": bool(share >= SHARE_MIN and sign >= SIGN_MIN)})
    return pd.DataFrame(baris)


# ---------------------------------------------------------------- klasifikasi
def _patahan_kaltara(sk, k, t, prev, jenis) -> bool:
    if k not in (6400, 6500):
        return False
    sampai = 2020 if sk.startswith("tabel:sdg15_tutupan_hutan") else (2018 if sk == KAWASAN else None)
    if sampai is None:
        return False
    if jenis == "antar_provinsi":
        return k == 6400 and t <= sampai
    return prev is not None and prev <= sampai < t


def klasifikasi(a: pd.DataFrame, s: pd.DataFrame, sb: pd.DataFrame, u: pd.DataFrame, ps: pd.DataFrame) -> pd.DataFrame:
    ada = set(s["rincian"])
    nama2kode = {v: k for k, v in G.PROV38.items()}
    a = a.copy()
    a["rincian_silver"] = [peta_rincian(r, ada) for r in a["rincian"]]
    a["wilayah_kode"] = a["wilayah"].str.strip().str.upper().map(nama2kode)
    a["periode"] = a["periode"].astype(int)
    perb = set(zip(u["seri_kode"], u["rincian"], u["wilayah_kode"], u["tahun"]))
    pat = set(map(tuple, ps[ps["patahan"]][["seri_kode", "rincian", "periode"]].itertuples(index=False)))
    ser = sb.sort_values("tahun").groupby(["seri_kode", "rincian", "wilayah_kode"])
    deret = {k: dict(zip(g["tahun"], g["nilai"])) for k, g in ser}
    aturan = u.groupby(["seri_kode", "rincian", "wilayah_kode", "tahun"])["aturan"].first().to_dict()
    hasil = []
    for r in a.itertuples(index=False):
        sk, rs, k, t = r.seri, r.rincian_silver, r.wilayah_kode, r.periode
        d = deret.get((sk, rs, k), {})
        th = sorted(d)
        prev = max([x for x in th if x < t], default=None)
        nxt = min([x for x in th if x > t], default=None)
        kat, sub, stat, bukti = None, "", "", ""
        if (sk, rs, k, t) in perb:
            kat, stat = "galat_input", "diperbaiki"
            sub, bukti = aturan[(sk, rs, k, t)], "lihat perbaikan_galat.csv"
        elif r.jenis == "loncatan" and prev is not None and (sk, rs, k, prev) in perb:
            kat, sub, stat = "galat_input", "akibat_galat_periode_sebelumnya", "ikut_terbenahi"
            bukti = f"nilai {prev} salah dan diperbaiki ({aturan[(sk, rs, k, prev)]})"
        elif _patahan_kaltara(sk, k, t, prev, r.jenis):
            kat, sub = "patahan", "cakupan_berubah_pemekaran_kaltara"
            bukti = "Kaltim 2014-2020 (tabel) / 2014-2018 (var1304) mencakup Kaltara; terpisah sesudahnya"
        elif r.jenis == "loncatan" and k in PEMEKARAN_PAPUA and t >= 2023 and prev is not None and prev <= 2022:
            kat, sub = "patahan", "cakupan_berubah_pemekaran_papua_2022"
            bukti = "provinsi induk Papua berubah cakupan setelah pemekaran 2022; provinsi baru baru muncul di 2023"
        elif r.jenis == "loncatan" and (sk, rs, t) in pat:
            kat, sub = "patahan", "serentak_banyak_provinsi"
            row = ps[(ps.seri_kode == sk) & (ps.rincian == rs) & (ps.periode == t)].iloc[0]
            bukti = f"{row.share_melewati:.0%} provinsi berubah melewati {row.ambang_persen_per_tahun}%/tahun, {row.share_searah:.0%} searah"
        else:
            v = d.get(t)
            lain = [d[x] for x in th if x != t]
            med = np.median(lain) if len(lain) >= 3 else np.nan
            rasio = v / med if (v is not None and pd.notna(med) and med != 0) else np.nan
            spike = (prev is not None and nxt is not None and d[prev] != d[t]
                     and abs(d[nxt] - d[prev]) <= 0.1 * abs(d[t] - d[prev]) and (d[t] - d[prev]) * (d[nxt] - d[t]) < 0)
            if pd.notna(rasio) and (9.5 <= abs(rasio) <= 10.5 or 0.095 <= abs(rasio) <= 0.105):
                kat, sub, stat = "galat_input", "dugaan_geser_desimal", "dugaan_tidak_diperbaiki"
                bukti = f"nilai = {rasio:.2f} x median periode lain provinsi ini; belum ada identitas independen untuk memastikan"
            elif spike:
                kat, sub, stat = "galat_input", "dugaan_lonjakan_sesaat", "dugaan_tidak_diperbaiki"
                bukti = f"naik/turun tajam pada {t} lalu kembali pada {nxt}; belum terbukti"
            else:
                kat = "outlier_asli"
                sub = {"antar_provinsi": "nilai_ekstrem_antar_provinsi", "loncatan": "perubahan_tajam_satu_provinsi"}[r.jenis]
                bukti = "tidak ada bukti galat input atau patahan; lolos uji identitas jumlah/persen yang tersedia"
        hasil.append((kat, sub, stat, bukti))
    a[["kategori", "subkategori", "status_galat", "bukti"]] = pd.DataFrame(hasil, index=a.index)
    return a


def ubah_setelah_perbaikan(a: pd.DataFrame, s: pd.DataFrame, sb: pd.DataFrame) -> pd.DataFrame:
    """Untuk loncatan yang ikut terbenahi: perubahan relatif sebelum dan sesudah perbaikan."""
    x = a[a["status_galat"].isin(["ikut_terbenahi", "diperbaiki"]) & (a["jenis"] == "loncatan")]
    def chg(df):
        c = _ubah(df).set_index(["seri_kode", "rincian", "wilayah_kode", "tahun"])["ubah"]
        return c
    c0, c1 = chg(s), chg(sb)
    k = list(zip(x["seri"], x["rincian_silver"], x["wilayah_kode"], x["periode"]))
    return pd.DataFrame({"seri_kode": x["seri"].to_numpy(), "rincian": x["rincian_silver"].to_numpy(),
                         "wilayah": x["wilayah"].to_numpy(), "periode": x["periode"].to_numpy(),
                         "ubah_persen_per_tahun_sebelum": [c0.get(i, np.nan) for i in k],
                         "ubah_persen_per_tahun_sesudah": [c1.get(i, np.nan) for i in k]})


# ---------------------------------------------------------------- laporan dan log
def tulis_laporan(ctx: dict):
    k = ctx["kls"]
    rk = pd.crosstab([k["seri"], k["jenis"]], k["kategori"]).reset_index()
    L = ["# Tahap 3: kategori calon anomali, perbaikan galat input, dan deduplikasi", "",
         "Sumber: `reports/tabel/calon_anomali.csv` (Tahap 2) dan `data/silver/silver.parquet`. Hanya galat input yang "
         "terbukti oleh identitas independen yang diperbaiki; outlier asli dan patahan ditandai dan dijelaskan.", "",
         "## Definisi kategori", "",
         "- **galat_input**: nilai salah karena proses input, dibuktikan oleh identitas (jumlah rincian = total, persen = luas/total, "
         "nilai milik provinsi lain, atau geser desimal). Status `diperbaiki` hanya bila lolos gerbang bukti; "
         "`dugaan_tidak_diperbaiki` bila hanya ada kecurigaan.",
         "- **patahan**: perubahan cakupan atau metode: pemekaran provinsi, atau lonjakan serentak "
         f"(≥{SHARE_MIN:.0%} provinsi melewati ambang pada tahun yang sama, ≥{SIGN_MIN:.0%} searah). Tidak diperbaiki.",
         "- **outlier_asli**: nilai ekstrem tanpa bukti galat atau patahan. Tidak diperbaiki.", "",
         "## Ringkasan", "", G.md(rk), "",
         f"Total calon anomali: {len(k)}; terpetakan ke Silver: {int(k['wilayah_kode'].notna().sum())}.", "",
         "## Perbaikan galat input", "",
         G.md(ctx["usul"].drop(columns=["bukti"])) if len(ctx["usul"]) else "_tidak ada_", "",
         "Bukti tiap aturan ada di `reports/tabel/perbaikan_galat.csv`.","Catatan hitungan: `perbaikan_galat.csv` memuat 103 sel (A1 100, A2 2, A3 1). Sembilan di antaranya (8 sel A1 dan 1 sel A3) tidak "
         "ada di daftar calon anomali Tahap 2: sel A1 tersebut ikut dipindah karena perbaikan A1 memindahkan satu blok provinsi utuh "
         "(luas dan persen) meski nilainya sendiri tidak cukup ekstrem untuk masuk profil, sedangkan sel A3 ditemukan lewat uji identitas "
         "persen. Sebaliknya, satu sel bisa muncul dua kali di daftar Tahap 2 (jenis antar_provinsi dan loncatan), sehingga jumlah baris "
         "berstatus `diperbaiki` (100) tidak sama dengan jumlah sel unik yang diperbaiki.", "", "",
         "## Uji identitas sebelum dan sesudah perbaikan", "", G.md(ctx["uji"]), "",
         "## Patahan serentak (hasil deteksi)", "",
         G.md(ctx["ps"][ctx["ps"]["patahan"]]) if ctx["ps"]["patahan"].any() else "_tidak ada tahun yang memenuhi kriteria serentak_", "",
         "Daftar semua tahun: `reports/tabel/patahan_serentak.csv`.", "",
         "## Deduplikasi", "",
         "- Kunci unik: sumber + seri + wilayah + periode + rincian (+ berkas).",
         "- Angka **sama** dari dua berkas/snapshot bukan duplikat yang salah: satu dipertahankan, lineage dicatat.",
         "- Angka **berbeda** adalah revisi: keduanya dipertahankan, dibedakan oleh `_berkas_raw`, tidak dirata-rata.",
         f"- Hasil pada Silver sekarang: {len(ctx['dup'])} kunci ganda.", ""]
    for kat in ["galat_input", "patahan", "outlier_asli"]:
        x = k[k["kategori"] == kat]
        L += [f"## Daftar {kat} ({len(x)})", "",
              G.md(x[["seri", "rincian_silver", "wilayah", "periode", "jenis", "subkategori", "status_galat"]].head(60)), "",
              "Daftar lengkap: `reports/tabel/anomali_berkategori.csv`.", ""]
    OUT_LAPORAN.write_text("\n".join(L), encoding="utf-8")


def catat_log(ctx: dict):
    ada, ada_teks = set(), set()
    if G.LOG.exists():
        with open(G.LOG, encoding="utf-8-sig", newline="") as f:
            rd = list(csv.DictReader(f))
        ada = {r["id"] for r in rd}
        ada_teks = {(r["tahap"], r["seri_kode"], r["keputusan"]) for r in rd}
    n = max([int(i.split("-")[1]) for i in ada if i.startswith("K-") and i.split("-")[1].isdigit()], default=0)
    u, k = ctx["usul"], ctx["kls"]
    c = k["kategori"].value_counts().to_dict()
    na = lambda a: int((u["aturan"] == a).sum())
    E = [
        ("semua BPS", "Deduplikasi: kunci sumber+seri+wilayah+periode+rincian; angka sama dari dua berkas bukan duplikat yang salah, angka beda adalah revisi",
         "menghapus semua baris kembar; merata-ratakan angka beda", "angka sama tidak membawa informasi baru tetapi lineage dijaga; angka beda adalah informasi revisi yang tidak boleh hilang", len(ctx["dup"])),
        ("semua BPS", "Calon anomali dikategorikan: galat_input, patahan (pemekaran atau serentak), outlier_asli; hanya galat input yang terbukti identitas independen yang diperbaiki",
         "memperbaiki atau menghapus semua outlier", "outlier asli dan patahan adalah informasi nyata; mengubahnya menghilangkan sinyal", len(k)),
        ("tabel:sdg15_tutupan_hutan:*", "A1: blok hutan/non_hutan/persen 2020 yang berada di provinsi salah dikembalikan ke pemiliknya (provinsi dengan total yang sama dengan hutan+non_hutan); nilai asal disimpan di nilai_asal",
         "membiarkan atau menghapus nilai 2020", "terbukti: siklus tertutup, jumlah rincian = total, persen = luas/total, jumlah nasional tidak berubah", na("A1_pertukaran_antarprovinsi")),
        ("tabel hutan, var1304", "A2: total yang 10x jumlah komponen (DI Yogyakarta 2016) dikoreksi menjadi jumlah komponen",
         "menghapus nilai", "komponen sama dengan total biasa provinsi ini dan persen hutan cocok", na("A2_geser_desimal_pada_total")),
        ("tabel:sdg15_tutupan_hutan:persen", "A3: persen yang membuat hutan+non_hutan != 100 dikoreksi bila sisi lain cocok dengan luas/total",
         "membiarkan", "dua perhitungan independen menghasilkan nilai yang sama", na("A3_persen_tidak_berjumlah_100")),
        ("semua BPS", "Patahan ditandai tanpa perbaikan: cakupan Kaltim-Kaltara, pemekaran Papua 2022, dan lonjakan serentak bila ada",
         "menyetel ulang deret agar mulus", "perubahan cakupan atau metode nyata; deret perlu dibaca sebagai dua segmen", c.get("patahan", 0)),
        ("semua BPS", "Dugaan galat tanpa bukti identitas (geser desimal atau lonjakan sesaat) ditandai, tidak diperbaiki",
         "memperbaiki dengan interpolasi", "tanpa bukti independen perbaikan berarti mengarang data", int((k["status_galat"] == "dugaan_tidak_diperbaiki").sum())),
        ("tabel:sdg15_tutupan_hutan:luas_ribu_ha", "Sisa satu pelanggaran jumlah rincian (Bali 2018: hutan+non_hutan 567,2 vs total 566,9, selisih 0,3) dibiarkan, dicatat sebagai dugaan pembulatan",
         "mengubah salah satu komponen atau total agar jumlahnya cocok", "selisih hanya sedikit di atas toleransi 0,25 dan tidak ada identitas independen yang menunjukkan komponen mana yang salah; mengubahnya berarti mengarang data", 1),
    ]
    t = date.today().isoformat()
    baru = []
    for seri, kep, alt, alasan, dampak in E:
        if ("silver", seri, kep) in ada_teks:
            continue
        n += 1
        baru.append([f"K-{n:03d}", t, G.NIM, "silver", seri, kep, alt, alasan, int(dampak)])
    if not baru:
        print("log-keputusan.csv: tidak ada entri baru (semua sudah tercatat)")
        return
    akhir = G.LOG.exists() and not G.LOG.read_bytes().endswith(b"\n")
    with open(G.LOG, "a", encoding="utf-8", newline="") as f:
        if akhir:
            f.write("\n")
        csv.writer(f, lineterminator="\n").writerows(baru)
    print("log-keputusan.csv: +", len(baru), "entri")


def uji_identitas(s: pd.DataFrame, sb: pd.DataFrame) -> pd.DataFrame:
    baris = []
    for nama, d in [("sebelum", s), ("sesudah", sb)]:
        d = G.seragamkan(d.drop(columns=["nilai_seragam", "satuan_seragam"], errors="ignore"))
        lg, rk = G.uji_jumlah(d)
        for r in rk.itertuples(index=False):
            baris.append({"tahap": nama, "uji": f"jumlah rincian: {r.seri_kode}", "melanggar": r.melanggar})
        baris.append({"tahap": nama, "uji": "persen vs luas/total", "melanggar": len(G.uji_persen_luas(d))})
        baris.append({"tahap": nama, "uji": "jumlah provinsi vs Indonesia (>0,5%)", "melanggar": len(G.uji_nasional(d))})
    t = pd.DataFrame(baris)
    return t.pivot_table(index="uji", columns="tahap", values="melanggar", aggfunc="first").reset_index()[["uji", "sebelum", "sesudah"]]


def main():
    OUT_TABEL.mkdir(parents=True, exist_ok=True)
    s = G.muat()
    a = pd.read_csv(ANOMALI)
    u = usulan(s)
    sb = terapkan(s, u)
    ps = patahan_serentak(sb)
    kls = klasifikasi(a, s, sb, u, ps)
    tak = kls[kls["wilayah_kode"].isna()]
    dup = cek_duplikat(s)
    ctx = {"usul": u, "kls": kls, "ps": ps, "dup": dup, "uji": uji_identitas(s, sb)}
    u.to_csv(OUT_TABEL / "perbaikan_galat.csv", index=False)
    kls.to_csv(OUT_TABEL / "anomali_berkategori.csv", index=False)
    ps.to_csv(OUT_TABEL / "patahan_serentak.csv", index=False)
    ubah_setelah_perbaikan(kls, s, sb).to_csv(OUT_TABEL / "loncatan_sebelum_sesudah_perbaikan.csv", index=False)
    tulis_laporan(ctx)
    print("calon anomali:", len(a), "| tak terpetakan ke provinsi Silver:", len(tak), "| kunci ganda di Silver:", len(dup))
    print(pd.crosstab(kls["kategori"], kls["status_galat"].replace("", "-")).to_string())
    print(kls.groupby(["kategori", "subkategori"]).size().to_string())
    print("perbaikan:", u["aturan"].value_counts().to_dict())
    print(ctx["uji"].to_string(index=False))
    print("tahun patahan serentak:", ps[ps["patahan"]][["seri_kode", "rincian", "periode", "share_melewati"]].to_string(index=False)
          if ps["patahan"].any() else "tidak ada")
    if "--terapkan" in sys.argv:
        sb.to_parquet(OUT_BERSIH, index=False)
        print("ditulis:", OUT_BERSIH, "|", int((sb["perbaikan"] != "").sum()), "sel diperbaiki")
    else:
        print("(simulasi: silver_bersih.parquet belum ditulis; tambah --terapkan)")
    if "--catat-log" in sys.argv:
        catat_log(ctx)


if __name__ == "__main__":
    main()