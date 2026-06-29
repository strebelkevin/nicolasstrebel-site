/* ==========================================================================
   Nicolas Strebel - site behaviour
   Vanilla JS, no dependencies. Loaded with `defer`.
   - Scroll-reveal (gentle fade/slide on enter)
   - Sticky nav shadow on scroll
   - Mobile nav drawer
   - Count-up trust stats
   - Footer year
   All motion respects prefers-reduced-motion.
   ========================================================================== */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Scroll reveal ---------------------------------------------------- */
  var revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length) {
    if (reduceMotion || !('IntersectionObserver' in window)) {
      revealEls.forEach(function (el) { el.classList.add('is-visible'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
      revealEls.forEach(function (el) { io.observe(el); });
    }
  }

  /* ---- Sticky nav shadow ------------------------------------------------ */
  var nav = document.querySelector('.nav');
  var heroMedia = document.querySelector('[data-parallax]');
  if (nav || heroMedia) {
    var ticking = false;
    var apply = function () {
      var y = window.scrollY;
      if (nav) nav.classList.toggle('is-scrolled', y > 24);
      // Hero parallax - subtle, opacity-safe, transform only
      if (heroMedia && !reduceMotion && y < window.innerHeight) {
        heroMedia.style.transform = 'translate3d(0,' + (y * 0.18) + 'px,0) scale(' + (1 + y * 0.0002) + ')';
      }
      ticking = false;
    };
    var onScroll = function () {
      if (!ticking) { window.requestAnimationFrame(apply); ticking = true; }
    };
    apply();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- Segmented path selector ----------------------------------------- */
  var sTabs = document.querySelectorAll('.selector__tab');
  if (sTabs.length) {
    var sPanels = document.querySelectorAll('.selector__panel');
    // Equalise all panels to the tallest so the box never changes height
    // when switching tabs (measures hidden panels off-screen).
    var equalizeSelector = function () {
      if (sPanels.length < 2) return;
      sPanels.forEach(function (p) { p.style.minHeight = ''; });
      var max = 0;
      sPanels.forEach(function (p) {
        var hidden = !p.classList.contains('is-active');
        if (hidden) {
          p.style.display = 'grid'; p.style.visibility = 'hidden';
          p.style.position = 'absolute'; p.style.left = '0'; p.style.right = '0';
        }
        max = Math.max(max, p.offsetHeight);
        if (hidden) {
          p.style.display = ''; p.style.visibility = '';
          p.style.position = ''; p.style.left = ''; p.style.right = '';
        }
      });
      sPanels.forEach(function (p) { p.style.minHeight = max + 'px'; });
    };
    sTabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        var key = tab.getAttribute('data-panel');
        sTabs.forEach(function (t) {
          var on = t === tab;
          t.classList.toggle('is-active', on);
          t.setAttribute('aria-selected', String(on));
        });
        sPanels.forEach(function (panel) {
          panel.classList.toggle('is-active', panel.getAttribute('data-panel') === key);
        });
      });
    });
    equalizeSelector();
    window.addEventListener('load', equalizeSelector);   // re-measure once fonts/images settle
    var sEqT;
    window.addEventListener('resize', function () { clearTimeout(sEqT); sEqT = setTimeout(equalizeSelector, 150); });
  }

  /* ---- Mobile nav drawer ------------------------------------------------ */
  var toggle = document.querySelector('.nav__toggle');
  var links = document.querySelector('.nav__links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        links.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* ---- Count-up trust stats --------------------------------------------- */
  var stats = document.querySelectorAll('[data-count]');
  if (stats.length && !reduceMotion && 'IntersectionObserver' in window) {
    var countObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var target = parseFloat(el.getAttribute('data-count'));
        var suffix = el.getAttribute('data-suffix') || '';
        var prefix = el.getAttribute('data-prefix') || '';
        var dur = 1400, start = null;
        var step = function (ts) {
          if (!start) start = ts;
          var p = Math.min((ts - start) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = prefix + Math.round(target * eased) + suffix;
          if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
        countObs.unobserve(el);
      });
    }, { threshold: 0.5 });
    stats.forEach(function (el) { countObs.observe(el); });
  } else {
    stats.forEach(function (el) {
      el.textContent = (el.getAttribute('data-prefix') || '') +
        el.getAttribute('data-count') + (el.getAttribute('data-suffix') || '');
    });
  }

  /* ---- Properties filter (scales to any number of listings) ------------- */
  var fGrid = document.querySelector('[data-filter-grid]');
  if (fGrid) {
    var fSelects = [].slice.call(document.querySelectorAll('[data-filter]'));
    var fCount = document.querySelector('[data-filter-count]');
    var fEmpty = document.querySelector('[data-filter-empty]');
    var fReset = document.querySelector('[data-filter-reset]');
    var fCards = [].slice.call(fGrid.querySelectorAll('.prop-card'));
    var fTotal = fCards.length;
    var applyFilters = function () {
      var f = {};
      fSelects.forEach(function (s) { f[s.getAttribute('data-filter')] = s.value; });
      var shown = 0;
      fCards.forEach(function (card) {
        var ok = true;
        if (f.type && card.dataset.type !== f.type) ok = false;
        if (f.region && card.dataset.region !== f.region) ok = false;
        if (f.beds && parseInt(card.dataset.beds, 10) < parseInt(f.beds, 10)) ok = false;
        if (f.price) {
          var pr = parseInt(card.dataset.price, 10);
          var b = f.price.split('-');
          if (pr < parseInt(b[0], 10) || pr > parseInt(b[1], 10)) ok = false;
        }
        card.style.display = ok ? '' : 'none';
        if (ok) shown++;
      });
      if (fCount) fCount.textContent = 'Showing ' + shown + ' of ' + fTotal + ' propert' + (fTotal === 1 ? 'y' : 'ies');
      if (fEmpty) fEmpty.hidden = shown !== 0;
    };
    fSelects.forEach(function (s) { s.addEventListener('change', applyFilters); });
    if (fReset) fReset.addEventListener('click', function () {
      fSelects.forEach(function (s) { s.value = ''; });
      applyFilters();
    });
  }

  /* ---- Footer year ------------------------------------------------------ */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---- Cookie notice (essential-only; remembers dismissal) -------------- */
  var cookieBanner = document.querySelector('[data-cookie-banner]');
  if (cookieBanner) {
    var seen = false;
    try { seen = localStorage.getItem('ns-cookie-ok') === '1'; } catch (e) { seen = false; }
    if (!seen) cookieBanner.hidden = false;
    var cookieOk = cookieBanner.querySelector('[data-cookie-ok]');
    if (cookieOk) cookieOk.addEventListener('click', function () {
      cookieBanner.hidden = true;
      try { localStorage.setItem('ns-cookie-ok', '1'); } catch (e) {}
    });
  }

  /* ---- Language dropdown (stub: EN live, DE/NL coming) ------------------ */
  var langToggle = document.querySelector('[data-lang-toggle]');
  var langMenu = document.querySelector('[data-lang-menu]');
  if (langToggle && langMenu) {
    langToggle.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = langMenu.classList.toggle('is-open');
      langToggle.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('click', function () {
      langMenu.classList.remove('is-open');
      langToggle.setAttribute('aria-expanded', 'false');
    });
    langMenu.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (a && a.getAttribute('aria-disabled') === 'true') e.preventDefault();
    });
  }

  /* ---- Video gallery (click a thumbnail to load it into the player) ----- */
  var vg = document.querySelector('[data-vgallery]');
  if (vg) {
    var vgVideo = vg.querySelector('[data-vgallery-video]');
    var vgCaption = vg.querySelector('[data-vgallery-caption]');
    var vgThumbs = [].slice.call(vg.querySelectorAll('.vgallery__thumb'));
    vgThumbs.forEach(function (btn) {
      btn.addEventListener('click', function () {
        vgThumbs.forEach(function (b) { b.classList.remove('is-active'); b.setAttribute('aria-selected', 'false'); });
        btn.classList.add('is-active'); btn.setAttribute('aria-selected', 'true');
        var loop = btn.getAttribute('data-loop') === '1';
        vgVideo.src = btn.getAttribute('data-src');
        vgVideo.poster = btn.getAttribute('data-poster');
        vgVideo.loop = loop;
        vgVideo.muted = loop;                 // before/after shorts loop muted; the full clip plays with sound
        if (vgCaption) vgCaption.textContent = btn.getAttribute('data-caption');
        vgVideo.load();
        var pr = vgVideo.play();
        if (pr && pr.catch) pr.catch(function () {});
      });
    });
  }

  /* ---- Contact form -> WhatsApp or email (no backend) ------------------- */
  var form = document.getElementById('contact-form');
  if (form) {
    var WA = '34670260445';
    var MAIL = 'info@nicolasstrebel.com';
    var chosen = 'whatsapp';
    form.querySelectorAll('[data-send]').forEach(function (btn) {
      btn.addEventListener('click', function () { chosen = btn.getAttribute('data-send'); });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = (form.name.value || '').trim();
      var contact = (form.contact.value || '').trim();
      var intent = form.intent.value;
      var message = (form.message.value || '').trim();
      if (!name || !contact) {
        if (!name) form.name.focus(); else form.contact.focus();
        return;
      }
      var lines = [
        'Hello Nicolas,',
        '',
        'Name: ' + name,
        'Contact: ' + contact,
        'Enquiry: ' + intent,
        message ? '\nMessage: ' + message : ''
      ].join('\n');
      if (chosen === 'email') {
        var subject = 'Website enquiry - ' + intent;
        window.location.href = 'mailto:' + MAIL +
          '?subject=' + encodeURIComponent(subject) +
          '&body=' + encodeURIComponent(lines);
      } else {
        window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(lines), '_blank', 'noopener');
      }
    });
  }

  /* ---- Properties sort (reorder the grid client-side) ------------------- */
  var sortSel = document.querySelector('[data-sort]');
  if (sortSel && fGrid) {
    sortSel.addEventListener('change', function () {
      var v = sortSel.value;
      var cards = [].slice.call(fGrid.querySelectorAll('.prop-card'));
      cards.sort(function (a, b) {
        if (v === 'price-asc')  return ((+a.dataset.price || Infinity) - (+b.dataset.price || Infinity));
        if (v === 'price-desc') return ((+b.dataset.price || 0) - (+a.dataset.price || 0));
        if (v === 'beds-desc')  return ((+b.dataset.beds || 0) - (+a.dataset.beds || 0));
        return (+a.dataset.order) - (+b.dataset.order); // newest = original order
      });
      cards.forEach(function (c) { fGrid.appendChild(c); });
    });
  }

  /* ---- Property enquiry -> Sooprema CRM (via /api/enquiry function) ----- */
  var ef = document.querySelector('[data-enquiry-form]');
  if (ef) {
    var efEls = ef.elements;
    var efStatus = ef.querySelector('[data-enquiry-status]');
    var efBtn = ef.querySelector('[data-enquiry-submit]');
    var efShow = function (msg, ok) {
      if (!efStatus) return;
      efStatus.hidden = false;
      efStatus.textContent = msg;
      efStatus.className = 'enquiry-form__status ' + (ok ? 'is-ok' : 'is-error');
    };
    ef.addEventListener('submit', function (e) {
      e.preventDefault();
      var payload = {
        id: ef.getAttribute('data-property-id'),
        name: (efEls.name.value || '').trim(),
        email: (efEls.email.value || '').trim(),
        phone: (efEls.phone.value || '').trim(),
        message: (efEls.message.value || '').trim(),
        consent: efEls.consent.checked
      };
      if (!payload.name || !payload.email || !payload.phone) { efShow('Please fill in your name, email and phone.', false); return; }
      if (!payload.consent) { efShow('Please tick the consent box so Nicolas may reply.', false); return; }
      efBtn.disabled = true;
      efBtn.textContent = 'Sending…';
      fetch('/api/enquiry', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(payload) })
        .then(function (r) { return r.json().then(function (d) { return { ok: r.ok && d.ok, d: d }; }, function () { return { ok: false, d: {} }; }); })
        .then(function (res) {
          if (res.ok) {
            ef.reset();
            efShow('Thank you - your enquiry has gone straight to Nicolas. He will be in touch shortly.', true);
          } else {
            efShow((res.d && res.d.error ? res.d.error + ' ' : '') + 'You can also reach Nicolas on WhatsApp below.', false);
          }
        })
        .catch(function () { efShow('Something went wrong. Please use WhatsApp below.', false); })
        .then(function () { efBtn.disabled = false; efBtn.textContent = 'Send enquiry'; });
    });
  }
})();
