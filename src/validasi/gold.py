"""Aturan validasi Gold dan rekonsiliasi (Sprint 2), berlaku untuk Kasus 20.

Setiap aturan = (nama, keterangan, keras, fungsi(silver, gold) -> DataFrame baris yang melanggar).
Aturan keras menghentikan pipeline bila ada baris yang melanggar. Fokus Sprint 2:

- kunci panel unik: indikator + wilayah + periode tidak kembar;
- satu satuan per indikator;
- setiap sel Gold punya pasangan di Silver (tertelusur lewat berkas mentah);
- setiap baris rekonsiliasi berpasangan punya kategori baku dan penjelasan.
"""
import pandas as pd

from src.gold.rekonsiliasi import KATEGORI

STATUS_SAH = {"terisi", "missing", "tidak_diterbitkan", "belum_ada", "batas_lama"}
KUNCI_PANEL = ["indikator", "wilayah_kode", "periode"]
KUNCI_SILVER = ["seri_kode", "wilayah_kode", "periode", "rincian", "_berkas_raw"]


def kunci_panel_unik(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Kunci panel Gold (indikator + wilayah_kode + periode) tidak boleh kembar."""
    p = gold["panel"]
    return p[p.duplicated(KUNCI_PANEL, keep=False)]


def satu_satuan_per_indikator(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Satu indikator panel hanya boleh punya satu satuan baku."""
    p = gold["panel"]
    n = p.groupby("indikator")["satuan"].nunique()
    return p[p["indikator"].isin(n[n != 1].index) | p["satuan"].isna()]


def status_dan_nilai_konsisten(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Status sel baku dan nilai ada jika dan hanya jika sel berstatus 'terisi'."""
    p = gold["panel"]
    salah_status = ~p["status_sel"].isin(STATUS_SAH)
    salah_nilai = (p["status_sel"] == "terisi") != p["nilai"].notna()
    return p[salah_status | salah_nilai]


def tertelusur_ke_silver(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Setiap sel terisi di Gold punya baris Silver asal (seri, wilayah, periode, rincian, berkas)."""
    p = gold["panel"]
    p = p[p["status_sel"] == "terisi"]
    if p.empty:
        return pd.DataFrame()

    kolom_kunci = KUNCI_SILVER
    kurang = [k for k in kolom_kunci if k not in p.columns or k not in silver.columns]
    if kurang:
        raise KeyError(f"kolom penelusuran tidak lengkap: {kurang}")

    s = silver[kolom_kunci].drop_duplicates()
    m = p.merge(s, on=kolom_kunci, how="left", indicator=True)
    return m[m["_merge"] != "both"].drop(columns="_merge")


def tabel_nasional_unik(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Tabel nasional tidak boleh punya duplikat seri + rincian + periode."""
    n = gold["nasional"]
    kolom = ["seri_kode", "rincian", "periode"]
    if not all(k in n.columns for k in kolom):
        return pd.DataFrame()
    return n[n.duplicated(kolom, keep=False)]


def rekonsiliasi_kategori_baku(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Semua baris rekonsiliasi harus memakai kategori baku dan penjelasan tidak kosong."""
    r = gold["rekonsiliasi"]
    salah_kategori = ~r["kategori"].isin(KATEGORI)
    salah_penjelasan = r["penjelasan"].isna() | (r["penjelasan"].astype(str).str.strip() == "")
    return r[salah_kategori | salah_penjelasan]


def rekonsiliasi_berpasangan_berkategori(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Setiap baris rekonsiliasi berpasangan (kedua sisi ada) wajib punya kategori dan penjelasan."""
    r = gold["rekonsiliasi"]
    berpasangan = r[r["asal"] == "keduanya"]
    salah = (
        berpasangan["kategori"].isna()
        | ~berpasangan["kategori"].isin(KATEGORI)
        | (berpasangan["kategori"] == "tanpa pasangan")
        | berpasangan["penjelasan"].isna()
        | (berpasangan["penjelasan"].astype(str).str.strip() == "")
    )
    return berpasangan[salah]


def rekonsiliasi_selisih_konsisten(silver: pd.DataFrame, gold: dict) -> pd.DataFrame:
    """Selisih harus sama dengan nilai_utama - nilai_pembanding."""
    r = gold["rekonsiliasi"]
    h = r[r["selisih"].notna() & r["nilai_utama"].notna() & r["nilai_pembanding"].notna()]
    if h.empty:
        return h
    return h[(h["selisih"] - (h["nilai_utama"] - h["nilai_pembanding"])).abs() > 1e-6]


ATURAN = [
    ("gold: kunci panel unik", "indikator + wilayah_kode + periode tidak kembar", True, kunci_panel_unik),
    ("gold: satu satuan per indikator", "satu indikator panel hanya punya satu satuan", True,
     satu_satuan_per_indikator),
    ("gold: status sel dan nilai", "status sel baku; nilai ada jika dan hanya jika sel terisi", True,
     status_dan_nilai_konsisten),
    ("gold: sel tertelusur ke Silver", "setiap sel terisi punya baris Silver asal (seri, wilayah, periode, rincian, berkas)",
     True, tertelusur_ke_silver),
    ("gold: tabel nasional unik", "seri + rincian + periode tidak kembar", True, tabel_nasional_unik),
    ("rekonsiliasi: kategori baku", "kategori dari daftar baku; penjelasan tidak kosong", True,
     rekonsiliasi_kategori_baku),
    ("rekonsiliasi: baris berpasangan berkategori", "setiap baris dengan kedua sisi punya kategori dan penjelasan",
     True, rekonsiliasi_berpasangan_berkategori),
    ("rekonsiliasi: selisih = utama - pembanding", "selisih dihitung ulang dan cocok", True,
     rekonsiliasi_selisih_konsisten),
]
