#!/usr/bin/env python3
"""Pass 1: query Pexels and dump candidate metadata so photos can be hand-picked."""
import json, os, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_key():
    with open(os.path.join(ROOT, ".env"), encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("PEXELS_API_KEY="):
                return line.split("=", 1)[1].strip()
    sys.exit("PEXELS_API_KEY missing from .env")


KEY = load_key()
# Pexels 403s the default Python-urllib agent.
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"

QUERIES = [
    ("blue sky clouds",                  "landscape", 15),
    ("modern luxury house exterior",     "landscape", 15),
    ("minimalist home architecture",     "landscape", 15),
    ("modern villa pool",                "landscape", 15),
    ("apartment building modern",        "landscape", 15),
    ("luxury home interior living room", "landscape", 15),
    ("real estate agent portrait",       "portrait",  15),
    ("happy couple new home",            "landscape", 15),
    ("modern luxury house exterior",     "portrait",  15),
    ("luxury home interior living room", "portrait",  15),
]


def fetch(query, orientation, per_page):
    url = ("https://api.pexels.com/v1/search?"
           + urllib.parse.urlencode({"query": query, "per_page": per_page,
                                     "orientation": orientation}))
    req = urllib.request.Request(url, headers={"Authorization": KEY, "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.load(resp)


out = {}
for q, orient, n in QUERIES:
    data = fetch(q, orient, n)
    key = f"{q} [{orient}]"
    out[key] = [
        {"id": p["id"], "w": p["width"], "h": p["height"],
         "photographer": p["photographer"], "url": p["url"],
         "alt": p.get("alt") or "", "original": p["src"]["original"]}
        for p in data.get("photos", [])
    ]
    print(f"{key}: {len(out[key])} results", file=sys.stderr)

path = os.path.join(ROOT, "scripts", "pexels-candidates.json")
with open(path, "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1, ensure_ascii=False)
print(f"wrote {path}", file=sys.stderr)
