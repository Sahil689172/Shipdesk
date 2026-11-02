# ShipDesk – Builder Agent Instructions (OpenCode)

Read this file completely before touching any file in the repository.
These instructions override any default OpenCode behaviour where they conflict.

---

## 1. Project Context

You are working on **FestiveKart** – a static e-commerce demo site built with
plain HTML, CSS and JavaScript. There is no build step, no bundler and no
framework. Every change is a direct edit to source files.

| Item | Value |
|------|-------|
| Repository | https://github.com/Sahil689172/Shipdesk |
| Website folder | `shipdesk-festivekart/` |
| Entry point | `shipdesk-festivekart/index.html` |
| Styles | `shipdesk-festivekart/style.css` |
| Scripts | `shipdesk-festivekart/script.js` |
| Design system | `shipdesk-festivekart/DESIGN.md` – read this before any visual change |
| Product images | `shipdesk-festivekart/assets/images/products/` |
| Banner images | `shipdesk-festivekart/assets/images/banners/` |
| Brand logos | `shipdesk-festivekart/assets/images/brand/` |
| Production branch | `main` |

---

## 2. Before Writing Any Code

1. **Read the task** in full – task ID, requirements, acceptance criteria, scope,
   out-of-scope constraints.
2. **Read `DESIGN.md`** for any change that touches colour, spacing, typography
   or layout. Use the CSS variables already defined; do not introduce new ones
   unless the task explicitly requires it.
3. **Read the files you will edit** – understand the existing structure before
   changing it.
4. **Check existing assets** – if the task references a product, banner or brand
   image, confirm the file exists in `assets/` before referencing it.
5. If anything in the task is unclear, post a `BLOCKED:` message in the Switch
   room and wait. Do not guess at requirements.

---

## 3. Git Workflow

```
# 1. Always start from a fresh main
git checkout main
git pull origin main

# 2. Create a feature branch (exact naming required)
git checkout -b feature/SD-NNN-short-description

# 3. Make your changes
# (edit only files within task scope)

# 4. Stage specific files – never git add .
git add shipdesk-festivekart/index.html
git add shipdesk-festivekart/style.css
# etc.

# 5. Commit with task ID prefix
git commit -m "SD-NNN: short imperative description of change"

# 6. Push
git push origin feature/SD-NNN-short-description

# 7. Open PR on GitHub
# Title:  SD-NNN: [same as commit message]
# Body:   use the implementation report format (section 6 below)
```

**Never use `git add .` or `git add -A`.** Stage only the files you intentionally changed.

---

## 4. Coding Rules

### HTML
- Preserve all existing `id` and `aria-*` attributes – they are used by CSS,
  JS and accessibility tooling.
- All images must have a descriptive `alt` attribute.
- New interactive elements need `aria-label` or visible text labels.
- Do not change the document structure (header, nav, main, footer) unless the
  task explicitly requires it.

### CSS
- Use existing CSS variables from `:root` in `style.css`. Never hardcode a
  colour, font size or spacing value that already has a variable.
- New rules go at the bottom of the relevant section, not scattered randomly.
- Responsive styles go in the existing media query blocks at the bottom of
  `style.css` – do not create new `@media` blocks unless necessary.
- Do not remove or rename existing CSS classes that are referenced in HTML or JS.

### JavaScript
- All new code goes in `script.js` following the existing module pattern
  (`const ModuleName = (() => { ... })()`).
- Do not use `var`. Use `const` and `let`.
- Do not add external libraries or CDN links unless the task explicitly requires it.
- Keep the `'use strict';` directive at the top.
- Add a `TODO (SD-NNN):` comment for any placeholder you leave intentionally.

### Assets
- Do not delete or rename existing asset files.
- New images go in the correct subfolder under `assets/images/`.
- Use `loading="lazy"` on all `<img>` tags except the first visible image.

---

## 5. Self-Check Before Posting the PR

Run through every acceptance criterion from the task and record your result:

- [ ] Open `shipdesk-festivekart/index.html` in a browser.
- [ ] Verify each acceptance criterion visually at 1280px (desktop).
- [ ] Verify each acceptance criterion visually at 375px (mobile – use browser DevTools).
- [ ] Check the browser console for JavaScript errors.
- [ ] Check that no existing sections have broken layout.
- [ ] Check that images load correctly (no broken image icons).
- [ ] Verify only files within scope were changed (`git diff --name-only main`).

---

## 6. Implementation Report (post to Switch room after opening PR)

```
IMPLEMENTATION COMPLETE
Task ID:        SD-NNN
Branch:         feature/SD-NNN-short-description
Commit SHA:     [full 40-character SHA]
PR URL:         [GitHub PR URL]
PR Number:      #NNN
Preview URL:    [Cloudflare preview URL – available a few minutes after push]

Files changed:
- shipdesk-festivekart/index.html  – [what changed]
- shipdesk-festivekart/style.css   – [what changed]

Summary:
[2–3 sentences: what was done, why, and how it satisfies the task]

Self-check results:
- Criterion 1: PASS – [what you observed]
- Criterion 2: PASS – [what you observed]

Ready for QA review.
```

---

## 7. Handling a QA Failure

When QA returns a `QA FAIL` report:

1. Read every listed defect carefully.
2. Do NOT open a new branch. Push a new commit to the same feature branch.
3. Fix each defect. Do not fix anything outside the listed defects without
   posting a note in the room first.
4. Run your self-check again.
5. Push the new commit.
6. Post a new implementation report with the **new commit SHA**.
7. The old QA report is now void. QA will re-review the new commit.

---

## 8. Things You Must Never Do

- Push directly to `main`
- Merge your own PR
- Use `git push --force`
- Edit files outside the task scope
- Delete existing CSS classes or JS functions without explicit instruction
- Add npm packages, bundlers or build tools
- Expose credentials, tokens or API keys in any file or commit message
- Skip the implementation report
