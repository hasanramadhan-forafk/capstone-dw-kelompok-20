"""Tahap 4–6 — Reshape, integrasi, dan penyimpanan ke Gold (pertemuan VII, IX, XI, XII).

Sprint 1: tabel nasional dan daftar pasangan rekonsiliasi (`nasional.py`).
Sprint 2: pemilihan satu nilai per sel (`pilih.py`) -> panel provinsi & nasional (`lebar.py`),
          tabel rekonsiliasi berkategori (`rekonsiliasi.py`), dan pemuatan Silver + Gold ke DuckDB (`muat_sql.py`).
"""
from src.gold import lebar, muat_sql, nasional, pilih, rekonsiliasi


def jalankan(silver=None):
    """Terima Silver, tulis tabel Gold, kembalikan {nama_tabel: DataFrame}."""
    hasil = nasional.jalankan(silver)
    g = pilih.jalankan(silver if silver is not None else pilih.SILVER)
    lebar.jalankan(g["panel"])
    hasil["gold_panel"], hasil["gold_nasional"], hasil["gold_ringkasan"] = g["panel"], g["nasional"], g["ringkasan"]
    hasil["rekonsiliasi"] = rekonsiliasi.jalankan(g["nasional"], silver)
    hasil["baris_sql"] = muat_sql.jalankan(
        silver,
        {"panel": g["panel"], "nasional": g["nasional"], "rekonsiliasi": hasil["rekonsiliasi"]},
    )
    return hasil
