#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phone-sized tiers for every image the home page loads.

At 390px with a 2x screen the browser asks for ~700-780 device pixels, which
was pulling the 1000w and 1200w desktop tiers down the wire. These tiers sit
just above that ask, encoded at a lower quality because they are only ever
painted at half their pixel size — the loss is invisible at 2x density and
worth several hundred kilobytes on a phone.

Run: python scripts/build_mobile_tiers.py
"""
import os

from PIL import Image

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")

Q = 72          # opaque photography
Q_ALPHA = 74    # the cut-out house and the cloud band
AQ = 60         # alpha channel — feathered mattes hide it entirely

# source, output, target width, quality, alpha
JOBS = [
    ("hero-sky.jpg",              "hero-sky-800.webp",         800, Q,       False),
    ("hero-cloudband-1600.webp",  "hero-cloudband-800.webp",   800, Q_ALPHA, True),
    ("hero-house.png",            "hero-house-750.webp",       750, Q_ALPHA, True),
    ("svc-buy-1200.webp",         "svc-buy-800.webp",          800, Q,       False),
    ("svc-manage-1200.webp",      "svc-manage-800.webp",       800, Q,       False),
    ("listing-waterfront-1200.webp", "listing-waterfront-800.webp", 800, Q,  False),
    ("agent-keerthana.jpg",       "agent-keerthana-500.webp",  500, Q,       False),
]

# Existing 500w card tiers were encoded at the desktop quality ladder. They are
# only ever seen at 250 CSS px, so re-encode them down.
REENCODE = [
    "seiras-card-500.webp",
    "seberang-jaya-card-500.webp",
    "gelugor-card-500.webp",
    "listing-mampu-500.webp",
    "listing-terrace-500.webp",
    "listing-waterfront-500.webp",
    "listing-ferringhi-500.webp",
]


def kb(path):
    return os.path.getsize(path) / 1024


def resize(im, width):
    if im.width <= width:
        return im
    height = round(im.height * width / im.width)
    return im.resize((width, height), Image.LANCZOS)


for src, dst, width, q, alpha in JOBS:
    sp = os.path.join(ROOT, src)
    dp = os.path.join(ROOT, dst)
    if not os.path.exists(sp):
        print("SKIP  %-30s (no source %s)" % (dst, src))
        continue
    im = Image.open(sp)
    im = im.convert("RGBA" if alpha else "RGB")
    im = resize(im, width)
    if alpha:
        im.save(dp, "WEBP", quality=q, alpha_quality=AQ, method=6)
    else:
        im.save(dp, "WEBP", quality=q, method=6)
    print("wrote %-30s %4dx%-4d  %6.1fKB  (from %s %.1fKB)"
          % (dst, im.width, im.height, kb(dp), src, kb(sp)))

for name in REENCODE:
    p = os.path.join(ROOT, name)
    if not os.path.exists(p):
        print("SKIP  %-30s (missing)" % name)
        continue
    before = kb(p)
    im = Image.open(p).convert("RGB")
    im.save(p, "WEBP", quality=Q, method=6)
    print("requ  %-30s %4dx%-4d  %6.1fKB  (was %.1fKB)" % (name, im.width, im.height, kb(p), before))
