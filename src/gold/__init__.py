"""Tahap 4–6 — Reshape, integrasi, dan penyimpanan ke Gold (pertemuan VII, IX, XI, XII).

Sprint 1: tabel nasional dan daftar pasangan rekonsiliasi.
"""
from src.gold import nasional


def jalankan(silver=None):
    """Terima Silver, tulis tabel Gold, kembalikan {nama_tabel: DataFrame}."""
    return nasional.jalankan(silver)
