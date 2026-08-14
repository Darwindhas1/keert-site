/**
 * Repeats the 4x-throttled hero scroll N times and reports the median, because
 * single throttled runs on this box swing by 15+ fps and are not decisive.
 */
async (page) => {
  const browser = page.context().browser();
  const runs = [];

  for (let i = 0; i < 3; i++) {
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const p = await ctx.newPage();
    await p.addInitScript(() => {
      window.__long = [];
      new PerformanceObserver((l) => {
        for (const e of l.getEntries()) window.__long.push(Math.round(e.duration));
      }).observe({ entryTypes: ['longtask'] });
    });
    const cdp = await ctx.newCDPSession(p);
    await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
    await p.goto('http://localhost:4173/index.html', { waitUntil: 'load' });
    await p.waitForTimeout(2500);
    await p.evaluate(() => {
      window.__long.length = 0; window.__f = []; window.__stop = false;
      let last = performance.now();
      (function t(now) {
        if (window.__stop) return;
        window.__f.push(now - last); last = now; requestAnimationFrame(t);
      })(performance.now());
    });
    await p.mouse.move(720, 450);
    for (let k = 0; k < 40; k++) { await p.mouse.wheel(0, 200); await p.waitForTimeout(45); }
    await p.waitForTimeout(300);
    runs.push(await p.evaluate(() => {
      window.__stop = true;
      const f = window.__f.slice(3), s = [...f].sort((a, b) => a - b);
      return {
        fps: Math.round(1000 / (f.reduce((a, b) => a + b, 0) / f.length)),
        p95: Math.round(s[Math.floor(s.length * 0.95)] * 10) / 10,
        jank: Math.round(f.filter((x) => x > 20).length / f.length * 100),
        longest: window.__long.length ? Math.max(...window.__long) : 0,
        tasks: window.__long.length
      };
    }));
    await ctx.close();
  }

  const med = (k) => [...runs.map((r) => r[k])].sort((a, b) => a - b)[1];
  return JSON.stringify({
    runs,
    median: { fps: med('fps'), p95: med('p95'), jank: med('jank'),
              longest: med('longest'), tasks: med('tasks') }
  }, null, 1);
}
