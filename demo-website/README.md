# FestiveKart

> **Shop Every Celebration** — India's trusted festive e-commerce platform.

FestiveKart is the demonstration client website for **ShipDesk**, an AI-powered website modification and deployment platform. It showcases a professional Indian e-commerce experience with a familiar shopping layout, high information density, and a vibrant festive design language.

**Live deployment:** Cloudflare Pages (see [Deployment](#deployment) section below)

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

| Technology     | Notes                                             |
|----------------|---------------------------------------------------|
| HTML5          | Semantic markup, ARIA roles, accessibility        |
| CSS3           | Custom properties (variables), Grid, Flexbox      |
| JavaScript     | Vanilla ES6+, strict mode, no frameworks          |
| Google Fonts   | Roboto (300, 400, 500, 700) — loaded via CDN      |

**No frameworks. No build tools. No package manager. No server required.**
Open `index.html` directly in any modern browser or serve it with any static host.

---

## Project Structure

```
shipdesk-festivekart/
├── index.html              # Main HTML document — all page sections
├── style.css               # All styles — CSS variables, layout, components
├── script.js               # JavaScript — carousel, cart, search, nav modules
├── DESIGN.md               # Design system — tokens, colors, typography, rules
├── README.md               # This file
└── assets/
    ├── images/
    │   ├── products/       # Product images (earbuds, laptop, tv, etc.)
    │   ├── banners/        # Hero carousel banners (banner1–3.png)
    │   └── brand/          # Brand logo images (Apple, Nike, Adidas, HP, LOQ)
    └── icons/
        └── categories/     # Reserved for category icon assets
```

### Page Sections

Each section has a stable semantic ID for AI agent targeting:

| Section ID             | Description                                       |
|------------------------|---------------------------------------------------|
| `#site-header`         | Sticky header: logo, search bar, login, cart      |
| `#category-nav`        | Horizontal scrollable product category bar        |
| `#hero-section`        | Auto-playing image carousel (3 banner slides)     |
| `#featured-products`   | 5-column featured product grid                    |
| `#brand-section`       | Shop by brand — 5 brand logo cards                |
| `#deals-section`       | Today's top deals with discount badges            |
| `#more-products`       | Second product grid — additional products         |
| `#promo-banners`       | 3-column promotional banner strip                 |
| `#product-categories`  | Shop-by-category card grid                        |
| `#cart-section`        | Cart empty state (hidden by default)              |
| `#about-section`       | Brand story and key statistics                    |
| `#site-footer`         | 5-column footer with links and copyright          |

---

## Running Locally

No installation or build step is required.

### Option 1 — Open directly in a browser

```
1. Navigate to the shipdesk-festivekart/ folder
2. Double-click index.html
3. The site opens in your default browser
```

> Note: Some browsers restrict loading local fonts or assets via `file://`. Use a local
> server (Option 2 or 3) if any resources appear missing.

### Option 2 — VS Code Live Server (recommended)

```
1. Open the shipdesk-festivekart/ folder in VS Code
2. Install the "Live Server" extension (ritwickdey.LiveServer)
3. Right-click index.html → "Open with Live Server"
4. Browser opens at http://127.0.0.1:5500
```

### Option 3 — Python built-in server

```bash
cd shipdesk-festivekart
python -m http.server 3000
# Visit http://localhost:3000
```

### Option 4 — Node.js via npx

```bash
cd shipdesk-festivekart
npx serve .
# Visit the URL printed in the terminal
```

---

## Deployment

FestiveKart is deployed as a **static website** on **Cloudflare Pages**.

### Why Cloudflare Pages?

- Free tier supports unlimited requests and bandwidth
- Global CDN — fast delivery to users across India and worldwide
- Automatic HTTPS with custom domain support
- Git-based deploys — every push to `main` triggers a new deployment
- No server, no backend, no configuration files needed for a plain HTML site

---

### Cloudflare Pages Build Configuration

Because FestiveKart is a plain HTML/CSS/JS site with no build step, use these exact settings when creating the Cloudflare Pages project:

| Setting                  | Value                        |
|--------------------------|------------------------------|
| **Framework preset**     | `None`                       |
| **Build command**        | *(leave blank)*              |
| **Build output directory** | `/` *(root — leave blank or enter `/`)* |
| **Root directory**       | `/` *(repository root)*      |
| **Node.js version**      | Not required                 |
| **Environment variables** | None required                |

Cloudflare Pages will serve `index.html` from the repository root automatically.

---

### Step-by-Step Deployment Guide

#### Step 1 — Push to GitHub

```bash
# From inside shipdesk-festivekart/
git init
git add .
git commit -m "Initial commit – FestiveKart Phase 1"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

> Replace `<your-username>` and `<your-repo>` with your actual GitHub username and repository name.

#### Step 2 — Create a Cloudflare Pages project

1. Log in to [dash.cloudflare.com](https://dash.cloudflare.com)
2. Go to **Workers & Pages** → **Pages** → **Create a project**
3. Select **Connect to Git** → authorise GitHub → select your repository
4. On the **Build settings** screen, enter:
   - Framework preset: **None**
   - Build command: *(leave empty)*
   - Build output directory: *(leave empty)*
5. Click **Save and Deploy**

Cloudflare will clone the repository and publish `index.html` directly.

#### Step 3 — Subsequent deployments

Every `git push` to the `main` branch triggers an automatic re-deployment.

```bash
git add .
git commit -m "Your change description"
git push
```

#### Step 4 — Custom domain (optional)

1. In Cloudflare Pages → your project → **Custom domains**
2. Click **Set up a custom domain**
3. Enter your domain (e.g. `festivekart.com`)
4. Follow the DNS instructions — Cloudflare handles HTTPS automatically

---

### What Gets Deployed

Cloudflare Pages will include every file tracked by git. The following are committed and will be deployed:

```
index.html
style.css
script.js
DESIGN.md
README.md
assets/images/banners/banner1.png
assets/images/banners/banner2.png
assets/images/banners/banner3.png
assets/images/products/earbuds.png
assets/images/products/watch.png
assets/images/products/laptop.png
assets/images/products/iphone.png
assets/images/products/tv.png
assets/images/products/ps5.png
assets/images/products/fridge.png
assets/images/products/shoes.png
assets/images/products/jacket1.png
assets/images/products/jersey.png
assets/images/brand/apple.png
assets/images/brand/nike.png
assets/images/brand/addidas.png
assets/images/brand/hp.png
assets/images/brand/LOQ.png
```

The `.gitignore` is configured to **never exclude** files in `assets/`. All images are committed.

---

## Design System

All design decisions are documented in [`DESIGN.md`](./DESIGN.md).

### Key Design Tokens

| Token         | Value     | Usage                       |
|---------------|-----------|-----------------------------|
| Primary Blue  | `#2874f0` | Header, buttons, links      |
| Brand Yellow  | `#ffe000` | Logo accent, highlights     |
| Action Orange | `#fb641b` | CTA buttons, discounts      |
| Background    | `#ffffff` | Page and card backgrounds   |
| Page Canvas   | `#f1f3f6` | Light grey between sections |
| Dark Text     | `#212121` | Headings, product titles    |
| Muted Text    | `#878787` | Secondary labels, meta      |
| Border        | `#e0e0e0` | Card edges, dividers        |

---

## Development Phases

| Phase        | Status       | Description                                              |
|--------------|--------------|----------------------------------------------------------|
| Subphase 1   | ✅ Complete   | Project foundation: HTML structure, CSS tokens, JS modules |
| Subphase 2   | ✅ Complete   | Asset integration: product images, banners, brand logos, UI refinement |
| Subphase 3   | 🔜 Planned    | Interactive features: cart, search, filters              |
| Subphase 4   | 🔜 Planned    | ShipDesk AI agent integration                            |
| Subphase 5   | ✅ Complete   | Deployment via Cloudflare Pages                          |

---

## For AI Agents (ShipDesk)

This project is designed to be modified autonomously by ShipDesk AI agents. Before making any change:

1. **Read `DESIGN.md`** — all visual decisions must follow the design tokens.
2. **Target sections by ID** — every major section has a stable semantic ID.
3. **CSS is commented** — each section of `style.css` has a numbered heading.
4. **JS is modular** — `Carousel`, `Cart`, `CategoryNav`, `Search` are independently modifiable.
5. **No framework lock-in** — plain HTML/CSS/JS, no toolchain required to read or modify.
6. **Never ignore assets** — the `.gitignore` must not exclude `assets/images/` or image file types.

---

## License

This project is a demonstration asset for ShipDesk.
All FestiveKart branding, design, and content is original.

---

*FestiveKart — Shop Every Celebration*
## ShipDesk Workflow Test

This change verifies the GitHub feature branch and pull request workflow.

Task ID: SD-001
Purpose: Test Cloudflare Pages preview deployments.