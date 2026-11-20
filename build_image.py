#!/usr/bin/env python3
"""Build the 20 November 2026 world-news image (1024x1024 PNG).

Drawn with Pillow only: flat colours, real text, no photos, no AI art.
Every story below was checked against news reported on 20 November 2026.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (251, 248, 241)
INK = (17, 17, 17)
GREY = (90, 90, 90)
RED = (180, 35, 24)
BLUE = (29, 78, 216)
TEAL = (15, 118, 110)
AMBER = (180, 83, 9)
PURPLE = (109, 40, 217)
GREEN = (21, 128, 61)
LIGHT = (238, 232, 220)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, fill=INK, leading=6):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def tag(draw, x, y, text, color):
    f = font(SANS_B, 20)
    tw = draw.textlength(text, font=f) + 20
    draw.rounded_rectangle([x, y, x + tw, y + 30], radius=4, fill=color)
    draw.text((x + 10, y + 4), text, font=f, fill=(255, 255, 255))
    return tw


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# outer border
d.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)

# ---- masthead ----
d.text((512, 28), "THE WORLD TODAY", font=font(SERIF_B, 62),
       fill=INK, anchor="ma")
d.text((512, 104), "FRIDAY  •  20 NOVEMBER 2026", font=font(SANS_B, 34),
       fill=RED, anchor="ma")
d.line([40, 158, 984, 158], fill=INK, width=3)
d.text((512, 168), "Six stories that defined the day, from Shenzhen to Antalya,",
       font=font(SANS, 22), fill=GREY, anchor="ma")
d.text((512, 196), "Wall Street to Gaza.",
       font=font(SANS, 22), fill=GREY, anchor="ma")
d.line([40, 232, 984, 232], fill=INK, width=2)

# ---- lead story ----
d.rectangle([40, 248, 984, 452], fill=(255, 255, 255), outline=INK, width=2)
tag(d, 60, 266, "LEAD  •  SHENZHEN", RED)
d.text((60, 306), "Trump, Xi and Putin issue",
       font=font(SERIF_B, 40), fill=INK)
d.text((60, 352), "\u2018peace declaration\u2019",
       font=font(SERIF_B, 40), fill=INK)
para(d, 60, 402, "First-ever US\u2013China\u2013Russia summit ends with a pledge that "
   "\u2018a nuclear war cannot be won\u2019 \u2014 but no arms cuts, and no mention "
   "of Ukraine or Iran.", font(SANS, 21), 900, leading=4)
# three leaders, one declaration: keep the lead box clean, no icon

# ---- 2x2 grid ----
stories = [
    ("MARKETS  •  NEW YORK", BLUE, "Anthropic\u2019s record $81bn debut",
     "Shares open at $111.50, up 34% on the $83 IPO price, and close "
     "at $97.17 \u2014 the biggest listing ever."),
    ("CLIMATE  •  ANTALYA", TEAL, "COP31 draft drops fossil fuels",
     "Thursday's draft in Turkey deletes any phase-out call; talks push "
     "electrification instead, to 35% by 2035."),
    ("UKRAINE  •  BERLIN", AMBER, "UK pledges 1,000+ drones for Kyiv",
     "\u00a3260m package of long-range strike drones, able to fly "
     "1,000 km, at the Coalition of the Willing."),
    ("GAZA  •  NUSEIRAT", PURPLE, "Israel ends Gaza ground raid",
     "Tanks pull back after a day-long operation; residents return "
     "to Nuseirat and Bureij as the road reopens."),
]
gx, gy = [40, 522], [468, 688]
gw, gh = 462, 204
for idx, (tg, col, head, body) in enumerate(stories):
    x = gx[idx % 2]
    y = gy[idx // 2]
    d.rectangle([x, y, x + gw, y + gh], fill=(255, 255, 255),
                outline=INK, width=2)
    tag(d, x + 16, y + 14, tg, col)
    yy = para(d, x + 16, y + 56, head, font(SERIF_B, 27), gw - 32, leading=2)
    para(d, x + 16, yy + 4, body, font(SANS, 20), gw - 32, leading=4)

# ---- bottom strip: Europe ----
d.rectangle([40, 908, 984, 984], fill=(17, 17, 17))
d.text((60, 920), "EUROPE  •  25 COUNTRIES",
       font=font(SANS_B, 20), fill=(251, 200, 80))
d.text((60, 946), "Youth march across Europe on 20 November \u2014 housing, pay and military spending.",
       font=font(SANS, 20), fill=(255, 255, 255))

# footer line above bottom strip is the box edge; add source line inside border
d.text((512, 992), "Reported 20 November 2026  •  Reuters  •  AFP  •  WSJ  •  CNA  •  Dawn  •  Straits Times",
       font=font(SANS, 15), fill=GREY, anchor="ma")

img.save("/home/hatch/workspace/make-fun/news-image-entry/entry.png",
         optimize=True)
print("saved entry.png", img.size)
