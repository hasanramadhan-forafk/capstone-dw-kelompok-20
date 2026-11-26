import pandas as pd
from src.bps import baca_csv_bps, baca_json_bps
from src.ekstraksi import jalankan
from src.ekstraksi.wdi import baca_wdi_data, baca_wdi_metadata
from src.common.manifest import RAW

print("="*50)
print("BUKTI TUGAS #1: PEMBACA BPS (CSV & JSON)")
print("="*50)
csv_files = ["sdg15_tutupan_hutan.csv", "sdg15_lahan_kritis.csv", "sdg15_tutupan_kawasan.csv", "sdg15_iklh.csv"]
json_files = ["sdg15_tutupan_hutan.json", "sdg15_lahan_kritis.json", "sdg15_tutupan_kawasan.json", "sdg15_iklh.json"]

for f in csv_files:
    df = baca_csv_bps(f)
    print(f"[CSV] {f} | Baris: {len(df)}")
    print(df[['_berkas_raw', '_sha256_raw']].head(1).to_string(), "\n")

for f in json_files:
    df = baca_json_bps(f)
    print(f"[JSON] {f} | Baris: {len(df)}")
    print(df[['_berkas_raw', '_sha256_raw']].head(1).to_string(), "\n")


print("="*50)
print("BUKTI TUGAS #2: PEMBACA WDI (DATA & METADATA)")
print("="*50)
path_data = RAW / "wdi" / "2026-10-20" / "data" / "kelompok-01-hal-01.json"
path_meta = RAW / "wdi" / "2026-10-20" / "metadata" / "sumber.json"

df_data = baca_wdi_data(path_data)
print(f"[WDI Data] {path_data.name} | Baris: {len(df_data)}")
print(df_data[['_berkas_raw', '_sha256_raw']].head(1).to_string(), "\n")

df_meta = baca_wdi_metadata(path_meta)
print(f"[WDI Metadata] {path_meta.name} | Baris: {len(df_meta)}")
if len(df_meta) > 0:
    print(df_meta[['_berkas_raw', '_sha256_raw']].head(1).to_string(), "\n")
else:
    print("-> 0 baris karena tidak ada indikator yang cocok di file sumber ini.\n")


print("="*50)
print("BUKTI TUGAS #3: PIPELINE JALANKAN()")
print("="*50)
hasil = jalankan()
total_baris = sum(len(df) for df in hasil.values())
print(f"Total Sumber Data Dibaca: {len(hasil)}")
print(f"Total Baris Tabel Mentah : {total_baris}")
for k, v in hasil.items():
    print(f"- {k}: {len(v)} baris")