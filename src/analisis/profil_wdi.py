"""Tahap 2: profil seri pembanding WDI, irisan tahun dengan seri utama, kandidat rincian sebanding.

Hanya mendaftar dan menandai; tidak ada nilai yang diubah atau dikonversi di data.
Berkas WDI berbentuk [meta, [rekaman]]; tiap rekaman = indikator x negara x tahun (tanpa rincian).
"""
import json
from pathlib import Path

import pandas as pd

from src.analisis.profil import md, muat, siapkan

RAW_WDI = Path("data/raw/wdi")
OUT_TABEL = Path("reports/tabel")
OUT_LAPORAN = Path("reports/profil_wdi.md")
WDI = ["AG.LND.FRST.ZS", "AG.LND.FRST.K2", "EN.ATM.PM25.MC.M3"]
SATUAN = {"AG.LND.FRST.ZS": "persen luas daratan", "AG.LND.FRST.K2": "km2",
          "EN.ATM.PM25.MC.M3": "ug/m3"}   # kolom `unit` API kosong; satuan dari nama indikator di metadata
IDN = {"IDN", "ID"}
KUNCI_BAKU = {"indicator", "country", "countryiso3code", "date", "value", "unit",
              "obs_status", "decimal", "scale"}

# (seri WDI, seri utama, rincian utama, status, alasan). Verifikasi akhir di tahap 6.
KANDIDAT = [
    ("AG.LND.FRST.ZS", "tabel:sdg15_tutupan_hutan:persen", "hutan", "kandidat",
     "Sama-sama persen luas hutan. Penyebut beda: WDI = luas daratan (FAO), BPS = jumlah luas wilayah; "
     "definisi hutan juga bisa beda. Bandingkan arah/tren dulu, level dengan catatan."),
    ("AG.LND.FRST.K2", "tabel:sdg15_tutupan_hutan:luas_ribu_ha", "hutan", "kandidat",
     "Sama-sama luas tutupan hutan. Seragamkan satuan (1 km2 = 0,1 ribu ha). Pembanding nasional BPS = "
     "jumlah 38 provinsi; Kaltim 2014-2020 masih gabungan dengan Kaltara dan nilai 2020 tertukar antarprovinsi "
     "(total nasional tidak terpengaruh jika murni tertukar)."),
    ("AG.LND.FRST.K2", "var1304", "Kawasan Hutan", "sekunder",
     "Kawasan hutan = status penetapan, bukan tutupan; level bisa berbeda jauh dari WDI."),
    ("AG.LND.FRST.ZS", "var1304", "Kawasan Hutan", "tidak sebanding",
     "Persen tutupan vs luas kawasan berstatus hutan: konsep berbeda."),
    ("EN.ATM.PM25.MC.M3", "var2532", "Indeks Kualitas Udara", "hanya arah",
     "PM2.5 (ug/m3, rata-rata tertimbang populasi nasional) vs indeks tanpa satuan: bandingkan arah tren "
     "atau korelasi, bukan level. Indeks lain (air, lahan, gambut) tidak sebanding."),
    ("AG.LND.FRST.ZS", "var588", "Kritis / Sangat Kritis / Jumlah", "tidak sebanding",
     "Lahan kritis tidak punya padanan di WDI; hanya 4 periode."),
    ("AG.LND.FRST.K2", "var588", "Kritis / Sangat Kritis / Jumlah", "tidak sebanding",
     "Lahan kritis tidak punya padanan di WDI; hanya 4 periode."),
    ("EN.ATM.PM25.MC.M3", "var1304", "(semua)", "tidak sebanding", "Variabel berbeda."),
    ("EN.ATM.PM25.MC.M3", "var588", "(semua)", "tidak sebanding", "Variabel berbeda."),
    ("EN.ATM.PM25.MC.M3", "tabel:sdg15_tutupan_hutan:luas_ribu_ha", "(semua)", "tidak sebanding", "Variabel berbeda."),
    ("EN.ATM.PM25.MC.M3", "tabel:sdg15_tutupan_hutan:persen", "(semua)", "tidak sebanding", "Variabel berbeda."),
]


def _rekaman(obj) -> list:
    if isinstance(obj, list) and len(obj) == 2 and isinstance(obj[1], list):
        return obj[1]
    return obj if isinstance(obj, list) else []


def muat_wdi() -> pd.DataFrame:
    baris, kunci_lain, nama = [], set(), {}
    for f in sorted(RAW_WDI.glob("*/data/*.json")):
        with open(f, encoding="utf-8") as h:
            obj = json.load(h)
        for r in _rekaman(obj):
            kunci_lain |= set(r) - KUNCI_BAKU
            ind = r.get("indicator") or {}
            nama[ind.get("id")] = ind.get("value")
            baris.append({
                "seri_kode": ind.get("id"), "nama_seri": ind.get("value"),
                "negara": r.get("countryiso3code") or (r.get("country") or {}).get("id"),
                "tahun": r.get("date"), "nilai": r.get("value"),
                "satuan_api": r.get("unit"), "obs_status": r.get("obs_status"),
                "_berkas_raw": f.name})
    d = pd.DataFrame(baris)
    d["tahun"] = pd.to_numeric(d["tahun"], errors="coerce")
    d["nilai"] = pd.to_numeric(d["nilai"], errors="coerce")
    d.attrs["kunci_tambahan"] = sorted(kunci_lain)
    return d


def metadata() -> dict:
    """Definisi dan sumber asli tiap seri dari metadata WDI (source id 2)."""
    hasil = {}
    for f in sorted(RAW_WDI.glob("*/metadata/sumber2_indikator.json")):
        with open(f, encoding="utf-8") as h:
            for m in json.load(h)[1]:
                if m["id"] in WDI:
                    hasil[m["id"]] = {"nama_resmi": m["name"], "definisi": m["sourceNote"],
                                      "organisasi_sumber": m["sourceOrganization"].split(", uri:")[0]}
    return hasil


def ketersediaan(d: pd.DataFrame, meta: dict) -> pd.DataFrame:
    hasil = []
    for s in WDI:
        x = d[d["seri_kode"] == s]
        i = x[x["negara"].isin(IDN)]
        ada = i.dropna(subset=["nilai"])
        rentang = range(int(i["tahun"].min()), int(i["tahun"].max()) + 1) if len(i) else []
        kosong = sorted(set(rentang) - set(ada["tahun"].astype(int)))
        hasil.append({
            "seri_kode": s, "nama": meta.get(s, {}).get("nama_resmi", ""),
            "satuan": SATUAN[s], "satuan_di_api": ", ".join(sorted(i["satuan_api"].dropna().astype(str).unique())) or "(kosong)",
            "n_entitas": x["negara"].nunique(), "n_baris_indonesia": len(i),
            "tahun_pertama_bernilai": int(ada["tahun"].min()), "tahun_terakhir_bernilai": int(ada["tahun"].max()),
            "n_tahun_bernilai": len(ada),
            "nilai_min": round(ada["nilai"].min(), 2), "nilai_maks": round(ada["nilai"].max(), 2),
            "tahun_kosong_dalam_rentang_bernilai": ", ".join(str(t) for t in kosong if ada["tahun"].min() <= t <= ada["tahun"].max()),
            "rincian": "tidak ada (1 nilai nasional per tahun)" if not d.attrs["kunci_tambahan"] else ", ".join(d.attrs["kunci_tambahan"]),
            "organisasi_sumber": meta.get(s, {}).get("organisasi_sumber", ""),
            "berkas": ", ".join(sorted(x["_berkas_raw"].unique()))})
    return pd.DataFrame(hasil)


def irisan(d: pd.DataFrame, u: pd.DataFrame) -> pd.DataFrame:
    hasil = []
    for s in WDI:
        t_w = set(d[(d["seri_kode"] == s) & d["negara"].isin(IDN)].dropna(subset=["nilai"])["tahun"].astype(int))
        for su, g in u.dropna(subset=["nilai"]).groupby("seri"):
            t_u = set(g["periode"].astype(int))
            ir = sorted(t_w & t_u)
            hasil.append({"seri_wdi": s, "seri_utama": su, "tahun_wdi": f"{min(t_w)}-{max(t_w)}",
                          "tahun_utama": ", ".join(map(str, sorted(t_u))), "n_irisan": len(ir),
                          "tahun_irisan": ", ".join(map(str, ir))})
    return pd.DataFrame(hasil)


def main():
    OUT_TABEL.mkdir(parents=True, exist_ok=True)
    d = muat_wdi()
    print("entitas di berkas:", sorted(d["negara"].dropna().unique()), "| jumlah seri di berkas:", d["seri_kode"].nunique())
    print("seri target ada:", [s for s in WDI if s in set(d["seri_kode"])], "| HILANG:", [s for s in WDI if s not in set(d["seri_kode"])])
    print("kunci tambahan di luar baku:", d.attrs["kunci_tambahan"])
    meta = metadata()
    u = siapkan(muat())
    k, ir = ketersediaan(d, meta), irisan(d, u)
    kand = pd.DataFrame(KANDIDAT, columns=["seri_wdi", "seri_utama", "rincian_utama", "status", "alasan"])
    kand = kand.merge(ir[["seri_wdi", "seri_utama", "n_irisan", "tahun_irisan"]], on=["seri_wdi", "seri_utama"], how="left")
    k.to_csv(OUT_TABEL / "wdi_ketersediaan.csv", index=False)
    ir.to_csv(OUT_TABEL / "wdi_irisan_tahun.csv", index=False)
    kand.to_csv(OUT_TABEL / "wdi_kandidat_rincian.csv", index=False)
    defs = [f"- **{s}**: {meta[s]['definisi']}" for s in WDI if s in meta]
    L = ["# Tahap 2: profil seri pembanding WDI", "",
         "Hanya Indonesia (nasional); tidak ada rincian jenis kelamin, umur, atau daerah. Tidak ada nilai yang diubah. "
         "Status kandidat adalah penilaian dari nama, satuan, dan definisi metadata; konfirmasi nilainya di tahap 6.", "",
         "## Definisi (metadata WDI)", *defs, "",
         "## Ketersediaan seri × periode × rincian", md(k), "",
         "## Irisan tahun dengan seri utama", md(ir), "",
         "## Kandidat rincian sebanding untuk tahap 6", md(kand), ""]
    OUT_LAPORAN.write_text("\n".join(L), encoding="utf-8")
    print(k.T.to_string()); print(kand[["seri_wdi", "seri_utama", "status", "n_irisan", "tahun_irisan"]].to_string())


if __name__ == "__main__":
    main()