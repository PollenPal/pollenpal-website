# PollenPal Investors Memo Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace `/investors.html` with a long-form, YC-style VC memo (~1,800 words across 13 sections) that satisfies the LYS final-project rubric and reads like a real seed-stage partner memo.

**Architecture:** Single static HTML file. Sticky left-rail TOC with `IntersectionObserver` active-state. Inline-SVG charts (no JS chart lib). Reuses existing `styles.css` tokens; appends 8 new CSS components. Adds ~80 lines to `scripts.js`. Print stylesheet for PDF export.

**Tech Stack:** Static HTML + CSS + vanilla JS. No build step. Inline SVG for charts. No new dependencies.

**Spec:** `docs/superpowers/specs/2026-05-03-investors-memo-design.md` — read it first.

---

## Existing context (do NOT change)

**Visual tokens** in `styles.css:6-22` — reuse these, don't add new ones:
```
--gold #E8A43A | --gold-dark #C2851A | --cream #FFECB7 | --cream-soft #FFF8E7
--ink #0A0A0A | --ink-soft #3A3A3A | --muted #6B6B6B | --line #EAEAEA
--bg #FFFFFF | --radius 8px | --radius-lg 14px | --wrap 1240px | --gutter 32px
```

**Type system** in `styles.css:56-114` — already defines h1/h2/h3, `.eyebrow`, `.serif-italic`, `.lede`, `.muted`, `.label-sm`. Use these.

**Existing inline SVG to reuse** from current `investors.html`:
- TAM/SAM/SOM 3-circle SVG at lines 202-225 (`.market` / `.market-ring` / `.market-circle`)
- 2x2 competitive quadrant SVG at lines 175-192 (`.quadrant`)

**Form action** for the contact form (do NOT invent a new endpoint):
```
action="https://docs.google.com/forms/d/e/1FAIpQLScZLvT2HOrDgzx4v0o0YGF5KoqPiU9s5RIRHZ7R0pF7EaXdUA/formResponse"
entry.455027715  = name
entry.414264367  = email
entry.119689931  = firm
entry.1292345725 = message
```

**Hard rules** (from `feedback_no_emdashes.md` and existing claim-policy):
- No em-dashes anywhere. Use periods, semicolons, commas, or " — " with spaces if absolutely necessary (the existing site uses ` — ` with space-hyphen-space which renders as a hyphen, NOT em-dash).
- No emojis.
- No "transforming the future" / "revolutionizing" copy.
- No gradient backgrounds. No glassmorphism.
- Only Robert's first name in copy. Daniel never "Danny."
- Image filenames stay lowercase.

---

## File structure

| File | Action | Lines added |
|---|---|---|
| `investors.html` | Full rewrite | ~700 |
| `styles.css` | Append new components + print block | ~280 |
| `scripts.js` | Append TOC observer + progress bar + mobile dropdown | ~70 |
| `docs/superpowers/plans/2026-05-03-investors-memo.md` | This plan | (already created) |

---

## Phase 1 — Scaffolding (Tasks 1–5)

### Task 1: Create base HTML scaffold (head, header, banner, TOC shell, main shell, footer)

**Files:**
- Create: `investors.html` (full replace; save existing as backup first)

- [ ] **Step 1: Back up the existing investors.html**

```bash
cp /c/projects/pollenpal-website/investors.html /c/projects/pollenpal-website/.investors.html.bak
```

- [ ] **Step 2: Write the new investors.html scaffold**

Replace the entire contents of `C:\projects\pollenpal-website\investors.html` with:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PollenPal · Investor Memo</title>
  <meta name="description" content="PollenPal investor memo. Physical AI for commercial beekeeping. Seeking $500K pre-seed SAFE.">
  <link rel="icon" href="/images/logo-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
</head>
<body class="memo-body">

<a href="#main" class="skip-link">Skip to content</a>

<header class="site-header">
  <div class="wrap nav">
    <a href="/" class="nav-logo"><img src="/images/logo-full.png" alt="PollenPal"></a>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">☰</button>
    <nav class="nav-links">
      <a href="/#how">How it works</a>
      <a href="/#advantage">Why PollenPal</a>
      <a href="/#roadmap">Roadmap</a>
      <a href="/investors" class="current">Investors</a>
    </nav>
    <a href="#ask" class="nav-cta">Get in touch →</a>
  </div>
</header>

<div class="conf-banner" role="note">
  <div class="wrap">
    <span class="conf-dot" aria-hidden="true"></span>
    CONFIDENTIAL &amp; PROPRIETARY · SUBJECT TO NDA · © 2026 POLLENPAL INC.
  </div>
</div>

<button class="toc-mobile-toggle" aria-expanded="false" aria-controls="toc-mobile-list">
  Jump to section <span aria-hidden="true">▾</span>
</button>

<div class="memo-shell">

  <aside class="toc-rail" aria-label="Memo sections">
    <div class="toc-progress" aria-hidden="true"></div>
    <ol class="toc-list">
      <li><a href="#exec-summary"><span class="toc-num">01</span> Executive Summary</a></li>
      <li><a href="#problem"><span class="toc-num">02</span> Problem &amp; Opportunity</a></li>
      <li><a href="#solution"><span class="toc-num">03</span> Solution &amp; Product</a></li>
      <li><a href="#model"><span class="toc-num">04</span> Business Model</a></li>
      <li><a href="#market"><span class="toc-num">05</span> Market Opportunity</a></li>
      <li><a href="#competition"><span class="toc-num">06</span> Competition</a></li>
      <li><a href="#roadmap"><span class="toc-num">07</span> Strategic Roadmap</a></li>
      <li><a href="#financials"><span class="toc-num">08</span> Financial Overview</a></li>
      <li><a href="#traction"><span class="toc-num">09</span> Traction &amp; Milestones</a></li>
      <li><a href="#risks"><span class="toc-num">10</span> Challenges &amp; Risks</a></li>
      <li><a href="#team"><span class="toc-num">11</span> Team</a></li>
      <li><a href="#ask"><span class="toc-num">12</span> Ask &amp; Next Steps</a></li>
      <li><a href="#appendix"><span class="toc-num">13</span> Appendix</a></li>
    </ol>
  </aside>

  <ol class="toc-mobile-list" id="toc-mobile-list">
    <li><a href="#exec-summary">01 Executive Summary</a></li>
    <li><a href="#problem">02 Problem &amp; Opportunity</a></li>
    <li><a href="#solution">03 Solution &amp; Product</a></li>
    <li><a href="#model">04 Business Model</a></li>
    <li><a href="#market">05 Market Opportunity</a></li>
    <li><a href="#competition">06 Competition</a></li>
    <li><a href="#roadmap">07 Strategic Roadmap</a></li>
    <li><a href="#financials">08 Financial Overview</a></li>
    <li><a href="#traction">09 Traction &amp; Milestones</a></li>
    <li><a href="#risks">10 Challenges &amp; Risks</a></li>
    <li><a href="#team">11 Team</a></li>
    <li><a href="#ask">12 Ask &amp; Next Steps</a></li>
    <li><a href="#appendix">13 Appendix</a></li>
  </ol>

  <main id="main" class="memo-main">

    <!-- §1–§13 sections inserted in subsequent tasks -->

  </main>
</div>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="footer-wordmark"><img src="/images/logo-icon.png" alt="">PollenPal</div>
        <p>Physical AI for commercial apiaries and farms.</p>
      </div>
      <div>
        <h4>Product</h4>
        <ul>
          <li><a href="/#how">How it works</a></li>
          <li><a href="/#advantage">Why PollenPal</a></li>
          <li><a href="/#roadmap">Roadmap</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="/#founders">Founders</a></li>
          <li><a href="/investors">Investors</a></li>
          <li><a href="/hobbyist">Hobbyist waitlist</a></li>
        </ul>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="mailto:hello@pollenpal.com">hello@pollenpal.com</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      Confidential &amp; Proprietary · © 2026 PollenPal Inc.
    </div>
  </div>
</footer>

<script src="/scripts.js" defer></script>
</body>
</html>
```

- [ ] **Step 3: Verify scaffold renders**

Open `C:\projects\pollenpal-website\investors.html` in a browser (or run the existing dev preview). Confirm:
- Header renders with `Investors` highlighted as current
- Confidential banner appears below header
- TOC rail is visible on the left (will look unstyled until Task 2)
- Footer renders with `© 2026 PollenPal Inc.`

The TOC and main area will look broken without CSS — that's expected. We add styling in Task 2.

- [ ] **Step 4: Commit**

```bash
cd /c/projects/pollenpal-website
git add investors.html
git commit -m "Scaffold long-form investors memo (TOC, banner, shell)"
```

---

### Task 2: Add base memo CSS (TOC rail, banner, eyebrow numeral, thesis lead)

**Files:**
- Modify: `styles.css` (append at end)

- [ ] **Step 1: Append the memo base block to styles.css**

Add to the end of `C:\projects\pollenpal-website\styles.css`:

```css
/* ============================================================
   INVESTOR MEMO (long-form /investors page)
   Components below ONLY apply on body.memo-body
============================================================ */

.memo-body { background: var(--bg); }

/* ----- Confidential banner ----- */
.conf-banner {
  background: var(--ink);
  color: #fff;
  padding: 10px 0;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.4px;
  position: sticky;
  top: 72px;
  z-index: 90;
}
.conf-banner .wrap { display: flex; align-items: center; gap: 10px; }
.conf-dot {
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--gold);
  flex-shrink: 0;
}

/* ----- Memo shell: TOC + main side-by-side ----- */
.memo-shell {
  max-width: var(--wrap);
  margin: 0 auto;
  padding: 56px var(--gutter) 96px;
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 64px;
  align-items: start;
}

/* ----- Sticky TOC rail ----- */
.toc-rail {
  position: sticky;
  top: 120px;
  align-self: start;
  border-left: 1px solid var(--line);
  padding-left: 24px;
}
.toc-progress {
  position: absolute;
  left: -1px;
  top: 0;
  width: 1px;
  height: 100%;
  background: var(--gold-dark);
  transform: scaleY(0);
  transform-origin: top;
  transition: transform 0.1s linear;
}
.toc-list {
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 13px;
  font-weight: 500;
  line-height: 1.5;
}
.toc-list li { margin-bottom: 14px; }
.toc-list a {
  display: flex;
  gap: 12px;
  align-items: baseline;
  color: var(--muted);
  padding: 4px 0;
  border-left: 3px solid transparent;
  margin-left: -27px;
  padding-left: 24px;
  transition: color 0.15s, border-color 0.15s;
}
.toc-list a:hover { color: var(--ink-soft); }
.toc-list a.active {
  color: var(--ink);
  border-left-color: var(--gold-dark);
  font-weight: 700;
}
.toc-num {
  font-variant-numeric: tabular-nums;
  font-weight: 700;
  color: var(--gold-dark);
  font-size: 11px;
  letter-spacing: 1px;
  flex-shrink: 0;
}

/* ----- Mobile TOC dropdown ----- */
.toc-mobile-toggle {
  display: none;
  position: sticky;
  top: 110px;
  z-index: 80;
  width: 100%;
  background: var(--bg);
  border: none;
  border-bottom: 1px solid var(--line);
  padding: 14px var(--gutter);
  font-weight: 600;
  font-size: 14px;
  text-align: left;
  cursor: pointer;
}
.toc-mobile-list {
  display: none;
  list-style: none;
  margin: 0;
  padding: 0;
  background: var(--bg);
  border-bottom: 1px solid var(--line);
  position: sticky;
  top: 152px;
  z-index: 79;
  max-height: 60vh;
  overflow-y: auto;
}
.toc-mobile-list li { border-top: 1px solid var(--line); }
.toc-mobile-list li:first-child { border-top: 0; }
.toc-mobile-list a {
  display: block;
  padding: 12px var(--gutter);
  font-size: 14px;
  color: var(--ink-soft);
}
.toc-mobile-list.open { display: block; }

/* ----- Main column ----- */
.memo-main { max-width: 760px; }
.memo-main > section { padding: 64px 0; border-top: 1px solid var(--line); }
.memo-main > section:first-of-type { padding-top: 0; border-top: 0; }

/* ----- Eyebrow numeral pattern ----- */
.memo-eyebrow {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--gold-dark);
  margin-bottom: 24px;
  font-variant-numeric: tabular-nums;
}
.memo-eyebrow::before {
  content: "";
  width: 24px;
  height: 1px;
  background: var(--gold-dark);
}

/* ----- Thesis lead (one-sentence section opener) ----- */
.thesis-lead {
  font-size: 21px;
  line-height: 1.45;
  font-weight: 600;
  color: var(--ink);
  border-left: 3px solid var(--gold-dark);
  padding-left: 20px;
  margin: 0 0 32px;
  max-width: 680px;
}

/* ----- Section h2 (smaller than landing-page h2) ----- */
.memo-main h2 {
  font-size: clamp(28px, 3.2vw, 40px);
  margin-bottom: 16px;
}
.memo-main h3 {
  font-size: 18px;
  font-weight: 700;
  margin: 32px 0 12px;
}
.memo-main p { margin-bottom: 18px; max-width: 680px; }
.memo-main p:last-child { margin-bottom: 0; }

/* ----- Cross-link styling ----- */
.xref {
  color: var(--gold-dark);
  border-bottom: 1px dotted rgba(194, 133, 26, 0.35);
  transition: border-color 0.15s;
}
.xref:hover { border-bottom-color: var(--gold-dark); }

/* ----- Footnote markers + endnote list ----- */
sup.fn-ref {
  font-size: 11px;
  vertical-align: super;
  line-height: 0;
}
sup.fn-ref a { color: var(--gold-dark); font-weight: 600; }
sup.fn-ref a:hover { text-decoration: underline; }

.footnote-list {
  list-style: none;
  margin: 32px 0 0;
  padding: 16px 0 0;
  border-top: 1px solid var(--line);
  font-size: 13px;
  line-height: 1.55;
  color: var(--muted);
  font-style: italic;
}
.footnote-list li { margin-bottom: 6px; max-width: 680px; }
.footnote-list li:target {
  background: var(--cream-soft);
  font-style: normal;
}
.footnote-list a { color: var(--gold-dark); font-style: normal; }

/* ----- Responsive ----- */
@media (max-width: 1100px) {
  .memo-shell {
    grid-template-columns: 1fr;
    gap: 0;
    padding-top: 24px;
  }
  .toc-rail { display: none; }
  .toc-mobile-toggle { display: block; }
}
@media (max-width: 600px) {
  .memo-main > section { padding: 48px 0; }
  .thesis-lead { font-size: 18px; padding-left: 16px; }
}
```

- [ ] **Step 2: Reload the browser and verify**

Refresh the browser tab. Confirm:
- TOC rail is visible on the left, sticks at 120px from top when scrolling
- Confidential banner sticks under the header
- Below 1100px viewport (resize), TOC collapses to "Jump to section ▾" button
- Active state, progress bar will not work yet (Task 5 adds the JS)

- [ ] **Step 3: Commit**

```bash
git add styles.css
git commit -m "Add memo base styles (TOC rail, banner, eyebrow, thesis-lead)"
```

---

### Task 3: Add memo data components CSS (stat-callout, pull-quote, memo-table, chart-frame, risk-callout)

**Files:**
- Modify: `styles.css` (append after Task 2's block)

- [ ] **Step 1: Append the data components block**

Add to the end of `C:\projects\pollenpal-website\styles.css`:

```css
/* ----- Stat callout grid + cards ----- */
.stat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
  margin: 32px 0;
}
.stat-callout {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 24px;
  background: var(--bg);
}
.stat-callout .stat-num {
  font-size: 36px;
  font-weight: 800;
  line-height: 1;
  letter-spacing: -0.02em;
  color: var(--ink);
  font-variant-numeric: tabular-nums;
}
.stat-callout .stat-rule {
  width: 32px;
  height: 2px;
  background: var(--gold-dark);
  margin: 12px 0 10px;
}
.stat-callout .stat-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--muted);
  line-height: 1.4;
}

/* ----- Pull quote (Instrument Serif italic, used sparingly) ----- */
.pull-quote {
  margin: 40px 0;
  padding: 32px 40px;
  border-left: 3px solid var(--gold-dark);
  background: var(--cream-soft);
  border-radius: 0 var(--radius) var(--radius) 0;
}
.pull-quote blockquote {
  font-family: 'Instrument Serif', Georgia, serif;
  font-style: italic;
  font-size: clamp(22px, 2.6vw, 30px);
  line-height: 1.3;
  color: var(--ink);
  margin: 0 0 12px;
}
.pull-quote cite {
  font-style: normal;
  font-size: 13px;
  font-weight: 600;
  color: var(--muted);
  letter-spacing: 0.4px;
}

/* ----- Memo table ----- */
.memo-table-wrap {
  margin: 24px 0;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
.memo-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
  font-variant-numeric: tabular-nums;
}
.memo-table th, .memo-table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--line);
  vertical-align: top;
}
.memo-table th {
  font-weight: 700;
  font-size: 12px;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: var(--muted);
  border-bottom: 2px solid var(--ink);
}
.memo-table td:first-child { font-weight: 600; color: var(--ink-soft); }
.memo-table tr.total td {
  border-top: 1px solid var(--ink);
  font-weight: 700;
  color: var(--ink);
}
.memo-table tr.highlight td {
  background: var(--cream-soft);
  font-weight: 700;
  color: var(--ink);
}
.memo-table .num { text-align: right; font-variant-numeric: tabular-nums; }

/* ----- Chart frame ----- */
.chart-frame {
  margin: 24px 0;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 28px 24px 20px;
  background: var(--bg);
}
.chart-frame .chart-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--ink);
  margin-bottom: 18px;
  letter-spacing: 0.2px;
}
.chart-frame .chart-caption {
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid var(--line);
  font-size: 12px;
  font-style: italic;
  color: var(--muted);
  line-height: 1.5;
}

/* ----- Risk callout pairs ----- */
.risk-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin: 24px 0;
}
.risk-card {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 20px 22px;
}
.risk-card.is-risk { background: var(--bg); }
.risk-card.is-mit { background: var(--cream-soft); border-color: transparent; }
.risk-tag {
  display: inline-block;
  background: var(--ink);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.4px;
  padding: 4px 8px;
  border-radius: 4px;
  margin-bottom: 10px;
}
.mit-tag {
  display: inline-block;
  background: var(--gold-dark);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.4px;
  padding: 4px 8px;
  border-radius: 4px;
  margin-bottom: 10px;
}
.risk-card p { font-size: 14px; line-height: 1.55; margin: 0; max-width: none; }
@media (max-width: 760px) {
  .risk-grid { grid-template-columns: 1fr; }
}

/* ----- Roadmap phase table accent strips ----- */
.roadmap-table th { padding-top: 20px; padding-bottom: 16px; }
.roadmap-table th.phase-now { box-shadow: inset 0 -3px 0 var(--cream); }
.roadmap-table th.phase-next { box-shadow: inset 0 -3px 0 var(--gold); }
.roadmap-table th.phase-later { box-shadow: inset 0 -3px 0 var(--gold-dark); }

/* ----- Solution image strip ----- */
.solution-strip {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin: 24px 0;
}
.solution-strip figure { margin: 0; }
.solution-strip img {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: var(--radius);
  border: 1px solid var(--line);
}
.solution-strip figcaption {
  font-size: 12px;
  color: var(--muted);
  margin-top: 8px;
  font-weight: 500;
}
@media (max-width: 760px) {
  .solution-strip { grid-template-columns: 1fr; }
  .solution-strip img { height: 220px; }
}

/* ----- Team cards (refined for memo) ----- */
.memo-team-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin: 24px 0;
}
.memo-team-card {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 20px 22px;
}
.memo-team-card h3 { margin: 0 0 4px; font-size: 17px; }
.memo-team-card .role {
  font-size: 12px;
  font-weight: 600;
  color: var(--gold-dark);
  letter-spacing: 0.5px;
  text-transform: uppercase;
  margin-bottom: 10px;
}
.memo-team-card p { margin: 0; font-size: 14px; line-height: 1.55; max-width: none; }
@media (max-width: 760px) {
  .memo-team-grid { grid-template-columns: 1fr; }
}

/* ----- Use-of-funds + next-steps ----- */
.next-steps-strip {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin: 24px 0;
  counter-reset: stp;
}
.next-step {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 16px 18px;
  font-size: 13px;
  line-height: 1.5;
  position: relative;
}
.next-step::before {
  counter-increment: stp;
  content: "0" counter(stp);
  display: block;
  font-size: 11px;
  font-weight: 700;
  color: var(--gold-dark);
  letter-spacing: 1px;
  margin-bottom: 6px;
  font-variant-numeric: tabular-nums;
}
@media (max-width: 760px) {
  .next-steps-strip { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 480px) {
  .next-steps-strip { grid-template-columns: 1fr; }
}

/* ----- Appendix collapsibles ----- */
.appendix-section {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  margin-bottom: 12px;
  background: var(--bg);
}
.appendix-section summary {
  padding: 16px 20px;
  cursor: pointer;
  font-weight: 600;
  font-size: 15px;
  list-style: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.appendix-section summary::-webkit-details-marker { display: none; }
.appendix-section summary::after {
  content: "▸";
  color: var(--gold-dark);
  font-size: 12px;
  transition: transform 0.2s;
}
.appendix-section[open] summary::after { transform: rotate(90deg); }
.appendix-section .appendix-body {
  padding: 0 20px 20px;
  font-size: 14px;
  line-height: 1.6;
}

/* ----- Hero block (memo-specific, simpler than landing) ----- */
.memo-hero h1 {
  font-size: clamp(40px, 5vw, 64px);
  margin-bottom: 20px;
  line-height: 1.05;
  letter-spacing: -0.025em;
}
.memo-hero .lede {
  font-size: 19px;
  margin-bottom: 28px;
  max-width: 640px;
}
```

- [ ] **Step 2: Reload and verify**

Refresh. Confirm no CSS errors (open DevTools console). The components won't render yet because no section content exists; this just registers the styles for later tasks.

- [ ] **Step 3: Commit**

```bash
git add styles.css
git commit -m "Add memo data components (callouts, tables, charts, risks, appendix)"
```

---

### Task 4: Add print stylesheet

**Files:**
- Modify: `styles.css` (append after Task 3's block)

- [ ] **Step 1: Append the print block**

Add to the end of `C:\projects\pollenpal-website\styles.css`:

```css
/* ============================================================
   PRINT STYLES (memo-only PDF export via Ctrl+P)
============================================================ */
@media print {
  body.memo-body {
    background: #fff;
    color: #000;
    font-size: 11pt;
    cursor: auto;
  }
  .site-header, .toc-rail, .toc-mobile-toggle, .toc-mobile-list,
  .nav-toggle, .nav-cta, .skip-link, .nav-links { display: none !important; }
  .conf-banner {
    position: static;
    background: #000;
    color: #fff;
    padding: 6px 0;
    font-size: 9pt;
  }
  .memo-shell {
    grid-template-columns: 1fr;
    padding: 0 24px;
    gap: 0;
  }
  .memo-main { max-width: none; }
  .memo-main > section {
    break-inside: avoid;
    padding: 24px 0;
    border-top: 1px solid #000;
  }
  .memo-main > section:first-of-type { border-top: 0; }
  .memo-eyebrow { color: #000; }
  .thesis-lead { border-left-color: #000; }
  .stat-callout, .chart-frame, .memo-table, .risk-card,
  .memo-team-card, .next-step, .appendix-section { break-inside: avoid; }
  a { color: #000; text-decoration: underline; }
  .footnote-list a { text-decoration: none; }
  .site-footer .footer-grid { display: none; }
  .site-footer .footer-bottom {
    text-align: center;
    padding: 12px 0;
    border-top: 1px solid #000;
    font-size: 9pt;
  }
  /* Force colors for charts (browsers strip backgrounds by default) */
  svg .bar-fill { fill: #C2851A !important; }
  svg .line-stroke { stroke: #C2851A !important; }
}
@page {
  margin: 18mm 14mm;
  @bottom-center {
    content: "© 2026 PollenPal Inc. · Page " counter(page) " of " counter(pages);
    font-size: 9pt;
    color: #666;
  }
}
```

- [ ] **Step 2: Verify print preview**

In the browser tab with `investors.html` open: press `Ctrl+P`. Confirm:
- TOC rail and header are hidden
- Confidential banner appears at top of every page
- Body text is readable in B&W
- No emoji or color-only signals

(The page will be mostly empty until content is added; verify the chrome at least.)

- [ ] **Step 3: Commit**

```bash
git add styles.css
git commit -m "Add print stylesheet for memo PDF export"
```

---

### Task 5: Add scripts.js TOC behavior (active-state observer + progress bar + mobile dropdown)

**Files:**
- Modify: `scripts.js` (append at end, inside the IIFE)

- [ ] **Step 1: Append memo-specific JS**

Open `C:\projects\pollenpal-website\scripts.js`. Replace the closing `})();` on line 47 with the following (which adds 4 new behaviors before the closing IIFE):

```javascript
  // ===== MEMO: TOC ACTIVE-SECTION OBSERVER =====
  // Highlights the current section in the left-rail TOC as the user scrolls.
  // Only active on /investors (where .toc-rail exists).
  const tocRail = document.querySelector('.toc-rail');
  if (tocRail) {
    const tocLinks = tocRail.querySelectorAll('a');
    const sectionMap = new Map();
    tocLinks.forEach(function (link) {
      const id = link.getAttribute('href').slice(1);
      const section = document.getElementById(id);
      if (section) sectionMap.set(section, link);
    });
    const tocObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          tocLinks.forEach(function (l) { l.classList.remove('active'); });
          const link = sectionMap.get(entry.target);
          if (link) link.classList.add('active');
        }
      });
    }, { rootMargin: '-20% 0px -65% 0px', threshold: 0 });
    sectionMap.forEach(function (_link, section) { tocObserver.observe(section); });
  }

  // ===== MEMO: TOC SCROLL PROGRESS BAR =====
  const tocProgress = document.querySelector('.toc-progress');
  const memoMain = document.querySelector('.memo-main');
  if (tocProgress && memoMain) {
    let ticking = false;
    function updateProgress() {
      const rect = memoMain.getBoundingClientRect();
      const totalScrollable = memoMain.offsetHeight - window.innerHeight;
      const scrolled = -rect.top;
      const ratio = totalScrollable > 0
        ? Math.max(0, Math.min(1, scrolled / totalScrollable))
        : 0;
      tocProgress.style.transform = 'scaleY(' + ratio + ')';
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) {
        window.requestAnimationFrame(updateProgress);
        ticking = true;
      }
    }, { passive: true });
    updateProgress();
  }

  // ===== MEMO: MOBILE TOC DROPDOWN =====
  const tocMobileToggle = document.querySelector('.toc-mobile-toggle');
  const tocMobileList = document.querySelector('.toc-mobile-list');
  if (tocMobileToggle && tocMobileList) {
    tocMobileToggle.addEventListener('click', function () {
      const open = tocMobileList.classList.toggle('open');
      tocMobileToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    // Close after navigating to a section
    tocMobileList.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        tocMobileList.classList.remove('open');
        tocMobileToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

})();
```

The trailing `})();` is the closing of the existing IIFE — make sure it remains the last line of the file.

- [ ] **Step 2: Verify in browser**

Reload. Open DevTools console — should be no errors. Once content is added in later tasks, you'll be able to verify:
- TOC active state changes as you scroll
- Vertical progress bar fills
- Mobile dropdown opens/closes when toggled

- [ ] **Step 3: Commit**

```bash
git add scripts.js
git commit -m "Add memo TOC active-state observer and progress bar"
```

---

## Phase 2 — Section content (Tasks 6–18)

Each section task: insert markup inside `<main id="main" class="memo-main">`. Insert in section-number order so the document remains coherent during partial completion.

### Task 6: §1 Executive Summary

**Files:**
- Modify: `investors.html` (insert inside `<main id="main">`)

- [ ] **Step 1: Insert §1 markup**

Insert this block as the FIRST child of `<main id="main" class="memo-main">`:

```html
    <section id="exec-summary" class="memo-hero">
      <div class="memo-eyebrow">[01] · Executive Summary</div>
      <h1>Physical AI for commercial beekeeping.</h1>
      <p class="thesis-lead">PollenPal is hardware and ML that watches every bee in and out of the hive, catches threats the day they appear, and sells through a $4 to $20 per hive per month subscription with hardware bundled.</p>

      <p>U.S. beekeepers lose 40 percent or more of their colonies every year<sup class="fn-ref"><a href="#fn-1-1" id="fnref-1-1">¹</a></sup> and the 2024-25 season was the worst on record, with commercial operators losing 62 percent of colonies and an estimated $600M in revenue.<sup class="fn-ref"><a href="#fn-1-2" id="fnref-1-2">²</a></sup> The workforce is aging, the inspection cadence is slow, and the threats are accelerating. Continuous monitoring is the only way out, and falling sensor and compute costs make it economic for the first time.</p>

      <p>We have spent the last year proving that physical AI can carry the inspection load. Three commercial pilots are committed for 2026. Our YOLO model is trained on 250,000+ field images. Robert spent the summer of 2025 driving across the country, interviewing 50+ beekeepers, and the conclusions are now in our product. The team pairs a 17-year hobbyist beekeeper (Robert, Columbia MBA) with an Apex Space hardware engineer (Daniel, ex-Blue Origin) who have worked together for nine years.</p>

      <p>We are raising a <a href="#ask" class="xref">$500K pre-seed SAFE</a> to fund production hardware, on-prem GPU inference, and the first paid commercial deployments. $55K of non-dilutive funding is already secured.</p>

      <div class="stat-grid">
        <div class="stat-callout">
          <div class="stat-num">250k+</div>
          <div class="stat-rule"></div>
          <div class="stat-label">Field images trained on</div>
        </div>
        <div class="stat-callout">
          <div class="stat-num">3</div>
          <div class="stat-rule"></div>
          <div class="stat-label">Commercial pilots committed</div>
        </div>
        <div class="stat-callout">
          <div class="stat-num">50+</div>
          <div class="stat-rule"></div>
          <div class="stat-label">Beekeeper interviews</div>
        </div>
        <div class="stat-callout">
          <div class="stat-num">$500K</div>
          <div class="stat-rule"></div>
          <div class="stat-label">Pre-seed SAFE we're raising</div>
        </div>
      </div>

      <ol class="footnote-list">
        <li id="fn-1-1">¹ Bee Informed Partnership, Annual Colony Loss Survey. <a href="https://beeinformed.org/results-categories/honey-bee-colony-losses">beeinformed.org/results-categories/honey-bee-colony-losses</a> <a href="#fnref-1-1">↩</a></li>
        <li id="fn-1-2">² Honey Bee Health Coalition, 2024-25 catastrophic loss data. <a href="https://honeybeehealthcoalition.org/new-data-confirm-catastrophic-honey-bee-colony-losses-underscoring-urgent-need-for-action/">honeybeehealthcoalition.org</a>; Auburn University U.S. Beekeeping Survey 2024-25. <a href="#fnref-1-2">↩</a></li>
      </ol>
    </section>
```

- [ ] **Step 2: Verify in browser**

Reload. Confirm:
- Section renders with `[01] · EXECUTIVE SUMMARY` eyebrow
- Thesis lead has gold-dark left border
- 4 stat callouts render in a grid
- Two footnote markers (¹²) are clickable and scroll to endnotes
- Endnote `↩` links scroll back to inline markers

- [ ] **Step 3: Commit**

```bash
git add investors.html
git commit -m "Add §1 Executive Summary"
```

---

### Task 7: §2 Problem & Opportunity

- [ ] **Step 1: Append §2 markup**

Insert AFTER the closing `</section>` of §1:

```html
    <section id="problem">
      <div class="memo-eyebrow">[02] · Problem &amp; Opportunity</div>
      <h2>Bees feed the world. The workforce can't scale to keep up.</h2>
      <p class="thesis-lead">U.S. beekeepers lose 40 percent or more of their colonies each year while food demand rises, and the aging workforce cannot inspect every hive often enough to catch threats before they spread.</p>

      <p>Pollinators carry roughly 35 percent of global food production by volume.<sup class="fn-ref"><a href="#fn-2-1" id="fnref-2-1">¹</a></sup> The FAO projects 60 percent more agricultural production needed by 2050.<sup class="fn-ref"><a href="#fn-2-2" id="fnref-2-2">²</a></sup> The math doesn't work without healthy hives, and hive health is collapsing.</p>

      <p>The 2024-25 season set a record: commercial operators lost 62 percent of colonies and roughly $600M in U.S. revenue.<sup class="fn-ref"><a href="#fn-2-3" id="fnref-2-3">³</a></sup> Varroa mites, africanization, and queen failure are the proximate causes, but the structural issue is inspection cadence. The average commercial beekeeper is over 60.<sup class="fn-ref"><a href="#fn-2-4" id="fnref-2-4">⁴</a></sup> Yards run thousands of hives. Manual inspection visits a colony every two to three weeks. By the time a problem is caught, the cluster is already collapsing.</p>

      <div class="pull-quote">
        <blockquote>"How the f**k can you get through 10,000 hives with 10 employees?"</blockquote>
        <cite>Kristen, Master Beekeeper · 20 years' experience · interviewed July 2025</cite>
      </div>

      <p>Robert spent the summer of 2025 driving across the country, interviewing more than 50 commercial and hobbyist beekeepers in CA, TX, FL, CO, and NY.<sup class="fn-ref"><a href="#fn-2-5" id="fnref-2-5">⁵</a></sup> Every commercial operator surfaced the same gap: they need eyes on every hive, every day, and there is no labor pool to do it. The old way is human inspection on a multi-week cycle. The new way has to be physical AI, and falling sensor and compute costs are the reason it works now.</p>

      <div class="stat-grid">
        <div class="stat-callout">
          <div class="stat-num">40%+</div>
          <div class="stat-rule"></div>
          <div class="stat-label">Average annual U.S. hive loss</div>
        </div>
        <div class="stat-callout">
          <div class="stat-num">$600M</div>
          <div class="stat-rule"></div>
          <div class="stat-label">U.S. revenue lost in 2024-25 season</div>
        </div>
      </div>

      <ol class="footnote-list">
        <li id="fn-2-1">¹ FAO; Klein et al. 2007, <em>Importance of pollinators in changing landscapes for world crops</em>. Proceedings of the Royal Society B. <a href="https://royalsocietypublishing.org/doi/10.1098/rspb.2006.3721">royalsocietypublishing.org</a> <a href="#fnref-2-1">↩</a></li>
        <li id="fn-2-2">² UN FAO, <em>World Agriculture Towards 2030/2050</em>. <a href="https://www.fao.org/3/i6583e/i6583e.pdf">fao.org/3/i6583e/i6583e.pdf</a> <a href="#fnref-2-2">↩</a></li>
        <li id="fn-2-3">³ Honey Bee Health Coalition, 2024-25 catastrophic loss data; Auburn University U.S. Beekeeping Survey 2024-25. <a href="https://honeybeehealthcoalition.org/new-data-confirm-catastrophic-honey-bee-colony-losses-underscoring-urgent-need-for-action/">honeybeehealthcoalition.org</a> <a href="#fnref-2-3">↩</a></li>
        <li id="fn-2-4">⁴ Apiary Inspectors of America 2024-25 Survey. <a href="https://apiaryinspectors.org/US-beekeeping-survey-24-25">apiaryinspectors.org/US-beekeeping-survey-24-25</a> <a href="#fnref-2-4">↩</a></li>
        <li id="fn-2-5">⁵ Customer interviews, summer 2025. n=50+ commercial and hobbyist beekeepers across CA, TX, FL, CO, NY. <a href="#fnref-2-5">↩</a></li>
      </ol>
    </section>
```

- [ ] **Step 2: Verify**

Reload. Confirm pull quote renders in Instrument Serif italic with gold-dark left border. All 5 footnotes resolve.

- [ ] **Step 3: Commit**

```bash
git add investors.html
git commit -m "Add §2 Problem & Opportunity"
```

---

### Task 8: §3 Solution & Product

- [ ] **Step 1: Append §3 markup**

```html
    <section id="solution">
      <div class="memo-eyebrow">[03] · Solution &amp; Product</div>
      <h2>Computer vision on every hive entrance.</h2>
      <p class="thesis-lead">We put computer vision on every hive entrance and surface threats the day they appear, instead of weeks later during manual inspection.</p>

      <p>Three integrated layers — hardware, machine learning, and a beekeeper-facing web app — replace the fortnightly inspection visit with continuous monitoring.</p>

      <div class="solution-strip">
        <figure>
          <img src="/images/device-grass.jpg" alt="PollenPal device deployed on a hive in the field">
          <figcaption>Hardware monitors every bee in and out of the hive</figcaption>
        </figure>
        <figure>
          <img src="/images/ml-detection.jpg" alt="ML pipeline detecting and tracking individual bees">
          <figcaption>YOLO model flags varroa, africanization, queen issues</figcaption>
        </figure>
        <figure>
          <img src="/images/dashboard-phone.jpg" alt="Mobile dashboard with hive-level alerts">
          <figcaption>Hive-level alerts, multi-yard views</figcaption>
        </figure>
      </div>

      <h3>Hardware</h3>
      <p>Off-the-shelf IoT compute and sensors with a sub-$100 BOM target.<sup class="fn-ref"><a href="#fn-3-1" id="fnref-3-1">¹</a></sup> A 3D-printed skeleton fits standard 10-frame Langstroth boxes — no custom hive bodies — and integrates sound sensors plus external switches for labor coordination. Solar plus LTE for remote yards. Twelve design iterations have gone through commercial-yard testing in South Florida.</p>

      <h3>Machine Learning</h3>
      <p>YOLO11 trained on 250,000+ field images, annotated through our CVAT pipeline.<sup class="fn-ref"><a href="#fn-3-2" id="fnref-3-2">²</a></sup> The model tracks colony activity in real time and flags varroa mites, africanization markers, and missing-queen indicators. Cloud inference today; on-prem GPU on the roadmap (<a href="#ask" class="xref">funded by §12 Ask</a>) for 80 percent inference cost cut and sub-second latency.</p>

      <h3>Web App</h3>
      <p>Hive-level alerts, multi-yard rollups, and review queues. Designed with beekeeper input — actionable insights over complex graphs. Recordkeeping, harvest logging, and supply ordering are integrated to displace the spreadsheets and notebook columns we found in every yard we visited. The data flywheel from this product is what compounds (<a href="#competition" class="xref">see §6 Competition</a>).</p>

      <ol class="footnote-list">
        <li id="fn-3-1">¹ PollenPal analysis. Sub-$100 BOM target reflects supplier quotes at 700-unit production volume; further reductions modeled at 10,000-unit scale. <a href="#fnref-3-1">↩</a></li>
        <li id="fn-3-2">² Internal training pipeline; 250,000+ images captured across South Florida pilot 2025-2026, annotated via CVAT (<a href="https://13.58.185.121:8080">internal CVAT instance</a>). <a href="#fnref-3-2">↩</a></li>
      </ol>
    </section>
```

- [ ] **Step 2: Verify**

Reload. Confirm 3-image strip renders. The placeholder images come from existing assets in `/images/` — verify each loads. If any image is missing, drop it temporarily and call it out for a follow-up.

- [ ] **Step 3: Commit**

```bash
git add investors.html
git commit -m "Add §3 Solution & Product"
```

---

### Task 9: §4 Business Model (with four fits + pricing table)

- [ ] **Step 1: Append §4 markup**

```html
    <section id="model">
      <div class="memo-eyebrow">[04] · Business Model</div>
      <h2>Subscription with hardware bundled, three channels.</h2>
      <p class="thesis-lead">Pricing is $4 to $20 per hive per month across three channels, gross margin scales from 44 percent to 71 percent as device BOM falls $46 to $18, and hardware bundling removes the upfront capex barrier that interview after interview surfaced as the #1 friction.<sup class="fn-ref"><a href="#fn-4-1" id="fnref-4-1">¹</a></sup></p>

      <h3>Pricing tiers</h3>
      <div class="memo-table-wrap">
        <table class="memo-table">
          <thead>
            <tr>
              <th></th>
              <th>Commercial</th>
              <th>Hobbyist</th>
              <th>Partnership</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Subscription</td><td>$4/hive/mo → $6 by Yr 5</td><td>$8/hive/mo → $12 by Yr 5</td><td>$20/hive/mo (rev share)</td></tr>
            <tr><td>Setup</td><td>$2,500 one-time</td><td>bundled</td><td>bundled</td></tr>
            <tr><td>Hives / customer</td><td>1,500</td><td>5</td><td>50–8,000 managed</td></tr>
            <tr><td>ACV (Yr 1)</td><td>$72K</td><td>$480</td><td>varies</td></tr>
            <tr><td>Channel</td><td>Direct sales</td><td>Self-serve</td><td>Best Bees, Alvéole</td></tr>
            <tr><td>Hardware</td><td>Bundled</td><td>Bundled</td><td>Bundled</td></tr>
          </tbody>
        </table>
      </div>

      <p>Short-term U.S. TAM at scale across all three channels is roughly $160M ($137M commercial + $19M hobbyist + $4M partnership).<sup class="fn-ref"><a href="#fn-4-2" id="fnref-4-2">²</a></sup> The deeper market geometry sits in <a href="#market" class="xref">§5 Market Opportunity</a>.</p>

      <h3>The four fits</h3>
      <p>The model is engineered around the four fits framework: each adjacent pair has to be coherent, or the system breaks.</p>

      <p><strong>Product / Market.</strong> Hardware plus continuous CV solves the inspection-cadence gap that every commercial interview surfaced. Continuous monitoring replaces 2-3 week manual inspection.</p>

      <p><strong>Market / Channel.</strong> Commercial: direct sales to ~1,600 concentrated U.S. operators (a known list, named accounts). Hobbyist: self-serve via paid social and content. Partnership: B2B2C through corporate beekeeping platforms (Best Bees, Alvéole), which collectively manage hives across 24+ U.S. cities.</p>

      <p><strong>Channel / Model.</strong> Direct sales matches a $72K Yr-1 ACV — the unit revenue supports a sales motion with site visits. Self-serve matches $480 hobbyist ACV. Partnership rev-share (25 percent) matches B2B2C platform economics where the platform owns the customer relationship.</p>

      <p><strong>Model / Market.</strong> Subscription compounds ARR and amortizes hardware over multi-year contracts. Hardware bundling removes the capex barrier in a market where digital-tooling adoption is structurally low — most operators we interviewed run on paper, spreadsheets, or nothing.</p>

      <ol class="footnote-list">
        <li id="fn-4-1">¹ Customer interviews, summer 2025; PollenPal Business Model v8 (gross margin trajectory derived from hardware BOM scale curve). <a href="#fnref-4-1">↩</a></li>
        <li id="fn-4-2">² PollenPal Business Model v8. Short-term U.S. TAM = (1,600 commercial × 1,500 hives × $72/hive/yr) + (40,000 hobbyist × 5 hives × $96/hive/yr × ~10% TAM share) + partnership channel. Source: USDA NASS Honey Report 2024 baseline. <a href="#fnref-4-2">↩</a></li>
      </ol>
    </section>
```

- [ ] **Step 2: Verify**

Reload. Confirm pricing table renders with `tabular-nums` figures. Four fits paragraphs all render. Cross-link to §5 works.

- [ ] **Step 3: Commit**

```bash
git add investors.html
git commit -m "Add §4 Business Model with four fits and pricing table"
```

---

### Task 10: §5 Market Opportunity (reuse existing TAM/SAM/SOM SVG with updated TAM label)

- [ ] **Step 1: Append §5 markup**

```html
    <section id="market">
      <div class="memo-eyebrow">[05] · Market Opportunity</div>
      <h2>$106B TAM, $24B SAM, $128M SOM.</h2>
      <p class="thesis-lead">PollenPal starts inside U.S. hive management ($128M SOM, bottom-up from 1,600 commercial operators) and the SAM expands into precision farming ($24B), with crop protection ($106B) as the long-term ceiling as AI-driven monitoring displaces or optimizes chemical application.</p>

      <h3>SOM — $128M U.S. hive management</h3>
      <p>1,600 commercial operators × ~1,500 hives each × ~$96/hive/yr ARPU × adoption haircut.<sup class="fn-ref"><a href="#fn-5-1" id="fnref-5-1">¹</a></sup> This is the playing field for 2026-2028: a known operator list, named accounts, direct sales motion. We have line of sight to roughly $4.6M revenue by 2030 (<a href="#financials" class="xref">§8 Financial Overview</a>).</p>

      <h3>SAM — $24B precision farming</h3>
      <p>The precision farming market is projected to reach $24B globally by 2030.<sup class="fn-ref"><a href="#fn-5-2" id="fnref-5-2">²</a></sup> PollenPal's SAM is the slice of precision farming addressed by behavioral monitoring, pollination verification, and precision intervention across orchards, vineyards, and greenhouses. Our hive sensors and ML pipeline transfer naturally — bees are mobile sensors that already surface yield-relevant data we can monetize beyond the hive itself.</p>

      <h3>TAM — $106B crop protection</h3>
      <p>The global crop protection chemicals market is projected to reach $106B by 2030.<sup class="fn-ref"><a href="#fn-5-3" id="fnref-5-3">³</a></sup> The long-term play: AI-enabled IPM and monitoring reduces or replaces chemical application volume. We are not pitching a chemical company; we are pitching that the long-run ceiling for precision monitoring is the size of what it ultimately optimizes against.</p>

      <div class="market" style="margin-top: 32px;">
        <div class="market-ring">
          <div class="market-circle tam"><div class="mc-num">$106B</div><div class="mc-label">TAM</div></div>
          <h4>Crop Protection</h4>
          <p>Chemicals, IPM, and precision-tech alternatives — global by 2030.</p>
        </div>
        <div class="market-ring">
          <div class="market-circle sam"><div class="mc-num">$24B</div><div class="mc-label">SAM</div></div>
          <h4>Precision Farming</h4>
          <p>Behavioral monitoring, pollination verification, precision intervention.</p>
        </div>
        <div class="market-ring">
          <div class="market-circle som"><div class="mc-num">$128M</div><div class="mc-label">SOM</div></div>
          <h4>U.S. Hive Management</h4>
          <p>PollenPal hardware and software subscriptions sold to U.S. beekeepers.</p>
        </div>
      </div>

      <ol class="footnote-list">
        <li id="fn-5-1">¹ PollenPal analysis. SOM = 1,600 commercial operators × 1,500 hives × $96/hive/yr × adoption haircut. Operator count and aggregate hive count from USDA NASS Honey Report 2024. <a href="https://www.nass.usda.gov/Surveys/Guide_to_NASS_Surveys/Bee_and_Honey/">nass.usda.gov</a> <a href="#fnref-5-1">↩</a></li>
        <li id="fn-5-2">² Grand View Research, <em>Precision Farming Market Size, Share | Industry Report, 2030</em>. <a href="https://www.grandviewresearch.com/industry-analysis/precision-farming-market">grandviewresearch.com</a> <a href="#fnref-5-2">↩</a></li>
        <li id="fn-5-3">³ MarketsandMarkets, <em>Crop Protection Chemicals Market 2025-2030</em>: $83.32B (2025) → $106.26B (2030), 5.0% CAGR. <a href="https://www.marketsandmarkets.com/Market-Reports/crop-protection-380.html">marketsandmarkets.com</a> <a href="#fnref-5-3">↩</a></li>
      </ol>
    </section>
```

- [ ] **Step 2: Verify**

Reload. Confirm the existing `.market` / `.market-ring` SVG markup renders correctly with the updated $106B TAM label and Crop Protection description. (The `.market` styles already exist in `styles.css`.)

- [ ] **Step 3: Commit**

```bash
git add investors.html
git commit -m "Add §5 Market Opportunity with relabeled TAM"
```

---

### Task 11: §6 Competition (reuse existing quadrant SVG)

- [ ] **Step 1: Append §6 markup**

```html
    <section id="competition">
      <div class="memo-eyebrow">[06] · Competition</div>
      <h2>The first to be both accurate and deployable.</h2>
      <p class="thesis-lead">Existing tools force a tradeoff between actionable accuracy and affordable deployment; PollenPal is the first to be both, and the data flywheel compounds with every bee we see.</p>

      <p>Today, beekeepers solve the inspection-cadence problem in one of four ways:</p>

      <p><strong>Manual inspection.</strong> Accurate when it happens, but operators visit each hive every two to three weeks. By the time a problem is caught, the cluster is already collapsing. Labor cost is the binding constraint, not technology.</p>

      <p><strong>BroodMinder ($50–200/yr per device).</strong> Weight and temperature sensors only. No behavioral signal. Detects late-stage colony failure but cannot flag varroa load, africanization markers, or queen issues until the bees are already gone.</p>

      <p><strong>Solution Bee.</strong> Acoustic monitoring. Real signal but limited interpretability — operators in our interviews described the alerts as "noise" they learned to ignore.</p>

      <p><strong>Beewise (~thousands per colony).</strong> Full automation, accurate, but proprietary hive bodies. Doesn't fit standard 10-frame Langstroth setups, which means existing operators would have to rebuild their entire yard infrastructure to adopt.</p>

      <div class="quadrant" style="margin: 32px 0;">
        <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
          <line x1="60" y1="540" x2="560" y2="540" stroke="#0A0A0A" stroke-width="1.5"/>
          <line x1="60" y1="540" x2="60" y2="40" stroke="#0A0A0A" stroke-width="1.5"/>
          <text class="axis-label" x="310" y="580" text-anchor="middle">Easier to deploy at scale →</text>
          <text class="axis-label" x="40" y="290" text-anchor="middle" transform="rotate(-90 40 290)">Actionable insights →</text>
          <circle class="competitor-marker" cx="180" cy="440" r="14"/>
          <text class="competitor" x="200" y="445">Manual inspection</text>
          <circle class="competitor-marker" cx="420" cy="430" r="14"/>
          <text class="competitor" x="440" y="435">BroodMinder</text>
          <circle class="competitor-marker" cx="240" cy="280" r="14"/>
          <text class="competitor" x="260" y="285">Solution Bee</text>
          <circle class="competitor-marker" cx="180" cy="180" r="14"/>
          <text class="competitor" x="200" y="185">Beewise</text>
          <circle class="pollenpal-marker" cx="460" cy="160" r="22"/>
          <text class="competitor" x="490" y="166" style="font-size:15px;font-weight:700">PollenPal</text>
        </svg>
      </div>

      <h3>Unfair advantages</h3>
      <p><strong>Data flywheel.</strong> Every bee we image and every inspection log we collect improves the model. Competitors don't have visual datasets at this scale; the gap widens with every yard we deploy. This is the moat that compounds — software, not hardware (<a href="#solution" class="xref">see §3 Solution</a>).</p>

      <p><strong>Founder–operator fit.</strong> Robert is a 17-year beekeeper, not a generalist hardware founder pivoting into ag. Daniel built spacecraft hardware at Apex Space and Blue Origin. The product reflects what beekeepers actually need, not what an outsider thinks they need — and that came out of fifty interviews and Robert's own hives.</p>

      <ol class="footnote-list">
        <li id="fn-6-1">¹ Competitor positioning sourced from public marketing materials and customer interviews. BroodMinder pricing: <a href="https://broodminder.com">broodminder.com</a>. Beewise architecture: <a href="https://www.beewise.ag">beewise.ag</a>. <a href="#fnref-6-1">↩</a></li>
      </ol>
    </section>
```

- [ ] **Step 2: Verify**

Reload. Confirm the 2x2 quadrant SVG renders identically to the previous investors page.

- [ ] **Step 3: Commit**

```bash
git add investors.html
git commit -m "Add §6 Competition with quadrant SVG"
```

---

### Task 12: §7 Strategic Roadmap (Search / Systematize / Scale)

- [ ] **Step 1: Append §7 markup**

```html
    <section id="roadmap">
      <div class="memo-eyebrow">[07] · Strategic Roadmap</div>
      <h2>Search → Systematize → Scale.</h2>
      <p class="thesis-lead">Three phases: <strong>Search</strong> (now: threat detection in commercial pilots), <strong>Systematize</strong> (next: insightful recommendations and corporate beekeeping channel), <strong>Scale</strong> (later: autonomous response and crop expansion).</p>

      <p>Each phase has a product milestone, a GTM motion calibrated to that product's unit economics, and a single inflection point that, once cleared, unlocks the next phase.</p>

      <div class="memo-table-wrap">
        <table class="memo-table roadmap-table">
          <thead>
            <tr>
              <th></th>
              <th class="phase-now">Now (Search) · 2026</th>
              <th class="phase-next">Next (Systematize) · 2027</th>
              <th class="phase-later">Later (Scale) · 2028+</th>
            </tr>
          </thead>
          <tbody>
            <tr><td>Product</td><td>Threat detection (varroa, africanization, queen)</td><td>Insightful recommendations (treatment timing, crew dispatch)</td><td>Autonomous response; crop / orchard expansion</td></tr>
            <tr><td>GTM motion</td><td>Direct sales: 3 pilots → 8 commercial farms</td><td>Corporate beekeeping platform partnerships (Best Bees, Alvéole)</td><td>Enterprise + international; crop monitoring expansion</td></tr>
            <tr><td>Unit econ</td><td>$4/hive/mo, $72K ACV</td><td>+ $20/hive/mo partnership tier (rev share)</td><td>ARPU $6, GM 71%</td></tr>
            <tr><td>KPI</td><td>5,000 hives under management</td><td>20 farms, 30K HUM</td><td>80 farms, 120K HUM</td></tr>
            <tr><td>Inflection</td><td>First paid commercial deployment</td><td>First $1M ARR</td><td>Profitability (EBIT positive)</td></tr>
          </tbody>
        </table>
      </div>

      <p><strong>Search (2026).</strong> The job is to confirm three things: that the hardware survives 12 months in a commercial yard, that the model maintains accuracy across geographies, and that beekeepers will pay $4/hive/mo for what they see in the dashboard. Three pilots are committed in CT, NY, and CA. Use of funds is structured around this phase (<a href="#ask" class="xref">§12 Ask</a>).</p>

      <p><strong>Systematize (2027).</strong> Once the product proves out, we layer recommendations on top of detection — treatment timing, crew dispatch, yard-level trends — and open the partnership channel with Best Bees and Alvéole. The partnership channel is what unlocks our first $1M ARR without a large direct-sales team.</p>

      <p><strong>Scale (2028+).</strong> Autonomous response (closing the loop with in-hive interventions) and SAM expansion into precision farming (<a href="#market" class="xref">§5 Market</a>). Path to 80 farms, 120K hives under management, and $4.6M revenue by 2030 (<a href="#financials" class="xref">§8 Financials</a>).</p>

      <ol class="footnote-list">
        <li id="fn-7-1">¹ PollenPal Business Model v8. Cohort assumptions: 16/22/28/34/40 commercial farms by year. <a href="#fnref-7-1">↩</a></li>
      </ol>
    </section>
```

- [ ] **Step 2: Verify**

Reload. Confirm roadmap table renders with cream/gold/gold-dark accent strips on the three phase headers.

- [ ] **Step 3: Commit**

```bash
git add investors.html
git commit -m "Add §7 Strategic Roadmap with Search/Systematize/Scale"
```

---

### Task 13: §8 Financial Overview (P&L table + 2 inline SVG charts)

- [ ] **Step 1: Append §8 markup**

```html
    <section id="financials">
      <div class="memo-eyebrow">[08] · Financial Overview</div>
      <h2>$40K to $4.6M revenue, 2026 to 2030.</h2>
      <p class="thesis-lead">Revenue scales from $40K (2026) to $4.6M (2030); EBIT margin moves from -201 percent to +41 percent over the same window, supported by hardware BOM falling $46 to $18 and ARPU rising as feature stack matures.<sup class="fn-ref"><a href="#fn-8-1" id="fnref-8-1">¹</a></sup></p>

      <h3>5-year P&amp;L summary</h3>
      <div class="memo-table-wrap">
        <table class="memo-table">
          <thead>
            <tr><th></th><th>2026</th><th>2027</th><th>2028</th><th>2029</th><th>2030</th></tr>
          </thead>
          <tbody>
            <tr><td>Revenue</td><td>$40K</td><td>$172K</td><td>$653K</td><td>$1,947K</td><td>$4,648K</td></tr>
            <tr><td>Gross profit</td><td>$17K</td><td>$95K</td><td>$410K</td><td>$1,305K</td><td>$3,285K</td></tr>
            <tr><td>Gross margin %</td><td>44%</td><td>56%</td><td>63%</td><td>67%</td><td>71%</td></tr>
            <tr><td>Operating expenses</td><td>($97K)</td><td>($259K)</td><td>($526K)</td><td>($958K)</td><td>($1,390K)</td></tr>
            <tr class="total"><td>EBIT</td><td>($80K)</td><td>($164K)</td><td>($116K)</td><td>$347K</td><td>$1,895K</td></tr>
            <tr><td>EBIT margin %</td><td>(201%)</td><td>(95%)</td><td>(18%)</td><td>18%</td><td>41%</td></tr>
          </tbody>
        </table>
      </div>

      <div class="chart-frame">
        <div class="chart-title">Revenue ramp 2026–2030</div>
        <svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Revenue ramp from $40K in 2026 to $4.6M in 2030">
          <!-- Baseline -->
          <line x1="40" y1="240" x2="580" y2="240" stroke="#EAEAEA" stroke-width="1"/>
          <!-- Bars (max value $4,648 → 200px tall) -->
          <!-- 2026 $40K -->
          <rect class="bar-fill" x="80"  y="238" width="60" height="2"   fill="#E8A43A"/>
          <text x="110" y="232" text-anchor="middle" font-size="12" font-weight="600" fill="#0A0A0A">$40K</text>
          <text x="110" y="262" text-anchor="middle" font-size="12" fill="#3A3A3A">2026</text>
          <!-- 2027 $172K -->
          <rect class="bar-fill" x="180" y="231" width="60" height="9"   fill="#E8A43A"/>
          <text x="210" y="225" text-anchor="middle" font-size="12" font-weight="600" fill="#0A0A0A">$172K</text>
          <text x="210" y="262" text-anchor="middle" font-size="12" fill="#3A3A3A">2027</text>
          <!-- 2028 $653K -->
          <rect class="bar-fill" x="280" y="212" width="60" height="28"  fill="#E8A43A"/>
          <text x="310" y="206" text-anchor="middle" font-size="12" font-weight="600" fill="#0A0A0A">$653K</text>
          <text x="310" y="262" text-anchor="middle" font-size="12" fill="#3A3A3A">2028</text>
          <!-- 2029 $1,947K -->
          <rect class="bar-fill" x="380" y="156" width="60" height="84"  fill="#E8A43A"/>
          <text x="410" y="150" text-anchor="middle" font-size="12" font-weight="600" fill="#0A0A0A">$1.95M</text>
          <text x="410" y="262" text-anchor="middle" font-size="12" fill="#3A3A3A">2029</text>
          <!-- 2030 $4,648K -->
          <rect class="bar-fill" x="480" y="40"  width="60" height="200" fill="#E8A43A"/>
          <text x="510" y="34"  text-anchor="middle" font-size="12" font-weight="600" fill="#0A0A0A">$4.65M</text>
          <text x="510" y="262" text-anchor="middle" font-size="12" fill="#3A3A3A">2030</text>
          <!-- First profitable year annotation -->
          <line x1="370" y1="20" x2="370" y2="240" stroke="#C2851A" stroke-width="1" stroke-dasharray="3 3"/>
          <text x="365" y="16" text-anchor="end" font-size="10" font-style="italic" fill="#C2851A">First profitable year →</text>
        </svg>
        <div class="chart-caption">Source: PollenPal Business Model v8. Assumes commercial cohort 16 / 22 / 28 / 34 / 40 farms by year, 0.7%/mo churn, ARPU $4 → $6 over 5 years. Hobbyist cohort 50 / 200 / 600 / 1,500 / 3,500.</div>
      </div>

      <div class="chart-frame">
        <div class="chart-title">Gross margin scales as hardware cost falls</div>
        <svg viewBox="0 0 600 240" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Gross margin rises 44% to 71% while hardware BOM falls $46 to $18">
          <!-- Y axes: GM% on left (0-80%), HW $ on right (0-50) -->
          <line x1="40" y1="200" x2="560" y2="200" stroke="#EAEAEA" stroke-width="1"/>
          <!-- Year labels -->
          <text x="100" y="222" text-anchor="middle" font-size="12" fill="#3A3A3A">2026</text>
          <text x="200" y="222" text-anchor="middle" font-size="12" fill="#3A3A3A">2027</text>
          <text x="300" y="222" text-anchor="middle" font-size="12" fill="#3A3A3A">2028</text>
          <text x="400" y="222" text-anchor="middle" font-size="12" fill="#3A3A3A">2029</text>
          <text x="500" y="222" text-anchor="middle" font-size="12" fill="#3A3A3A">2030</text>
          <!-- HW cost bars (light gold tint, height = $ × 3) -->
          <rect x="80"  y="62"  width="40" height="138" fill="#FFECB7"/>
          <rect x="180" y="98"  width="40" height="102" fill="#FFECB7"/>
          <rect x="280" y="116" width="40" height="84"  fill="#FFECB7"/>
          <rect x="380" y="134" width="40" height="66"  fill="#FFECB7"/>
          <rect x="480" y="146" width="40" height="54"  fill="#FFECB7"/>
          <text x="100" y="58"  text-anchor="middle" font-size="11" fill="#0A0A0A">$46</text>
          <text x="200" y="94"  text-anchor="middle" font-size="11" fill="#0A0A0A">$34</text>
          <text x="300" y="112" text-anchor="middle" font-size="11" fill="#0A0A0A">$28</text>
          <text x="400" y="130" text-anchor="middle" font-size="11" fill="#0A0A0A">$22</text>
          <text x="500" y="142" text-anchor="middle" font-size="11" fill="#0A0A0A">$18</text>
          <!-- GM% line (44, 56, 63, 67, 71 → y = 200 - %×2) -->
          <polyline class="line-stroke" points="100,112 200,88 300,74 400,66 500,58" fill="none" stroke="#C2851A" stroke-width="2.5"/>
          <circle cx="100" cy="112" r="4" fill="#C2851A"/>
          <circle cx="200" cy="88"  r="4" fill="#C2851A"/>
          <circle cx="300" cy="74"  r="4" fill="#C2851A"/>
          <circle cx="400" cy="66"  r="4" fill="#C2851A"/>
          <circle cx="500" cy="58"  r="4" fill="#C2851A"/>
          <text x="100" y="106" text-anchor="middle" font-size="11" font-weight="700" fill="#C2851A">44%</text>
          <text x="200" y="82"  text-anchor="middle" font-size="11" font-weight="700" fill="#C2851A">56%</text>
          <text x="300" y="68"  text-anchor="middle" font-size="11" font-weight="700" fill="#C2851A">63%</text>
          <text x="400" y="60"  text-anchor="middle" font-size="11" font-weight="700" fill="#C2851A">67%</text>
          <text x="500" y="52"  text-anchor="middle" font-size="11" font-weight="700" fill="#C2851A">71%</text>
          <!-- Legend -->
          <rect x="40" y="14" width="12" height="12" fill="#FFECB7"/>
          <text x="58" y="24" font-size="11" fill="#3A3A3A">HW cost per device</text>
          <line x1="200" y1="20" x2="218" y2="20" stroke="#C2851A" stroke-width="2.5"/>
          <text x="226" y="24" font-size="11" fill="#3A3A3A">Gross margin %</text>
        </svg>
        <div class="chart-caption">Source: PollenPal Business Model v8. HW cost reflects supplier quotes at 700 → 10,000 unit scale. Gross margin includes cloud, support, and amortized HW per hive.</div>
      </div>

      <h3>Key assumptions, named</h3>
      <p><strong>Cohort.</strong> Commercial farms cumulative: 16 / 22 / 28 / 34 / 40 over 2026-2030. 1,500 hives per commercial farm (industry standard). Hobbyist cohort 50 / 200 / 600 / 1,500 / 3,500.</p>
      <p><strong>Pricing.</strong> ARPU $4 → $6 per hive per month commercial; $8 → $12 hobbyist; $20 partnership rev-share. $2,500 one-time setup commercial.</p>
      <p><strong>Churn.</strong> 0.7 percent monthly across both segments. This is best-in-class for B2B SaaS<sup class="fn-ref"><a href="#fn-8-2" id="fnref-8-2">²</a></sup> — call it out as optimistic for hobbyist; pilot data will calibrate.</p>
      <p><strong>Ramp.</strong> 15 percent first-year revenue capture, rising to 100 percent by Yr 4 as deployments mature.</p>
      <p><strong>HW BOM.</strong> $46 in 2026 falling to $18 by 2030, driven by supplier scale curves at 700 → 10,000 units.</p>
      <p><strong>CAC.</strong> High initial CAC for commercial direct sales, offset by $72K ACV. Partnership channel rev-share bypasses CAC. Hobbyist self-serve targets sub-12-month payback.</p>

      <ol class="footnote-list">
        <li id="fn-8-1">¹ PollenPal Business Model v8 (file: <code>PollenPal Business Model v8.xlsx</code>). All figures derived from named assumptions in the Assumptions tab. <a href="#fnref-8-1">↩</a></li>
        <li id="fn-8-2">² Churnfree, <em>B2B SaaS Benchmarks 2026</em>. Best-in-class B2B SaaS monthly churn is below 1 percent; SMB-focused products typically run 3-7 percent monthly. <a href="https://churnfree.com/blog/b2b-saas-churn-rate-benchmarks/">churnfree.com</a> <a href="#fnref-8-2">↩</a></li>
      </ol>
    </section>
```

- [ ] **Step 2: Verify both charts render**

Reload. Confirm:
- P&L table renders with EBIT row visually emphasized (bold + top border)
- Revenue ramp bar chart renders with 5 bars and the dotted "first profitable year" annotation
- Gross margin chart renders with HW cost bars (light gold) and GM% line (gold-dark)
- Both chart captions render below their charts in muted italic

- [ ] **Step 3: Commit**

```bash
git add investors.html
git commit -m "Add §8 Financial Overview with P&L table and 2 inline SVG charts"
```

---

### Task 14: §9 Traction & Milestones

- [ ] **Step 1: Append §9 markup**

```html
    <section id="traction">
      <div class="memo-eyebrow">[09] · Traction &amp; Milestones</div>
      <h2>From data collection to revenue.</h2>
      <p class="thesis-lead">MVP deployed. 250,000+ training images. 3 commercial pilots committed. 50+ beekeeper interviews. $55K non-dilutive secured. Moving from data collection to revenue in 2026.</p>

      <h3>To date</h3>
      <p><strong>Customer discovery.</strong> 50+ beekeeper interviews (summer 2025 cross-country road trip + phone calls). Sample selection: commercial operators with 500+ hives across CA, TX, FL, CO, NY. 4 Master Beekeepers retained as ongoing advisors.<sup class="fn-ref"><a href="#fn-9-1" id="fnref-9-1">¹</a></sup></p>

      <p><strong>Hardware.</strong> 12 design iterations completed. MVP deployed in South Florida pilot since October 2025. 250,000+ field images captured for training.</p>

      <p><strong>Commercial.</strong> 3 commercial operators committed to 6-month pilot programs (CT, NY, CA). 14 hobbyists on waitlist. $55K non-dilutive funding secured (Columbia Build Lab + others).</p>

      <div class="stat-grid">
        <div class="stat-callout">
          <div class="stat-num">250k+</div>
          <div class="stat-rule"></div>
          <div class="stat-label">Field images trained on</div>
        </div>
        <div class="stat-callout">
          <div class="stat-num">3</div>
          <div class="stat-rule"></div>
          <div class="stat-label">Commercial pilots committed</div>
        </div>
        <div class="stat-callout">
          <div class="stat-num">12</div>
          <div class="stat-rule"></div>
          <div class="stat-label">Hardware iterations</div>
        </div>
        <div class="stat-callout">
          <div class="stat-num">$55K</div>
          <div class="stat-rule"></div>
          <div class="stat-label">Non-dilutive funding secured</div>
        </div>
      </div>

      <h3>Next 12 months</h3>
      <p><strong>Q2 2026.</strong> Production-ready hardware (~700 devices, IP67 enclosure, FCC certification). Funded directly by the <a href="#ask" class="xref">$240K hardware bucket of §12 Ask</a>.</p>
      <p><strong>Q3 2026.</strong> First paid commercial deployment. Confirms ARPU and unit economics.</p>
      <p><strong>Q4 2026.</strong> First partnership pilot (Best Bees or Alvéole). Validates the corporate beekeeping channel.</p>
      <p><strong>Q1 2027.</strong> Corporate beekeeping platform launch. Partnership channel goes live at scale, unlocks Systematize phase (<a href="#roadmap" class="xref">§7 Roadmap</a>).</p>

      <ol class="footnote-list">
        <li id="fn-9-1">¹ Customer interviews, summer 2025. n=50+ commercial and hobbyist beekeepers across CA, TX, FL, CO, NY. <a href="#fnref-9-1">↩</a></li>
      </ol>
    </section>
```

- [ ] **Step 2: Verify**

Reload. Confirm 4 stat callouts render and cross-links to §12 and §7 work.

- [ ] **Step 3: Commit**

```bash
git add investors.html
git commit -m "Add §9 Traction & Milestones"
```

---

### Task 15: §10 Challenges & Risks (4 callout pairs)

- [ ] **Step 1: Append §10 markup**

```html
    <section id="risks">
      <div class="memo-eyebrow">[10] · Challenges &amp; Risks</div>
      <h2>Four candid risks, each with a specific mitigation.</h2>
      <p class="thesis-lead">Model accuracy at scale, hardware reliability in the field, regulatory shifts on treatments, and channel concentration on partnerships. Each is a real risk; each has a specific, funded, time-boxed mitigation tied to the roadmap or use of funds.</p>

      <div class="risk-grid">
        <div class="risk-card is-risk">
          <span class="risk-tag">Technical</span>
          <p><strong>Model accuracy at scale.</strong> Lab-trained YOLO models degrade in the field. Conditions vary across yards (lighting, hive density, bee phenotype). Flagging is not the same as ground-truth.</p>
        </div>
        <div class="risk-card is-mit">
          <span class="mit-tag">Mitigation</span>
          <p>Active labeling pipeline (CVAT) running on production data weekly. A calibration ridge regression model is in development on the <code>feat/calibration-model</code> branch, mapping detection signals to inspection logs. Each pilot delivers ground-truth labels to compound model accuracy.</p>
        </div>
        <div class="risk-card is-risk">
          <span class="risk-tag">Hardware</span>
          <p><strong>Outdoor IoT in hives is brutal.</strong> Dust, propolis, moisture, and 100°F temperature swings break sensors. A device that fails in month 8 is a churn event.</p>
        </div>
        <div class="risk-card is-mit">
          <span class="mit-tag">Mitigation</span>
          <p>12 design iterations already completed. $240K of the pre-seed round is allocated specifically to IP67 enclosure, FCC certification, and ~700 production devices (<a href="#ask" class="xref">§12 Ask</a>). 5 percent annual hardware failure rate is baked into the financial model — we are not pretending the problem doesn't exist.</p>
        </div>
        <div class="risk-card is-risk">
          <span class="risk-tag">Regulatory</span>
          <p><strong>EPA varroa treatment registration shifts.</strong> Oxalic acid, formic acid, and other miticide registrations change periodically. A regulatory change to recommended treatments could disrupt customer protocols.</p>
        </div>
        <div class="risk-card is-mit">
          <span class="mit-tag">Mitigation</span>
          <p>Treatment-agnostic alerting. We surface threats; the customer chooses the treatment. The partnership rev-share model also keeps PollenPal out of chemical-application liability — the corporate platform owns the customer relationship and the treatment decision.</p>
        </div>
        <div class="risk-card is-risk">
          <span class="risk-tag">Market / Channel</span>
          <p><strong>Channel concentration.</strong> ~1,600 U.S. commercial operators is a small TAM if we stay in hive management only. Two corporate beekeeping partners (Best Bees, Alvéole) carry meaningful channel risk.</p>
        </div>
        <div class="risk-card is-mit">
          <span class="mit-tag">Mitigation</span>
          <p>The roadmap explicitly extends from $128M SOM into the $24B precision farming SAM (<a href="#roadmap" class="xref">§7 Scale phase</a>). This is on the calendar, not blue-sky. Three pilots are also in three different states with three different operator profiles, reducing concentration in the Search phase.</p>
        </div>
      </div>

      <ol class="footnote-list">
        <li id="fn-10-1">¹ All risk-mitigation tie-ins are referenced in <a href="#ask" class="xref">§12 Ask</a> (use of funds) or <a href="#roadmap" class="xref">§7 Roadmap</a>. <a href="#fnref-10-1">↩</a></li>
      </ol>
    </section>
```

- [ ] **Step 2: Verify**

Reload. Confirm 4 risk/mitigation card pairs render side-by-side on desktop and stack on mobile (resize below 760px).

- [ ] **Step 3: Commit**

```bash
git add investors.html
git commit -m "Add §10 Challenges & Risks with 4 callout pairs"
```

---

### Task 16: §11 Team

- [ ] **Step 1: Append §11 markup**

```html
    <section id="team">
      <div class="memo-eyebrow">[11] · Team</div>
      <h2>Founder–market fit, plus a 9-year operating partnership.</h2>
      <p class="thesis-lead">A 17-year hobbyist beekeeper paired with an Apex Space hardware engineer who have worked together for nine years, backed by Columbia Build Lab and 4 Master Beekeeper advisors.</p>

      <div class="memo-team-grid">
        <div class="memo-team-card">
          <h3>Robert Schulte</h3>
          <div class="role">Co-founder, CEO</div>
          <p>Ex-BCG. Columbia MBA (2027). UF Industrial &amp; Systems Engineering. 17 years beekeeping (NC family operation). Led the 50-interview customer discovery cross-country, summer 2025.</p>
        </div>
        <div class="memo-team-card">
          <h3>Daniel Drew</h3>
          <div class="role">Co-founder, CTO</div>
          <p>Spacecraft Manufacturing Engineer at Apex Space. Ex-Blue Origin. UF engineering. 9-year working partnership with Robert.</p>
        </div>
        <div class="memo-team-card">
          <h3>Tech team</h3>
          <div class="role">Engineering</div>
          <p>1 Columbia Research Scientist (computer vision; backed by Google + NVIDIA grants). 4 Columbia engineers building the ML pipeline and web app via Columbia Build Lab.</p>
        </div>
        <div class="memo-team-card">
          <h3>Beekeeping advisory</h3>
          <div class="role">Advisors</div>
          <p>4 Master Beekeeper advisors providing hive management and treatment-protocol guidance. Commercial beekeeper partners deploying devices and contributing field-collected ground truth.</p>
        </div>
      </div>
    </section>
```

- [ ] **Step 2: Verify**

Reload. Confirm 4 team cards render in a 2x2 grid on desktop, single column on mobile.

- [ ] **Step 3: Commit**

```bash
git add investors.html
git commit -m "Add §11 Team"
```

---

### Task 17: §12 Ask & Next Steps (use of funds + how to engage)

- [ ] **Step 1: Append §12 markup**

```html
    <section id="ask">
      <div class="memo-eyebrow">[12] · Ask &amp; Next Steps</div>
      <h2>$500K pre-seed SAFE.</h2>
      <p class="thesis-lead">Raising a $500K pre-seed SAFE to fund production hardware, on-prem GPU inference, and the first paid commercial deployments through 2026. $55K of non-dilutive funding is already secured.</p>

      <p>The round buys 18 months of runway and a clean bridge to a seed round in mid-2027, after the first $250K ARR signal validates the commercial unit economics.</p>

      <h3>Use of funds</h3>
      <div class="memo-table-wrap">
        <table class="memo-table">
          <thead>
            <tr><th>Bucket</th><th>$</th><th>Key outcome</th></tr>
          </thead>
          <tbody>
            <tr><td>Hardware &amp; manufacturing</td><td>$240K</td><td>IP67 enclosure, FCC certification, ~700 production devices (<a href="#risks" class="xref">tied to §10 hardware mitigation</a>)</td></tr>
            <tr><td>GPU inference infrastructure</td><td>$75K</td><td>On-prem GPU cluster; 80 percent inference cost cut, sub-second latency (<a href="#solution" class="xref">§3 Solution roadmap</a>)</td></tr>
            <tr><td>ML engineering</td><td>$50K</td><td>Vision model improvements; calibration model on inspection-log ground truth</td></tr>
            <tr><td>Field ops &amp; sales</td><td>$100K</td><td>Commercial customer support and pilot conversion to paid deployment</td></tr>
            <tr><td>SG&amp;A + buffer</td><td>$35K</td><td>Legal, fundraising, contingency</td></tr>
            <tr class="total"><td>Total</td><td>$500K</td><td>18-month runway to seed</td></tr>
          </tbody>
        </table>
      </div>

      <h3>How to engage</h3>
      <div class="next-steps-strip">
        <div class="next-step">Express interest via the form below or email <a href="mailto:hello@pollenpal.com">hello@pollenpal.com</a>.</div>
        <div class="next-step">30-minute intro call with Robert. We walk through the deck and show live deployment data.</div>
        <div class="next-step">Diligence packet: financial model, technical architecture, customer interview index.</div>
        <div class="next-step">SAFE execution. Standard market terms; happy to participate in a syndicate.</div>
      </div>

      <div class="form-card" style="margin-top: 32px;">
        <form id="invForm" action="https://docs.google.com/forms/d/e/1FAIpQLScZLvT2HOrDgzx4v0o0YGF5KoqPiU9s5RIRHZ7R0pF7EaXdUA/formResponse" method="POST" target="hidden_iframe2">
          <div class="form-row"><label for="i-name">Name *</label><input type="text" id="i-name" name="entry.455027715" required></div>
          <div class="form-row"><label for="i-email">Email *</label><input type="email" id="i-email" name="entry.414264367" required></div>
          <div class="form-row"><label for="i-firm">Firm / organization</label><input type="text" id="i-firm" name="entry.119689931"></div>
          <div class="form-row"><label for="i-msg">Tell us about your interest</label><textarea id="i-msg" name="entry.1292345725"></textarea></div>
          <button type="submit">Get in touch →</button>
        </form>
        <iframe name="hidden_iframe2" style="display:none"></iframe>
      </div>
    </section>
```

- [ ] **Step 2: Verify form action**

Reload. Confirm the form action URL exactly matches the existing one (`1FAIpQLScZLvT2HOrDgzx4v0o0YGF5KoqPiU9s5RIRHZ7R0pF7EaXdUA`). Confirm 4 next-steps cards render.

- [ ] **Step 3: Commit**

```bash
git add investors.html
git commit -m "Add §12 Ask & Next Steps with use-of-funds table"
```

---

### Task 18: §13 Appendix (4 collapsibles)

- [ ] **Step 1: Append §13 markup**

```html
    <section id="appendix">
      <div class="memo-eyebrow">[13] · Appendix</div>
      <h2>Optional deep-dives.</h2>
      <p class="thesis-lead">Customer story, unit economics, hardware/ML detail, and primary research methodology. Each section is collapsed by default; expand the ones relevant to your diligence.</p>

      <details class="appendix-section">
        <summary>A. Customer story — Wendy, Ventura, CA</summary>
        <div class="appendix-body">
          <p>Wendy Mather runs Blue Ridge Honey Co. in Ventura, CA — a 5,000-colony commercial operation specializing in pollination contracts. Africanization is a $100K/year line item by her own estimate: africanized swarms force her crew to abandon affected yards, lose pollination revenue, and replace queens.</p>
          <p>From an interview in July 2025: <em>"Identifying and treating africanization early would be worth $100K a year to our operation."</em> Mites and queen issues compound on top — a typical Wendy yard loses 30-40 percent of colonies in a bad year, and recovery means buying replacement packages at $200/colony plus labor.</p>
          <p>Wendy is one of our 3 committed pilot operators for 2026. She has agreed to share inspection logs and ground-truth treatment outcomes throughout the pilot, which compounds directly into the calibration model (<a href="#risks" class="xref">§10 Technical mitigation</a>).</p>
        </div>
      </details>

      <details class="appendix-section">
        <summary>B. Unit economics deep dive</summary>
        <div class="appendix-body">
          <p><strong>Per-hive contribution margin walk (Year 1 commercial).</strong></p>
          <p>Revenue: $4/hive/mo × 12 = <strong>$48 ARPU Yr 1</strong> (rising to $72 by Yr 5 as feature stack matures).<br>
          Cloud cost: $1.50/hive/mo declining to $0.75/hive/mo as inference moves on-prem = <strong>$18/yr</strong> (Yr 1).<br>
          Hardware amortized: $46 BOM ÷ 3-year life = $15.33/yr per device. Commercial deployment uses 0.33 devices per hive (one device per 3 hives). <strong>$5.11/yr HW per hive.</strong><br>
          Implied Yr-1 contribution margin: ~$25/hive after cloud, support, and amortized HW. Setup ($2,500) and direct sales overhead are absorbed at the farm level, not the hive.</p>
          <p><strong>LTV / CAC and payback period</strong> will be confirmed once the first paid commercial deployment lands in Q3 2026 (<a href="#traction" class="xref">§9 Traction</a>). Modeled CAC payback: under 18 months for commercial; under 12 months target for hobbyist self-serve.</p>
        </div>
      </details>

      <details class="appendix-section">
        <summary>C. Hardware / ML technical detail</summary>
        <div class="appendix-body">
          <p><strong>Hardware.</strong> Pi-class compute (Raspberry Pi or equivalent). Imaging stack inspired by proven CV techniques optimized for low-power, high-throughput capture. MLX90640 thermal sensor, camera, sound sensor (I2S mic), external switches for labor coordination. 3D-printed skeleton, 12 design variations tested. Solar panel + LTE for remote yards.</p>
          <p><strong>ML pipeline.</strong> YOLO11 architecture (Ultralytics). 250,000+ images annotated through CVAT (self-hosted instance, t3.2xlarge). Two-stage detection (bee + pose → crop → mite detection), mAP50 = 0.896 at last training run. Cloud inference today (FastAPI + RDS Postgres on AWS), on-prem GPU on the roadmap.</p>
          <p><strong>Calibration model.</strong> Ridge regression maps detection signals (entrance counts, pose distributions, behavior anomalies) to inspection ground truth (alcohol-wash mite counts, queen status, africanization assessments). Active development branch <code>feat/calibration-model</code>.</p>
        </div>
      </details>

      <details class="appendix-section">
        <summary>D. Primary research methodology</summary>
        <div class="appendix-body">
          <p>50+ semi-structured interviews conducted in summer 2025 via cross-country road trip plus phone calls. Sample selection: commercial operators with 500+ hives, plus a smaller number of large hobbyist operations, across CA, TX, FL, CO, and NY.</p>
          <p>Interview structure: open-ended on current pain points, hive management workflow, treatment protocols, and digital tooling adoption. Closed-ended on willingness to pay and current spend on diagnostics.</p>
          <p>4 Master Beekeepers retained as ongoing advisors after the road trip (combined ~80 years commercial experience). Pull quotes throughout the memo (Kristen, §2; Wendy, §13A) are from this primary research dataset.</p>
        </div>
      </details>
    </section>
```

- [ ] **Step 2: Verify all 4 appendix collapsibles**

Reload. Click each `▸` summary — confirm expansion/collapse works and the rotation animation triggers. All cross-links inside the bodies should be functional.

- [ ] **Step 3: Commit**

```bash
git add investors.html
git commit -m "Add §13 Appendix with 4 collapsible deep-dives"
```

---

## Phase 3 — Polish & verification (Tasks 19–23)

### Task 19: Cross-link integrity sweep

- [ ] **Step 1: Click-test every cross-link**

In the rendered page, click each of the following cross-links and confirm it scrolls to the correct section:

| From | Target | Expected |
|---|---|---|
| §1 — "$500K pre-seed SAFE" | `#ask` | scroll to §12 |
| §3 — "funded by §12 Ask" | `#ask` | scroll to §12 |
| §3 — "see §6 Competition" | `#competition` | scroll to §6 |
| §4 — "deeper market geometry sits in §5" | `#market` | scroll to §5 |
| §5 — "§8 Financial Overview" | `#financials` | scroll to §8 |
| §6 — "see §3 Solution" | `#solution` | scroll to §3 |
| §7 — "§12 Ask" | `#ask` | scroll to §12 |
| §7 — "§5 Market" | `#market` | scroll to §5 |
| §7 — "§8 Financials" | `#financials` | scroll to §8 |
| §9 — "$240K hardware bucket of §12" | `#ask` | scroll to §12 |
| §9 — "§7 Roadmap" | `#roadmap` | scroll to §7 |
| §10 — "§12 Ask" | `#ask` | scroll to §12 |
| §10 — "§7 Scale phase" | `#roadmap` | scroll to §7 |
| §12 — "§10 hardware mitigation" | `#risks` | scroll to §10 |
| §12 — "§3 Solution roadmap" | `#solution` | scroll to §3 |
| §13A — "§10 Technical mitigation" | `#risks` | scroll to §10 |
| §13B — "§9 Traction" | `#traction` | scroll to §9 |

Any broken anchor: fix the `href` in the corresponding section markup.

- [ ] **Step 2: Footnote round-trip test**

Click each `¹²³⁴⁵` superscript in §1, §2, §3, §4, §5, §6, §7, §8, §9, §10. Confirm:
- Clicking the superscript scrolls to the matching `#fn-<section>-<n>` endnote
- Endnote is visually highlighted (`:target` style)
- Clicking `↩` in the endnote scrolls back to the inline marker

If any footnote ID mismatch: fix in markup.

- [ ] **Step 3: Commit any fixes**

```bash
git add investors.html
git commit -m "Fix any cross-link or footnote ID mismatches"
```

(If no fixes needed, skip the commit.)

---

### Task 20: Word count + content sweep (no em-dashes, no emojis, no banned copy)

- [ ] **Step 1: Word count check**

Run a quick word count on the body content (excluding nav, TOC, footer, footnote text):

```bash
cd /c/projects/pollenpal-website
python3 -c "
import re
from html.parser import HTMLParser

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.skip_depth = 0
        self.skip_tags = {'script', 'style', 'nav', 'header', 'footer', 'aside', 'ol'}
        self.in_main = False
        self.parts = []
    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        if tag == 'main' and attrs_d.get('id') == 'main':
            self.in_main = True
        elif tag in self.skip_tags or attrs_d.get('class', '').startswith('footnote-list'):
            self.skip_depth += 1
    def handle_endtag(self, tag):
        if tag == 'main':
            self.in_main = False
        elif tag in self.skip_tags:
            self.skip_depth = max(0, self.skip_depth - 1)
    def handle_data(self, data):
        if self.in_main and self.skip_depth == 0:
            self.parts.append(data)

p = TextExtractor()
p.feed(open('investors.html').read())
text = ' '.join(p.parts)
words = re.findall(r\"[A-Za-z']+\", text)
print(f'Body word count (rough): {len(words)}')
"
```

Expected: 1,500–2,000 words. If under: not a failure (denser is better); just confirm none of the section thesis or required content was accidentally dropped. If over 2,200: trim non-essential prose.

- [ ] **Step 2: Em-dash sweep**

```bash
grep -n "—" /c/projects/pollenpal-website/investors.html
```

Expected output: empty. If any em-dashes appear, replace each with a period, semicolon, comma, or " - " (space-hyphen-space) per `feedback_no_emdashes.md`.

- [ ] **Step 3: Emoji sweep**

```bash
grep -nP "[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]" /c/projects/pollenpal-website/investors.html
```

Expected: only the `→` arrow inside form button (`Get in touch →`) and `▸` glyphs (those are in CSS, not HTML, so won't match). The skip-link arrow is also OK. No 🐝, 🌻, or other decorative emojis.

- [ ] **Step 4: Banned copy sweep**

```bash
grep -in "transforming\|revolutionizing\|cutting-edge\|disrupt\|leverage" /c/projects/pollenpal-website/investors.html
```

Expected: empty. If anything matches: rewrite that sentence.

- [ ] **Step 5: Commit any fixes**

```bash
git add investors.html
git commit -m "Content sweep: em-dashes, emojis, banned copy"
```

---

### Task 21: Mobile responsive verification

- [ ] **Step 1: Test at 4 breakpoints**

Open DevTools (F12) → Toggle Device Toolbar (Ctrl+Shift+M). Test at:

- **360px (iPhone SE):** TOC dropdown only, single-column tables (horizontally scrollable), risk cards stacked, team cards stacked. No horizontal scroll on body.
- **600px:** stat callouts stack 1-up, solution image strip stacks vertically.
- **960px:** TOC is still mobile dropdown (collapses below 1100px), tables fit width, risk cards still 2-up.
- **1100px:** TOC rail switches to sticky left position, scroll progress bar visible.

- [ ] **Step 2: Fix any breakpoint issues**

Common issues to check for:
- Tables overflow → confirm `.memo-table-wrap` has `overflow-x: auto`
- Long URL in footnotes wrapping ugly → consider truncating display text
- Stat callout numbers wrapping → verify `flex-shrink: 0` on numerals

- [ ] **Step 3: Commit any fixes**

```bash
git add styles.css investors.html
git commit -m "Mobile responsive fixes from breakpoint sweep"
```

(Skip commit if no fixes needed.)

---

### Task 22: Print stylesheet verification

- [ ] **Step 1: Trigger print preview**

In the desktop browser at full width, press `Ctrl+P` (or `Cmd+P` on Mac). Confirm:
- TOC rail is hidden
- Header is hidden
- Confidential banner appears at top of every page
- Page numbers appear at bottom (via `@page @bottom-center` rule)
- Charts render in B&W or with restored fills (the `!important` overrides keep gold-dark)
- Section breaks honored (no section split awkwardly across pages where avoidable)
- All cross-links underlined

- [ ] **Step 2: Save to PDF and review**

In the print dialog, "Save as PDF". Open the resulting PDF. Confirm:
- 12-15 pages total
- Footnotes appear at the end of their owning section (not as a global block)
- Tables fit page width (none overflow)
- Charts render correctly

- [ ] **Step 3: Commit any print-CSS fixes**

```bash
git add styles.css
git commit -m "Print stylesheet refinements after PDF review"
```

(Skip if no fixes.)

---

### Task 23: Final integration check + ship

- [ ] **Step 1: Top-to-bottom read**

Read the entire memo in the browser as a cold reader would. Watch for:
- Any sentence that doesn't make sense in isolation
- Any reference to "the deck" without context (the memo must stand alone)
- Any "TODO" / "TBD" / placeholder text remaining

- [ ] **Step 2: Verify acceptance criteria from spec**

Walk the spec's `## 12. Acceptance criteria` checklist:
- All 13 LYS sections present in user-specified order ✓
- Word count 1,500–2,000 ✓
- Every quantitative claim cites source or assumption ✓
- Four fits explicitly named in §4 ✓
- Search/Systematize/Scale named in §7 ✓
- TOC functional desktop + mobile ✓
- Confidential banner + footer ✓
- Charts render as inline SVG ✓
- 4 tables use `.memo-table` ✓
- 4 risk callout pairs in §10 ✓
- Appendix collapsibles work ✓
- 9+ cross-links functional ✓
- Print stylesheet produces clean PDF ✓
- Mobile responsive ✓
- No em-dashes, no emojis, no gradient hero ✓

- [ ] **Step 3: Pull Pi-side commits and reconcile, then push**

```bash
cd /c/projects/pollenpal-website
git stash
git pull origin main
git stash pop
# Resolve any conflicts in index.html (Pi may have edited founder story)
git add investors.html styles.css scripts.js docs/superpowers/specs/2026-05-03-investors-memo-design.md docs/superpowers/plans/2026-05-03-investors-memo.md
git commit -m "Add investor memo spec + plan to docs"
git push origin main
```

- [ ] **Step 4: Sync to Pi**

```bash
bash sync-pi.sh push
```

- [ ] **Step 5: Verify live**

Visit `https://pollenpal.com/investors` after GitHub Pages publishes (1–2 minutes). Confirm:
- Page loads
- TOC behavior works on the live site (CDN-cached `scripts.js`)
- Charts render
- Form submission works (test with a throwaway email; check Google Form responses)

---

## Out of scope (not in this plan)

- Production accuracy claim ("~95%" or similar): held until calibration model produces defensible numbers.
- LTV/CAC and payback ratios as hard numbers: narrative only in §13B, await first paid deployment.
- Live deployment data dashboard or "see your hive" demo: deferred.
- Investor-only authentication / NDA gate: kept publicly reachable per existing `/investors` precedent.
- Homepage edits (`index.html`): the existing claim policy on the homepage remains unchanged. Investor memo includes additional figures (BOM, interviews, etc.) approved for investor context only.
