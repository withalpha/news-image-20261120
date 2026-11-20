#!/usr/bin/env python3
"""Build the make.fun news-image entry: one front page for Friday 20 Nov 2026.

Every story was verified against news sources before it was written here:
each one happened, or was first reported, on Friday 20 November 2026 in at
least one time zone. Stories first reported on 18-19 Nov are excluded on
purpose and named in the DATE CHECK box instead.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (248, 244, 233)
INK = (25, 25, 25)
MUTED = (96, 92, 80)
RED = (158, 27, 27)
NAVY = (22, 34, 46)
PANEL = (238, 232, 214)
RULE = (201, 194, 174)
WHITE = (255, 255, 255)
TEAL = (31, 93, 99)
GOLD = (176, 132, 52)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap_text(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit inside width px."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
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


def draw_para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in wrap_text(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- numbers band
NUMBERS = [
    ("300,000+", "evacuated ahead of Cyclone Akvan"),
    ("\u22125.1%", "Nikkei's Friday fall"),
    ("\u22128.5%", "MSCI Asia-Pacific on the week"),
    ("2.3%", "Japan Oct headline CPI"),
    ("118", "Phillips' historic century vs India"),
    ("8 yrs", "BepiColombo's trip to Mercury"),
]

CHIPS = [
    ("EUROPE 9", (158, 27, 27)),
    ("AMERICAS 6", (31, 93, 99)),
    ("ASIA-PACIFIC 11", (176, 132, 52)),
    ("MIDEAST 4", (96, 92, 80)),
    ("AFRICA 1", (22, 34, 46)),
    ("OCEANIA 2", (90, 60, 120)),
    ("WORLD / SPACE 3", (25, 25, 25)),
]

# ------------------------------------------------------------- featured stories
# (num, place, field, headline, body, source, art)
FEATURED = [
    (1, "ODISHA, INDIA", "CYCLONE",
     "Cyclone Akvan makes landfall in eastern India",
     "Storm crosses near Gopalpur; 300,000+ evacuated, winds 70\u201380 "
     "gusting 90 km/h, 423 rescue teams deployed, schools shut.",
     "IMD, The Hindu", "cyclone"),
    (2, "KYIV, UKRAINE", "WAR",
     "Russia's overnight barrage hits Kyiv",
     "Overnight waves of missiles and ~400 drones hit energy and transport "
     "sites; fires burn in three districts.",
     "Kyiv Independent, CNA", "kyiv"),
    (3, "ANTALYA, T\u00dcRKIYE", "CLIMATE",
     "COP31 reaches its final day deadlocked",
     "Talks close on a 19 Nov draft that omits the fossil-fuel phase-out; "
     "$120bn adaptation finance unresolved; hosts push \"35 by 35\" goal.",
     "UN News, Reuters", "cop"),
    (4, "SEOUL / TOKYO", "MARKETS",
     "AI sell-off sinks Asia to worst week since 2020",
     "Nikkei \u22125.1% to a seven-month low; Kospi \u22125.2%, Taiwan \u22126.2%; "
     "MSCI \u22128.5% on week.",
     "Reuters, Jiji", "markets"),
    (5, "MERCURY", "SPACE",
     "BepiColombo closes in on Mercury after 8 years",
     "ESA/JAXA probe ends 6bn-mile trip; orbit insertion set for Saturday.",
     "ESA, BBC", "bepi"),
    (6, "BRUSSELS", "EUROPE",
     "Burnham joins EU\u2013UK reset summit",
     "Second post-Brexit summit in Brussels; agrifood & "
     "carbon-market links eyed.",
     "EU Council", "summit"),
    (7, "TOKYO", "ECONOMY",
     "Japan inflation hits 2.3%; BoJ hike eyed",
     "Oct headline CPI rises from 2.1%; core 2.2%, above 2% for a second month.",
     "Reuters", "cpi"),
    (8, "BEIJING", "RATES",
     "China holds lending rates for 18th month",
     "1-year LPR stays at 3.0%, 5-year at 3.5% as expected.",
     "PBOC, Reuters", "lpr"),
    (9, "WELLINGTON", "CRICKET",
     "Phillips makes history with 118 vs India",
     "First NZ batter with centuries in all 3 formats vs India in a year; NZ 368.",
     "ICC, AP", "cricket"),
    (10, "ROME", "LABOUR",
     "Italy's CGIL holds 24-hr general strike",
     "Unions rally in ~100 squares against 2027 budget.",
     "CGIL, AFP", "strike"),
    (11, "BARCELONA", "HEALTH",
     "Pancreatic cancer pill shows 60.7% response",
     "Daraxonrasib + chemo in 61 patients, early trial; no control group yet, "
     "Phase III to come.",
     "Reuters", "pill"),
    (12, "EUROPE", "YOUTH",
     "Youth action called in 25+ countries",
     "Youth groups call action over housing, pay and military spending, "
     "20\u201322 Nov.",
     "Malay Mail, UNI Europa", "youth"),
    (13, "WASHINGTON", "DEFENCE",
     "CBO: AUKUS sub sales could shrink US fleet",
     "Supplying 3\u20135 nuclear subs to Australia from 2032 could cut US fleet; "
     "yards build 1.13 a year.",
     "The Guardian", "sub"),
]

# ------------------------------------------------------------------ world briefs
# (num, place, text, source) -- one line each in the finished image
BRIEFS = [
    (14, "SHENZHEN", "APEC ministers issue joint statement as summit week closes.", "APEC"),
    (15, "SEOUL", "Ruling party formally adopts push to impeach Chief Justice Cho Hee-dae.", "Yonhap"),
    (16, "GLOBAL", "UN marks World Children's Day; theme \"My day, my rights, my future\".", "UN News"),
    (17, "NEW DELHI", "Pakistan climate minister in Delhi for SCO talks, first since 2023.", "The Hindu"),
    (18, "HONG KONG", "Goh/Lai upset world No. 5 Guo/Chen 21\u201315, 21\u201315 to reach Open semis.", "The Sun"),
    (19, "TURIN", "Alcaraz\u2013Cobolli & Medvedev\u2013Tiafoe close ATP Finals group play.", "ATP"),
    (20, "WELLINGTON", "Nicholls 175* in 216-run stand with Phillips; NZ 368.", "ICC"),
    (21, "TAIWAN", "Short-sell curbs take effect; stocks down 3.5%+ can't be shorted below close.", "CNA"),
    (22, "KUALA LUMPUR", "Malaysia's monthly trade tops RM400bn for first time.", "NST"),
    (23, "KENYA", "Chief Justice releases state of the Judiciary report.", "Nation"),
    (24, "LONDON", "Save the Children: Gaza 'peace plan' has failed, one year on.", "Save the Children"),
    (25, "QATAR", "U17 World Cup: Australia stun Argentina 2\u20130.", "FIFA"),
    (26, "WASHINGTON", "Trump to hold noon press conference at White House.", "White House"),
    (27, "CALIFORNIA", "SpaceX to launch classified USSF-317 Friday evening from Vandenberg.", "Spaceflight Now"),
    (28, "EUROPE", "Shares head for steepest weekly drop since March; STOXX 600 \u22121% at open.", "Reuters"),
    (29, "GLOBAL", "UN: digital government advances worldwide, but divides persist.", "UN"),
    (30, "PARIS", "Harris to meet Macron in \"courtesy meeting\" amid 2028 speculation.", "Le Monde"),
    (31, "CALIFORNIA", "State launches probe into Nvidia over China chip claims.", "NST"),
    (32, "NEW YORK", "NBA: Grizzlies rout Warriors 126\u201398; Lillard's 33 sinks Bucks.", "Field Level Media"),
    (33, "TOKYO", "India, Japan agree Japanese forces will train in Indian ranges.", "The Hindu"),
    (34, "YEMEN", "Houthis accuse Saudi forces of killing 19 in attack on civilian boat.", "NST"),
    (35, "GAZA", "Nearly 65,000 tents approved for entry as winterisation continues.", "Scoop"),
    (36, "FLORIDA", "Jeeno, Davidson and Kim share LPGA Tour Championship lead at 7-under.", "NST"),
]

DATE_CHECK = (
    "DATE CHECK \u2014 First reported 18\u201319 Nov, NOT Friday's news: "
    "Shenzhen summit \u2022 Anthropic $83 IPO & debut \u2022 ICJ Rohingya verdict "
    "\u2022 GTA VI launch \u2022 $190.4m Van Gogh \u2022 Voyager 1 one-light-day "
    "\u2022 Senate 48\u201351 Iran vote \u2022 UK 1,000-drone pledge \u2022 Israel's "
    "one-day Gaza raid \u2022 Denmark ratifies Greenland deal"
)

FOOTER = (
    "Every story here happened, or was first reported, on Friday 20 November "
    "2026 in at least one time zone. Sources: Reuters, AP, AFP, BBC, IMD, "
    "UN News, Al Jazeera, ICC, EU Council, PBOC."
)

# ------------------------------------------------------------- dot-matrix world map
# 64 cols (lon -180..180) x 32 rows (lat 75..-55); land given as row spans.
LAND_SPANS = {
    0: [(22, 24), (33, 50)],
    1: [(7, 17), (21, 24), (31, 54)],
    2: [(6, 18), (33, 56)],
    3: [(6, 19), (30, 58)],
    4: [(6, 20), (29, 60)],
    5: [(7, 20), (30, 60)],
    6: [(8, 20), (29, 59)],
    7: [(9, 19), (28, 58)],
    8: [(9, 19), (29, 57)],
    9: [(10, 18), (30, 57)],
    10: [(11, 18), (31, 55)],
    11: [(12, 17), (33, 54)],
    12: [(13, 16), (35, 52)],
    13: [(14, 16), (37, 50)],
    14: [(15, 18), (37, 47)],
    15: [(15, 19), (38, 47)],
    16: [(16, 20), (38, 45)],
    17: [(16, 20), (39, 44)],
    18: [(17, 20), (39, 44)],
    19: [(17, 20), (40, 43)],
    20: [(18, 20), (40, 43), (52, 58)],
    21: [(18, 20), (40, 42), (52, 58)],
    22: [(19, 20), (41, 42), (53, 57)],
    23: [(19, 20), (41, 42), (53, 56)],
    24: [(19, 19), (61, 62)],
    25: [(19, 20), (62, 62)],
    26: [(62, 63)],
}

# story number -> (grid col, grid row) on the map
PINS = {
    1: (47, 13), 2: (37, 6), 3: (38, 10), 4: (55, 9),
    6: (33, 6), 7: (58, 10), 8: (52, 8), 9: (62, 26),
    10: (35, 8), 11: (31, 8), 13: (18, 9),
}


# ------------------------------------------------------------ small illustrations
def art_cyclone(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 68, 86))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(232, 214, 170))
    d.text((x + 8, y + h - 22), "BAY OF BENGAL", font=font(SANS_B, 10),
           fill=(60, 50, 30))
    cx, cy = x + w // 2, y + h // 2 - 6
    for r, col in ((32, WHITE), (24, (200, 220, 230)), (15, WHITE)):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=4)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    d.text((x + 8, y + 6), "GOPALPUR", font=font(SANS_B, 10), fill=WHITE)
    d.text((x + w - 118, y + 6), "GUSTS 90 KM/H", font=font(SANS_B, 10),
           fill=(255, 210, 120))


def art_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 26, 40))
    for sx, sy in ((12, 14), (40, 8), (70, 18), (110, 10), (150, 16),
                   (190, 8), (230, 14), (270, 10)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    base = y + h
    for bx, bw, bh in ((0, 34, 34), (38, 26, 48), (68, 30, 28), (102, 24, 42),
                       (130, 34, 30), (168, 26, 50), (198, 30, 34),
                       (232, 28, 44), (264, 30, 28)):
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(8, 14, 22))
    for x0, x1, peak in ((10, 120, 34), (90, 210, 30), (170, 290, 32)):
        d.arc([x + x0, y + peak - 22, x + x1, y + peak + 40], 200, 340,
              fill=(255, 150, 60), width=3)
        d.ellipse([x + x1 - 4, y + peak + 8, x + x1 + 2, y + peak + 14],
                  fill=(255, 200, 90))
    d.text((x + 8, y + h - 20), "01:25 LOCAL", font=font(SANS_B, 10),
           fill=(255, 210, 120))


def art_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 68, 86))
    cx, cy, r = x + 52, y + h // 2, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 160, 170),
              outline=WHITE, width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=WHITE, width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 120, 240, fill=WHITE, width=2)
    tx = x + 108
    d.rounded_rectangle([tx, y + 12, tx + 16, y + h - 12], radius=8,
                        fill=WHITE, outline=RED, width=2)
    d.ellipse([tx - 3, y + h - 30, tx + 19, y + h - 8], fill=RED)
    d.rectangle([tx + 6, y + 18, tx + 10, y + h - 22], fill=RED)
    d.rectangle([x + w - 118, y + 8, x + w - 8, y + 34], fill=RED)
    d.text((x + w - 110, y + 12), "FINAL DAY", font=font(SANS_B, 12),
           fill=WHITE)
    d.text((x + w - 118, y + h - 22), "COP31", font=font(SANS_B, 12),
           fill=WHITE)


def art_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(248, 244, 233))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    pts = [(x + 10, y + 8), (x + 50, y + 14), (x + 90, y + 12),
           (x + 130, y + 20), (x + 170, y + 19), (x + 210, y + 24),
           (x + 250, y + 26)]
    d.line(pts, fill=RED, width=3)
    d.polygon(pts + [(x + 250, y + h - 4), (x + 10, y + h - 4)],
              fill=(158, 27, 27, 40))
    d.text((x + 8, y + h - 20), "NIKKEI \u22125.1%", font=font(SANS_B, 11),
           fill=RED)


def art_bepi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 26, 40))
    for sx, sy in ((14, 12), (46, 20), (90, 10), (150, 16), (200, 12),
                   (250, 18), (280, 10)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    d.ellipse([x + w - 64, y + 4, x + w - 34, y + 34], fill=(200, 190, 170))
    d.ellipse([x + w - 56, y + 12, x + w - 48, y + 20], fill=(170, 158, 140))
    d.ellipse([x + w - 46, y + 22, x + w - 40, y + 28], fill=(170, 158, 140))
    d.line([x + 24, y + h - 8, x + w - 52, y + 22], fill=(255, 200, 90),
           width=2)
    d.rectangle([x + 16, y + h - 20, x + 40, y + h - 6], fill=(230, 220, 200))
    d.polygon([(x + 40, y + h - 18), (x + 56, y + h - 12), (x + 40, y + h - 6)],
              fill=(255, 200, 90))
    d.text((x + 8, y + 6), "6BN MILES", font=font(SANS_B, 10), fill=WHITE)


def art_summit(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(248, 244, 233))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    d.rectangle([x + 12, y + 10, x + w // 2 - 4, y + h - 10], fill=(0, 51, 153))
    for sx, sy in ((28, 22), (44, 16), (58, 26), (36, 38), (52, 42)):
        d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=(255, 204, 0))
    d.rectangle([x + w // 2 + 4, y + 10, x + w - 12, y + h - 10],
                fill=(200, 16, 46))
    d.line([x + w // 2 + 4, y + h // 2, x + w - 12, y + h // 2], fill=WHITE,
           width=5)
    d.line([(x + w // 2 + 4 + (w // 2 - 16) // 2), y + 10,
            (x + w // 2 + 4 + (w // 2 - 16) // 2), y + h - 10], fill=WHITE,
           width=5)
    d.text((x + 12, y + h - 20), "EU", font=font(SANS_B, 11), fill=WHITE)
    d.text((x + w - 30, y + h - 20), "UK", font=font(SANS_B, 11),
           fill=WHITE)


def art_cpi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(248, 244, 233))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    base = y + h - 8
    vals = [("2.1", 18, MUTED), ("2.3", 20, RED), ("2.2", 19, TEAL)]
    bx = x + 22
    for label, vh, col in vals:
        d.rectangle([bx, base - vh, bx + 34, base], fill=col)
        d.text((bx + 2, base - vh - 14), label, font=font(SANS_B, 10),
               fill=INK)
        bx += 52
    d.line([x + 10, base, x + w - 10, base], fill=INK, width=1)


def art_lpr(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(248, 244, 233))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    d.line([x + 12, y + 14, x + w - 12, y + 14], fill=RED, width=3)
    d.line([x + 12, y + 28, x + w - 12, y + 28], fill=TEAL, width=3)
    d.text((x + 12, y + 3), "3.50% 5Y", font=font(SANS_B, 11), fill=RED)
    d.text((x + 12, y + 17), "3.00% 1Y", font=font(SANS_B, 11), fill=TEAL)


def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(34, 100, 60))
    d.rectangle([x + 14, y + h - 20, x + w - 14, y + h - 6], fill=(210, 190, 140))
    for sx in (46, 56, 66):
        d.line([x + sx, y + 4, x + sx, y + h - 20], fill=(240, 220, 150),
               width=3)
    d.line([x + 46, y + 2, x + 66, y + 2], fill=(240, 220, 150),
           width=3)
    d.line([x + 118, y + 6, x + 138, y + h - 22], fill=(210, 180, 120),
           width=7)
    d.ellipse([x + w - 46, y + 12, x + w - 30, y + 28], fill=RED)
    d.text((x + 8, y + 6), "118 \u2022 RECORD", font=font(SANS_B, 11),
           fill=WHITE)


def art_strike(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(248, 244, 233))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    d.rectangle([x + 10, y + 8, x + 40, y + h - 8], fill=(0, 146, 70))
    d.rectangle([x + 40, y + 8, x + 70, y + h - 8], fill=WHITE)
    d.rectangle([x + 70, y + 8, x + 100, y + h - 8], fill=(205, 0, 42))
    for hx in range(112, w - 8, 18):
        d.ellipse([x + hx, y + h - 22, x + hx + 10, y + h - 12], fill=INK)
        d.polygon([(x + hx - 2, y + h - 6), (x + hx + 12, y + h - 6),
                   (x + hx + 5, y + h - 12)], fill=INK)
    d.text((x + 112, y + 8), "100 SQUARES", font=font(SANS_B, 11), fill=RED)


def art_pill(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(248, 244, 233))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    cx, cy = x + w - 52, y + h // 2
    for r, col in ((18, RED), (12, WHITE), (7, RED)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)
    d.rounded_rectangle([x + 12, y + h // 2 - 10, x + 76, y + h // 2 + 10],
                        radius=10, fill=(240, 120, 60))
    d.rounded_rectangle([x + 12, y + h // 2 - 10, x + 44, y + h // 2 + 10],
                        radius=10, fill=(250, 210, 90))
    d.text((x + 12, y + 6), "60.7% RESPONSE", font=font(SANS_B, 11), fill=RED)


def art_youth(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 34, 46))
    for hx in range(12, w - 8, 20):
        d.ellipse([x + hx, y + h - 36, x + hx + 11, y + h - 25], fill=WHITE)
        d.polygon([(x + hx - 2, y + h - 8), (x + hx + 13, y + h - 8),
                   (x + hx + 5, y + h - 26)], fill=WHITE)
    for px, label in ((16, "PAY"), (76, "HOMES"), (136, "FUTURE")):
        d.line([x + px + 12, y + 12, x + px + 12, y + 34], fill=WHITE, width=2)
        d.rectangle([x + px, y + 12, x + px + 46, y + 28], fill=RED)
        d.text((x + px + 4, y + 15), label, font=font(SANS_B, 9), fill=WHITE)


def art_sub(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 68, 86))
    for wy in (h - 8, h - 4):
        d.line([x + 8, y + wy, x + w - 8, y + wy], fill=(140, 190, 200),
               width=2)
    d.rounded_rectangle([x + 30, y + 12, x + w - 30, y + 28], radius=8,
                        fill=(40, 50, 60))
    d.rectangle([x + w // 2 - 8, y + 6, x + w // 2 + 8, y + 14],
                fill=(40, 50, 60))
    d.ellipse([x + w - 52, y + 16, x + w - 44, y + 24],
              fill=(255, 210, 120))
    d.text((x + 8, y + 2), "3\u20135 BOATS", font=font(SANS_B, 9), fill=WHITE)


ART = {
    "cyclone": art_cyclone, "kyiv": art_kyiv, "cop": art_cop,
    "markets": art_markets, "bepi": art_bepi, "summit": art_summit,
    "cpi": art_cpi, "lpr": art_lpr, "cricket": art_cricket,
    "strike": art_strike, "pill": art_pill, "youth": art_youth,
    "sub": art_sub,
}


def draw_map(d, x, y, w, h):
    """Dot-matrix world map with numbered pins for the featured stories."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    cols, rows = 64, 32
    sx, sy = w / cols, h / rows
    land = set()
    for r, spans in LAND_SPANS.items():
        for c0, c1 in spans:
            for c in range(c0, c1 + 1):
                land.add((c, r))
    for (c, r) in land:
        cx, cy = x + (c + 0.5) * sx, y + (r + 0.5) * sy
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(150, 170, 185))
    for num, (c, r) in sorted(PINS.items()):
        cx, cy = x + (c + 0.5) * sx, y + (r + 0.5) * sy
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=RED,
                  outline=WHITE, width=1)
        t = str(num)
        tw = d.textlength(t, font=font(SANS_B, 9))
        d.text((cx - tw / 2, cy - 6), t, font=font(SANS_B, 9), fill=WHITE)
    d.rectangle([x + 6, y + h - 26, x + 118, y + h - 6], fill=RED)
    d.text((x + 12, y + h - 23), "5 \u2022 SPACE Mercury",
           font=font(SANS_B, 11), fill=WHITE)


# ------------------------------------------------------------------ composition
def draw_topbar(d, y):
    d.text((24, y), "THE WORLD IN ONE DAY", font=font(SANS_B, 13), fill=INK)
    right = "FRIDAY'S NEWS \u2022 ONE PAGE \u2022 36 STORIES \u2022 6 CONTINENTS"
    tw = d.textlength(right, font=font(SANS, 12))
    d.text((1000 - tw, y + 1), right, font=font(SANS, 12), fill=MUTED)
    return y + 16


def draw_masthead(d, y):
    title = "Friday 20 November 2026"
    tw = d.textlength(title, font=font(SERIF_B, 42))
    d.text(((W - tw) / 2, y), title, font=font(SERIF_B, 42), fill=INK)
    sub = "Cyclone Akvan strikes India \u2022 Kyiv hit overnight \u2022 Asia shares plunge"
    sw = d.textlength(sub, font=font(SERIF, 16))
    d.text(((W - sw) / 2, y + 46), sub, font=font(SERIF, 16), fill=RED)
    d.line([24, y + 68, 1000, y + 68], fill=INK, width=2)
    d.line([24, y + 72, 1000, y + 72], fill=INK, width=1)
    return y + 76


def draw_numbers(d, y):
    x0, total_w = 24, 976
    cell = total_w / len(NUMBERS)
    for i, (num, label) in enumerate(NUMBERS):
        x = x0 + i * cell
        if i:
            d.line([x - 6, y + 4, x - 6, y + 44], fill=RULE, width=1)
        d.text((x, y), num, font=font(SANS_B, 21), fill=RED)
        draw_para(d, x, y + 24, label, font(SANS, 11), cell - 14, fill=MUTED,
                  leading=11.5)
    return y + 48


def draw_chips(d, y):
    x = 24
    for label, col in CHIPS:
        fnt = font(SANS_B, 11)
        w = d.textlength(label, font=fnt) + 16
        d.rounded_rectangle([x, y, x + w, y + 18], radius=4, fill=col)
        d.text((x + 8, y + 3), label, font=fnt, fill=WHITE)
        x += w + 6
    right = "ALL STORIES: FRI 20 NOV 2026, ANY TIME ZONE"
    tw = d.textlength(right, font=font(SANS_B, 10))
    d.text((1000 - tw, y + 4), right, font=font(SANS_B, 10), fill=MUTED)
    return y + 18


def draw_lead(d, x, y, w, story):
    num, place, field, head, body, source, art = story
    ART[art](d, x, y, w, 76)
    tag = "%02d \u2022 %s \u2022 %s" % (num, place, field)
    d.text((x, y + 82), tag, font=font(SANS_B, 11), fill=RED)
    draw_para(d, x, y + 96, head, font(SERIF_B, 17), w, leading=20)
    draw_para(d, x, y + 140, body, font(SANS, 12), w, leading=14)
    d.text((x, y + 184), "(%s)" % source, font=font(SANS, 10), fill=MUTED)
    return y + 200


def draw_feature(d, x, y, w, story):
    num, place, field, head, body, source, art = story
    ART[art](d, x, y, w, 40)
    tag = "%02d \u2022 %s \u2022 %s" % (num, place, field)
    d.text((x, y + 45), tag, font=font(SANS_B, 10), fill=RED)
    draw_para(d, x, y + 58, head, font(SANS_B, 13), w, leading=16)
    draw_para(d, x, y + 92, body, font(SANS, 11), w, leading=13)
    d.text((x, y + 133), "(%s)" % source, font=font(SANS, 9), fill=MUTED)
    return y + 148


def draw_bottom(d, y, height):
    # --- map panel (left)
    mx, mw = 24, 324
    d.text((mx, y), "WHERE IT HAPPENED", font=font(SANS_B, 14), fill=INK)
    note = "Pins 1\u201311 & 13"
    nw = d.textlength(note, font=font(SANS, 10))
    d.text((mx + mw - nw, y + 3), note, font=font(SANS, 10), fill=MUTED)
    map_h = height - 44
    draw_map(d, mx, y + 20, mw, map_h)
    legend = "\u25cf 1\u20133 Lead    \u25cf 4\u201313 Feature Stories"
    d.text((mx, y + 20 + map_h + 6), legend, font=font(SANS, 10),
           fill=MUTED)
    # --- briefs panel (right)
    bx, bw = 360, 640
    d.text((bx, y), "ALSO ON FRIDAY 20 NOVEMBER \u2014 23 MORE STORIES",
           font=font(SANS_B, 14), fill=INK)
    rn = "World Briefs (14\u201336)"
    rw = d.textlength(rn, font=font(SANS, 10))
    d.text((bx + bw - rw, y + 3), rn, font=font(SANS, 10), fill=MUTED)
    ly = y + 22
    f_num = font(SANS_B, 11)
    f_pl = font(SANS_B, 11)
    f_tx = font(SANS, 11)
    for num, place, text, source in BRIEFS:
        cx = bx
        part = "%d " % num
        d.text((cx, ly), part, font=f_num, fill=RED)
        cx += d.textlength(part, font=f_num)
        part = place + " "
        d.text((cx, ly), part, font=f_pl, fill=INK)
        cx += d.textlength(part, font=f_pl)
        d.text((cx, ly), "\u2014 " + text, font=f_tx, fill=INK)
        sw = d.textlength(" (%s)" % source, font=f_tx)
        d.text((bx + bw - sw, ly), " (%s)" % source, font=f_tx, fill=MUTED)
        ly += 10.3
    return y + height


def draw_datecheck(d, y):
    lines = wrap_text(d, DATE_CHECK, font(SANS, 11), 976 - 20)
    box_h = len(lines) * 14 + 10
    d.rectangle([24, y, 1000, y + box_h], outline=RED, width=2)
    ty = y + 5
    for line in lines:
        d.text((34, ty), line, font=font(SANS, 11), fill=INK)
        ty += 14
    return y + box_h


def check_layout(d):
    """Sanity checks: nothing overflows its slot. Prints warnings."""
    issues = []
    for num, place, text, source in BRIEFS:
        line = "%d %s \u2014 %s (%s)" % (num, place, text, source)
        w = d.textlength(line, font=font(SANS, 11))
        if w > 640:
            issues.append("brief %d too wide: %.0fpx" % (num, w))
    for story in FEATURED[:3]:
        _, _, _, head, body, _, _ = story
        if len(wrap_text(d, head, font(SERIF_B, 17), 317)) > 2:
            issues.append("lead headline too long: %s" % head)
        if len(wrap_text(d, body, font(SANS, 12), 317)) > 3:
            issues.append("lead body too long: %s" % body[:40])
    for story in FEATURED[3:]:
        _, _, _, head, body, _, _ = story
        if len(wrap_text(d, head, font(SANS_B, 13), 189)) > 2:
            issues.append("feature headline too long: %s" % head)
        if len(wrap_text(d, body, font(SANS, 11), 189)) > 3:
            issues.append("feature body too long: %s" % body[:40])
    for num, label in NUMBERS:
        if len(wrap_text(d, label, font(SANS, 11), 148)) > 2:
            issues.append("number label too long: %s" % label)
    dc = wrap_text(d, DATE_CHECK, font(SANS, 11), 956)
    if len(dc) > 2:
        issues.append("date check wraps to %d lines" % len(dc))
    for i in issues:
        print("LAYOUT:", i)
    if not issues:
        print("LAYOUT: all slots fit")
    return issues


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 6
    y = draw_topbar(d, y)
    y = draw_masthead(d, y + 4)
    y = draw_numbers(d, y + 4)
    y = draw_chips(d, y + 4)
    # lead row: stories 1-3
    y0 = y + 4
    col_w = 317
    for i, story in enumerate(FEATURED[:3]):
        draw_lead(d, 24 + i * (col_w + 12), y0, col_w, story)
    y = y0 + 200
    d.line([24, y + 3, 1000, y + 3], fill=RULE, width=1)
    # feature rows: stories 4-8 and 9-13
    f_w = 189
    for row, group in enumerate((FEATURED[3:8], FEATURED[8:13])):
        y0 = y + 6
        for i, story in enumerate(group):
            draw_feature(d, 24 + i * (f_w + 7), y0, f_w, story)
        y = y0 + 148
        d.line([24, y + 3, 1000, y + 3], fill=RULE, width=1)
    y = draw_bottom(d, y + 6, 258)
    y = draw_datecheck(d, y + 4)
    d.text((24, y + 6), FOOTER, font=font(SANS, 10), fill=MUTED)
    print("final y:", y + 18, "of", H)
    check_layout(d)
    img.save(OUT, "PNG")
    print("saved", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
