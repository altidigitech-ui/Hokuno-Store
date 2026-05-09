/* hokuno.js — Hokuno Shopify Theme */
'use strict';

/* ============================================================
   UTILITY
   ============================================================ */
function formatMoney(cents) {
  if (typeof cents === 'string') cents = cents.replace('.', '');
  var value = (parseInt(cents, 10) / 100).toFixed(2);
  return value.replace('.', ',') + ' €';
}

/* ============================================================
   MOBILE MENU
   ============================================================ */
function initMobileMenu() {
  var toggle = document.getElementById('menu-toggle');
  var overlay = document.getElementById('mobile-menu');
  var close = document.getElementById('mobile-menu-close');
  if (!toggle || !overlay) return;

  function openMenu() {
    overlay.classList.add('open');
    document.body.classList.add('scroll-lock');
    toggle.setAttribute('aria-expanded', 'true');
  }

  function closeMenu() {
    overlay.classList.remove('open');
    document.body.classList.remove('scroll-lock');
    toggle.setAttribute('aria-expanded', 'false');
  }

  toggle.addEventListener('click', function () {
    overlay.classList.contains('open') ? closeMenu() : openMenu();
  });

  if (close) close.addEventListener('click', closeMenu);

  overlay.addEventListener('click', function (e) {
    if (e.target === overlay) closeMenu();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeMenu();
  });
}

/* ============================================================
   CART AJAX
   ============================================================ */
function updateCartCounters(count) {
  var counters = document.querySelectorAll('.cart-count');
  counters.forEach(function (el) {
    el.textContent = count;
    el.style.display = count > 0 ? 'flex' : 'none';
  });
}

function showCartNotification(title) {
  var notif = document.getElementById('cart-notification');
  if (!notif) return;
  var titleEl = notif.querySelector('.cart-notif-title');
  if (titleEl && title) titleEl.textContent = title;
  notif.classList.add('visible');
  setTimeout(function () {
    notif.classList.remove('visible');
  }, 3000);
}

function fetchCartCount() {
  fetch('/cart.js')
    .then(function (r) { return r.json(); })
    .then(function (cart) { updateCartCounters(cart.item_count); })
    .catch(function () {});
}

function addToCart(variantId, qty, title) {
  if (!variantId) return;
  var btn = document.getElementById('add-to-cart-btn');
  if (btn) {
    btn.disabled = true;
    btn.classList.add('loading');
  }

  fetch('/cart/add.js', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
    body: JSON.stringify({ id: variantId, quantity: qty || 1 })
  })
    .then(function (r) { return r.json(); })
    .then(function (item) {
      fetchCartCount();
      showCartNotification(item.title || title);
      trackAddToCart(item);
    })
    .catch(function (err) {
      console.error('Cart error', err);
    })
    .finally(function () {
      if (btn) {
        btn.disabled = false;
        btn.classList.remove('loading');
      }
    });
}

function updateQty(key, qty) {
  fetch('/cart/change.js', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Requested-With': 'XMLHttpRequest' },
    body: JSON.stringify({ id: key, quantity: qty })
  })
    .then(function (r) { return r.json(); })
    .then(function (cart) {
      updateCartCounters(cart.item_count);
      if (qty === 0) {
        var row = document.querySelector('[data-item-key="' + key + '"]');
        if (row) row.remove();
      }
      var subtotalEl = document.getElementById('cart-subtotal');
      if (subtotalEl) subtotalEl.textContent = formatMoney(cart.total_price);
      checkCartEmpty(cart);
    })
    .catch(function (err) { console.error('Update qty error', err); });
}

function checkCartEmpty(cart) {
  if (cart.item_count === 0) {
    var wrap = document.getElementById('cart-items-wrap');
    var empty = document.getElementById('cart-empty');
    if (wrap) wrap.style.display = 'none';
    if (empty) empty.style.display = 'block';
  }
}

function initCartPage() {
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-cart-remove]');
    if (btn) {
      var key = btn.dataset.cartRemove;
      if (key) updateQty(key, 0);
    }

    var plus = e.target.closest('[data-cart-plus]');
    if (plus) {
      var key = plus.dataset.cartPlus;
      var input = document.querySelector('[data-cart-qty="' + key + '"]');
      if (input) {
        var newQty = parseInt(input.value, 10) + 1;
        input.value = newQty;
        updateQty(key, newQty);
      }
    }

    var minus = e.target.closest('[data-cart-minus]');
    if (minus) {
      var key = minus.dataset.cartMinus;
      var input = document.querySelector('[data-cart-qty="' + key + '"]');
      if (input) {
        var newQty = Math.max(0, parseInt(input.value, 10) - 1);
        input.value = newQty;
        updateQty(key, newQty);
      }
    }
  });
}

/* ============================================================
   PRODUCT GALLERY
   ============================================================ */
function initGallery() {
  var main = document.getElementById('gallery-main');
  var thumbs = document.querySelectorAll('.gallery-thumb');
  if (!main || !thumbs.length) return;

  thumbs.forEach(function (thumb) {
    thumb.addEventListener('click', function () {
      thumbs.forEach(function (t) { t.classList.remove('active'); });
      thumb.classList.add('active');
      var src = thumb.dataset.src;
      var img = main.querySelector('img');
      if (img && src) {
        img.src = src;
        img.srcset = '';
      }
    });
  });

  // Swipe support
  var touchStartX = 0;
  var touchStartY = 0;
  var allSrcs = Array.from(thumbs).map(function (t) { return t.dataset.src; });
  var currentIndex = 0;

  main.addEventListener('touchstart', function (e) {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
  }, { passive: true });

  main.addEventListener('touchend', function (e) {
    var dx = e.changedTouches[0].clientX - touchStartX;
    var dy = e.changedTouches[0].clientY - touchStartY;
    if (Math.abs(dx) < Math.abs(dy) || Math.abs(dx) < 40) return;

    if (dx < 0 && currentIndex < allSrcs.length - 1) currentIndex++;
    else if (dx > 0 && currentIndex > 0) currentIndex--;

    var img = main.querySelector('img');
    if (img && allSrcs[currentIndex]) {
      img.src = allSrcs[currentIndex];
      img.srcset = '';
    }
    thumbs.forEach(function (t, i) {
      t.classList.toggle('active', i === currentIndex);
    });
  }, { passive: true });
}

/* ============================================================
   VARIANT SELECTION (product page)
   ============================================================ */
function initVariants() {
  var form = document.getElementById('product-form');
  if (!form) return;

  var variantsData = form.dataset.variants;
  if (!variantsData) return;

  var variants = JSON.parse(variantsData);
  var hiddenInput = form.querySelector('[name="id"]');
  var priceEl = document.getElementById('product-price');
  var comparePriceEl = document.getElementById('product-compare-price');
  var addBtn = document.getElementById('add-to-cart-btn');

  function getSelected() {
    var color = null;
    var size = null;
    var activeColor = form.querySelector('.color-swatch.active');
    var activeSize = form.querySelector('.size-btn.active');
    if (activeColor) color = activeColor.dataset.value;
    if (activeSize) size = activeSize.dataset.value;
    return { color: color, size: size };
  }

  function updateSelectedVariant() {
    var sel = getSelected();
    var match = null;

    for (var i = 0; i < variants.length; i++) {
      var v = variants[i];
      var opt1 = v.option1 ? v.option1.toLowerCase() : '';
      var opt2 = v.option2 ? v.option2.toLowerCase() : '';
      var opt3 = v.option3 ? v.option3.toLowerCase() : '';

      var colorMatch = !sel.color || opt1 === sel.color.toLowerCase() || opt2 === sel.color.toLowerCase() || opt3 === sel.color.toLowerCase();
      var sizeMatch = !sel.size || opt1 === sel.size.toLowerCase() || opt2 === sel.size.toLowerCase() || opt3 === sel.size.toLowerCase();

      if (colorMatch && sizeMatch) {
        match = v;
        break;
      }
    }

    if (match) {
      if (hiddenInput) hiddenInput.value = match.id;
      if (priceEl) priceEl.textContent = formatMoney(match.price);
      if (comparePriceEl) {
        if (match.compare_at_price && match.compare_at_price > match.price) {
          comparePriceEl.textContent = formatMoney(match.compare_at_price);
          comparePriceEl.style.display = 'inline';
        } else {
          comparePriceEl.style.display = 'none';
        }
      }
      if (addBtn) {
        addBtn.disabled = !match.available;
        addBtn.dataset.variantId = match.id;
      }
    } else {
      if (addBtn) addBtn.disabled = true;
    }
  }

  // Color swatches
  form.querySelectorAll('.color-swatch').forEach(function (swatch) {
    swatch.addEventListener('click', function () {
      form.querySelectorAll('.color-swatch').forEach(function (s) { s.classList.remove('active'); });
      swatch.classList.add('active');
      updateSelectedVariant();
    });
  });

  // Size buttons
  form.querySelectorAll('.size-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (btn.disabled) return;
      form.querySelectorAll('.size-btn').forEach(function (b) { b.classList.remove('active'); });
      btn.classList.add('active');
      updateSelectedVariant();
    });
  });

  updateSelectedVariant();
}

/* ============================================================
   QUANTITY +/- (product page)
   ============================================================ */
function changeQty(delta) {
  var input = document.getElementById('qty-input');
  if (!input) return;
  var val = parseInt(input.value, 10) || 1;
  val = Math.max(1, val + delta);
  input.value = val;
}

window.changeQty = changeQty;

/* ============================================================
   ADD TO CART BUTTON (product page)
   ============================================================ */
function initAddToCart() {
  var btn = document.getElementById('add-to-cart-btn');
  var form = document.getElementById('product-form');
  if (!btn || !form) return;

  btn.addEventListener('click', function (e) {
    e.preventDefault();
    var variantId = btn.dataset.variantId || form.querySelector('[name="id"]').value;
    var qty = parseInt((document.getElementById('qty-input') || {}).value || '1', 10);
    var title = form.dataset.productTitle || '';
    if (variantId) addToCart(parseInt(variantId, 10), qty, title);
  });
}

/* ============================================================
   ACCORDIONS — product page (description, infos, taille)
   ============================================================ */
function initAccordions() {
  document.querySelectorAll('.accord-header').forEach(function (header) {
    header.addEventListener('click', function () {
      var parent = header.closest('.accord-item') || header.parentElement;
      var isOpen = parent.classList.contains('open');

      // Close all siblings
      var container = parent.parentElement;
      if (container) {
        container.querySelectorAll('.accord-item').forEach(function (item) {
          item.classList.remove('open');
          var btn = item.querySelector('.accord-header');
          if (btn) btn.setAttribute('aria-expanded', 'false');
        });
      }

      if (!isOpen) {
        parent.classList.add('open');
        header.setAttribute('aria-expanded', 'true');
      }
    });

    header.setAttribute('aria-expanded', 'false');
  });
}

/* ============================================================
   FAQ ACCORDION
   ============================================================ */
function initFaq() {
  document.querySelectorAll('.faq-question').forEach(function (question) {
    question.addEventListener('click', function () {
      var item = question.closest('.faq-item') || question.parentElement;
      var isOpen = item.classList.contains('open');

      document.querySelectorAll('.faq-item').forEach(function (fi) {
        fi.classList.remove('open');
        var q = fi.querySelector('.faq-question');
        if (q) q.setAttribute('aria-expanded', 'false');
      });

      if (!isOpen) {
        item.classList.add('open');
        question.setAttribute('aria-expanded', 'true');
      }
    });

    question.setAttribute('aria-expanded', 'false');
  });
}

/* ============================================================
   WISHLIST
   ============================================================ */
function initWishlist() {
  var btn = document.getElementById('wishlist-btn');
  if (!btn) return;

  var productId = btn.dataset.productId;
  if (!productId) return;

  var key = 'hokuno_wishlist';

  function getWishlist() {
    try { return JSON.parse(localStorage.getItem(key) || '[]'); } catch (e) { return []; }
  }

  function saveWishlist(list) {
    try { localStorage.setItem(key, JSON.stringify(list)); } catch (e) {}
  }

  function updateBtn(active) {
    btn.classList.toggle('active', active);
    btn.setAttribute('aria-pressed', active ? 'true' : 'false');
  }

  var list = getWishlist();
  updateBtn(list.indexOf(productId) > -1);

  btn.addEventListener('click', function () {
    var list = getWishlist();
    var idx = list.indexOf(productId);
    if (idx > -1) {
      list.splice(idx, 1);
      updateBtn(false);
    } else {
      list.push(productId);
      updateBtn(true);
    }
    saveWishlist(list);
  });
}

/* ============================================================
   PASSWORD RECOVERY TOGGLE
   ============================================================ */
function initPasswordRecovery() {
  var loginForm = document.getElementById('customer-login-form');
  var recoverForm = document.getElementById('recover-password-form');
  var recoverLink = document.getElementById('recover-link');
  var backLink = document.getElementById('back-to-login');

  if (!loginForm || !recoverForm) return;

  function showRecover() {
    loginForm.style.display = 'none';
    recoverForm.style.display = 'block';
  }

  function showLogin() {
    recoverForm.style.display = 'none';
    loginForm.style.display = 'block';
  }

  if (window.location.hash === '#recover') showRecover();

  if (recoverLink) recoverLink.addEventListener('click', function (e) {
    e.preventDefault();
    showRecover();
    history.pushState(null, '', '#recover');
  });

  if (backLink) backLink.addEventListener('click', function (e) {
    e.preventDefault();
    showLogin();
    history.pushState(null, '', window.location.pathname);
  });
}

/* ============================================================
   COOKIE CONSENT & ANALYTICS
   ============================================================ */
var hokuno_consent = false;
window.hokuno_consent = false;

function loadAnalytics() {
  var ga4Id = window.hokuno_ga4_id;
  var metaId = window.hokuno_meta_pixel_id;
  var tiktokId = window.hokuno_tiktok_pixel_id;

  // GA4
  if (ga4Id) {
    var s1 = document.createElement('script');
    s1.async = true;
    s1.src = 'https://www.googletagmanager.com/gtag/js?id=' + ga4Id;
    document.head.appendChild(s1);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', ga4Id, { anonymize_ip: true });
  }

  // Meta Pixel
  if (metaId) {
    (function (f, b, e, v, n, t, s) {
      if (f.fbq) return;
      n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
      if (!f._fbq) f._fbq = n;
      n.push = n; n.loaded = true; n.version = '2.0'; n.queue = [];
      t = b.createElement(e); t.async = true; t.src = v;
      s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
    }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js'));
    window.fbq('init', metaId);
    window.fbq('track', 'PageView');
  }

  // TikTok Pixel
  if (tiktokId) {
    (function (w, d, t) {
      w.TiktokAnalyticsObject = t;
      var ttq = w[t] = w[t] || [];
      ttq.methods = ['page','track','identify','instances','debug','on','off','once','ready','alias','group','enableCookie','disableCookie'];
      ttq.setAndDefer = function (t, e) { t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))); }; };
      for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]);
      ttq.instance = function (t) { for (var e = ttq._i[t] || [], n = 0; n < ttq.methods.length; n++) ttq.setAndDefer(e, ttq.methods[n]); return e; };
      ttq.load = function (e, n) { var i = 'https://analytics.tiktok.com/i18n/pixel/events.js'; ttq._i = ttq._i || {}; ttq._i[e] = []; ttq._i[e]._u = i; ttq._t = ttq._t || {}; ttq._t[e] = +new Date; ttq._o = ttq._o || {}; ttq._o[e] = n || {}; var o = document.createElement('script'); o.type = 'text/javascript'; o.async = true; o.src = i + '?sdkid=' + e + '&lib=' + t; var a = document.getElementsByTagName('script')[0]; a.parentNode.insertBefore(o, a); };
      ttq.load(tiktokId);
      ttq.page();
    }(window, document, 'ttq'));
  }

  hokuno_consent = true;
  window.hokuno_consent = true;
}

function acceptCookies() {
  try { localStorage.setItem('hokuno_cookies', 'accepted'); } catch (e) {}
  var banner = document.getElementById('cookie-banner');
  if (banner) banner.style.display = 'none';
  loadAnalytics();
}

function refuseCookies() {
  try { localStorage.setItem('hokuno_cookies', 'refused'); } catch (e) {}
  var banner = document.getElementById('cookie-banner');
  if (banner) banner.style.display = 'none';
}

window.acceptCookies = acceptCookies;
window.refuseCookies = refuseCookies;

function initCookieBanner() {
  var consent;
  try { consent = localStorage.getItem('hokuno_cookies'); } catch (e) {}

  if (consent === 'accepted') {
    loadAnalytics();
    return;
  }

  if (consent === 'refused') return;

  // Show banner after short delay
  setTimeout(function () {
    var banner = document.getElementById('cookie-banner');
    if (banner) banner.style.display = 'flex';
  }, 1000);
}

/* ============================================================
   ANALYTICS HELPERS
   ============================================================ */
function trackEvent(eventName, params) {
  if (!window.hokuno_consent) return;
  if (window.gtag) window.gtag('event', eventName, params || {});
}

function trackMeta(eventName, params) {
  if (!window.hokuno_consent) return;
  if (window.fbq) window.fbq('track', eventName, params || {});
}

function trackTikTok(eventName, params) {
  if (!window.hokuno_consent) return;
  if (window.ttq) window.ttq.track(eventName, params || {});
}

function trackAddToCart(item) {
  trackEvent('add_to_cart', {
    currency: 'EUR',
    value: item.price / 100,
    items: [{ item_id: item.variant_id, item_name: item.title, price: item.price / 100, quantity: item.quantity }]
  });
  trackMeta('AddToCart', { content_ids: [item.variant_id], content_name: item.title, value: item.price / 100, currency: 'EUR' });
  trackTikTok('AddToCart', { content_id: item.variant_id, content_name: item.title, value: item.price / 100, currency: 'EUR' });
}

window.trackEvent = trackEvent;
window.trackMeta = trackMeta;
window.trackTikTok = trackTikTok;

/* ============================================================
   SCROLL ANIMATIONS (IntersectionObserver)
   ============================================================ */
function initScrollAnimations() {
  if (!window.IntersectionObserver) return;

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.animate-on-scroll').forEach(function (el) {
    observer.observe(el);
  });
}

/* ============================================================
   SEARCH
   ============================================================ */
function initSearchToggle() {
  var openBtn = document.getElementById('search-open');
  var closeBtn = document.getElementById('search-close');
  var searchWrap = document.getElementById('search-overlay');
  if (!openBtn || !searchWrap) return;

  openBtn.addEventListener('click', function () {
    searchWrap.classList.add('open');
    var input = searchWrap.querySelector('input[type="search"]');
    if (input) setTimeout(function () { input.focus(); }, 100);
  });

  if (closeBtn) closeBtn.addEventListener('click', function () {
    searchWrap.classList.remove('open');
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') searchWrap.classList.remove('open');
  });
}

/* ============================================================
   COLLECTION FILTER & SORT
   ============================================================ */
function initCollectionFilter() {
  var sortSelect = document.getElementById('sort-select');
  if (sortSelect) {
    sortSelect.addEventListener('change', function () {
      var url = new URL(window.location.href);
      url.searchParams.set('sort_by', sortSelect.value);
      window.location.href = url.toString();
    });
  }

  // Active filter tags
  document.querySelectorAll('[data-filter-tag]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var tag = btn.dataset.filterTag;
      var url = new URL(window.location.href);
      var params = url.searchParams;
      var existing = params.get('constraint') || '';
      if (existing === tag) {
        params.delete('constraint');
        btn.classList.remove('active');
      } else {
        params.set('constraint', tag);
        document.querySelectorAll('[data-filter-tag]').forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
      }
      window.location.href = url.toString();
    });
  });
}

/* ============================================================
   SHIPPING PROGRESS BAR (cart)
   ============================================================ */
function initShippingProgress() {
  var bar = document.getElementById('shipping-progress-bar');
  var msg = document.getElementById('shipping-progress-msg');
  if (!bar) return;

  var threshold = window.hokuno_free_shipping_threshold || 7000; // 70 EUR in cents
  var current = parseInt(bar.dataset.cartTotal || '0', 10);
  var pct = Math.min(100, Math.round((current / threshold) * 100));
  bar.style.width = pct + '%';

  if (msg) {
    if (pct >= 100) {
      msg.textContent = msg.dataset.free || 'Livraison offerte !';
    } else {
      var remaining = formatMoney(threshold - current);
      var tpl = msg.dataset.remaining || 'Plus que {amount} pour la livraison offerte';
      msg.textContent = tpl.replace('{amount}', remaining);
    }
  }
}

/* ============================================================
   LANGUAGE SELECTOR
   ============================================================ */
function initLangSelector() {
  var btn = document.getElementById('lang-btn');
  var dropdown = document.getElementById('lang-dropdown');
  if (!btn || !dropdown) return;

  btn.addEventListener('click', function (e) {
    e.stopPropagation();
    dropdown.classList.toggle('open');
  });

  document.addEventListener('click', function () {
    dropdown.classList.remove('open');
  });
}

/* ============================================================
   TOAST / NOTIFICATION CLOSE
   ============================================================ */
function initNotificationClose() {
  var notif = document.getElementById('cart-notification');
  if (!notif) return;
  var close = notif.querySelector('.cart-notif-close');
  if (close) {
    close.addEventListener('click', function () {
      notif.classList.remove('visible');
    });
  }
}

/* ============================================================
   IMAGE LAZY LOAD FALLBACK
   ============================================================ */
function initLazyImages() {
  if ('loading' in HTMLImageElement.prototype) return; // native lazy load supported
  if (!window.IntersectionObserver) return;

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        var img = entry.target;
        if (img.dataset.src) { img.src = img.dataset.src; delete img.dataset.src; }
        if (img.dataset.srcset) { img.srcset = img.dataset.srcset; delete img.dataset.srcset; }
        observer.unobserve(img);
      }
    });
  });

  document.querySelectorAll('img[data-src]').forEach(function (img) { observer.observe(img); });
}

/* ============================================================
   BACK TO TOP
   ============================================================ */
function initBackToTop() {
  var btn = document.getElementById('back-to-top');
  if (!btn) return;

  window.addEventListener('scroll', function () {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });

  btn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

/* ============================================================
   HERO PARALLAX (subtle)
   ============================================================ */
function initHeroParallax() {
  var hero = document.getElementById('hero');
  if (!hero) return;
  if (window.matchMedia('(max-width: 768px)').matches) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  window.addEventListener('scroll', function () {
    var y = window.scrollY;
    var bg = hero.querySelector('.hero-bg');
    if (bg) bg.style.transform = 'translateY(' + (y * 0.3) + 'px)';
  }, { passive: true });
}

/* ============================================================
   INIT
   ============================================================ */
document.addEventListener('DOMContentLoaded', function () {
  fetchCartCount();
  initMobileMenu();
  initCartPage();
  initGallery();
  initVariants();
  initAddToCart();
  initAccordions();
  initFaq();
  initWishlist();
  initPasswordRecovery();
  initCookieBanner();
  initScrollAnimations();
  initSearchToggle();
  initCollectionFilter();
  initShippingProgress();
  initLangSelector();
  initNotificationClose();
  initLazyImages();
  initBackToTop();
  initHeroParallax();
});
