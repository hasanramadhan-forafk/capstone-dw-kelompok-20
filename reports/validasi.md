# Hasil Validasi Pipeline Data (Silver & Gold)

 tahap                         aturan              jenis                 hasil
Silver          keunikan_kunci_primer       keras (umum)                 LOLOS
Silver             rentang_satuan_sah       keras (umum)                 LOLOS
Silver           satu_satuan_per_seri       keras (umum)                 LOLOS
Silver               wilayah_kode_sah       keras (umum)                 LOLOS
Silver            kolom_wajib_lengkap       keras (umum)                 LOLOS
Silver             luas_tidak_negatif      keras (kasus)                 LOLOS
Silver              komponen_iklh_sah      keras (kasus)                 LOLOS
Silver       konsistensi_lahan_kritis      keras (kasus)                 LOLOS
Silver           deteksi_anomali_2020 peringatan (kasus) PERINGATAN (26 baris)
  Gold          gold_kunci_panel_unik       keras (gold)                 LOLOS
  Gold gold_satu_satuan_per_indikator       keras (gold)                 LOLOS
  Gold          gold_status_dan_nilai       keras (gold)                 LOLOS
  Gold      gold_tertelusur_ke_silver       keras (gold)                 LOLOS
  Gold         gold_nilai_sama_silver       keras (gold)                 LOLOS
  Gold       gold_tabel_nasional_unik       keras (gold)                 LOLOS
  Gold            rekon_kategori_baku       keras (gold)                 LOLOS
  Gold        rekon_selisih_konsisten       keras (gold)                 LOLOS