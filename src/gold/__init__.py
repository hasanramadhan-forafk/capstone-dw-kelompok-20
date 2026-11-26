"""Tahap 4–6 — Reshape, integrasi, dan penyimpanan ke Gold (pertemuan VII, IX, XI, XII).

Sprint 1: tabel nasional dan daftar pasangan rekonsiliasi.
Sprint 2: aturan pemilihan satu nilai per sel (src/gold/pilih.py) -> panel provinsi dan tabel nasional.
"""
from src.gold import panel, nasional, nasional_gold, rekonsiliasi, muat_sql

from src.gold import lebar, muat_sql, nasional, pilih 


def jalankan(silver=None):
    """Terima Silver, tulis tabel Gold, kembalikan {nama_tabel: DataFrame}."""
    hasil = nasional.jalankan(silver)
    hasil["baris_sql"] = muat_sql.jalankan(silver)
    g = pilih.jalankan(silver if silver is not None else pilih.SILVER)
    lebar.jalankan(g["panel"])                               
    hasil["gold_panel"], hasil["gold_nasional"], hasil["gold_ringkasan"] = g["panel"], g["nasional"], g["ringkasan"]
    return hasil
