# Tabel nasional dan pasangan rekonsiliasi

Dihasilkan `python pipeline.py` (`src/gold/nasional.py`) dari Silver dan `src/konfigurasi.py`. Selisih dihitung di Sprint 2; Sprint 1 memastikan setiap pasangan memang sebanding dan mencatat tahun yang beririsan.

Tabel nasional (periode x seri, rincian total, tampilan lebar): `reports/tabel-nasional.csv`. Kolom BPS hanya terisi pada tahun survei; itu bentuk datanya, tidak diisi.

## Ringkasan pasangan

| id | seri_utama | pembanding | jenis | periode_beririsan | tahun | dugaan_kategori |
|---|---|---|---|---|---|---|
| P1 | tabel:sdg15_tutupan_hutan:luas_ribu_ha | AG.LND.FRST.K2 [total] | selisih | 10 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 | definisi (tutupan lahan berhutan KLHK vs definisi FAO) setelah satuan diseragamkan (1 ribu ha = 10 km2) |
| P2 | tabel:sdg15_tutupan_hutan:persen | AG.LND.FRST.ZS [total] | selisih | 10 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 | definisi (penyebut: luas penutupan lahan vs luas daratan) |
| P3 | var2532 | EN.ATM.PM25.MC.M3 [total] | konteks | 5 | 2019, 2020, 2021, 2022, 2023 | arah berlawanan: indeks tinggi = baik, PM2.5 tinggi = buruk |
| P4 | var1304 | tabel:sdg15_tutupan_hutan:luas_ribu_ha [total] | selisih | 6 | 2014, 2015, 2016, 2017, 2018, 2023 | sumber sama (rekalkulasi KLHK); jumlah luas seharusnya sama |

## Rincian per pasangan

### P1: Luas hutan nasional: BPS (ribu ha) vs WDI (km persegi)
- Seri utama: `tabel:sdg15_tutupan_hutan:luas_ribu_ha` (rincian `tutupan=hutan`)
- Pembanding: `AG.LND.FRST.K2` (rincian `total`)
- Jenis: **selisih**; tahun beririsan: 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023
- Dugaan kategori selisih (diuji di Sprint 2): definisi (tutupan lahan berhutan KLHK vs definisi FAO) setelah satuan diseragamkan (1 ribu ha = 10 km2)

Pertanyaan keterbandingan dan jawabannya:

1. **Konversi?** 1 ribu hektar = 10 km persegi; dikerjakan di Gold.
2. **Definisi?** FAO: pohon >= 5 m, tanpa perkebunan (sourceNote); KLHK: kelas penutupan lahan hutan.

### P2: Persentase hutan: BPS (terhadap penutupan lahan) vs WDI (terhadap luas daratan)
- Seri utama: `tabel:sdg15_tutupan_hutan:persen` (rincian `tutupan=hutan`)
- Pembanding: `AG.LND.FRST.ZS` (rincian `total`)
- Jenis: **selisih**; tahun beririsan: 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023
- Dugaan kategori selisih (diuji di Sprint 2): definisi (penyebut: luas penutupan lahan vs luas daratan)

Pertanyaan keterbandingan dan jawabannya:

1. **Penyebut WDI?** Luas daratan (name WDI).
2. **Penyebut BPS?** Jumlah luas penutupan lahan provinsi (tabel).

### P3: Indeks kualitas udara (BPS) vs PM2.5 (WDI): konteks
- Seri utama: `var2532` (rincian `komponen=iku`)
- Pembanding: `EN.ATM.PM25.MC.M3` (rincian `total`)
- Jenis: **konteks**; tahun beririsan: 2019, 2020, 2021, 2022, 2023
- Dugaan kategori selisih (diuji di Sprint 2): arah berlawanan: indeks tinggi = baik, PM2.5 tinggi = buruk

Pertanyaan keterbandingan dan jawabannya:

1. **Arah?** IKU tinggi berarti udara baik; PM2.5 tinggi berarti buruk.

### P4: Kawasan hutan (var1304) vs tutupan hutan (tabel statis): dua tabel KLHK
- Seri utama: `var1304` (rincian `total`)
- Pembanding: `tabel:sdg15_tutupan_hutan:luas_ribu_ha` (rincian `total`)
- Jenis: **selisih**; tahun beririsan: 2014, 2015, 2016, 2017, 2018, 2023
- Dugaan kategori selisih (diuji di Sprint 2): sumber sama (rekalkulasi KLHK); jumlah luas seharusnya sama

Pertanyaan keterbandingan dan jawabannya:

1. **Apa beda keduanya?** var1304 dipecah menurut status kawasan, tabel statis menurut hutan/non hutan; jumlahnya luas yang sama.
