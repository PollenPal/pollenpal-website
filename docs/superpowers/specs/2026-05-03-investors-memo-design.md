# Investors Memo (`/investors`) Long-Form — Design Spec

**Author:** Robert Schulte
**Date:** 2026-05-03
**Course context:** Launch Your Startup (LYS), Final Project. Graded against rubric in `LYS - Final Project.pdf`.
**Status:** Approved for implementation planning.

---

## 1. Goal

Replace the existing `/investors` page (currently a condensed deck-style flow) with a long-form, web-native investment memo that reads like a real VC partner memo to seed investors. The memo must:

- Be self-contained — a reader who never sees the deck must understand what PollenPal does, why it matters, and how it wins.
- Hit every required section in the LYS rubric and the user-supplied 13-section spec.
- Read at YC / a16z company-page density: ~1,500–2,000 words, scannable, leans on tables, charts, and callouts.
- Cite every quantitative claim with either a verifiable external source or a named internal assumption.
- Match the existing site's restrained, premium visual identity. No gradients, no glassmorphism, no "transforming the future" copy.

## 2. Scope

- **In scope:** Full rewrite of `/investors.html`. New CSS components added to `styles.css`. New JS for TOC active-state handling in `scripts.js`. New inline-SVG charts for revenue ramp and gross margin. Reuse of existing inline-SVG quadrant and TAM/SAM/SOM rings.
- **Out of scope:** Backend changes, form changes (existing Google Form action reused), homepage edits, hobbyist page edits, deck file changes.

## 3. Page architecture

```
+--------------------------------------------------------------+
| Site header (existing, slim)  [Home] [How] [Why] [Investors] |
+--------------------------------------------------------------+
| Confidential banner (thin, dark, gold dot)                   |
+--------------------------------------------------------------+
|                  |                                            |
|  TOC RAIL        |  HERO + EXEC SUMMARY                       |
|  (sticky, 280px) |  (full content column, max 920px wide)     |
|  01 Summary      |                                            |
|  02 Problem      |  SECTION 02 — PROBLEM                      |
|  ...             |  ...                                       |
|  13 Appendix     |  SECTION 13 — APPENDIX                     |
+--------------------------------------------------------------+
| Footer: Confidential & Proprietary | © 2026 PollenPal Inc.   |
+--------------------------------------------------------------+
```

- Outer wrap: 1240px max, 32px gutter (existing).
- Content column: 920px max when TOC is sticky on desktop. Drops to full-width on mobile.
- TOC: 280px wide, sticks at `top: 88px` (under header + banner). Highlights active section via `IntersectionObserver`. Subtle vertical gold-dark progress bar fills as user scrolls.
- TOC collapses to a top dropdown ("Jump to section ▾") below 1100px viewport. Below 600px, dropdown only.
- Confidential banner directly under header: thin `--ink` strip, one line in tracked uppercase: `CONFIDENTIAL & PROPRIETARY · SUBJECT TO NDA · © 2026 POLLENPAL INC.` with a small gold dot before the first phrase.
- Site header `Investors` link gets the `current` state (already does this in current investors.html — preserve).

## 4. Section-by-section content plan

Word budget totals ~1,800 words across 13 sections. Each section opens with an eyebrow numeral (`[01]` style, gold-dark, tracked) and a one-sentence thesis (`.thesis-lead` component) before body content.

### §1 Executive Summary (~200 words)

**Thesis:** "PollenPal is physical AI for commercial beekeeping — hardware and ML that watches every bee, catches threats the day they appear, and sells through a $4–20/hive/mo subscription with hardware bundled."

**Beats:**
- What we do (sensor + CV on every hive entrance; alerts; recordkeeping)
- Problem (40%+ annual loss; commercial 62% in 2024-25 season)
- Why now (data + sub-$100 BOM make continuous monitoring viable for the first time)
- Status: 3 commercial pilots committed; 250k+ training images; 50+ beekeeper interviews; $55K non-dilutive secured
- Team: Robert (17yr beekeeper, Columbia MBA) + Daniel (Apex Space, ex-Blue Origin)
- Ask: $500K pre-seed SAFE

**Visual:** 4 stat callouts — `250k+ images`, `3 pilots committed`, `50+ interviews`, `$500K SAFE`.

**Cross-links:** stats link to §9; ask links to §12.

### §2 Problem / Opportunity (~150 words)

**Thesis:** "U.S. beekeepers lose 40%+ of colonies each year while food demand rises — and the aging workforce can't scale to inspect every hive."

**Beats:**
- 40%+ annual loss (Bee Informed Partnership, multi-year average)
- 62% commercial loss in 2024-25 season (USDA / Auburn / Honey Bee Health Coalition) — newer, more striking
- $600M U.S. revenue lost in 2024-25 season (USDA via Honey Bee Health Coalition)
- 35% of food production relies on pollinators (FAO / Klein et al. 2007)
- Aging workforce — average commercial beekeeper over 60 (industry surveys)
- Old way: 2-3 week manual inspection → damage already done. New way: continuous monitoring → day-of-detection.
- Validation: 50+ beekeeper interviews (summer 2025, cross-country).

**Visual:**
- Pull quote: Kristen, Master Beekeeper — "How the f**k can you get through 10,000 hives with 10 employees?" (`.pull-quote` component, Instrument Serif italic)
- 2 stat callouts: `40%+ annual loss`, `$600M lost in 2024-25`

### §3 Solution / Product (~180 words)

**Thesis:** "We put computer vision on every hive entrance and surface threats the day they appear, instead of weeks later during inspection."

**Beats:**
- Hardware: off-the-shelf IoT compute, sub-$100 BOM target, 3D-printed skeleton, fits standard 10-frame Langstroth, solar+LTE for remote yards. No custom hive bodies.
- ML: YOLO trained on 250k+ field images; tracks colony activity in real time; flags varroa mites, africanization markers, missing-queen indicators. Cloud inference today, on-prem GPU on roadmap (80% cost cut, <1s latency target).
- Web app: hive-level alerts, multi-yard views, harvest logging. Designed with beekeeper input — actionable insights over complex graphs.
- Differentiation: continuous monitoring (vs. 3-week manual cadence); standard-hive compatibility (vs. Beewise's custom hive); affordable per-hive cost (vs. labor-intensive inspection).

**Visual:** 3-step image strip — `device-grass.jpg` / `ml-detection.jpg` / `dashboard-phone.jpg` (existing assets).

**Cross-links:** "data flywheel" → §6 (competitive advantage). On-prem GPU → §12 (use of funds).

### §4 Business Model (~220 words)

**Thesis:** "Subscription with hardware bundled, $4–20/hive/mo across three channels — gross margin scales from 44% to 71% as device BOM falls $46 → $18."

**Beats:**
- Three pricing tiers (see Table 1).
- Hardware bundled into subscription removes upfront adoption barrier (most operators in interviews cited capex as #1 friction).
- Pricing grows with feature maturity: detection (now) → recommendations (next) → automation (later).
- $160M short-term U.S. TAM at scale ($137M commercial + $19M hobbyist + $4M partnership).

**The four fits — explicitly named:**

- **Product / Market.** Hardware + ML solves the inspection-cadence gap commercial operators raised in customer-discovery interviews. Continuous monitoring replaces 2-3 week manual inspection.
- **Market / Channel.** Commercial: direct sales to ~1,600 concentrated U.S. operators. Hobbyist: self-serve via paid social + content. Partnership: B2B2C through corporate beekeeping platforms (Best Bees, Alvéole — 24+ U.S. cities combined).
- **Channel / Model.** Direct sales matches $72K Yr-1 ACV economics for commercial. Self-serve matches $480 ACV for hobbyist. Rev-share (25%) matches partnership platform economics.
- **Model / Market.** Subscription compounds ARR; hardware bundling removes the adoption barrier in a market where digital tooling penetration is low; hardware costs amortize across multi-year subscriptions.

**Visual:** Pricing tiers table (Table 1).

**Cross-links:** GM trajectory → §8. SOM math → §5.

### §5 Market Opportunity (~150 words)

**Thesis:** "TAM $106B crop protection; SAM $24B precision farming; SOM $128M U.S. hive management — bottom-up from 1,600 commercial operators × 1,500 hives × ARPU."

**Beats:**
- **TAM $106B** — global crop protection (chemicals + precision-tech alternatives) by 2030. PollenPal's long-term ceiling: AI-enabled monitoring and IPM that reduces or replaces chemical application. (MarketsandMarkets 2025-2030.)
- **SAM $24B** — precision farming market by 2030. PollenPal's near-term expansion: pollination verification, monitoring, precision intervention across orchards/vineyards/greenhouses. (Grand View Research 2024.)
- **SOM $128M** — U.S. hive management. Bottom-up: 1,600 commercial operators × 1,500 hives × ~$96/hive/yr ARPU × ~50% adoption haircut. (USDA NASS 2024 + PollenPal analysis.)
- **Short-term capturable U.S. TAM ~$160M:** $137M commercial + $19M hobbyist + $4M partnership.

**Visual:** TAM/SAM/SOM 3-circle SVG (reuse existing `investors.html` lines 202-225 — verify $106B label, no other changes needed).

### §6 Competition (~150 words)

**Thesis:** "Existing tools force a tradeoff between accuracy and deployability — PollenPal is the first to be both, with a data flywheel that compounds with every bee we see."

**Beats:**
- **Manual inspection:** accurate, unscalable, 2-3 week cadence; threats already established by detection.
- **BroodMinder ($50-200/yr):** weight + temperature only; no behavioral signal; missed threats.
- **Solution Bee:** acoustic monitoring; basic, non-actionable.
- **Beewise (~$thousands/colony):** full automation but proprietary hive bodies, doesn't fit standard Langstroth, prohibitive for existing operators.
- **PollenPal:** continuous CV monitoring + standard-hive compatibility + sub-$100 BOM.
- **Unfair advantages:** (1) data flywheel — every bee labeled improves the model; competitors don't have visual datasets at this scale; (2) founder–operator fit — Robert is a 17-year beekeeper, not a generalist hardware founder.

**Visual:** 2x2 quadrant SVG (reuse existing `investors.html` lines 175-192 — no changes).

**Cross-links:** crop expansion → §7 (Scale phase).

### §7 Strategic Roadmap (~220 words)

**Thesis:** "Three phases — **Search** (now: threat detection in commercial pilots), **Systematize** (next: recommendations + corporate beekeeping channel), **Scale** (later: autonomous response and crop expansion)."

**Beats:** see Table 3. Each phase has product milestone / GTM motion / unit economics / KPI / inflection point.

**Inflection points highlighted in body prose:**
- End of Search: 5,000 HUM → first paid commercial deployment confirms ARPU.
- End of Systematize: $1M ARR → unlocks seed-stage pricing/valuation conversation.
- End of Scale: profitability (EBIT+) by 2029, $4.6M revenue and 41% EBIT margin by 2030.

**Visual:** 3-column phase table (Table 3) + extension of deck slide 5 timeline.

### §8 Financial Overview (~200 words)

**Thesis:** "$40K → $4.6M revenue 2026–2030; EBIT margin –201% → +41%; supported by HW BOM falling $46 → $18 and ARPU rising as feature stack matures."

**Beats:**
- 5-year P&L summary (Table 2).
- Key assumptions, named explicitly:
  - Commercial farm cohort: 16 / 22 / 28 / 34 / 40 by year (cumulative)
  - 1,500 hives per commercial farm (industry standard)
  - 0.7%/mo churn (best-in-class B2B SaaS benchmark; flagged as optimistic for hobbyist pending pilot data)
  - 15% Yr-1 ramp rising to 100% by Yr-4
  - ARPU $4 → $6 commercial, $8 → $12 hobbyist over 5 years (feature-tier pricing)
  - HW BOM $46 → $18 (supplier quotes at 700 → 10,000-unit scale; PollenPal analysis)
- CAC / payback narrative: high initial CAC for direct commercial sales offset by $72K ACV; partnership rev-share bypasses CAC entirely; hobbyist self-serve targets <12-month payback.

**Visuals:**
- Chart 1: Revenue ramp (vertical bar, 2026-2030).
- Chart 2: Gross margin trajectory (line) + HW cost overlay (bars).
- Table 2: 5-year P&L.

### §9 Traction & Milestones (~150 words)

**Thesis:** "MVP deployed, 250k+ training images, 3 pilots committed, 50+ beekeeper interviews, $55K non-dilutive secured — moving from data collection to revenue in 2026."

**Beats — to date:**
- 50+ beekeeper interviews (summer 2025 cross-country)
- 12 hardware design iterations
- MVP deployed in South Florida pilot
- 250k+ field images captured for training
- 3 commercial pilots committed (CT, NY, CA)
- 14 hobbyists on waitlist
- $55K non-dilutive grants secured (Columbia + others)
- 4 Master Beekeeper advisors

**Beats — next 12 months:**
- Q2 2026: production hardware ready (~700 devices, IP67 enclosure, FCC cert)
- Q3 2026: first paid commercial deployment
- Q4 2026: first partnership pilot (Best Bees or Alvéole)
- Q1 2027: corporate beekeeping platform launch

**Visual:** Timeline (extends deck slide 5 timeline forward to Q1 2027).

### §10 Challenges & Risks (~200 words)

**Thesis:** "Four candid risks — model accuracy at scale, hardware reliability in the field, regulatory shifts on treatments, channel concentration on partnerships — each with a specific mitigation."

**Risks:**

| Risk | Description | Mitigation |
|---|---|---|
| **Technical** | Model accuracy at scale: flagging ≠ ground-truth; field conditions vary across yards. | Active labeling pipeline (CVAT); calibration ridge regression tied to inspection logs. Active calibration model in development on `feat/calibration-model` branch. |
| **Hardware** | Outdoor IoT in hives is brutal (dust, propolis, moisture, temperature swings). | 12 design iterations completed; $240K of pre-seed funds explicitly allocated to IP67 enclosure + FCC cert (see §12); 5% annual failure rate baked into model. |
| **Regulatory** | EPA varroa treatment registration shifts (e.g., oxalic acid changes) could disrupt customer treatment protocols. | Treatment-agnostic alerting — we surface threats, customer chooses treatment. Partnership rev-share model doesn't expose us to chemical-application liability. |
| **Market / Channel** | ~1,600 U.S. commercial operators is a small TAM if we stay in hive management only. | Roadmap §7 explicitly extends into precision farming SAM ($24B) — not blue-sky, on calendar. Partnership channel reduces dependence on direct-sales motion. |

**Visual:** 4 risk callout pairs (TECHNICAL / HARDWARE / REGULATORY / MARKET), each with risk + mitigation paragraph.

**Cross-links:** Hardware mitigation → §12 (HW use of funds). Market mitigation → §7 (Scale phase).

### §11 Team (~130 words)

**Thesis:** "Founder–market fit: 17-year beekeeper + Apex Space hardware engineer with a 9-year working partnership, backed by Columbia Build Lab and 4 Master Beekeeper advisors."

**Members:**
- **Robert Schulte** — Co-founder, CEO. Ex-BCG, Columbia MBA, UF Industrial & Systems Engineering. 17 years beekeeping. Led 50-interview customer discovery cross-country, summer 2025.
- **Daniel Drew** — Co-founder, CTO. Spacecraft Manufacturing Engineer at Apex Space. Ex-Blue Origin. UF engineering. 9-year working partnership with Robert.
- **Tech team** — 1 Columbia Research Scientist (computer vision; backed by Google + NVIDIA). 4 Columbia engineers building ML pipeline + web app via Columbia Build Lab.
- **Beekeeping advisory** — 4 Master Beekeeper advisors providing hive-management and treatment-protocol guidance. Commercial beekeeper partners deploying devices and contributing field data.

**Visual:** 4 team cards (existing markup; refresh copy).

### §12 Ask / Next Steps (~180 words)

**Thesis:** "Raising $500K pre-seed SAFE to fund production hardware, on-prem GPU inference, and first commercial deployments through 2026."

**Beats:**
- $500K pre-seed SAFE (terms TBD, market-rate post-money cap).
- $55K non-dilutive already secured (Columbia + others).
- 18-month runway to mid-2027.
- Bridge to seed round after first $250K ARR signal.

**Use of funds:** see Table 4. Five buckets totaling $500K, each tied to a measurable outcome.

**Next steps process:**
1. Express interest via the form below or [hello@pollenpal.com](mailto:hello@pollenpal.com).
2. Intro call (30 min) — walk through the deck and live deployment data.
3. Diligence packet — financial model, technical architecture, customer interviews.
4. SAFE.

**Visual:** Use of funds table (Table 4) + 4-step "how to engage" strip.

**Cross-links:** HW spend → §10 hardware mitigation. GPU spend → §3 on-prem note.

### §13 Appendix (~250 words across 4 collapsibles)

**Thesis:** "Optional deep-dives — customer story, unit economics, hardware/ML detail, primary research methodology."

Each subsection in `<details>` element, closed by default, opens with a `▸ Expand` affordance.

- **A. Customer story — Wendy, Ventura, CA (~80 words).** 5,000-colony commercial operator. Africanization is a $100K/year line item — mites and queen issues compound on top. Quoted in the v4 deck and current homepage testimonial band: "Identifying and treating Africanization early would be worth $100K a year to our operation."
- **B. Unit economics deep dive (~80 words).** Per-hive contribution margin walk: $4/mo × 12 = $48 ARPU Yr 1 (rising to $72 by Yr 5). Per-hive cloud cost $1.50/mo declining to $0.75/mo. Per-hive HW amortized: $46 BOM ÷ 3-yr life = $15.33/yr ÷ 3 hives per device (0.33 devices/hive in commercial deployment) = $5.11/yr HW per hive. Implied Yr-1 contribution margin ~$25/hive after cloud, support, and amortized HW. LTV/CAC and payback period to be confirmed once first paid deployment lands.
- **C. Hardware / ML detail (~50 words).** Pi-class compute, MLX90640 thermal sensor, camera, sound sensor, external switches. 3D-printed skeleton, 12 design variations tested. YOLO11 architecture; 250k images annotated via CVAT pipeline. Calibration ridge regression maps detection signals to inspection ground truth.
- **D. Primary research methodology (~40 words).** 50+ semi-structured interviews, summer 2025. Cross-country road trip + phone calls. Sample selection: commercial operators with 500+ hives across CA, TX, FL, CO, NY. 4 Master Beekeepers retained as ongoing advisors.

## 5. Visual system additions

All additions reuse existing tokens in `styles.css`. No new colors, no new fonts.

### New CSS components (8)

| Component | Purpose |
|---|---|
| `.toc-rail` | Left sticky TOC with active-section highlight + scroll progress bar |
| `.conf-banner` | Thin dark strip under header; `--ink` background, gold dot accent |
| `.thesis-lead` | Section opener; 3px gold-dark left border, Inter 600, 19px, 1.4 line-height |
| `.stat-callout` | Big number + label; 1px line border, `--line`, 8px radius, 24px pad |
| `.pull-quote` | Instrument Serif italic, oversized opening quote glyph, gold-dark rule below |
| `.memo-table` | Refined table: 1px line borders, generous padding, `tabular-nums` for figures |
| `.chart-frame` | Wrapper for inline-SVG charts; thin border, caption below |
| `.footnote-list` | Per-section endnote block; Inter 400 italic, 13px, `--muted` |

### Section-opener pattern

```html
<section id="executive-summary">
  <div class="eyebrow">[01] · EXECUTIVE SUMMARY</div>
  <p class="thesis-lead">PollenPal is physical AI for commercial beekeeping...</p>
  <div class="memo-body">
    <p>Body paragraphs follow at 17px, 1.6 line-height...</p>
  </div>
  <ol class="footnote-list">
    <li id="fn-1-1">¹ Source: ... <a href="#fnref-1-1">↩</a></li>
  </ol>
</section>
```

### TOC rail behavior

- Width 280px, sticks at `top: 88px` (under header + banner).
- Each entry: `[01]` numeral (Inter 600, gold-dark, tabular figures) + section title (Inter 500, 14px).
- Active state: 3px gold-dark left border on the entry; text shifts to ink-bold.
- Hover state: `--muted` text → `--ink-soft`.
- Progress bar: 1px-wide vertical gold-dark bar on the left edge of the rail; fills from top as user scrolls (CSS `transform: scaleY()` bound to scroll position via `scripts.js`).
- Mobile (<1100px): collapses into a sticky top "Jump to section ▾" dropdown bar.

### Stat callout pattern

```
┌──────────────────┐
│   40%+           │  ← Inter 800, 36px, --ink
│   ─              │  ← --gold-dark underline, 32px
│   annual hive    │  ← Inter 500, 13px, --muted
│   loss in US     │
└──────────────────┘
```

Used in §1 (4 callouts), §2 (2 callouts), §9 (numerical recap).

### Risk callout pattern (§10)

Each risk pair: a `.risk-tag` chip (uppercase, Inter 700, white on `--ink`) tops the risk callout. The mitigation block sits in `--cream-soft` background to differentiate. Two-up grid on desktop, stacked on mobile.

### Print / PDF styles

`@media print` rules:
- TOC rail hidden.
- Confidential banner becomes running header on every page.
- Footer shows page numbers + `© 2026 PollenPal Inc.`
- Charts render at 90% scale, inline below their text reference (not floated).
- Anchor links underlined in print (color cues lost in B&W).
- `break-before: page` on each `<section>`.

## 6. Citation system

**Numbering: per-section, resets each section** (¹²³…). Each section is a self-contained citation island so a YC-style scanning reader can drop in mid-document.

**Inline marker:** `<sup class="fn-ref"><a href="#fn-2-1" id="fnref-2-1">¹</a></sup>` — superscript, gold-dark, 11px.

**Endnote block:** `.footnote-list` at end of each section. Each entry: number + source name + truncated URL + `↩` back-link to the inline marker.

**Three citation entry templates:**

| Type | Format |
|---|---|
| External published | `¹ Bee Informed Partnership, Annual Colony Loss Survey 2023–24. beeinformed.org/results-categories/honey-bee-colony-losses ↩` |
| Internal primary | `² Customer interviews, summer 2025. n=50+ commercial and hobbyist beekeepers across CA, TX, FL, CO, NY ↩` |
| Derived figure | `³ PollenPal analysis. SOM = 1,600 commercial operators × 1,500 hives × $96/hive/yr × ~50% adoption haircut. Source: USDA NASS Honey Report 2024 ↩` |

**Cross-link styling (distinct from footnotes):**
- HTML: `<a href="#financials" class="xref">§8 Financials</a>`
- CSS: `--gold-dark` color, dotted 1px gold-dark underline at 30% opacity. Hover: solid underline, full opacity.
- External links get a small `↗` glyph appended.

## 7. Source inventory (resolved)

All citations the memo will use, with verified sources. **No `{{NEEDS SOURCE}}` placeholders remain.**

| Claim | Source | URL |
|---|---|---|
| 40%+ annual hive loss (multi-year U.S. avg) | Bee Informed Partnership Annual Colony Loss Survey | https://beeinformed.org/results-categories/honey-bee-colony-losses |
| 62% commercial loss in 2024-25 season | Honey Bee Health Coalition / Auburn / USDA | https://honeybeehealthcoalition.org/new-data-confirm-catastrophic-honey-bee-colony-losses-underscoring-urgent-need-for-action/ |
| $600M U.S. revenue lost in 2024-25 season | USDA via Honey Bee Health Coalition (1.7M colonies × $200/colony + lost honey + lost pollination income) | https://honeybeehealthcoalition.org/new-data-confirm-catastrophic-honey-bee-colony-losses-underscoring-urgent-need-for-action/ |
| 35% of food production relies on pollinators | FAO / Klein et al. 2007 *Importance of pollinators in changing landscapes for world crops* | https://royalsocietypublishing.org/doi/10.1098/rspb.2006.3721 |
| 60% increase in agricultural production by 2050 | UN FAO World Agriculture Towards 2050 | https://www.fao.org/3/i6583e/i6583e.pdf |
| Average commercial beekeeper over 60 | Apiary Inspectors of America 2024-25 survey + agricultural marketing resource center | https://apiaryinspectors.org/US-beekeeping-survey-24-25 |
| ~1,600 U.S. commercial beekeepers | USDA NASS Honey Report 2024 | https://www.nass.usda.gov/Statistics_by_State/Florida/Publications/Livestock_Releases/Bee_and_Honey/2024/index.php |
| **TAM $106B crop protection 2030** | MarketsandMarkets, Crop Protection Chemicals 2025-2030 | https://www.marketsandmarkets.com/Market-Reports/crop-protection-380.html |
| **SAM $24B precision farming 2030** | Grand View Research, Precision Farming Market | https://www.grandviewresearch.com/industry-analysis/precision-farming-market |
| **SOM $128M U.S. hive management** | PollenPal analysis (1,600 × 1,500 × $96/yr × ~50% adoption haircut). Underlying market data: USDA NASS Honey Report 2024. | (derived) |
| 5-year P&L numbers | PollenPal Business Model v8 (`C:\projects\PollenPal Business Model\PollenPal Business Model v8.xlsx`) | (internal) |
| Pricing tiers | PollenPal Business Model v8 + v5 deck | (internal) |
| HW BOM $46 → $18 | PollenPal analysis (supplier quotes at 700 → 10,000-unit scale) | (internal) |
| 0.7%/mo churn | Company assumption — best-in-class B2B SaaS benchmark per Churnfree 2026 | https://churnfree.com/blog/b2b-saas-churn-rate-benchmarks/ |
| 250k+ training images, 12 HW iterations, 50+ interviews, 14 hobbyist waitlist, $55K non-dilutive | Internal | (internal) |
| Wendy quote ($100K/yr Africanization value) | Customer interview, Blue Ridge Honey Co. | (internal) |
| Kristen quote ("how the f**k...") | Customer interview, Master Beekeeper, 20yr experience | (internal) |
| BroodMinder pricing $50-200/yr | Public pricing | https://broodminder.com |
| Beewise architecture | Public marketing material | https://www.beewise.ag |

### Explicit unsupported gaps (called out per user instruction)

The following claims appear in earlier site/deck materials but **will be omitted from the memo** because no defensible source was found:

- ❌ "Median commercial beekeeper age 66" — no NASS or peer-reviewed source. Replaced with "average commercial beekeeper over 60."
- ❌ "79% of commercial beekeepers use no digital tools" — no supporting source found. Dropped entirely per Robert's call.
- ❌ "$2.5B+ global hive replacement cost" — no defensible global figure. Replaced with "$600M U.S. revenue lost in 2024-25 season" (more specific, more recent, more striking).
- ❌ "$107B precision agriculture IoT TAM" — actual ag-IoT market is ~$13–55B by 2030. The $107B figure aligns with crop protection chemicals, not IoT. **TAM relabeled** to "Crop protection" with the same $106B headline number, properly cited.

These gaps are flagged in the spec deliberately so reviewers understand what was removed and why.

## 8. Charts (3 total)

### Chart 1 — Revenue ramp 2026-2030 (§8)

- Type: vertical bar, inline SVG, 100% wrapper width × 280px tall
- Data: `2026 $40K | 2027 $172K | 2028 $653K | 2029 $1,947K | 2030 $4,648K`
- Bars filled `--gold`. Year labels `--ink-soft` 13px below; value labels `--ink` 14px Inter 600 above.
- No Y-axis line; thin `--line` baseline only; no gridlines.
- Annotation: dotted `--gold-dark` line at 2029 marking "first profitable year".
- Caption: "Source: PollenPal Business Model v8. Assumes commercial cohort 16/22/28/34/40 farms, 0.7%/mo churn, ARPU $4 → $6."

### Chart 2 — Gross margin trajectory 2026-2030 (§8)

- Type: line + bar combo, 100% wrapper width × 240px tall
- Primary axis (line, `--gold-dark`, 2px): GM% — 44%, 56%, 63%, 67%, 71%
- Secondary axis (bars, soft gold tint): HW cost per unit — $46, $34, $28, $22, $18
- Title row: "Gross margin scales as hardware cost falls"
- Caption: "Source: PollenPal Business Model v8. HW cost reflects supplier quotes at 700 → 10,000-unit scale."

### Chart 3 — TAM / SAM / SOM (§5)

REUSE existing inline SVG from `investors.html` lines 202-225. Update one label only: TAM section description from "Precision Crop Protection: IoT, intervention marketplace, pollination verification, and precision application OS" to "Crop Protection: chemicals, IPM, and precision-tech alternatives". Same headline number ($107B+ → may round to $106B for citation match).

## 9. Tables (4 total)

### Table 1 — Pricing tiers (§4)

| | Commercial | Hobbyist | Partnership |
|---|---|---|---|
| Subscription | $4/hive/mo → $6 by Yr 5 | $8/hive/mo → $12 by Yr 5 | $20/hive/mo (rev share) |
| Setup | $2,500 one-time | bundled | bundled |
| Hives / customer | 1,500 | 5 | 50–8,000 managed |
| ACV (Yr 1) | $72K | $480 | varies |
| Channel | Direct sales | Self-serve | Best Bees, Alvéole |
| Hardware | Bundled | Bundled | Bundled |

### Table 2 — 5-year P&L (§8)

| | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---|---|---|---|---|
| Revenue | $40K | $172K | $653K | $1,947K | $4,648K |
| Gross profit | $17K | $95K | $410K | $1,305K | $3,285K |
| Gross margin % | 44% | 56% | 63% | 67% | 71% |
| Operating expenses | ($97K) | ($259K) | ($526K) | ($958K) | ($1,390K) |
| EBIT | ($80K) | ($164K) | ($116K) | $347K | $1,895K |
| EBIT margin % | (201%) | (95%) | (18%) | 18% | 41% |

### Table 3 — Roadmap: Now / Next / Later (§7)

| | Now (Search) 2026 | Next (Systematize) 2027 | Later (Scale) 2028+ |
|---|---|---|---|
| Product | Threat detection (varroa, africanization, queen) | Insightful recommendations (treatment timing, dispatch) | Autonomous response; crop expansion |
| GTM motion | Direct sales, 3 pilots → 8 commercial farms | Corporate beekeeping platform partnerships | Enterprise + intl; crop / orchard |
| Unit econ | $4/hive/mo, $72K ACV | + $20/hive/mo partner tier | ARPU $6, GM 71% |
| KPI | 5,000 HUM | 20 farms, 30K HUM | 80 farms, 120K HUM |
| Inflection | First paid commercial | First $1M ARR | Profitability (EBIT+) |

### Table 4 — Use of funds (§12)

| Bucket | $ | Key outcome |
|---|---|---|
| Hardware & manufacturing | $240K | IP67 enclosure, FCC cert, ~700 production devices |
| GPU inference infra | $75K | On-prem GPU; 80% inference cost cut, <1s latency |
| ML engineering | $50K | Vision model improvements, calibration model |
| Field ops & sales | $100K | Commercial customer support and pilot conversion |
| SG&A + buffer | $35K | Legal, fundraising, contingency |
| **Total** | **$500K** | **18-month runway to seed** |

## 10. Cross-link inventory

| From section | To section | Reason |
|---|---|---|
| §1 — "3 pilots committed" stat | §9 Traction | substantiate |
| §1 — "$500K SAFE" stat | §12 Ask | detail |
| §3 — "data flywheel" | §6 Competition (advantage) | reinforce moat |
| §3 — "on-prem GPU" | §12 Ask (GPU bucket) | tie to funding |
| §4 — "GM 44% → 71%" | §8 Financials | substantiate |
| §4 — "SOM math" | §5 Market | reuse derivation |
| §6 — "expansion to crops" | §7 Roadmap (Scale) | timing |
| §10 — "hardware reliability mitigation" | §12 Ask (HW bucket) | mitigation tied to funding |
| §10 — "channel concentration mitigation" | §7 Roadmap (Systematize → Scale) | mitigation tied to roadmap |

## 11. File structure

| File | Change |
|---|---|
| `investors.html` | Full rewrite (replace existing) |
| `styles.css` | Add 8 new components (Section 5). Add `@media print` block. |
| `scripts.js` | Add `IntersectionObserver` for TOC active-state. Add scroll-position bind for TOC progress bar. Add mobile dropdown toggle. |
| `images/` | Reuse existing assets. No new images required. |

## 12. Acceptance criteria

The memo is ready to ship when:

- [ ] All 13 LYS-rubric sections present in user-specified order, each with eyebrow numeral + thesis lead.
- [ ] Word count between 1,500 and 2,000 across body sections (excluding footnotes, captions, table cells).
- [ ] Every quantitative claim has an inline footnote linking to a per-section endnote with verifiable source or named assumption. No `{{NEEDS SOURCE}}` markers remain.
- [ ] Four fits explicitly named (Product/Market, Market/Channel, Channel/Model, Model/Market) in §4.
- [ ] Search / Systematize / Scale explicitly named in §7.
- [ ] Sticky left-rail TOC functional on desktop (>1100px); collapses to dropdown on mobile.
- [ ] Confidential banner under header. Footer shows `© 2026 PollenPal Inc.`
- [ ] Charts: revenue ramp + gross margin trajectory render as inline SVG. TAM/SAM/SOM circles reused (label updated).
- [ ] Tables: pricing tiers, 5-year P&L, roadmap, use of funds — all four use `.memo-table`.
- [ ] Risk section uses 4 callout pairs (TECHNICAL / HARDWARE / REGULATORY / MARKET).
- [ ] Appendix sections collapsible via `<details>`.
- [ ] Cross-links between sections functional (all 9 from Section 10 above).
- [ ] Print stylesheet produces a clean `Ctrl+P` PDF.
- [ ] Mobile responsive at 360px, 600px, 960px, 1100px breakpoints.
- [ ] No emojis. No em-dashes. No "transforming the future" copy. No gradients. No glassmorphism.
- [ ] Existing claim-policy preserved on homepage (unchanged); investor memo includes the additional figures (BOM, interviews, etc.) approved for investor context.

## 13. Out of scope (deferred decisions)

- Production accuracy claim ("~95%" or similar) — not included until calibration model produces defensible numbers.
- LTV/CAC and payback ratios — narrative only in §13B; deferred until first paid deployment confirms unit economics.
- Live deployment data dashboard / "see your hive" demo on the page — out of scope for this memo; could be a future addition.
- Downloadable PDF of the memo — print stylesheet handles this; no separate PDF generation pipeline.
- Investor-only authentication / NDA gate — the new memo will remain publicly reachable at `/investors`, same as the existing page (matches HoneyCheck precedent of accepting prototype-stage exposure). The Confidential banner is policy signaling, not access control.
