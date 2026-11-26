"""Komponen Transformasi dan panel, kasus 20 (hutan, lahan, kualitas lingkungan).

Tahap 4 Sprint 1: tabel mentah BPS -> data/silver/silver.parquet yang lolos src.common.skema.
"""
from pathlib import Path

import pandas as pd

from src.common.manifest import RAW, baca, sha256_raw
from src.common.skema import KOLOM, periksa_silver

SILVER = Path(__file__).resolve().parents[2] / "data" / "silver" / "silver.parquet"

# 38 provinsi susunan 2025 (kode BPS x 100) + 9999 Indonesia.
PROVINSI_2025 = {
    1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2100,
    3100, 3200, 3300, 3400, 3500, 3600, 5100, 5200, 5300,
    6100, 6200, 6300, 6400, 6500, 7100, 7200, 7300, 7400, 7500, 7600,
    8100, 8200, 9100, 9200, 9400, 9500, 9600, 9700,
}
INDONESIA = 9999

# Metadata seri. kode_sdg tidak masuk Silver (skema tidak punya kolomnya); dipakai Gold dan data dictionary.
# pembagi: nilai silver = nilai mentah / pembagi (dibagi, bukan dikali 0,001, agar tidak ada galat float).
META_SERI = {
    "tabel:sdg15_tutupan_hutan:luas_ribu_ha": dict(berkas="sdg15_tutupan_hutan.csv", satuan_asal="ribu ha",
                                                   satuan="ribu_hektar", pembagi=1, kode_sdg="15.1.1"),
    "tabel:sdg15_tutupan_hutan:persen": dict(berkas="sdg15_tutupan_hutan.csv", satuan_asal="persen",
                                             satuan="persen", pembagi=1, kode_sdg="15.1.1"),
    "var1304": dict(berkas="sdg15_tutupan_kawasan.csv", satuan_asal="Ribu Hektar",
                    satuan="ribu_hektar", pembagi=1, kode_sdg="15.3.1"),
    "var588": dict(berkas="sdg15_lahan_kritis.csv", satuan_asal="Hektar",
                   satuan="ribu_hektar", pembagi=1000, kode_sdg="15.3.1"),
    "var2532": dict(berkas="sdg15_iklh.csv", satuan_asal="(kosong)",
                    satuan="tidak_ada", pembagi=1, kode_sdg="11.6.2"),
}

RINCIAN_BPS = {
    "var1304": {1155: "kawasan_hutan", 1156: "apl", 1461: "total"},
    "var588": {770: "kritis", 771: "sangat_kritis", 772: "total"},
    "var2532": {2175: "kualitas_udara", 2176: "kualitas_air", 2177: "kualitas_tutupan_lahan",
                2178: "kualitas_lahan", 2179: "kualitas_ekosistem_gambut", 2180: "kualitas_air_laut"},
}
VAR_ID = {"var1304": 1304, "var588": 588, "var2532": 2532}
BERKAS_BPS = ["sdg15_tutupan_kawasan.csv", "sdg15_lahan_kritis.csv", "sdg15_iklh.csv"]
BERKAS_HUTAN = "sdg15_tutupan_hutan.csv"

KOLOM_MENTAH_BPS = {"var_id", "wilayah_id", "wilayah", "turvar_id", "turvar", "tahun", "periode", "nilai"}
KOLOM_MENTAH_HUTAN = {"wilayah", "tahun", "tutupan", "ukuran", "nilai"}


def _cari_berkas(nama, raw=RAW):
    """Jalur relatif data/raw/ untuk sebuah nama berkas, persis seperti tertulis di MANIFEST.csv."""
    cocok = [b for b in baca(Path(raw)) if Path(b).name == nama]
    if len(cocok) != 1:
        raise FileNotFoundError(f"{nama}: ditemukan {len(cocok)} di MANIFEST.csv, harus tepat 1")
    return cocok[0]


def _nama_ke_kode(tabel_bps):
    """Pasangan nama wilayah -> wilayah_kode dari CSV BPS yang punya wilayah_id."""
    pas = pd.concat([t[["wilayah", "wilayah_id"]] for t in tabel_bps.values()]).drop_duplicates()
    if pas["wilayah"].duplicated().any() or pas["wilayah_id"].duplicated().any():
        raise ValueError("pasangan nama-kode wilayah tidak satu-satu antar CSV BPS")
    return dict(zip(pas["wilayah"], pas["wilayah_id"].astype("int64")))


def _bps_panjang(df, seri):
    m = META_SERI[seri]
    d = df[df["var_id"] == VAR_ID[seri]]
    rincian = d["turvar_id"].map(RINCIAN_BPS[seri])
    if rincian.isna().any():
        raise ValueError(f"{seri}: turvar_id tak dikenal {sorted(d.loc[rincian.isna(), 'turvar_id'].unique())}")
    return pd.DataFrame({
        "seri_kode": seri, "wilayah_kode": d["wilayah_id"].astype("int64"), "nama_wilayah": d["wilayah"],
        "periode": d["tahun"].astype(int).astype(str), "rincian": rincian,
        "nilai": d["nilai"].astype(float) / m["pembagi"], "satuan": m["satuan"]})


def _hutan(df, seri, ukuran, nama_ke_kode):
    m = META_SERI[seri]
    d = df[df["ukuran"] == ukuran]
    kode = d["wilayah"].map(nama_ke_kode)
    if kode.isna().any():
        raise ValueError(f"{seri}: nama wilayah tanpa kode {sorted(d.loc[kode.isna(), 'wilayah'].unique())}")
    return pd.DataFrame({
        "seri_kode": seri, "wilayah_kode": kode.astype("int64"), "nama_wilayah": d["wilayah"],
        "periode": d["tahun"].astype(int).astype(str), "rincian": d["tutupan"].replace({"jumlah": "total"}),
        "nilai": d["nilai"].astype(float) / m["pembagi"], "satuan": m["satuan"]})


def ke_silver(mentah, raw=RAW):
    """mentah: {nama berkas CSV: DataFrame mentah}. Mengembalikan (silver, laporan).

    laporan: {seri_kode: baris tanpa nilai yang tidak dimasukkan}, untuk kolom dampak_baris di log.
    """
    bps = {n: mentah[n] for n in BERKAS_BPS}
    for n, t in {**bps, BERKAS_HUTAN: mentah[BERKAS_HUTAN]}.items():
        perlu = KOLOM_MENTAH_HUTAN if n == BERKAS_HUTAN else KOLOM_MENTAH_BPS
        if perlu - set(t.columns):
            raise ValueError(f"{n}: kolom mentah kurang {sorted(perlu - set(t.columns))}")
    nama_ke_kode = _nama_ke_kode(bps)

    bagian = {
        "tabel:sdg15_tutupan_hutan:luas_ribu_ha": _hutan(mentah[BERKAS_HUTAN], "tabel:sdg15_tutupan_hutan:luas_ribu_ha",
                                                         "luas_ribu_ha", nama_ke_kode),
        "tabel:sdg15_tutupan_hutan:persen": _hutan(mentah[BERKAS_HUTAN], "tabel:sdg15_tutupan_hutan:persen",
                                                   "persen", nama_ke_kode),
        "var1304": _bps_panjang(bps["sdg15_tutupan_kawasan.csv"], "var1304"),
        "var588": _bps_panjang(bps["sdg15_lahan_kritis.csv"], "var588"),
        "var2532": _bps_panjang(bps["sdg15_iklh.csv"], "var2532"),
    }
    laporan, hasil = {}, []
    for seri, t in bagian.items():
        laporan[seri] = int(t["nilai"].isna().sum())
        t = t.dropna(subset=["nilai"]).copy()
        berkas = _cari_berkas(META_SERI[seri]["berkas"], raw)
        t["sumber"], t["jenis_periode"] = "bps", "tahun"
        t["_berkas_raw"], t["_sha256_raw"] = berkas, sha256_raw(berkas, raw)
        hasil.append(t)
    silver = pd.concat(hasil, ignore_index=True)[KOLOM]

    liar = set(silver["wilayah_kode"]) - PROVINSI_2025 - {INDONESIA}
    if liar:
        raise ValueError(f"wilayah_kode di luar 38 provinsi 2025 dan 9999: {sorted(liar)}")
    return silver.sort_values(["seri_kode", "wilayah_kode", "periode", "rincian"]).reset_index(drop=True), laporan


def baca_mentah(raw=RAW):
    return {n: pd.read_csv(Path(raw) / _cari_berkas(n, raw)) for n in BERKAS_BPS + [BERKAS_HUTAN]}


def main():
    silver, laporan = ke_silver(baca_mentah())
    SILVER.parent.mkdir(parents=True, exist_ok=True)
    silver.to_parquet(SILVER, index=False)
    print(f"{len(silver):,} baris ditulis ke {SILVER}")
    print("baris tanpa nilai (tidak masuk Silver):", {k: v for k, v in laporan.items() if v})
    salah = periksa_silver(silver, baca(RAW))
    print("skema:", "LOLOS" if not salah else salah)


if __name__ == "__main__":
    main()