"""Tiny SVG toolkit: brand fonts as outlined paths, tapes, cards, characters."""
import base64, io, os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from PIL import Image

S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(S, "fonts")
CHARS = os.path.join(S, "chars")

INK = "#16161C"
PAPER = "#F7F4EE"
PANEL = "#EFE9DE"
CARD = "#FFFDF9"
MUTED = "#6B675F"
YELLOW = "#FFD54A"
C = {
    "dan": "#2B2B31",
    "research": "#A98BF5",
    "build": "#3A6FF0",
    "connect": "#FF7A66",
    "verify": "#86C98C",
}


def ntos(v):
    s = f"{v:.1f}"
    s = s.rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Font:
    def __init__(self, name):
        path = os.path.join(FONTS, name)
        data = open(path, "rb").read()
        self.hbf = hb.Font(hb.Face(data))
        self.tt = TTFont(path)
        self.gs = self.tt.getGlyphSet()
        self.upem = self.tt["head"].unitsPerEm
        self.order = self.tt.getGlyphOrder()

    def _shape(self, text):
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(self.hbf, buf, {"kern": True, "liga": True})
        return buf.glyph_infos, buf.glyph_positions

    def width(self, text, size, ls=0.0):
        infos, pos = self._shape(text)
        return sum(p.x_advance for p in pos) * size / self.upem + ls * len(infos)

    def d(self, text, x, y, size, ls=0.0):
        infos, pos = self._shape(text)
        sc = size / self.upem
        pen = SVGPathPen(self.gs, ntos=ntos)
        cx = x
        for i, p in zip(infos, pos):
            name = self.order[i.codepoint]
            tp = TransformPen(pen, (sc, 0, 0, -sc, cx + p.x_offset * sc, y - p.y_offset * sc))
            self.gs[name].draw(tp)
            cx += p.x_advance * sc + ls
        return pen.getCommands()

    def text(self, text, x, y, size, fill=INK, ls=0.0, anchor="start", extra=""):
        w = self.width(text, size, ls)
        if anchor == "middle":
            x -= w / 2
        elif anchor == "end":
            x -= w
        return f'<path d="{self.d(text, x, y, size, ls)}" fill="{fill}"{extra}/>'

    def wrap(self, text, size, maxw, ls=0.0):
        lines, cur = [], ""
        for word in text.split():
            t = (cur + " " + word).strip()
            if self.width(t, size, ls) <= maxw or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


DISPLAY = Font("static-fraunces.ttf")
DISPLAY_IT = Font("static-fraunces-it.ttf")
BODY = Font("static-bricolage.ttf")
BODY_B = Font("static-bricolage-bold.ttf")
MONO = Font("static-martian.ttf")


def char_uri(name, height, work=False):
    """A clay character as a webp data URI, sized for 2x displays."""
    im = Image.open(os.path.join(CHARS, f"{name}{'-work' if work else ''}.png"))
    h = int(height * 2)
    w = round(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=88, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode(), w / 2, height


def image_uri(path, width, quality=82):
    im = Image.open(path).convert("RGB")
    w = int(width * 2)
    h = round(im.height * w / im.width)
    im = im.resize((w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=quality, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode(), width, h / 2


def character(name, cx, floor, height, cls="", work=False, shadow=True):
    """Character standing on `floor`, centred on cx, with its own contact shadow."""
    uri, w, h = char_uri(name, height, work)
    out = []
    if shadow:
        out.append(
            f'<ellipse class="sh {cls}" cx="{ntos(cx)}" cy="{ntos(floor - 2)}" rx="{ntos(w * 0.36)}" ry="{ntos(height * 0.05)}" fill="{INK}" opacity=".16"/>'
        )
    out.append(
        f'<image class="ch {cls}" href="{uri}" x="{ntos(cx - w / 2)}" y="{ntos(floor - h)}" width="{ntos(w)}" height="{ntos(h)}"/>'
    )
    return "\n".join(out)


def tape(x, y, label, color, size=15, ink=INK, rot=-2.0, pad=14, h=None):
    """Label-maker tape: a colour strip with uppercase mono text."""
    label = label.upper()
    ls = size * 0.08
    w = MONO.width(label, size, ls) + pad * 2
    h = h or size * 2.1
    cx, cy = x + w / 2, y + h / 2
    return (
        f'<g transform="rotate({rot} {ntos(cx)} {ntos(cy)})">'
        f'<rect x="{ntos(x)}" y="{ntos(y)}" width="{ntos(w)}" height="{ntos(h)}" rx="3" fill="{color}"/>'
        f'<rect x="{ntos(x)}" y="{ntos(y + h - 4)}" width="{ntos(w)}" height="4" fill="{INK}" opacity=".12"/>'
        + MONO.text(label, x + pad, y + h / 2 + size * 0.36, size, ink, ls)
        + "</g>"
    ), w, h


def outlined(x, y, w, h, fill, r=22, lip=7, stroke=3):
    """Ink-outlined card with a chunky bottom lip, like the site's Toy HQ cards."""
    return (
        f'<rect x="{ntos(x)}" y="{ntos(y + lip)}" width="{ntos(w)}" height="{ntos(h)}" rx="{r}" fill="{INK}"/>'
        f'<rect x="{ntos(x)}" y="{ntos(y)}" width="{ntos(w)}" height="{ntos(h)}" rx="{r}" fill="{fill}" stroke="{INK}" stroke-width="{stroke}"/>'
    )


def chip(x, y, label, size=13, fg=INK, bg="none", border=INK):
    label = label.upper()
    ls = size * 0.06
    w = MONO.width(label, size, ls) + 20
    h = size * 2.0
    return (
        f'<rect x="{ntos(x)}" y="{ntos(y)}" width="{ntos(w)}" height="{ntos(h)}" rx="{ntos(h / 2)}" fill="{bg}" stroke="{border}" stroke-width="1.5"/>'
        + MONO.text(label, x + 10, y + h / 2 + size * 0.36, size, fg, ls)
    ), w


def svg(w, h, body, title, style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{title}">'
        f"<title>{title}</title>"
        + (f"<style>{style}</style>" if style else "")
        + body
        + "</svg>"
    )
