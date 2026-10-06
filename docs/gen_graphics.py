"""Generates the ScaleEngraver SVG graphics (geometry computed, brand neutral).
Run: python docs/gen_graphics.py   (docs/render.ps1 does that and renders the PNGs)."""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INK, ACC, HELP, ORG, BG = "#1b1f24", "#1f6feb", "#9aa4b2", "#e8710a", "#f5f7fa"
FONT = "Arial, Segoe UI, sans-serif"


def f(x):
    return f"{x:.2f}".rstrip("0").rstrip(".")


def svg(w, h, body, bg=None, comment=""):
    r = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="{FONT}">\n{comment}{r}\n{body}\n</svg>\n')


def line(x1, y1, x2, y2, col=INK, w=2, extra=""):
    return (f'<line x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{col}" '
            f'stroke-width="{w}" stroke-linecap="round" {extra}/>')


def text(x, y, s, size, col=INK, anchor="middle", weight="400", extra=""):
    return (f'<text x="{f(x)}" y="{f(y)}" font-size="{size}" fill="{col}" text-anchor="{anchor}" '
            f'font-weight="{weight}" {extra}>{s}</text>')


def ruler(x0, y0, length, vmax, unit, w_major, w_med, w_min, size, skip_first=True,
          col=INK, major_step=10, med_every=5):
    """Ruler along +X, ticks up; tick lengths 6 / 4.5 / 3 units (unit = px per length unit)."""
    out = [line(x0, y0, x0 + length, y0, col, w_major)]
    px = length / vmax
    gap = 1.8 * unit
    for v in range(vmax + 1):
        x = x0 + v * px
        if v % major_step == 0:
            L, w = 6, w_major
        elif v % med_every == 0:
            L, w = 4.5, w_med
        else:
            L, w = 3, w_min
        out.append(line(x, y0, x, y0 - L * unit, col, w))
        if v % major_step == 0 and not (skip_first and v == 0):
            out.append(text(x, y0 - L * unit - gap, str(v), size, col))
    return "\n".join(out)


def dial(cx, cy, R, unit, vmax, major, minor_div, size, col=INK, w=(3, 2),
         start=90, end=None, inward=False, hlabel=False):
    """Circular scale, clockwise. Value v at angle start - v/vmax*sweep (math degrees)."""
    sweep = 360 if end is None else (start - end)
    out = []
    if sweep == 360:
        out.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(R)}" fill="none" stroke="{col}" stroke-width="{w[0]}"/>')
    else:
        a0, a1 = math.radians(start), math.radians(end)
        out.append(f'<path d="M {f(cx+R*math.cos(a0))} {f(cy-R*math.sin(a0))} A {f(R)} {f(R)} 0 0 1 '
                   f'{f(cx+R*math.cos(a1))} {f(cy-R*math.sin(a1))}" fill="none" stroke="{col}" '
                   f'stroke-width="{w[0]}" stroke-linecap="round"/>')
    step = major / minor_div
    n = int(round(vmax / step))
    sgn = -1 if inward else 1
    gap = 1.6 * unit
    for i in range(n + 1):
        v = i * step
        if sweep == 360 and i == n:
            break
        a = math.radians(start - v / vmax * sweep)
        ca, sa = math.cos(a), math.sin(a)
        ismaj = abs(v / major - round(v / major)) < 1e-9
        L = 6 if ismaj else 3
        out.append(line(cx + R * ca, cy - R * sa, cx + (R + sgn * L * unit) * ca,
                        cy - (R + sgn * L * unit) * sa, col, w[0] if ismaj else w[1]))
        if ismaj:
            lab = str(int(round(v)))
            if hlabel:
                rl = R + sgn * (L * unit + gap + size * 0.7)
                out.append(text(cx + rl * ca, cy - rl * sa + size * 0.35, lab, size, col))
            else:
                rl = R + sgn * (L * unit + gap)
                px_, py_ = cx + rl * ca, cy - rl * sa
                out.append(f'<g transform="translate({f(px_)} {f(py_)}) rotate({f(90 - math.degrees(a))})">'
                           + text(0, 0, lab, size, col) + '</g>')
    return "\n".join(out)


def w(path, content):
    p = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)


# 2 hero ruler ---------------------------------------------------------
w("docs/hero_ruler.svg", svg(1000, 260, ruler(60, 190, 880, 100, 10, 4, 3.5, 2.5, 26, True), BG))

# 3 hero dial ----------------------------------------------------------
w("docs/hero_dial.svg", svg(640, 640, dial(320, 320, 205, 8, 360, 30, 6, 26, INK, w=(4, 2.5)), BG))

# 4 protractor: 0..180 clockwise from the left, ticks inward, numbers inside
body = [dial(400, 400, 340, 8, 180, 20, 4, 24, INK, start=180, end=0, inward=True, hlabel=True, w=(4, 2.5)),
        f'<circle cx="400" cy="400" r="6" fill="{ACC}"/>']
w("docs/protractor.svg", svg(800, 440, "\n".join(body), BG))


# 5 workflow -----------------------------------------------------------
def box(x, y, wd, h, lines, dashed=False, accent=False, size=24):
    col = HELP if dashed else (ACC if accent else INK)
    st = f'stroke="{col}" stroke-width="3"' + (' stroke-dasharray="10 8"' if dashed else "")
    s = f'<rect x="{x}" y="{y}" width="{wd}" height="{h}" rx="14" fill="none" {st}/>'
    n = len(lines)
    y0 = y + h / 2 - (n - 1) * 15 + 8
    for i, t in enumerate(lines):
        s += text(x + wd / 2, y0 + i * 30, t, size, INK, weight="700" if i == 0 else "400")
    return s


def arrow(x1, y1, x2, y2, dashed=False, col=INK):
    a = math.atan2(y2 - y1, x2 - x1)
    L = 14
    p = [(x2, y2), (x2 - L * math.cos(a - .4), y2 - L * math.sin(a - .4)),
         (x2 - L * math.cos(a + .4), y2 - L * math.sin(a + .4))]
    d = 'stroke-dasharray="10 8"' if dashed else ""
    pts = " ".join(f(u) + "," + f(v) for u, v in p)
    return (line(x1, y1, x2 - 8 * math.cos(a), y2 - 8 * math.sin(a), col, 3, d) +
            f'<polygon points="{pts}" fill="{col}"/>')


body = [box(40, 50, 260, 110, ["Parameters"], accent=True),
        box(370, 50, 260, 110, ["Plan", "lines, arcs, labels"]),
        box(700, 50, 260, 110, ["Engrave", "motion"], accent=True),
        arrow(300, 105, 370, 105), arrow(630, 105, 700, 105),
        text(830, 200, "tool, Rpm, Feed, Spindle On/Off", 18, INK),
        text(830, 224, "come from your program", 18, INK),
        arrow(500, 160, 500, 208, True, HELP),
        box(330, 210, 340, 70, ["Preview / web API (planned)"], dashed=True, size=20)]
w("docs/workflow.svg", svg(1000, 300, "\n".join(body), BG))

# 6 move sequence (side view of one tick) ------------------------------
sy, ry, ay, dy = 190, 50, 150, 250
xa, xb = 40, 690
x0, x1, x2 = 150, 330, 540
body = [f'<rect x="{xa}" y="{sy}" width="{xb-xa}" height="130" fill="#e3e8ef"/>',
        line(xa, ry, xb, ry, HELP, 1.5, 'stroke-dasharray="4 6"'),
        line(xa, ay, xb, ay, HELP, 1.5, 'stroke-dasharray="4 6"'),
        line(xa, dy, xb, dy, ORG, 1.5, 'stroke-dasharray="4 6"'),
        line(xa, sy, xb, sy, INK, 3),
        f'<polyline points="{x0},{dy} {x0},{ry} {x1},{ry} {x1},{ay}" fill="none" stroke="{INK}" '
        f'stroke-width="3" stroke-dasharray="10 7" stroke-linejoin="round"/>',
        line(x1, ay, x1, dy, ACC, 4), line(x1, dy, x2, dy, ACC, 4),
        f'<polyline points="{x2},{dy} {x2},{ry}" fill="none" stroke="{INK}" stroke-width="3" '
        f'stroke-dasharray="10 7"/>',
        f'<circle cx="{x1}" cy="{dy}" r="6" fill="{ORG}"/>',
        text(705, ry + 6, "retractZ", 20, INK, "start"),
        text(705, ay + 6, "approachZ", 20, INK, "start"),
        text(705, sy + 6, "surface Z=0", 20, INK, "start", "700"),
        text(705, dy + 6, "depth", 20, ORG, "start", "700"),
        text((x1 + x2) / 2, dy + 38, "cut", 20, ACC, "middle", "700")]
w("docs/move_sequence.svg", svg(900, 360, "\n".join(body), BG))
print("ok")
