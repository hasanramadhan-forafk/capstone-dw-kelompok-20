# AI_LOG — MBG : Memang Banyak tuGas

Satu baris per pemakaian AI yang bermakna (ChatGPT, Claude, Copilot, Bravais, dan sejenisnya).
Ringkas dan jujur; transkrip penuh tidak diminta. Yang dinilai bukan "pakai AI atau tidak",
melainkan "mengerti atau tidak" — isi kolom terakhir dengan apa yang Anda ubah dari keluarannya.

| Tanggal | Siapa (NIM) | Alat | Untuk apa | Apa yang diubah dari keluarannya |
|---|---|---|---|---|
| 2026-11-03 | 12345678 | Copilot | kerangka DataLoader | ganti normalisasi, tambah seed worker |
| 2026-11-18 | 124450026 | Claude | kerangka transformasi Silver kasus 20 | Memperbaiki IndentationError karena ada indentasi yang salah pada saat code dijalankan |
| 2026-11-20 | 124450026 | Claude | mencocokkan satuan dan kode SDG semua seri dengan metadata untuk revisi #8 | membuka manifest_asal.json dan memeriksadefinisi SDG |
| 2026-11-20 | 124450013 | Gemini | Rancangan awal modul `src/validasi/__init__.py`: 9 aturan keras dan peringatan untuk Silver Kasus 20 | Memisahkan logika menjadi 3 berkas modular (`aturan.py`, `khusus.py`, `__init__.py`) mengikuti arsitektur referensi sprint-1; menghapus ketergantungan pada `konfigurasi.py` yang belum ada di repo tim |
| 2026-11-20 | 124450013 | Gemini | Penyusunan isi `docs/data-dictionary.md` untuk seluruh kolom Silver | Menyesuaikan contoh baris penelusuran lineage dengan nilai nyata dari `silver.parquet` repo tim |
| 2026-11-20 | 124450013 | Gemini | Draf komentar pelaporan ke dosen pembimbing (validasi, data dictionary, penutupan sprint) | Mempersingkat menjadi format ringkas dan menyesuaikan tautan branch dengan nama branch aktif tim |
| 2026-11-20 | 124450013 | Gemini | Penyusunan naskah DEMO.md Sprint 1 | menyusun kerangka naskah 5 menit |
| 2026-11-21 | 124450087 | Claude | Merancang skema SQL  Sprint 1 | mengubah data tabular (tabel parquet) menjadi struktur database relasional |
| 2026-11-25 | 124450013 | Gemini | Rancangan modul validasi Gold dan Rekonsiliasi `src/validasi/gold.py` (Sprint 2) | Menghilangkan ketergantungan impor internal referensi (`src.gold.rekonsiliasi`, `src.silver.deret`); menyederhanakan validasi toleransi selisih floating-point |
| 2026-11-25 | 124450013 | Gemini | Integrasi validasi Gold ke `src/validasi/__init__.py` dan penanganan error tabulate | Menambahkan blok try-except fallback ke `to_string()` jika paket tabulate belum terpasang agar pipeline tidak crash |
| 2026-11-25 | 124450013 | Gemini | Pembaruan kamus data `docs/data-dictionary.md` dengan skema Gold (panel, nasional, rekonsiliasi) | Menyesuaikan penjelasan dimensi indikator dan status sel dengan konteks Kasus 20 tim |
| 2026-11-25 | 124450013 | Gemini | Penyusunan Sprint Goal dan log sprint anggota untuk Sprint 2 | Memastikan keselarasan Definition of Done Sprint 2 dengan target Papan Tim |
| 2026-11-26 | 124450026 | Gemini | modul panel lebar src/gold/lebar.py | membantu baca isi dari panel panjang |