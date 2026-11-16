"""Tahap 2: profil deskriptif, grafik, dan calon anomali.

Tujuan: Nyari calon anomali, bukan memperbaikinya. Tidak ada nilai yang diubah.
Membaca CSV mentah BPS di data/raw (Silver belum ada). Hanya muat() yang bergantung
pada format mentah; ganti di situ kalau nanti memakai pembaca Tahap 1 atau Silver.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RAW_BPS = Path("data/raw/bps")
OUT_GAMBAR = Path("reports/gambar")
OUT_TABEL = Path("reports/tabel")
OUT_LAPORAN = Path("reports/profil_per_seri.md")

SERI = [
    "tabel:sdg15_tutupan_hutan:luas_ribu_ha",
    "tabel:sdg15_tutupan_hutan:persen",
    "var1304", "var588", "var2532",
]
VAR_ID = [1304, 588, 2532]
NASIONAL = {"INDONESIA", "NASIONAL"}
Z_AMBANG = 3.0
IQR_K = 1.5
MIN_N_PROV = 8
MIN_N_LONCAT = 20
KOL_A = ["seri", "rincian", "wilayah", "periode", "nilai", "jenis", "z", "kuat", "alasan"]


# Persdiapannnnnnnn hikjs
def muat() -> pd.DataFrame:
    """Gabungkan CSV BPS mentah ke satu tabel panjang: seri, rincian, wilayah, periode, nilai."""
    bagian = []
    for f in sorted(RAW_BPS.glob("*/sdg15_*.csv")):
        d = pd.read_csv(f, encoding="utf-8-sig")
        if "var_id" in d.columns:
            d = d[d["var_id"].isin(VAR_ID)]
            if d.empty:
                continue
            out = pd.DataFrame({
                "seri": "var" + d["var_id"].astype(int).astype(str),
                "rincian": d["turvar"],
                "wilayah": d["wilayah"],
                "wilayah_id": d["wilayah_id"],
                "periode": d["tahun"],
                "nilai": d["nilai"],
                "satuan": d["satuan"],
            })
        elif {"ukuran", "tutupan"} <= set(d.columns):
            out = pd.DataFrame({
                "seri": "tabel:" + f.stem + ":" + d["ukuran"].astype(str),
                "rincian": d["tutupan"],
                "wilayah": d["wilayah"],
                "wilayah_id": np.nan,
                "periode": d["tahun"],
                "nilai": d["nilai"],
                "satuan": d["ukuran"],
            })
        else:
            continue
        out["_berkas_raw"] = f.name
        bagian.append(out)
    return pd.concat(bagian, ignore_index=True)


def siapkan(d: pd.DataFrame) -> pd.DataFrame:
    d = d[d["seri"].isin(SERI)].copy()
    asli = d["nilai"]
    d["nilai"] = pd.to_numeric(asli, errors="coerce")
    print("nilai tak terbaca sebagai angka:", int((asli.notna() & d["nilai"].isna()).sum()))
    d["periode"] = pd.to_numeric(d["periode"], errors="coerce")
    d = d.dropna(subset=["periode"])
    d["periode"] = d["periode"].astype(int)
    d["rincian"] = d["rincian"].fillna("(tanpa rincian)").astype(str)
    d["wilayah"] = d["wilayah"].astype(str).str.strip()
    nas = d["wilayah"].str.upper().isin(NASIONAL) | (d["wilayah_id"] == 9999)
    print("baris nasional dikeluarkan dari statistik provinsi:", int(nas.sum()))
    d = d[~nas]
    kunci = ["seri", "rincian", "wilayah", "periode"]
    print("baris kembar pada kunci seri/rincian/wilayah/periode:", int(d.duplicated(kunci).sum()))
    return d.sort_values(kunci).reset_index(drop=True)


# profil
def profil(d: pd.DataFrame, by: list) -> pd.DataFrame:
    p = d.groupby(by)["nilai"].agg(
        n="count", n_kosong=lambda s: s.isna().sum(), rerata="mean", sd="std", min="min",
        q1=lambda s: s.quantile(.25), median="median",
        q3=lambda s: s.quantile(.75), maks="max")
    p["iqr"] = p["q3"] - p["q1"]
    p["cv_persen"] = p["sd"] / p["rerata"].abs() * 100
    return p.reset_index()


def profil_seri(d: pd.DataFrame) -> pd.DataFrame:
    p = profil(d, ["seri", "rincian"])
    e = d.groupby(["seri", "rincian"]).agg(
        satuan=("satuan", "first"), n_provinsi=("wilayah", "nunique"),
        n_periode=("periode", "nunique"), periode_min=("periode", "min"),
        periode_maks=("periode", "max")).reset_index()
    return p.merge(e, on=["seri", "rincian"])


def profil_provinsi(d: pd.DataFrame) -> pd.DataFrame:
    p = profil(d, ["seri", "rincian", "wilayah"])
    baris = []
    for (s, r, w), g in d.sort_values("periode").groupby(["seri", "rincian", "wilayah"]):
        v = g["nilai"].dropna().to_numpy()
        sama = float(np.mean(v[1:] == v[:-1]) * 100) if len(v) > 1 else np.nan
        baris.append({"seri": s, "rincian": r, "wilayah": w, "persen_sama_dgn_sebelumnya": sama})
    return p.merge(pd.DataFrame(baris), on=["seri", "rincian", "wilayah"])


# anomali
def _skor(x: pd.Series) -> pd.DataFrame:
    sd = x.std(ddof=1)
    z = (x - x.mean()) / sd if (pd.notna(sd) and sd > 0) else pd.Series(np.nan, index=x.index)
    q1, q3 = x.quantile(.25), x.quantile(.75)
    iqr = q3 - q1
    lo, hi = q1 - IQR_K * iqr, q3 + IQR_K * iqr
    iqr_flag = ((x < lo) | (x > hi)) if iqr > 0 else pd.Series(False, index=x.index)
    return pd.DataFrame({"z": z, "lo": lo, "hi": hi, "z_flag": z.abs() > Z_AMBANG, "iqr_flag": iqr_flag})


def _teks(sk: pd.DataFrame, i) -> str:
    a = []
    if sk.at[i, "z_flag"]:
        a.append(f"z={sk.at[i, 'z']:+.2f} (ambang ±{Z_AMBANG:g})")
    if sk.at[i, "iqr_flag"]:
        a.append(f"di luar pagar IQR [{sk.at[i, 'lo']:.2f}; {sk.at[i, 'hi']:.2f}]")
    return ", ".join(a)


def antar_provinsi(d: pd.DataFrame) -> list:
    hasil = []
    for (s, r, p), g in d.dropna(subset=["nilai"]).groupby(["seri", "rincian", "periode"]):
        if len(g) < MIN_N_PROV:
            continue
        sk = _skor(g["nilai"])
        m = (sk["z_flag"] | sk["iqr_flag"]).to_numpy()
        for i in g.index[m]:
            hasil.append({
                "seri": s, "rincian": r, "wilayah": g.at[i, "wilayah"], "periode": int(p),
                "nilai": g.at[i, "nilai"], "jenis": "antar_provinsi",
                "z": round(float(sk.at[i, "z"]), 2),
                "kuat": bool(sk.at[i, "z_flag"] and sk.at[i, "iqr_flag"]),
                "alasan": f"nilai {g.at[i, 'nilai']:g} dibanding provinsi lain tahun {p}: " + _teks(sk, i)})
    return hasil


def loncatan(d: pd.DataFrame) -> list:
    hasil = []
    for (s, r), g in d.dropna(subset=["nilai"]).groupby(["seri", "rincian"]):
        g = g.sort_values(["wilayah", "periode"]).copy()
        grup = g.groupby("wilayah")
        g["nilai_sebelum"] = grup["nilai"].shift()
        g["periode_sebelum"] = grup["periode"].shift()
        g = g.dropna(subset=["nilai_sebelum"])
        selang = g["periode"] - g["periode_sebelum"]
        g["ubah"] = (g["nilai"] - g["nilai_sebelum"]) / g["nilai_sebelum"].abs() * 100 / selang
        g["ubah"] = g["ubah"].replace([np.inf, -np.inf], np.nan)
        g = g.dropna(subset=["ubah"])
        if len(g) < MIN_N_LONCAT:
            continue
        sk = _skor(g["ubah"])
        m = (sk["z_flag"] | sk["iqr_flag"]).to_numpy()
        for i in g.index[m]:
            hasil.append({
                "seri": s, "rincian": r, "wilayah": g.at[i, "wilayah"], "periode": int(g.at[i, "periode"]),
                "nilai": g.at[i, "nilai"], "jenis": "loncatan",
                "z": round(float(sk.at[i, "z"]), 2),
                "kuat": bool(sk.at[i, "z_flag"] and sk.at[i, "iqr_flag"]),
                "alasan": (f"dari {g.at[i, 'nilai_sebelum']:g} ({int(g.at[i, 'periode_sebelum'])}) ke "
                           f"{g.at[i, 'nilai']:g}, {g.at[i, 'ubah']:+.1f}%/tahun: " + _teks(sk, i))})
    return hasil


def calon_anomali(d: pd.DataFrame) -> pd.DataFrame:
    a = pd.DataFrame(antar_provinsi(d) + loncatan(d), columns=KOL_A)
    a["kuat"] = a["kuat"].astype(bool)
    return a.sort_values(["seri", "rincian", "wilayah", "periode", "jenis"]).reset_index(drop=True)


# grafik
def nama_aman(s: str) -> str:
    return s.replace(":", "_")


def _kisi(n: int):
    kol = 2 if n > 1 else 1
    baris = int(np.ceil(n / kol))
    fig, axes = plt.subplots(baris, kol, figsize=(7 * kol, 4 * baris), squeeze=False)
    axes = axes.ravel()
    for ax in axes[n:]:
        ax.set_visible(False)
    return fig, axes


def gambar_boxplot(d: pd.DataFrame, seri: str) -> Path:
    s = d[d["seri"] == seri].dropna(subset=["nilai"])
    rincian = sorted(s["rincian"].unique())
    fig, axes = _kisi(len(rincian))
    for ax, r in zip(axes, rincian):
        t = s[s["rincian"] == r]
        thn = sorted(t["periode"].unique())
        ax.boxplot([t.loc[t["periode"] == y, "nilai"] for y in thn],
                   flierprops={"markerfacecolor": "red", "markersize": 4})
        ax.set_xticks(range(1, len(thn) + 1))
        ax.set_xticklabels(thn)
        ax.set_title(r, fontsize=10)
        ax.set_xlabel("tahun")
    fig.suptitle(f"Boxplot antar provinsi per tahun: {seri}")
    fig.tight_layout()
    f = OUT_GAMBAR / f"boxplot_{nama_aman(seri)}.png"
    fig.savefig(f, dpi=150)
    plt.close(fig)
    return f


def gambar_deret(d: pd.DataFrame, a: pd.DataFrame, seri: str) -> Path:
    s = d[d["seri"] == seri].dropna(subset=["nilai"])
    rincian = sorted(s["rincian"].unique())
    fig, axes = _kisi(len(rincian))
    for ax, r in zip(axes, rincian):
        t = s[s["rincian"] == r]
        for _, g in t.groupby("wilayah"):
            g = g.sort_values("periode")
            ax.plot(g["periode"], g["nilai"], color="grey", alpha=.4, lw=1, marker="o", ms=2)
        med = t.groupby("periode")["nilai"].median()
        ax.plot(med.index, med.values, color="blue", lw=2, label="median provinsi")
        t_a = a[(a["seri"] == seri) & (a["rincian"] == r)].drop_duplicates(["wilayah", "periode"])
        ax.scatter(t_a["periode"], t_a["nilai"], color="red", zorder=3, s=18, label="calon anomali")
        ax.set_xticks(sorted(t["periode"].unique()))
        ax.set_title(r, fontsize=10)
        ax.set_xlabel("tahun")
        ax.legend(fontsize=8)
    fig.suptitle(f"Deret waktu per provinsi: {seri}")
    fig.tight_layout()
    f = OUT_GAMBAR / f"deret_{nama_aman(seri)}.png"
    fig.savefig(f, dpi=150)
    plt.close(fig)
    return f


# laporan
def _fmt(v) -> str:
    if pd.isna(v):
        return ""
    if isinstance(v, float):
        return f"{v:.3f}"
    return str(v).replace("|", "\\|")


def md(df: pd.DataFrame) -> str:
    kol = list(df.columns)
    baris = ["| " + " | ".join(kol) + " |", "|" + "---|" * len(kol)]
    for r in df.astype(object).itertuples(index=False):
        baris.append("| " + " | ".join(_fmt(v) for v in r) + " |")
    return "\n".join(baris)


def tulis_laporan(d, p_seri, a, cb):
    ada = set(d["seri"].unique())
    L = ["# Tahap 2: profil statistik dan calon anomali", "",
         "Sumber: CSV mentah BPS di `data/raw/bps`. Tujuannya menemukan calon anomali; "
         "tidak ada nilai yang diperbaiki.", "",
         "## Metode", "",
         f"- **Antar provinsi:** tiap seri × rincian × tahun dengan minimal {MIN_N_PROV} provinsi dinilai "
         f"dengan z-score (|z| > {Z_AMBANG:g}) dan pagar IQR ({IQR_K:g}×IQR).",
         "- **Loncatan:** perubahan relatif per tahun antara dua periode berurutan per provinsi, "
         "dikumpulkan per seri × rincian, lalu dinilai dengan ambang yang sama.",
         "- Tidak ada uji z per deret provinsi: dengan n titik, |z| maksimum adalah (n-1)/√n "
         "(4 titik: 1,5; 10 titik: 2,85), sehingga ambang 3 tidak mungkin tercapai.",
         "- `kuat` berarti lolos z-score dan IQR sekaligus.",
         "- Luas absolut dipengaruhi ukuran provinsi, jadi tanda antar provinsi pada seri luas belum tentu galat.", ""]
    if len(a):
        rk = a.groupby(["seri", "jenis"]).agg(titik=("nilai", "size"), kuat=("kuat", "sum")).reset_index()
        L += ["## Ringkasan calon anomali", md(rk), ""]
    for s in SERI:
        L += [f"## {s}", ""]
        if s not in ada:
            L += ["Seri tidak ditemukan di data.", ""]
            continue
        b = gambar_boxplot(d, s)
        t = gambar_deret(d, a, s)
        ps = p_seri[p_seri["seri"] == s].drop(columns="seri")
        sa = a[a["seri"] == s]
        kuat = sa[sa["kuat"]][["rincian", "wilayah", "periode", "nilai", "jenis", "z", "alasan"]]
        L += ["### Profil per rincian", md(ps), "",
              f"![boxplot antar provinsi per tahun](gambar/{b.name})", "",
              f"![deret waktu per provinsi](gambar/{t.name})", "",
              f"### Calon anomali: {len(sa)} titik, {len(kuat)} kuat", ""]
        L += [md(kuat) if len(kuat) else "_tidak ada yang kuat_", "",
              f"Daftar lengkap (termasuk yang bukan kuat): `reports/tabel/calon_anomali.csv`.", ""]

    # di luar loop: ditulis sekali saja
    L += ["## Ketidakkonsistenan bawaan tabel tutupan hutan", "",
          "Baris yang ditandai kolom `cek` oleh sumber, atau yang selisih hutan + non_hutan terhadap jumlah "
          "lebih dari 0,5 ribu ha. Daftar lengkap: `reports/tabel/calon_anomali_cek_bawaan.csv`.", "",
          f"Total: {len(cb)} pasangan wilayah-tahun.", ""]
    if len(cb):
        L += [md(cb.groupby("tahun").size().rename("jumlah_wilayah").reset_index()), "",
            md(cb[["wilayah", "tahun", "hutan", "non_hutan", "jumlah", "selisih",
                "hutan_dari_persen", "hn_sama_dengan_jumlah_milik", "alasan"]]), ""]

    OUT_LAPORAN.write_text("\n".join(L), encoding="utf-8")

def cek_bawaan() -> pd.DataFrame:
    """Wilayah-tahun yang ditandai kolom `cek` sumber atau selisih hutan + non_hutan - jumlah > 0,5."""
    f = next(RAW_BPS.glob("*/sdg15_tutupan_hutan.csv"))
    d = pd.read_csv(f, encoding="utf-8-sig")
    d = d[~d["wilayah"].str.upper().isin(NASIONAL)]
    luas = d[d["ukuran"] == "luas_ribu_ha"]
    w = luas.pivot_table(index=["wilayah", "tahun"], columns="tutupan", values="nilai", aggfunc="first")
    w["selisih"] = w["hutan"] + w["non_hutan"] - w["jumlah"]
    w["hn"] = (w["hutan"] + w["non_hutan"]).round(1)
    pers = d[(d["ukuran"] == "persen") & (d["tutupan"] == "hutan")].set_index(["wilayah", "tahun"])["nilai"]
    w["hutan_dari_persen"] = (pers.reindex(w.index) * w["jumlah"] / 100).round(1)
    w = w.join(luas.groupby(["wilayah", "tahun"])["cek"].first().rename("cek_sumber")).reset_index()
    pemilik = (w.dropna(subset=["jumlah"]).assign(j=lambda x: x["jumlah"].round(1))
                 .groupby("j")["wilayah"].agg(lambda s: ", ".join(sorted(set(s)))))
    w["hn_sama_dengan_jumlah_milik"] = w["hn"].map(pemilik)
    w = w[w["cek_sumber"].notna() | (w["selisih"].abs() > 0.5)].copy()
    w["alasan"] = "hutan + non_hutan - jumlah = " + w["selisih"].round(1).astype(str) + " ribu ha"
    return w

def catatan_sumber() -> pd.DataFrame:
    f = next(RAW_BPS.glob("*/sdg15_tutupan_hutan.csv"))
    d = pd.read_csv(f, encoding="utf-8-sig")
    k = d[d["catatan"].notna()]
    return (k.groupby(["wilayah", "catatan"])["tahun"]
              .agg(lambda s: ", ".join(str(int(x)) for x in sorted(set(s)))).reset_index())

def nilai_kosong(d: pd.DataFrame) -> pd.DataFrame:
    k = d[d["nilai"].isna()]
    g = k.groupby(["seri", "rincian", "wilayah"]).agg(
        n=("periode", "size"),
        periode_kosong=("periode", lambda s: ", ".join(str(int(x)) for x in sorted(s)))).reset_index()
    g["alasan"] = "nilai kosong di berkas mentah (KASUS.md menyebut mentah tanpa baris kosong)"
    return g

def main():
    OUT_GAMBAR.mkdir(parents=True, exist_ok=True)
    OUT_TABEL.mkdir(parents=True, exist_ok=True)
    d = siapkan(muat())
    ada = set(d["seri"].unique())
    print("seri ditemukan:", sorted(ada))
    print("seri HILANG:", [s for s in SERI if s not in ada])
    print(d.groupby(["seri", "rincian"]).agg(
        provinsi=("wilayah", "nunique"), periode=("periode", "nunique"),
        kosong=("nilai", lambda s: s.isna().sum())).to_string())
    p_seri, p_prov, a = profil_seri(d), profil_provinsi(d), calon_anomali(d)
    p_seri.to_csv(OUT_TABEL / "profil_per_seri.csv", index=False)
    p_prov.to_csv(OUT_TABEL / "profil_per_provinsi.csv", index=False)
    a.to_csv(OUT_TABEL / "calon_anomali.csv", index=False)

    cb = cek_bawaan()
    cb.to_csv(OUT_TABEL / "calon_anomali_cek_bawaan.csv", index=False)
    print("tidak konsisten hutan+non_hutan vs jumlah:", len(cb), "baris wilayah-tahun")
    print(cb.groupby("tahun").size().to_string())

    tulis_laporan(d, p_seri, a, cb)
    nk = nilai_kosong(d)
    nk.to_csv(OUT_TABEL / "calon_anomali_nilai_kosong.csv", index=False)
    cs = catatan_sumber()
    cs.to_csv(OUT_TABEL / "catatan_sumber.csv", index=False)
    with OUT_LAPORAN.open("a", encoding="utf-8") as f:
        f.write("\n## Nilai kosong di berkas mentah\n\n" + md(nk) + "\n")
        f.write("\n## Catatan dari sumber (kolom catatan)\n\n" + md(cs) + "\n")


if __name__ == "__main__":
    main()
