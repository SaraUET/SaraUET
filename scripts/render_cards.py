
#!/usr/bin/env python3

import os
import json
import html
import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "cards"
DATA = ROOT / "data" / "contributions.json"

USERNAME = "SaraUET"
STATIC = os.getenv("STATIC", "0") == "1"

# ------------------------------------------
# BRAND COLOURS
# ------------------------------------------

INK = "#3d0a1b"
MAROON = "#7b1e3a"
ROSE = "#b83a5a"
ACCENT = "#c0506a"
PALE = "#f3dfe3"
LIGHT = "#fff5f6"
MUTED = "#c9a3ad"
DARK = "#35101e"

# ------------------------------------------
# PROFILE INFORMATION
# ------------------------------------------

PROFILE = {
    "name": "Sara Shafqat",
    "about": "BBIT graduate blending IT, business operations and a designer's eye.",
    "tagline": "IT  /  DESIGN  /  WEB  /  CREATIVE IDEAS",

    "links": [
        {
            "name": "PORTFOLIO",
            "description": "My creative space",
            "url": "https://saruet.github.io",
            "symbol": "↗",
            "number": "01"
        },
        {
            "name": "LINKEDIN",
            "description": "Let's connect",
            "url": "https://linkedin.com/in/sarashafqat",
            "symbol": "in",
            "number": "02"
        },
        {
            "name": "INSTAGRAM",
            "description": "Art, design & more",
            "url": "https://instagram.com/gallerieeme",
            "symbol": "✳",
            "number": "03"
        }
    ],

    "repos": [
        {
            "name": "CakeBlogSite",
            "description": "A baking-focused web project.",
            "language": "HTML / CSS",
            "url": "https://github.com/SaraUET/CakeBlogSite",
            "type": "CREATIVE BUILD",
            "number": "01"
        },
        {
            "name": "Portfolio",
            "description": "My personal portfolio and creative work.",
            "language": "HTML / CSS / JS",
            "url": "https://github.com/SaraUET/SaraUET.github.io",
            "type": "PERSONAL SPACE",
            "number": "02"
        }
    ]
}


# ------------------------------------------
# HELPERS
# ------------------------------------------

def esc(value):
    return html.escape(str(value), quote=True)


def start_svg(width, height, delay=0):

    animation = ""

    if not STATIC:
        animation = f"""
        .card {{
            animation: enter .8s ease-out {delay}s both;
        }}

        .rise {{
            animation: rise .8s ease-out {delay + 0.15}s both;
        }}

        .float {{
            animation: float 5s ease-in-out infinite;
        }}

        .glow {{
            animation: glow 4s ease-in-out infinite;
        }}

        @keyframes enter {{
            from {{
                opacity: 0;
                transform: translateY(15px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes rise {{
            from {{
                opacity: 0;
                transform: translateY(12px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-8px); }}
        }}

        @keyframes glow {{
            0%, 100% {{ opacity: .15; }}
            50% {{ opacity: .45; }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            .card, .rise, .float, .glow {{
                animation: none !important;
                opacity: 1 !important;
                transform: none !important;
            }}
        }}
        """

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{width}" height="{height}"
         viewBox="0 0 {width} {height}">

    <style>
        text {{
            font-family: Poppins, Arial, sans-serif;
        }}
        {animation}
    </style>

    <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="{INK}"/>
            <stop offset="55%" stop-color="{MAROON}"/>
            <stop offset="100%" stop-color="{ROSE}"/>
        </linearGradient>

        <linearGradient id="blush" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#fff9fa"/>
            <stop offset="100%" stop-color="{PALE}"/>
        </linearGradient>

        <pattern id="dots" width="22" height="22"
                 patternUnits="userSpaceOnUse">
            <circle cx="2" cy="2" r="1.2"
                    fill="{PALE}" opacity=".28"/>
        </pattern>
    </defs>
    """


def save_card(filename, svg):

    CARDS.mkdir(parents=True, exist_ok=True)

    (CARDS / filename).write_text(
        svg + "\n</svg>\n",
        encoding="utf-8"
    )


# ------------------------------------------
# 01. HERO CARD
# ------------------------------------------

def hero_card():

    svg = start_svg(1000, 280, 0)

    svg += f"""
    <g class="card">
        <rect width="1000" height="280"
              rx="26" fill="url(#bg)"/>
    </g>

    <rect x="660" y="0" width="340" height="280"
          fill="url(#dots)"/>

    <circle cx="855" cy="135" r="112"
            fill="none" stroke="{PALE}"
            stroke-width="1.5" opacity=".3"/>

    <circle cx="855" cy="135" r="91"
            fill="none" stroke="{PALE}"
            stroke-dasharray="3 9" opacity=".6"
            class="float"/>

    <circle cx="945" cy="45" r="9"
            fill="{LIGHT}" class="glow"/>

    <circle cx="750" cy="220" r="5"
            fill="{PALE}"/>

    <path d="M720 55 Q800 0 890 45"
          fill="none" stroke="{PALE}"
          stroke-width="2" opacity=".4"/>

    <g class="rise">
        <text x="58" y="55"
              fill="{PALE}" font-size="13"
              letter-spacing="4">
            HELLO, I'M
        </text>

        <text x="55" y="130"
              fill="{LIGHT}" font-size="54"
              font-weight="700">
            {esc(PROFILE['name'])}
        </text>

        <text x="59" y="171"
              fill="{PALE}" font-size="16">
            {esc(PROFILE['about'])}
        </text>

        <path d="M60 198 H340"
              stroke="{PALE}" opacity=".5"/>

        <text x="60" y="230"
              fill="{LIGHT}" font-size="12"
              letter-spacing="2">
            {esc(PROFILE['tagline'])}
        </text>
    </g>

    <g class="float">
        <circle cx="855" cy="135" r="67"
                fill="{PALE}" opacity=".15"/>

        <circle cx="855" cy="135" r="57"
                fill="none" stroke="{PALE}"
                stroke-width="1.5"/>

        <text x="855" y="153"
              fill="{LIGHT}" font-size="52"
              font-weight="600"
              text-anchor="middle">
            S.
        </text>
    </g>

    <text x="940" y="246"
          fill="{PALE}" font-size="10"
          text-anchor="end" letter-spacing="2">
        PERSONAL PROFILE / 2026
    </text>
    """

    save_card("hero.svg", svg)


# ------------------------------------------
# 02. SOCIAL LINK CARDS
# ------------------------------------------

def link_card(link, index):

    svg = start_svg(320, 130, .2 + index * .18)

    svg += f"""
    <g class="card">
        <rect x="2" y="2" width="316" height="126"
              rx="22" fill="url(#blush)"
              stroke="{ROSE}" stroke-width="1.2"/>
    </g>

    <path d="M245 2 H296 Q318 2 318 24 V75 Z"
          fill="{ROSE}" opacity=".08"/>

    <text x="25" y="26"
          fill="{ROSE}" font-size="10"
          letter-spacing="2">
        {link['number']} / CONNECT
    </text>

    <circle cx="57" cy="81" r="28"
            fill="{MAROON}"/>

    <circle cx="57" cy="81" r="33"
            fill="none" stroke="{ROSE}"
            opacity=".4"/>

    <text x="57" y="89"
          fill="{LIGHT}" font-size="21"
          text-anchor="middle">
        {esc(link['symbol'])}
    </text>

    <text x="103" y="73"
          fill="{INK}" font-size="15"
          font-weight="700">
        {esc(link['name'])}
    </text>

    <text x="103" y="96"
          fill="{MAROON}" font-size="11">
        {esc(link['description'])}
    </text>

    <text x="290" y="98"
          fill="{ROSE}" font-size="21"
          text-anchor="middle">
        ↗
    </text>

    <path d="M103 108 H175"
          stroke="{ROSE}" opacity=".5"/>
    """

    save_card(f"link-{index + 1}.svg", svg)


# ------------------------------------------
# 03. CONTRIBUTION DATA
# ------------------------------------------

def load_data():

    empty = {
        "total": 0,
        "months": [],
        "days": [],
        "current_streak": 0,
        "active_days": 0,
        "busiest_day": "—"
    }

    try:
        if DATA.exists():
            saved = json.loads(
                DATA.read_text(encoding="utf-8")
            )
            return {**empty, **saved}

    except (OSError, json.JSONDecodeError):
        print("Contribution data could not be read.")

    return empty


# ------------------------------------------
# 04. ACTIVITY DASHBOARD
# ------------------------------------------

def activity_card(data):

    svg = start_svg(1000, 330, .5)

    months = data.get("months", [])
    total = int(data.get("total", 0) or 0)

    svg += f"""
    <g class="card">
        <rect x="20" y="20" width="960" height="290"
              rx="24" fill="url(#bg)"/>
    </g>

    <rect x="20" y="20" width="960" height="290"
          rx="24" fill="url(#dots)"/>

    <text x="55" y="65"
          fill="{LIGHT}" font-size="22"
          font-weight="700">
        CONTRIBUTION RHYTHM
    </text>

    <text x="55" y="91"
          fill="{PALE}" font-size="11"
          letter-spacing="2">
        A LITTLE PROGRESS, DAY BY DAY
    </text>
    """

    stats = [
        ("TOTAL", f"{total:,}"),
        ("STREAK", f"{data.get('current_streak', 0)} days"),
        ("ACTIVE DAYS", str(data.get("active_days", 0))),
        ("BUSIEST DAY", str(data.get("busiest_day", "—")))
    ]

    for i, (label, value) in enumerate(stats):

        x = 545 + i * 105

        svg += f"""
        <text x="{x}" y="51"
              fill="{PALE}" font-size="9"
              text-anchor="middle">
            {esc(label)}
        </text>

        <text x="{x}" y="78"
              fill="{LIGHT}" font-size="15"
              font-weight="700"
              text-anchor="middle">
            {esc(value)}
        </text>
        """

    if months and max(m.get("count", 0) for m in months) > 0:

        maximum = max(m["count"] for m in months)
        slot = 870 / len(months)

        for i, month in enumerate(months[-12:]):

            value = month["count"]
            height = max(5, 115 * value / maximum)

            x = 65 + i * slot + slot * .2
            y = 252 - height

            month_number = int(month["month"][-2:])
            label = [
                "Jan", "Feb", "Mar", "Apr",
                "May", "Jun", "Jul", "Aug",
                "Sep", "Oct", "Nov", "Dec"
            ][month_number - 1]

            svg += f"""
            <rect x="{x:.1f}" y="{y:.1f}"
                  width="{slot * .58:.1f}"
                  height="{height:.1f}"
                  rx="7" fill="{PALE}"
                  class="rise"/>

            <text x="{x + slot * .29:.1f}"
                  y="278" fill="{PALE}"
                  font-size="10"
                  text-anchor="middle">
                {label}
            </text>
            """

    else:

        svg += f"""
        <path d="M65 252 H935"
              stroke="{PALE}" opacity=".3"
              stroke-dasharray="4 7"/>

        <text x="500" y="166"
              fill="{LIGHT}" font-size="18"
              text-anchor="middle"
              font-weight="600">
            Your activity story starts here.
        </text>

        <text x="500" y="194"
              fill="{PALE}" font-size="12"
              text-anchor="middle">
            Connect your GitHub activity to reveal your monthly rhythm.
        </text>

        <text x="500" y="218"
              fill="{PALE}" font-size="10"
              text-anchor="middle">
            Real activity only. No made-up statistics.
        </text>
        """

    svg += f"""
    <text x="55" y="296"
          fill="{PALE}" font-size="10"
          letter-spacing="1">
        GITHUB ACTIVITY / PERSONAL DASHBOARD
    </text>
    """

    save_card("activity.svg", svg)


# ------------------------------------------
# 05. FEATURED REPOSITORIES
# ------------------------------------------

def repo_card(repo, index):

    svg = start_svg(1000, 180, .7 + index * .2)

    svg += f"""
    <g class="card">
        <rect x="2" y="2" width="996" height="176"
              rx="24" fill="url(#blush)"
              stroke="{ROSE}" stroke-width="1.2"/>
    </g>

    <rect x="2" y="2" width="13" height="176"
          rx="6" fill="{MAROON}"/>

    <text x="50" y="40"
          fill="{ROSE}" font-size="10"
          letter-spacing="2">
        {esc(repo['type'])} / {esc(repo['number'])}
    </text>

    <circle cx="85" cy="109" r="30"
            fill="{MAROON}"/>

    <text x="85" y="117"
          fill="{LIGHT}" font-size="19"
          text-anchor="middle">
        {index + 1:02d}
    </text>

    <text x="140" y="91"
          fill="{INK}" font-size="25"
          font-weight="700">
        {esc(repo['name'])}
    </text>

    <text x="140" y="120"
          fill="{MAROON}" font-size="13">
        {esc(repo['description'])}
    </text>

    <rect x="140" y="137" width="160" height="23"
          rx="11" fill="{ROSE}" opacity=".13"/>

    <text x="220" y="153"
          fill="{MAROON}" font-size="10"
          text-anchor="middle">
        {esc(repo['language'])}
    </text>

    <circle cx="930" cy="90" r="25"
            fill="{ROSE}" opacity=".12"/>

    <text x="930" y="99"
          fill="{ROSE}" font-size="25"
          text-anchor="middle">
        ↗
    </text>

    <text x="930" y="135"
          fill="{MAROON}" font-size="9"
          text-anchor="middle">
        VIEW REPO
    </text>
    """

    save_card(f"repo-{index + 1}.svg", svg)


# ------------------------------------------
# 06. CONTRIBUTION HEATMAP
# ------------------------------------------

def contribution_graph(data):

    svg = start_svg(1000, 230, 1.2)

    days = data.get("days", [])[-371:]

    svg += f"""
    <g class="card">
        <rect x="20" y="20" width="960" height="190"
              rx="24" fill="url(#bg)"/>
    </g>

    <rect x="20" y="20" width="960" height="190"
          rx="24" fill="url(#dots)"/>

    <text x="55" y="59"
          fill="{LIGHT}" font-size="21"
          font-weight="700">
        A YEAR OF MAKING THINGS
    </text>

    <text x="55" y="81"
          fill="{PALE}" font-size="10"
          letter-spacing="2">
        EVERY LITTLE COMMIT COUNTS
    </text>
    """

    if days:

        cell = 10
        gap = 5
        start_x = 55
        start_y = 105

        for i, day in enumerate(days):

            col = i // 7
            row = i % 7

            count = day.get("contributionCount", 0)

            if count == 0:
                fill, opacity = PALE, .13
            elif count <= 2:
                fill, opacity = "#d98ca0", .75
            elif count <= 5:
                fill, opacity = "#e9a8b8", .9
            elif count <= 9:
                fill, opacity = "#f7cbd4", .98
            else:
                fill, opacity = "#fff0f3", 1

            x = start_x + col * (cell + gap)
            y = start_y + row * (cell + gap)

            svg += f"""
            <rect x="{x}" y="{y}"
                  width="{cell}" height="{cell}"
                  rx="2.5" fill="{fill}"
                  opacity="{opacity}"/>
            """

    else:

        svg += f"""
        <rect x="55" y="105" width="890" height="68"
              rx="12" fill="url(#dots)"/>

        <text x="500" y="139"
              fill="{LIGHT}" font-size="16"
              text-anchor="middle"
              font-weight="600">
            Your contribution map is waiting.
        </text>

        <text x="500" y="161"
              fill="{PALE}" font-size="11"
              text-anchor="middle">
            Your real GitHub activity will appear here when connected.
        </text>
        """

    save_card("contributions.svg", svg)


# ------------------------------------------
# MAIN RENDERER
# ------------------------------------------

def main():

    CARDS.mkdir(parents=True, exist_ok=True)
    (ROOT / "data").mkdir(parents=True, exist_ok=True)

    data = load_data()

    hero_card()

    for i, link in enumerate(PROFILE["links"]):
        link_card(link, i)

    activity_card(data)

    for i, repo in enumerate(PROFILE["repos"]):
        repo_card(repo, i)

    contribution_graph(data)

    print("All profile cards rendered successfully!")
    print(f"Cards saved in: {CARDS}")


if __name__ == "__main__":
    main()
