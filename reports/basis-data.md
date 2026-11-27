# Silver dan Gold di SQL

Dihasilkan `python pipeline.py` (`src/gold/muat_sql.py`). DDL: `src/gold/silver.sql` dan `src/gold/gold.sql`. Basis data `data/gold/gudang.duckdb` (4.73 MB) dibuat ulang setiap kali dan tidak di-commit.

## Isi

| tabel | baris | sumber |
|---|---|---|
| seri | 8 | docs/seri.csv |
| silver | 3940 | data/silver/silver.parquet |
| gold_panel | 2616 | data/gold/panel_provinsi.parquet |
| gold_nasional | 184 | data/gold/nasional.parquet |
| rekonsiliasi | 36 | data/gold/rekonsiliasi.parquet |
| dokumen_mentah | 9 | data/raw/**/*.json |

Jumlah baris setiap tabel yang memiliki sumber Parquet dicocokkan langsung saat dimuat; beda satu baris pun menghentikan pipeline.

## Kunci primer dan batasan

- `seri`: (seri_kode) — kamus metadata baku referensi *foreign key*.
- `silver`: (sumber, seri_kode, wilayah_kode, periode, rincian, _berkas_raw) — dua snapshot boleh berdampingan.
- `gold_panel`: (indikator, wilayah_kode, periode) — satu nilai per sel; CHECK status sel dan nilai kosong hanya bila sel kosong.
- `gold_nasional`: (seri_kode, rincian, periode) — seri utama, pembanding, dan agregat nasional.
- `rekonsiliasi`: (pasangan_id, seri_pembanding, rincian_pembanding, periode) — CHECK kategori baku dan selisih = utama − pembanding.
- `dokumen_mentah`: (_berkas_raw) — penyimpanan dokumen JSON utuh per berkas.

Uji kunci primer pada `gold_panel`: memasukkan ulang satu baris yang sudah ada → ditolak (ConstraintException).

## Mengapa DuckDB, dan mengapa tabel (bukan dokumen)

DuckDB dipilih karena satu berkas tanpa server (*serverless*), mendukung eksekusi kolumnar untuk agregasi/pivot analitik, dan dapat membaca Parquet secara langsung; SQLite atau PostgreSQL sama sahnya. Lapis Silver dan Gold disimpan sebagai **tabel relasional** karena pertanyaan analisisnya selalu berdimensi `seri × wilayah × periode × rincian` dan membutuhkan penegakan integritas (kunci primer yang menolak sel ganda, *foreign key* ke `seri`, serta `CHECK` status/kategori). Sebaliknya, berkas JSON mentah disimpan sebagai **dokumen** (`dokumen_mentah`) hanya sebagai pembanding dan arsip lapis Bronze: bentuk dokumen menjaga struktur bersarang dan metadata asli (`var`, `vervar`, `turvar`), tetapi setiap kueri harus mengurai struktur JSON dan tidak memiliki kunci primer tingkat observasi.

| pertanyaan | tabel_silver | dokumen_json | ms_silver | ms_dokumen | catatan |
|---|---|---|---|---|---|
| berapa angka var1304 di `bps/2026-10-17/json/sdg15_tutupan_kawasan.json` | 627 | 627 | 4.59 | 32.55 | dokumen menghitung semua kunci datacontent pada JSON bersarang (termasuk sel kosong/non-panel); tabel Silver hanya baris observasi tervalidasi |
