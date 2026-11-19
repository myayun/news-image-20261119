#!/usr/bin/env python3
"""v7 — v6 improved. Same stories, bigger pictures: heroes 150px tall
with red number badges, numbers strip with 4 big red figures, tighter
briefs. White paper, big serif masthead, 3 illustrated heroes, 2
illustrated wide cards, 35 numbered briefs, markets strip. Deterministic,
Pillow only. Writes assets/entry.png and entry.png (1024x1024, <1 MiB)."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1024, 1024
PAPER = (255, 255, 255)
INK = (17, 17, 17)
RED = (178, 34, 34)
GREY = (110, 110, 110)
LIGHT = (225, 225, 225)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

ILLUS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "illustrations")
ILLUS = {
    "hero_shenzhen": "hero_shenzhen.webp",
    "gulf": "media-generation-gulf-0-942cdce1-0a01-468b-89a7-c747f8f96594.webp",
    "crimea": "media-generation-crimea-0-081602c8-c73b-4c35-aeee-4a9e46eaca2f.webp",
    "hero_anthropic": "hero_anthropic.webp",
    "hero_gta": "hero_gta.webp",
}

def F(p, s): return ImageFont.truetype(p, s)
def wrap(dr, text, font, max_w):
    out = []
    for para in text.split("\n"):
        cur = ""
        for w in para.split():
            t = (cur + " " + w).strip()
            if dr.textlength(t, font=font) <= max_w: cur = t
            else:
                if cur: out.append(cur)
                cur = w
        if cur: out.append(cur)
    return out
def wrapped(dr, x, y, text, font, max_w, leading, fill=INK, max_lines=None):
    lines = wrap(dr, text, font, max_w)
    if max_lines: lines = lines[:max_lines]
    for ln in lines:
        dr.text((x, y), ln, font=font, fill=fill); y += leading
    return y, len(lines)
def illus(w, h, key):
    """Center-crop a bundled illustration to w x h. Deterministic."""
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

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- masthead ----
d.text((32, 22), "THE WORLD IN ONE DAY", font=F(SERIF_B, 46), fill=INK)
d.text((32, 82), "Thursday 19 November 2026  •  40 stories  •  One image", font=F(SANS_B, 14), fill=RED)
d.text((992, 84), "5 pictures drawn for this page", font=F(SANS, 11), fill=GREY, anchor="ra")
d.line([(32, 108), (992, 108)], fill=INK, width=3)
d.line([(32, 113), (992, 113)], fill=RED, width=1)

# ---- 3 illustrated heroes, bigger, with red number badges ----
def hero(x, y, w, num, kick, head, deck, key):
    h = 270
    d.rectangle([x, y, x + w, y + h], outline=LIGHT, width=1)
    img.paste(illus(w - 2, 150, key), (x + 1, y + 1))
    d.ellipse([x + 12, y + 12, x + 36, y + 36], fill=RED, outline=(255, 255, 255), width=2)
    d.text((x + 24, y + 24), str(num), font=F(SANS_B, 14), fill=(255, 255, 255), anchor="mm")
    d.rectangle([x, y + 151, x + w, y + 173], fill=INK)
    d.text((x + 10, y + 155), kick, font=F(SANS_B, 10), fill=(255, 255, 255))
    _, n = wrapped(d, x + 10, y + 181, head, F(SERIF_B, 18), w - 20, 22, max_lines=2)
    wrapped(d, x + 10, y + 181 + n * 22 + 4, deck, F(SANS, 11), w - 20, 14, fill=(50, 50, 50), max_lines=3)

hero(32, 124, 304, 1, "SHENZHEN  •  SUMMIT",
     "Trump, Xi and Putin meet in Shenzhen",
     "First three-way summit of the three nuclear powers, on the APEC sidelines. Agenda: Ukraine, Iran, nuclear arms, trade and AI. Few results expected.",
     "hero_shenzhen")
hero(352, 124, 304, 2, "GULF  •  CONFLICT",
     "Iran strikes Gulf states after US hit on Qeshm",
     "Iran fired at US bases in Kuwait and Bahrain; the US hit a Revolutionary Guard missile site. A tanker was struck in the Strait of Hormuz.",
     "gulf")
hero(672, 124, 320, 3, "UKRAINE  •  WAR",
     "Ukraine hits Crimean Bridge a third time",
     "Third strike this week, as allies meet in Berlin and the EU proposes a €45bn loan for Ukraine, to be repaid after Russia pays reparations.",
     "crimea")

# ---- 2 illustrated wide cards, with number badges ----
def wide(x, y, w, num, kick, head, deck, key):
    h = 96
    d.rectangle([x, y, x + w, y + h], outline=LIGHT, width=1)
    img.paste(illus(150, h - 2, key), (x + 1, y + 1))
    d.ellipse([x + 8, y + 8, x + 28, y + 28], fill=RED, outline=(255, 255, 255), width=2)
    d.text((x + 18, y + 18), str(num), font=F(SANS_B, 12), fill=(255, 255, 255), anchor="mm")
    tx = x + 160
    d.text((tx, y + 8), kick, font=F(SANS_B, 10), fill=RED)
    _, n = wrapped(d, tx, y + 26, head, F(SERIF_B, 16), w - 170, 20, max_lines=2)
    wrapped(d, tx, y + 26 + n * 20 + 3, deck, F(SANS, 11), w - 170, 14, fill=(50, 50, 50), max_lines=2)

wide(32, 406, 472, 4, "BUSINESS  •  RECORD IPO",
     "Anthropic prices record IPO at $83 a share",
     "The AI firm's listing did not lift Asian shares. Hang Seng fell 2.78%, FTSE 100 fell 1.3%.",
     "hero_anthropic")
wide(520, 406, 472, 5, "CULTURE  •  GAMES",
     "GTA VI goes on sale after 13 years",
     "Gamers enter Vice City as Grand Theft Auto VI begins its global rollout.",
     "hero_gta")

# ---- numbers strip: 4 big red figures ----
nums = [("$81.3bn", "Anthropic raises the largest IPO on record"),
        ("15.9m", "GTA VI pre-orders banked before release"),
        ("200,000", "evacuated ahead of Cyclone Aqwan"),
        ("$190.4m", "Van Gogh sells for a record at auction")]
x = 32
for big, cap in nums:
    d.text((x, 514), big, font=F(SERIF_B, 22), fill=RED)
    wrapped(d, x, 540, cap, F(SANS, 10), 220, 12, fill=(60, 60, 60), max_lines=2)
    x += 240
d.line([(32, 570), (992, 570)], fill=INK, width=1)

# ---- briefs: 35 more stories, 3 columns ----
d.text((32, 580), "THE DAY IN BRIEF  —  35 more stories, numbered", font=F(SANS_B, 14), fill=INK)
d.line([(32, 602), (992, 602)], fill=INK, width=2)

briefs = [
    "UN court to rule on Myanmar Rohingya genocide case",
    "Israel delays E1 settlement; settler kills woman near Jericho",
    "Israel ground operation beyond Yellow Line in central Gaza",
    "Gaza flooding: Australia, Canada, Italy, UK call for aid access",
    "IAEA: North Korea expanded uranium enrichment",
    "Ethiopia and Eritrea mass forces along border",
    "Houthi missile aimed at Riyadh; Saudis plan long Yemen campaign",
    "Trump: Iran exploring chemical and biological weapons",
    "EU approves Indonesia trade deal to counter US tariffs",
    "South Korea and China agree to expand cultural exchange",
    "Record rain from atmospheric river hits California",
    "Cyclone Aqwan to hit India's east coast",
    "COP31 deadlock persists as countries launch climate check",
    "US loses measles elimination status",
    "Strain-specific Ebola vaccines to be trialled in DR Congo",
    "Fiji and Tonga declare emergencies over El Niño drought",
    "NASA sets coverage for Northrop Grumman CRS-25 launch",
    "Voyager 1 reaches one light-day from Earth",
    "Webb confirms rare merger of supergiant and sun-like star",
    "Waymo pulls driverless taxis from US freeways",
    "Democrats win Alaska seat, take 56-seat Senate majority",
    "US and Venezuela restore military cooperation",
    "Court sentences Imamoglu and eight others in CHP case",
    "Pew projects Islam to pass Christianity by 2035",
    "South Korea college exam held under AI cheating curbs",
    "Five EU nations plan to send asylum seekers to Rwanda",
    "Sudan: aid for displaced as drones drive civilian toll",
    "Nearly 1 in 4 children live in conflict zones",
    "Bangladesh unrest over Hasina return and wage demands",
    "Australia unemployment rises to 4.9%",
    "IMF reaches deal to unlock $2.3bn for Egypt",
    "Gold, copper and bitcoin slide as war and AI weigh",
    "Cambridge Dictionary names 'human' word of the year",
    "Alcaraz beats Medvedev at ATP Finals",
    "Chelsea beat PSG 1-0 in Women's Champions League",
]
cols = [briefs[:12], briefs[12:24], briefs[24:]]
for ci, col in enumerate(cols):
    x = 32 + ci * 328
    y = 614
    for i, b in enumerate(col):
        n = 6 + ci * 12 + i
        d.text((x, y), f"{n}.", font=F(SANS_B, 10), fill=RED)
        _, lines = wrapped(d, x + 24, y, b, F(SANS_B, 10), 280, 13, max_lines=2)
        y += lines * 13 + 8

# ---- markets + footer ----
d.line([(32, 924), (992, 924)], fill=INK, width=2)
d.text((32, 936), "MARKETS  •  S&P 500 7,324  -0.23%   •   FTSE 100 10,551  -1.30%   •   Hang Seng  -2.78%   •   Brent $89.3  +0.15%   •   US 10-yr 5.07%", font=F(SANS_B, 11), fill=INK)
d.text((32, 962), "Every story here happened, or was first reported, on Thursday 19 November 2026. Sources: Reuters, AP, AFP, BBC, The Hindu, IMD, NASA, ICJ, Pew. Illustrations drawn for this page.", font=F(SANS, 10), fill=GREY)

img.save("assets/entry.png", "PNG", optimize=True)
img.save("entry.png", "PNG", optimize=True)
print("saved v7 1024x1024")
