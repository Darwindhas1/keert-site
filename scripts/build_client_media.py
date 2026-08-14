#!/usr/bin/env python3
"""
Optimise the client-supplied images.

Two of the four are portrait marketing posters with text baked into them, so a
straight 4:3 card crop would slice the headline and phone number into
fragments. For those we crop the photographic region only, and keep the full
poster as a separate asset for the detail page.

Outputs WebP at 700w and 1200w plus a JPEG fallback at each width.
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
MAX_KB = 250

# name, source, crop box for the card (or None for centre-crop), card aspect
CARD_JOBS = [
    # Inside the gold circle on the poster — clear of all lettering.
    ("seberang-jaya-card", "seberang-jaya.jpg", (259, 388, 651, 682), (4, 3)),
    # The tower render only: below the "Luxury Living" strapline, above the
    # inset circle and the "Location Highlights" panel, and clear of the
    # scroll arrows the screenshot picked up on the right edge.
    ("gelugor-card", "gelugor.jpg", (260, 270, 720, 615), (4, 3)),
    ("seiras-card", "seiras.jpg", None, (4, 3)),
]

# Full posters, kept whole for the detail page
POSTER_JOBS = [
    ("seberang-jaya-poster", "seberang-jaya.jpg"),
    ("gelugor-poster", "gelugor.jpg"),
]

PORTRAIT_JOBS = [("agent-keerthana", "agent-keerthana.jpg", (1, 1))]


def cover(im, w, aspect):
    tw = w
    th = round(w * aspect[1] / aspect[0])
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    frame = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - tw) // 2, (nh - th) // 2
    return frame.crop((left, top, left + tw, top + th))


def save_pair(frame, base, width):
    webp = os.path.join(IMG, f"{base}-{width}.webp")
    for q in (88, 82, 76, 70, 64, 58):
        frame.save(webp, "WEBP", quality=q, method=6)
        if os.path.getsize(webp) <= MAX_KB * 1024:
            break
    jpg = os.path.join(IMG, f"{base}-{width}.jpg")
    for q in (86, 80, 74, 68, 62):
        frame.save(jpg, "JPEG", quality=q, optimize=True, progressive=True)
        if os.path.getsize(jpg) <= MAX_KB * 1024:
            break
    print(f"  {base}-{width}: {frame.size[0]}x{frame.size[1]}  "
          f"webp {os.path.getsize(webp)//1024}KB  jpg {os.path.getsize(jpg)//1024}KB")


print("card crops")
for base, src, box, aspect in CARD_JOBS:
    im = Image.open(os.path.join(IMG, src)).convert("RGB")
    if box:
        im = im.crop(box)
    for w in (1200, 700):
        if w > im.size[0] * 2:      # never upscale beyond 2x
            continue
        save_pair(cover(im, w, aspect), base, w)

print("posters (kept whole)")
for base, src in POSTER_JOBS:
    im = Image.open(os.path.join(IMG, src)).convert("RGB")
    ratio = im.size[1] / im.size[0]
    for w in (1200, 700):
        if w > im.size[0]:
            w = im.size[0]
        frame = im.resize((w, round(w * ratio)), Image.LANCZOS)
        save_pair(frame, base, w)

print("portrait")
for base, src, aspect in PORTRAIT_JOBS:
    im = Image.open(os.path.join(IMG, src)).convert("RGB")
    for w in (700,):
        save_pair(cover(im, w, aspect), base, w)
