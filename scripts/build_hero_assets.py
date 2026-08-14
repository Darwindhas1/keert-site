#!/usr/bin/env python3
"""
Build every hero asset from the two supplied source images.

Both uploads are PNGs (despite the .jpg names). The house render already ships
a clean alpha channel on a near-black background, so NO colour keying is done:
keying on white would have erased the lit windows, the pool and the umbrella.
The alpha is used as-is, cropped to its real content band and feathered along
the bottom 8%.

The sky is never upscaled — exports stop at its native width.
"""
import os
import shutil

from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
MAX_KB = 250

SKY_SRC = os.path.join(ROOT, "cloud photo.jpg")
HOUSE_SRC = os.path.join(ROOT, "house render.jpg")


def encode(im, path, ladder=None):
    """Shrink the alpha channel before sacrificing colour quality.

    WebP stores alpha separately, and on a cut-out with a large soft edge the
    alpha is what blows the budget. Dropping alpha_quality costs nothing
    visible on a feathered matte, whereas dropping `quality` to 30 visibly
    wrecks the render.
    """
    if ladder is None:
        ladder = ((90, 100), (86, 85), (84, 70), (82, 55),
                  (78, 45), (72, 35), (64, 25), (56, 20))
    for q, aq in ladder:
        im.save(path, "WEBP", quality=q, alpha_quality=aq, method=6)
        if os.path.getsize(path) <= MAX_KB * 1024 or (q, aq) == ladder[-1]:
            return os.path.getsize(path) // 1024, f"q{q}/a{aq}"


# ---------------------------------------------------------------- sky -----
shutil.copyfile(SKY_SRC, os.path.join(IMG, "hero-sky.jpg"))
sky = Image.open(SKY_SRC).convert("RGB")
SW, SH = sky.size
print(f"sky source: {SW}x{SH}")

sky_widths = [w for w in (1600, 2400) if w <= SW]
if SW not in sky_widths:
    sky_widths.append(SW)          # native cap — never upscale
for w in sorted(set(sky_widths)):
    frame = sky if w == SW else sky.resize((w, round(w * SH / SW)), Image.LANCZOS)
    kb, q = encode(frame, os.path.join(IMG, f"hero-sky-{w}.webp"))
    print(f"hero-sky-{w}.webp ({frame.size[0]}x{frame.size[1]}, {kb}KB, q{q})")

# Cloud band for the bottom blend — the lower part of the same sky, where the
# cumulus sits, so the two layers are visually the same sky.
band = sky.crop((0, int(SH * 0.40), SW, SH))
bw = min(1600, SW)
band = band.resize((bw, round(bw * band.size[1] / band.size[0])), Image.LANCZOS)
kb, q = encode(band, os.path.join(IMG, "hero-cloudband-1600.webp"))
print(f"hero-cloudband-1600.webp ({band.size[0]}x{band.size[1]}, {kb}KB, q{q})")

# -------------------------------------------------------------- house -----
shutil.copyfile(HOUSE_SRC, os.path.join(IMG, "hero-house-raw.jpg"))
house = Image.open(HOUSE_SRC).convert("RGBA")
HW, HH = house.size
print(f"house source: {HW}x{HH}")

# Real content band (alpha bbox is the full frame because stray pixels touch
# the edges, so scan row coverage instead).
alpha = house.getchannel("A")
rows = [sum(1 for v in alpha.crop((0, y, HW, y + 1)).getdata() if v > 10)
        for y in range(HH)]
top = next(y for y, c in enumerate(rows) if c > HW * 0.01)
bottom = max(y for y, c in enumerate(rows) if c > HW * 0.01)
house = house.crop((0, top, HW, bottom + 1))
CW, CH = house.size
print(f"cropped to content: {CW}x{CH} (aspect {CW / CH:.2f}:1)")

# The render ends in a solid, full-width ground strip (~91 rows). Its abrupt
# termination is the hard horizontal line. Trim the flat terminal edge before
# feathering — but only the last 5%, because the full 16% band is the pool and
# lawn foreground, which is real imagery worth keeping.
GROUND_TRIM = 0.05
house = house.crop((0, 0, CW, CH - int(CH * GROUND_TRIM)))
CW, CH = house.size
print(f"trimmed terminal ground edge ({GROUND_TRIM:.0%}): {CW}x{CH}")


def feather_bottom(im, frac=0.08):
    w, h = im.size
    a = im.getchannel("A")
    start = int(h * (1 - frac))
    ramp = Image.new("L", (1, h), 255)
    for y in range(start, h):
        t = (y - start) / max(1, (h - 1 - start))
        ramp.putpixel((0, y), int(round(255 * (1 - t))))
    im.putalpha(ImageChops.multiply(a, ramp.resize((w, h))))
    return im


MASTER_W = 1900
master = house.resize((MASTER_W, round(MASTER_W * CH / CW)), Image.LANCZOS)
master = feather_bottom(master, 0.18)

# The last row must be fully transparent or a hairline edge shows on screen.
_last = max(master.getchannel("A").crop(
    (0, master.size[1] - 1, master.size[0], master.size[1])).getdata())
assert _last == 0, f"bottom row is not transparent (max alpha {_last})"
print(f"feathered bottom 18%; last row max alpha = {_last}")

png_path = os.path.join(IMG, "hero-house.png")
master.save(png_path, "PNG", optimize=True)
print(f"hero-house.png ({master.size[0]}x{master.size[1]}, "
      f"{os.path.getsize(png_path) // 1024}KB, alpha=True)")

for w in (1900, 1500, 1000):
    frame = master if w == MASTER_W else master.resize(
        (w, round(w * master.size[1] / master.size[0])), Image.LANCZOS)
    out = os.path.join(IMG, f"hero-house-{w}.webp")
    kb, q = encode(frame, out)
    print(f"hero-house-{w}.webp ({frame.size[0]}x{frame.size[1]}, {kb}KB, q{q}, "
          f"alpha={Image.open(out).mode})")

# ------------------------------------------------------------ QA proof ----
for name, bg in (("black", (0, 0, 0, 255)),
                 ("sky", (170, 209, 238, 255)),
                 ("magenta", (255, 0, 255, 255))):
    proof = Image.new("RGBA", master.size, bg)
    proof.alpha_composite(master)
    proof.convert("RGB").save(os.path.join(ROOT, f"shot-house-on-{name}.png"))
print("wrote cutout proofs on black / sky / magenta")
