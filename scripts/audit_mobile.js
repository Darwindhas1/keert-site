/**
 * Mobile audit: every page at every width.
 *
 * Reports, per page/width:
 *   - horizontal overflow, naming the widest offending elements
 *   - body/label text rendering below the legibility floor
 *   - tap targets under 44x44
 *   - text sitting closer than 20px to the screen edge
 *   - content colliding with the fixed nav
 *
 * Run via browser_run_code_unsafe with filename = scripts/audit_mobile.js
 */
async (page) => {
  const browser = page.context().browser();
  const PAGES = ['index.html', 'properties.html', 'services.html', 'about.html',
                 'contact.html', '404.html',
                 'property-seberang-jaya.html', 'property-gelugor.html',
                 'property-mampu-kwasa.html', 'property-seiras.html',
                 'property-terrace-batu-kawan.html',
                 'property-waterfront-andaman.html', 'property-ferringhi-hills.html'];
  const WIDTHS = [360, 390, 430, 768, 1024];
  const rows = [];

  for (const w of WIDTHS) {
    const ctx = await browser.newContext({
      viewport: { width: w, height: 780 },
      deviceScaleFactor: 2,
      isMobile: w < 768,
      hasTouch: w < 768,
      reducedMotion: 'reduce'
    });
    const p = await ctx.newPage();

    for (const slug of PAGES) {
      await p.goto('http://localhost:4173/' + slug, { waitUntil: 'load' });
      await p.evaluate(() => [...document.images].forEach(i => { i.loading = 'eager'; }));
      await p.waitForTimeout(1400);

      const r = await p.evaluate(() => {
        const vw = document.documentElement.clientWidth;
        const out = { overflow: 0, offenders: [], small: [], taps: [], gutter: [], navHits: [] };

        out.overflow = Math.max(0, document.documentElement.scrollWidth - vw);

        const label = (el) => {
          const id = el.id ? '#' + el.id : '';
          const cls = typeof el.className === 'string' && el.className
            ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
          return el.tagName.toLowerCase() + id + cls;
        };

        const all = [...document.body.querySelectorAll('*')];

        // --- what is actually sticking out past the viewport ---------------
        if (out.overflow > 0) {
          const bad = [];
          for (const el of all) {
            const cs = getComputedStyle(el);
            if (cs.display === 'none' || cs.visibility === 'hidden') continue;
            const b = el.getBoundingClientRect();
            if (b.width === 0) continue;
            if (b.right > vw + 1 || b.left < -1) {
              // only report the outermost offender in each subtree
              if (!bad.some((x) => x.el.contains(el))) {
                bad.push({ el, over: Math.round(Math.max(b.right - vw, -b.left)) });
              }
            }
          }
          out.offenders = bad.sort((a, b) => b.over - a.over).slice(0, 4)
            .map((x) => label(x.el) + ' (+' + x.over + 'px)');
        }

        // --- text below the legibility floor -------------------------------
        const seenSmall = new Set();
        for (const el of all) {
          if (!el.childNodes.length) continue;
          const direct = [...el.childNodes]
            .filter((n) => n.nodeType === 3 && n.textContent.trim()).length;
          if (!direct) continue;
          const cs = getComputedStyle(el);
          if (cs.display === 'none' || cs.visibility === 'hidden') continue;
          const size = parseFloat(cs.fontSize);
          if (size < 14) {
            const k = label(el) + '@' + size.toFixed(1);
            if (!seenSmall.has(k)) { seenSmall.add(k); out.small.push(k + 'px'); }
          }
        }

        // --- tap targets ---------------------------------------------------
        const seenTap = new Set();
        for (const el of document.querySelectorAll(
          'a[href], button:not([disabled]), input, select, textarea')) {
          const cs = getComputedStyle(el);
          if (cs.display === 'none' || cs.visibility === 'hidden') continue;
          const b = el.getBoundingClientRect();
          if (b.width === 0 && b.height === 0) continue;
          if (b.width < 44 || b.height < 44) {
            const k = label(el) + ' ' + Math.round(b.width) + 'x' + Math.round(b.height);
            if (!seenTap.has(k)) { seenTap.add(k); out.taps.push(k); }
          }
        }

        // --- text hugging the screen edge ----------------------------------
        const seenGut = new Set();
        for (const el of document.querySelectorAll('p, h1, h2, h3, li, span.card-img__price')) {
          const cs = getComputedStyle(el);
          if (cs.display === 'none' || cs.visibility === 'hidden') continue;
          if (!el.textContent.trim()) continue;
          const b = el.getBoundingClientRect();
          if (b.width === 0) continue;
          const gap = Math.min(b.left, vw - b.right);
          if (gap < 20) {
            const k = label(el) + ' gap=' + Math.round(gap);
            if (!seenGut.has(k)) { seenGut.add(k); out.gutter.push(k); }
          }
        }

        // --- content colliding with the fixed nav --------------------------
        const nav = document.querySelector('.site-nav');
        if (nav) {
          const nb = nav.getBoundingClientRect();
          for (const el of document.querySelectorAll('main h1, main h2, main p, main .btn')) {
            const b = el.getBoundingClientRect();
            if (b.height && b.top < nb.bottom && b.bottom > nb.top && b.top >= 0) {
              out.navHits.push(label(el));
              break;
            }
          }
        }
        return out;
      });

      rows.push({ w, slug, ...r });
    }
    await ctx.close();
  }

  // compact text report
  const lines = [];
  for (const w of WIDTHS) {
    lines.push('### ' + w + 'px');
    for (const row of rows.filter((x) => x.w === w)) {
      const bits = [];
      if (row.overflow) bits.push('OVERFLOW +' + row.overflow + 'px [' + row.offenders.join(', ') + ']');
      if (row.small.length) bits.push('small-text: ' + row.small.slice(0, 4).join(', '));
      if (row.taps.length) bits.push('taps<44: ' + row.taps.length + ' [' + row.taps.slice(0, 3).join(', ') + ']');
      if (row.gutter.length) bits.push('gutter<20: ' + row.gutter.slice(0, 3).join(', '));
      if (row.navHits.length) bits.push('under-nav: ' + row.navHits.join(', '));
      lines.push('  ' + row.slug.padEnd(22) + (bits.length ? bits.join(' | ') : 'clean'));
    }
  }
  return lines.join('\n');
}
