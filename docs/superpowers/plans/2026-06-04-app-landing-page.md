# PollenPal App Landing Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the `/hobbyist` page with an image-heavy, software-only landing page that sells the deviceless PollenPal inspection app (free 30-day trial, then $6.99/mo, up to 10 hives) and drives self-serve signup at `app.pollenpal.com`.

**Architecture:** Static HTML page (`hobbyist.html`) reusing the existing `styles.css` design system, with a small set of new CSS components (alternating feature rows, a pricing block, an FAQ). Real app screenshots of Bill's deviceless hives (captured as `robert@pollenpal.com`) are the centerpiece imagery. No build step, no framework, no backend. The old camera-hardware version is archived.

**Tech Stack:** HTML5, CSS (hand-written, `styles.css`), `scripts.js` (existing mobile nav + form swap), Python `http.server` for local preview, Chrome DevTools MCP for verification and screenshot capture, `scripts/prep_assets.py` (Pillow) for image optimization.

**Spec:** `docs/superpowers/specs/2026-06-04-app-landing-page-design.md`

**Branch:** `hobbyist-app-page` (already created; spec already committed there).

---

## Conventions for this plan

- This is a static site with no test runner. "Verification" = serve the repo locally and check rendering + console with the Chrome DevTools MCP.
- **Local preview:** run once at the start, leave running in the background:
  ```bash
  cd /c/projects/Pollenpal-website && python -m http.server 8099
  ```
  Then the page is at `http://localhost:8099/hobbyist.html` (and `http://localhost:8099/` for the homepage).
- **Console check** after any page change: use `mcp__chrome-devtools__navigate_page` to the URL, then `mcp__chrome-devtools__list_console_messages` and confirm no errors (ignore favicon 404s on localhost).
- **No em-dashes** anywhere (site-wide rule). Use periods, semicolons, commas.
- Reuse existing classes; only add new CSS where this plan defines it.

---

## File Structure

- **Modify:** `hobbyist.html` — full content replacement (the new app landing page).
- **Modify:** `styles.css` — append new components: `.feature-row`, `.pricing`, `.faq`.
- **Modify:** `index.html` — fix footer "Hobbyist waitlist" link label.
- **Modify:** `investors.html` — fix footer "Hobbyist waitlist" link label (if present).
- **Create:** `archive/hobbyist-hardware/index.html` — preserved old camera-hobbyist page.
- **Create:** `images/app-hero.jpg`, `images/app-inspection.jpg`, `images/app-reminder.jpg`, `images/app-apiary.jpg`, `images/app-history.jpg` — captured deviceless app screenshots.

---

## Task 1: Archive the old camera-hobbyist page

Preserve the current `/hobbyist` content before replacing it.

**Files:**
- Create: `archive/hobbyist-hardware/index.html`

- [ ] **Step 1: Copy the current hobbyist page into the archive**

```bash
cd /c/projects/Pollenpal-website
mkdir -p archive/hobbyist-hardware
cp hobbyist.html archive/hobbyist-hardware/index.html
```

- [ ] **Step 2: Fix asset/link paths in the archived copy**

The archived page lives one level deeper but `styles.css`, `/images/...`, and `/scripts.js` are referenced with absolute `/` paths, so they still resolve. No path edits needed. Verify by grepping that all asset refs are root-absolute:

```bash
grep -nE 'src="(?!/|https)|href="(?!/|https|#|mailto)' archive/hobbyist-hardware/index.html || echo "all refs are absolute or external — OK"
```

Expected: prints "all refs are absolute or external — OK".

- [ ] **Step 3: Commit**

```bash
git add archive/hobbyist-hardware/index.html
git commit -m "archive: preserve camera-hardware hobbyist page before app rebuild"
```

---

## Task 2: Add new CSS components to styles.css

Add three components the new page needs and the design system lacks: an alternating image/text feature row, a pricing block, and an FAQ list. Append to the END of `styles.css` so existing rules are untouched.

**Files:**
- Modify: `styles.css` (append)

- [ ] **Step 1: Append the new component CSS**

Append exactly this block to the end of `styles.css`:

```css

/* ============================================================
   APP LANDING PAGE COMPONENTS (hobbyist.html)
   ============================================================ */

/* Alternating image/text feature rows */
.feature-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 72px;
  align-items: center;
  padding: 72px 0;
}
.feature-row + .feature-row { border-top: 1px solid var(--line); }
.feature-row .feature-copy h2 { font-size: clamp(28px, 4vw, 38px); margin-bottom: 18px; }
.feature-row .feature-copy p { color: var(--ink-soft); font-size: 17px; line-height: 1.65; }
.feature-shot {
  display: flex; justify-content: center;
}
.feature-shot img {
  width: 100%; max-width: 300px;
  border-radius: var(--radius-lg);
  box-shadow: 0 30px 80px -20px rgba(10,10,10,0.25), 0 8px 20px -6px rgba(10,10,10,0.12);
}
/* Flip every even row so images alternate sides */
.feature-row:nth-child(even) .feature-copy { order: 2; }
.feature-row:nth-child(even) .feature-shot { order: 1; }
@media (max-width: 860px) {
  .feature-row { grid-template-columns: 1fr; gap: 36px; padding: 56px 0; }
  .feature-row:nth-child(even) .feature-copy { order: 2; }
  .feature-row:nth-child(even) .feature-shot { order: 1; }
  .feature-row .feature-copy { order: 2; }
  .feature-row .feature-shot { order: 1; }
  .feature-shot img { max-width: 260px; }
}

/* Pricing block */
.pricing { text-align: center; }
.pricing .price-card {
  max-width: 460px; margin: 40px auto 0;
  border: 1px solid var(--line); border-radius: var(--radius-lg);
  padding: 44px 36px; background: var(--cream-soft);
}
.pricing .price-amount { font-size: 48px; font-weight: 800; color: var(--ink); line-height: 1; }
.pricing .price-amount span { font-size: 18px; font-weight: 600; color: var(--muted); }
.pricing .price-trial { margin: 14px 0 4px; font-size: 18px; color: var(--gold-dark); font-weight: 700; }
.pricing .price-note { color: var(--ink-soft); font-size: 15px; margin-bottom: 28px; }

/* FAQ */
.faq .faq-list { max-width: 720px; margin: 40px auto 0; }
.faq .faq-item { padding: 24px 0; border-top: 1px solid var(--line); }
.faq .faq-item:last-child { border-bottom: 1px solid var(--line); }
.faq .faq-item h3 { font-size: 19px; margin-bottom: 8px; }
.faq .faq-item p { color: var(--ink-soft); font-size: 16px; line-height: 1.6; }
```

- [ ] **Step 2: Verify CSS parses (no stray braces)**

```bash
cd /c/projects/Pollenpal-website
node -e "const c=require('fs').readFileSync('styles.css','utf8');const o=(c.match(/{/g)||[]).length,x=(c.match(/}/g)||[]).length;if(o!==x){console.error('UNBALANCED braces',o,x);process.exit(1)}console.log('braces balanced:',o)"
```

Expected: prints `braces balanced: <n>` with matching counts, exit 0.

- [ ] **Step 3: Commit**

```bash
git add styles.css
git commit -m "css: add feature-row, pricing, and faq components for app page"
```

---

## Task 3: Build the new hobbyist.html with placeholder screenshot slots

Replace the page body with the full app-landing structure. Use the existing `images/dashboard-phone.jpg` as a temporary placeholder in every screenshot slot so the layout is verifiable before real captures exist (Task 4 swaps them in).

**Files:**
- Modify: `hobbyist.html` (full replacement)

- [ ] **Step 1: Replace the entire file with the new page**

Write `hobbyist.html` with exactly this content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PollenPal · The hive inspection app for beekeepers</title>
  <meta name="description" content="Log every hive inspection from your phone. Digital records, reminders, and history for your bees. No hardware required. Free 30-day trial, then $6.99/month.">
  <link rel="icon" href="/images/logo-icon.png">
  <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
  <style>
    .hero { position: relative; padding: 96px 0 40px; overflow: hidden; }
    .hero::before {
      content: ""; position: absolute; top: 0; right: -15%;
      width: 60%; height: 100%;
      background: radial-gradient(ellipse at center, var(--cream-soft) 0%, transparent 70%);
      pointer-events: none;
    }
    .hero-grid { position: relative; display: grid; grid-template-columns: 1.15fr 1fr; gap: 72px; align-items: center; }
    .hero h1 { margin-bottom: 28px; }
    .hero .lede { margin-bottom: 28px; }
    .hero-subnote { font-size: 14px; color: var(--muted); margin-top: 16px; }
    .hero-visual { position: relative; display: flex; justify-content: center; align-items: center; }
    .phone-frame {
      position: relative; width: 100%; max-width: 300px; aspect-ratio: 9/19;
      border-radius: 34px; overflow: hidden; background: var(--ink);
      border: 8px solid var(--ink);
      box-shadow: 0 30px 80px -20px rgba(10,10,10,0.25), 0 8px 20px -6px rgba(10,10,10,0.12);
    }
    .phone-frame img { width: 100%; height: 100%; object-fit: cover; object-position: top center; }
    @media (max-width: 960px) {
      .hero { padding: 56px 0 64px; }
      .hero-grid { grid-template-columns: 1fr; gap: 40px; }
      .hero-visual { order: -1; }
      .phone-frame { max-width: 240px; }
    }
  </style>
</head>
<body>

<a href="#main" class="skip-link">Skip to content</a>

<header class="site-header">
  <div class="wrap nav">
    <a href="/" class="nav-logo"><img src="/images/logo-full.png" alt="PollenPal"></a>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">☰</button>
    <nav class="nav-links">
      <a href="/hobbyist" class="current">The app</a>
      <a href="/investors">Investors</a>
    </nav>
    <a href="https://app.pollenpal.com" class="nav-cta nav-cta-login">Log in</a>
    <a href="https://app.pollenpal.com" class="nav-cta">Start free trial →</a>
  </div>
</header>

<main id="main">

  <!-- HERO -->
  <section class="hero">
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <div class="eyebrow">The hive inspection app</div>
        <h1>Every inspection, finally in <span class="serif-italic">one place</span>.</h1>
        <p class="lede">Log what you see at the hive from your phone. Track frames, brood, the queen, and what each colony needs next. No notebook, no hardware. Just your bees and your phone.</p>
        <a href="https://app.pollenpal.com" class="btn btn-primary">Start your free trial →</a>
        <p class="hero-subnote">Free for 30 days. No credit card. Just your phone.</p>
      </div>
      <div class="hero-visual">
        <div class="phone-frame">
          <img src="/images/dashboard-phone.jpg" alt="PollenPal app showing a hive overview">
        </div>
      </div>
    </div>
  </section>

  <!-- FEATURE ROWS -->
  <section class="section">
    <div class="wrap">

      <div class="feature-row">
        <div class="feature-copy">
          <div class="eyebrow">Digital inspections</div>
          <h2>Log it once, the right way.</h2>
          <p>A structured form for every inspection: frames of bees, brood, honey and pollen, queen status, temperament, feeding, and swarm signs. Tap through it in the bee yard and you are done. No more squinting at a rained-on notebook.</p>
        </div>
        <div class="feature-shot"><img src="/images/dashboard-phone.jpg" alt="PollenPal inspection form on a phone"></div>
      </div>

      <div class="feature-row">
        <div class="feature-copy">
          <div class="eyebrow">Reminders</div>
          <h2>Never forget what a hive needs.</h2>
          <p>Set the next visit when you close up the box and PollenPal reminds you when it is due. The colony that needs feeding, the split you planned, the requeen you promised yourself. It is all waiting for you next time.</p>
        </div>
        <div class="feature-shot"><img src="/images/dashboard-phone.jpg" alt="PollenPal next-inspection reminder on a phone"></div>
      </div>

      <div class="feature-row">
        <div class="feature-copy">
          <div class="eyebrow">Your apiary</div>
          <h2>One hive or a hundred.</h2>
          <p>Organize your hives into yards and see them all at a glance. Whether you keep two colonies in the backyard or a few yards across town, every hive has its own home in the app.</p>
        </div>
        <div class="feature-shot"><img src="/images/dashboard-phone.jpg" alt="PollenPal apiary and hive list on a phone"></div>
      </div>

      <div class="feature-row">
        <div class="feature-copy">
          <div class="eyebrow">History and photos</div>
          <h2>See how a colony is doing over time.</h2>
          <p>Every inspection is saved with the photos you took, building a timeline for each hive. Scroll back through the season and actually understand what happened, instead of guessing.</p>
        </div>
        <div class="feature-shot"><img src="/images/dashboard-phone.jpg" alt="PollenPal inspection history timeline with photos on a phone"></div>
      </div>

    </div>
  </section>

  <!-- TESTIMONIAL -->
  <section class="testimonial" style="background-image:none;background:var(--cream-soft);">
    <div class="wrap" style="position:relative;z-index:1;">
      <blockquote style="color:var(--ink);">"For my first 4 years, I spent $600 on lost hives, and I didn't know why I was losing them."</blockquote>
      <cite style="color:var(--gold-dark);">Karen · Backyard beekeeper, South Florida</cite>
    </div>
  </section>

  <!-- PRICING -->
  <section class="section pricing">
    <div class="wrap">
      <div class="eyebrow center">Simple pricing</div>
      <h2>Start free. Keep going for the price of a coffee.</h2>
      <div class="price-card">
        <div class="price-trial">Free for 30 days</div>
        <div class="price-amount">$6.99<span>/month</span></div>
        <p class="price-note">After your trial. Up to 10 hives. Cancel anytime.</p>
        <a href="https://app.pollenpal.com" class="btn btn-primary">Start your free trial →</a>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section bg-cream faq">
    <div class="wrap">
      <div class="eyebrow center">Questions</div>
      <h2 style="text-align:center;">Good to know.</h2>
      <div class="faq-list">
        <div class="faq-item">
          <h3>Do I need the PollenPal device?</h3>
          <p>No. The app works entirely on its own. The device is a separate product; this is just the inspection software, and it runs on the phone in your pocket.</p>
        </div>
        <div class="faq-item">
          <h3>What do I need to get started?</h3>
          <p>A phone and your hives. Sign up, add your hives, and log your first inspection in a couple of minutes.</p>
        </div>
        <div class="faq-item">
          <h3>Can I cancel anytime?</h3>
          <p>Yes. Cancel whenever you like. If you cancel during the free trial you are never charged.</p>
        </div>
        <div class="faq-item">
          <h3>Is my data mine?</h3>
          <p>Yes. Your hives and your inspection records belong to you.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- FINAL CTA -->
  <section class="pilot">
    <div class="wrap">
      <div class="eyebrow center">Start today</div>
      <h2>Your bees are worth better notes.</h2>
      <p class="lede">Start your free 30-day trial and log your next inspection in the app.</p>
      <a href="https://app.pollenpal.com" class="btn btn-gold">Start your free trial →</a>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="wrap">

    <div class="footer-newsletter" id="newsletter">
      <div class="footer-newsletter-copy">
        <h3>Stay in touch.</h3>
        <p>Occasional updates on what we're shipping, what we're learning, and where we'll be in the field. No spam.</p>
      </div>
      <div class="footer-newsletter-form-wrap">
        <form class="newsletter-form" action="https://docs.google.com/forms/d/e/1FAIpQLSdT98RF4UgkrU8RsYQ9yk9aVOO_F7xNktjant5XbnB6q_x0lQ/formResponse" method="POST" target="hidden_iframe_newsletter" data-success-title="You're on the list." data-success-body="Watch your inbox for occasional updates from PollenPal.">
          <input type="text" name="company" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px;" aria-hidden="true">
          <label class="visually-hidden" for="nl-name">Name</label>
          <input type="text" id="nl-name" name="entry.1325735936" placeholder="Name" required>
          <label class="visually-hidden" for="nl-email">Email</label>
          <input type="email" id="nl-email" name="entry.205724635" placeholder="you@example.com" required>
          <div class="cf-turnstile" data-sitekey="0x4AAAAAADc8h3Y34Jgk0u2e"></div>
          <button type="submit">Subscribe →</button>
        </form>
        <iframe name="hidden_iframe_newsletter" style="display:none"></iframe>
      </div>
    </div>

    <div class="footer-grid">
      <div class="footer-brand">
        <div class="footer-wordmark"><img src="/images/logo-icon.png" alt="">PollenPal</div>
        <p>Physical AI for commercial apiaries and farms.</p>
      </div>
      <div>
        <h4>Product</h4>
        <ul>
          <li><a href="/hobbyist">The app</a></li>
          <li><a href="/#how">How it works</a></li>
          <li><a href="/#advantage">Why PollenPal</a></li>
          <li><a href="/#pilot">Request a pilot</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="/#founders">Founders</a></li>
          <li><a href="/investors">Investors</a></li>
          <li><a href="https://app.pollenpal.com">Log in</a></li>
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
      © 2026 PollenPal Inc.
    </div>
  </div>
</footer>

<script src="/scripts.js" defer></script>
</body>
</html>
```

Note: the waitlist form is intentionally removed (no waitlist on this page). The Cloudflare Turnstile `<script>` and the newsletter form's Turnstile widget are KEPT so the newsletter retains the spam protection added in PR #3. The newsletter still posts to the Google Form via the hidden iframe and the `scripts.js` swap.

- [ ] **Step 2: Start the local server (background) if not already running**

```bash
cd /c/projects/Pollenpal-website && python -m http.server 8099
```

- [ ] **Step 3: Load the page and check for console errors**

Use `mcp__chrome-devtools__navigate_page` → `http://localhost:8099/hobbyist.html`, then `mcp__chrome-devtools__list_console_messages`.
Expected: no JS errors (a favicon 404 is fine).

- [ ] **Step 4: Visually verify desktop layout**

Use `mcp__chrome-devtools__resize_page` to 1280×900, then `mcp__chrome-devtools__take_screenshot`.
Expected: hero with copy left + phone mockup right; four feature rows alternating image side; cream testimonial; pricing card; FAQ; dark final CTA; footer. All placeholder images render.

- [ ] **Step 5: Visually verify mobile layout**

Use `mcp__chrome-devtools__resize_page` to 390×844, then `mcp__chrome-devtools__take_screenshot`.
Expected: single column; in each feature row the image sits ABOVE the copy; hamburger nav visible and not floating mid-header; no horizontal scroll.

- [ ] **Step 6: Commit**

```bash
git add hobbyist.html
git commit -m "feat: rebuild /hobbyist as deviceless app landing page (placeholder shots)"
```

---

## Task 4: Capture deviceless app screenshots

Capture five real screenshots from the live app, logged in as `robert@pollenpal.com`, showing ONLY Bill's (B005 / OCBS) hives that have NO device attached. Optimize and save to `images/`.

**Hard constraint:** no PollenPal-device data in any shot. No camera/entrance feeds, no activity charts, no mite counts, no colony-strength tiles, no "Calibrating" state. If a hive screen shows device chrome, pick a different (deviceless) hive.

**Prerequisite:** the `robert@pollenpal.com` password. If not available, pause and ask Robert before proceeding.

**Files:**
- Create: `images/app-hero.jpg`, `images/app-inspection.jpg`, `images/app-reminder.jpg`, `images/app-apiary.jpg`, `images/app-history.jpg`

- [ ] **Step 1: Open the app at phone size and log in**

Use `mcp__chrome-devtools__new_page` → `https://app.pollenpal.com`, `mcp__chrome-devtools__resize_page` to 390×844, then `mcp__chrome-devtools__fill_form` / `mcp__chrome-devtools__click` to log in as `robert@pollenpal.com`.
Expected: authenticated app view at phone width.

- [ ] **Step 2: Navigate to one of Bill's deviceless hives and confirm it is device-free**

Navigate to Bill's apiary, open a hive with no device. Use `mcp__chrome-devtools__take_snapshot` and confirm the screen shows inspection/record UI and NO camera feed, activity chart, mite count, or calibration tile.
Expected: a clean deviceless hive screen.

- [ ] **Step 3: Capture the five shots**

For each target screen, frame it and call `mcp__chrome-devtools__take_screenshot` (PNG), saving to a temp path, then move/rename:
- `app-hero.jpg` — the most attractive single hive/overview screen
- `app-inspection.jpg` — the inspection form (frames, brood, queen, etc.)
- `app-reminder.jpg` — the next-inspection / schedule UI
- `app-apiary.jpg` — Bill's yard with multiple deviceless hives listed
- `app-history.jpg` — a hive's inspection history timeline with photos

Expected: five PNG screenshots captured, each verified device-free.

- [ ] **Step 4: Optimize screenshots into images/**

Convert/resize to web-friendly JPGs (max ~900px wide, quality ~82) using the project's Pillow install. Run:

```bash
cd /c/projects/Pollenpal-website
py -3.13 -c "
from PIL import Image; import os
m={'app-hero':'app-hero','app-inspection':'app-inspection','app-reminder':'app-reminder','app-apiary':'app-apiary','app-history':'app-history'}
for src in ['app-hero','app-inspection','app-reminder','app-apiary','app-history']:
    p=f'.superpowers/deck_media/{src}.png'
    if not os.path.exists(p): print('MISSING',p); continue
    im=Image.open(p).convert('RGB'); w,h=im.size
    if w>900: im=im.resize((900,int(h*900/w)))
    im.save(f'images/{src}.jpg','JPEG',quality=82,optimize=True); print('wrote images/'+src+'.jpg')
"
```

Expected: prints `wrote images/<name>.jpg` for all five. (Place the raw PNGs in `.superpowers/deck_media/` first; that dir is gitignored.)

- [ ] **Step 5: Commit the optimized images**

```bash
git add images/app-hero.jpg images/app-inspection.jpg images/app-reminder.jpg images/app-apiary.jpg images/app-history.jpg
git commit -m "assets: deviceless app screenshots (Bill's no-device hives) for app page"
```

---

## Task 5: Wire real screenshots into the page

Swap the placeholder `dashboard-phone.jpg` references for the real captured screenshots.

**Files:**
- Modify: `hobbyist.html`

- [ ] **Step 1: Replace the hero image src**

In `hobbyist.html`, change the hero `.phone-frame` img from `/images/dashboard-phone.jpg` to `/images/app-hero.jpg` (keep the alt text).

- [ ] **Step 2: Replace each feature-row image src in order**

Map the four `.feature-shot` images top-to-bottom:
- Digital inspections row → `/images/app-inspection.jpg`
- Reminders row → `/images/app-reminder.jpg`
- Apiary row → `/images/app-apiary.jpg`
- History and photos row → `/images/app-history.jpg`

- [ ] **Step 3: Confirm no placeholder refs remain on the app page**

```bash
cd /c/projects/Pollenpal-website
grep -n 'dashboard-phone' hobbyist.html && echo "STILL HAS PLACEHOLDER — fix" || echo "no placeholders — OK"
```

Expected: prints "no placeholders — OK".

- [ ] **Step 4: Reload and verify real shots render device-free**

`mcp__chrome-devtools__navigate_page` → `http://localhost:8099/hobbyist.html`; `take_screenshot` at 390×844 and 1280×900.
Expected: all five real app screenshots render; visually re-confirm none show device telemetry.

- [ ] **Step 5: Commit**

```bash
git add hobbyist.html
git commit -m "feat: use real deviceless app screenshots on /hobbyist"
```

---

## Task 6: Cross-page footer link cleanup

`/hobbyist` is no longer a waitlist, so fix stale "Hobbyist waitlist" footer links on the other pages.

**Files:**
- Modify: `index.html`
- Modify: `investors.html`

- [ ] **Step 1: Find the stale links**

```bash
cd /c/projects/Pollenpal-website
grep -nE 'Hobbyist waitlist|hobbyist' index.html investors.html
```

Expected: shows footer `<li><a href="/hobbyist">Hobbyist waitlist</a></li>` entries (and possibly other hobbyist refs).

- [ ] **Step 2: Update the link text in index.html**

Change `>Hobbyist waitlist<` to `>The app<` in `index.html` (keep `href="/hobbyist"`).

- [ ] **Step 3: Update the link text in investors.html (if present)**

If the grep showed a "Hobbyist waitlist" link in `investors.html`, change its text to `The app` the same way. If none exists, skip.

- [ ] **Step 4: Verify no "waitlist" label points at /hobbyist anymore**

```bash
cd /c/projects/Pollenpal-website
grep -nE 'Hobbyist waitlist' index.html investors.html && echo "STILL THERE — fix" || echo "clean — OK"
```

Expected: prints "clean — OK".

- [ ] **Step 5: Commit**

```bash
git add index.html investors.html
git commit -m "copy: relabel /hobbyist footer links from waitlist to The app"
```

---

## Task 7: Full responsive + regression verification

Confirm the page holds up across breakpoints and that the homepage and investors pages still render after the footer edits.

**Files:** none (verification only)

- [ ] **Step 1: Check the app page at three widths**

For each of 1280×900, 768×1024, 390×844: `mcp__chrome-devtools__resize_page` then `mcp__chrome-devtools__take_screenshot` of `http://localhost:8099/hobbyist.html`.
Expected at each: no horizontal overflow; eyebrows centered where `.center` is used; nav-toggle pinned right on mobile; feature rows alternate on desktop and stack image-over-copy on mobile; pricing card and FAQ readable.

- [ ] **Step 2: Console check the app page**

`mcp__chrome-devtools__list_console_messages` on the app page.
Expected: no JS errors.

- [ ] **Step 3: Regression-check homepage and investors**

`navigate_page` to `http://localhost:8099/` and `http://localhost:8099/investors.html`; `take_screenshot` of each footer area.
Expected: footers render; "The app" link present; no layout breakage from the text change.

- [ ] **Step 4: Stop the local server**

Stop the background `python -m http.server 8099` process.

- [ ] **Step 5: Final review commit (if any tweaks were made)**

If Step 1-3 surfaced fixes, apply them and commit:

```bash
git add -A
git commit -m "fix: responsive tweaks on app landing page"
```

If no tweaks were needed, skip.

---

## Done criteria

- `/hobbyist` is the deviceless app landing page; old camera version preserved at `archive/hobbyist-hardware/`.
- All five screenshots are real app captures of Bill's deviceless hives, none showing device telemetry.
- Every CTA links to `https://app.pollenpal.com`; pricing reads free 30 days then $6.99/mo, up to 10 hives.
- Page renders cleanly at desktop/tablet/mobile with no console errors; homepage + investors footers updated and unbroken.
- All work committed on `hobbyist-app-page`.

## After implementation

Use `superpowers:finishing-a-development-branch` to decide how to integrate (PR vs merge). Note the Pi can also push to this repo, so check `feedback_pi_collision_check` before merging. Deploy is GitHub Pages on `main` → live at `pollenpal.com/hobbyist`.
