
#!/usr/bin/env python3

import os
import json
import html
import base64
import datetime
import subprocess
import urllib.request
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
CARDS = ROOT / "cards"
DATA = ROOT / "data" / "contributions.json"
FONTS = ROOT / "fonts"

USERNAME = os.getenv("GITHUB_USERNAME", "SaraUET")
STATIC = os.getenv("STATIC", "0") == "1"

# BRAND COLOURS
INK = "#3d0a1b"
MAROON = "#7b1e3a"
ROSE = "#b83a5a"
ACCENT = "#c0506a"
PALE = "#f3dfe3"
LIGHT = "#f6e7e9"
MUTED = "#c9a3ad"

# PROFILE INFORMATION
PROFILE = {
    "name": "Sara Shafqat",
    "about": "BBIT graduate blending IT, business operations and a designer's eye.",
    "portrait": "",

    "links": [
        {
            "name": "PORTFOLIO",
            "description": "My creative space",
            "url": "https://saruet.github.io",
            "symbol": "↗"
        },
        {
            "name": "LINKEDIN",
            "description": "Let's connect",
            "url": "https://linkedin.com/in/sarashafqat",
            "symbol": "in"
        },
        {
            "name": "INSTAGRAM",
            "description": "Art, design & more",
            "url": "https://instagram.com/gallerieeme",
            "symbol": "✳"
        }
    ],

    "repos": [
        {
            "name": "CakeBlogSite",
            "description": "A baking-focused web project.",
            "language": "HTML / CSS",
            "url": "https://github.com/SaraUET/CakeBlogSite"
        },
        {
            "name": "Portfolio",
            "description": "My personal portfolio and creative work.",
            "language": "HTML / CSS / JS",
            "url": "https://github.com/SaraUET/SaraUET.github.io"
        }
    ]
}

MONTHS = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
]


def escape(value):
    return html.escape(str(value), quote=True)


def font_data():
    font = FONTS / "Poppins-Regular.ttf"

    if not font.exists():
        return ""

    output = CARDS / "poppins.woff"

    subprocess.run([
        "pyftsubset",
        str(font),
        f"--output-file={output}",
        "--flavor=woff",
        "--unicodes=U+0000-00FF,U+2010-205E"
    ], check=True)

    encoded = base64.b64encode(
        output.read_bytes()
    ).decode()

    return f"data:font/woff;base64,{encoded}"


FONT_URI = ""


def svg_start(width, height, delay=0):

    font = ""

    if FONT_URI:
        font = f"""
        @font-face {{
            font-family: Poppins;
            src: url('{FONT_URI}') format('woff');
        }}
        """

    animation = ""

    if not STATIC:
        animation = f"""
        .card {{
            opacity: 0;
            animation: appear .9s ease-out
            {delay}s forwards;
        }}

        .rise {{
            opacity: 0;
            animation: rise .8s ease-out
            {delay + .2}s forwards;
        }}

        @keyframes appear {{
            to {{ opacity: 1; }}
        }}

        @keyframes rise {{
            from {{
                opacity: 0;
                transform: translateY(15px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @media (prefers-reduced-motion: reduce) {{
            .card, .rise {{
                animation: none !important;
                opacity: 1 !important;
                transform: none !important;
            }}
        }}
        """

    return f"""
    <svg xmlns="http://www.w3.org/2000/svg"
         xmlns:xlink="http://www.w3.org/1999/xlink"
         width="{width}" height="{height}"
         viewBox="0 0 {width} {height}">

    <style>
        {font}
        text {{ font-family: Poppins, Arial, sans-serif; }}
        {animation}
    </style>

    <defs>
        <linearGradient id="background"
                        x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="{INK}"/>
            <stop offset="60%" stop-color="{MAROON}"/>
            <stop offset="100%" stop-color="{ROSE}"/>
        </linearGradient>
    </defs>

    <g class="card">
        <rect width="100%" height="100%"
              rx="22" fill="url(#background)"/>
    </g>
    """


def save_card(filename, svg):

    CARDS.mkdir(exist_ok=True)

    (CARDS / filename).write_text(
        svg + "\n</svg>",
        encoding="utf-8"
    )


# 1. HERO CARD

def hero_card():

    svg = svg_start(1000, 250, 0)

    svg += f"""
    <text x="50" y="48"
          fill="{PALE}" font-size="14"
          letter-spacing="4" class="rise">
        HELLO, I'M
    </text>

    <text x="48" y="120"
          fill="{LIGHT}" font-size="51"
          font-weight="600" class="rise">
        {escape(PROFILE['name'])}
    </text>

    <text x="50" y="160"
          fill="{PALE}" font-size="17"
          class="rise">
        {escape(PROFILE['about'])}
    </text>

    <path d="M50 190 H260"
          stroke="{PALE}" opacity=".5"/>

    <text x="50" y="220"
          fill="{PALE}" font-size="12"
          letter-spacing="2">
        IT · DESIGN · WEB · CREATIVE IDEAS
    </text>

    <circle cx="870" cy="120" r="68"
            fill="none" stroke="{PALE}"
            stroke-opacity=".5" stroke-width="2"/>

    <circle cx="870" cy="120" r="53"
            fill="{PALE}" fill-opacity=".12"/>

    <text x="870" y="139"
          fill="{LIGHT}" font-size="48"
          text-anchor="middle">
        S.
    </text>
    """

    save_card("hero.svg", svg)


# 2. THREE LINKED TILES

def link_card(link, index):

    svg = svg_start(320, 110, .3 + index * .2)

    svg += f"""
    <rect x="1" y="1" width="318" height="108"
          rx="18" fill="{PALE}"/>

    <circle cx="48" cy="55" r="27"
            fill="{MAROON}"/>

    <text x="48" y="63"
          fill="{LIGHT}" font-size="22"
          text-anchor="middle">
        {escape(link['symbol'])}
    </text>

    <text x="90" y="45"
          fill="{INK}" font-size="15"
          font-weight="600">
        {escape(link['name'])}
    </text>

    <text x="90" y="72"
          fill="{MAROON}" font-size="11">
        {escape(link['description'])}
    </text>

    <text x="290" y="63"
          fill="{ROSE}" font-size="20">
        ↗
    </text>
    """

    save_card(f"link-{index + 1}.svg", svg)


# 3. GITHUB CONTRIBUTION DATA

def get_contributions():

    token = os.getenv("GITHUB_TOKEN")

    if not token:
        raise RuntimeError("GITHUB_TOKEN is missing")

    query = """
    query($login:String!) {
      user(login:$login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks {
              contributionDays {
                date
                contributionCount
                weekday
              }
            }
          }
        }
      }
    }
    """

    payload = json.dumps({
        "query": query,
        "variables": {"login": USERNAME}
    }).encode()

    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )

    with urllib.request.urlopen(request) as response:
        result = json.load(response)

    if result.get("errors") or not result.get("data", {}).get("user"):
        raise RuntimeError(f"GitHub API error: {result.get('errors')}")

    calendar = result["data"]["user"][
        "contributionsCollection"
    ]["contributionCalendar"]

    days = [
        day
        for week in calendar["weeks"]
        for day in week["contributionDays"]
    ]

    monthly = defaultdict(int)

    for day in days:
        monthly[day["date"][:7]] += day["contributionCount"]

    active = [
        day for day in days
        if day["contributionCount"] > 0
    ]

    daily = {
        datetime.date.fromisoformat(day["date"]):
        day["contributionCount"]
        for day in days
    }

    today = datetime.date.today()

    if daily.get(today, 0) == 0:
        today -= datetime.timedelta(days=1)

    streak = 0

    while daily.get(today, 0) > 0:
        streak += 1
        today -= datetime.timedelta(days=1)

    weekdays = Counter()

    for day in active:
        weekdays[day["weekday"]] += day["contributionCount"]

    names = [
        "Sunday", "Monday", "Tuesday",
        "Wednesday", "Thursday", "Friday",
        "Saturday"
    ]

    data = {
        "total": calendar["totalContributions"],
        "months": [
            {"month": month, "count": count}
            for month, count in sorted(monthly.items())[-12:]
        ],
        "days": days,
        "current_streak": streak,
        "active_days": len(active),
        "busiest_day": (
            names[weekdays.most_common(1)[0][0]]
            if weekdays else "—"
        ),
        "updated_at": datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()
    }

    DATA.parent.mkdir(parents=True, exist_ok=True)

    DATA.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )

    return data


def load_data():

    try:
        return json.loads(DATA.read_text())
    except (OSError, json.JSONDecodeError):
        return {
            "total": 0,
            "months": [],
            "days": [],
            "current_streak": 0,
            "active_days": 0,
            "busiest_day": "—"
        }


# 4. MONTHLY ACTIVITY CARD

def activity_card(data):

    svg = svg_start(1000, 290, .6)

    svg += f"""
    <text x="40" y="45"
          fill="{LIGHT}" font-size="21"
          font-weight="600">
        CONTRIBUTION RHYTHM
    </text>
    """

    stats = [
        ("STREAK", f"{data['current_streak']} days"),
        ("ACTIVE DAYS", data["active_days"]),
        ("BUSIEST DAY", data["busiest_day"])
    ]

    for i, (label, value) in enumerate(stats):

        x = 640 + i * 110

        svg += f"""
        <text x="{x}" y="42"
              fill="{PALE}" font-size="10"
              text-anchor="middle">
            {escape(label)}
        </text>

        <text x="{x}" y="68"
              fill="{LIGHT}" font-size="15"
              text-anchor="middle">
            {escape(value)}
        </text>
        """

    months = data.get("months", [])
    maximum = max(
        [m["count"] for m in months] or [1]
    ) or 1

    x_start = 50
    y_base = 225
    chart_height = 120
    slot = 900 / max(len(months), 1)

    for i, month in enumerate(months):

        value = month["count"]
        height = max(3, chart_height * value / maximum)

        x = x_start + i * slot + slot * .2
        y = y_base - height

        month_number = int(month["month"][-2:])
        label = MONTHS[month_number - 1]

        svg += f"""
        <rect x="{x}" y="{y}"
              width="{slot * .58}" height="{height}"
              rx="5" fill="{ROSE}" class="rise"/>

        <text x="{x + slot * .29}" y="250"
              fill="{PALE}" font-size="11"
              text-anchor="middle">
            {label}
        </text>
        """

    svg += f"""
    <text x="50" y="275"
          fill="{PALE}" font-size="12">
        TOTAL CONTRIBUTIONS: {data['total']:,}
    </text>
    """

    save_card("activity.svg", svg)


# 5. INDIVIDUAL REPOSITORY CARDS

def repo_card(repo, index):

    svg = svg_start(1000, 155, 1 + index * .2)

    svg += f"""
    <rect x="1" y="1" width="998" height="153"
          rx="21" fill="{PALE}"/>

    <circle cx="65" cy="77" r="31"
            fill="{MAROON}"/>

    <text x="65" y="85"
          fill="{LIGHT}" font-size="22"
          text-anchor="middle">
        {index + 1}
    </text>

    <text x="120" y="60"
          fill="{INK}" font-size="22"
          font-weight="600">
        {escape(repo['name'])}
    </text>

    <text x="120" y="89"
          fill="{MAROON}" font-size="14">
        {escape(repo['description'])}
    </text>

    <text x="120" y="120"
          fill="{MUTED}" font-size="12">
        {escape(repo['language'])}
    </text>

    <text x="950" y="88"
          fill="{ROSE}" font-size="26"
          text-anchor="middle">
        ↗
    </text>
    """

    save_card(f"repo-{index + 1}.svg", svg)


# 6. CONTRIBUTION GRAPH

def contribution_graph(data):

    svg = svg_start(1000, 190, 1.5)

    svg += f"""
    <text x="40" y="42"
          fill="{LIGHT}" font-size="20"
          font-weight="600">
        A YEAR OF MAKING THINGS
    </text>
    """

    days = data.get("days", [])[-364:]

    cell = 10
    gap = 5
    start_x = 45
    start_y = 70

    for i, day in enumerate(days):

        col = i // 7
        row = i % 7

        count = day["contributionCount"]

        opacity = (
            .13 if count == 0
            else min(.95, .28 + count * .17)
        )

        x = start_x + col * (cell + gap)
        y = start_y + row * (cell + gap)

        svg += f"""
        <rect x="{x}" y="{y}"
              width="{cell}" height="{cell}"
              rx="2" fill="{ROSE}"
              opacity="{opacity}"/>
        """

    save_card("contributions.svg", svg)


# MAIN RENDERER

def main():

    global FONT_URI

    CARDS.mkdir(exist_ok=True)

    FONT_URI = font_data()

    if "--refresh-data" in os.sys.argv:
        data = get_contributions()
    else:
        data = load_data()

    hero_card()

    for i, link in enumerate(PROFILE["links"]):
        link_card(link, i)

    activity_card(data)

    for i, repo in enumerate(PROFILE["repos"]):
        repo_card(repo, i)

    contribution_graph(data)

    print("All profile cards rendered!")


if __name__ == "__main__":
    main()
