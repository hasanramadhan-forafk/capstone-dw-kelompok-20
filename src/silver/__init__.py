"""Tahap 2–4 — Profil, pembersihan, dan penyeragaman ke Silver (pertemuan II–VII). Milik tim.

Keluaran: data/silver/silver.parquet dengan skema minimal di src/common/skema.py.
Satu baris = satu seri x wilayah x periode x rincian x berkas sumber. Nilai dari sumber berbeda
TIDAK digabung di sini. Setiap keputusan pembersihan dicatat di log-keputusan.csv.
Versi sementara: Silver dibangun dari CSV BPS lewat src/silver/transformasi.py (keputusan K-010:
JSON tidak dimuat). Argumen `ekstraksi` diterima agar cocok dengan pipeline.py tetapi belum dipakai;
ganti dengan tabel hasil Ekstraksi bila keluarannya sudah dibakukan.
"""


def jalankan(ekstraksi=None):
    # impor di dalam fungsi agar `python -m src.silver.transformasi` tidak memicu peringatan runpy
    from src.silver.transformasi import SILVER, baca_mentah, ke_silver

    silver, laporan = ke_silver(baca_mentah())
    SILVER.parent.mkdir(parents=True, exist_ok=True)
    silver.to_parquet(SILVER, index=False)
    print(f"silver: {len(silver):,} baris, {silver['seri_kode'].nunique()} seri ditulis ke {SILVER}")
    print("silver: baris tanpa nilai (tidak masuk Silver):", {k: v for k, v in laporan.items() if v})
    return silver