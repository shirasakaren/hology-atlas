import sys
sys.path.insert(0, ".")
from helpers import *

c = Canvas(1400, 780)
c.defs_arrowhead(INK4)

c.eyebrow(60, 56, "ARSITEKTUR SISTEM")
c.text(60, 92, "Topologi Deployment", size=32, family=F_DISPLAY, weight=700, fill=INK)
c.text(60, 118, "Produksi berjalan nyata di atlas.creations.ren, bukan rencana di atas kertas.",
        size=14, family=F_SANS, fill=INK3)

# Cloudflare
c.node(560, 160, 280, 80, "Cloudflare DNS", ["Empat subdomain, DNS-only"], mono="creations.ren", accent=YELLOW, accent_tint=YELLOW_50, icon=icon_cloud)

# Railway group box
c.rect(140, 290, 760, 300, fill=SURFACE_MUTED, stroke=LINE, sw=1.2, rx=18)
c.eyebrow(170, 322, "RAILWAY: PLATFORM MANAGED")
c.node(170, 340, 210, 100, "frontend", ["Next.js, Docker", "atlas.creations.ren"], accent=BLUE, accent_tint=BLUE_50, icon=icon_server)
c.node(400, 340, 210, 100, "backend", ["NestJS, Docker", "api.atlas.creations.ren"], accent=BLUE, accent_tint=BLUE_50, icon=icon_server)
c.node(630, 340, 240, 100, "yjs", ["y-websocket sidecar", "yjs.atlas.creations.ren"], accent=GREEN, accent_tint=GREEN_50, icon=icon_grid)
c.node(170, 470, 240, 100, "Postgres", ["Template terkelola Railway"], mono="managed", accent=GREEN, accent_tint=GREEN_50, icon=icon_db)
c.wrapped_text(430, 530, ["Penyimpanan berkas: dikonfigurasi lewat Godmode (lokal / S3 / R2),", "tanpa perlu redeploy ulang."],
        size=12.5, family=F_SANS, fill=INK3, lh=18)

# VPS group box
c.rect(980, 290, 280, 300, fill=SURFACE_MUTED, stroke=LINE, sw=1.2, rx=18)
c.eyebrow(1005, 322, "VPS TERPISAH")
c.node(1000, 350, 240, 110, "LiveKit + Caddy", ["Media WebRTC + reverse proxy", "UDP mux dipublikasikan langsung"], mono="443 / UDP 7882", accent=RED, accent_tint=RED_50, icon=icon_voice)
c.wrapped_text(1005, 500, ["Dipisah dari Railway karena", "Railway tidak menyediakan", "ingress UDP publik untuk media."],
        size=12.5, family=F_SANS, fill=INK3, lh=18)

c.arrow(700, 240, 700, 290, color=YELLOW, sw=2)
c.arrow(700, 240, 1120, 290, color=YELLOW, sw=2, curve=60)

c.text(700, 640, "Firewall (ufw) di VPS hanya membuka 22/80/443/7882, default deny untuk selebihnya.",
        size=13, family=F_SANS, fill=INK3, anchor="middle")
c.wrapped_text(700, 700, ["Catatan kejujuran teknis: rekaman panggilan (LiveKit Egress) belum aktif di VPS 2GB saat ini,", "kemampuannya sudah ada di kode, tinggal menambah sumber daya."],
        size=12.5, family=F_SANS, fill=INK4, anchor="middle", lh=18)

c.save("deployment.svg")
print("ok")
