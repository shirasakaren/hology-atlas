import sys, math
sys.path.insert(0, ".")
from helpers import *

c = Canvas(1400, 950)
c.defs_arrowhead(BLUE)

c.eyebrow(60, 56, "METODE PENGEMBANGAN")
c.text(60, 92, "Siklus Iteratif Pengembangan Atlas", size=32, family=F_DISPLAY, weight=700, fill=INK)
c.text(60, 118, "Enam tahap berulang, bukan air terjun satu arah: tiap rilis kembali ke tahap Temukan.",
        size=14, family=F_SANS, fill=INK3)

stages = ["Temukan", "Rancang", "Bangun", "Uji", "Rilis", "Pelajari"]
sub = ["Wawancara & riset kebutuhan", "Wireframe & sistem desain", "Implementasi fitur", "Jest, Playwright, axe-core", "Deploy ke produksi", "Metrik & umpan balik"]

cx, cy, R = 700, 500, 310
n = len(stages)
box_w, box_h = 220, 100
for i, (title, s) in enumerate(zip(stages, sub)):
    angle = -math.pi/2 + i * (2*math.pi/n)
    x = cx + R * math.cos(angle) - box_w/2
    y = cy + R * math.sin(angle) - box_h/2
    accent = [BLUE, GREEN, YELLOW, RED, BLUE, GREEN][i]
    tint = [BLUE_50, GREEN_50, YELLOW_50, RED_50, BLUE_50, GREEN_50][i]
    c.node(x, y, box_w, box_h, f"{i+1}. {title}", [s], accent=accent, accent_tint=tint)

# connecting arrows along the circle
def rect_edge_point(bx, by, half_w, half_h, theta):
    """Point on the boundary of an axis-aligned rectangle centered at
    (bx,by), travelling from its own center along angle theta - always
    lands exactly on the box outline, regardless of approach angle."""
    dx, dy = math.cos(theta), math.sin(theta)
    tx = abs(half_w / dx) if abs(dx) > 1e-9 else float('inf')
    ty = abs(half_h / dy) if abs(dy) > 1e-9 else float('inf')
    t = min(tx, ty)
    return bx + t * dx, by + t * dy

gap = 8
bulge = 32
for i in range(n):
    a1 = -math.pi/2 + i * (2*math.pi/n)
    a2 = -math.pi/2 + (i+1) * (2*math.pi/n)
    bx1, by1 = cx + R*math.cos(a1), cy + R*math.sin(a1)
    bx2, by2 = cx + R*math.cos(a2), cy + R*math.sin(a2)
    dir_out = math.atan2(by2 - by1, bx2 - bx1)
    dir_in = math.atan2(by1 - by2, bx1 - bx2)
    x1, y1 = rect_edge_point(bx1, by1, box_w/2 + gap, box_h/2 + gap, dir_out)
    x2, y2 = rect_edge_point(bx2, by2, box_w/2 + gap, box_h/2 + gap, dir_in)
    midx, midy = (x1+x2)/2, (y1+y2)/2
    mdx, mdy = midx - cx, midy - cy
    mdlen = math.hypot(mdx, mdy) or 1
    ctrl_x = midx + mdx/mdlen*bulge
    ctrl_y = midy + mdy/mdlen*bulge
    c.raw(f'<path d="M {x1:.0f} {y1:.0f} Q {ctrl_x:.0f} {ctrl_y:.0f} {x2:.0f} {y2:.0f}" '
          f'fill="none" stroke="{INK4}" stroke-width="2" marker-end="url(#arrowhead)"/>')

c.text(cx, cy+8, "ATLAS", size=22, family=F_DISPLAY, weight=700, fill=INK4, anchor="middle")

c.save("metode-cycle.svg")
print("ok")
