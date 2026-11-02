# FestiveKart – Design System

This document defines the canonical design tokens, layout conventions, and visual language for FestiveKart.
It is the single source of truth for all UI implementation decisions.
All agents, developers, and AI tools working on this project must read and follow this document first.

---

## 1. Brand Identity

| Property       | Value                                      |
|----------------|--------------------------------------------|
| Brand Name     | FestiveKart                                |
| Tagline        | Shop Every Celebration                     |
| Category       | Indian e-commerce platform                 |
| Tone           | Trustworthy, vibrant, familiar, accessible |

---

## 2. Color Palette

### Primary Colors

| Token                  | Variable Name              | Hex Value  | Usage                                  |
|------------------------|----------------------------|------------|----------------------------------------|
| Primary Blue           | `--color-primary`          | `#2874f0`  | Header background, primary buttons, links |
| Brand Yellow           | `--color-yellow`           | `#ffe000`  | Logo accent, highlights, badges        |
| Action Orange          | `--color-action`           | `#fb641b`  | CTA buttons, "Add to Cart", sale badges |

### Neutral Colors

| Token                  | Variable Name              | Hex Value  | Usage                                  |
|------------------------|----------------------------|------------|----------------------------------------|
| White Background       | `--color-bg`               | `#ffffff`  | Page background, card backgrounds      |
| Dark Foreground        | `--color-text-primary`     | `#212121`  | Headings, product titles, body text    |
| Muted Text             | `--color-text-muted`       | `#878787`  | Secondary labels, descriptions, meta   |
| Thin Border            | `--color-border`           | `#f0f0f0`  | Card borders, dividers, separators     |
| Light Gray Background  | `--color-bg-light`         | `#f1f3f6`  | Page canvas, section backgrounds       |
| Hover State            | `--color-hover`            | `#e8f0fe`  | Nav item hover, button hover states    |

### Semantic Colors

| Token                  | Variable Name              | Hex Value  | Usage                                  |
|------------------------|----------------------------|------------|----------------------------------------|
| Success Green          | `--color-success`          | `#388e3c`  | In-stock labels, success messages      |
| Warning Amber          | `--color-warning`          | `#ff6f00`  | Low stock, cautionary badges           |
| Error Red              | `--color-error`            | `#d32f2f`  | Out-of-stock, error messages           |
| Rating Star Gold       | `--color-rating`           | `#ff9f00`  | Star ratings                           |

---

## 3. Typography

### Font Stack

```css
font-family: 'Roboto', 'Helvetica Neue', Arial, sans-serif;
```

Google Fonts import: `https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap`

### Type Scale

| Token              | Variable Name           | Size    | Weight | Usage                         |
|--------------------|-------------------------|---------|--------|-------------------------------|
| Display            | `--text-display`        | 24px    | 700    | Hero section headings         |
| Heading Large      | `--text-heading-lg`     | 20px    | 700    | Section titles                |
| Heading Medium     | `--text-heading-md`     | 16px    | 700    | Card titles, product names    |
| Heading Small      | `--text-heading-sm`     | 14px    | 500    | Sub-section labels            |
| Body               | `--text-body`           | 14px    | 400    | General content               |
| Body Small         | `--text-body-sm`        | 12px    | 400    | Meta, descriptions, captions  |
| Caption            | `--text-caption`        | 11px    | 400    | Labels, badges, fine print    |

---

## 4. Spacing System

Uses an 8px base grid.

| Token              | Variable Name      | Value  | Usage                              |
|--------------------|--------------------|--------|------------------------------------|
| Spacing XS         | `--space-xs`       | 4px    | Tight inner padding, icon gaps     |
| Spacing SM         | `--space-sm`       | 8px    | Component inner padding            |
| Spacing MD         | `--space-md`       | 16px   | Standard section padding           |
| Spacing LG         | `--space-lg`       | 24px   | Card padding, larger gaps          |
| Spacing XL         | `--space-xl`       | 32px   | Section gaps                       |
| Spacing XXL        | `--space-xxl`      | 48px   | Major section separation           |

---

## 5. Border & Radius

| Token              | Variable Name        | Value   | Usage                             |
|--------------------|----------------------|---------|-----------------------------------|
| Radius None        | `--radius-none`      | 0px     | Sharp elements                    |
| Radius SM          | `--radius-sm`        | 2px     | Badges, tags                      |
| Radius MD          | `--radius-md`        | 4px     | Cards, input fields, buttons      |
| Radius LG          | `--radius-lg`        | 8px     | Modals, larger containers         |
| Radius Round       | `--radius-round`     | 50%     | Avatar images, circular elements  |
| Border Default     | `--border-default`   | 1px solid #f0f0f0 | Standard card borders  |
| Border Focus       | `--border-focus`     | 1px solid #2874f0 | Input focus states    |

---

## 6. Shadows

| Token              | Variable Name      | Value                                      | Usage                   |
|--------------------|--------------------|---------------------------------------------|-------------------------|
| Shadow Card        | `--shadow-card`    | `0 1px 4px 0 rgba(0,0,0,0.12)`             | Product cards           |
| Shadow Header      | `--shadow-header`  | `0 2px 4px 0 rgba(0,0,0,0.16)`             | Sticky header           |
| Shadow Dropdown    | `--shadow-dropdown`| `0 4px 16px 0 rgba(0,0,0,0.16)`            | Menus, dropdowns        |
| Shadow Modal       | `--shadow-modal`   | `0 8px 32px 0 rgba(0,0,0,0.24)`            | Modals, overlays        |

---

## 7. Layout

| Property                | Value        |
|-------------------------|--------------|
| Max page width          | 1280px       |
| Header height           | 56px         |
| Category nav height     | 44px         |
| Content gutter          | 16px         |
| Card grid columns       | 5 (desktop), 3 (tablet), 2 (mobile) |
| Card min width          | 200px        |

---

## 8. Component Conventions

### Header
- Background: `--color-primary` (#2874f0)
- Logo uses yellow (#ffe000) accent on blue background
- Search bar: white background, full-width center column
- Right actions (Login, Cart): white text on blue

### Product Cards
- White background, thin border, subtle shadow on hover
- Image ratio: 1:1 square
- Title: 2-line clamp, `--text-heading-md`
- Price: bold, `--color-text-primary`
- MRP: line-through, `--color-text-muted`
- Discount %: `--color-action` (#fb641b)

### Buttons
- Primary CTA: `--color-action` background, white text
- Secondary: `--color-primary` background, white text
- Ghost: transparent, `--color-primary` border and text
- Height: 40px standard, 32px compact

### Category Pills
- Horizontal scrollable row
- Icon + label below it
- Active state: underline in `--color-primary`

### Banners / Hero Carousel
- Full-width within content area
- Dot indicators for slide navigation

---

## 9. Responsive Breakpoints

| Name       | Min Width  | Description                  |
|------------|------------|------------------------------|
| Mobile     | 0px        | Single column, stacked layout |
| Tablet     | 768px      | 2–3 column grids             |
| Desktop    | 1024px     | Full 5-column grid, header   |
| Wide       | 1280px     | Max content width capped     |

---

## 10. Iconography

- Use inline SVG or Unicode symbols for Phase 1.
- Icon size: 20×20px standard, 24×24px for header actions.
- Icons are in `assets/icons/`.

---

## 11. Asset Paths

| Asset Type         | Path                        |
|--------------------|-----------------------------|
| Product images     | `assets/images/products/`   |
| Banner images      | `assets/images/banners/`    |
| Category icons     | `assets/icons/categories/`  |
| Brand assets       | `assets/images/brand/`      |

---

## 12. Accessibility

- Minimum contrast ratio: 4.5:1 for body text, 3:1 for large text.
- All interactive elements must have `:focus-visible` styles.
- Images must have descriptive `alt` attributes.
- Forms must have associated `<label>` elements.
- Use semantic HTML landmarks (`<header>`, `<nav>`, `<main>`, `<footer>`).

---

*Last updated: Subphase 1 – Project Foundation*
*This file should be updated whenever design tokens change.*
