#!/usr/bin/env python3
"""
Stamp the shared chrome from index.html into the other pages.

index.html is the single source of truth for the nav, the CTA band and the
footer. This lifts those blocks verbatim and wraps each page's own <head> and
<main> content around them, so the chrome cannot drift. Output is plain static
HTML — the site itself still has no build step.

Run:  python scripts/build_pages.py
Check: python scripts/check_chrome.py
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

index = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()

# Shared chrome: everything from the skip link to the opening <main>, and
# everything from the CTA band to </html>.
NAV = index[index.index('<a class="skip-link"'):index.index('<main id="main">')]
TAIL = index[index.index('  <section class="cta" data-nav-dark>'):]

HEAD = """<!DOCTYPE html>
<html lang="en-MY">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://homy.com.my/{slug}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Homy">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://homy.com.my/{slug}">
<meta property="og:image" content="https://homy.com.my/assets/img/og-default.jpg">
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

BED = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
       'stroke-linecap="round" aria-hidden="true"><path d="M2 4v16"/>'
       '<path d="M2 9h18a2 2 0 0 1 2 2v9"/><path d="M2 16h20"/><path d="M6 9V6"/></svg>')
BATH = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" aria-hidden="true"><path d="M4 12V5a2 2 0 0 1 3.4-1.4L9 5"/>'
        '<path d="M2 12h20v3a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4z"/><path d="M7 19v2"/>'
        '<path d="M17 19v2"/></svg>')
AREA = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" aria-hidden="true"><path d="M8 3H5a2 2 0 0 0-2 2v3"/>'
        '<path d="M21 8V5a2 2 0 0 0-2-2h-3"/><path d="M3 16v3a2 2 0 0 0 2 2h3"/>'
        '<path d="M16 21h3a2 2 0 0 0 2-2v-3"/></svg>')
HOUSE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22v-9h6v9"/></svg>')
GLYPH = ('<svg class="eyebrow__glyph" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/>'
         '<circle cx="12" cy="12" r="3.5" fill="currentColor" stroke="none"/></svg>')

# img, name, area, price, suffix, type, location, beds, baths, sqft, alt
LISTINGS = [
    ("listing-01", "Straits Residence", "Tanjung Tokong, Penang", "RM 1,850,000", "", "buy", "penang", 4, 3, "2,150", "Contemporary country house with a stone and timber facade"),
    ("listing-02", "Gurney Paragon Suites", "George Town, Penang", "RM 4,200", "/mo", "rent", "penang", 3, 2, "1,480", "Modern luxury villa with floor-to-ceiling windows and a lawn"),
    ("listing-03", "Villa Anggerik", "Tambun, Ipoh", "RM 2,450,000", "", "buy", "ipoh", 5, 4, "3,600", "Oceanfront villa with an infinity pool at dusk"),
    ("listing-04", "Teluk Baru Beachfront", "Pantai Cenang, Langkawi", "RM 6,800", "/mo", "rent", "langkawi", 3, 3, "1,900", "Apartment block with a concrete facade and glass balconies"),
    ("listing-05", "Rumah Lestari", "Bukit Gambir, Penang", "RM 1,290,000", "", "buy", "penang", 3, 2, "1,750", "House with wide glass frontage surrounded by mature trees"),
    ("listing-06", "Cenang Bayview Villa", "Pantai Cenang, Langkawi", "RM 3,900,000", "", "buy", "langkawi", 5, 5, "4,200", "Stone villa with an infinity pool lit at twilight"),
    ("listing-07", "Seri Ampangan Court", "Alor Setar, Kedah", "RM 1,950", "/mo", "rent", "alor-setar", 2, 1, "980", "Low-rise apartment building with pale panel cladding"),
    ("listing-08", "Taman Ipoh Timur Bungalow", "Ipoh, Perak", "RM 1,680,000", "", "buy", "ipoh", 4, 3, "2,800", "Single-storey house opening onto a paved patio and garden"),
    ("listing-09", "Andaman Cove Residence", "Kuah, Langkawi", "RM 5,500", "/mo", "rent", "langkawi", 3, 2, "1,620", "Modern villa with a swimming pool framed by palm trees"),
    ("listing-10", "The Light Waterfront", "Gelugor, Penang", "RM 2,150,000", "", "buy", "penang", 4, 3, "2,400", "Residential tower with curved glass balconies"),
    ("listing-11", "Kinta Riverside House", "Ipoh, Perak", "RM 3,100", "/mo", "rent", "ipoh", 3, 2, "1,540", "Contemporary house with a covered terrace and tall windows"),
    ("listing-12", "Darulaman Heights", "Alor Setar, Kedah", "RM 890,000", "", "buy", "alor-setar", 4, 2, "2,050", "Low-slung villa beside a still reflecting pool"),
]


def card(row, hidden):
    img, name, area, price, suffix, kind, loc, beds, baths, sqft, alt = row
    label = "For Rent" if kind == "rent" else "For Buy"
    sfx = f'<span class="small">{suffix}</span>' if suffix else ""
    return f"""          <a class="card-img" href="property-detail.html" data-card
             data-type="{kind}" data-loc="{loc}"{' hidden' if hidden else ''}>
            <img class="card-img__media" src="assets/img/{img}-1200.webp"
                 srcset="assets/img/{img}-700.webp 700w, assets/img/{img}-1200.webp 1200w"
                 sizes="(max-width: 900px) 92vw, 31vw" width="1200" height="900"
                 alt="{alt}" loading="lazy" decoding="async">
            <span class="badge badge--glass card-img__status">{HOUSE}{label}</span>
            <div class="card-img__body">
              <p class="card-img__name">{name}, {area}</p>
              <div class="card-img__foot">
                <div>
                  <p class="card-img__price">{price}{sfx}</p>
                  <ul class="meta-row">
                    <li>{BED}{beds} beds</li>
                    <li>{BATH}{baths} baths</li>
                    <li>{AREA}{sqft} sq ft</li>
                  </ul>
                </div>
              </div>
            </div>
          </a>"""


CHIPS = [("all", "All"), ("buy", "Buy"), ("rent", "Rent"),
         ("penang", "Penang"), ("ipoh", "Ipoh"),
         ("langkawi", "Langkawi"), ("alor-setar", "Alor Setar")]

chips_html = "\n".join(
    f'          <button class="chip{" is-on" if v == "all" else ""}" type="button" '
    f'data-filter="{v}" aria-pressed="{"true" if v == "all" else "false"}">{t}</button>'
    for v, t in CHIPS)

cards_html = "\n".join(card(r, i >= 6) for i, r in enumerate(LISTINGS))

PROPERTIES_MAIN = f"""<main id="main">

  <!-- ===================== PAGE INTRO ===================== -->
  <section class="section page-intro">
    <div class="container">
      <div class="page-intro__head">
        <span class="eyebrow" data-reveal>{GLYPH}Property listings</span>
        <h1 data-reveal>Every home we have<br>on the market</h1>
        <p class="lede" data-reveal>
          Twelve properties across Penang, Ipoh, Langkawi and Alor Setar. Each one
          has been walked, measured and photographed by our own negotiators — what
          you see here is what you will find at the viewing.
        </p>
      </div>
    </div>
  </section>

  <!-- ===================== FILTERS + GRID ===================== -->
  <section class="section props">
    <div class="container">

      <div class="filters" role="group" aria-label="Filter listings" data-reveal>
{chips_html}
      </div>

      <p class="filters__count" data-count-out role="status">Showing 6 of 12 homes</p>

      <div class="props__grid" data-grid>
{cards_html}
      </div>

      <div class="props__more">
        <button class="btn btn--ghost" type="button" data-load-more>
          Load more homes
          <span class="btn__chip" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14"/><path d="m19 12-7 7-7-7"/></svg>
          </span>
        </button>
        <p class="props__empty" data-empty hidden>No homes match that filter yet. Try another area.</p>
      </div>

    </div>
  </section>

"""

import page_content as pc

PAGES = {
    "properties.html": dict(
        title="Properties for Sale &amp; Rent in Penang, Ipoh &amp; Langkawi — Homy",
        ogtitle="Homy — Properties for Sale and Rent across Malaysia",
        desc="Browse verified homes for sale and rent across Penang, Ipoh, Langkawi and "
             "Alor Setar. Filter by type and location, with full specs on every listing.",
        main=PROPERTIES_MAIN,
    ),
    "property-detail.html": dict(
        title="Bukit Jambul Hillside Estate, Bayan Lepas — Homy",
        ogtitle="Bukit Jambul Hillside Estate — six bedrooms above Bayan Lepas",
        desc="A six-bedroom freehold detached house on the Bukit Jambul ridge, Penang. "
             "Full gallery, measured specifications, and viewings booked direct with the "
             "listing negotiator.",
        main="<main id=\"main\">\n\n" + pc.DETAIL,
    ),
    "services.html": dict(
        title="Buying, Renting, Management &amp; Valuation — Homy",
        ogtitle="Homy — Four property services, done properly",
        desc="Buying, renting, property management and valuation across Penang, Ipoh, "
             "Langkawi and Alor Setar. Independent valuations, tenancies held in trust "
             "and one contact from first viewing to handover.",
        main="<main id=\"main\">\n\n" + pc.SERVICES,
    ),
    "about.html": dict(
        title="About Homy — a licensed agency in four Malaysian markets",
        ogtitle="About Homy — twelve years in four Malaysian markets",
        desc="Homy is an eleven-person licensed estate agency working Penang, Ipoh, "
             "Langkawi and Alor Setar since 2014. Meet the negotiators and read the four "
             "rules we have never broken.",
        main="<main id=\"main\">\n\n" + pc.ABOUT,
    ),
    "contact.html": dict(
        title="Contact Homy — George Town, Pulau Pinang",
        ogtitle="Contact Homy — we reply within one working day",
        desc="Talk to a licensed negotiator about buying, renting or managing property in "
             "Penang, Ipoh, Langkawi or Alor Setar. Office on Lebuh Farquhar, George Town.",
        main="<main id=\"main\">\n\n" + pc.CONTACT,
    ),
    "404.html": dict(
        title="Page not found — Homy",
        ogtitle="Page not found — Homy",
        desc="That page has moved or never existed. Browse current listings across "
             "Penang, Ipoh, Langkawi and Alor Setar instead.",
        main="<main id=\"main\">\n\n" + pc.NOTFOUND,
    ),
}

for slug, page in PAGES.items():
    html = (HEAD.format(title=page["title"], desc=page["desc"],
                        ogtitle=page["ogtitle"], slug=slug)
            + NAV + page["main"] + TAIL)
    with open(os.path.join(ROOT, slug), "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"wrote {slug} ({len(html) // 1024}KB)")
