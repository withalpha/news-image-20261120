#!/usr/bin/env python3
"""Build the 20 November 2026 world-news image (1024x1024 PNG).

Drawn with Pillow only: flat colours, real text, no photos, no AI art.
Every story below was checked against news reported on 20 November 2026.

Layout, top to bottom:
  - masthead: paper name, the date in red, a one-line standfirst
  - lead story: a full-width white box for the Shenzhen summit
  - 2x2 grid: markets, climate, Ukraine, Gaza
  - bottom strip: a black bar for the marches across Europe
  - footer: the sources the stories were reported by

Palette: warm paper background, near-black ink, one strong colour
per story tag. Text is DejaVu Serif bold for headlines and DejaVu
Sans for body copy, so the image renders the same anywhere.
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


def wrap_text(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels, word by word."""
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


def draw_para(draw, x, y, text, fnt, max_w, fill=INK, leading=6):
    """Draw a wrapped paragraph, returning the y below its last line."""
    lines = wrap_text(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def draw_tag(draw, x, y, text, color):
    """Draw a coloured kicker label, returning its width in pixels."""
    f = font(SANS_B, 20)
    tw = draw.textlength(text, font=f) + 20
    draw.rounded_rectangle([x, y, x + tw, y + 30], radius=4, fill=color)
    draw.text((x + 10, y + 4), text, font=f, fill=(255, 255, 255))
    return tw


def draw_story_box(draw, x, y, kicker, accent, headline, body_text, cell_w, cell_h):
    """Draw one grid cell: white box, tag, headline, body copy."""
    draw.rectangle([x, y, x + cell_w, y + cell_h], fill=(255, 255, 255),
                   outline=INK, width=2)
    draw_tag(draw, x + 16, y + 14, kicker, accent)
    below_head = draw_para(draw, x + 16, y + 56, headline,
                           font(SERIF_B, 27), cell_w - 32, leading=2)
    draw_para(draw, x + 16, below_head + 4, body_text,
              font(SANS, 20), cell_w - 32, leading=4)


def main():
    canvas = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)

    # outer border
    draw.rectangle([8, 8, W - 9, H - 9], outline=INK, width=3)

    # ---- masthead ----
    draw.text((512, 28), "THE WORLD TODAY", font=font(SERIF_B, 62),
              fill=INK, anchor="ma")
    draw.text((512, 104), "FRIDAY  •  20 NOVEMBER 2026", font=font(SANS_B, 34),
              fill=RED, anchor="ma")
    draw.line([40, 158, 984, 158], fill=INK, width=3)
    draw.text((512, 168), "Six stories that defined the day, from Shenzhen to Antalya,",
              font=font(SANS, 22), fill=GREY, anchor="ma")
    draw.text((512, 196), "Wall Street to Gaza.",
              font=font(SANS, 22), fill=GREY, anchor="ma")
    draw.line([40, 232, 984, 232], fill=INK, width=2)

    # ---- lead story ----
    draw.rectangle([40, 248, 984, 452], fill=(255, 255, 255), outline=INK, width=2)
    draw_tag(draw, 60, 266, "LEAD  •  SHENZHEN", RED)
    draw.text((60, 306), "Trump, Xi and Putin issue",
              font=font(SERIF_B, 40), fill=INK)
    draw.text((60, 352), "\u2018peace declaration\u2019",
              font=font(SERIF_B, 40), fill=INK)
    draw_para(draw, 60, 402, "First-ever US\u2013China\u2013Russia summit ends with a pledge that "
              "\u2018a nuclear war cannot be won\u2019 \u2014 but no arms cuts, and no mention "
              "of Ukraine or Iran.", font(SANS, 21), 900, leading=4)
    # three leaders, one declaration: keep the lead box clean, no icon

    # ---- 2x2 grid ----
    grid_stories = [
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
    grid_xs, grid_ys = [40, 522], [468, 688]
    cell_w, cell_h = 462, 204
    for i, (kicker, accent, headline, body_text) in enumerate(grid_stories):
        draw_story_box(draw, grid_xs[i % 2], grid_ys[i // 2], kicker, accent,
                       headline, body_text, cell_w, cell_h)

    # ---- bottom strip: Europe ----
    draw.rectangle([40, 908, 984, 984], fill=(17, 17, 17))
    draw.text((60, 920), "EUROPE  •  25 COUNTRIES",
              font=font(SANS_B, 20), fill=(251, 200, 80))
    draw.text((60, 946), "Youth march across Europe on 20 November \u2014 housing, pay and military spending.",
              font=font(SANS, 20), fill=(255, 255, 255))

    # footer line above bottom strip is the box edge; add source line inside border
    draw.text((512, 992), "Reported 20 November 2026  •  Reuters  •  AFP  •  WSJ  •  CNA  •  Dawn  •  Straits Times",
              font=font(SANS, 15), fill=GREY, anchor="ma")

    canvas.save("/home/hatch/workspace/make-fun/news-image-entry/entry.png",
                optimize=True)
    print("saved entry.png", canvas.size)


if __name__ == "__main__":
    main()
