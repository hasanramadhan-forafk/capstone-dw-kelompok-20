# Tahap 2: profil seri pembanding WDI

Hanya Indonesia (nasional); tidak ada rincian jenis kelamin, umur, atau daerah. Tidak ada nilai yang diubah. Status kandidat adalah penilaian dari nama, satuan, dan definisi metadata; konfirmasi nilainya di tahap 6.

## Definisi (metadata WDI)
- **AG.LND.FRST.ZS**: Forest area (% of land area) is the share of total land area that is under natural or planted stands of trees of at least 5 meters in situ, whether productive or not, and excludes tree stands in agricultural production systems (for example, in fruit plantations and agroforestry systems) and trees in urban parks and gardens.
- **AG.LND.FRST.K2**: Forest area is land under natural or planted stands of trees of at least 5 meters in situ, whether productive or not, and excludes tree stands in agricultural production systems (for example, in fruit plantations and agroforestry systems) and trees in urban parks and gardens.
- **EN.ATM.PM25.MC.M3**: Population-weighted exposure to ambient PM2.5 pollution is defined as the average level of exposure of a nation's population to concentrations of suspended particles measuring less than 2.5 microns in aerodynamic diameter, which are capable of penetrating deep into the respiratory tract and causing severe health damage. Exposure is calculated by weighting mean annual concentrations of PM2.5 by population in both urban and rural areas.

## Ketersediaan seri × periode × rincian
| seri_kode | nama | satuan | satuan_di_api | n_entitas | n_baris_indonesia | tahun_pertama_bernilai | tahun_terakhir_bernilai | n_tahun_bernilai | nilai_min | nilai_maks | tahun_kosong_dalam_rentang_bernilai | rincian | organisasi_sumber | berkas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AG.LND.FRST.ZS | Forest area (% of land area) | persen luas daratan | (kosong) | 1 | 66 | 1990 | 2024 | 35 | 48.980 | 64.220 |  | tidak ada (1 nilai nasional per tahun) | FAOSTAT, Food and Agriculture Organization of the United Nations (FAO) | kelompok-01-hal-01.json |
| AG.LND.FRST.K2 | Forest area (sq. km) | km2 | (kosong) | 1 | 66 | 1990 | 2025 | 36 | 919586.000 | 1163345.000 |  | tidak ada (1 nilai nasional per tahun) | FAOSTAT, Food and Agriculture Organization of the United Nations (FAO) | kelompok-01-hal-01.json |
| EN.ATM.PM25.MC.M3 | PM2.5 air pollution, mean annual exposure (micrograms per cubic meter) | ug/m3 | (kosong) | 1 | 66 | 1990 | 2023 | 34 | 17.800 | 31.380 |  | tidak ada (1 nilai nasional per tahun) | Global Burden of Disease Study 2023 (GBD 2023) Air Pollution Exposure Estimates and Risk Curves 1990-2023, GBD Collaborator Network | kelompok-01-hal-01.json |

## Irisan tahun dengan seri utama
| seri_wdi | seri_utama | tahun_wdi | tahun_utama | n_irisan | tahun_irisan |
|---|---|---|---|---|---|
| AG.LND.FRST.ZS | tabel:sdg15_tutupan_hutan:luas_ribu_ha | 1990-2024 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 | 10 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 |
| AG.LND.FRST.ZS | tabel:sdg15_tutupan_hutan:persen | 1990-2024 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 | 10 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 |
| AG.LND.FRST.ZS | var1304 | 1990-2024 | 2014, 2015, 2016, 2017, 2018, 2023 | 6 | 2014, 2015, 2016, 2017, 2018, 2023 |
| AG.LND.FRST.ZS | var2532 | 1990-2024 | 2019, 2020, 2021, 2022, 2023, 2024 | 6 | 2019, 2020, 2021, 2022, 2023, 2024 |
| AG.LND.FRST.ZS | var588 | 1990-2024 | 2006, 2011, 2013, 2018 | 4 | 2006, 2011, 2013, 2018 |
| AG.LND.FRST.K2 | tabel:sdg15_tutupan_hutan:luas_ribu_ha | 1990-2025 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 | 10 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 |
| AG.LND.FRST.K2 | tabel:sdg15_tutupan_hutan:persen | 1990-2025 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 | 10 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 |
| AG.LND.FRST.K2 | var1304 | 1990-2025 | 2014, 2015, 2016, 2017, 2018, 2023 | 6 | 2014, 2015, 2016, 2017, 2018, 2023 |
| AG.LND.FRST.K2 | var2532 | 1990-2025 | 2019, 2020, 2021, 2022, 2023, 2024 | 6 | 2019, 2020, 2021, 2022, 2023, 2024 |
| AG.LND.FRST.K2 | var588 | 1990-2025 | 2006, 2011, 2013, 2018 | 4 | 2006, 2011, 2013, 2018 |
| EN.ATM.PM25.MC.M3 | tabel:sdg15_tutupan_hutan:luas_ribu_ha | 1990-2023 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 | 10 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 |
| EN.ATM.PM25.MC.M3 | tabel:sdg15_tutupan_hutan:persen | 1990-2023 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 | 10 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 |
| EN.ATM.PM25.MC.M3 | var1304 | 1990-2023 | 2014, 2015, 2016, 2017, 2018, 2023 | 6 | 2014, 2015, 2016, 2017, 2018, 2023 |
| EN.ATM.PM25.MC.M3 | var2532 | 1990-2023 | 2019, 2020, 2021, 2022, 2023, 2024 | 5 | 2019, 2020, 2021, 2022, 2023 |
| EN.ATM.PM25.MC.M3 | var588 | 1990-2023 | 2006, 2011, 2013, 2018 | 4 | 2006, 2011, 2013, 2018 |

## Kandidat rincian sebanding untuk tahap 6
| seri_wdi | seri_utama | rincian_utama | status | alasan | n_irisan | tahun_irisan |
|---|---|---|---|---|---|---|
| AG.LND.FRST.ZS | tabel:sdg15_tutupan_hutan:persen | hutan | kandidat | Sama-sama persen luas hutan. Penyebut beda: WDI = luas daratan (FAO), BPS = jumlah luas wilayah; definisi hutan juga bisa beda. Bandingkan arah/tren dulu, level dengan catatan. | 10 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 |
| AG.LND.FRST.K2 | tabel:sdg15_tutupan_hutan:luas_ribu_ha | hutan | kandidat | Sama-sama luas tutupan hutan. Seragamkan satuan (1 km2 = 0,1 ribu ha). Pembanding nasional BPS = jumlah 38 provinsi; Kaltim 2014-2020 masih gabungan dengan Kaltara dan nilai 2020 tertukar antarprovinsi (total nasional tidak terpengaruh jika murni tertukar). | 10 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 |
| AG.LND.FRST.K2 | var1304 | Kawasan Hutan | sekunder | Kawasan hutan = status penetapan, bukan tutupan; level bisa berbeda jauh dari WDI. | 6 | 2014, 2015, 2016, 2017, 2018, 2023 |
| AG.LND.FRST.ZS | var1304 | Kawasan Hutan | tidak sebanding | Persen tutupan vs luas kawasan berstatus hutan: konsep berbeda. | 6 | 2014, 2015, 2016, 2017, 2018, 2023 |
| EN.ATM.PM25.MC.M3 | var2532 | Indeks Kualitas Udara | hanya arah | PM2.5 (ug/m3, rata-rata tertimbang populasi nasional) vs indeks tanpa satuan: bandingkan arah tren atau korelasi, bukan level. Indeks lain (air, lahan, gambut) tidak sebanding. | 5 | 2019, 2020, 2021, 2022, 2023 |
| AG.LND.FRST.ZS | var588 | Kritis / Sangat Kritis / Jumlah | tidak sebanding | Lahan kritis tidak punya padanan di WDI; hanya 4 periode. | 4 | 2006, 2011, 2013, 2018 |
| AG.LND.FRST.K2 | var588 | Kritis / Sangat Kritis / Jumlah | tidak sebanding | Lahan kritis tidak punya padanan di WDI; hanya 4 periode. | 4 | 2006, 2011, 2013, 2018 |
| EN.ATM.PM25.MC.M3 | var1304 | (semua) | tidak sebanding | Variabel berbeda. | 6 | 2014, 2015, 2016, 2017, 2018, 2023 |
| EN.ATM.PM25.MC.M3 | var588 | (semua) | tidak sebanding | Variabel berbeda. | 4 | 2006, 2011, 2013, 2018 |
| EN.ATM.PM25.MC.M3 | tabel:sdg15_tutupan_hutan:luas_ribu_ha | (semua) | tidak sebanding | Variabel berbeda. | 10 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 |
| EN.ATM.PM25.MC.M3 | tabel:sdg15_tutupan_hutan:persen | (semua) | tidak sebanding | Variabel berbeda. | 10 | 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023 |
