# Laporan tim — MBG : Memang Banyak tuGas, kasus 20 Hutan, lahan, dan lingkungan

Status: draf akhir Sprint 2. Angka dapat ditarik ulang dari `data/silver/silver.parquet`, `data/gold/`, `reports/`, dan `log-keputusan.csv` (id K-xxx).

## Ringkasan

Kasus 20 (Hutan, lahan, dan lingkungan) mengintegrasikan tabel statis tutupan hutan (luas dan persen), tiga seri dinamis BPS (penutupan lahan menurut status kawasan `var1304`, luas lahan kritis `var588`, dan komponen penyusun IKLH `var2532`), serta tiga seri pembanding WDI (`AG.LND.FRST.K2`, `AG.LND.FRST.ZS`, dan `EN.ATM.PM25.MC.M3`). Dataset Silver pertama memuat 3.940 baris BPS yang lolos uji skema minimal dan berhasil dimuat ke basis data relasional DuckDB. Temuan terpenting pada Sprint 1 adalah terdeteksinya galat sistematis pada berkas mentah: kolom tahun 2020 pada tabel tutupan hutan tertukar antarprovinsi yang berhasil dibuktikan dan direkonstruksi secara matematis melalui relasi jumlah komponen dan persentase luas.

## Data dan lineage

Sebanyak 13 berkas mentah yang tercatat pada `data/raw/MANIFEST.csv` berhasil diekstraksi dan divalidasi nilai hash SHA-256 miliknya tanpa ada perbedaan:
- **BPS (snapshot 17 Oktober 2026)**: 3 JSON WebAPI dinamis, 1 JSON tabel statis tutupan hutan, 4 berkas CSV pendamping, dan 1 berkas `manifest_asal.json`.
- **WDI (snapshot 20 Oktober 2026)**: 1 berkas data JSON (`kelompok-01-hal-01.json`) memuat 60 seri untuk Indonesia, serta 3 berkas metadata indikator dan sumber.

Seluruh baris observasi di Silver memiliki kolom penelusuran asal (`_berkas_raw`) dan sidik jari kriptografis (`_sha256_raw`) yang dipetakan langsung dari MANIFEST tanpa intervensi manual.

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

Telah disusun tabel nasional periode × seri (1990–2025) di `reports/tabel-nasional.csv` dan pemetaan 4 pasangan rekonsiliasi di `reports/pasangan-rekonsiliasi.md`:
- **P1 (Luas Hutan)**: `tabel:sdg15_tutupan_hutan:luas_ribu_ha` vs WDI `AG.LND.FRST.K2` (10 tahun beririsan: 2014–2023). Kategori selisih: definisi (tutupan lahan berhutan KLHK vs definisi FAO pohon $\ge 5\text{ m}$ tanpa perkebunan) setelah konversi satuan $1\text{ ribu ha} = 10\text{ km}^2$.
- **P2 (Persentase Hutan)**: `tabel:sdg15_tutupan_hutan:persen` vs WDI `AG.LND.FRST.ZS` (10 tahun beririsan: 2014–2023). Kategori selisih: perbedaan penyebut (BPS menggunakan total luas penutupan lahan provinsi, WDI menggunakan luas daratan/land area).
- **P3 (Kualitas Udara)**: `var2532` (komponen IKU) vs WDI `EN.ATM.PM25.MC.M3` (5 tahun beririsan: 2019–2023). Kategori: kontekstual arah berlawanan (IKU semakin tinggi semakin baik, PM2.5 semakin tinggi semakin tercemar).
- **P4 (Kawasan vs Tutupan)**: `var1304` vs `tabel:sdg15_tutupan_hutan:luas_ribu_ha` (6 tahun beririsan: 2014–2018, 2023). Kategori: dua tabel dari sumber yang sama (rekalkulasi KLHK) dengan pembagian kategori berbeda (status penetapan kawasan vs kondisi biofisik tutupan).

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

---

## Sprint 2: Gold, rekonsiliasi, dan validasi

**Sprint Goal.** Setiap sel panel Gold yang terisi punya satu nilai yang tertelusur ke Silver, setiap
indikator punya satu satuan baku, Silver dan Gold tersimpan di DuckDB dengan kunci yang menolak sel
ganda, dan setiap baris rekonsiliasi berpasangan punya kategori serta penjelasan.

### Bukti ketiga butir Definition of Done

1. **Panel Gold provinsi x periode x indikator.** `python pipeline.py` menulis
   `data/gold/panel.parquet` (2.616 baris, 12 indikator, 5 seri) dan `data/gold/panel_lebar.parquet`
   (474 baris provinsi x tahun). Kunci `indikator + wilayah_kode + periode` diperiksa otomatis dan
   lolos; setiap sel terisi tertelusur ke baris Silver asal lewat `_berkas_raw`.
2. **Silver dan Gold di SQL.** `data/gold/gudang.duckdb` memuat tabel `silver` (3.940 baris),
   `gold_panel` (2.616), `gold_nasional` (184), dan `rekonsiliasi` (116). Skema ada di
   `src/gold/silver.sql` dan `src/gold/gold.sql`; alasan memilih DuckDB ada di `reports/basis-data.md`.
3. **Rekonsiliasi seri utama vs pembanding nasional.** `reports/rekonsiliasi.md` memuat 4 pasangan
   (P1 luas hutan, P2 persen hutan, P3 kualitas udara kontekstual, P4 kawasan vs tutupan), 25 baris
   berpasangan, dan 20 selisih terhitung. Setiap baris berpasangan punya kategori dan penjelasan.

### Validasi

`reports/validasi.md`: 17 aturan, **16 LOLOS, 0 GAGAL, 1 PERINGATAN** (anomali 2020 yang sudah
dikoreksi di Silver). Aturan Gold dan rekonsiliasi berjalan dari `validasi.jalankan(silver, gold)`.
Metrik: `results/124450013/metrics.json` (`aturan_validasi=17`, `aturan_lolos=16`,
`aturan_peringatan=1`, `berkas_terverifikasi=13`).
