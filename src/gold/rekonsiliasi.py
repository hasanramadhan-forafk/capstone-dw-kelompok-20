"""Tahap 6 - Tabel rekonsiliasi seri utama vs pembanding nasional.

Untuk setiap pasangan di ``konfigurasi.PASANGAN`` dan setiap seri pembandingnya, satu baris per
periode yang ada di salah satu sisi (gabung luar). Selisih = nilai utama - nilai pembanding sesudah
satuan disamakan. Selisih tidak dihapus dan tidak dipaksa sama.

Setiap baris berpasangan (``asal == "keduanya"``) wajib punya kategori baku dan penjelasan. Baris
yang hanya ada di satu sisi diberi kategori ``tanpa pasangan``. Kategori pasangan ditetapkan dari
bukti Sprint 1, bukan dari besar selisihnya.
"""
from pathlib import Path

import pandas as pd

from src import konfigurasi as K
from src.laporan import ROOT, catat, tabel_md, tulis

KATEGORI = (
    "definisi berbeda",
    "metode berbeda",
    "vintage berbeda",
    "cakupan berbeda",
    "konteks berbeda",
    "belum terjelaskan",
    "tanpa pasangan",
    "tidak berselisih",
)

# Kategori baku tiap pasangan (bukti: reports/pasangan-rekonsiliasi.md Sprint 1).
KATEGORI_BAKU = {
    "P1": "definisi berbeda",
    "P2": "definisi berbeda",
    "P3": "konteks berbeda",
    "P4": "belum terjelaskan",
}

# 1 km2 = 100 ha = 0,1 ribu hektar.
KONVERSI = {("km2", "ribu_hektar"): 0.1}

# Nama rincian di konfigurasi vs rincian yang dipakai Gold (pilih.py).
ALIAS_RINCIAN = {
    "tutupan=hutan": "hutan",
    "tutupan=non_hutan": "non_hutan",
    "komponen=iku": "kualitas_udara",
    "komponen=ika": "kualitas_air",
    "komponen=iktl": "kualitas_tutupan_lahan",
    "komponen=ikl": "kualitas_lahan",
    "komponen=ikeg": "kualitas_ekosistem_gambut",
    "komponen=ikal": "kualitas_air_laut",
}

KOLOM = [
    "pasangan_id", "jenis", "seri_utama", "rincian_utama", "seri_pembanding",
    "rincian_pembanding", "periode", "nilai_utama", "nilai_pembanding", "satuan",
    "selisih", "selisih_relatif", "asal", "kategori", "penjelasan", "catatan",
]
TOLERANSI = 1e-9


def _normalisasi(nasional: pd.DataFrame) -> pd.DataFrame:
    n = nasional.copy()
    if "periode" not in n.columns:
        n["periode"] = n["tahun"].astype(str)
    else:
        n["periode"] = n["periode"].astype(str)
    if "satuan" not in n.columns:
        n["satuan"] = n["satuan_baku"]
    return n


def sisi(nasional: pd.DataFrame, seri: str, rincian: str) -> pd.DataFrame:
    """Ambil satu sisi rekonsiliasi: periode, nilai, satuan (satu baris per periode)."""
    r = ALIAS_RINCIAN.get(rincian, rincian)
    s = nasional[(nasional["seri_kode"] == seri) & (nasional["rincian"] == r)]
    s = s[["periode", "nilai", "satuan"]].drop_duplicates("periode")
    return s.sort_values("periode").reset_index(drop=True)


def _faktor(dari, ke):
    if dari == ke:
        return 1.0
    return KONVERSI.get((dari, ke))


def _kategori(p: dict, asal: str, selisih, faktor) -> str:
    if asal != "keduanya":
        return "tanpa pasangan"
    if p["jenis"] != "selisih":
        return KATEGORI_BAKU.get(p["id"], "konteks berbeda")
    if faktor is None:
        return "belum terjelaskan"
    if selisih is not None and abs(selisih) <= TOLERANSI:
        return "tidak berselisih"
    return KATEGORI_BAKU.get(p["id"], "belum terjelaskan")


def satu_pasangan(nasional: pd.DataFrame, p: dict) -> list:
    utama = p["utama"].split(",")[0].strip()
    rincian_utama = p.get("rincian_utama", "total")
    a = sisi(nasional, utama, rincian_utama)
    # Satuan aktual di Gold didahulukan: pilih.py sudah menyeragamkan luas ke ribu_hektar.
    satuan_u = (a["satuan"].iloc[0] if len(a)
                else K.SERI.get(utama, {}).get("satuan"))

    baris = []
    for seri_b, rincian_b in p["pembanding"]:
        b = sisi(nasional, seri_b, rincian_b)
        satuan_b = (b["satuan"].iloc[0] if len(b)
                    else K.SERI.get(seri_b, {}).get("satuan"))
        faktor = _faktor(satuan_b, satuan_u) if seri_b else None
        gabung = a.merge(b, on="periode", how="outer", suffixes=("_u", "_b"), indicator=True)
        gabung = gabung.sort_values("periode")

        for r in gabung.to_dict("records"):
            asal = {"both": "keduanya", "left_only": "hanya_utama", "right_only": "hanya_pembanding"}[r["_merge"]]
            nilai_u = None if pd.isna(r["nilai_u"]) else float(r["nilai_u"])
            nilai_b = None if pd.isna(r["nilai_b"]) else float(r["nilai_b"])
            catatan = []
            if nilai_b is not None and faktor not in (None, 1.0):
                nilai_b = nilai_b * faktor
                catatan.append(f"pembanding dikali {faktor:g} ({satuan_b} -> {satuan_u})")

            selisih = None
            selisih_relatif = None
            if asal == "keduanya" and p["jenis"] == "selisih" and faktor is not None:
                selisih = nilai_u - nilai_b
                if nilai_b not in (None, 0):
                    selisih_relatif = 100 * selisih / nilai_b
            elif asal == "keduanya" and p["jenis"] != "selisih":
                catatan.append("pasangan konteks: selisih tidak dihitung")
            elif asal == "keduanya" and faktor is None:
                catatan.append(f"satuan berbeda ({satuan_b} vs {satuan_u}) tanpa faktor konversi")

            kategori = _kategori(p, asal, selisih, faktor)
            if asal == "hanya_utama":
                penjelasan = f"{p['kategori']}; periode ini hanya ada di seri utama."
            elif asal == "hanya_pembanding":
                penjelasan = f"{p['kategori']}; periode ini hanya ada di seri pembanding."
            else:
                penjelasan = p["kategori"]

            baris.append({
                "pasangan_id": p["id"], "jenis": p["jenis"], "seri_utama": utama,
                "rincian_utama": rincian_utama, "seri_pembanding": seri_b,
                "rincian_pembanding": rincian_b, "periode": r["periode"],
                "nilai_utama": nilai_u, "nilai_pembanding": nilai_b, "satuan": satuan_u,
                "selisih": selisih, "selisih_relatif": selisih_relatif, "asal": asal,
                "kategori": kategori, "penjelasan": penjelasan,
                "catatan": "; ".join(catatan) or None,
            })
    return baris


def jalankan(nasional: pd.DataFrame) -> pd.DataFrame:
    n = _normalisasi(nasional)
    rows = [b for p in K.PASANGAN for b in satu_pasangan(n, p)]
    t = pd.DataFrame(rows, columns=KOLOM)
    for c in ("nilai_utama", "nilai_pembanding", "selisih", "selisih_relatif"):
        t[c] = pd.to_numeric(t[c], errors="coerce")

    tujuan = ROOT / "data" / "gold" / "rekonsiliasi.parquet"
    tujuan.parent.mkdir(parents=True, exist_ok=True)
    t.to_parquet(tujuan, index=False)

    berpasangan = t[t["asal"] == "keduanya"]
    dihitung = t[t["selisih"].notna()]
    ring = (
        t.groupby(["pasangan_id", "seri_pembanding"], sort=False)
        .agg(jenis=("jenis", "first"), periode=("periode", "size"),
             berpasangan=("asal", lambda s: int((s == "keduanya").sum())),
             selisih_dihitung=("selisih", lambda s: int(s.notna().sum())),
             median_selisih_relatif=("selisih_relatif", lambda s: s.abs().median()),
             kategori=("kategori", lambda s: ", ".join(f"{k} ({v})" for k, v in s.value_counts().items())))
        .reset_index()
    )

    bagian = []
    for p in K.PASANGAN:
        isi = t[t["pasangan_id"] == p["id"]][
            ["seri_pembanding", "periode", "nilai_utama", "nilai_pembanding", "selisih",
             "selisih_relatif", "asal", "kategori", "catatan"]
        ]
        bagian.append("\n\n".join([
            f"### {p['id']}: {p['judul']}",
            f"Jenis **{p['jenis']}**; kategori baku: **{KATEGORI_BAKU.get(p['id'], 'belum terjelaskan')}**. "
            f"{p['kategori'][0].upper()}{p['kategori'][1:]}.",
            tabel_md(isi, 2),
        ]))

    med = float(dihitung["selisih_relatif"].abs().median()) if len(dihitung) else 0.0
    catat(
        baris_rekonsiliasi=len(t),
        baris_rekonsiliasi_berpasangan=len(berpasangan),
        selisih_dihitung=len(dihitung),
        selisih_median_relatif=round(med, 2),
        rekonsiliasi_tanpa_pasangan=int((t["kategori"] == "tanpa pasangan").sum()),
        rekonsiliasi_kategori=int(t["kategori"].nunique()),
        **{f"rek_{pid.lower()}_berpasangan": int(g["asal"].eq("keduanya").sum())
           for pid, g in t.groupby("pasangan_id")},
        **{f"rek_{pid.lower()}_dihitung": int(g["selisih"].notna().sum())
           for pid, g in t.groupby("pasangan_id")},
    )
    tulis("rekonsiliasi.md", "\n\n".join([
        "# Tabel rekonsiliasi seri utama vs pembanding nasional",
        "Dihasilkan `python pipeline.py` (`src/gold/rekonsiliasi.py`) dari tabel nasional Gold. "
        "Selisih = nilai utama - nilai pembanding sesudah satuan disamakan; selisih relatif dalam persen "
        "terhadap pembanding. Periode tanpa pasangan tetap ditampilkan, tidak dihapus.",
        "## Ringkasan per pasangan", tabel_md(ring, 2),
        f"Baris berpasangan: {len(berpasangan)}; selisih dihitung: {len(dihitung)}; "
        f"median selisih relatif mutlak: {med:.2f}%.",
        "## Kategori",
        "Kategori baku: " + ", ".join(f"*{k}*" for k in KATEGORI) + ". Setiap baris berpasangan "
        "(`asal = keduanya`) wajib punya kategori dan penjelasan; ini diperiksa otomatis oleh "
        "`src/validasi/gold.py`.",
        "## Rincian per pasangan", *bagian,
    ]))
    return t
