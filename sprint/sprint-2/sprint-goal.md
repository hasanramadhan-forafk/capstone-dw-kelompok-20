# Sprint 2 (23–29 November 2026) — Tim MBG (Kasus 20)

## Sprint Goal

Setiap sel panel Gold Kasus 20 punya satu nilai yang tertelusur ke Silver (atau kategori sel kosong), Silver dan Gold tersimpan di DuckDB dengan kunci yang menolak sel ganda, dan setiap selisih antara seri utama dan pembanding nasional punya kategori dan penjelasan, sehingga Sprint 3 tinggal menguji revisi pembanding dan menulis laporan.

## Definition of Done yang dipakai

- [x] Reshape ke panel Gold provinsi × periode × indikator (tahap 4): `data/gold/panel.parquet`.
- [x] Silver dan Gold tersimpan di SQL beserta alasan pilihannya (tahap 5): `reports/basis-data.md`.
- [x] Tabel rekonsiliasi seri utama vs pembanding nasional, selisih dijelaskan (tahap 6): `reports/rekonsiliasi.md`.
- [x] Validasi Gold dan Rekonsiliasi berjalan otomatis via pipeline dengan 8 aturan keras lolos.
