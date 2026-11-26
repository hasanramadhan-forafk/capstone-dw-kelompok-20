# Tabel rekonsiliasi seri utama vs pembanding nasional

Dihasilkan `python pipeline.py` (`src/gold/rekonsiliasi.py`) dari tabel nasional Gold. Selisih = nilai utama - nilai pembanding sesudah satuan disamakan; selisih relatif dalam persen terhadap pembanding. Periode tanpa pasangan tetap ditampilkan, tidak dihapus.

## Ringkasan per pasangan

| pasangan_id | seri_pembanding | jenis | periode | berpasangan | selisih_dihitung | median_selisih_relatif | kategori |
|---|---|---|---|---|---|---|---|
| P1 | AG.LND.FRST.K2 | selisih | 36 | 10 | 10 | 0.38 | tanpa pasangan (26), definisi berbeda (9), tidak berselisih (1) |
| P2 | AG.LND.FRST.ZS | selisih | 35 | 10 | 10 | 0.83 | tanpa pasangan (25), definisi berbeda (10) |
| P3 | EN.ATM.PM25.MC.M3 | konteks | 35 | 5 | 0 |  | tanpa pasangan (30), konteks berbeda (5) |
| P4 | tabel:sdg15_tutupan_hutan:luas_ribu_ha | selisih | 10 | 0 | 0 |  | tanpa pasangan (10) |

Baris berpasangan: 25; selisih dihitung: 20; median selisih relatif mutlak: 0.50%.

## Kategori

Kategori baku: *definisi berbeda*, *metode berbeda*, *vintage berbeda*, *cakupan berbeda*, *konteks berbeda*, *belum terjelaskan*, *tanpa pasangan*, *tidak berselisih*. Setiap baris berpasangan (`asal = keduanya`) wajib punya kategori dan penjelasan; ini diperiksa otomatis oleh `src/validasi/gold.py`.

## Rincian per pasangan

### P1: Luas hutan nasional: BPS (ribu ha) vs WDI (km persegi)

Jenis **selisih**; kategori baku: **definisi berbeda**. Definisi (tutupan lahan berhutan KLHK vs definisi FAO) setelah satuan diseragamkan (1 ribu ha = 10 km2).

| seri_pembanding | periode | nilai_utama | nilai_pembanding | selisih | selisih_relatif | asal | kategori | catatan |
|---|---|---|---|---|---|---|---|---|
| AG.LND.FRST.K2 | 1990 |  | 116,334.50 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 1991 |  | 113,896.91 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 1992 |  | 111,459.32 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 1993 |  | 109,021.73 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 1994 |  | 106,584.14 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 1995 |  | 104,146.55 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 1996 |  | 101,708.96 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 1997 |  | 99,271.37 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 1998 |  | 96,833.78 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 1999 |  | 94,396.19 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2000 |  | 91,958.60 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2001 |  | 92,393.26 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2002 |  | 92,827.92 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2003 |  | 93,262.58 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2004 |  | 93,697.24 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2005 |  | 94,131.90 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2006 |  | 94,566.56 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2007 |  | 95,001.22 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2008 |  | 95,435.88 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2009 |  | 95,870.54 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2010 |  | 96,305.20 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2011 |  | 96,049.74 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2012 |  | 95,794.28 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2013 |  | 95,538.82 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2014 | 95,766.40 | 95,283.36 | 483.04 | 0.51 | keduanya | definisi berbeda |  |
| AG.LND.FRST.K2 | 2015 | 95,028.00 | 95,027.90 | 0.10 | 0.00 | keduanya | definisi berbeda |  |
| AG.LND.FRST.K2 | 2016 | 95,271.90 | 95,134.70 | 137.20 | 0.14 | keduanya | definisi berbeda |  |
| AG.LND.FRST.K2 | 2017 | 93,949.70 | 95,241.50 | -1,291.80 | -1.36 | keduanya | definisi berbeda |  |
| AG.LND.FRST.K2 | 2018 | 93,526.20 | 95,348.30 | -1,822.10 | -1.91 | keduanya | definisi berbeda |  |
| AG.LND.FRST.K2 | 2019 | 94,114.10 | 95,455.10 | -1,341.00 | -1.40 | keduanya | definisi berbeda |  |
| AG.LND.FRST.K2 | 2020 | 95,561.90 | 95,561.90 | -0.00 | -0.00 | keduanya | tidak berselisih |  |
| AG.LND.FRST.K2 | 2021 | 95,335.30 | 95,643.38 | -308.08 | -0.32 | keduanya | definisi berbeda |  |
| AG.LND.FRST.K2 | 2022 | 95,969.30 | 95,724.86 | 244.44 | 0.26 | keduanya | definisi berbeda |  |
| AG.LND.FRST.K2 | 2023 | 96,231.40 | 95,806.34 | 425.06 | 0.44 | keduanya | definisi berbeda |  |
| AG.LND.FRST.K2 | 2024 |  | 95,887.82 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.K2 | 2025 |  | 95,969.30 |  |  | hanya_pembanding | tanpa pasangan |  |

### P2: Persentase hutan: BPS (terhadap penutupan lahan) vs WDI (terhadap luas daratan)

Jenis **selisih**; kategori baku: **definisi berbeda**. Definisi (penyebut: luas penutupan lahan vs luas daratan).

| seri_pembanding | periode | nilai_utama | nilai_pembanding | selisih | selisih_relatif | asal | kategori | catatan |
|---|---|---|---|---|---|---|---|---|
| AG.LND.FRST.ZS | 1990 |  | 64.22 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 1991 |  | 62.87 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 1992 |  | 61.53 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 1993 |  | 60.18 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 1994 |  | 58.84 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 1995 |  | 57.49 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 1996 |  | 56.14 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 1997 |  | 54.80 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 1998 |  | 53.45 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 1999 |  | 52.11 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2000 |  | 48.98 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2001 |  | 49.21 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2002 |  | 49.44 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2003 |  | 49.67 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2004 |  | 49.90 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2005 |  | 50.14 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2006 |  | 50.37 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2007 |  | 50.60 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2008 |  | 50.83 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2009 |  | 51.06 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2010 |  | 51.29 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2011 |  | 51.16 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2012 |  | 51.02 |  |  | hanya_pembanding | tanpa pasangan |  |
| AG.LND.FRST.ZS | 2013 |  | 50.89 |  |  | hanya_pembanding | tanpa pasangan |  |
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
| AG.LND.FRST.ZS | 2024 |  | 50.67 |  |  | hanya_pembanding | tanpa pasangan |  |

### P3: Indeks kualitas udara (BPS) vs PM2.5 (WDI): konteks

Jenis **konteks**; kategori baku: **konteks berbeda**. Arah berlawanan: indeks tinggi = baik, PM2.5 tinggi = buruk.

| seri_pembanding | periode | nilai_utama | nilai_pembanding | selisih | selisih_relatif | asal | kategori | catatan |
|---|---|---|---|---|---|---|---|---|
| EN.ATM.PM25.MC.M3 | 1990 |  | 31.38 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 1991 |  | 30.71 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 1992 |  | 30.24 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 1993 |  | 29.77 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 1994 |  | 29.30 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 1995 |  | 28.42 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 1996 |  | 28.35 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 1997 |  | 27.88 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 1998 |  | 27.41 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 1999 |  | 26.94 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2000 |  | 26.67 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2001 |  | 25.30 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2002 |  | 25.89 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2003 |  | 24.19 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2004 |  | 25.73 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2005 |  | 24.89 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2006 |  | 22.60 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2007 |  | 20.32 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2008 |  | 19.53 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2009 |  | 21.15 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2010 |  | 18.82 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2011 |  | 19.81 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2012 |  | 20.16 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2013 |  | 19.35 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2014 |  | 23.91 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2015 |  | 25.61 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2016 |  | 20.96 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2017 |  | 17.80 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2018 |  | 20.36 |  |  | hanya_pembanding | tanpa pasangan |  |
| EN.ATM.PM25.MC.M3 | 2019 | 86.56 | 23.97 |  |  | keduanya | konteks berbeda | pasangan konteks: selisih tidak dihitung |
| EN.ATM.PM25.MC.M3 | 2020 | 87.21 | 18.86 |  |  | keduanya | konteks berbeda | pasangan konteks: selisih tidak dihitung |
| EN.ATM.PM25.MC.M3 | 2021 | 87.36 | 19.99 |  |  | keduanya | konteks berbeda | pasangan konteks: selisih tidak dihitung |
| EN.ATM.PM25.MC.M3 | 2022 | 88.06 | 19.77 |  |  | keduanya | konteks berbeda | pasangan konteks: selisih tidak dihitung |
| EN.ATM.PM25.MC.M3 | 2023 | 88.67 | 20.84 |  |  | keduanya | konteks berbeda | pasangan konteks: selisih tidak dihitung |
| EN.ATM.PM25.MC.M3 | 2024 | 90.13 |  |  |  | hanya_utama | tanpa pasangan |  |

### P4: Kawasan hutan (var1304) vs tutupan hutan (tabel statis): dua tabel KLHK

Jenis **selisih**; kategori baku: **belum terjelaskan**. Sumber sama (rekalkulasi KLHK); jumlah luas seharusnya sama.

| seri_pembanding | periode | nilai_utama | nilai_pembanding | selisih | selisih_relatif | asal | kategori | catatan |
|---|---|---|---|---|---|---|---|---|
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2014 |  | 187,751.90 |  |  | hanya_pembanding | tanpa pasangan |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2015 |  | 187,751.90 |  |  | hanya_pembanding | tanpa pasangan |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2016 |  | 187,751.90 |  |  | hanya_pembanding | tanpa pasangan |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2017 |  | 187,751.90 |  |  | hanya_pembanding | tanpa pasangan |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2018 |  | 187,751.90 |  |  | hanya_pembanding | tanpa pasangan |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2019 |  | 187,751.90 |  |  | hanya_pembanding | tanpa pasangan |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2020 |  | 187,751.90 |  |  | hanya_pembanding | tanpa pasangan |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2021 |  | 187,679.10 |  |  | hanya_pembanding | tanpa pasangan |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2022 |  | 187,587.90 |  |  | hanya_pembanding | tanpa pasangan |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 2023 |  | 187,938.70 |  |  | hanya_pembanding | tanpa pasangan |  |
