#!/usr/bin/env python3
"""Pesan pengingat BaZi harian siap kirim (WhatsApp/Telegram) untuk Alim.

Isinya mencakup kerjaan & karier, uang, konten, kesehatan, pacar, hubungan,
jam terbaik, lakukan/hindari, dan hari penting 7 hari ke depan.
Tidak butuh internet atau AI: semuanya dihitung dari aturan chart.

Pakai:
    python3 bazi/tools/daily_brief.py              # hari ini (WIB)
    python3 bazi/tools/daily_brief.py 2026-11-08   # tanggal tertentu

Keluaran berupa teks polos dengan format WhatsApp (*tebal*), siap dikirim Mila.
"""
import sys
from datetime import date, datetime, timedelta

from bazi_pillars import (ALIM_BRANCH, COUPLE_BRANCH, EL_B, EL_S, PACAR_BRANCH, PACAR_STEM,
                          SCORE_ALIM, SCORE_PACAR, WIB, pillars, rating)

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
CLASH = {"子": "午", "午": "子", "丑": "未", "未": "丑", "寅": "申", "申": "寅",
         "卯": "酉", "酉": "卯", "辰": "戌", "戌": "辰", "巳": "亥", "亥": "巳"}

KERJA = {
    "甲": "belajar dari mentor & rapikan dokumen, lalu langsung praktikkan.",
    "乙": "riset & susun strategi, tapi pasang batas waktu.",
    "丙": "kolaborasi & networking; jaga gesekan dengan atasan.",
    "丁": "kerja bareng rekan; pertahankan posisi dengan tenang.",
    "戊": "hari berkarya: kirim proposal, pitching, presentasi.",
    "己": "kerja kreatif lancar: bikin konten, produk, atau dokumentasi.",
    "庚": "negosiasi, kirim invoice, ambil keputusan tegas.",
    "辛": "kejar peluang sampingan atau klien baru dengan teliti.",
    "壬": "tugas dari atasan menumpuk; kerjakan yang paling penting dulu.",
    "癸": "tekanan tinggi; fokus menyelesaikan, jangan berdebat.",
}
UANG = {
    "Logam": "hari uang: negosiasi, tagih invoice, cek investasi rutin.",
    "Tanah": "bagus untuk merapikan keuangan, menabung, dan urus pajak.",
    "Api": "rawan boros & ajakan teman; jangan meminjamkan uang.",
    "Air": "uang tersedot ke kewajiban; tahan keputusan besar.",
    "Kayu": "belanja ilmu boleh, asal ada rencana menghasilkan.",
}
KONTEN = {
    "Tanah": "waktunya posting & produksi.",
    "Logam": "bikin konten yang menjual atau penawaran.",
    "Api": "tampil, live, atau kolaborasi.",
    "Kayu": "riset ide & tulis draf.",
    "Air": "jadwalkan konten yang sudah ada; jangan memaksa ide baru.",
}
SEHAT = {
    "Air": "energi cenderung turun: tidur cukup, hangatkan badan, olahraga ringan.",
    "Kayu": "kepala penuh: jalan kaki atau olahraga untuk mengurai pikiran.",
    "Api": "energi tinggi: salurkan ke olahraga, jangan begadang.",
    "Tanah": "jaga pencernaan & makan teratur.",
    "Logam": "jaga napas: kardio ringan & udara segar.",
}
HINDARI_STEM = {
    "甲": "riset tanpa output", "乙": "overthinking", "丙": "meminjamkan uang atau patungan",
    "丁": "ikut-ikutan teman soal uang", "戊": "nada tajam ke atasan", "己": "terlalu santai",
    "庚": "keputusan uang tanpa cek angka", "辛": "tergoda peluang yang terlalu bagus",
    "壬": "menerima tugas tambahan tanpa prioritas", "癸": "debat berat & konfrontasi",
}
HINDARI_BRANCH = {
    "子": "nada sinis; jaga batasan dengan lawan jenis", "酉": "membahas keputusan hubungan",
    "巳": "keputusan besar karena emosi", "申": "terpaku pada rencana; hati-hati di jalan",
    "亥": "begadang & overthinking", "辰": "berasumsi; tanyakan langsung",
    "午": "mempermasalahkan hal kecil", "卯": "mengulang pola lama", "寅": "kebanyakan rencana",
}
JAM = [("辰", "07–09"), ("未", "13–15"), ("申", "15–17"), ("酉", "17–19"), ("戌", "19–21")]
MILESTONES = [
    (date(2028, 10, 8), date(2028, 11, 6), "💍 Jendela lamaran ideal (8 Okt–6 Nov 2028)."),
    (date(2029, 9, 7), date(2029, 10, 7), "⚠️ Puncak ujian hubungan 2029: jangan ambil keputusan hubungan besar."),
    (date(2030, 10, 8), date(2030, 11, 6), "💒 Jendela menikah ideal (8 Okt–6 Nov 2030)."),
    (date(2032, 3, 5), date(2032, 4, 3), "⚠️ Bulan berat 2032: jaga hormat & transparansi."),
    (date(2032, 9, 7), date(2032, 10, 7), "⚠️ Bulan berat 2032: jangan ultimatum."),
    (date(2032, 12, 6), date(2033, 1, 4), "⚠️ Bulan terberat 2032: kurangi pemicu cemburu."),
]


def scores(st: str, br: str) -> tuple:
    sa = SCORE_ALIM[EL_S[st]] + SCORE_ALIM[EL_B[br]]
    sp = SCORE_PACAR[EL_S[st]] + SCORE_PACAR[EL_B[br]]
    if st == "癸" or br in "子酉":
        sa -= 1
    if st == "丁" or br in "申酉子":
        sp -= 1
    return sa, sp


def tag(d: date) -> str:
    _, mp, dp = pillars(d)
    st, br = dp
    tags = []
    if br == "戌":
        tags.append("⭐ hari terbaik kalian")
    if br in "酉子":
        tags.append("⚠️ hubungan sensitif")
    if st in "庚辛":
        tags.append("💰 hari uang")
    if st in "戊己":
        tags.append("🛠️ hari berkarya")
    if st == "癸":
        tags.append("⚠️ tekanan, hindari debat")
    if pillars(d - timedelta(days=1))[1] != mp:
        tags.append(f"🌙 masuk bulan {mp}")
    return ", ".join(tags)


def brief(d: date) -> str:
    yp, mp, dp = pillars(d)
    st, br = dp
    sa, sp = scores(st, br)
    head = f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"
    jam = [j for b, j in JAM if CLASH[br] != b][:2]
    dukung = ("beri ruang & dengarkan, jangan debat." if sp <= -1 else
              "dukung dia tampil/berkarya, jadi penonton pertamanya." if sp >= 1 else
              "beri apresiasi kecil hari ini.")
    hubungan = COUPLE_BRANCH.get(br, "netral, cocok untuk ngobrol santai")
    if st in "丁癸":
        hubungan += "; Day Master kalian bentrok, hindari debat berat"
    hindari = [HINDARI_STEM[st]] + ([HINDARI_BRANCH[br]] if br in HINDARI_BRANCH else [])
    lines = [
        f"*📅 {head}*",
        f"Hari {dp} · Bulan {mp} · Tahun {yp} · energi kamu {rating(sa)}",
        "",
        f"*💼 Kerjaan & karier:* {KERJA[st]}",
        f"*💰 Uang:* {UANG[EL_S[st]]}",
        f"*📣 Konten:* {KONTEN[EL_S[st]]}",
        f"*🫀 Kesehatan:* {SEHAT[EL_B[br]]}",
        f"*🧭 Catatan hari ini:* {ALIM_BRANCH[br]}",
        f"*💛 Dia {rating(sp)}:* {PACAR_STEM[st]}. {PACAR_BRANCH[br]}. Cara dukung: {dukung}",
        f"*🤝 Kalian:* {hubungan}.",
        f"*⏰ Jam terbaik:* {', '.join(jam)} WIB; hindari keputusan besar 21–01.",
        "",
        "*✅ Lakukan:* satu hal kerja sampai selesai, satu langkah kecil untuk keuangan, "
        "dan kirim pesan hangat ke dia.",
        f"*⛔ Hindari:* {'; '.join(hindari)}.",
    ]
    nxt = [f"- {HARI[(d + timedelta(days=i)).weekday()][:3]} {(d + timedelta(days=i)).day} "
           f"({pillars(d + timedelta(days=i))[2]}): {tag(d + timedelta(days=i))}"
           for i in range(1, 7) if tag(d + timedelta(days=i))]
    if nxt:
        lines += ["", "*🔭 6 hari ke depan:*"] + nxt
    for start, end, text in MILESTONES:
        if start - timedelta(days=30) <= d <= end:
            lines += ["", text]
    lines += ["", "_Peta cuaca, bukan takdir._"]
    return "\n".join(lines)


if __name__ == "__main__":
    day = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.now(WIB).date()
    print(brief(day))
