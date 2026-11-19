#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page.

One self-contained picture: a newspaper front page for Thursday
19 November 2026. Masthead with the date, a lead story (GTA VI),
six story tiles with hand-drawn pictograms, and an "also today"
strip. Every fact was checked against live news reports of the day
before drawing. Output: entry.png, 1024x1024.

Run: python3 gen.py   (writes entry.png next to this file)
Requires Pillow + DejaVu fonts in this build machine only; the
submitted program (main.py) just copies the finished PNG.
"""

import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

PAPER = (247, 243, 234)      # newsprint cream
INK = (22, 22, 34)           # near-black
NAVY = (18, 28, 61)          # masthead
GOLD = (224, 164, 88)        # date accent
PINK = (255, 46, 136)        # Vice City neon
CYAN = (0, 194, 255)
TEAL = (0, 122, 122)
RUST = (178, 58, 32)
SLATE = (84, 96, 120)
WHITE = (255, 255, 255)
DUSK_TOP = (38, 16, 64)      # lead panel sky
DUSK_BOT = (122, 28, 86)


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)
REG = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


# ---------------------------------------------------------------- tiles
def icon_globe(d, x, y, s, c1, c2):
    d.ellipse([x, y, x + s, y + s], outline=c1, width=6)
    d.ellipse([x + s * 0.28, y, x + s * 0.72, y + s], outline=c1, width=4)
    d.line([x, y + s * 0.5, x + s, y + s * 0.5], fill=c1, width=4)
    d.arc([x - s * 0.18, y + s * 0.18, x + s * 1.18, y + s * 0.82],
          start=300, end=60, fill=c2, width=5)


def icon_capitol(d, x, y, s, c, _c2=None):
    # dome + pediment + columns
    d.pieslice([x + s * 0.3, y + s * 0.05, x + s * 0.7, y + s * 0.45],
               start=180, end=360, fill=c)
    d.rectangle([x + s * 0.47, y, x + s * 0.53, y + s * 0.1], fill=c)
    d.polygon([(x + s * 0.12, y + s * 0.45), (x + s * 0.88, y + s * 0.45),
               (x + s * 0.5, y + s * 0.28)], fill=c)
    for i in range(5):
        cx = x + s * (0.18 + i * 0.16)
        d.rectangle([cx, y + s * 0.5, cx + s * 0.07, y + s * 0.85], fill=c)
    d.rectangle([x + s * 0.08, y + s * 0.88, x + s * 0.92, y + s * 0.95], fill=c)


def icon_burst(d, x, y, s, c, _c2=None):
    cx, cy = x + s / 2, y + s / 2
    for k in range(8):
        ang = k * 3.14159 / 4
        x2 = cx + (s * 0.48) * math.cos(ang)
        y2 = cy + (s * 0.48) * math.sin(ang)
        d.line([cx, cy, x2, y2], fill=c, width=6)
    d.ellipse([cx - s * 0.16, cy - s * 0.16, cx + s * 0.16, cy + s * 0.16],
              fill=c)


def icon_euro(d, x, y, s, c, _c2=None):
    f = BOLD(int(s * 0.95))
    d.text((x + s * 0.5, y + s * 0.5), "\u20ac", font=f, fill=c,
           anchor="mm")


def icon_spiral(d, x, y, s, c, _c2=None):
    cx, cy = x + s / 2, y + s / 2
    for r in range(8, int(s * 0.48), 9):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
              fill=c, width=6)


def icon_probe(d, x, y, s, c, _c2=None):
    # little rocket: nose, body, fins, window, flame
    d.polygon([(x + s * 0.5, y + s * 0.02), (x + s * 0.32, y + s * 0.3),
               (x + s * 0.68, y + s * 0.3)], fill=c)
    d.rectangle([x + s * 0.32, y + s * 0.3, x + s * 0.68, y + s * 0.72],
                fill=c)
    d.polygon([(x + s * 0.32, y + s * 0.55), (x + s * 0.12, y + s * 0.78),
               (x + s * 0.32, y + s * 0.72)], fill=c)
    d.polygon([(x + s * 0.68, y + s * 0.55), (x + s * 0.88, y + s * 0.78),
               (x + s * 0.68, y + s * 0.72)], fill=c)
    d.ellipse([x + s * 0.42, y + s * 0.4, x + s * 0.58, y + s * 0.56],
              fill=PAPER)
    d.polygon([(x + s * 0.5, y + s * 0.98), (x + s * 0.4, y + s * 0.76),
               (x + s * 0.6, y + s * 0.76)], fill=(224, 164, 88))


TILES = [
    ("SHENZHEN \u00b7 APEC", "TRUMP, XI & PUTIN MEET",
     "First three-way summit as APEC gathers in China", icon_globe,
     (178, 58, 32)),
    ("WASHINGTON", "JEFFRIES FOR SPEAKER",
     "Democrats nominate him; would be first Black Speaker",
     icon_capitol, (18, 28, 61)),
    ("MIDDLE EAST", "U.S.\u2013IRAN FIRE WIDENS",
     "Iran hits a U.S. base in Kuwait and Bahrain again",
     icon_burst, (178, 58, 32)),
    ("BRUSSELS", "\u20ac45BN LOAN FOR UKRAINE",
     "EU plan repaid only once Russia pays reparations",
     icon_euro, (0, 122, 122)),
    ("INDIA", "CYCLONE AKVAN NEARS",
     "Severe storm off the east coast; landfall due Friday",
     icon_spiral, (0, 122, 122)),
    ("SPACE", "VOYAGER 1, A LIGHT-DAY OUT",
     "NASA confirms the farthest human-made object",
     icon_probe, (18, 28, 61)),
]


def draw_lead(d, img):
    """Night skyline over Vice City: gradient sky, lit towers, palm
    silhouettes; headline sits in a solid ink band below the scene."""
    x0, y0, x1, y1 = 0, 112, W, 300
    for yy in range(y0, y1):
        t = (yy - y0) / (y1 - y0)
        r = int(DUSK_TOP[0] + (DUSK_BOT[0] - DUSK_TOP[0]) * t)
        g = int(DUSK_TOP[1] + (DUSK_BOT[1] - DUSK_TOP[1]) * t)
        b = int(DUSK_TOP[2] + (DUSK_BOT[2] - DUSK_TOP[2]) * t)
        d.line([(x0, yy), (x1, yy)], fill=(r, g, b))
    # low sun
    d.ellipse([W - 210, 150, W - 110, 250], fill=(255, 190, 90))
    # skyline
    rng = random.Random(20261119)
    base = y1
    x = 8
    while x < W - 8:
        bw = rng.randint(34, 74)
        bh = rng.randint(60, 165)
        d.rectangle([x, base - bh, x + bw, base], fill=(12, 8, 28))
        for wy in range(base - bh + 10, base - 8, 16):
            for wx in range(x + 7, x + bw - 6, 14):
                if rng.random() < 0.45:
                    d.rectangle([wx, wy, wx + 6, wy + 8],
                                fill=(255, 214, 120) if rng.random() < 0.7
                                else CYAN)
        # rooftop beacon
        if rng.random() < 0.5:
            d.ellipse([x + bw / 2 - 3, base - bh - 8, x + bw / 2 + 3,
                       base - bh - 2], fill=PINK)
        x += bw + rng.randint(4, 14)
    # neon strip along the water line
    d.rectangle([0, base - 4, W, base], fill=PINK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 110], fill=NAVY)
    d.rectangle([0, 106, W, 112], fill=GOLD)
    text(d, (W / 2, 12), "THE WORLD IN ONE DAY", BOLD(56), WHITE,
         anchor="ma")
    text(d, (W / 2, 70), "THURSDAY  \u00b7  19 NOVEMBER 2026",
         BOLD(27), GOLD, anchor="ma")

    # ---- lead story
    draw_lead(d, img)
    d.rectangle([0, 300, W, 402], fill=INK)
    text(d, (24, 310), "GTA VI IS HERE", BOLD(48), WHITE)
    text(d, (W - 24, 322), "CULTURE \u00b7 TOP STORY", BOLD(20), PINK,
         anchor="ra")
    text(d, (24, 364),
         "After 13 years, Rockstar's epic rolls out worldwide at midnight",
         REG(23), (220, 220, 230))

    # ---- story tiles, 2 columns x 3 rows
    gx, gy, gw, gh, gap = 16, 418, 488, 164, 16
    for i, (kick, head, sub, icon, col) in enumerate(TILES):
        x = gx + (i % 2) * (gw + gap)
        y = gy + (i // 2) * (gh + gap)
        d.rectangle([x, y, x + gw, y + gh], fill=WHITE,
                    outline=(200, 192, 172), width=2)
        d.rectangle([x, y, x + gw, y + 34], fill=col)
        text(d, (x + 14, y + 5), kick, BOLD(19), WHITE)
        # pictogram, right side
        icon(d, x + gw - 118, y + 48, 96, col, GOLD)
        # headline, wrapped, left of the icon
        lines = wrap(d, head, BOLD(28), gw - 150)
        yy = y + 42
        for ln in lines[:2]:
            text(d, (x + 14, yy), ln, BOLD(28), INK)
            yy += 33
        slines = wrap(d, sub, REG(19), gw - 150)
        yy += 4
        for ln in slines[:2]:
            text(d, (x + 14, yy), ln, REG(19), SLATE)
            yy += 23

    # ---- also-today strip: gold label inline with two white lines
    fy = 418 + 3 * 164 + 2 * 16  # 942
    d.rectangle([0, fy, W, H], fill=NAVY)
    label = "ALSO TODAY \u2014  "
    lw = d.textlength(label, font=BOLD(21))
    briefs = ("Nvidia: Huang is out for good  \u00b7  "
              "Fed minutes point to more rate rises  \u00b7  "
              "Pew: Islam set to be the largest faith by 2035")
    # line 1 shares its row with the label; line 2 uses the full width
    words = briefs.split()
    used, cur = 0, ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=REG(21)) <= W - 48 - lw:
            cur, used = trial, used + 1
        else:
            break
    line1 = cur
    rest = " ".join(words[used:])
    line2 = wrap(d, rest, REG(21), W - 48)[0] if rest else ""
    text(d, (24, fy + 12), label, BOLD(21), GOLD)
    text(d, (24 + lw, fy + 12), line1, REG(21), WHITE)
    if line2:
        text(d, (24, fy + 42), line2, REG(21), WHITE)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
