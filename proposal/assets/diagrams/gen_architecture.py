import sys
sys.path.insert(0, ".")
from helpers import *

c = Canvas(1400, 820)
c.defs_arrowhead(INK4)

c.eyebrow(60, 56, "ARSITEKTUR SISTEM")
c.text(60, 92, "Arsitektur Atlas", size=32, family=F_DISPLAY, weight=700, fill=INK)

# Tier 1: browser
bx, by, bw, bh = 560, 130, 280, 90
c.node(bx, by, bw, bh, "Browser Pengguna", ["Next.js client, tanpa cookie"], mono="localStorage: sesi", accent=BLUE, accent_tint=BLUE_50, icon=icon_browser)

# Tier 2: frontend / livekit / yjs
fy = 280
c.node(560, fy, 280, 110, "Frontend", ["Next.js 15 (App Router)", "Render UI + panggilan REST"], mono="pnpm apps/frontend", accent=BLUE, accent_tint=BLUE_50, icon=icon_server)
c.node(140, fy, 300, 110, "y-websocket", ["Relay sinkronisasi Yjs (CRDT)", "Catatan & whiteboard real-time"], mono="ws — realtime docs", accent=GREEN, accent_tint=GREEN_50, icon=icon_grid)
c.node(960, fy, 300, 110, "LiveKit SFU + Egress", ["Media WebRTC suara/panggilan", "Egress: rekaman opsional"], mono="webrtc — voice", accent=RED, accent_tint=RED_50, icon=icon_voice)

# Tier 3: backend
by3 = 450
c.node(560, by3, 280, 100, "Backend", ["NestJS 10, REST /api/v1", "Validasi sesi tiap permintaan"], mono="Bearer <sessionId>", accent=BLUE, accent_tint=BLUE_50, icon=icon_shield)

# Tier 4: data/infra
dy = 620
c.node(140, dy, 250, 110, "PostgreSQL", ["Sumber kebenaran utama", "Terkelola oleh Railway"], mono="Prisma ORM", accent=GREEN, accent_tint=GREEN_50, icon=icon_db)
c.node(420, dy, 250, 110, "Redis", ["Cache & rate limiting", "Siap untuk multi-replika"], mono="infra/redis", accent=GREEN, accent_tint=GREEN_50, icon=icon_db)
c.node(700, dy, 250, 110, "Penyimpanan Berkas", ["Lokal / S3 / R2", "Dipilih lewat Godmode"], mono="avatar, lampiran", accent=GREEN, accent_tint=GREEN_50, icon=icon_cloud)
c.node(980, dy, 280, 110, "LiveKit Control Plane", ["Penerbitan token & webhook", "Dari backend, bukan browser"], mono="server-to-server", accent=RED, accent_tint=RED_50, icon=icon_shield)

# arrows: browser -> frontend / yjs / livekit
c.arrow(bx+40, by+bh, 700, fy, color=BLUE, label="HTTPS")
c.arrow(bx+10, by+bh, 380, fy, color=GREEN, label="WebSocket")
c.arrow(bx+bw-10, by+bh, 1080, fy, color=RED, label="WebRTC")

# frontend -> backend
c.arrow(700, fy+110, 700, by3, color=BLUE, label="REST")

# backend -> data/infra
c.arrow(640, by3+100, 265, dy, color=INK3, label="SQL")
c.arrow(660, by3+100, 545, dy, color=INK3, label="cache")
c.arrow(720, by3+100, 825, dy, color=INK3, label="upload")
c.arrow(760, by3+100, 1090, dy, color=INK3, label="token", dashed=True)

c.text(700, 810, "Backend hanya menjadi jembatan kontrol; media suara dan sinkronisasi dokumen mengalir langsung antara browser dan sidecar-nya.",
        size=13, family=F_SANS, weight=400, fill=INK3, anchor="middle")

c.save("architecture.svg")
print("architecture.svg written")
