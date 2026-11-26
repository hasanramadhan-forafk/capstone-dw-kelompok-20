# Sprint 1 (9–22 November 2026) — Kasus 20: Hutan, Lahan, dan Lingkungan

## Sprint Goal
Seluruh berkas mentah Kasus 20 (BPS dan WDI) berhasil terbaca lengkap dengan silsilah kriptografis (lineage), setiap seri telah ditetapkan satuan baku dan kode SDG dengan bukti dari metadata sumber, anomali data (termasuk pergeseran kolom 2020) telah teridentifikasi dan dicatat di log keputusan, serta tabel Silver pertama berhasil dibangun dan lolos pemeriksa skema minimal maupun aturan validasi dasar, sehingga tim siap melangkah ke penyusunan panel Gold dan rekonsiliasi pada Sprint 2.

## Definition of Done (DoD) Sprint 1
- [x] Seluruh berkas mentah di `data/raw/` (13 berkas) lolos verifikasi hash SHA-256 terhadap `MANIFEST.csv`.
- [x] Parser ekstraksi mampu membaca seluruh format mentah (CSV dan JSON berhalaman BPS, serta data & metadata WDI) tanpa menghilangkan baris.
- [x] Profil statistik dan deteksi calon anomali selesai dievaluasi untuk seluruh seri utama.
- [x] Keputusan penanganan galat input, patahan wilayah, dan deduplikasi tercatat transparan di `log-keputusan.csv`.
- [x] Tabel `data/silver/silver.parquet` berhasil dibentuk dan lolos pengujian `python -m src.common.skema`.
- [x] Aturan validasi dasar Silver (luas non-negatif, rentang persen 0–100, keunikan kunci primer) berjalan sukses di `pipeline.py`.
- [x] Dokumen `docs/data-dictionary.md` terisi lengkap untuk seluruh kolom Silver beserta contoh penelusuran lineage.
- [x] Berkas `results/<nim>/metrics.json` seluruh anggota tim telah di-commit dan dikirimkan sebagai bukti artefak di Papan Tim.