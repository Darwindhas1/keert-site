/* =========================================================================
   HOMY — MOTION  (BRIEF §7)
   GSAP + ScrollTrigger, on native scroll.

   Performance contract:
   - Native scroll only — no smooth-scroll library. gsap.ticker is the single
     rAF loop in the page.
   - Scroll-linked work is transform-only (yPercent), never layout props.
   - Parallax and magnetic hover are desktop-only, via gsap.matchMedia.
   - Nothing carries a permanent will-change; GSAP applies it per tween.

   Every effect degrades to static content: if GSAP never arrives, or the
   visitor asks for reduced motion, .js-motion is dropped and all content is
   simply visible.
   ========================================================================= */

(function () {
  "use strict";

  var root = document.documentElement;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function standDown() {
    root.classList.remove("js-motion");
  }

  // Failsafe: a blocked CDN must never leave the page blank.
  var failsafe = window.setTimeout(standDown, 2000);

  if (reduced || !window.gsap || !window.ScrollTrigger) {
    window.clearTimeout(failsafe);
    standDown();
    return;
  }

  window.clearTimeout(failsafe);
  var gsap = window.gsap;
  var ScrollTrigger = window.ScrollTrigger;
  gsap.registerPlugin(ScrollTrigger);

  var EASE = "power3.out";
  var DUR = 0.9;

  /* No smooth-scroll library. The page scrolls natively; ScrollTrigger reads
     the browser's own scroll position, and gsap.ticker is the only rAF loop
     in the page. Anchor links use the browser's default jump. */
  gsap.ticker.lagSmoothing(0);

  /* --- Hero headline: word-by-word reveal on load ------------------------ */
  var headline = document.querySelector("[data-split]");
  if (headline) {
    var html = headline.innerHTML;
    var out = html.split(/(<br\s*\/?>)/i).map(function (chunk) {
      if (/^<br/i.test(chunk)) return chunk;
      return chunk.split(/\s+/).filter(Boolean).map(function (w) {
        return '<span class="word"><span class="word__in">' + w + "</span></span>";
      }).join(" ");
    }).join("");
    headline.innerHTML = out;

    gsap.set(headline, { opacity: 1 });
    gsap.from(headline.querySelectorAll(".word__in"), {
      yPercent: 110, duration: 1, ease: EASE, stagger: 0.06, delay: 0.15
    });
  }

  /* --- Rest of the hero stack ------------------------------------------- */
  var heroLoad = document.querySelectorAll("[data-hero-in]");
  if (heroLoad.length) {
    gsap.set(heroLoad, { opacity: 0, y: 24 });
    gsap.to(heroLoad, {
      opacity: 1, y: 0, duration: DUR, ease: EASE, stagger: 0.1, delay: 0.1
    });
  }

  /* --- Hero house: rises on load ---------------------------------------- */
  var house = document.querySelector("[data-hero-house]");
  var stage = document.querySelector("[data-hero-stage]");
  var cloudBand = document.querySelector("[data-hero-clouds]");
  if (house) {
    gsap.fromTo(house,
      { y: 80, opacity: 0 },
      { y: 0, opacity: 1, duration: 1.1, ease: "power3.out", delay: 0.3 });
  }

  /* --- Reveals: one trigger per section, header then content -------------
     Each section announces itself: the header block (eyebrow, H2, right
     paragraph) fades up first, then the content below it follows 0.15s
     later. One ScrollTrigger per section — not one per element.          */
  gsap.utils.toArray("section, .site-footer").forEach(function (section) {
    var items = gsap.utils.toArray("[data-reveal]", section);
    if (!items.length) return;

    var head = items.filter(function (el) { return el.closest(".split-head"); });
    var body = items.filter(function (el) { return !el.closest(".split-head"); });

    gsap.set(items, { opacity: 0, y: 40 });

    ScrollTrigger.create({
      trigger: section,
      start: "top 80%",
      once: true,
      onEnter: function () {
        if (head.length) {
          gsap.to(head, {
            opacity: 1, y: 0, duration: DUR, ease: EASE, stagger: 0.08
          });
        }
        if (body.length) {
          gsap.to(body, {
            opacity: 1, y: 0, duration: DUR, ease: EASE, stagger: 0.08,
            delay: head.length ? 0.15 : 0
          });
        }
      }
    });
  });

  /* --- Stat count-up ----------------------------------------------------- */
  document.querySelectorAll("[data-count]").forEach(function (el) {
    var target = parseFloat(el.dataset.count);
    var decimals = parseInt(el.dataset.countDecimals || "0", 10);
    var prefix = el.dataset.countPrefix || "";
    var suffix = el.dataset.countSuffix || "";
    var proxy = { v: 0 };
    // Build the formatter once. toLocaleString() constructs a fresh Intl
    // formatter on every call, which showed up in the scroll profile.
    var fmt = new Intl.NumberFormat("en-MY", {
      minimumFractionDigits: decimals, maximumFractionDigits: decimals
    });

    gsap.to(proxy, {
      v: target, duration: 1.6, ease: "power2.out",
      scrollTrigger: { trigger: el, start: "top 85%", once: true },
      onUpdate: function () {
        el.textContent = prefix + fmt.format(proxy.v) + suffix;
      }
    });
  });

  /* --- Desktop-only: parallax + magnetic CTA ----------------------------- */
  var mm = gsap.matchMedia();

  mm.add("(min-width: 1024px)", function () {
    /* The signature move: the house rises and grows up out of the cloud band
       and passes in front of the headline, which fades away beneath it.
       Transform + opacity only, so it all stays on the compositor. */
    if (house) {
      // One element, one tween, one composited layer — the badge, headline,
      // subhead and CTAs already share .hero__inner, so fading four separate
      // targets only bought four tweens and four layers.
      var heroText = document.querySelector(".hero__inner");
      var isFront = false;

      var tl = gsap.timeline({
        scrollTrigger: {
          trigger: ".hero",
          start: "top top",
          end: "bottom top",
          // Eases toward the scroll position over ~0.5s. scrub:true locks to
          // it frame-for-frame, which is what made the hero feel sticky.
          scrub: 0.5,
          // Pinned: without this the hero simply scrolls away and the house
          // leaves the screen before it can grow into the frame.
          pin: true,
          anticipatePin: 1,
          invalidateOnRefresh: true,
          onUpdate: function (self) {
            // Once it has climbed far enough, the house owns the frame.
            // Only touch the DOM when the state actually flips.
            var front = self.progress > 0.35;
            if (stage && front !== isFront) {
              isFront = front;
              stage.classList.toggle("is-front", front);
            }
          }
        }
      });

      // Rise only — no scale. Scaling a 1900w image with alpha forced a
      // re-raster every frame, which is what made the scrub feel sticky.
      // A pure translate stays on the compositor.
      tl.to(house, {
        yPercent: -18, ease: "none", duration: 1, force3D: true
      }, 0);
      if (cloudBand) {
        // Drifts slower than the house, so the house reads as rising past it.
        tl.to(cloudBand, {
          yPercent: 10, ease: "none", duration: 1, force3D: true
        }, 0);
      }
      tl.to(heroText, {
        opacity: 0, yPercent: -8, ease: "none", duration: 0.5, force3D: true
      }, 0);
    }

    document.querySelectorAll("[data-parallax]").forEach(function (el) {
      var amount = parseFloat(el.dataset.parallax) || 10;
      gsap.fromTo(el,
        { yPercent: amount * -0.5 },
        {
          yPercent: amount * 0.5, ease: "none",
          scrollTrigger: {
            trigger: el.parentElement,
            start: "top bottom", end: "bottom top",
            scrub: 1, invalidateOnRefresh: true
          }
        });
    });
  });

  mm.add("(min-width: 1024px) and (hover: hover) and (pointer: fine)", function () {
    document.querySelectorAll("[data-magnetic]").forEach(function (el) {
      // quickTo reuses one tween per property instead of allocating a new
      // tween on every mousemove.
      var xTo = gsap.quickTo(el, "x", { duration: 0.4, ease: "power3" });
      var yTo = gsap.quickTo(el, "y", { duration: 0.4, ease: "power3" });
      var queued = false;
      var mx = 0, my = 0;

      var onMove = function (e) {
        mx = e.clientX;
        my = e.clientY;
        if (queued) return;              // throttle to one read per frame
        queued = true;
        window.requestAnimationFrame(function () {
          queued = false;
          var r = el.getBoundingClientRect();
          xTo((mx - (r.left + r.width / 2)) * 0.3);
          yTo((my - (r.top + r.height / 2)) * 0.3);
        });
      };
      var onLeave = function () { xTo(0); yTo(0); };

      el.addEventListener("mousemove", onMove);
      el.addEventListener("mouseleave", onLeave);

      return function () {
        el.removeEventListener("mousemove", onMove);
        el.removeEventListener("mouseleave", onLeave);
        gsap.set(el, { x: 0, y: 0 });
      };
    });
  });

  /* --- Page transition: fade out on internal navigation ------------------ */
  var shell = document.querySelector("main");
  if (shell) {
    document.addEventListener("click", function (e) {
      var a = e.target.closest('a[href]');
      if (!a) return;
      var href = a.getAttribute("href");
      if (!href || href.startsWith("#") || href.startsWith("mailto:") ||
          href.startsWith("tel:") || a.target === "_blank" ||
          a.hasAttribute("download") || a.host !== window.location.host) return;

      e.preventDefault();
      gsap.to(shell, {
        opacity: 0, duration: 0.28, ease: "power2.in",
        onComplete: function () { window.location.href = href; }
      });
    });

    window.addEventListener("pageshow", function (e) {
      if (e.persisted) gsap.set(shell, { opacity: 1 });
    });
  }
})();
