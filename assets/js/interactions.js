/* ============================================================
   DOCHMO PORTFOLIO — interactions.js
   Cursor, scroll-reveal, particles, navbar, preloader,
   skill bars, timeline, flashlight cards, scroll progress
   ============================================================ */
'use strict';

/* ─── UTILS ─────────────────────────────────────────────────── */
const qs = (s, ctx = document) => ctx.querySelector(s);
const qsa = (s, ctx = document) => [...ctx.querySelectorAll(s)];
const lerp = (a, b, t) => a + (b - a) * t;

/* ─── PRELOADER ─────────────────────────────────────────────── */
function initPreloader() {
  const loader = qs('#preloader');
  const bar = qs('#preloader-bar');
  const text = qs('#preloader-text');
  if (!loader) return;

  let progress = 0;
  const interval = setInterval(() => {
    progress += Math.random() * 18 + 4;
    if (progress >= 100) { progress = 100; clearInterval(interval); }
    bar.style.width = progress + '%';
  }, 80);

  window.addEventListener('load', () => {
    setTimeout(() => {
      clearInterval(interval);
      bar.style.width = '100%';
      setTimeout(() => {
        loader.style.opacity = '0';
        loader.style.pointerEvents = 'none';
        document.body.style.overflow = '';
        setTimeout(() => { loader.remove(); initSite(); }, 600);
      }, 350);
    }, 400);
  });

  document.body.style.overflow = 'hidden';
}

/* ─── SITE INIT (called after preloader) ──────────────────────── */
function initSite() {
  initScrollReveal();
  initSkillBars();
  initTimelineAnim();
  initCounters();
  initHeroSlices();
}

/* ─── CUSTOM CURSOR ─────────────────────────────────────────── */
function initCursor() {
  const ring = qs('#cursor-ring');
  const dot = qs('#cursor-dot');
  if (!ring || !dot) return;

  let mx = -100, my = -100;
  let rx = -100, ry = -100;
  let raf;

  document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });

  function animate() {
    rx = lerp(rx, mx, 0.14);
    ry = lerp(ry, my, 0.14);
    ring.style.left = rx + 'px';
    ring.style.top = ry + 'px';
    dot.style.left = mx + 'px';
    dot.style.top = my + 'px';
    raf = requestAnimationFrame(animate);
  }
  animate();

  /* Hover states */
  qsa('a, button, .btn, .proj-card, .skill-card, .timeline-card, [data-cursor]').forEach(el => {
    el.addEventListener('mouseenter', () => ring.classList.add('hover-active'));
    el.addEventListener('mouseleave', () => ring.classList.remove('hover-active'));
  });

  document.addEventListener('mouseleave', () => {
    ring.style.opacity = '0'; dot.style.opacity = '0';
  });
  document.addEventListener('mouseenter', () => {
    ring.style.opacity = ''; dot.style.opacity = '';
  });
}

/* ─── SCROLL PROGRESS ───────────────────────────────────────── */
function initScrollProgress() {
  const bar = qs('.scroll-progress');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const doc = document.documentElement;
    const pct = doc.scrollTop / (doc.scrollHeight - doc.clientHeight);
    bar.style.transform = `scaleX(${pct})`;
  }, { passive: true });
}

/* ─── NAVBAR SCROLL STATE ──────────────────────────────────── */
function initNavbar() {
  const nav = qs('.nav');
  if (!nav) return;
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  }, { passive: true });

  /* Active link highlight */
  const sections = qsa('section[id]');
  const navLinks = qsa('.nav-links a');
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        navLinks.forEach(a => a.classList.remove('active'));
        let targetId = entry.target.id;
        if (targetId === 'certificacao') targetId = 'sobre';
        const link = qs(`.nav-links a[href="#${targetId}"]`);
        if (link) link.classList.add('active');
      }
    });
  }, { rootMargin: '-40% 0px -55% 0px' });
  sections.forEach(s => io.observe(s));
}

/* ─── SCROLL REVEAL ─────────────────────────────────────────── */
function initScrollReveal() {
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  qsa('.sr').forEach(el => io.observe(el));

  /* Text reveal wrappers */
  const trIO = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        trIO.unobserve(entry.target);
      }
    });
  }, { threshold: 0.3 });
  qsa('.tr-wrap').forEach(el => trIO.observe(el));
}

/* ─── SKILL BARS ────────────────────────────────────────────── */
function initSkillBars() {
  const cards = qsa('.skill-card');
  if (!cards.length) return;
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const card = entry.target;
        const bar = card.querySelector('.skill-card__bar');
        if (bar) {
          const lvl = bar.dataset.level || '0.7';
          bar.style.width = (parseFloat(lvl) * 100) + '%';
          bar.classList.add('animated');
        }
        io.unobserve(card);
      }
    });
  }, { threshold: 0.2 });
  cards.forEach(c => io.observe(c));
}

/* ─── TIMELINE REVEAL ───────────────────────────────────────── */
function initTimelineAnim() {
  /* Already handled by .sr class; add extra for odd/even */
  qsa('.timeline-item').forEach((item, i) => {
    item.style.transitionDelay = (i * 0.12) + 's';
  });
}

/* ─── COUNTER ANIMATION ─────────────────────────────────────── */
function initCounters() {
  const counters = qsa('[data-count]');
  if (!counters.length) return;
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const end = parseFloat(el.dataset.count);
      const dec = el.dataset.dec || 0;
      const dur = 1800;
      const start = performance.now();
      function update(now) {
        const t = Math.min((now - start) / dur, 1);
        const ease = 1 - Math.pow(1 - t, 4);
        el.textContent = (end * ease).toFixed(dec);
        if (t < 1) requestAnimationFrame(update);
        else el.textContent = end.toFixed(dec);
      }
      requestAnimationFrame(update);
      io.unobserve(el);
    });
  }, { threshold: 0.5 });
  counters.forEach(c => io.observe(c));
}

/* ─── FLASHLIGHT CARDS ──────────────────────────────────────── */
function initFlashlight() {
  qsa('.proj-card.flashlight').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${e.clientX - rect.left}px`);
      card.style.setProperty('--my', `${e.clientY - rect.top}px`);
    });
  });
}

/* ─── CANVAS PARTICLES (hero) ──────────────── */
function initParticles() {
  const canvas = qs('#hero-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W, H, particles;

  function resize() {
    W = canvas.width = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
  }

  /* ── Floating Particle (original) ── */
  class Particle {
    constructor() { this.reset(true); }
    reset(init) {
      this.x = Math.random() * W;
      this.y = init ? Math.random() * H : H + 10;
      this.vy = -(Math.random() * 0.4 + 0.15);
      this.vx = (Math.random() - 0.5) * 0.3;
      this.size = Math.random() * 1.4 + 0.4;
      this.alpha = 0;
      this.maxAlpha = Math.random() * 0.45 + 0.15;
      this.life = 0;
      this.maxLife = Math.random() * 350 + 200;
    }
    update() {
      this.life++;
      this.x += this.vx;
      this.y += this.vy;
      const pct = this.life / this.maxLife;
      if (pct < 0.15) this.alpha = (pct / 0.15) * this.maxAlpha;
      else if (pct > 0.8) this.alpha = ((1 - pct) / 0.2) * this.maxAlpha;
      else this.alpha = this.maxAlpha;
      if (this.life > this.maxLife || this.y < -10) this.reset(false);
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(66,165,245,${this.alpha})`;
      ctx.fill();
    }
  }

  function init() {
    resize();
    const isMobile = window.innerWidth <= 768;
    const pCount = isMobile ? 20 : 90;
    particles = Array.from({ length: pCount }, () => new Particle());
  }

  function tick() {
    ctx.clearRect(0, 0, W, H);
    /* Grid lines */
    ctx.strokeStyle = 'rgba(30,136,229,0.055)';
    ctx.lineWidth = 1;
    for (let x = 0; x < W; x += 60) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
    }
    for (let y = 0; y < H; y += 60) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    }
    /* Floating particles */
    particles.forEach(p => { p.update(); p.draw(); });
    requestAnimationFrame(tick);
  }

  window.addEventListener('resize', () => { resize(); }, { passive: true });
  init();
  tick();
}

/* ─── MOBILE MENU ───────────────────────────────────────────── */
function initMobileMenu() {
  const toggle = qs('#menu-toggle');
  const menu = qs('#mobile-menu');
  const iconBurger = qs('#icon-burger');
  const iconClose = qs('#icon-close');
  if (!toggle || !menu) return;

  toggle.addEventListener('click', () => {
    const isOpen = menu.classList.toggle('open');
    toggle.setAttribute('aria-expanded', isOpen);
    if (isOpen) {
      menu.style.display = 'flex';
      if (iconBurger) iconBurger.style.display = 'none';
      if (iconClose) iconClose.style.display = 'block';
    } else {
      menu.style.display = 'none';
      if (iconBurger) iconBurger.style.display = 'block';
      if (iconClose) iconClose.style.display = 'none';
    }
  });

  qsa('#mobile-menu a').forEach(a => {
    a.addEventListener('click', () => {
      menu.classList.remove('open');
      menu.style.display = 'none';
      toggle.setAttribute('aria-expanded', 'false');
      if (iconBurger) iconBurger.style.display = 'block';
      if (iconClose) iconClose.style.display = 'none';
    });
  });
}

/* ─── CONTACT FORM ──────────────────────────────────────────── */
function initContactForm() {
  const form = qs('#contact-form');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const orig = btn.textContent;
    btn.textContent = 'Enviando...';
    btn.disabled = true;

    // Coleta os dados do formulário
    const formData = new FormData();

    // Chave de acesso do Web3Forms (web3forms.com)
    formData.append("access_key", "b367466a-89a0-40d3-856e-a08e9cc87a56");

    formData.append("name", qs('#form-name').value);
    formData.append("email", qs('#form-email').value);
    formData.append("subject", qs('#form-subject').value);
    formData.append("message", qs('#form-msg').value);

    // Permite que você clique em "Responder" no seu e-mail e vá direto pro visitante
    formData.append("replyto", qs('#form-email').value);

    try {
      const response = await fetch("https://api.web3forms.com/submit", {
        method: "POST",
        body: formData,
        headers: {
          'Accept': 'application/json'
        }
      });

      const result = await response.json();

      if (response.ok && result.success) {
        btn.textContent = 'Mensagem enviada ✓';
        setTimeout(() => { btn.textContent = orig; btn.disabled = false; form.reset(); }, 3500);
      } else {
        btn.textContent = 'Erro ao enviar. Tente novamente.';
        setTimeout(() => { btn.textContent = orig; btn.disabled = false; }, 3500);
      }
    } catch (error) {
      btn.textContent = 'Erro de conexão.';
      setTimeout(() => { btn.textContent = orig; btn.disabled = false; }, 3500);
    }
  });
}

/* ─── HERO SLICES ─────────────────────────────────────────── */
function initHeroSlices() {
  const panel = qs('#hero-slices');
  const slices = qsa('.hero-slice');
  const glassCards = qsa('.hero-stat-glass');
  if (!slices.length || !panel) return;

  /* Stagger entrance: slices reveal left-to-right, glass cards after */
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      slices.forEach((slice, i) => {
        setTimeout(() => slice.classList.add('revealed'), i * 130);
      });
      glassCards.forEach((card, i) => {
        setTimeout(() => card.classList.add('revealed'), 780 + i * 240);
      });
      io.disconnect();
    });
  }, { threshold: 0.1 });

  io.observe(panel);
}

/* ─── HERO SCROLL PARALLAX ─────────────────────────────────────── */
function initHeroScrollParallax() {
  if (window.innerWidth <= 768) return;
  if (typeof gsap === 'undefined') return;
  gsap.registerPlugin(ScrollTrigger);

  const hero = qs('#hero');
  const textSide = qs('#hero-text-side');
  const slices = qsa('.hero-slice');
  if (!hero || !textSide || slices.length === 0) return;

  // Text Side: subtle float down on scroll (no blur, no opacity drop)
  gsap.to(textSide, {
    y: 120,
    ease: 'none',
    scrollTrigger: {
      trigger: hero,
      start: 'top top',
      end: 'bottom top',
      scrub: true
    }
  });

  // Image Panel: subtle unified float down to create premium parallax without breaking the face
  const photoPanel = qs('.hero-photo-panel');
  if (photoPanel) {
    gsap.to(photoPanel, {
      y: 200,
      ease: 'none',
      scrollTrigger: {
        trigger: hero,
        start: 'top top',
        end: 'bottom top',
        scrub: true
      }
    });
  }
}


/* ─── METEOR SHOWER (GLOBAL) ────────────────────────────────── */
function initMeteors() {
  const canvas = qs('#meteor-canvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  let W, H, diagonalBeams;

  function resize() {
    W = canvas.width = window.innerWidth;
    H = canvas.height = window.innerHeight;
  }

  class DiagonalBeam {
    constructor(index = 0) { this.reset(true, index); }
    reset(init, index = 0) {
      /* =========================================
         [MANUAL TUNING] - FREQUENCY & SPEED
         ========================================= */
      /* 1. DELAY (in frames. 60 frames = 1 sec)
         Min & Max time the meteor "sleeps" off-screen before spawning.
         Higher values = less frequent meteors. */
      const minWaitFrames = 300;    // ~5 seconds minimum
      const randomWaitFrames = 420; // Up to +7 seconds extra (max ~12s)

      /* 2. SPEED
         Base speed multiplier. */
      const baseSpeed = Math.random() * 2.0 + 1.2;
      /* ========================================= */

      /* Initial spawn (init): enforce perfect stagger so they don't clump */
      if (init) {
        this.delay = index * 260 + (Math.random() * 60); 
      } else {
        this.delay = Math.random() * randomWaitFrames + minWaitFrames;
      }

      /* Fixed angle (45 degrees) */
      this.speedX = -baseSpeed * 1.0;
      this.speedY = baseSpeed * 1.0;

      /* Spawn strictly off-screen to avoid popping in */
      if (Math.random() > 0.5) {
        /* Spawn on TOP edge: spread across total width */
        this.x = Math.random() * (W + 600); 
        this.y = -(Math.random() * 200 + 50); 
      } else {
        /* Spawn on RIGHT edge: spread across total height */
        this.x = W + (Math.random() * 300 + 50); 
        this.y = Math.random() * H - 100; 
      }

      /* Longer tails for higher speed */
      this.len = Math.random() * 180 + 100;
      this.width = Math.random() * 0.6 + 0.2;
      this.alpha = 0;
      this.maxAlpha = Math.random() * 0.15 + 0.05;
      this.life = 0;
      this.maxLife = (W / Math.abs(this.speedX)) + (H / this.speedY);
    }
    update() {
      if (this.delay > 0) {
        this.delay--;
        return;
      }
      this.life++;
      this.x += this.speedX;
      this.y += this.speedY;
      const pct = this.life / this.maxLife;
      if (pct < 0.12) this.alpha = (pct / 0.12) * this.maxAlpha;
      else if (pct > 0.82) this.alpha = ((1 - pct) / 0.18) * this.maxAlpha;
      else this.alpha = this.maxAlpha;
      /* Reset if it goes off bottom or off left side */
      if (this.y > H + 80 || this.x < -80) this.reset(false);
    }
    draw() {
      if (this.delay > 0) return;
      const ratio = this.speedX / this.speedY;
      const tailX = this.x - this.len * ratio;
      const tailY = this.y - this.len;
      const grad = ctx.createLinearGradient(tailX, tailY, this.x, this.y);
      grad.addColorStop(0, `rgba(66,165,245,0)`);
      grad.addColorStop(1, `rgba(66,165,245,${this.alpha})`);
      ctx.save();
      ctx.strokeStyle = grad;
      ctx.lineWidth = this.width;
      ctx.beginPath();
      ctx.moveTo(tailX, tailY);
      ctx.lineTo(this.x, this.y);
      ctx.stroke();
      ctx.restore();
    }
  }

  function init() {
    resize();
    const isMobile = window.innerWidth <= 768;
    /* Minimalist count: 5 on PC, 2 on Mobile */
    const bCount = isMobile ? 2 : 5;
    diagonalBeams = Array.from({ length: bCount }, (v, i) => new DiagonalBeam(i));
  }

  function tick() {
    ctx.clearRect(0, 0, W, H);
    diagonalBeams.forEach(b => { b.update(); b.draw(); });
    requestAnimationFrame(tick);
  }

  window.addEventListener('resize', () => { resize(); }, { passive: true });
  init();
  tick();

  /* Intersection Observer to hide meteors in Hero section */
  const hero = qs('#hero');
  if (hero) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          canvas.style.opacity = '0';
        } else {
          canvas.style.opacity = '1';
        }
      });
    }, { threshold: 0.1 });
    io.observe(hero);
  }
}

/* ─── BOOT ──────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  initPreloader();
  initCursor();
  initScrollProgress();
  initNavbar();
  initFlashlight();
  initMobileMenu();
  initContactForm();
  initHeroScrollParallax();
  initParticles();
  initMeteors();
});
