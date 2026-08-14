#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Per-page <main> content for the five inner pages.
Kept apart from build_pages.py so the chrome-stamping logic stays readable.
"""

GLYPH = ('<svg class="eyebrow__glyph" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/>'
         '<circle cx="12" cy="12" r="3.5" fill="currentColor" stroke="none"/></svg>')

ARROW = ('<span class="btn__chip" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" '
         'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" '
         'stroke-linejoin="round"><path d="M7 17 17 7"/><path d="M7 7h10v10"/></svg></span>')


def intro(eyebrow, h1, lede):
    return f"""  <section class="section page-intro">
    <div class="container">
      <div class="page-intro__head">
        <span class="eyebrow" data-reveal>{GLYPH}{eyebrow}</span>
        <h1 data-reveal>{h1}</h1>
        <p class="lede" data-reveal>{lede}</p>
      </div>
    </div>
  </section>
"""


# ===================================================================== detail
GALLERY = [
    ("gallery-01", "Front elevation at dusk with the driveway lit"),
    ("gallery-02", "Living room with sofas facing the garden windows"),
    ("gallery-03", "Reception room with a flower vase beside the armchair"),
    ("gallery-04", "Open-plan living space under sculptural pendants"),
    ("gallery-05", "Double-height living area with a grand chandelier"),
    ("gallery-06", "Bright sitting room off the main hall"),
]

SPECS = [
    ("Property type", "Detached bungalow"),
    ("Tenure", "Freehold"),
    ("Built-up area", "6,400 sq ft"),
    ("Land area", "11,200 sq ft"),
    ("Bedrooms", "6"),
    ("Bathrooms", "7"),
    ("Car parks", "4 covered"),
    ("Completed", "2021"),
    ("Title", "Individual, residential"),
    ("Reference", "HMY-BJ-0119"),
]


def _gallery_items():
    out = []
    for i, (img, alt) in enumerate(GALLERY):
        cls = "pd-gallery__item pd-gallery__item--lead" if i == 0 else "pd-gallery__item"
        out.append(f"""        <button class="{cls}" type="button" data-lightbox
                data-full="assets/img/{img}-1600.webp" data-alt="{alt}">
          <img src="assets/img/{img}-900.webp"
               srcset="assets/img/{img}-500.webp 500w, assets/img/{img}-900.webp 900w"
               sizes="(max-width: 900px) 92vw, 30vw" width="900" height="562"
               alt="{alt}" loading="lazy" decoding="async">
        </button>""")
    return "\n".join(out)


def _spec_rows():
    return "\n".join(
        f"          <div class=\"spec\"><dt>{k}</dt><dd>{v}</dd></div>" for k, v in SPECS)


DETAIL = intro(
    "Property detail",
    "Bukit Jambul<br>Hillside Estate",
    "A six-bedroom detached house on a ridge above Bayan Lepas, finished in 2021 and "
    "held on an individual freehold title. Sixteen minutes to the airport, nine to "
    "Queensbay."
) + f"""
  <!-- ===================== GALLERY ===================== -->
  <section class="section pd-gallery-sec">
    <div class="container">
      <div class="pd-gallery">
{_gallery_items()}
      </div>
    </div>
  </section>

  <!-- ===================== SPECS + AGENT ===================== -->
  <section class="section pd-detail">
    <div class="container pd-detail__grid">

      <div class="pd-detail__main">
        <span class="eyebrow" data-reveal>{GLYPH}The particulars</span>
        <h2 data-reveal>What you are<br>actually buying</h2>
        <p class="lede" data-reveal>
          Every figure below was measured on site by our own team. Where a number
          differs from the developer's brochure, ours is the one we will stand behind
          at the valuation.
        </p>
        <dl class="spec-table" data-reveal>
{_spec_rows()}
        </dl>
      </div>

      <aside class="pd-agent" data-reveal>
        <div class="pd-agent__head">
          <img src="assets/img/agent-01.webp" width="480" height="480"
               alt="Nurul Aisyah Rahim, principal negotiator at Homy"
               loading="lazy" decoding="async">
          <div>
            <p class="pd-agent__name">Nurul Aisyah Rahim</p>
            <p class="pd-agent__role">Principal negotiator &middot; REN 12894</p>
          </div>
        </div>
        <p class="pd-agent__note">
          I have walked this house four times and will meet you there. Ask me anything
          before you book — including what I would change about it.
        </p>

        <form class="pd-book" data-contact-form novalidate>
          <input type="hidden" name="access_key" value="REPLACE_WITH_WEB3FORMS_KEY">
          <input type="hidden" name="subject" value="Viewing request — Bukit Jambul Hillside Estate">

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
            <label for="bk-date">Preferred date</label>
            <input id="bk-date" name="date" type="date" required>
            <p class="field__error" data-error hidden></p>
          </div>

          <button class="btn btn--dark btn--block" type="submit">
            Book a viewing{ARROW}
          </button>
          <p class="form__status" data-form-status role="status"></p>
        </form>
      </aside>

    </div>
  </section>

  <!-- ===================== MAP ===================== -->
  <section class="section pd-map-sec">
    <div class="container">
      <div class="split-head">
        <div class="split-head__left">
          <span class="eyebrow" data-reveal>{GLYPH}Where it sits</span>
          <h2 data-reveal>Jalan Bukit Jambul,<br>11900 Bayan Lepas</h2>
        </div>
        <div class="split-head__right">
          <p class="lede" data-reveal>
            On the quiet side of the ridge, five minutes off the Tun Dr Lim Chong Eu
            expressway and walking distance from Bukit Jambul Country Club.
          </p>
        </div>
      </div>
      <div class="map-frame" data-reveal>
        <iframe title="Map showing Jalan Bukit Jambul, Bayan Lepas, Penang"
                src="https://www.openstreetmap.org/export/embed.html?bbox=100.2730%2C5.3270%2C100.2930%2C5.3430&amp;layer=mapnik&amp;marker=5.3350%2C100.2830"
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
"""


# =================================================================== services
OFFERINGS = [
    ("svc-buy", "01", "Buy",
     "Buy with your eyes open",
     "Title search, structural walkthrough and a written valuation land in your inbox "
     "before you sign anything. If the strata title is in dispute or the building has a "
     "sinking-fund problem, you will hear it from us first.",
     ["Independent written valuation", "Title and encumbrance search",
      "Structural walkthrough with photos", "Negotiation handled end to end"],
     "Couple celebrating in front of a sold sign at their new house"),
    ("svc-rent", "02", "Rent",
     "Rent without the runaround",
     "Tenancy drafted by our own panel, deposit held in a client account, and a handover "
     "documented room by room so the exit inspection is a formality rather than an argument.",
     ["Tenancy agreement drafted and stamped", "Deposit held in trust",
      "Room-by-room handover record", "Tenant screening and reference checks"],
     "Modern luxury villa with a lit pool at twilight"),
    ("svc-manage", "03", "Manage",
     "Hand us the keys",
     "Rent collection, repairs and annual compliance handled quietly. You get one "
     "statement a month and a call only when something genuinely needs your decision.",
     ["Monthly rent collection and statement", "Vetted contractors for repairs",
      "Assessment and quit rent handled", "Annual condition report"],
     "Spacious living room with chandeliers and a plush sofa"),
    ("svc-valuation", "04", "Valuation",
     "Know what it is worth",
     "A defensible market valuation for financing, probate or a family settlement — "
     "built from completed transactions in the same scheme, not from asking prices.",
     ["Based on completed transactions", "Comparables listed in full",
      "Accepted by the major local banks", "Turnaround in five working days"],
     "Architectural scale model of a modern house"),
]


def _offering(o, i):
    img, num, label, title, body, points, alt = o
    flip = " feature--flip" if i % 2 else ""
    items = "\n".join(f"            <li>{p}</li>" for p in points)
    return f"""      <article class="feature{flip}" data-reveal>
        <div class="feature__media">
          <img src="assets/img/{img}-1200.webp"
               srcset="assets/img/{img}-700.webp 700w, assets/img/{img}-1200.webp 1200w"
               sizes="(max-width: 900px) 92vw, 46vw" width="1200" height="900"
               alt="{alt}" loading="lazy" decoding="async">
        </div>
        <div class="feature__text">
          <p class="feature__label"><span class="feature__num">.{num}</span> {label}</p>
          <h2>{title}</h2>
          <p class="lede">{body}</p>
          <ul class="feature__list">
{items}
          </ul>
        </div>
      </article>"""


SERVICES = intro(
    "Our services",
    "Four things we do,<br>and nothing else",
    "We are a small agency working four markets. That means we say no to instructions "
    "outside Penang, Ipoh, Langkawi and Alor Setar — and that the person who lists your "
    "home is the person who shows it."
) + """
  <section class="section features">
    <div class="container features__stack">
""" + "\n\n".join(_offering(o, i) for i, o in enumerate(OFFERINGS)) + """
    </div>
  </section>
"""


# ====================================================================== about
VALUES = [
    ("Fewer listings, known properly",
     "We cap the book at around forty homes. If we cannot walk it in a morning, we "
     "cannot describe it honestly."),
    ("The negotiator who lists it, shows it",
     "No handing you to a junior on the day. The person who measured the rooms is the "
     "person standing in them with you."),
    ("Numbers we will defend",
     "Every valuation cites the completed transactions behind it. Ask for the "
     "comparables and you get them."),
    ("We will talk you out of it",
     "Four times last year we advised a client not to buy. Two of them bought "
     "something else through us later."),
]

TEAM = [
    ("team-01", "Nurul Aisyah Rahim", "Principal &middot; REN 12894"),
    ("team-02", "Tan Wei Jien", "Senior negotiator &middot; Penang"),
    ("team-03", "Priya Maniam", "Negotiator &middot; Ipoh"),
    ("team-04", "Hafiz Abdullah", "Negotiator &middot; Langkawi"),
    ("team-05", "Lim Sook Mun", "Property management"),
    ("team-06", "Ravi Chandran", "Valuation lead"),
]


def _values():
    return "\n".join(
        f"""        <article class="value-card" data-reveal>
          <h3>{t}</h3>
          <p class="lede">{b}</p>
        </article>""" for t, b in VALUES)


def _team():
    return "\n".join(
        f"""        <figure class="team-card" data-reveal>
          <img src="assets/img/{img}.webp" width="480" height="480"
               alt="{name}, {role.replace('&middot;', '-')}" loading="lazy" decoding="async">
          <figcaption>
            <p class="team-card__name">{name}</p>
            <p class="team-card__role">{role}</p>
          </figcaption>
        </figure>""" for img, name, role in TEAM)


ABOUT = intro(
    "About Homy",
    "Twelve years in four<br>Malaysian markets",
    "Homy started in a shophouse on Lebuh Farquhar in 2014 with one negotiator and a "
    "borrowed camera. We still work the same four markets, and we still photograph "
    "every home ourselves."
) + f"""
  <!-- ===================== STORY ===================== -->
  <section class="section story">
    <div class="container story__grid">
      <div class="story__media" data-reveal>
        <img src="assets/img/about-story-1400.webp"
             srcset="assets/img/about-story-800.webp 800w, assets/img/about-story-1400.webp 1400w"
             sizes="(max-width: 900px) 92vw, 46vw" width="1400" height="1000"
             alt="Contemporary home with panoramic glazing opening to a green lawn"
             loading="lazy" decoding="async">
      </div>
      <div class="story__text">
        <span class="eyebrow" data-reveal>{GLYPH}How we got here</span>
        <h2 data-reveal>We grew slowly<br>and on purpose</h2>
        <p class="lede" data-reveal>
          The agency turned down franchise offers twice because both would have meant
          carrying three hundred listings we had never visited. Instead we added one
          market at a time — Ipoh in 2017, Langkawi in 2019, Alor Setar in 2022 — and
          only once someone on the team actually lived there.
        </p>
        <p class="lede" data-reveal>
          Today there are eleven of us. Six are licensed negotiators, two handle
          management, one does valuations, and two keep the photography and paperwork
          moving. That is the whole company.
        </p>
      </div>
    </div>
  </section>

  <!-- ===================== VALUES ===================== -->
  <section class="section values-sec">
    <div class="container">
      <div class="split-head">
        <div class="split-head__left">
          <span class="eyebrow" data-reveal>{GLYPH}How we work</span>
          <h2 data-reveal>Four rules we have<br>never broken</h2>
        </div>
        <div class="split-head__right">
          <p class="lede" data-reveal>
            They cost us instructions every year. We have kept them anyway, because
            they are the reason clients come back.
          </p>
        </div>
      </div>
      <div class="values__grid">
{_values()}
      </div>
    </div>
  </section>

  <!-- ===================== TEAM ===================== -->
  <section class="section team-sec">
    <div class="container">
      <div class="split-head">
        <div class="split-head__left">
          <span class="eyebrow" data-reveal>{GLYPH}The team</span>
          <h2 data-reveal>Eleven people,<br>four markets</h2>
        </div>
        <div class="split-head__right">
          <p class="lede" data-reveal>
            Every negotiator below is registered with the Board of Valuers, Appraisers,
            Estate Agents and Property Managers.
          </p>
        </div>
      </div>
      <div class="team__grid">
{_team()}
      </div>
    </div>
  </section>

  <!-- ===================== STAT BAND ===================== -->
  <section class="section statband">
    <img class="statband__bg" src="assets/img/about-band-1800.webp"
         srcset="assets/img/about-band-1000.webp 1000w, assets/img/about-band-1800.webp 1800w"
         sizes="100vw" width="1800" height="900"
         alt="Couple carrying boxes and plants into their new home"
         loading="lazy" decoding="async">
    <div class="container statband__inner">
      <div class="statband__item" data-reveal>
        <span class="statband__num" data-count="3500" data-count-suffix="+">3,500+</span>
        <span class="statband__label">Homes sold</span>
      </div>
      <div class="statband__item" data-reveal>
        <span class="statband__num" data-count="1.24" data-count-decimals="2" data-count-prefix="RM " data-count-suffix="B">RM 1.24B</span>
        <span class="statband__label">Total value</span>
      </div>
      <div class="statband__item" data-reveal>
        <span class="statband__num" data-count="4.9" data-count-decimals="1" data-count-suffix="/5">4.9/5</span>
        <span class="statband__label">Client rating</span>
      </div>
    </div>
  </section>
"""


# ==================================================================== contact
CONTACT = intro(
    "Contact",
    "Tell us the postcode<br>and the budget",
    "We reply to everything within one working day. If you would rather talk it through, "
    "the office line is answered by a negotiator, not a switchboard."
) + f"""
  <section class="section contact-sec">
    <div class="container contact__grid">

      <form class="contact-form" data-contact-form novalidate>
        <input type="hidden" name="access_key" value="REPLACE_WITH_WEB3FORMS_KEY">
        <input type="hidden" name="subject" value="Enquiry from homy.com.my">

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
            <option>Ipoh</option>
            <option>Langkawi</option>
            <option>Alor Setar</option>
            <option>Not sure yet</option>
          </select>
        </div>

        <div class="field">
          <label for="c-msg">What are you after?</label>
          <textarea id="c-msg" name="message" required
                    placeholder="Three bedrooms near a decent primary school, up to RM900k."></textarea>
          <p class="field__error" data-error hidden></p>
        </div>

        <button class="btn btn--dark" type="submit">Send enquiry{ARROW}</button>
        <p class="form__status" data-form-status role="status"></p>
      </form>

      <aside class="contact-side">
        <img class="contact-side__img" src="assets/img/contact-agent-900.webp"
             srcset="assets/img/contact-agent-600.webp 600w, assets/img/contact-agent-900.webp 900w"
             sizes="(max-width: 900px) 92vw, 30vw" width="900" height="1200"
             alt="Homy negotiator with a clipboard in the George Town office"
             loading="lazy" decoding="async">

        <div class="contact-side__block">
          <h2>Office</h2>
          <p class="lede">18 Lebuh Farquhar<br>10200 George Town<br>Pulau Pinang</p>
          <p class="lede">Monday to Friday, 9am&ndash;6pm<br>Saturday viewings by appointment</p>
        </div>

        <div class="contact-side__block">
          <h2>Direct</h2>
          <ul class="footer-list footer-list--icons contact-links">
            <li><a href="tel:+60187814127">+601 8781 4127</a></li>
            <li><a href="mailto:darwindhas1799@gmail.com">darwindhas1799@gmail.com</a></li>
            <li><a href="https://wa.me/60187814127" rel="noopener">WhatsApp us</a></li>
          </ul>
        </div>
      </aside>

    </div>
  </section>

  <section class="section contact-map">
    <div class="container">
      <div class="map-frame" data-reveal>
        <iframe title="Map showing the Homy office on Lebuh Farquhar, George Town"
                src="https://www.openstreetmap.org/export/embed.html?bbox=100.3300%2C5.4100%2C100.3500%2C5.4280&amp;layer=mapnik&amp;marker=5.4190%2C100.3400"
                loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>
    </div>
  </section>
"""


# ======================================================================== 404
NOTFOUND = f"""  <section class="section notfound">
    <img class="notfound__bg" src="assets/img/notfound-1600.webp"
         srcset="assets/img/notfound-900.webp 900w, assets/img/notfound-1600.webp 1600w"
         sizes="100vw" width="1600" height="900"
         alt="Minimalist cube house standing alone at sunset" loading="eager" decoding="async">
    <div class="container notfound__inner">
      <p class="notfound__num" data-reveal>404</p>
      <h1 data-reveal>This one is<br>off the market</h1>
      <p class="lede" data-reveal>
        The page you were after has moved or never existed. The listings below are all
        still standing.
      </p>
      <div class="notfound__ctas" data-reveal>
        <a class="btn btn--dark" href="index.html">Back to home{ARROW}</a>
        <a class="btn btn--ghost" href="properties.html">Browse listings</a>
      </div>
    </div>
  </section>
"""
