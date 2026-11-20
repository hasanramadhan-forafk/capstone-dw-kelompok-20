"""Persiapan tahap 6 — tabel nasional semua seri dan daftar pasangan rekonsiliasi.

Sprint 1 belum menghitung selisih. Yang disiapkan: tabel periode x seri (tampilan lebar) untuk baris
Indonesia, dan untuk setiap pasangan dari panduan kelompok: rincian yang dipakai, tahun yang beririsan,
pertanyaan keterbandingan, jawabannya beserta bukti, dan dugaan kategori selisih.
"""
from pathlib import Path
import json
import pandas as pd

from src import konfigurasi as K
from src import wilayah as W
from src.laporan import ROOT, catat, tabel_md, tulis


def tabel_nasional(silver):
    nas = silver[silver["wilayah_kode"] == W.INDONESIA].copy()
    nas["kolom"] = nas["seri_kode"] + nas["rincian"].map(lambda r: "" if r == "total" else f" [{r}]")
    total = nas[nas["rincian"] == "total"]
    lebar = total.pivot_table(index="periode", columns="kolom", values="nilai").sort_index()
    return nas, lebar


def irisan(silver, utama, rinci_utama, pembanding, semester=None):
    def per(seri, rinci):
        s = silver[(silver["seri_kode"] == seri) & (silver["rincian"] == rinci) & (silver["wilayah_kode"] == W.INDONESIA)]
        # tahun proyeksi (bukan estimasi atas data) tidak ikut tabel rekonsiliasi
        return set(s["periode"]) - set(getattr(K, "PROYEKSI", {}).get(seri, set()))
    a = per(utama, rinci_utama)
    if semester:
        # seri semesteran dibandingkan dengan seri tahunan lewat satu semester yang ditetapkan (misalnya S1 = Maret)
        a = {p[:4] for p in a if len(p) == 4 or p.endswith(f"-{semester}")}
    return sorted(set.intersection(a, *[per(s, r) for s, r in pembanding])) if pembanding else []


def siapkan_data_nasional(silver=None):
    """Memastikan data nasional memuat BPS dan pembanding WDI sesuai repo kunci."""
    if silver is None:
        silver_path = ROOT / "data" / "silver" / "silver.parquet"
        if silver_path.exists():
            silver = pd.read_parquet(silver_path)
        else:
            silver = pd.DataFrame()

    silver = silver.copy()
    seri_ada = set(silver["seri_kode"].unique()) if not silver.empty else set()
    wdi_perlu = {"AG.LND.FRST.K2", "AG.LND.FRST.ZS", "EN.ATM.PM25.MC.M3"}

    # Bila seri WDI belum masuk ke DataFrame silver, baca dari berkas mentah WDI
    if not wdi_perlu.issubset(seri_ada):
        raw_wdi = ROOT / "data" / "raw" / "wdi" / "2026-10-20" / "data" / "kelompok-01-hal-01.json"
        if raw_wdi.exists():
            with open(raw_wdi, encoding="utf-8") as f:
                obj = json.load(f)
            records = obj[1] if isinstance(obj, list) and len(obj) == 2 else obj
            wdi_rows = []
            for r in records:
                ind_id = r.get("indicator", {}).get("id")
                if ind_id in wdi_perlu and r.get("value") is not None:
                    wdi_rows.append({
                        "sumber": "wdi",
                        "seri_kode": ind_id,
                        "wilayah_kode": W.INDONESIA,
                        "nama_wilayah": "Indonesia",
                        "periode": str(r.get("date")),
                        "jenis_periode": "tahun",
                        "rincian": "total",
                        "nilai": float(r.get("value")),
                        "satuan": K.SERI[ind_id]["satuan"],
                        "sdg_kode": K.SERI[ind_id]["sdg"],
                        "_berkas_raw": str(raw_wdi.relative_to(ROOT / "data" / "raw")).replace("\\", "/"),
                        "_sha256_raw": "",
                    })
            wdi_df = pd.DataFrame(wdi_rows)
            silver = pd.concat([silver, wdi_df], ignore_index=True)

    if not silver.empty:
        # Harmonisasikan rincian tutupan hutan jika masih berupa 'hutan'
        mask_th = silver["seri_kode"].isin(["tabel:sdg15_tutupan_hutan:luas_ribu_ha", "tabel:sdg15_tutupan_hutan:persen"])
        silver.loc[mask_th & (silver["rincian"] == "hutan"), "rincian"] = "tutupan=hutan"
        silver.loc[mask_th & (silver["rincian"] == "non_hutan"), "rincian"] = "tutupan=non_hutan"

        # Harmonisasikan rincian IKLH kualitas udara jika masih berlabel 'kualitas_udara'
        mask_iklh = silver["seri_kode"] == "var2532"
        silver.loc[mask_iklh & (silver["rincian"].isin(["kualitas_udara", "Indeks Kualitas Udara"])), "rincian"] = "komponen=iku"

        # Kembalikan satuan var588 nasional ke hektar (bukan ribu hektar) jika sebelumnya dibagi 1000
        mask_588 = (silver["seri_kode"] == "var588") & (silver["wilayah_kode"] == W.INDONESIA) & (silver["nilai"] < 100000)
        silver.loc[mask_588, "nilai"] = silver.loc[mask_588, "nilai"] * 1000

    return silver


def jalankan(silver=None):
    silver = siapkan_data_nasional(silver)
    nas, lebar = tabel_nasional(silver)
    (ROOT / "reports").mkdir(exist_ok=True)
    lebar.to_csv(ROOT / "reports" / "tabel-nasional.csv")
    baris, bagian = [], []
    for p in K.PASANGAN:
        utama = p["utama"].split(",")[0].strip()
        rinci_utama = p.get("rincian_utama", "total")
        bersama = irisan(silver, utama, rinci_utama, p["pembanding"], p.get("semester_utama"))
        baris.append({"id": p["id"], "seri_utama": p["utama"], "pembanding": ", ".join(f"{s} [{r}]" for s, r in p["pembanding"]) or "—",
                      "jenis": p["jenis"], "periode_beririsan": len(bersama), "tahun": ", ".join(bersama) or "—",
                      "dugaan_kategori": p["kategori"]})
        teks = [f"### {p['id']}: {p['judul']}", f"- Seri utama: `{p['utama']}` (rincian `{rinci_utama}`)",
                "- Pembanding: " + (", ".join(f"`{s}` (rincian `{r}`)" for s, r in p["pembanding"]) or "tidak ada di paket"),
                f"- Jenis: **{p['jenis']}**; tahun beririsan: {', '.join(bersama) or '—'}",
                f"- Dugaan kategori selisih (diuji di Sprint 2): {p['kategori']}", "", "Pertanyaan keterbandingan dan jawabannya:", ""]
        teks += [f"{i}. **{q}** {a}" for i, (q, a) in enumerate(p["pertanyaan"], 1)]
        bagian.append("\n".join(teks))
    daftar = pd.DataFrame(baris)
    n_selisih = int((daftar["jenis"] == "selisih").sum())
    catat(pasangan_rekonsiliasi=n_selisih, pasangan_konteks=int((daftar["jenis"] != "selisih").sum()),
          periode_beririsan=int(daftar.loc[daftar["jenis"] == "selisih", "periode_beririsan"].sum()),
          **{f"irisan_{r.id.lower()}": r.periode_beririsan for r in daftar.itertuples()})
    tulis("pasangan-rekonsiliasi.md", "\n\n".join([
        "# Tabel nasional dan pasangan rekonsiliasi",
        "Dihasilkan `python pipeline.py` (`src/gold/nasional.py`) dari Silver dan `src/konfigurasi.py`. Selisih dihitung "
        "di Sprint 2; Sprint 1 memastikan setiap pasangan memang sebanding dan mencatat tahun yang beririsan.",
        "Tabel nasional (periode x seri, rincian total, tampilan lebar): `reports/tabel-nasional.csv`. "
        "Kolom BPS hanya terisi pada tahun survei; itu bentuk datanya, tidak diisi.",
        "## Ringkasan pasangan", tabel_md(daftar),
        "## Rincian per pasangan", *bagian,
    ]))
    return {"nasional": nas, "pasangan": daftar}


if __name__ == "__main__":
    hasil = jalankan()
    print("Tabel nasional dan pasangan rekonsiliasi selesai disusun.")
    print(hasil["pasangan"].to_string())
