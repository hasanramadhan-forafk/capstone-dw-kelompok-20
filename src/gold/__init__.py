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