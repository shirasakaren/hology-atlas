import sys
sys.path.insert(0, ".")
from helpers import *

c = Canvas(1400, 620)
c.defs_arrowhead(INK4)

c.eyebrow(60, 56, "ARSITEKTUR SISTEM")
c.text(60, 92, "Alur Autentikasi & Sesi", size=32, family=F_DISPLAY, weight=700, fill=INK)

y = 170
methods = ["Kata sandi", "Magic link", "OTP telepon", "Passphrase instansi", "OAuth2", "OIDC / SAML"]
mw, mh, gap = 205, 64, 16
total = len(methods) * mw + (len(methods) - 1) * gap
x0 = (1400 - total) / 2
for i, m in enumerate(methods):
    x = x0 + i * (mw + gap)
    c.rect(x, y, mw, mh, fill=BLUE_50, stroke=BLUE, sw=1.2, rx=12)
    c.text(x + mw/2, y + mh/2 + 5, m, size=13.5, family=F_SANS, weight=600, fill=BLUE, anchor="middle")

c.text(700, y - 20, "Pengguna memilih metode masuk", size=14, family=F_SANS, weight=500, fill=INK3, anchor="middle")

# converge to issueSession
iy = 300
c.node(560, iy, 280, 90, "AuthService.issueSession()", ["Backend menerbitkan sesi", "satu jalur untuk semua metode"], accent=BLUE, accent_tint=BLUE_50, icon=icon_shield)
for i, m in enumerate(methods):
    x = x0 + i * (mw + gap) + mw/2
    c.arrow(x, y+mh, 700, iy, color=LINE_STRONG, sw=1.5)

# session row
sy = 430
c.node(140, sy, 300, 100, "Baris Session di PostgreSQL", ["UUID buram (opaque)", "Bukan JWT yang bisa dibaca"], mono="tabel: Session", accent=GREEN, accent_tint=GREEN_50, icon=icon_db)
c.node(560, sy, 280, 100, "localStorage Browser", ["Disimpan di client", "Tanpa cookie, tanpa NextAuth"], mono="atlas_session", accent=BLUE, accent_tint=BLUE_50, icon=icon_browser)
c.node(960, sy, 300, 100, "Setiap Permintaan API", ["Header disertakan otomatis", "Divalidasi ulang tiap request"], mono="Authorization: Bearer <id>", accent=RED, accent_tint=RED_50, icon=icon_shield)

c.arrow(560+140, iy+90, 290, sy, color=INK3, label="simpan baris")
c.arrow(700, iy+90, 700, sy, color=INK3, label="kirim ke client")
c.arrow(840, sy+50, 960, sy+50, color=INK3, label="tiap panggilan")

c.text(700, 600, "Metode masuk berbeda-beda, tetapi semuanya bermuara pada satu penerbit sesi — konsisten dan mudah diaudit.",
        size=13, family=F_SANS, fill=INK3, anchor="middle")

c.save("auth-flow.svg")
print("ok")
