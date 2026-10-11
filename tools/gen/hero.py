from lib import *

W, H = 1280, 560

ANIM = """
.ch,.sh{transform-box:fill-box}
.ch{transform-origin:50% 100%;animation:hop 3.2s cubic-bezier(.3,.7,.4,1) infinite}
.sh{transform-origin:50% 50%;animation:shadow 3.2s cubic-bezier(.3,.7,.4,1) infinite}
.d1{animation-delay:-.2s}.d2{animation-delay:-1.1s}.d3{animation-delay:-2.3s}.d4{animation-delay:-.7s}.d5{animation-delay:-1.7s}
@keyframes hop{0%,58%,100%{transform:translateY(0) scale(1,1)}64%{transform:translateY(0) scale(1.06,.92)}74%{transform:translateY(-30px) scale(.96,1.05)}84%{transform:translateY(0) scale(1.07,.92)}90%{transform:translateY(0) scale(.98,1.02)}95%{transform:translateY(0) scale(1,1)}}
@keyframes shadow{0%,58%,100%{transform:scale(1);opacity:.16}74%{transform:scale(.62);opacity:.07}84%{transform:scale(1.08);opacity:.18}}
.bub{transform-box:fill-box;transform-origin:10% 100%;animation:bub 6.4s ease-in-out infinite}
@keyframes bub{0%{transform:scale(0);opacity:0}6%{transform:scale(1.08);opacity:1}10%,88%{transform:scale(1);opacity:1}94%,100%{transform:scale(0);opacity:0}}
.sw{animation:sw 6.4s ease-out infinite}
@keyframes sw{0%{stroke-dashoffset:360}12%,100%{stroke-dashoffset:0}}
@media (prefers-reduced-motion:reduce){.ch,.sh,.bub,.sw{animation:none}}
"""


def build():
    b = []
    b.append(
        f'<defs><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        f'<circle cx="2" cy="2" r="1.4" fill="{INK}" opacity=".09"/></pattern>'
        f'<clipPath id="cardclip"><rect x="6" y="6" width="{W - 12}" height="{H - 22}" rx="34"/></clipPath></defs>'
    )
    b.append(outlined(6, 6, W - 12, H - 22, PAPER, r=34, lip=9))
    b.append(f'<rect x="6" y="6" width="{W - 12}" height="{H - 22}" rx="34" fill="url(#dots)"/>')

    # left column
    x0 = 70
    t, tw, _ = tape(x0, 58, "Daniel Gildenbrand", YELLOW, size=16, rot=-2.5)
    b.append(t)
    t, _, _ = tape(x0 + tw + 14, 62, "New York, NY", C["build"], size=16, ink=CARD, rot=1.5)
    b.append(t)

    a, bpart = "I’ll build the ", "system."
    size = 92
    while DISPLAY.width(a, size) + DISPLAY_IT.width(bpart, size) > 640:
        size -= 1
    y1, y2 = 200, 200 + size * 1.04
    pre = "Give me the "
    gx = x0 + DISPLAY.width(pre, size)
    gw = DISPLAY.width("goal", size)
    # yellow highlighter swash behind "goal"
    b.append(
        f'<path class="sw" d="M{ntos(gx - 8)} {ntos(y1 - size * .22)} C {ntos(gx + gw * .3)} {ntos(y1 - size * .3)}, {ntos(gx + gw * .7)} {ntos(y1 - size * .16)}, {ntos(gx + gw + 12)} {ntos(y1 - size * .26)}" '
        f'stroke="{YELLOW}" stroke-width="{ntos(size * .42)}" stroke-linecap="round" fill="none" stroke-dasharray="360"/>'
    )
    b.append(DISPLAY.text("Give me the goal.", x0, y1, size))
    b.append(DISPLAY.text(a, x0, y2, size))
    b.append(DISPLAY_IT.text(bpart, x0 + DISPLAY.width(a, size), y2, size, C["build"]))

    by = y2 + 62
    lines = BODY.wrap(
        "AI systems engineer and full-stack builder. I run a small company of AI agents: "
        "they research, build, connect and verify, and I scope the goal and review every diff.",
        23, 600)
    for i, ln in enumerate(lines):
        b.append(BODY.text(ln, x0, by + i * 34, 23, MUTED))

    # keycap row
    ky = by + len(lines) * 34 + 22
    kx = x0
    for label, col, fg in (("danbrand.nyc", INK, CARD), ("7+ years shipping", CARD, INK), ("5 AI hackathon wins", CARD, INK)):
        arrow = col == INK
        w = BODY_B.width(label, 19) + 36 + (22 if arrow else 0)
        b.append(outlined(kx, ky, w, 44, col, r=12, lip=5, stroke=2.5))
        b.append(BODY_B.text(label, kx + 18, ky + 29, 19, fg))
        if arrow:
            ax = kx + w - 34
            b.append(f'<path d="M{ax} {ky + 30} L{ax + 12} {ky + 18} M{ax + 3} {ky + 17} H{ax + 13} V{ky + 27}" stroke="{YELLOW}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')
        kx += w + 14

    # stage
    b.append(f'<ellipse cx="990" cy="474" rx="285" ry="50" fill="{PANEL}"/>')
    b.append(character("research", 872, 396, 142, "d2"))
    b.append(character("build", 1100, 396, 128, "d4"))
    b.append(character("connect", 772, 490, 182, "d3"))
    b.append(character("verify", 1176, 490, 140, "d5"))
    b.append(character("dan", 988, 500, 240, "d1"))

    # speech bubble
    bx, byy, bw, bh = 1030, 58, 228, 86
    bub = (
        f'<g class="bub"><path d="M{bx + 30} {byy + bh - 2} L{bx + 6} {byy + bh + 34} L{bx + 62} {byy + bh - 2} Z" fill="{CARD}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
        f'<rect x="{bx}" y="{byy}" width="{bw}" height="{bh}" rx="22" fill="{CARD}" stroke="{INK}" stroke-width="3"/>'
        f'<rect x="{bx + 29}" y="{byy + bh - 6}" width="34" height="8" fill="{CARD}"/>'
        + BODY_B.text("What do you", bx + bw / 2, byy + 37, 22, INK, anchor="middle")
        + BODY_B.text("need done?", bx + bw / 2, byy + 66, 22, C["build"], anchor="middle")
        + "</g>"
    )
    b.append(bub)
    return svg(W, H, "".join(b), "Daniel Gildenbrand. Give me the goal. I'll build the system. AI systems engineer and full-stack builder who runs a team of AI agents.", ANIM)


if __name__ == "__main__":
    import sys
    open(sys.argv[1], "w").write(build())
