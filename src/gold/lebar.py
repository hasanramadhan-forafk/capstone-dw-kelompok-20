"""Komponen Transformasi dan panel, Sprint 2: panel lebar dari panel panjang Gold.

Aturan:
  - pivot dipakai, bukan pivot_table: bila satu sel punya dua nilai, program berhenti dengan galat
    dan tidak ada nilai yang dirata-rata diam-diam;
  - tiap kolom hanya punya satu satuan baku (diperiksa);
  - komponen indeks lingkungan tetap kolom sendiri-sendiri, tidak dirata-rata;
  - nilai tidak dinormalisasi; panel panjang (dengan nilai_asal) tetap menjadi versi asli;
  - setiap sel lebar sama dengan satu baris panel panjang (kunci: indikator, wilayah_kode, tahun),
    dan lineage ke Silver ada di baris panel panjang itu. Jumlah sel terisi dicocokkan.
"""
import re
from pathlib import Path

import pandas as pd

GOLD = Path(__file__).resolve().parents[2] / "data" / "gold"
PANJANG = GOLD / "panel_provinsi.parquet"
LEBAR = GOLD / "panel_lebar.parquet"
KAMUS = GOLD / "kamus_indikator.parquet"
PERLU = ["wilayah_kode", "nama_wilayah", "tahun", "indikator", "seri_kode", "rincian", "nilai", "satuan_baku"]


def nama_kolom(indikator):
    return re.sub(r"[^0-9a-zA-Z]+", "_", str(indikator)).strip("_")


def bentuk_lebar(panel):
    """Mengembalikan (panel_lebar, kamus_indikator) dari panel panjang."""
    kurang = [k for k in PERLU if k not in panel.columns]
    if kurang:
        raise ValueError(f"kolom panel panjang kurang: {kurang}")

    ganda = panel.groupby("indikator")["satuan_baku"].nunique()
    if (ganda > 1).any():
        raise ValueError(f"indikator dengan lebih dari satu satuan: {sorted(ganda[ganda > 1].index)}")
    nama = panel.groupby("wilayah_kode")["nama_wilayah"].nunique()
    if (nama > 1).any():
        raise ValueError(f"wilayah_kode dengan lebih dari satu nama: {sorted(nama[nama > 1].index)}")

    kolom = {i: nama_kolom(i) for i in panel["indikator"].unique()}
    if len(set(kolom.values())) != len(kolom):
        raise ValueError("dua indikator menghasilkan nama kolom yang sama")

    lebar = panel.pivot(index=["wilayah_kode", "tahun"], columns="indikator", values="nilai")
    lebar = lebar.rename(columns=kolom).reset_index()
    lebar.columns.name = None
    nama_wil = panel.drop_duplicates("wilayah_kode").set_index("wilayah_kode")["nama_wilayah"]
    lebar.insert(1, "nama_wilayah", lebar["wilayah_kode"].map(nama_wil))

    terisi_lebar = int(lebar[list(kolom.values())].notna().sum().sum())
    terisi_panjang = int(panel["nilai"].notna().sum())
    if terisi_lebar != terisi_panjang:
        raise ValueError(f"sel terisi tidak cocok: lebar {terisi_lebar}, panjang {terisi_panjang}")

    kamus = (panel[["indikator", "seri_kode", "rincian", "satuan_baku"]].drop_duplicates()
             .assign(kolom=lambda d: d["indikator"].map(kolom))
             .sort_values("indikator").reset_index(drop=True))[["kolom", "indikator", "seri_kode", "rincian", "satuan_baku"]]
    return lebar.sort_values(["wilayah_kode", "tahun"]).reset_index(drop=True), kamus


def jalankan(panel=None):
    if panel is None or isinstance(panel, (str, Path)):
        panel = pd.read_parquet(panel or PANJANG)
    lebar, kamus = bentuk_lebar(panel)
    GOLD.mkdir(parents=True, exist_ok=True)
    lebar.to_parquet(LEBAR, index=False)
    kamus.to_parquet(KAMUS, index=False)
    print(f"gold lebar: {len(lebar):,} baris provinsi x tahun, {len(kamus)} indikator, "
          f"{panel['seri_kode'].nunique()} seri; kamus ditulis ke {KAMUS.name}")
    return {"panel_lebar": lebar, "kamus_indikator": kamus}