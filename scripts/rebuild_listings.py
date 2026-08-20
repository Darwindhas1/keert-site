#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rebuild every listing image from its true original, in one pass.

Two rules, both of which the previous tiers broke:

1. NEVER EXPORT ABOVE NATIVE. Three of the client cards are crops taken out
   of marketing-poster screenshots, so their real resolution is far below the
   tier names that were sitting on disk:

       seberang-jaya-card   crop is  392x294  ->  a 700w tier was a 1.79x upscale
       gelugor-card         crop is  460x345  ->  a 700w tier was a 1.52x upscale
       seiras-card          crop is  900x900  ->  a 1200w tier was a 1.33x upscale

   Upscaling adds bytes and zero detail, and it is the reason those cards look
   soft. Tiers are now clamped to the native width; anything wider is skipped.

2. NEVER RE-ENCODE A WEBP. Earlier passes rebuilt the 500w tiers and some 800w
   tiers out of already-compressed webp files, which stacks generation loss.
   Every tier here is written from the original pixels — the client JPEGs, or
   a fresh Pexels download for the three stock listings.

Quality is fixed at 82 for listing imagery rather than stepped down to hit a
byte cap; the cap only decides which tiers exist, not how hard they are
squashed.

Run: python scripts/rebuild_listings.py
"""
import io
import json
import os
import urllib.request

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")

Q = 82          # floor for listing heroes, per the brief
Q_JPG = 84
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126 Safari/537.36")

# base, local source, crop box in the source (None = whole frame), aspect, tiers
CLIENT = [
    ("seberang-jaya-card", "seberang-jaya.jpg", (259, 388, 651, 682), (4, 3), [500, 700]),
    ("gelugor-card",       "gelugor.jpg",       (260, 270, 720, 615), (4, 3), [500, 700]),
    ("seiras-card",        "seiras.jpg",        None,                 (4, 3), [500, 700, 900]),
    ("listing-mampu",      "listing-mampu-source.jpg", None,   (1080, 607), [500, 700, 800, 1080]),
]

# base, pexels id, aspect, tiers — re-downloaded so nothing is re-compressed
STOCK = [
    ("listing-terrace",    8134817,  (4, 3), [500, 700, 1200]),
    ("listing-waterfront", 36806778, (4, 3), [500, 700, 800, 1200]),
    ("listing-ferringhi",  7501130,  (4, 3), [500, 700, 1200]),
]


def api_key():
    for line in io.open(os.path.join(ROOT, ".env"), encoding="utf-8"):
        if line.startswith("PEXELS_API_KEY"):
            return line.split("=", 1)[1].strip()
    raise SystemExit("PEXELS_API_KEY missing from .env")


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def cover(im, w, aspect):
    """Resize+crop to `w` at `aspect`. Caller guarantees w <= native."""
    tw = w
    th = round(w * aspect[1] / aspect[0])
    sw, sh = im.size
    scale = max(tw / sw, th / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    frame = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - tw) // 2, (nh - th) // 2
    return frame.crop((left, top, left + tw, top + th))


def native_width(im, aspect):
    """Widest honest render of this frame at the target aspect."""
    sw, sh = im.size
    want = aspect[0] / aspect[1]
    return sw if sw / sh <= want else round(sh * want)


def emit(src_im, base, aspect, tiers, jpg_twin):
    nat = native_width(src_im, aspect)
    kept, skipped = [], []
    for w in sorted(tiers):
        if w > nat:
            skipped.append(w)
            continue
        frame = cover(src_im, w, aspect)
        wp = os.path.join(IMG, "%s-%d.webp" % (base, w))
        frame.save(wp, "WEBP", quality=Q, method=6)
        size = os.path.getsize(wp) / 1024
        if jpg_twin:
            jp = os.path.join(IMG, "%s-%d.jpg" % (base, w))
            frame.save(jp, "JPEG", quality=Q_JPG, optimize=True, progressive=True)
        kept.append((w, frame.size[1], size))
    # a listing with no honest tier still needs one file: give it its native width
    if not kept:
        frame = cover(src_im, nat, aspect)
        wp = os.path.join(IMG, "%s-%d.webp" % (base, nat))
        frame.save(wp, "WEBP", quality=Q, method=6)
        if jpg_twin:
            frame.save(os.path.join(IMG, "%s-%d.jpg" % (base, nat)), "JPEG",
                       quality=Q_JPG, optimize=True, progressive=True)
        kept.append((nat, frame.size[1], os.path.getsize(wp) / 1024))
    print("  %-22s native %4dpx | kept %s%s"
          % (base, nat,
             ", ".join("%dw (%.0fKB)" % (w, kb) for w, _, kb in kept),
             ("  | SKIPPED as upscale: " + ", ".join("%dw" % w for w in skipped))
             if skipped else ""))
    return nat, [w for w, _, _ in kept], skipped


report = {}

print("client-supplied sources")
for base, src, box, aspect, tiers in CLIENT:
    im = Image.open(os.path.join(IMG, src)).convert("RGB")
    if box:
        im = im.crop(box)
    nat, kept, skipped = emit(im, base, aspect, tiers, jpg_twin=True)
    report[base] = dict(native=nat, kept=kept, skipped=skipped, source=src)

print("\nstock sources — re-downloaded, never re-encoded from webp")
key = api_key()
for base, pid, aspect, tiers in STOCK:
    meta = json.loads(get("https://api.pexels.com/v1/photos/%d" % pid,
                          {"Authorization": key}))
    raw = get("%s?auto=compress&cs=tinysrgb&w=2400" % meta["src"]["original"])
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    nat, kept, skipped = emit(im, base, aspect, tiers, jpg_twin=False)
    report[base] = dict(native=nat, kept=kept, skipped=skipped,
                        source="pexels %d (%dx%d original)" % (pid, meta["width"], meta["height"]))

with io.open(os.path.join(ROOT, "scripts", "listing-resolution.json"), "w",
             encoding="utf-8") as fh:
    fh.write(json.dumps(report, indent=1) + "\n")
print("\nwrote scripts/listing-resolution.json")
