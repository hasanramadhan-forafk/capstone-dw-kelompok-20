# Tahap 3: grid provinsi × periode dan kelengkapan panel

Sumber: `data/silver/silver.parquet` (BPS, CSV). Tidak ada nilai yang diisi atau diperbaiki; sel kosong hanya dihitung dan diberi kategori.

## Ringkasan

- Baris Silver: **3940** (3825 provinsi, 115 baris Indonesia dipisahkan, 0 baris kode wilayah tak dikenal).
- Sel grid (38 provinsi × periode terbit per seri × rincian): **4370**; terisi 3825.
- **sel_kosong_grid = 545**: belum_ada 334, di_luar_cakupan 156, digabung_induk 50, missing 5.

## Aturan grid

- Periode grid = periode yang benar-benar terbit untuk tiap seri × rincian. Tahun yang tidak terbit (mis. `var1304` 2019–2022, `var588` di luar 4 tahunnya) bukan missing.
- `di_luar_cakupan`: provinsi tanpa satu pun observasi pada seri × rincian itu (bukan sel yang hilang).
- `belum_ada`: periode sebelum tahun pertama provinsi pemekaran muncul di data: Papua Barat Daya, Selatan, Tengah, Pegunungan sebelum 2023 (dibentuk 2022, data 2022 masih susunan lama); Kalimantan Utara sebelum 2012.
- `digabung_induk`: Kalimantan Utara tanpa observasi karena tergabung di Kalimantan Timur: tabel tutupan hutan 2014–2020 (dasar: kolom `catatan` sumber) dan `var1304` 2014–2018 (dasar: jumlah 33 provinsi = baris Indonesia).
- `missing`: sisanya. Hanya ini yang dihitung sebagai celah sebenarnya.

## tabel:sdg15_tutupan_hutan:luas_ribu_ha

Persen sel terisi per tahun, semua sel (38 provinsi):

| rincian | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| hutan | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 89.5 | 89.5 | 100.0 |
| non_hutan | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 89.5 | 89.5 | 100.0 |
| total | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 89.5 | 89.5 | 100.0 |

Persen sel terisi per tahun, hanya sel yang berlaku (tanpa di_luar_cakupan, belum_ada, digabung_induk):

| rincian | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| hutan | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| non_hutan | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| total | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |

## tabel:sdg15_tutupan_hutan:persen

Persen sel terisi per tahun, semua sel (38 provinsi):

| rincian | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| hutan | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 89.5 | 89.5 | 100.0 |
| non_hutan | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 89.5 | 89.5 | 100.0 |

Persen sel terisi per tahun, hanya sel yang berlaku (tanpa di_luar_cakupan, belum_ada, digabung_induk):

| rincian | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|---|---|---|---|---|
| hutan | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| non_hutan | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |

## var1304

Persen sel terisi per tahun, semua sel (38 provinsi):

| rincian | 2014 | 2015 | 2016 | 2017 | 2018 | 2023 |
|---|---|---|---|---|---|---|
| apl | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 100.0 |
| kawasan_hutan | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 100.0 |
| total | 86.8 | 86.8 | 86.8 | 86.8 | 86.8 | 100.0 |

Persen sel terisi per tahun, hanya sel yang berlaku (tanpa di_luar_cakupan, belum_ada, digabung_induk):

| rincian | 2014 | 2015 | 2016 | 2017 | 2018 | 2023 |
|---|---|---|---|---|---|---|
| apl | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| kawasan_hutan | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| total | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |

## var2532

Persen sel terisi per tahun, semua sel (38 provinsi):

| rincian | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|
| kualitas_air | 89.5 | 89.5 | 89.5 | 89.5 | 100.0 | 100.0 |
| kualitas_air_laut | 89.5 | 89.5 | 89.5 | 89.5 | 94.7 | 97.4 |
| kualitas_ekosistem_gambut | 50.0 | 50.0 | 50.0 | 50.0 | 60.5 | 60.5 |
| kualitas_lahan |  | 89.5 | 89.5 | 89.5 | 100.0 | 100.0 |
| kualitas_tutupan_lahan | 86.8 | 89.5 | 89.5 | 89.5 | 100.0 | 100.0 |
| kualitas_udara | 89.5 | 89.5 | 89.5 | 89.5 | 100.0 | 100.0 |

Persen sel terisi per tahun, hanya sel yang berlaku (tanpa di_luar_cakupan, belum_ada, digabung_induk):

| rincian | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|
| kualitas_air | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| kualitas_air_laut | 100.0 | 100.0 | 100.0 | 100.0 | 97.3 | 100.0 |
| kualitas_ekosistem_gambut | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| kualitas_lahan |  | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| kualitas_tutupan_lahan | 97.1 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| kualitas_udara | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |

## var588

Persen sel terisi per tahun, semua sel (38 provinsi):

| rincian | 2006 | 2011 | 2013 | 2018 |
|---|---|---|---|---|
| kritis | 81.6 | 84.2 | 86.8 | 86.8 |
| sangat_kritis | 81.6 | 84.2 | 86.8 | 86.8 |
| total | 81.6 | 84.2 | 86.8 | 86.8 |

Persen sel terisi per tahun, hanya sel yang berlaku (tanpa di_luar_cakupan, belum_ada, digabung_induk):

| rincian | 2006 | 2011 | 2013 | 2018 |
|---|---|---|---|---|
| kritis | 96.9 | 100.0 | 100.0 | 100.0 |
| sangat_kritis | 96.9 | 100.0 | 100.0 | 100.0 |
| total | 96.9 | 100.0 | 100.0 | 100.0 |

## Provinsi di luar cakupan seri × rincian

| seri_kode | rincian | n_provinsi | provinsi |
|---|---|---|---|
| var2532 | kualitas_air_laut | 1 | PAPUA PEGUNUNGAN |
| var2532 | kualitas_ekosistem_gambut | 15 | BALI, BANTEN, DI YOGYAKARTA, DKI JAKARTA, GORONTALO, JAWA BARAT, JAWA TENGAH, JAWA TIMUR, MALUKU, MALUKU UTARA, NUSA TENGGARA BARAT, NUSA TENGGARA TIMUR, SULAWESI SELATAN, SULAWESI TENGGARA, SULAWESI UTARA |
| var588 | kritis | 5 | DKI JAKARTA, PAPUA BARAT DAYA, PAPUA PEGUNUNGAN, PAPUA SELATAN, PAPUA TENGAH |
| var588 | sangat_kritis | 5 | DKI JAKARTA, PAPUA BARAT DAYA, PAPUA PEGUNUNGAN, PAPUA SELATAN, PAPUA TENGAH |
| var588 | total | 5 | DKI JAKARTA, PAPUA BARAT DAYA, PAPUA PEGUNUNGAN, PAPUA SELATAN, PAPUA TENGAH |

## Periode terbit untuk seri tetapi tidak untuk rincian tertentu

| seri_kode | rincian | periode_tak_terbit |
|---|---|---|
| var2532 | kualitas_lahan | 2019 |

## Uji jumlah rincian = rincian jumlah (setelah penyeragaman satuan ke ribu hektar)

| seri_kode | diuji | melanggar | toleransi | catatan |
|---|---|---|---|---|
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 347 | 27 | 0.2 |  |
| tabel:sdg15_tutupan_hutan:persen | 347 | 1 | 0.1 |  |
| var1304 | 209 | 1 | 0.2 |  |
| var588 | 133 | 0 | 0.0 |  |

Pelanggaran: 29 baris (ditandai, tidak diperbaiki). Daftar: `reports/tabel/uji_jumlah_pelanggaran.csv`.

| seri_kode | wilayah_kode | nama_wilayah | tahun | jumlah_rincian | rincian_jumlah | selisih |
|---|---|---|---|---|---|---|
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 1700 | BENGKULU | 2020 | 1659.7 | 2002.9 | -343.2 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 1800 | LAMPUNG | 2020 | 2002.9 | 3435.4 | -1432.5 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 1900 | KEP. BANGKA BELITUNG | 2020 | 3435.4 | 1659.7 | 1775.7 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 3100 | DKI JAKARTA | 2020 | 939.2 | 65.3 | 873.9 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 3200 | JAWA BARAT | 2020 | 65.3 | 3698.6 | -3633.3 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 3300 | JAWA TENGAH | 2020 | 3698.6 | 3456.6 | 242.0 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 3400 | DI YOGYAKARTA | 2016 | 319.4 | 3194.0 | -2874.6 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 3400 | DI YOGYAKARTA | 2020 | 3456.6 | 319.4 | 3137.2 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 3500 | JAWA TIMUR | 2020 | 319.4 | 4837.7 | -4518.3 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 3600 | BANTEN | 2020 | 4837.7 | 939.2 | 3898.5 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 5100 | BALI | 2018 | 567.2 | 566.9 | 0.3 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 5100 | BALI | 2020 | 14572.8 | 566.9 | 14005.9 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 5200 | NUSA TENGGARA BARAT | 2020 | 3713.9 | 1980.2 | 1733.7 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 5300 | NUSA TENGGARA TIMUR | 2020 | 15266.2 | 4722.5 | 10543.7 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 6100 | KALIMANTAN BARAT | 2020 | 19504.8 | 14572.8 | 4932.0 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 6200 | KALIMANTAN TENGAH | 2020 | 1439.5 | 15266.2 | -13826.7 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 6300 | KALIMANTAN SELATAN | 2020 | 1198.5 | 3713.9 | -2515.4 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 6400 | KALIMANTAN TIMUR | 2020 | 6034.7 | 19504.8 | -13470.1 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 7100 | SULAWESI UTARA | 2020 | 3611.6 | 1439.5 | 2172.1 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 7200 | SULAWESI TENGAH | 2020 | 1680.2 | 6034.7 | -4354.5 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 7400 | SULAWESI TENGGARA | 2020 | 566.9 | 3611.6 | -3044.7 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 7500 | GORONTALO | 2020 | 1980.2 | 1198.5 | 781.7 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 7600 | SULAWESI BARAT | 2020 | 4722.5 | 1680.2 | 3042.3 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 8100 | MALUKU | 2020 | 3130.6 | 4622.1 | -1491.5 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 8200 | MALUKU UTARA | 2020 | 4622.1 | 3130.6 | 1491.5 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 9100 | PAPUA BARAT | 2020 | 31076.9 | 9624.9 | 21452.0 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | 9400 | PAPUA | 2020 | 9624.9 | 31076.9 | -21452.0 |
| tabel:sdg15_tutupan_hutan:persen | 9400 | PAPUA | 2018 | 99.4 | 100.0 | -0.6 |
| var1304 | 3400 | DI YOGYAKARTA | 2016 | 319.4 | 3194.0 | -2874.6 |

## Dugaan penyebab pelanggaran pada tabel luas

| wilayah_kode | nama_wilayah | tahun | hutan_plus_non_hutan | total_di_baris | total_biasa_provinsi_ini | total_di_baris_sama_dgn_biasa | hutan_plus_non_hutan_sama_dgn_total_milik | jenis_dugaan |
|---|---|---|---|---|---|---|---|---|
| 1700 | BENGKULU | 2020 | 1659.7 | 2002.9 | 2002.9 | True | KEP. BANGKA BELITUNG | tertukar_antarprovinsi |
| 1800 | LAMPUNG | 2020 | 2002.9 | 3435.4 | 3435.4 | True | BENGKULU | tertukar_antarprovinsi |
| 1900 | KEP. BANGKA BELITUNG | 2020 | 3435.4 | 1659.7 | 1659.7 | True | LAMPUNG | tertukar_antarprovinsi |
| 3100 | DKI JAKARTA | 2020 | 939.2 | 65.3 | 65.3 | True | BANTEN | tertukar_antarprovinsi |
| 3200 | JAWA BARAT | 2020 | 65.3 | 3698.6 | 3698.6 | True | DKI JAKARTA | tertukar_antarprovinsi |
| 3300 | JAWA TENGAH | 2020 | 3698.6 | 3456.6 | 3456.6 | True | JAWA BARAT | tertukar_antarprovinsi |
| 3400 | DI YOGYAKARTA | 2016 | 319.4 | 3194.0 | 319.4 | False |  | geser_desimal_pada_total |
| 3400 | DI YOGYAKARTA | 2020 | 3456.6 | 319.4 | 319.4 | True | JAWA TENGAH | tertukar_antarprovinsi |
| 3500 | JAWA TIMUR | 2020 | 319.4 | 4837.7 | 4837.7 | True | DI YOGYAKARTA | tertukar_antarprovinsi |
| 3600 | BANTEN | 2020 | 4837.7 | 939.2 | 939.2 | True | JAWA TIMUR | tertukar_antarprovinsi |
| 5100 | BALI | 2018 | 567.2 | 566.9 | 566.9 | True |  | selisih_kecil (pembulatan?) |
| 5100 | BALI | 2020 | 14572.8 | 566.9 | 566.9 | True | KALIMANTAN BARAT | tertukar_antarprovinsi |
| 5200 | NUSA TENGGARA BARAT | 2020 | 3713.9 | 1980.2 | 1980.2 | True | KALIMANTAN SELATAN | tertukar_antarprovinsi |
| 5300 | NUSA TENGGARA TIMUR | 2020 | 15266.2 | 4722.5 | 4722.5 | True | KALIMANTAN TENGAH | tertukar_antarprovinsi |
| 6100 | KALIMANTAN BARAT | 2020 | 19504.8 | 14572.8 | 14572.8 | True | KALIMANTAN TIMUR | tertukar_antarprovinsi |
| 6200 | KALIMANTAN TENGAH | 2020 | 1439.5 | 15266.2 | 15266.2 | True | SULAWESI UTARA | tertukar_antarprovinsi |
| 6300 | KALIMANTAN SELATAN | 2020 | 1198.5 | 3713.9 | 3713.9 | True | GORONTALO | tertukar_antarprovinsi |
| 6400 | KALIMANTAN TIMUR | 2020 | 6034.7 | 19504.8 | 19504.8 | True | SULAWESI TENGAH | tertukar_antarprovinsi |
| 7100 | SULAWESI UTARA | 2020 | 3611.6 | 1439.5 | 1439.5 | True | SULAWESI TENGGARA | tertukar_antarprovinsi |
| 7200 | SULAWESI TENGAH | 2020 | 1680.2 | 6034.7 | 6034.7 | True | SULAWESI BARAT | tertukar_antarprovinsi |
| 7400 | SULAWESI TENGGARA | 2020 | 566.9 | 3611.6 | 3611.6 | True | BALI | tertukar_antarprovinsi |
| 7500 | GORONTALO | 2020 | 1980.2 | 1198.5 | 1198.5 | True | NUSA TENGGARA BARAT | tertukar_antarprovinsi |
| 7600 | SULAWESI BARAT | 2020 | 4722.5 | 1680.2 | 1680.2 | True | NUSA TENGGARA TIMUR | tertukar_antarprovinsi |
| 8100 | MALUKU | 2020 | 3130.6 | 4622.1 | 4622.1 | True | MALUKU UTARA | tertukar_antarprovinsi |
| 8200 | MALUKU UTARA | 2020 | 4622.1 | 3130.6 | 3130.6 | True | MALUKU | tertukar_antarprovinsi |
| 9100 | PAPUA BARAT | 2020 | 31076.9 | 9624.9 | 9624.9 | True | PAPUA | tertukar_antarprovinsi |
| 9400 | PAPUA | 2020 | 9624.9 | 31076.9 | 31076.9 | True | PAPUA BARAT | tertukar_antarprovinsi |

## Uji persen vs luas / total (tabel tutupan hutan)

| wilayah_kode | nama_wilayah | tahun | rincian | persen_sumber | persen_dari_luas | selisih_persen_poin |
|---|---|---|---|---|---|---|
| 1700 | BENGKULU | 2020 | hutan | 11.6 | 9.6 | 2.0 |
| 1800 | LAMPUNG | 2020 | hutan | 33.2 | 19.4 | 13.8 |
| 1900 | KEP. BANGKA BELITUNG | 2020 | hutan | 10.0 | 20.7 | -10.7 |
| 3100 | DKI JAKARTA | 2020 | hutan | 16.3 | 234.2 | -217.9 |
| 3200 | JAWA BARAT | 2020 | hutan | 1.4 | 0.0 | 1.4 |
| 3300 | JAWA TENGAH | 2020 | hutan | 19.2 | 20.6 | -1.4 |
| 3400 | DI YOGYAKARTA | 2016 | hutan | 14.4 | 1.4 | 13.0 |
| 3400 | DI YOGYAKARTA | 2020 | hutan | 18.4 | 198.7 | -180.3 |
| 3500 | JAWA TIMUR | 2020 | hutan | 6.4 | 0.4 | 6.0 |
| 3600 | BANTEN | 2020 | hutan | 24.7 | 127.0 | -102.3 |
| 5100 | BALI | 2020 | hutan | 38.8 | 997.8 | -959.0 |
| 5200 | NUSA TENGGARA BARAT | 2020 | hutan | 25.5 | 47.9 | -22.4 |
| 5300 | NUSA TENGGARA TIMUR | 2020 | hutan | 48.9 | 158.0 | -109.1 |
| 6100 | KALIMANTAN BARAT | 2020 | hutan | 68.1 | 91.2 | -23.1 |
| 6200 | KALIMANTAN TENGAH | 2020 | hutan | 38.9 | 3.7 | 35.2 |
| 6300 | KALIMANTAN SELATAN | 2020 | hutan | 61.0 | 19.7 | 41.3 |
| 6400 | KALIMANTAN TIMUR | 2020 | hutan | 63.0 | 19.5 | 43.5 |
| 7100 | SULAWESI UTARA | 2020 | hutan | 52.4 | 131.4 | -79.0 |
| 7200 | SULAWESI TENGAH | 2020 | hutan | 49.9 | 13.9 | 36.0 |
| 7400 | SULAWESI TENGGARA | 2020 | hutan | 17.2 | 2.7 | 14.5 |
| 7500 | GORONTALO | 2020 | hutan | 43.9 | 72.6 | -28.7 |
| 7600 | SULAWESI BARAT | 2020 | hutan | 36.5 | 102.7 | -66.2 |
| 8100 | MALUKU | 2020 | hutan | 64.6 | 43.8 | 20.8 |
| 8200 | MALUKU UTARA | 2020 | hutan | 66.5 | 98.2 | -31.7 |
| 9100 | PAPUA BARAT | 2020 | hutan | 81.7 | 263.9 | -182.2 |
| 9400 | PAPUA | 2020 | hutan | 93.2 | 28.9 | 64.3 |
| 1700 | BENGKULU | 2020 | non_hutan | 88.4 | 73.3 | 15.1 |
| 1800 | LAMPUNG | 2020 | non_hutan | 66.8 | 38.9 | 27.9 |
| 1900 | KEP. BANGKA BELITUNG | 2020 | non_hutan | 90.0 | 186.3 | -96.3 |
| 3100 | DKI JAKARTA | 2020 | non_hutan | 83.7 | 1204.1 | -1120.4 |
| 3200 | JAWA BARAT | 2020 | non_hutan | 98.6 | 1.7 | 96.9 |
| 3300 | JAWA TENGAH | 2020 | non_hutan | 80.8 | 86.4 | -5.6 |
| 3400 | DI YOGYAKARTA | 2016 | non_hutan | 85.6 | 8.6 | 77.0 |
| 3400 | DI YOGYAKARTA | 2020 | non_hutan | 81.6 | 883.6 | -802.0 |
| 3500 | JAWA TIMUR | 2020 | non_hutan | 93.6 | 6.2 | 87.4 |
| 3600 | BANTEN | 2020 | non_hutan | 75.3 | 388.1 | -312.8 |
| 5100 | BALI | 2020 | non_hutan | 61.2 | 1572.8 | -1511.6 |
| 5200 | NUSA TENGGARA BARAT | 2020 | non_hutan | 74.5 | 139.7 | -65.2 |
| 5300 | NUSA TENGGARA TIMUR | 2020 | non_hutan | 51.1 | 165.3 | -114.2 |
| 6100 | KALIMANTAN BARAT | 2020 | non_hutan | 31.9 | 42.7 | -10.8 |
| 6200 | KALIMANTAN TENGAH | 2020 | non_hutan | 61.1 | 5.8 | 55.3 |
| 6300 | KALIMANTAN SELATAN | 2020 | non_hutan | 39.0 | 12.6 | 26.4 |
| 6400 | KALIMANTAN TIMUR | 2020 | non_hutan | 37.0 | 11.4 | 25.6 |
| 7100 | SULAWESI UTARA | 2020 | non_hutan | 47.6 | 119.5 | -71.9 |
| 7200 | SULAWESI TENGAH | 2020 | non_hutan | 50.1 | 14.0 | 36.1 |
| 7400 | SULAWESI TENGGARA | 2020 | non_hutan | 82.8 | 13.0 | 69.8 |
| 7500 | GORONTALO | 2020 | non_hutan | 56.1 | 92.7 | -36.6 |
| 7600 | SULAWESI BARAT | 2020 | non_hutan | 63.5 | 178.4 | -114.9 |
| 8100 | MALUKU | 2020 | non_hutan | 35.4 | 24.0 | 11.4 |
| 8200 | MALUKU UTARA | 2020 | non_hutan | 33.5 | 49.4 | -15.9 |
| 9100 | PAPUA BARAT | 2020 | non_hutan | 18.3 | 59.0 | -40.7 |
| 9400 | PAPUA | 2018 | non_hutan | 19.0 | 19.6 | -0.6 |
| 9400 | PAPUA | 2020 | non_hutan | 6.8 | 2.1 | 4.7 |

## Uji jumlah 38 provinsi vs baris Indonesia (seri luas, selisih > 0,5%)

| seri_kode | rincian | tahun | jumlah_provinsi | n_provinsi | nasional | selisih | selisih_persen |
|---|---|---|---|---|---|---|---|
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | total | 2016 | 190626.3 | 33 | 187751.9 | 2874.4 | 1.5 |
| var1304 | total | 2016 | 190626.3 | 33 | 187751.9 | 2874.4 | 1.5 |

## Kecocokan seri_kode dengan judul berkas

| seri_kode | berkas | judul_berkas | var_di_manifest | kecocokan_kode | satuan_silver | kode_sdg_katalog | rincian |
|---|---|---|---|---|---|---|---|
| tabel:sdg15_tutupan_hutan:luas_ribu_ha | sdg15_tutupan_hutan | Rekapitulasi Luas Penutupan Lahan Hutan dan Non Hutan Menurut Provinsi Tahun 2014-2023 (Ribu Ha) |  | tabel statis (tanpa var) | ribu_hektar | 15.1.1 | hutan \| non_hutan \| total |
| tabel:sdg15_tutupan_hutan:persen | sdg15_tutupan_hutan | Rekapitulasi Luas Penutupan Lahan Hutan dan Non Hutan Menurut Provinsi Tahun 2014-2023 (Ribu Ha) |  | tabel statis (tanpa var) | persen | 15.1.1 | hutan \| non_hutan |
| var1304 | sdg15_tutupan_kawasan | Luas Penutupan Lahan Indonesa di Dalam dan di Luar Kawasan Hutan Menurut Provinsi | 1304 | cocok | ribu_hektar | 15.3.1 | apl \| kawasan_hutan \| total |
| var2532 | sdg15_iklh | Komponen Penyusun Indeks Kualitas Lingkungan Hidup Menurut Provinsi | 2532 | cocok | tidak_ada | 11.6.2 | kualitas_air \| kualitas_air_laut \| kualitas_ekosistem_gambut \| kualitas_lahan \| kualitas_tutupan_lahan \| kualitas_udara |
| var588 | sdg15_lahan_kritis | Luas dan Penyebaran Lahan Kritis Menurut Provinsi | 588 | cocok | ribu_hektar | 15.3.1 | kritis \| sangat_kritis \| total |

## Usulan kode SDG komponen var2532 (IKLH)

Judul berkas: komponen penyusun Indeks Kualitas Lingkungan Hidup, bukan konsentrasi PM2.5. Kode 11.6.2 di katalog hanya masuk akal untuk komponen udara.

| rincian | kode_sdg_usulan | status |
|---|---|---|
| kualitas_air | (bukan 11.6.2) | perlu konfirmasi dosen; berkas bernama sdg15, kandidat target 15.x |
| kualitas_air_laut | (bukan 11.6.2) | perlu konfirmasi dosen; berkas bernama sdg15, kandidat target 15.x |
| kualitas_ekosistem_gambut | (bukan 11.6.2) | perlu konfirmasi dosen; berkas bernama sdg15, kandidat target 15.x |
| kualitas_lahan | (bukan 11.6.2) | perlu konfirmasi dosen; berkas bernama sdg15, kandidat target 15.x |
| kualitas_tutupan_lahan | (bukan 11.6.2) | perlu konfirmasi dosen; berkas bernama sdg15, kandidat target 15.x |
| kualitas_udara | 11.6.2 | sesuai katalog; hanya komponen udara yang berkaitan dengan 11.6.2 |
