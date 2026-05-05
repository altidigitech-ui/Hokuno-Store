/* Hokuno — Custom Theme JS */

(function() {
  'use strict';

  // ── Particles ──────────────────────────────────────────────
  function initParticles() {
    const canvas = document.getElementById('hk-particles');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let particles = [];
    let W, H, raf;

    function resize() {
      W = canvas.width = window.innerWidth;
      H = canvas.height = window.innerHeight;
    }

    function Particle() {
      this.reset();
    }

    Particle.prototype.reset = function() {
      this.x = Math.random() * W;
      this.y = Math.random() * H;
      this.r = Math.random() * 1.5 + 0.3;
      this.speed = Math.random() * 0.3 + 0.1;
      this.angle = Math.random() * Math.PI * 2;
      this.opacity = Math.random() * 0.5 + 0.1;
      this.drift = (Math.random() - 0.5) * 0.002;
    };

    Particle.prototype.update = function() {
      this.angle += this.drift;
      this.x += Math.cos(this.angle) * this.speed;
      this.y -= this.speed * 0.5;
      if (this.y < -10 || this.x < -10 || this.x > W + 10) this.reset();
    };

    Particle.prototype.draw = function() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(212, 168, 83, ${this.opacity})`;
      ctx.fill();
    };

    function init() {
      particles = [];
      const count = Math.min(80, Math.floor((W * H) / 15000));
      for (let i = 0; i < count; i++) particles.push(new Particle());
    }

    function loop() {
      ctx.clearRect(0, 0, W, H);
      particles.forEach(p => { p.update(); p.draw(); });
      raf = requestAnimationFrame(loop);
    }

    window.addEventListener('resize', () => { resize(); init(); });
    resize();
    init();
    loop();
  }

  // ── Header scroll behavior ──────────────────────────────────
  function initHeader() {
    const header = document.querySelector('.hk-header');
    if (!header) return;
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 40);
    }, { passive: true });
  }

  // ── Mobile menu ────────────────────────────────────────────
  function initMobileMenu() {
    const burger = document.querySelector('.hk-burger');
    const menu = document.querySelector('.hk-mobile-menu');
    if (!burger || !menu) return;

    burger.addEventListener('click', () => {
      const open = burger.classList.toggle('open');
      if (open) {
        menu.classList.add('open');
        document.body.style.overflow = 'hidden';
      } else {
        menu.classList.remove('open');
        document.body.style.overflow = '';
      }
    });

    menu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        burger.classList.remove('open');
        menu.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  // ── Product gallery ────────────────────────────────────────
  function initGallery() {
    const main = document.querySelector('.hk-gallery-main img');
    if (!main) return;

    const thumbs = document.querySelectorAll('.hk-gallery-thumb');
    const navEl = document.querySelector('.hk-gallery-nav');
    let current = 0;
    const total = thumbs.length;

    function activate(idx) {
      if (idx < 0 || idx >= total) return;
      current = idx;
      thumbs.forEach((t, i) => {
        t.classList.toggle('active', i === current);
        if (i === current) {
          const src = t.querySelector('img').src;
          main.src = src;
          if (navEl) navEl.querySelector('.hk-nav-cur').textContent = String(current + 1).padStart(2, '0');
        }
      });
    }

    thumbs.forEach((t, i) => {
      t.addEventListener('click', () => activate(i));
    });

    // Swipe support on main image
    let touchStart = 0;
    main.parentElement.addEventListener('touchstart', e => { touchStart = e.touches[0].clientX; }, { passive: true });
    main.parentElement.addEventListener('touchend', e => {
      const diff = touchStart - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 40) activate(diff > 0 ? current + 1 : current - 1);
    });

    activate(0);
  }

  // ── Size selector ──────────────────────────────────────────
  function initSizeSelector() {
    document.querySelectorAll('.hk-size-btn:not(.unavailable)').forEach(btn => {
      btn.addEventListener('click', () => {
        btn.closest('.hk-size-grid').querySelectorAll('.hk-size-btn').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
      });
    });
  }

  // ── 3D card hover ──────────────────────────────────────────
  function initCardTilt() {
    document.querySelectorAll('.hk-product-card').forEach(card => {
      card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const x = ((e.clientX - rect.left) / rect.width - 0.5) * 8;
        const y = ((e.clientY - rect.top) / rect.height - 0.5) * -8;
        card.style.transform = `translateY(-4px) rotateY(${x}deg) rotateX(${y}deg)`;
      });
      card.addEventListener('mouseleave', () => {
        card.style.transform = '';
      });
    });
  }

  // ── Collection filters ─────────────────────────────────────
  function initFilters() {
    document.querySelectorAll('.hk-filter-tag').forEach(tag => {
      tag.addEventListener('click', () => {
        document.querySelectorAll('.hk-filter-tag').forEach(t => t.classList.remove('active'));
        tag.classList.add('active');
      });
    });
  }

  // ── Scroll reveal ──────────────────────────────────────────
  function initScrollReveal() {
    if (!window.IntersectionObserver) return;
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('hk-revealed');
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.hk-reveal').forEach(el => obs.observe(el));
  }

  // ── Smooth anchor scroll ───────────────────────────────────
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(a => {
      a.addEventListener('click', e => {
        const target = document.querySelector(a.getAttribute('href'));
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  // ── Newsletter form ────────────────────────────────────────
  function initNewsletter() {
    const forms = document.querySelectorAll('.hk-newsletter-form');
    forms.forEach(form => {
      form.addEventListener('submit', e => {
        e.preventDefault();
        const input = form.querySelector('.hk-newsletter-input');
        const btn = form.querySelector('.hk-newsletter-btn');
        if (!input || !input.value) return;
        btn.textContent = '✓';
        btn.style.background = '#27ae60';
        input.value = '';
        setTimeout(() => {
          btn.textContent = 'OK';
          btn.style.background = '';
        }, 3000);
      });
    });
  }

  // ── ATC feedback ──────────────────────────────────────────
  function initATC() {
    document.querySelectorAll('.hk-atc-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const orig = btn.innerHTML;
        btn.innerHTML = '✓ Ajouté';
        btn.style.background = '#27ae60';
        setTimeout(() => {
          btn.innerHTML = orig;
          btn.style.background = '';
        }, 2000);
      });
    });
  }

  // ── Bottom nav active state ────────────────────────────────
  function initBottomNav() {
    const path = window.location.pathname;
    document.querySelectorAll('.hk-bottom-nav-item[href]').forEach(item => {
      if (item.getAttribute('href') === path || (path === '/' && item.dataset.page === 'home')) {
        item.classList.add('active');
      }
    });
  }

  // ── Lang switcher ──────────────────────────────────────────
  function initLang() {
    const btns = document.querySelectorAll('.hk-header-lang');
    const locale = document.documentElement.lang || 'fr';
    btns.forEach(btn => {
      if (btn.dataset.lang === locale.substring(0, 2)) btn.classList.add('active');
    });
  }

  // ── Init all ──────────────────────────────────────────────
  function init() {
    initParticles();
    initHeader();
    initMobileMenu();
    initGallery();
    initSizeSelector();
    initCardTilt();
    initFilters();
    initScrollReveal();
    initSmoothScroll();
    initNewsletter();
    initATC();
    initBottomNav();
    initLang();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
