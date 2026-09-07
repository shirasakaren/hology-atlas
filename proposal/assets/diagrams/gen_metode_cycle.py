import sys, math
sys.path.insert(0, ".")
from helpers import *

c = Canvas(1400, 760)
c.defs_arrowhead(BLUE)

c.eyebrow(60, 56, "METODE PENGEMBANGAN")
c.text(60, 92, "Siklus Iteratif Pengembangan Atlas", size=32, family=F_DISPLAY, weight=700, fill=INK)
c.text(60, 118, "Enam tahap berulang, bukan air terjun satu arah — tiap rilis kembali ke tahap Temukan.",
        size=14, family=F_SANS, fill=INK3)

stages = ["Temukan", "Rancang", "Bangun", "Uji", "Rilis", "Pelajari"]
sub = ["Wawancara & riset kebutuhan", "Wireframe & sistem desain", "Implementasi fitur", "Jest, Playwright, axe-core", "Deploy ke produksi", "Metrik & umpan balik"]

cx, cy, R = 700, 440, 260
n = len(stages)
box_w, box_h = 230, 110
for i, (title, s) in enumerate(zip(stages, sub)):
    angle = -math.pi/2 + i * (2*math.pi/n)
    x = cx + R * math.cos(angle) - box_w/2
    y = cy + R * math.sin(angle) - box_h/2
    accent = [BLUE, GREEN, YELLOW, RED, BLUE, GREEN][i]
    tint = [BLUE_50, GREEN_50, YELLOW_50, RED_50, BLUE_50, GREEN_50][i]
    c.node(x, y, box_w, box_h, f"{i+1}. {title}", [s], accent=accent, accent_tint=tint)

# connecting arrows along the circle
for i in range(n):
    a1 = -math.pi/2 + i * (2*math.pi/n)
    a2 = -math.pi/2 + (i+1) * (2*math.pi/n)
    r0 = R + 5
    x1 = cx + (R+ (box_h/2)+2) * math.cos(a1 + 0.35)
    y1 = cy + (R+ (box_h/2)+2) * math.sin(a1 + 0.35)
    x2 = cx + (R+ (box_h/2)+2) * math.cos(a2 - 0.35)
    y2 = cy + (R+ (box_h/2)+2) * math.sin(a2 - 0.35)
    mid_a = (a1+a2)/2
    curvex = (R+90) * math.cos(mid_a) - (cx + R*math.cos(mid_a))
    curvey = (R+90) * math.sin(mid_a) - (cy + R*math.sin(mid_a))
    c.raw(f'<path d="M {x1:.0f} {y1:.0f} Q {cx + (R+70)*math.cos(mid_a):.0f} {cy + (R+70)*math.sin(mid_a):.0f} {x2:.0f} {y2:.0f}" '
          f'fill="none" stroke="{INK4}" stroke-width="2" marker-end="url(#arrowhead)"/>')

c.text(cx, cy+8, "ATLAS", size=22, family=F_DISPLAY, weight=700, fill=INK4, anchor="middle")

c.save("metode-cycle.svg")
print("ok")
