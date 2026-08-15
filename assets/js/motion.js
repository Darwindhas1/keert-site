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

  var PHONE = "(max-width: 768px)";
  var isPhone = window.matchMedia(PHONE).matches;

  var headline = document.querySelector("[data-split]");
  var house = document.querySelector("[data-hero-house]");
  var stage = document.querySelector("[data-hero-stage]");
  var cloudBand = document.querySelector("[data-hero-clouds]");

  /* --- Hero headline: word-by-word reveal on load ------------------------
     Desktop only. The phone headline is two lines, so per-word tweens buy a
     handful of extra layers and no legibility. Decided once at load rather
     than inside matchMedia: this rewrites the DOM, and re-splitting on every
     resize across the breakpoint is not worth the reflow. */
  if (headline && !isPhone) {
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

  /* --- Hero load sequence ------------------------------------------------ */
  if (isPhone) {
    /* One list, one tween each, explicit delays — the stack reads top to
       bottom rather than arriving as a block. */
    [
      [".hero__badge", 0.1],
      ["[data-split]", 0.2],
      [".hero__sub", 0.32],
      [".hero__ctas", 0.44]
    ].forEach(function (pair) {
      var el = document.querySelector(pair[0]);
      if (!el) return;
      gsap.set(el, { opacity: 0, y: 24 });
      gsap.to(el, {
        opacity: 1, y: 0, duration: 0.7, ease: EASE, delay: pair[1], force3D: true
      });
    });

    if (house) {
      gsap.fromTo(house,
        { y: 60, opacity: 0 },
        { y: 0, opacity: 1, duration: 1, ease: EASE, delay: 0.35, force3D: true });
    }
  } else {
    var heroLoad = document.querySelectorAll("[data-hero-in]");
    if (heroLoad.length) {
      gsap.set(heroLoad, { opacity: 0, y: 24 });
      gsap.to(heroLoad, {
        opacity: 1, y: 0, duration: DUR, ease: EASE, stagger: 0.1, delay: 0.1
      });
    }
    if (house) {
      gsap.fromTo(house,
        { y: 80, opacity: 0 },
        { y: 0, opacity: 1, duration: 1.1, ease: EASE, delay: 0.3 });
    }
  }

  /* --- Reveals: one trigger per section, header then content -------------
     Each section announces itself: the header block (eyebrow, H2, right
     paragraph) fades up first, then the content below it follows 0.15s
     later. One ScrollTrigger per section — not one per element.          */
  var GRIDS = ".listings__grid, .props__grid, .why__grid, .svc-row, .team__grid," +
              " .values__grid, .pd-gallery, .features__stack";

  gsap.utils.toArray("section, .site-footer").forEach(function (section) {
    var items = gsap.utils.toArray("[data-reveal]", section);
    if (!items.length) return;

    var head = [], cards = [], body = [];
    items.forEach(function (el) {
      if (el.closest(".split-head") || el.closest(".page-intro__head")) head.push(el);
      else if (el.closest(GRIDS)) cards.push(el);
      else body.push(el);
    });

    gsap.set(items, { opacity: 0, y: 32 });

    ScrollTrigger.create({
      trigger: section,
      start: "top 85%",
      once: true,
      onEnter: function () {
        if (head.length) {
          gsap.to(head, {
            opacity: 1, y: 0, duration: DUR, ease: EASE, stagger: 0.08, force3D: true
          });
        }
        var after = head.length ? 0.12 : 0;
        if (body.length) {
          gsap.to(body, {
            opacity: 1, y: 0, duration: DUR, ease: EASE, stagger: 0.08,
            delay: after, force3D: true
          });
        }
        // Cards move as a run of their own, tighter than the prose above them.
        if (cards.length) {
          gsap.to(cards, {
            opacity: 1, y: 0, duration: DUR, ease: EASE, stagger: 0.06,
            delay: after, force3D: true
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

  var mm = gsap.matchMedia();

  /* --- Phone: the same hero move as desktop, without the pin -------------
     Desktop pins the hero and flips the house in front of the headline. On a
     phone that would park a building over the copy on a screen with no room
     to spare, so the house rises behind and the text fades out from under
     it. No pin either: the hero is 100svh, so it leaves naturally.

     One timeline, three targets, transform and opacity only.              */
  mm.add(PHONE, function () {
    if (!house) return;
    var heroText = document.querySelector(".hero__inner");

    var tl = gsap.timeline({
      scrollTrigger: {
        trigger: ".hero",
        start: "top top",
        end: "bottom top",
        scrub: 0.6,
        invalidateOnRefresh: true
      }
    });

    tl.to(house, { yPercent: -14, ease: "none", duration: 1, force3D: true }, 0);

    /* The cloud drift is deliberately absent here, and it is the one thing
       cut from the brief. Measured at 4x CPU throttle, 3 runs, median:

         390px with cloud drift    54.9fps,  7 dropped frames
         390px without             58.4fps,  2 dropped frames
         390px without + no house scrub  58.4fps,  2 dropped frames

       The band carries a mask and 50% opacity, so translating it re-composites
       the mask every frame; the house scrub on its own costs nothing. Cutting
       the clouds first is the order the brief set out, and the house keeps the
       move that matters. The band stays where it is, static. */

    // Gone by halfway, so the house has the lower screen to itself.
    tl.to(heroText, {
      opacity: 0, yPercent: -6, ease: "none", duration: 0.5, force3D: true
    }, 0);

    return function () {
      gsap.set([house, heroText], { clearProps: "transform,opacity" });
    };
  });

  /* --- Desktop-only: parallax + magnetic CTA ----------------------------- */

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
