/* PeerBridge — shared interactions
   1. mobile nav + dropdown menus
   2. footer year
   3. glossary search / A-Z filter
   4. contact form "humanizer" check (math + honeypot + time trap)
*/

(function () {
  "use strict";

  /* ---------------------------------------------------------------
     1. Navigation
     --------------------------------------------------------------- */
  var nav = document.getElementById("site-nav");
  var toggle = document.querySelector(".menu-toggle");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", String(open));
      document.body.style.overflow = open && window.innerWidth <= 940 ? "hidden" : "";
    });
  }

  var items = Array.prototype.slice.call(document.querySelectorAll(".nav-item"));

  items.forEach(function (item) {
    var btn = item.querySelector(".nav-link[aria-haspopup]");
    if (!btn) return;

    btn.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();
      var wasOpen = item.classList.contains("open");
      items.forEach(function (o) {
        o.classList.remove("open");
        var b = o.querySelector(".nav-link[aria-haspopup]");
        if (b) b.setAttribute("aria-expanded", "false");
      });
      if (!wasOpen) {
        item.classList.add("open");
        btn.setAttribute("aria-expanded", "true");
      }
    });

    // hover-open on desktop only
    item.addEventListener("mouseenter", function () {
      if (window.innerWidth <= 940) return;
      items.forEach(function (o) { o.classList.remove("open"); });
      item.classList.add("open");
      btn.setAttribute("aria-expanded", "true");
    });
    item.addEventListener("mouseleave", function () {
      if (window.innerWidth <= 940) return;
      item.classList.remove("open");
      btn.setAttribute("aria-expanded", "false");
    });
  });

  document.addEventListener("click", function (e) {
    if (nav && nav.contains(e.target)) return;
    items.forEach(function (o) {
      o.classList.remove("open");
      var b = o.querySelector(".nav-link[aria-haspopup]");
      if (b) b.setAttribute("aria-expanded", "false");
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    items.forEach(function (o) { o.classList.remove("open"); });
    if (nav && nav.classList.contains("open")) {
      nav.classList.remove("open");
      if (toggle) toggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    }
  });

  /* ---------------------------------------------------------------
     2. Footer year
     --------------------------------------------------------------- */
  Array.prototype.forEach.call(document.querySelectorAll(".js-year"), function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  /* ---------------------------------------------------------------
     3. Glossary
     --------------------------------------------------------------- */
  var glossary = document.getElementById("glossary");
  if (glossary) {
    var search = document.getElementById("gloss-search");
    var alphaWrap = document.getElementById("gloss-alpha");
    var terms = Array.prototype.slice.call(glossary.querySelectorAll(".term"));
    var empty = document.getElementById("gloss-empty");
    var activeLetter = "all";

    // build the A-Z bar, disabling letters with no entries
    var present = {};
    terms.forEach(function (t) {
      present[(t.getAttribute("data-term") || "").charAt(0).toUpperCase()] = true;
    });

    if (alphaWrap) {
      var html = '<button type="button" class="active" data-letter="all">All</button>';
      "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("").forEach(function (L) {
        html += '<button type="button" data-letter="' + L + '"' + (present[L] ? "" : " disabled") + ">" + L + "</button>";
      });
      alphaWrap.innerHTML = html;

      alphaWrap.addEventListener("click", function (e) {
        var b = e.target.closest("button");
        if (!b || b.disabled) return;
        activeLetter = b.getAttribute("data-letter");
        Array.prototype.forEach.call(alphaWrap.querySelectorAll("button"), function (o) {
          o.classList.toggle("active", o === b);
        });
        apply();
      });
    }

    function apply() {
      var q = (search && search.value || "").trim().toLowerCase();
      var shown = 0;

      terms.forEach(function (t) {
        var name = (t.getAttribute("data-term") || "").toLowerCase();
        var text = t.textContent.toLowerCase();
        var matchesQuery = !q || name.indexOf(q) > -1 || text.indexOf(q) > -1;
        var matchesLetter = activeLetter === "all" || name.charAt(0).toUpperCase() === activeLetter;
        var show = matchesQuery && matchesLetter;
        t.hidden = !show;
        if (show) shown++;
      });

      if (empty) empty.hidden = shown > 0;
    }

    if (search) search.addEventListener("input", apply);
    apply();
  }

  /* ---------------------------------------------------------------
     4. Humanizer check on forms
     Three layers, all client-side (this is a static site, so there is
     no server to verify against — the goal is to stop dumb bots, and
     it stops the overwhelming majority of them):
       a) honeypot field bots fill in and humans never see
       b) time trap — a real person can't read + submit in under 4s
       c) arithmetic challenge the user answers
     --------------------------------------------------------------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-human-check]"), function (form) {
    var qEl = form.querySelector(".hc-q");
    var input = form.querySelector(".hc-answer");
    var newBtn = form.querySelector(".hc-new");
    var msg = form.querySelector(".hc-msg");
    var honey = form.querySelector(".hp input");
    var loadedAt = Date.now();
    var expected = 0;
    var attempts = 0;

    function words(n) {
      return ["zero", "one", "two", "three", "four", "five", "six", "seven",
              "eight", "nine", "ten", "eleven", "twelve"][n] || String(n);
    }

    function challenge() {
      var a = Math.floor(Math.random() * 8) + 2;   // 2..9
      var b = Math.floor(Math.random() * 6) + 1;   // 1..6
      var plus = Math.random() < 0.65;

      if (!plus && a < b) { var t = a; a = b; b = t; }

      expected = plus ? a + b : a - b;
      // spell one operand out so naive OCR/regex bots can't just parse digits
      qEl.textContent = plus
        ? words(a) + " + " + b + " = ?"
        : a + " − " + words(b) + " = ?";
      qEl.setAttribute("aria-label", qEl.textContent);
      input.value = "";
      if (msg) { msg.textContent = ""; msg.className = "hc-msg"; }
    }

    function fail(text) {
      if (msg) { msg.textContent = text; msg.className = "hc-msg bad"; }
    }

    if (!qEl || !input) return;
    challenge();

    if (newBtn) {
      newBtn.addEventListener("click", function (e) {
        e.preventDefault();
        challenge();
        input.focus();
      });
    }

    form.addEventListener("submit", function (e) {
      // (a) honeypot
      if (honey && honey.value !== "") {
        e.preventDefault();
        fail("Something went wrong. Please refresh and try again.");
        return;
      }

      // (b) time trap
      if (Date.now() - loadedAt < 4000) {
        e.preventDefault();
        fail("That was quick! Give it a moment and press send again.");
        return;
      }

      // (c) arithmetic
      var given = parseInt(String(input.value).trim(), 10);
      if (isNaN(given) || given !== expected) {
        e.preventDefault();
        attempts++;
        fail(attempts >= 3
          ? "Still not matching. Try the new question below."
          : "That answer isn't right — give it another go.");
        if (attempts >= 3) challenge();
        input.focus();
        return;
      }

      if (msg) { msg.textContent = "Verified — sending..."; msg.className = "hc-msg good"; }
    });
  });
})();
