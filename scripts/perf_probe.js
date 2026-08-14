/**
 * Repeatable performance probe for index.html.
 * Run via the Playwright MCP `browser_run_code_unsafe` tool with
 * filename = scripts/perf_probe.js.
 *
 * Runs in a FRESH browser context every time. This matters: init scripts
 * registered on a long-lived page accumulate across runs, each one wrapping
 * requestAnimationFrame again, which silently multiplies the rAF count and
 * duplicates PerformanceObserver entries. A clean context is the only way to
 * get numbers that mean anything run to run.
 *
 * Reports: rAF schedulers per frame (with attribution), ScrollTrigger count,
 * frame pacing under a real wheel scroll, long tasks, LCP, and bytes.
 */
async (page) => {
  const browser = page.context().browser();
  const ctx = await browser.newContext({ viewport: { width: 1440, height: 960 } });
  const p = await ctx.newPage();

  await p.addInitScript(() => {
    window.__raf = 0;
    window.__callers = {};
    const orig = window.requestAnimationFrame.bind(window);
    window.requestAnimationFrame = function (cb) {
      window.__raf++;
      const s = (new Error().stack || '').split('\n')[2] || '?';
      const key = s.trim().replace(/^at\s+/, '').replace(/https?:\/\/[^\s)]*\//g, '')
        .replace(/[:\d]+\)?$/, '');
      window.__callers[key] = (window.__callers[key] || 0) + 1;
      return orig(cb);
    };

    window.__long = [];
    new PerformanceObserver((l) => {
      for (const e of l.getEntries()) window.__long.push(Math.round(e.duration));
    }).observe({ entryTypes: ['longtask'] });

    window.__lcp = 0;
    new PerformanceObserver((l) => {
      const es = l.getEntries();
      window.__lcp = Math.round(es[es.length - 1].startTime);
    }).observe({ type: 'largest-contentful-paint', buffered: true });
  });

  // A fast dev box hides the jank users feel. Throttle CPU 4x, no cache.
  const cdp = await ctx.newCDPSession(p);
  await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
  await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });

  await p.goto('http://localhost:4173/index.html', { waitUntil: 'load' });
  await p.waitForTimeout(2500); // let entrance animations settle

  const sum = (a) => a.reduce((x, y) => x + y, 0);
  const settled = await p.evaluate(() => ({
    scrollTriggers: window.ScrollTrigger ? window.ScrollTrigger.getAll().length : 0,
    lcpMs: window.__lcp,
    longTasksOnLoad: window.__long.length,
    worstLoadTaskMs: window.__long.length ? Math.max(...window.__long) : 0,
    blockingMsOnLoad: window.__long.reduce((a, b) => a + Math.max(0, b - 50), 0),
  }));

  // --- frame pacing during a real wheel scroll --------------------------
  await p.evaluate(() => {
    window.__raf = 0;
    window.__callers = {};
    window.__long.length = 0;
    window.__frames = [];
    window.__stop = false;
    let last = performance.now();
    (function tick(now) {
      if (window.__stop) return;
      window.__frames.push(now - last);
      last = now;
      requestAnimationFrame(tick);
    })(performance.now());
  });

  await p.mouse.move(720, 500);
  for (let i = 0; i < 45; i++) {
    await p.mouse.wheel(0, 220);
    await p.waitForTimeout(45);
  }
  await p.waitForTimeout(400);

  const scroll = await p.evaluate(() => {
    window.__stop = true;
    const f = window.__frames.slice(3);
    const sorted = [...f].sort((a, b) => a - b);
    const pct = (q) => Math.round(sorted[Math.floor(sorted.length * q)] * 10) / 10;
    const avg = f.reduce((a, b) => a + b, 0) / f.length;
    return {
      frames: f.length,
      avgFps: Math.round(1000 / avg),
      medianFrameMs: pct(0.5),
      p95FrameMs: pct(0.95),
      worstFrameMs: Math.round(sorted[sorted.length - 1]),
      jankFramesOver20ms: f.filter((x) => x > 20).length,
      jankPct: Math.round((f.filter((x) => x > 20).length / f.length) * 100),
      longTasksDuringScroll: window.__long.length,
      worstScrollTaskMs: window.__long.length ? Math.max(...window.__long) : 0,
      // 1 of these is the probe's own tick; the rest are the page's.
      rafPerFrame: Math.round((window.__raf / f.length) * 100) / 100,
      rafBySource: Object.entries(window.__callers)
        .sort((a, b) => b[1] - a[1]).slice(0, 6)
        .map(([k, v]) => k + ' = ' + (Math.round((v / f.length) * 100) / 100) + '/frame'),
    };
  });

  const bytes = await p.evaluate(() => {
    const all = performance.getEntriesByType('resource');
    const imgs = all.filter((r) => r.initiatorType === 'img');
    const kb = (rs) => Math.round(
      rs.reduce((a, r) => a + (r.encodedBodySize || r.transferSize || 0), 0) / 1024);
    return { imageKB: kb(imgs), heroKB: kb(imgs.filter((r) => /hero-/.test(r.name))), totalKB: kb(all) };
  });

  await ctx.close();
  return JSON.stringify({ settled, scroll, bytes }, null, 1);
}
