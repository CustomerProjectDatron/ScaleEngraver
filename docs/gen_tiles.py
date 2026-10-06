"""Generates the tile-style icons in docs/tiles/ (flat white line glyphs on a blue tile, like the control's home screen).

  python gen_tiles.py      -> docs/tiles/*.svg and docs/tiles/contact_sheet.svg
  render.ps1 / resvg       -> PNGs
"""
import math
from pathlib import Path

W = "#ffffff"
ACC = "#ffb020"          # one accent: the part that does the work (needle, major ticks)
SW = 9                   # glyph stroke width on the 256 grid
OUT = Path(__file__).with_name("tiles")
OUT.mkdir(exist_ok=True)


def tile(inner: str) -> str:
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256">\n'
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#07629e"/><stop offset="1" stop-color="#054478"/></linearGradient></defs>\n'
        '<rect width="256" height="256" rx="6" fill="url(#bg)"/>\n'
        '<path d="M0 0 H256 V46 L0 92 Z" fill="#ffffff" opacity="0.09"/>\n'
        + inner + "\n</svg>\n"
    )


def line(x1, y1, x2, y2, col=W, w=SW):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'


def polar(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy - r * math.sin(a)


def radial(cx, cy, r1, r2, deg, col=W, w=SW):
    x1, y1 = polar(cx, cy, r1, deg)
    x2, y2 = polar(cx, cy, r2, deg)
    return line(x1, y1, x2, y2, col, w)


def ring(cx, cy, r, col=W, w=SW):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="{w}"/>'


def arc(cx, cy, r, a0, a1, col=W, w=SW):
    """arc from angle a0 to a1 (degrees, counter-clockwise, 0 = +X); drawn clockwise when a1 < a0."""
    x0, y0 = polar(cx, cy, r, a0)
    x1, y1 = polar(cx, cy, r, a1)
    sweep = a1 - a0
    large = 1 if abs(sweep) > 180 else 0
    cw = 1 if sweep < 0 else 0
    return (f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 {large} {cw} {x1:.1f} {y1:.1f}" fill="none" '
            f'stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')


def hub(cx, cy):
    return f'<circle cx="{cx}" cy="{cy}" r="10" fill="{W}"/>'


icons = {}

# ---- ruler: outlined strip, ticks hanging from the top edge, major ticks in the accent colour
parts = [f'<rect x="26" y="88" width="204" height="80" rx="10" fill="none" stroke="{W}" stroke-width="{SW}"/>']
for i in range(11):
    x = 46 + i * 16.4
    major = i % 5 == 0
    parts.append(line(x, 99, x, 99 + (34 if major else 18), ACC if major else W, 8 if major else 6))
icons["ruler"] = "\n".join(parts)

# ---- dial: ring, twelve ticks inside, needle in the accent colour
parts = [ring(128, 128, 82)]
for k in range(12):
    parts.append(radial(128, 128, 56, 68, 90 - k * 30, W, 8))
parts.append(radial(128, 128, 0, 46, 30, ACC, 10))
parts.append(hub(128, 128))
icons["dial"] = "\n".join(parts)

# ---- gauge: 270 degree arc, ticks outside, needle
parts = [arc(128, 136, 70, 225, -45)]
for k in range(11):
    a = 225 - k * 27
    major = k % 5 == 0
    parts.append(radial(128, 136, 80, 94 if major else 90, a, ACC if major else W, 8 if major else 6))
parts.append(radial(128, 136, 0, 54, 60, ACC, 10))
parts.append(hub(128, 136))
icons["gauge"] = "\n".join(parts)

# ---- protractor: half circle with the base line, ticks inside
cx, cy = 128, 176
parts = [f'<path d="M36 {cy} A92 92 0 0 1 220 {cy} Z" fill="none" stroke="{W}" stroke-width="{SW}" stroke-linejoin="round"/>']
for k in range(1, 12):
    a = 180 - k * 15
    major = k % 3 == 0
    parts.append(radial(cx, cy, 60 if major else 66, 78, a, ACC if major else W, 8 if major else 6))
parts.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{W}"/>')
icons["protractor"] = "\n".join(parts)

# ---- inch ruler: outlined strip, ticks of five heights (whole, 1/2, 1/4, 1/8, 1/16)
parts = [f'<rect x="26" y="88" width="204" height="80" rx="10" fill="none" stroke="{W}" stroke-width="{SW}"/>']
heights = {0: 40, 1: 32, 2: 24, 3: 16, 4: 9}
n = 16
for i in range(n + 1):
    x = 44 + (212 - 44) * i / n
    lvl = 0 if i % 16 == 0 else 1 if i % 8 == 0 else 2 if i % 4 == 0 else 3 if i % 2 == 0 else 4
    parts.append(line(x, 98, x, 98 + heights[lvl], ACC if lvl == 0 else W, 7 if lvl <= 1 else 5))
icons["inch_ruler"] = "\n".join(parts)

# ---- app logo: dial above, ruler below
parts = [ring(128, 108, 62)]
for k in range(12):
    parts.append(radial(128, 108, 42, 52, 90 - k * 30, W, 7))
parts.append(radial(128, 108, 0, 34, 30, ACC, 9))
parts.append(hub(128, 108))
parts.append(f'<rect x="34" y="186" width="188" height="44" rx="8" fill="none" stroke="{W}" stroke-width="8"/>')
for i in range(10):
    x = 52 + i * 16.9
    major = i % 3 == 0
    parts.append(line(x, 194, x, 194 + (22 if major else 12), ACC if major else W, 7 if major else 5))
icons["logo"] = "\n".join(parts)

for name, inner in icons.items():
    (OUT / f"tile_{name}.svg").write_text(tile(inner), encoding="utf-8")

# contact sheet (3 x 2) to check the family at a glance
names = list(icons)
cell, gap = 256, 24
cols = 3
rows = math.ceil(len(names) / cols)
sheet = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cols*(cell+gap)+gap} {rows*(cell+gap)+gap}" '
         f'width="{cols*(cell+gap)+gap}" height="{rows*(cell+gap)+gap}">',
         '<rect width="100%" height="100%" fill="#1b1b1b"/>']
for idx, name in enumerate(names):
    x = gap + (idx % cols) * (cell + gap)
    y = gap + (idx // cols) * (cell + gap)
    body = tile(icons[name]).split("\n", 1)[1].rsplit("</svg>", 1)[0].replace('id="bg"', f'id="bg{idx}"').replace('url(#bg)', f'url(#bg{idx})')
    sheet.append(f'<g transform="translate({x},{y})">{body}</g>')
sheet.append("</svg>")
(OUT / "contact_sheet.svg").write_text("\n".join(sheet), encoding="utf-8")
print("tiles written:", ", ".join(names))
