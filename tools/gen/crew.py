from lib import *

W, H = 1280, 900

TEAM = [
    ("research", "Research", "RAG, search & live data",
     "Grounds every answer with cited retrieval, multimodal search and live market data.",
     ["pgvector", "Weaviate", "Gemini", "WebSockets"]),
    ("build", "Build", "Full-stack product & UI",
     "Turns the plan into a shipped product: apps, data models, payments, mobile, motion.",
     ["Next.js", "TypeScript", "Postgres", "Stripe"]),
    ("connect", "Connect", "Integrations & MCP",
     "Wires the systems together: MCP servers, automations, Shopify, HubSpot, Amazon.",
     ["MCP", "Activepieces", "Shopify", "HubSpot"]),
    ("verify", "Verify", "Evals, CI/CD & gates",
     "Nothing ships unchecked: evals, CI pipelines, tests and human approval gates.",
     ["Evals", "GitHub Actions", "Docker", "Jest"]),
]

ANIM = """
.ch{transform-box:fill-box;transform-origin:50% 100%;animation:bob 2.6s ease-in-out infinite}
.d1{animation-delay:-.3s}.d2{animation-delay:-1.2s}.d3{animation-delay:-2s}.d4{animation-delay:-.8s}.d0{animation-delay:-1.6s}
@keyframes bob{0%,100%{transform:translateY(0) scale(1,1)}50%{transform:translateY(-7px) scale(.985,1.015)}}
.sh{display:none}
.wire{stroke-dasharray:3 13;animation:flow 1.1s linear infinite}
@keyframes flow{to{stroke-dashoffset:-16}}
.pk{animation:pk 2.4s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){.ch,.wire,.pk{animation:none}}
"""


def build():
    b = []
    b.append(outlined(6, 6, W - 12, H - 22, PANEL, r=34, lip=9))
    t, _, _ = tape(64, 54, "The team", YELLOW, size=16, rot=-2)
    b.append(t)
    b.append(DISPLAY.text("One coordinator.", 64, 150, 58))
    b.append(DISPLAY_IT.text("Four specialists.", 64 + DISPLAY.width("One coordinator. ", 58), 150, 58, C["connect"]))
    b.append(BODY.text("Like running your own company: I hold the goal and the judgment, the agents do the legwork.", 64, 194, 22, MUTED))

    # coordinator
    dx, dfloor = 640, 420
    cw = 580
    b.append(outlined(dx - cw / 2, 236, cw, 196, CARD, r=24))
    b.append(character("dan", dx - 185, dfloor, 168, "d0", shadow=False))
    t, _, _ = tape(dx - 80, 262, "Dan · coordinate", C["dan"], size=14, ink=CARD, rot=-1.5)
    b.append(t)
    for i, ln in enumerate(BODY.wrap("Scopes the goal, splits it into workstreams, routes each one to the right agent, and reviews every diff before it ships.", 19.5, 345)):
        b.append(BODY.text(ln, dx - 78, 330 + i * 27, 19.5, INK))

    # cards
    cwid, gap = 274, 22
    x = (W - (cwid * 4 + gap * 3)) / 2
    top = 520
    for i, (cid, name, role, pitch, stack) in enumerate(TEAM):
        col = C[cid]
        cx = x + cwid / 2
        # wire from coordinator to card
        sx, sy = dx - 180 + i * 120, 432 + 7
        b.append(
            f'<path class="wire" d="M{ntos(sx)} {sy} C {ntos(sx)} {sy + 50}, {ntos(cx)} {top - 80}, {ntos(cx)} {top - 4}" '
            f'stroke="{col}" stroke-width="5" stroke-linecap="round" fill="none"/>'
        )
        b.append(outlined(x, top, cwid, 330, CARD, r=22))
        b.append(f'<rect x="{ntos(x + 1.5)}" y="{top + 1.5}" width="{cwid - 3}" height="118" rx="20.5" fill="{col}" opacity=".22"/>')
        b.append(character(cid, cx, top + 112, 100, f"d{i + 1}", shadow=False))
        t, _, _ = tape(x + 18, top + 128, name, col, size=14, ink=CARD if cid == "build" else INK, rot=-2 + i)
        b.append(t)
        b.append(BODY_B.text(role, x + 18, top + 190, 20, INK))
        for j, ln in enumerate(BODY.wrap(pitch, 16.5, cwid - 36)[:3]):
            b.append(BODY.text(ln, x + 18, top + 218 + j * 22, 16.5, MUTED))
        # stack chips, two rows max
        chx, chy = x + 18, top + 280
        for s in stack:
            c, w = chip(chx, chy, s, size=10.5)
            if chx + w > x + cwid - 14:
                chx, chy = x + 18, chy + 26
                c, w = chip(chx, chy, s, size=10.5)
            if chy > top + 306:
                break
            b.append(c)
            chx += w + 6
        x += cwid + gap
    return svg(W, H, "".join(b), "The team: Dan coordinates four AI specialists. Research does RAG, search and live data. Build does full-stack product and UI. Connect does integrations and MCP. Verify does evals, CI/CD and approval gates.", ANIM)


if __name__ == "__main__":
    import sys
    open(sys.argv[1], "w").write(build())
