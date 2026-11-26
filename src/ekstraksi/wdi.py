import json
from pathlib import Path
import pandas as pd
from src.common import manifest

SERI_WDI = ["AG.LND.FRST.ZS", "AG.LND.FRST.K2", "EN.ATM.PM25.MC.M3"]

def _lineage(df: pd.DataFrame, path: Path) -> pd.DataFrame:
    berkas_relatif = str(path.resolve().relative_to(manifest.RAW)).replace("\\", "/")
    
    df["_berkas_raw"] = berkas_relatif
    df["_sha256_raw"] = manifest.sha256_raw(berkas_relatif) 
    return df

def baca_wdi_data(path: Path) -> pd.DataFrame:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
        
    # PERBAIKAN: Ambil data dari elemen ke-1 jika bentuknya List [metadata, data]
    if isinstance(raw, list) and len(raw) > 1:
        rekaman = raw[1]
    else:
        rekaman = raw
        
    df = pd.json_normalize(rekaman)
    
    if "indicator.id" in df.columns:
        df = df[df["indicator.id"].isin(SERI_WDI)].copy()
        
    df["sumber"] = "WDI"
    return _lineage(df, path)

def baca_wdi_metadata(path: Path) -> pd.DataFrame:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
        
    if isinstance(raw, list) and len(raw) > 1:
        rekaman = raw[1]
    else:
        rekaman = raw
        
    df = pd.json_normalize(rekaman)
    
    if "id" in df.columns:
        df = df[df["id"].isin(SERI_WDI)].copy()
        
    df["sumber"] = "WDI"
    return _lineage(df, path)