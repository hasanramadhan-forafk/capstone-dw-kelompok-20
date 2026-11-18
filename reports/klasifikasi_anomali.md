# Tahap 3: kategori calon anomali, perbaikan galat input, dan deduplikasi

Sumber: `reports/tabel/calon_anomali.csv` (Tahap 2) dan `data/silver/silver.parquet`. Hanya galat input yang terbukti oleh identitas independen yang diperbaiki; outlier asli dan patahan ditandai dan dijelaskan.

## Definisi kategori

- **galat_input**: nilai salah karena proses input, dibuktikan oleh identitas (jumlah rincian = total, persen = luas/total, nilai milik provinsi lain, atau geser desimal). Status `diperbaiki` hanya bila lolos gerbang bukti; `dugaan_tidak_diperbaiki` bila hanya ada kecurigaan.
- **patahan**: perubahan cakupan atau metode: pemekaran provinsi, atau lonjakan serentak (≥50% provinsi melewati ambang pada tahun yang sama, ≥80% searah). Tidak diperbaiki.
- **outlier_asli**: nilai ekstrem tanpa bukti galat atau patahan. Tidak diperbaiki.

## Ringkasan

| seri | jenis | galat_input | outlier_asli | patahan |
|---|---|---|---|---|
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | antar_provinsi | 7 | 84 | 13 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | loncatan | 111 | 62 | 4 |
| tabel:sdg15_tutupan_hutan:persen | loncatan | 99 | 67 | 3 |
| var1304 | antar_provinsi | 0 | 46 | 10 |
| var1304 | loncatan | 1 | 4 | 1 |
| var2532 | antar_provinsi | 0 | 50 | 0 |
| var2532 | loncatan | 1 | 96 | 0 |
| var588 | antar_provinsi | 0 | 31 | 0 |
| var588 | loncatan | 1 | 34 | 0 |

Total calon anomali: 725; terpetakan ke Silver: 725.

## Perbaikan galat input

| seri_kode | rincian | wilayah_kode | tahun | nilai_asal | nilai_baru | aturan | nama_wilayah |
|---|---|---|---|---|---|---|---|
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 3100 | 2020 | 152.9 | 0.9 | A1_pertukaran_antarprovinsi | DKI JAKARTA |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 3100 | 2020 | 786.3 | 64.4 | A1_pertukaran_antarprovinsi | DKI JAKARTA |
| tabel:sdg15_tutupan_hutan:persen | hutan | 3100 | 2020 | 16.3 | 1.4 | A1_pertukaran_antarprovinsi | DKI JAKARTA |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 3100 | 2020 | 83.7 | 98.6 | A1_pertukaran_antarprovinsi | DKI JAKARTA |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 3600 | 2020 | 1192.6 | 152.9 | A1_pertukaran_antarprovinsi | BANTEN |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 3600 | 2020 | 3645.1 | 786.3 | A1_pertukaran_antarprovinsi | BANTEN |
| tabel:sdg15_tutupan_hutan:persen | hutan | 3600 | 2020 | 24.7 | 16.3 | A1_pertukaran_antarprovinsi | BANTEN |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 3600 | 2020 | 75.3 | 83.7 | A1_pertukaran_antarprovinsi | BANTEN |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 3500 | 2020 | 20.3 | 1192.6 | A1_pertukaran_antarprovinsi | JAWA TIMUR |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 3500 | 2020 | 299.1 | 3645.1 | A1_pertukaran_antarprovinsi | JAWA TIMUR |
| tabel:sdg15_tutupan_hutan:persen | hutan | 3500 | 2020 | 6.4 | 24.7 | A1_pertukaran_antarprovinsi | JAWA TIMUR |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 3500 | 2020 | 93.6 | 75.3 | A1_pertukaran_antarprovinsi | JAWA TIMUR |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 3400 | 2020 | 634.5 | 20.3 | A1_pertukaran_antarprovinsi | DI YOGYAKARTA |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 3400 | 2020 | 2822.1 | 299.1 | A1_pertukaran_antarprovinsi | DI YOGYAKARTA |
| tabel:sdg15_tutupan_hutan:persen | hutan | 3400 | 2020 | 18.4 | 6.4 | A1_pertukaran_antarprovinsi | DI YOGYAKARTA |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 3400 | 2020 | 81.6 | 93.6 | A1_pertukaran_antarprovinsi | DI YOGYAKARTA |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 3300 | 2020 | 710.4 | 634.5 | A1_pertukaran_antarprovinsi | JAWA TENGAH |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 3300 | 2020 | 2988.2 | 2822.1 | A1_pertukaran_antarprovinsi | JAWA TENGAH |
| tabel:sdg15_tutupan_hutan:persen | hutan | 3300 | 2020 | 19.2 | 18.4 | A1_pertukaran_antarprovinsi | JAWA TENGAH |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 3300 | 2020 | 80.8 | 81.6 | A1_pertukaran_antarprovinsi | JAWA TENGAH |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 3200 | 2020 | 0.9 | 710.4 | A1_pertukaran_antarprovinsi | JAWA BARAT |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 3200 | 2020 | 64.4 | 2988.2 | A1_pertukaran_antarprovinsi | JAWA BARAT |
| tabel:sdg15_tutupan_hutan:persen | hutan | 3200 | 2020 | 1.4 | 19.2 | A1_pertukaran_antarprovinsi | JAWA BARAT |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 3200 | 2020 | 98.6 | 80.8 | A1_pertukaran_antarprovinsi | JAWA BARAT |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 7200 | 2020 | 837.6 | 3802.4 | A1_pertukaran_antarprovinsi | SULAWESI TENGAH |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 7200 | 2020 | 842.6 | 2232.3 | A1_pertukaran_antarprovinsi | SULAWESI TENGAH |
| tabel:sdg15_tutupan_hutan:persen | hutan | 7200 | 2020 | 49.9 | 63.0 | A1_pertukaran_antarprovinsi | SULAWESI TENGAH |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 7200 | 2020 | 50.1 | 37.0 | A1_pertukaran_antarprovinsi | SULAWESI TENGAH |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 7600 | 2020 | 1725.4 | 837.6 | A1_pertukaran_antarprovinsi | SULAWESI BARAT |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 7600 | 2020 | 2997.1 | 842.6 | A1_pertukaran_antarprovinsi | SULAWESI BARAT |
| tabel:sdg15_tutupan_hutan:persen | hutan | 7600 | 2020 | 36.5 | 49.9 | A1_pertukaran_antarprovinsi | SULAWESI BARAT |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 7600 | 2020 | 63.5 | 50.1 | A1_pertukaran_antarprovinsi | SULAWESI BARAT |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 5300 | 2020 | 7459.3 | 1725.4 | A1_pertukaran_antarprovinsi | NUSA TENGGARA TIMUR |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 5300 | 2020 | 7806.9 | 2997.1 | A1_pertukaran_antarprovinsi | NUSA TENGGARA TIMUR |
| tabel:sdg15_tutupan_hutan:persen | hutan | 5300 | 2020 | 48.9 | 36.5 | A1_pertukaran_antarprovinsi | NUSA TENGGARA TIMUR |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 5300 | 2020 | 51.1 | 63.5 | A1_pertukaran_antarprovinsi | NUSA TENGGARA TIMUR |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 6200 | 2020 | 560.0 | 7459.3 | A1_pertukaran_antarprovinsi | KALIMANTAN TENGAH |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 6200 | 2020 | 879.5 | 7806.9 | A1_pertukaran_antarprovinsi | KALIMANTAN TENGAH |
| tabel:sdg15_tutupan_hutan:persen | hutan | 6200 | 2020 | 38.9 | 48.9 | A1_pertukaran_antarprovinsi | KALIMANTAN TENGAH |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 6200 | 2020 | 61.1 | 51.1 | A1_pertukaran_antarprovinsi | KALIMANTAN TENGAH |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 7100 | 2020 | 1891.2 | 560.0 | A1_pertukaran_antarprovinsi | SULAWESI UTARA |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 7100 | 2020 | 1720.4 | 879.5 | A1_pertukaran_antarprovinsi | SULAWESI UTARA |
| tabel:sdg15_tutupan_hutan:persen | hutan | 7100 | 2020 | 52.4 | 38.9 | A1_pertukaran_antarprovinsi | SULAWESI UTARA |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 7100 | 2020 | 47.6 | 61.1 | A1_pertukaran_antarprovinsi | SULAWESI UTARA |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 7400 | 2020 | 97.5 | 1891.2 | A1_pertukaran_antarprovinsi | SULAWESI TENGGARA |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 7400 | 2020 | 469.4 | 1720.4 | A1_pertukaran_antarprovinsi | SULAWESI TENGGARA |
| tabel:sdg15_tutupan_hutan:persen | hutan | 7400 | 2020 | 17.2 | 52.4 | A1_pertukaran_antarprovinsi | SULAWESI TENGGARA |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 7400 | 2020 | 82.8 | 47.6 | A1_pertukaran_antarprovinsi | SULAWESI TENGGARA |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 5100 | 2020 | 5656.6 | 97.5 | A1_pertukaran_antarprovinsi | BALI |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 5100 | 2020 | 8916.2 | 469.4 | A1_pertukaran_antarprovinsi | BALI |
| tabel:sdg15_tutupan_hutan:persen | hutan | 5100 | 2020 | 38.8 | 17.2 | A1_pertukaran_antarprovinsi | BALI |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 5100 | 2020 | 61.2 | 82.8 | A1_pertukaran_antarprovinsi | BALI |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 6100 | 2020 | 13289.5 | 5656.6 | A1_pertukaran_antarprovinsi | KALIMANTAN BARAT |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 6100 | 2020 | 6215.3 | 8916.2 | A1_pertukaran_antarprovinsi | KALIMANTAN BARAT |
| tabel:sdg15_tutupan_hutan:persen | hutan | 6100 | 2020 | 68.1 | 38.8 | A1_pertukaran_antarprovinsi | KALIMANTAN BARAT |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 6100 | 2020 | 31.9 | 61.2 | A1_pertukaran_antarprovinsi | KALIMANTAN BARAT |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 6400 | 2020 | 3802.4 | 13289.5 | A1_pertukaran_antarprovinsi | KALIMANTAN TIMUR |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 6400 | 2020 | 2232.3 | 6215.3 | A1_pertukaran_antarprovinsi | KALIMANTAN TIMUR |
| tabel:sdg15_tutupan_hutan:persen | hutan | 6400 | 2020 | 63.0 | 68.1 | A1_pertukaran_antarprovinsi | KALIMANTAN TIMUR |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 6400 | 2020 | 37.0 | 31.9 | A1_pertukaran_antarprovinsi | KALIMANTAN TIMUR |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 1700 | 2020 | 191.9 | 665.0 | A1_pertukaran_antarprovinsi | BENGKULU |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 1700 | 2020 | 1467.8 | 1337.9 | A1_pertukaran_antarprovinsi | BENGKULU |
| tabel:sdg15_tutupan_hutan:persen | hutan | 1700 | 2020 | 11.6 | 33.2 | A1_pertukaran_antarprovinsi | BENGKULU |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 1700 | 2020 | 88.4 | 66.8 | A1_pertukaran_antarprovinsi | BENGKULU |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 1900 | 2020 | 344.2 | 191.9 | A1_pertukaran_antarprovinsi | KEP. BANGKA BELITUNG |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 1900 | 2020 | 3091.2 | 1467.8 | A1_pertukaran_antarprovinsi | KEP. BANGKA BELITUNG |
| tabel:sdg15_tutupan_hutan:persen | hutan | 1900 | 2020 | 10.0 | 11.6 | A1_pertukaran_antarprovinsi | KEP. BANGKA BELITUNG |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 1900 | 2020 | 90.0 | 88.4 | A1_pertukaran_antarprovinsi | KEP. BANGKA BELITUNG |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 1800 | 2020 | 665.0 | 344.2 | A1_pertukaran_antarprovinsi | LAMPUNG |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 1800 | 2020 | 1337.9 | 3091.2 | A1_pertukaran_antarprovinsi | LAMPUNG |
| tabel:sdg15_tutupan_hutan:persen | hutan | 1800 | 2020 | 33.2 | 10.0 | A1_pertukaran_antarprovinsi | LAMPUNG |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 1800 | 2020 | 66.8 | 90.0 | A1_pertukaran_antarprovinsi | LAMPUNG |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 8200 | 2020 | 3075.5 | 2023.2 | A1_pertukaran_antarprovinsi | MALUKU UTARA |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 8200 | 2020 | 1546.6 | 1107.4 | A1_pertukaran_antarprovinsi | MALUKU UTARA |
| tabel:sdg15_tutupan_hutan:persen | hutan | 8200 | 2020 | 66.5 | 64.6 | A1_pertukaran_antarprovinsi | MALUKU UTARA |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 8200 | 2020 | 33.5 | 35.4 | A1_pertukaran_antarprovinsi | MALUKU UTARA |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 8100 | 2020 | 2023.2 | 3075.5 | A1_pertukaran_antarprovinsi | MALUKU |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 8100 | 2020 | 1107.4 | 1546.6 | A1_pertukaran_antarprovinsi | MALUKU |
| tabel:sdg15_tutupan_hutan:persen | hutan | 8100 | 2020 | 64.6 | 66.5 | A1_pertukaran_antarprovinsi | MALUKU |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 8100 | 2020 | 35.4 | 33.5 | A1_pertukaran_antarprovinsi | MALUKU |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 5200 | 2020 | 948.5 | 869.6 | A1_pertukaran_antarprovinsi | NUSA TENGGARA BARAT |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 5200 | 2020 | 2765.4 | 1110.6 | A1_pertukaran_antarprovinsi | NUSA TENGGARA BARAT |
| tabel:sdg15_tutupan_hutan:persen | hutan | 5200 | 2020 | 25.5 | 43.9 | A1_pertukaran_antarprovinsi | NUSA TENGGARA BARAT |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 5200 | 2020 | 74.5 | 56.1 | A1_pertukaran_antarprovinsi | NUSA TENGGARA BARAT |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 6300 | 2020 | 731.1 | 948.5 | A1_pertukaran_antarprovinsi | KALIMANTAN SELATAN |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 6300 | 2020 | 467.4 | 2765.4 | A1_pertukaran_antarprovinsi | KALIMANTAN SELATAN |
| tabel:sdg15_tutupan_hutan:persen | hutan | 6300 | 2020 | 61.0 | 25.5 | A1_pertukaran_antarprovinsi | KALIMANTAN SELATAN |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 6300 | 2020 | 39.0 | 74.5 | A1_pertukaran_antarprovinsi | KALIMANTAN SELATAN |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 7500 | 2020 | 869.6 | 731.1 | A1_pertukaran_antarprovinsi | GORONTALO |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 7500 | 2020 | 1110.6 | 467.4 | A1_pertukaran_antarprovinsi | GORONTALO |
| tabel:sdg15_tutupan_hutan:persen | hutan | 7500 | 2020 | 43.9 | 61.0 | A1_pertukaran_antarprovinsi | GORONTALO |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 7500 | 2020 | 56.1 | 39.0 | A1_pertukaran_antarprovinsi | GORONTALO |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 9400 | 2020 | 8967.3 | 25396.6 | A1_pertukaran_antarprovinsi | PAPUA |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 9400 | 2020 | 657.6 | 5680.3 | A1_pertukaran_antarprovinsi | PAPUA |
| tabel:sdg15_tutupan_hutan:persen | hutan | 9400 | 2020 | 93.2 | 81.7 | A1_pertukaran_antarprovinsi | PAPUA |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 9400 | 2020 | 6.8 | 18.3 | A1_pertukaran_antarprovinsi | PAPUA |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | 9100 | 2020 | 25396.6 | 8967.3 | A1_pertukaran_antarprovinsi | PAPUA BARAT |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | 9100 | 2020 | 5680.3 | 657.6 | A1_pertukaran_antarprovinsi | PAPUA BARAT |
| tabel:sdg15_tutupan_hutan:persen | hutan | 9100 | 2020 | 81.7 | 93.2 | A1_pertukaran_antarprovinsi | PAPUA BARAT |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 9100 | 2020 | 18.3 | 6.8 | A1_pertukaran_antarprovinsi | PAPUA BARAT |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | total | 3400 | 2016 | 3194.0 | 319.4 | A2_geser_desimal_pada_total | DI YOGYAKARTA |
| var1304 | total | 3400 | 2016 | 3194.0 | 319.4 | A2_geser_desimal_pada_total | DI YOGYAKARTA |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | 9400 | 2018 | 19.0 | 19.6 | A3_persen_tidak_berjumlah_100 | PAPUA |

Bukti tiap aturan ada di `reports/tabel/perbaikan_galat.csv`.
Catatan hitungan: `perbaikan_galat.csv` memuat 103 sel (A1 100, A2 2, A3 1). Sembilan di antaranya (8 sel A1 dan 1 sel A3) tidak ada di daftar calon anomali Tahap 2: sel A1 tersebut ikut dipindah karena perbaikan A1 memindahkan satu blok provinsi utuh (luas dan persen) meski nilainya sendiri tidak cukup ekstrem untuk masuk profil, sedangkan sel A3 ditemukan lewat uji identitas persen. Sebaliknya, satu sel bisa muncul dua kali di daftar Tahap 2 (jenis antar_provinsi dan loncatan), sehingga jumlah baris berstatus `diperbaiki` (100) tidak sama dengan jumlah sel unik yang diperbaiki.


## Uji identitas sebelum dan sesudah perbaikan

| uji | sebelum | sesudah |
|---|---|---|
| jumlah provinsi vs Indonesia (>0,5%) | 2 | 0 |
| jumlah rincian: tabel:sdg15_tutupan_hutan:luas_ribu_ha | 27 | 1 |
| jumlah rincian: tabel:sdg15_tutupan_hutan:persen | 1 | 0 |
| jumlah rincian: var1304 | 1 | 0 |
| jumlah rincian: var588 | 0 | 0 |
| persen vs luas/total | 53 | 0 |

## Patahan serentak (hasil deteksi)

_tidak ada tahun yang memenuhi kriteria serentak_

Daftar semua tahun: `reports/tabel/patahan_serentak.csv`.

## Deduplikasi

- Kunci unik: sumber + seri + wilayah + periode + rincian (+ berkas).
- Angka **sama** dari dua berkas/snapshot bukan duplikat yang salah: satu dipertahankan, lineage dicatat.
- Angka **berbeda** adalah revisi: keduanya dipertahankan, dibedakan oleh `_berkas_raw`, tidak dirata-rata.
- Hasil pada Silver sekarang: 0 kunci ganda.

## Daftar galat_input (220)

| seri | rincian_silver | wilayah | periode | jenis | subkategori | status_galat |
|---|---|---|---|---|---|---|
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | BALI | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | BALI | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | BANTEN | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | BANTEN | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | BENGKULU | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | BENGKULU | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | DI YOGYAKARTA | 2016 | loncatan | dugaan_lonjakan_sesaat | dugaan_tidak_diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | DI YOGYAKARTA | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | DI YOGYAKARTA | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | DKI JAKARTA | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | DKI JAKARTA | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | GORONTALO | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | GORONTALO | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAWA BARAT | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAWA BARAT | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAWA TENGAH | 2015 | loncatan | dugaan_lonjakan_sesaat | dugaan_tidak_diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAWA TENGAH | 2016 | loncatan | dugaan_lonjakan_sesaat | dugaan_tidak_diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAWA TENGAH | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAWA TIMUR | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAWA TIMUR | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN BARAT | 2020 | antar_provinsi | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN BARAT | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN BARAT | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN SELATAN | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN SELATAN | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TENGAH | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TENGAH | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TIMUR | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TIMUR | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KEP. BANGKA BELITUNG | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KEP. BANGKA BELITUNG | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | LAMPUNG | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | LAMPUNG | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | MALUKU | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | MALUKU | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | MALUKU UTARA | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | MALUKU UTARA | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | NUSA TENGGARA BARAT | 2016 | loncatan | dugaan_lonjakan_sesaat | dugaan_tidak_diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | NUSA TENGGARA BARAT | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | NUSA TENGGARA BARAT | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | NUSA TENGGARA TIMUR | 2016 | loncatan | dugaan_lonjakan_sesaat | dugaan_tidak_diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | NUSA TENGGARA TIMUR | 2020 | antar_provinsi | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | NUSA TENGGARA TIMUR | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | NUSA TENGGARA TIMUR | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA | 2020 | antar_provinsi | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA BARAT | 2020 | antar_provinsi | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA BARAT | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA BARAT | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | SULAWESI BARAT | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | SULAWESI BARAT | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | SULAWESI TENGAH | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | SULAWESI TENGAH | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | SULAWESI TENGGARA | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | SULAWESI TENGGARA | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | SULAWESI UTARA | 2020 | loncatan | A1_pertukaran_antarprovinsi | diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | SULAWESI UTARA | 2021 | loncatan | akibat_galat_periode_sebelumnya | ikut_terbenahi |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | SUMATERA SELATAN | 2015 | loncatan | dugaan_lonjakan_sesaat | dugaan_tidak_diperbaiki |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | total | DI YOGYAKARTA | 2016 | loncatan | A2_geser_desimal_pada_total | diperbaiki |

Daftar lengkap: `reports/tabel/anomali_berkategori.csv`.

## Daftar patahan (31)

| seri | rincian_silver | wilayah | periode | jenis | subkategori | status_galat |
|---|---|---|---|---|---|---|
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TIMUR | 2014 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TIMUR | 2015 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TIMUR | 2016 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TIMUR | 2017 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TIMUR | 2018 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TIMUR | 2019 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA | 2023 | loncatan | cakupan_berubah_pemekaran_papua_2022 |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA BARAT | 2023 | loncatan | cakupan_berubah_pemekaran_papua_2022 |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | total | KALIMANTAN TIMUR | 2014 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | total | KALIMANTAN TIMUR | 2015 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | total | KALIMANTAN TIMUR | 2016 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | total | KALIMANTAN TIMUR | 2017 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | total | KALIMANTAN TIMUR | 2018 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | total | KALIMANTAN TIMUR | 2019 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | total | KALIMANTAN TIMUR | 2020 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | PAPUA | 2023 | loncatan | cakupan_berubah_pemekaran_papua_2022 |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | non_hutan | PAPUA BARAT | 2023 | loncatan | cakupan_berubah_pemekaran_papua_2022 |  |
| tabel:sdg15_tutupan_hutan:persen | hutan | PAPUA | 2023 | loncatan | cakupan_berubah_pemekaran_papua_2022 |  |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | PAPUA | 2023 | loncatan | cakupan_berubah_pemekaran_papua_2022 |  |
| tabel:sdg15_tutupan_hutan:persen | non_hutan | PAPUA BARAT | 2023 | loncatan | cakupan_berubah_pemekaran_papua_2022 |  |
| var1304 | total | KALIMANTAN TIMUR | 2014 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| var1304 | total | KALIMANTAN TIMUR | 2015 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| var1304 | total | KALIMANTAN TIMUR | 2016 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| var1304 | total | KALIMANTAN TIMUR | 2017 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| var1304 | total | KALIMANTAN TIMUR | 2018 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| var1304 | kawasan_hutan | KALIMANTAN TIMUR | 2014 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| var1304 | kawasan_hutan | KALIMANTAN TIMUR | 2015 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| var1304 | kawasan_hutan | KALIMANTAN TIMUR | 2016 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| var1304 | kawasan_hutan | KALIMANTAN TIMUR | 2017 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| var1304 | kawasan_hutan | KALIMANTAN TIMUR | 2018 | antar_provinsi | cakupan_berubah_pemekaran_kaltara |  |
| var1304 | kawasan_hutan | PAPUA | 2023 | loncatan | cakupan_berubah_pemekaran_papua_2022 |  |

Daftar lengkap: `reports/tabel/anomali_berkategori.csv`.

## Daftar outlier_asli (474)

| seri | rincian_silver | wilayah | periode | jenis | subkategori | status_galat |
|---|---|---|---|---|---|---|
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | BALI | 2016 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | BANTEN | 2016 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | BANTEN | 2019 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | DI YOGYAKARTA | 2017 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | DI YOGYAKARTA | 2022 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAMBI | 2017 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAMBI | 2020 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAMBI | 2023 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAWA BARAT | 2019 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAWA TENGAH | 2017 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAWA TENGAH | 2019 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | JAWA TIMUR | 2019 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN BARAT | 2014 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN BARAT | 2015 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN BARAT | 2016 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN BARAT | 2017 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN BARAT | 2018 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN BARAT | 2019 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN SELATAN | 2019 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TENGAH | 2014 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TENGAH | 2015 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TENGAH | 2016 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TENGAH | 2017 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TENGAH | 2018 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TENGAH | 2019 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TENGAH | 2021 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TENGAH | 2022 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TIMUR | 2021 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KALIMANTAN TIMUR | 2022 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KEP. BANGKA BELITUNG | 2015 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KEP. BANGKA BELITUNG | 2019 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KEP. BANGKA BELITUNG | 2023 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KEP. RIAU | 2015 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KEP. RIAU | 2016 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | KEP. RIAU | 2022 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | LAMPUNG | 2015 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | NUSA TENGGARA BARAT | 2017 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | NUSA TENGGARA BARAT | 2019 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | NUSA TENGGARA TIMUR | 2015 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | NUSA TENGGARA TIMUR | 2017 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | NUSA TENGGARA TIMUR | 2019 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA | 2014 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA | 2015 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA | 2016 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA | 2017 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA | 2018 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA | 2019 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA | 2021 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA | 2022 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA BARAT | 2014 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA BARAT | 2015 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA BARAT | 2016 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA BARAT | 2017 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA BARAT | 2018 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA BARAT | 2019 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA BARAT | 2021 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | PAPUA BARAT | 2022 | antar_provinsi | nilai_ekstrem_antar_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | RIAU | 2015 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | RIAU | 2016 | loncatan | perubahan_tajam_satu_provinsi |  |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | RIAU | 2017 | loncatan | perubahan_tajam_satu_provinsi |  |

Daftar lengkap: `reports/tabel/anomali_berkategori.csv`.
