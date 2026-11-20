<<<<<<< HEAD
"""Tahap 4-6: Pembentukan data Gold (Panel, Nasional, Rekonsiliasi, dan SQL).

Alur eksekusi dimulai dari hasil Silver, lalu dilanjutkan secara berurutan hingga siap dimuat ke DuckDB.
"""
from src.gold import panel, nasional, nasional_gold, rekonsiliasi, muat_sql

def jalankan(data_silver):
    output_gold = nasional.jalankan(data_silver)
    
    # Melengkapi komponen hasil Gold
    output_gold["panel_provinsi"] = panel.jalankan(data_silver)
    output_gold["tabel_nasional"] = nasional_gold.jalankan(data_silver)
    output_gold["hasil_rekonsiliasi"] = rekonsiliasi.jalankan(output_gold["tabel_nasional"])
    output_gold["data_sql"] = muat_sql.jalankan(data_silver, output_gold)
    
    return output_gold
=======
"""Tahap 4–6 — Reshape, integrasi, dan penyimpanan ke Gold (pertemuan VII, IX, XI, XII).

Panel provinsi x periode x indikator dan tabel rekonsiliasi dengan selisih dikerjakan di Sprint 2.
"""
from src.gold import muat_sql, nasional


def jalankan(silver=None):
    """Terima Silver, tulis tabel Gold, kembalikan {nama_tabel: DataFrame}."""
    hasil = nasional.jalankan(silver)
    hasil["baris_sql"] = muat_sql.jalankan(silver)
    return hasil
