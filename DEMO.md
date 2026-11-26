# Naskah Demo Sprint 2 (10 menit) - Kasus 20

Demo memperlihatkan perjalanan satu angka dari Silver ke panel Gold, ke DuckDB, ke tabel rekonsiliasi,
lalu ke aturan validasi Gold. Rekam layar terminal dan editor. Unggah video demo paling lambat
**29 November 2026** dan tautkan di Papan Tim.

| Menit | Tunjukkan | Perintah atau berkas |
|---|---|---|
| 0-1 | Sprint Goal dan tiga butir DoD | `sprint/sprint-2/sprint-goal.md` |
| 1-3 | Satu perintah dari mentah sampai Gold, SQL, validasi | `python pipeline.py` |
| 3-4 | Panel Gold panjang dan lebar | `data/gold/panel.parquet`, `data/gold/panel_lebar.parquet`, `reports/panel-gold.md` (bila ada) |
| 4-5 | Kunci panel unik dan satu satuan per indikator | `reports/validasi.md` baris `gold: kunci panel unik` dan `gold: satu satuan per indikator` |
| 5-6 | Silver + Gold di DuckDB | kueri di bawah; `reports/basis-data.md` |
| 6-8 | Rekonsiliasi P1/P2: BPS vs WDI, kategori dan selisih | `reports/rekonsiliasi.md`; median selisih relatif 0,50% |
| 8-9 | Setiap sel Gold tertelusur ke Silver dan setiap baris berpasangan berkategori | `reports/validasi.md` baris `gold: sel tertelusur ke Silver` dan `rekonsiliasi: baris berpasangan berkategori` |
| 9-10 | Metrik dan rencana Sprint 3 | `results/124450013/metrics.json`; `sprint/sprint-2/sprint-goal.md` |

## Kueri DuckDB

```bash
python - <<'EOF'
import duckdb
con = duckdb.connect("data/gold/gudang.duckdb", read_only=True)
print(con.sql("SHOW TABLES"))
print(con.sql("SELECT count(*) AS baris FROM gold_panel"))
print(con.sql("""
    SELECT pasangan_id, kategori, count(*) AS n
    FROM rekonsiliasi
    GROUP BY ALL
    ORDER BY pasangan_id, kategori
"""))
EOF
```

## Poin narasi

- `python pipeline.py` menjalankan ekstraksi, Silver, Gold, dan validasi dalam satu perintah.
- Panel Gold memakai kunci `indikator + wilayah_kode + periode`; satu indikator hanya punya satu satuan.
- Setiap sel panel yang terisi punya baris Silver asal lewat `_berkas_raw`; tidak ada nilai yang dikarang di Gold.
- Rekonsiliasi memakai gabung luar: periode tanpa pasangan tetap tampil dengan kategori `tanpa pasangan`.
- Setiap baris berpasangan (`asal = keduanya`) punya kategori baku dan penjelasan; ini diperiksa otomatis.
- Hasil validasi terakhir: 17 aturan, 16 LOLOS, 0 GAGAL, 1 PERINGATAN (anomali 2020 yang sudah dikoreksi).

## Uji reproduksi (tugas Reproduksi)

Klon repo ke folder baru, jalankan `unduh_data.py` dan `pipeline.py`, lalu bandingkan berkas Gold dengan
yang di-commit:

```bash
python - <<'EOF'
import pandas as pd
for f in ["silver/silver", "gold/panel", "gold/nasional", "gold/rekonsiliasi"]:
    a = pd.read_parquet(f"data/{f}.parquet")
    b = pd.read_parquet(f"/jalur/repo-asli/data/{f}.parquet")
    print(f, "sama" if a.equals(b) else "berbeda")
EOF
```
