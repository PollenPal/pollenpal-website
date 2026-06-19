# Design: App-forward narrative via a two-door front door

**Date:** 2026-06-19
**Status:** Implemented on branch `narrative/app-forward-landing` (not yet merged/deployed)
**Author:** Robert + Claude

## Goal

`pollenpal.com` led 100% with the commercial hardware story ("Physical AI for
commercial apiaries", CTA "Request a pilot"). The hive-management **app** — now a
real, shipped, self-serve product — was buried on a separate `/hobbyist` page and
invisible from the front door. Reframe the site so the app is a first-class
entrance alongside the hardware, without diluting either. The `/investors` memo
stays as-is (content untouched).

## Final information architecture

A thin **router splash** at `/` sends visitors to two dedicated product pages.

| URL | File | What it is | Change |
|---|---|---|---|
| `/` | `index.html` | NEW brand splash, two product doors | brand-new page |
| `/hardware` | `hardware.html` | Commercial hardware page (was the old homepage) | moved from old `index.html`, nav/footer/links updated |
| `/app` | `app.html` | The inspection-software page (was `/hobbyist`) | renamed from `hobbyist.html`, nav/footer/links updated |
| `/hobbyist` | `hobbyist.html` | redirect stub → `/app` | meta-refresh + `rel=canonical` + `noindex` (preserves old/ad links) |
| `/investors` | `investors.html` | Investor memo | content untouched; only nav/footer cross-links repointed |

No `sitemap.xml`/`robots.txt`/`404.html` in the repo (static GitHub Pages), so
nothing else to regenerate.

## The splash (`/`)

Centered brand block, then two large clickable product cards ("doors"), slim
header, thin footer. Reuses the existing design system (Inter, gold/cream palette,
bee cursor). Splash-specific CSS is inlined in `index.html` (same pattern as the
other pages' hero CSS). GA4 + GTM snippets carried over.

- **Header:** logo → `/`; `Contact us` (→ `/hardware#pilot`); `Beekeeper login →`
  (→ `app.pollenpal.com`). No Investors link (intentional — investor page is shared
  by direct link, not advertised publicly).
- **Brand block:** H1 `Helping beekeepers with technology that *actually* works.`
  (gold-italic "actually"); a **trust badge** pill `BEEKEEPER TESTED & APPROVED`
  with a gold check-seal SVG; sub-line `From a backyard hive to ten thousand
  colonies. Choose your tool to get started.`
- **Two doors** (`.door-card`, whole card is the link):
  - Left — kicker `FOR COMMERCIAL OPERATIONS`, title **PollenPal Hardware**, real
    photo of the white PollenPal base unit under a wooden Langstroth hive
    (`device-hive.jpg`, from IMG_5470), copy about watching hive activity +
    monitoring colony health, solar-powered/field-ready/off-grid, gold button
    **Explore the hardware →** (→ `/hardware`).
  - Right — kicker `FOR EVERY BEEKEEPER`, title **PollenPal Software**, a fan of
    three black-framed **phone screenshots** (apiary "Your hives" front-and-center,
    inspection form left, hive overview right; `app2-apiary/inspection/history.jpg`,
    captured from the live app on no-device hives so no telemetry shows), gold
    button **Get the app →** (→ `/app`).

## Destination pages

Content is unchanged (both pages were already strong and deck-v9-aligned, and the
site claim-policy is respected). Mechanical changes only:

- **Unified header** on `/hardware` and `/app`: `logo · Hardware · Software ·
  Investors · Beekeeper-login · [page CTA]`, current page marked.
- **Unified footer**: Products (Hardware, Software), Company (Founders, Investors),
  Contact → the inquiry form (`#pilot` / `/hardware#pilot`). Brand blurb
  "Technology for every beekeeper." Newsletter band retained.
- Cross-page anchors that moved off `/` repointed to `/hardware#…`; `/hobbyist` →
  `/app`.

## Investors page

Memo body, exhibits, footnotes: zero changes. Only the header nav and footer
cross-links repointed (`/#how` → `/hardware#how`, etc.; `/hobbyist` → `/app`), and
the dead `hello@pollenpal.com` mention in the `#ask` "Express interest" line
removed (form remains).

## Contact links

`hello@pollenpal.com` is not a real inbox. Every contact link now routes to the
existing Google-Form-backed inquiry form: splash + app footers → `/hardware#pilot`,
hardware footer → `#pilot`, investors footer → its own `#ask` section.

## Assets

- `device-hive.jpg` — hardware door photo (converted from `IMG_5470.HEIC` via
  pillow-heif, downscaled to 1280w).
- `app2-apiary.jpg`, `app2-inspection.jpg`, `app2-history.jpg` — live-app phone
  screenshots (414px viewport via chrome-devtools, from no-device Costa Mesa hives).
- Old `app-*.jpg` retained (still used by `/app` feature rows).

## Notable design decisions

- Door CTAs are full gold buttons (`.door-cta`) so they read as pressable, while the
  entire card remains the click target.
- Phone frames widened (~0.65 ratio) to fit the 0.749 viewport screenshots with
  minimal side-crop; center phone anchored left so "Your hives" isn't cut. The
  headless capture height is hard-capped, so true phone-portrait (~0.46) shots
  weren't obtainable; this is the best fit with current assets. Replacing with true
  tall phone screenshots later would let the frames go fully phone-shaped.
- Splash H1 sized down (`clamp(34px,5vw,58px)`) vs the global hero H1 so headline +
  both doors sit together above the fold.

## Future / not done

- Optionally make `/hardware` and `/app` titles/eyebrows lean further into the app.
- Replace phone screenshots with true full-length phone-portrait captures for a
  perfectly phone-shaped fan.
