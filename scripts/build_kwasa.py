#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tiers for the Kwasa Damansara developer render.

Unlike the Pexels listings this one is not pre-cropped to 4:3. The source is
1.78:1 and the cards are 4/3 on desktop and 4/5 on phones, so the framing is
done in CSS with object-position rather than baked into the file — see
--kwasa-focus in tokens.css. Shipping the full frame keeps both crops honest.

The source is 1080px wide, so 1080 is the largest tier: a 1200 would be an
11% upscale, which is fake resolution.

Run: python scripts/build_kwasa.py
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
SRC = os.path.join(ROOT, "listing-mampu-kwasa.jpg")

BASE = "listing-mampu"
WIDTHS = (500, 700, 800, 1080)
Q = 82          # a clean architectural render shows banding below this
Q_JPG = 84


def kb(p):
    return os.path.getsize(p) / 1024


src = Image.open(SRC).convert("RGB")
print("source %dx%d  ar=%.3f" % (src.width, src.height, src.width / src.height))

for w in WIDTHS:
    if w > src.width:
        print("SKIP %dw — would upscale past the source" % w)
        continue
    h = round(src.height * w / src.width)
    im = src.resize((w, h), Image.LANCZOS) if w != src.width else src

    wp = os.path.join(IMG, "%s-%d.webp" % (BASE, w))
    im.save(wp, "WEBP", quality=Q, method=6)

    jp = os.path.join(IMG, "%s-%d.jpg" % (BASE, w))
    im.save(jp, "JPEG", quality=Q_JPG, optimize=True, progressive=True)

    print("wrote %s-%d  %dx%d   webp %6.1fKB   jpg %6.1fKB" % (BASE, w, w, h, kb(wp), kb(jp)))
