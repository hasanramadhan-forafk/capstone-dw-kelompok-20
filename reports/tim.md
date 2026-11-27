# Laporan tim — MBG : Memang Banyak tuGas, kasus 20 Hutan, lahan, dan lingkungan

Status: draf akhir Sprint 1. Angka dapat ditarik ulang dari `data/silver/silver.parquet`, `reports/`, dan `log-keputusan.csv` (id K-xxx).

## Ringkasan

Kasus 20 (Hutan, lahan, dan lingkungan) mengintegrasikan tabel statis tutupan hutan (luas dan persen), tiga seri dinamis BPS (penutupan lahan menurut status kawasan `var1304`, luas lahan kritis `var588`, dan komponen penyusun IKLH `var2532`), serta tiga seri pembanding WDI (`AG.LND.FRST.K2`, `AG.LND.FRST.ZS`, dan `EN.ATM.PM25.MC.M3`). Dataset Silver pertama memuat 3.940 baris BPS yang lolos uji skema minimal dan berhasil dimuat ke basis data relasional DuckDB. Temuan terpenting pada Sprint 1 adalah terdeteksinya galat sistematis pada berkas mentah: kolom tahun 2020 pada tabel tutupan hutan tertukar antarprovinsi yang berhasil dibuktikan dan direkonstruksi secara matematis melalui relasi jumlah komponen dan persentase luas.

## Data dan lineage

Sebanyak 13 berkas mentah yang tercatat pada `data/raw/MANIFEST.csv` berhasil diekstraksi dan divalidasi nilai hash SHA-256 miliknya tanpa ada perbedaan:
- **BPS (snapshot 17 Oktober 2026)**: 3 JSON WebAPI dinamis, 1 JSON tabel statis tutupan hutan, 4 berkas CSV pendamping, dan 1 berkas `manifest_asal.json`.
- **WDI (snapshot 20 Oktober 2026)**: 1 berkas data JSON (`kelompok-01-hal-01.json`) memuat 60 seri untuk Indonesia, serta 3 berkas metadata indikator dan sumber.

Seluruh baris observasi di Silver memiliki kolom penelusuran asal (`_berkas_raw`) dan sidik jari kriptografis (`_sha256_raw`) yang dipetakan langsung dari MANIFEST tanpa intervensi manual.

### Penyimpanan Basis Data (Tabel Relasional vs Dokumen)

Lapis Silver (`seri`, `silver`) dan Gold (`gold_panel`, `gold_nasional`, `rekonsiliasi`) dimuat ulang setiap kali `python pipeline.py` dijalankan ke basis data **DuckDB** (`data/gold/gudang.duckdb`, tidak di-commit karena dibentuk ulang oleh pipeline) berdasarkan DDL di `src/gold/silver.sql` dan `src/gold/gold.sql`, dengan verifikasi jumlah baris yang sama persis terhadap berkas Parquet-nya.

- **Mengapa DuckDB:** Beroperasi dalam satu berkas lokal tanpa server (*serverless*) sehingga setiap anggota dan pemeriksa cukup menjalankan `python pipeline.py`, mendukung kueri analitik kolumnar (agregasi, *pivot*, *join*) dengan cepat, serta terintegrasi langsung dengan format Parquet.
- **Tabel Relasional vs Dokumen JSON:** Berkas respons mentah BPS dan WDI disimpan apa adanya pada tabel `dokumen_mentah` (`isi JSON`) sebagai pembanding (hasil perbandingan kueri di `reports/basis-data.md`). Pendekatan **dokumen** cocok untuk arsip lapis Bronze karena menjaga struktur hierarkis dan metadata asli (`var`, `vervar`, `turvar`), namun lambat/rumit diurai saat agregasi dan tidak bisa menegakkan keunikan tingkat sel. Sebaliknya, **tabel relasional** cocok untuk Silver dan Gold karena analisis selalu berdimensi `seri × wilayah × periode × rincian`, serta memungkinkan penegakan kunci primer komposit (menolak sel ganda), *foreign key* ke `seri`, dan batasan `CHECK` pada wilayah, status sel, kategori rekonsiliasi, serta konsistensi selisih.

## Masalah data dan penanganannya

Rangkuman keputusan pembersihan data, penanganan anomali, serta standardisasi yang diambil selama Sprint 1 tercatat secara berurutan di `log-keputusan.csv` (K-001 s.d. K-031):

| Masalah | Bukti | Keputusan | Baris terdampak | Log |
|---|---|---|---|---|
| Satuan luas berbeda | `var588` dalam hektar, seri lain ribu ha | Dibagi 1.000 menjadi ribu hektar di Silver agar sebanding | 399 | K-002, K-018 |
| Standardisasi rincian total | Label 'Jumlah' dari berbagai sumber | Diganti 'total' sesuai aturan baku tim | 689 | K-003 |
| Penamaan rincian dinamis | Label rincian BPS berubah antar-rilis | Kode rincian dibentuk dari `turvar_id` unik BPS | 2.205 | K-004 |
| Komponen IKLH tanpa satuan | Indeks kualitas lingkungan di sumber bernilai kosong | Satuan ditulis 'tidak_ada' di Silver, dipisah 6 komponen | 1.179 | K-005, K-012 |
| Pemekaran Kaltim-Kaltara | Kaltara 2014–2020 kosong / digabung Kaltim | Ditandai `digabung_induk` / `batas_lama`, tidak dibuang | 50 | K-006, K-007, K-016 |
| Kelengkapan panel (grid) | 4.370 sel grid 38 provinsi × periode | 545 sel kosong: 334 `belum_ada`, 156 `di_luar_cakupan`, 50 `digabung_induk`, 5 `missing` | 545 | K-013, K-014, K-015, K-017 |
| Ralat kode SDG katalog | Judul `var1304` penutupan kawasan, berkas IKLH | `var1304` diralat ke 15.1.1; `var2532` dicatat tujuan 15 (11.6.2 hanya udara) | 1.179 | K-020 |
| Baris nasional di data provinsi | Wilayah kode 9999 bercampur dengan provinsi | Dipisahkan dari panel provinsi untuk uji jumlah dan rekonsiliasi | 115 | K-021 |
| Deduplikasi | Observasi ganda antar berkas BPS | Kunci komposit unik; 0 duplikasi salah yang merusak data | 0 | K-022 |
| Blok 2020 tertukar antarprovinsi | Uji konsistensi: `jumlah rincian = total` & `persen = luas/total` | Blok hutan/non_hutan/persen 2020 dikembalikan ke provinsi pemilik sahnya | 100 | K-024 |
| Total 10x jumlah komponen | DIY 2016 total 10x lebih besar dari jumlah rincian | Dikoreksi menjadi jumlah komponen berdasarkan identitas matematis | 2 | K-025 |
| Pelanggaran jumlah persen | Hutan + non_hutan ≠ 100% pada tabel persen | Dikoreksi bila salah satu sisi cocok dengan luas/total | 1 | K-026 |
| Patahan cakupan wilayah | Pemekaran Papua 2022 dan Kaltim-Kaltara | Ditandai sebagai patahan, tidak diselaraskan paksa | 31 | K-027 |
| Dugaan galat tanpa bukti | Lonjakan sesaat tanpa pembuktian identitas independen | Ditandai tanpa diubah agar tidak mengarang data | 26 | K-028 |
| Pembulatan sisa rincian | Bali 2018 selisih 0,3 (567,2 vs 566,9) | Dibiarkan dan dicatat sebagai dugaan pembulatan | 1 | K-029 |
| Rekonsiliasi nasional BPS vs WDI | Perbedaan satuan, definisi FAO vs KLHK, polaritas arah IKU | 4 pasangan rekonsiliasi: 3 selisih (26 periode beririsan), 1 kontekstual | 10 | K-030 |
| Skema relasional & basis data | Validasi integritas tingkat basis data | Silver dimuat ke DuckDB dengan kunci primer dan batasan CHECK | 3.940 | K-031 |

### Rangkuman Temuan Kualitas Data
1. **Celah Panel (Missing vs Struktural)**:
   Dari total 4.370 sel grid (38 provinsi × periode terbit × rincian), terdapat 3.825 sel terisi dan 545 sel kosong. Celah panel bukan missing murni, melainkan didominasi faktor struktural: **334 sel `belum_ada`** (4 provinsi baru Papua sebelum 2023 dan Kaltara sebelum 2012), **156 sel `di_luar_cakupan`** (rincian air laut/gambut yang memang tidak dimiliki provinsi pedalaman/tanpa laut/tanpa gambut), dan **50 sel `digabung_induk`** (Kaltara yang digabung dengan Kaltim pada rilis resmi BPS). Celah *missing* sebenarnya hanya ditemukan pada 5 sel (Kepulauan Riau pada `var588`).
2. **Galat Input dan Anomali Sumber**:
   Sebanyak 725 calon anomali teridentifikasi dari deteksi ambang IQR dan loncatan deret waktu. Prinsip penanganan yang dipegang tim: *hanya galat input yang terbukti secara matematis oleh identitas independen yang diperbaiki; outlier asli dan patahan nyata dipertahankan agar tidak menghilangkan sinyal data*.
   - **Galat blok 2020 tertukar**: Nilai rincian hutan dan non-hutan pada 25 provinsi tertukar posisinya antarprovinsi. Masalah ini berhasil diselesaikan melalui pembuktian siklus tertutup (*closed-cycle matching*) di mana nilai yang dipindahkan tepat menghasilkan `hutan + non_hutan = total` dan `persen = luas / total`.
   - **Galat salah ketik / desimal**: DIY 2016 pada dua tabel tutupan kawasan memiliki total 10 kali lipat dari jumlah rinciannya (faktor 10x), yang dikoreksi menjadi jumlah rincian.
   - **Galat tanpa bukti independen**: 26 calon anomali yang dicurigai sebagai lonjakan sesaat namun tidak memiliki pembanding independen tetap ditandai tanpa diubah, guna mencegah manipulasi data tanpa dasar bukti.
3. **Patahan Seri dan Wilayah**:
   Patahan terkonfirmasi akibat pemekaran Kalimantan Utara dan pemekaran empat provinsi di Papua tahun 2022 ditandai sebagai batas segmen analitik (31 baris terdampak).
4. **Koreksi Katalog Metadata**:
   Ditemukan inkonsistensi metadata katalog BPS: `var1304` terdaftar dengan kode SDG 15.3.1 (padahal merupakan tutupan kawasan hutan 15.1.1, bukan degradasi lahan), dan `var2532` terdaftar dengan kode SDG 11.6.2 (padahal IKLH mencakup 6 komponen lingkungan hidup dan masuk Tujuan 15, sementara 11.6.2 hanya spesifik kualitas udara perkotaan).

## Integrasi dan rekonsiliasi

Tabel nasional Gold (`data/gold/nasional.parquet`, 184 baris dari 8 seri, 1990–2025) menyandingkan seri utama nasional BPS dengan pembanding WDI, dan tabel rekonsiliasi berkategori (`data/gold/rekonsiliasi.parquet`, 36 baris; rincian di `reports/rekonsiliasi.md`) menghitung selisih pada periode beririsan tanpa menghapus maupun memaksa angka menjadi sama. Median selisih relatif mutlak untuk pasangan seri utama provinsi adalah **0,29%** (26 baris berpasangan selisih).

| Pasangan | Yang dibandingkan | Median selisih relatif | Kategori | Penjelasan |
|---|---|---|---|---|
| P1 | Luas hutan nasional: BPS (ribu ha) vs WDI (`AG.LND.FRST.K2`, km²) | 0,38% | definisi berbeda (9), tidak berselisih (1) | Tutupan lahan berhutan KLHK vs definisi FAO (pohon ≥ 5 m, tanpa perkebunan) setelah konversi WDI km² × 0,1 menjadi ribu hektar |
| P2 | Persentase hutan: BPS (terhadap penutupan lahan) vs WDI (`AG.LND.FRST.ZS`, terhadap luas daratan) | 0,83% | definisi berbeda (10) | Penyebut berbeda: total luas penutupan lahan (BPS) vs total luas daratan (*land area*, WDI) |
| P3 | Indeks kualitas udara (`var2532` IKU) vs PM2.5 (`EN.ATM.PM25.MC.M3`): konteks | — | definisi berbeda (6) | Pasangan kontekstual berarah berlawanan (IKU tinggi = baik; PM2.5 tinggi = buruk); selisih tidak dihitung |
| P4 | Kawasan hutan (`var1304`) vs tutupan hutan (`tabel:sdg15_tutupan_hutan:luas_ribu_ha`) | 0,00% | tidak berselisih (6), tanpa pasangan (4) | Sumber sama (rekalkulasi KLHK) dengan klasifikasi berbeda; jumlah luas identik pada 6 tahun beririsan (`2014–2018`, `2023`) dan `tanpa pasangan` pada `2019–2022` |

Periode pembanding di luar rentang tahun seri utama tidak ditulis (P1: 26 tahun, P2: 25 tahun, P3: 29 tahun), sedangkan seluruh periode seri utama tetap tampil termasuk yang tanpa pasangan.

## Validasi dan reproduksibilitas

Pipeline validasi dijalankan secara terpadu melalui skrip `pipeline.py`:
- **Pemeriksaan Skema Minimal**: Memastikan seluruh kolom wajib Silver terpenuhi tipe data dan ketiadaan nilai kosong pada kunci unik (`python -m src.common.skema data/silver/silver.parquet` -> **LOLOS 3.940 baris**).
- **Pemuatan Basis Data SQL**: Skrip `src/gold/muat_sql.py` memuat 3.940 baris Silver ke DuckDB (`data/gold/gudang.duckdb`) dengan verifikasi kunci primer komposit, foreign key katalog seri, dan batasan `CHECK` wilayah serta rentang nilai.
- **Reproduksibilitas**: Seluruh alur dari data mentah sampai penyusunan Silver dan Gold dapat direproduksi dalam satu perintah tanpa dependensi eksternal yang rumit.

## Pembagian kerja

| Anggota | NIM | Komponen | Tugas sampingan | Bagian laporan yang ditulis |
|---|---|---|---|---|
| Hasan Nur Ramadhan | 124450013 | Validasi dan dokumentasi | Koordinator | Validasi dan reproduksibilitas, koordinasi naskah |
| Dwi Rahma Fitriani | 124450084 | Ekstraksi dan lineage | Penjaga Data & Evaluasi | Data dan lineage, verifikasi sha256 |
| Farhanah Hadaya Fatin | 124450026 | Transformasi dan panel | Reproduksi & Demo | Transformasi Silver, uji reproduksi |
| Melva Shaprina Febrianti | 124450087 | Integrasi, penyimpanan, dan skala | Analis Utama | Masalah data dan penanganannya, integrasi & rekonsiliasi |
| Raisya Izzati Harira | 124450122 | Profil dan pembersihan | Integrator | Ringkasan, profil per seri, klasifikasi anomali |
