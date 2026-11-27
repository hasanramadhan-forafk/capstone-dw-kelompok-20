"""Aturan validasi Gold dan rekonsiliasi (Sprint 2), berlaku untuk Kasus 20 (Hutan, Lahan, dan Lingkungan).

Setiap fungsi mengembalikan DataFrame baris yang melanggar.
Jika tidak ada pelanggaran, fungsi mengembalikan DataFrame kosong.
Aturan dirancang mandiri tanpa dependensi rapuh, siap dijalankan pada objek `gold`
yang berisi dict {'panel': df_panel, 'nasional': df_nasional, 'rekonsiliasi': df_rekonsiliasi}.
"""
import pandas as pd

STATUS_SAH = {"terisi", "missing", "tidak_diterbitkan", "belum_ada", "batas_lama"}
KATEGORI_SAH = {
    "definisi berbeda",
    "metode berbeda",
    "vintage berbeda",
    "cakupan berbeda",
    "belum terjelaskan",
    "tanpa pasangan",
    "tidak berselisih",
    "definisi_berbeda",
    "metodologi_berbeda",
    "vintage_berbeda",
    "cakupan_berbeda",
    "agregasi_spasial",
    "proyeksi",
    "konversi_satuan",
    "identik",
    "tidak_dapat_dibandingkan",
}
KUNCI_PANEL = ["indikator", "wilayah_kode", "periode"]
JUMLAH_LABEL = "total"


def kunci_panel_unik(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Memeriksa keunikan kunci panel: indikator + wilayah_kode + periode tidak boleh kembar."""
    if "panel" not in gold or gold["panel"] is None or gold["panel"].empty:
        return pd.DataFrame()
    p = gold["panel"]
    return p[p.duplicated(KUNCI_PANEL, keep=False)]


def satu_satuan_per_indikator(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Memeriksa setiap indikator panel hanya memiliki satu satuan baku."""
    if "panel" not in gold or gold["panel"] is None or gold["panel"].empty:
        return pd.DataFrame()
    p = gold["panel"]
    n = p.groupby("indikator")["satuan"].nunique()
    multi_satuan = n[n != 1].index
    return p[p["indikator"].isin(multi_satuan) | p["satuan"].isna()]


def status_dan_nilai_konsisten(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Status sel harus baku dan nilai ada jika dan hanya jika sel berstatus 'terisi'."""
    if "panel" not in gold or gold["panel"] is None or gold["panel"].empty:
        return pd.DataFrame()
    p = gold["panel"]
    if "status_sel" not in p.columns:
        return pd.DataFrame()
    salah_status = ~p["status_sel"].isin(STATUS_SAH)
    salah_nilai = (p["status_sel"] == "terisi") != p["nilai"].notna()
    return p[salah_status | salah_nilai]


def tertelusur_ke_silver(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Setiap sel terisi di Gold harus tertelusur ke baris Silver yang sesuai."""
    if "panel" not in gold or gold["panel"] is None or gold["panel"].empty:
        return pd.DataFrame()
    p = gold["panel"]
    if "status_sel" in p.columns:
        p = p[p["status_sel"] == "terisi"]
    if p.empty:
        return pd.DataFrame()

    kolom_kunci = ["seri_kode", "wilayah_kode", "periode", "rincian", "_berkas_raw"]
    # Periksa apakah semua kolom kunci ada di panel dan silver
    if not all(col in p.columns for col in kolom_kunci) or not all(col in silver.columns for col in kolom_kunci):
        return pd.DataFrame()

    s = silver[kolom_kunci].drop_duplicates()
    m = p.merge(s, on=kolom_kunci, how="left", indicator=True)
    return m[m["_merge"] != "both"].drop(columns="_merge")


def nilai_sama_dengan_silver(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Nilai panel Gold harus identik dengan nilai Silver asalnya (tidak ada nilai yang diubah di Gold)."""
    if "panel" not in gold or gold["panel"] is None or gold["panel"].empty:
        return pd.DataFrame()
    p = gold["panel"]
    if "status_sel" in p.columns:
        p = p[p["status_sel"] == "terisi"]
    if p.empty:
        return pd.DataFrame()

    kolom_kunci = ["seri_kode", "wilayah_kode", "periode", "rincian", "_berkas_raw"]
    if not all(col in p.columns for col in kolom_kunci + ["nilai"]) or not all(col in silver.columns for col in kolom_kunci + ["nilai"]):
        return pd.DataFrame()

    s = silver[kolom_kunci + ["nilai"]]
    m = p.merge(s, on=kolom_kunci, suffixes=("", "_silver"))
    if m.empty:
        return pd.DataFrame()
    return m[(m["nilai"] - m["nilai_silver"]).abs() > 1e-6]


def tabel_nasional_unik(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Tabel nasional tidak boleh memiliki duplikat pada seri_kode + rincian + periode."""
    if "nasional" not in gold or gold["nasional"] is None or gold["nasional"].empty:
        return pd.DataFrame()
    n = gold["nasional"]
    kolom = ["seri_kode", "rincian", "periode"]
    if not all(col in n.columns for col in kolom):
        return pd.DataFrame()
    return n[n.duplicated(kolom, keep=False)]


def rekonsiliasi_kategori_baku(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Kategori rekonsiliasi harus berasal dari daftar kategori baku dan penjelasannya tidak boleh kosong."""
    if "rekonsiliasi" not in gold or gold["rekonsiliasi"] is None or gold["rekonsiliasi"].empty:
        return pd.DataFrame()
    r = gold["rekonsiliasi"]
    if "kategori" not in r.columns or "penjelasan" not in r.columns:
        return pd.DataFrame()
    salah_kategori = ~r["kategori"].isin(KATEGORI_SAH)
    salah_penjelasan = r["penjelasan"].isna() | (r["penjelasan"].astype(str).str.strip() == "")
    return r[salah_kategori | salah_penjelasan]


def rekonsiliasi_selisih_konsisten(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Nilai selisih rekonsiliasi harus konsisten dengan: nilai_utama - nilai_pembanding."""
    if "rekonsiliasi" not in gold or gold["rekonsiliasi"] is None or gold["rekonsiliasi"].empty:
        return pd.DataFrame()
    r = gold["rekonsiliasi"]
    kolom = ["selisih", "nilai_utama", "nilai_pembanding"]
    if not all(col in r.columns for col in kolom):
        return pd.DataFrame()
    h = r[r["selisih"].notna() & r["nilai_utama"].notna() & r["nilai_pembanding"].notna()]
    return h[(h["selisih"] - (h["nilai_utama"] - h["nilai_pembanding"])).abs() > 1e-4]
