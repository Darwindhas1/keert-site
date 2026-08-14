#!/usr/bin/env python3
"""Static check: every src/srcset/href in every page resolves to a real file."""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pages = [f for f in os.listdir(ROOT) if f.endswith(".html")]
missing, checked = [], 0

attr_re = re.compile(r'(?:src|href)="([^"]+)"')
srcset_re = re.compile(r'srcset="([^"]+)"')


def local(url):
    return not (url.startswith(("http://", "https://", "//", "#", "mailto:",
                                "tel:", "data:")))


for page in sorted(pages):
    text = open(os.path.join(ROOT, page), encoding="utf-8").read()

    urls = [u for u in attr_re.findall(text) if local(u)]
    for block in srcset_re.findall(text):
        urls += [p.strip().split()[0] for p in block.split(",") if p.strip()]

    for url in urls:
        checked += 1
        path = os.path.join(ROOT, url.split("?")[0].split("#")[0])
        if not os.path.isfile(path):
            missing.append(f"{page} -> {url}")

print(f"checked {checked} local references across {len(pages)} page(s)")
if missing:
    print("MISSING:")
    for m in sorted(set(missing)):
        print("  " + m)
    sys.exit(1)
print("all local references resolve")
