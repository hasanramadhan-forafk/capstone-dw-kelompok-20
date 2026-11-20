# Data Dictionary — MBG : Memang Banyak tuGas (Kasus 20: Hutan, Lahan, dan Lingkungan)

Dokumen ini mendokumentasikan skema, tipe data, satuan, definisi, serta silsilah data (*data lineage*) untuk tabel **Silver** (`data/silver/silver.parquet`). Kolom Gold akan ditambahkan pada Sprint 2–3.

---

## 1. Tabel Utama: `data/silver/silver.parquet`

* **Jumlah Baris:** 3.940 baris (BPS) hingga 4.045 baris (dengan WDI).
* **Definisi Satu Baris:** Satu baris merepresentasikan observasi tunggal dari satu kombinasi: **seri indikator × wilayah × periode × rincian dimensi × berkas sumber**.
* **Kunci Unik (*Composite Primary Key*):** `sumber`, `seri_kode`, `wilayah_kode`, `periode`, `rincian`, `_berkas_raw`.

| Nama Kolom | Tipe Data | Satuan Baku | Boleh Kosong | Rentang / Nilai Sah | Asal Kolom | Definisi & Keterangan |
|---|:---:|:---:|:---:|---|---|---|
| `sumber` | `string` | — | Tidak | `bps`, `wdi` | Nama folder sumber di `data/raw/` | Lembaga penerbit data resmi (*publisher*). |
| `seri_kode` | `string` | — | Tidak | `tabel:sdg15_tutupan_hutan:luas_ribu_ha`, `tabel:sdg15_tutupan_hutan:persen`, `var1304`, `var588`, `var2532`, `AG.LND.FRST.K2`, `AG.LND.FRST.ZS`, `EN.ATM.PM25.MC.M3` | Metadata BPS (`var_id`) dan World Bank Indicator ID | Identitas unik seri indikator. Definisi rinci pada tabel seri di bawah. |
| `wilayah_kode` | `int64` | — | Tidak | `1100` – `9700`, `9999` | Kamus standar wilayah (Log K-001) | Kode wilayah baku: 2 digit kode provinsi BPS × 100. Kode `9999` melambangkan agregat Nasional (Indonesia). |
| `nama_wilayah` | `string` | — | Tidak | Aceh, Sumatera Utara, ..., Papua Barat Daya, INDONESIA (39 nama) | Pemetaan wilayah BPS 2025 | Nama provinsi baku berdasarkan susunan 38 provinsi tahun 2025. |
| `periode` | `string` | — | Tidak | `1990` s.d. `2025` | Kolom `tahun` BPS / `date` WDI | Periode waktu observasi data dalam format tahun baku 4 digit. |
| `jenis_periode` | `string` | — | Tidak | `tahun` | Diturunkan dari kolom `periode` (Log K-009) | Frekuensi observasi penerbitan data. Seluruh data kasus ini berfrekuensi tahunan. |
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

## 2. Rincian Dimensi (*Breakdown*) per Seri

Penulisan rincian dimensi diseragamkan dengan huruf kecil dan pemisah *underscore*:

1. **Seri Tutupan Hutan (`tabel:sdg15_tutupan_hutan`):**
   * `total`: Luas keseluruhan daratan provinsi.
   * `hutan`: Areal berpenutupan hutan.
   * `non_hutan`: Areal non-hutan (lahan terbuka, terbangun, perkebunan).
2. **Seri Lahan Kritis (`var588`):**
   * `total`: Akumulasi lahan kritis dan sangat kritis.
   * `kritis`: Kategori lahan dengan tingkat kerusakan kritis.
   * `sangat_kritis`: Kategori lahan dengan tingkat kerusakan sangat kritis.
3. **Seri Tutupan Kawasan (`var1304`):**
   * `total`: Total luas daratan.
   * `kawasan_hutan`: Areal di dalam kawasan hutan negara (Hutan Lindung, Konservasi, Produksi).
   * `apl`: Areal Penggunaan Lain (di luar kawasan hutan negara).
4. **Seri Komponen IKLH (`var2532`):**
   * `kualitas_udara`: Indeks Kualitas Udara (IKU).
   * `kualitas_air`: Indeks Kualitas Air (IKA).
   * `kualitas_tutupan_lahan`: Indeks Kualitas Tutupan Lahan (IKTL).
   * `kualitas_lahan`: Indeks Kualitas Lahan (IKL).
   * `kualitas_ekosistem_gambut`: Indeks Kualitas Ekosistem Gambut (IKEG).
   * `kualitas_air_laut`: Indeks Kualitas Air Laut (IKAL).

---

## 3. Satuan Baku, Kode SDG, dan Aturan Konversi

| Kode Seri | Satuan Asal di Mentah | Satuan Baku Silver | Faktor Pembagi / Konversi | Kode SDG | Alasan & Bukti Sumber |
|---|:---:|:---:|:---:|:---:|---|
| `tabel:sdg15_tutupan_hutan:luas_ribu_ha` | `Ribu Ha` | `ribu_hektar` | 1 (Tetap) | 15.1.1 | Judul tabel BPS menyebutkan *(Ribu Ha)*. |
| `tabel:sdg15_tutupan_hutan:persen` | `%` | `persen` | 1 (Tetap) | 15.1.1 | Header kolom BPS mencantumkan `%`. |
| `var1304` | `Ribu Hektar` | `ribu_hektar` | 1 (Tetap) | 15.1.1 | BPS `var.unit`: `Ribu Hektar`. Kode SDG dikoreksi dari 15.3.1 ke 15.1.1 karena mengukur tutupan hutan. |
| `var588` | `Hektar` | `ribu_hektar` | **1.000** | 15.3.1 | BPS `var.unit`: `Hektar`. **Dibagi 1.000** agar seragam dengan seri luas lainnya (Log K-002). |
| `var2532` | *(kosong)* | `indeks` | 1 (Tetap) | 15 / 11.6.2 | Skala 0–100. Komponen udara merujuk 11.6.2; agregat merujuk SDG 15 (Log K-005, K-020). |
| `AG.LND.FRST.K2` | `sq. km` | `km2` | 1 (Tetap) | 15.1.1 | WDI: Luas tutupan hutan nasional. |
| `AG.LND.FRST.ZS` | `% of land area` | `persen` | 1 (Tetap) | 15.1.1 | WDI: Persentase luas hutan terhadap luas daratan. |
| `EN.ATM.PM25.MC.M3` | `ug/m3` | `mikrogram_per_m3` | 1 (Tetap) | 11.6.2 | WDI: Paparan polusi udara tahunan rata-rata penduduk. |

---

## 4. Standar Kode Wilayah

* **Provinsi:** Menggunakan kode resmi 2-digit BPS dikalikan 100 (contoh: Aceh = `1100`, Jawa Barat = `3200`, Papua Barat Daya = `9600`).
* **Nasional (Indonesia):** Ditetapkan secara konsisten dengan kode **`9999`**. Kode WDI `ID`/`IDN` dipetakan ke `9999`.

---

## 5. Contoh Penelusuran Satu Baris (*Lineage Audit Trail*)

Setiap baris data pada tabel Silver dapat diverifikasi keabsahannya hingga ke berkas fisik mentah asalnya. Berikut adalah contoh audit penelusuran satu baris data konkret:

### Baris Data Terpilih di `silver.parquet`:
```python
{
    'sumber': 'bps',
    'seri_kode': 'tabel:sdg15_tutupan_hutan:luas_ribu_ha',
    'wilayah_kode': 1100,
    'nama_wilayah': 'ACEH',
    'periode': '2014',
    'jenis_periode': 'tahun',
    'rincian': 'total',
    'nilai': 5647.3,
    'satuan': 'ribu_hektar',
    '_berkas_raw': 'bps/2026-10-17/sdg15_tutupan_hutan.csv',
    '_sha256_raw': '93f5d2d2ce3e9f5db97fd8409fa658f08c9cadd44634c7d1f8b3ee1234861bd1'
}
```

### Langkah Pembuktian Silsilah (*Step-by-Step*):
1. **Identifikasi Berkas Sumber:** Kolom `_berkas_raw` merujuk langsung ke berkas fisik `data/raw/bps/2026-10-17/sdg15_tutupan_hutan.csv`.
2. **Pencocokan Integritas Kriptografis:**
   * Di dalam berkas `data/raw/MANIFEST.csv`, berkas `bps/2026-10-17/sdg15_tutupan_hutan.csv` memiliki catatan hash:
     $$\texttt{93f5d2d2ce3e9f5db97fd8409fa658f08c9cadd44634c7d1f8b3ee1234861bd1}$$
   * Nilai ini cocok 100% dengan kolom `_sha256_raw` pada baris data, membuktikan bahwa data diekstrak dari berkas asli yang tidak pernah dimanipulasi sejak diunduh.
3. **Pencocokan Nilai pada Berkas Mentah:**
   * Membuka berkas `data/raw/bps/2026-10-17/sdg15_tutupan_hutan.csv` pada baris wilayah `ACEH`, tahun `2014`, tutupan `jumlah`, ukuran `luas_ribu_ha`:
     ```csv
     ACEH,2014,jumlah,luas_ribu_ha,5647.3,,
     ```
   * Nilai mentah adalah `5647.3` dengan rincian `jumlah` yang dipetakan menjadi `total`. Terbukti nilai pada Silver persis sama dan setia pada sumber aslinya.