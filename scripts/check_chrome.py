#!/usr/bin/env python3
"""Fail if the nav / CTA / footer chrome has drifted between pages."""
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))

NAV_START, NAV_END = '<a class="skip-link"', '<main id="main">'
TAIL_START = '  <section class="cta" data-nav-dark>'


def block(text, start, end=None):
    i = text.index(start)
    return text[i:text.index(end)] if end else text[i:]


def digest(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


rows, navs, tails = [], {}, {}
for page in pages:
    text = open(os.path.join(ROOT, page), encoding="utf-8").read()
    try:
        nav = digest(block(text, NAV_START, NAV_END))
        tail = digest(block(text, TAIL_START))
    except ValueError:
        print(f"  {page}: MISSING chrome markers")
        sys.exit(1)
    navs.setdefault(nav, []).append(page)
    tails.setdefault(tail, []).append(page)
    rows.append((page, nav, tail))

for page, nav, tail in rows:
    print(f"  {page:<24} nav {nav}  tail {tail}")

ok = True
if len(navs) > 1:
    ok = False
    print("\nNAV DRIFT:")
    for h, ps in navs.items():
        print(f"  {h}: {', '.join(ps)}")
if len(tails) > 1:
    ok = False
    print("\nCTA/FOOTER DRIFT:")
    for h, ps in tails.items():
        print(f"  {h}: {', '.join(ps)}")

print("\n" + ("chrome identical across all pages" if ok else "CHROME HAS DRIFTED"))
sys.exit(0 if ok else 1)
