#!/usr/bin/env python3
"""
Build the hero house cut-out.

The supplied file (assets/img/hero-house-raw.jpg) is actually a PNG with a
clean alpha channel already, so no keying is needed. What it does need is a
feathered bottom edge so the house dissolves into the page instead of ending
on a hard horizontal line.

Master is built once at 1800w, then the smaller widths are derived from it so
every export shares the same feather.
"""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
SRC = os.path.join(IMG, "hero-house-raw.jpg")

MASTER_W = 1800
WIDTHS = [1800, 1400, 900]
FEATHER = 0.18   # fraction of height that fades out at the bottom
MAX_KB = 250


def feather_bottom(im, frac):
    """Ramp alpha to zero across the bottom `frac` of the image."""
    w, h = im.size
    alpha = im.getchannel("A")
    start = int(h * (1 - frac))

    # One-column gradient, stretched across the full width — cheap and exact.
    ramp = Image.new("L", (1, h), 255)
    for y in range(start, h):
        t = (y - start) / max(1, (h - 1 - start))
        ramp.putpixel((0, y), int(round(255 * (1 - t))))
    ramp = ramp.resize((w, h))

    from PIL import ImageChops
    im.putalpha(ImageChops.multiply(alpha, ramp))
    return im


src = Image.open(SRC).convert("RGBA")
print(f"source: {src.size[0]}x{src.size[1]}")

# The render is roughly half empty transparent sky. Cropping to the alpha
# bounding box turns a 1.5:1 image into a wide band that actually fits a hero
# strip, and drops the wasted pixels from every export.
bbox = src.getchannel("A").getbbox()
if bbox:
    src = src.crop(bbox)
    print(f"cropped to content: {src.size[0]}x{src.size[1]} "
          f"(aspect {src.size[0] / src.size[1]:.2f}:1)")

ratio = src.size[1] / src.size[0]
master = src.resize((MASTER_W, round(MASTER_W * ratio)), Image.LANCZOS)
master = feather_bottom(master, FEATHER)

png_path = os.path.join(IMG, "hero-house.png")
master.save(png_path, "PNG", optimize=True)
print(f"hero-house.png ({master.size[0]}x{master.size[1]}, "
      f"{os.path.getsize(png_path) // 1024}KB)")

for w in WIDTHS:
    frame = master if w == MASTER_W else master.resize(
        (w, round(w * ratio)), Image.LANCZOS)
    out = os.path.join(IMG, f"hero-house-{w}.webp")
    for q in (88, 82, 76, 70, 64, 58, 50):
        frame.save(out, "WEBP", quality=q, method=6, exact=False)
        if os.path.getsize(out) <= MAX_KB * 1024 or q == 50:
            break
    kb = os.path.getsize(out) // 1024
    has_alpha = Image.open(out).mode in ("RGBA", "LA")
    print(f"hero-house-{w}.webp ({frame.size[0]}x{frame.size[1]}, "
          f"{kb}KB, q{q}, alpha={has_alpha})")
