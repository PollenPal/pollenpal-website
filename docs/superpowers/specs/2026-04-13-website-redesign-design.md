# PollenPal Website Redesign — v4 Narrative + Visual Refresh

**Date:** 2026-04-13
**Status:** Design draft — awaiting approval
**Scope:** Full redesign of pollenpal.com (visual + content + structure), driven by the v4 pitch deck.

---

## Goals

1. **Look like a startup, not a consumer brand.** Tight editorial layout, confident type, restrained color, generous whitespace. Inspired by Linear/Vercel/Ramp execution but keeping PollenPal's warm mission DNA.
2. **Speak to commercial beekeepers first.** Homepage is a single-audience B2B pitch. Secondary audiences (investors, hobbyists) get focused sub-pages.
3. **Sync with v4 deck narrative.** New positioning ("physical AI for commercial apiaries and farms"), new market frame (precision agriculture IoT), new roadmap (Detect → Recommend → Respond), new asset set (deck imagery + 360° hero GIF).
4. **Stay shippable.** Static HTML on GitHub Pages. No framework, no build step, no backend beyond existing Google Forms.

## Non-goals

- Authenticated user flows, login, or the product app itself (lives at app.pollenpal.com).
- Blog/CMS/documentation system.
- Internationalization.
- E-commerce.
- Redesigning the hobbyist-facing flow beyond a single tight page.

---

## Architecture

### Pages

```
/                 index.html       Commercial beekeeper homepage (primary)
/investors        investors.html   Investor pitch page (deck flow, condensed)
/hobbyist         hobbyist.html    Backyard beekeeper waitlist page
```

All three pages share a single stylesheet (`styles.css`) and reuse the same header/footer markup. No JS framework. One small `scripts.js` for form handling and mobile nav toggle.

### Deployment

GitHub Pages serves the root. `CNAME` already points to `pollenpal.com`. No change.

### Assets

**Homepage assets** (deck media extracted from `PollenPal v4_Pitch.pptx`, renamed for clarity):
- `hero.mp4` — re-encoded from deck `image17.gif` (224 frames, 190×336) into web-optimized H.264/AAC, ~800KB–1.5MB
- `hero-poster.jpg` — first frame static poster (used for `prefers-reduced-motion` and as `<video poster>`)
- `device-grass.jpg` — from deck `image5.png` (used in How it works step 1)
- `ml-detection.jpg` — from deck `image32.png` (used in How it works step 2)
- `dashboard-phone.jpg` — from deck `image6.png` (used in How it works step 3)
- `wendy-ventura.jpg` — from deck `image24.jpeg` (testimonial band backdrop)
- `robert.png` and `daniel.png` — individual founder headshots for the story section. If unavailable at build time, fall back to the existing `robert_and_danny.png`.

**Investor-page-only assets** (used on `/investors`, not homepage):
- `device-field.jpg` — from deck `image35.png` (device in field landscape; supports the solution section)
- `device-cad.jpg` — from deck `image34.png` (CAD exploded view; hardware detail)
- `ml-detection-simple.jpg` — from deck `image7.png` (cleaner bbox viz, secondary use)
- `nyc-rooftop.jpg` — from deck `image25.jpeg` (urban beekeeping, secondary photo for partnerships)

**Existing site assets retained:** `logo-full.png`, `logo-icon.png`, `robert_and_danny.png` (founder fallback), `dashboard-web.png` (investor page solution screenshot), `columbia-logo.png`.

Everything else in the current `images/` folder: reviewed case-by-case; unused assets deleted.

---

## Visual system

Token values are final; named here once and reused throughout both stylesheet and spec.

### Color

| Token | Value | Use |
|---|---|---|
| `--gold` | `#E8A43A` | Primary accent (matches deck SOM circle) |
| `--gold-dark` | `#C2851A` | Hover, emphasis, italic serif accent |
| `--cream` | `#FFECB7` | Solid cream highlight (deck TAM circle) |
| `--cream-soft` | `#FFF8E7` | Section tint, hero glow background |
| `--ink` | `#0A0A0A` | Headings, CTAs, dark bands |
| `--ink-soft` | `#3A3A3A` | Body text |
| `--muted` | `#6B6B6B` | Captions, meta, labels |
| `--line` | `#EAEAEA` | 1px dividers, card borders |
| `--bg` | `#FFFFFF` | Dominant background |
| `--success` | `#1F8A3B` | Positive delta, in-development badges |
| `--alert` | `#E04A3A` | Threat alert indicators |

### Typography

- **Primary:** Inter 400/500/600/700/800 (Google Fonts). Tight letter-spacing on headings (`-0.025em` to `-0.035em`).
- **Accent:** Instrument Serif (italic) used sparingly — one word per hero headline, sparingly in section headings. Gold-dark color.
- **Scale:** hero `clamp(46px, 6.2vw, 88px)`, section title `clamp(32px, 4vw, 56px)`, body `17–19px`, small `13–14px`.
- **Line-height:** body `1.55–1.65`, headings `0.98–1.1`.

### Layout and feel

- Max content width `1240px`; gutter `32px`.
- Vertical rhythm between sections `96–120px` desktop, `56–72px` mobile.
- Radius cap at `8px–14px`. No pill buttons, no bubbly cards.
- Shadows used once for the hero visual frame only. Everything else uses 1px `--line` borders or cream tinted backgrounds.
- Dividers are 1px solid `--line`; section separators are whitespace, not lines (except the "Backed by" strip).
- No stock honeycomb patterns, no chamfered SVG swooshes, no glassmorphism.

### Buttons

- `.btn-primary` — solid `--ink` fill, white text, `8px` radius, `15px 28px` padding. Hover → `--gold-dark` background.
- `.btn-secondary` — transparent, `--line` border, `--ink` text. Hover → `--ink` border.
- Button copy uses an arrow glyph `→` at end.

---

## Homepage (`/`) — section by section

Commercial beekeeper only. Order is final.

### 1. Header

Sticky, white, 1px bottom divider.
- Left: `logo-full.png` at 32px height.
- Center: nav links `Product · How it works · Pilots · Company`.
- Right: single CTA button "Request a pilot →".
- Mobile: nav collapses into hamburger; CTA stays visible.

### 2. Hero (`#hero`)

Two-column grid, 1.15 : 1 ratio. Reference mock validated 2026-04-13.

**Left column:**
- Eyebrow: `PHYSICAL AI FOR COMMERCIAL APIARIES & FARMS` (gold-dark, 1.8px tracking, all caps, 12px). Small 28px gold rule before the text.
- Headline (H1): two-line, `Inspect every hive.` / `<em>Every</em> day.` — the word "Every" in Instrument Serif italic gold-dark.
- Sub-headline: "PollenPal watches every bee in and out of your hive and flags varroa, africanization, and queen issues before they spread. Your crews treat the problem. They don't hunt for it."
- CTAs: `Request a pilot →` (primary) + `See how it works` (secondary).
- Proof row (below 1px top divider): three metrics horizontally — `20k+ Field images trained` / `~80% Varroa detection` / `3 Commercial pilots`.

**Right column:**
- 4:5 aspect dark frame (max 440px wide) containing the 360° apiary video loop.
- Top-left pill: `● Live apiary feed`.
- Bottom gradient (transparent → 55% black) with caption: pulsing gold dot + "Ventura yard · 48 hives monitored · updating in real time".
- Two floating stat cards overlap the frame:
  - Top-left: red dot + "Varroa alert · Hive 14" / "Detected 6 min ago".
  - Bottom-right: "COLONIES MONITORED / 4,712 / +284 this week".
- Hidden on mobile < 960px (cards only); frame reorders above copy.

**Background:** large soft radial glow using `--cream-soft` behind the right half of the hero.

### 3. Backed-by strip

Cream `#FFF8E7` band, 1px top + bottom divider.
- Single line: `BACKED BY  ·  Columbia Business School  ·  Big Idea Pitch Winners 2025  ·  4 Master Beekeepers`.
- All uppercase, muted gray, 12–14px, 1px tracking.
- Replaces current site's disconnected Columbia logo block.

### 4. Problem (`#problem`)

White bg, generous padding.
- Section eyebrow: `THE STAKES`.
- Section headline (pullquote style, serif italic for one phrase): **"Bees feed the world. But bees are <em>dying faster</em> than food demand is growing."** — paraphrased from deck slide 2.
- Lead paragraph: one tight paragraph explaining that commercial beekeepers lose ~40% of colonies a year, that manual inspection doesn't scale, and that the two biggest killers are varroa mites and africanization.
- Two problem cards, side by side, cream-tinted, 1px gold-dark left border:
  - **Varroa Mites** — "Parasites spread deadly viruses undetected until collapse. By inspection time, the damage is done."
  - **Africanization** — "Invasive bees outcompete European bees and turn gentle yards aggressive in weeks. Entire operations become unworkable."
- Stat bar below cards: dark `--ink` band, gold numerals. "40%+ annual colony losses · $635M+ in damages to US beekeepers annually".

### 5. How it works (`#how`)

Cream-soft background band.
- Eyebrow: `HOW IT WORKS`.
- Section title: "From bee to alert in minutes." (or similar — TBD in copy review).
- Three numbered steps, horizontal on desktop, stacked on mobile. Each step is a minimal card: image on top, `01` numeral in gold, title, short description.
  1. **Hardware watches** — `device-grass.jpg`. "A solar-powered PollenPal box sits as the base of your hive stack. Its camera and sound sensors watch every bee in and out, 24/7."
  2. **ML catches threats** — `ml-detection.jpg`. "YOLOv11 trained on 20,000+ field images spots varroa at 1–1.5mm, africanization markers, and queen problems — things a beekeeper can't catch by eye."
  3. **You get an alert** — `dashboard-phone.jpg`. "When something looks wrong, your phone gets a notification. Clear explanation, clear action, no guesswork."

### 6. Why PollenPal (`#advantage`)

Competitive advantage section. Replaces the deeper product walk-through and the financial table — both felt too dense for a marketing homepage, and the differentiation story does more work than either.

Anchored on deck slide 9's positioning: PollenPal is the only solution that's both **highly accurate** and **easy/affordable to deploy at scale**. Manual inspection is cheap but doesn't catch what matters. Existing smart-hive products are either too expensive, too coarse, or too hard to deploy in a real commercial yard.

White background.
- Eyebrow: `WHY POLLENPAL`.
- Title: "Built for commercial scale, not science fairs."
- Lead paragraph: one tight paragraph reframing the trade-off — every other tool forces beekeepers to choose between cheap-but-blind (manual inspection) and accurate-but-impractical (heavy in-hive sensors, six-figure systems). PollenPal is the first that doesn't.

**Three differentiator cards** (horizontal on desktop, stacked on mobile). Each: small gold icon/numeral, short title, 2–3 sentences. Border-only, no shadow.

1. **Continuous, per-hive monitoring**
   "Manual inspection happens every few weeks. Smart-hive systems average across the whole yard. PollenPal watches every bee, every day, in every hive — so threats get caught the day they appear, not the next visit."

2. **Sub-$100 hardware that drops in**
   "Most smart-hive products cost thousands per colony and require a custom hive body. PollenPal's box uses off-the-shelf compute and sits under your standard 10-frame Langstroth — no adapters, no rewiring, no swap-out. Solar and LTE mean it works in remote yards."

3. **A data moat that compounds**
   "Every PollenPal in the field improves the model for every other PollenPal. After one full season we already had 20,000+ field-labeled images and ~80% varroa accuracy. *By digitizing apiaries, we're collecting data unobtainable any other way. Our models compound in accuracy with every bee we see.*"

The third card's italic line is the deck's data-moat quote — kept as the closer of the section since it's the most defensible long-term claim.

### 7. Traction (`#traction`)

White background.
- Eyebrow: `TRACTION`.
- Title: "Pilot-ready and proven in the field."
- Horizontal strip of 6 stat cards (minimal, border-only, no shadow):
  - `50+ Beekeeper interviews`
  - `20k+ Field images trained`
  - `~80% Varroa accuracy`
  - `3 Commercial pilots committed (CT, NY, CA)`
  - `12 Hardware iterations`
  - `4 Master Beekeeper advisors`
- No Columbia logo here — moved to the backed-by strip at the top.

### 8. Roadmap (`#roadmap`)

White background.
- Eyebrow: `WHAT'S NEXT`.
- Title: "From threat detection to autonomous response."
- Horizontal 3-stage timeline (responsive: stacks vertically on mobile):
  1. **2026 · Threat Detection** — "Shipping to commercial pilots now. Varroa, africanization, queen issues."
  2. **2026 · Insightful Recommendations** — "In development. Treatment timing, yard-level trends, crew dispatch."
  3. **2027 · Autonomous Response** — "R&D. Closing the loop with in-hive interventions."
- Timeline bar: gold fill through current stage, muted line for future stages. Small status pills per stage: `SHIPPING` / `IN DEVELOPMENT` / `R&D`.
- Taken directly from deck slide 5.

### 9. Founders (`#founders`)

The most story-shaped section on the page. Long-form, two narrative columns of text flanked by photos. Designed to feel like a magazine feature, not a team card.

Cream-soft background band, generous vertical padding (140px+ desktop). Max content width 880px, narrower than the rest of the homepage to feel intimate and editorial.

**Layout:**
- Eyebrow at top (centered): `WHO'S BUILDING THIS`.
- Title (centered, serif italic accent on one phrase): **"Robert and Danny have been building this story for <em>seventeen years</em>."**
- Below the title, two photos side by side with thin line dividers (no shadows, no rounded circles): `robert.png` and `daniel.png`. Captions underneath: `Robert Schulte · Co-founder, CEO` and `Daniel Drew · Co-founder, CTO`.
- Then the story, set as flowing prose in a single column. ~350–450 words total. Inter 18px, line-height 1.7, drop-cap on the first paragraph (gold-dark, Instrument Serif italic).

**Story copy (draft, narrative voice — lock before build):**

> Robert started keeping bees when he was nine. By high school he had a half-dozen hives in his parents' backyard in Florida, and by the time he finished an engineering degree at UF, he had over a decade of seasons behind him — losing colonies the way every beekeeper loses colonies, watching mites arrive, watching queens fail, watching a treatment work one year and stop working the next.
>
> The summer before starting business school, he packed his car and spent three months on the road. He drove from Florida to Vermont to Montana to California, sleeping in the back seat most nights, sitting down with commercial beekeepers in their yards and warehouses and pickup trucks. Fifty-some interviews. He kept hearing the same things. *Mites are spreading faster than we can inspect.* *Africanized bees are taking over yards in weeks.* *I've got 10,000 colonies and 10 employees and we can't keep up.*
>
> One conversation, with a commercial operator outside Ventura, California, turned into the question Robert hasn't been able to put down since: **what if every hive could tell you when something's wrong, before you lose it?** Not after the next inspection. Not after the next yard visit. The same day.
>
> Danny is the answer to *how*. Robert and Danny have been friends since UF — nine years of building things together, from undergraduate projects to side hardware experiments. Danny went on to build spacecraft at Blue Origin and now leads satellite delivery at Apex Space in Los Angeles. He knows how to make hardware survive in places where you can't fix it later, which turns out to be exactly the problem with a bee box that has to live in a remote yard for a year on solar power.
>
> They started PollenPal at the kitchen table. They're building it the same way Robert learned to keep bees — by listening to the people who actually do the work, and refusing to ship anything that doesn't pull its weight in the field.

- Closing line, centered, smaller, muted: "Built with guidance from 4 Master Beekeepers and a research team at Columbia University."
- No CTA in this section; it flows directly into the testimonial band, which is the emotional handoff to the pilot CTA.

**Asset note:** the spec assumes individual headshots `robert.png` and `daniel.png` exist or will be sourced. If only `robert_and_danny.png` is available, fall back to that single image at full width above the prose, with the captions removed.

### 10. Testimonial band (`#testimonial`)

Full-bleed, photographic background (`wendy-ventura.jpg`) with dark overlay (65% black).
- Centered pullquote in white: *"Identifying and treating Africanization early would be worth $100k a year to our operation."*
- Attribution: `Wendy · Blue Ridge Honey Co. · Ventura, CA` (amber accent).
- One section only. Single quote. The deck's "Wendy slide" visual reference.

### 11. Pilot CTA (`#pilot`)

Dark `--ink` background section.
- Centered column, max 640px wide.
- Eyebrow (gold): `RUN A PILOT`.
- Title (white): "Deploy PollenPal on your yard."
- Sub: "We're running pilots with commercial operators in 2026. Tell us about your operation and we'll be in touch within 2 business days."
- Form (white card):
  - Name*, Email*, Company / operation*, Hive count, Region, Notes (textarea).
  - Submit: "Request a pilot →" (gold-filled button on white bg).
  - Reuses existing Google Form action URL and `entry.*` field names — no new backend.
- After-submit state: replace form with success message "We'll be in touch within 2 business days."

### 12. Footer

Dark `--ink` background, but lighter treatment than current site.
- Logo + tagline: "Physical AI for commercial apiaries and farms."
- Three columns of links:
  - **Product**: How it works, Pilots, Roadmap
  - **Company**: Founders, Investors (`/investors`), Hobbyist waitlist (`/hobbyist`), Press
  - **Contact**: hello@pollenpal.com
- Bottom strip: `© 2026 PollenPal Inc.` and `Confidential & Proprietary` removed (that belongs on the deck, not the website).

---

## `/investors` — condensed deck flow

Inherits the same visual system. Different section order and copy density — more dense, more numbers, less emotional framing.

**Sections:**
1. **Header** (same as homepage; current page highlighted in nav).
2. **Hero** — "Empowering beekeeping through physical AI for commercial apiaries and farms." Single CTA: "Get in touch". No floating stat cards; cleaner frame.
3. **The problem** — deck slide 2 verbatim framing. Food-system stakes. 40%+ losses. $2.5B+ global replacement cost.
4. **The solution** — deck slide 3 3-step. Hardware → ML → alerts.
5. **Financial impact** — deck slide 4 table with "data moat" callout beneath.
6. **Traction & milestones** — same 6-stat strip as homepage, expanded with any investor-only metrics (commitments, MoUs, LOIs) if shareable.
7. **Competitive positioning** — deck slide 9 quadrant. Custom SVG: X-axis "Difficult → Easy to deploy", Y-axis "Basic → Actionable insights". PollenPal in top-right quadrant. Manual inspection, Beewise, Solutionbee, Broodminder plotted. Use deck slide 9 as reference for placement.
8. **Market opportunity** — deck slide 10. TAM/SAM/SOM as three stacked circles, matching deck's `$107B TAM / $24B SAM / $128M SOM`. Same cream/gold fills as deck.
9. **Partnerships** — deck slide 11 two-channel framing: Corporate Managed Beekeeping + Honey & Pollinator Brands. Short paragraphs, no card grid mess.
10. **Roadmap** — same as homepage.
11. **Team** — Robert + Danny + support teams (Columbia research scientist, 4 Columbia Build Lab students, 4 Master Beekeepers).
12. **Investor contact** — dark CTA section. Form reuses Google Form endpoint. Copy: "Interested in learning more? We'd love to hear from you."
13. **Footer** — same.

**Cut from deck to web:**
- Slide 1 title slide (replaced by hero).
- Slide 7 closing slide (replaced by CTA).
- Slide 12 "Meet Wendy" (web version uses the testimonial band on homepage only; no dedicated customer slide on investor page).
- Slide 13/14 hardware deep-dive (linked from investor page to homepage product section; no duplication).

---

## `/hobbyist` — tight one-pager

Single-focus page for backyard beekeepers who found the site via press, word of mouth, or a beekeeper association.

**Sections:**
1. **Header** (same).
2. **Hero** — "Your 5 hives deserve more than annual inspections." Sub: "PollenPal's backyard version plugs into your home WiFi and power. Get alerts the moment something's wrong, and talk to a real beekeeper when you need one." CTA: "Join the waitlist".
3. **How it's different from commercial** — short 3-bullet list: WiFi + power setup, AI assistant with photo diagnosis, optional live beekeeper chat, live hive streaming.
4. **Impact** — the 5-hive table from the current site (hive loss, honey value, value added).
5. **Testimonial** — Karen quote: "For my first 4 years, I spent $600 on lost hives, and I didn't know why I was losing them."
6. **Waitlist form** — reuses Google Form endpoint. Name, email, hives, notes.
7. **Footer** (same).

---

## Responsiveness

Breakpoints:
- `≥ 1200px` — full layout, 1240px max wrap.
- `960–1199px` — same grid, slightly tighter gutters.
- `720–959px` — hero collapses to single column (visual first), section grids collapse to single column, floating stat cards hidden, nav collapses to hamburger.
- `< 720px` — same as above; padding reduced; button widths full-bleed inside container.

No separate mobile design. Same sections, same copy, same order on every breakpoint.

## Accessibility

- All images have alt text scoped to their narrative purpose (device, ML viz, founders, etc.).
- Color contrast: ink on white and ink on cream both pass WCAG AA. Gold on white fails AA for body text — so gold is reserved for accents, eyebrows, and large display headings, never for paragraph text.
- Video: `autoplay muted loop playsinline` on hero. Poster fallback. Prefers-reduced-motion disables autoplay and shows the poster image instead.
- Forms: labels associated with inputs, required fields marked, submit button has keyboard focus ring.
- Semantic HTML: `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`. Section headings in order.
- Skip-to-content link at top.

## Performance

- Hero video re-encoded to H.264/AAC MP4, ~800KB–1.5MB. Poster image as preloadable `<img>` fallback.
- All deck images re-exported at web-optimized sizes (max 1600px wide, JPEG/WebP where lossy is fine, PNG for UI elements).
- Single CSS file, inlined critical CSS for the hero in `<style>` block.
- No JS framework. One small `scripts.js` for mobile nav toggle and form submission handler. Defer-loaded.
- Google Fonts loaded with `display=swap`; preconnect hints in `<head>`.
- Target: Lighthouse ≥ 90 on mobile and desktop.

## Copy decisions made (call-outs)

1. **Hero headline:** "Inspect every hive. Every day." with italic "Every". Locked.
2. **Positioning line:** "Physical AI for commercial apiaries and farms." Matches deck, used as footer tagline and homepage eyebrow.
3. **Cut from current site (homepage):**
   - The "For Beekeepers / For Investors" top-level tabs.
   - The "Commercial / Hobbyist" sub-tabs.
   - The ecosystem value grid (Farmers / Pollination Brokers / State & Local Govts) — moves to investor page or cut entirely.
   - The "Adjacent Markets" (OrchardPal / AlmondPal / PescaPal) section — investor-only, and even there, demoted to a single paragraph.
   - The "Confidential & Proprietary" footer line.
4. **Cut from earlier draft of this spec:**
   - **Product deep-dive section** (Hardware / ML / Web app subsections) — felt too dense for a marketing homepage. Hardware and ML detail moves to `/investors`. Product feature highlights are absorbed into the new "Why PollenPal" section.
   - **Financial impact margin table** — too dense for the homepage's tone, and beekeepers will read it as "you're going to do my P&L for me." The table still lives on `/investors`, where the audience expects it.
5. **Added from deck:**
   - "Physical AI" language throughout.
   - Roadmap section (Detect / Recommend / Respond).
   - Data moat callout ("collecting data unobtainable any other way") — now lives in the "Why PollenPal" section.
   - Wendy testimonial as a dedicated band.
   - Precision ag IoT framing on investor page.
6. **New on homepage:**
   - **"Why PollenPal" section** (section 6) — a competitive-advantage section anchored on deck slide 9's positioning. Three differentiator cards: continuous per-hive monitoring, sub-$100 drop-in hardware, compounding data moat.
   - **Long-form Founders section** (section 9) — rewritten as a magazine-style narrative, ~350–450 words, drop cap, narrower column. Robert's story leads, Danny enters as the *how*.

## Open questions (to resolve before implementation)

1. **Hero video encoding target** — final file size budget. Soft cap 1.5MB, hard cap 2.5MB.
2. **"How it works" section title** — "From bee to alert in minutes." is a placeholder. Final copy pass before build.
3. **"Why PollenPal" section title** — "Built for commercial scale, not science fairs." is a draft; OK or needs reworking?
4. **Founder story prose** — the ~400-word draft in section 9 is a first pass. Robert should review and rewrite in his own voice before build, especially the Ventura-conversation paragraph (is that a real conversation we can attribute, or should it be more general?).
5. **Founder headshots** — do `robert.png` and `daniel.png` exist as individual headshots, or should we ship with the existing combined `robert_and_danny.png`?
6. **Press / logo bar content** — is "Backed by Columbia Business School · Big Idea Winners · 4 Master Beekeepers" final, or do we swap in press mentions / accelerator logos if available?
7. **Stat card floating animation** — static is simpler. Want subtle entrance animation on scroll, or skip?
8. **Hobbyist page priority** — build simultaneously, or ship homepage + investors first and `/hobbyist` as a fast-follow?

---

## Out of scope, explicitly

- Building a blog or press page.
- Dashboard or product screenshots beyond what's already available (`dashboard-web.png`, `dashboard-phone.png` from current site, `phone.png` from deck).
- Migration to a CMS or headless framework.
- Payment, e-commerce, or self-serve onboarding flows.
- Any change to `app.pollenpal.com` — that's a separate product, and the marketing site only links to it.

---

## Review checkpoint

Per user request: **do not commit anything to git until this spec is reviewed and approved.** After approval, next step is to invoke the `writing-plans` skill to break this design into a concrete implementation plan.
