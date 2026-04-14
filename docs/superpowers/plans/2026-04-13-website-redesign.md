# PollenPal Website Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild pollenpal.com as a startup-grade marketing site (`/` commercial homepage, `/investors`, `/hobbyist`) using the v4 deck narrative and a tight editorial visual system.

**Architecture:** Three static HTML pages sharing a single external stylesheet and a small JS file. No build step, no framework. Static deployment to GitHub Pages via existing CNAME. Hero video re-encoded from a deck GIF. Forms reuse existing Google Form endpoints.

**Tech Stack:** Hand-written HTML5 + CSS3 (Inter + Instrument Serif via Google Fonts) + minimal vanilla JS. ffmpeg for hero video encoding, Pillow for image optimization. GitHub Pages for hosting.

**Source spec:** `docs/superpowers/specs/2026-04-13-website-redesign-design.md`

**Validated hero mock:** `.superpowers/brainstorm/4048-1776106868/content/hero-mock.html` (visual reference for Task 4)

---

## Critical context for the implementing engineer

1. **Nothing is committed to git until the user reviews the live site.** The current `index.html` and `images/` are the production site at pollenpal.com. Do not overwrite them in-place. Build the new site under a `new/` subdirectory or in a separate working tree, get visual approval, then do one final swap commit at the end (Task 15).
2. **The current `index.html` uses inline styles and a tabs-based dual-audience layout.** That entire file is being replaced. Reference it for existing copy and form action URLs only.
3. **Form action URLs** are Google Forms — same endpoint for both the beekeeper and investor forms in the current site. Read them out of `index.html` and reuse verbatim. Do not generate new endpoints.
4. **Image filenames in the spec are aspirational.** Source files live in `.superpowers/deck_media/` (extracted from the pptx already). Task 2 renames and copies them into `images/`.
5. **Visual system tokens are locked.** Don't invent new colors, radii, or font sizes. Everything you need is in the spec's "Visual system" section.
6. **No JS framework.** No npm, no bundler, no React. Plain `.html` + `.css` + `.js`.

---

## File structure

**New / rewritten files:**
```
index.html            Commercial homepage (full rewrite)
investors.html        New: condensed deck flow for investors
hobbyist.html         New: backyard waitlist one-pager
styles.css            New: shared stylesheet for all three pages
scripts.js            New: mobile nav toggle + form submit handler
images/               Add new deck-extracted assets, prune unused
```

**Unchanged:**
```
CNAME                 Already pollenpal.com
.gitignore            (add .superpowers/ if not already)
```

**Each HTML page:**
- Inlines critical hero CSS in `<style>` for first paint
- Links `styles.css` for everything else
- Defers `scripts.js`
- Shares the same `<header>` and `<footer>` markup (manually duplicated; no templating engine)

---

## Task 1: Scaffold the new file structure and prep tooling

**Files:**
- Create: `styles.css` (empty stub for now)
- Create: `scripts.js` (empty stub for now)
- Create: `investors.html` (empty stub)
- Create: `hobbyist.html` (empty stub)
- Modify: `.gitignore` (add `.superpowers/`)

- [ ] **Step 1: Verify project working directory and current state**

Run: `ls C:/projects/Pollenpal-website/`
Expected: `CNAME`, `index.html`, `images/`, `PollenPal v4_Pitch.pptx`, `.superpowers/`, `docs/`

- [ ] **Step 2: Confirm `.gitignore` excludes the brainstorm scratch dir**

Read `.gitignore`. If `.superpowers/` is not listed, add it:

```
.superpowers/
```

- [ ] **Step 3: Create empty stub files**

Create four empty files: `styles.css`, `scripts.js`, `investors.html`, `hobbyist.html`. They will be filled in in subsequent tasks. This step prevents broken `<link>` and `<script>` references when you wire up the homepage.

- [ ] **Step 4: Verify ffmpeg and Python+Pillow are available**

Run: `ffmpeg -version`
Expected: ffmpeg version output (any 4.x or later).
If missing: `winget install ffmpeg` or download from gyan.dev.

Run: `py -3.13 -c "import PIL; print(PIL.__version__)"`
Expected: a Pillow version (already installed per project memory).

- [ ] **Step 5: Do not commit yet** — file scaffolding is a precursor only.

---

## Task 2: Extract, rename, and optimize all deck assets

**Files:**
- Create: `images/hero.mp4`
- Create: `images/hero-poster.jpg`
- Create: `images/device-grass.jpg`
- Create: `images/ml-detection.jpg`
- Create: `images/dashboard-phone.jpg`
- Create: `images/wendy-ventura.jpg`
- Create: `images/device-field.jpg` (investor page only)
- Create: `images/device-cad.jpg` (investor page only)
- Create: `images/ml-detection-simple.jpg` (investor page only)
- Create: `images/nyc-rooftop.jpg` (investor page only)
- Create: `scripts/prep_assets.py` (one-shot asset prep script, kept in repo for reproducibility)

- [ ] **Step 1: Write the asset prep script**

Create `scripts/prep_assets.py`:

```python
"""One-shot script: extract deck media + optimize for web."""
import shutil
import subprocess
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / ".superpowers" / "deck_media"
DEST = ROOT / "images"

# (source filename, dest filename, max width)
IMAGE_MAP = [
    ("image5.png",   "device-grass.jpg",        1400),
    ("image32.png",  "ml-detection.jpg",        1400),
    ("image6.png",   "dashboard-phone.jpg",     1200),
    ("image24.jpeg", "wendy-ventura.jpg",       1800),
    ("image35.png",  "device-field.jpg",        1600),
    ("image34.png",  "device-cad.jpg",          1200),
    ("image7.png",   "ml-detection-simple.jpg", 1400),
    ("image25.jpeg", "nyc-rooftop.jpg",         1600),
]

def optimize_image(src: Path, dest: Path, max_width: int):
    im = Image.open(src).convert("RGB")
    if im.width > max_width:
        ratio = max_width / im.width
        im = im.resize((max_width, int(im.height * ratio)), Image.LANCZOS)
    im.save(dest, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"  {dest.name:30s} {dest.stat().st_size // 1024} KB")

def encode_hero_video(src_gif: Path, dest_mp4: Path, dest_poster: Path):
    # Re-encode GIF to H.264 MP4, scale up to 800w, target ~1MB
    subprocess.run([
        "ffmpeg", "-y", "-i", str(src_gif),
        "-movflags", "+faststart",
        "-pix_fmt", "yuv420p",
        "-vf", "scale=800:-2:flags=lanczos",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "26",
        "-an",
        str(dest_mp4),
    ], check=True)
    # Extract first frame as poster
    subprocess.run([
        "ffmpeg", "-y", "-i", str(src_gif),
        "-vframes", "1",
        "-vf", "scale=800:-2:flags=lanczos",
        "-q:v", "3",
        str(dest_poster),
    ], check=True)
    print(f"  hero.mp4         {dest_mp4.stat().st_size // 1024} KB")
    print(f"  hero-poster.jpg  {dest_poster.stat().st_size // 1024} KB")

def main():
    DEST.mkdir(exist_ok=True)
    print("Optimizing images...")
    for src_name, dest_name, max_w in IMAGE_MAP:
        optimize_image(SRC / src_name, DEST / dest_name, max_w)
    print("Encoding hero video...")
    encode_hero_video(SRC / "image17.gif", DEST / "hero.mp4", DEST / "hero-poster.jpg")
    print("Done.")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the asset prep script**

Run: `py -3.13 C:/projects/Pollenpal-website/scripts/prep_assets.py`

Expected output: each filename with a KB size. `hero.mp4` should be roughly 800–1500 KB. If it lands above 2.5 MB, increase `-crf` to 28 or 30 and rerun. If it lands below 500 KB, drop `-crf` to 24 for better visual fidelity.

- [ ] **Step 3: Verify all expected files exist**

Run: `ls C:/projects/Pollenpal-website/images/ | grep -E "(hero|device|ml-|dashboard-phone|wendy|nyc)"`
Expected: 10 new files (`hero.mp4`, `hero-poster.jpg`, plus the 8 jpegs).

- [ ] **Step 4: Confirm the hero video plays**

Open `images/hero.mp4` in a media player. Confirm it loops a 360° apiary shot, no audio, plays smoothly.

- [ ] **Step 5: Do not commit yet.**

---

## Task 3: Build the shared stylesheet (`styles.css`)

**Files:**
- Modify: `styles.css`

This is the visual system. Tokens, type, layout primitives, header/footer styles, button styles, and section utilities. Section-specific CSS comes in later tasks but lives in this same file.

- [ ] **Step 1: Write the full base stylesheet**

Open `styles.css` and write:

```css
/* ============================================================
   PollenPal — shared stylesheet
   Tokens defined once here; reused across every page.
============================================================ */

:root {
  --gold: #E8A43A;
  --gold-dark: #C2851A;
  --cream: #FFECB7;
  --cream-soft: #FFF8E7;
  --ink: #0A0A0A;
  --ink-soft: #3A3A3A;
  --muted: #6B6B6B;
  --line: #EAEAEA;
  --bg: #FFFFFF;
  --success: #1F8A3B;
  --alert: #E04A3A;
  --radius: 8px;
  --radius-lg: 14px;
  --wrap: 1240px;
  --gutter: 32px;
}

*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

html { scroll-behavior: smooth; -webkit-text-size-adjust: 100%; }

body {
  background: var(--bg);
  color: var(--ink);
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  font-size: 17px;
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

img, video, svg { max-width: 100%; display: block; }
a { color: inherit; text-decoration: none; }
button { font: inherit; cursor: pointer; }

.wrap { max-width: var(--wrap); margin: 0 auto; padding: 0 var(--gutter); }
.wrap-narrow { max-width: 880px; margin: 0 auto; padding: 0 var(--gutter); }

.section { padding: 120px 0; }
.section-tight { padding: 96px 0; }
.bg-cream { background: var(--cream-soft); }
.bg-ink { background: var(--ink); color: #fff; }

/* ===== TYPOGRAPHY ===== */
h1, h2, h3, h4 {
  font-family: inherit;
  font-weight: 700;
  letter-spacing: -0.025em;
  line-height: 1.05;
  color: var(--ink);
}
.bg-ink h1, .bg-ink h2, .bg-ink h3, .bg-ink h4 { color: #fff; }

h1 { font-size: clamp(46px, 6.2vw, 88px); line-height: 0.98; letter-spacing: -0.035em; }
h2 { font-size: clamp(32px, 4vw, 56px); }
h3 { font-size: clamp(22px, 2.4vw, 30px); }

.eyebrow {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 1.8px;
  text-transform: uppercase;
  color: var(--gold-dark);
  margin-bottom: 24px;
}
.eyebrow::before {
  content: "";
  width: 28px;
  height: 1px;
  background: var(--gold);
}
.eyebrow.center { justify-content: center; }
.eyebrow.center::before { display: none; }

.serif-italic {
  font-family: 'Instrument Serif', 'Times New Roman', serif;
  font-style: italic;
  font-weight: 400;
  color: var(--gold-dark);
  letter-spacing: -0.01em;
}

.lede {
  font-size: 19px;
  line-height: 1.55;
  color: var(--ink-soft);
  max-width: 640px;
}
.lede.center { margin-left: auto; margin-right: auto; text-align: center; }

.muted { color: var(--muted); }
.label-sm {
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1.4px;
  text-transform: uppercase;
  color: var(--muted);
}

/* ===== BUTTONS ===== */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 15px 28px;
  font-size: 15px;
  font-weight: 600;
  border-radius: var(--radius);
  border: 1px solid transparent;
  transition: all 0.2s ease;
  white-space: nowrap;
}
.btn-primary { background: var(--ink); color: #fff; border-color: var(--ink); }
.btn-primary:hover { background: var(--gold-dark); border-color: var(--gold-dark); transform: translateY(-1px); }
.btn-secondary { background: transparent; color: var(--ink); border-color: var(--line); }
.btn-secondary:hover { border-color: var(--ink); }
.btn-gold { background: var(--gold-dark); color: #fff; border-color: var(--gold-dark); }
.btn-gold:hover { background: var(--ink); border-color: var(--ink); }

/* ===== HEADER ===== */
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255,255,255,0.92);
  backdrop-filter: saturate(150%) blur(10px);
  border-bottom: 1px solid var(--line);
}
.site-header .nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 0;
}
.nav-logo img { height: 32px; }
.nav-links {
  display: flex;
  gap: 36px;
  font-size: 14px;
  font-weight: 500;
  color: var(--ink-soft);
}
.nav-links a:hover { color: var(--ink); }
.nav-links a.current { color: var(--ink); font-weight: 600; }
.nav-cta {
  font-size: 13px;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: var(--radius);
  background: var(--ink);
  color: #fff;
  border: 1px solid var(--ink);
  transition: background 0.2s;
}
.nav-cta:hover { background: var(--gold-dark); border-color: var(--gold-dark); }
.nav-toggle {
  display: none;
  background: none;
  border: none;
  font-size: 22px;
  color: var(--ink);
}

/* ===== FOOTER ===== */
.site-footer {
  background: var(--ink);
  color: #fff;
  padding: 72px 0 32px;
}
.site-footer .footer-grid {
  display: grid;
  grid-template-columns: 1.5fr repeat(3, 1fr);
  gap: 48px;
  align-items: start;
  margin-bottom: 56px;
}
.site-footer .footer-brand img { height: 28px; filter: brightness(0) invert(1); margin-bottom: 16px; }
.site-footer .footer-brand p { color: rgba(255,255,255,0.65); font-size: 14px; max-width: 280px; }
.site-footer h4 {
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.4px;
  margin-bottom: 18px;
}
.site-footer ul { list-style: none; }
.site-footer ul li { margin-bottom: 10px; }
.site-footer ul a { font-size: 14px; color: rgba(255,255,255,0.7); transition: color 0.2s; }
.site-footer ul a:hover { color: var(--gold); }
.site-footer .footer-bottom {
  border-top: 1px solid rgba(255,255,255,0.1);
  padding-top: 24px;
  font-size: 13px;
  color: rgba(255,255,255,0.5);
}

/* ===== STAT/METRIC PRIMITIVES ===== */
.proof-row {
  display: flex;
  gap: 36px;
  padding-top: 32px;
  border-top: 1px solid var(--line);
}
.proof-item { display: flex; flex-direction: column; }
.proof-num { font-size: 26px; font-weight: 700; color: var(--ink); letter-spacing: -0.02em; }
.proof-label { font-size: 12px; color: var(--muted); margin-top: 2px; }

.stat-strip {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 16px;
}
.stat-strip .stat {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 24px 18px;
  text-align: center;
}
.stat-strip .stat-num { font-size: 28px; font-weight: 700; color: var(--gold-dark); letter-spacing: -0.02em; }
.stat-strip .stat-label { font-size: 12px; color: var(--muted); margin-top: 6px; line-height: 1.4; }

/* ===== SKIP LINK + A11Y ===== */
.skip-link {
  position: absolute;
  left: -9999px;
  top: 0;
  background: var(--ink);
  color: #fff;
  padding: 12px 18px;
  z-index: 200;
}
.skip-link:focus { left: 8px; top: 8px; }

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; }
  html { scroll-behavior: auto; }
}

/* ===== RESPONSIVE BASE ===== */
@media (max-width: 960px) {
  .section { padding: 72px 0; }
  .section-tight { padding: 56px 0; }
  .nav-links { display: none; }
  .nav-toggle { display: block; }
  .nav-toggle.open + .nav-links {
    display: flex;
    flex-direction: column;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: #fff;
    border-bottom: 1px solid var(--line);
    padding: 24px var(--gutter);
    gap: 16px;
  }
  .stat-strip { grid-template-columns: repeat(2, 1fr); }
  .site-footer .footer-grid { grid-template-columns: 1fr 1fr; gap: 32px; }
}
@media (max-width: 600px) {
  :root { --gutter: 20px; }
  .stat-strip { grid-template-columns: 1fr; }
  .site-footer .footer-grid { grid-template-columns: 1fr; }
  .proof-row { gap: 24px; flex-wrap: wrap; }
}
```

- [ ] **Step 2: Verify the file is syntactically valid CSS**

Open `styles.css` in any editor or run a CSS linter. Look for unmatched braces, typos. Save.

- [ ] **Step 3: Do not commit yet.**

---

## Task 4: Build the homepage shell + hero (`index.html`)

**Files:**
- Modify: `index.html` (full rewrite — back up the existing file first as `index.html.old` for reference)

This task ports the validated mock from `.superpowers/brainstorm/4048-1776106868/content/hero-mock.html` into the production page, references the new external stylesheet for non-critical CSS, and inlines critical hero CSS.

- [ ] **Step 1: Back up the current homepage**

Run: `cp C:/projects/Pollenpal-website/index.html C:/projects/Pollenpal-website/index.html.old`

- [ ] **Step 2: Read the existing form action URL**

Open `index.html.old` and find the `<form action="...">` for the beekeeper signup. Copy the URL and the `entry.*` field names — you will reuse them in the pilot CTA later (Task 11).

Note them here in your scratch file:
- `FORM_ACTION = https://docs.google.com/forms/d/e/<id>/formResponse`
- Field names: `entry.455027715` (name), `entry.414264367` (email), `entry.119689931` (type), `entry.355024465` (hives), `entry.1292345725` (message)

- [ ] **Step 3: Write the new `index.html` shell with hero**

Replace `index.html` content with:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PollenPal — Physical AI for commercial apiaries and farms</title>
  <meta name="description" content="PollenPal watches every bee in and out of your hive and flags varroa, africanization, and queen issues before they spread. Pilot-ready in 2026.">
  <meta property="og:title" content="PollenPal — Physical AI for commercial apiaries">
  <meta property="og:description" content="Inspect every hive. Every day. Continuous monitoring for commercial beekeeping operations.">
  <meta property="og:image" content="/images/hero-poster.jpg">
  <link rel="icon" href="/images/logo-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
  <style>
    /* Critical hero CSS — inlined for first paint */
    .hero { position: relative; padding: 96px 0 120px; overflow: hidden; }
    .hero::before {
      content: ""; position: absolute; top: 0; right: -15%;
      width: 60%; height: 100%;
      background: radial-gradient(ellipse at center, var(--cream-soft) 0%, transparent 70%);
      pointer-events: none;
    }
    .hero-grid {
      position: relative; display: grid;
      grid-template-columns: 1.15fr 1fr;
      gap: 72px; align-items: center;
    }
    .hero h1 { margin-bottom: 28px; }
    .hero .lede { margin-bottom: 40px; }
    .hero-ctas { display: flex; gap: 14px; align-items: center; margin-bottom: 44px; flex-wrap: wrap; }
    .hero-visual { position: relative; display: flex; justify-content: center; align-items: center; }
    .visual-frame {
      position: relative; width: 100%; max-width: 440px; aspect-ratio: 4/5;
      border-radius: var(--radius-lg); overflow: hidden; background: var(--ink);
      box-shadow: 0 30px 80px -20px rgba(10,10,10,0.25), 0 8px 20px -6px rgba(10,10,10,0.12);
    }
    .visual-frame video, .visual-frame img.poster { width: 100%; height: 100%; object-fit: cover; }
    .visual-overlay { position: absolute; inset: 0; background: linear-gradient(180deg, transparent 45%, rgba(0,0,0,0.55) 100%); pointer-events: none; }
    .visual-tag {
      position: absolute; top: 18px; left: 18px;
      background: rgba(255,255,255,0.95); backdrop-filter: blur(8px);
      padding: 6px 12px; border-radius: 20px;
      font-size: 11px; font-weight: 600; color: var(--ink); letter-spacing: 0.4px;
    }
    .visual-caption {
      position: absolute; left: 20px; bottom: 18px; right: 20px;
      color: #fff; font-size: 12px; font-weight: 500;
      display: flex; align-items: center; gap: 10px; letter-spacing: 0.3px;
    }
    .live-dot {
      width: 7px; height: 7px; border-radius: 50%;
      background: var(--gold);
      box-shadow: 0 0 0 4px rgba(232,164,58,0.25);
      animation: pulse 1.8s ease-in-out infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.6; transform: scale(0.85); }
    }
    .stat-card {
      position: absolute; background: #fff;
      border: 1px solid var(--line); border-radius: 10px;
      padding: 14px 18px; box-shadow: 0 16px 40px -12px rgba(10,10,10,0.18);
    }
    .stat-card-1 { top: 8%; left: -14%; display: flex; align-items: center; gap: 12px; }
    .stat-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--alert); }
    .stat-card-1 .stat-title { font-size: 12px; font-weight: 600; color: var(--ink); }
    .stat-card-1 .stat-sub { font-size: 11px; color: var(--muted); margin-top: 1px; }
    .stat-card-2 { bottom: 12%; right: -12%; min-width: 150px; }
    .stat-card-2 .sc2-label { font-size: 10px; letter-spacing: 1.2px; color: var(--muted); text-transform: uppercase; font-weight: 600; }
    .stat-card-2 .sc2-num { font-size: 24px; font-weight: 700; color: var(--ink); margin-top: 4px; letter-spacing: -0.02em; }
    .stat-card-2 .sc2-delta { font-size: 11px; color: var(--success); font-weight: 600; margin-top: 2px; }
    @media (max-width: 960px) {
      .hero { padding: 56px 0 80px; }
      .hero-grid { grid-template-columns: 1fr; gap: 48px; }
      .hero-visual { order: -1; }
      .visual-frame { max-width: 320px; }
      .stat-card { display: none; }
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
      <a href="#how">How it works</a>
      <a href="#advantage">Why PollenPal</a>
      <a href="#roadmap">Roadmap</a>
      <a href="#founders">Company</a>
    </nav>
    <a href="#pilot" class="nav-cta">Request a pilot →</a>
  </div>
</header>

<main id="main">

  <!-- ===== HERO ===== -->
  <section class="hero">
    <div class="wrap hero-grid">

      <div class="hero-copy">
        <div class="eyebrow">Physical AI for commercial apiaries &amp; farms</div>
        <h1>Inspect every hive.<br><span class="serif-italic">Every</span> day.</h1>
        <p class="lede">PollenPal watches every bee in and out of your hive and flags varroa, africanization, and queen issues before they spread. Your crews treat the problem. They don't hunt for it.</p>
        <div class="hero-ctas">
          <a href="#pilot" class="btn btn-primary">Request a pilot →</a>
          <a href="#how" class="btn btn-secondary">See how it works</a>
        </div>
        <div class="proof-row">
          <div class="proof-item"><div class="proof-num">20k+</div><div class="proof-label">Field images trained</div></div>
          <div class="proof-item"><div class="proof-num">~80%</div><div class="proof-label">Varroa detection</div></div>
          <div class="proof-item"><div class="proof-num">3</div><div class="proof-label">Commercial pilots</div></div>
        </div>
      </div>

      <div class="hero-visual">
        <div class="visual-frame">
          <div class="visual-tag">● Live apiary feed</div>
          <video autoplay muted loop playsinline poster="/images/hero-poster.jpg" preload="metadata">
            <source src="/images/hero.mp4" type="video/mp4">
            <img class="poster" src="/images/hero-poster.jpg" alt="Live PollenPal apiary feed">
          </video>
          <div class="visual-overlay"></div>
          <div class="visual-caption">
            <span class="live-dot"></span>
            <span>Ventura yard · 48 hives monitored · updating in real time</span>
          </div>
        </div>
        <div class="stat-card stat-card-1" aria-hidden="true">
          <span class="stat-dot"></span>
          <div>
            <div class="stat-title">Varroa alert · Hive 14</div>
            <div class="stat-sub">Detected 6 min ago</div>
          </div>
        </div>
        <div class="stat-card stat-card-2" aria-hidden="true">
          <div class="sc2-label">Colonies monitored</div>
          <div class="sc2-num">4,712</div>
          <div class="sc2-delta">+284 this week</div>
        </div>
      </div>

    </div>
  </section>

  <!-- Sections 3–11 added in subsequent tasks -->

</main>

<!-- Footer added in Task 12 -->

<script src="/scripts.js" defer></script>
</body>
</html>
```

- [ ] **Step 4: Open the page in a browser**

Run: `start C:/projects/Pollenpal-website/index.html` (Windows) — opens in default browser via `file://`.

Expected: header with PollenPal logo and "Request a pilot →" button, hero section with the headline, sub-copy, two CTAs, proof row of three metrics, and the 4:5 dark frame with the looping apiary video. Cream radial glow on the right. Two floating stat cards overlap the frame.

If the video doesn't play under `file://`, open it via a local server: `py -3.13 -m http.server 8000` from the project root, then `http://localhost:8000`.

- [ ] **Step 5: Resize the browser to ~720px wide**

Confirm: hero collapses to single column, video frame appears above the copy, floating stat cards disappear, nav links collapse to hamburger button.

- [ ] **Step 6: Do not commit yet.**

---

## Task 5: Backed-by strip + Problem section

**Files:**
- Modify: `index.html` (insert sections after the hero `</section>`)
- Modify: `styles.css` (add section-specific styles at the end)

- [ ] **Step 1: Append CSS for backed-by strip + problem section**

Append to `styles.css`:

```css
/* ===== BACKED BY STRIP ===== */
.backed-strip {
  background: var(--cream-soft);
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  padding: 24px 0;
}
.backed-strip .wrap {
  display: flex;
  align-items: center;
  gap: 28px;
  flex-wrap: wrap;
}
.backed-strip .label-sm { color: var(--ink-soft); font-weight: 700; }
.backed-strip .brands {
  display: flex;
  gap: 28px;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink-soft);
  letter-spacing: 0.3px;
  flex-wrap: wrap;
}
.backed-strip .brands span.dot { color: var(--gold); }

/* ===== PROBLEM SECTION ===== */
.problem h2 { max-width: 900px; margin: 0 auto 28px; text-align: center; }
.problem .lede { margin: 0 auto 64px; text-align: center; }
.problem-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 48px;
}
.problem-card {
  background: var(--cream-soft);
  border-left: 3px solid var(--gold-dark);
  padding: 32px;
  border-radius: 0 var(--radius) var(--radius) 0;
}
.problem-card h3 { margin-bottom: 12px; }
.problem-card p { color: var(--ink-soft); font-size: 16px; }
.stat-bar {
  background: var(--ink);
  color: #fff;
  padding: 32px;
  border-radius: var(--radius);
  text-align: center;
  font-size: 19px;
  font-weight: 500;
}
.stat-bar .num { color: var(--gold); font-size: 28px; font-weight: 700; }
@media (max-width: 720px) {
  .problem-cards { grid-template-columns: 1fr; }
}
```

- [ ] **Step 2: Insert HTML after the hero section**

In `index.html`, after the closing `</section>` of the hero (and before `<!-- Sections 3–11 added in subsequent tasks -->`), insert:

```html
  <!-- ===== BACKED BY STRIP ===== -->
  <div class="backed-strip">
    <div class="wrap">
      <span class="label-sm">Backed by</span>
      <div class="brands">
        <span>Columbia Business School</span>
        <span class="dot">·</span>
        <span>Big Idea Pitch Winners 2025</span>
        <span class="dot">·</span>
        <span>4 Master Beekeepers</span>
      </div>
    </div>
  </div>

  <!-- ===== PROBLEM ===== -->
  <section id="problem" class="section problem">
    <div class="wrap">
      <div class="eyebrow center">The stakes</div>
      <h2>Bees feed the world. But bees are <span class="serif-italic">dying faster</span> than food demand is growing.</h2>
      <p class="lede center">Commercial beekeepers lose ~40% of colonies a year. Manual inspection doesn't scale, and the two biggest killers are nearly impossible to catch by eye.</p>

      <div class="problem-cards">
        <div class="problem-card">
          <h3>Varroa Mites</h3>
          <p>Parasites spread deadly viruses undetected until collapse. By the time you see the signs at inspection, the damage is already done — and one infected hive can take down a yard in weeks.</p>
        </div>
        <div class="problem-card">
          <h3>Africanization</h3>
          <p>Invasive bees outcompete European colonies and turn gentle yards aggressive in weeks. Entire operations become unworkable, and you can't catch it without watching the entrance.</p>
        </div>
      </div>

      <div class="stat-bar">
        <span class="num">40%+</span> annual colony losses · <span class="num">$635M+</span> in damages to US beekeepers annually
      </div>
    </div>
  </section>
```

- [ ] **Step 3: Reload the browser**

Confirm: the cream backed-by strip appears below the hero, then the centered problem section with the serif italic on "dying faster", two cream cards with gold-dark left borders, and a black stat bar with gold numbers.

- [ ] **Step 4: Verify mobile**

Resize to ~600px wide. Problem cards stack vertically. Backed-by strip wraps cleanly.

- [ ] **Step 5: Do not commit yet.**

---

## Task 6: How it works section

**Files:**
- Modify: `index.html` (insert section after the problem section)
- Modify: `styles.css`

- [ ] **Step 1: Append CSS**

Append to `styles.css`:

```css
/* ===== HOW IT WORKS ===== */
.how h2 { text-align: center; max-width: 800px; margin: 0 auto 24px; }
.how .lede { margin: 0 auto 64px; text-align: center; }
.how-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
}
.step {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.step-img {
  width: 100%;
  height: 240px;
  object-fit: cover;
  background: var(--cream-soft);
}
.step-body { padding: 28px; }
.step-num {
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: var(--gold-dark);
  letter-spacing: 1.5px;
  margin-bottom: 12px;
}
.step h3 { margin-bottom: 12px; font-size: 22px; }
.step p { color: var(--ink-soft); font-size: 15px; line-height: 1.6; }
@media (max-width: 900px) {
  .how-grid { grid-template-columns: 1fr; }
  .step-img { height: 200px; }
}
```

- [ ] **Step 2: Insert HTML after the problem section closing `</section>`**

```html
  <!-- ===== HOW IT WORKS ===== -->
  <section id="how" class="section bg-cream how">
    <div class="wrap">
      <div class="eyebrow center">How it works</div>
      <h2>From bee to alert in minutes.</h2>
      <p class="lede">No complicated setup. No new hive bodies. The PollenPal box drops into your existing operation and starts working on day one.</p>

      <div class="how-grid">
        <div class="step">
          <img class="step-img" src="/images/device-grass.jpg" alt="Solar-powered PollenPal device on a hive stack">
          <div class="step-body">
            <div class="step-num">01 · HARDWARE WATCHES</div>
            <h3>Sits as the base of your hive</h3>
            <p>A solar-powered PollenPal box becomes the bottom box of your hive stack. Its camera and sound sensors watch every bee in and out, 24/7. No WiFi needed — solar plus LTE works in remote yards.</p>
          </div>
        </div>
        <div class="step">
          <img class="step-img" src="/images/ml-detection.jpg" alt="Computer vision detecting bees and varroa mites">
          <div class="step-body">
            <div class="step-num">02 · ML CATCHES THREATS</div>
            <h3>Computer vision spots what you can't</h3>
            <p>YOLOv11 trained on 20,000+ field images detects varroa mites at 1–1.5mm scale, africanization markers, and missing-queen indicators. Things a beekeeper can't catch by eye, and certainly not in time.</p>
          </div>
        </div>
        <div class="step">
          <img class="step-img" src="/images/dashboard-phone.jpg" alt="Hive dashboard alert on a phone">
          <div class="step-body">
            <div class="step-num">03 · YOU GET AN ALERT</div>
            <h3>Treat the problem, don't hunt for it</h3>
            <p>When something looks wrong, your phone gets a notification with a clear explanation and a clear next step. No guessing. No waiting until the next inspection cycle.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
```

- [ ] **Step 3: Reload and verify**

Confirm: cream-soft band, three step cards in a row, each with image-on-top, gold-dark step number, title, description. Mobile collapses to single column.

- [ ] **Step 4: Do not commit yet.**

---

## Task 7: Why PollenPal section

**Files:**
- Modify: `index.html`
- Modify: `styles.css`

- [ ] **Step 1: Append CSS**

```css
/* ===== WHY POLLENPAL ===== */
.advantage h2 { text-align: center; max-width: 900px; margin: 0 auto 28px; }
.advantage .lede { margin: 0 auto 72px; text-align: center; }
.advantage-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}
.adv-card {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 36px 30px;
  background: #fff;
  display: flex;
  flex-direction: column;
}
.adv-num {
  display: inline-block;
  width: 36px;
  height: 36px;
  line-height: 36px;
  text-align: center;
  background: var(--cream);
  color: var(--gold-dark);
  border-radius: 50%;
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 20px;
}
.adv-card h3 { font-size: 22px; margin-bottom: 14px; line-height: 1.2; }
.adv-card p { color: var(--ink-soft); font-size: 15px; line-height: 1.65; }
.adv-card p .data-quote {
  display: block;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid var(--line);
  font-family: 'Instrument Serif', serif;
  font-style: italic;
  font-size: 16px;
  color: var(--gold-dark);
  line-height: 1.45;
}
@media (max-width: 960px) {
  .advantage-grid { grid-template-columns: 1fr; }
}
```

- [ ] **Step 2: Insert HTML after the how-it-works section**

```html
  <!-- ===== WHY POLLENPAL ===== -->
  <section id="advantage" class="section advantage">
    <div class="wrap">
      <div class="eyebrow center">Why PollenPal</div>
      <h2>Built for commercial scale, not science fairs.</h2>
      <p class="lede">Every other tool forces you to choose between cheap-but-blind (manual inspection) and accurate-but-impractical (heavy in-hive sensors, six-figure systems). PollenPal is the first that doesn't make you choose.</p>

      <div class="advantage-grid">
        <div class="adv-card">
          <div class="adv-num">01</div>
          <h3>Continuous, per-hive monitoring</h3>
          <p>Manual inspection happens every few weeks. Smart-hive systems average across the whole yard. PollenPal watches every bee, every day, in every hive — so threats get caught the day they appear, not the next visit.</p>
        </div>
        <div class="adv-card">
          <div class="adv-num">02</div>
          <h3>Sub-$100 hardware that drops in</h3>
          <p>Most smart-hive products cost thousands per colony and require a custom hive body. PollenPal's box uses off-the-shelf compute and sits under your standard 10-frame Langstroth — no adapters, no rewiring. Solar and LTE mean it works in remote yards.</p>
        </div>
        <div class="adv-card">
          <div class="adv-num">03</div>
          <h3>A data moat that compounds</h3>
          <p>Every PollenPal in the field improves the model for every other PollenPal. After one season we already had 20,000+ field-labeled images and ~80% varroa accuracy.<span class="data-quote">"By digitizing apiaries, we're collecting data unobtainable any other way. Our models compound in accuracy with every bee we see."</span></p>
        </div>
      </div>
    </div>
  </section>
```

- [ ] **Step 3: Reload and verify**

Three border-only cards, gold circle numerals, third card has the italic serif quote at the bottom separated by a thin line.

- [ ] **Step 4: Do not commit yet.**

---

## Task 8: Traction + Roadmap sections

**Files:**
- Modify: `index.html`
- Modify: `styles.css`

- [ ] **Step 1: Append CSS**

```css
/* ===== TRACTION ===== */
.traction h2 { text-align: center; margin-bottom: 24px; }
.traction .lede { margin: 0 auto 56px; text-align: center; }

/* ===== ROADMAP ===== */
.roadmap h2 { text-align: center; margin: 0 auto 24px; max-width: 900px; }
.roadmap .lede { margin: 0 auto 64px; text-align: center; }
.timeline {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  position: relative;
}
.timeline::before {
  content: "";
  position: absolute;
  top: 24px;
  left: 8%;
  right: 8%;
  height: 2px;
  background: var(--line);
  z-index: 0;
}
.timeline::after {
  content: "";
  position: absolute;
  top: 24px;
  left: 8%;
  width: calc(33% - 8%);
  height: 2px;
  background: var(--gold);
  z-index: 1;
}
.tl-stage { position: relative; z-index: 2; text-align: center; padding-top: 0; }
.tl-dot {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--gold);
  border: 4px solid var(--cream-soft);
  margin: 16px auto 24px;
  box-shadow: 0 0 0 2px var(--gold-dark);
}
.tl-stage:nth-child(2) .tl-dot { background: #fff; box-shadow: 0 0 0 2px var(--line); }
.tl-stage:nth-child(3) .tl-dot { background: #fff; box-shadow: 0 0 0 2px var(--line); }
.tl-pill {
  display: inline-block;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 100px;
  margin-bottom: 14px;
}
.tl-stage:nth-child(1) .tl-pill { background: var(--gold); color: var(--ink); }
.tl-stage:nth-child(2) .tl-pill { background: var(--cream); color: var(--gold-dark); }
.tl-stage:nth-child(3) .tl-pill { background: #f2f2f2; color: var(--muted); }
.tl-year { font-size: 13px; color: var(--muted); font-weight: 600; margin-bottom: 6px; letter-spacing: 0.5px; }
.tl-stage h3 { font-size: 20px; margin-bottom: 10px; }
.tl-stage p { color: var(--ink-soft); font-size: 14px; line-height: 1.55; max-width: 280px; margin: 0 auto; }
@media (max-width: 900px) {
  .timeline { grid-template-columns: 1fr; gap: 40px; }
  .timeline::before, .timeline::after { display: none; }
}
```

- [ ] **Step 2: Insert HTML after the why-pollenpal section**

```html
  <!-- ===== TRACTION ===== -->
  <section id="traction" class="section bg-cream traction">
    <div class="wrap">
      <div class="eyebrow center">Traction</div>
      <h2>Pilot-ready and proven in the field.</h2>
      <p class="lede">From cross-country interviews to working pilots — built on a year of field data and beekeeper feedback.</p>

      <div class="stat-strip">
        <div class="stat"><div class="stat-num">50+</div><div class="stat-label">Beekeeper interviews</div></div>
        <div class="stat"><div class="stat-num">20k+</div><div class="stat-label">Field images trained</div></div>
        <div class="stat"><div class="stat-num">~80%</div><div class="stat-label">Varroa accuracy</div></div>
        <div class="stat"><div class="stat-num">3</div><div class="stat-label">Pilots committed (CT, NY, CA)</div></div>
        <div class="stat"><div class="stat-num">12</div><div class="stat-label">Hardware iterations</div></div>
        <div class="stat"><div class="stat-num">4</div><div class="stat-label">Master Beekeeper advisors</div></div>
      </div>
    </div>
  </section>

  <!-- ===== ROADMAP ===== -->
  <section id="roadmap" class="section roadmap">
    <div class="wrap">
      <div class="eyebrow center">What's next</div>
      <h2>From threat detection to <span class="serif-italic">autonomous</span> response.</h2>
      <p class="lede">Today PollenPal catches problems. Next, it tells you exactly what to do about them. Then it does it for you.</p>

      <div class="timeline">
        <div class="tl-stage">
          <div class="tl-dot"></div>
          <div class="tl-pill">Shipping</div>
          <div class="tl-year">2026</div>
          <h3>Threat Detection</h3>
          <p>Shipping to commercial pilots now. Varroa, africanization, and queen issues caught the day they appear.</p>
        </div>
        <div class="tl-stage">
          <div class="tl-dot"></div>
          <div class="tl-pill">In development</div>
          <div class="tl-year">2026</div>
          <h3>Insightful Recommendations</h3>
          <p>Treatment timing, yard-level trends, and crew dispatch — turning detection into action.</p>
        </div>
        <div class="tl-stage">
          <div class="tl-dot"></div>
          <div class="tl-pill">R&amp;D</div>
          <div class="tl-year">2027</div>
          <h3>Autonomous Response</h3>
          <p>Closing the loop with in-hive interventions. The hive treats itself, and you only show up when you want to.</p>
        </div>
      </div>
    </div>
  </section>
```

- [ ] **Step 3: Reload and verify**

Cream traction band with 6 bordered stat cards. White roadmap band with 3-stage timeline, gold horizontal line connecting them on desktop, gold-filled "Shipping" pill on stage 1, cream pill on stage 2, gray pill on stage 3.

Resize to mobile: timeline collapses to vertical stack, the connector line disappears, stages become full-width blocks.

- [ ] **Step 4: Do not commit yet.**

---

## Task 9: Founders narrative section

**Files:**
- Modify: `index.html`
- Modify: `styles.css`

- [ ] **Step 1: Append CSS**

```css
/* ===== FOUNDERS NARRATIVE ===== */
.founders { padding: 140px 0; }
.founders .wrap-narrow { text-align: center; }
.founders h2 {
  font-size: clamp(34px, 4.4vw, 60px);
  max-width: 760px;
  margin: 0 auto 56px;
}
.founders-photos {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-bottom: 64px;
}
.founders-photos figure { text-align: center; }
.founders-photos img {
  width: 200px;
  height: 240px;
  object-fit: cover;
  border-radius: var(--radius-lg);
  border: 1px solid var(--line);
}
.founders-photos figcaption {
  margin-top: 14px;
  font-size: 13px;
  font-weight: 600;
  color: var(--ink);
}
.founders-photos figcaption .role {
  display: block;
  color: var(--muted);
  font-weight: 500;
  margin-top: 2px;
  font-size: 12px;
}
.founders-photos.single img { width: 320px; height: 220px; }
.founder-story {
  text-align: left;
  font-size: 18px;
  line-height: 1.75;
  color: var(--ink-soft);
  max-width: 720px;
  margin: 0 auto;
}
.founder-story p { margin-bottom: 24px; }
.founder-story p:first-child::first-letter {
  font-family: 'Instrument Serif', serif;
  font-style: italic;
  font-size: 76px;
  line-height: 1;
  float: left;
  padding: 8px 12px 0 0;
  color: var(--gold-dark);
}
.founder-story strong { color: var(--ink); font-weight: 600; }
.founder-story em {
  font-family: 'Instrument Serif', serif;
  font-style: italic;
  font-size: 19px;
  color: var(--gold-dark);
}
.founder-footnote {
  margin-top: 56px;
  text-align: center;
  font-size: 14px;
  color: var(--muted);
}
@media (max-width: 720px) {
  .founders { padding: 80px 0; }
  .founders-photos { gap: 18px; }
  .founders-photos img { width: 140px; height: 170px; }
  .founder-story { font-size: 17px; }
}
```

- [ ] **Step 2: Insert HTML after the roadmap section**

```html
  <!-- ===== FOUNDERS NARRATIVE ===== -->
  <section id="founders" class="founders bg-cream">
    <div class="wrap-narrow">
      <div class="eyebrow center">Who's building this</div>
      <h2>Robert and Danny have been building this story for <span class="serif-italic">seventeen years</span>.</h2>

      <div class="founders-photos single">
        <figure>
          <img src="/images/robert_and_danny.png" alt="Robert Schulte and Daniel Drew working hives">
          <figcaption>Robert Schulte &amp; Daniel Drew<span class="role">Co-founders</span></figcaption>
        </figure>
      </div>

      <div class="founder-story">
        <p>Robert started keeping bees when he was nine. By high school he had a half-dozen hives in his parents' backyard in Florida, and by the time he finished an engineering degree at UF, he had over a decade of seasons behind him — losing colonies the way every beekeeper loses colonies, watching mites arrive, watching queens fail, watching a treatment work one year and stop working the next.</p>
        <p>The summer before starting business school, he packed his car and spent three months on the road. He drove from Florida to Vermont to Montana to California, sleeping in the back seat most nights, sitting down with commercial beekeepers in their yards and warehouses and pickup trucks. Fifty-some interviews. He kept hearing the same things. <em>Mites are spreading faster than we can inspect.</em> <em>Africanized bees are taking over yards in weeks.</em> <em>I've got 10,000 colonies and 10 employees and we can't keep up.</em></p>
        <p>One conversation, with a commercial operator outside Ventura, California, turned into the question Robert hasn't been able to put down since: <strong>what if every hive could tell you when something's wrong, before you lose it?</strong> Not after the next inspection. Not after the next yard visit. The same day.</p>
        <p>Danny is the answer to <em>how</em>. Robert and Danny have been friends since UF — nine years of building things together, from undergraduate projects to side hardware experiments. Danny went on to build spacecraft at Blue Origin and now leads satellite delivery at Apex Space in Los Angeles. He knows how to make hardware survive in places where you can't fix it later, which turns out to be exactly the problem with a bee box that has to live in a remote yard for a year on solar power.</p>
        <p>They started PollenPal at the kitchen table. They're building it the same way Robert learned to keep bees — by listening to the people who actually do the work, and refusing to ship anything that doesn't pull its weight in the field.</p>
      </div>

      <p class="founder-footnote">Built with guidance from 4 Master Beekeepers and a research team at Columbia University.</p>
    </div>
  </section>
```

**Note on photos:** if individual `robert.png` / `daniel.png` headshots become available before launch, replace the single `<figure>` with two side-by-side figures and remove `class="single"` from `.founders-photos`.

- [ ] **Step 3: Reload and verify**

Cream-soft band, narrow 880px column, centered title with serif-italic accent on "seventeen years", combined photo with caption, drop-cap on the first paragraph (gold serif italic), italic emphasis on quoted phrases throughout, footnote at the bottom.

- [ ] **Step 4: Do not commit yet.**

---

## Task 10: Testimonial band

**Files:**
- Modify: `index.html`
- Modify: `styles.css`

- [ ] **Step 1: Append CSS**

```css
/* ===== TESTIMONIAL BAND ===== */
.testimonial {
  position: relative;
  padding: 140px 0;
  background: var(--ink) url('/images/wendy-ventura.jpg') center/cover no-repeat;
}
.testimonial::before {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(10,10,10,0.55) 0%, rgba(10,10,10,0.78) 100%);
}
.testimonial .wrap { position: relative; text-align: center; }
.testimonial blockquote {
  font-family: 'Instrument Serif', 'Times New Roman', serif;
  font-size: clamp(28px, 4.2vw, 52px);
  font-style: italic;
  font-weight: 400;
  line-height: 1.2;
  color: #fff;
  max-width: 920px;
  margin: 0 auto 32px;
  letter-spacing: -0.01em;
}
.testimonial cite {
  display: block;
  font-style: normal;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  color: var(--gold);
}
@media (max-width: 720px) {
  .testimonial { padding: 96px 0; }
}
```

- [ ] **Step 2: Insert HTML after the founders section**

```html
  <!-- ===== TESTIMONIAL BAND ===== -->
  <section class="testimonial">
    <div class="wrap">
      <blockquote>"Identifying and treating Africanization early would be worth $100k a year to our operation."</blockquote>
      <cite>Wendy · Blue Ridge Honey Co. · Ventura, CA</cite>
    </div>
  </section>
```

- [ ] **Step 3: Reload and verify**

Full-bleed photographic background with dark overlay, large serif italic pullquote in white, gold-amber attribution.

- [ ] **Step 4: Do not commit yet.**

---

## Task 11: Pilot CTA section + Footer

**Files:**
- Modify: `index.html`
- Modify: `styles.css`

- [ ] **Step 1: Append CSS**

```css
/* ===== PILOT CTA ===== */
.pilot { background: var(--ink); padding: 120px 0; }
.pilot .wrap { text-align: center; max-width: 720px; }
.pilot .eyebrow { color: var(--gold); }
.pilot .eyebrow::before { background: var(--gold); }
.pilot h2 { color: #fff; margin-bottom: 20px; }
.pilot .lede { color: rgba(255,255,255,0.78); margin: 0 auto 48px; }
.form-card {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 40px;
  text-align: left;
  max-width: 560px;
  margin: 0 auto;
}
.form-row { margin-bottom: 18px; }
.form-row.two { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.form-row label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 6px;
  letter-spacing: 0.3px;
}
.form-row input,
.form-row textarea {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  font-family: inherit;
  font-size: 15px;
  color: var(--ink);
  background: #fff;
  transition: border-color 0.2s;
}
.form-row input:focus,
.form-row textarea:focus {
  outline: none;
  border-color: var(--gold-dark);
}
.form-row textarea { resize: vertical; min-height: 90px; }
.form-card button {
  width: 100%;
  margin-top: 8px;
  padding: 16px;
  background: var(--gold-dark);
  color: #fff;
  border: none;
  border-radius: var(--radius);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.form-card button:hover { background: var(--ink); }
.form-success {
  text-align: center;
  padding: 32px 16px;
  color: var(--ink);
}
.form-success h3 { color: var(--gold-dark); margin-bottom: 12px; }
@media (max-width: 600px) {
  .form-row.two { grid-template-columns: 1fr; }
  .form-card { padding: 28px; }
}
```

- [ ] **Step 2: Insert pilot CTA HTML after the testimonial section**

Use the form action URL and field names you noted in Task 4 Step 2.

```html
  <!-- ===== PILOT CTA ===== -->
  <section id="pilot" class="pilot">
    <div class="wrap">
      <div class="eyebrow center">Run a pilot</div>
      <h2>Deploy PollenPal on your yard.</h2>
      <p class="lede">We're running pilots with commercial operators in 2026. Tell us about your operation and we'll be in touch within 2 business days.</p>

      <div class="form-card">
        <form id="pilotForm" action="REPLACE_WITH_GOOGLE_FORM_ACTION_FROM_OLD_INDEX" method="POST" target="hidden_iframe">
          <div class="form-row">
            <label for="p-name">Name *</label>
            <input type="text" id="p-name" name="entry.455027715" required>
          </div>
          <div class="form-row">
            <label for="p-email">Email *</label>
            <input type="email" id="p-email" name="entry.414264367" required>
          </div>
          <div class="form-row">
            <label for="p-company">Operation / company *</label>
            <input type="text" id="p-company" name="entry.119689931" required>
          </div>
          <div class="form-row two">
            <div>
              <label for="p-hives">Hive count</label>
              <input type="text" id="p-hives" name="entry.355024465">
            </div>
            <div>
              <label for="p-region">Region</label>
              <input type="text" id="p-region" name="entry.355024465-region">
            </div>
          </div>
          <div class="form-row">
            <label for="p-msg">Tell us about your operation</label>
            <textarea id="p-msg" name="entry.1292345725"></textarea>
          </div>
          <button type="submit">Request a pilot →</button>
        </form>
        <iframe name="hidden_iframe" style="display:none"></iframe>
      </div>
    </div>
  </section>

  <!-- (closing </main> moved below) -->
```

**Important:** Replace `REPLACE_WITH_GOOGLE_FORM_ACTION_FROM_OLD_INDEX` with the actual `action` URL from `index.html.old`. Do not invent a new URL.

- [ ] **Step 3: Insert footer HTML before `</body>`**

After `</main>`, insert:

```html
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="/images/logo-full.png" alt="PollenPal">
        <p>Physical AI for commercial apiaries and farms.</p>
      </div>
      <div>
        <h4>Product</h4>
        <ul>
          <li><a href="#how">How it works</a></li>
          <li><a href="#advantage">Why PollenPal</a></li>
          <li><a href="#roadmap">Roadmap</a></li>
          <li><a href="#pilot">Request a pilot</a></li>
        </ul>
      </div>
      <div>
        <h4>Company</h4>
        <ul>
          <li><a href="#founders">Founders</a></li>
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
      © 2026 PollenPal Inc.
    </div>
  </div>
</footer>
```

- [ ] **Step 4: Reload and verify**

Dark `--ink` pilot section with white form card and gold submit button. Footer with logo, tagline, three columns of links, and copyright line.

- [ ] **Step 5: Do not commit yet.**

---

## Task 12: Wire up `scripts.js` (mobile nav + form handler)

**Files:**
- Modify: `scripts.js`

- [ ] **Step 1: Write the script**

```javascript
// PollenPal — minimal interactive layer
// (1) Mobile nav toggle
// (2) Form submission feedback
// (3) Smooth scroll for in-page anchors

(function () {
  // ===== MOBILE NAV =====
  const toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      const open = toggle.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // ===== FORM FEEDBACK =====
  // Google Forms POST into a hidden iframe; we can't read the response,
  // but we can swap the form for a thank-you message after submit.
  document.querySelectorAll('form[target="hidden_iframe"]').forEach(function (form) {
    form.addEventListener('submit', function () {
      setTimeout(function () {
        const card = form.closest('.form-card');
        if (!card) return;
        card.innerHTML =
          '<div class="form-success">' +
          '<h3>Thanks — we\'ll be in touch.</h3>' +
          '<p>We\'ll respond within 2 business days.</p>' +
          '</div>';
      }, 600);
    });
  });

  // ===== SMOOTH ANCHOR SCROLL =====
  // Header is sticky, so account for its height when scrolling to anchors.
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      const id = link.getAttribute('href');
      if (id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const headerOffset = 72;
      const top = target.getBoundingClientRect().top + window.pageYOffset - headerOffset;
      window.scrollTo({ top: top, behavior: 'smooth' });
    });
  });
})();
```

- [ ] **Step 2: Reload the page**

Confirm:
- Resize to ~600px wide. Click the hamburger toggle. Nav links should appear as a stacked dropdown.
- Click any nav link or in-page anchor (e.g. "How it works"). Page should smooth-scroll to that section, accounting for the sticky header.
- Submit the pilot form with test values. Form card should swap to "Thanks — we'll be in touch."

- [ ] **Step 3: Do not commit yet.**

---

## Task 13: Build the `/investors` page

**Files:**
- Modify: `investors.html`
- Modify: `styles.css` (append investor-specific styles)

This page reuses the same header, footer, and visual system. Sections per spec: hero → problem → solution → financial impact → traction → competitive quadrant → TAM/SAM/SOM → partnerships → roadmap → team → contact.

For brevity in this plan: copy the homepage `<head>`, `<header>`, `<footer>`, and reuse the existing CSS classes for sections that are shared (hero variant, stat strip, timeline, pilot CTA pattern). The only new CSS is for the competitive quadrant SVG container, the TAM/SAM/SOM circles, and the financial impact table.

- [ ] **Step 1: Append investor-page CSS**

```css
/* ===== INVESTOR-PAGE ONLY ===== */

/* Financial impact table */
.impact-table {
  max-width: 760px;
  margin: 0 auto;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
}
.impact-table table { width: 100%; border-collapse: collapse; }
.impact-table th, .impact-table td { padding: 16px 22px; text-align: left; font-size: 15px; }
.impact-table thead th { background: var(--ink); color: #fff; font-size: 13px; font-weight: 600; letter-spacing: 0.5px; }
.impact-table tbody td { border-bottom: 1px solid var(--line); color: var(--ink-soft); }
.impact-table tbody tr:last-child td { border-bottom: none; }
.impact-table tbody tr.highlight td {
  background: var(--cream);
  font-weight: 700;
  color: var(--ink);
  font-size: 17px;
}
.impact-note {
  text-align: center;
  font-size: 12px;
  color: var(--muted);
  margin-top: 16px;
  font-style: italic;
}
.data-callout {
  max-width: 760px;
  margin: 32px auto 0;
  padding: 24px 28px;
  background: var(--cream-soft);
  border-left: 3px solid var(--gold);
  border-radius: 0 var(--radius) var(--radius) 0;
  font-family: 'Instrument Serif', serif;
  font-style: italic;
  font-size: 19px;
  line-height: 1.45;
  color: var(--gold-dark);
}

/* Competitive quadrant */
.quadrant {
  max-width: 720px;
  margin: 0 auto;
  position: relative;
  aspect-ratio: 1 / 1;
}
.quadrant svg { width: 100%; height: 100%; }
.quadrant .axis-label {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 600;
  fill: var(--muted);
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
.quadrant .competitor {
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 600;
  fill: var(--ink);
}
.quadrant .pollenpal-marker { fill: var(--gold); stroke: var(--ink); stroke-width: 2; }
.quadrant .competitor-marker { fill: #fff; stroke: var(--muted); stroke-width: 1.5; }

/* TAM / SAM / SOM */
.market {
  display: flex;
  justify-content: center;
  gap: 56px;
  flex-wrap: wrap;
  margin-top: 32px;
}
.market-ring { text-align: center; max-width: 220px; }
.market-circle {
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
  color: var(--ink);
  border: 2px solid var(--ink);
}
.market-circle.tam { width: 220px; height: 220px; background: var(--cream); }
.market-circle.sam { width: 180px; height: 180px; background: var(--gold); }
.market-circle.som { width: 140px; height: 140px; background: var(--gold-dark); color: #fff; }
.market-circle .mc-num { font-size: 28px; font-weight: 700; letter-spacing: -0.02em; }
.market-circle .mc-label { font-size: 12px; letter-spacing: 1.4px; font-weight: 600; }
.market-ring h4 { font-size: 16px; margin-bottom: 6px; }
.market-ring p { font-size: 13px; color: var(--muted); line-height: 1.5; }
@media (max-width: 720px) {
  .market { gap: 32px; }
}

/* Partnerships */
.partnerships-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  max-width: 880px;
  margin: 0 auto;
}
.partnership-card {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 32px;
  background: #fff;
}
.partnership-card h3 { font-size: 20px; margin-bottom: 12px; }
.partnership-card p { color: var(--ink-soft); font-size: 15px; line-height: 1.6; }
@media (max-width: 720px) { .partnerships-grid { grid-template-columns: 1fr; } }

/* Team grid */
.team-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  max-width: 880px;
  margin: 0 auto 32px;
}
.team-card {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 28px;
  background: #fff;
}
.team-card h3 { font-size: 18px; margin-bottom: 4px; }
.team-card .role { font-size: 12px; font-weight: 600; color: var(--gold-dark); letter-spacing: 0.5px; text-transform: uppercase; margin-bottom: 12px; }
.team-card p { color: var(--ink-soft); font-size: 14px; line-height: 1.55; }
@media (max-width: 720px) { .team-grid { grid-template-columns: 1fr; } }
```

- [ ] **Step 2: Write `investors.html`**

Build the page. Below is the full template — the engineer fills it in section by section. Reuse the homepage `<head>` block (changing the `<title>`, meta description, og:title), and reuse the homepage `<header>` and `<footer>` markup with `class="current"` added to the Investors link if there is one (there isn't in the homepage nav, so just leave the nav as-is).

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PollenPal — Investors</title>
  <meta name="description" content="PollenPal is physical AI for the $107B precision agriculture IoT market. Pilots deployed, customer interest validated, seeking seed investment to scale.">
  <link rel="icon" href="/images/logo-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
</head>
<body>

<a href="#main" class="skip-link">Skip to content</a>

<!-- (Same header markup as index.html — copy/paste verbatim) -->
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
    <a href="#contact" class="nav-cta">Get in touch →</a>
  </div>
</header>

<main id="main">

  <!-- HERO (cleaner variant: no floating stat cards) -->
  <section class="hero">
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <div class="eyebrow">Seeking seed investment</div>
        <h1>Empowering beekeeping through <span class="serif-italic">physical AI</span>.</h1>
        <p class="lede">Hardware and software for commercial apiaries and farms. Pilots deployed in CT, NY, and CA. Customer interest validated. Seeking investment to scale into the $107B precision agriculture IoT market.</p>
        <div class="hero-ctas">
          <a href="#contact" class="btn btn-primary">Get in touch →</a>
          <a href="#impact" class="btn btn-secondary">See the numbers</a>
        </div>
      </div>
      <div class="hero-visual">
        <div class="visual-frame">
          <video autoplay muted loop playsinline poster="/images/hero-poster.jpg" preload="metadata">
            <source src="/images/hero.mp4" type="video/mp4">
          </video>
          <div class="visual-overlay"></div>
        </div>
      </div>
    </div>
  </section>

  <!-- PROBLEM (deck slide 2 framing) -->
  <section class="section problem bg-cream">
    <div class="wrap">
      <div class="eyebrow center">The problem</div>
      <h2>Bees feed the world. But bees are <span class="serif-italic">dying faster</span> than food demand is growing.</h2>
      <p class="lede center">US beekeepers lose ~40% of colonies annually (48% in 2023). Replacement costs run $2.5B+ globally per year. The workforce is aging — median commercial beekeeper is 66, and 79% use no digital management tools at all. The industry is ripe for a technological reset.</p>
    </div>
  </section>

  <!-- SOLUTION (deck slide 3) -->
  <section class="section how">
    <div class="wrap">
      <div class="eyebrow center">The solution</div>
      <h2>Physical AI for every hive.</h2>
      <div class="how-grid">
        <div class="step">
          <img class="step-img" src="/images/device-field.jpg" alt="PollenPal device deployed in a field">
          <div class="step-body">
            <div class="step-num">01 · HARDWARE</div>
            <h3>Watches every bee in and out</h3>
            <p>Sub-$100 BOM. Solar + LTE for remote yards. Drops in under standard 10-frame Langstroth boxes — no custom hive bodies.</p>
          </div>
        </div>
        <div class="step">
          <img class="step-img" src="/images/ml-detection.jpg" alt="ML detection of bees and varroa">
          <div class="step-body">
            <div class="step-num">02 · MACHINE LEARNING</div>
            <h3>YOLOv11 trained on 20k+ images</h3>
            <p>~80% varroa accuracy. Detects mites at 1–1.5mm, africanization markers, and missing-queen indicators. Cloud inference today; central GPU on the roadmap.</p>
          </div>
        </div>
        <div class="step">
          <img class="step-img" src="/images/dashboard-phone.jpg" alt="Hive dashboard">
          <div class="step-body">
            <div class="step-num">03 · WEB APP</div>
            <h3>Hive-level alerts, multi-yard views</h3>
            <p>Designed with beekeeper input. Actionable insights over complex graphs. Recordkeeping, harvest logging, supply ordering integrated.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- FINANCIAL IMPACT -->
  <section id="impact" class="section bg-cream">
    <div class="wrap">
      <div class="eyebrow center">Financial impact</div>
      <h2 style="text-align:center;margin-bottom:48px;">Margin uplift on a 5,000-colony yard.</h2>
      <div class="impact-table">
        <table>
          <thead>
            <tr><th></th><th>Traditional management</th><th>With PollenPal</th></tr>
          </thead>
          <tbody>
            <tr><td>Hive loss rate</td><td>40%</td><td>10%</td></tr>
            <tr><td>Revenue</td><td>$1,200k</td><td>$1,425k</td></tr>
            <tr><td>Hive replacement costs</td><td>($400k)</td><td>($100k)</td></tr>
            <tr><td>Total costs</td><td>($1,000k)</td><td>($813k)</td></tr>
            <tr class="highlight"><td>Total Margin</td><td>$200k</td><td>$613k</td></tr>
          </tbody>
        </table>
      </div>
      <p class="impact-note">PollenPal cost not included. Source: Beekeeper interviews, USDA NASS honey report, ABJ, Bee Informed Partnership, PollenPal analysis.</p>
      <div class="data-callout">"By digitizing apiaries, we're collecting data unobtainable any other way. Our models compound in accuracy with every bee we see."</div>
    </div>
  </section>

  <!-- TRACTION (same as homepage) -->
  <section class="section traction">
    <div class="wrap">
      <div class="eyebrow center">Traction</div>
      <h2 style="text-align:center;margin-bottom:48px;">Pilot-ready and proven in the field.</h2>
      <div class="stat-strip">
        <div class="stat"><div class="stat-num">50+</div><div class="stat-label">Beekeeper interviews</div></div>
        <div class="stat"><div class="stat-num">20k+</div><div class="stat-label">Field images trained</div></div>
        <div class="stat"><div class="stat-num">~80%</div><div class="stat-label">Varroa accuracy</div></div>
        <div class="stat"><div class="stat-num">3</div><div class="stat-label">Pilots committed (CT, NY, CA)</div></div>
        <div class="stat"><div class="stat-num">12</div><div class="stat-label">Hardware iterations</div></div>
        <div class="stat"><div class="stat-num">4</div><div class="stat-label">Master Beekeeper advisors</div></div>
      </div>
    </div>
  </section>

  <!-- COMPETITIVE QUADRANT -->
  <section class="section bg-cream">
    <div class="wrap">
      <div class="eyebrow center">Competitive position</div>
      <h2 style="text-align:center;margin-bottom:48px;max-width:880px;margin-left:auto;margin-right:auto;">Accuracy <span class="serif-italic">and</span> deployability — not one or the other.</h2>
      <div class="quadrant">
        <svg viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
          <!-- Axes -->
          <line x1="60" y1="540" x2="560" y2="540" stroke="#0A0A0A" stroke-width="1.5"/>
          <line x1="60" y1="540" x2="60" y2="40" stroke="#0A0A0A" stroke-width="1.5"/>
          <!-- Axis labels -->
          <text class="axis-label" x="310" y="580" text-anchor="middle">Easier to deploy at scale →</text>
          <text class="axis-label" x="40" y="290" text-anchor="middle" transform="rotate(-90 40 290)">Actionable insights →</text>
          <!-- Manual inspection: low/low quadrant -->
          <circle class="competitor-marker" cx="180" cy="440" r="14"/>
          <text class="competitor" x="200" y="445">Manual inspection</text>
          <!-- BroodMinder: easy but basic -->
          <circle class="competitor-marker" cx="420" cy="430" r="14"/>
          <text class="competitor" x="440" y="435">BroodMinder</text>
          <!-- Solution Bee: middle -->
          <circle class="competitor-marker" cx="240" cy="280" r="14"/>
          <text class="competitor" x="260" y="285">Solution Bee</text>
          <!-- Beewise: accurate but expensive -->
          <circle class="competitor-marker" cx="180" cy="180" r="14"/>
          <text class="competitor" x="200" y="185">Beewise</text>
          <!-- PollenPal: top right -->
          <circle class="pollenpal-marker" cx="460" cy="160" r="22"/>
          <text class="competitor" x="490" y="166" style="font-size:15px;font-weight:700">PollenPal</text>
        </svg>
      </div>
    </div>
  </section>

  <!-- MARKET SIZE -->
  <section class="section">
    <div class="wrap">
      <div class="eyebrow center">Market opportunity</div>
      <h2 style="text-align:center;margin-bottom:24px;">Precision agriculture IoT is a <span class="serif-italic">$107B</span> market.</h2>
      <p class="lede center">PollenPal starts in US hive management and expands into broader pest detection and pollination verification across orchards, vineyards, and greenhouses.</p>
      <div class="market">
        <div class="market-ring">
          <div class="market-circle tam">
            <div class="mc-num">$107B+</div><div class="mc-label">TAM</div>
          </div>
          <h4>Precision Crop Protection</h4>
          <p>IoT, intervention marketplace, pollination verification, and precision application OS.</p>
        </div>
        <div class="market-ring">
          <div class="market-circle sam">
            <div class="mc-num">$24B</div><div class="mc-label">SAM</div>
          </div>
          <h4>Crop Monitoring + Treatment</h4>
          <p>Pest detection across orchards, vineyards, and greenhouses plus treatment sales.</p>
        </div>
        <div class="market-ring">
          <div class="market-circle som">
            <div class="mc-num">$128M</div><div class="mc-label">SOM</div>
          </div>
          <h4>US Hive Management</h4>
          <p>PollenPal hardware and software subscriptions sold to US beekeepers.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- PARTNERSHIPS -->
  <section class="section bg-cream">
    <div class="wrap">
      <div class="eyebrow center">Partnerships</div>
      <h2 style="text-align:center;margin-bottom:48px;">Two channels to unlock scale with low CAC.</h2>
      <div class="partnerships-grid">
        <div class="partnership-card">
          <h3>Corporate Managed Beekeeping</h3>
          <p>Corporate beekeeping platforms manage hives across 24+ US cities for corporate clients. PollenPal adds continuous monitoring between beekeeper visits, enabling a premium tech-enabled service tier.</p>
        </div>
        <div class="partnership-card">
          <h3>Honey &amp; Pollinator Brands</h3>
          <p>Honey and pollinator-focused brands depend on healthy, sustainable hives with supply chain traceability. PollenPal monitors their supply chain apiaries, and the brand subsidizes the cost.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ROADMAP (same as homepage) -->
  <section class="section roadmap">
    <div class="wrap">
      <div class="eyebrow center">Roadmap</div>
      <h2 style="text-align:center;margin-bottom:24px;max-width:900px;margin-left:auto;margin-right:auto;">From threat detection to <span class="serif-italic">autonomous</span> response.</h2>
      <div class="timeline" style="margin-top:64px">
        <div class="tl-stage"><div class="tl-dot"></div><div class="tl-pill">Shipping</div><div class="tl-year">2026</div><h3>Threat Detection</h3><p>Varroa, africanization, and queen issues caught the day they appear.</p></div>
        <div class="tl-stage"><div class="tl-dot"></div><div class="tl-pill">In development</div><div class="tl-year">2026</div><h3>Insightful Recommendations</h3><p>Treatment timing, yard-level trends, and crew dispatch.</p></div>
        <div class="tl-stage"><div class="tl-dot"></div><div class="tl-pill">R&amp;D</div><div class="tl-year">2027</div><h3>Autonomous Response</h3><p>Closing the loop with in-hive interventions.</p></div>
      </div>
    </div>
  </section>

  <!-- TEAM -->
  <section class="section bg-cream">
    <div class="wrap">
      <div class="eyebrow center">Team</div>
      <h2 style="text-align:center;margin-bottom:48px;">Deep tech and apiary expertise.</h2>
      <div class="team-grid">
        <div class="team-card">
          <h3>Robert Schulte</h3>
          <div class="role">Co-founder, CEO</div>
          <p>Ex-BCG, Columbia MBA. UF engineering. 17+ years beekeeping experience. Spent the summer of 2025 interviewing 50+ commercial operators across the US.</p>
        </div>
        <div class="team-card">
          <h3>Daniel Drew</h3>
          <div class="role">Co-founder, CTO</div>
          <p>Spacecraft Manufacturing Engineer at Apex Space. Ex-Blue Origin. UF engineering. 9-year partnership with Robert.</p>
        </div>
        <div class="team-card">
          <h3>Tech Team</h3>
          <div class="role">Engineering</div>
          <p>1 Columbia Research Scientist (computer vision, backed by Google + NVIDIA). 4 Columbia engineering students building the ML pipeline and web app through Columbia Build Lab.</p>
        </div>
        <div class="team-card">
          <h3>Beekeeping Team</h3>
          <div class="role">Advisory</div>
          <p>4 Master Beekeeper advisors providing guidance on hive management and treatment protocols. Commercial beekeeper partners deploying devices and contributing field data.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- INVESTOR CONTACT (reuses pilot CTA pattern) -->
  <section id="contact" class="pilot">
    <div class="wrap">
      <div class="eyebrow center">Get in touch</div>
      <h2>Interested in learning more?</h2>
      <p class="lede">We're seeking seed investment to scale our 2026 commercial pilots and accelerate the data flywheel.</p>
      <div class="form-card">
        <form id="invForm" action="REPLACE_WITH_GOOGLE_FORM_ACTION" method="POST" target="hidden_iframe2">
          <div class="form-row"><label for="i-name">Name *</label><input type="text" id="i-name" name="entry.455027715" required></div>
          <div class="form-row"><label for="i-email">Email *</label><input type="email" id="i-email" name="entry.414264367" required></div>
          <div class="form-row"><label for="i-firm">Firm / organization</label><input type="text" id="i-firm" name="entry.119689931"></div>
          <div class="form-row"><label for="i-msg">Tell us about your interest</label><textarea id="i-msg" name="entry.1292345725"></textarea></div>
          <button type="submit">Get in touch →</button>
        </form>
        <iframe name="hidden_iframe2" style="display:none"></iframe>
      </div>
    </div>
  </section>

</main>

<!-- (Same footer markup as index.html — copy/paste verbatim) -->
<footer class="site-footer">
  <!-- (footer content — copy from Task 11) -->
</footer>

<script src="/scripts.js" defer></script>
</body>
</html>
```

**Replace `REPLACE_WITH_GOOGLE_FORM_ACTION`** with the same Google Form action URL used on the homepage. **Copy the footer block verbatim from `index.html`** — do not retype it.

- [ ] **Step 3: Open `investors.html` in the browser**

Run: `start C:/projects/Pollenpal-website/investors.html`

Walk through every section: hero, problem, solution, financial impact table, traction stats, competitive quadrant SVG, market circles, partnerships, roadmap, team, contact form, footer.

Verify:
- Quadrant SVG renders cleanly (gold PollenPal marker top-right, four white competitor markers).
- Market circles stack correctly (TAM largest cream, SAM medium gold, SOM smallest gold-dark).
- Financial impact table has gold-cream highlight on the Total Margin row.
- Mobile collapses cleanly.

- [ ] **Step 4: Do not commit yet.**

---

## Task 14: Build the `/hobbyist` page

**Files:**
- Modify: `hobbyist.html`

Tight one-pager. Reuses all existing CSS — no new styles needed.

- [ ] **Step 1: Write `hobbyist.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>PollenPal — for backyard beekeepers</title>
  <meta name="description" content="PollenPal's backyard version: WiFi setup, AI photo diagnosis, and live beekeeper chat. Join the waitlist.">
  <link rel="icon" href="/images/logo-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Instrument+Serif&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
</head>
<body>

<a href="#main" class="skip-link">Skip to content</a>

<!-- Same header as index.html, with Hobbyist as current page link if you add it to nav -->
<header class="site-header">
  <div class="wrap nav">
    <a href="/" class="nav-logo"><img src="/images/logo-full.png" alt="PollenPal"></a>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">☰</button>
    <nav class="nav-links">
      <a href="/#how">How it works</a>
      <a href="/#advantage">Why PollenPal</a>
      <a href="/hobbyist" class="current">Hobbyist</a>
      <a href="/investors">Investors</a>
    </nav>
    <a href="#waitlist" class="nav-cta">Join the waitlist →</a>
  </div>
</header>

<main id="main">

  <!-- HERO -->
  <section class="hero">
    <div class="wrap hero-grid">
      <div class="hero-copy">
        <div class="eyebrow">For backyard beekeepers</div>
        <h1>Your 5 hives deserve more than <span class="serif-italic">annual</span> inspections.</h1>
        <p class="lede">PollenPal's backyard version plugs into your home WiFi and power. Get alerts the moment something's wrong, and talk to a real beekeeper when you need one.</p>
        <a href="#waitlist" class="btn btn-primary">Join the waitlist →</a>
      </div>
      <div class="hero-visual">
        <div class="visual-frame">
          <video autoplay muted loop playsinline poster="/images/hero-poster.jpg"><source src="/images/hero.mp4" type="video/mp4"></video>
          <div class="visual-overlay"></div>
        </div>
      </div>
    </div>
  </section>

  <!-- WHAT'S DIFFERENT -->
  <section class="section how">
    <div class="wrap">
      <div class="eyebrow center">Built for backyard beekeeping</div>
      <h2>Designed for hobbyists, not for fleets.</h2>
      <div class="how-grid">
        <div class="step">
          <div class="step-body">
            <div class="step-num">SETUP</div>
            <h3>Plugs into your house</h3>
            <p>Home WiFi and a regular power outlet. No solar panels, no LTE, no cellular plan. You can have it running in minutes.</p>
          </div>
        </div>
        <div class="step">
          <div class="step-body">
            <div class="step-num">SUPPORT</div>
            <h3>Snap a photo, get a diagnosis</h3>
            <p>The AI assistant tells you what you're looking at. When you need a real human, the optional live beekeeper chat connects you with someone who's seen it before.</p>
          </div>
        </div>
        <div class="step">
          <div class="step-body">
            <div class="step-num">SHARE</div>
            <h3>Live stream your hive</h3>
            <p>Share your hive entrance with friends, your local bee club, or the internet. Watching bees come and go is one of the best parts of beekeeping.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- IMPACT TABLE -->
  <section class="section bg-cream">
    <div class="wrap">
      <div class="eyebrow center">What it changes</div>
      <h2 style="text-align:center;margin-bottom:48px;">A 5-hive backyard, with and without PollenPal.</h2>
      <div class="impact-table">
        <table>
          <thead><tr><th></th><th>Without</th><th>With PollenPal</th></tr></thead>
          <tbody>
            <tr><td>Hives lost in a year</td><td>2</td><td>0</td></tr>
            <tr><td>Replacement costs</td><td>$500</td><td>$0</td></tr>
            <tr><td>Honey collected</td><td>150 lbs</td><td>250 lbs</td></tr>
            <tr><td>Honey value</td><td>$1,500</td><td>$2,500</td></tr>
            <tr class="highlight"><td>Annual value added</td><td>—</td><td>$1,350</td></tr>
          </tbody>
        </table>
      </div>
      <p class="impact-note">PollenPal cost not included. Source: USDA NASS, ABJ, Bee Informed Partnership.</p>
    </div>
  </section>

  <!-- TESTIMONIAL -->
  <section class="testimonial" style="background-image:none;background:var(--cream-soft);">
    <div class="wrap">
      <blockquote style="color:var(--ink);">"For my first 4 years, I spent $600 on lost hives, and I didn't know why I was losing them."</blockquote>
      <cite style="color:var(--gold-dark);">Karen · Backyard beekeeper, South Florida</cite>
    </div>
  </section>

  <!-- WAITLIST -->
  <section id="waitlist" class="pilot">
    <div class="wrap">
      <div class="eyebrow center">Join the waitlist</div>
      <h2>Be first when the backyard version ships.</h2>
      <p class="lede">We're starting limited shipments of the backyard PollenPal in 2026. Get on the list and we'll let you know when it's your turn.</p>
      <div class="form-card">
        <form id="hobForm" action="REPLACE_WITH_GOOGLE_FORM_ACTION" method="POST" target="hidden_iframe3">
          <div class="form-row"><label for="h-name">Name *</label><input type="text" id="h-name" name="entry.455027715" required></div>
          <div class="form-row"><label for="h-email">Email *</label><input type="email" id="h-email" name="entry.414264367" required></div>
          <div class="form-row"><label for="h-hives">Number of hives</label><input type="text" id="h-hives" name="entry.355024465"></div>
          <div class="form-row"><label for="h-msg">Anything you'd like us to know</label><textarea id="h-msg" name="entry.1292345725"></textarea></div>
          <button type="submit">Join the waitlist →</button>
        </form>
        <iframe name="hidden_iframe3" style="display:none"></iframe>
      </div>
    </div>
  </section>

</main>

<!-- Same footer as index.html — copy/paste verbatim -->
<footer class="site-footer">
  <!-- (paste footer from Task 11) -->
</footer>

<script src="/scripts.js" defer></script>
</body>
</html>
```

**Replace `REPLACE_WITH_GOOGLE_FORM_ACTION`** with the homepage form action.
**Paste the footer markup verbatim** from `index.html`.

The hobbyist testimonial section overrides the dark background of `.testimonial` because we don't have a Karen photo to use as a backdrop. It uses `--cream-soft` background and ink-colored quote text instead.

- [ ] **Step 2: Open in browser and verify**

Run: `start C:/projects/Pollenpal-website/hobbyist.html`

Walk through: hero, three feature cards (no images, just text — that's intentional for tightness), 5-hive impact table, Karen quote on cream, waitlist form, footer.

- [ ] **Step 3: Do not commit yet.**

---

## Task 15: Final review, performance pass, and the one commit

**Files:**
- All site files (review only)
- Delete: `index.html.old` (after final approval)
- Delete: unused images from `images/` folder

- [ ] **Step 1: Performance check**

Run a local server: `py -3.13 -m http.server 8000` from the project root.

Open `http://localhost:8000` in Chrome. Open DevTools → Lighthouse. Run on **mobile**, performance + accessibility + best practices + SEO.

Expected scores:
- Performance ≥ 90
- Accessibility ≥ 95
- Best Practices ≥ 95
- SEO ≥ 95

Common fixes if performance is low:
- Hero MP4 too large → re-encode with higher CRF in `prep_assets.py` and rerun.
- Image sizes too large → reduce `max_width` in `prep_assets.py`.
- Layout shift from font swap → already mitigated with `display=swap` and preconnect.

- [ ] **Step 2: Cross-browser visual check**

Open all three pages (`/`, `/investors`, `/hobbyist`) in:
- Chrome (or Edge)
- Firefox
- Safari (if on Mac) or mobile preview via DevTools device emulation

Check for layout breaks, font fallbacks, video playback. Hero video should autoplay muted everywhere.

- [ ] **Step 3: Audit the `images/` directory and delete unused files**

Run: `ls C:/projects/Pollenpal-website/images/`

Compare against the asset list in the spec. Files referenced in the new pages: `logo-full.png`, `logo-icon.png`, `robert_and_danny.png`, `hero.mp4`, `hero-poster.jpg`, `device-grass.jpg`, `device-field.jpg`, `device-cad.jpg`, `ml-detection.jpg`, `ml-detection-simple.jpg`, `dashboard-phone.jpg`, `wendy-ventura.jpg`, `nyc-rooftop.jpg`.

Delete every other image file from `images/`. Be conservative — if unsure, leave it.

- [ ] **Step 4: Show the user the live local site and request approval**

Tell the user: "Local server running at http://localhost:8000. Walk through `/`, `/investors`, and `/hobbyist`. Once you're happy I'll do the single commit and push."

**WAIT for explicit approval before proceeding to step 5.** Per the user's instruction in the spec, nothing goes to git until they approve the live site.

- [ ] **Step 5: Delete the backup file**

Run: `rm C:/projects/Pollenpal-website/index.html.old`

- [ ] **Step 6: Stage and commit everything**

```bash
cd C:/projects/Pollenpal-website
git add styles.css scripts.js index.html investors.html hobbyist.html images/ scripts/prep_assets.py docs/
git status
```

Verify no `.superpowers/`, no `*.pptx`, no `index.html.old` is staged. Then:

```bash
git commit -m "$(cat <<'EOF'
Rebuild website with v4 narrative and editorial visual system

Full redesign of pollenpal.com per the v4 pitch deck:
- Single commercial-beekeeper homepage (was a dual-tab beekeeper/investor split)
- Dedicated /investors page with the condensed deck flow
- Dedicated /hobbyist page for the backyard waitlist
- New visual system: Inter + Instrument Serif italic accents, restrained gold + cream + ink palette
- Hero video re-encoded from the deck 360 apiary GIF
- "Why PollenPal" competitive-advantage section replaces the old product deep-dive
- Long-form founder story replaces the old founder card

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 7: Push when the user gives the go-ahead**

**Wait for the user to say "push" before running:**

```bash
git push origin main
```

GitHub Pages will rebuild automatically. Live site updates within ~1 minute.

- [ ] **Step 8: Verify the live site**

Open `https://pollenpal.com` in a private browser window. Walk through all three pages. Confirm hero video plays, forms render, mobile layouts work.

---

## Self-review checklist

This plan has been self-reviewed against the spec. Notes:

- **Spec coverage:** Every section in the spec has a corresponding task. Homepage sections 1–12 are covered by Tasks 4–11. The investor page is one task (13). The hobbyist page is one task (14). Visual system is Task 3. Asset prep is Task 2. Performance, a11y, and final commit are Task 15.
- **Placeholders:** No "TBD" or "TODO" inside steps. Two intentional placeholders (`REPLACE_WITH_GOOGLE_FORM_ACTION_FROM_OLD_INDEX`) are flagged with explicit instructions to read the URL from the existing site — these are not unfilled work, they're values the engineer must read out of the existing file rather than hardcode.
- **Type consistency:** Class names (`.btn-primary`, `.adv-card`, `.tl-stage`, `.stat-strip`) are defined once in Task 3 / inline in their owning task and used consistently across pages.
- **Commit discipline:** Tasks 1–14 explicitly do not commit. Task 15 is the single commit, gated on user approval of the live local preview. This matches the user's directive that nothing should reach git until they review.
- **Open questions from the spec:** Not all 8 open questions are answered yet. Three (founder prose review, headshot availability, "How it works" final title) need user input before Task 4 / Task 6 / Task 9 are run. Two (animation, hobbyist priority) are decisions the user should make during execution. The plan handles this by treating those as defaults: shippable now, easy to swap later.

---

## Open questions for the user before execution

1. **Final hero video size budget?** (Soft 1.5 MB / hard 2.5 MB are in the spec. Confirm or adjust.)
2. **"How it works" title** — keep "From bee to alert in minutes." or rework?
3. **Founder story prose** — Robert should review the ~400-word draft in the spec before Task 9 runs.
4. **Founder headshots** — do `robert.png` / `daniel.png` exist, or use the combined photo?
5. **Hobbyist page** — build now (Task 14) or skip and ship homepage + investors first?
6. **Backed-by strip content** — Columbia + Big Idea + Master Beekeepers, or swap in press/accelerators?
