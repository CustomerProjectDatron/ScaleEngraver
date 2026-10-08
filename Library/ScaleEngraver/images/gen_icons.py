# Generates the 64x64 parameter icons (SVG). Run render.ps1 to also create the PNGs.
import math, os
G = "#555555"; B = "#1f6feb"; L = "#bbbbbb"
OUT = os.path.dirname(os.path.abspath(__file__))
icons = {}

def st(c, w=3, extra=""):
    return f'fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}'
def line(x1, y1, x2, y2, c=G, w=3, dash=None):
    d = f'stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" {st(c, w, d)}/>'
def path(d, c=G, w=3, dash=None):
    ds = f'stroke-dasharray="{dash}"' if dash else ""
    return f'<path d="{d}" {st(c, w, ds)}/>'
def dim(x1, y1, x2, y2, c=B, w=2.5, h=4):
    """double arrow with open heads"""
    a = math.atan2(y2 - y1, x2 - x1)
    def head(x, y, d):
        p1 = (x - h * math.cos(d - 0.6), y - h * math.sin(d - 0.6))
        p2 = (x - h * math.cos(d + 0.6), y - h * math.sin(d + 0.6))
        return f'M{p1[0]:.1f},{p1[1]:.1f} L{x:.1f},{y:.1f} L{p2[0]:.1f},{p2[1]:.1f}'
    return line(x1, y1, x2, y2, c, w) + path(head(x2, y2, a) + " " + head(x1, y1, a + math.pi), c, w)
def circle(x, y, r, c=G, w=3, fill="none"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{c}" stroke-width="{w}"/>'
def sq(x, y, s, c, filled=True):
    if filled:
        return f'<rect x="{x-s/2:.1f}" y="{y-s/2:.1f}" width="{s}" height="{s}" rx="1.5" fill="{c}"/>'
    return f'<rect x="{x-s/2:.1f}" y="{y-s/2:.1f}" width="{s}" height="{s}" rx="1.5" {st(c, 2, "stroke-dasharray=" + chr(34) + "3 2.5" + chr(34))}/>'
def glyph(x, top, c=G):
    # a bold "5" as simple polyline, 14 wide, 16 tall
    return path(f"M{x+7},{top} H{x-6} V{top+7} H{x+3} Q{x+7},{top+7} {x+7},{top+11.5} Q{x+7},{top+16} {x+3},{top+16} H{x-7}", c, 3)
def pol(cx, cy, r, deg):
    a = math.radians(deg); return cx + r * math.cos(a), cy - r * math.sin(a)

def ruler(ticks, base=44, x0=6, x1=58, bc=G):
    s = line(x0, base, x1, base, bc)
    for x, ln, c in ticks:
        s += line(x, base, x, base - ln, c)
    return s

# ---- ruler based ---------------------------------------------------------
icons["tickLength"] = ruler([(10, 9, G), (22, 9, G), (34, 26, B), (46, 9, G), (58, 9, G)], 48, 6, 60)
icons["majorStep"] = ruler([(8, 20, G), (32, 20, G), (56, 20, G)], 48) + dim(8, 20, 32, 20)
icons["minorDivisions"] = ruler([(8, 22, G), (56, 22, G)] + [(8 + 12 * k, 11, B) for k in range(1, 4)], 48)
icons["mediumEvery"] = ruler([(8, 22, G), (56, 22, G), (32, 15, B)] + [(x, 8, G) for x in (16, 24, 40, 48)], 48)
icons["scaleLength"] = ruler([(8, 14, G), (20, 8, G), (32, 14, G), (44, 8, G), (56, 14, G)], 34) + \
    line(8, 38, 8, 56, L, 2) + line(56, 38, 56, 56, L, 2) + dim(8, 50, 56, 50)
_ang = math.atan2(28, 46)
_rot = line(8, 52, 58, 52, L, 3, "4 5") + line(8, 52, 54, 24, B) + path("M26,52 A18,18 0 0 0 23.4,42.3", B, 2.5)
for t in (0.0, 0.34, 0.67, 1.0):
    px, py = 8 + 46 * t, 52 - 28 * t
    _rot += line(px, py, px - 9 * math.sin(_ang), py - 9 * math.cos(_ang), B)
icons["rotationAngle"] = _rot
icons["side_positive"] = line(6, 38, 52, 38, G) + path("M47,33 L54,38 L47,43", G) + "".join(line(x, 38, x, 20, B) for x in (14, 28, 42))
icons["side_negative"] = line(6, 26, 52, 26, G) + path("M47,21 L54,26 L47,31", G) + "".join(line(x, 26, x, 44, B) for x in (14, 28, 42))
icons["baselineDepth"] = line(6, 42, 58, 42, B, 4) + "".join(line(x, 42, x, 28, G) for x in (12, 24, 36, 48, 58))

# ---- labels ----------------------------------------------------------------
def lab_base(extra="", gx=32):
    return glyph(gx, 8) + line(gx, 44, gx, 56, G) + line(8, 56, 56, 56, G) + extra
icons["labelHeight"] = lab_base(dim(50, 8, 50, 24))
icons["labelWidth"] = lab_base(dim(25, 30, 39, 30))
icons["labelOffset"] = lab_base(dim(32, 28, 32, 42))
def labrow(kinds):
    xs = (10, 25, 40, 55) if len(kinds) == 4 else (10, 22, 34, 46, 58)
    s = line(4, 52, 60, 52, G)
    for x, k in zip(xs, kinds):
        s += line(x, 52, x, 40, B if k == "tickoff" else G, 3, "1 4" if k == "tickoff" else None)
        if k == "on":
            s += sq(x, 28, 10, G)
        elif k in ("off", "tickoff"):
            s += sq(x, 28, 10, B, False)
        elif k == "blue":
            s += sq(x, 28, 10, B)
    return s
icons["labelEvery"] = labrow(["blue", "none", "blue", "none", "blue"])
icons["skipFirstLabel"] = labrow(["off", "on", "on", "on"])
icons["skipLastLabel"] = labrow(["on", "on", "on", "off"])
icons["skipFirstTick"] = labrow(["tickoff", "on", "on", "on"])
icons["skipLastTick"] = labrow(["on", "on", "on", "tickoff"])

# ---- circular --------------------------------------------------------------
cx, cy, R = 32, 33, 22
def ring(c=G, r=R, w=3):
    return circle(cx, cy, r, c, w)
icons["radius"] = ring() + line(cx, cy, *pol(cx, cy, R - 1, -35), B) + circle(cx, cy, 3, B, 1, B)
icons["startAngle"] = ring(L) + line(cx, cy, cx + R + 6, cy, G, 3, "3 4") + line(cx, cy, cx, cy - R - 4, B) + path(f"M{cx+13},{cy} A13,13 0 0 0 {cx},{cy-13}", B, 2.5)
_e = pol(cx, cy, R + 4, -50)
_a1 = pol(cx, cy, 14, 90); _a2 = pol(cx, cy, 14, -50)
_dx, _dy = math.sin(math.radians(-50)), math.cos(math.radians(-50))   # clockwise direction at -50 deg
_hx, _hy = _a2
def _arm(s):
    ca, sa = math.cos(0.5), math.sin(0.5)
    bx, by = -_dx, -_dy
    return _hx + 7 * (bx * ca - s * by * sa), _hy + 7 * (by * ca + s * bx * sa)
_p1, _p2 = _arm(1), _arm(-1)
_s1 = pol(cx, cy, 19, -50)
icons["endAngle"] = ring(L) + line(cx, cy, cx, cy - R - 4, G) + line(*_s1, *_e, B) +     path("M%.1f,%.1f A14,14 0 0 1 %.1f,%.1f" % (_a1[0], _a1[1], _a2[0], _a2[1]), B, 2.5) +     path("M%.1f,%.1f L%.1f,%.1f L%.1f,%.1f" % (_p1[0], _p1[1], _hx, _hy, _p2[0], _p2[1]), B, 2.5)
def bar(x, y, ang, c=B, ln=13, th=6):
    return f'<rect x="{-ln/2}" y="{-th/2}" width="{ln}" height="{th}" rx="2" fill="{c}" transform="translate({x:.1f},{y:.1f}) rotate({-ang})"/>'
def orient(top_ang, right_ang):
    ccx, ccy, r = 22, 42, 15
    s = circle(ccx, ccy, r, G, 3)
    s += line(*pol(ccx, ccy, r, 90), *pol(ccx, ccy, r + 5, 90), G) + line(*pol(ccx, ccy, r, 0), *pol(ccx, ccy, r + 5, 0), G)
    return s + bar(*pol(ccx, ccy, r + 5 + 6, 90), top_ang) + bar(*pol(ccx, ccy, r + 5 + 7, 0), right_ang)
icons["orientation_tangential"] = orient(0, 90)
icons["orientation_radial"] = orient(90, 0)
icons["orientation_horizontal"] = orient(0, 0)

# ---- side views ------------------------------------------------------------
SURF = 42
PATH = "M6,22 H18 V54 H34 V22 H46 V8 H58"
def side(level_y):
    return line(4, SURF, 60, SURF, L, 3) + line(4, level_y, 60, level_y, B, 3, "4 4") + path(PATH, G, 3)
icons["referenceZ"] = line(4, 54, 60, 54, L, 2.5, "4 4") + line(4, 28, 60, 28, G, 3.5) + dim(32, 54, 32, 28, B, 2.5, 4)
icons["feedHeight"] = line(4, 44, 60, 44, L, 3) + line(4, 26, 60, 26, B, 2.5, "4 4") + path("M20,6 V26", G, 3) + line(20, 26, 20, 56, B, 4) + dim(46, 44, 46, 26, B, 2.5, 4)
icons["infeedZ"] = line(4, 14, 60, 14, L, 3) + line(14, 30, 54, 30, B, 2.5, "4 4") + line(14, 46, 54, 46, B, 2.5, "4 4") + path("M10,6 V14 L14,14 V30 H50 V46 H14", G, 3) + dim(58, 14, 58, 30, B, 2.5, 4)
icons["tickDepth"] = line(4, 18, 60, 18, L, 3) + "".join(line(x, 18, x, 50, B, 4) for x in (14, 32, 50))
icons["depth"] = line(4, 18, 60, 18, L, 3) + path("M10,6 V50 H54 V6", G) + dim(32, 18, 32, 50)

# ---- fraction (inch) scale ------------------------------------------------
_H = {0: 30, 4: 22, 2: 15, 6: 15}
def fticks(colors=None, base=54):
    colors = colors or {}
    s = line(6, base, 60, base, G)
    for i in range(9):
        s += line(8 + 6 * i, base, 8 + 6 * i, base - _H.get(i, 9), colors.get(i, G))
    return s
def fblock(x, y, w, h, c):
    return f'<rect x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w}" height="{h}" rx="1.5" fill="{c}"/>'
def fglyph(x, y, c, k=1.0):
    # fraction glyph: dot, bar, dot
    return circle(x, y - 6 * k, 1.8 * k, c, 1, c) + line(x - 4.5 * k, y, x + 4.5 * k, y, c, 2.5) + circle(x, y + 6 * k, 1.8 * k, c, 1, c)
icons["levels"] = fticks() + "".join(circle(8 + 6 * i, 54 - _H.get(i, 9), 3, B, 1, B) for i in (0, 4, 2, 1))
icons["tickStyles"] = fticks({0: B, 4: B, 1: B})
icons["unitLabel"] = fticks() + fblock(8, 12, 12, 11, B)
icons["fractionLabel"] = fticks() + fblock(8, 12, 12, 11, G) + fglyph(32, 22, B, 0.9)
icons["fractionLabelLevel"] = fticks() + fblock(8, 12, 12, 11, G) + fblock(32, 25, 6, 5, B) + fblock(20, 32, 6, 5, B) + fblock(44, 32, 6, 5, B)
icons["fractionDenominator"] = line(6, 54, 60, 54, G) + line(32, 54, 32, 28, G) + fglyph(32, 14, B, 1.4)

for n, body in icons.items():
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">'
           f'<rect width="64" height="64" fill="#ffffff"/>{body}</svg>\n')
    with open(os.path.join(OUT, n + ".svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
print(len(icons), "icons")
