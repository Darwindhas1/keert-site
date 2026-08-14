#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Delete images in assets/img/ that no page or stylesheet references.

Two traps this guards against:

  * Some assets are referenced by ABSOLUTE url (the Open Graph card is
    "https://.../assets/img/og-default.jpg"), so a scan for relative paths
    alone would wrongly mark them dead.
  * Several files are build INPUTS rather than page assets — the client
    posters and the raw hero render. Nothing links to them, but deleting
    them would make the build scripts unrunnable.

Dry run by default. Pass --apply to actually delete.
"""
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")

# Build inputs: no page links to these, but the scripts read them.
PROTECTED = {
    "hero-house-raw.jpg",      # build_hero_assets.py
    "hero-sky.jpg",            # build_hero_assets.py
    "hero-house.png",          # requested deliverable: cut-out with true alpha
    "og-default-1200.webp",    # fetch_avatars.py renders og-default.jpg from this
}

# Anything derived from a client-supplied image is kept whether or not a page
# currently links to it: these are the client's own assets, and the JPEG
# fallbacks are deliberately unwired rather than dead.
PROTECTED_PREFIXES = ("seberang-jaya", "gelugor", "seiras", "agent-keerthana")


def protected(name):
    return name in PROTECTED or name.startswith(PROTECTED_PREFIXES)

refs = set()
for path in glob.glob(os.path.join(ROOT, "*.html")) + \
        glob.glob(os.path.join(ROOT, "assets", "css", "*.css")):
    text = open(path, encoding="utf-8").read()
    # matches both "assets/img/x.webp" and "https://host/assets/img/x.jpg"
    refs.update(re.findall(r"assets/img/([A-Za-z0-9._-]+)", text))

files = sorted(os.path.basename(p) for p in
               glob.glob(os.path.join(IMG, "*.webp")) +
               glob.glob(os.path.join(IMG, "*.jpg")) +
               glob.glob(os.path.join(IMG, "*.png")))

dead = [f for f in files if f not in refs and not protected(f)]
kept_protected = [f for f in files if f not in refs and protected(f)]

total = sum(os.path.getsize(os.path.join(IMG, f)) for f in dead)

print("referenced by a page or stylesheet : %d" % len([f for f in files if f in refs]))
print("protected build inputs / deliverable: %d" % len(kept_protected))
for f in kept_protected:
    print("    keep  %s" % f)
print("unreferenced, safe to delete       : %d  (%.1f MB)" % (len(dead), total / 1048576))

groups = {}
for f in dead:
    stem = re.sub(r"-\d+\.(webp|jpg|png)$", "", f)
    stem = re.sub(r"\.(webp|jpg|png)$", "", stem)
    groups.setdefault(stem, []).append(f)

for stem in sorted(groups):
    size = sum(os.path.getsize(os.path.join(IMG, f)) for f in groups[stem])
    print("    %-24s %2d files  %6.0f KB" % (stem, len(groups[stem]), size / 1024))

if "--apply" in sys.argv:
    for f in dead:
        os.remove(os.path.join(IMG, f))
    print("\nDELETED %d files, reclaimed %.1f MB" % (len(dead), total / 1048576))
else:
    print("\ndry run — pass --apply to delete")
