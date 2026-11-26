import os
import pandas as pd
import warnings
import json
import html
import contextlib
import io
from pathlib import Path
from src.common.manifest import sha256_raw, RAW

warnings.filterwarnings('ignore') # Menyembunyikan peringatan pandas

# Path dasar folder BPS
BPS_DIR = RAW / "bps" / "2026-10-17"

def baca_csv_bps(nama_file):
    filepath = BPS_DIR / nama_file
    berkas_relatif = str(filepath.relative_to(RAW)).replace("\\", "/")
    
    try:
        df = pd.read_csv(filepath, sep=';', decimal=',', encoding='utf-8')
        if len(df.columns) < 2: 
            raise ValueError("Bukan titik koma")
    except:
        df = pd.read_csv(filepath, sep=',', decimal='.', encoding='utf-8')
    
    df['_berkas_raw'] = berkas_relatif
    df['_sha256_raw'] = sha256_raw(berkas_relatif)
    return df

def baca_json_bps(nama_file):
    filepath = BPS_DIR / "json" / nama_file
    berkas_relatif = str(filepath.relative_to(RAW)).replace("\\", "/")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data_json = json.load(f)
        
    if isinstance(data_json, list):
        data_json = data_json[0]
        
    # Tipe 1: JSON berisi HTML
    if 'data' in data_json and isinstance(data_json['data'], dict) and 'table' in data_json['data']:
        html_unescaped = html.unescape(data_json['data']['table'])
        with contextlib.redirect_stdout(io.StringIO()):
            df = pd.read_html(html_unescaped)[0]
            
        df.columns = df.iloc[0]
        df = df[1:].reset_index(drop=True)
        df['_berkas_raw'] = berkas_relatif
        df['_sha256_raw'] = sha256_raw(berkas_relatif)
        return df
        
    # Tipe 2: JSON bersarang (IKLH, dll)
    vervar_list = data_json.get('vervar', [])
    turvar_list = data_json.get('turvar', [])
    tahun_list = data_json.get('tahun', [])
    datacontent = data_json.get('datacontent', {})
    
    rows = []
    for v in vervar_list:
        kode_vervar = str(v.get('val', ''))
        label_vervar = str(v.get('label', ''))
        
        for t in turvar_list:
            kode_turvar = str(t.get('val', ''))
            label_turvar = str(t.get('label', ''))
            
            for th in tahun_list:
                kode_tahun = str(th.get('val', ''))
                label_tahun = str(th.get('label', ''))
                
                nilai = None
                for key, val in datacontent.items():
                    key_str = str(key)
                    if kode_vervar in key_str and kode_turvar in key_str and kode_tahun in key_str:
                        nilai = val
                        break 
                
                if nilai is not None:
                    rows.append({
                        'wilayah': label_vervar,
                        'komponen': label_turvar,
                        'tahun': label_tahun,
                        'nilai': nilai
                    })
                    
    df = pd.DataFrame(rows)
    df['_berkas_raw'] = berkas_relatif
    df['_sha256_raw'] = sha256_raw(berkas_relatif)
    return df

# ==========================================
# BLOK UJI COBA FINAL
# ==========================================
if __name__ == "__main__":
    file_csv_list = [
        "sdg15_tutupan_hutan.csv",
        "sdg15_lahan_kritis.csv",
        "sdg15_tutupan_kawasan.csv",
        "sdg15_iklh.csv"
    ]
    
    file_json_list = [
        "sdg15_tutupan_hutan.json",
        "sdg15_lahan_kritis.json",
        "sdg15_tutupan_kawasan.json",
        "sdg15_iklh.json"
    ]
    
    # Bersihkan layar sebelum mulai
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=== MENGUJI SEMUA FILE CSV ===")
    for file in file_csv_list:
        try:
            df = baca_csv_bps(file)
            print(f" {file} | Baris: {len(df)}")
        except Exception as e:
            print(f" Gagal baca {file}: {e}")
            
    # Bersihkan layar lagi sebelum JSON (untuk membuang teks HTML dari lxml)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=== MENGUJI SEMUA FILE JSON ===")
    for file in file_json_list:
        try:
            df = baca_json_bps(file)
            print(f" Berhasil baca {file} | Baris: {len(df)}")
        except Exception as e:
            print(f" Gagal baca {file}: {e}")
            
    print("\n=== SELESAI ===")