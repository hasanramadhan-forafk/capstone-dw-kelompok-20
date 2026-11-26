"""Orkestrator Validasi: aturan Silver (Sprint 1) + aturan Gold dan rekonsiliasi (Sprint 2).

Dijalankan dari ``python pipeline.py`` sebagai ``validasi.jalankan(silver, gold)``.
Aturan keras yang gagal menghentikan pipeline setelah laporan ditulis.
"""
from pathlib import Path

import pandas as pd

from src.validasi import aturan, gold as aturan_gold, khusus
from src.laporan import simpan_angka

ROOT = Path(__file__).resolve().parents[2]


def _muat_gold(gold):
    if isinstance(gold, dict) and gold.get("panel") is not None:
        return gold
    g = {}
    for nama, berkas in [("panel", "panel_provinsi.parquet"), ("nasional", "nasional.parquet"),
                         ("rekonsiliasi", "rekonsiliasi.parquet")]:
        jalur = ROOT / "data" / "gold" / berkas
        g[nama] = pd.read_parquet(jalur) if jalur.exists() else pd.DataFrame()
    return g


def jalankan(silver: pd.DataFrame, gold=None) -> pd.DataFrame:
    if not isinstance(silver, pd.DataFrame):
        silver = pd.read_parquet(ROOT / "data" / "silver" / "silver.parquet")
    gold = _muat_gold(gold)

    hasil = []

    # ---------------------------------------------------------------- Silver
    def catat_silver(nama, jenis, lolos, keterangan=""):
        hasil.append({"tahap": "Silver", "aturan": nama, "jenis": jenis,
                      "keterangan": keterangan, "hasil": "LOLOS" if lolos else "GAGAL"})

    catat_silver("keunikan_kunci_primer", "keras (umum)", aturan.cek_keunikan_kunci(silver),
                 "sumber + seri + wilayah + periode + rincian + berkas tidak kembar")
    catat_silver("rentang_satuan_sah", "keras (umum)", aturan.cek_rentang_satuan(silver),
                 "persen 0-100; luas dan indeks tidak negatif")
    catat_silver("satu_satuan_per_seri", "keras (umum)", aturan.cek_satuan_seragam(silver),
                 "satu seri hanya punya satu satuan")
    catat_silver("wilayah_kode_sah", "keras (umum)", aturan.cek_wilayah_sah(silver),
                 "kode wilayah dari 38 provinsi 2025 + 9999")
    catat_silver("kolom_wajib_lengkap", "keras (umum)", aturan.cek_tidak_ada_null(silver),
                 "kolom kunci, nilai, dan satuan tidak kosong")

    gagal = khusus.luas_tidak_negatif(silver)
    catat_silver("luas_tidak_negatif", "keras (kasus)", gagal.empty,
                 f"{len(gagal)} baris melanggar" if not gagal.empty else "tidak ada luas negatif")

    gagal = khusus.komponen_iklh_sah(silver)
    catat_silver("komponen_iklh_sah", "keras (kasus)", gagal.empty,
                 f"{len(gagal)} baris melanggar" if not gagal.empty else "komponen IKLH sah")

    gagal = khusus.konsistensi_lahan_kritis(silver)
    catat_silver("konsistensi_lahan_kritis", "keras (kasus)", gagal.empty,
                 f"{len(gagal)} baris melanggar" if not gagal.empty else "kritis + sangat_kritis = total")

    anomali = khusus.deteksi_kolom_2020_tergeser(silver)
    hasil.append({"tahap": "Silver", "aturan": "deteksi_anomali_2020", "jenis": "peringatan (kasus)",
                  "keterangan": "kolom 2020 tertukar antarprovinsi (sudah dikoreksi di Silver)",
                  "hasil": f"PERINGATAN ({len(anomali)} baris)" if not anomali.empty else "LOLOS"})

    # ---------------------------------------------------------------- Gold
    for nama, keterangan, keras, fungsi in aturan_gold.ATURAN:
        buruk = fungsi(silver, gold)
        hasil.append({
            "tahap": "Gold", "aturan": nama,
            "jenis": "keras (gold)" if keras else "peringatan (gold)",
            "keterangan": keterangan,
            "hasil": ("LOLOS" if buruk.empty
                      else (f"GAGAL ({len(buruk)} baris)" if keras else f"PERINGATAN ({len(buruk)} baris)")),
        })

    df = pd.DataFrame(hasil)

    # ---------------------------------------------------------------- layar
    print("\n" + "=" * 72)
    print("               HASIL VALIDASI DATA (SILVER & GOLD)")
    print("=" * 72)
    for r in df.itertuples(index=False):
        simbol = "OK " if r.hasil == "LOLOS" else ("!  " if "PERINGATAN" in r.hasil else "X  ")
        print(f" [{simbol}] [{r.tahap:<6}] {r.aturan:<38} [{r.jenis}]: {r.hasil}")
    total = len(df)
    lolos = int((df["hasil"] == "LOLOS").sum())
    gagal = int((df["hasil"] == "GAGAL").sum())
    peringatan = int(df["hasil"].str.startswith("PERINGATAN").sum())
    print("-" * 72)
    print(f" Total aturan: {total} | LOLOS: {lolos} | GAGAL: {gagal} | PERINGATAN: {peringatan}")
    print("=" * 72)

    # ---------------------------------------------------------------- laporan
    laporan = ROOT / "reports" / "validasi.md"
    laporan.parent.mkdir(parents=True, exist_ok=True)
    try:
        tabel = df.to_markdown(index=False)
    except Exception:
        tabel = df.to_string(index=False)
    laporan.write_text(
        "# Hasil Validasi Silver dan Gold\n\n"
        "Dihasilkan `python pipeline.py` (`src/validasi/`). Aturan Silver melanjutkan aturan Sprint 1; "
        "aturan Gold memeriksa kunci panel, satuan per indikator, ketertelusuran setiap sel ke Silver, "
        "serta kategori setiap baris rekonsiliasi berpasangan.\n\n"
        f"**Ringkasan:** {total} aturan, {lolos} LOLOS, {gagal} GAGAL, {peringatan} PERINGATAN.\n\n" + tabel + "\n",
        encoding="utf-8",
    )
    simpan_angka()

    if gagal:
        nama = ", ".join(df.loc[df["hasil"] == "GAGAL", "aturan"])
        raise SystemExit(f"Validasi gagal: {nama}. Lihat reports/validasi.md")
    return df
