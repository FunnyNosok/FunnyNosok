"""Generates all SVG assets for the FunnyNosok GitHub profile README.

Usage: python scripts/gen.py
Site cards need 1440x900 PNG screenshots named <site>.png in $SHOTS_DIR
(default: scripts/shots), e.g. made with headless Chrome:
  chrome --headless=new --window-size=1440,900 --screenshot=shots/mariya.png <url>
Requires Pillow.
"""
import base64, io, os, random
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = str(ROOT / "assets")
SHOTS = os.environ.get("SHOTS_DIR", str(ROOT / "scripts" / "shots"))
os.makedirs(OUT, exist_ok=True)

BG, PANEL, BORDER = "#0b0b0c", "#111112", "#26262a"
VIOLET, PURPLE, CYAN, PINK = "#e4e4e7", "#3f3f46", "#a1a1aa", "#71717a"
TEXT, MUTED, DIM = "#f4f4f5", "#8b8b92", "#4b4b52"
MONO = "'JetBrains Mono','Fira Code','Cascadia Code',Consolas,'Courier New',monospace"
SANS = "'Segoe UI','Inter',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def save(name, svg):
    with open(f"{OUT}/{name}", "w", encoding="utf-8") as f:
        f.write(svg)
    print(name, len(svg) // 1024, "KB")


def shot_b64(name, w=1136, h=710):
    im = Image.open(f"{SHOTS}/{name}.png").convert("RGB").crop((0, 0, 1440, 900)).resize((w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=74, optimize=True, progressive=True)
    return base64.b64encode(buf.getvalue()).decode()


def defs_common():
    return f"""
  <linearGradient id="brand" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VIOLET}"/><stop offset=".55" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}"/>
  </linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity=".55"/><stop offset=".5" stop-color="{BORDER}"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".45"/>
  </linearGradient>"""


# ───────────────────────────── HEADER ─────────────────────────────
def header():
    W, H = 1200, 420
    rnd = random.Random(7)
    stars = "".join(
        f'<circle cx="{rnd.randint(10, W-10)}" cy="{rnd.randint(10, 250)}" r="{rnd.choice([0.8, 1, 1.2, 1.6])}" fill="#fff" '
        f'style="animation:tw {rnd.uniform(2.5, 6):.1f}s ease-in-out {rnd.uniform(-6, 0):.1f}s infinite"/>'
        for _ in range(70))
    hz = 292  # horizon
    vlines = "".join(
        f'<line x1="{600 + (i * 38)}" y1="{hz}" x2="{600 + i * 260}" y2="{H}" />' for i in range(-9, 10))
    hlines = "".join(
        f'<line x1="0" y1="{hz}" x2="{W}" y2="{hz}" style="animation:floor 3.2s cubic-bezier(.55,0,1,.45) {-i * 0.4:.1f}s infinite"/>'
        for i in range(8))
    hexes = ["CA FE BA BE", "00 00 00 41", "AES-256-GCM", "0x7F 45 4C 46", "invokevirtual", "ldc #42", "SEALED", "jvm::decrypt()"]
    floating = "".join(
        f'<text x="{x}" y="{y}" style="animation:drift {rnd.uniform(7, 12):.1f}s ease-in-out {rnd.uniform(-8, 0):.1f}s infinite">{t}</text>'
        for t, (x, y) in zip(hexes, [(70, 110), (1010, 92), (1000, 200), (120, 232), (1040, 262), (60, 170), (1040, 128), (210, 80)]))
    title = "FUNNYNOSOK"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>{defs_common()}
  <clipPath id="c"><rect width="{W}" height="{H}" rx="22"/></clipPath>
  <radialGradient id="g1" cx=".25" cy=".25" r=".5"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".55"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>
  <radialGradient id="g2" cx=".8" cy=".75" r=".45"><stop offset="0" stop-color="{CYAN}" stop-opacity=".28"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <radialGradient id="sun" cx=".5" cy="1" r=".6"><stop offset="0" stop-color="{PINK}" stop-opacity=".35"/><stop offset=".5" stop-color="{VIOLET}" stop-opacity=".12"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
  <linearGradient id="title" x1="0" y1="0" x2="{W}" y2="0" gradientUnits="userSpaceOnUse" spreadMethod="reflect">
    <stop offset="0" stop-color="#ffffff"/><stop offset=".3" stop-color="{VIOLET}"/><stop offset=".6" stop-color="{CYAN}"/><stop offset="1" stop-color="#ffffff"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="0 0;{W} 0" dur="7s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".35" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff"/></linearGradient>
  <mask id="floorMask"><rect y="{hz}" width="{W}" height="{H - hz}" fill="url(#fade)"/></mask>
  <filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<style>
  @keyframes tw {{ 0%,100% {{ opacity:.12 }} 50% {{ opacity:.9 }} }}
  @keyframes floor {{ 0% {{ transform:translateY(0); opacity:0 }} 15% {{ opacity:.9 }} 100% {{ transform:translateY({H - hz}px); opacity:1 }} }}
  @keyframes pulse {{ 0%,100% {{ opacity:.75 }} 50% {{ opacity:1 }} }}
  @keyframes drift {{ 0%,100% {{ transform:translateY(0); opacity:.18 }} 50% {{ transform:translateY(-10px); opacity:.42 }} }}
  @keyframes gl1 {{ 0%,90%,100% {{ transform:translate(0,0); opacity:0 }} 91% {{ transform:translate(-7px,2px); opacity:.85 }} 93% {{ transform:translate(6px,-3px); opacity:.85 }} 95% {{ transform:translate(-2px,1px); opacity:.6 }} 96% {{ opacity:0 }} }}
  @keyframes type {{ from {{ transform:translateX(0) }} to {{ transform:translateX(760px) }} }}
  @keyframes blink {{ 50% {{ opacity:0 }} }}
  @keyframes dot {{ 0%,100% {{ opacity:1 }} 50% {{ opacity:.3 }} }}
  .fl text {{ font:500 13px {MONO}; fill:{VIOLET} }}
  .grid line {{ stroke:{VIOLET}; stroke-opacity:.35; stroke-width:1 }}
</style>
<g clip-path="url(#c)">
  <rect width="{W}" height="{H}" fill="{BG}"/>
  <rect width="{W}" height="{H}" fill="url(#g1)" style="animation:pulse 6s ease-in-out infinite"/>
  <rect width="{W}" height="{H}" fill="url(#g2)" style="animation:pulse 7s ease-in-out -3s infinite"/>
  <g>{stars}</g>
  <ellipse cx="600" cy="{hz}" rx="520" ry="150" fill="url(#sun)"/>
  <g class="grid" mask="url(#floorMask)">{vlines}{hlines}<line x1="0" y1="{hz}" x2="{W}" y2="{hz}" style="stroke:{PINK};stroke-opacity:.7"/></g>
  <g class="fl">{floating}</g>

  <g font-family="{MONO}" font-size="13" font-weight="600" letter-spacing="1.5">
    <circle cx="44" cy="40" r="5" fill="#d4d4d8" style="animation:dot 1.6s ease-in-out infinite"/>
    <text x="58" y="45" fill="{MUTED}">ONLINE · BUILDING STUFF</text>
    <text x="{W - 40}" y="45" fill="{MUTED}" text-anchor="end">0xCAFEBABE</text>
  </g>

  <g font-family="{SANS}" font-weight="900" font-size="104" letter-spacing="6" text-anchor="middle">
    <text x="600" y="192" fill="{VIOLET}" opacity=".5" filter="url(#glow)">{title}</text>
    <text x="600" y="192" fill="{CYAN}" style="animation:gl1 5s steps(1) infinite">{title}</text>
    <text x="600" y="192" fill="{PINK}" style="animation:gl1 5s steps(1) -2.4s infinite">{title}</text>
    <text x="600" y="192" fill="url(#title)">{title}</text>
  </g>

  <clipPath id="tc"><rect x="220" y="218" width="760" height="40"/></clipPath>
  <g font-family="{MONO}" font-size="19" font-weight="500" clip-path="url(#tc)">
    <text x="600" y="246" text-anchor="middle" fill="{TEXT}" letter-spacing="1"><tspan fill="{PINK}">&gt;</tspan> jvm security <tspan fill="{DIM}">·</tspan> web <tspan fill="{DIM}">·</tspan> telegram bots <tspan fill="{DIM}">·</tspan> ai</text>
    <rect x="220" y="222" width="760" height="34" fill="{BG}" style="animation:type 2.4s steps(38) .4s forwards"/>
  </g>

  <g font-family="{MONO}" font-size="15" fill="{MUTED}">
    <text x="40" y="{H - 30}"><tspan fill="{CYAN}">~/funnynosok</tspan> <tspan fill="{VIOLET}">$</tspan> ./run --mode=ship-it<tspan fill="{TEXT}" style="animation:blink 1s steps(1) infinite"> █</tspan></text>
    <text x="{W - 40}" y="{H - 30}" text-anchor="end">java · kotlin · c++ · rust · ts · python</text>
  </g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="22" fill="none" stroke="url(#edge)"/>
</svg>"""
    save("header.svg", svg)


# ───────────────────────────── SECTION TITLES ─────────────────────────────
def section(num, label, hint):
    W, H = 1200, 76
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>{defs_common()}
  <linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".9"/><stop offset=".6" stop-color="{CYAN}" stop-opacity=".35"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
</defs>
<style>@keyframes run {{ from {{ transform:translateX(-120px) }} to {{ transform:translateX({W}px) }} }}</style>
<text x="4" y="48" font-family="{MONO}" font-size="30" font-weight="700" fill="url(#brand)">{num}</text>
<text x="62" y="48" font-family="{SANS}" font-size="30" font-weight="800" fill="{TEXT}" letter-spacing="1">{esc(label)}</text>
<text x="{W - 4}" y="46" font-family="{MONO}" font-size="14" fill="{MUTED}" text-anchor="end">// {esc(hint)}</text>
<rect x="4" y="64" width="{W - 8}" height="2" fill="url(#ln)"/>
<rect x="0" y="63" width="120" height="4" rx="2" fill="{CYAN}" opacity=".9" style="animation:run 4.5s cubic-bezier(.6,0,.4,1) infinite"/>
</svg>"""
    save(f"sec-{num}.svg", svg)


# ───────────────────────────── ABOUT (terminal) ─────────────────────────────
def about():
    W = 1200
    lines = [
        ("cmd", "whoami"),
        ("out", [(TEXT, "Funny"), (MUTED, " — fullstack & low-level разработчик")]),
        ("gap", None),
        ("cmd", "cat ~/focus.txt"),
        ("out", [(VIOLET, "▸ "), (TEXT, "Защита JVM"), (MUTED, " — патчу OpenJDK, шифрую классы и строки внутри VM")]),
        ("out", [(CYAN, "▸ "), (TEXT, "Сайты под ключ"), (MUTED, " — дизайн → вёрстка → деплой на Vercel")]),
        ("out", [(PINK, "▸ "), (TEXT, "Боты и AI"), (MUTED, " — Telegram-боты, AI-агенты, интеграции с LLM")]),
        ("out", [("#d4d4d8", "▸ "), (TEXT, "Эксперименты"), (MUTED, " — Android на Kotlin, Rust, C")]),
        ("gap", None),
        ("cmd", "echo $STATUS"),
        ("out", [("#d4d4d8", "● "), (TEXT, "открыт к заказам"), (MUTED, " — пиши в Telegram")]),
    ]
    y, rows, t = 104, [], 0.3
    for kind, content in lines:
        if kind == "gap":
            y += 14
            continue
        if kind == "cmd":
            spans = f'<tspan fill="{CYAN}">funny@dev</tspan><tspan fill="{MUTED}">:</tspan><tspan fill="{VIOLET}">~</tspan><tspan fill="{MUTED}">$ </tspan><tspan fill="{TEXT}">{esc(content)}</tspan>'
        else:
            spans = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for c, s in content)
        rows.append(f'<text x="44" y="{y}" style="animation:in .35s ease-out {t:.2f}s both">{spans}</text>')
        t += 0.45 if kind == "cmd" else 0.22
        y += 34
    H = y + 22
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>{defs_common()}
  <radialGradient id="gl" cx="1" cy="0" r=".9"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".22"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" opacity=".025"/></pattern>
</defs>
<style>
  @keyframes in {{ from {{ opacity:0; transform:translateX(-8px) }} to {{ opacity:1; transform:none }} }}
  @keyframes blink {{ 50% {{ opacity:0 }} }}
  text {{ font:500 19px {MONO} }}
</style>
<rect width="{W}" height="{H}" rx="18" fill="{PANEL}"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#gl)"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#scan)"/>
<path d="M0 18a18 18 0 0 1 18-18h{W - 36}a18 18 0 0 1 18 18v32H0z" fill="#151517"/>
<line x1="0" y1="50" x2="{W}" y2="50" stroke="{BORDER}"/>
<circle cx="30" cy="25" r="7" fill="#3f3f46"/><circle cx="54" cy="25" r="7" fill="#3f3f46"/><circle cx="78" cy="25" r="7" fill="#3f3f46"/>
<text x="600" y="31" text-anchor="middle" style="font-size:14px;fill:{MUTED}">funny@dev — zsh — 120×32</text>
{''.join(rows)}
<rect x="44" y="{y - 22}" width="11" height="22" fill="{VIOLET}" style="animation:blink 1s steps(1) infinite"/>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="url(#edge)"/>
</svg>"""
    save("about.svg", svg)


# ───────────────────────────── FUNNYGUARD CARD ─────────────────────────────
def funnyguard():
    W, H = 1200, 480
    rnd = random.Random(42)
    plain = [
        "CA FE BA BE 00 00 00 41 00 2F 0A 00",
        "07 00 18 09 00 19 00 1A 08 00 1B 0A",
        "00 1C 00 1D 07 00 1E 01 00 06 3C 69",
        "6E 69 74 3E 01 00 03 28 29 56 01 00",
        "04 43 6F 64 65 01 00 0F 4C 69 6E 65",
        "4E 75 6D 62 65 72 54 61 62 6C 65 01",
        "00 04 6D 61 69 6E 01 00 16 28 5B 4C",
        "6A 61 76 61 2F 6C 61 6E 67 2F 53 74",
    ]
    cipher = [" ".join(f"{rnd.randint(0, 255):02X}" for _ in range(12)) for _ in plain]
    px, py, rowh = 668, 150, 32
    rows = []
    for i, (p, c) in enumerate(zip(plain, cipher)):
        y = py + i * rowh
        d = f"{i * 0.3:.1f}s"
        rows.append(
            f'<text x="{px + 70}" y="{y}" class="p" style="animation-delay:{d}">{p}</text>'
            f'<text x="{px + 70}" y="{y}" class="c" style="animation-delay:{d}">{c}</text>'
            f'<text x="{px + 22}" y="{y}" class="off">{i * 12:04X}</text>')
    chips = ["Java", "C++", "OpenJDK", "AES-256-GCM", "JNI"]
    cx, chip_svg = 60, []
    for ch in chips:
        w = len(ch) * 10 + 30
        chip_svg.append(f'<rect x="{cx}" y="352" width="{w}" height="32" rx="16" fill="{VIOLET}" fill-opacity=".1" stroke="{VIOLET}" stroke-opacity=".45"/>'
                        f'<text x="{cx + w / 2}" y="373" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{TEXT}">{ch}</text>')
        cx += w + 10
    feats = [("per-class AES-256-GCM", VIOLET), ("native string vault", CYAN), ("sealed server-key mode", PINK), ("runtime hardening", "#d4d4d8")]
    feat_svg = "".join(
        f'<circle cx="{66}" cy="{246 + i * 26}" r="4" fill="{c}"/><text x="82" y="{251 + i * 26}" font-family="{MONO}" font-size="15" fill="{TEXT}">{t}</text>'
        for i, (t, c) in enumerate(feats))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>{defs_common()}
  <radialGradient id="gl" cx="0" cy="0" r=".8"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".35"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>
  <radialGradient id="gl2" cx="1" cy="1" r=".7"><stop offset="0" stop-color="{CYAN}" stop-opacity=".18"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
  <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".5"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
  <clipPath id="panel"><rect x="{px}" y="96" width="480" height="300" rx="14"/></clipPath>
</defs>
<style>
  .p,.c,.off {{ font:500 15px {MONO}; letter-spacing:.5px }}
  .p {{ fill:{VIOLET}; animation:p 6s linear infinite }}
  .c {{ fill:{CYAN}; opacity:0; animation:c 6s linear infinite }}
  .off {{ fill:{DIM} }}
  @keyframes p {{ 0%,9% {{ opacity:1 }} 11%,84% {{ opacity:0 }} 90%,100% {{ opacity:1 }} }}
  @keyframes c {{ 0%,9% {{ opacity:0 }} 11%,84% {{ opacity:1 }} 90%,100% {{ opacity:0 }} }}
  @keyframes scan {{ 0%,8% {{ transform:translateY(-40px); opacity:0 }} 10% {{ opacity:1 }} 47% {{ transform:translateY({7 * rowh + 10}px); opacity:1 }} 52%,100% {{ transform:translateY({7 * rowh + 10}px); opacity:0 }} }}
  @keyframes lock {{ 0%,45% {{ opacity:.35 }} 50%,84% {{ opacity:1 }} 90%,100% {{ opacity:.35 }} }}
  @keyframes shine {{ from {{ transform:translateX(-300px) }} to {{ transform:translateX(900px) }} }}
</style>
<rect width="{W}" height="{H}" rx="22" fill="{PANEL}"/>
<rect width="{W}" height="{H}" rx="22" fill="url(#gl)"/>
<rect width="{W}" height="{H}" rx="22" fill="url(#gl2)"/>

<text x="60" y="84" font-family="{MONO}" font-size="14" font-weight="700" letter-spacing="3" fill="{CYAN}">★ FEATURED PROJECT</text>
<text x="56" y="152" font-family="{SANS}" font-size="64" font-weight="900" fill="url(#brand)">FunnyGuard</text>
<text font-family="{SANS}" font-size="19" fill="{MUTED}">
  <tspan x="60" y="192">Шифрование байткода на уровне JVM.</tspan>
  <tspan x="60" y="218"><tspan fill="{TEXT}">Ни одного читаемого класса на диске.</tspan></tspan>
</text>
{feat_svg}
{''.join(chip_svg)}
<text x="60" y="428" font-family="{MONO}" font-size="15" fill="{VIOLET}">github.com/FunnyNosok/FunnyGuard <tspan fill="{CYAN}">→</tspan></text>

<rect x="{px}" y="56" width="480" height="340" rx="14" fill="#0c0c0e" stroke="{BORDER}"/>
<text x="{px + 22}" y="84" font-family="{MONO}" font-size="14" fill="{MUTED}">Client.class</text>
<g transform="translate({px + 440},68)" style="animation:lock 6s linear infinite">
  <rect x="0" y="8" width="18" height="14" rx="3" fill="{CYAN}"/>
  <path d="M4 8V5a5 5 0 0 1 10 0v3" fill="none" stroke="{CYAN}" stroke-width="2.4"/>
</g>
<text x="{px + 424}" y="84" font-family="{MONO}" font-size="12" fill="{CYAN}" text-anchor="end" style="animation:lock 6s linear infinite">ENCRYPTED</text>
<line x1="{px}" y1="98" x2="{px + 480}" y2="98" stroke="{BORDER}"/>
<g clip-path="url(#panel)">
  {''.join(rows)}
  <rect x="{px}" y="{py - 34}" width="480" height="44" fill="url(#bar)" style="animation:scan 6s linear infinite"/>
</g>
<text x="{px + 22}" y="{H - 60}" font-family="{MONO}" font-size="14" fill="#d4d4d8">✓ readable bytecode on disk: 0 bytes</text>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="22" fill="none" stroke="url(#edge)"/>
<g opacity=".08"><rect x="0" y="0" width="120" height="{H}" fill="#fff" transform="skewX(-20)" style="animation:shine 7s ease-in-out infinite"/></g>
</svg>"""
    save("funnyguard.svg", svg)


# ───────────────────────────── SITE CARDS ─────────────────────────────
def site_card(name, title, tag, domain, accent):
    W, H = 600, 470
    b64 = shot_b64(name)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>{defs_common()}
  <clipPath id="s"><rect x="16" y="52" width="568" height="355" rx="10"/></clipPath>
  <linearGradient id="sh" x1="0" y1="0" x2="0" y2="1"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".45"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{PANEL}"/>
<circle cx="34" cy="28" r="5.5" fill="#3f3f46"/><circle cx="52" cy="28" r="5.5" fill="#3f3f46"/><circle cx="70" cy="28" r="5.5" fill="#3f3f46"/>
<rect x="96" y="15" width="400" height="26" rx="13" fill="#18181b" stroke="{BORDER}"/>
<text x="296" y="33" text-anchor="middle" font-family="{MONO}" font-size="12.5" fill="{MUTED}"><tspan fill="#d4d4d8">🔒</tspan> {domain}</text>
<g clip-path="url(#s)">
  <image x="16" y="52" width="568" height="355" preserveAspectRatio="xMidYMin slice" href="data:image/jpeg;base64,{b64}" xlink:href="data:image/jpeg;base64,{b64}"/>
  <rect x="16" y="52" width="568" height="355" fill="url(#sh)"/>
</g>
<rect x="16" y="52" width="568" height="355" rx="10" fill="none" stroke="#fff" stroke-opacity=".06"/>
<rect x="24" y="428" width="4" height="26" rx="2" fill="{accent}"/>
<text x="40" y="449" font-family="{SANS}" font-size="22" font-weight="800" fill="{TEXT}">{esc(title)}</text>
<text x="{W - 24}" y="447" text-anchor="end" font-family="{MONO}" font-size="13" fill="{MUTED}">{esc(tag)} <tspan fill="{accent}">↗</tspan></text>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="url(#edge)"/>
</svg>"""
    save(f"site-{name}.svg", svg)


def cta_card():
    W, H = 600, 470
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>{defs_common()}
  <radialGradient id="g" cx=".5" cy=".42" r=".6"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".5"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>
  <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.3" fill="{VIOLET}" opacity=".22"/></pattern>
</defs>
<style>
  @keyframes spin {{ to {{ transform:rotate(360deg) }} }}
  @keyframes pulse {{ 0%,100% {{ transform:scale(1); opacity:.9 }} 50% {{ transform:scale(1.06); opacity:1 }} }}
</style>
<rect width="{W}" height="{H}" rx="18" fill="{PANEL}"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#dots)"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#g)"/>
<g transform="translate(300,178)">
  <circle r="74" fill="none" stroke="url(#brand)" stroke-width="2" stroke-dasharray="6 10" style="animation:spin 18s linear infinite"/>
  <g style="animation:pulse 2.4s ease-in-out infinite">
    <circle r="50" fill="{VIOLET}" fill-opacity=".14" stroke="{VIOLET}" stroke-opacity=".6"/>
    <path d="M-16 0h32M0 -16v32" stroke="{TEXT}" stroke-width="5" stroke-linecap="round"/>
  </g>
</g>
<text x="300" y="316" text-anchor="middle" font-family="{SANS}" font-size="30" font-weight="900" fill="{TEXT}">Нужен сайт?</text>
<text x="300" y="350" text-anchor="middle" font-family="{SANS}" font-size="17" fill="{MUTED}">Лендинг, визитка или сайт для бизнеса —</text>
<text x="300" y="374" text-anchor="middle" font-family="{SANS}" font-size="17" fill="{MUTED}">от идеи до запуска.</text>
<rect x="190" y="400" width="220" height="44" rx="22" fill="url(#brand)"/>
<text x="300" y="428" text-anchor="middle" font-family="{MONO}" font-size="15" font-weight="700" fill="{BG}">написать в TG →</text>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="url(#edge)"/>
</svg>"""
    save("site-cta.svg", svg)


# ───────────────────────────── LAB CARDS ─────────────────────────────
def lab_card(key, name, lang, color, desc, icon):
    W, H = 600, 170
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>{defs_common()}
  <radialGradient id="g" cx="1" cy="0" r=".9"><stop offset="0" stop-color="{color}" stop-opacity=".22"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{W}" height="{H}" rx="18" fill="{PANEL}"/>
<rect width="{W}" height="{H}" rx="18" fill="url(#g)"/>
<rect x="28" y="30" width="56" height="56" rx="14" fill="{color}" fill-opacity=".14" stroke="{color}" stroke-opacity=".5"/>
<text x="56" y="64" text-anchor="middle" font-family="{MONO}" font-size="17" font-weight="700" fill="{TEXT}">{icon}</text>
<text x="104" y="56" font-family="{SANS}" font-size="24" font-weight="800" fill="{TEXT}">{esc(name)}</text>
<circle cx="110" cy="76" r="5" fill="{color}"/>
<text x="122" y="81" font-family="{MONO}" font-size="14" fill="{MUTED}">{esc(lang)}</text>
<text x="28" y="128" font-family="{SANS}" font-size="17" fill="{MUTED}">{esc(desc)}</text>
<text x="{W - 28}" y="56" text-anchor="end" font-family="{MONO}" font-size="18" fill="{color}">↗</text>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="url(#edge)"/>
</svg>"""
    save(f"lab-{key}.svg", svg)


# ───────────────────────────── STACK ─────────────────────────────
def stack():
    W = 1200
    groups = [
        ("CORE / LOW-LEVEL", VIOLET, [("Java", "#e4e4e7"), ("Kotlin", "#a1a1aa"), ("C++", "#a1a1aa"), ("C", "#71717a"), ("Rust", "#a1a1aa"), ("OpenJDK", "#a1a1aa")]),
        ("WEB", CYAN, [("TypeScript", "#e4e4e7"), ("JavaScript", "#d4d4d8"), ("HTML/CSS", "#a1a1aa"), ("Node.js", "#71717a"), ("Vercel", "#ffffff")]),
        ("BOTS &amp; AI", PINK, [("Python", "#a1a1aa"), ("Telegram API", "#3f3f46"), ("LLM APIs", "#e4e4e7"), ("Git", "#71717a")]),
    ]
    colw, rows = 376, []
    for gi, (gname, gc, items) in enumerate(groups):
        x0 = 24 + gi * (colw + 12)
        rows.append(f'<rect x="{x0}" y="24" width="{colw}" height="252" rx="14" fill="#0e0e10" stroke="{BORDER}"/>')
        rows.append(f'<text x="{x0 + 22}" y="58" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="2.5" fill="{gc}">{gname}</text>')
        rows.append(f'<rect x="{x0 + 22}" y="70" width="36" height="2" fill="{gc}"/>')
        cx, cy = x0 + 22, 92
        for n, c in items:
            w = len(n) * 10 + 44
            if cx + w > x0 + colw - 16:
                cx, cy = x0 + 22, cy + 48
            rows.append(f'<rect x="{cx}" y="{cy}" width="{w}" height="36" rx="10" fill="#161618" stroke="#2a2a2e"/>'
                        f'<circle cx="{cx + 17}" cy="{cy + 18}" r="5" fill="{c}"/>'
                        f'<text x="{cx + 30}" y="{cy + 23.5}" font-family="{MONO}" font-size="14.5" fill="{TEXT}">{esc(n)}</text>')
            cx += w + 10
    H = 300
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>{defs_common()}</defs>
<rect width="{W}" height="{H}" rx="20" fill="{PANEL}"/>
{''.join(rows)}
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="none" stroke="url(#edge)"/>
</svg>"""
    save("stack.svg", svg)


# ───────────────────────────── BUTTONS ─────────────────────────────
def button(key, label, sub, color, icon_path):
    W, H = 300, 72
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>{defs_common()}
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{color}" stop-opacity=".22"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>
</defs>
<rect width="{W}" height="{H}" rx="16" fill="{PANEL}"/>
<rect width="{W}" height="{H}" rx="16" fill="url(#g)"/>
<rect x="14" y="14" width="44" height="44" rx="12" fill="#1f1f23" stroke="{color}" stroke-opacity=".5"/>
<g transform="translate(24,24)" fill="#fff">{icon_path}</g>
<text x="74" y="33" font-family="{SANS}" font-size="18" font-weight="800" fill="{TEXT}">{label}</text>
<text x="74" y="54" font-family="{MONO}" font-size="12.5" fill="{MUTED}">{esc(sub)}</text>
<text x="{W - 22}" y="42" text-anchor="end" font-family="{MONO}" font-size="18" fill="{color}">→</text>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{color}" stroke-opacity=".45"/>
</svg>"""
    save(f"btn-{key}.svg", svg)


def footer():
    W, H = 1200, 130
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>{defs_common()}
  <linearGradient id="ln" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0"/><stop offset=".5" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
</defs>
<style>@keyframes w {{ 0%,100% {{ opacity:.35 }} 50% {{ opacity:1 }} }}</style>
<rect x="100" y="30" width="1000" height="1.5" fill="url(#ln)" style="animation:w 4s ease-in-out infinite"/>
<text x="600" y="78" text-anchor="middle" font-family="{MONO}" font-size="16" fill="{MUTED}">compiled with <tspan fill="{PINK}">♥</tspan>, coffee &amp; bytecode <tspan fill="{DIM}">·</tspan> <tspan fill="{VIOLET}">FunnyNosok</tspan> <tspan fill="{DIM}">·</tspan> 2026</text>
<text x="600" y="106" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{DIM}">0xCAFEBABE — EOF</text>
</svg>"""
    save("footer.svg", svg)


if __name__ == "__main__":
    header()
    for n, l, h in [("01", "Обо мне", "whoami"), ("02", "Главный проект", "featured"), ("03", "Сайты", "live on vercel"),
                    ("04", "Лаборатория", "bots · ai · experiments"), ("05", "Стек", "tools of the trade"), ("06", "Активность", "commits don't lie")]:
        section(n, l, h)
    about()
    funnyguard()
    site_card("zabeymsy", "Забьёмся", "тату-студия · Воронеж", "zabeymsy-landing.vercel.app", PINK)
    site_card("mariya", "Мария · Nails", "ногтевая студия · Тула", "mariya-nails-nu.vercel.app", "#d4d4d8")
    site_card("onlytatoo", "Only Tattoo", "тату-студия", "onlytatoo.vercel.app", VIOLET)
    site_card("hostel", "Хостелы ЕКБ", "4 адреса · Екатеринбург", "hostel-ekb.vercel.app", "#d4d4d8")
    site_card("hosteldemo", "Hostel Concepts", "4 дизайн-концепта", "hostel-sites-demo.vercel.app", CYAN)
    cta_card()
    lab_card("tgws", "TGWSANDROID", "Kotlin", "#a1a1aa", "Прокси и обход блокировок Telegram на Android", "KT")
    lab_card("gpt", "GptTgBot", "Python", "#a1a1aa", "Telegram-бот с GPT внутри", "PY")
    lab_card("orion", "Orion AI", "AI Agent", PINK, "Автономный AI-агент", "AI")
    lab_card("shooter", "Shooter", "Rust", "#a1a1aa", "Игра-шутер на Rust", "RS")
    stack()
    tg = '<path d="M21.5 3.5 2.7 10.8c-1.3.5-1.3 1.2-.2 1.6l4.8 1.5 1.8 5.6c.2.6.1.9.8.9.5 0 .7-.2 1-.5l2.4-2.3 4.9 3.6c.9.5 1.5.2 1.8-.8l3.2-15.2c.3-1.3-.5-1.9-1.5-1.5zM8.9 13.6l9.6-6.1c.5-.3.9-.1.5.2l-8.1 7.4-.3 3.4z" transform="scale(1)"/>'
    mail = '<path d="M2 5h20v14H2z" fill="none" stroke="#fff" stroke-width="2"/><path d="m2 6 10 7 10-7" fill="none" stroke="#fff" stroke-width="2"/>'
    web = '<circle cx="12" cy="12" r="10" fill="none" stroke="#fff" stroke-width="2"/><path d="M2 12h20M12 2c3 3 3 17 0 20M12 2c-3 3-3 17 0 20" fill="none" stroke="#fff" stroke-width="2"/>'
    button("tg", "Telegram", "@Funnyqe", "#3f3f46", tg)
    button("mail", "Email", "danilimatov4@gmail.com", "#3f3f46", mail)
    button("web", "Сайт-визитка", "funny-iota-seven.vercel.app", VIOLET, web)
    footer()
