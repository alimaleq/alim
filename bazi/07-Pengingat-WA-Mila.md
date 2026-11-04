---
title: Pengingat BaZi lewat WhatsApp (Mila)
tags: [bazi, pengingat, mila]
updated: 2026-11-04
---

# Pengingat BaZi lewat WhatsApp (Mila)

Tujuan: setiap pagi Mila mengirim pengingat BaZi harian ke WhatsApp Alim, selain yang muncul di sesi Claude Code "📅 Saran BaZi Harian". Lihat juga [[00-Index]] dan [[05-Rencana-Aksi]].

## Isi pesan

Dibuat oleh `bazi/tools/daily_brief.py`. Script ini tidak butuh internet atau AI; semuanya dihitung dari aturan chart. Isinya:

- kerjaan & karier, uang, konten, kesehatan;
- energi pacar dan cara mendukungnya;
- hubungan kalian;
- jam terbaik untuk kerja/keputusan;
- lakukan & hindari;
- hari penting 6 hari ke depan (hari terbaik, hari sensitif, hari uang, ganti bulan);
- pengingat jendela penting (lamaran 2028, ujian 2029, nikah 2030, bulan-bulan berat 2032).

Contoh:

```bash
python3 bazi/tools/daily_brief.py 2026-11-05
```

## Cara Mila mengirim (tiap hari ±05.45 WIB)

1. `git -C <folder-repo-alim> pull` (branch `claude/bazi-notes`)
2. `python3 <folder-repo-alim>/bazi/tools/daily_brief.py`
3. Kirim seluruh keluaran ke WhatsApp Alim apa adanya (format *tebal* WhatsApp sudah disiapkan).

## Instruksi siap tempel untuk Mila

> Mila, setiap hari jam 05.45 WIB: buka folder repo `alim`, jalankan `git pull`, lalu jalankan `python3 bazi/tools/daily_brief.py`. Kirim seluruh hasilnya ke WhatsApp aku apa adanya. Kalau perintahnya gagal, kirim pesan singkat bahwa pengingat hari ini gagal dibuat.

## Instruksi untuk Claude di komputer tempat OpenClaw (Mila) berjalan

Tempel teks ini ke Claude Code atau Claude desktop di komputer itu:

```text
Tolong atur Mila (agent OpenClaw aku) supaya tiap pagi mengirim pengingat BaZi harian ke WhatsApp aku.

Sumber data: repo GitHub alimaleq/alim, branch claude/bazi-notes. Script bazi/tools/daily_brief.py (Python 3, tanpa dependency) menghasilkan pesan siap kirim. Detail ada di bazi/07-Pengingat-WA-Mila.md dan CLAUDE.md.

Langkah:
1. Clone repo itu ke ~/alim (atau git pull kalau sudah ada). Pakai akses GitHub yang sudah ada di komputer ini.
2. Tes: cd ~/alim && python3 bazi/tools/daily_brief.py, pastikan pesannya keluar.
3. Cek cara OpenClaw di komputer ini membuat tugas terjadwal (cron) dan mengirim pesan WhatsApp (lihat dokumentasi, CLI, atau config OpenClaw yang terpasang). Buat jadwal harian jam 05:45 zona Asia/Jakarta yang:
   a. menjalankan git -C ~/alim pull --ff-only
   b. menjalankan python3 ~/alim/bazi/tools/daily_brief.py
   c. mengirim seluruh hasilnya apa adanya ke WhatsApp aku (nomor pemilik yang sudah terdaftar di Mila)
   d. kalau ada langkah yang gagal, mengirim pesan singkat ke aku bahwa pengingat hari ini gagal, plus alasannya.
4. Tambahkan ke memori/instruksi Mila: catatan BaZi aku ada di ~/alim (CLAUDE.md dan folder bazi/). Kalau aku tanya soal BaZi, tanggal baik, atau pengingat, Mila boleh membaca file itu dan menjalankan python3 ~/alim/bazi/tools/bazi_pillars.py <tanggal>. Hanya baca: jangan ubah atau commit apa pun.
5. Kirim satu pesan tes ke WhatsApp aku sekarang.
6. Laporkan ke aku: jadwal yang dibuat (jam dan perintahnya), lokasi repo, dan cara mengubah atau mematikannya.

Batasan: jangan ubah atau commit isi repo dari komputer ini; jangan kirim ke nomor lain atau grup; jangan bagikan isi catatan ke siapa pun.
```

## Kalau mau update nanti

- **Bacaan atau catatan baru:** cukup diperbarui di repo (lewat Claude cloud). Mila otomatis ikut, karena tiap pagi menjalankan `git pull` dulu.
- **Ganti jam atau isi pesan:** bilang ke Claude di komputer itu, misalnya "Ubah jadwal pengingat BaZi Mila jadi jam 06.30" atau "Tambahkan bagian X ke pengingat Mila".

## Status

- **Belum tersambung.** Sesi cloud Claude tidak punya akses WhatsApp, dan belum ada folder komputer yang dibagikan lewat Remote Control.
- Cara menyambungkan, pilih salah satu:
  1. Bagikan folder tempat Mila berjalan lewat Remote Control di komputer itu (aplikasi Claude desktop: Settings → Claude Code → Remote Control, atau jalankan `claude remote-control` di folder itu). Setelah itu Claude bisa memasang jadwalnya langsung.
  2. Tempel instruksi di atas ke Mila sendiri.
