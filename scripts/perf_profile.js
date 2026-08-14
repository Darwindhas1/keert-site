/**
 * Hero scroll profiler. Fresh context every run (init scripts accumulate on a
 * long-lived page and corrupt rAF counts otherwise).
 *
 * Captures, while scrolling through the hero:
 *   - frame pacing (FPS, p95, worst, jank%)
 *   - longest long-task
 *   - a CDP CPU profile aggregated by self-time, so "what is the main thread
 *     doing" is answered with data rather than a guess
 *   - rAF schedulers, attributed to their caller
 *
 * Runs at 1x (real desktop) and 4x (low-end machine).
 */
async (page) => {
  const browser = page.context().browser();
  const results = [];

  for (const rate of [1, 4]) {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const p = await ctx.newPage();

    await p.addInitScript(() => {
      window.__raf = 0;
      window.__callers = {};
      // Building a stack on every rAF call costs more than the code under
      // test at 4x throttle. Sample the first N for attribution, then just
      // count, so the probe stops polluting its own profile.
      const orig = window.requestAnimationFrame.bind(window);
      let sampled = 0;
      window.requestAnimationFrame = function (cb) {
        window.__raf++;
        if (sampled < 120) {
          sampled++;
          const s = (new Error().stack || '').split('\n')[2] || '?';
          const key = s.trim().replace(/^at\s+/, '')
            .replace(/https?:\/\/[^\s)]*\//g, '').replace(/[:\d]+\)?$/, '');
          window.__callers[key] = (window.__callers[key] || 0) + 1;
        }
        return orig(cb);
      };
      window.__long = [];
      new PerformanceObserver((l) => {
        for (const e of l.getEntries()) window.__long.push(Math.round(e.duration));
      }).observe({ entryTypes: ['longtask'] });
    });

    const cdp = await ctx.newCDPSession(p);
    await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
    if (rate > 1) await cdp.send('Emulation.setCPUThrottlingRate', { rate });

    await p.goto('http://localhost:4173/index.html', { waitUntil: 'load' });
    await p.waitForTimeout(2500);

    await p.evaluate(() => {
      window.__raf = 0; window.__callers = {}; window.__long.length = 0;
      window.__f = []; window.__stop = false;
      let last = performance.now();
      (function t(now) {
        if (window.__stop) return;
        window.__f.push(now - last); last = now; requestAnimationFrame(t);
      })(performance.now());
    });

    await cdp.send('Profiler.enable');
    await cdp.send('Profiler.setSamplingInterval', { interval: 200 });
    await cdp.send('Profiler.start');

    await p.mouse.move(720, 450);
    for (let i = 0; i < 40; i++) { await p.mouse.wheel(0, 200); await p.waitForTimeout(45); }
    await p.waitForTimeout(400);

    const { profile } = await cdp.send('Profiler.stop');

    // Aggregate self time per function from the sampled profile.
    const byId = new Map(profile.nodes.map((n) => [n.id, n]));
    const self = new Map();
    const deltas = profile.timeDeltas || [];
    (profile.samples || []).forEach((id, i) => {
      const n = byId.get(id);
      if (!n) return;
      const cf = n.callFrame;
      let name = cf.functionName || '(anonymous)';
      const url = (cf.url || '').split('/').pop();
      if (name === '(program)' || name === '(idle)' || name === '(garbage collector)') {
        name = name.replace(/[()]/g, '');
      } else {
        name = `${name} — ${url || 'inline'}`;
      }
      self.set(name, (self.get(name) || 0) + Math.max(0, deltas[i] || 0) / 1000);
    });
    const top = [...self.entries()]
      .sort((a, b) => b[1] - a[1]).slice(0, 10)
      .map(([k, ms]) => `${k}: ${Math.round(ms)}ms`);

    const frames = await p.evaluate(() => {
      window.__stop = true;
      const f = window.__f.slice(3);
      const s = [...f].sort((a, b) => a - b);
      return {
        avgFps: Math.round(1000 / (f.reduce((a, b) => a + b, 0) / f.length)),
        medianMs: Math.round(s[Math.floor(s.length * 0.5)] * 10) / 10,
        p95Ms: Math.round(s[Math.floor(s.length * 0.95)] * 10) / 10,
        worstMs: Math.round(s[s.length - 1]),
        jankPct: Math.round(f.filter((x) => x > 20).length / f.length * 100),
        longTasks: window.__long.length,
        longestTaskMs: window.__long.length ? Math.max(...window.__long) : 0,
        rafPerFrame: Math.round(window.__raf / f.length * 100) / 100,
        // Sampled attribution: shares of the first 120 rAF registrations.
        rafBySource: Object.entries(window.__callers).sort((a, b) => b[1] - a[1])
          .slice(0, 5).map(([k, v]) => `${k} = ${v}`)
      };
    });

    results.push({ cpu: rate + 'x', ...frames, mainThreadTop: top });
    await ctx.close();
  }
  return JSON.stringify(results, null, 1);
}
