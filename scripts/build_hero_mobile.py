#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phone art direction for the hero: a taller crop of the house, plus the badge
avatars.

The shipped cut-out is 1900x677 — 2.81:1. At width:100vw on a 390px screen
that is 139px tall, or 16% of the viewport, and the windows and interior
lights are far too small to read. Height and width cannot both be satisfied
from one asset: filling 45% of an 844px viewport at 2.81:1 needs a 1068px-wide
image, nearly three times the screen.

So the phone gets its own crop. Taking the centre of the villa at 1.15:1 makes
the house 87vw tall — 37-44% of an 844px viewport depending on width — while
staying exactly 100vw wide, and the upper storeys, glazing and warm lighting
all read at phone size. The crop is native resolution out of the 1900px
master, never upscaled.

Tightening AR further trades sky for house: 1.10 reaches 46% at 430px but
leaves only 23px above the badge, and 1.25 is roomier at the top but drops the
house to 34-40%. Change AR here and --hero-house-h-sm in tokens.css together.

Run: python scripts/build_hero_mobile.py
"""
import io
import os
import urllib.request

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")

AR = 1.15          # crop aspect; house height on a phone is 100vw / AR
WIDTHS = (500, 778)
Q, AQ = 78, 70     # the house is the hero subject — encoded above the card tiers

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126 Safari/537.36")

# Illustrated, not photographic. A photograph of a real person in a
# "families housed" badge reads as a claim that they are a real client.
AVATARS = [
    ("hero-avatar-1", "https://api.dicebear.com/9.x/personas/png?seed=Aina&size=96"
                      "&backgroundColor=d6ebf7"),
    ("hero-avatar-2", "https://api.dicebear.com/9.x/personas/png?seed=Rahul&size=96"
                      "&backgroundColor=e6e6e8"),
    ("hero-avatar-3", "https://api.dicebear.com/9.x/personas/png?seed=Mei&size=96"
                      "&backgroundColor=eaf4fb"),
]


def kb(path):
    return os.path.getsize(path) / 1024


def build_house():
    src = Image.open(os.path.join(IMG, "hero-house.png")).convert("RGBA")
    cw = min(src.width, int(round(src.height * AR)))
    x0 = (src.width - cw) // 2
    crop = src.crop((x0, 0, x0 + cw, src.height))
    print("crop %dx%d from %dx%d (centre %d%% of the villa)"
          % (crop.width, crop.height, src.width, src.height, cw / src.width * 100))

    for w in WIDTHS:
        if w > crop.width:
            print("SKIP  %dw — would upscale past the master" % w)
            continue
        h = round(crop.height * w / crop.width)
        out = os.path.join(IMG, "hero-house-mobile-%d.webp" % w)
        crop.resize((w, h), Image.LANCZOS).save(
            out, "WEBP", quality=Q, alpha_quality=AQ, method=6)
        print("wrote hero-house-mobile-%d.webp  %dx%d  %.1fKB" % (w, w, h, kb(out)))


def build_avatars():
    for name, url in AVATARS:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read()
        img = Image.open(io.BytesIO(raw)).convert("RGB").resize((48, 48), Image.LANCZOS)
        out = os.path.join(IMG, name + ".webp")
        img.save(out, "WEBP", quality=82, method=6)
        print("wrote %s.webp  48x48  %.1fKB" % (name, kb(out)))


if __name__ == "__main__":
    build_house()
    build_avatars()
