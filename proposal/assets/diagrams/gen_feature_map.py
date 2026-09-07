import sys
sys.path.insert(0, ".")
from helpers import *

c = Canvas(1400, 760)
c.defs_arrowhead(INK4)

c.eyebrow(60, 56, "FITUR APLIKASI")
c.text(60, 92, "Peta Modul Atlas", size=32, family=F_DISPLAY, weight=700, fill=INK)
c.text(60, 118, "Satu ruang kerja, tujuh modul — semuanya berjalan di satu instance yang Anda kendalikan penuh.",
        size=14, family=F_SANS, fill=INK3)

items = [
    ("Dashboard", "Ringkasan lintas proyek & tugas untuk Anda", icon_grid, BLUE, BLUE_50),
    ("PMO", "Kanban, list, timeline, catatan, whiteboard, berkas", icon_server, GREEN, GREEN_50),
    ("Chat", "Kanal per proyek + kanal lintas workspace", icon_chat, YELLOW, YELLOW_50),
    ("Voice", "Panggilan suara WebRTC, screen-share, moderasi", icon_voice, RED, RED_50),
    ("Dokumen Real-time", "Catatan & whiteboard kolaboratif berbasis Yjs", icon_grid, GREEN, GREEN_50),
    ("Godmode", "Panel kendali self-host: auth, tema, storage, modul", icon_shield, BLUE, BLUE_50),
    ("Admin Console", "Tag, role kolaborasi, sticker, feature flag", icon_db, INK2, SURFACE_MUTED),
]

cols = 4
cw, ch, gx, gy = 300, 200, 26, 26
x0, y0 = 60, 190
for i, (title, desc, icon, accent, tint) in enumerate(items):
    col = i % cols
    row = i // cols
    x = x0 + col * (cw + gx)
    y = y0 + row * (ch + gy)
    c.rect(x, y, cw, ch, fill=SURFACE, stroke=LINE_STRONG, sw=1.5, rx=16)
    c.raw(f'<circle cx="{x+34}" cy="{y+34}" r="22" fill="{tint}"/>')
    icon(c, x + 20, y + 20, s=28, color=accent)
    c.text(x + 24, y + 92, title, size=19, family=F_DISPLAY, weight=700, fill=INK)
    # wrap desc into two lines manually at ~28 chars
    words = desc.split(" ")
    l1, l2 = [], []
    cur = l1
    total = 0
    for w in words:
        if total + len(w) > 26 and cur is l1:
            cur = l2
            total = 0
        cur.append(w)
        total += len(w) + 1
    c.text(x + 24, y + 118, " ".join(l1), size=13.5, family=F_SANS, fill=INK3)
    if l2:
        c.text(x + 24, y + 138, " ".join(l2), size=13.5, family=F_SANS, fill=INK3)

c.save("feature-map.svg")
print("ok")
