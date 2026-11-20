"""Orkestrator Validasi: menjalankan aturan.py dan khusus.py."""
from pathlib import Path
import pandas as pd
from src.validasi import aturan, khusus


def jalankan(silver: pd.DataFrame, gold=None) -> pd.DataFrame:
    if not isinstance(silver, pd.DataFrame):
        path_silver = Path(__file__).resolve().parents[2] / "data" / "silver" / "silver.parquet"
        silver = pd.read_parquet(path_silver)

    hasil = []

    # 1. Jalankan Aturan Umum (Keras) dari aturan.py
    hasil.append({"aturan": "keunikan_kunci_primer", "jenis": "keras (umum)", 
                  "hasil": "LOLOS" if aturan.cek_keunikan_kunci(silver) else "GAGAL"})
    hasil.append({"aturan": "rentang_satuan_sah", "jenis": "keras (umum)", 
                  "hasil": "LOLOS" if aturan.cek_rentang_satuan(silver) else "GAGAL"})
    hasil.append({"aturan": "satu_satuan_per_seri", "jenis": "keras (umum)", 
                  "hasil": "LOLOS" if aturan.cek_satuan_seragam(silver) else "GAGAL"})
    hasil.append({"aturan": "wilayah_kode_sah", "jenis": "keras (umum)", 
                  "hasil": "LOLOS" if aturan.cek_wilayah_sah(silver) else "GAGAL"})
    hasil.append({"aturan": "kolom_wajib_lengkap", "jenis": "keras (umum)", 
                  "hasil": "LOLOS" if aturan.cek_tidak_ada_null(silver) else "GAGAL"})

    # 2. Jalankan Aturan Khusus Kasus 20 dari khusus.py
    gagal_luas = khusus.luas_tidak_negatif(silver)
    hasil.append({"aturan": "luas_tidak_negatif", "jenis": "keras (kasus)", 
                  "hasil": "LOLOS" if gagal_luas.empty else f"GAGAL ({len(gagal_luas)} baris)"})

    gagal_iklh = khusus.komponen_iklh_sah(silver)
    hasil.append({"aturan": "komponen_iklh_sah", "jenis": "keras (kasus)", 
                  "hasil": "LOLOS" if gagal_iklh.empty else f"GAGAL ({len(gagal_iklh)} baris)"})

    gagal_588 = khusus.konsistensi_lahan_kritis(silver)
    hasil.append({"aturan": "konsistensi_lahan_kritis", "jenis": "keras (kasus)", 
                  "hasil": "LOLOS" if gagal_588.empty else f"GAGAL ({len(gagal_588)} baris)"})

    anomali_2020 = khusus.deteksi_kolom_2020_tergeser(silver)
    hasil.append({"aturan": "deteksi_anomali_2020", "jenis": "peringatan (kasus)", 
                  "hasil": f"PERINGATAN ({len(anomali_2020)} baris)" if not anomali_2020.empty else "LOLOS"})

    df_hasil = pd.DataFrame(hasil)

    # Cetak hasil ke layar terminal
    print("\n" + "=" * 60)
    print("               HASIL VALIDASI SILVER")
    print("=" * 60)
    for _, r in df_hasil.iterrows():
        simbol = "✓" if r["hasil"] == "LOLOS" else ("!" if "PERINGATAN" in r["hasil"] else "✗")
        print(f" [{simbol}] {r['aturan']:<28} [{r['jenis']}]: {r['hasil']}")
    print("=" * 60)

    # Tulis laporan ke reports/validasi.md
    path_reports = Path(__file__).resolve().parents[2] / "reports"
    path_reports.mkdir(parents=True, exist_ok=True)
    with open(path_reports / "validasi.md", "w", encoding="utf-8") as f:
        f.write("# Hasil Validasi Silver\n\n")
        f.write(df_hasil.to_markdown(index=False))

    return df_hasil