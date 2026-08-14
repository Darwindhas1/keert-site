/* =========================================================================
   HOMY — SHARED BEHAVIOUR
   Nav scroll state, mobile menu, footer year, newsletter.
   Runs on every page. No dependencies.
   ========================================================================= */

(function () {
  "use strict";

  /* The header is transparent at every scroll position, so there is no
     scrolled state to track — the old .is-stuck toggle, its sentinel and its
     IntersectionObserver have been removed rather than left running. */

  /* --- Mobile menu ------------------------------------------------------ */
  var burger = document.querySelector("[data-menu-open]");
  var menu = document.getElementById("mobile-menu");
  var closeBtn = document.querySelector("[data-menu-close]");

  if (burger && menu) {
    var lastFocused = null;

    var focusables = function () {
      return Array.prototype.slice.call(
        menu.querySelectorAll('a[href], button:not([disabled])')
      ).filter(function (el) { return el.offsetParent !== null; });
    };

    var openMenu = function () {
      lastFocused = document.activeElement;
      menu.removeAttribute("inert");
      // Force a style flush — the subtree only becomes focusable once the
      // removed inert attribute has been committed.
      void menu.offsetWidth;
      menu.classList.add("is-open");
      burger.setAttribute("aria-expanded", "true");
      document.body.classList.add("is-locked");

      var target = closeBtn || focusables()[0];
      if (target) {
        target.focus();
        // Belt and braces if the flush above was not enough.
        if (document.activeElement !== target) {
          window.requestAnimationFrame(function () { target.focus(); });
        }
      }
    };

    var closeMenu = function () {
      menu.classList.remove("is-open");
      menu.setAttribute("inert", "");
      burger.setAttribute("aria-expanded", "false");
      document.body.classList.remove("is-locked");
      if (lastFocused && lastFocused !== document.body) lastFocused.focus();
      else burger.focus();
    };

    burger.addEventListener("click", openMenu);
    if (closeBtn) closeBtn.addEventListener("click", closeMenu);

    // Close on any link tap inside the overlay.
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) closeMenu();
    });

    document.addEventListener("keydown", function (e) {
      if (!menu.classList.contains("is-open")) return;

      if (e.key === "Escape") {
        closeMenu();
        return;
      }

      if (e.key === "Tab") {
        var items = focusables();
        if (!items.length) return;
        var first = items[0];
        var last = items[items.length - 1];
        if (e.shiftKey && document.activeElement === first) {
          e.preventDefault();
          last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
          e.preventDefault();
          first.focus();
        }
      }
    });

    // Drop back to the desktop nav if the viewport grows while open.
    window.matchMedia("(min-width: 901px)").addEventListener("change", function (e) {
      if (e.matches && menu.classList.contains("is-open")) closeMenu();
    });
  }

  /* --- Nav inversion over dark sections ---------------------------------
     The bar is transparent, so black text vanishes over the black CTA band
     and footer. An IntersectionObserver whose root is squeezed to a 1px
     line at the nav's midpoint reports which dark sections are currently
     under the bar; any overlap inverts it. Works on every page — mark a
     section with data-nav-dark and it is watched automatically.          */
  var navBar = document.querySelector(".site-nav");
  var darkZones = document.querySelectorAll("[data-nav-dark]");

  if (navBar && darkZones.length && "IntersectionObserver" in window) {
    var overlapping = new Set();
    var navObserver = null;

    var buildObserver = function () {
      if (navObserver) navObserver.disconnect();
      overlapping.clear();

      var mid = Math.round(navBar.getBoundingClientRect().height / 2);
      var bottom = Math.max(0, window.innerHeight - mid - 1);

      navObserver = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) overlapping.add(entry.target);
          else overlapping.delete(entry.target);
        });
        navBar.classList.toggle("site-nav--inverted", overlapping.size > 0);
      }, { rootMargin: "-" + mid + "px 0px -" + bottom + "px 0px", threshold: 0 });

      darkZones.forEach(function (zone) { navObserver.observe(zone); });
    };

    buildObserver();

    // The 1px probe line is pinned to viewport height, so rebuild on resize.
    var resizeTimer = null;
    window.addEventListener("resize", function () {
      window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(buildObserver, 150);
    }, { passive: true });
  }

  /* --- Services accordion ------------------------------------------------
     One card is open at a time. It follows the pointer, and auto-advances
     every 4s until the visitor takes over — after the first hover the cycle
     stops for good. Below 1024px the CSS stacks all three open, so the JS
     stands down entirely.                                                 */
  var svcRow = document.querySelector("[data-svc-row]");
  if (svcRow) {
    var cards = Array.prototype.slice.call(svcRow.querySelectorAll("[data-svc]"));
    var desktop = window.matchMedia("(min-width: 1025px)");
    var calm = window.matchMedia("(prefers-reduced-motion: reduce)");
    var timer = null;
    var index = 0;
    var takenOver = false;

    var setActive = function (i) {
      index = i;
      for (var n = 0; n < cards.length; n++) {
        cards[n].classList.toggle("is-active", n === i);
      }
    };

    var stopCycle = function () {
      takenOver = true;
      if (timer) { window.clearInterval(timer); timer = null; }
    };

    var startCycle = function () {
      if (takenOver || timer || !desktop.matches || calm.matches) return;
      timer = window.setInterval(function () {
        setActive((index + 1) % cards.length);
      }, 4000);
    };

    cards.forEach(function (card, i) {
      var take = function () {
        if (!desktop.matches) return;
        stopCycle();
        setActive(i);
      };
      card.addEventListener("mouseenter", take);
      card.addEventListener("focus", take);
    });

    startCycle();
    desktop.addEventListener("change", function (e) {
      if (!e.matches) { stopCycle(); }
    });
  }

  /* --- Property filters + load more --------------------------------------
     Chips narrow by type or location; "load more" reveals the rest of the
     matching set. Both share one render pass so the count, the button and
     the empty state never disagree.                                       */
  var grid = document.querySelector("[data-grid]");
  if (grid) {
    var allCards = Array.prototype.slice.call(grid.querySelectorAll("[data-card]"));
    var chips = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
    var moreBtn = document.querySelector("[data-load-more]");
    var countOut = document.querySelector("[data-count-out]");
    var emptyOut = document.querySelector("[data-empty]");
    var PAGE = 6;
    var filter = "all";
    var shown = PAGE;

    var matches = function (card) {
      if (filter === "all") return true;
      return card.dataset.type === filter || card.dataset.loc === filter;
    };

    var render = function () {
      var hits = allCards.filter(matches);
      allCards.forEach(function (card) { card.hidden = true; });
      hits.slice(0, shown).forEach(function (card) { card.hidden = false; });

      var visible = Math.min(shown, hits.length);
      if (countOut) {
        countOut.textContent = hits.length
          ? "Showing " + visible + " of " + hits.length +
            (hits.length === 1 ? " home" : " homes")
          : "No homes match that filter";
      }
      if (moreBtn) moreBtn.hidden = visible >= hits.length;
      if (emptyOut) emptyOut.hidden = hits.length !== 0;
    };

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        filter = chip.dataset.filter;
        shown = PAGE;
        chips.forEach(function (c) {
          var on = c === chip;
          c.classList.toggle("is-on", on);
          c.setAttribute("aria-pressed", on ? "true" : "false");
        });
        render();
      });
    });

    if (moreBtn) {
      moreBtn.addEventListener("click", function () {
        shown += PAGE;
        render();
      });
    }

    render();
  }

  /* --- Gallery lightbox -------------------------------------------------- */
  var lbDialog = document.querySelector("[data-lightbox-dialog]");
  if (lbDialog) {
    var lbImg = lbDialog.querySelector("[data-lightbox-img]");
    var lbClose = lbDialog.querySelector("[data-lightbox-close]");
    var lbOpener = null;

    var openLb = function (btn) {
      lbOpener = btn;
      lbImg.src = btn.dataset.full;
      lbImg.alt = btn.dataset.alt || "";
      lbDialog.hidden = false;
      document.body.classList.add("is-locked");
      lbClose.focus();
    };

    var closeLb = function () {
      lbDialog.hidden = true;
      lbImg.removeAttribute("src");
      document.body.classList.remove("is-locked");
      if (lbOpener) lbOpener.focus();
    };

    document.querySelectorAll("[data-lightbox]").forEach(function (btn) {
      btn.addEventListener("click", function () { openLb(btn); });
    });

    lbClose.addEventListener("click", closeLb);
    lbDialog.addEventListener("click", function (e) {
      if (e.target === lbDialog) closeLb();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !lbDialog.hidden) closeLb();
    });
  }

  /* --- Contact / booking forms -------------------------------------------
     Validates in the page, then posts to Web3Forms. Until a real access key
     is pasted in, it says so plainly rather than appearing to send.       */
  document.querySelectorAll("[data-contact-form]").forEach(function (form) {
    var status = form.querySelector("[data-form-status]");
    var KEY_PLACEHOLDER = "REPLACE_WITH_WEB3FORMS_KEY";

    var setError = function (field, message) {
      var slot = field.querySelector("[data-error]");
      field.dataset.invalid = message ? "true" : "false";
      if (!slot) return;
      slot.textContent = message || "";
      slot.hidden = !message;
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;

      form.querySelectorAll(".field").forEach(function (field) {
        var input = field.querySelector("input, textarea, select");
        if (!input || !input.required) return;
        if (!input.value.trim()) {
          setError(field, "This one is required.");
          ok = false;
        } else if (input.type === "email" && !input.checkValidity()) {
          setError(field, "That email address does not look right.");
          ok = false;
        } else {
          setError(field, "");
        }
      });

      if (!ok) {
        var firstBad = form.querySelector('[data-invalid="true"] input, [data-invalid="true"] textarea');
        if (firstBad) firstBad.focus();
        if (status) { status.textContent = "Check the highlighted fields."; status.removeAttribute("data-state"); }
        return;
      }

      var key = form.querySelector('[name="access_key"]');
      if (!key || key.value === KEY_PLACEHOLDER) {
        if (status) {
          status.textContent =
            "Looks good — but the form is not connected yet. Add a Web3Forms access key to start receiving these.";
          status.removeAttribute("data-state");
        }
        return;
      }

      if (status) { status.textContent = "Sending…"; status.removeAttribute("data-state"); }

      fetch("https://api.web3forms.com/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify(Object.fromEntries(new FormData(form)))
      }).then(function (res) {
        if (!res.ok) throw new Error(res.status);
        form.reset();
        if (status) {
          status.textContent = "Thank you — we reply within one working day.";
          status.setAttribute("data-state", "ok");
        }
      }).catch(function () {
        if (status) {
          status.textContent = "That did not send. Email darwindhas1799@gmail.com and we will pick it up.";
          status.removeAttribute("data-state");
        }
      });
    });
  });

  /* --- Footer year ------------------------------------------------------ */
  var year = document.querySelector("[data-year]");
  if (year) year.textContent = String(new Date().getFullYear());

  /* --- Newsletter: inline validation only, no backend wired ------------- */
  var news = document.querySelector("[data-newsletter]");
  if (news) {
    var note = news.parentElement.querySelector("[data-newsletter-note]");
    news.addEventListener("submit", function (e) {
      e.preventDefault();
      var input = news.querySelector("input[type='email']");
      if (!note || !input) return;
      if (!input.checkValidity()) {
        note.textContent = "Enter a valid email address so we can reach you.";
        note.removeAttribute("data-state");
        input.focus();
        return;
      }
      note.textContent = "You are on the list. New Penang and Ipoh listings land every Thursday.";
      note.setAttribute("data-state", "ok");
      news.reset();
    });
  }
})();
