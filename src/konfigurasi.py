"""Keputusan wrangling Kasus 20 — Hutan, lahan, dan lingkungan.

Semua keputusan khas kasus ada di berkas ini supaya mudah ditinjau: identitas seri, satuan luas dan kode
SDG beserta buktinya, cara membaca tabel statis (luas dan persen dipisah), kamus komponen indeks, ambang
anomali, dan pasangan rekonsiliasi. Setiap keputusan juga tercatat di log-keputusan.csv.
Ini salah satu jawaban yang dapat dipertahankan, bukan satu-satunya.
"""

KASUS = 20
SLUG = "hutan-lahan-lingkungan"
JUDUL = "Hutan, lahan, dan lingkungan"

FORMAT_BPS = "json"

LUAS = "tabel:sdg15_tutupan_hutan:luas_ribu_ha"
PERSEN = "tabel:sdg15_tutupan_hutan:persen"
_TH = "tabel statis (HTML) rekalkulasi penutupan lahan 2014–2023; Kalimantan Timur = gabungan dengan Kalimantan Utara (keterangan tabel)"
SERI = {
    LUAS: dict(
        sumber="bps", tingkat="provinsi", nama="Luas penutupan lahan hutan dan non hutan (ribu ha)",
        satuan="ribu_hektar", katalog_satuan="ribu_hektar", bukti_satuan="judul tabel '(Ribu Ha)'; header 'Luas Penutupan Lahan (Ribu Ha)'",
        sdg="15.1.1", katalog_sdg="15.1.1", bukti_sdg="luas hutan = dasar indikator 15.1.1", cakupan=_TH + "; rincian hutan, non hutan, jumlah",
    ),
    PERSEN: dict(
        sumber="bps", tingkat="provinsi", nama="Persentase penutupan lahan hutan dan non hutan",
        satuan="persen", katalog_satuan="persen", bukti_satuan="header '%'",
        sdg="15.1.1", katalog_sdg="15.1.1", bukti_sdg="persentase hutan terhadap luas penutupan lahan", cakupan=_TH + "; rincian hutan, non hutan",
    ),
    "var1304": dict(
        sumber="bps", tingkat="provinsi", nama="Luas penutupan lahan di dalam dan di luar kawasan hutan (ribu ha)",
        satuan="ribu_hektar", katalog_satuan="ribu_hektar", bukti_satuan="var.unit: 'Ribu Hektar'",
        sdg="15.1.1", katalog_sdg="15.3.1",
        bukti_sdg="judul: penutupan lahan menurut status kawasan hutan, bukan lahan terdegradasi (15.3.1)",
        cakupan="rekalkulasi penutupan lahan KLHK 2014–2018, 2023; rincian kawasan hutan, APL, jumlah",
        koreksi="kode SDG 15.3.1 -> 15.1.1 (luas tutupan, bukan degradasi)",
    ),
    "var588": dict(
        sumber="bps", tingkat="provinsi", nama="Luas lahan kritis dan sangat kritis (hektar)",
        satuan="hektar", katalog_satuan="hektar", bukti_satuan="var.unit: 'Hektar'",
        sdg="15.3.1", katalog_sdg="15.3.1", bukti_sdg="lahan kritis = proksi lahan terdegradasi 15.3.1",
        cakupan="review lahan kritis tiap ±5 tahun (var.note): 2006, 2011, 2013, 2018; rincian kritis, sangat kritis, jumlah",
    ),
    "var2532": dict(
        sumber="bps", tingkat="provinsi", nama="Komponen penyusun Indeks Kualitas Lingkungan Hidup (IKLH)",
        satuan="indeks", katalog_satuan="tidak_ada", bukti_satuan="judul 'Indeks'; nilai 0–100",
        sdg="15", katalog_sdg="11.6.2",
        bukti_sdg="nama berkas sdg15_iklh dan judul IKLH (enam komponen); 11.6.2 hanya kualitas udara perkotaan; "
                  "IKLH tidak punya indikator global, dicatat tujuan 15",
        cakupan="enam komponen di turvar; air laut dan gambut hanya provinsi yang punya; KLHK 2019–2024",
        koreksi="satuan tidak_ada -> indeks; kode SDG 11.6.2 -> 15",
    ),
    "AG.LND.FRST.K2": dict(
        sumber="wdi", tingkat="nasional", nama="Forest area (sq. km)", satuan="km2", katalog_satuan="—",
        bukti_satuan="name: '(sq. km)'", sdg="15.1.1", katalog_sdg="—", bukti_sdg="tercantum di metadata/sumber46_indikator.json",
        cakupan="FAO; pohon >= 5 m; tidak termasuk perkebunan (sourceNote)", koreksi="kode SDG kosong -> 15.1.1",
    ),
    "AG.LND.FRST.ZS": dict(
        sumber="wdi", tingkat="nasional", nama="Forest area (% of land area)", satuan="persen", katalog_satuan="—",
        bukti_satuan="name: '(% of land area)'", sdg="15.1.1", katalog_sdg="—", bukti_sdg="tercantum di metadata/sumber46_indikator.json",
        cakupan="penyebut luas daratan", koreksi="kode SDG kosong -> 15.1.1",
    ),
    "EN.ATM.PM25.MC.M3": dict(
        sumber="wdi", tingkat="nasional", nama="PM2.5 air pollution, mean annual exposure (micrograms per cubic meter)",
        satuan="mikrogram_per_m3", katalog_satuan="—", bukti_satuan="name: '(micrograms per cubic meter)'",
        sdg="11.6.2", katalog_sdg="—", bukti_sdg="tercantum di metadata/sumber46_indikator.json",
        cakupan="paparan rata-rata tertimbang penduduk; GBD", koreksi="kode SDG kosong -> 11.6.2",
    ),
}

# K-002: tabel statis dibaca dari HTML; header tahun x tutupan x ukuran; luas dan persen menjadi dua seri
_TABEL = dict(berkas="sdg15_tutupan_hutan", header=("tahun", "tutupan", "ukuran"),
              dimensi={"tutupan": ("tutupan", {})}, total={"jumlah"},
              kamus_header={"ukuran": {"luas_penutupan_lahan_ribu_ha": "luas_ribu_ha", "": "persen", "jumlah": "luas_ribu_ha"}})
TABEL_STATIS = {LUAS: {**_TABEL, "pisah": ("ukuran", "luas_ribu_ha")}, PERSEN: {**_TABEL, "pisah": ("ukuran", "persen")}}

RINCIAN_TOTAL_BPS = {"tidak ada", "jumlah"}
KOMPONEN = {"Indeks Kualitas Air": "ika", "Indeks Kualitas Air Laut (IKAL)": "ikal", "Indeks Kualitas Ekosistem Gambut (IKEG)": "ikeg",
            "Indeks Kualitas Lahan (IKL)": "ikl", "Indeks Kualitas Tutupan Lahan (IKTL)": "iktl", "Indeks Kualitas Udara": "iku"}
RINCIAN_BPS = {
    "var1304": ("kawasan", {"Kawasan Hutan": "kawasan_hutan", "Di Luar Kawasan Hutan/Areal Penggunaan Lain (APL)": "apl"}),
    "var588": ("kekritisan", {"Kritis": "kritis", "Sangat Kritis": "sangat_kritis"}),
    "var2532": ("komponen", KOMPONEN),
}
RINCIAN_TOTAL_WHO = {"TOTAL", ""}
RINCIAN_DIMENSI = {}
RINCIAN_NILAI = {}
KODE_RINCIAN = {"tutupan": {"hutan", "non_hutan"}, "kawasan": {"kawasan_hutan", "apl"},
                "kekritisan": {"kritis", "sangat_kritis"}, "komponen": set(KOMPONEN.values())}

# komponen yang ada di (hampir) semua provinsi; air laut dan gambut hanya sebagian provinsi
DERET = {"var2532": ["komponen=iku", "komponen=ika", "komponen=iktl"], PERSEN: ["tutupan=hutan"]}

RUJUKAN_TAHUN = {}
TIDAK_TERBIT = {("var588", 3100, th): "DKI Jakarta tidak ada di keempat review lahan kritis (2006, 2011, 2013, 2018)"
                for th in ("2006", "2011", "2013", "2018")}
TAHUN_TERBIT = {}

# batas atas = luas daratan Indonesia (±1,9 juta km2 = ±190 ribu ribu ha) dengan kelonggaran
RENTANG = {"persen": (0, 100), "ribu_hektar": (0, 250_000), "hektar": (0, 250_000_000), "indeks": (0, 100),
           "km2": (0, 3_000_000), "mikrogram_per_m3": (0, 500)}

ANOMALI = {"k_iqr": 1.5, "min_titik_samping": 6, "lompat_relatif": 0.20, "porsi_patahan": 0.70}

PASANGAN = [
    dict(id="P1", judul="Luas hutan nasional: BPS (ribu ha) vs WDI (km persegi)",
         utama=LUAS, rincian_utama="tutupan=hutan", pembanding=[("AG.LND.FRST.K2", "total")],
         jenis="selisih", kategori="definisi (tutupan lahan berhutan KLHK vs definisi FAO) setelah satuan diseragamkan (1 ribu ha = 10 km2)",
         alasan_rincian="BPS tutupan=hutan",
         pertanyaan=[("Konversi?", "1 ribu hektar = 10 km persegi; dikerjakan di Gold."),
                     ("Definisi?", "FAO: pohon >= 5 m, tanpa perkebunan (sourceNote); KLHK: kelas penutupan lahan hutan.")]),
    dict(id="P2", judul="Persentase hutan: BPS (terhadap penutupan lahan) vs WDI (terhadap luas daratan)",
         utama=PERSEN, rincian_utama="tutupan=hutan", pembanding=[("AG.LND.FRST.ZS", "total")],
         jenis="selisih", kategori="definisi (penyebut: luas penutupan lahan vs luas daratan)", alasan_rincian="tutupan=hutan",
         pertanyaan=[("Penyebut WDI?", "Luas daratan (name WDI)."), ("Penyebut BPS?", "Jumlah luas penutupan lahan provinsi (tabel).")]),
    dict(id="P3", judul="Indeks kualitas udara (BPS) vs PM2.5 (WDI): konteks",
         utama="var2532", rincian_utama="komponen=iku", pembanding=[("EN.ATM.PM25.MC.M3", "total")],
         jenis="konteks", kategori="arah berlawanan: indeks tinggi = baik, PM2.5 tinggi = buruk", alasan_rincian="komponen udara",
         pertanyaan=[("Arah?", "IKU tinggi berarti udara baik; PM2.5 tinggi berarti buruk.")]),
    dict(id="P4", judul="Kawasan hutan (var1304) vs tutupan hutan (tabel statis): dua tabel KLHK",
         utama="var1304", rincian_utama="total", pembanding=[(LUAS, "total")],
         jenis="selisih", kategori="sumber sama (rekalkulasi KLHK); jumlah luas seharusnya sama", alasan_rincian="rincian jumlah",
         pertanyaan=[("Apa beda keduanya?", "var1304 dipecah menurut status kawasan, tabel statis menurut hutan/non hutan; jumlahnya luas yang sama.")]),
]
