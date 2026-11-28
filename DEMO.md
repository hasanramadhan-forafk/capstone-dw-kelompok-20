# Naskah Demo Sprint 2 (±4 Menit) — Tim MBG (Kasus 20)

| Menit | Topik | Perintah / Berkas | Narasi Singkat |
|:---:|---|---|---|
| **00:00–00:30** | Pembukaan | `sprint/sprint-2/sprint-goal.md` | Perkenalan Tim MBG (Kasus 20) dan 3 target Sprint 2: Panel Gold, DuckDB, dan Rekonsiliasi. |
| **00:30–01:45** | Eksekusi Pipeline | `python pipeline.py` | Jalankan satu perintah: 13 berkas cocok `MANIFEST.csv` $\to$ Silver (3.940 baris) $\to$ Gold (Panel, Nasional, Rekonsiliasi, DuckDB) $\to$ Validasi. |
| **01:45–03:00** | Panel, DuckDB & Rekonsiliasi | `reports/basis-data.md` & `reports/rekonsiliasi.md` | Tunjukkan panel 2.616 baris, bukti PK DuckDB menolak duplikat, dan ringkasan selisih BPS vs WDI. |
| **03:00–04:00** | Validasi & Penutup | `reports/validasi.md` & `results/124450013/metrics.json` | Tunjukkan 17 aturan validasi (16 `LOLOS`, 1 `PERINGATAN` 2020, 0 `GAGAL`) dan metrik tercatat. |

### Perintah Uji Reproduksi:
```bash
python unduh_data.py --kasus 20
python pipeline.py
```
