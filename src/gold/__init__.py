"""Tahap 4-6 - Reshape, integrasi, dan penyimpanan ke Gold (pertemuan VII, IX, XI, XII).

Sprint 2: panel provinsi x periode x indikator (satu nilai per sel), tabel nasional, tabel
rekonsiliasi seri utama vs pembanding nasional, panel lebar, dan Silver + Gold di DuckDB.
"""
import pandas as pd

from src.gold import lebar, muat_sql, pilih, rekonsiliasi


def jalankan(silver=None):
    """Terima Silver, tulis tabel Gold, kembalikan {nama_tabel: DataFrame}.

    Kunci ``panel``, ``nasional``, dan ``rekonsiliasi`` dipakai langsung oleh
    ``src.validasi.jalankan(silver, gold)``.
    """
    silver = silver if silver is not None else pilih.SILVER
    if not isinstance(silver, pd.DataFrame):
        silver = pd.read_parquet(silver)
    g = pilih.jalankan(silver)
    panel, nasional = g["panel"], g["nasional"]
    rek = rekonsiliasi.jalankan(nasional)
    lebar_hasil = lebar.jalankan(panel)
    baris_sql = muat_sql.jalankan(silver, {"panel": panel, "nasional": nasional, "rekonsiliasi": rek})
    return {
        "panel": panel,
        "nasional": nasional,
        "rekonsiliasi": rek,
        "panel_lebar": lebar_hasil["panel_lebar"],
        "kamus_indikator": lebar_hasil["kamus_indikator"],
        "ringkasan": g["ringkasan"],
        "baris_sql": baris_sql,
    }
