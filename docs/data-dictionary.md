# Data Dictionary — Tim MBG (Kasus 20: Hutan, Lahan, dan Lingkungan)

Dokumen ini mendokumentasikan skema, tipe data, satuan, definisi, serta silsilah data (*data lineage*) untuk tabel **Silver** (`data/silver/silver.parquet`) dan rangkaian tabel **Gold** (`data/gold/*.parquet`) sesuai target Sprint 1 s.d. Sprint 2.

---

## 1. Tabel Silver: `data/silver/silver.parquet`

* **Jumlah Baris:** 3.940 baris (BPS) hingga 4.045 baris (dengan WDI).
* **Definisi Satu Baris:** Satu baris merepresentasikan observasi tunggal dari satu kombinasi: **seri indikator × wilayah × periode × rincian dimensi × berkas sumber**. Nilai dari sumber berbeda tidak digabung di sini.
* **Kunci Unik (*Composite Primary Key*):** `sumber`, `seri_kode`, `wilayah_kode`, `periode`, `rincian`, `_berkas_raw`.

| Nama Kolom | Tipe Data | Satuan Baku | Boleh Kosong | Rentang / Nilai Sah | Asal Kolom | Definisi & Keterangan |
|---|:---:|:---:|:---:|---|---|---|
| `sumber` | `string` | — | Tidak | `bps`, `wdi` | Nama folder sumber di `data/raw/` | Lembaga penerbit data resmi (*publisher*). |
| `seri_kode` | `string` | — | Tidak | `tabel:sdg15_tutupan_hutan:luas_ribu_ha`, `tabel:sdg15_tutupan_hutan:persen`, `var1304`, `var588`, `var2532`, `AG.LND.FRST.K2`, `AG.LND.FRST.ZS`, `EN.ATM.PM25.MC.M3` | Metadata BPS (`var_id`) dan World Bank Indicator ID | Identitas unik seri indikator. |
| `wilayah_kode` | `int64` | — | Tidak | `1100` – `9700`, `9999` | Kamus standar wilayah (Log K-001) | Kode wilayah baku: 2 digit kode provinsi BPS × 100. Kode `9999` melambangkan agregat Nasional (Indonesia). |
| `nama_wilayah` | `string` | — | Tidak | Aceh, Sumatera Utara, ..., Papua Barat Daya, INDONESIA (39 nama) | Pemetaan wilayah BPS 2025 | Nama provinsi baku berdasarkan susunan 38 provinsi tahun 2025. |
| `periode` | `string` | — | Tidak | `1990` s.d. `2025` | Kolom `tahun` BPS / `date` WDI | Periode waktu observasi data dalam format tahun baku 4 digit. |
| `jenis_periode` | `string` | — | Tidak | `tahun` | Diturunkan dari kolom `periode` (Log K-009) | Frekuensi observasi penerbitan data (tahunan). |
| `rincian` | `string` | — | Tidak | `total`, `hutan`, `non_hutan`, `kritis`, `sangat_kritis`, `kawasan_hutan`, `apl`, `kualitas_udara`, `kualitas_air`, `kualitas_tutupan_lahan`, `kualitas_lahan`, `kualitas_ekosistem_gambut`, `kualitas_air_laut` | Kolom `turvar` BPS / `tutupan` tabel statis | Kategori pecahan atau dimensi indikator. Nilai tanpa pecahan ditulis `total`. |
| `nilai` | `float64` | Mengikuti kolom `satuan` | Tidak | $\ge 0$ (luas/indeks), $0$ – $100$ (persen) | Kolom `nilai` mentah setelah transformasi satuan | Nilai numerik observasi. Sel kosong (*missing*) atau *null* tidak dimuat ke Silver. |
| `satuan` | `string` | — | Tidak | `ribu_hektar`, `persen`, `indeks`, `km2`, `mikrogram_per_m3` | Keputusan wrangling (Log K-002, K-005, K-018) | Satuan ukuran baku metrik. Setiap seri hanya memiliki satu satuan yang seragam. |
| `sdg_kode` | `string` | — | Ya | `15.1.1`, `15.3.1`, `11.6.2`, `15` | Metadata sumber & koreksi katalog (Log K-007, K-020) | Kode target Tujuan Pembangunan Berkelanjutan (SDG) yang terkait. |
| `batas_bawah` | `float64` | — | Ya | Kosong (*NaN*) | Ekstraksi sumber WHO (tidak ada di kasus 20) | Batas bawah interval kepercayaan estimasi. |
| `batas_atas` | `float64` | — | Ya | Kosong (*NaN*) | Ekstraksi sumber WHO (tidak ada di kasus 20) | Batas atas interval kepercayaan estimasi. |
| `rujukan_tahun` | `int64` | — | Ya | Kosong (*NaN*) | Catatan teknis survei BPS | Rentang jendela tahun rujukan jika menggunakan survei bertingkat. |
| `_berkas_raw` | `string` | — | Tidak | Contoh: `bps/2026-10-17/sdg15_iklh.csv` | Jalur relatif terhadap folder `data/raw/` | **Lineage:** Berkas mentah spesifik asal baris data ini diekstrak. |
| `_sha256_raw` | `string` | — | Tidak | String heksadesimal 64 karakter SHA-256 | `src.common.manifest.sha256_raw` | **Lineage:** Sidik jari kriptografis berkas mentah untuk audit integritas data. |

---

## 2. Tabel Gold: `data/gold/panel.parquet` (Panel Provinsi Panjang)

* **Definisi Satu Baris:** Satu baris merepresentasikan satu sel grid kombinasi: **indikator × provinsi × periode**, mencakup sel terisi maupun sel kosong yang telah terklasifikasi.
* **Kunci Unik (*Composite Primary Key*):** `indikator`, `wilayah_kode`, `periode`.

| Nama Kolom | Tipe Data | Satuan Baku | Boleh Kosong | Rentang / Nilai Sah | Asal Kolom | Definisi & Keterangan |
|---|:---:|:---:|:---:|---|---|---|
| `indikator` | `string` | — | Tidak | `tabel:sdg15_tutupan_hutan:luas_ribu_ha`, `tabel:sdg15_tutupan_hutan:persen [tutupan=hutan]`, `var1304`, `var2532 [komponen=ika]`, `var2532 [komponen=iktl]`, `var2532 [komponen=iku]`, `var588` | Diturunkan dari seri dan rincian utama Silver | Label deret indikator utama yang dimonitor pada level provinsi. |
| `seri_kode` | `string` | — | Tidak | `tabel:sdg15_tutupan_hutan:luas_ribu_ha`, `tabel:sdg15_tutupan_hutan:persen`, `var1304`, `var2532`, `var588` | Silver `seri_kode` | Kode seri asal di tingkat Silver. |
| `rincian` | `string` | — | Tidak | `total`, `tutupan=hutan`, `komponen=ika`, `komponen=iktl`, `komponen=iku` | Silver `rincian` | Dimensi spesifik indikator. |
| `wilayah_kode` | `int64` | — | Tidak | `1100` – `9700` | Silver `wilayah_kode` | Kode provinsi BPS (hanya 38 provinsi, tanpa kode nasional 9999). |
| `nama_wilayah` | `string` | — | Tidak | Aceh s.d. Papua Barat Daya (38 provinsi) | Silver `nama_wilayah` | Nama resmi provinsi susunan 2025. |
| `periode` | `string` | — | Tidak | `2006` s.d. `2024` | Grid panel tahunan | Tahun observasi panel. |
| `jenis_periode` | `string` | — | Tidak | `tahun` | Silver `jenis_periode` | Frekuensi observasi (tahunan). |
| `nilai` | `float64` | Mengikuti kolom `satuan` | Ya (jika kosong) | Sesuai rentang Silver | Silver `nilai` | Nilai indikator. Bernilai *null/NaN* jika status sel bukan `terisi`. |
| `satuan` | `string` | — | Tidak | `ribu_hektar`, `persen`, `indeks`, `hektar` | Silver `satuan` | Satuan baku indikator. Satu indikator hanya memiliki satu satuan seragam. |
| `status_sel` | `string` | — | Tidak | `terisi`, `missing`, `tidak_diterbitkan`, `belum_ada`, `batas_lama` | Hasil audit grid panel (Sprint 2) | Kategori status sel: `terisi` (ada nilai), `belum_ada` (provinsi baru belum dimekarkan), `tidak_diterbitkan` (misal DKI Jakarta di lahan kritis), `missing` (data bolong). |
| `penanda` | `string` | — | Ya | `outlier`, `patahan_wilayah`, `perbedaan_struktural` | Laporan deteksi anomali Sprint 1 | Penanda kualitas data tanpa mengubah nilai asli. |
| `rujukan_tahun` | `float64` | — | Ya | Kosong (*NaN*) | Silver `rujukan_tahun` | Rujukan jendela survei. |
| `_berkas_raw` | `string` | — | Ya | Relatif terhadap `data/raw/` | Silver `_berkas_raw` | Lineage berkas mentah (hanya terisi jika sel berstatus `terisi`). |
| `_sha256_raw` | `string` | — | Ya | Hash SHA-256 | Silver `_sha256_raw` | Lineage sidik berkas mentah. |

---

## 3. Tabel Gold: `data/gold/nasional.parquet` (Tabel Seri Tingkat Nasional)

* **Definisi Satu Baris:** Satu baris merepresentasikan observasi seri indikator pada tingkat agregat **Nasional (Indonesia / wilayah_kode = 9999)** atau indikator pembanding internasional (WDI).
* **Kunci Unik (*Composite Primary Key*):** `seri_kode`, `rincian`, `periode`.

| Nama Kolom | Tipe Data | Keterangan & Asal |
|---|:---:|---|
| `seri_kode` | `string` | Kode seri BPS atau WDI (`AG.LND.FRST.K2`, `AG.LND.FRST.ZS`, `EN.ATM.PM25.MC.M3`, dll.). |
| `rincian` | `string` | Rincian dimensi (misal: `total`, `tutupan=hutan`, `komponen=iku`). |
| `sumber` | `string` | Asal penerbit data (`bps` atau `wdi`). |
| `periode` | `string` | Tahun observasi (1990–2025). |
| `jenis_periode` | `string` | Frekuensi observasi (`tahun`). |
| `nilai` | `float64` | Nilai metrik nasional. |
| `satuan` | `string` | Satuan metrik (`km2`, `persen`, `ribu_hektar`, `indeks`, `mikrogram_per_m3`). |
| `asal` | `string` | `baris_indonesia` (disediakan langsung oleh BPS) atau `pembanding` (berasal dari WDI). |
| `_berkas_raw` | `string` | Lineage berkas mentah asal baris nasional ini. |
| `_sha256_raw` | `string` | Lineage hash SHA-256 berkas mentah. |

---

## 4. Tabel Gold: `data/gold/rekonsiliasi.parquet` (Rekonsiliasi BPS vs WDI)

* **Definisi Satu Baris:** Satu baris merepresentasikan komparasi antara **seri utama nasional (BPS)** dan **seri pembanding (WDI / FAO)** untuk periode tahun yang sama.
* **Kunci Unik (*Composite Primary Key*):** `pasangan_id`, `seri_pembanding`, `rincian_pembanding`, `periode`.

| Nama Kolom | Tipe Data | Keterangan & Asal |
|---|:---:|---|
| `pasangan_id` | `string` | ID Pasangan rekonsiliasi (`P1`, `P2`, `P3`, `P4`) merujuk `reports/pasangan-rekonsiliasi.md`. |
| `jenis` | `string` | `selisih` (dihitung angka deviasinya) atau `konteks` (disandingkan sebagai latar belakang). |
| `seri_utama` | `string` | Seri data nasional rujukan utama (BPS / KLHK). |
| `rincian_utama` | `string` | Rincian dimensi seri utama yang diperbandingkan. |
| `seri_pembanding` | `string` | Seri data pembanding internasional (WDI / World Bank / FAO). |
| `rincian_pembanding` | `string` | Rincian dimensi seri pembanding (`total`). |
| `periode` | `string` | Tahun pengamatan yang beririsan. |
| `nilai_utama` | `float64` | Nilai dari seri utama nasional (sudah disetarakan satuannya jika diperlukan). |
| `nilai_pembanding`| `float64` | Nilai dari seri pembanding internasional. |
| `selisih` | `float64` | Hasil perhitungan: $\text{nilai\_utama} - \text{nilai\_pembanding}$. |
| `persen_selisih` | `float64` | Persentase deviasi terhadap seri pembanding: $(\text{selisih} / \text{nilai\_pembanding}) \times 100\%$. |
| `kategori` | `string` | Klasifikasi penyebab selisih baku (misal: `definisi_berbeda`, `metodologi_berbeda`, `vintage_berbeda`, `identik`). |
| `penjelasan` | `string` | Narasi argumentatif mengenai latar belakang penyebab timbulnya selisih data. |

---

## 5. Ringkasan Pasangan Rekonsiliasi (Kasus 20)

| ID Pasangan | Seri Utama (BPS/Nasional) | Seri Pembanding (WDI) | Jenis | Kategori Dugaan Selisih | Alasan Keterbandingan |
|:---:|---|---|:---:|---|---|
| **P1** | `tabel:sdg15_tutupan_hutan:luas_ribu_ha` [tutupan=hutan] | `AG.LND.FRST.K2` | `selisih` | `definisi_berbeda` | KLHK memakai citra satelit tutupan hutan, sedangkan FAO (WDI) memakai definisi kanopi pohon $\ge 5$m tanpa perkebunan sawit. Faktor konversi: 1 ribu ha = 10 km². |
| **P2** | `tabel:sdg15_tutupan_hutan:persen` [tutupan=hutan] | `AG.LND.FRST.ZS` | `selisih` | `metodologi_berbeda` | BPS menghitung persentase terhadap total tutupan daratan provinsi, WDI menghitung terhadap total luas daratan (*land area*). |
| **P3** | `var1304` [kawasan=kawasan_hutan] | `tabel:sdg15_tutupan_hutan:luas_ribu_ha` [tutupan=hutan] | `selisih` | `definisi_berbeda` | Penutupan hutan di dalam kawasan hutan negara vs total penutupan hutan daratan nasional. |
| **P4** | `var2532` [komponen=iku] | `EN.ATM.PM25.MC.M3` | `konteks` | `tidak_dapat_dibandingkan` | IKU adalah indeks komposit kualitas udara (skala 0–100), sedangkan WDI mengukur konsentrasi partikulat debu halus PM2.5 ($\mu g/m^3$). |

---

## 6. Contoh Penelusuran Silsilah Data (*Lineage Audit Trail*)

Setiap baris data pada tabel Silver maupun Gold dapat diverifikasi keabsahannya hingga ke berkas fisik mentah asalnya:

### Contoh Baris Data di `silver.parquet`:
```python
{
    'sumber': 'bps',
    'seri_kode': 'tabel:sdg15_tutupan_hutan:luas_ribu_ha',
    'wilayah_kode': 1100,
    'nama_wilayah': 'Aceh',
    'periode': '2014',
    'jenis_periode': 'tahun',
    'rincian': 'total',
    'nilai': 5647.3,
    'satuan': 'ribu_hektar',
    '_berkas_raw': 'bps/2026-10-17/sdg15_tutupan_hutan.csv',
    '_sha256_raw': '93f5d2d2ce3e9f5db97fd8409fa658f08c9cadd44634c7d1f8b3ee1234861bd1'
}
```
* **Verifikasi Berkas:** Menunjuk ke berkas mentah `data/raw/bps/2026-10-17/sdg15_tutupan_hutan.csv`.
* **Integritas Berkas:** Nilai hash `_sha256_raw` cocok 100% dengan entri di `data/raw/MANIFEST.csv`.
* **Penelusuran ke Gold:** Pada `data/gold/panel.parquet`, baris di atas tertelusur menjadi indikator `tabel:sdg15_tutupan_hutan:luas_ribu_ha` wilayah `1100` tahun `2014` dengan nilai `5647.3` dan status `terisi`.
