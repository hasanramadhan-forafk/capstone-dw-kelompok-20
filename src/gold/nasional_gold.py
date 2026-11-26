"""Tahap 6: Penyusunan tabel nasional Gold.

Menggabungkan seri utama dan pembanding ke dalam satu periode (satu baris per seri/rincian).
Sumber data mencakup baris Indonesia dari BPS/instansi, pembanding dari WDI, dan hasil agregat provinsi.
Output disimpan dalam format Parquet di data/gold/nasional.parquet.
"""
import pandas as pd

from src import konfigurasi as K
from src.wilayah import INDONESIA
from src.laporan import ROOT, catat
from src.silver import deret

# Daftar kolom yang wajib ada di output akhir
KOLOM_TARGET = [
    "seri_kode", "rincian", "sumber", "periode", "jenis_periode", 
    "nilai", "satuan", "batas_bawah", "batas_atas", 
    "rujukan_tahun", "asal", "_berkas_raw", "_sha256_raw"
]

def dapatkan_rincian_relevan():
    """Mengumpulkan daftar rincian yang dibutuhkan berdasarkan konfigurasi pasangan."""
    rincian_map = {}
    for pasangan in K.PASANGAN:
        seri_utama = pasangan["utama"].split(",")[0].strip()
        
        # Ambil rincian utama (default 'total' jika tidak ada)
        default_r = pasangan.get("rincian_utama", "total")
        rincian_list = pasangan.get("rincian_utama_jumlah") or [default_r]
        rincian_map.setdefault(seri_utama, set()).update(rincian_list)
        
        # Ambil rincian dari seri pembanding
        for seri_banding, rincian_banding in pasangan["pembanding"]:
            rincian_map.setdefault(seri_banding, set()).add(rincian_banding)
            
    return rincian_map

def hapus_duplikat(df):
    """Memfilter data agar hanya tersisa satu baris unik per sel (seri, rincian, periode)."""
    df_kerja = df.copy()
    
    # Tentukan prioritas berdasarkan peringkat berkas
    df_kerja["_prioritas"] = df_kerja["_berkas_raw"].map(deret.peringkat)
    df_sorted = df_kerja.sort_values(by=["_prioritas", "_berkas_raw"])
    
    # Buang duplikat dan bersihkan kolom bantu
    df_clean = df_sorted.drop_duplicates(subset=["seri_kode", "rincian", "periode"])
    return df_clean.drop(columns=["_prioritas"])

def hitung_agregat_wilayah(data_silver):
    """Menghitung nilai nasional dari penjumlahan provinsi jika diatur dalam GOLD_AGREGAT."""
    hasil_agregat = []
    aturan_agregat = getattr(K, "GOLD_AGREGAT", {})
    
    for seri, aturan in aturan_agregat.items():
        rincian = aturan.get("rincian", "total")
        
        # Filter data tingkat provinsi
        df_prov = data_silver[
            (data_silver["seri_kode"] == seri) & 
            (data_silver["rincian"] == rincian) & 
            (data_silver["wilayah_kode"] != INDONESIA)
        ]
        
        # Jika diwajibkan berasal dari berkas yang sama dengan baris Indonesia
        if aturan.get("berkas_sama"):
            df_ind = data_silver[
                (data_silver["seri_kode"] == seri) & 
                (data_silver["rincian"] == rincian) & 
                (data_silver["wilayah_kode"] == INDONESIA)
            ]
            idx_induk = df_ind.set_index(["periode", "_berkas_raw"]).index
            df_prov = df_prov[df_prov.set_index(["periode", "_berkas_raw"]).index.isin(idx_induk)]
            
        # Pilih satu baris per provinsi per periode
        df_prov = df_prov.copy()
        df_prov["_prioritas"] = df_prov["_berkas_raw"].map(deret.peringkat)
        df_prov = df_prov.sort_values(["_prioritas", "_berkas_raw"]).drop_duplicates(["wilayah_kode", "periode"])
        
        # Agregasi (Sum)
        df_sum = df_prov.groupby("periode", as_index=False).agg(
            nilai=("nilai", "sum"), 
            jenis_periode=("jenis_periode", "first"), 
            sumber=("sumber", "first"),
            satuan=("satuan", "first"), 
            _berkas_raw=("_berkas_raw", lambda x: ";".join(sorted(set(x))))
        )
        
        # Tambahkan penanda bahwa ini hasil agregat
        df_sum = df_sum.assign(
            seri_kode=f"{seri} (agregat provinsi)", 
            rincian=rincian, 
            asal="agregat", 
            _sha256_raw=None,
            batas_bawah=None, 
            batas_atas=None, 
            rujukan_tahun=None
        )
        hasil_agregat.append(df_sum)
        
    return hasil_agregat

def jalankan(data_silver):
    """Fungsi utama untuk membangun dan menyimpan tabel nasional."""
    rincian_map = dapatkan_rincian_relevan()
    
    # 1. Filter baris yang mewakili Indonesia
    df_nas = data_silver[data_silver["wilayah_kode"] == INDONESIA]
    
    # 2. Saring hanya rincian yang diizinkan
    mask_rincian = [
        r in ({"total"} | rincian_map.get(s, set())) 
        for s, r in zip(df_nas["seri_kode"], df_nas["rincian"])
    ]
    df_nas = df_nas[mask_rincian]
    df_nas = hapus_duplikat(df_nas)
    
    # 3. Tentukan status asal data
    tingkat_seri = {k: v["tingkat"] for k, v in K.SERI.items()}
    df_nas["asal"] = df_nas["seri_kode"].apply(
        lambda s: "baris_indonesia" if tingkat_seri.get(s) == "provinsi" else "pembanding"
    )
    
    # 4. Gabungkan dengan hasil agregat
    daftar_agregat = hitung_agregat_wilayah(data_silver)
    df_final = pd.concat([df_nas, *daftar_agregat], ignore_index=True)
    
    # 5. Pastikan struktur kolom lengkap
    for kol in KOLOM_TARGET:
        if kol not in df_final:
            df_final[kol] = None
            
    df_final = df_final[KOLOM_TARGET].sort_values(["seri_kode", "rincian", "periode"]).reset_index(drop=True)
    
    # 6. Konversi tipe data untuk kolom numerik agar seragam
    for kol in ("batas_bawah", "batas_atas", "rujukan_tahun"):
        df_final[kol] = pd.to_numeric(
            df_final[kol].astype(object).where(df_final[kol].notna(), None), 
            errors="coerce"
        ).astype("float64")
        
    # 7. Ekspor ke Parquet
    folder_gold = ROOT / "data" / "gold"
    folder_gold.mkdir(parents=True, exist_ok=True)
    df_final.to_parquet(folder_gold / "nasional.parquet", index=False)
    
    # 8. Catat log
    catat(baris_nasional_gold=len(df_final), seri_nasional_gold=int(df_final["seri_kode"].nunique()))
    
    return df_final