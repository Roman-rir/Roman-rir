"""Generate the profile README SVGs in assets/ for dark and light themes.

Colors and type follow the portfolio (roman-rir.github.io/Portfolio).
Run from the repository root: python scripts/build_assets.py
"""

from html import escape
from pathlib import Path
import textwrap

OUT = Path(__file__).resolve().parent.parent / "assets"

THEMES = {
    "dark": {
        "bg": "#11130f", "surface": "#191d17", "raised": "#22281e", "text": "#f1f2e9",
        "muted": "#aab1a1", "line": "#343b2f", "accent": "#d4f77d", "soft": "#26321a",
        "honor": "#dfc48b", "honor_soft": "#2d291e", "mark": ".06",
    },
    "light": {
        "bg": "#f5f4ed", "surface": "#eeeee5", "raised": "#e5e8dc", "text": "#1c2819",
        "muted": "#5b6654", "line": "#d0d6c7", "accent": "#365928", "soft": "#dfe8d1",
        "honor": "#815a19", "honor_soft": "#eee5d1", "mark": ".05",
    },
}

SANS = "'Space Grotesk','Segoe UI',-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif"
MONO = "'IBM Plex Mono',ui-monospace,SFMono-Regular,Consolas,'Liberation Mono',monospace"
BASE_CSS = f".sans{{font-family:{SANS}}}.mono{{font-family:{MONO}}}"
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"

# Each portfolio project card: label, title, description, tags, award flag.
CARDS = [
    ("risc", "01 / SILICON", "RISC-V3 Processor",
     "Pipelined RISC processor in SystemVerilog, taken from RTL through verification, "
     "synthesis, STA, and place-and-route.",
     ["SystemVerilog", "Genus", "Innovus"], False),
    ("vlsi", "02 / VLSI", "Transistor-Level IC Layout",
     "Digital IC layout in Cadence Virtuoso with device placement, power rails, and "
     "signal routing, checked with DRC and LVS.",
     ["Virtuoso", "DRC / LVS", "Transient sim"], False),
    ("bpt", "03 / BIOMEDICAL", "Blood Pressure Trending",
     "Cuffless monitor that shows blood pressure trends, heart rate, SpO2, and "
     "temperature on an integrated display.",
     ["ESP8266", "MAX32664", "PPG"], True),
    ("ptt", "04 / SIGNALS", "Pulse Transit Time",
     "Cuffless blood pressure estimation from ECG and PPG timing, with R-peak and "
     "waveform feature detection.",
     ["MAX86150", "Raspberry Pi", "ECG + PPG"], True),
    ("robot", "05 / EMBEDDED", "Human Follower Trolley",
     "Raspberry Pi trolley that follows a QR marker, stops for obstacles within 20 cm, "
     "and weighs items with a load cell.",
     ["OpenCV", "HX711", "Flask"], False),
    ("music", "06 / AUDIO ML", "Music Context Retrieval",
     "Audio-text retrieval on MusicCaps. Contrastive training raised Recall@10 from "
     "0.83% to 17.77% on held-out pairs.",
     ["PyTorch", "GraphSAGE", "DistilBERT"], False),
]


def svg(width, height, title, body, css=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">'
        f"<title>{escape(title)}</title><style>{BASE_CSS}{css}{REDUCED}</style>{body}</svg>\n"
    )


def banner(c):
    traces = [
        "M560 334H690L720 304V264H760",
        "M1200 108H1172V128H1140",
        "M940 0V30L962 52V60",
        "M1200 262H1140",
        "M610 0V22L640 52H700",
    ]
    base = "".join(f'<path d="{d}" fill="none" stroke="{c["line"]}" stroke-width="2"/>' for d in traces)
    pulses = "".join(
        f'<path class="trace" style="animation-delay:-{i * 1.3:.1f}s" d="{d}"/>' for i, d in enumerate(traces)
    )
    vias = "".join(
        f'<circle cx="{x}" cy="{y}" r="4" fill="{c["bg"]}" stroke="{c["line"]}" stroke-width="2"/>'
        for x, y in [(560, 334), (700, 52), (962, 52)]
    )
    rows = [
        (150, "ROLE", "AI Automation Engineer", "SOFTVENCE AGENCY"),
        (200, "STUDY", "MSc, EEE", "BRAC UNIVERSITY"),
        (250, "FOCUS", "RTL · Embedded · AI", "OPEN TO COLLABORATION"),
    ]
    panel_rows = "".join(
        f'<text class="mono" x="788" y="{y}" font-size="12.5" letter-spacing="1.2" fill="{c["muted"]}">{label}</text>'
        f'<text class="sans" x="868" y="{y}" font-size="19" font-weight="500" fill="{c["text"]}">{escape(value)}</text>'
        f'<text class="mono" x="868" y="{y + 21}" font-size="12.5" letter-spacing="1" fill="{c["muted"]}">{sub}</text>'
        for y, label, value, sub in rows
    )
    stats = "".join(
        f'<text class="mono" x="{x}" y="318" font-size="14" letter-spacing="1.2" fill="{c["muted"]}">'
        f'<tspan font-size="18" font-weight="600" fill="{c["text"]}">{num}</tspan>  {label}</text>'
        for x, num, label in [(60, "06", "PROJECTS"), (220, "06", "PAPERS"), (366, "3×", "DEAN’S LIST")]
    )
    css = (
        f'.trace{{fill:none;stroke:{c["accent"]};stroke-width:2;stroke-linecap:round;'
        "stroke-dasharray:26 420;animation:flow 6.5s linear infinite}"
        "@keyframes flow{from{stroke-dashoffset:446}to{stroke-dashoffset:0}}"
        ".dot{animation:blink 1.6s ease-in-out infinite}@keyframes blink{50%{opacity:.2}}"
    )
    body = (
        '<defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
        f'<path d="M40 0H0V40" fill="none" stroke="{c["line"]}" stroke-width="1"/></pattern>'
        '<linearGradient id="fade" x1="0" x2="1"><stop offset=".25" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity=".55"/></linearGradient>'
        '<mask id="m"><rect width="1200" height="360" fill="url(#fade)"/></mask>'
        '<clipPath id="clip"><rect width="1200" height="360" rx="20"/></clipPath></defs>'
        '<g clip-path="url(#clip)">'
        f'<rect width="1200" height="360" fill="{c["bg"]}"/>'
        '<rect width="1200" height="360" fill="url(#grid)" mask="url(#m)"/>'
        f"{base}{pulses}{vias}</g>"
        f'<rect x=".5" y=".5" width="1199" height="359" rx="20" fill="none" stroke="{c["line"]}"/>'
        '<g>'
        f'<rect x="60" y="68" width="9" height="9" rx="2" fill="{c["accent"]}"/>'
        f'<text class="mono" x="80" y="77" font-size="14" letter-spacing="2.4" fill="{c["accent"]}">'
        "ENGINEERING / RESEARCH / AUTOMATION</text></g>"
        '<g>'
        f'<text class="sans" x="56" y="168" font-size="78" font-weight="600" letter-spacing="-3.5" fill="{c["text"]}">'
        f'Hi, I’m <tspan fill="{c["accent"]}">Roman.</tspan></text></g>'
        '<g>'
        f'<text class="sans" x="60" y="220" font-size="26" font-weight="500" letter-spacing="-.5" fill="{c["text"]}">'
        "Semiconductor &amp; AI Automation Engineer</text>"
        f'<text class="mono" x="60" y="258" font-size="15" fill="{c["muted"]}">'
        "EEE, AIUB  ·  MSc, BRAC University  ·  Dhaka, Bangladesh</text></g>"
        f'<g><path d="M60 286H640" stroke="{c["line"]}"/>{stats}</g>'
        '<g>'
        f'<rect x="760" y="60" width="380" height="240" rx="16" fill="{c["surface"]}" stroke="{c["line"]}"/>'
        f'<text class="mono" x="788" y="96" font-size="12.5" letter-spacing="1.5" fill="{c["muted"]}">CURRENTLY</text>'
        f'<circle class="dot" cx="978" cy="92" r="4" fill="{c["accent"]}"/>'
        f'<text class="mono" x="1112" y="96" text-anchor="end" font-size="12.5" letter-spacing="1" fill="{c["accent"]}">'
        "SYS.STATUS / OK</text>"
        f'<path d="M788 114H1112" stroke="{c["line"]}"/>{panel_rows}</g>'
    )
    return svg(1200, 360, "Hi, I'm Roman. Semiconductor & AI Automation Engineer.", body, css)


def ticker(c):
    items = ["RTL &amp; VLSI Design", "Embedded Systems", "AI Automation",
             "Signal Processing", "Physical Design", "Biomedical Signals"]
    star = f'<tspan fill="{c["accent"]}">  ✦  </tspan>'
    line = star.join(items) + star
    span = 1100
    copies = "".join(
        f'<text class="sans" x="{i * span}" y="39" font-size="18" font-weight="500" '
        f'textLength="{span}" lengthAdjust="spacing" fill="{c["text"]}">{line}</text>'
        for i in range(3)
    )
    css = f".belt{{animation:slide 34s linear infinite}}@keyframes slide{{to{{transform:translateX(-{span}px)}}}}"
    body = (
        '<defs><clipPath id="clip"><rect width="1200" height="64" rx="14"/></clipPath>'
        f'<linearGradient id="l"><stop offset="0" stop-color="{c["surface"]}"/>'
        f'<stop offset="1" stop-color="{c["surface"]}" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="r"><stop offset="0" stop-color="{c["surface"]}" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="{c["surface"]}"/></linearGradient></defs>'
        f'<g clip-path="url(#clip)"><rect width="1200" height="64" fill="{c["surface"]}"/>'
        f'<g class="belt">{copies}</g>'
        '<rect width="90" height="64" fill="url(#l)"/><rect x="1110" width="90" height="64" fill="url(#r)"/></g>'
        f'<rect x=".5" y=".5" width="1199" height="63" rx="14" fill="none" stroke="{c["line"]}"/>'
    )
    return svg(1200, 64, "RTL and VLSI Design, Embedded Systems, AI Automation, Signal Processing, "
               "Physical Design, Biomedical Signals", body, css)


def card(c, label, title, desc, tags, award):
    lines = textwrap.wrap(desc, 50)[:3]
    desc_svg = "".join(
        f'<text class="sans" x="26" y="{116 + i * 21}" font-size="14" fill="{c["muted"]}">{escape(t)}</text>'
        for i, t in enumerate(lines)
    )
    x, pills = 26, ""
    for tag in tags:
        w = round(len(tag) * 6.6 + 24)
        pills += (
            f'<rect x="{x}" y="178" width="{w}" height="26" rx="13" fill="{c["raised"]}" stroke="{c["line"]}"/>'
            f'<text class="mono" x="{x + w / 2}" y="195" text-anchor="middle" font-size="11" fill="{c["text"]}">'
            f"{escape(tag)}</text>"
        )
        x += w + 8
    chip = (
        f'<rect x="216" y="22" width="132" height="24" rx="12" fill="{c["honor_soft"]}"/>'
        f'<text class="mono" x="282" y="38" text-anchor="middle" font-size="10" letter-spacing=".8" '
        f'fill="{c["honor"]}">★ BEST CAPSTONE</text>'
        if award else ""
    )
    number = label.split(" ")[0]
    body = (
        f'<rect x=".5" y=".5" width="419" height="229" rx="16" fill="{c["surface"]}" stroke="{c["line"]}"/>'
        f'<text class="sans" x="402" y="220" text-anchor="end" font-size="84" font-weight="700" '
        f'letter-spacing="-4" fill="{c["accent"]}" opacity="{c["mark"]}">{number}</text>'
        f'<text class="mono" x="26" y="39" font-size="11.5" letter-spacing="1.6" fill="{c["accent"]}">'
        f"{escape(label)}</text>{chip}"
        f'<circle cx="380" cy="34" r="15" fill="none" stroke="{c["line"]}"/>'
        f'<path d="M375 39L385 29M378 29H385V36" fill="none" stroke="{c["text"]}" stroke-width="1.6" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<text class="sans" x="26" y="84" font-size="23" font-weight="600" letter-spacing="-.6" '
        f'fill="{c["text"]}">{escape(title)}</text>{desc_svg}{pills}'
    )
    return svg(420, 230, f"{title}: {desc}", body)


def main():
    OUT.mkdir(exist_ok=True)
    for name, c in THEMES.items():
        (OUT / f"banner-{name}.svg").write_text(banner(c), encoding="utf-8")
        (OUT / f"ticker-{name}.svg").write_text(ticker(c), encoding="utf-8")
        for key, label, title, desc, tags, award in CARDS:
            (OUT / f"card-{key}-{name}.svg").write_text(card(c, label, title, desc, tags, award), encoding="utf-8")
    print(f"Wrote {len(list(OUT.glob('*.svg')))} SVG files to {OUT}")


if __name__ == "__main__":
    main()
