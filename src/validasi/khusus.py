"""Aturan validasi khusus Kasus 20 (Hutan, lahan, dan kualitas lingkungan)."""
import pandas as pd

KOMPONEN_IKLH_SAH = {
    "kualitas_udara", "kualitas_air", "kualitas_tutupan_lahan",
    "kualitas_lahan", "kualitas_ekosistem_gambut", "kualitas_air_laut"
}


def luas_tidak_negatif(silver: pd.DataFrame) -> pd.DataFrame:
    """Memastikan luas tidak negatif. Mengembalikan baris pelanggaran."""
    s = silver[silver["satuan"].isin(["ribu_hektar", "hektar", "km2"])]
    return s[s["nilai"] < 0]


def komponen_iklh_sah(silver: pd.DataFrame) -> pd.DataFrame:
    """Rincian IKLH (var2532) harus komponen resmi."""
    s = silver[silver["seri_kode"] == "var2532"]
    return s[~s["rincian"].isin(KOMPONEN_IKLH_SAH)]


def konsistensi_lahan_kritis(silver: pd.DataFrame) -> pd.DataFrame:
    """Pemeriksaan kritis + sangat_kritis == total pada var588."""
    s = silver[silver["seri_kode"] == "var588"]
    piv = s.pivot_table(index=["wilayah_kode", "periode"], columns="rincian", values="nilai")
    if {"kritis", "sangat_kritis", "total"}.issubset(piv.columns):
        selisih = (piv["kritis"] + piv["sangat_kritis"]) - piv["total"]
        gagal = piv[selisih.abs() > 0.05]
        return gagal
    return pd.DataFrame()


def deteksi_kolom_2020_tergeser(silver: pd.DataFrame) -> pd.DataFrame:
    """Aturan peringatan: mendeteksi anomali kolom 2020 pada tutupan hutan."""
    s = silver[silver["seri_kode"] == "tabel:sdg15_tutupan_hutan:luas_ribu_ha"]
    piv = s.pivot_table(index=["wilayah_kode", "periode"], columns="rincian", values="nilai")
    if {"hutan", "non_hutan", "total"}.issubset(piv.columns):
        selisih = (piv["hutan"] + piv["non_hutan"]) - piv["total"]
        anomali = piv[selisih.abs() > 1.0]
        return anomali
    return pd.DataFrame()