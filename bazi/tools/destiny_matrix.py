#!/usr/bin/env python3
"""Destiny Matrix (metode Natalia Ladini, 22 Arcana Mayor) - kalkulator sederhana.

Pakai:
    python destiny_matrix.py 1995-12-02                # satu orang
    python destiny_matrix.py 1995-12-02 1998-08-24     # + titik utama matriks pasangan

Rumus sama dengan matrix-destiny.com (sudah dicek terhadap screenshot matriks Alim).
Titik pasangan memakai metode penjumlahan titik-per-titik; metode antar situs bisa beda.
"""
import sys
from datetime import date

ARCANA = {
    1: "Magician", 2: "High Priestess", 3: "Empress", 4: "Emperor", 5: "Hierophant",
    6: "Lovers", 7: "Chariot", 8: "Justice", 9: "Hermit", 10: "Wheel of Fortune",
    11: "Strength", 12: "Hanged Man", 13: "Death", 14: "Temperance", 15: "Devil",
    16: "Tower", 17: "Star", 18: "Moon", 19: "Sun", 20: "Judgement", 21: "World", 22: "Fool",
}


def r(n: int) -> int:
    """Reduksi ke 1..22 dengan menjumlahkan digit."""
    while n > 22:
        n = sum(int(d) for d in str(n))
    return n


def matrix(d: date) -> dict:
    A = r(d.day)
    B = r(d.month)
    C = r(sum(int(x) for x in str(d.year)))
    D = r(A + B + C)
    E = r(A + B + C + D)
    F, G, H, I = r(A + B), r(B + C), r(C + D), r(D + A)
    E2 = r(F + G + H + I)  # pusat kotak leluhur
    m = dict(A=A, B=B, C=C, D=D, E=E, F=F, G=G, H=H, I=I, E2=E2)
    m["A1"] = r(A + E); m["A2"] = r(A + m["A1"]); m["A3"] = r(m["A1"] + E)
    m["B1"] = r(B + E); m["B2"] = r(B + m["B1"]); m["B3"] = r(m["B1"] + E)
    m["C1"] = r(C + E); m["C2"] = r(C + m["C1"])
    m["D1"] = r(D + E); m["D2"] = r(D + m["D1"])
    m["X"] = r(m["C1"] + m["D1"])
    m["money"] = r(m["X"] + m["C1"])
    m["love"] = r(m["X"] + m["D1"])
    for k in "FGHI":
        m[k + "_in"] = r(m[k] + E2)
        m[k + "_mid"] = r(m[k] + m[k + "_in"])
    sky, earth = r(B + D), r(A + C)
    personal = r(sky + earth)
    male, female = r(F + H), r(G + I)
    social = r(male + female)
    spiritual = r(personal + social)
    planetary = r(social + spiritual)
    m.update(sky=sky, earth=earth, personal=personal, male=male, female=female,
             social=social, spiritual=spiritual, planetary=planetary)
    m["karmic_tail"] = (m["D1"], m["D2"], D)
    rows = [("Sahasrara", A, B), ("Ajna", m["A2"], m["B2"]), ("Vishuddha", m["A1"], m["B1"]),
            ("Anahata", m["A3"], m["B3"]), ("Manipura", E, E),
            ("Svadhisthana", m["C1"], m["D1"]), ("Muladhara", C, D)]
    m["chakras"] = [(n, p, e, r(p + e)) for n, p, e in rows]
    tp = r(sum(c[1] for c in m["chakras"]))
    te = r(sum(c[2] for c in m["chakras"]))
    m["chakra_total"] = (tp, te, r(tp + te))
    return m


def ring(m: dict) -> list:
    """Cincin usia 0-80 tahun: (usia, arcana) tiap 1.25 tahun."""
    pts = [(0, m["A"]), (10, m["F"]), (20, m["B"]), (30, m["G"]), (40, m["C"]),
           (50, m["H"]), (60, m["D"]), (70, m["I"]), (80, m["A"])]
    out = []
    for (a0, v0), (_, v1) in zip(pts, pts[1:]):
        mid = r(v0 + v1)
        q1, q3 = r(v0 + mid), r(mid + v1)
        out += [(a0, v0), (a0 + 1.25, r(v0 + q1)), (a0 + 2.5, q1), (a0 + 3.75, r(q1 + mid)),
                (a0 + 5, mid), (a0 + 6.25, r(mid + q3)), (a0 + 7.5, q3), (a0 + 8.75, r(q3 + v1))]
    return out


def add_years(d: date, years: float) -> str:
    months = round(years * 12)
    y, mo = divmod(d.month - 1 + months, 12)
    return f"{d.year + y}-{mo + 1:02d}"


def name(n: int) -> str:
    return f"{n} {ARCANA[n]}"


def show(d: date) -> dict:
    m = matrix(d)
    print(f"\n=== Destiny Matrix {d.isoformat()} ===")
    for k, label in [("A", "Potret diri (kiri, 0 th)"), ("B", "Bakat (atas, 20 th)"),
                     ("C", "Materi (kanan, 40 th)"), ("D", "Ekor karma (bawah, 60 th)"),
                     ("E", "Inti / zona nyaman (pusat)")]:
        print(f"{label:32s}: {name(m[k])}")
    print(f"Leluhur F/G/H/I               : {m['F']} / {m['G']} / {m['H']} / {m['I']} (pusat leluhur {m['E2']})")
    print(f"Garis ayah (F+H) / ibu (G+I)  : {name(m['male'])} / {name(m['female'])}")
    print(f"Langit / Bumi                 : {name(m['sky'])} / {name(m['earth'])}")
    print(f"Tujuan pribadi (20-40)        : {name(m['personal'])}")
    print(f"Tujuan sosial (40-60)         : {name(m['social'])}")
    print(f"Tujuan spiritual              : {name(m['spiritual'])}")
    print(f"Tujuan planet                 : {name(m['planetary'])}")
    print(f"Bakat (B, B2, B1)             : {m['B']} - {m['B2']} - {m['B1']}")
    print(f"Uang: $={m['money']}  pintu C1={m['C1']}  C2={m['C2']}  X={m['X']}")
    print(f"Cinta: hati={m['love']}  pintu D1={m['D1']}  D2={m['D2']}  X={m['X']}")
    print(f"Ekor karma (D1-D2-D)          : {'-'.join(map(str, m['karmic_tail']))}")
    print("Cakra (fisik, energi, emosi):")
    for n, p, e, s in m["chakras"]:
        print(f"  {n:13s} {p:2d} {e:2d} {s:2d}")
    print(f"  {'TOTAL':13s} {m['chakra_total'][0]:2d} {m['chakra_total'][1]:2d} {m['chakra_total'][2]:2d}")
    print("Cincin usia (usia -> kira-kira bulan, arcana):")
    for age, v in ring(m):
        if age <= 70:
            print(f"  {age:5.2f} ~{add_years(d, age)}  {name(v)}")
    return m


def couple(m1: dict, m2: dict) -> None:
    print("\n=== Titik utama matriks pasangan (penjumlahan titik-per-titik) ===")
    for k, label in [("A", "Wajah pasangan"), ("B", "Tujuan bersama"), ("C", "Materi bersama"),
                     ("D", "Fondasi/karma bersama"), ("E", "Inti/zona nyaman pasangan")]:
        print(f"{label:28s}: {name(r(m1[k] + m2[k]))}")
    for k, label in [("money", "Titik uang (gabungan)"), ("love", "Titik cinta (gabungan)")]:
        print(f"{label:28s}: {name(r(m1[k] + m2[k]))}  [{m1[k]} + {m2[k]}]")


if __name__ == "__main__":
    dates = [date.fromisoformat(a) for a in sys.argv[1:]] or [date(1995, 12, 2)]
    ms = [show(d) for d in dates]
    if len(ms) == 2:
        couple(*ms)
