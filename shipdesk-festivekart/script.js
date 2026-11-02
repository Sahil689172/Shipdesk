/**
 * FestiveKart – Main JavaScript
 * Phase 1, Subphase 1: Foundation
 *
 * PURPOSE:
 * Lightweight script to power the core FestiveKart UI interactions.
 * Follows a modular, function-based pattern with no external dependencies.
 * Each module is clearly marked and isolated for easy AI-agent modification.
 *
 * MODULES:
 *  1. App State
 *  2. DOM Utility Helpers
 *  3. Hero Carousel
 *  4. Category Navigation
 *  5. Cart (state foundation)
 *  6. Search
 *  7. Initialisation
 */

'use strict';


/* =============================================================
   1. APP STATE
   Central state object. All runtime data lives here.
   Future modules (product listing, checkout, auth) add to this.
   ============================================================= */
const AppState = {
  cart: {
    items: [],       // Array of { id, name, price, qty }
    count: 0,        // Total item count (for badge)
  },
  carousel: {
    current: 0,      // Active slide index
    total: 0,        // Set on init
    autoplayTimer: null,
    autoplayDelay: 4000, // ms
  },
  search: {
    query: '',
  },
};


/* =============================================================
   2. DOM UTILITY HELPERS
   Thin wrappers around common DOM operations.
   ============================================================= */

/**
 * Select a single element. Returns null if not found.
 * @param {string} selector - CSS selector
 * @param {Document|Element} [root=document]
 * @returns {Element|null}
 */
function $(selector, root = document) {
  return root.querySelector(selector);
}

/**
 * Select all matching elements as an Array.
 * @param {string} selector - CSS selector
 * @param {Document|Element} [root=document]
 * @returns {Element[]}
 */
function $$(selector, root = document) {
  return Array.from(root.querySelectorAll(selector));
}

/**
 * Add one or more CSS classes to an element.
 * @param {Element} el
 * @param {...string} classes
 */
function addClass(el, ...classes) {
  if (el) el.classList.add(...classes);
}

/**
 * Remove one or more CSS classes from an element.
 * @param {Element} el
 * @param {...string} classes
 */
function removeClass(el, ...classes) {
  if (el) el.classList.remove(...classes);
}

/**
 * Toggle a CSS class on an element.
 * @param {Element} el
 * @param {string} cls
 * @param {boolean} [force]
 */
function toggleClass(el, cls, force) {
  if (el) el.classList.toggle(cls, force);
}


/* =============================================================
   3. HERO CAROUSEL
   Handles slide transitions, arrow buttons, dot indicators,
   and auto-play for the hero promotional carousel.
   ============================================================= */
const Carousel = (() => {
  let track, dots, prevBtn, nextBtn;

  /**
   * Move the carousel to a specific slide index.
   * @param {number} index - Target slide index
   */
  function goToSlide(index) {
    const { total } = AppState.carousel;

    // Wrap around
    if (index < 0) index = total - 1;
    if (index >= total) index = 0;

    AppState.carousel.current = index;

    // Shift the track
    if (track) {
      track.style.transform = `translateX(-${index * 100}%)`;
    }

    // Update dot indicators
    dots.forEach((dot, i) => {
      const isActive = i === index;
      toggleClass(dot, 'active', isActive);
      dot.setAttribute('aria-selected', String(isActive));
    });
  }

  /** Advance to the next slide. */
  function next() {
    goToSlide(AppState.carousel.current + 1);
  }

  /** Go back one slide. */
  function prev() {
    goToSlide(AppState.carousel.current - 1);
  }

  /** Start the auto-play timer. */
  function startAutoplay() {
    stopAutoplay(); // clear any existing timer first
    AppState.carousel.autoplayTimer = setInterval(next, AppState.carousel.autoplayDelay);
  }

  /** Stop the auto-play timer. */
  function stopAutoplay() {
    if (AppState.carousel.autoplayTimer) {
      clearInterval(AppState.carousel.autoplayTimer);
      AppState.carousel.autoplayTimer = null;
    }
  }

  /**
   * Initialise the carousel. Queries DOM, sets up event listeners.
   * Safe to call even if carousel elements are absent from the page.
   */
  function init() {
    const carouselEl = $('#hero-carousel');
    if (!carouselEl) return;

    track   = $('#carousel-track', carouselEl);
    prevBtn = $('#carousel-prev', carouselEl);
    nextBtn = $('#carousel-next', carouselEl);
    dots    = $$('.carousel-dot', carouselEl);

    AppState.carousel.total = $$('.carousel-slide', carouselEl).length;

    if (!track || AppState.carousel.total === 0) return;

    // Arrow buttons
    if (prevBtn) prevBtn.addEventListener('click', () => { stopAutoplay(); prev(); startAutoplay(); });
    if (nextBtn) nextBtn.addEventListener('click', () => { stopAutoplay(); next(); startAutoplay(); });

    // Dot indicators
    dots.forEach((dot, i) => {
      dot.addEventListener('click', () => {
        stopAutoplay();
        goToSlide(i);
        startAutoplay();
      });
    });

    // Pause on hover / focus (accessibility)
    carouselEl.addEventListener('mouseenter', stopAutoplay);
    carouselEl.addEventListener('mouseleave', startAutoplay);
    carouselEl.addEventListener('focusin',    stopAutoplay);
    carouselEl.addEventListener('focusout',   startAutoplay);

    // Keyboard navigation when carousel is focused
    carouselEl.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft')  { stopAutoplay(); prev(); startAutoplay(); }
      if (e.key === 'ArrowRight') { stopAutoplay(); next(); startAutoplay(); }
    });

    // Start
    goToSlide(0);
    startAutoplay();
  }

  return { init, goToSlide, next, prev };
})();


/* =============================================================
   4. CATEGORY NAVIGATION
   Marks the active category when clicked and enables horizontal
   scroll on the category bar.
   ============================================================= */
const CategoryNav = (() => {
  /**
   * Initialise category link active-state toggling.
   */
  function init() {
    const links = $$('.category-link');
    if (!links.length) return;

    links.forEach((link) => {
      link.addEventListener('click', (e) => {
        // Prevent navigation in Phase 1 (no product pages yet)
        e.preventDefault();

        // Remove active from all, set on clicked
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
   Manages cart state and the cart count badge.
   Product listing pages (Subphase 2+) will call Cart.addItem().
   ============================================================= */
const Cart = (() => {
  /**
   * Update the cart count badge in the header.
   */
  function updateBadge() {
    const badge = $('#cart-count');
    if (!badge) return;

    const count = AppState.cart.count;
    badge.textContent = count > 0 ? String(count) : '';
    badge.setAttribute('data-count', String(count));
    badge.setAttribute('aria-label', `${count} item${count !== 1 ? 's' : ''} in cart`);
  }

  /**
   * Add an item to the cart.
   * @param {{ id: string, name: string, price: number }} item
   */
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

  /**
   * Remove one unit of an item from the cart.
   * @param {string} itemId
   */
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

  /**
   * Return a copy of current cart items.
   * @returns {Array}
   */
  function getItems() {
    return [...AppState.cart.items];
  }

  /**
   * Initialise the cart from any persisted state (localStorage in Phase 2+).
   */
  function init() {
    updateBadge();
  }

  return { init, addItem, removeItem, getItems };
})();


/* =============================================================
   6. SEARCH
   Foundation for search interaction. Full search results page
   will be implemented in a later subphase.
   ============================================================= */
const Search = (() => {
  /**
   * Handle the search form submission.
   * @param {SubmitEvent} e
   */
  function handleSubmit(e) {
    e.preventDefault();
    const input = $('#search-input');
    if (!input) return;

    const query = input.value.trim();
    if (!query) return;

    AppState.search.query = query;

    // Placeholder: log the query until search results page is built.
    console.info('[FestiveKart Search] Query submitted:', query);

    // TODO (Subphase 2): navigate to search results page or render inline results.
  }

  /**
   * Initialise search form event listeners.
   */
  function init() {
    const form = $('.search-form');
    if (form) form.addEventListener('submit', handleSubmit);
  }

  return { init };
})();


/* =============================================================
   7. INITIALISATION
   Entry point. Runs after the DOM is fully loaded.
   ============================================================= */
function initApp() {
  Carousel.init();
  CategoryNav.init();
  Cart.init();
  Search.init();

  console.info('[FestiveKart] App initialised successfully.');
}

// Kick off once DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
