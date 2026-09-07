import sys
sys.path.insert(0, ".")
from helpers import *

c = Canvas(1500, 980)
c.defs_arrowhead(INK4)

c.eyebrow(60, 56, "ARSITEKTUR SISTEM")
c.text(60, 92, "Model Data Inti (ERD Disederhanakan)", size=32, family=F_DISPLAY, weight=700, fill=INK)
c.text(60, 118, "13 entitas utama dari skema Prisma penuh, kolom lengkap tersedia di source code.",
        size=14, family=F_SANS, fill=INK3)

def ent(x, y, w, h, title, fields, accent=BLUE, tint=BLUE_50):
    c.node(x, y, w, h, title, fields, accent=accent, accent_tint=tint)

# hub
ent(610, 150, 280, 100, "User", ["id, email, name", "avatarUrl, isAdmin"], accent=BLUE, tint=BLUE_50)

# identity branch
ent(60, 320, 230, 90, "Session", ["sessionId (opaque)", "expiresAt, method"], accent=INK2, tint=SURFACE_MUTED)
ent(320, 320, 230, 90, "UserRole", ["userId -> roleId"], accent=INK2, tint=SURFACE_MUTED)
ent(320, 470, 230, 90, "Role", ["code, permissions[]"], accent=INK2, tint=SURFACE_MUTED)
ent(60, 470, 230, 90, "Notification", ["type, title, link", "readAt"], accent=INK2, tint=SURFACE_MUTED)

# project branch
ent(610, 320, 280, 90, "ProjectMember", ["userId, projectId, role"], accent=GREEN, tint=GREEN_50)
ent(610, 470, 280, 90, "Project", ["slug, title, phase", "visibility"], accent=GREEN, tint=GREEN_50)
ent(610, 620, 280, 90, "TaskList", ["name, projectKey", "taskCounter"], accent=GREEN, tint=GREEN_50)
ent(560, 770, 230, 90, "Task", ["key, title, status", "priority, dueAt"], accent=GREEN, tint=GREEN_50)
ent(850, 770, 230, 90, "TaskAssignee", ["taskId -> userId"], accent=GREEN, tint=GREEN_50)

# chat branch
ent(1130, 320, 260, 90, "ChatChannel", ["projectId (nullable)", "name, isGeneral"], accent=RED, tint=RED_50)
ent(1130, 470, 260, 90, "ChatMessage", ["channelId, authorId", "body, createdAt"], accent=RED, tint=RED_50)

# standalone
c.rect(1130, 700, 260, 90, fill=SURFACE, stroke=LINE_STRONG, sw=1.5, rx=14)
c.raw('<rect x="1130" y="700" width="260" height="6" rx="3" fill="%s"/>' % YELLOW)
c.text(1154, 736, "AppSetting", size=17, family=F_DISPLAY, weight=700, fill=INK)
c.text(1154, 758, "key -> value (JSON)", size=13, family=F_SANS, fill=INK3)
c.text(1154, 776, "instance-wide, bukan per-user", size=12, family=F_SANS, fill=INK4)

# arrows
c.arrow(700, 250, 700, 320, color=GREEN)
c.arrow(750, 410, 750, 470, color=GREEN)
c.arrow(750, 560, 750, 620, color=GREEN)
c.arrow(700, 710, 680, 770, color=GREEN, label="1:N")
c.arrow(790, 815, 850, 815, color=GREEN, label="assignee")
c.arrow(1075, 810, 1075, 200, color=INK4, dashed=True, label="userId", curve=-80)

c.arrow(610, 190, 290, 320, color=INK2, label="1:N")
c.arrow(610, 200, 550, 320, color=INK2, label="N:N", curve=-30)
c.arrow(435, 410, 435, 470, color=INK2)
c.arrow(610, 210, 290, 470, color=INK2, label="1:N", curve=30)

c.arrow(890, 470, 1130, 380, color=RED, label="channel milik project")
c.arrow(1260, 410, 1260, 470, color=RED, label="1:N")
c.arrow(1260, 560, 1075, 260, color=INK4, dashed=True, label="author", curve=120)

c.text(750, 940, "Garis putus-putus = relasi balik ke User (assignee / author), digambar melengkung agar diagram tetap terbaca.",
        size=12.5, family=F_SANS, fill=INK4, anchor="middle")

c.save("erd.svg")
print("ok")
