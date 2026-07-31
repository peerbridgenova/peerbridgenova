#!/usr/bin/env python3
"""Generates the PeerBridge static site. No dependencies. Run: python3 _build.py"""
import os, re

OUT = os.path.dirname(os.path.abspath(__file__))
IG = "https://www.instagram.com/peerbridgenova/"
EMAIL = "peerbridgenova@gmail.com"

# palette (mirrors styles.css)
SKY, SKYD, CREAM, TEAL, TEALD, TEALI, GOLD, GOLDS, WHITE = (
    "#eaf5f9", "#d8ecf3", "#fdf9f1", "#1198b8", "#0c6d86", "#0a3f4f",
    "#d4b14d", "#f8edd2", "#ffffff")


# =========================================================== ILLUSTRATIONS
# Every one of these sits inside <div class="illus">. To swap any for a real
# photo, replace the <svg>...</svg> with <img src="assets/img/your-photo.jpg" alt="">

def person(x, base, color, head=None, s=1.0):
    """Abstract figure: rounded shoulders + head. `base` is where the feet sit."""
    head = head or color
    w, bh, r = 20 * s, 24 * s, 13 * s
    return (f'<path d="M{x-w:.0f} {base}a{w:.0f} {bh:.0f} 0 0 1 {2*w:.0f} 0z" fill="{color}"/>'
            f'<circle cx="{x}" cy="{base-bh-r+3:.0f}" r="{r:.0f}" fill="{head}"/>')


def _bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])

# arch bezier, so the hangers land exactly on the curve
_A = ((198, 386), (240, 186), (400, 186), (442, 386))
_DECK = 300

def _hangers():
    out = []
    for t in (0.22, 0.5, 0.78):
        x, y = _bez(*_A, t)
        out.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{x:.0f}" y2="{_DECK}" '
                   f'stroke="{GOLD}" stroke-width="5" stroke-linecap="round" opacity=".65"/>')
    return "".join(out)


HERO = f'''<svg viewBox="0 0 640 470" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Two groups of people connected by a bridge">
  <rect width="640" height="470" fill="{SKY}"/>

  <!-- sun -->
  <circle cx="498" cy="106" r="80" fill="{GOLDS}"/>
  <circle cx="498" cy="106" r="46" fill="{GOLD}" opacity=".55"/>

  <!-- clouds -->
  <g fill="{WHITE}" opacity=".9">
    <ellipse cx="104" cy="88" rx="52" ry="24"/>
    <ellipse cx="140" cy="76" rx="34" ry="20"/>
    <ellipse cx="70" cy="80" rx="28" ry="17"/>
  </g>
  <g fill="{WHITE}" opacity=".6">
    <ellipse cx="252" cy="128" rx="34" ry="15"/>
    <ellipse cx="272" cy="120" rx="22" ry="12"/>
  </g>
  <circle cx="330" cy="74" r="6" fill="{TEAL}" opacity=".3"/>
  <circle cx="382" cy="132" r="9" fill="{TEAL}" opacity=".2"/>
  <circle cx="196" cy="152" r="5" fill="{GOLD}" opacity=".6"/>

  <!-- water -->
  <rect y="386" width="640" height="84" fill="#c2dfea"/>
  <path d="M238 418q12-8 24 0t24 0M330 440q12-8 24 0t24 0M262 452q10-7 20 0t20 0" fill="none" stroke="{WHITE}" stroke-width="4" stroke-linecap="round" opacity=".6"/>

  <!-- banks -->
  <path d="M0 470V384a34 34 0 0 1 34-34h152a34 34 0 0 1 34 34v86z" fill="{SKYD}"/>
  <path d="M640 470V384a34 34 0 0 0-34-34H454a34 34 0 0 0-34 34v86z" fill="{SKYD}"/>

  <!-- bridge -->
  <path d="M{_A[0][0]} {_A[0][1]}C{_A[1][0]} {_A[1][1]} {_A[2][0]} {_A[2][1]} {_A[3][0]} {_A[3][1]}" fill="none" stroke="{GOLD}" stroke-width="12" stroke-linecap="round"/>
  {_hangers()}
  <line x1="188" y1="{_DECK}" x2="452" y2="{_DECK}" stroke="{GOLD}" stroke-width="13" stroke-linecap="round"/>
  <line x1="188" y1="{_DECK}" x2="452" y2="{_DECK}" stroke="{WHITE}" stroke-width="3" stroke-linecap="round" opacity=".45"/>

  <!-- figures -->
  {person(74, 384, TEALD)}
  {person(134, 384, TEAL)}
  {person(320, _DECK - 6, TEALD, GOLD)}
  {person(506, 384, TEAL)}
  {person(566, 384, TEALD)}

  <circle cx="48" cy="424" r="7" fill="{TEAL}" opacity=".18"/>
  <circle cx="600" cy="430" r="9" fill="{TEAL}" opacity=".18"/>
</svg>'''


ILL_TALK = f'''<svg viewBox="0 0 520 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Two people in conversation">
  <rect width="520" height="400" fill="{SKY}"/>
  <circle cx="440" cy="72" r="62" fill="{GOLDS}"/>
  <circle cx="72" cy="330" r="46" fill="{SKYD}"/>
  <path d="M74 96h206a30 30 0 0 1 30 30v78a30 30 0 0 1-30 30H140l-42 38v-38H74a30 30 0 0 1-30-30v-78a30 30 0 0 1 30-30z" fill="{WHITE}"/>
  <rect x="82" y="134" width="150" height="13" rx="6.5" fill="{SKYD}"/>
  <rect x="82" y="162" width="188" height="13" rx="6.5" fill="{SKYD}"/>
  <rect x="82" y="190" width="106" height="13" rx="6.5" fill="{GOLD}" opacity=".5"/>
  <path d="M478 196H310a26 26 0 0 0-26 26v66a26 26 0 0 0 26 26h122l38 32v-32h8a26 26 0 0 0 26-26v-66a26 26 0 0 0-26-26z" fill="{TEALD}"/>
  <rect x="306" y="230" width="140" height="12" rx="6" fill="{WHITE}" opacity=".55"/>
  <rect x="306" y="256" width="98" height="12" rx="6" fill="{WHITE}" opacity=".35"/>
  {person(120, 372, TEALD)}
  {person(400, 372, TEAL)}
</svg>'''


ILL_COMMUNITY = f'''<svg viewBox="0 0 520 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Overlapping circles representing community">
  <rect width="520" height="400" fill="{SKY}"/>
  <circle cx="190" cy="160" r="118" fill="{TEAL}" opacity=".22"/>
  <circle cx="330" cy="160" r="118" fill="{GOLD}" opacity=".28"/>
  <circle cx="260" cy="266" r="118" fill="{TEALD}" opacity=".20"/>
  <circle cx="260" cy="196" r="46" fill="{WHITE}"/>
  {person(260, 226, TEALD)}
  <circle cx="86" cy="72" r="9" fill="{GOLD}" opacity=".6"/>
  <circle cx="452" cy="330" r="12" fill="{TEAL}" opacity=".35"/>
  <circle cx="60" cy="326" r="6" fill="{TEAL}" opacity=".4"/>
  <circle cx="436" cy="66" r="6" fill="{TEALD}" opacity=".35"/>
</svg>'''


ILL_RESOURCES = f'''<svg viewBox="0 0 520 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Stacked cards of resources">
  <rect width="520" height="400" fill="{SKY}"/>
  <circle cx="452" cy="86" r="58" fill="{GOLDS}"/>
  <rect x="118" y="96" width="290" height="200" rx="26" fill="{SKYD}" transform="rotate(-7 263 196)"/>
  <rect x="126" y="104" width="290" height="200" rx="26" fill="{WHITE}" transform="rotate(3 271 204)"/>
  <rect x="158" y="140" width="164" height="15" rx="7.5" fill="{TEALD}" opacity=".8" transform="rotate(3 240 147)"/>
  <rect x="156" y="178" width="222" height="12" rx="6" fill="{SKYD}" transform="rotate(3 267 184)"/>
  <rect x="158" y="208" width="200" height="12" rx="6" fill="{SKYD}" transform="rotate(3 258 214)"/>
  <rect x="160" y="238" width="112" height="12" rx="6" fill="{GOLD}" opacity=".55" transform="rotate(3 216 244)"/>
  <circle cx="86" cy="322" r="40" fill="{TEAL}" opacity=".18"/>
  <circle cx="446" cy="320" r="16" fill="{GOLD}" opacity=".45"/>
</svg>'''


ILL_GROW = f'''<svg viewBox="0 0 520 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A growing team">
  <rect width="520" height="400" fill="{SKY}"/>
  <circle cx="260" cy="230" r="150" fill="{WHITE}" opacity=".7"/>
  <path d="M110 250a150 150 0 0 1 300 0" fill="none" stroke="{GOLD}" stroke-width="10" stroke-linecap="round" opacity=".55"/>
  <path d="M150 250a110 110 0 0 1 220 0" fill="none" stroke="{TEAL}" stroke-width="8" stroke-linecap="round" opacity=".4"/>
  {person(150, 320, TEALD)}
  {person(260, 320, TEAL)}
  {person(370, 320, TEALD)}
  <circle cx="205" cy="292" r="16" fill="{GOLDS}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="5 5"/>
  <circle cx="315" cy="292" r="16" fill="{GOLDS}" stroke="{GOLD}" stroke-width="3" stroke-dasharray="5 5"/>
  <circle cx="96" cy="98" r="8" fill="{GOLD}" opacity=".6"/>
  <circle cx="430" cy="112" r="12" fill="{TEAL}" opacity=".3"/>
</svg>'''


ILL_STORY = f'''<svg viewBox="0 0 520 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Someone writing their story">
  <rect width="520" height="400" fill="{SKY}"/>
  <circle cx="428" cy="300" r="76" fill="{SKYD}"/>
  <circle cx="104" cy="88" r="52" fill="{GOLDS}"/>
  <rect x="120" y="70" width="266" height="272" rx="28" fill="{WHITE}"/>
  <rect x="156" y="118" width="130" height="16" rx="8" fill="{TEALD}" opacity=".85"/>
  <rect x="156" y="158" width="196" height="12" rx="6" fill="{SKYD}"/>
  <rect x="156" y="188" width="180" height="12" rx="6" fill="{SKYD}"/>
  <rect x="156" y="218" width="196" height="12" rx="6" fill="{SKYD}"/>
  <rect x="156" y="248" width="120" height="12" rx="6" fill="{SKYD}"/>
  <path d="M300 272q22-8 34 6t-14 26q-14 8-26 2" fill="none" stroke="{GOLD}" stroke-width="7" stroke-linecap="round"/>
  <path d="M368 224l40-42a20 20 0 0 1 28 28l-42 40-32 6z" fill="{GOLD}"/>
  <path d="M362 256l32-6-8-8z" fill="{TEALD}" opacity=".5"/>
  {person(430, 344, TEAL)}
</svg>'''


ILL_SUPPORT = f'''<svg viewBox="0 0 520 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Hands supporting a heart">
  <rect width="520" height="400" fill="{SKY}"/>
  <circle cx="260" cy="180" r="128" fill="{WHITE}" opacity=".75"/>
  <path d="M260 240c-58-40-88-70-88-104a44 44 0 0 1 88-16 44 44 0 0 1 88 16c0 34-30 64-88 104z" fill="{GOLD}"/>
  <path d="M260 240c-58-40-88-70-88-104a44 44 0 0 1 44-44" fill="none" stroke="{WHITE}" stroke-width="6" stroke-linecap="round" opacity=".55"/>
  <path d="M120 292c26-30 60-30 84-8l56 50 56-50c24-22 58-22 84 8" fill="none" stroke="{TEALD}" stroke-width="18" stroke-linecap="round"/>
  <circle cx="96" cy="102" r="9" fill="{GOLD}" opacity=".55"/>
  <circle cx="430" cy="96" r="13" fill="{TEAL}" opacity=".3"/>
  <circle cx="446" cy="352" r="7" fill="{TEAL}" opacity=".35"/>
</svg>'''


ILL_REACH = f'''<svg viewBox="0 0 520 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A message being sent">
  <rect width="520" height="400" fill="{SKY}"/>
  <circle cx="440" cy="96" r="66" fill="{GOLDS}"/>
  <circle cx="90" cy="316" r="52" fill="{SKYD}"/>
  <rect x="112" y="118" width="296" height="196" rx="28" fill="{WHITE}"/>
  <path d="M112 152l148 96 148-96" fill="none" stroke="{TEAL}" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="392" cy="126" r="28" fill="{GOLD}"/>
  <path d="M380 126l8 9 16-18" fill="none" stroke="{WHITE}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="86" cy="122" r="8" fill="{GOLD}" opacity=".55"/>
  <circle cx="452" cy="330" r="11" fill="{TEAL}" opacity=".3"/>
</svg>'''


ILL_DONE = f'''<svg viewBox="0 0 520 400" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Message received">
  <rect width="520" height="400" fill="{SKY}"/>
  <circle cx="260" cy="196" r="122" fill="{WHITE}" opacity=".8"/>
  <circle cx="260" cy="196" r="86" fill="{TEAL}" opacity=".16"/>
  <circle cx="260" cy="196" r="56" fill="{TEALD}"/>
  <path d="M236 196l16 17 33-36" fill="none" stroke="{WHITE}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="112" cy="92" r="12" fill="{GOLD}" opacity=".6"/>
  <circle cx="418" cy="112" r="8" fill="{TEAL}" opacity=".45"/>
  <circle cx="410" cy="316" r="16" fill="{GOLDS}"/>
  <circle cx="104" cy="308" r="9" fill="{TEAL}" opacity=".3"/>
</svg>'''


# --- small round icons (74x74) -------------------------------------------------
def icon(inner, bg=SKY):
    return f'<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><circle cx="32" cy="32" r="32" fill="{bg}"/>{inner}</svg>'

IC_EVENTS = icon(f'<circle cx="24" cy="26" r="7" fill="{TEALD}"/><circle cx="41" cy="26" r="7" fill="{GOLD}"/>'
                 f'<path d="M13 46a11 11 0 0 1 22 0z" fill="{TEALD}" opacity=".85"/>'
                 f'<path d="M30 46a11 11 0 0 1 22 0z" fill="{GOLD}" opacity=".85"/>')

IC_TALK = icon(f'<path d="M14 20h28a6 6 0 0 1 6 6v12a6 6 0 0 1-6 6H26l-10 8v-8h-2a6 6 0 0 1-6-6V26a6 6 0 0 1 6-6z" fill="{TEALD}"/>'
               f'<circle cx="22" cy="32" r="3" fill="{WHITE}"/><circle cx="31" cy="32" r="3" fill="{WHITE}"/><circle cx="40" cy="32" r="3" fill="{GOLD}"/>')

IC_BOOK = icon(f'<rect x="14" y="15" width="36" height="34" rx="6" fill="{WHITE}"/>'
               f'<rect x="20" y="23" width="24" height="4" rx="2" fill="{TEALD}"/>'
               f'<rect x="20" y="31" width="20" height="4" rx="2" fill="{SKYD}"/>'
               f'<rect x="20" y="39" width="14" height="4" rx="2" fill="{GOLD}"/>')

IC_HAND = icon(f'<path d="M32 44c-13-9-19-15-19-23a10 10 0 0 1 19-3 10 10 0 0 1 19 3c0 8-6 14-19 23z" fill="{GOLD}"/>', GOLDS)

IC_LINK = icon(f'<circle cx="22" cy="32" r="9" fill="{TEALD}"/><circle cx="42" cy="32" r="9" fill="{GOLD}"/>'
               f'<rect x="22" y="29" width="20" height="6" rx="3" fill="{TEAL}"/>')

IC_SHARE = icon(f'<circle cx="21" cy="32" r="7" fill="{TEALD}"/><circle cx="43" cy="21" r="7" fill="{GOLD}"/><circle cx="43" cy="43" r="7" fill="{TEAL}"/>'
                f'<path d="M27 29l11-5M27 35l11 5" stroke="{TEALD}" stroke-width="3" stroke-linecap="round"/>')

IC_HEART_SM = f'''<svg class="heart" viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <circle cx="22" cy="22" r="22" fill="{GOLDS}"/>
  <path d="M22 32c-9-6-13-10-13-15a7 7 0 0 1 13-2 7 7 0 0 1 13 2c0 5-4 9-13 15z" fill="{GOLD}"/>
</svg>'''


# --- article card mini-illustrations ------------------------------------------
def post_art(kind):
    a = {
      "stigma":  f'<circle cx="70" cy="60" r="42" fill="{TEAL}" opacity=".22"/><circle cx="130" cy="60" r="42" fill="{GOLD}" opacity=".3"/><path d="M40 100h120" stroke="{TEALD}" stroke-width="6" stroke-linecap="round" opacity=".4"/>',
      "support": f'<path d="M100 96c-26-18-40-31-40-47a20 20 0 0 1 40-7 20 20 0 0 1 40 7c0 16-14 29-40 47z" fill="{GOLD}"/><path d="M46 108c12-13 27-13 38-3" stroke="{TEALD}" stroke-width="7" stroke-linecap="round" fill="none"/><path d="M154 108c-12-13-27-13-38-3" stroke="{TEALD}" stroke-width="7" stroke-linecap="round" fill="none"/>',
      "burnout": f'<rect x="46" y="30" width="108" height="70" rx="16" fill="{WHITE}"/><path d="M62 82l24-30 22 26 16-18 14 22" stroke="{GOLD}" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/><circle cx="140" cy="46" r="10" fill="{TEAL}" opacity=".35"/>',
      "start":   f'<circle cx="100" cy="64" r="40" fill="{WHITE}"/><path d="M100 42v24l16 10" stroke="{TEALD}" stroke-width="7" stroke-linecap="round" fill="none"/><circle cx="44" cy="100" r="9" fill="{GOLD}" opacity=".6"/><circle cx="156" cy="98" r="7" fill="{TEAL}" opacity=".4"/>',
      "therapy": f'<rect x="40" y="34" width="60" height="66" rx="14" fill="{WHITE}"/><rect x="112" y="46" width="48" height="54" rx="12" fill="{TEALD}" opacity=".85"/><circle cx="70" cy="60" r="10" fill="{GOLD}"/><rect x="54" y="80" width="32" height="6" rx="3" fill="{SKYD}"/>',
      "policy":  f'<rect x="56" y="26" width="88" height="76" rx="14" fill="{WHITE}"/><rect x="72" y="46" width="56" height="7" rx="3.5" fill="{TEALD}"/><rect x="72" y="62" width="46" height="7" rx="3.5" fill="{SKYD}"/><rect x="72" y="78" width="34" height="7" rx="3.5" fill="{GOLD}" opacity=".7"/>',
    }[kind]
    return f'<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{a}</svg>'


# --- team avatars --------------------------------------------------------------
def avatar(i):
    combos = [(TEALD, "#2ba9c9"), (TEAL, "#0f7d99"), ("#0f7d99", TEAL), (TEALD, "#3fb3d0")]
    body, head = combos[i % 4]
    dash = ["10 240", "70 240", "130 240", "190 240"][i % 4]
    return (f'<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
            f'<circle cx="50" cy="50" r="50" fill="{SKY}"/>'
            f'<circle cx="50" cy="50" r="45" fill="none" stroke="{GOLD}" stroke-width="4" '
            f'stroke-linecap="round" stroke-dasharray="{dash}" opacity=".8"/>'
            f'<circle cx="50" cy="41" r="17" fill="{head}"/>'
            f'<path d="M17 100a33 33 0 0 1 66 0z" fill="{body}"/></svg>')


# --- curved section edges ------------------------------------------------------
def curve(pos, fill):
    """pos: 'top' fills downward from the edge above; 'bottom' fills upward."""
    if pos == "top":
        d = "M0 0C240 64 480 64 720 32S1200 0 1440 40V0z"
    else:
        d = "M0 88C240 24 480 24 720 56s480 32 720-8V88z"
    return (f'<div class="curve curve-{pos}" aria-hidden="true">'
            f'<svg viewBox="0 0 1440 88" preserveAspectRatio="none">'
            f'<path d="{d}" fill="{fill}"/></svg></div>')


BLOBS = '<div class="blobs" aria-hidden="true"><span class="blob blob-a"></span><span class="blob blob-b"></span><span class="blob blob-c"></span></div>'


# =========================================================== SHELL
NAV = [
    ("Home", "index.html", None),
    ("About", None, [
        ("Our Mission", "about.html", "Why PeerBridge exists"),
        ("Our Team", "team.html", "The students behind it"),
    ]),
    ("Resources", None, [
        ("Articles", "articles.html", "Reading on student wellbeing"),
        ("Glossary", "glossary.html", "Mental health terms, explained"),
    ]),
    ("Get Involved", None, [
        ("Join the Team", "get-involved.html", "Open and upcoming roles"),
        ("Share Your Story", "stories.html", "Tell us what you've lived"),
        ("Contact Us", "contact.html", "Questions and collaboration"),
    ]),
]

def build_nav(page):
    out = []
    for label, href, kids in NAV:
        if kids is None:
            cur = " current" if page == href else ""
            out.append(f'      <div class="nav-item"><a class="nav-link{cur}" href="{href}">{label}</a></div>')
        else:
            cur = " current" if any(page == k[1] for k in kids) else ""
            links = "\n".join(f'          <a href="{h}">{t}<small>{d}</small></a>' for t, h, d in kids)
            out.append(
                '      <div class="nav-item">\n'
                f'        <button class="nav-link{cur}" type="button" aria-haspopup="true" aria-expanded="false">{label}<span class="caret"></span></button>\n'
                f'        <div class="dropdown">\n{links}\n        </div>\n'
                '      </div>')
    return "\n".join(out)


def head(title, desc):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#eaf5f9">
<link rel="icon" href="assets/img/peerbridge-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,500;1,9..144,400&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>

<div class="announce">
  <div class="wrap">
    <span>Student-led mental health support in Northern Virginia</span>
    <a href="{IG}" target="_blank" rel="noopener">Follow @peerbridgenova</a>
  </div>
</div>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">
      <img src="assets/img/peerbridge-logo.png" alt="">
      <span>
        <span class="brand-name">PeerBridge</span>
        <span class="brand-tag">Mental health &amp; community</span>
      </span>
    </a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
    <nav id="site-nav" class="nav" aria-label="Main">
{{navitems}}
      <a class="btn btn-gold nav-cta" href="donate.html">Support Us</a>
    </nav>
  </div>
</header>

<main id="main">
'''


FOOT = f'''</main>

<div class="crisis">
  <div class="wrap">
    <div class="inner">
      {IC_HEART_SM}
      <p><strong>If you need help right now, you don't have to wait.</strong> Call or text <a href="tel:988">988</a> for the Suicide &amp; Crisis Lifeline, or text <strong>HOME</strong> to <a href="sms:741741">741741</a>. Both are free and staffed around the clock. In an emergency, call 911.</p>
    </div>
  </div>
</div>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <span class="brand-name">PeerBridge</span>
        <span class="brand-tag">Mental health &amp; community</span>
        <p class="footer-blurb">A student-led initiative working to make mental health support in Northern Virginia easier to find, easier to talk about, and easier to reach.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="about.html">Our Mission</a></li>
          <li><a href="team.html">Our Team</a></li>
        </ul>
      </div>
      <div>
        <h4>Resources</h4>
        <ul>
          <li><a href="articles.html">Articles</a></li>
          <li><a href="glossary.html">Glossary</a></li>
          <li><a href="stories.html">Stories</a></li>
        </ul>
      </div>
      <div>
        <h4>Get Involved</h4>
        <ul>
          <li><a href="get-involved.html">Join the Team</a></li>
          <li><a href="donate.html">Support Us</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; <span class="js-year">2026</span> PeerBridge &middot; a student organization, not a clinical or emergency service.</span>
      <div class="social">
        <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41-.56-.22-.96-.48-1.38-.9-.42-.42-.68-.82-.9-1.38-.16-.42-.36-1.06-.41-2.23C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16zm0 3.08A6.76 6.76 0 1 0 18.76 12 6.76 6.76 0 0 0 12 5.24zm0 11.15A4.39 4.39 0 1 1 16.39 12 4.39 4.39 0 0 1 12 16.39zm8.6-11.42a1.58 1.58 0 1 1-1.58-1.58 1.58 1.58 0 0 1 1.58 1.58z"/></svg>
        </a>
        <a href="mailto:{EMAIL}" aria-label="Email">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4.24-8 4.76-8-4.76V6l8 4.76L20 6z"/></svg>
        </a>
      </div>
    </div>
  </div>
</footer>

<script src="script.js"></script>
</body>
</html>
'''


def page(filename, title, desc, body):
    html = head(title, desc).replace("{navitems}", build_nav(filename)) + body + FOOT
    with open(os.path.join(OUT, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", filename)


# =========================================================== INDEX
page("index.html",
 "PeerBridge | Student-Led Mental Health in Northern Virginia",
 "PeerBridge is a student-led mental health initiative in Northern Virginia, making support easier to find, easier to talk about, and easier to reach.",
f'''
<section class="hero">
  {BLOBS}
  <div class="wrap">
    <div class="split wide-left">
      <div>
        <span class="kicker">Student-led &middot; Northern Virginia</span>
        <h1>You shouldn't have to figure it out alone.</h1>
        <p class="lead">PeerBridge is built by students who got tired of watching people struggle quietly. We make mental health support easier to find, easier to talk about, and easier to actually reach.</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="get-involved.html">Get involved</a>
          <a class="btn btn-soft" href="about.html">What we do</a>
        </div>
        <div class="hero-badges">
          <span>Free &amp; student-run</span>
          <span>No sign-up needed</span>
          <span>Built in NoVA</span>
        </div>
      </div>
      <div class="illus illus-plain">{HERO}</div>
    </div>
  </div>
  {curve("bottom", WHITE)}
</section>

<section class="band bg-white">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.8rem;">
      <span class="kicker">Why this matters</span>
      <h2 class="narrow center">The need is real, and it starts young</h2>
    </div>
  </div>
</section>

<section class="band-sm bg-deep on-deep" style="padding-bottom:clamp(4rem,7vw,6rem);">
  {BLOBS}
  {curve("top", WHITE)}
  <div class="wrap" style="padding-top:clamp(2rem,4vw,3rem);">
    <div class="figures">
      <div class="figure"><b>1 in 5</b><span>U.S. teens live with a mental health condition</span></div>
      <div class="figure"><b>~50%</b><span>of lifetime conditions begin by age 14</span></div>
      <div class="figure"><b>Under half</b><span>of affected youth receive any treatment</span></div>
      <div class="figure"><b>2nd</b><span>leading cause of death, ages 10&ndash;24</span></div>
    </div>
    <p style="margin-top:1.4rem;font-size:.83rem;color:#8fc0d1;">Sources: CDC and the National Institute of Mental Health.</p>
  </div>
  {curve("bottom", SKY)}
</section>

<section class="band bg-sky">
  <div class="wrap">
    <div class="split">
      <div class="illus illus-plain">{ILL_TALK}</div>
      <div>
        <span class="kicker">Who we are</span>
        <h2>A bridge, not a clinic</h2>
        <p class="lead">We're not therapists and we don't pretend to be. What we <em>are</em> is the people sitting next to you in class &mdash; the ones who can say the first honest thing, point you toward someone qualified, and make sure you don't have to Google your way through it.</p>
        <p>PeerBridge started because the distance between <span class="hand">something's wrong</span> and <span class="hand">I got help</span> is enormous, and almost nobody talks about how to cross it. That distance is our whole job.</p>
        <div class="btn-row"><a class="btn btn-soft" href="about.html">Read our mission</a></div>
      </div>
    </div>
  </div>
</section>

<section class="band bg-white">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.6rem;">
      <span class="kicker">What we do</span>
      <h2 class="narrow center">Three things, done properly</h2>
    </div>
    <div class="grid g3">
      <article class="card card-sky">
        <div class="illus-icon">{IC_EVENTS}</div>
        <h3>Show up in person</h3>
        <p>Wellness events, tabling, and campus programming people actually want to attend &mdash; not another assembly nobody remembers. Presence is what makes support feel real.</p>
      </article>
      <article class="card card-sky">
        <div class="illus-icon">{IC_TALK}</div>
        <h3>Start the honest conversation</h3>
        <p>Spaces where students talk about stress, burnout, and stigma without performing. No pressure to have a diagnosis or a tidy story.</p>
      </article>
      <article class="card card-sky">
        <div class="illus-icon">{IC_BOOK}</div>
        <h3>Translate the resources</h3>
        <p>Plain-language explanations of the terms and next steps that usually get buried in clinical language. Our <a class="arrow" href="glossary.html">glossary</a> is where that starts.</p>
      </article>
    </div>
  </div>
</section>

<section class="band bg-cream">
  <div class="wrap">
    <div class="split flip">
      <div>
        <span class="kicker">Stories</span>
        <h2>What it's really like</h2>
        <p class="lead">Statistics don't move people. People move people. We're collecting honest accounts from students in NoVA &mdash; the quiet wins, the hard weeks, the moment something shifted.</p>
        <p>If you've lived it, your story is worth more than any brochure we could write.</p>
        <div class="btn-row"><a class="btn btn-primary" href="stories.html">Share your story</a></div>
      </div>
      <div class="illus illus-plain">{ILL_STORY}</div>
    </div>
  </div>
</section>

<section class="band bg-deep on-deep">
  {BLOBS}
  <div class="wrap center">
    <span class="kicker">Get involved</span>
    <h2 class="narrow center">We're small on purpose &mdash; but not forever</h2>
    <p class="lead wide">PeerBridge is early. We're building the foundation properly before we grow. When we open applications for writers, designers, and outreach leads, this is where they'll be posted.</p>
    <div class="btn-row">
      <a class="btn btn-on-deep" href="get-involved.html">See upcoming roles</a>
      <a class="btn btn-outline-deep" href="contact.html">Reach out early</a>
    </div>
  </div>
</section>

<section class="band bg-white">
  <div class="wrap">
    <div class="split wide-left" style="align-items:start;">
      <div>
        <span class="kicker">Reading</span>
        <h2>From the blog</h2>
        <p class="lead">Writing on stigma, burnout, and how to support someone without needing all the answers.</p>
        <div class="btn-row"><a class="btn btn-soft" href="articles.html">All articles</a></div>
      </div>
      <div class="grid">
        <article class="card card-flat">
          <div class="meta"><span class="tag">Stigma</span><span>6 min</span></div>
          <h3>Breaking the stigma, one conversation at a time</h3>
          <p>How student-led communities make support feel safer and more visible than any poster campaign.</p>
        </article>
        <article class="card card-flat">
          <div class="meta"><span class="tag">Support</span><span>7 min</span></div>
          <h3>How to support a friend without having all the answers</h3>
          <p>Listening, noticing, and holding boundaries &mdash; the parts nobody teaches you.</p>
        </article>
      </div>
    </div>
  </div>
</section>
''')


# =========================================================== ABOUT
page("about.html", "Our Mission | PeerBridge",
 "Why PeerBridge exists: making mental health support in Northern Virginia visible, understandable, and reachable for students.",
f'''
<section class="page-head">
  {BLOBS}
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a><span>/</span>About<span>/</span>Our Mission</p>
    <div class="split wide-left">
      <div>
        <span class="kicker">Our mission</span>
        <h1>Closing the distance between struggling and getting help.</h1>
        <p class="lead wide">Knowing you need support and knowing how to get it are two completely different problems &mdash; and almost nobody helps students with the second one.</p>
      </div>
      <div class="illus illus-plain">{ILL_COMMUNITY}</div>
    </div>
  </div>
  {curve("bottom", WHITE)}
</section>

<section class="band bg-white">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="kicker">Why we started</span>
        <h2>The information exists. The path to it doesn't.</h2>
        <p>Every school has a counselor. Every district has a resource page. Most students still have no idea what to do when a friend says something that scares them, or when they themselves stop sleeping in October and don't start again until March.</p>
        <p>The problem isn't a shortage of services. It's that the route to them is invisible, intimidating, and written in a language nobody speaks. So people wait &mdash; often until things get much worse than they needed to.</p>
        <p>PeerBridge was built to be the missing step in between: the peer who says the honest thing first, explains what the words mean, and walks alongside you toward the person who's actually trained to help.</p>
      </div>
      <div class="illus illus-plain">{ILL_RESOURCES}</div>
    </div>
  </div>
</section>

<section class="band bg-sky">
  <div class="wrap">
    <div class="grid g2">
      <div class="quote">
        <span class="kicker">Mission</span>
        <p class="statement">Make mental health support in Northern Virginia visible, understandable, and genuinely reachable for every student who needs it.</p>
      </div>
      <div class="quote">
        <span class="kicker">Vision</span>
        <p class="statement">A school culture where asking for help is as unremarkable as asking for notes from a class you missed.</p>
      </div>
    </div>
  </div>
</section>

<section class="band bg-white">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.6rem;">
      <span class="kicker">How we work</span>
      <h2 class="narrow center">Four commitments we hold ourselves to</h2>
    </div>
    <div class="grid g4">
      <div class="card card-cream"><div class="card-num">01</div><h3>Peers, not experts</h3><p>We're students. We're clear about what we're not qualified to do, and we refer out early rather than late.</p></div>
      <div class="card card-cream"><div class="card-num">02</div><h3>Plain language</h3><p>If a resource needs a clinical vocabulary to understand, it isn't accessible. So we translate it.</p></div>
      <div class="card card-cream"><div class="card-num">03</div><h3>No performance</h3><p>Awareness that stops at a coloured ribbon isn't awareness. We'd rather do one useful thing than ten visible ones.</p></div>
      <div class="card card-cream"><div class="card-num">04</div><h3>Built to outlast us</h3><p>We're documenting how this works so PeerBridge survives its founders graduating.</p></div>
    </div>
  </div>
</section>

<section class="band bg-cream">
  <div class="wrap">
    <div class="split flip">
      <div>
        <span class="kicker">Where we are now</span>
        <h2>Honestly: early</h2>
        <p class="lead">PeerBridge is in its first year. We have a small founding team, a growing set of resources, and a clear plan &mdash; not a track record yet. We'd rather say that plainly than inflate what we've done.</p>
        <p>Practically, that means we're focused on building the resource library, running our first events, and getting the structure right before we expand. If you want to be part of the version of this that comes next, <a class="arrow" href="get-involved.html">that page is for you</a>.</p>
      </div>
      <div class="illus illus-plain">{ILL_GROW}</div>
    </div>
  </div>
</section>

<section class="band bg-deep on-deep">
  {BLOBS}
  <div class="wrap center">
    <h2 class="narrow center">Want to work with us?</h2>
    <p class="lead wide">Schools, counselors, student groups, and local organizations &mdash; we're actively looking for partners.</p>
    <div class="btn-row"><a class="btn btn-on-deep" href="contact.html">Start a conversation</a></div>
  </div>
</section>
''')


# =========================================================== TEAM
members = [
    ("Michael Mafanire", "President", "Sets direction and keeps PeerBridge pointed at student needs rather than whatever is easiest to post about.", "Can solve a Rubik's cube."),
    ("Jaisan Samatov", "Vice President", "Works on strategy, events, and outreach — the logistics of turning an intention into something that actually happens.", "Lucki, top artist four years running."),
    ("Anwar Kiyar", "Secretary", "Runs communication and the digital side, including this site. Makes sure things get written down.", "Types 140 WPM."),
    ("Nam Ngo", "Treasurer", "Keeps the organization sustainable behind the scenes so the plans we make are ones we can actually fund.", "Names any Travis Scott song in five seconds."),
]
mcards = "\n".join(
    f'''      <article class="member">
        <div class="face">{avatar(i)}</div>
        <h3>{n}</h3>
        <span class="role">{r}</span>
        <p>{b}</p>
        <p class="fact">{f}</p>
      </article>''' for i, (n, r, b, f) in enumerate(members))

page("team.html", "Our Team | PeerBridge",
 "Meet the founding student team behind PeerBridge.",
f'''
<section class="page-head">
  {BLOBS}
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a><span>/</span>About<span>/</span>Our Team</p>
    <div class="center">
      <span class="kicker">Our team</span>
      <h1 class="narrow center">The students who started this</h1>
      <p class="lead wide">A small founding team in Northern Virginia. We're building the structure now so the people who come after us inherit something that works.</p>
    </div>
  </div>
  {curve("bottom", WHITE)}
</section>

<section class="band bg-white">
  <div class="wrap">
    <div class="grid g4">
{mcards}
    </div>
    <p class="note note-sky" style="margin-top:2rem;"><strong>Those are illustrations, not photos.</strong> We'll swap in real ones as we take them.</p>
  </div>
</section>

<section class="band bg-sky">
  <div class="wrap">
    <div class="split">
      <div class="illus illus-plain">{ILL_GROW}</div>
      <div>
        <span class="kicker">Growing the team</span>
        <h2>Four people isn't the plan &mdash; it's the start</h2>
        <p class="lead">We're deliberately small right now. Once the foundation is solid, we'll open applications for writers, designers, outreach leads, and school chapter organizers.</p>
        <p>If you already know you want in, don't wait for a posting. Tell us what you'd want to build.</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="get-involved.html">Upcoming roles</a>
          <a class="btn btn-soft" href="contact.html">Introduce yourself</a>
        </div>
      </div>
    </div>
  </div>
</section>
''')


# =========================================================== ARTICLES
posts = [
 ("stigma","Stigma","6 min","Breaking the stigma, one conversation at a time","Awareness campaigns don't reduce stigma. Ordinary people saying ordinary true things do. What that looks like in a hallway, not a keynote."),
 ("support","Support","7 min","How to support a friend without having all the answers","You are not their therapist, and trying to be one usually backfires. A practical guide to listening, noticing changes, and keeping boundaries that protect both of you."),
 ("burnout","Burnout","5 min","Burnout isn't laziness and rest isn't a reward","What academic burnout actually does to attention, sleep, and motivation — and why “just try harder” makes it measurably worse."),
 ("start","First steps","4 min","Where to start when you don't know what help you need","A decision guide for the moment you know something's off but can't name it. Who to talk to first, what to expect, and what it costs."),
 ("therapy","Explainer","8 min","What actually happens in your first therapy appointment","Most of the fear is fear of the unknown. Here's the unknown, described step by step — including what you don't have to say."),
 ("policy","Explainer","6 min","Reading a school's mental health policy without falling asleep","Confidentiality, mandatory reporting, and what a counselor can and can't keep private. The parts that decide whether you talk to them."),
]
pcards = "\n".join(
 f'''      <article class="post">
        <div class="post-illus">{post_art(k)}</div>
        <div class="post-body">
          <div class="meta"><span class="tag{' tag-gold' if t=='Explainer' else ''}">{t}</span><span>{m}</span></div>
          <h3>{title}</h3>
          <p>{d}</p>
          <p style="margin-top:1rem;"><span class="tag">Coming soon</span></p>
        </div>
      </article>''' for k, t, m, title, d in posts)

page("articles.html", "Articles | PeerBridge",
 "Plain-language writing on student mental health, stigma, burnout, and how to support the people around you.",
f'''
<section class="page-head">
  {BLOBS}
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a><span>/</span>Resources<span>/</span>Articles</p>
    <div class="split wide-left">
      <div>
        <span class="kicker">Articles</span>
        <h1>Writing worth the time it takes to read.</h1>
        <p class="lead wide">Short, specific pieces on the things students actually deal with. No inspirational filler.</p>
      </div>
      <div class="illus illus-plain">{ILL_RESOURCES}</div>
    </div>
  </div>
  {curve("bottom", WHITE)}
</section>

<section class="band bg-white">
  <div class="wrap">
    <div class="grid g3">
{pcards}
    </div>
    <p class="note" style="margin-top:2.4rem;"><strong>These are our planned first pieces.</strong> We're writing them properly rather than publishing filler to look busy. Want to write one? <a href="get-involved.html">We'll need writers.</a></p>
  </div>
</section>

<section class="band bg-sky">
  <div class="wrap center">
    <h2 class="narrow center">In the meantime, the glossary is live</h2>
    <p class="lead wide">Thirty-two mental health terms explained in plain English, searchable.</p>
    <div class="btn-row"><a class="btn btn-primary" href="glossary.html">Open the glossary</a></div>
  </div>
</section>
''')


# =========================================================== GLOSSARY
TERMS = [
 ("Anxiety disorder","A group of conditions where fear or worry is persistent, out of proportion to the situation, and interferes with daily life. Different from ordinary nervousness, which passes once the stressor does.","Includes generalized anxiety, social anxiety, and panic disorder."),
 ("Attention-deficit/hyperactivity disorder (ADHD)","A neurodevelopmental condition affecting attention regulation, impulse control, and executive function. It is not a deficit of effort or intelligence.",None),
 ("Bipolar disorder","A condition involving episodes of unusually elevated mood and energy (mania or hypomania) alternating with periods of depression.",None),
 ("Boundary","A limit you set on your time, energy, or involvement. Setting one with a struggling friend is not abandonment &mdash; it is what makes long-term support possible.",None),
 ("Burnout","Exhaustion, cynicism, and reduced effectiveness caused by prolonged stress, most often from school or work. Recognized by the WHO as an occupational phenomenon rather than a medical diagnosis.",None),
 ("Cognitive behavioral therapy (CBT)","A structured, short-term therapy focused on identifying and changing unhelpful thought and behavior patterns. One of the most evidence-supported treatments for anxiety and depression.",None),
 ("Confidentiality","A provider's obligation to keep what you say private. It has legal limits &mdash; typically broken if someone is at serious risk of harm. Ask what the limits are before assuming them.","See also: mandatory reporting."),
 ("Coping mechanism","Anything you do to manage stress. Adaptive coping (sleep, movement, talking to someone) helps over time; maladaptive coping (avoidance, substance use) relieves the moment and worsens the pattern.",None),
 ("Crisis","An acute situation where someone is at immediate risk of harming themselves or others, or cannot function safely. Requires urgent professional help, not peer support alone.","In the U.S., call or text 988."),
 ("Depression","A mood disorder involving persistent low mood, loss of interest, and changes to sleep, appetite, energy, and concentration lasting two weeks or more. Clinically distinct from sadness.",None),
 ("Dissociation","Feeling detached from your body, thoughts, or surroundings &mdash; often described as unreality, or watching yourself from outside. Commonly linked to stress or trauma.",None),
 ("Eating disorder","A serious condition involving disturbed eating behaviors and distress about food, weight, or body shape. Among the highest-mortality mental health conditions, and highly treatable with early intervention.",None),
 ("Executive function","The mental processes that let you plan, start tasks, hold information in mind, and switch focus. Frequently disrupted by ADHD, depression, anxiety, and sleep deprivation.",None),
 ("Grounding","A set of techniques for reorienting to the present during anxiety, panic, or dissociation &mdash; typically using the senses, breath, or physical surroundings.",None),
 ("Intrusive thought","An unwanted, distressing thought that arrives without intent. Extremely common and, on its own, not an indication of what a person wants or will do.",None),
 ("Mandatory reporting","A legal duty requiring certain adults &mdash; including teachers and counselors &mdash; to report suspected abuse, neglect, or imminent danger to authorities.",None),
 ("Mental health","Emotional, psychological, and social wellbeing. It affects how you think, feel, handle stress, relate to others, and make decisions. Everyone has it; it isn't only relevant when something is wrong.",None),
 ("Obsessive-compulsive disorder (OCD)","A condition involving intrusive obsessions and compulsions performed to reduce the resulting distress. It is not a preference for tidiness.",None),
 ("Panic attack","A sudden surge of intense fear with physical symptoms &mdash; racing heart, shortness of breath, chest tightness, shaking. Typically peaks within ten minutes. Frightening, but not physically dangerous.",None),
 ("Peer support","Help offered by someone with comparable lived experience rather than clinical training. Effective for connection and navigation; not a substitute for treatment.","This is the category PeerBridge operates in."),
 ("Post-traumatic stress disorder (PTSD)","A condition that can follow a traumatic event, involving intrusive memories, avoidance, negative changes in mood, and heightened reactivity, persisting more than a month.",None),
 ("Psychiatrist","A medical doctor specializing in mental health who can diagnose conditions and prescribe medication.",None),
 ("Psychologist","A clinician trained in assessment and therapy, typically holding a doctorate. In most U.S. states, psychologists do not prescribe medication.",None),
 ("Resilience","The capacity to adapt and recover from difficulty. It is built through support, skills, and circumstances &mdash; not a fixed personal trait, and not a reason to withhold help.",None),
 ("Rumination","Repetitively cycling through the same distressing thoughts without moving toward resolution. A strong predictor of prolonged depression and anxiety.",None),
 ("Safety plan","A written, personalized plan listing warning signs, coping strategies, supportive people, and emergency contacts, prepared in advance for use during a crisis.",None),
 ("Self-care","Deliberate actions that maintain physical and mental health &mdash; sleep, nutrition, movement, connection, treatment adherence. Frequently trivialized; it is maintenance, not indulgence.",None),
 ("Self-harm","Deliberately injuring oneself, usually as a way of coping with overwhelming emotion. It warrants professional support and a non-judgmental response, not punishment or ultimatums.",None),
 ("Stigma","Negative beliefs and attitudes about mental illness that lead to shame, silence, and discrimination. One of the largest documented barriers to young people seeking help.",None),
 ("Therapy","Structured conversation with a trained clinician aimed at understanding and changing patterns in thought, emotion, or behavior. Many approaches exist; fit with the therapist matters as much as the method.","Also called counseling or psychotherapy."),
 ("Trigger","A stimulus that provokes a strong emotional or physiological reaction linked to past distress. A clinical term, distinct from the casual use meaning “annoyed”.",None),
 ("Warning signs","Observable changes that may indicate someone is struggling &mdash; withdrawal, sleep or appetite changes, giving away possessions, dropping activities, talking about being a burden.",None),
]

def term_block(t, d, a):
    plain = re.sub(r"<[^>]+>", "", t)
    also = f'<span class="also">{a}</span>' if a else ""
    return (f'      <div class="term" data-term="{plain}">\n'
            f'        <dt>{t}</dt>\n'
            f'        <dd>{d}{also}</dd>\n'
            f'      </div>')

term_html = "\n".join(term_block(*t) for t in TERMS)

page("glossary.html", "Glossary of Mental Health Terms | PeerBridge",
 "Plain-language definitions of the mental health terms students actually encounter, from anxiety disorder to warning signs.",
f'''
<section class="page-head">
  {BLOBS}
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a><span>/</span>Resources<span>/</span>Glossary</p>
    <div class="split wide-left">
      <div>
        <span class="kicker">Glossary</span>
        <h1>The words, in plain English.</h1>
        <p class="lead wide">Mental health language gets used loosely in conversation and precisely in a clinic. Here's what {len(TERMS)} of the most common terms actually mean.</p>
      </div>
      <div class="illus illus-plain">{ILL_RESOURCES}</div>
    </div>
  </div>
  {curve("bottom", WHITE)}
</section>

<section class="band bg-white">
  <div class="wrap">
    <div class="gloss-tools">
      <label for="gloss-search" class="hp">Search terms</label>
      <input id="gloss-search" class="gloss-search" type="search" placeholder="Search a term or definition&hellip;" autocomplete="off">
      <div class="alpha" id="gloss-alpha"></div>
    </div>

    <dl class="terms" id="glossary">
{term_html}
    </dl>

    <p class="no-results" id="gloss-empty" hidden>No terms match that search. Try a shorter word, or <a class="arrow" href="contact.html">suggest a term</a> we should add.</p>

    <p class="note" style="margin-top:2.4rem;"><strong>These are educational definitions, not diagnostic criteria.</strong> Recognizing yourself in a description here is a reason to talk to a qualified professional &mdash; not a reason to conclude you have a condition. PeerBridge does not diagnose or treat.</p>
  </div>
</section>

<section class="band bg-sky">
  <div class="wrap center">
    <div class="illus illus-plain" style="max-width:300px;margin:0 auto 1.8rem;">{ILL_REACH}</div>
    <h2 class="narrow center">A term we're missing?</h2>
    <p class="lead wide">If something confused you, it's confusing other people too. Tell us and we'll add it.</p>
    <div class="btn-row"><a class="btn btn-primary" href="contact.html">Suggest a term</a></div>
  </div>
</section>
''')


# =========================================================== STORIES
page("stories.html", "Stories | PeerBridge",
 "Honest accounts from students in Northern Virginia about mental health, and an invitation to share your own.",
f'''
<section class="page-head">
  {BLOBS}
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a><span>/</span>Get Involved<span>/</span>Share Your Story</p>
    <div class="split wide-left">
      <div>
        <span class="kicker">Stories</span>
        <h1>What's your story?</h1>
        <p class="lead wide">The quiet victories, the hard weeks, the moment something shifted. Told by students, in their own words.</p>
        <div class="btn-row"><a class="btn btn-primary" href="#share">Tell your story</a></div>
      </div>
      <div class="illus illus-plain">{ILL_STORY}</div>
    </div>
  </div>
  {curve("bottom", WHITE)}
</section>

<section class="band bg-white">
  <div class="wrap center">
    <span class="kicker">Why this page exists</span>
    <h2 class="narrow center">Statistics don't change minds. People do.</h2>
    <p class="lead wide">You can read that half of lifetime mental health conditions begin by age fourteen and feel nothing. You read one person describing the specific Tuesday they realized they needed help, and it lands.</p>
    <p class="lead wide">That's what this page is for. Not inspiration, not tidy redemption arcs &mdash; just accurate accounts from people who were there.</p>
  </div>
</section>

<section class="band bg-sky">
  <div class="wrap">
    <div class="center" style="margin-bottom:2rem;">
      <span class="kicker">Voices</span>
      <h2 class="narrow center">From the community</h2>
    </div>
    <div class="empty-state">
      <p class="statement" style="margin-bottom:1rem;">This is where the first story goes.</p>
      <p class="lead wide" style="margin-inline:auto;">We're collecting them now. If you're reading this and thinking about it &mdash; you'd be the first, and that matters more than being the tenth.</p>
      <div class="btn-row" style="justify-content:center;"><a class="btn btn-primary" href="#share">Be the first</a></div>
    </div>
  </div>
</section>

<section class="band bg-white" id="share">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="kicker">Share your story</span>
        <h2>Here's exactly how it works</h2>
        <div class="step">
          <span class="dot">1</span>
          <div><h3>You write it, your way</h3><p>Any length. A paragraph is fine. There's no template and no required arc &mdash; it does not need to end well to be worth telling.</p></div>
        </div>
        <div class="step">
          <span class="dot">2</span>
          <div><h3>You choose the name on it</h3><p>Full name, first name, initials, or fully anonymous. We use exactly what you pick and nothing else.</p></div>
        </div>
        <div class="step">
          <span class="dot">3</span>
          <div><h3>You approve before anything goes up</h3><p>We send you the final version first. If we suggest a light edit for clarity, you see it. Change your mind at any point &mdash; before or after publishing &mdash; and we take it down, no questions.</p></div>
        </div>
        <p class="note" style="margin-top:1.8rem;"><strong>One thing we'll be careful about.</strong> To keep this page safe for everyone reading it, we follow standard safe-messaging guidance and don't publish detailed descriptions of methods of self-harm or suicide. We'll work with you on wording if that comes up. If you're in crisis right now, please reach out to <a href="tel:988">988</a> before writing anything &mdash; this page can wait.</p>
      </div>

      <div>
        <div class="form-card">
          <div class="illus-icon">{IC_SHARE}</div>
          <h3>Send it to us</h3>
          <p>The contact form is the fastest route &mdash; pick &ldquo;Sharing my story&rdquo; from the dropdown. If you'd rather just email or DM, that works too.</p>
          <div class="btn-row"><a class="btn btn-primary" href="contact.html">Use the contact form</a></div>
          <ul class="contact-list" style="margin-top:1.4rem;">
            <li><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><strong>Instagram DM</strong><a href="{IG}" target="_blank" rel="noopener">@peerbridgenova</a></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>
''')


# =========================================================== GET INVOLVED
page("get-involved.html", "Get Involved | PeerBridge",
 "Join the PeerBridge team, start a chapter, or partner with us. Upcoming student roles in Northern Virginia.",
f'''
<section class="page-head">
  {BLOBS}
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a><span>/</span>Get Involved<span>/</span>Join the Team</p>
    <div class="split wide-left">
      <div>
        <span class="kicker">Get involved</span>
        <h1>Build this with us.</h1>
        <p class="lead wide">PeerBridge is early enough that the people joining now get to shape what it becomes, not just carry out someone else's plan.</p>
      </div>
      <div class="illus illus-plain">{ILL_GROW}</div>
    </div>
  </div>
  {curve("bottom", WHITE)}
</section>

<section class="band bg-white">
  <div class="wrap center">
    <span class="kicker">Where we are</span>
    <h2 class="narrow center">We're not hiring yet &mdash; and we're saying so</h2>
    <p class="lead wide">Plenty of new organizations post open roles they aren't ready to fill. We'd rather be straight with you: our founding team is still building the foundation, and bringing people on before there's real work for them wastes their time.</p>
    <p class="lead wide">Here's what we expect to open, and roughly when. If one of these is you, <a class="arrow" href="contact.html">get in touch now</a> &mdash; early interest genuinely moves these timelines up.</p>
  </div>
</section>

<section class="band bg-sky">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.4rem;">
      <span class="kicker">Upcoming roles</span>
      <h2 class="narrow center">What we'll be looking for</h2>
    </div>
    <div class="grid g2">
      <div class="role">
        <span class="status">Opening first</span>
        <h3>Student Writer</h3>
        <p>Research and write one plain-language article per month for our Resources section &mdash; explainers through to first-person perspective pieces.</p>
        <p><strong>Good fit if:</strong> you write clearly, check your sources, and can explain something complicated without dumbing it down.</p>
        <p><strong>You get:</strong> a published byline, editorial feedback, and volunteer service hours.</p>
      </div>
      <div class="role">
        <span class="status">Opening first</span>
        <h3>Social Media &amp; Design</h3>
        <p>Build and run our Instagram presence &mdash; graphics, campaign planning, and post copy that doesn't sound like a pamphlet.</p>
        <p><strong>Good fit if:</strong> you have a design eye, know Canva or Figma, and understand what people actually stop scrolling for.</p>
        <p><strong>You get:</strong> a real portfolio piece and full creative input.</p>
      </div>
      <div class="role">
        <span class="status soon">Later this year</span>
        <h3>Outreach Lead</h3>
        <p>Connect PeerBridge with schools, counselors, and local organizations. Coordinate events and represent us in rooms we're not in yet.</p>
        <p><strong>Good fit if:</strong> you're comfortable emailing adults you've never met, and following up when they don't reply.</p>
      </div>
      <div class="role">
        <span class="status soon">Later this year</span>
        <h3>School Chapter Organizer</h3>
        <p>Start and run a PeerBridge presence at your own school &mdash; meetings, events, and a point of contact for students there.</p>
        <p><strong>Good fit if:</strong> you're already the person your friends come to, and you want structure and backing behind that.</p>
      </div>
    </div>
    <p class="note" style="margin-top:2.2rem;"><strong>Eligibility.</strong> Roles are open to students, generally ages 14&ndash;18. No prior experience needed for writer or design roles &mdash; we care more about care and reliability than a resume.</p>
  </div>
</section>

<section class="band bg-white">
  <div class="wrap">
    <div class="center" style="margin-bottom:2.4rem;">
      <span class="kicker">Other ways in</span>
      <h2 class="narrow center">You don't need a title to help</h2>
    </div>
    <div class="grid g3">
      <article class="card card-cream">
        <div class="illus-icon">{IC_SHARE}</div>
        <h3>Share your story</h3>
        <p>The single most useful thing most people can give us. Anonymous is completely fine.</p>
        <p style="margin-top:1rem;"><a class="arrow" href="stories.html">Tell your story</a></p>
      </article>
      <article class="card card-cream">
        <div class="illus-icon">{IC_LINK}</div>
        <h3>Bring us to your school</h3>
        <p>Introduce us to a counselor, club sponsor, or student government. One warm intro beats fifty cold emails.</p>
        <p style="margin-top:1rem;"><a class="arrow" href="contact.html">Make an intro</a></p>
      </article>
      <article class="card card-cream">
        <div class="illus-icon">{IC_HAND}</div>
        <h3>Support the work</h3>
        <p>Skills, supplies, venue space, or funding once we're properly set up to accept it.</p>
        <p style="margin-top:1rem;"><a class="arrow" href="donate.html">Ways to support</a></p>
      </article>
    </div>
  </div>
</section>

<section class="band bg-deep on-deep">
  {BLOBS}
  <div class="wrap center">
    <h2 class="narrow center">Interested in a role that isn't open yet?</h2>
    <p class="lead wide">Tell us which one and what you'd do with it. We keep a list, and we go to it first.</p>
    <div class="btn-row"><a class="btn btn-on-deep" href="contact.html">Register your interest</a></div>
  </div>
</section>
''')


# =========================================================== DONATE
page("donate.html", "Support Us | PeerBridge",
 "Ways to support PeerBridge, a student-led mental health initiative in Northern Virginia.",
f'''
<section class="page-head">
  {BLOBS}
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a><span>/</span>Support Us</p>
    <div class="split wide-left">
      <div>
        <span class="kicker">Support us</span>
        <h1>Help us build this properly.</h1>
        <p class="lead wide">PeerBridge runs on student time and almost no money. Here's what we need &mdash; and an honest note about where donations stand.</p>
      </div>
      <div class="illus illus-plain">{ILL_SUPPORT}</div>
    </div>
  </div>
  {curve("bottom", WHITE)}
</section>

<section class="band bg-white">
  <div class="wrap">
    <div class="narrow center" style="margin-inline:auto;">
      <p class="note"><strong>We are not currently accepting financial donations.</strong> PeerBridge is a student organization that hasn't yet completed nonprofit registration. Until we have that status &mdash; or a fiscal sponsor &mdash; we won't ask anyone for money, because contributions wouldn't be tax-deductible and we won't route them through a personal account. When that changes, a verified donation option will appear right here, and we'll say exactly what it funds.</p>
      <p class="lead wide" style="margin-top:1.8rem;">In the meantime, the things below are worth more to us than a small cash donation would be anyway.</p>
    </div>
  </div>
</section>

<section class="band bg-sky">
  <div class="wrap">
    <div class="split">
      <div>
        <span class="kicker">What actually helps right now</span>
        <h2>Five things, in order of usefulness</h2>
        <div class="step"><span class="dot">1</span><div><h3>An introduction</h3><p>Connect us with a school counselor, club sponsor, teacher, or local youth organization. Access is our biggest bottleneck, and one email from you solves it faster than anything else here.</p></div></div>
        <div class="step"><span class="dot">2</span><div><h3>Your skills</h3><p>Writing, design, photography, video, web work, or event help. A few hours of real skill beats a small check.</p></div></div>
        <div class="step"><span class="dot">3</span><div><h3>In-kind goods</h3><p>Printing, snacks and supplies for events, or meeting space. Concrete, immediately usable, no legal complications.</p></div></div>
        <div class="step"><span class="dot">4</span><div><h3>Reach</h3><p>Follow and share <a class="arrow" href="{IG}" target="_blank" rel="noopener">@peerbridgenova</a>. Send this site to one student who needs the glossary. That's a real contribution.</p></div></div>
        <div class="step"><span class="dot">5</span><div><h3>A pledge for later</h3><p>If you want to give financially once we're set up, tell us now. Knowing what we can count on determines whether we register independently or find a fiscal sponsor &mdash; and how fast.</p></div></div>
        <div class="btn-row">
          <a class="btn btn-primary" href="contact.html">Offer support</a>
          <a class="btn btn-soft" href="get-involved.html">Join the team instead</a>
        </div>
      </div>

      <div class="form-card">
        <span class="kicker">Roadmap</span>
        <h3 style="font-size:1.35rem;">Getting donation-ready</h3>
        <p style="font-size:.96rem;margin-bottom:1.6rem;">The steps between here and a working donate button, so you can see exactly where we are:</p>
        <div class="step"><span class="dot done">&#10003;</span><div><h3>Founding team and mission</h3><p>Done.</p></div></div>
        <div class="step"><span class="dot">2</span><div><h3>Choose a structure</h3><p>Independent 501(c)(3) registration, or fiscal sponsorship under an existing nonprofit. Sponsorship is faster; registration gives us more control.</p></div></div>
        <div class="step"><span class="dot">3</span><div><h3>EIN and an organizational bank account</h3><p>No PeerBridge money touches a personal account. Ever.</p></div></div>
        <div class="step"><span class="dot">4</span><div><h3>Register to solicit in Virginia</h3><p>Required before publicly asking for charitable donations in the Commonwealth.</p></div></div>
        <div class="step"><span class="dot">5</span><div><h3>Publish a budget, then open donations</h3><p>You'll be able to see what your money pays for before you give it.</p></div></div>
      </div>
    </div>
  </div>
</section>

<section class="band bg-deep on-deep">
  {BLOBS}
  <div class="wrap center">
    <h2 class="narrow center">Know how to do this?</h2>
    <p class="lead wide">If you've set up a nonprofit or run a fiscal sponsorship before, twenty minutes of your advice would save us months.</p>
    <div class="btn-row"><a class="btn btn-on-deep" href="contact.html">Get in touch</a></div>
  </div>
</section>
''')


# =========================================================== CONTACT
page("contact.html", "Contact | PeerBridge",
 "Get in touch with PeerBridge about joining the team, partnering, sharing a story, or suggesting a resource.",
f'''
<section class="page-head">
  {BLOBS}
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Home</a><span>/</span>Get Involved<span>/</span>Contact</p>
    <div class="split wide-left">
      <div>
        <span class="kicker">Contact</span>
        <h1>Say something.</h1>
        <p class="lead wide">Joining the team, partnering, sharing a story, correcting something we got wrong &mdash; it all goes to the same place, and a person reads it.</p>
      </div>
      <div class="illus illus-plain">{ILL_REACH}</div>
    </div>
  </div>
  {curve("bottom", WHITE)}
</section>

<section class="band bg-white">
  <div class="wrap">
    <div class="split" style="align-items:start;">
      <div class="form-card">
        <h2 style="font-size:clamp(1.4rem,2.4vw,1.9rem);">Send a message</h2>
        <form class="form" data-human-check action="https://formsubmit.co/anwarkiyar8@gmail.com" method="POST">
          <input type="hidden" name="_subject" value="New PeerBridge contact form submission">
          <input type="hidden" name="_template" value="table">
          <input type="hidden" name="_captcha" value="false">
          <input type="hidden" name="_next" value="https://peerbridgenova.vercel.app/thanks.html">

          <!-- Honeypot: invisible to people, irresistible to bots.
               FormSubmit also silently drops any submission where _honey is filled. -->
          <div class="hp" aria-hidden="true">
            <label>Leave this field empty
              <input type="text" name="_honey" tabindex="-1" autocomplete="off">
            </label>
          </div>

          <label>Name
            <input type="text" name="name" placeholder="Your name" required autocomplete="name">
          </label>
          <label>Email
            <input type="email" name="email" placeholder="you@example.com" required autocomplete="email">
          </label>
          <label>What's this about?
            <select name="topic" required>
              <option value="">Choose one&hellip;</option>
              <option>Joining the team</option>
              <option>Sharing my story</option>
              <option>Partnership or collaboration</option>
              <option>Suggesting a glossary term or resource</option>
              <option>Supporting PeerBridge</option>
              <option>Something else</option>
            </select>
          </label>
          <label>Message
            <textarea name="message" rows="6" placeholder="Tell us what's on your mind." required></textarea>
            <span class="hint">Please don't include anything you'd consider medical information &mdash; this form is email, not a secure channel.</span>
          </label>

          <div class="human">
            <span class="hc-label">Quick check &mdash; are you human?</span>
            <div class="hc-row">
              <span class="hc-q">&hellip;</span>
              <label class="hp" for="hc-answer">Your answer</label>
              <input id="hc-answer" class="hc-answer" type="text" inputmode="numeric" autocomplete="off" aria-label="Answer to the maths question" required>
              <button type="button" class="hc-new">New question</button>
            </div>
            <p class="hc-msg" role="status" aria-live="polite"></p>
          </div>

          <button class="btn btn-primary" type="submit">Send message</button>
        </form>
      </div>

      <div>
        <div class="card card-sky card-flat">
          <span class="kicker">Direct</span>
          <h3>Other ways to reach us</h3>
          <ul class="contact-list">
            <li><strong>Instagram &mdash; fastest</strong><a href="{IG}" target="_blank" rel="noopener">@peerbridgenova</a></li>
            <li><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><strong>Based in</strong>Northern Virginia</li>
            <li><strong>Typical reply time</strong>Within a few days &mdash; we're students, so allow for exam weeks</li>
          </ul>
        </div>

        <p class="note" style="margin-top:1.4rem;"><strong>This form is not monitored for emergencies.</strong> If you or someone you know is in immediate danger, call <a href="tel:911">911</a>. For urgent mental health support, call or text <a href="tel:988">988</a>, or text HOME to <a href="sms:741741">741741</a>. Those lines are staffed around the clock; we are not.</p>

        <div class="card card-flat" style="margin-top:1.4rem;">
          <h3 style="font-size:1.1rem;">Privacy</h3>
          <p>Messages go to a team inbox and are read only by PeerBridge officers. We don't sell, share, or publish anything you send &mdash; and we'd never publish a story without your explicit approval first.</p>
        </div>
      </div>
    </div>
  </div>
</section>
''')


# =========================================================== THANKS
page("thanks.html", "Message sent | PeerBridge", "Thanks for reaching out to PeerBridge.",
f'''
<section class="page-head">
  {BLOBS}
  <div class="wrap center">
    <div class="illus illus-plain" style="max-width:340px;margin:0 auto 2rem;">{ILL_DONE}</div>
    <span class="kicker">Message sent</span>
    <h1 class="narrow center">Thanks &mdash; we've got it.</h1>
    <p class="lead wide">A real person reads every message. We'll usually reply within a few days; if it's urgent, DM us on Instagram, which we check far more often.</p>
    <div class="btn-row">
      <a class="btn btn-primary" href="index.html">Back to home</a>
      <a class="btn btn-soft" href="glossary.html">Browse the glossary</a>
    </div>
  </div>
  {curve("bottom", WHITE)}
</section>

<section class="band bg-white">
  <div class="wrap">
    <div class="grid g3">
      <article class="card card-sky"><div class="illus-icon">{IC_BOOK}</div><h3>Read the glossary</h3><p>Plain-English definitions of the terms that come up most.</p><p style="margin-top:1rem;"><a class="arrow" href="glossary.html">Open glossary</a></p></article>
      <article class="card card-sky"><div class="illus-icon">{IC_SHARE}</div><h3>Share your story</h3><p>Anonymous is fine. Yours might be the one someone needed to read.</p><p style="margin-top:1rem;"><a class="arrow" href="stories.html">Tell your story</a></p></article>
      <article class="card card-sky"><div class="illus-icon">{IC_LINK}</div><h3>Follow along</h3><p>Instagram is where the day-to-day happens.</p><p style="margin-top:1rem;"><a class="arrow" href="{IG}" target="_blank" rel="noopener">@peerbridgenova</a></p></article>
    </div>
  </div>
</section>
''')

print("done")
