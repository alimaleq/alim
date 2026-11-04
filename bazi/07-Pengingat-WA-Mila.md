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

## Status

- **Belum tersambung.** Sesi cloud Claude tidak punya akses WhatsApp, dan belum ada folder komputer yang dibagikan lewat Remote Control.
- Cara menyambungkan, pilih salah satu:
  1. Bagikan folder tempat Mila berjalan lewat Remote Control di komputer itu (aplikasi Claude desktop: Settings → Claude Code → Remote Control, atau jalankan `claude remote-control` di folder itu). Setelah itu Claude bisa memasang jadwalnya langsung.
  2. Tempel instruksi di atas ke Mila sendiri.
