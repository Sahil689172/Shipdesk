# FestiveKart

> **Shop Every Celebration** — India's trusted festive e-commerce platform.

FestiveKart is the demonstration client website for **ShipDesk**, an AI-powered website modification and deployment platform. It showcases a professional Indian e-commerce experience with a familiar shopping layout, high information density, and a vibrant festive design language.

---

## What is FestiveKart?

FestiveKart is a full-featured Indian online shopping platform demo. It covers electronics, fashion, home decor, appliances, grocery, toys, beauty, and more — built around India's festive calendar: Diwali, Holi, Eid, Christmas, and beyond.

### What is ShipDesk?

ShipDesk is an agentic AI platform that modifies, improves, and deploys client websites on demand. FestiveKart is its Phase 1 demonstration website — the canvas on which ShipDesk's AI agents practice making real, reviewable UI changes.

Every file in this project is written to be **easily read and modified by an AI coding agent**:
- Semantic IDs on every major section
- Clearly commented CSS with a table of contents
- Modular JavaScript with isolated, named modules
- A `DESIGN.md` design system as the single source of truth

---

## Technologies Used

| Technology     | Version / Notes                        |
|----------------|----------------------------------------|
| HTML5          | Semantic markup, ARIA accessibility    |
| CSS3           | Custom properties (variables), Grid, Flexbox |
| JavaScript     | Vanilla ES6+, strict mode, no frameworks |
| Google Fonts   | Roboto (300, 400, 500, 700)            |

**No frameworks. No build tools. No package manager. No dependencies.**  
Open `index.html` directly in any modern browser.

---

## Project Structure

```
shipdesk-festivekart/
├── index.html          # Main HTML document — all page sections
├── style.css           # All styles — CSS variables, layout, components
├── script.js           # JavaScript — carousel, cart, search, nav modules
├── DESIGN.md           # Design system — tokens, colors, typography, layout rules
├── README.md           # This file
└── assets/
    ├── images/
    │   ├── products/   # Product images (added in Subphase 2)
    │   ├── banners/    # Hero/promotional banner images (Subphase 2)
    │   └── brand/      # Logo and brand assets (Subphase 2)
    └── icons/
        └── categories/ # Category icons (Subphase 2)
```

---

## Page Sections

The following sections are implemented in `index.html`, each with a unique ID for AI agent targeting:

| Section ID            | Description                                      |
|-----------------------|--------------------------------------------------|
| `#site-header`        | Sticky header: logo, search bar, login, cart     |
| `#category-nav`       | Horizontal scrollable product category bar       |
| `#hero-section`       | Auto-playing promotional carousel                |
| `#featured-products`  | 5-column featured product grid                   |
| `#product-categories` | Shop-by-category card grid                       |
| `#deals-section`      | Today's top deals with discount badges           |
| `#promo-banners`      | 3-column promotional banner strip                |
| `#cart-section`       | Cart empty state (foundation for Subphase 2)     |
| `#about-section`      | Brand story and key statistics                   |
| `#site-footer`        | 5-column footer with links and copyright         |

---

## Design System

All design decisions are documented in [`DESIGN.md`](./DESIGN.md).

### Key Design Tokens

| Token              | Value     | Usage                          |
|--------------------|-----------|--------------------------------|
| Primary Blue       | `#2874f0` | Header, buttons, links         |
| Brand Yellow       | `#ffe000` | Logo accent, highlights        |
| Action Orange      | `#fb641b` | CTA buttons, discounts         |
| Background         | `#ffffff` | Page and card backgrounds      |
| Page Canvas        | `#f1f3f6` | Light grey between sections    |
| Dark Text          | `#212121` | Headings, product titles       |
| Muted Text         | `#878787` | Secondary labels, meta         |
| Border             | `#f0f0f0` | Card edges, dividers           |

---

## How to Run Locally

No installation or build step required.

### Option 1 — Open directly in a browser

```
1. Navigate to shipdesk-festivekart/
2. Double-click index.html
3. The site opens in your default browser
```

### Option 2 — Use a local dev server (recommended for hot reload)

If you have VS Code with the **Live Server** extension:

```
1. Open the shipdesk-festivekart/ folder in VS Code
2. Right-click index.html → "Open with Live Server"
3. Browser opens at http://127.0.0.1:5500
```

Using Python (built-in HTTP server):

```bash
# Python 3
cd shipdesk-festivekart
python -m http.server 8080
# Visit http://localhost:8080
```

Using Node.js (npx):

```bash
cd shipdesk-festivekart
npx serve .
# Visit the URL shown in the terminal
```

---

## Development Phases

| Phase / Subphase   | Status      | Description                                      |
|--------------------|-------------|--------------------------------------------------|
| Subphase 1         | ✅ Complete  | Project foundation: HTML structure, CSS tokens, JS modules |
| Subphase 2         | 🔜 Planned   | Full visual styling, product images, real layout |
| Subphase 3         | 🔜 Planned   | Interactive features: cart, search, filters      |
| Subphase 4         | 🔜 Planned   | ShipDesk AI agent integration                    |
| Subphase 5         | 🔜 Planned   | Deployment via Cloudflare Pages                  |

---

## For AI Agents (ShipDesk)

This project is designed to be modified autonomously by ShipDesk AI agents. Before making any change:

1. **Read `DESIGN.md`** — all visual decisions must follow the design tokens.
2. **Target sections by ID** — every major section has a stable, semantic ID.
3. **CSS is commented** — each section of `style.css` has a matching heading.
4. **JS is modular** — each module (`Carousel`, `Cart`, `Search`, etc.) is independently modifiable.
5. **No framework lock-in** — all code is plain HTML/CSS/JS, readable without tooling.

---

## License

This project is a demonstration asset for ShipDesk.  
All FestiveKart branding, design, and content is original.

---

*FestiveKart — Shop Every Celebration*
