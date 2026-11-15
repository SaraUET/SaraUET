
from pathlib import Path
from html import escape
import json

# ==================================================
# PROJECT PATHS
# ==================================================

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "cards"
DATA = ROOT / "data" / "contributions.json"

CARDS.mkdir(parents=True, exist_ok=True)
DATA.parent.mkdir(parents=True, exist_ok=True)


# ==================================================
# BURGUNDY / NEON PINK COLOUR PALETTE
# ==================================================

BG = "#10030A"
PANEL = "#1B0610"
WINE = "#3C0A1F"
BURGUNDY = "#7D173B"
ROSE = "#D84C80"
BLUSH = "#F3B2CA"
PALE = "#FBEAF1"
MUTED = "#B9869B"


# ==================================================
# SVG FOUNDATION
# ==================================================

def svg_start(width, height, title):

    return f'''<svg xmlns="http://www.w3.org/2000/svg"
        width="{width}"
        height="{height}"
        viewBox="0 0 {width} {height}"
        role="img">

<defs>

  <linearGradient id="background" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{BG}"/>
    <stop offset=".55" stop-color="{PANEL}"/>
    <stop offset="1" stop-color="#31091C"/>
  </linearGradient>

  <linearGradient id="pink" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{BURGUNDY}"/>
    <stop offset=".55" stop-color="{ROSE}"/>
    <stop offset="1" stop-color="{BLUSH}"/>
  </linearGradient>

  <radialGradient id="mist">
    <stop offset="0" stop-color="{ROSE}" stop-opacity=".32"/>
    <stop offset="1" stop-color="{ROSE}" stop-opacity="0"/>
  </radialGradient>

  <filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
    <feGaussianBlur stdDeviation="5" result="blur"/>
    <feMerge>
      <feMergeNode in="blur"/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>

  <filter id="smoke">
    <feGaussianBlur stdDeviation="16"/>
  </filter>

  <pattern id="grid" width="28" height="28"
           patternUnits="userSpaceOnUse">
    <path d="M28 0H0V28"
          fill="none"
          stroke="{ROSE}"
          stroke-opacity=".09"/>
  </pattern>

  <style>
    .heading {{
      font-family: Georgia, serif;
      fill: {PALE};
    }}

    .mono {{
      font-family: monospace;
      fill: {BLUSH};
    }}

    .muted {{
      font-family: monospace;
      fill: {MUTED};
    }}

    .pink {{
      fill: {ROSE};
    }}

    .line {{
      stroke: {ROSE};
      stroke-opacity: .65;
      fill: none;
    }}
  </style>

</defs>

<title>{escape(title)}</title>

<rect width="100%" height="100%" rx="22"
      fill="url(#background)"/>

<rect width="100%" height="100%" rx="22"
      fill="url(#grid)"/>

<!-- ATMOSPHERIC SMOKE -->

<g filter="url(#smoke)" opacity=".55">

  <ellipse cx="8%" cy="15%" rx="20%" ry="28%"
           fill="{BURGUNDY}" opacity=".5"/>

  <ellipse cx="90%" cy="80%" rx="24%" ry="30%"
           fill="{ROSE}" opacity=".18"/>

</g>

<!-- PINK MIST -->

<ellipse cx="85%" cy="15%" rx="28%" ry="40%"
         fill="url(#mist)"/>

<!-- GLOWING BORDER -->

<rect x="1" y="1"
      width="98%" height="98%"
      rx="21"
      fill="none"
      stroke="{ROSE}"
      stroke-opacity=".65"/>

<!-- DECORATIVE STARS -->

<g fill="{BLUSH}" filter="url(#glow)">

  <path d="M88 30l4 12 12 4-12 4-4 12-4-12-12-4 12-4z"/>

  <path d="M90 75l3 9 9 3-9 3-3 9-3-9-9-3 9-3z"/>

</g>

'''


def svg_end():
    return "</svg>"


def save(filename, content):
    filepath = CARDS / filename
    filepath.write_text(content + svg_end(), encoding="utf-8")


# ==================================================
# BUTTERFLY DECORATION
# ==================================================

def butterfly(x, y, scale=1):

    return f'''
    <g transform="translate({x} {y}) scale({scale})"
       filter="url(#glow)">

      <path d="
        M0 0
        C-45 -70 -100 -50 -72 -5
        C-50 28 -22 20 0 0
        C22 20 50 28 72 -5
        C100 -50 45 -70 0 0Z"
        fill="{ROSE}"
        fill-opacity=".15"
        stroke="{BLUSH}"
        stroke-width="1.5"/>

      <path d="
        M0 0
        C-30 30 -40 70 -8 48
        L0 0
        L8 48
        C40 70 30 30 0 0Z"
        fill="{BURGUNDY}"
        stroke="{ROSE}"/>

      <path d="
        M-3 -5Q-20 -35 -35 -40
        M3 -5Q20 -35 35 -40"
        stroke="{BLUSH}"
        fill="none"/>

      <path d="M0 -5V40"
            stroke="{PALE}"
            stroke-width="2"/>

    </g>
    '''


# ==================================================
# SECTION HEADING
# ==================================================

def heading(kicker, title, x=30, y=40):

    return f'''
    <text x="{x}" y="{y}"
          class="pink mono"
          font-size="12"
          letter-spacing="3">
      {escape(kicker)}
    </text>

    <text x="{x}" y="{y+48}"
          class="heading"
          font-size="30">
      {escape(title)}
    </text>

    <path d="M{x} {y+65}H410"
          class="line"/>
    '''


# ==================================================
# HERO CARD
# ==================================================

def hero_card():

    s = svg_start(1000, 340, "Sara Shafqat — GitHub profile")

    s += '''
    <g filter="url(#smoke)" opacity=".6">
      <ellipse cx="850" cy="90"
               rx="180" ry="110"
               fill="#A51E50"
               opacity=".45"/>
    </g>

    <rect x="25" y="25"
          width="950" height="290"
          rx="25"
          fill="none"
          stroke="#D84C80"
          stroke-opacity=".45"/>

    <!-- PORTRAIT PLACEHOLDER -->

    <circle cx="150" cy="160" r="86"
            fill="#3C0A1F"
            stroke="#D84C80"
            stroke-width="2"/>

    <circle cx="150" cy="160" r="75"
            fill="none"
            stroke="#F3B2CA"
            stroke-dasharray="3 7"
            opacity=".7"/>

    <text x="150" y="185"
          text-anchor="middle"
          class="heading"
          font-size="70">S.</text>

    <!-- INTRODUCTION -->

    <text x="280" y="105"
          class="pink mono"
          font-size="13"
          letter-spacing="4">
      HELLO, WORLD — I'M
    </text>

    <text x="275" y="175"
          class="heading"
          font-size="59">
      Sara Shafqat
    </text>

    <text x="280" y="218"
          class="mono"
          font-size="16"
          letter-spacing="1">
      BUILDING THINGS. BREAKING PATTERNS.
    </text>

    <rect x="280" y="250"
          width="205" height="34"
          rx="17"
          fill="#3C0A1F"
          stroke="#D84C80"/>

    <circle cx="300" cy="267" r="4"
            fill="#F3B2CA"/>

    <text x="315" y="272"
          class="mono"
          font-size="11">
      OPEN TO OPPORTUNITIES
    </text>

    <text x="45" y="300"
          class="muted"
          font-size="10"
          letter-spacing="2">
      IT × BUSINESS × DESIGN
    </text>
    '''

    s += butterfly(850, 160, 1.05)

    save("hero.svg", s)


# ==================================================
# ABOUT CARD
# ==================================================

def about_card():

    s = svg_start(440, 230, "About Sara")

    s += heading("01 / ABOUT ME", "A little about me.")

    s += '''
    <text x="30" y="140" class="mono" font-size="14">
      BBIT graduate blending IT,
    </text>

    <text x="30" y="165" class="mono" font-size="14">
      business operations and a
    </text>

    <text x="30" y="190" class="mono" font-size="14">
      designer's eye.
    </text>

    <text x="30" y="215" class="muted" font-size="9">
      CURIOUS BY NATURE · CREATIVE BY DEFAULT
    </text>
    '''

    save("about.svg", s)


# ==================================================
# TECH STACK CARD
# ==================================================

def stack_card():

    s = svg_start(440, 250, "Tools and interests")

    s += heading("02 / WHAT I WORK WITH", "Tools & interests.")

    skills = [
        "HTML / CSS",
        "JavaScript",
        "Python",
        "Git & GitHub",
        "UI / UX",
        "Business Ops"
    ]

    for i, skill in enumerate(skills):

        x = 30 + (i % 3) * 128
        y = 125 + (i // 3) * 53

        s += f'''
        <rect x="{x}" y="{y}"
              width="112" height="34"
              rx="17"
              fill="{WINE}"
              stroke="{BURGUNDY}"/>

        <text x="{x+56}" y="{y+22}"
              text-anchor="middle"
              class="mono"
              font-size="10">
          {escape(skill)}
        </text>
        '''

    s += '''
    <text x="30" y="235"
          class="muted"
          font-size="9">
      ALWAYS LEARNING, ALWAYS EXPERIMENTING
    </text>
    '''

    save("stack.svg", s)


# ==================================================
# SOCIAL CARD
# ==================================================

def social_card():

    s = svg_start(440, 190, "Find me elsewhere")

    s += heading("03 / FIND ME ELSEWHERE", "Let's connect.")

    s += '''
    <text x="30" y="135" class="mono" font-size="12">
      PORTFOLIO
    </text>

    <text x="160" y="135" class="mono" font-size="12">
      LINKEDIN
    </text>

    <text x="300" y="135" class="mono" font-size="12">
      INSTAGRAM
    </text>

    <text x="30" y="165" class="muted" font-size="9">
      IDEAS · COLLABORATIONS · GOOD CONVERSATIONS
    </text>
    '''

    save("social.svg", s)


# ==================================================
# CONTRIBUTION DATA
# ==================================================

def load_data():

    if DATA.exists():

        try:
            return json.loads(
                DATA.read_text(encoding="utf-8")
            )

        except (json.JSONDecodeError, OSError):
            print("Could not read contribution data. Using empty data.")

    return {
        "total": 0,
        "months": [],
        "days": [],
        "current_streak": 0,
        "active_days": 0,
        "busiest_day": "—"
    }


def activity_card():

    data = load_data()

    total = data.get("total", 0)
    streak = data.get("current_streak", 0)
    active = data.get("active_days", 0)
    busiest = data.get("busiest_day", "—")

    s = svg_start(650, 440, "GitHub activity")

    s += heading(
        "04 / GITHUB ACTIVITY",
        "The work in progress."
    )

    s += f'''
    <text x="30" y="145"
          class="muted"
          font-size="11">
      CONTRIBUTION OVERVIEW
    </text>

    <rect x="30" y="165"
          width="590" height="105"
          rx="15"
          fill="{BG}"
          stroke="{BURGUNDY}"/>

    <text x="55" y="205"
          class="pink mono"
          font-size="12">
      TOTAL CONTRIBUTIONS
    </text>

    <text x="55" y="242"
          class="heading"
          font-size="30">
      {total}
    </text>

    <text x="245" y="205"
          class="pink mono"
          font-size="12">
      CURRENT STREAK
    </text>

    <text x="245" y="242"
          class="heading"
          font-size="30">
      {streak}
    </text>

    <text x="435" y="205"
          class="pink mono"
          font-size="12">
      ACTIVE DAYS
    </text>

    <text x="435" y="242"
          class="heading"
          font-size="30">
      {active}
    </text>

    <text x="30" y="315"
          class="mono"
          font-size="12">
      BUSIEST DAY: {escape(str(busiest))}
    </text>
    '''

    days = data.get("days", [])

    colours = [
        "#260817",
        "#4A0D29",
        "#7D173B",
        "#C02F6B",
        "#F3B2CA"
    ]

    for i, day in enumerate(days[-182:]):

        if isinstance(day, dict):
            count = int(day.get("count", 0))
        else:
            count = int(day)

        level = min(max(count, 0), 4)

        x = 30 + (i % 26) * 22
        y = 335 + (i // 26) * 16

        s += f'''
        <rect x="{x}" y="{y}"
              width="14" height="11"
              rx="3"
              fill="{colours[level]}"/>
        '''

    if not days:

        s += '''
        <text x="30" y="365"
              class="muted"
              font-size="11">
          CONTRIBUTION DATA NOT CONNECTED YET
        </text>
        '''

    s += butterfly(565, 75, .35)

    save("activity.svg", s)


# ==================================================
# CONTRIBUTION HISTORY CARD
# ==================================================

def contributions_card():

    data = load_data()
    days = data.get("days", [])[-364:]

    s = svg_start(1000, 190, "Contribution history")

    s += heading(
        "05 / CONTRIBUTION HISTORY",
        "A year of little steps."
    )

    colours = [
        "#260817",
        "#4A0D29",
        "#7D173B",
        "#C02F6B",
        "#F3B2CA"
    ]

    for i, day in enumerate(days):

        if isinstance(day, dict):
            count = int(day.get("count", 0))
        else:
            count = int(day)

        level = min(max(count, 0), 4)

        x = 30 + (i % 52) * 18
        y = 105 + (i // 52) * 13

        s += f'''
        <rect x="{x}" y="{y}"
              width="12" height="9"
              rx="2"
              fill="{colours[level]}"/>
        '''

    if not days:

        s += '''
        <text x="30" y="135"
              class="muted"
              font-size="12">
          YOUR CONTRIBUTION HISTORY WILL APPEAR HERE
        </text>
        '''

    save("contributions.svg", s)


# ==================================================
# REPOSITORY CARDS
# ==================================================

def repo_card(filename, number, title, description, language):

    s = svg_start(480, 175, title)

    s += f'''
    <text x="28" y="38"
          class="pink mono"
          font-size="11"
          letter-spacing="2">
      FEATURED REPOSITORY / {escape(number)}
    </text>

    <text x="28" y="83"
          class="heading"
          font-size="29">
      {escape(title)}
    </text>

    <text x="28" y="112"
          class="mono"
          font-size="12">
      {escape(description)}
    </text>

    <rect x="28" y="132"
          width="125" height="25"
          rx="13"
          fill="{WINE}"
          stroke="{BURGUNDY}"/>

    <text x="90" y="149"
          text-anchor="middle"
          class="mono"
          font-size="10">
      {escape(language)}
    </text>

    <text x="430" y="145"
          class="heading"
          font-size="25">↗</text>
    '''

    save(filename, s)


# ==================================================
# RENDER ALL CARDS
# ==================================================

def main():

    print("Rendering burgundy profile cards...")

    hero_card()
    about_card()
    stack_card()
    social_card()
    activity_card()
    contributions_card()

    repo_card(
        "repo-1.svg",
        "01",
        "CakeBlogSite",
        "A baking-focused web project.",
        "HTML / CSS"
    )

    repo_card(
        "repo-2.svg",
        "02",
        "Portfolio",
        "Personal portfolio and creative work.",
        "HTML / CSS / JS"
    )

    print("All eight profile cards rendered successfully!")
    print(f"Cards saved in: {CARDS}")


if __name__ == "__main__":
    main()
