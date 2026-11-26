"""Tahap 3: grid provinsi x periode, kelengkapan panel, penyeragaman satuan, uji jumlah.
    python -m src.analisis.grid
    python -m src.analisis.grid --catat-log
"""
import csv
import json
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

SILVER = Path("data/silver/silver.parquet")
RAW_BPS = Path("data/raw/bps")
OUT_TABEL = Path("reports/tabel")
OUT_LAPORAN = Path("reports/kelengkapan_panel.md")
LOG = Path("log-keputusan.csv")
NIM = "124450122"
NASIONAL = 9999

# Susunan 38 provinsi tahun 2025 (kode BPS x 100).
PROV38 = {
    1100: "ACEH", 1200: "SUMATERA UTARA", 1300: "SUMATERA BARAT", 1400: "RIAU", 1500: "JAMBI",
    1600: "SUMATERA SELATAN", 1700: "BENGKULU", 1800: "LAMPUNG", 1900: "KEP. BANGKA BELITUNG",
    2100: "KEP. RIAU", 3100: "DKI JAKARTA", 3200: "JAWA BARAT", 3300: "JAWA TENGAH",
    3400: "DI YOGYAKARTA", 3500: "JAWA TIMUR", 3600: "BANTEN", 5100: "BALI",
    5200: "NUSA TENGGARA BARAT", 5300: "NUSA TENGGARA TIMUR", 6100: "KALIMANTAN BARAT",
    6200: "KALIMANTAN TENGAH", 6300: "KALIMANTAN SELATAN", 6400: "KALIMANTAN TIMUR",
    6500: "KALIMANTAN UTARA", 7100: "SULAWESI UTARA", 7200: "SULAWESI TENGAH",
    7300: "SULAWESI SELATAN", 7400: "SULAWESI TENGGARA", 7500: "GORONTALO", 7600: "SULAWESI BARAT",
    8100: "MALUKU", 8200: "MALUKU UTARA", 9100: "PAPUA BARAT", 9200: "PAPUA BARAT DAYA",
    9400: "PAPUA", 9500: "PAPUA SELATAN", 9600: "PAPUA TENGAH", 9700: "PAPUA PEGUNUNGAN"}

# ---- aturan pemetaan/pemekaran (USULAN; harus dikonfirmasi dan dicatat di log-keputusan.csv) ----
# Tahun pertama BPS menyajikan provinsi dengan susunan barunya; periode sebelumnya = belum_ada (bukan missing).
# Papua Barat Daya/Selatan/Tengah/Pegunungan: dibentuk 2022, tetapi di semua seri observasi pertamanya 2023
# (data 2022 masih memakai susunan lama). Kalimantan Utara: dibentuk 2012.
BERDIRI = {9200: 2023, 9500: 2023, 9600: 2023, 9700: 2023, 6500: 2012}
# Kaltara tidak punya observasi pada periode ini karena datanya masih tergabung di Kaltim:
# (kode, awalan seri, sampai tahun, dasar)
DIGABUNG = [
    (6500, "tabel:sdg15_tutupan_hutan:", 2020, "kolom catatan sumber: gabungan Kaltim dan Kaltara"),
    (6500, "var1304", 2018, "jumlah 33 provinsi sama dengan baris Indonesia pada 2014-2018 (selisih 2016 = galat DI Yogyakarta)"),
]

# Faktor ke ribu hektar. Nilai asli tetap disimpan; kolom nilai_seragam ditambahkan.
FAKTOR_LUAS = {"hektar": 0.001, "ribu_hektar": 1.0}

# (seri, rincian total atau angka total, komponen, toleransi pembulatan)
ATURAN_JUMLAH = [
    ("tabel:sdg15_tutupan_hutan:luas_ribu_ha", "total", ["hutan", "non_hutan"], 0.25),
    ("tabel:sdg15_tutupan_hutan:persen", 100.0, ["hutan", "non_hutan"], 0.15),
    ("var1304", "total", ["kawasan_hutan", "apl"], 0.2),
    ("var588", "total", ["kritis", "sangat_kritis"], 0.003),
]

SDG_KATALOG = {"tabel:sdg15_tutupan_hutan:luas_ribu_ha": "15.1.1", "tabel:sdg15_tutupan_hutan:persen": "15.1.1",
               "var1304": "15.3.1", "var588": "15.3.1", "var2532": "11.6.2"}


# ---------------------------------------------------------------- grid
def muat() -> pd.DataFrame:
    s = pd.read_parquet(SILVER)
    s["tahun"] = s["periode"].astype(int)
    return s


def seragamkan(s: pd.DataFrame) -> pd.DataFrame:
    s = s.copy()
    f = s["satuan"].map(FAKTOR_LUAS)
    s["nilai_seragam"] = np.where(f.notna(), s["nilai"] * f.fillna(1.0), s["nilai"])
    s["satuan_seragam"] = s["satuan"].replace({"hektar": "ribu_hektar"})
    return s


def pisah(s: pd.DataFrame):
    nas = s[s["wilayah_kode"] == NASIONAL]
    prov = s[s["wilayah_kode"].isin(PROV38)]
    lain = s[~s["wilayah_kode"].isin(PROV38) & (s["wilayah_kode"] != NASIONAL)]
    return nas, prov, lain


def _kategori(seri, kode, tahun, ada, terisi) -> str:
    if terisi:
        return "terisi"
    if kode not in ada:
        return "di_luar_cakupan"
    if kode in BERDIRI and tahun < BERDIRI[kode]:
        return "belum_ada"
    if any(kode == k and seri.startswith(aw) and tahun <= sd for k, aw, sd, _ in DIGABUNG):
        return "digabung_induk"
    return "missing"


def bentuk_grid(prov: pd.DataFrame) -> pd.DataFrame:
    """Per seri x rincian: 38 provinsi x periode yang terbit untuk seri x rincian itu."""
    bagian = []
    for (seri, rincian), g in prov.groupby(["seri_kode", "rincian"]):
        periode = sorted(g["tahun"].unique())
        idx = pd.MultiIndex.from_product([sorted(PROV38), periode], names=["wilayah_kode", "tahun"])
        w = g.set_index(["wilayah_kode", "tahun"])
        if w.index.duplicated().any():
            raise ValueError(f"baris kembar pada {seri} / {rincian}")
        t = w[["nilai", "nilai_seragam"]].reindex(idx).reset_index()
        ada = set(g["wilayah_kode"])
        t["kategori"] = [_kategori(seri, k, y, ada, pd.notna(v))
                         for k, y, v in zip(t["wilayah_kode"], t["tahun"], t["nilai"])]
        t.insert(0, "rincian", rincian)
        t.insert(0, "seri_kode", seri)
        t.insert(3, "nama_wilayah", t["wilayah_kode"].map(PROV38))
        bagian.append(t)
    return pd.concat(bagian, ignore_index=True)


def kelengkapan(grid: pd.DataFrame) -> pd.DataFrame:
    k = pd.crosstab([grid["seri_kode"], grid["rincian"], grid["tahun"]], grid["kategori"])
    for c in ["terisi", "di_luar_cakupan", "belum_ada", "digabung_induk", "missing"]:
        if c not in k.columns:
            k[c] = 0
    k["sel"] = k[["terisi", "di_luar_cakupan", "belum_ada", "digabung_induk", "missing"]].sum(axis=1)
    k["persen_terisi_semua_sel"] = k["terisi"] / k["sel"] * 100
    berlaku = k["sel"] - k["di_luar_cakupan"] - k["belum_ada"] - k["digabung_induk"]
    k["persen_terisi_sel_berlaku"] = k["terisi"] / berlaku.replace(0, np.nan) * 100
    return k.reset_index()


def periode_tak_terbit_di_rincian(prov: pd.DataFrame) -> pd.DataFrame:
    """Periode yang terbit untuk seri tetapi tidak untuk sebuah rincian (bukan missing, dicatat saja)."""
    baris = []
    for seri, g in prov.groupby("seri_kode"):
        semua = set(g["tahun"])
        for r, h in g.groupby("rincian"):
            beda = sorted(semua - set(h["tahun"]))
            if beda:
                baris.append({"seri_kode": seri, "rincian": r, "periode_tak_terbit": ", ".join(map(str, beda))})
    return pd.DataFrame(baris, columns=["seri_kode", "rincian", "periode_tak_terbit"])


def di_luar_cakupan(grid: pd.DataFrame) -> pd.DataFrame:
    x = grid[grid["kategori"] == "di_luar_cakupan"]
    return (x.groupby(["seri_kode", "rincian"])["nama_wilayah"]
             .agg(n_provinsi="nunique", provinsi=lambda s: ", ".join(sorted(set(s)))).reset_index())


# ---------------------------------------------------------------- uji
def uji_jumlah(s: pd.DataFrame):
    """Jumlah rincian harus sama dengan rincian jumlah (atau 100 untuk persen)."""
    langgar, ringkas = [], []
    for seri, total, komp, tol in ATURAN_JUMLAH:
        x = s[s["seri_kode"] == seri]
        if x.empty:
            continue
        w = x.pivot_table(index=["wilayah_kode", "nama_wilayah", "tahun"], columns="rincian",
                          values="nilai_seragam", aggfunc="first")
        if any(c not in w.columns for c in komp + ([total] if isinstance(total, str) else [])):
            ringkas.append({"seri_kode": seri, "diuji": 0, "melanggar": 0, "toleransi": tol,
                            "catatan": "nama rincian tidak ditemukan"})
            continue
        hit = w[komp].sum(axis=1, min_count=len(komp))
        ref = w[total] if isinstance(total, str) else pd.Series(total, index=w.index)
        d = (hit - ref).dropna()
        bad = d[d.abs() > tol]
        ringkas.append({"seri_kode": seri, "diuji": len(d), "melanggar": len(bad), "toleransi": tol, "catatan": ""})
        t = bad.rename("selisih").reset_index()
        t["seri_kode"] = seri
        t["jumlah_rincian"] = hit.reindex(bad.index).to_numpy()
        t["rincian_jumlah"] = ref.reindex(bad.index).to_numpy()
        langgar.append(t)
    kol = ["seri_kode", "wilayah_kode", "nama_wilayah", "tahun", "jumlah_rincian", "rincian_jumlah", "selisih"]
    L = pd.concat(langgar, ignore_index=True)[kol] if langgar else pd.DataFrame(columns=kol)
    return L, pd.DataFrame(ringkas)


def uji_persen_luas(s: pd.DataFrame, tol=0.2) -> pd.DataFrame:
    """Persen hutan/non_hutan harus sama dengan luas hutan/non_hutan dibagi total x 100."""
    luas = s[s["seri_kode"] == "tabel:sdg15_tutupan_hutan:luas_ribu_ha"].pivot_table(
        index=["wilayah_kode", "nama_wilayah", "tahun"], columns="rincian", values="nilai", aggfunc="first")
    per = s[s["seri_kode"] == "tabel:sdg15_tutupan_hutan:persen"].pivot_table(
        index=["wilayah_kode", "nama_wilayah", "tahun"], columns="rincian", values="nilai", aggfunc="first")
    x = luas.join(per, rsuffix="_persen", how="inner")
    baris = []
    for r in ["hutan", "non_hutan"]:
        if r in x.columns and f"{r}_persen" in x.columns and "total" in x.columns:
            hit = x[r] / x["total"] * 100
            d = (x[f"{r}_persen"] - hit).dropna()
            b = d[d.abs() > tol].rename("selisih_persen_poin").reset_index()
            b["rincian"] = r
            b["persen_sumber"] = x[f"{r}_persen"].reindex(d[d.abs() > tol].index).to_numpy()
            b["persen_dari_luas"] = hit.reindex(d[d.abs() > tol].index).to_numpy()
            baris.append(b)
    kol = ["wilayah_kode", "nama_wilayah", "tahun", "rincian", "persen_sumber", "persen_dari_luas", "selisih_persen_poin"]
    return pd.concat(baris, ignore_index=True)[kol] if baris else pd.DataFrame(columns=kol)


def analisis_tertukar(langgar: pd.DataFrame, s: pd.DataFrame) -> pd.DataFrame:
    """Untuk pelanggaran tabel luas: jenis dugaan dan provinsi pemilik `total` yang sama dengan hutan + non_hutan."""
    seri = "tabel:sdg15_tutupan_hutan:luas_ribu_ha"
    x = langgar[langgar["seri_kode"] == seri].copy()
    tot = s[(s["seri_kode"] == seri) & (s["rincian"] == "total") & (s["wilayah_kode"].isin(PROV38))]
    modal = tot.groupby("wilayah_kode")["nilai"].agg(lambda v: v.round(1).mode().iloc[0])
    baris = []
    for r in x.itertuples(index=False):
        sama = tot[(tot["tahun"] == r.tahun) & ((tot["nilai"] - r.jumlah_rincian).abs() < 0.15)]["nama_wilayah"].tolist()
        rasio = r.rincian_jumlah / r.jumlah_rincian if r.jumlah_rincian else np.nan
        if abs(r.selisih) < 1:
            jenis = "selisih_kecil (pembulatan?)"
        elif sama and sama != [r.nama_wilayah]:
            jenis = "tertukar_antarprovinsi"
        elif abs(rasio - 10) < 0.05 or abs(rasio - 0.1) < 0.005:
            jenis = "geser_desimal_pada_total"
        else:
            jenis = "tidak_cocok"
        baris.append({"wilayah_kode": r.wilayah_kode, "nama_wilayah": r.nama_wilayah, "tahun": r.tahun,
                      "hutan_plus_non_hutan": round(r.jumlah_rincian, 1), "total_di_baris": r.rincian_jumlah,
                      "total_biasa_provinsi_ini": modal.get(r.wilayah_kode),
                      "total_di_baris_sama_dgn_biasa": bool(abs(r.rincian_jumlah - modal.get(r.wilayah_kode, np.nan)) < 0.15),
                      "hutan_plus_non_hutan_sama_dgn_total_milik": ", ".join(sama) if sama else "",
                      "jenis_dugaan": jenis})
    return pd.DataFrame(baris)


def uji_nasional(s: pd.DataFrame, batas_persen=0.5) -> pd.DataFrame:
    """Jumlah 38 provinsi vs baris Indonesia pada seri luas (ribu hektar)."""
    luas = s[s["satuan_seragam"] == "ribu_hektar"]
    kunci = ["seri_kode", "rincian", "tahun"]
    nas = luas[luas["wilayah_kode"] == NASIONAL].set_index(kunci)["nilai_seragam"].rename("nasional")
    prov = (luas[luas["wilayah_kode"].isin(PROV38)].groupby(kunci)["nilai_seragam"]
            .agg(jumlah_provinsi="sum", n_provinsi="count"))
    t = prov.join(nas, how="inner")
    t["selisih"] = t["jumlah_provinsi"] - t["nasional"]
    t["selisih_persen"] = t["selisih"] / t["nasional"].abs() * 100
    return t[t["selisih_persen"].abs() > batas_persen].reset_index()


def katalog(s: pd.DataFrame) -> pd.DataFrame:
    meta = {}
    for f in sorted(RAW_BPS.glob("*/manifest_asal.json")):
        with open(f, encoding="utf-8") as h:
            meta.update({k: v for k, v in json.load(h)["tabel"].items() if k.startswith("sdg15")})
    baris = []
    for (seri, berkas), g in s.groupby(["seri_kode", "_berkas_raw"]):
        stem = Path(berkas).stem
        m = meta.get(stem, {})
        if not m:
            cocok = "manifest_asal.json tidak memuat berkas ini"
        elif seri.startswith("var"):
            cocok = "cocok" if m.get("var") == int(seri[3:]) else "TIDAK COCOK"
        else:
            cocok = "tabel statis (tanpa var)"
        baris.append({"seri_kode": seri, "berkas": stem, "judul_berkas": m.get("judul", ""),
                      "var_di_manifest": m.get("var", ""), "kecocokan_kode": cocok,
                      "satuan_silver": ", ".join(sorted(g["satuan"].unique())),
                      "kode_sdg_katalog": SDG_KATALOG.get(seri, ""),
                      "rincian": " | ".join(sorted(g["rincian"].unique()))})
    return pd.DataFrame(baris)


def sdg_var2532(s: pd.DataFrame) -> pd.DataFrame:
    """Usulan kode SDG per komponen IKLH; perlu konfirmasi dosen."""
    r = sorted(s.loc[s["seri_kode"] == "var2532", "rincian"].unique())
    baris = []
    for x in r:
        if "udara" in x.lower():
            baris.append({"rincian": x, "kode_sdg_usulan": "11.6.2",
                          "status": "sesuai katalog; hanya komponen udara yang berkaitan dengan 11.6.2"})
        else:
            baris.append({"rincian": x, "kode_sdg_usulan": "(bukan 11.6.2)",
                          "status": "perlu konfirmasi dosen; berkas bernama sdg15, kandidat target 15.x"})
    return pd.DataFrame(baris)


# ---------------------------------------------------------------- laporan
def _fmt(v) -> str:
    if pd.isna(v):
        return ""
    if isinstance(v, (float, np.floating)):
        return f"{v:.1f}"
    return str(v).replace("|", "\\|")


def md(df: pd.DataFrame) -> str:
    kol = [str(c) for c in df.columns]
    baris = ["| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)]
    for r in df.astype(object).itertuples(index=False):
        baris.append("| " + " | ".join(_fmt(v) for v in r) + " |")
    return "\n".join(baris)


def pivot_persen(kel: pd.DataFrame, seri: str, kolom: str) -> pd.DataFrame:
    x = kel[kel["seri_kode"] == seri]
    return x.pivot(index="rincian", columns="tahun", values=kolom).reset_index()


def tulis_laporan(ctx: dict):
    L = ["# Tahap 3: grid provinsi × periode dan kelengkapan panel", "",
         "Sumber: `data/silver/silver.parquet` (BPS, CSV). Tidak ada nilai yang diisi atau diperbaiki; "
         "sel kosong hanya dihitung dan diberi kategori.", "",
         "## Ringkasan", "",
         f"- Baris Silver: **{ctx['n_silver']}** ({ctx['n_prov']} provinsi, {ctx['n_nas']} baris Indonesia dipisahkan, "
         f"{ctx['n_lain']} baris kode wilayah tak dikenal).",
         f"- Sel grid (38 provinsi × periode terbit per seri × rincian): **{ctx['n_sel']}**; terisi {ctx['n_terisi']}.",
         f"- **sel_kosong_grid = {ctx['n_kosong']}**: " + ", ".join(f"{k} {v}" for k, v in ctx["kat"].items() if k != "terisi") + ".", "",
         "## Aturan grid", "",
         "- Periode grid = periode yang benar-benar terbit untuk tiap seri × rincian. Tahun yang tidak terbit "
         "(mis. `var1304` 2019–2022, `var588` di luar 4 tahunnya) bukan missing.",
         "- `di_luar_cakupan`: provinsi tanpa satu pun observasi pada seri × rincian itu (bukan sel yang hilang).",
         "- `belum_ada`: periode sebelum tahun pertama provinsi pemekaran muncul di data: Papua Barat Daya, Selatan, Tengah, "
         "Pegunungan sebelum 2023 (dibentuk 2022, data 2022 masih susunan lama); Kalimantan Utara sebelum 2012.",
         "- `digabung_induk`: Kalimantan Utara tanpa observasi karena tergabung di Kalimantan Timur: tabel tutupan hutan 2014–2020 "
         "(dasar: kolom `catatan` sumber) dan `var1304` 2014–2018 (dasar: jumlah 33 provinsi = baris Indonesia).",
         "- `missing`: sisanya. Hanya ini yang dihitung sebagai celah sebenarnya.", ""]
    for seri in sorted(ctx["kel"]["seri_kode"].unique()):
        L += [f"## {seri}", "", "Persen sel terisi per tahun, semua sel (38 provinsi):", "",
              md(pivot_persen(ctx["kel"], seri, "persen_terisi_semua_sel")), "",
              "Persen sel terisi per tahun, hanya sel yang berlaku (tanpa di_luar_cakupan, belum_ada, digabung_induk):", "",
              md(pivot_persen(ctx["kel"], seri, "persen_terisi_sel_berlaku")), ""]
    L += ["## Provinsi di luar cakupan seri × rincian", "", md(ctx["luar"]) if len(ctx["luar"]) else "_tidak ada_", "",
          "## Periode terbit untuk seri tetapi tidak untuk rincian tertentu", "",
          md(ctx["tak_terbit"]) if len(ctx["tak_terbit"]) else "_tidak ada_", "",
          "## Uji jumlah rincian = rincian jumlah (setelah penyeragaman satuan ke ribu hektar)", "",
          md(ctx["ringkas"]), "",
          f"Pelanggaran: {len(ctx['langgar'])} baris (ditandai, tidak diperbaiki). Daftar: `reports/tabel/uji_jumlah_pelanggaran.csv`.", "",
          md(ctx["langgar"].head(40)) if len(ctx["langgar"]) else "", "",
          "## Dugaan penyebab pelanggaran pada tabel luas", "",
          md(ctx["tertukar"]) if len(ctx["tertukar"]) else "", "",
          "## Uji persen vs luas / total (tabel tutupan hutan)", "",
          md(ctx["persen_luas"]) if len(ctx["persen_luas"]) else "_tidak ada selisih_", "",
          "## Uji jumlah 38 provinsi vs baris Indonesia (seri luas, selisih > 0,5%)", "",
          md(ctx["nasional"].head(40)) if len(ctx["nasional"]) else "_tidak ada selisih di atas ambang_", "",
          "## Kecocokan seri_kode dengan judul berkas", "", md(ctx["katalog"]), "",
          "## Usulan kode SDG komponen var2532 (IKLH)", "",
          "Judul berkas: komponen penyusun Indeks Kualitas Lingkungan Hidup, bukan konsentrasi PM2.5. "
          "Kode 11.6.2 di katalog hanya masuk akal untuk komponen udara.", "", md(ctx["sdg"]), ""]
    OUT_LAPORAN.write_text("\n".join(L), encoding="utf-8")


# ---------------------------------------------------------------- log
def catat_log(ctx: dict):
    ada = set()
    if LOG.exists():
        with open(LOG, encoding="utf-8-sig", newline="") as f:
            ada = {r["id"] for r in csv.DictReader(f)}
    nomor = [int(i.split("-")[1]) for i in ada if i.startswith("K-") and i.split("-")[1].isdigit()]
    n = max(nomor, default=0)
    kat, t = ctx["kat"], date.today().isoformat()
    E = [
        ("semua BPS", "Silver hanya dari CSV BPS; JSON tidak dimuat",
         "memuat CSV dan JSON sekaligus", "JSON adalah salinan data yang sama; kunci unik mencakup berkas sehingga baris ganda lolos dan terhitung dua kali", ctx["n_silver"]),
        ("tabel:sdg15_tutupan_hutan:*", "Baris bernilai kosong (Kalimantan Utara 2014-2020) tidak masuk Silver dan tidak diisi",
         "mengisi 0, atau menyalin nilai Kalimantan Timur", "skema Silver menolak nilai kosong; mengisi berarti mengarang data", kat.get("digabung_induk", 0)),
        ("var2532", "Satuan kosong di berkas mentah ditulis 'tidak_ada'",
         "membiarkan kosong", "skema Silver melarang sel kosong selain nilai; katalog kasus mencatat 'tidak_ada'", ctx["n_var2532"]),
        ("semua BPS", "Grid = 38 provinsi x periode yang terbit per seri x rincian",
         "grid kalender penuh (semua tahun dalam rentang seri)", "tahun yang tidak terbit untuk seri bukan missing", ctx["n_sel"]),
        ("semua BPS", "Provinsi tanpa satu observasi pun pada seri x rincian dikategorikan di_luar_cakupan, bukan missing",
         "menghitungnya sebagai missing", "bukan sel yang hilang tetapi provinsi yang tidak tercakup seri (mis. gambut, lahan kritis pra-pemekaran)", kat.get("di_luar_cakupan", 0)),
        ("semua BPS", "Sel sebelum tahun pertama observasi provinsi pemekaran dikategorikan belum_ada: Papua Barat Daya/Selatan/Tengah/Pegunungan sebelum 2023, Kalimantan Utara sebelum 2012",
         "mengalokasikan ulang dari provinsi induk; menganggap 2022 sebagai missing", "tidak ada dasar pembagian; di semua seri provinsi baru Papua baru muncul 2023 (data 2022 masih susunan lama)", kat.get("belum_ada", 0)),
        ("tabel hutan, var1304", "Kalimantan Utara dikategorikan digabung_induk (tabel hutan 2014-2020, var1304 2014-2018) dan tidak dialokasikan",
         "memisahkan dari Kalimantan Timur", "kolom catatan sumber menandai Kaltim sebagai gabungan; pada var1304 jumlah 33 provinsi sama dengan baris Indonesia; pemisahan butuh data tambahan", kat.get("digabung_induk", 0)),
        ("var588, var2532", "Sel missing sebenarnya dibiarkan kosong pada Tahap 3 (Kep. Riau var588 2006; Kaltara IKTL 2019; Papua Tengah IKAL 2023)",
         "imputasi pada tahap ini", "baru 5 sel dan tiap sel punya kemungkinan sebab berbeda; strategi imputasi diputuskan di pembersihan lanjutan", kat.get("missing", 0)),
        ("var588", "Satuan hektar sudah diseragamkan ke ribu hektar di Silver (diverifikasi: nilai Silver = nilai mentah / 1000)",
         "membiarkan hektar", "satuan luas harus seragam antarseri sebelum diuji dan digabung", ctx["n_var588"]),
        ("tabel hutan, var1304, var588", "Pelanggaran jumlah rincian vs rincian jumlah hanya ditandai, tidak diperbaiki",
         "memperbaiki otomatis dari jumlah", "blok hutan/non_hutan/persen 2020 bergeser antarprovinsi sementara total tetap, dan jumlah nasional tidak berubah; DI Yogyakarta 2016 geser desimal pada total; perbaikan ditunda ke penanganan outlier", len(ctx["langgar"])),
        ("var2532", "Kode SDG 11.6.2 hanya untuk komponen udara; komponen lain menunggu konfirmasi (kandidat 15.x)",
         "memakai 11.6.2 untuk seluruh seri", "judul berkas adalah komponen IKLH, bukan PM2.5", ctx["n_var2532"]),
        ("semua BPS", "Baris Indonesia (kode 9999) dipisahkan dari baris provinsi",
         "membiarkan di panel provinsi", "agregat nasional bukan provinsi; dipakai untuk uji jumlah", ctx["n_nas"]),
    ]
    baru = []
    for seri, kep, alt, alasan, dampak in E:
        n += 1
        baru.append([f"K-{n:03d}", t, NIM, "silver", seri, kep, alt, alasan, int(dampak)])
    kosong_akhir = LOG.exists() and not LOG.read_bytes().endswith(b"\n")
    with open(LOG, "a", encoding="utf-8", newline="") as f:
        if kosong_akhir:
            f.write("\n")
        csv.writer(f, lineterminator="\n").writerows(baru)
    print("log-keputusan.csv: +", len(baru), "entri")


# ---------------------------------------------------------------- main
def main():
    OUT_TABEL.mkdir(parents=True, exist_ok=True)
    s = seragamkan(muat())
    nas, prov, lain = pisah(s)
    print("baris Silver:", len(s), "| provinsi:", len(prov), "| Indonesia:", len(nas), "| kode tak dikenal:", len(lain))
    if len(lain):
        print("  kode tak dikenal:", sorted(lain["wilayah_kode"].unique()))
    grid = bentuk_grid(prov)
    kel = kelengkapan(grid)
    kat = grid["kategori"].value_counts().to_dict()
    n_kosong = int((grid["kategori"] != "terisi").sum())
    langgar, ringkas = uji_jumlah(s)
    pl, tk = uji_persen_luas(s), analisis_tertukar(langgar, s)
    ctx = {"tertukar": tk, "persen_luas": pl, "n_silver": len(s), "n_prov": len(prov), "n_nas": len(nas), "n_lain": len(lain),
           "n_sel": len(grid), "n_terisi": kat.get("terisi", 0), "n_kosong": n_kosong, "kat": kat,
           "kel": kel, "luar": di_luar_cakupan(grid), "tak_terbit": periode_tak_terbit_di_rincian(prov),
           "ringkas": ringkas, "langgar": langgar, "nasional": uji_nasional(s), "katalog": katalog(s),
           "sdg": sdg_var2532(s), "n_var2532": int((s["seri_kode"] == "var2532").sum()),
           "n_var588": int((s["seri_kode"] == "var588").sum())}
    grid.to_csv(OUT_TABEL / "grid_panel.csv", index=False)
    kel.to_csv(OUT_TABEL / "kelengkapan_panel.csv", index=False)
    langgar.to_csv(OUT_TABEL / "uji_jumlah_pelanggaran.csv", index=False)
    tk.to_csv(OUT_TABEL / "analisis_tertukar.csv", index=False)
    pl.to_csv(OUT_TABEL / "uji_persen_luas.csv", index=False)
    grid[grid["kategori"] == "missing"].to_csv(OUT_TABEL / "sel_missing.csv", index=False)
    ctx["luar"].to_csv(OUT_TABEL / "provinsi_di_luar_cakupan.csv", index=False)
    ctx["katalog"].to_csv(OUT_TABEL / "katalog_seri.csv", index=False)
    ctx["sdg"].to_csv(OUT_TABEL / "usulan_sdg_var2532.csv", index=False)
    tulis_laporan(ctx)
    print("sel grid:", len(grid), "| kategori:", kat)
    print(ringkas.to_string(index=False))
    print("uji nasional di atas ambang:", len(ctx["nasional"]), "| uji persen vs luas melanggar:", len(pl))
    print(tk["jenis_dugaan"].value_counts().to_string())
    print(ctx["katalog"][["seri_kode", "berkas", "kecocokan_kode"]].to_string(index=False))
    a = Path("reports/tabel/calon_anomali.csv")
    outlier = int(pd.read_csv(a)["kuat"].sum()) if a.exists() else "ISI_DARI_TAHAP_2"
    print("\nperintah metrics (jalankan setelah hasil diperiksa):")
    print(f"python -m src.common.hasil {NIM} berkas_terverifikasi=13 baris_silver={len(s)} "
          f"sel_kosong_grid={n_kosong} outlier_ditandai={outlier}")
    if "--catat-log" in sys.argv:
        catat_log(ctx)


if __name__ == "__main__":
    main()