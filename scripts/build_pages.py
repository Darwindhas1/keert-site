#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stamp the shared chrome from index.html into the other pages.

index.html is the single source of truth for the nav, the CTA band and the
footer. This lifts those blocks verbatim and wraps each page's own <head> and
<main> content around them, so the chrome cannot drift. Output is plain static
HTML — the site itself still has no build step.

Run:   python scripts/build_pages.py
Check: python scripts/check_chrome.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import page_content as pc  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://darwindhas1.github.io/homy-site/"

index = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

# Shared chrome: skip link -> opening <main>, and the CTA band -> </html>.
NAV = index[index.index('<a class="skip-link"'):index.index('<main id="main">')]
TAIL = index[index.index('  <section class="cta" data-nav-dark>'):]

HEAD = """<!DOCTYPE html>
<html lang="en-MY">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">

<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}{slug}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="A2Z Properties">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}{slug}">
<meta property="og:image" content="{site}assets/img/og-default.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Crect width='24' height='24' rx='6' fill='%230A0A0B'/%3E%3Cpath d='m5 11 7-5.5 7 5.5v7a1 1 0 0 1-1 1h-4v-5h-4v5H6a1 1 0 0 1-1-1z' fill='%23FAFAFA'/%3E%3C/svg%3E">

<link rel="preconnect" href="https://api.fontshare.com">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f%5B%5D=satoshi@700,800,900&amp;display=swap">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;display=swap">

<link rel="stylesheet" href="assets/css/tokens.css">
<link rel="stylesheet" href="assets/css/base.css">
<link rel="stylesheet" href="assets/css/components.css">
<link rel="stylesheet" href="assets/css/sections.css">
<link rel="stylesheet" href="assets/css/pages.css">

<script>document.documentElement.classList.add('js-motion');</script>
</head>

<body>
"""

OPEN_MAIN = '<main id="main">\n\n'

PAGES = {
    "properties.html": dict(
        title="New Project Launches in Penang &amp; Selangor — A2Z Properties",
        ogtitle="A2Z Properties — new project launches in Penang and Selangor",
        desc="Current new project launches across Penang and Selangor, from affordable "
             "housing to waterfront high-rise. Filter by state and speak to Keerthana direct.",
        main=OPEN_MAIN + pc.PROPERTIES,
    ),
    "property-detail.html": dict(
        title="Seberang Jaya — Penang new project launch — A2Z Properties",
        ogtitle="Seberang Jaya — Penang's largest affordable housing development",
        desc="Seberang Jaya, Penang. Freehold, built with PPVC technology, from RM3xx,xxx. "
             "Minutes from Sunway Mall, Penang 1st Bridge and Penang Sentral.",
        main=OPEN_MAIN + pc.DETAIL,
    ),
    "services.html": dict(
        title="Buying, Selling &amp; Investing — A2Z Properties",
        ogtitle="A2Z Properties — buying, selling and investing in Penang and Selangor",
        desc="Buying, selling and investing in new project launches across Penang and "
             "Selangor, with direct developer access and one point of contact throughout.",
        main=OPEN_MAIN + pc.SERVICES,
    ),
    "about.html": dict(
        title="About A2Z Properties — Keerthana Murugeswaran",
        ogtitle="About A2Z Properties — your local agent in Penang and Selangor",
        desc="A2Z Properties is led by Keerthana Murugeswaran, a local real estate agent "
             "covering new project launches across Penang and Selangor.",
        main=OPEN_MAIN + pc.ABOUT,
    ),
    "contact.html": dict(
        title="Contact A2Z Properties — Penang &amp; Selangor",
        ogtitle="Contact A2Z Properties — we reply within one business day",
        desc="Reach out for a viewing, a valuation, or just to ask what is out there. "
             "Covering Penang and Selangor, Malaysia.",
        main=OPEN_MAIN + pc.CONTACT,
    ),
    "404.html": dict(
        title="Page not found — A2Z Properties",
        ogtitle="Page not found — A2Z Properties",
        desc="That page has moved or never existed. Browse current new project launches "
             "across Penang and Selangor instead.",
        main=OPEN_MAIN + pc.NOTFOUND,
    ),
}

for slug, page in PAGES.items():
    html = (HEAD.format(title=page["title"], desc=page["desc"],
                        ogtitle=page["ogtitle"], slug=slug, site=SITE)
            + NAV + page["main"] + TAIL)
    with open(os.path.join(ROOT, slug), "w", encoding="utf-8") as fh:
        fh.write(html)
    print("wrote %s (%dKB)" % (slug, len(html) // 1024))
