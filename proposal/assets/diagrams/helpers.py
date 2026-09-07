"""Shared SVG primitives for the Atlas/HOLOGY proposal diagrams.
Design tokens copied verbatim from ~/lab/design-system/DESIGN_SYSTEM.md
"""

INK = "#0e1116"
INK2 = "#3b4150"
INK3 = "#6b7280"
INK4 = "#9aa1ad"
LINE = "#ececea"
LINE_STRONG = "#d8d8d2"
SURFACE = "#ffffff"
SURFACE_MUTED = "#f7f7f5"
SURFACE_INVERSE = "#0e1116"

BLUE = "#3a6dc5"
YELLOW = "#f7bf33"
RED = "#f94141"
GREEN = "#0f8657"
BLUE_50 = "#ecf1fa"
YELLOW_50 = "#fef6e0"
RED_50 = "#fee5e5"
GREEN_50 = "#e2f1ea"

F_DISPLAY = "Bricolage Grotesque"
F_SANS = "Geist"
F_MONO = "Geist Mono"


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.body = []

    def raw(self, s):
        self.body.append(s)

    def rect(self, x, y, w, h, fill=SURFACE, stroke=LINE, sw=1.5, rx=16):
        self.raw(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def text(self, x, y, s, size=16, family=F_SANS, weight=400, fill=INK,
              anchor="start", spacing=None, upper=False):
        s = s.upper() if upper else s
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        s = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        self.raw(
            f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls}>{s}</text>'
        )

    def wrapped_text(self, x, y, lines, size=14, family=F_SANS, weight=400,
                       fill=INK3, anchor="start", lh=None):
        lh = lh or size * 1.4
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, size=size, family=family, weight=weight,
                       fill=fill, anchor=anchor)

    def node(self, x, y, w, h, title, subtitle=None, mono=None, accent=BLUE,
              accent_tint=BLUE_50, icon=None):
        """A titled card node: colored top rule, title, optional subtitle line(s), optional mono tag."""
        self.rect(x, y, w, h, fill=SURFACE, stroke=LINE_STRONG, sw=1.5, rx=14)
        self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="6" rx="3" fill="{accent}"/>')
        tx = x + 24
        ty = y + 44
        if icon:
            icon(self, x + 20, y + 24)
            tx = x + 58
        self.text(tx, ty, title, size=19, family=F_DISPLAY, weight=700, fill=INK)
        cy = ty + 22
        if subtitle:
            for ln in subtitle:
                self.text(tx, cy, ln, size=13.5, family=F_SANS, weight=400, fill=INK3)
                cy += 19
        if mono:
            self.raw(
                f'<rect x="{tx}" y="{cy-2}" width="{8*len(mono)+16}" height="21" rx="6" '
                f'fill="{accent_tint}"/>'
            )
            self.text(tx + 8, cy + 13, mono, size=12, family=F_MONO, weight=500, fill=accent)

    def arrow(self, x1, y1, x2, y2, color=INK3, sw=2, dashed=False, label=None,
               label_size=12.5, curve=0, label_bg=True):
        marker = "url(#arrowhead)"
        dash = ' stroke-dasharray="6,6"' if dashed else ""
        if curve:
            mx, my = (x1 + x2) / 2 + curve, (y1 + y2) / 2
            path = f"M {x1} {y1} Q {mx} {my} {x2} {y2}"
            self.raw(
                f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{sw}"{dash} '
                f'marker-end="{marker}"/>'
            )
            lx, ly = mx, my
        else:
            self.raw(
                f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
                f'stroke-width="{sw}"{dash} marker-end="{marker}"/>'
            )
            lx, ly = (x1 + x2) / 2, (y1 + y2) / 2
        if label:
            w = 9 * len(label) + 14
            if label_bg:
                self.raw(
                    f'<rect x="{lx - w/2}" y="{ly - 12}" width="{w}" height="19" rx="5" '
                    f'fill="{SURFACE}" stroke="{LINE}" stroke-width="1"/>'
                )
            self.text(lx, ly + 2, label, size=label_size, family=F_MONO, weight=500,
                        fill=INK2, anchor="middle")

    def defs_arrowhead(self, color=INK3):
        self.raw(
            f'<defs><marker id="arrowhead" markerWidth="10" markerHeight="9" '
            f'refX="9" refY="4.5" orient="auto"><path d="M0,0 L10,4.5 L0,9 z" '
            f'fill="{color}"/></marker></defs>'
        )

    def pattern_corner(self, x, y, size, svg_snippet_shapes, rotate=0):
        self.raw(f'<g transform="translate({x} {y}) rotate({rotate})" opacity="0.85">{svg_snippet_shapes}</g>')

    def eyebrow(self, x, y, text_, color=INK3):
        self.text(x, y, text_, size=12, family=F_SANS, weight=700, fill=color,
                     spacing="0.12em", upper=True)

    def render(self):
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}">'
            f'<rect width="{self.w}" height="{self.h}" fill="{SURFACE}"/>'
            + "".join(self.body) + "</svg>"
        )

    def save(self, path):
        with open(path, "w") as f:
            f.write(self.render())


# --- tiny hand-drawn stroke icons (Lucide-ish, 2.25px stroke, round caps) ---

def _icon_wrap(inner):
    return f'<g stroke-width="2.25" stroke-linecap="round" stroke-linejoin="round" fill="none">{inner}</g>'

def icon_browser(c, x, y, s=28, color=INK2):
    c.raw(f'<g transform="translate({x} {y})" stroke="{color}">' + _icon_wrap(
        f'<rect x="0" y="0" width="{s}" height="{s*0.78}" rx="4"/>'
        f'<line x1="0" y1="{s*0.26}" x2="{s}" y2="{s*0.26}"/>'
        f'<circle cx="{s*0.16}" cy="{s*0.13}" r="1.4" fill="{color}"/>'
    ) + '</g>')

def icon_server(c, x, y, s=28, color=BLUE):
    c.raw(f'<g transform="translate({x} {y})" stroke="{color}">' + _icon_wrap(
        f'<rect x="0" y="0" width="{s}" height="{s*0.42}" rx="4"/>'
        f'<rect x="0" y="{s*0.5}" width="{s}" height="{s*0.42}" rx="4"/>'
        f'<circle cx="{s*0.18}" cy="{s*0.21}" r="1.6" fill="{color}"/>'
        f'<circle cx="{s*0.18}" cy="{s*0.71}" r="1.6" fill="{color}"/>'
    ) + '</g>')

def icon_db(c, x, y, s=28, color=GREEN):
    c.raw(f'<g transform="translate({x} {y})" stroke="{color}">' + _icon_wrap(
        f'<ellipse cx="{s/2}" cy="{s*0.18}" rx="{s/2}" ry="{s*0.16}"/>'
        f'<path d="M0 {s*0.18} L0 {s*0.82} A{s/2} {s*0.16} 0 0 0 {s} {s*0.82} L{s} {s*0.18}"/>'
    ) + '</g>')

def icon_voice(c, x, y, s=28, color=RED):
    c.raw(f'<g transform="translate({x} {y})" stroke="{color}">' + _icon_wrap(
        f'<rect x="{s*0.32}" y="0" width="{s*0.36}" height="{s*0.58}" rx="{s*0.18}"/>'
        f'<path d="M{s*0.14} {s*0.42} A{s*0.36} {s*0.36} 0 0 0 {s*0.86} {s*0.42}"/>'
        f'<line x1="{s/2}" y1="{s*0.78}" x2="{s/2}" y2="{s}"/>'
    ) + '</g>')

def icon_chat(c, x, y, s=28, color=YELLOW):
    c.raw(f'<g transform="translate({x} {y})" stroke="{color}">' + _icon_wrap(
        f'<path d="M0 {s*0.1} h{s} v{s*0.6} h-{s*0.6} l-{s*0.22} {s*0.22} v-{s*0.22} h-{s*0.18} z"/>'
    ) + '</g>')

def icon_shield(c, x, y, s=28, color=BLUE):
    c.raw(f'<g transform="translate({x} {y})" stroke="{color}">' + _icon_wrap(
        f'<path d="M{s/2} 0 L{s} {s*0.2} V{s*0.5} C{s} {s*0.82} {s*0.72} {s} {s/2} {s} '
        f'C{s*0.28} {s} 0 {s*0.82} 0 {s*0.5} V{s*0.2} Z"/>'
    ) + '</g>')

def icon_grid(c, x, y, s=28, color=INK2):
    half = s * 0.42
    gap = s * 0.16
    c.raw(f'<g transform="translate({x} {y})" stroke="{color}">' + _icon_wrap(
        f'<rect x="0" y="0" width="{half}" height="{half}" rx="3"/>'
        f'<rect x="{half+gap}" y="0" width="{half}" height="{half}" rx="3"/>'
        f'<rect x="0" y="{half+gap}" width="{half}" height="{half}" rx="3"/>'
        f'<rect x="{half+gap}" y="{half+gap}" width="{half}" height="{half}" rx="3"/>'
    ) + '</g>')

def icon_cloud(c, x, y, s=28, color=INK2):
    c.raw(f'<g transform="translate({x} {y})" stroke="{color}">' + _icon_wrap(
        f'<path d="M{s*0.2} {s*0.65} a{s*0.2} {s*0.2} 0 0 1 0 -{s*0.4} '
        f'a{s*0.28} {s*0.28} 0 0 1 {s*0.52} -{s*0.08} a{s*0.22} {s*0.22} 0 0 1 {s*0.08} {s*0.42} z"/>'
    ) + '</g>')
