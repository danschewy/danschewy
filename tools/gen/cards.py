import os, sys
from lib import *

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ANIM = """
.ch{transform-box:fill-box;transform-origin:50% 100%;animation:bob 2.8s ease-in-out infinite}
.d1{animation-delay:-.4s}.d2{animation-delay:-1.3s}.d3{animation-delay:-2.1s}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
.led{animation:led 1.6s steps(2) infinite}.l2{animation-delay:-.5s}.l3{animation-delay:-1.1s}
@keyframes led{50%{opacity:.25}}
@media (prefers-reduced-motion:reduce){.ch,.led{animation:none}}
"""

SMALL = [
    dict(id="nowmal", name="Nowmal", meta="Gmail agent · 2026", color="research",
         tagline="An intelligence layer for Gmail",
         detail="Finds requests, deadlines and promises in your mail, each traced to the exact email. Its agent works through narrow typed tools, and nothing sends without a fresh human approval.",
         stack=["Eve", "Next.js", "Neon", "MCP"], crew=["research", "connect", "verify"], link=True),
    dict(id="gotham-valet", name="Gotham Valet", meta="Hackathon · 2026", color="connect",
         tagline="Action-first NYC concierge",
         detail="Plans and runs city errands across transit, weather, Citi Bike and delivery, streams every tool call as it works, then keeps tracking long orders in the background.",
         stack=["Claude tool use", "Next.js", "Blaxel"], crew=["connect", "build"], link=True),
    dict(id="twelvesocial", name="TwelveSocial", meta="Best Use of DigitalOcean · 2025", color="build",
         tagline="Long videos in, social clips out",
         detail="Multimodal search across the visual, audio and text of long-form video finds the moments worth posting, and an AI chat cuts them into ready-to-post clips.",
         stack=["TwelveLabs", "DigitalOcean", "Next.js"], crew=["research", "build"], link=True),
    dict(id="uncompiler", name="Uncompiler", meta="uncompiler.com · 2026", color="verify",
         tagline="Research PDFs → compiling LaTeX",
         detail="Multimodel vision parsing, bibliography and figure recovery, and sandboxed agentic repair until the paper compiles. Web, REST and MCP interfaces.",
         stack=["Gemini", "Claude", "Tectonic", "MCP"], crew=["research", "build", "verify"], link=True),
    dict(id="olympus", name="Olympus", meta="Personal ops · 2026", color="dan",
         tagline="A chief-of-staff agent team",
         detail="A router hands work to named specialists, each behind approval gates. Untrusted email goes to a quarantined reader with no tools, and injection evals fail the build.",
         stack=["Eve", "Next.js", "Neon", "Evals"], crew=["dan", "connect", "verify"], link=False),
    dict(id="tradingmind", name="TradingMind", meta="Multi-agent · 2026", color="research",
         tagline="Multi-agent market intelligence",
         detail="Live WebSocket feeds, Claude Vision on charts, indicators, sentiment and order books combined into signals, with tool-calling chat over the live market.",
         stack=["Claude", "WebSockets", "Binance API"], crew=["research", "connect", "build"], link=True),
    dict(id="godeli", name="GoDeli", meta="Marketplace · 2026", color="build",
         tagline="Local delivery marketplace",
         detail="Customers, neighborhood stores and couriers in one real-time system: checkout, geospatial dispatch, proof of delivery, Stripe Connect payouts and native mobile.",
         stack=["Next.js", "Stripe Connect", "Capacitor"], crew=["build", "connect", "verify"], link=False),
    dict(id="robinclaw", name="RobinClaw", meta="Onchain · 2026", color="connect",
         tagline="Tokenized equity terminal",
         detail="Compares tokenized equities across Robinhood Chain, xStocks and Ondo against official prices, with direct Uniswap v4 reads, alerts and a native MCP server.",
         stack=["Viem", "Uniswap v4", "MCP"], crew=["research", "connect"], link=False),
]


def arrow_key(x, y, fg=YELLOW, bg=INK):
    return (outlined(x, y, 46, 46, bg, r=12, lip=5, stroke=2.5)
            + f'<path d="M{x + 15} {y + 31} L{x + 30} {y + 16} M{x + 18} {y + 15} H{x + 31} V{y + 28}" stroke="{fg}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')


def crew_row(ids, right, floor, h):
    out, x = [], right
    for i, cid in enumerate(reversed(ids)):
        uri, w, hh = char_uri(cid, h)
        x -= w * 0.78
        out.insert(0, f'<image class="ch d{i + 1}" href="{uri}" x="{ntos(x)}" y="{ntos(floor - hh)}" width="{ntos(w)}" height="{ntos(hh)}"/>')
    return "".join(out)


def small(p):
    W, H = 640, 360
    b = [outlined(6, 6, W - 12, H - 22, CARD, r=26, lip=8)]
    col = C[p["color"]]
    b.append(f'<rect x="7.5" y="7.5" width="14" height="{H - 25}" rx="7" fill="{col}"/>'
             f'<rect x="14" y="7.5" width="12" height="{H - 25}" fill="{col}"/>'
             f'<path d="M26 7.5 V{H - 17.5}" stroke="{INK}" stroke-width="2.5"/>')
    t, _, _ = tape(54, 34, p["meta"], col if p["color"] != "dan" else YELLOW, size=12.5,
                   ink=CARD if p["color"] in ("build",) else INK, rot=-2)
    b.append(t)
    if p["link"]:
        b.append(arrow_key(W - 72, 30))
    else:
        c, w = chip(W - 30 - MONO.width("PRIVATE REPO", 11, .66) - 20, 38, "Private repo", size=11, fg=MUTED, border=MUTED)
        b.append(c)
    b.append(DISPLAY.text(p["name"], 54, 128, 46))
    b.append(BODY_B.text(p["tagline"], 54, 166, 21, col if p["color"] not in ("verify", "dan", "research") else INK))
    for i, ln in enumerate(BODY.wrap(p["detail"], 17.5, W - 54 - 40)[:3]):
        b.append(BODY.text(ln, 54, 200 + i * 25, 17.5, MUTED))
    cx = 54
    for s in p["stack"]:
        c, w = chip(cx, 286, s, size=11)
        b.append(c)
        cx += w + 7
    b.append(crew_row(p["crew"], W - 22, H - 20, 70))
    return svg(W, H, "".join(b), f'{p["name"]}: {p["tagline"]}. {p["detail"]}', ANIM)


def gb10(x, y, w, h):
    """The Dell Pro Max GB10 as a little silver toy box."""
    out = [outlined(x, y, w, h, "#CFCBC2", r=14, lip=7, stroke=3)]
    for i in range(9):
        gx = x + 22 + i * 12
        out.append(f'<rect x="{gx}" y="{y + 18}" width="6" height="{h - 36}" rx="3" fill="{INK}" opacity=".22"/>')
    out.append(MONO.text("PRO MAX GB10", x + w - 20, y + h / 2 + 5, 13, INK, 1, anchor="end"))
    for i, cls in enumerate(("led", "led l2", "led l3")):
        out.append(f'<circle class="{cls}" cx="{x + w - 30 - i * 14}" cy="{y + h - 16}" r="4" fill="{["#86C98C", "#FFD54A", "#3A6FF0"][i]}"/>')
    return "".join(out)


def evehub():
    W, H = 1280, 470
    b = [outlined(6, 6, W - 12, H - 22, INK, r=32, lip=9)]
    b.append(f'<rect x="6" y="6" width="{W - 12}" height="{H - 22}" rx="32" fill="none" stroke="#3a3a44" stroke-width="1"/>')
    t, tw, _ = tape(58, 46, "Dell × NVIDIA AI Hackathon · 2026", YELLOW, size=14, rot=-2)
    b.append(t)
    b.append(DISPLAY.text("Eve Hub", 58, 148, 66, CARD))
    b.append(DISPLAY_IT.text("+ OmniPresence", 58 + DISPLAY.width("Eve Hub ", 66), 148, 66, C["research"]))
    b.append(BODY.text("Enterprise agents on hardware you own: one Dell Pro Max GB10, mostly offline.", 58, 190, 22, "#CFCBC2"))
    parts = [
        ("Eve Hub", C["build"], "Self-hosted agent hub: durable sessions on local Qwen through vLLM, no-egress OpenShell sandboxes with checkpoints, approval gates, and computer use on demand."),
        ("OmniPresence", C["verify"], "On the same box at once: face recognition, Whisper speech and a local Gemma “Overseer” that hands you per-person context mid-conversation."),
    ]
    for i, (n, col, txt) in enumerate(parts):
        px = 58 + i * 400
        b.append(f'<rect x="{px}" y="226" width="5" height="120" rx="2.5" fill="{col}"/>')
        b.append(BODY_B.text(n, px + 18, 248, 20, col))
        for j, ln in enumerate(BODY.wrap(txt, 16.5, 360)[:4]):
            b.append(BODY.text(ln, px + 18, 276 + j * 23, 16.5, CARD))
    cx = 58
    for s in ["128 GB unified memory", "Qwen on vLLM", "Gemma 12B", "Whisper", "InsightFace + YOLO"]:
        c, w = chip(cx, 386, s, size=11, fg="#CFCBC2", border="#6B675F")
        b.append(c)
        cx += w + 8
    # crew on top of the box
    b.append(gb10(900, 300, 320, 92))
    b.append(crew_row(["research", "build", "verify"], 1206, 302, 120))
    b.append(arrow_key(W - 78, 40, fg=INK, bg=YELLOW))
    return svg(W, H, "".join(b), "Eve Hub and OmniPresence, Dell x NVIDIA AI Hackathon 2026: enterprise agents on hardware you own, one Dell Pro Max GB10, mostly offline.", ANIM)


def roomscan():
    W, H = 1280, 470
    b = [outlined(6, 6, W - 12, H - 22, CARD, r=32, lip=9)]
    t, _, _ = tape(58, 46, "Dell × NVIDIA AI Hackathon · 2026", C["connect"], size=14, rot=-2)
    b.append(t)
    b.append(DISPLAY.text("ROOMSCAN", 58, 148, 66))
    lines = BODY_B.wrap("A few phones film a room. One offline GB10 turns their clips into a 3D scene you can fly through in the browser.", 21, 560)
    for i, ln in enumerate(lines):
        b.append(BODY_B.text(ln, 58, 192 + i * 29, 21, INK))
    y = 192 + len(lines) * 29 + 12
    for i, ln in enumerate(BODY.wrap("New clips rebuild the scene and open viewers swap to the fresh revision without reloading. People are masked out with YOLO. A 1M-point cloud plus a 300k-Gaussian splat takes about 43 seconds.", 17, 560)[:4]):
        b.append(BODY.text(ln, 58, y + i * 24, 17, MUTED))
    cx = 58
    for s in ["VGGT + Pi3X", "Gaussian splats", "SparkJS", "YOLO", "Fully offline"]:
        c, w = chip(cx, 386, s, size=11)
        b.append(c)
        cx += w + 8
    # poster, tilted, with a tape
    uri, pw, ph = image_uri(os.path.join(TOOLS, "roomscan-poster.webp"), 520)
    px, py = 690, 70
    b.append(f'<g transform="rotate(2 {px + pw / 2} {py + ph / 2})">'
             + outlined(px - 8, py - 8, pw + 16, ph + 16, CARD, r=18, lip=8, stroke=3)
             + f'<clipPath id="pc"><rect x="{px}" y="{py}" width="{ntos(pw)}" height="{ntos(ph)}" rx="10"/></clipPath>'
             f'<image href="{uri}" x="{px}" y="{py}" width="{ntos(pw)}" height="{ntos(ph)}" clip-path="url(#pc)" preserveAspectRatio="xMidYMid slice"/>'
             f'<rect x="{px}" y="{py}" width="{ntos(pw)}" height="{ntos(ph)}" rx="10" fill="none" stroke="{INK}" stroke-width="2"/></g>')
    t, _, _ = tape(px + 20, py - 26, "Live 3D splat", YELLOW, size=13, rot=-4)
    b.append(t)
    b.append(crew_row(["research", "build", "connect"], 1236, 444, 96))
    return svg(W, H, "".join(b), "ROOMSCAN, Dell x NVIDIA AI Hackathon 2026: a few phones film a room and one offline GB10 turns their clips into a 3D scene you can fly through in the browser.", ANIM)


if __name__ == "__main__":
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "eve-hub.svg"), "w").write(evehub())
    open(os.path.join(out, "roomscan.svg"), "w").write(roomscan())
    for p in SMALL:
        open(os.path.join(out, p["id"] + ".svg"), "w").write(small(p))
