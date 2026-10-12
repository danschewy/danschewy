#!/usr/bin/env bash
# Rebuilds every SVG in ../assets. Needs python3 with fonttools, uharfbuzz and pillow.
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p fonts
B=https://raw.githubusercontent.com/google/fonts/main/ofl
[ -f fonts/fraunces.ttf ] || curl -sSfL -o fonts/fraunces.ttf "$B/fraunces/Fraunces%5BSOFT,WONK,opsz,wght%5D.ttf"
[ -f fonts/fraunces-it.ttf ] || curl -sSfL -o fonts/fraunces-it.ttf "$B/fraunces/Fraunces-Italic%5BSOFT,WONK,opsz,wght%5D.ttf"
[ -f fonts/bricolage.ttf ] || curl -sSfL -o fonts/bricolage.ttf "$B/bricolagegrotesque/BricolageGrotesque%5Bopsz,wdth,wght%5D.ttf"
[ -f fonts/martian.ttf ] || curl -sSfL -o fonts/martian.ttf "$B/martianmono/MartianMono%5Bwdth,wght%5D.ttf"
python3 - <<'PY'
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
for src, out, loc in [
    ("fraunces.ttf", "static-fraunces.ttf", dict(SOFT=100, WONK=1, opsz=144, wght=900)),
    ("fraunces-it.ttf", "static-fraunces-it.ttf", dict(SOFT=100, WONK=1, opsz=144, wght=800)),
    ("bricolage.ttf", "static-bricolage.ttf", dict(opsz=24, wdth=100, wght=400)),
    ("bricolage.ttf", "static-bricolage-bold.ttf", dict(opsz=24, wdth=100, wght=700)),
    ("martian.ttf", "static-martian.ttf", dict(wdth=87.5, wght=700)),
]:
    t = TTFont("fonts/" + src)
    instantiateVariableFont(t, loc, inplace=True)
    t.save("fonts/" + out)
PY
cd gen
python3 hero.py ../../assets/hero.svg
python3 crew.py ../../assets/crew.svg
python3 cards.py ../../assets/projects
python3 extras.py ../../assets
