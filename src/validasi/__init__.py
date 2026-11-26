"""Orkestrator Validasi: menjalankan aturan.py, khusus.py (Silver), dan gold.py (Gold)."""
from pathlib import Path
import pandas as pd
from src.validasi import aturan, khusus, gold as validasi_gold

def jalankan(silver: pd.DataFrame, gold=None) -> pd.DataFrame:
    if not isinstance(silver, pd.DataFrame):
        path_silver = Path(__file__).resolve().parents[2] / "data" / "silver" / "silver.parquet"
        silver = pd.read_parquet(path_silver)

    hasil = []

    # ==============================================================
    # 1. ATURAN VALIDASI SILVER
    # ==============================================================
    hasil.append({"tahap": "Silver", "aturan": "keunikan_kunci_primer", "jenis": "keras (umum)", 
                  "hasil": "LOLOS" if aturan.cek_keunikan_kunci(silver) else "GAGAL"})
    hasil.append({"tahap": "Silver", "aturan": "rentang_satuan_sah", "jenis": "keras (umum)", 
                  "hasil": "LOLOS" if aturan.cek_rentang_satuan(silver) else "GAGAL"})
    hasil.append({"tahap": "Silver", "aturan": "satu_satuan_per_seri", "jenis": "keras (umum)", 
                  "hasil": "LOLOS" if aturan.cek_satuan_seragam(silver) else "GAGAL"})
    hasil.append({"tahap": "Silver", "aturan": "wilayah_kode_sah", "jenis": "keras (umum)", 
                  "hasil": "LOLOS" if aturan.cek_wilayah_sah(silver) else "GAGAL"})
    hasil.append({"tahap": "Silver", "aturan": "kolom_wajib_lengkap", "jenis": "keras (umum)", 
                  "hasil": "LOLOS" if aturan.cek_tidak_ada_null(silver) else "GAGAL"})

    gagal_luas = khusus.luas_tidak_negatif(silver)
    hasil.append({"tahap": "Silver", "aturan": "luas_tidak_negatif", "jenis": "keras (kasus)", 
                  "hasil": "LOLOS" if gagal_luas.empty else f"GAGAL ({len(gagal_luas)} baris)"})

    gagal_iklh = khusus.komponen_iklh_sah(silver)
    hasil.append({"tahap": "Silver", "aturan": "komponen_iklh_sah", "jenis": "keras (kasus)", 
                  "hasil": "LOLOS" if gagal_iklh.empty else f"GAGAL ({len(gagal_iklh)} baris)"})

    gagal_588 = khusus.konsistensi_lahan_kritis(silver)
    hasil.append({"tahap": "Silver", "aturan": "konsistensi_lahan_kritis", "jenis": "keras (kasus)", 
                  "hasil": "LOLOS" if gagal_588.empty else f"GAGAL ({len(gagal_588)} baris)"})

    anomali_2020 = khusus.deteksi_kolom_2020_tergeser(silver)
    hasil.append({"tahap": "Silver", "aturan": "deteksi_anomali_2020", "jenis": "peringatan (kasus)", 
                  "hasil": f"PERINGATAN ({len(anomali_2020)} baris)" if not anomali_2020.empty else "LOLOS"})

    # ==============================================================
    # 2. ATURAN VALIDASI GOLD (Sprint 2)
    # ==============================================================
    if isinstance(gold, dict) and any(k in gold for k in ["panel", "nasional", "rekonsiliasi"]):
        g_panel_unik = validasi_gold.kunci_panel_unik(silver, gold)
        hasil.append({"tahap": "Gold", "aturan": "gold_kunci_panel_unik", "jenis": "keras (gold)",
                      "hasil": "LOLOS" if g_panel_unik.empty else f"GAGAL ({len(g_panel_unik)} baris)"})

        g_satuan = validasi_gold.satu_satuan_per_indikator(silver, gold)
        hasil.append({"tahap": "Gold", "aturan": "gold_satu_satuan_per_indikator", "jenis": "keras (gold)",
                      "hasil": "LOLOS" if g_satuan.empty else f"GAGAL ({len(g_satuan)} baris)"})

        g_status = validasi_gold.status_dan_nilai_konsisten(silver, gold)
        hasil.append({"tahap": "Gold", "aturan": "gold_status_dan_nilai", "jenis": "keras (gold)",
                      "hasil": "LOLOS" if g_status.empty else f"GAGAL ({len(g_status)} baris)"})

        g_telusur = validasi_gold.tertelusur_ke_silver(silver, gold)
        hasil.append({"tahap": "Gold", "aturan": "gold_tertelusur_ke_silver", "jenis": "keras (gold)",
                      "hasil": "LOLOS" if g_telusur.empty else f"GAGAL ({len(g_telusur)} baris)"})

        g_nilai = validasi_gold.nilai_sama_dengan_silver(silver, gold)
        hasil.append({"tahap": "Gold", "aturan": "gold_nilai_sama_silver", "jenis": "keras (gold)",
                      "hasil": "LOLOS" if g_nilai.empty else f"GAGAL ({len(g_nilai)} baris)"})

        g_nasional = validasi_gold.tabel_nasional_unik(silver, gold)
        hasil.append({"tahap": "Gold", "aturan": "gold_tabel_nasional_unik", "jenis": "keras (gold)",
                      "hasil": "LOLOS" if g_nasional.empty else f"GAGAL ({len(g_nasional)} baris)"})

        g_rekon_kat = validasi_gold.rekonsiliasi_kategori_baku(silver, gold)
        hasil.append({"tahap": "Gold", "aturan": "rekon_kategori_baku", "jenis": "keras (gold)",
                      "hasil": "LOLOS" if g_rekon_kat.empty else f"GAGAL ({len(g_rekon_kat)} baris)"})

        g_rekon_sel = validasi_gold.rekonsiliasi_selisih_konsisten(silver, gold)
        hasil.append({"tahap": "Gold", "aturan": "rekon_selisih_konsisten", "jenis": "keras (gold)",
                      "hasil": "LOLOS" if g_rekon_sel.empty else f"GAGAL ({len(g_rekon_sel)} baris)"})

    df_hasil = pd.DataFrame(hasil)

    # Cetak hasil ke layar terminal
    print("\n" + "=" * 65)
    print("               HASIL VALIDASI DATA (SILVER & GOLD)")
    print("=" * 65)
    for _, r in df_hasil.iterrows():
        simbol = "✓" if r["hasil"] == "LOLOS" else ("!" if "PERINGATAN" in r["hasil"] else "✗")
        print(f" [{simbol}] [{r['tahap']:<6}] {r['aturan']:<30} [{r['jenis']}]: {r['hasil']}")
    print("=" * 65)

    # Tulis laporan ke reports/validasi.md
    path_reports = Path(__file__).resolve().parents[2] / "reports"
    path_reports.mkdir(parents=True, exist_ok=True)
    with open(path_reports / "validasi.md", "w", encoding="utf-8") as f:
        f.write("# Hasil Validasi Pipeline Data (Silver & Gold)\n\n")
        try:
            f.write(df_hasil.to_markdown(index=False))
        except Exception:
            f.write(df_hasil.to_string(index=False))

    return df_hasil
