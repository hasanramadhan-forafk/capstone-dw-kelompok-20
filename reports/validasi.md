# Hasil Validasi Silver dan Gold

Dihasilkan `python pipeline.py` (`src/validasi/`). Aturan Silver melanjutkan aturan Sprint 1; aturan Gold memeriksa kunci panel, satuan per indikator, ketertelusuran setiap sel ke Silver, serta kategori setiap baris rekonsiliasi berpasangan.

**Ringkasan:** 17 aturan, 16 LOLOS, 0 GAGAL, 1 PERINGATAN.

 tahap                                      aturan              jenis                                                                          keterangan                 hasil
Silver                       keunikan_kunci_primer       keras (umum)                   sumber + seri + wilayah + periode + rincian + berkas tidak kembar                 LOLOS
Silver                          rentang_satuan_sah       keras (umum)                                         persen 0-100; luas dan indeks tidak negatif                 LOLOS
Silver                        satu_satuan_per_seri       keras (umum)                                                   satu seri hanya punya satu satuan                 LOLOS
Silver                            wilayah_kode_sah       keras (umum)                                           kode wilayah dari 38 provinsi 2025 + 9999                 LOLOS
Silver                         kolom_wajib_lengkap       keras (umum)                                         kolom kunci, nilai, dan satuan tidak kosong                 LOLOS
Silver                          luas_tidak_negatif      keras (kasus)                                                              tidak ada luas negatif                 LOLOS
Silver                           komponen_iklh_sah      keras (kasus)                                                                   komponen IKLH sah                 LOLOS
Silver                    konsistensi_lahan_kritis      keras (kasus)                                                      kritis + sangat_kritis = total                 LOLOS
Silver                        deteksi_anomali_2020 peringatan (kasus)                       kolom 2020 tertukar antarprovinsi (sudah dikoreksi di Silver) PERINGATAN (26 baris)
  Gold                      gold: kunci panel unik       keras (gold)                                     indikator + wilayah_kode + periode tidak kembar                 LOLOS
  Gold             gold: satu satuan per indikator       keras (gold)                                        satu indikator panel hanya punya satu satuan                 LOLOS
  Gold                  gold: status sel dan nilai       keras (gold)                           status sel baku; nilai ada jika dan hanya jika sel terisi                 LOLOS
  Gold              gold: sel tertelusur ke Silver       keras (gold) setiap sel terisi punya baris Silver asal (seri, wilayah, periode, rincian, berkas)                 LOLOS
  Gold                   gold: tabel nasional unik       keras (gold)                                               seri + rincian + periode tidak kembar                 LOLOS
  Gold                 rekonsiliasi: kategori baku       keras (gold)                                  kategori dari daftar baku; penjelasan tidak kosong                 LOLOS
  Gold rekonsiliasi: baris berpasangan berkategori       keras (gold)                        setiap baris dengan kedua sisi punya kategori dan penjelasan                 LOLOS
  Gold  rekonsiliasi: selisih = utama - pembanding       keras (gold)                                                    selisih dihitung ulang dan cocok                 LOLOS
