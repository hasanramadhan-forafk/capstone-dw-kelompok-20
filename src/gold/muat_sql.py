"""Tahap 5 - memuat Silver dan Gold ke DuckDB dengan kunci primer dan batasan.

Basis data dibuat ulang setiap kali (berkas lama dihapus), jadi hasilnya selalu sama dengan
data/silver/silver.parquet dan tabel Gold yang baru ditulis. Berkas .duckdb tidak di-commit;
jalankan pipeline untuk membuatnya.
"""
from pathlib import Path

import duckdb
import pandas as pd

from src.laporan import ROOT, catat

DB = ROOT / "data" / "gold" / "gudang.duckdb"
DDL_SILVER = Path(__file__).with_name("silver.sql")
DDL_GOLD = Path(__file__).with_name("gold.sql")

KOLOM_PANEL = ["indikator", "seri_kode", "rincian", "wilayah_kode", "nama_wilayah", "periode",
               "jenis_periode", "nilai", "satuan", "status_sel", "_berkas_raw", "_sha256_raw"]
KOLOM_NASIONAL = ["seri_kode", "rincian", "sumber", "periode", "jenis_periode", "nilai", "satuan",
                  "asal", "_berkas_raw", "_sha256_raw"]
KOLOM_REKONSILIASI = ["pasangan_id", "jenis", "seri_utama", "rincian_utama", "seri_pembanding",
                      "rincian_pembanding", "periode", "nilai_utama", "nilai_pembanding", "satuan",
                      "selisih", "selisih_relatif", "asal", "kategori", "penjelasan", "catatan"]


def _muat_tabel(con, nama, df, kolom):
    """Muat DataFrame ke tabel yang sudah dibuat, hanya kolom yang dikenal DDL."""
    if df is None or len(df) == 0:
        return 0
    d = df.copy()
    if "asal" in kolom and "asal" not in d.columns:
        d["asal"] = d["sumber"].map({"bps": "baris_indonesia", "wdi": "pembanding"}).fillna("pembanding")
    pakai = [k for k in kolom if k in d.columns]
    d = d[pakai]
    con.register(f"{nama}_df", d)
    con.execute(f"INSERT INTO {nama} ({', '.join(pakai)}) SELECT {', '.join(pakai)} FROM {nama}_df")
    return len(d)


def jalankan(silver=None, gold=None):
    if silver is None:
        silver = pd.read_parquet(ROOT / "data" / "silver" / "silver.parquet")
    DB.parent.mkdir(parents=True, exist_ok=True)
    DB.unlink(missing_ok=True)
    seri = pd.read_csv(ROOT / "docs" / "seri.csv")[["seri_kode", "sumber", "tingkat", "nama_baku", "satuan", "sdg_kode"]]
    seri["sdg_kode"] = seri["sdg_kode"].astype(str)
    s = silver.copy()
    if "rujukan_tahun" in s.columns:
        s["rujukan_tahun"] = s["rujukan_tahun"].astype("float64")
    with duckdb.connect(str(DB)) as con:
        con.execute(DDL_SILVER.read_text(encoding="utf-8"))
        con.register("seri_df", seri)
        con.execute("INSERT INTO seri SELECT * FROM seri_df")
        con.register("silver_df", s)
        kolom = ", ".join(s.columns)
        con.execute(f"INSERT INTO silver ({kolom}) SELECT {kolom} FROM silver_df")
        n = con.execute("SELECT count(*) FROM silver").fetchone()[0]

        n_gold = {}
        if isinstance(gold, dict) and gold.get("panel") is not None:
            con.execute(DDL_GOLD.read_text(encoding="utf-8"))
            n_gold["panel"] = _muat_tabel(con, "gold_panel", gold.get("panel"), KOLOM_PANEL)
            n_gold["nasional"] = _muat_tabel(con, "gold_nasional", gold.get("nasional"), KOLOM_NASIONAL)
            n_gold["rekonsiliasi"] = _muat_tabel(con, "rekonsiliasi", gold.get("rekonsiliasi"),
                                                  KOLOM_REKONSILIASI)

    if n != len(silver):
        raise AssertionError(f"DuckDB memuat {n} baris, Silver {len(silver)} baris")
    catat(baris_sql=n, **{f"baris_sql_{k}": v for k, v in n_gold.items()})
    return n
