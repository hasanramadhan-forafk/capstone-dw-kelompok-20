"""Aturan validasi umum Silver yang berlaku untuk semua seri dan kasus."""
import pandas as pd

PROVINSI_2025 = {
    1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2100,
    3100, 3200, 3300, 3400, 3500, 3600, 5100, 5200, 5300,
    6100, 6200, 6300, 6400, 6500, 7100, 7200, 7300, 7400, 7500, 7600,
    8100, 8200, 9100, 9200, 9400, 9500, 9600, 9700, 9999
}

KUNCI = ["sumber", "seri_kode", "wilayah_kode", "periode", "rincian", "_berkas_raw"]


def cek_keunikan_kunci(df: pd.DataFrame) -> bool:
    """Kombinasi kunci primer tidak boleh ada duplikat."""
    return df.duplicated(subset=KUNCI).sum() == 0


def cek_rentang_satuan(df: pd.DataFrame) -> bool:
    """Persen harus 0-100, luas harus >= 0, indeks harus 0-100."""
    # Persen
    p = df[df["satuan"] == "persen"]["nilai"]
    if not p.empty and not ((p >= 0) & (p <= 100)).all():
        return False
    # Luas
    l = df[df["satuan"].isin(["ribu_hektar", "hektar", "km2"])]["nilai"]
    if not l.empty and not (l >= 0).all():
        return False
    return True


def cek_satuan_seragam(df: pd.DataFrame) -> bool:
    """Satu seri_kode hanya boleh memiliki satu jenis satuan."""
    return (df.groupby("seri_kode")["satuan"].nunique() <= 1).all()


def cek_wilayah_sah(df: pd.DataFrame) -> bool:
    """Kode wilayah harus terdaftar di 38 provinsi 2025 atau 9999."""
    return df["wilayah_kode"].isin(PROVINSI_2025).all()


def cek_tidak_ada_null(df: pd.DataFrame) -> bool:
    """Kolom kunci dan nilai tidak boleh kosong."""
    return not df[KUNCI + ["nilai", "satuan"]].isna().any().any()