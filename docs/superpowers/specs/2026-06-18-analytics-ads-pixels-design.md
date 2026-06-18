# Analytics + Ads Pixels — pollenpal.com (and later app.pollenpal.com)

**Status:** SCOPED / PARKED — design only, no implementation. Parked 2026-06-18 at Robert's
request ("focus on other stuff right now"). Pick this up when paid campaigns are imminent.
**Owner:** software (GTM agent to track on Backlog Sheet)
**Date:** 2026-06-18

---

## Goal

Stand up marketing + ad-conversion measurement so we can run **Google Ads** and **Meta Ads**
campaigns and actually optimize spend toward paying beekeepers. Three tags:

1. **Google Analytics 4 (GA4)** — traffic + behavior analytics
2. **Google Ads** — base tag + remarketing + conversion tracking
3. **Meta (Facebook/Instagram) Pixel** — PageView + Lead / conversion events

None of these accounts/IDs exist yet (confirmed 2026-06-18). No analytics of any kind is on
the site today.

## Key decision driving the whole design

**The real ad conversion happens in the app, not on the marketing site.** The funnel is:

```
ad click → pollenpal.com (marketing) → "Get started" → app.pollenpal.com → signup → subscribe (Stripe)
```

If we only pixel pollenpal.com, Google/Meta can optimize toward "visited a page" — a weak
signal. To optimize toward **paying customers**, the conversion events must fire where the
conversion completes (the app), and the two domains must be stitched into one funnel
(cross-domain measurement). Hence the work spans **both** surfaces, but they get **different
jobs** and are sequenced.

### Scope split

| | pollenpal.com (static HTML, GitHub Pages) | app.pollenpal.com (Next.js, Amplify) |
|---|---|---|
| **GA4** | PageViews + form-lead events | Product analytics, **cross-domain linked** to the site |
| **Google Ads** | base tag + remarketing | **conversion**: signup complete / subscribe |
| **Meta Pixel** | PageView + **Lead** | **CompleteRegistration / Subscribe** only |
| **Privacy posture** | marketing pages, lighter | logged-in product — **do NOT** blast every authenticated page to ad networks |

## Sequencing (decided)

- **Phase 1 — pollenpal.com (this repo).** Fast: static HTML. Where ad clicks land. Ship first.
- **Phase 2 — app.pollenpal.com (`PollenPal/pollenpal-app`, `webapp/`).** Higher value
  (closes the conversion loop) but more careful: Next.js integration, cross-domain linking,
  consent, and privacy on authenticated pages. Separate spec when we get to it.

This document fully scopes **Phase 1** and outlines **Phase 2**.

---

## Architecture — OPEN DECISION (recommendation: GTM)

Two viable ways to wire three tags. **Not yet finalized** — decide at implementation time.

### Option A — Google Tag Manager (recommended)
One GTM container snippet per page. GA4, Google Ads, and Meta Pixel are all configured
inside GTM's web UI. Future conversion events / new pixels (LinkedIn, TikTok, etc.) = GUI
change + publish, **no git deploy to either repo**.

- **Pros:** single control plane across two very different codebases (static HTML + Next.js);
  cleanest cross-domain linking and Google **Consent Mode v2** support; marketers can iterate
  on conversions without an engineer; one snippet to maintain.
- **Cons:** a third dashboard to learn; Meta Pixel in GTM is a "Custom HTML" tag (standard but
  slightly fiddly); container is an extra runtime dependency.

### Option B — Hardcoded directly
GA4 + Google Ads via one shared `gtag.js` loader; Meta via its own `fbevents.js` snippet.
Config lives in the repo (head snippet per page + event calls in the shared `/scripts.js`).

- **Pros:** simplest mental model; full control in code; no extra dashboard; marginally faster.
- **Cons:** every future conversion-event tweak or new pixel is a code change + push, in
  **two** repos once the app is in scope; three separate snippets to keep in sync.

**Recommendation:** **GTM.** We're about to spend on two ad platforms and will iterate on
conversions constantly in early campaigns; a GUI control plane that spans the static site and
the Next.js app is worth the one-time setup. Revisit only if we want zero third-party tag
runtime.

---

## Phase 1 — pollenpal.com implementation plan

### Site facts (verified 2026-06-18)
- Static HTML on GitHub Pages. Repo `PollenPal/pollenpal-website`, public, `CNAME = pollenpal.com`.
- **Three live pages:** `index.html`, `hobbyist.html`, `investors.html`.
- **No shared `<head>`** (static HTML) → the GTM/GA head snippet must be pasted into each
  page's `<head>` (and the GTM `<noscript>` right after each `<body>` open).
- **Shared script:** `/scripts.js` is `defer`-loaded on all three pages → the right home for
  conversion event calls (`gtag`/`fbq`/`dataLayer.push`) on form submit.
- **Already loaded third-party:** Cloudflare Turnstile (`challenges.cloudflare.com`) — account
  for it in any CSP / consent work.

### Conversion points (the forms)
All forms POST to Google Forms via a hidden iframe (no redirect; success shown in-page by
`scripts.js`). So the conversion signal is the **submit handler in `scripts.js`**, not a
thank-you page.

| Form | Page | Element | Event value |
|---|---|---|---|
| **Request a pilot** (commercial) | `index.html` | `#pilotForm` | **highest** — `generate_lead` / Meta `Lead` (primary conversion) |
| **Investor — get in touch** | `investors.html` | `#invForm` | investor lead (separate event/label) |
| **Newsletter subscribe** | all three | `.newsletter-form` | soft lead (`sign_up` / `Subscribe`) |

### Work items (Phase 1)
1. **Decide architecture** (GTM vs direct) — see above.
2. **If GTM:** paste container snippet into `<head>` + `<noscript>` after `<body>` on all 3
   pages. Configure GA4 / Google Ads / Meta tags + triggers inside GTM.
   **If direct:** add the gtag.js + fbevents.js head snippets to all 3 pages; put `gtag`/`fbq`
   init in a small shared head include pattern (or inline per page, kept in sync).
3. **Wire conversion events** in `/scripts.js` on the three form submit handlers (pilot,
   investor, newsletter), with distinct event names/labels so Google Ads & Meta can target the
   commercial-pilot lead specifically.
4. **Outbound "go to app" tracking:** tag the "Get started / app" CTA links so we can see
   click-through to `app.pollenpal.com` (and so cross-domain linking has a handoff to measure
   in Phase 2).
5. **Consent banner — OPEN DECISION** (see Privacy below).
6. **Verify:** GA4 Realtime shows hits; Google Tag Assistant / Meta Pixel Helper confirm all
   three fire; test each form submit fires its conversion. Document the GA4 property + Ads
   conversion IDs + Meta Pixel ID in a non-public place (NOT this public repo).

---

## Phase 2 — app.pollenpal.com (outline only)

Repo `PollenPal/pollenpal-app`, `webapp/` (Next.js 16 + next-intl, Amplify-hosted).

- **GA4:** add via `next/script` in the root layout (or GTM container). Same GA4 property as
  the site (or a second one) with **cross-domain linking** so site↔app is one session/funnel.
- **Google Ads + Meta:** fire **conversion events only** at the moments that matter —
  signup complete (`CompleteRegistration`) and subscription success (`Subscribe`/`Purchase`,
  hook off the existing Stripe success path / billing events). **Do not** put a blanket
  PageView pixel on every authenticated route.
- **Cross-domain:** ensure `gclid`/`fbclid` (ad click IDs) survive the `pollenpal.com →
  app.pollenpal.com` hop; GA4 linker + URL params. This is what actually attributes a paying
  beekeeper back to the ad that produced them.
- **Privacy:** authenticated product pages carry PII risk — keep ad pixels to conversion
  moments, integrate Consent Mode, and review what parameters get sent.

---

## Privacy / consent — OPEN DECISION

- Audience is mostly US (beekeepers), but Meta Pixel + EU/UK visitors raise GDPR/ePrivacy and
  Google **Consent Mode v2** is effectively required for EU ad features.
- **Options:** (a) ship without a banner initially (fastest, common for early US marketing
  sites, accept the gap); (b) lightweight consent banner + Consent Mode v2 (GTM makes this
  much easier — another point for Option A).
- Add a short privacy-policy / cookie note if we add a banner.
- **Decide before launching paid EU traffic.** Defer for US-only launch is defensible.

## Account-creation guide (to get the IDs)

When we resume, create accounts in this order and capture each ID:

1. **GA4** — analytics.google.com → create Account + Property → add a **Web data stream** for
   `pollenpal.com` (and later `app.pollenpal.com`) → copy **Measurement ID** `G-XXXXXXXXXX`.
2. **Google Ads** — ads.google.com → create account → Tools → Conversions → create conversion
   actions (pilot lead, newsletter; later signup/subscribe). Note the **Ads ID** `AW-XXXXXXXXXX`
   and each conversion's **label**. (Can link Ads ↔ GA4 to import GA4 conversions.)
3. **Meta** — business.facebook.com → Events Manager → create a **Pixel** → copy the numeric
   **Pixel ID**. Set up domain verification for `pollenpal.com`.
4. **(If GTM) Google Tag Manager** — tagmanager.google.com → create a **Web container** for
   `pollenpal.com` → copy **Container ID** `GTM-XXXXXXX`. Add GA4 / Ads / Meta tags + triggers
   inside it.

Store the resulting IDs somewhere private (1Password / the PollenPal `.env` conventions) — they
go in code/GTM, **never committed as anything sensitive** (GA/Ads/Meta web IDs are public-by-
design, but keep account access controlled).

## Open decisions before implementation (checklist)
- [ ] Architecture: **GTM** vs direct hardcoded
- [ ] Consent banner now vs defer (US-only launch)
- [ ] Same GA4 property for site + app, or two
- [ ] Which form submits count as primary conversions (proposed: pilot = primary)
- [ ] Who creates the ad accounts / owns ongoing GTM (Robert vs delegate)

## Backlog entry (for the Backlog Sheet)
> **Item:** Set up Google Analytics + Google Ads pixel + Meta Ads pixel on pollenpal.com (Phase 1),
> then app.pollenpal.com (Phase 2). **Category:** Marketing/Infra. **Owner:** software.
> **Source/Context:** Robert ask 2026-06-18. **Notes:** Scoped + parked — full design at
> `docs/superpowers/specs/2026-06-18-analytics-ads-pixels-design.md` in pollenpal-website.
> Blocked on: create the 4 accounts/IDs (GA4, Google Ads, Meta Pixel, GTM) + pick GTM-vs-direct.
> Real conversion is in-app, so Phase 2 closes the loop.
