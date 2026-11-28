# Tabel rekonsiliasi seri utama vs pembanding nasional

Dihasilkan `python pipeline.py` (`src/gold/rekonsiliasi.py`) dari `data/gold/nasional.parquet`. Selisih = nilai utama − nilai pembanding; selisih relatif dalam persen terhadap pembanding. Periode tanpa pasangan tetap ditampilkan. Selisih tidak dihapus dan tidak dipaksa sama.

## Ringkasan per pasangan

| pasangan_id | seri_pembanding | jenis | periode | berpasangan | selisih_dihitung | median_selisih | median_selisih_relatif | kategori |
|---|---|---|---|---|---|---|---|---|
| P1 | AG.LND.FRST.K2 | selisih | 10 | 10 | 10 | 0.05 | 0.38 | definisi berbeda (9), tidak berselisih (1) |
| P2 | AG.LND.FRST.ZS | selisih | 10 | 10 | 10 | 0.02 | 0.83 | definisi berbeda (10) |
| P3 | EN.ATM.PM25.MC.M3 | konteks | 6 | 5 | 0 |  |  | definisi berbeda (6) |
| P4 | tabel:sdg15_tutupan_hutan:luas_ribu_ha | selisih | 10 | 6 | 6 | 0.00 | 0.00 | tidak berselisih (6), tanpa pasangan (4) |

Median selisih relatif mutlak, pasangan yang seri utamanya seri provinsi (BPS/BNPB): 0.29% (26 baris); semua pasangan termasuk antarpembanding: 0.29% (26 baris).

Periode pembanding di luar rentang seri utama yang tidak ditulis: P1 26, P2 25, P3 29.

## Kategori

Kategori baku: *definisi berbeda*, *metode berbeda*, *vintage berbeda*, *cakupan berbeda*, *belum terjelaskan*, *tanpa pasangan*, *tidak berselisih*. Kategori pasangan ditetapkan dari bukti di pasangan rekonsiliasi Sprint 1 (`reports/pasangan-rekonsiliasi.md`); baris satu sisi menjadi *tanpa pasangan*, baris yang angkanya sama menjadi *tidak berselisih*.

## Rincian per pasangan

### P1: Luas hutan nasional: BPS (ribu ha) vs WDI (km persegi)

Jenis **selisih**; kategori pasangan: **definisi berbeda**. Definisi (tutupan lahan berhutan KLHK vs definisi FAO) setelah satuan diseragamkan (1 ribu ha = 10 km2).

Rincian: BPS tutupan=hutan.

| seri_pembanding | periode | nilai_utama | nilai_pembanding | selisih | selisih_relatif | asal | kategori | catatan |
|---|---|---|---|---|---|---|---|---|
| AG.LND.FRST.K2 | 2014 | 95,766.40 | 95,283.36 | 483.04 | 0.51 | keduanya | definisi berbeda | satuan pembanding sudah dikonversi di Gold (km2 → ribu_hektar, faktor 0.1) |
| AG.LND.FRST.K2 | 2015 | 95,028.00 | 95,027.90 | 0.10 | 0.00 | keduanya | definisi berbeda | satuan pembanding sudah dikonversi di Gold (km2 → ribu_hektar, faktor 0.1) |
| AG.LND.FRST.K2 | 2016 | 95,271.90 | 95,134.70 | 137.20 | 0.14 | keduanya | definisi berbeda | satuan pembanding sudah dikonversi di Gold (km2 → ribu_hektar, faktor 0.1) |
| AG.LND.FRST.K2 | 2017 | 93,949.70 | 95,241.50 | -1,291.80 | -1.36 | keduanya | definisi berbeda | satuan pembanding sudah dikonversi di Gold (km2 → ribu_hektar, faktor 0.1) |
| AG.LND.FRST.K2 | 2018 | 93,526.20 | 95,348.30 | -1,822.10 | -1.91 | keduanya | definisi berbeda | satuan pembanding sudah dikonversi di Gold (km2 → ribu_hektar, faktor 0.1) |
| AG.LND.FRST.K2 | 2019 | 94,114.10 | 95,455.10 | -1,341.00 | -1.40 | keduanya | definisi berbeda | satuan pembanding sudah dikonversi di Gold (km2 → ribu_hektar, faktor 0.1) |
| AG.LND.FRST.K2 | 2020 | 95,561.90 | 95,561.90 | -0.00 | -0.00 | keduanya | tidak berselisih | satuan pembanding sudah dikonversi di Gold (km2 → ribu_hektar, faktor 0.1) |
| AG.LND.FRST.K2 | 2021 | 95,335.30 | 95,643.38 | -308.08 | -0.32 | keduanya | definisi berbeda | satuan pembanding sudah dikonversi di Gold (km2 → ribu_hektar, faktor 0.1) |
| AG.LND.FRST.K2 | 2022 | 95,969.30 | 95,724.86 | 244.44 | 0.26 | keduanya | definisi berbeda | satuan pembanding sudah dikonversi di Gold (km2 → ribu_hektar, faktor 0.1) |
| AG.LND.FRST.K2 | 2023 | 96,231.40 | 95,806.34 | 425.06 | 0.44 | keduanya | definisi berbeda | satuan pembanding sudah dikonversi di Gold (km2 → ribu_hektar, faktor 0.1) |

### P2: Persentase hutan: BPS (terhadap penutupan lahan) vs WDI (terhadap luas daratan)

Jenis **selisih**; kategori pasangan: **definisi berbeda**. Definisi (penyebut: luas penutupan lahan vs luas daratan).

Rincian: tutupan=hutan.

| seri_pembanding | periode | nilai_utama | nilai_pembanding | selisih | selisih_relatif | asal | kategori | catatan |
|---|---|---|---|---|---|---|---|---|
| AG.LND.FRST.ZS | 2014 | 51.00 | 50.75 | 0.25 | 0.49 | keduanya | definisi berbeda |  |
| AG.LND.FRST.ZS | 2015 | 50.60 | 50.61 | -0.01 | -0.03 | keduanya | definisi berbeda |  |
| AG.LND.FRST.ZS | 2016 | 50.70 | 50.67 | 0.03 | 0.06 | keduanya | definisi berbeda |  |
| AG.LND.FRST.ZS | 2017 | 50.00 | 50.73 | -0.73 | -1.43 | keduanya | definisi berbeda |  |
| AG.LND.FRST.ZS | 2018 | 49.80 | 50.78 | -0.98 | -1.94 | keduanya | definisi berbeda |  |
| AG.LND.FRST.ZS | 2019 | 50.10 | 50.84 | -0.74 | -1.46 | keduanya | definisi berbeda |  |
| AG.LND.FRST.ZS | 2020 | 50.90 | 50.90 | 0.00 | 0.00 | keduanya | definisi berbeda |  |
| AG.LND.FRST.ZS | 2021 | 50.80 | 50.54 | 0.26 | 0.52 | keduanya | definisi berbeda |  |
| AG.LND.FRST.ZS | 2022 | 51.20 | 50.58 | 0.62 | 1.23 | keduanya | definisi berbeda |  |
| AG.LND.FRST.ZS | 2023 | 51.20 | 50.63 | 0.57 | 1.13 | keduanya | definisi berbeda |  |

### P3: Indeks kualitas udara (BPS) vs PM2.5 (WDI): konteks

Jenis **konteks**; kategori pasangan: **definisi berbeda**. Arah berlawanan: indeks tinggi = baik, PM2.5 tinggi = buruk.

Rincian: komponen udara.

| seri_pembanding | periode | nilai_utama | nilai_pembanding | selisih | selisih_relatif | asal | kategori | catatan |
|---|---|---|---|---|---|---|---|---|
| EN.ATM.PM25.MC.M3 | 2019 | 86.56 | 23.97 |  |  | keduanya | definisi berbeda | pasangan konteks: selisih tidak dihitung |
| EN.ATM.PM25.MC.M3 | 2020 | 87.21 | 18.86 |  |  | keduanya | definisi berbeda | pasangan konteks: selisih tidak dihitung |
| EN.ATM.PM25.MC.M3 | 2021 | 87.36 | 19.99 |  |  | keduanya | definisi berbeda | pasangan konteks: selisih tidak dihitung |
| EN.ATM.PM25.MC.M3 | 2022 | 88.06 | 19.77 |  |  | keduanya | definisi berbeda | pasangan konteks: selisih tidak dihitung |
| EN.ATM.PM25.MC.M3 | 2023 | 88.67 | 20.84 |  |  | keduanya | definisi berbeda | pasangan konteks: selisih tidak dihitung |
| EN.ATM.PM25.MC.M3 | 2024 | 90.13 |  |  |  | hanya_utama | definisi berbeda |  |

### P4: Kawasan hutan (var1304) vs tutupan hutan (tabel statis): dua tabel KLHK

Jenis **selisih**; kategori pasangan: **belum terjelaskan**. Sumber sama (rekalkulasi KLHK); jumlah luas seharusnya sama.

Rincian: rincian jumlah.

| seri_pembanding | periode | nilai_utama | nilai_pembanding | selisih | selisih_relatif | asal | kategori | catatan |
|---|---|---|---|---|---|---|---|---|
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2014 | 187,751.90 | 187,751.90 | 0.00 | 0.00 | keduanya | tidak berselisih |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2015 | 187,751.90 | 187,751.90 | 0.00 | 0.00 | keduanya | tidak berselisih |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2016 | 187,751.90 | 187,751.90 | 0.00 | 0.00 | keduanya | tidak berselisih |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2017 | 187,751.90 | 187,751.90 | 0.00 | 0.00 | keduanya | tidak berselisih |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2018 | 187,751.90 | 187,751.90 | 0.00 | 0.00 | keduanya | tidak berselisih |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2019 |  | 187,751.90 |  |  | hanya_pembanding | tanpa pasangan |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2020 |  | 187,751.90 |  |  | hanya_pembanding | tanpa pasangan |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2021 |  | 187,679.10 |  |  | hanya_pembanding | tanpa pasangan |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2022 |  | 187,587.90 |  |  | hanya_pembanding | tanpa pasangan |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2023 | 187,938.70 | 187,938.70 | 0.00 | 0.00 | keduanya | tidak berselisih |  |
