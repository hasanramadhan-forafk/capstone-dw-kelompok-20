"""Tahap 1 - Ekstraksi (pertemuan X). Milik tim.

Baca setiap berkas di data/raw/ (CSV, JSON WebAPI BPS, XLSX BNPB, SDMX ILO, JSON WDI) menjadi
DataFrame mentah yang setiap pada sumbernya: jangan membersihkan di sini, cukup ratakan struktur
dan catat asal tiap baris (`_berkas_raw` relatif data/raw/, `_sha256_raw` dari src.common.manifest).
"""

import pandas as pd
from src.common.manifest import RAW
from src.ekstraksi.wdi import baca_wdi_data
from src.bps import baca_csv_bps, baca_json_bps

def jalankan():
    """Kembalikan {nama_sumber: DataFrame mentah}."""
    hasil_ekstraksi = {}
    
    # 1. Ekstraksi WDI
    path_wdi = RAW / "wdi" / "2026-10-20" / "data" / "kelompok-01-hal-01.json"
    if path_wdi.exists():
        try:
            hasil_ekstraksi["wdi_data"] = baca_wdi_data(path_wdi)
        except Exception as e:
            print(f"Gagal baca WDI: {e}")

    # 2. Ekstraksi BPS (CSV)
    file_bps_csv = ["sdg15_tutupan_hutan.csv", "sdg15_lahan_kritis.csv", "sdg15_tutupan_kawasan.csv", "sdg15_iklh.csv"]
    for file in file_bps_csv:
        try:
            nama_kunci = f"bps_csv_{file.replace('.csv', '')}"
            hasil_ekstraksi[nama_kunci] = baca_csv_bps(file)
        except Exception as e:
            print(f"Gagal baca BPS CSV {file}: {e}")

    # 3. Ekstraksi BPS (JSON)
    file_bps_json = ["sdg15_tutupan_hutan.json", "sdg15_lahan_kritis.json", "sdg15_tutupan_kawasan.json", "sdg15_iklh.json"]
    for file in file_bps_json:
        try:
            nama_kunci = f"bps_json_{file.replace('.json', '')}"
            hasil_ekstraksi[nama_kunci] = baca_json_bps(file)
        except Exception as e:
            print(f"Gagal baca BPS JSON {file}: {e}")
            
    # Anda bisa menambahkan pembaca lain di sini (XLSX BNPB, SDMX ILO) jika ada

    return hasil_ekstraksi