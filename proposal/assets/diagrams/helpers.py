"""Shared SVG primitives for the Atlas/HOLOGY proposal diagrams.
Restyled to match the FCS academic-journal template (atlas.cls): thin-line
technical diagrams, sparse two-color palette (blue primary, orange only for
emphasis), serif headings to match newtxtext body text.
"""

INK = "#1a1a1a"
INK2 = "#3d3d3d"
INK3 = "#6b6b6b"
INK4 = "#9a9a9a"
LINE = "#c9c9c9"
LINE_STRONG = "#8a8a8a"
SURFACE = "#ffffff"
SURFACE_MUTED = "#f2f2f2"
SURFACE_INVERSE = "#1a1a1a"

FCSBLUE = "#002EA6"
FCSORANGE = "#BF4D00"

# Legacy names kept so gen_*.py scripts need no edits: collapse the old
# 4-hue category system onto the new 2-color academic palette (blue does
# double duty for "core"/"data" categories, orange is reserved for the
# emphasis category - matches how the old scripts used RED for
# voice/security-sensitive nodes).
BLUE = FCSBLUE
GREEN = FCSBLUE
YELLOW = INK3
RED = FCSORANGE
BLUE_50 = "#e8ecf7"
YELLOW_50 = SURFACE_MUTED
RED_50 = "#f5e9e0"
GREEN_50 = "#e8ecf7"

F_DISPLAY = "Times New Roman"
F_SANS = "Times New Roman"
F_MONO = "Courier New"


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.body = []

    def raw(self, s):
        self.body.append(s)

    def rect(self, x, y, w, h, fill=SURFACE, stroke=LINE, sw=1, rx=3):
        self.raw(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def text(self, x, y, s, size=16, family=F_SANS, weight=400, fill=INK,
              anchor="start", spacing=None, upper=False, italic=False):
        s = s.upper() if upper else s
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        it = ' font-style="italic"' if italic else ""
        s = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        self.raw(
            f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{ls}{it}>{s}</text>'
        )

    def wrapped_text(self, x, y, lines, size=13, family=F_SANS, weight=400,
                       fill=INK3, anchor="start", lh=None):
        lh = lh or size * 1.35
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, size=size, family=family, weight=weight,
                       fill=fill, anchor=anchor)

    def node(self, x, y, w, h, title, subtitle=None, mono=None, accent=BLUE,
              accent_tint=BLUE_50, icon=None):
        """A titled technical box: thin border, thin top rule, serif title,
        optional subtitle lines, optional bracketed mono tag - no filled
        color blocks, matching the academic figure convention."""
        self.rect(x, y, w, h, fill=SURFACE, stroke=LINE_STRONG, sw=1, rx=2)
        self.raw(f'<rect x="{x}" y="{y}" width="{w}" height="2.5" fill="{accent}"/>')
        tx = x + 18
        ty = y + 30
        if icon:
            icon(self, x + 16, y + 16, s=20, color=accent)
            tx = x + 44
        self.text(tx, ty, title, size=15.5, family=F_DISPLAY, weight=700, fill=INK)
        cy = ty + 18
        if subtitle:
            for ln in subtitle:
                self.text(tx, cy, ln, size=11.5, family=F_SANS, weight=400, fill=INK3)
                cy += 15
        if mono:
            self.text(tx, cy + 3, f"[{mono}]", size=10.5, family=F_MONO, weight=400, fill=accent)

    def arrow(self, x1, y1, x2, y2, color=INK3, sw=1.25, dashed=False, label=None,
               label_size=11, curve=0, label_bg=True):
        marker = "url(#arrowhead)"
        dash = ' stroke-dasharray="4,4"' if dashed else ""
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
            w = 7.2 * len(label) + 10
            if label_bg:
                self.raw(
                    f'<rect x="{lx - w/2}" y="{ly - 10}" width="{w}" height="16" '
                    f'fill="{SURFACE}"/>'
                )
            self.text(lx, ly + 3, label, size=label_size, family=F_MONO, weight=400,
                        fill=INK2, anchor="middle")

    def defs_arrowhead(self, color=INK3):
        self.raw(
            f'<defs><marker id="arrowhead" markerWidth="9" markerHeight="8" '
            f'refX="8" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 z" '
            f'fill="{color}"/></marker></defs>'
        )

    def pattern_corner(self, x, y, size, svg_snippet_shapes, rotate=0):
        self.raw(f'<g transform="translate({x} {y}) rotate({rotate})" opacity="0.85">{svg_snippet_shapes}</g>')

    def eyebrow(self, x, y, text_, color=INK3):
        self.text(x, y, text_, size=10.5, family=F_SANS, weight=700, fill=color,
                     spacing="0.1em", upper=True)

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


# --- tiny hand-drawn stroke icons (unchanged geometry, recolored by caller) ---

def _icon_wrap(inner):
    return f'<g stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none">{inner}</g>'

def icon_browser(c, x, y, s=28, color=INK2):
    c.raw(f'<g transform="translate({x} {y})" stroke="{color}">' + _icon_wrap(
        f'<rect x="0" y="0" width="{s}" height="{s*0.78}" rx="2"/>'
        f'<line x1="0" y1="{s*0.26}" x2="{s}" y2="{s*0.26}"/>'
        f'<circle cx="{s*0.16}" cy="{s*0.13}" r="1" fill="{color}"/>'
    ) + '</g>')

def icon_server(c, x, y, s=28, color=BLUE):
    c.raw(f'<g transform="translate({x} {y})" stroke="{color}">' + _icon_wrap(
        f'<rect x="0" y="0" width="{s}" height="{s*0.42}" rx="2"/>'
        f'<rect x="0" y="{s*0.5}" width="{s}" height="{s*0.42}" rx="2"/>'
        f'<circle cx="{s*0.18}" cy="{s*0.21}" r="1.2" fill="{color}"/>'
        f'<circle cx="{s*0.18}" cy="{s*0.71}" r="1.2" fill="{color}"/>'
    ) + '</g>')

def icon_db(c, x, y, s=28, color=BLUE):
    c.raw(f'<g transform="translate({x} {y})" stroke="{color}">' + _icon_wrap(
        f'<ellipse cx="{s/2}" cy="{s*0.18}" rx="{s/2}" ry="{s*0.16}"/>'
        f'<path d="M0 {s*0.18} L0 {s*0.82} A{s/2} {s*0.16} 0 0 0 {s} {s*0.82} L{s} {s*0.18}"/>'
    ) + '</g>')

def icon_voice(c, x, y, s=28, color=RED):
    c.raw(f'<g transform="translate({x} {y})" stroke="{color}">' + _icon_wrap(
        f'<rect x="{s*0.32}" y="0" width="{s*0.36}" height="{s*0.58}" rx="{s*0.15}"/>'
        f'<path d="M{s*0.14} {s*0.42} A{s*0.36} {s*0.36} 0 0 0 {s*0.86} {s*0.42}"/>'
        f'<line x1="{s/2}" y1="{s*0.78}" x2="{s/2}" y2="{s}"/>'
    ) + '</g>')

def icon_chat(c, x, y, s=28, color=BLUE):
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
        f'<rect x="0" y="0" width="{half}" height="{half}" rx="1.5"/>'
        f'<rect x="{half+gap}" y="0" width="{half}" height="{half}" rx="1.5"/>'
        f'<rect x="0" y="{half+gap}" width="{half}" height="{half}" rx="1.5"/>'
        f'<rect x="{half+gap}" y="{half+gap}" width="{half}" height="{half}" rx="1.5"/>'
    ) + '</g>')

def icon_cloud(c, x, y, s=28, color=INK2):
    c.raw(f'<g transform="translate({x} {y})" stroke="{color}">' + _icon_wrap(
        f'<path d="M{s*0.2} {s*0.65} a{s*0.2} {s*0.2} 0 0 1 0 -{s*0.4} '
        f'a{s*0.28} {s*0.28} 0 0 1 {s*0.52} -{s*0.08} a{s*0.22} {s*0.22} 0 0 1 {s*0.08} {s*0.42} z"/>'
    ) + '</g>')
