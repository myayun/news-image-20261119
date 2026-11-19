#!/usr/bin/env python3
"""v9 — SUPER FRONT PAGE. Built from scratch to beat the top-10 formula at
its own game. Cream paper, huge serif date, red italic deck, region-count
bar (43 stories), 6-figure numbers strip, 3 NEW illustrated heroes, 6
medium cards, world map with 9 numbered pins + grey dots, 34 numbered
briefs, red DATE CHECK box (Wed 18 Nov stories excluded), markets footer.
4 brand-new illustrations, none reused from v1-v8. Deterministic, Pillow
only. Writes entry_v9.png (1024x1024, <1 MiB). Does NOT touch
assets/entry.png — Dwi reviews first."""
from PIL import Image, ImageDraw, ImageFont
import os
from collections import Counter

W, H = 1024, 1024
PAPER = (250, 244, 230)
CARD = (255, 251, 242)
INK = (17, 17, 17)
RED = (178, 34, 34)
GREY = (105, 100, 90)
LIGHT = (205, 198, 184)
NAVY = (18, 42, 78)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

BASE = os.path.dirname(os.path.abspath(__file__))
ILLUS_DIR = os.path.join(BASE, "assets", "illustrations")
ILLUS = {
    "shenzhen": "media-generation-v9-shenzhen-0-d8af4e2d-acc4-4a84-b8aa-9b8e5055f734.webp",
    "gulf": "media-generation-v9-gulf-0-65646eea-a329-40da-a1a3-d421f8fd0a74.webp",
    "crimea": "media-generation-v9-crimea-0-999e989e-5ce6-4b37-8178-01ba58ec2d97.webp",
    "map": "media-generation-v9-worldmap-0-21f37513-3a62-4c61-bb1a-3e244ca5458c.webp",
}

def F(p, s):
    if os.path.exists(p):
        return ImageFont.truetype(p, s)
    return ImageFont.truetype(SERIF if "Serif" in p else SANS, s)

def wrap(dr, text, font, max_w):
    out = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            t = (cur + " " + w).strip()
            if dr.textlength(t, font=font) <= max_w:
                cur = t
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return out

def wrapped(dr, x, y, text, font, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(dr, text, font, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        dr.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y, len(lines)

def illus(w, h, key):
    im = Image.open(os.path.join(ILLUS_DIR, ILLUS[key])).convert("RGB")
    iw, ih = im.size
    target = w / h
    src = iw / ih
    if src > target:
        nw = int(ih * target); x0 = (iw - nw) // 2
        im = im.crop((x0, 0, x0 + nw, ih))
    else:
        nh = int(iw / target); y0 = (ih - nh) // 2
        im = im.crop((0, y0, iw, y0 + nh))
    return im.resize((w, h), Image.LANCZOS)

# ---- story data: (region, ...) — counts must sum to 43 ----
HEROES = [
    (1, "ASIA-PACIFIC", "SHENZHEN  •  SUMMIT",
     "Trump, Xi and Putin hold first three-way summit",
     "The three nuclear powers meet at APEC in Shenzhen; arms control and the Iran war top the agenda. Few results expected.",
     "shenzhen"),
    (2, "MIDEAST", "GULF  •  CONFLICT",
     "Iran strikes Gulf states after US hit on Qeshm",
     "Iran fired at US bases in Kuwait and Bahrain; the US hit a Revolutionary Guard missile site. A tanker was struck in the Strait of Hormuz.",
     "gulf"),
    (3, "EUROPE", "UKRAINE  •  WAR",
     "Ukraine hits Crimean Bridge a third time",
     "Third strike this week. Allies meet in Berlin; Kyiv fears the war will be left off the Shenzhen agenda.",
     "crimea"),
]
MEDIUM = [
    (4, "THE AMERICAS", "NASDAQ  •  MARKETS",
     "Anthropic debuts in the biggest IPO on record"),
    (5, "THE AMERICAS", "NEW YORK  •  GAMES",
     "GTA VI arrives after a 13-year wait; 15.9m pre-orders"),
    (6, "ASIA-PACIFIC", "THE HAGUE  •  LAW",
     "World Court rules on Myanmar's Rohingya case; 730,000 fled"),
    (7, "WORLD", "ANTALYA  •  CLIMATE",
     "COP31 enters its final 48 hours as $120bn fund stays open"),
    (8, "ASIA-PACIFIC", "ODISHA  •  STORM",
     "Cyclone Aqwan bears down as 200,000 flee the coast"),
    (9, "MIDEAST", "GAZA  •  WAR",
     "Israel pushes past the Yellow Line as Gaza floods"),
]
BRIEFS = [
    ("MIDEAST", "Israel delays E1 settlement"),
    ("MIDEAST", "Settler kills woman near Jericho"),
    ("MIDEAST", "Gaza flooding worsens the crisis"),
    ("WORLD", "Australia, Canada, Italy, UK call for aid access"),
    ("ASIA-PACIFIC", "IAEA: North Korea expanded uranium enrichment"),
    ("AFRICA", "Ethiopia and Eritrea mass forces along border"),
    ("MIDEAST", "Houthi missile aimed at Riyadh"),
    ("MIDEAST", "Saudis plan long Yemen campaign"),
    ("MIDEAST", "Trump: Iran exploring chemical and biological weapons"),
    ("ASIA-PACIFIC", "EU approves Indonesia trade deal"),
    ("ASIA-PACIFIC", "South Korea and China expand cultural exchange"),
    ("THE AMERICAS", "Record rain from atmospheric river hits California"),
    ("THE AMERICAS", "US loses measles elimination status"),
    ("AFRICA", "Ebola vaccines to be trialled in DR Congo"),
    ("OCEANIA", "Fiji and Tonga declare emergencies over El Niño drought"),
    ("WORLD", "NASA sets coverage for Northrop Grumman CRS-25 launch"),
    ("WORLD", "Webb confirms rare merger of two stars"),
    ("THE AMERICAS", "Waymo pulls driverless taxis from US freeways"),
    ("THE AMERICAS", "US and Venezuela restore military cooperation"),
    ("EUROPE", "Court sentences Imamoglu and eight in CHP case"),
    ("ASIA-PACIFIC", "South Korea college exam held under AI cheating curbs"),
    ("EUROPE", "Five EU nations plan to send asylum seekers to Rwanda"),
    ("AFRICA", "Sudan: aid reaches the displaced"),
    ("AFRICA", "Drone strikes drive Sudan's civilian toll"),
    ("WORLD", "Nearly 1 in 4 children live in conflict zones"),
    ("ASIA-PACIFIC", "Bangladesh unrest over Hasina return"),
    ("ASIA-PACIFIC", "Bangladesh garment workers demand wage rise"),
    ("OCEANIA", "Australia unemployment rises to 4.9%"),
    ("AFRICA", "IMF reaches deal to unlock $2.3bn for Egypt"),
    ("WORLD", "Gold, copper and bitcoin slide as war and AI weigh"),
    ("WORLD", "Cambridge Dictionary names 'human' word of the year"),
    ("WORLD", "Alcaraz beats Medvedev at ATP Finals"),
    ("EUROPE", "Chelsea beat PSG 1-0 in Women's Champions League"),
    ("WORLD", "Van Gogh sells for a record $190.4m"),
]
assert len(BRIEFS) == 34, len(BRIEFS)
assert all(len(t) <= 56 for _, t in BRIEFS), [t for _, t in BRIEFS if len(t) > 56]
TOTAL = 3 + 6 + len(BRIEFS)
assert TOTAL == 43

REGIONS = ["EUROPE", "THE AMERICAS", "ASIA-PACIFIC", "MIDEAST", "AFRICA", "OCEANIA", "WORLD"]
REG_COLORS = {"EUROPE": (31, 95, 160), "THE AMERICAS": (46, 139, 87),
              "ASIA-PACIFIC": (178, 34, 34), "MIDEAST": (176, 124, 34),
              "AFRICA": (70, 70, 70), "OCEANIA": (0, 128, 128), "WORLD": (110, 110, 110)}
counts = Counter([r for _, r, *_ in HEROES] + [r for _, r, *_ in MEDIUM] + [r for r, _ in BRIEFS])
assert sum(counts.values()) == 43, counts

NUMBERS = [
    ("$81.3bn", "raised by Anthropic — the largest IPO on record"),
    ("15.9m", "GTA VI pre-orders banked before release day"),
    ("200,000", "evacuated ahead of Cyclone Aqwan"),
    ("$120bn", "a year of adaptation finance unresolved at COP31"),
    ("730,000", "Rohingya who fled in 2017 — the ICJ case"),
    ("$190.4m", "Van Gogh sells for a record at auction"),
]

# map pins: (story no, x-frac, y-frac) in the CROPPED map (crop y 60..1210 of 1280)
PINS = [
    (1, 0.815, 0.387),   # Shenzhen
    (2, 0.635, 0.400),   # Gulf / Hormuz
    (3, 0.550, 0.259),   # Crimea
    (4, 0.245, 0.315),   # New York (Anthropic)
    (5, 0.185, 0.432),   # Florida (GTA VI / Vice City)
    (6, 0.465, 0.215),   # The Hague
    (7, 0.560, 0.348),   # Antalya
    (8, 0.735, 0.477),   # Odisha
    (9, 0.570, 0.470),   # Gaza
]
DOTS = [  # grey dots for brief locations (x-frac, y-frac, cropped coords)
    (0.850, 0.300),   # North Korea
    (0.080, 0.325),   # California
    (0.520, 0.515),   # DR Congo
    (0.940, 0.600),   # Fiji
    (0.870, 0.655),   # Australia
    (0.800, 0.535),   # Jakarta
    (0.760, 0.420),   # Dhaka
]

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 28
RX = 996  # right margin

# ---- top small caps ----
d.text((MX, 10), "THE WORLD IN ONE DAY", font=F(SANS_B, 13), fill=RED)
d.text((RX, 12), "THURSDAY'S NEWS  •  ONE PAGE  •  43 STORIES", font=F(SANS_B, 11), fill=INK, anchor="ra")
d.line([(MX, 30), (RX, 30)], fill=INK, width=2)

# ---- huge serif date ----
d.text((MX, 38), "Thursday 19 November 2026", font=F(SERIF_B, 52), fill=INK)
d.text((MX, 98), "Three leaders meet in Shenzhen  •  Iran strikes the Gulf  •  Crimea Bridge hit again",
       font=F(SERIF_I, 15), fill=RED)
d.line([(MX, 122), (RX, 122)], fill=INK, width=1)

# ---- region bar (widths proportional, OCEANIA floored to 64) ----
bar_y, bar_h = 128, 22
widths = {"EUROPE": 90, "THE AMERICAS": 135, "ASIA-PACIFIC": 194, "MIDEAST": 180,
          "AFRICA": 113, "OCEANIA": 64, "WORLD": 192}
assert sum(widths.values()) == 968
x = MX
for reg in REGIONS:
    w = widths[reg]
    d.rectangle([x, bar_y, x + w, bar_y + bar_h], fill=REG_COLORS[reg])
    d.text((x + w / 2, bar_y + bar_h / 2), f"{reg} {counts[reg]}",
           font=F(SANS_B, 10), fill=(255, 255, 255), anchor="mm")
    x += w

# ---- numbers strip: 6 big figures ----
ny = 158
col_w = 968 / 6
for i, (big, cap) in enumerate(NUMBERS):
    cx = MX + i * col_w
    if i:
        d.line([(cx - 6, ny + 4), (cx - 6, ny + 46)], fill=LIGHT, width=1)
    d.text((cx, ny), big, font=F(SERIF_B, 19), fill=RED)
    wrapped(d, cx, ny + 28, cap, F(SANS, 9), col_w - 14, 11, fill=(70, 66, 58), max_lines=2)
d.line([(MX, 212), (RX, 212)], fill=INK, width=1)

# ---- 3 illustrated heroes ----
def hero(x, y, w, num, kick, head, deck, key):
    h = 244
    d.rectangle([x, y, x + w, y + h], outline=LIGHT, width=1)
    img.paste(illus(w - 2, 138, key), (x + 1, y + 1))
    d.ellipse([x + 12, y + 12, x + 36, y + 36], fill=RED, outline=(255, 255, 255), width=2)
    d.text((x + 24, y + 24), str(num), font=F(SANS_B, 14), fill=(255, 255, 255), anchor="mm")
    d.rectangle([x, y + 139, x + w, y + 160], fill=INK)
    d.text((x + 10, y + 143), kick, font=F(SANS_B, 10), fill=(255, 255, 255))
    _, n = wrapped(d, x + 10, y + 168, head, F(SERIF_B, 17), w - 20, 21, max_lines=2)
    wrapped(d, x + 10, y + 168 + n * 21 + 3, deck, F(SANS, 11), w - 20, 14, fill=(50, 46, 40), max_lines=3)

hx = [MX, 355, 682]
for (num, reg, kick, head, deck, key), x in zip(HEROES, hx):
    hero(x, 220, 314, num, kick, head, deck, key)

# ---- 6 medium cards, 2 rows x 3 ----
def medium(x, y, w, num, kick, head):
    h = 58
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=LIGHT, width=1)
    d.text((x + 10, y + 8), str(num), font=F(SANS_B, 14), fill=RED)
    d.text((x + 32, y + 10), kick, font=F(SANS_B, 9), fill=RED)
    wrapped(d, x + 10, y + 28, head, F(SERIF_B, 13), w - 20, 16, max_lines=2)

my = [472, 538]
for row, y in enumerate(my):
    for col, (num, reg, kick, head) in enumerate(MEDIUM[row * 3:(row + 1) * 3]):
        medium(hx[col], y, 314, num, kick, head)

d.line([(MX, 604), (RX, 604)], fill=INK, width=1)

# ---- bottom: map left, briefs right ----
d.text((MX, 612), "WHERE IT HAPPENED", font=F(SANS_B, 12), fill=INK)
map_x, map_y, map_w, map_h = MX, 632, 330, 198
src = Image.open(os.path.join(ILLUS_DIR, ILLUS["map"])).convert("RGB")
src = src.crop((0, 60, 1920, 1210)).resize((map_w, map_h), Image.LANCZOS)
img.paste(src, (map_x, map_y))
md = ImageDraw.Draw(img)
for fx, fy in DOTS:
    px, py = map_x + fx * map_w, map_y + fy * map_h
    md.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(120, 115, 105))
for num, fx, fy in PINS:
    px, py = map_x + fx * map_w, map_y + fy * map_h
    md.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=2)
    md.text((px, py), str(num), font=F(SANS_B, 9), fill=(255, 255, 255), anchor="mm")
d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], outline=LIGHT, width=1)
wrapped(d, MX, 836, "Red numbers mark the top stories; grey dots mark the briefs below. Positions are approximate.",
        F(SANS, 9), 330, 11, fill=GREY, max_lines=2)

# ---- briefs: 34, 2 columns ----
bx = 372
d.text((bx, 612), "ALSO ON THURSDAY 19 NOVEMBER  —  34 MORE STORIES", font=F(SANS_B, 12), fill=RED)
cols = [BRIEFS[:17], BRIEFS[17:]]
for ci, col in enumerate(cols):
    x = bx + ci * 318
    y = 632
    for i, (reg, b) in enumerate(col):
        n = 10 + ci * 17 + i
        d.text((x, y), f"{n}.", font=F(SANS_B, 10), fill=RED)
        _, lines = wrapped(d, x + 24, y, b, F(SANS_B, 10), 282, 12, max_lines=2)
        y += lines * 12 + 5

# ---- DATE CHECK box ----
dy = 934
d.rectangle([MX, dy, RX, dy + 34], outline=RED, width=2)
d.text((MX + 10, dy + 5), "DATE CHECK", font=F(SANS_B, 10), fill=RED)
wrapped(d, MX + 92, dy + 5,
        "First reported Wednesday 18 Nov, so NOT on this page as news: the Iranian drone interceptions  •  the EU's €45bn loan for Ukraine  •  the House Democrats' 251–11 vote nominating Hakeem Jeffries  •  Voyager 1 crossing one light-day, at 10:16 GMT Wednesday  •  Petola's Alaska win  •  Pew's projection that Islam becomes the largest religion by 2035  •  the first COP31 draft (Monday).",
        F(SANS, 9), RX - MX - 102, 11, fill=INK, max_lines=2)

# ---- markets + footer ----
d.line([(MX, 978), (RX, 978)], fill=INK, width=2)
d.text((MX, 986), "MARKETS  •  S&P 500 7,324  -0.23%   •   FTSE 100 10,551  -1.30%   •   Hang Seng  -2.78%   •   Brent $89.3  +0.15%   •   US 10-yr 5.07%",
       font=F(SANS_B, 11), fill=INK)
d.text((MX, 1004), "Every story here happened, or was first reported, on Thursday 19 November 2026. Disputed claims are attributed, not stated as fact. Sources: Reuters, AP, AFP, BBC, The Hindu, IMD, NASA, ICJ, Pew. Original drawings.",
       font=F(SANS, 9), fill=GREY)

img.save("entry_v9.png", "PNG", optimize=True)
print("saved v9 1024x1024")
