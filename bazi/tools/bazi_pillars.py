#!/usr/bin/env python3
"""Pilar BaZi (tahun / bulan / hari) untuk tanggal tertentu + catatan singkat
untuk Alim (丁卯, cowok) dan pacarnya (癸卯, cewek).

Pakai:
    python bazi_pillars.py              # hari ini (WIB)
    python bazi_pillars.py 2027-06-10   # tanggal tertentu
    python bazi_pillars.py 2027-06-10 7 # tujuh hari mulai tanggal itu

Cara hitung:
- Pilar hari: 1949-10-01 adalah hari 甲子 (siklus 60 hari).
- Pilar bulan/tahun: berdasarkan bujur matahari (rumus Meeus, akurasi ~menit),
  tahun BaZi berganti di 立春 (bujur 315°), bulan berganti tiap 30°.
"""
import math
import sys
from datetime import date, datetime, timedelta, timezone

S = "甲乙丙丁戊己庚辛壬癸"
B = "子丑寅卯辰巳午未申酉戌亥"
EL_S = {"甲": "Kayu", "乙": "Kayu", "丙": "Api", "丁": "Api", "戊": "Tanah", "己": "Tanah",
        "庚": "Logam", "辛": "Logam", "壬": "Air", "癸": "Air"}
EL_B = {"子": "Air", "丑": "Tanah", "寅": "Kayu", "卯": "Kayu", "辰": "Tanah", "巳": "Api",
        "午": "Api", "未": "Tanah", "申": "Logam", "酉": "Logam", "戌": "Tanah", "亥": "Air"}
WIB = timezone(timedelta(hours=7))

# ---- skor elemen (positif = mendukung) ----
SCORE_ALIM = {"Tanah": 1, "Logam": 1, "Api": 0.5, "Kayu": -0.5, "Air": -1}
SCORE_PACAR = {"Api": 1, "Kayu": 1, "Tanah": -0.5, "Logam": -1, "Air": -1}

ALIM_STEM = {
    "甲": "mentor/dukungan (正印): belajar lalu langsung praktik",
    "乙": "intuisi & riset (偏印): awas overthinking",
    "丙": "劫財: kompetisi & godaan boros; 丙壬沖 = gesekan dengan atasan",
    "丁": "比肩: rekan/saingan; jaga uang dari ajakan teman",
    "戊": "傷官 (Tanah = 用神): berkarya, bicara, jualan; jangan konfrontasi atasan",
    "己": "食神 (Tanah = 用神): konten, kreativitas, menikmati hidup",
    "庚": "正財 (Logam): uang, negosiasi, keputusan tegas; bintang istri",
    "辛": "偏財: uang sampingan & peluang; jaga batas dari godaan",
    "壬": "正官 (丁壬合): komitmen & tanggung jawab kerja menumpuk",
    "癸": "七殺, 丁癸沖: tekanan & konflik; jangan debat berat",
}
ALIM_BRANCH = {
    "子": "子卯刑 + 桃花: gesekan di rumah & perhatian dari luar; jaga nada dan batasan",
    "丑": "財庫: bagus untuk membereskan keuangan & tabungan",
    "寅": "Kayu (寅亥合): banyak ide/belajar, jangan sampai cuma mikir",
    "卯": "istana pasangan 伏吟: pola lama muncul lagi; sabar",
    "辰": "output bagus (傷官) tapi 卯辰害: rawan salah paham",
    "巳": "巳亥沖 + 驛馬: gerak/perubahan/perjalanan; jangan putuskan hal besar karena emosi",
    "午": "祿: percaya diri tinggi; 卯午破: retak kecil, beri apresiasi",
    "未": "卯未 + 紅艷: hangat & memesona; bagus untuk kencan",
    "申": "Logam (bintang istri/uang) + 卯申暗合; 寅申沖: rencana bisa berubah",
    "酉": "天乙 + 文昌 (bantuan & belajar, uang sampingan) TAPI 卯酉沖: hubungan sensitif",
    "戌": "卯戌合: harmoni hubungan; Tanah = berkarya lancar",
    "亥": "天乙, tapi 亥亥 self-punishment: overthinking malam; jangan menyendiri",
}
PACAR_STEM = {
    "甲": "傷官 (傷官見官): ide besar & berani tampil, tapi lidah tajam",
    "乙": "食神: kreatif, konten, menikmati; 乙庚合 = terikat urusan keluarga",
    "丙": "正財 (用神): uang & peluang",
    "丁": "偏財 tapi 丁癸沖: intens; jangan belanja/debat impulsif",
    "戊": "正官, 戊癸合: komitmen/ikatan, banyak tuntutan",
    "己": "七殺: tekanan; 甲己合 = bakatnya menaklukkan tekanan",
    "庚": "正印 (Logam): dukungan tapi terasa berat/kaku",
    "辛": "偏印: overthinking, intuisi",
    "壬": "劫財: uang bocor ke teman, saingan",
    "癸": "比肩: ego naik; 戊癸 爭合 = rasa bersaing",
}
PACAR_BRANCH = {
    "子": "子卯刑 + 桃花: emosi naik & gesekan; jangan umbar urusan pribadi",
    "丑": "energi rendah (七殺/Logam): istirahat",
    "寅": "傷官: kreatif & bergerak; 寅申沖 = hati-hati di jalan",
    "卯": "桃花 + 伏吟: pesona tinggi, perasaan sensitif",
    "辰": "得龍而運: momentum ide; 卯辰害 = salah paham",
    "巳": "天乙 + uang (正財); 三刑: teliti kontrak & kesehatan",
    "午": "uang & visibilitas (寅午); 卯午破 = retak kecil",
    "未": "卯未: hangat; 華蓋 = butuh waktu sendiri",
    "申": "伏吟 bulan + 寅申沖 + 紅艷: gejolak, biaya, hati-hati di jalan",
    "酉": "卯酉沖 + Logam: mood turun, hubungan sensitif",
    "戌": "卯戌合 + 財庫: harmoni, menabung",
    "亥": "寅亥合/亥卯: kreatif & produktif; 申亥害 = gesekan keluarga/kerja",
}
COUPLE_BRANCH = {
    "戌": "HARI BAIK hubungan (卯戌合 untuk kalian berdua): kencan, obrolan serius, rujuk",
    "未": "hangat (卯未)", "亥": "hangat (亥卯)", "申": "ikatan diam-diam (卯申暗合)",
    "酉": "SENSITIF (卯酉沖 kalian berdua): hindari debat & keputusan hubungan",
    "子": "SENSITIF (子卯刑 + 桃花 kalian berdua): jaga nada, transparan",
    "辰": "rawan salah paham (卯辰害): bicara terang",
    "午": "retak kecil (卯午破): beri apresiasi",
    "卯": "pola lama muncul (伏吟): sabar",
}


def jd(dt: datetime) -> float:
    dt = dt.astimezone(timezone.utc)
    y, m = dt.year, dt.month
    D = dt.day + (dt.hour + dt.minute / 60) / 24
    if m <= 2:
        y -= 1
        m += 12
    a = y // 100
    b = 2 - a + a // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + D + b - 1524.5


def sun_lon(dt: datetime) -> float:
    t = (jd(dt) - 2451545.0) / 36525
    l0 = 280.46646 + 36000.76983 * t + 0.0003032 * t * t
    mm = math.radians(357.52911 + 35999.05029 * t - 0.0001537 * t * t)
    c = ((1.914602 - 0.004817 * t - 0.000014 * t * t) * math.sin(mm)
         + (0.019993 - 0.000101 * t) * math.sin(2 * mm) + 0.000289 * math.sin(3 * mm))
    om = math.radians(125.04 - 1934.136 * t)
    return (l0 + c - 0.00569 - 0.00478 * math.sin(om)) % 360


def pillars(d: date) -> tuple:
    noon = datetime(d.year, d.month, d.day, 12, tzinfo=WIB)
    lon = sun_lon(noon)
    month_idx = int(((lon - 315) % 360) // 30)          # 0 = 寅
    # tahun BaZi: sebelum 立春 masih tahun sebelumnya
    by = d.year if (d.month > 2 or month_idx < 10) else d.year - 1
    if d.month <= 2 and month_idx >= 10:
        by = d.year - 1
    ys = (by - 1984) % 10
    year_p = S[ys] + B[(by - 1984) % 12]
    first = {0: 2, 5: 2, 1: 4, 6: 4, 2: 6, 7: 6, 3: 8, 8: 8, 4: 0, 9: 0}[ys]
    month_p = S[(first + month_idx) % 10] + B[(2 + month_idx) % 12]
    n = (d - date(1949, 10, 1)).days % 60
    day_p = S[n % 10] + B[n % 12]
    return year_p, month_p, day_p


def rating(score: float) -> str:
    return "🟢" if score >= 1 else ("🔴" if score <= -1 else "🟡")


def report(d: date) -> None:
    yp, mp, dp = pillars(d)
    st, br = dp[0], dp[1]
    sa = SCORE_ALIM[EL_S[st]] + SCORE_ALIM[EL_B[br]]
    sp = SCORE_PACAR[EL_S[st]] + SCORE_PACAR[EL_B[br]]
    if st == "癸" or br in "子酉":
        sa -= 1
    if st == "丁" or br in "申酉子":
        sp -= 1
    print(f"{d.isoformat()}  tahun {yp} · bulan {mp} · hari {dp} ({EL_S[st]}/{EL_B[br]})")
    print(f"  Alim  {rating(sa)} {ALIM_STEM[st]} | {ALIM_BRANCH[br]}")
    print(f"  Pacar {rating(sp)} {PACAR_STEM[st]} | {PACAR_BRANCH[br]}")
    note = COUPLE_BRANCH.get(br, "netral")
    if st in "丁癸":
        note += " · DM kalian (丁 vs 癸) bentrok diperkuat: hindari debat berat"
    print(f"  Kalian: {note}")


if __name__ == "__main__":
    start = (date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1
             else datetime.now(WIB).date())
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    for i in range(days):
        report(start + timedelta(days=i))
