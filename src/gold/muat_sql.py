"""Tahap 5 — Silver dan Gold di DuckDB, beserta pembanding penyimpanan dokumen.

Basis data dibuat ulang setiap kali (berkas lama dihapus), jadi isinya selalu sama dengan Parquet di
data/silver dan data/gold. Berkas .duckdb tidak di-commit; jalankan pipeline untuk membuatnya.

Selain tabel relasional, berkas JSON mentah disimpan apa adanya di tabel `dokumen_mentah` (kolom JSON) untuk
membandingkan dua cara penyimpanan pada pertanyaan yang sama; hasilnya di reports/basis-data.md.
"""
import json
import time
from pathlib import Path

import duckdb
import pandas as pd

from src.common.manifest import baca
from src.laporan import ROOT, catat, tabel_md, tulis

DB = ROOT / "data" / "gold" / "gudang.duckdb"
DDL = [Path(__file__).with_name("silver.sql"), Path(__file__).with_name("gold.sql")]
RAW = ROOT / "data" / "raw"
GOLD = ROOT / "data" / "gold"

KOLOM_PANEL = (
    "indikator", "seri_kode", "rincian", "wilayah_kode", "nama_wilayah", "periode", "jenis_periode", "nilai",
    "satuan", "status_sel", "penanda", "rujukan_tahun", "_berkas_raw", "_sha256_raw",
)
KOLOM_NASIONAL = (
    "seri_kode", "rincian", "sumber", "periode", "jenis_periode", "nilai", "satuan", "batas_bawah", "batas_atas",
    "rujukan_tahun", "asal", "_berkas_raw", "_sha256_raw",
)
KOLOM_REKONSILIASI = (
    "pasangan_id", "jenis", "seri_utama", "rincian_utama", "seri_pembanding", "rincian_pembanding", "periode",
    "nilai_utama", "nilai_pembanding", "satuan", "selisih", "selisih_relatif", "asal", "kategori", "penjelasan",
    "catatan",
)


def _q(con, sql, param=None):
    """DuckDB 2: hasil setiap execute harus dihabiskan sebelum perintah berikutnya."""
    return con.execute(sql, param or []).fetchall()


def _muat(con, tabel, df):
    con.register("_df", df)
    kolom = ", ".join(df.columns)
    _q(con, f"INSERT INTO {tabel} ({kolom}) SELECT {kolom} FROM _df")
    con.unregister("_df")
    n = _q(con, f"SELECT count(*) FROM {tabel}")[0][0]
    if n != len(df):
        raise AssertionError(f"DuckDB memuat {n} baris {tabel}, Parquet {len(df)} baris")
    return n


def _ambil_gold(gold, kunci, berkas_parquet, syarat_kolom=()):
    """Ambil DataFrame Gold dari dict hasil tahap Gold atau dari berkas Parquet bila sudah tersedia."""
    if isinstance(gold, dict):
        for k in (kunci, f"gold_{kunci}"):
            if k in gold and isinstance(gold[k], pd.DataFrame):
                df = gold[k]
                if not syarat_kolom or all(c in df.columns for c in syarat_kolom):
                    return df
    for nama in berkas_parquet:
        jalur = GOLD / nama
        if jalur.exists():
            return pd.read_parquet(jalur)
    return None


def _siapkan_panel(df):
    p = df.copy()
    if "periode" not in p.columns and "tahun" in p.columns:
        p["periode"] = p["tahun"].astype(int).astype(str)
    if "jenis_periode" not in p.columns:
        p["jenis_periode"] = "tahun"
    if "satuan" not in p.columns and "satuan_baku" in p.columns:
        p["satuan"] = p["satuan_baku"]
    if "status_sel" not in p.columns:
        p["status_sel"] = "terisi"
    p = p[[c for c in KOLOM_PANEL if c in p.columns]].copy()
    if "rujukan_tahun" in p.columns:
        p["rujukan_tahun"] = pd.to_numeric(
            p["rujukan_tahun"].astype(object).where(p["rujukan_tahun"].notna(), None), errors="coerce"
        ).astype("float64")
    return p


def _siapkan_nasional(df):
    n = df.copy()
    if "periode" not in n.columns and "tahun" in n.columns:
        n["periode"] = n["tahun"].astype(int).astype(str)
    if "jenis_periode" not in n.columns:
        n["jenis_periode"] = "tahun"
    if "satuan" not in n.columns and "satuan_baku" in n.columns:
        n["satuan"] = n["satuan_baku"]
    if "asal" not in n.columns and "sumber" in n.columns:
        n["asal"] = n["sumber"].map(lambda s: "baris_indonesia" if s == "bps" else "pembanding")
    n = n[[c for c in KOLOM_NASIONAL if c in n.columns]].copy()
    for c in ("batas_bawah", "batas_atas", "rujukan_tahun"):
        if c in n.columns:
            n[c] = pd.to_numeric(
                n[c].astype(object).where(n[c].notna(), None), errors="coerce"
            ).astype("float64")
    return n


def _siapkan_rekonsiliasi(df):
    return df[[c for c in KOLOM_REKONSILIASI if c in df.columns]].copy()


def dokumen(con):
    """Semua berkas JSON mentah ke tabel dokumen_mentah (isi utuh, tanpa diratakan)."""
    sha = baca(RAW)
    n = 0
    for berkas, s in sorted(sha.items()):
        if not berkas.endswith(".json"):
            continue
        teks = (RAW / berkas).read_text(encoding="utf-8-sig")
        json.loads(teks)
        _q(con, "INSERT INTO dokumen_mentah VALUES (?, ?, ?, ?)", [berkas, s, berkas.split("/")[0], teks])
        n += 1
    return n


def bandingkan(con, silver):
    """Pertanyaan yang sama dijawab dari tabel Silver dan dari dokumen JSON mentah."""
    hasil = []
    bps = silver[silver["sumber"] == "bps"]
    if not len(bps):
        return pd.DataFrame(hasil)

    dok_json = {r[0] for r in _q(con, "SELECT _berkas_raw FROM dokumen_mentah WHERE sumber = 'bps'")}
    kandidat = None
    for berkas in bps["_berkas_raw"].drop_duplicates():
        if berkas.endswith(".json") and berkas in dok_json:
            kandidat = (berkas, berkas)
            break
        stem = Path(berkas).stem
        padanan = next((d for d in sorted(dok_json) if Path(d).stem == stem and "tutupan_hutan" not in d), None)
        if padanan:
            kandidat = (berkas, padanan)
            break
    if not kandidat:
        berkas = bps["_berkas_raw"].iloc[0]
        stem = Path(berkas).stem
        padanan = next((d for d in sorted(dok_json) if Path(d).stem == stem), None)
        if not padanan:
            return pd.DataFrame(hasil)
        kandidat = (berkas, padanan)

    berkas_silver, berkas_json = kandidat
    seri = bps.loc[bps["_berkas_raw"] == berkas_silver, "seri_kode"].iloc[0]

    t0 = time.perf_counter()
    a = _q(con, "SELECT count(*) FROM silver WHERE _berkas_raw = ?", [berkas_silver])[0][0]
    t1 = time.perf_counter()
    b = _q(
        con,
        "SELECT CASE "
        "WHEN json_type(isi) = 'ARRAY' THEN ("
        "  SELECT coalesce(sum(json_array_length(json_keys(h.value -> '$.datacontent'))), 0) "
        "  FROM json_each(isi) h"
        ") "
        "ELSE coalesce(json_array_length(json_keys(isi -> '$.datacontent')), 0) "
        "END "
        "FROM dokumen_mentah WHERE _berkas_raw = ?",
        [berkas_json],
    )[0][0]
    t2 = time.perf_counter()

    hasil.append({
        "pertanyaan": f"berapa angka {seri} di `{berkas_json}`",
        "tabel_silver": a,
        "dokumen_json": b,
        "ms_silver": round(1000 * (t1 - t0), 2),
        "ms_dokumen": round(1000 * (t2 - t1), 2),
        "catatan": "dokumen menghitung semua kunci datacontent pada JSON bersarang (termasuk sel kosong/non-panel); "
                   "tabel Silver hanya baris observasi tervalidasi",
    })
    return pd.DataFrame(hasil)


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

    panel_df = _ambil_gold(gold, "panel", ("panel_provinsi.parquet", "panel.parquet"), ("indikator", "wilayah_kode"))
    nasional_df = _ambil_gold(gold, "nasional", ("nasional.parquet",), ("seri_kode", "nilai"))
    rekonsiliasi_df = _ambil_gold(gold, "rekonsiliasi", ("rekonsiliasi.parquet",), ("pasangan_id", "kategori"))

    with duckdb.connect(str(DB)) as con:
        for f in DDL:
            teks = "\n".join(b for b in f.read_text(encoding="utf-8").splitlines() if not b.strip().startswith("--"))
            for perintah in teks.split(";"):
                if perintah.strip():
                    _q(con, perintah)

        n_seri = _muat(con, "seri", seri)
        n = {"silver": _muat(con, "silver", s)}
        n["gold_panel"] = _muat(con, "gold_panel", _siapkan_panel(panel_df)) if panel_df is not None else 0
        n["gold_nasional"] = _muat(con, "gold_nasional", _siapkan_nasional(nasional_df)) if nasional_df is not None else 0
        n["rekonsiliasi"] = _muat(con, "rekonsiliasi", _siapkan_rekonsiliasi(rekonsiliasi_df)) if rekonsiliasi_df is not None else 0

        n_dok = dokumen(con)
        banding = bandingkan(con, silver)

        tabel_uji = "gold_panel" if n["gold_panel"] > 0 else "silver"
        try:
            _q(con, f"INSERT INTO {tabel_uji} SELECT * FROM {tabel_uji} LIMIT 1")
            tolak = "TIDAK ditolak"
        except duckdb.ConstraintException:
            tolak = "ditolak (ConstraintException)"

    ukuran = DB.stat().st_size
    baris_gold = n["gold_panel"] + n["gold_nasional"] + n["rekonsiliasi"]
    catat(
        baris_sql=n["silver"],
        baris_sql_gold=baris_gold,
        dokumen_json=n_dok,
        tabel_sql=6,
        mb_duckdb=round(ukuran / 1e6, 2),
    )

    sumber_tabel = {
        "seri": "docs/seri.csv",
        "silver": "data/silver/silver.parquet",
        "gold_panel": "data/gold/panel_provinsi.parquet" if (GOLD / "panel_provinsi.parquet").exists() else "data/gold/panel.parquet",
        "gold_nasional": "data/gold/nasional.parquet",
        "rekonsiliasi": "data/gold/rekonsiliasi.parquet",
        "dokumen_mentah": "data/raw/**/*.json",
    }
    tabel = pd.DataFrame([
        {"tabel": k, "baris": v, "sumber": sumber_tabel[k]}
        for k, v in {"seri": n_seri, **n, "dokumen_mentah": n_dok}.items()
    ])
    tulis("basis-data.md", "\n\n".join([
        "# Silver dan Gold di SQL",
        "Dihasilkan `python pipeline.py` (`src/gold/muat_sql.py`). DDL: `src/gold/silver.sql` dan `src/gold/gold.sql`. "
        f"Basis data `data/gold/gudang.duckdb` ({ukuran / 1e6:.2f} MB) dibuat ulang setiap kali dan tidak di-commit.",
        "## Isi", tabel_md(tabel),
        "Jumlah baris setiap tabel yang memiliki sumber Parquet dicocokkan langsung saat dimuat; beda satu baris pun menghentikan pipeline.",
        "## Kunci primer dan batasan",
        "- `seri`: (seri_kode) — kamus metadata baku referensi *foreign key*.\n"
        "- `silver`: (sumber, seri_kode, wilayah_kode, periode, rincian, _berkas_raw) — dua snapshot boleh berdampingan.\n"
        "- `gold_panel`: (indikator, wilayah_kode, periode) — satu nilai per sel; CHECK status sel dan nilai kosong hanya bila sel kosong.\n"
        "- `gold_nasional`: (seri_kode, rincian, periode) — seri utama, pembanding, dan agregat nasional.\n"
        "- `rekonsiliasi`: (pasangan_id, seri_pembanding, rincian_pembanding, periode) — CHECK kategori baku dan selisih = utama − pembanding.\n"
        "- `dokumen_mentah`: (_berkas_raw) — penyimpanan dokumen JSON utuh per berkas.",
        f"Uji kunci primer pada `{tabel_uji}`: memasukkan ulang satu baris yang sudah ada → {tolak}.",
        "## Mengapa DuckDB, dan mengapa tabel (bukan dokumen)",
        "DuckDB dipilih karena satu berkas tanpa server (*serverless*), mendukung eksekusi kolumnar untuk agregasi/pivot analitik, "
        "dan dapat membaca Parquet secara langsung; SQLite atau PostgreSQL sama sahnya. Lapis Silver dan Gold disimpan sebagai "
        "**tabel relasional** karena pertanyaan analisisnya selalu berdimensi `seri × wilayah × periode × rincian` dan membutuhkan "
        "penegakan integritas (kunci primer yang menolak sel ganda, *foreign key* ke `seri`, serta `CHECK` status/kategori). "
        "Sebaliknya, berkas JSON mentah disimpan sebagai **dokumen** (`dokumen_mentah`) hanya sebagai pembanding dan arsip lapis Bronze: "
        "bentuk dokumen menjaga struktur bersarang dan metadata asli (`var`, `vervar`, `turvar`), tetapi setiap kueri harus mengurai struktur JSON "
        "dan tidak memiliki kunci primer tingkat observasi.",
        tabel_md(banding) if len(banding) else "Tidak ada berkas JSON BPS untuk dibandingkan.",
    ]))
    return n


if __name__ == "__main__":
    n = jalankan()
    print(f"Berhasil memuat DuckDB ke {DB}: {n}")
