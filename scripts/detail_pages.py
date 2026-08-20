#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The seven property detail pages.

One template, seven listings. Everything here is client-supplied: specs and
prices come from the listing data, and descriptive copy exists only where
Keerthana has actually provided it.

Where there is no copy, `lede` is None and the page simply has no description
section — specs, price, location and the enquiry block, nothing invented about
the development. Same for `items` (the features / getting-around list) and for
`map`, which is omitted rather than dropping a marker on a locality that cannot
be placed with confidence.
"""
from page_content import ARROW, GLYPH

DETAILS = [
    dict(
        slug="property-seberang-jaya.html",
        eyebrow="New project",
        name="Seberang Jaya",
        place="Seberang Jaya, Penang",
        lede="Penang's largest affordable housing development. Freehold, built with "
             "PPVC technology, and within ten minutes of the first bridge and "
             "Penang Sentral.",
        specs=[("Project", "Seberang Jaya"), ("Location", "Seberang Jaya, Penang"),
               ("Tenure", "Freehold"), ("Construction", "PPVC technology"),
               ("Price from", "RM3xx,xxx"), ("Status", "New project launch")],
        list_head="Getting around",
        items=["3 minutes to Sunway Mall and Sunway Hospital",
               "5 minutes to the beach",
               "10 minutes to Penang 1st Bridge",
               "10 minutes to Penang Sentral"],
        gallery=[("seberang-jaya-card-392", 392, 294, "seberang-jaya-card-392",
                  "High-rise towers and landscaped pool deck at Seberang Jaya"),
                 ("seberang-jaya-poster-700", 700, 1050, "seberang-jaya-poster-900",
                  "Seberang Jaya project poster with pricing and travel times")],
        map=dict(h2="Seberang Jaya,<br>mainland Penang",
                 lede="On the mainland side, minutes from Sunway Carnival and within "
                      "a short drive of both the first bridge and Penang Sentral.",
                 title="Map showing Seberang Jaya, Penang",
                 bbox="100.3720%2C5.3800%2C100.4120%2C5.4080",
                 marker="5.3940%2C100.3920"),
        title="Seberang Jaya &mdash; Penang new project launch &mdash; A2Z Properties",
        ogtitle="Seberang Jaya &mdash; Penang's largest affordable housing development",
        desc="Seberang Jaya, Penang. Freehold, built with PPVC technology, from "
             "RM3xx,xxx. Minutes from Sunway Mall, Penang 1st Bridge and Penang Sentral.",
    ),
    dict(
        slug="property-gelugor.html",
        eyebrow="New project",
        name="Gelugor",
        place="Gelugor, Penang",
        lede="High-rise luxury condominium with sea and city skyline views. Infinity "
             "pool and sky facilities. Directly opposite a future LRT station, near "
             "the Penang Bridge, with easy access to Bayan Lepas and George Town. "
             "Limited prime units.",
        specs=[("Project", "Gelugor"), ("Location", "Gelugor, Penang"),
               ("Price", "RM8xx,xxx &ndash; RM1.x Million"),
               ("Status", "New project launch")],
        list_head="Features",
        items=["Sea and city skyline views",
               "Infinity pool and sky facilities",
               "Future LRT station directly opposite",
               "Near the Penang Bridge",
               "Easy access to Bayan Lepas and George Town",
               "Limited prime units"],
        gallery=[("gelugor-card-460", 460, 345, "gelugor-card-460",
                  "Luxury high-rise condominium beside Penang Bridge at sunset"),
                 ("gelugor-poster-700", 700, 981, "gelugor-poster-794",
                  "Gelugor project poster with pricing and unit details")],
        map=dict(h2="Gelugor,<br>Penang island",
                 lede="On the island's east coast, beside the Penang Bridge "
                      "interchange and within reach of Bayan Lepas and George Town.",
                 title="Map showing Gelugor, Penang",
                 bbox="100.2850%2C5.3450%2C100.3250%2C5.3730",
                 marker="5.3590%2C100.3050"),
        title="Gelugor &mdash; Penang luxury condominium launch &mdash; A2Z Properties",
        ogtitle="Gelugor &mdash; sea and city views, opposite a future LRT station",
        desc="Gelugor, Penang. High-rise luxury condominium with sea and city views, "
             "infinity pool and sky facilities, opposite a future LRT station. "
             "RM8xx,xxx to RM1.x Million.",
    ),
    dict(
        slug="property-mampu-kwasa.html",
        eyebrow="New project",
        name="Rumah Mampu Milik",
        place="Kwasa Damansara, Selangor",
        # The one descriptive line Keerthana supplied, used verbatim.
        lede="Affordable housing in the Kwasa Damansara transit corridor.",
        specs=[("Project", "Rumah Mampu Milik"),
               ("Location", "Kwasa Damansara, Selangor"),
               ("Bedrooms", "2"), ("Bathrooms", "1"), ("Built-up", "550 sq ft"),
               ("Price from", "RM2xx,xxx"), ("Status", "New project launch")],
        list_head=None,
        items=None,
        gallery=[("listing-mampu-1080", 1080, 607, "listing-mampu-1080",
                  "Developer render of the Rumah Mampu Milik tower at Kwasa "
                  "Damansara, with the MRT line running past its podium at dusk")],
        map=dict(h2="Kwasa Damansara,<br>Selangor",
                 lede="In the Kwasa Damansara transit corridor, on the MRT line "
                      "north-west of Kuala Lumpur.",
                 title="Map showing Kwasa Damansara, Selangor",
                 bbox="101.5520%2C3.1580%2C101.5920%2C3.1860",
                 marker="3.1720%2C101.5720"),
        title="Rumah Mampu Milik, Kwasa Damansara &mdash; A2Z Properties",
        ogtitle="Rumah Mampu Milik &mdash; affordable housing at Kwasa Damansara",
        desc="Rumah Mampu Milik, Kwasa Damansara, Selangor. 2 bedrooms, 1 bathroom, "
             "550 sq ft, from RM2xx,xxx. Affordable housing in the transit corridor.",
    ),
    dict(
        slug="property-seiras.html",
        eyebrow="New project",
        name="Seiras",
        place="Batu Kawan, Penang",
        lede=None,
        specs=[("Project", "Seiras"), ("Location", "Batu Kawan, Penang"),
               ("Bedrooms", "3"), ("Bathrooms", "3"), ("Built-up", "1,033 sq ft"),
               ("Price from", "RM5xxK"), ("Status", "New project launch")],
        list_head=None,
        items=None,
        gallery=[("seiras-card-900", 900, 675, "seiras-card-900",
                  "Landscaped pool deck below a modern residential tower")],
        map=dict(h2="Batu Kawan,<br>mainland Penang",
                 lede="On the mainland beside the second bridge, in the Batu Kawan "
                      "growth corridor.",
                 title="Map showing Batu Kawan, Penang",
                 bbox="100.4200%2C5.2330%2C100.4600%2C5.2610",
                 marker="5.2470%2C100.4400"),
        title="Seiras, Batu Kawan &mdash; Penang new project launch &mdash; A2Z Properties",
        ogtitle="Seiras &mdash; 3-bedroom homes at Batu Kawan, Penang",
        desc="Seiras, Batu Kawan, Penang. 3 bedrooms, 3 bathrooms, 1,033 sq ft, "
             "from RM5xxK. Speak to Keerthana for the full price list.",
    ),
    dict(
        slug="property-terrace-batu-kawan.html",
        eyebrow="New project",
        name="2 Storey Terrace",
        place="Batu Kawan, Penang",
        lede=None,
        specs=[("Project", "2 Storey Terrace"), ("Location", "Batu Kawan, Penang"),
               ("Bedrooms", "4"), ("Bathrooms", "3"),
               ("Built-up", "1,739 &ndash; 1,912 sq ft"),
               ("Price from", "RM7xxK"), ("Status", "New project launch")],
        list_head=None,
        items=None,
        gallery=[("listing-terrace-1200", 1200, 900, "listing-terrace-1200",
                  "Two-storey house with a timber facade and covered entrance")],
        map=dict(h2="Batu Kawan,<br>mainland Penang",
                 lede="On the mainland beside the second bridge, in the Batu Kawan "
                      "growth corridor.",
                 title="Map showing Batu Kawan, Penang",
                 bbox="100.4200%2C5.2330%2C100.4600%2C5.2610",
                 marker="5.2470%2C100.4400"),
        title="2 Storey Terrace, Batu Kawan &mdash; A2Z Properties",
        ogtitle="2 Storey Terrace &mdash; 4-bedroom homes at Batu Kawan, Penang",
        desc="2 Storey Terrace, Batu Kawan, Penang. 4 bedrooms, 3 bathrooms, "
             "1,739 to 1,912 sq ft, from RM7xxK.",
    ),
    dict(
        slug="property-waterfront-andaman.html",
        eyebrow="New project",
        name="Waterfront",
        place="Andaman Island, Penang",
        lede=None,
        specs=[("Project", "Waterfront"), ("Location", "Andaman Island, Penang"),
               ("Bedrooms", "2"), ("Bathrooms", "2"), ("Built-up", "936 sq ft"),
               ("Price from", "RM7xxK"), ("Status", "New project launch")],
        list_head=None,
        items=None,
        gallery=[("listing-waterfront-1200", 1200, 900, "listing-waterfront-1200",
                  "Modern apartment building overlooking the sea")],
        # No map. "Andaman Island, Penang" is not a locality that can be placed
        # with confidence, and a marker in the wrong bay is worse than none.
        map=None,
        title="Waterfront, Andaman Island &mdash; Penang &mdash; A2Z Properties",
        ogtitle="Waterfront &mdash; 2-bedroom seafront homes in Penang",
        desc="Waterfront, Andaman Island, Penang. 2 bedrooms, 2 bathrooms, "
             "936 sq ft, from RM7xxK.",
    ),
    dict(
        slug="property-ferringhi-hills.html",
        eyebrow="New project",
        name="Ferringhi Hills",
        place="Batu Ferringhi, Penang",
        lede=None,
        specs=[("Project", "Ferringhi Hills"), ("Location", "Batu Ferringhi, Penang"),
               ("Bedrooms", "4 + home studio"), ("Bathrooms", "5"),
               ("Built-up", "1,050 sq ft"),
               ("Price from", "RM1.3M"), ("Status", "New project launch")],
        list_head=None,
        items=None,
        gallery=[("listing-ferringhi-1200", 1200, 900, "listing-ferringhi-1200",
                  "Contemporary white house set into a green hillside")],
        map=dict(h2="Batu Ferringhi,<br>Penang island",
                 lede="On the island's north coast, along the Batu Ferringhi beach "
                      "strip.",
                 title="Map showing Batu Ferringhi, Penang",
                 bbox="100.2270%2C5.4590%2C100.2670%2C5.4870",
                 marker="5.4730%2C100.2470"),
        title="Ferringhi Hills, Batu Ferringhi &mdash; A2Z Properties",
        ogtitle="Ferringhi Hills &mdash; hillside homes at Batu Ferringhi, Penang",
        desc="Ferringhi Hills, Batu Ferringhi, Penang. 4 bedrooms plus a home studio, "
             "5 bathrooms, 1,050 sq ft, RM1.3M.",
    ),
]

# slug per listing base image, so the cards can be wired to the right page
SLUG_BY_IMAGE = {g[0].rsplit("-", 1)[0] if g[0].startswith("listing-") else g[0]: d["slug"]
                 for d in DETAILS for g in d["gallery"][:1]}


def _intro(cfg):
    """Eyebrow, project name, and a description only where there is copy."""
    lede = ('        <p class="lede" data-reveal>%s</p>\n' % cfg["lede"]) if cfg["lede"] else ""
    return """  <section class="section page-intro">
    <div class="container">
      <div class="page-intro__head">
        <span class="eyebrow" data-reveal>%s%s</span>
        <h1 data-reveal>%s</h1>
%s      </div>
    </div>
  </section>
""" % (GLYPH, cfg["eyebrow"], cfg["name"], lede)


def _gallery(cfg):
    """One photo means one photo — the grid only splits when there are two."""
    shots = cfg["gallery"]
    mod = " pd-gallery--pair" if len(shots) > 1 else " pd-gallery--single"
    items = []
    for i, (src, w, h, full, alt) in enumerate(shots):
        variant = ""
        if len(shots) > 1:
            variant = " pd-gallery__item--lead" if i == 0 else " pd-gallery__item--poster"
        items.append(
            """        <button class="pd-gallery__item%s" type="button" data-lightbox
                data-full="assets/img/%s.webp"
                data-alt="%s">
          <img src="assets/img/%s.webp" width="%d" height="%d"
               alt="%s"
               loading="lazy" decoding="async">
        </button>""" % (variant, full, alt, src, w, h, alt))
    return """  <section class="section pd-gallery-sec">
    <div class="container">
      <div class="pd-gallery%s">
%s
      </div>
    </div>
  </section>
""" % (mod, "\n".join(items))


def _map(cfg):
    m = cfg["map"]
    if not m:
        return ""
    return """
  <section class="section pd-map-sec">
    <div class="container">
      <div class="split-head">
        <div class="split-head__left">
          <span class="eyebrow" data-reveal>%sWhere it sits</span>
          <h2 data-reveal>%s</h2>
        </div>
        <div class="split-head__right">
          <p class="lede" data-reveal>%s</p>
        </div>
      </div>
      <div class="map-frame" data-reveal>
        <iframe title="%s"
                src="https://www.openstreetmap.org/export/embed.html?bbox=%s&amp;layer=mapnik&amp;marker=%s"
                loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </section>
""" % (GLYPH, m["h2"], m["lede"], m["title"], m["bbox"], m["marker"])


LIGHTBOX = """
  <div class="lightbox" data-lightbox-dialog hidden>
    <button class="lightbox__close" type="button" data-lightbox-close aria-label="Close image">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
    </button>
    <img alt="" data-lightbox-img>
  </div>
"""


def _body(cfg):
    rows = "\n".join('          <div class="spec"><dt>%s</dt><dd>%s</dd></div>' % (k, v)
                     for k, v in cfg["specs"])
    extra = ""
    if cfg["items"]:
        extra = """

        <h3 class="pd-subhead" data-reveal>%s</h3>
        <ul class="feature__list" data-reveal>
%s
        </ul>""" % (cfg["list_head"],
                    "\n".join("          <li>%s</li>" % i for i in cfg["items"]))

    return """
  <section class="section pd-detail">
    <div class="container pd-detail__grid">

      <div class="pd-detail__main">
        <span class="eyebrow" data-reveal>%sThe particulars</span>
        <h2 data-reveal>What the developer<br>has confirmed</h2>
        <p class="lede" data-reveal>
          Only what has been released so far. Unit layouts, bumiputera allocation and
          the exact price list follow when the developer opens the book &mdash; ask and
          we will send them the day they land.
        </p>
        <dl class="spec-table" data-reveal>
%s
        </dl>%s
      </div>

      <aside class="pd-agent" data-reveal>
        <div class="pd-agent__head">
          <img src="assets/img/agent-keerthana-700.webp"
             srcset="assets/img/agent-keerthana-500.webp 500w, assets/img/agent-keerthana-700.webp 700w" width="700" height="700"
               alt="Keerthana Murugeswaran, real estate agent at A2Z Properties"
               loading="lazy" decoding="async">
          <div>
            <p class="pd-agent__name">Keerthana Murugeswaran</p>
            <p class="pd-agent__role">A2Z Properties &middot; Penang &amp; Selangor</p>
          </div>
        </div>
        <p class="pd-agent__note">
          Ask me anything about this launch &mdash; pricing, layouts, or whether it
          suits what you are actually after.
        </p>

        <form class="pd-book" data-contact-form novalidate>
          <input type="hidden" name="access_key" value="REPLACE_WITH_WEB3FORMS_KEY">
          <input type="hidden" name="subject" value="Enquiry &mdash; %s">

          <div class="field">
            <label for="bk-name">Your name</label>
            <input id="bk-name" name="name" type="text" required autocomplete="name">
            <p class="field__error" data-error hidden></p>
          </div>

          <div class="field">
            <label for="bk-email">Email</label>
            <input id="bk-email" name="email" type="email" required autocomplete="email">
            <p class="field__error" data-error hidden></p>
          </div>

          <div class="field">
            <label for="bk-phone">Phone</label>
            <input id="bk-phone" name="phone" type="tel" autocomplete="tel">
          </div>

          <button class="btn btn--dark btn--block" type="submit">
            Request details%s
          </button>
          <p class="form__status" data-form-status role="status"></p>
        </form>
      </aside>

    </div>
  </section>
""" % (GLYPH, rows, extra, cfg["name"], ARROW)


def page(cfg):
    return _intro(cfg) + _gallery(cfg) + _body(cfg) + _map(cfg) + LIGHTBOX
