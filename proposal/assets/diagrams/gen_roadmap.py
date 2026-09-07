import sys
sys.path.insert(0, ".")
from helpers import *

c = Canvas(1500, 700)
c.defs_arrowhead(INK4)

c.eyebrow(60, 56, "RENCANA IMPLEMENTASI")
c.text(60, 92, "Peta Jalan Atlas", size=32, family=F_DISPLAY, weight=700, fill=INK)
c.text(60, 118, "Dari MVP yang sudah live hari ini menuju ekosistem kolaborasi yang lebih luas.",
        size=14, family=F_SANS, fill=INK3)

y_line = 350
c.raw(f'<line x1="100" y1="{y_line}" x2="1420" y2="{y_line}" stroke="{LINE_STRONG}" stroke-width="3"/>')

milestones = [
    ("Sekarang", "MVP produksi & self-hostable", "PMO, chat, voice, dokumen real-time, Godmode: berjalan di atlas.creations.ren dengan lisensi AGPL-3.0.", BLUE),
    ("Jangka Pendek", "Validasi pengguna nyata", "Uji coba bersama organisasi kampus & komunitas, penguatan keamanan, egress rekaman panggilan.", GREEN),
    ("Menengah", "Perluasan jangkauan", "Aplikasi mobile, integrasi kalender & email eksternal, laporan analitik proyek.", YELLOW),
    ("Panjang", "Ekosistem terbuka", "Marketplace plugin/integrasi, federasi multi-instance antar organisasi.", RED),
]

n = len(milestones)
xs = [210, 610, 1010, 1310]
for i, (tag, title, desc, color) in enumerate(zip([m[0] for m in milestones], [m[1] for m in milestones], [m[2] for m in milestones], [m[3] for m in milestones])):
    x = xs[i]
    c.raw(f'<circle cx="{x}" cy="{y_line}" r="10" fill="{SURFACE}" stroke="{color}" stroke-width="4"/>')
    above = i % 2 == 0
    box_w = 280
    bx = x - box_w/2
    if above:
        by = y_line - 210
        c.raw(f'<line x1="{x}" y1="{y_line-10}" x2="{x}" y2="{by+150}" stroke="{color}" stroke-width="2"/>')
    else:
        by = y_line + 40
        c.raw(f'<line x1="{x}" y1="{y_line+10}" x2="{x}" y2="{by}" stroke="{color}" stroke-width="2"/>')
    c.rect(bx, by, box_w, 150, fill=SURFACE, stroke=LINE_STRONG, sw=1.5, rx=14)
    c.raw(f'<rect x="{bx}" y="{by}" width="{box_w}" height="6" rx="3" fill="{color}"/>')
    c.eyebrow(bx+20, by+34, tag, color=color)
    c.text(bx+20, by+60, title, size=17, family=F_DISPLAY, weight=700, fill=INK)
    words = desc.split(" ")
    lines, cur, total = [], [], 0
    for w in words:
        if total + len(w) > 34:
            lines.append(" ".join(cur)); cur=[]; total=0
        cur.append(w); total += len(w)+1
    lines.append(" ".join(cur))
    c.wrapped_text(bx+20, by+82, lines[:4], size=12.5, family=F_SANS, fill=INK3, lh=17)

c.save("roadmap.svg")
print("ok")
