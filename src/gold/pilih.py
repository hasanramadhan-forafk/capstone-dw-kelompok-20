"""Tahap 4 (persiapan Gold): aturan yang memilih TEPAT SATU nilai per wilayah x tahun x indikator.

Silver boleh punya beberapa baris untuk sel yang sama (snapshot berbeda, format berbeda, rincian,
periode non-tahunan). Gold tidak. Semua aturan ada di sini sebagai kode, bukan saringan tangan:

  1. Perbaikan galat input Sprint 1 diterapkan bila Silver masih memuat nilai asal (nilai_asal disimpan).
  2. Periode semester/triwulan/bulan diagregasi ke tahun (mean; min. separuh periode terisi).
  3. Hanya rincian yang terdaftar di PANEL_RINCIAN yang masuk Gold; sisanya tetap di Silver.
  4. Satuan dibakukan (luas -> ribu_hektar).
  5. Satu nilai per sel: snapshot terbaru; bila angka berbeda antar snapshot = revisi (nilai lama dicatat);
     bila snapshot sama, CSV didahulukan atas JSON.
  6. Baris Indonesia (9999) dipisahkan dari panel provinsi ke tabel nasional.
  7. Penanda anomali Sprint 1 (galat_input / patahan / outlier_asli) ikut terbawa; tidak ada yang dihapus.
  8. Komponen var2532 disimpan terpisah; TIDAK dirata-rata menjadi indeks baru.

    python -m src.gold.pilih                # baca data/silver/silver.parquet, tulis data/gold/
    python -m src.gold.pilih --catat-log    # sekali saja: tulis entri tahap gold ke log-keputusan.csv
"""
import csv
import re
import sys
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

from src.laporan import catat, tabel_md, tulis

ROOT = Path(__file__).resolve().parents[2]
SILVER = ROOT / "data" / "silver" / "silver.parquet"
GOLD = ROOT / "data" / "gold"
OUT_TABEL = ROOT / "reports" / "tabel"
ANOMALI = OUT_TABEL / "anomali_berkategori.csv"
PERBAIKAN = OUT_TABEL / "perbaikan_galat.csv"
LOG = ROOT / "log-keputusan.csv"
NIM = "124450122"
NASIONAL = 9999

PROV38 = {1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2100, 3100, 3200, 3300, 3400, 3500, 3600,
          5100, 5200, 5300, 6100, 6200, 6300, 6400, 6500, 7100, 7200, 7300, 7400, 7500, 7600, 8100, 8200,
          9100, 9200, 9400, 9500, 9600, 9700}

# Rincian yang masuk Gold. "*" = semua rincian. Seri yang tidak terdaftar: semua rincian (dengan peringatan).
# Prinsip: komponen yang membawa informasi sendiri masuk; total dan pelengkap yang hanya turunan aritmetika
# tetap di Silver. `total` luas dipertahankan SEKALI (tabel hutan) sebagai penyebut/luas wilayah.
PANEL_RINCIAN = {
    "tabel:sdg15_tutupan_hutan:luas_ribu_ha": {"hutan", "total"},
    "tabel:sdg15_tutupan_hutan:persen": {"hutan"},
    "var1304": {"kawasan_hutan"},
    "var588": {"kritis", "sangat_kritis"},
    "var2532": "*",          # komponen terpisah, tanpa indeks gabungan
    "AG.LND.FRST.ZS": "*", "AG.LND.FRST.K2": "*", "EN.ATM.PM25.MC.M3": "*",
}
# Konversi ke satuan baku: satuan -> (satuan baku, faktor)
SATUAN_BAKU = {"hektar": ("ribu_hektar", 0.001), "km2": ("ribu_hektar", 0.1), "km_persegi": ("ribu_hektar", 0.1),
               "sq._km": ("ribu_hektar", 0.1)}
# Agregasi periode non-tahunan: seri -> mean | sum | last (bawaan mean, untuk indeks/rasio/tingkat)
AGREGASI = {}
PERIODE_PER_TAHUN = {"semester": 2, "triwulan": 4, "bulan": 12}
MIN_ISI = 0.5
PRIORITAS = {"galat_input": 3, "patahan": 2, "outlier_asli": 1}


def _snapshot(b: str) -> str:
    m = re.search(r"(\d{4}-\d{2}-\d{2})", str(b))
    return m.group(1) if m else "0000-00-00"


def _fmt_rank(b: str) -> int:
    e = str(b).rsplit(".", 1)[-1].lower()
    return {"csv": 0, "json": 1}.get(e, 2)


def muat_silver(silver) -> pd.DataFrame:
    if isinstance(silver, (str, Path)):
        silver = pd.read_parquet(silver)
    if not isinstance(silver, pd.DataFrame):
        raise TypeError(f"gold.jalankan menerima DataFrame Silver atau jalur parquet, bukan {type(silver).__name__}")
    s = silver.copy().reset_index(drop=True)
    s["_id"] = np.arange(len(s))
    s["_asal"] = 1
    return s

WDI_SATUAN = {"AG.LND.FRST.ZS": "persen", "AG.LND.FRST.K2": "km2", "EN.ATM.PM25.MC.M3": "ug_per_m3"}


def _baca_wdi() -> pd.DataFrame:
    """Baca berkas WDI di data/raw lewat pembaca tim (src.ekstraksi.wdi). Kosong bila tidak ada."""
    from src.common.manifest import RAW
    from src.ekstraksi.wdi import baca_wdi_data
    out = [baca_wdi_data(f) for f in sorted((RAW / "wdi").glob("*/data/*.json"))]
    return pd.concat(out, ignore_index=True) if out else pd.DataFrame()


def baris_wdi(s: pd.DataFrame) -> tuple:
    """Silver tim hanya memuat BPS (K-010). Baris WDI Indonesia dibentuk di sini dengan skema Silver.
    Nilai kosong WDI dilewati (dihitung). Mengembalikan (baris, jumlah nilai kosong)."""
    ada = set(s["seri_kode"].unique())
    try:
        w = _baca_wdi()
    except Exception as e:
        print(f"gold: WDI tidak terbaca ({e})")
        return pd.DataFrame(), 0
    if w.empty:
        return pd.DataFrame(), 0
    w = w[w["indicator.id"].isin(WDI_SATUAN) & ~w["indicator.id"].isin(ada) & (w["countryiso3code"] == "IDN")]
    kosong = int(w["value"].isna().sum())
    w = w.dropna(subset=["value"])
    d = pd.DataFrame({"sumber": "wdi", "seri_kode": w["indicator.id"], "wilayah_kode": NASIONAL,
                      "nama_wilayah": "Indonesia", "periode": w["date"].astype(str), "jenis_periode": "tahun",
                      "rincian": "total", "nilai": w["value"].astype(float),
                      "satuan": w["indicator.id"].map(WDI_SATUAN),
                      "_berkas_raw": w["_berkas_raw"], "_sha256_raw": w["_sha256_raw"]})
    d["_asal"], d["_id"] = 0, -1
    return d.reset_index(drop=True), kosong


# ---------------------------------------------------------------- aturan
def terapkan_perbaikan(s: pd.DataFrame) -> tuple:
    s["nilai_asal"] = s.get("nilai_asal", np.nan)
    s["perbaikan"] = s.get("perbaikan", "")
    n = 0
    if not PERBAIKAN.exists():
        return s, n
    u = pd.read_csv(PERBAIKAN)
    s["_tahun"] = pd.to_numeric(s["periode"].astype(str).str[:4], errors="coerce")
    for r in u.itertuples(index=False):
        m = ((s["seri_kode"] == r.seri_kode) & (s["rincian"] == r.rincian) & (s["wilayah_kode"] == r.wilayah_kode)
             & (s["_tahun"] == r.tahun) & (s["jenis_periode"] == "tahun") & ((s["nilai"] - r.nilai_asal).abs() < 1e-6))
        if m.any():                      # semua salinan (snapshot/format) yang masih memuat nilai salah
            s.loc[m, "nilai_asal"], s.loc[m, "nilai"], s.loc[m, "perbaikan"] = r.nilai_asal, r.nilai_baru, r.aturan
            n += int(m.sum())
    return s.drop(columns="_tahun"), n


def ke_tahunan(s: pd.DataFrame) -> tuple:
    """Periode non-tahunan -> tahun. Mengembalikan (tabel, jumlah baris Silver yang diagregasi, yang gugur)."""
    s["tahun"] = pd.to_numeric(s["periode"].astype(str).str[:4], errors="coerce").astype("Int64")
    s["n_periode_sumber"] = 1
    lain = s[s["jenis_periode"] != "tahun"]
    if lain.empty:
        return s, 0, 0
    k = ["sumber", "seri_kode", "wilayah_kode", "nama_wilayah", "rincian", "satuan", "tahun", "_berkas_raw", "_sha256_raw"]
    baris, gugur = [], 0
    for key, g in lain.groupby(k, dropna=False):
        harap = PERIODE_PER_TAHUN.get(g["jenis_periode"].iloc[0], 1)
        if len(g) < np.ceil(MIN_ISI * harap):
            gugur += len(g)
            continue
        how = AGREGASI.get(key[1], "mean")
        v = {"mean": g["nilai"].mean(), "sum": g["nilai"].sum(),
             "last": g.sort_values("periode")["nilai"].iloc[-1]}[how]
        d = dict(zip(k, key))
        d.update(nilai=v, periode=str(int(key[6])), jenis_periode="tahun", n_periode_sumber=len(g),
                 nilai_asal=np.nan, perbaikan="", _id=-1, _asal=0)
        baris.append(d)
    tahunan = s[s["jenis_periode"] == "tahun"]
    return pd.concat([tahunan, pd.DataFrame(baris)], ignore_index=True), len(lain) - gugur, gugur


def bakukan_satuan(s: pd.DataFrame) -> tuple:
    s["satuan_baku"] = s["satuan"]
    n = 0
    for sat, (baru, f) in SATUAN_BAKU.items():
        m = s["satuan"].astype(str).str.lower().str.replace("\u00b2", "2").str.replace(" ", "_") == sat
        n += int(m.sum())
        s.loc[m, "nilai"] = s.loc[m, "nilai"] * f
        s.loc[m, "nilai_asal"] = s.loc[m, "nilai_asal"].fillna(np.nan)
        s.loc[m, "satuan_baku"] = baru
    return s, n


def saring_rincian(s: pd.DataFrame) -> tuple:
    def boleh(r):
        a = PANEL_RINCIAN.get(r.seri_kode, "*")
        return a == "*" or r.rincian in a
    m = np.fromiter((boleh(r) for r in s[["seri_kode", "rincian"]].itertuples(index=False)), bool, len(s))
    return s[m].copy(), s[~m].copy()


def pilih_satu(s: pd.DataFrame) -> tuple:
    """Satu baris per sumber x seri x wilayah x tahun x rincian. Mengembalikan (terpilih, tak_terpilih+alasan)."""
    k = ["sumber", "seri_kode", "wilayah_kode", "tahun", "rincian"]
    s = s.copy()
    s["_snap"] = s["_berkas_raw"].map(_snapshot)
    s["_fmt"] = s["_berkas_raw"].map(_fmt_rank)
    s = s.sort_values(k + ["_snap", "_fmt", "_berkas_raw"], ascending=[True] * len(k) + [False, True, True])
    s["_rank"] = s.groupby(k).cumcount()
    pilih = s[s["_rank"] == 0].copy()
    sisa = s[s["_rank"] > 0].copy()
    ref = pilih.set_index(k)[["nilai", "_snap", "nilai_asal"]]
    sisa = sisa.join(ref, on=k, rsuffix="_pilih")
    sama = (sisa["nilai"] - sisa["nilai_pilih"]).abs() < 1e-9
    lama = sisa["_snap"] < sisa["_snap_pilih"]
    sisa["alasan"] = np.select(
        [lama & sama, lama & ~sama, ~lama & sama, ~lama & ~sama],
        ["snapshot_lebih_lama_angka_sama", "snapshot_lebih_lama_revisi", "berkas_lain_snapshot_sama_angka_sama",
         "berkas_lain_snapshot_sama_ANGKA_BEDA"], default="")
    rev = sisa[sisa["alasan"] == "snapshot_lebih_lama_revisi"].groupby(k)["nilai"].first().rename("nilai_snapshot_terdahulu")
    pilih = pilih.join(rev, on=k)
    pilih["revisi"] = pilih["nilai_snapshot_terdahulu"].notna()
    return pilih.drop(columns=["_snap", "_fmt", "_rank"]), sisa


def bawa_penanda(g: pd.DataFrame) -> tuple:
    g = g.copy()
    for c, v in [("penanda", ""), ("subkategori", ""), ("status_galat", ""), ("n_penanda", 0)]:
        g[c] = v
    if not ANOMALI.exists():
        return g, 0, 0
    a = pd.read_csv(ANOMALI).dropna(subset=["wilayah_kode"])
    a["wilayah_kode"], a["periode"] = a["wilayah_kode"].astype(int), a["periode"].astype(int)
    a["_p"] = a["kategori"].map(PRIORITAS)
    a = a.sort_values("_p", ascending=False)
    ring = a.groupby(["seri", "rincian_silver", "wilayah_kode", "periode"]).agg(
        penanda=("kategori", "first"), subkategori=("subkategori", "first"),
        status_galat=("status_galat", lambda x: x.dropna().iloc[0] if x.notna().any() else ""),
        n_penanda=("kategori", "size")).reset_index()
    ring = ring.rename(columns={"seri": "seri_kode", "rincian_silver": "rincian", "periode": "tahun"})
    ring["tahun"] = ring["tahun"].astype("Int64")
    g = g.drop(columns=["penanda", "subkategori", "status_galat", "n_penanda"]).merge(
        ring, on=["seri_kode", "rincian", "wilayah_kode", "tahun"], how="left")
    for c in ["penanda", "subkategori", "status_galat"]:
        g[c] = g[c].fillna("")
    g["n_penanda"] = g["n_penanda"].fillna(0).astype(int)
    terbawa = int(g["n_penanda"].sum())
    hilang = len(a) - terbawa     # penanda pada rincian yang hanya di Silver (bukan hilang dari Silver)
    return g, terbawa, hilang


KOLOM_GOLD = ["sumber", "indikator", "seri_kode", "rincian", "wilayah_kode", "nama_wilayah", "tahun", "nilai",
              "satuan_baku", "penanda", "subkategori", "status_galat", "n_penanda", "nilai_asal", "perbaikan",
              "revisi", "nilai_snapshot_terdahulu", "n_periode_sumber", "_berkas_raw", "_sha256_raw"]


def bangun(silver) -> dict:
    s = muat_silver(silver)
    n_silver = len(s)
    wdi, n_wdi_kosong = baris_wdi(s)
    if len(wdi):
        s = pd.concat([s, wdi], ignore_index=True)
    alasan = {}                                           # alasan -> jumlah baris Silver tidak terpilih
    s, n_perbaikan = terapkan_perbaikan(s)
    s, n_agregat, n_gugur = ke_tahunan(s)
    alasan["diagregasi_ke_tahun_non_tahunan"] = n_agregat + n_gugur
    s, n_konversi = bakukan_satuan(s)
    s, tak = saring_rincian(s)
    alasan["rincian_hanya_di_silver"] = int(tak["_asal"].sum())
    nas_kode = (s["wilayah_kode"] == NASIONAL)
    asing = s[~nas_kode & ~s["wilayah_kode"].isin(PROV38)]
    alasan["wilayah_di_luar_38_provinsi"] = int(asing["_asal"].sum())
    s = s[nas_kode | s["wilayah_kode"].isin(PROV38)]
    terpilih, sisa = pilih_satu(s)
    for a, n in sisa.groupby("alasan")["_asal"].sum().items():
        alasan[a] = int(n)
    terpilih["indikator"] = terpilih["seri_kode"] + "|" + terpilih["rincian"]
    terpilih, terbawa, di_silver_saja = bawa_penanda(terpilih)
    # sel yang pernah dikoreksi selalu bertanda, walau tidak pernah jadi calon anomali di profil
    tanpa = (terpilih["perbaikan"].fillna("") != "") & (terpilih["penanda"] == "")
    terpilih.loc[tanpa, ["penanda", "subkategori", "status_galat"]] = ["galat_input", "diperbaiki_tanpa_calon_anomali", "diperbaiki"]
    terpilih.loc[tanpa, "n_penanda"] = 1
    terbawa += int(tanpa.sum())
    for c in KOLOM_GOLD:
        if c not in terpilih.columns:
            terpilih[c] = np.nan
    t = terpilih[terpilih["wilayah_kode"] != NASIONAL]
    panel = t[KOLOM_GOLD].sort_values(["seri_kode", "rincian", "wilayah_kode", "tahun"]).reset_index(drop=True)
    nasional = terpilih[terpilih["wilayah_kode"] == NASIONAL][KOLOM_GOLD].sort_values(
        ["sumber", "seri_kode", "rincian", "tahun"]).reset_index(drop=True)
    for nama, d, k in [("panel", panel, ["sumber", "seri_kode", "rincian", "wilayah_kode", "tahun"]),
                       ("nasional", nasional, ["sumber", "seri_kode", "rincian", "wilayah_kode", "tahun"])]:
        if d.duplicated(k).any():
            raise ValueError(f"Gold {nama} masih punya sel ganda: {int(d.duplicated(k).sum())}")
    dari_silver = int(terpilih["_asal"].sum())
    tak_terpilih = int(sum(alasan.values()))
    assert dari_silver + tak_terpilih == n_silver, (dari_silver, tak_terpilih, n_silver)
    ring = {"baris_silver": n_silver, "baris_panel": len(panel), "baris_nasional": len(nasional),
            "baris_silver_tak_terpilih": tak_terpilih, "alasan": alasan, "perbaikan_diterapkan": n_perbaikan,
            "baris_dikonversi_satuan": n_konversi, "penanda_terbawa": terbawa,
            "penanda_pada_rincian_hanya_silver": di_silver_saja,
            "sel_revisi": int(terpilih["revisi"].sum()), "baris_agregat_tahunan": n_agregat,
            "baris_wdi_ditambahkan": len(wdi), "nilai_kosong_wdi_dilewati": n_wdi_kosong}
    tak_df = pd.concat([tak.assign(alasan="rincian_hanya_di_silver"), asing.assign(alasan="wilayah_di_luar_38_provinsi"), sisa],
                       ignore_index=True)
    return {"panel": panel, "nasional": nasional, "tak_terpilih": tak_df, "ringkasan": ring}


def jalankan(silver) -> dict:
    """Dipanggil pipeline.py: gold.jalankan(h['silver'])."""
    h = bangun(silver)
    GOLD.mkdir(parents=True, exist_ok=True)
    OUT_TABEL.mkdir(parents=True, exist_ok=True)
    # Kolom baku untuk validasi Gold: periode (string) dan satuan (bukan hanya satuan_baku).
    # Panel Gold hanya memuat sel terisi; sel kosong tetap berada di grid Silver.
    h["panel"] = h["panel"].assign(
        periode=h["panel"]["tahun"].astype(str),
        satuan=h["panel"]["satuan_baku"],
        status_sel="terisi",
        jenis_periode="tahun",
    )
    h["nasional"] = h["nasional"].assign(
        periode=h["nasional"]["tahun"].astype(str),
        satuan=h["nasional"]["satuan_baku"],
        jenis_periode="tahun",
    )
    h["panel"].to_parquet(GOLD / "panel_provinsi.parquet", index=False)
    h["panel"].to_parquet(GOLD / "panel.parquet", index=False)
    h["nasional"].to_parquet(GOLD / "nasional.parquet", index=False)
    cols = [c for c in ["sumber", "seri_kode", "rincian", "wilayah_kode", "periode", "nilai", "satuan", "_berkas_raw", "alasan"]
            if c in h["tak_terpilih"].columns]
    h["tak_terpilih"][cols].to_csv(OUT_TABEL / "gold_silver_tak_terpilih.csv", index=False)
    r = h["ringkasan"]
    print(f"Gold: panel {r['baris_panel']} baris, nasional {r['baris_nasional']} baris; "
          f"{r['baris_silver_tak_terpilih']} dari {r['baris_silver']} baris Silver tidak terpilih")
    for a, n in r["alasan"].items():
        print(f"  {a}: {n}")
    print(f"  WDI ditambahkan: {r['baris_wdi_ditambahkan']} baris (nilai kosong dilewati: {r['nilai_kosong_wdi_dilewati']})")
    print(f"  perbaikan galat diterapkan: {r['perbaikan_diterapkan']} | penanda terbawa: {r['penanda_terbawa']} | revisi: {r['sel_revisi']}")
    p = h["panel"]
    ringkas = (p.groupby(["indikator", "satuan"])
               .agg(periode=("periode", lambda s: f"{s.min()}-{s.max()}" if s.nunique() > 1 else s.min()),
                    jumlah_periode=("periode", "nunique"), sel=("nilai", "size"),
                    terisi=("nilai", "count"), ditandai=("penanda", lambda s: int((s.astype(str) != "").sum())))
               .reset_index())
    catat(seri_panel=int(p["indikator"].nunique()), baris_gold=len(p), sel_gold_terisi=int(p["nilai"].notna().sum()),
          sel_gold_ditandai=int((p["penanda"].astype(str) != "").sum()),
          silver_tidak_terpilih=int(r["baris_silver_tak_terpilih"]))
    tulis("panel-gold.md", "\n\n".join([
        "# Panel Gold provinsi x periode x indikator",
        "Dihasilkan `python pipeline.py` (`src/gold/pilih.py` dan `src/gold/lebar.py`) dari Silver.",
        "## Aturan satu nilai per sel",
        "1. Snapshot terbaru dipakai; angka berbeda antar snapshot dicatat sebagai revisi.\n"
        "2. CSV didahulukan atas JSON bila snapshot sama.\n"
        "3. Rincian turunan (non_hutan, APL, total var1304/var588) tetap di Silver.\n"
        "4. Satuan luas dibakukan ke ribu_hektar.\n"
        "5. Baris Indonesia (9999) dipisah ke tabel nasional.\n"
        "6. Penanda anomali Sprint 1 terbawa; tidak ada nilai yang dihapus.",
        f"Panel panjang: **{len(p):,} baris**, {p['indikator'].nunique()} indikator, "
        f"{p['seri_kode'].nunique()} seri. Panel lebar: `data/gold/panel_lebar.parquet`.",
        "## Indikator", tabel_md(ringkas),
        "Kunci panel: `indikator + wilayah_kode + periode`; setiap sel terisi tertelusur ke Silver "
        "lewat `_berkas_raw`. Diperiksa otomatis di `reports/validasi.md`.",
    ]))
    return h


def catat_log(r: dict):
    ada = set()
    if LOG.exists():
        with open(LOG, encoding="utf-8-sig", newline="") as f:
            ada = {x["id"] for x in csv.DictReader(f)}
    n = max([int(i.split("-")[1]) for i in ada if i.startswith("K-") and i.split("-")[1].isdigit()], default=0)
    a = r["alasan"]
    tp = lambda *ks: sum(a.get(k, 0) for k in ks)
    E = [
        ("semua", "Snapshot: dipakai yang terbaru; bila angka beda antar snapshot dicatat sebagai revisi (nilai_snapshot_terdahulu, revisi=True); angka sama = bukan duplikat salah",
         "rata-rata antar snapshot; snapshot tertua", "revisi mencerminkan koreksi sumber dan tidak boleh dirata-rata; snapshot terbaru paling mutakhir",
         tp("snapshot_lebih_lama_angka_sama", "snapshot_lebih_lama_revisi")),
        ("semua", "Snapshot sama dari dua format: CSV didahulukan atas JSON; angka beda pada snapshot yang sama dilaporkan sebagai peringatan",
         "mengambil JSON", "CSV memuat kolom lengkap dan dibaca tanpa penguraian HTML", tp("berkas_lain_snapshot_sama_angka_sama", "berkas_lain_snapshot_sama_ANGKA_BEDA")),
        ("tabel hutan, var1304, var588", "Rincian di Gold: hutan dan total luas (penyebut); persen hutan; kawasan_hutan; kritis dan sangat_kritis. non_hutan, apl, dan total var1304/var588 tetap hanya di Silver",
         "memasukkan semua rincian", "non_hutan, apl, dan total adalah turunan aritmetika dari yang sudah masuk; memasukkannya menggandakan informasi", tp("rincian_hanya_di_silver")),
        ("var2532", "Enam komponen IKLH disimpan terpisah sebagai indikator sendiri; tidak dirata-rata menjadi indeks baru",
         "rata-rata sederhana semua komponen", "tidak ada bobot resmi; rata-rata tanpa bobot menciptakan indeks yang tidak ada di sumber", 0),
        ("semua", "Periode semester/triwulan/bulan diagregasi ke tahun dengan rata-rata bila minimal separuh periode terisi; jumlah periode dicatat (n_periode_sumber); seri aditif dikecualikan lewat AGREGASI",
         "menyimpan periode non-tahunan di panel; mengisi periode yang hilang", "panel Gold bertahun; periode yang tidak cukup tidak dipaksakan", tp("diagregasi_ke_tahun_non_tahunan")),
        ("semua", "Satuan dibakukan: luas ke ribu_hektar (hektar x0,001; km2 x0,1); persen dan indeks tetap; baris Indonesia (9999) dipisahkan ke tabel nasional bersama seri WDI",
         "memakai satuan sumber", "perbandingan antarseri dan dengan WDI memerlukan satuan sama", r["baris_dikonversi_satuan"]),
        ("semua", "Penanda anomali Sprint 1 (galat_input, patahan, outlier_asli) dan nilai_asal perbaikan terbawa ke Gold sebagai kolom; tidak ada nilai yang dihapus",
         "membuang baris outlier atau patahan", "penanda adalah informasi untuk analisis; menghapusnya menghilangkan sinyal", r["penanda_terbawa"]),
        ("AG.LND.FRST.ZS, AG.LND.FRST.K2, EN.ATM.PM25.MC.M3", "Seri WDI Indonesia masuk tabel nasional Gold: dibaca lewat src.ekstraksi.wdi.baca_wdi_data (Silver tim hanya BPS, K-010); wilayah_kode 9999, rincian total, periode tahunan; nilai kosong WDI dilewati dan tidak diisi; K2 dibakukan km2 -> ribu_hektar",
         "mengisi nilai kosong dengan interpolasi; mengubah Silver tim", "WDI sebagai pembanding nasional tidak boleh mengarang angka; Silver milik tim tidak diubah", r["nilai_kosong_wdi_dilewati"]),
    ]
    t = date.today().isoformat()
    baru = []
    for seri, kep, alt, alasan, dampak in E:
        n += 1
        baru.append([f"K-{n:03d}", t, NIM, "gold", seri, kep, alt, alasan, int(dampak)])
    akhir = LOG.exists() and not LOG.read_bytes().endswith(b"\n")
    with open(LOG, "a", encoding="utf-8", newline="") as f:
        if akhir:
            f.write("\n")
        csv.writer(f, lineterminator="\n").writerows(baru)
    print("log-keputusan.csv: +", len(baru), "entri (tahap gold)")


if __name__ == "__main__":
    h = jalankan(SILVER)
    if "--catat-log" in sys.argv:
        catat_log(h["ringkasan"])