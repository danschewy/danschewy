import os, sys
from lib import *

ANIM = """
.ch{transform-box:fill-box;transform-origin:50% 100%;animation:bob 2.6s ease-in-out infinite}
.d1{animation-delay:-.4s}.d2{animation-delay:-1.3s}.d3{animation-delay:-2.1s}.d4{animation-delay:-.9s}.d5{animation-delay:-1.8s}
@keyframes bob{0%,100%{transform:translateY(0) scale(1,1)}50%{transform:translateY(-8px) scale(.98,1.02)}}
.sh{display:none}
.st{transform-box:fill-box;transform-origin:50% 50%;animation:wob 5s ease-in-out infinite}
.s2{animation-delay:-1.6s}.s3{animation-delay:-3.2s}
@keyframes wob{0%,100%{transform:rotate(0)}50%{transform:rotate(1.6deg)}}
.cur{animation:blink 1s steps(2) infinite}
@keyframes blink{50%{opacity:0}}
@media (prefers-reduced-motion:reduce){.ch,.st,.cur{animation:none}}
"""


def stats():
    W, H = 1280, 330
    b = []
    items = [
        ("7+", "years shipping production software", YELLOW, "dan", -3),
        ("6", "developers led as a tech lead", C["research"], "research", 2),
        ("5", "AI hackathon awards, 2025–26", C["verify"], "verify", -2),
    ]
    sw, gap = 372, 40
    x = (W - sw * 3 - gap * 2) / 2
    for i, (num, label, col, who, rot) in enumerate(items):
        y = 96
        cx, cy = x + sw / 2, y + 100
        g = [outlined(x, y, sw, 196, col, r=26, lip=9)]
        g.append(DISPLAY.text(num, x + 32, y + 118, 96))
        for j, ln in enumerate(BODY_B.wrap(label, 22, sw - 64)):
            g.append(BODY_B.text(ln, x + 32, y + 154 + j * 28, 22))
        b.append(f'<g class="st s{i + 1}"><g transform="rotate({rot} {ntos(cx)} {ntos(cy)})">' + "".join(g) + "</g></g>")
        b.append(character(who, x + sw - 86, y + 36, 112 if who != "dan" else 128, f"d{i + 1}", shadow=False))
        x += sw + gap
    return svg(W, H, "".join(b), "7+ years shipping production software. 6 developers led as a tech lead. 5 AI hackathon awards in 2025 and 2026.", ANIM)


def cta():
    W, H = 1280, 360
    b = [outlined(6, 6, W - 12, H - 22, INK, r=34, lip=9)]
    t, _, _ = tape(60, 50, "Dispatch", YELLOW, size=15, rot=-2)
    b.append(t)
    b.append(DISPLAY.text("What do you", 60, 160, 64, CARD))
    b.append(DISPLAY_IT.text("need done?", 60 + DISPLAY.width("What do you ", 64), 160, 64, YELLOW))
    # a fake prompt line with a blinking cursor
    b.append(f'<rect x="60" y="196" width="640" height="58" rx="14" fill="#24242c" stroke="#3a3a44" stroke-width="2"/>')
    b.append(MONO.text("> give the team a goal at danbrand.nyc", 82, 232, 16, "#CFCBC2", 0.5))
    cw = MONO.width("> give the team a goal at danbrand.nyc", 16, 0.5)
    b.append(f'<rect class="cur" x="{ntos(84 + cw)}" y="214" width="11" height="24" fill="{YELLOW}"/>')
    b.append(BODY.text("I pick it up, split it across the team, and ship it with a human review on every diff.", 60, 296, 19, "#A9A59C"))
    # cast lineup on the right
    xs = [("connect", 830, 150), ("research", 925, 118), ("dan", 1040, 170), ("build", 1150, 110), ("verify", 1225, 100)]
    b.append(f'<ellipse cx="1030" cy="314" rx="230" ry="26" fill="#24242c"/>')
    for i, (cid, cx, h) in enumerate(xs):
        b.append(character(cid, cx, 318, h, f"d{i + 1}", shadow=False))
    return svg(W, H, "".join(b), "What do you need done? Give the team a goal at danbrand.nyc.", ANIM)


def header(label, color, ink=INK, name="h"):
    t, w, h = tape(10, 16, label, color, size=22, ink=ink, rot=-1.5, pad=20)
    return svg(round(w + 20), 80, t, label.title())


if __name__ == "__main__":
    out = sys.argv[1]
    open(os.path.join(out, "stats.svg"), "w").write(stats())
    open(os.path.join(out, "cta.svg"), "w").write(cta())
    for slug, label, col, ink in [("h-team", "The team", YELLOW, INK), ("h-built", "Things the team built", C["build"], CARD),
                                  ("h-numbers", "By the numbers", C["verify"], INK), ("h-wins", "Wins", C["connect"], INK)]:
        open(os.path.join(out, slug + ".svg"), "w").write(header(label, col, ink))
