# Homy

A seven-page marketing site for **Homy**, a fictional licensed real-estate agency
working four Malaysian markets — Penang, Ipoh, Langkawi and Alor Setar.

Bold, airy, premium-editorial: a monochrome black/white/grey shell with sky blue as
the only atmospheric accent, so all the real colour comes from the photography.
The signature moment is the home-page hero — a cut-out house that rises out of a
bank of cloud and passes in front of the headline as you scroll.

## Pages

| Page | Contents |
|---|---|
| `index.html` | Hero, impact stats, services accordion, listings, featured property, testimonials |
| `properties.html` | Filter chips (type + location), 12 listings, load-more |
| `property-detail.html` | Gallery with lightbox, measured spec table, agent card, booking form, map |
| `services.html` | Buy / Rent / Manage / Valuation, alternating feature splits |
| `about.html` | Story, values, team grid, stat band |
| `contact.html` | Validating enquiry form, office details, map |
| `404.html` | On-brand not-found page |

## Tech stack

Static HTML, CSS and vanilla JavaScript. **No framework and no build step** — the
files in the repo root are exactly what the browser gets.

- **GSAP + ScrollTrigger** (CDN) for the pinned hero and per-section scroll reveals
- Native scroll — no smooth-scroll library
- **Satoshi** (Fontshare) for display, **Inter** (Google Fonts) for body
- Inline SVG icons throughout; no icon font, no emoji
- OpenStreetMap embeds for the two maps

### CSS architecture

| File | Role |
|---|---|
| `assets/css/tokens.css` | Every colour, size, radius and duration. One `:root` block — the single source of truth |
| `assets/css/base.css` | Reset, type scale, layout primitives, accessibility |
| `assets/css/components.css` | Nav, footer, buttons, cards, forms — the shared chrome |
| `assets/css/sections.css` | Home-page section layouts and the section surface rhythm |
| `assets/css/pages.css` | Inner-page layouts |

No hard-coded hex values or raw pixel sizes live outside `tokens.css`.

## Running locally

Any static file server will do. From the project root:

```bash
python -m http.server 4173
```

Then open <http://localhost:4173>. Opening `index.html` straight off disk mostly
works, but a server is needed for the maps and the form endpoints to behave.

## Media

All photography comes from [Pexels](https://www.pexels.com) under the Pexels
licence, and is **downloaded at build time into `assets/img/`** — the live site
makes no API calls and ships no API key. Photographer credits are listed in
[`assets/img/CREDITS.md`](assets/img/CREDITS.md), with per-asset attribution in
`assets/img/credits.json`. Avatar photos come from RandomUser and Pravatar.

To re-pull or add media you need a free Pexels API key:

```bash
cp .env.example .env      # then paste your key into PEXELS_API_KEY
python scripts/fetch_media.py            # all assets
python scripts/fetch_media.py svc-rent   # just one
```

`.env` is gitignored and must stay that way.

## Scripts

Development helpers — none of them run in the browser.

| Script | Purpose |
|---|---|
| `scripts/fetch_media.py` | Download and re-encode Pexels photos as responsive WebP under 250 KB |
| `scripts/build_hero_assets.py` | Cut out and feather the hero house, build the sky and cloud layers |
| `scripts/build_pages.py` | Stamp the nav/CTA/footer from `index.html` into the other pages |
| `scripts/check_chrome.py` | Fail if the shared chrome has drifted between pages |
| `scripts/check_assets.py` | Fail if any `src`/`href` points at a missing file |
| `scripts/perf_profile.py` | Frame pacing and main-thread profile for a hero scroll |

`build_pages.py` is a development convenience, not a runtime build step: it writes
plain static HTML that is committed to the repo.

## Contact forms

The enquiry and booking forms validate in the browser and post to
[Web3Forms](https://web3forms.com). They ship with a placeholder access key and
will say so rather than pretending to send. Paste a real key into the
`access_key` hidden input in `contact.html` and `property-detail.html` to go live.

## Licence

Site code is free to reuse. Photography remains under the
[Pexels licence](https://www.pexels.com/license/).
