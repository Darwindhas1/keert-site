#!/usr/bin/env python3
"""
Pass 2: download hand-picked Pexels photos into /assets/img as responsive WebP.

Every asset is encoded to WebP at each declared width, with quality stepped down
until the file lands under MAX_KB. Writes assets/img/credits.json + CREDITS.md
so photographer attribution can be rendered in the footer.

Run:  python scripts/fetch_media.py
"""
import io
import json
import os
import sys
import urllib.request

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
MAX_KB = 250
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126 Safari/537.36")


def load_key():
    with open(os.path.join(ROOT, ".env"), encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("PEXELS_API_KEY="):
                return line.split("=", 1)[1].strip()
    sys.exit("PEXELS_API_KEY missing from .env")


KEY = load_key()

# --- asset plan -----------------------------------------------------------
# name, pexels id, aspect (w/h), [widths], alt text
PLAN = [
    # Hero. The sky itself is a CSS gradient now; this is only a light cloud
    # layer screened over it, so it stays small and is not fetchpriority=high.
    ("hero-clouds",     1493759, (5, 2),    [1000], "Soft white clouds"),
    ("hero-house",      8134821, (16, 10),  [1600, 1200, 700], "Contemporary two-storey luxury home with a paved driveway and landscaped garden"),

    # Impact / stats
    ("impact-left",    30211366, (3, 4),    [900, 600], "Modern white house exterior with palm trees and an open patio"),
    ("impact-right",   38874193, (3, 4),    [900, 600], "Warmly lit modern lounge with a curved sofa and standing lamp"),

    # Services
    ("service-centre",  7546323, (4, 3),    [1200, 700], "Sleek modern living room with sculptural furniture and warm lighting"),

    # Listings (index uses 01-04, properties.html uses all twelve)
    ("listing-01",      7031406, (4, 3),    [1200, 700], "Contemporary country house with a stone and timber facade"),
    ("listing-02",      8082328, (4, 3),    [1200, 700], "Modern luxury villa with floor-to-ceiling windows and a lawn"),
    ("listing-03",     12720677, (4, 3),    [1200, 700], "Oceanfront villa with an infinity pool at dusk"),
    ("listing-04",     11631278, (4, 3),    [1200, 700], "Apartment block with a concrete facade and glass balconies"),
    ("listing-05",      7598368, (4, 3),    [1200, 700], "House with wide glass frontage surrounded by mature trees"),
    ("listing-06",     28054849, (4, 3),    [1200, 700], "Stone villa with an infinity pool lit at twilight"),
    ("listing-07",      9308434, (4, 3),    [1200, 700], "Low-rise apartment building with pale panel cladding"),
    ("listing-08",     13600836, (4, 3),    [1200, 700], "Single-storey house opening onto a paved patio and garden"),
    ("listing-09",     10647324, (4, 3),    [1200, 700], "Modern villa with a swimming pool framed by palm trees"),
    ("listing-10",     16110999, (4, 3),    [1200, 700], "Residential tower with curved glass balconies"),
    ("listing-11",      7031412, (4, 3),    [1200, 700], "Contemporary house with a covered terrace and tall windows"),
    ("listing-12",     34378030, (4, 3),    [1200, 700], "Low-slung villa beside a still reflecting pool"),

    # Featured full-bleed
    ("featured",       27626186, (16, 9),   [2000, 1200, 700], "Contemporary villa with an infinity pool overlooking a mountain range"),

    # Testimonials
    ("review-portrait", 30781748, (3, 4),   [800, 500], "Property consultant smiling in a bright office"),

    # About
    ("about-story",     7031604, (7, 5),    [1400, 800], "Contemporary home with panoramic glazing opening to a green lawn"),
    ("about-value-01", 12441654, (4, 3),    [1000, 600], "Open-plan living area with restrained minimalist furnishing"),
    ("about-value-02", 37857082, (4, 3),    [1000, 600], "Row of black and white houses in a modern residential street"),
    ("about-band",      7217929, (2, 1),    [1800, 1000], "Couple carrying boxes and plants into their new home"),

    # Services page — one per offering
    ("svc-buy",         7641919, (4, 3),    [1200, 700], "Couple celebrating in front of a sold sign at their new house"),
    ("svc-rent",       30781823, (4, 3),    [1200, 700], "Modern luxury villa with a lit pool at twilight"),
    ("svc-manage",      8135492, (4, 3),    [1200, 700], "Spacious living room with chandeliers and a plush sofa"),
    ("svc-valuation",  13729358, (4, 3),    [1200, 700], "Architectural scale model of a modern house"),

    # Property detail gallery
    ("gallery-01",      7031405, (16, 10),  [1600, 900, 500], "Modern cottage facade with mixed timber and stone cladding"),
    ("gallery-02",      7174113, (16, 10),  [1600, 900, 500], "Living room with sofas arranged on a rug facing the windows"),
    ("gallery-03",      7045703, (16, 10),  [1600, 900, 500], "Living room with a flower vase on the table beside an armchair"),
    ("gallery-04",      8135496, (16, 10),  [1600, 900, 500], "Open-plan living room with sculptural pendant lighting"),
    ("gallery-05",      8082312, (16, 10),  [1600, 900, 500], "Living area with floor-to-ceiling windows and a grand chandelier"),
    ("gallery-06",      7166640, (16, 10),  [1600, 900, 500], "Bright living room with a chandelier and a cosy sofa"),

    # Contact + 404
    ("contact-agent",   7641824, (3, 4),    [900, 600], "Property agent holding a clipboard in an office"),
    ("notfound",       28529023, (16, 9),   [1600, 900], "Minimalist cube house standing alone at sunset"),

    # A2Z listings with no client photography — stock stand-ins, chosen to
    # match the property type rather than hotlinking the developer sites.
    ("listing-mampu",      8221720, (4, 3), [1200, 700], "Contemporary apartment block with balconies and glazed facade"),
    ("listing-terrace",    8134817, (4, 3), [1200, 700], "Two-storey house with a timber facade and covered entrance"),
    ("listing-waterfront", 36806778, (4, 3), [1200, 700], "Modern apartment building overlooking the sea"),
    ("listing-ferringhi",  7501130, (4, 3), [1200, 700], "Contemporary white house set into a green hillside"),

    # Open Graph share card
    ("og-default",     8134821, (1200, 630), [1200], "Homy — contemporary luxury home with a landscaped driveway"),
]


def http_get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return resp.read()


def pexels_photo(pid):
    data = json.loads(http_get(f"https://api.pexels.com/v1/photos/{pid}",
                               {"Authorization": KEY}))
    return data


def encode(img, path, width, height):
    """Write WebP under MAX_KB, stepping quality down as needed."""
    frame = img.copy()
    frame = frame.convert("RGB")
    # cover-crop to the target aspect, then resize
    tw, th = width, height
    sw, sh = frame.size
    scale = max(tw / sw, th / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    frame = frame.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - tw) // 2, (nh - th) // 2
    frame = frame.crop((left, top, left + tw, top + th))

    for quality in (86, 80, 74, 68, 62, 56, 50):
        buf = io.BytesIO()
        frame.save(buf, "WEBP", quality=quality, method=6)
        if buf.tell() <= MAX_KB * 1024 or quality == 50:
            with open(path, "wb") as fh:
                fh.write(buf.getvalue())
            return buf.tell(), quality
    return 0, 0


os.makedirs(IMG, exist_ok=True)
credits = []

# Optional asset-name filter so a single photo can be re-pulled without
# re-downloading the whole set: python scripts/fetch_media.py service-centre
only = set(sys.argv[1:])
plan = [row for row in PLAN if not only or row[0] in only]

for name, pid, aspect, widths, alt in plan:
    meta = pexels_photo(pid)
    # pull a generous source once, then derive every width from it locally
    src_w = max(widths) if max(widths) > 1600 else 1600
    src = f"{meta['src']['original']}?auto=compress&cs=tinysrgb&w={max(src_w, 2400)}"
    raw = http_get(src)
    img = Image.open(io.BytesIO(raw))

    aw, ah = aspect
    made = []
    for w in widths:
        h = round(w * ah / aw)
        out = os.path.join(IMG, f"{name}-{w}.webp")
        size, q = encode(img, out, w, h)
        made.append(f"{name}-{w}.webp ({w}x{h}, {size // 1024}KB, q{q})")

    credits.append({
        "asset": name, "pexels_id": pid, "alt": alt,
        "photographer": meta["photographer"],
        "photographer_url": meta["photographer_url"],
        "source": meta["url"],
        "files": [f"{name}-{w}.webp" for w in widths],
    })
    print(" | ".join(made))

credits_path = os.path.join(IMG, "credits.json")

# A filtered run must not wipe the entries it did not rebuild.
if only and os.path.isfile(credits_path):
    with open(credits_path, encoding="utf-8") as fh:
        merged = {c["asset"]: c for c in json.load(fh)}
    merged.update({c["asset"]: c for c in credits})
    order = [row[0] for row in PLAN]
    credits = [merged[a] for a in order if a in merged]

with open(credits_path, "w", encoding="utf-8") as fh:
    json.dump(credits, fh, indent=1, ensure_ascii=False)

lines = ["# Photo credits", "",
         "All photography sourced from [Pexels](https://www.pexels.com) under the "
         "Pexels licence. Downloaded at build time — the live site makes no API calls.", ""]
seen = set()
for c in credits:
    tag = (c["photographer"], c["photographer_url"])
    if tag in seen:
        continue
    seen.add(tag)
    lines.append(f"- [{c['photographer']}]({c['photographer_url']})")
with open(os.path.join(IMG, "CREDITS.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")

print(f"\n{len(credits)} assets, {len(seen)} photographers -> assets/img/CREDITS.md")
