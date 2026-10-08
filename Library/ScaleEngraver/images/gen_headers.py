# Generates the header images of the two top-level commands (EngraveRuler, EngraveDial).
# Same icon language as the parameter icons: grey linework, blue for the part that matters, no text.
import math, os
G = "#555555"; B = "#1f6feb"
OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 360, 120

def st(c, w):
    return f'fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'
def line(x1, y1, x2, y2, c=G, w=3):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" {st(c, w)}/>'
def glyph(cx, cy, c=B, k=0.75):
    # single-stroke "5", centred on (cx, cy)
    d = "M7,0 H-6 V7 H3 Q7,7 7,11.5 Q7,16 3,16 H-7"
    return f'<g transform="translate({cx:.1f} {cy:.1f}) scale({k}) translate(0 -8)"><path d="{d}" {st(c, 3.4)}/></g>'

def ruler():
    x0, x1, base = 20, 340, 92
    s = line(x0, base, x1, base, G, 3.5)
    n = 20
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        if i % 10 == 0:
            s += line(x, base, x, base - 42, B, 4)
            if i:
                s += glyph(x, base - 62)
        elif i % 5 == 0:
            s += line(x, base, x, base - 29, G, 3.5)
        else:
            s += line(x, base, x, base - 20, G, 3)
    return s

def dial():
    cx, cy, r = 180, 60, 30
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" {st(G, 3.5)}/>'
    for i in range(36):
        a = math.radians(90 - i * 10)
        major = i % 3 == 0
        L = 11 if major else 6
        c = B if major else G
        s += line(cx + r * math.cos(a), cy - r * math.sin(a), cx + (r + L) * math.cos(a), cy - (r + L) * math.sin(a), c, 4 if major else 3)
        if major and i:
            rl = r + L + 8
            s += glyph(cx + rl * math.cos(a), cy - rl * math.sin(a), B, 0.5)
    return s + f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{G}"/>'

def angle_scale():
    # a speed square scale: ticks every degree, spacing grows with the tangent, ticks radial to the pivot (above, out of the image)
    x0, base, d = 40, 100, 280 / math.tan(math.radians(45))
    s = line(x0, base, x0 + d * math.tan(math.radians(45)), base, G, 3.5)
    for deg in range(0, 46):
        x = x0 + d * math.tan(math.radians(deg))
        sa, ca = math.sin(math.radians(deg)), math.cos(math.radians(deg))
        L, col, w = (36, B, 4) if deg % 10 == 0 else ((26, G, 3.5) if deg % 5 == 0 else (18, G, 3))
        s += line(x, base, x - L * sa, base - L * ca, col, w)
        if deg % 10 == 0 and deg:
            r = L + 14
            s += glyph(x - r * sa, base - r * ca, B, 0.6)
    return s

for name, body in (("header_EngraveRuler", ruler()), ("header_EngraveAngleScale", angle_scale()), ("header_EngraveDial", dial())):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>{body}</svg>\n')
    with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(svg)
print("headers written")
