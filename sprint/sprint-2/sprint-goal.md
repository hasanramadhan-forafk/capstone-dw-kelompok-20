# Sprint 2 (23-29 November 2026) - Tim MBG (Kasus 20)

## Sprint Goal

Setiap sel panel Gold Kasus 20 yang terisi punya satu nilai yang tertelusur ke Silver, setiap indikator
punya satu satuan baku, Silver dan Gold tersimpan di DuckDB dengan kunci yang menolak sel ganda, dan
setiap baris rekonsiliasi berpasangan antara seri utama dan pembanding nasional punya kategori serta
penjelasan, sehingga Sprint 3 tinggal menguji revisi pembanding dan menulis laporan.

## Definition of Done yang dipakai

- [x] Reshape ke panel Gold provinsi x periode x indikator (tahap 4): `data/gold/panel.parquet`.
- [x] Silver dan Gold tersimpan di SQL beserta alasan pilihannya (tahap 5): `reports/basis-data.md`.
- [x] Tabel rekonsiliasi seri utama vs pembanding nasional, selisih dijelaskan (tahap 6):
  `reports/rekonsiliasi.md`.

## Bukti validasi Sprint 2 (bukan DoD tambahan)

- Aturan Gold dan rekonsiliasi berjalan otomatis dari `python pipeline.py` melalui
  `validasi.jalankan(silver, gold)`: kunci panel unik, satu satuan per indikator, setiap sel terisi
  tertelusur ke Silver, tabel nasional unik, kategori baku, setiap baris berpasangan berkategori, dan
  selisih konsisten.
- Hasil terakhir: **17 aturan, 16 LOLOS, 0 GAGAL, 1 PERINGATAN** (peringatan anomali 2020 yang sudah
  dikoreksi di Silver). Rincian di `reports/validasi.md`.
- Metrik: `results/124450013/metrics.json` memuat `aturan_validasi=17`, `aturan_lolos=16`,
  `aturan_peringatan=1`, dan metrik Sprint 1 `berkas_terverifikasi=13`.
