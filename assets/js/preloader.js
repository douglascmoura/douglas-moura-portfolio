/**
 * DOCHMO PORTFOLIO — preloader.js
 * Ultra-Smooth & Premium Velvet Preloader Controller
 * Manages 3-phase typography animation (DCM -> DOCHMO), progress bar, session state & GSAP triggers.
 */

(function () {
  'use strict';

  function runPreloader() {
    const preloader = document.getElementById('dochmo-preloader');
    if (!preloader) return;

    // Session check and page reload detection
    const isReload = (function () {
      try {
        const navEntries = performance.getEntriesByType('navigation');
        if (navEntries.length > 0) {
          return navEntries[0].type === 'reload';
        }
        return performance.navigation.type === 1;
      } catch (e) {
        return false;
      }
    })();

    const hasSeenPreloader = sessionStorage.getItem('dochmo_preloaded');
    const forcePreload = window.location.search.includes('force_preloader=1');

    // Skip preloader if already seen in current session, unless explicit F5 or query force
    if (hasSeenPreloader && !isReload && !forcePreload) {
      preloader.style.display = 'none';
      if (document.body) document.body.classList.remove('preloader-active');
      if (window.ScrollTrigger) window.ScrollTrigger.refresh();
      return;
    }

    // Persist preloader state in session storage
    try {
      sessionStorage.setItem('dochmo_preloaded', 'true');
    } catch (e) {}

    if (document.body) document.body.classList.add('preloader-active');

    const fillEl = document.getElementById('preloader-fill');
    const counterEl = document.getElementById('preloader-counter');
    const subEl = document.querySelector('.preloader-sub');

    const charD = preloader.querySelector('.char-d');
    const charO1 = preloader.querySelector('.char-o');
    const charC = preloader.querySelector('.char-c');
    const charH = preloader.querySelector('.char-h');
    const charM = preloader.querySelector('.char-m');
    const charO2 = preloader.querySelector('.char-o2');

    // ─── 1. PROGRESS BAR & COUNTER (0% -> 100%) ──────────────────────
    let progress = 0;
    const duration = 2650; // Total animation duration in ms
    const startTime = performance.now();

    function updateProgress(now) {
      const elapsed = now - startTime;
      progress = Math.min(Math.floor((elapsed / duration) * 100), 100);

      if (fillEl) fillEl.style.width = `${progress}%`;
      if (counterEl) counterEl.textContent = `${progress}%`;

      if (progress < 100) {
        requestAnimationFrame(updateProgress);
      }
    }
    requestAnimationFrame(updateProgress);

    // ─── 2. 3-PHASE VELVET BRAND TYPOGRAPHY SEQUENCE ──────────────

    // Stage 0 (0ms): Initial centered cluster for D, C, M with soft fog blur
    [charD, charC, charM].forEach((el) => {
      if (el) el.classList.add('char-fade-entry');
    });

    [charO1, charH, charO2].forEach((el) => {
      if (el) {
        el.classList.add('char-hidden-veil');
        el.classList.remove('char-reveal-veil');
      }
    });

    if (charM) charM.classList.add('char-accent');
    if (charO2) charO2.classList.add('char-accent');

    // Initial character entry
    setTimeout(() => {
      [charD, charC, charM].forEach((el) => {
        if (el) el.classList.remove('char-fade-entry');
      });
    }, 180);

    // Stage 2 (650ms): Smooth 1.3s decelerated expansion & unveil of O, H, O
    setTimeout(() => {
      [charO1, charH, charO2].forEach((el) => {
        if (el) {
          el.classList.add('char-reveal-veil');
          el.classList.remove('char-hidden-veil');
        }
      });
    }, 650);

    // Stage 3 (1100ms): Subtitle fade-in while logo unveils
    setTimeout(() => {
      if (subEl) {
        subEl.classList.add('sub-visible');
      }
    }, 1100);

    // ─── 3. PRELOADER EXIT & GSAP REFRESH (2850ms) ───────────────
    setTimeout(() => {
      preloader.classList.add('preloader-hidden');
      if (document.body) document.body.classList.remove('preloader-active');

      if (window.ScrollTrigger) {
        window.ScrollTrigger.refresh();
      }

      setTimeout(() => {
        preloader.style.display = 'none';
      }, 950);
    }, 2850);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runPreloader);
  } else {
    runPreloader();
  }
})();
