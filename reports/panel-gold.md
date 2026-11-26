# Panel Gold provinsi x periode x indikator

Dihasilkan `python pipeline.py` (`src/gold/pilih.py` dan `src/gold/lebar.py`) dari Silver.

## Aturan satu nilai per sel

1. Snapshot terbaru dipakai; angka berbeda antar snapshot dicatat sebagai revisi.
2. CSV didahulukan atas JSON bila snapshot sama.
3. Rincian turunan (non_hutan, APL, total var1304/var588) tetap di Silver.
4. Satuan luas dibakukan ke ribu_hektar.
5. Baris Indonesia (9999) dipisah ke tabel nasional.
6. Penanda anomali Sprint 1 terbawa; tidak ada nilai yang dihapus.

Panel panjang: **2,616 baris**, 12 indikator, 5 seri. Panel lebar: `data/gold/panel_lebar.parquet`.

## Indikator

| indikator | satuan | periode | jumlah_periode | sel | terisi | ditandai |
|---|---|---|---|---|---|---|
| tabel:sdg15_tutupan_hutan:luas_ribu_ha\|hutan | ribu_hektar | 2014-2023 | 10 | 337 | 337 | 126 |
| tabel:sdg15_tutupan_hutan:luas_ribu_ha\|total | ribu_hektar | 2014-2023 | 10 | 337 | 337 | 38 |
| tabel:sdg15_tutupan_hutan:persen\|hutan | persen | 2014-2023 | 10 | 337 | 337 | 87 |
| var1304\|kawasan_hutan | ribu_hektar | 2014-2023 | 6 | 203 | 203 | 28 |
| var2532\|kualitas_air | tidak_ada | 2019-2024 | 6 | 212 | 212 | 21 |
| var2532\|kualitas_air_laut | tidak_ada | 2019-2024 | 6 | 209 | 209 | 11 |
| var2532\|kualitas_ekosistem_gambut | tidak_ada | 2019-2024 | 6 | 122 | 122 | 14 |
| var2532\|kualitas_lahan | tidak_ada | 2020-2024 | 5 | 178 | 178 | 18 |
| var2532\|kualitas_tutupan_lahan | tidak_ada | 2019-2024 | 6 | 211 | 211 | 42 |
| var2532\|kualitas_udara | tidak_ada | 2019-2024 | 6 | 212 | 212 | 36 |
| var588\|kritis | ribu_hektar | 2006-2018 | 4 | 129 | 129 | 19 |
| var588\|sangat_kritis | ribu_hektar | 2006-2018 | 4 | 129 | 129 | 20 |

Kunci panel: `indikator + wilayah_kode + periode`; setiap sel terisi tertelusur ke Silver lewat `_berkas_raw`. Diperiksa otomatis di `reports/validasi.md`.
