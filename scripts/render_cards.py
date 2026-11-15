#!/usr/bin/env python3
"""Renders every SVG card of the GitHub profile (no dependencies).

    python scripts/render_cards.py            # re-render from data/contributions.json
    python scripts/render_cards.py --fetch    # refresh the data from GitHub first
                                              # (needs GITHUB_TOKEN in the environment)

Edit CFG below to change text, links and repositories.
"""
import base64, datetime as dt, json, os, sys, urllib.request
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "cards"

CFG = dict(
    user="SaraUET",
    name="Sara Shafqat",
    tagline="Building things. Breaking patterns.",
    sub="IT \u2022 DESIGN \u2022 DEVELOPMENT \u2022 CREATIVE IDEAS",
    status="Available for opportunities",
    about=["BBIT graduate blending", "IT, business operations", "and a designer\u2019s eye."],
    about_foot="> Always learning...",
    stack=[["Python", "JavaScript", "HTML"], ["CSS", "React", "Git", "SQL"], ["UI/UX Design", "Business Ops"]],
    links=[("Portfolio", "https://saraUET.github.io", "portfolio"),
           ("LinkedIn", "https://linkedin.com/in/sarashafqat", "linkedin"),
           ("Instagram", "https://instagram.com/YOUR_INSTAGRAM", "instagram")],
    repos=[dict(name="CakeBlogSite", desc=["A baking-focused web project."], tag="HTML / CSS", icon="cake"),
           dict(name="Portfolio", desc=["My personal portfolio and", "creative work."], tag="HTML / CSS / JS", icon="laptop")],
)

# Colours sampled from the reference screenshot.
BORDER, TEXT, SOFT, BODY = "#702b3c", "#f5eaed", "#e6d1d5", "#da9ca9"
ACCENT, ROSE, SUB, MONTH = "#ee9bae", "#d0567a", "#df8ba7", "#d3aab2"
EMPTY = ["#2b0711", "#2f0813", "#340a16", "#390c19", "#3f0e1c", "#46111f"]
ACTIVE = ["#7d1f3c", "#a52a52", "#d03a68", "#f0577f"]

W, GAP, LEFT, RIGHT = 850, 10, 236, 602
H_ABOUT, H_STACK, H_SOCIAL = 146, 108, 70
H_BODY = H_ABOUT + H_STACK + H_SOCIAL + 2 * GAP      # 344
H_ACT = 196
H_HERO_FULL, H_HERO = 216, 186

STYLE = """<style>
.serif{font-family:'Cormorant Garamond','Playfair Display',Georgia,'Times New Roman',serif}
.mono{font-family:'JetBrains Mono','SF Mono',Consolas,'Courier New',monospace}
.sans{font-family:'Inter','Segoe UI',Helvetica,Arial,sans-serif}
.caret{animation:blink 1.1s steps(1) infinite}
.live{animation:pulse 2.4s ease-in-out infinite}
@keyframes blink{50%{opacity:0}}
@keyframes pulse{50%{opacity:.45}}
@media (prefers-reduced-motion:reduce){.caret,.live{animation:none}}
</style>"""


def defs():
    return f"""<defs>{STYLE}
<linearGradient id="gCard" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a0610"/><stop offset="1" stop-color="#130206"/></linearGradient>
<linearGradient id="gHero" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1d0409"/><stop offset=".55" stop-color="#0c0204"/><stop offset="1" stop-color="#16030a"/></linearGradient>
<linearGradient id="gStat" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#40101e"/><stop offset="1" stop-color="#2a0812"/></linearGradient>
<linearGradient id="gRepo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3e101b"/><stop offset="1" stop-color="#26080f"/></linearGradient>
<linearGradient id="gPill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a121c"/><stop offset="1" stop-color="#22090f"/></linearGradient>
<linearGradient id="gFade" x1="0" y1="0" x2="1" y2="0"><stop offset=".45" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="mGrid" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H_HERO_FULL}"><rect width="{W}" height="{H_HERO_FULL}" fill="url(#gFade)"/></mask>
<pattern id="pGrid" width="26" height="26" patternUnits="userSpaceOnUse"><path d="M26 0H0V26" fill="none" stroke="#b04462" stroke-opacity=".17"/></pattern>
<filter id="fCloud" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="11"/></filter>
<radialGradient id="gPuff" cx=".38" cy=".28" r=".85"><stop offset="0" stop-color="#e6a9b0"/><stop offset=".3" stop-color="#bf5a72"/><stop offset=".65" stop-color="#7a2640"/><stop offset="1" stop-color="#4a1424" stop-opacity="0"/></radialGradient>
<filter id="fPuff" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5.500"/></filter>
<filter id="fSoft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4"/></filter>
<clipPath id="cHeroF"><rect width="{W}" height="{H_HERO_FULL}" rx="16"/></clipPath>
<clipPath id="cHeroS"><rect width="{W}" height="{H_HERO}" rx="16"/></clipPath>
</defs>"""


def svg(w, h, body, title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<title>{esc(title)}</title>{defs()}{body}</svg>\n')


def frame(w, h, rx=14, fill="url(#gCard)", op=.85):
    return (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{rx}" fill="{fill}" stroke="{BORDER}" stroke-opacity="{op}"/>'
            f'<rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="{rx-1}" fill="none" stroke="#ffb0c0" stroke-opacity=".045"/>')


def T(x, y, s, size, fill, cls="mono", anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'dominant-baseline="central" {extra}>{esc(s)}</text>')


# ---------- icons (all drawn around 0,0) ----------
def spark(cx, cy, r, fill=ACCENT, op=1):
    k = r * .18
    return (f'<path d="M{cx} {cy-r}Q{cx+k} {cy-k} {cx+r} {cy}Q{cx+k} {cy+k} {cx} {cy+r}Q{cx-k} {cy+k} {cx-r} {cy}Q{cx-k} {cy-k} {cx} {cy-r}Z" '
            f'fill="{fill}" fill-opacity="{op}"/>')


def heart(x, y, s=1.0, stroke=ROSE):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M0 9S-8 4.200-8 -1.500A4.200 4.200 0 0 1 0 -3.200A4.200 4.200 0 0 1 8 -1.500C8 4.200 0 9 0 9Z" '
            f'transform="scale(.6) translate(0 -3)" fill="none" stroke="{stroke}" stroke-width="2"/></g>')


GLYPH = {  # 24x24 brand glyphs
    "github": "M12 .5a11.5 11.5 0 0 0-3.6 22.4c.6.1.8-.3.8-.6v-2c-3.2.7-3.9-1.5-3.9-1.5-.5-1.300-1.300-1.700-1.300-1.700-1-.7.1-.7.1-.7 1.200.1 1.800 1.200 1.800 1.200 1 1.800 2.700 1.300 3.400 1 .1-.8.4-1.300.7-1.600-2.600-.3-5.300-1.300-5.300-5.700 0-1.300.5-2.300 1.200-3.100-.1-.3-.5-1.500.1-3.100 0 0 1-.3 3.200 1.200a11 11 0 0 1 5.800 0c2.200-1.500 3.200-1.200 3.200-1.200.6 1.600.2 2.800.1 3.100.8.800 1.200 1.800 1.200 3.100 0 4.400-2.700 5.400-5.300 5.700.4.4.8 1.100.8 2.200v3.200c0 .3.2.7.8.6A11.500 11.500 0 0 0 12 .5Z",
    "linkedin": "M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9.5h4V21H3V9.5Zm7 0h3.8v1.6h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.6 4.8 6V21h-4v-5c0-1.2 0-2.8-1.7-2.8s-2 1.3-2 2.7V21h-4V9.5Z",
    "instagram": "M7 3h10a4 4 0 0 1 4 4v10a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4V7a4 4 0 0 1 4-4Zm0 2a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2H7Zm5 3a4 4 0 1 1 0 8 4 4 0 0 1 0-8Zm0 2a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm5.200-3.700a1 1 0 1 1 0 2 1 1 0 0 1 0-2Z",
    "portfolio": "M14 3h7v7h-2V6.400l-8.300 8.300-1.400-1.400L17.600 5H14V3ZM5 5h6v2H6v11h11v-5h2v7H4V5h1Z",
}


def glyph(name, cx, cy, size, fill=ACCENT):
    s = size / 24
    return f'<path d="{GLYPH[name]}" transform="translate({cx-size/2:.1f} {cy-size/2:.1f}) scale({s:.3f})" fill="{fill}"/>'


# ---------- data ----------
def load():
    p = ROOT / "data" / "contributions.json"
    d = json.loads(p.read_text()) if p.exists() else {}
    year = d.get("year", dt.date.today().year)
    return year, {x["date"]: x["count"] for x in d.get("days", [])}


def fetch(user, year):
    q = ("query($u:String!,$f:DateTime!,$t:DateTime!){user(login:$u){contributionsCollection(from:$f,to:$t)"
         "{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}")
    body = json.dumps({"query": q, "variables": {"u": user, "f": f"{year}-01-01T00:00:00Z", "t": f"{year}-12-31T23:59:59Z"}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", body,
                                 {"Authorization": "bearer " + os.environ["GITHUB_TOKEN"], "Content-Type": "application/json"})
    cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [{"date": d["date"], "count": d["contributionCount"]} for w in cal["weeks"] for d in w["contributionDays"]]
    (ROOT / "data" / "contributions.json").write_text(json.dumps({"year": year, "total": cal["totalContributions"], "days": days}, indent=1))


def stats(year, counts):
    total = sum(counts.values())
    active = sum(1 for v in counts.values() if v > 0)
    best = max(counts.items(), key=lambda kv: kv[1], default=(None, 0))
    busiest = "\u2014"
    if best[1] > 0:
        d = dt.date.fromisoformat(best[0]); busiest = f"{d:%b} {d.day}"
    today = dt.date.today()
    d = today if today.year == year else dt.date(year, 12, 31)
    if counts.get(d.isoformat(), 0) == 0:
        d -= dt.timedelta(1)
    streak = 0
    while counts.get(d.isoformat(), 0) > 0:
        streak += 1; d -= dt.timedelta(1)
    return total, streak, active, busiest


# ---------- cards ----------
def heat(year, counts, x0, y0, pitch=10.49, rp=10.5, size=8.6):
    first = dt.date(year, 1, 1)
    off = (first.weekday() + 1) % 7
    mx = max(counts.values(), default=0)
    out, d, i = [], first, off
    while d.year == year:
        col, row = divmod(i, 7)
        c = counts.get(d.isoformat(), 0)
        if c > 0:
            fill = ACTIVE[min(4, max(1, -(-4 * c // mx))) - 1]
        else:
            fill = EMPTY[((col * 5 + row * 11 + col * row * 3) % 9) // 2 if False else ((col * 5 + row * 11 + col * row * 3) % 9) // 2 % len(EMPTY)]
        out.append(f'<rect x="{x0+col*pitch:.1f}" y="{y0+row*rp:.1f}" width="{size}" height="{size}" rx="2" fill="{fill}"/>')
        d += dt.timedelta(1); i += 1
    for m in range(1, 13):
        col = (off + (dt.date(year, m, 1) - first).days) // 7
        out.append(T(f"{x0+col*pitch:.1f}", y0 + 7 * rp + 12, dt.date(year, m, 1).strftime("%b"), 8.8, MONTH))
    return "".join(out)


def about(w=LEFT, h=H_ABOUT):
    b = frame(w, h) + spark(26, 24, 7.5) + T(42, 24, "About Me", 17, TEXT, "serif", extra='font-weight="500"')
    for i, line in enumerate(CFG["about"]):
        b += T(18, 52 + i * 16, line, 10.5, BODY)
    b += f'<path d="M18 102H60" stroke="{BORDER}" stroke-opacity=".9"/>'
    b += T(18, 124, CFG["about_foot"], 10.5, ROSE) + heart(160, 124, 1.0)
    b += f'<path d="M150 146C178 120 205 112 236 104" stroke="#ee9bae" stroke-opacity=".12" fill="none"/>'
    return b


def stack(w=LEFT, h=H_STACK):
    b = frame(w, h)
    b += (f'<path d="M26 12 20 18l6 6M34 12l6 6-6 6M31 9l-3 18" transform="translate(-2 -1) scale(.72) translate(6 6)" '
          f'stroke="{ACCENT}" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    b += T(42, 17, "Tech Stack", 15, TEXT, "serif", extra='font-weight="500"')
    for r, row in enumerate(CFG["stack"]):
        x, cy = 18, 44 + r * 23
        for label in row:
            cw = len(label) * 5.4 + 18
            b += (f'<rect x="{x:.1f}" y="{cy-10}" width="{cw:.1f}" height="20" rx="9" fill="#340713" stroke="{BORDER}" stroke-opacity=".7"/>'
                  + T(f"{x+cw/2:.1f}", cy, label, 8.8, "#dec4c7", anchor="middle"))
            x += cw + 7
    return b


def social(w=LEFT, h=H_SOCIAL):
    b = frame(w, h) + heart(24, 16, 1.0) + T(36, 16, "Find Me Elsewhere", 8.8, TEXT)
    for i, g in enumerate(["github", "linkedin", "instagram"]):
        cx, cy = 31 + i * 52, 43
        b += (f'<circle cx="{cx}" cy="{cy}" r="15.5" fill="#2a0a12" stroke="{BORDER}" stroke-opacity=".9"/>' + glyph(g, cx, cy, 15))
    return b


def activity(year, counts, w=RIGHT, h=H_ACT):
    total, streak, active, busiest = stats(year, counts)
    b = frame(w, h)
    b += (f'<rect x="19" y="26" width="3.500" height="9" fill="{ACCENT}"/><rect x="25" y="18" width="3.500" height="17" fill="{ACCENT}"/>'
          f'<rect x="31" y="22" width="3.500" height="13" fill="{ACCENT}"/>')
    b += T(42, 21, "GitHub Activity", 17, TEXT, "serif", extra='font-weight="500"')
    b += T(w - 34, 21, "A little progress, day by day", 8.6, "#e05f82", anchor="end") + heart(w - 24, 21, .9)
    bw = (w - 44 - 30) / 4
    items = [("Total Commits", str(total), ""), ("Current Streak", str(streak), "days"), ("Active Days", str(active), ""), ("Busiest Day", busiest, "")]
    for i, (lab, val, unit) in enumerate(items):
        x = 22 + i * (bw + 10)
        b += (f'<rect x="{x:.1f}" y="40" width="{bw:.1f}" height="48" rx="10" fill="url(#gStat)" stroke="#6a2538" stroke-opacity=".8"/>'
              + T(f"{x+14:.1f}", 54, lab, 8.8, SOFT, "sans")
              + T(f"{x+14:.1f}", 74, val, 22, "#f8e7ec", "serif", extra='font-weight="500"'))
        if unit:
            b += T(f"{x+14+len(val)*11+6:.1f}", 76, unit, 9.5, SOFT, "sans")
    b += heat(year, counts, 23, 100)
    return b


def contributions(year, counts, w=RIGHT, h=128):
    return frame(w, h) + heat(year, counts, 23, 22)


def repo_icon(kind, x, y):
    if kind == "cake":  # sharp vector cake slice, 44x44 box
        pk = "#e8a4b4"
        body = (
            '<defs>'
            '<linearGradient id="cEdge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e3a6b6"/><stop offset="1" stop-color="#b4607a"/></linearGradient>'
            '<linearGradient id="cTop" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#dc90a4"/><stop offset=".6" stop-color="#c26a83"/><stop offset="1" stop-color="#9a4560"/></linearGradient>'
            '<linearGradient id="cBand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4a1428"/><stop offset="1" stop-color="#2e0a16"/></linearGradient>'
            '<filter id="cGlow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="1.800"/></filter></defs>'
            '<path d="M9.500 28 24 15Q34 11 46 19L46.500 38.500 10 49.500Z" fill="#e8708f" fill-opacity=".16" filter="url(#cGlow)"/>'
            '<path d="M9.500 28 24 15Q34 11 46 19L46.500 38.500 10 49.500Z" fill="url(#cBand)"/>'
            '<path d="M9.500 28 24 15Q34 11 46 19L46 22 9.500 32Z" fill="url(#cTop)"/>'
            '<path d="M10 28.500 24.500 15.800Q34 12 44.500 18.500" fill="none" stroke="#f2c2cd" stroke-opacity=".4" stroke-width=".8" stroke-linecap="round"/>'
            '<path d="M9.500 30.800 46 21.200" stroke="url(#cEdge)" stroke-width="1.500" fill="none"/>'
            '<path d="M10 40.500 46 29.600" stroke="url(#cEdge)" stroke-width="1.400" fill="none"/>'
            '<ellipse cx="27.800" cy="35.100" rx="1.600" ry="1" transform="rotate(-17 27.800 35.100)" fill="#4a1428" stroke="#d98ba0" stroke-width=".7"/>'
            '<path d="M9.500 28 24 15Q34 11 46 19L46.500 38.500 10 49.500Z" fill="none" stroke="url(#cEdge)" stroke-width="1.500" stroke-linejoin="round"/>'
            '<path d="M9.800 28.500 10.100 49" stroke="#e3a6b6" stroke-width=".8" stroke-opacity=".5" fill="none"/>'
            '<path d="M24.500 11.200 26.200 17.300 30.600 17.500 32.200 11.800Z" fill="#d98ba0" stroke="#eab4c1" stroke-width=".8" stroke-linejoin="round"/>'
            '<path d="M25 12.300 31.800 12.700" stroke="#a8506a" stroke-width=".7"/>'
            '<ellipse cx="32.600" cy="13.600" rx="2.700" ry="3" fill="#4a1022" stroke="#d98ba0" stroke-width=".8"/>'
            '<path d="M29.500 11.500 30.300 8 32.500 11" fill="#b4607a" stroke="#d98ba0" stroke-width=".6" stroke-linejoin="round"/>')
        return f'<g transform="translate({x-6} {y-6})">{body}</g>'
    st = f'fill="none" stroke="{ACCENT}" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round"'
    d = "M7 6h26a2 2 0 0 1 2 2v17H5V8a2 2 0 0 1 2-2ZM1 31h38l-3-6H4Z"
    return f'<g transform="translate({x} {y})"><path d="{d}" {st}/></g>'
    st = f'fill="none" stroke="{ACCENT}" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round"'
    if kind == "cake":
        d = "M2 14 30 7l4 9L6 23ZM6 23v13l28-7V16M18 11l1.600 8M24 4.500a2 2 0 1 1 .1 0"
    else:
        d = "M7 6h26a2 2 0 0 1 2 2v17H5V8a2 2 0 0 1 2-2ZM1 31h38l-3-6H4Z"
    return f'<g transform="translate({x} {y})"><path d="{d}" {st}/></g>'


def repo(r, w=295, h=84):
    cy = h - 19
    b = frame(w, h, 12, "url(#gRepo)", .7) + repo_icon(r["icon"], 18, h / 2 - 20)
    b += T(78, 21, r["name"], 15.5, "#ecd0d7", "serif", extra='font-weight="600"')
    for i, line in enumerate(r["desc"]):
        b += T(78, 36 + i * 11, line, 8, "#c77691")
    b += f'<circle cx="82" cy="{h-19}" r="3" fill="#c95b7b"/>' + T(91, h - 19, r["tag"], 8.5, "#cfa0aa")
    b += (f'<circle cx="{w-24}" cy="{cy}" r="11" fill="none" stroke="{BORDER}"/>'
          f'<path d="M{w-29} {cy}H{w-19}M{w-23} {cy-4}l4 4-4 4" stroke="{ACCENT}" fill="none" stroke-width="1.300" stroke-linecap="round"/>')
    return b


def featured(counts_unused=None, w=RIGHT, h=H_BODY - H_ACT - GAP):
    b = frame(w, h)
    b += (f'<path d="M24 17l2.300 4.800 5.200.7-3.800 3.600 1 5.200-4.700-2.600-4.700 2.600 1-5.200-3.800-3.600 5.200-.7Z" transform="translate(-3 -4) scale(.95)" fill="{ACCENT}"/>')
    b += T(42, 21, "Featured Repositories", 17, TEXT, "serif", extra='font-weight="500"')
    b += T(w - 36, 21, "View all", 8.8, SOFT, anchor="end")
    b += f'<path d="M{w-30} 21h9M{w-25} 17l4 4-4 4" stroke="{SOFT}" fill="none" stroke-width="1.200"/>'
    cw, ch = (w - 28 - 12) / 2, h - 44 - 14
    for i, r in enumerate(CFG["repos"]):
        b += f'<g transform="translate({14 + i*(cw+12):.1f} 44)">{repo(r, cw, ch)}</g>'
    return b


def pill(x, y, w, label, icon):
    return (f'<g transform="translate({x} {y})"><rect x=".5" y=".5" width="{w-1}" height="29" rx="14.500" fill="url(#gPill)" stroke="{BORDER}" stroke-opacity=".95"/>'
            + glyph(icon, 20, 15, 12) + T(34, 15.5, label, 9.5, "#e7c6cf", "sans") + '</g>')


PILL_W = [96, 96, 104]


def avatar(cx, cy, ring, hid):
    p = ROOT / "data" / "avatar.jpg"
    r = ring - 9
    b = (f'<circle cx="{cx}" cy="{cy}" r="{ring}" fill="none" stroke="#d05a78" stroke-opacity=".5" filter="url(#fSoft)" stroke-width="3"/>'
         f'<circle cx="{cx}" cy="{cy}" r="{ring}" fill="none" stroke="#e0708c" stroke-opacity=".7"/>'
         f'<circle cx="{cx}" cy="{cy}" r="{ring-4.5}" fill="none" stroke="#b8405f" stroke-opacity=".55"/>')
    if p.exists():
        uri = "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()
        b += (f'<clipPath id="{hid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
              f'<image href="{uri}" x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{hid})"/>')
    else:
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#2a0610"/>' + T(cx, cy, "S", 48, ACCENT, "serif", "middle")
    return b


def hero(full=True):
    H = H_HERO_FULL if full else H_HERO
    dy = 0 if full else -14
    clip = "cHeroF" if full else "cHeroS"
    b = f'<rect width="{W}" height="{H}" rx="16" fill="url(#gHero)"/>'
    b += f'<g clip-path="url(#{clip})">'
    b += f'<rect width="{W}" height="{H_HERO_FULL}" fill="url(#pGrid)" mask="url(#mGrid)"/>'
    b += f'<ellipse cx="740" cy="{H+5}" rx="190" ry="70" fill="#5e1a2e" fill-opacity=".85" filter="url(#fCloud)"/>'
    puffs = [(628, H - 14, 58, 36), (676, H - 40, 60, 46), (726, H - 62, 62, 48), (782, H - 86, 58, 48), (836, H - 100, 52, 44),
             (850, H - 58, 52, 46), (796, H - 34, 70, 46), (722, H - 8, 66, 30), (590, H + 4, 50, 26), (668, H - 78, 34, 26)]
    for cx, cy, rx, ry in puffs:
        b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#gPuff)" filter="url(#fPuff)"/>'
    b += '</g>'
    b += f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{BORDER}" stroke-opacity=".85"/>'
    b += spark(32, 36, 12) + spark(494, 60 + dy, 5, ACCENT, .8) + spark(598, H - 37, 4, ACCENT, .8)
    b += avatar(90, 122 if full else 93, 83 if full else 78, f"cAv{H}")
    b += (f'<rect x="703" y="{24}" width="143" height="24" rx="12" fill="#14030a" fill-opacity=".85" stroke="{BORDER}"/>'
          '<circle class="live" cx="717" cy="36" r="3.500" fill="#2fd47a"/>'
          + T(727, 36.5, CFG["status"], 9, "#d9c4c8", "sans", extra='textLength="105"'))
    b += T(210, 76 + dy, CFG["name"], 43, TEXT, "serif", extra='textLength="226" font-weight="500"')
    b += T(210, 120 + dy, "> " + CFG["tagline"], 12.6, SOFT, extra='textLength="276"')
    b += f'<rect class="caret" x="{210+280}" y="{113+dy}" width="7" height="14" fill="#d9607e"/>'
    b += T(210, 144 + dy, CFG["sub"], 9.5, SUB, extra='textLength="322"')
    if full:
        x = 210
        for (label, _, icon), pw in zip(CFG["links"], PILL_W):
            b += pill(x, 166, pw, label, icon); x += pw + 8
    return b


def grid(year, counts):
    b = (f'<g>{about()}</g><g transform="translate(0 {H_ABOUT+GAP})">{stack()}</g>'
         f'<g transform="translate(0 {H_ABOUT+H_STACK+2*GAP})">{social()}</g>'
         f'<g transform="translate({LEFT+12} 0)">{activity(year, counts)}</g>'
         f'<g transform="translate({LEFT+12} {H_ACT+GAP})">{featured()}</g>')
    return b


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def main():
    year = dt.date.today().year
    if "--fetch" in sys.argv:
        fetch(CFG["user"], year)
    year, counts = load()
    GW = LEFT + 12 + RIGHT
    write("cards/hero.svg", svg(W, H_HERO, hero(False), CFG["name"]))
    for i, ((label, _, icon), pw) in enumerate(zip(CFG["links"], PILL_W), 1):
        write(f"cards/link-{i}.svg", svg(pw, 30, pill(0, 0, pw, label, icon), label))
    write("cards/about.svg", svg(LEFT, H_ABOUT, about(), "About me"))
    write("cards/stack.svg", svg(LEFT, H_STACK, stack(), "Tech stack"))
    write("cards/social.svg", svg(LEFT, H_SOCIAL, social(), "Find me elsewhere"))
    write("cards/activity.svg", svg(RIGHT, H_ACT, activity(year, counts), "GitHub activity"))
    write("cards/contributions.svg", svg(RIGHT, 128, contributions(year, counts), "Contribution calendar"))
    for i, r in enumerate(CFG["repos"], 1):
        write(f"cards/repo-{i}.svg", svg(295, 84, repo(r), r["name"]))
    write("cards/grid.svg", svg(GW, H_BODY, grid(year, counts), "Profile details"))
    full = hero(True) + f'<g transform="translate(0 {H_HERO_FULL+12})">{grid(year, counts)}</g>'
    write("profile.svg", svg(W, H_HERO_FULL + 12 + H_BODY, '<rect width="850" height="572" fill="#050102"/>' + full, CFG["name"]))
    print("Rendered", len(list(CARDS.glob("*.svg"))), "cards + profile.svg")


if __name__ == "__main__":
    main()
