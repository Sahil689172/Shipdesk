/**
 * FestiveKart – Main JavaScript
 * Phase 1, Subphase 2: Asset Integration & UI Refinement
 *
 * MODULES:
 *  1. App State
 *  2. DOM Utility Helpers
 *  3. Hero Carousel  (updated: 3 image-based slides)
 *  4. Category Navigation
 *  5. Cart
 *  6. Search
 *  7. Initialisation
 */

'use strict';


/* =============================================================
   1. APP STATE
   ============================================================= */
const AppState = {
  cart: {
    items: [],   // { id, name, price, qty }
    count: 0,
  },
  carousel: {
    current: 0,
    total: 0,
    autoplayTimer: null,
    autoplayDelay: 4500, // ms – slightly longer for image banners
  },
  search: {
    query: '',
  },
};


/* =============================================================
   2. DOM UTILITY HELPERS
   ============================================================= */

/** Select one element */
function $(selector, root = document) {
  return root.querySelector(selector);
}

/** Select all elements as an Array */
function $$(selector, root = document) {
  return Array.from(root.querySelectorAll(selector));
}

function addClass(el, ...classes)        { if (el) el.classList.add(...classes); }
function removeClass(el, ...classes)     { if (el) el.classList.remove(...classes); }
function toggleClass(el, cls, force)     { if (el) el.classList.toggle(cls, force); }


/* =============================================================
   3. HERO CAROUSEL
   Works with both image slides (Subphase 2) and any future
   content slides. Slide count is detected from the DOM.
   ============================================================= */
const Carousel = (() => {
  let track, dots, prevBtn, nextBtn;

  /**
   * Go to a specific slide index (wraps around).
   * @param {number} index
   */
  function goToSlide(index) {
    const { total } = AppState.carousel;
    if (total === 0) return;

    // Wrap
    if (index < 0) index = total - 1;
    if (index >= total) index = 0;

    AppState.carousel.current = index;

    if (track) {
      track.style.transform = `translateX(-${index * 100}%)`;
    }

    dots.forEach((dot, i) => {
      const active = i === index;
      toggleClass(dot, 'active', active);
      dot.setAttribute('aria-selected', String(active));
    });
  }

  function next() { goToSlide(AppState.carousel.current + 1); }
  function prev() { goToSlide(AppState.carousel.current - 1); }

  function startAutoplay() {
    stopAutoplay();
    AppState.carousel.autoplayTimer = setInterval(next, AppState.carousel.autoplayDelay);
  }

  function stopAutoplay() {
    if (AppState.carousel.autoplayTimer) {
      clearInterval(AppState.carousel.autoplayTimer);
      AppState.carousel.autoplayTimer = null;
    }
  }

  function init() {
    const carouselEl = $('#hero-carousel');
    if (!carouselEl) return;

    track   = $('#carousel-track', carouselEl);
    prevBtn = $('#carousel-prev', carouselEl);
    nextBtn = $('#carousel-next', carouselEl);
    dots    = $$('.carousel-dot', carouselEl);

    AppState.carousel.total = $$('.carousel-slide', carouselEl).length;
    if (!track || AppState.carousel.total === 0) return;

    // Arrow controls
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        stopAutoplay(); prev(); startAutoplay();
      });
    }
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        stopAutoplay(); next(); startAutoplay();
      });
    }

    // Dot controls
    dots.forEach((dot, i) => {
      dot.addEventListener('click', () => {
        stopAutoplay(); goToSlide(i); startAutoplay();
      });
    });

    // Pause autoplay on hover / focus (accessibility)
    carouselEl.addEventListener('mouseenter', stopAutoplay);
    carouselEl.addEventListener('mouseleave', startAutoplay);
    carouselEl.addEventListener('focusin',    stopAutoplay);
    carouselEl.addEventListener('focusout',   startAutoplay);

    // Keyboard arrow navigation
    carouselEl.setAttribute('tabindex', '0');
    carouselEl.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft')  { stopAutoplay(); prev(); startAutoplay(); }
      if (e.key === 'ArrowRight') { stopAutoplay(); next(); startAutoplay(); }
    });

    // Touch / swipe support
    let touchStartX = 0;
    carouselEl.addEventListener('touchstart', (e) => {
      touchStartX = e.touches[0].clientX;
    }, { passive: true });
    carouselEl.addEventListener('touchend', (e) => {
      const delta = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(delta) > 40) {
        stopAutoplay();
        if (delta < 0) next(); else prev();
        startAutoplay();
      }
    }, { passive: true });

    goToSlide(0);
    startAutoplay();
  }

  return { init, goToSlide, next, prev };
})();


/* =============================================================
   4. CATEGORY NAVIGATION
   ============================================================= */
const CategoryNav = (() => {
  function init() {
    const links = $$('.category-link');
    if (!links.length) return;

    links.forEach((link) => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        links.forEach((l) => {
          removeClass(l, 'active');
          l.removeAttribute('aria-current');
        });
        addClass(link, 'active');
        link.setAttribute('aria-current', 'page');
      });
    });
  }

  return { init };
})();


/* =============================================================
   5. CART
   ============================================================= */
const Cart = (() => {
  function updateBadge() {
    const badge = $('#cart-count');
    if (!badge) return;
    const count = AppState.cart.count;
    badge.textContent = count > 0 ? String(count) : '';
    badge.setAttribute('data-count', String(count));
    badge.setAttribute('aria-label', `${count} item${count !== 1 ? 's' : ''} in cart`);
  }

  function addItem(item) {
    const existing = AppState.cart.items.find((i) => i.id === item.id);
    if (existing) {
      existing.qty += 1;
    } else {
      AppState.cart.items.push({ ...item, qty: 1 });
    }
    AppState.cart.count += 1;
    updateBadge();
  }

  function removeItem(itemId) {
    const idx = AppState.cart.items.findIndex((i) => i.id === itemId);
    if (idx === -1) return;
    const item = AppState.cart.items[idx];
    if (item.qty > 1) {
      item.qty -= 1;
    } else {
      AppState.cart.items.splice(idx, 1);
    }
    AppState.cart.count = Math.max(0, AppState.cart.count - 1);
    updateBadge();
  }

  function getItems() { return [...AppState.cart.items]; }

  function init() { updateBadge(); }

  return { init, addItem, removeItem, getItems };
})();


/* =============================================================
   6. SEARCH
   ============================================================= */
const Search = (() => {
  function handleSubmit(e) {
    e.preventDefault();
    const input = $('#search-input');
    if (!input) return;
    const query = input.value.trim();
    if (!query) return;
    AppState.search.query = query;
    console.info('[FestiveKart Search] Query submitted:', query);
    // TODO (Subphase 3): navigate to search results or render inline.
  }

  function init() {
    const form = $('.search-form');
    if (form) form.addEventListener('submit', handleSubmit);
  }

  return { init };
})();


/* =============================================================
   7. INITIALISATION
   ============================================================= */
function initApp() {
  Carousel.init();
  CategoryNav.init();
  Cart.init();
  Search.init();
  console.info('[FestiveKart] App initialised successfully.');
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
