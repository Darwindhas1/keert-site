#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-page <main> content for A2Z Properties.

Everything here is client-supplied or derived from client-supplied copy.
Nothing is invented — no transaction counts, no ratings, no awards, no
testimonials, no team beyond the one named agent.
"""

GLYPH = ('<svg class="eyebrow__glyph" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/>'
         '<circle cx="12" cy="12" r="3.5" fill="currentColor" stroke="none"/></svg>')

ARROW = ('<span class="btn__chip" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" '
         'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
         'stroke-linejoin="round"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg></span>')

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
SPARK = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M12 3v4"/><path d="M12 17v4"/><path d="M3 12h4"/><path d="M17 12h4"/>'
         '<path d="m6 6 2.5 2.5"/><path d="m15.5 15.5 2.5 2.5"/>'
         '<path d="m18 6-2.5 2.5"/><path d="m8.5 15.5-2.5 2.5"/></svg>')
HOUSE = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22v-9h6v9"/></svg>')


def intro(eyebrow, h1, lede):
    return """  <section class="section page-intro">
    <div class="container">
      <div class="page-intro__head">
        <span class="eyebrow" data-reveal>%s%s</span>
        <h1 data-reveal>%s</h1>
        <p class="lede" data-reveal>%s</p>
      </div>
    </div>
  </section>
""" % (GLYPH, eyebrow, h1, lede)


# ================================================================= listings
# name, area, state key, price, image base, widths, alt, meta, bullets
LISTINGS = [
    ("Seberang Jaya", "Seberang Jaya, Penang", "penang", "From RM3xx,xxx",
     "seberang-jaya-card", [500, 700],
     "High-rise towers and landscaped pool deck at Seberang Jaya",
     None, ["3 min to Sunway Mall", "10 min to Penang 1st Bridge"]),
    ("Gelugor", "Gelugor, Penang", "penang", "RM8xx,xxx &ndash; RM1.x Million",
     "gelugor-card", [500, 700],
     "Luxury high-rise condominium beside Penang Bridge at sunset",
     None, ["Future LRT station opposite", "Infinity pool &amp; sky facilities"]),
    ("Rumah Mampu Milik", "Kwasa Damansara, Selangor", "selangor", "RM2xx,xxx",
     "listing-mampu", [500, 700, 1200],
     "Contemporary apartment block with balconies and glazed facade",
     [("2 beds", BED), ("1 bath", BATH), ("550 sq ft", AREA)], None),
    ("Seiras", "Batu Kawan, Penang", "penang", "RM5xxK",
     "seiras-card", [500, 700, 1200],
     "Landscaped pool deck below a modern residential tower",
     [("3 beds", BED), ("3 baths", BATH), ("1,033 sq ft", AREA)], None),
    ("2 Storey Terrace", "Batu Kawan, Penang", "penang", "RM7xxK",
     "listing-terrace", [500, 700, 1200],
     "Two-storey house with a timber facade and covered entrance",
     [("4 beds", BED), ("3 baths", BATH), ("1,739 / 1,912 sq ft", AREA)], None),
    ("Waterfront", "Andaman Island, Penang", "penang", "RM7xxK",
     "listing-waterfront", [500, 700, 800, 1200],
     "Modern apartment building overlooking the sea",
     [("2 beds", BED), ("2 baths", BATH), ("936 sq ft", AREA)], None),
    ("Ferringhi Hills", "Batu Ferringhi, Penang", "penang", "RM1.3M",
     "listing-ferringhi", [500, 700, 1200],
     "Contemporary white house set into a green hillside",
     [("4 beds + studio", BED), ("5 baths", BATH), ("1,050 sq ft", AREA)], None),
]


def _srcset(base, widths):
    return ", ".join("assets/img/%s-%d.webp %dw" % (base, w, w) for w in widths)


def card_place(name, area):
    """Project name plus where it is, without repeating the name.

    Several projects are named after the town they sit in, so the naive
    "name, area" join produced "Seberang Jaya, Seberang Jaya, Penang". Drop
    any leading area segment that simply restates the project name.
    """
    parts = [p.strip() for p in area.split(",") if p.strip()]
    while parts and parts[0].casefold() == name.strip().casefold():
        parts.pop(0)
    return ", ".join([name] + parts)


def listing_card(row, hidden=False, sizes="(max-width: 640px) 60vw, (max-width: 900px) 92vw, 31vw"):
    name, area, state, price, base, widths, alt, meta, bullets = row
    big = max(widths)
    if meta:
        items = "\n".join("                    <li>%s%s</li>" % (i, t) for t, i in meta)
    else:
        items = "\n".join("                    <li>%s%s</li>" % (SPARK, b) for b in bullets)
    return """          <a class="card-img" href="property-detail.html" data-card
             data-type="new" data-loc="%s"%s>
            <img class="card-img__media" src="assets/img/%s-%d.webp"
                 srcset="%s"
                 sizes="%s" width="%d" height="%d"
                 alt="%s" loading="lazy" decoding="async">
            <span class="badge badge--glass card-img__status">%sNew Project</span>
            <div class="card-img__body">
              <p class="card-img__name">%s</p>
              <div class="card-img__foot">
                <div>
                  <p class="card-img__price">%s</p>
                  <ul class="meta-row">
%s
                  </ul>
                </div>
              </div>
            </div>
          </a>""" % (state, " hidden" if hidden else "", base, big,
                     _srcset(base, widths), sizes, big, round(big * 0.75),
                     alt, HOUSE, card_place(name, area), price, items)


CHIPS = [("all", "All"), ("penang", "Penang"), ("selangor", "Selangor")]

_chips = "\n".join(
    '          <button class="chip%s" type="button" data-filter="%s" '
    'aria-pressed="%s">%s</button>'
    % (" is-on" if v == "all" else "", v, "true" if v == "all" else "false", t)
    for v, t in CHIPS)

_cards = "\n".join(listing_card(r, i >= 6) for i, r in enumerate(LISTINGS))

PROPERTIES = intro(
    "Property listings",
    "New project launches<br>in Penang and Selangor",
    "Every listing below is a current new project launch. Prices are indicative "
    "until the developer opens the book &mdash; ask and we will tell you where a "
    "unit actually lands."
) + """
  <section class="section props">
    <div class="container">

      <div class="filters" role="group" aria-label="Filter listings" data-reveal>
%s
      </div>

      <p class="filters__count" data-count-out role="status">Showing 6 of 7 projects</p>

      <div class="props__grid" data-grid>
%s
      </div>

      <div class="props__more">
        <button class="btn btn--ghost" type="button" data-load-more>
          Load more projects
          <span class="btn__chip" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14"/><path d="m19 12-7 7-7-7"/></svg>
          </span>
        </button>
        <p class="props__empty" data-empty hidden>No projects in that area right now.</p>
      </div>

    </div>
  </section>
""" % (_chips, _cards)


# =========================================================== property detail
SPECS = [
    ("Project", "Seberang Jaya"),
    ("Location", "Seberang Jaya, Penang"),
    ("Tenure", "Freehold"),
    ("Construction", "PPVC technology"),
    ("Price from", "RM3xx,xxx"),
    ("Status", "New project launch"),
]

_spec_rows = "\n".join(
    '          <div class="spec"><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in SPECS)

DETAIL = intro(
    "New project",
    "Seberang Jaya",
    "Penang's largest affordable housing development. Freehold, built with PPVC "
    "technology, and within ten minutes of the first bridge and Penang Sentral."
) + """
  <section class="section pd-gallery-sec">
    <div class="container">
      <div class="pd-gallery pd-gallery--pair">
        <button class="pd-gallery__item pd-gallery__item--lead" type="button" data-lightbox
                data-full="assets/img/seberang-jaya-card-700.webp"
                data-alt="High-rise towers and landscaped pool deck at Seberang Jaya">
          <img src="assets/img/seberang-jaya-card-700.webp" width="700" height="525"
               alt="High-rise towers and landscaped pool deck at Seberang Jaya"
               loading="lazy" decoding="async">
        </button>
        <button class="pd-gallery__item pd-gallery__item--poster" type="button" data-lightbox
                data-full="assets/img/seberang-jaya-poster-900.webp"
                data-alt="Seberang Jaya project poster with pricing and travel times">
          <img src="assets/img/seberang-jaya-poster-700.webp" width="700" height="1050"
               alt="Seberang Jaya project poster with pricing and travel times"
               loading="lazy" decoding="async">
        </button>
      </div>
    </div>
  </section>

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
        </dl>

        <h3 class="pd-subhead" data-reveal>Getting around</h3>
        <ul class="feature__list" data-reveal>
          <li>3 minutes to Sunway Mall and Sunway Hospital</li>
          <li>5 minutes to the beach</li>
          <li>10 minutes to Penang 1st Bridge</li>
          <li>10 minutes to Penang Sentral</li>
        </ul>
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
          <input type="hidden" name="subject" value="Enquiry — Seberang Jaya">

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

  <section class="section pd-map-sec">
    <div class="container">
      <div class="split-head">
        <div class="split-head__left">
          <span class="eyebrow" data-reveal>%sWhere it sits</span>
          <h2 data-reveal>Seberang Jaya,<br>mainland Penang</h2>
        </div>
        <div class="split-head__right">
          <p class="lede" data-reveal>
            On the mainland side, minutes from Sunway Carnival and within a short
            drive of both the first bridge and Penang Sentral.
          </p>
        </div>
      </div>
      <div class="map-frame" data-reveal>
        <iframe title="Map showing Seberang Jaya, Penang"
                src="https://www.openstreetmap.org/export/embed.html?bbox=100.3720%%2C5.3800%%2C100.4120%%2C5.4080&amp;layer=mapnik&amp;marker=5.3940%%2C100.3920"
                loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </section>

  <div class="lightbox" data-lightbox-dialog hidden>
    <button class="lightbox__close" type="button" data-lightbox-close aria-label="Close image">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
    </button>
    <img alt="" data-lightbox-img>
  </div>
""" % (GLYPH, _spec_rows, ARROW, GLYPH)


# ================================================================== services
OFFERINGS = [
    ("svc-buy", "01", "Buying",
     "Find the right one, not just an available one",
     "New project launches across Penang and Selangor, matched to what you actually "
     "need the place to do &mdash; the commute, the schools, the budget you are "
     "comfortable with rather than the one you could stretch to.",
     "Couple celebrating in front of a sold sign at their new house"),
    ("listing-waterfront", "02", "Selling",
     "Priced on what the market will pay",
     "An honest read on where your unit sits against current launches in the same "
     "corridor, and what it will realistically fetch &mdash; before it goes on the "
     "market, not after three months of silence.",
     "Modern apartment building overlooking the sea"),
    ("svc-manage", "03", "Investing",
     "Yield you can actually bank on",
     "Which corridors are absorbing supply and which are not, what a unit rents for "
     "today rather than in a projection, and what the holding costs really come to.",
     "Spacious living room with chandeliers and a plush sofa"),
    ("listing-mampu", "04", "New launches",
     "Direct developer access",
     "Units straight from the developer at launch pricing, with the paperwork and the "
     "booking sequence handled so you are not chasing a sales gallery for updates.",
     "Contemporary apartment block with balconies and glazed facade"),
]


def _offering(o, i):
    img, num, label, title, body, alt = o
    flip = " feature--flip" if i % 2 else ""
    return """      <article class="feature%s" data-reveal>
        <div class="feature__media">
          <img src="assets/img/%s-1200.webp"
               srcset="assets/img/%s-700.webp 700w, assets/img/%s-800.webp 800w, assets/img/%s-1200.webp 1200w"
               sizes="(max-width: 900px) 92vw, 46vw" width="1200" height="900"
               alt="%s" loading="lazy" decoding="async">
        </div>
        <div class="feature__text">
          <p class="feature__label"><span class="feature__num">.%s</span> %s</p>
          <h2>%s</h2>
          <p class="lede">%s</p>
        </div>
      </article>""" % (flip, img, img, img, img, alt, num, label, title, body)


SERVICES = intro(
    "Our services",
    "Buying, selling<br>and investing",
    "A2Z Properties works new project launches across Penang and Selangor. One agent "
    "from the first enquiry through to the keys."
) + """
  <!-- ==========================================================================
       PLACEHOLDER — AWAITING CLIENT INPUT

       The four offerings below were written from the only service wording the
       client has supplied so far ("whether you're buying, selling, or
       investing"). The categories, the headings and the descriptions are all
       provisional. Nothing here has been confirmed by Keerthana.

       Replace once the real service list is available, and check whether A2Z
       also offers property management, valuations or loan referral.
       ========================================================================== -->
  <section class="section features">
    <div class="container features__stack">
%s
    </div>
  </section>
""" % ("\n\n".join(_offering(o, i) for i, o in enumerate(OFFERINGS)))


# ===================================================================== about
ABOUT = intro(
    "About A2Z Properties",
    "Your local agent in<br>Penang and Selangor",
    "A2Z Properties focuses on new project launches in two states, with direct "
    "developer access and one point of contact throughout."
) + """
  <section class="section story">
    <div class="container story__grid">
      <div class="story__media" data-reveal>
        <img src="assets/img/agent-keerthana-700.webp"
             srcset="assets/img/agent-keerthana-500.webp 500w, assets/img/agent-keerthana-700.webp 700w" width="700" height="700"
             alt="Keerthana Murugeswaran, real estate agent at A2Z Properties"
             loading="lazy" decoding="async">
      </div>
      <div class="story__text">
        <span class="eyebrow" data-reveal>%sYour agent</span>
        <h2 data-reveal>Keerthana<br>Murugeswaran</h2>
        <p class="lede" data-reveal>
          Hi, I'm Keerthana, your local real estate expert in Penang and Selangor.
          I'm passionate about helping clients find their dream home or achieve their
          investment goals.
        </p>
        <p class="lede" data-reveal>
          Whether you're buying, selling, or investing, my commitment to personalised
          service and market knowledge ensures a smooth and successful real estate
          journey. I'm not just an agent, I'm a trusted advisor, and I'm eager to help
          you navigate the local market with confidence.
        </p>
        <div class="agent__ctas" data-reveal>
          <a class="btn btn--dark btn--sm" href="https://wa.me/60143315253" rel="noopener">
            WhatsApp Keerthana%s
          </a>
          <a class="btn btn--ghost btn--sm" href="tel:+60143315253">014 331 5253</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section why">
    <div class="container">
      <div class="split-head">
        <div class="split-head__left">
          <span class="eyebrow" data-reveal>%sWhy A2Z</span>
          <h2 data-reveal>What you get<br>working with us</h2>
        </div>
        <div class="split-head__right">
          <p class="lede" data-reveal>
            A small operation covering two states properly, rather than a big one
            covering the whole country badly.
          </p>
        </div>
      </div>

      <div class="why__grid">
        <article class="why-card" data-reveal>
          <span class="why-card__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg></span>
          <h3>Local knowledge</h3>
          <p class="lede">Penang and Selangor corridors, tracked launch by launch.</p>
        </article>
        <article class="why-card" data-reveal>
          <span class="why-card__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 21V8l6-4 6 4v13"/><path d="M15 21V11l6 3v7"/><path d="M7 21v-5h4v5"/></svg></span>
          <h3>Direct developer access</h3>
          <p class="lede">New project units straight from the developer, not resold listings.</p>
        </article>
        <article class="why-card" data-reveal>
          <span class="why-card__icon" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20.6 13.4 12 22l-9-9V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/></svg></span>
          <h3>Honest pricing</h3>
          <p class="lede">What a unit actually costs, including what the brochure leaves out.</p>
        </article>
      </div>
    </div>
  </section>
""" % (GLYPH, ARROW, GLYPH)


# =================================================================== contact
CONTACT = intro(
    "Contact",
    "Tell us what<br>you're looking for",
    "Reach out for a viewing, a valuation, or just to ask what's out there. We reply "
    "within one business day."
) + """
  <section class="section contact-sec">
    <div class="container contact__grid">

      <form class="contact-form" data-contact-form novalidate>
        <input type="hidden" name="access_key" value="REPLACE_WITH_WEB3FORMS_KEY">
        <input type="hidden" name="subject" value="Enquiry from A2Z Properties">

        <div class="field">
          <label for="c-name">Your name</label>
          <input id="c-name" name="name" type="text" required autocomplete="name">
          <p class="field__error" data-error hidden></p>
        </div>

        <div class="field">
          <label for="c-email">Email</label>
          <input id="c-email" name="email" type="email" required autocomplete="email">
          <p class="field__error" data-error hidden></p>
        </div>

        <div class="field">
          <label for="c-phone">Phone</label>
          <input id="c-phone" name="phone" type="tel" autocomplete="tel">
        </div>

        <div class="field">
          <label for="c-area">Where are you looking?</label>
          <select id="c-area" name="area">
            <option>Penang</option>
            <option>Selangor</option>
            <option>Either</option>
          </select>
        </div>

        <div class="field">
          <label for="c-msg">What are you after?</label>
          <textarea id="c-msg" name="message" required
                    placeholder="Two bedrooms near Sunway Carnival, up to RM4xx,xxx."></textarea>
          <p class="field__error" data-error hidden></p>
        </div>

        <button class="btn btn--dark" type="submit">Send enquiry%s</button>
        <p class="form__status" data-form-status role="status"></p>
      </form>

      <aside class="contact-side">
        <img class="contact-side__img" src="assets/img/agent-keerthana-700.webp"
             width="700" height="700"
             alt="Keerthana Murugeswaran, real estate agent at A2Z Properties"
             loading="lazy" decoding="async">

        <div class="contact-side__block">
          <h2>Speak to Keerthana</h2>
          <ul class="footer-list footer-list--icons contact-links">
            <li><a href="tel:+60143315253">014 331 5253</a></li>
            <li><a href="mailto:keer43337@gmail.com">keer43337@gmail.com</a></li>
            <li><a href="https://wa.me/60143315253" rel="noopener">WhatsApp us</a></li>
          </ul>
        </div>

        <div class="contact-side__block">
          <h2>Areas covered</h2>
          <p class="lede">Penang &amp; Selangor, Malaysia</p>
        </div>
      </aside>

    </div>
  </section>
""" % ARROW


# ======================================================================= 404
NOTFOUND = """  <section class="section notfound">
    <img class="notfound__bg" src="assets/img/notfound-1600.webp"
         srcset="assets/img/notfound-800.webp 800w, assets/img/notfound-900.webp 900w, assets/img/notfound-1600.webp 1600w"
         sizes="100vw" width="1600" height="900"
         alt="Minimalist cube house standing alone at sunset" loading="eager" decoding="async">
    <div class="container notfound__inner">
      <p class="notfound__num" data-reveal>404</p>
      <h1 data-reveal>This one is<br>off the market</h1>
      <p class="lede" data-reveal>
        The page you were after has moved or never existed. The current launches are
        all still listed.
      </p>
      <div class="notfound__ctas" data-reveal>
        <a class="btn btn--dark" href="index.html">Back to home%s</a>
        <a class="btn btn--ghost" href="properties.html">Browse listings</a>
      </div>
    </div>
  </section>
""" % ARROW
