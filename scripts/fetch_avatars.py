#!/usr/bin/env python3
"""
Faces: RandomUser for testimonial/hero-stack avatars, Pravatar for the larger
team + agent portraits. Names are written by hand in the page copy (Malaysian),
so only the photos are taken from these services.

Also emits a JPEG twin of the Open Graph card — some crawlers still refuse WebP.
"""
import io
import json
import os
import urllib.request

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126 Safari/537.36")


def http_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def save_square(raw, path, size):
    img = Image.open(io.BytesIO(raw)).convert("RGB")
    w, h = img.size
    side = min(w, h)
    img = img.crop(((w - side) // 2, (h - side) // 2,
                    (w - side) // 2 + side, (h - side) // 2 + side))
    img = img.resize((size, size), Image.LANCZOS)
    img.save(path, "WEBP", quality=88, method=6)
    return os.path.getsize(path)


os.makedirs(IMG, exist_ok=True)

# --- RandomUser: hero avatar stack (4) + testimonial faces (2) --------------
data = json.loads(http_get("https://randomuser.me/api/?results=12&inc=picture&noinfo"))
pics = [r["picture"]["large"] for r in data["results"]]

targets = [("avatar-01", 96), ("avatar-02", 96), ("avatar-03", 96), ("avatar-04", 96),
           ("review-01", 128), ("review-02", 128)]
for (name, size), url in zip(targets, pics):
    n = save_square(http_get(url), os.path.join(IMG, f"{name}.webp"), size)
    print(f"{name}.webp ({size}x{size}, {n // 1024}KB) <- randomuser")

# --- Pravatar: team grid (6) + agent card (1), larger crops ----------------
for i, seed in enumerate(["homy-team-1", "homy-team-2", "homy-team-3",
                          "homy-team-4", "homy-team-5", "homy-team-6"], start=1):
    raw = http_get(f"https://i.pravatar.cc/600?u={seed}")
    n = save_square(raw, os.path.join(IMG, f"team-0{i}.webp"), 480)
    print(f"team-0{i}.webp (480x480, {n // 1024}KB) <- pravatar")

n = save_square(http_get("https://i.pravatar.cc/600?u=homy-agent-lead"),
                os.path.join(IMG, "agent-01.webp"), 480)
print(f"agent-01.webp (480x480, {n // 1024}KB) <- pravatar")

# --- JPEG twin of the OG card ---------------------------------------------
og = Image.open(os.path.join(IMG, "og-default-1200.webp")).convert("RGB")
og.save(os.path.join(IMG, "og-default.jpg"), "JPEG", quality=82, optimize=True)
print(f"og-default.jpg (1200x630, "
      f"{os.path.getsize(os.path.join(IMG, 'og-default.jpg')) // 1024}KB)")
