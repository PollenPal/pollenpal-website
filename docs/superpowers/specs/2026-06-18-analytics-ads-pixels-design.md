# Analytics + Ads Tracking — pollenpal.com (and later app.pollenpal.com)

**Status:** ACTIVE — decisions locked 2026-06-18 (resumed from PARKED). Design approved by
Robert; implementation blocked only on account creation (Robert's part). 
**Owner:** software (GTM agent to track on Backlog Sheet)
**Date:** 2026-06-18

---

## Decisions locked (2026-06-18)

| Decision | Choice | Why |
|---|---|---|
| **Architecture** | **Google Tag Manager (GTM)** | One control plane across the static site + Next.js app; add/change tags from a GUI with no code deploy; cleanest cross-domain linking + Consent Mode later. |
| **Scope (now)** | **Google only — GA4 + Google Ads.** Meta (Facebook/Instagram) Pixel **deferred.** | Matches the actual ask ("Google ad tracking") and where spend is going. GTM makes adding Meta later a ~10-min dashboard job, not a rebuild. |
| **Consent banner** | **Defer** (no banner now) | Audience is US beekeepers. Revisit only before targeting paid EU/UK traffic. |
| **GA4 property** | **One property, shared site + app**, cross-domain linked | So `ad → site → app signup → subscribe` reads as ONE funnel, not two disconnected halves. |
| **Primary site conversion** | **"Request a pilot" lead** (commercial). Investor + newsletter = secondary. | Pilot is the real commercial prospect. |
| **In-app product analytics** | **SEPARATE future project** (self-hosted PostHog), NOT part of this | Different job, different tool, different privacy posture — see "Product analytics" below. |
| **App "conversion" = trial-start vs first paid invoice** | **DEFERRED to Phase 2** | Trial-first billing makes this a real ROAS decision; decide when we build Phase 2. |

---

## Goal

Stand up ad-conversion measurement so we can run **Google Ads** campaigns and optimize spend
toward paying beekeepers. Two Google tags now, via GTM:

1. **Google Analytics 4 (GA4)** — traffic + behavior analytics
2. **Google Ads** — base tag + remarketing + conversion tracking

**Meta (Facebook/Instagram) Pixel is deferred** — add it inside GTM when Meta ads become a
plan. No analytics of any kind is on the site OR the app today (confirmed by audit 2026-06-18);
no GA4 / Google Ads / GTM accounts exist yet.

## Key design decision (drives the whole thing)

**The real ad conversion happens in the app, not on the marketing site.** The funnel is:

```
ad click → pollenpal.com (marketing) → "Start free trial" → app.pollenpal.com → signup → subscribe (Stripe)
```

If we only tag pollenpal.com, Google can optimize toward "visited a page" — a weak signal. To
optimize toward **paying customers**, the conversion events must fire where the conversion
completes (the app), and the two domains must be stitched into one funnel (cross-domain
measurement). So the work spans **both** surfaces, with **different jobs**, sequenced.

### Scope split

| | pollenpal.com (static HTML) | app.pollenpal.com (Next.js, Amplify) |
|---|---|---|
| **GA4** | PageViews + form-lead events | Product analytics, **cross-domain linked** to the site |
| **Google Ads** | base tag + remarketing | **conversion**: signup complete + subscribe |
| **Privacy posture** | marketing pages, lighter | logged-in product — **do NOT** blast every authenticated page to Google |

## Sequencing

- **Phase 1 — pollenpal.com (`PollenPal/pollenpal-website`, this repo).** Fast: static HTML.
  Where ad clicks land. **Ship first.** Fully scoped below.
- **Phase 2 — app.pollenpal.com (`PollenPal/pollenpal-app`, `webapp/`).** Higher value (closes
  the conversion loop), more careful: Next.js integration, cross-domain linking, privacy on
  authenticated pages. **Outlined below; gets its own implementation spec when we get to it.**

---

## Architecture — DECIDED: Google Tag Manager

One GTM container snippet per page (head + `<noscript>`). GA4 and Google Ads are configured
inside GTM's web UI; Meta and any future tags (LinkedIn, TikTok) get added there later with no
code deploy. Cleanest path for cross-domain linking and (later) Consent Mode v2. Trade-off
accepted: one extra dashboard to learn, GTM container is an extra runtime dependency.

(Rejected alternative: hardcoding `gtag.js`/`fbevents.js` per page — simpler mental model but
every future tweak is a code change + redeploy across two repos. Not worth it when we'll iterate
on conversions during early campaigns.)

---

## Phase 1 — pollenpal.com implementation plan

### Site facts (audited 2026-06-18 — see "Audit corrections" for what the first draft got wrong)
- Static HTML, repo `PollenPal/pollenpal-website`, `CNAME = pollenpal.com`. **Hosting method
  (GitHub Pages) is NOT provable from the repo — no workflow / `_config.yml` / `.nojekyll`.
  VERIFY hosting out-of-band before go-live** (doesn't change the plan, just a box to tick).
- **Three primary live pages:** `index.html`, `hobbyist.html`, `investors.html`.
- **Two leftover `archive/` pages also git-tracked and publicly reachable:** `archive/v1/index.html`
  and `archive/hobbyist-hardware/index.html` (the latter is fully live — Turnstile, its own
  `#hobForm` + newsletter form, links to app.pollenpal.com). **Plan: add `<meta name="robots"
  content="noindex">` and do NOT instrument them**, so they don't pollute analytics. (There is
  NO `how-it-works` page — "How it works" is the in-page anchor `/#how`.)
- **No shared `<head>`** — each page has its own inline head. The GTM head snippet must be pasted
  into each page's `<head>`, and the GTM `<noscript>` right after each `<body>` open.
- **Shared script:** `/scripts.js` is `defer`-loaded on all pages (`index.html:443`,
  `hobbyist.html:258`, `investors.html:739`) → the right home for the conversion `dataLayer.push`
  calls on form submit.
- **Already-loaded third-party:** Cloudflare Turnstile + Google Fonts. **No CSP exists**, so
  adding GTM won't be blocked (and there's no CSP to update).

### Conversion points (the forms)
All forms natively POST to a **Google Form** via a hidden iframe (no redirect). Success UI is
rendered in `scripts.js` on a **fixed ~600ms timer after the honeypot + Turnstile guards pass** —
the page cannot read the cross-origin Google Forms response, so "success" means "submitted &
passed spam checks," not "Google confirmed save." **Therefore: fire the conversion inside the
success path, AFTER the honeypot/Turnstile guards (`scripts.js:27,37`) — never before** (else
spam/bot submits count as conversions).

| Form | Page(s) | Selector | GTM `dataLayer` event | Google Ads conversion |
|---|---|---|---|---|
| **Request a pilot** (commercial) | `index.html` (`#pilotForm`) | id | `pilot_lead` | **primary** |
| **Investor — get in touch** | `investors.html` (`#invForm`) | id | `investor_lead` | secondary |
| **Newsletter subscribe** | all 3 (`.newsletter-form`) | class | `newsletter_signup` | soft / secondary |

> **Differentiation note:** `#pilotForm` and `#invForm` POST to the **same** Google Form with the
> same `entry.*` field IDs. They can only be told apart by **form id**, not by action URL — so the
> `scripts.js` handler must branch on the element (`#pilotForm` vs `#invForm` vs `.newsletter-form`)
> when pushing the dataLayer event.

### Cross-domain handoff (sets up Phase 2)
All "go to the app" CTAs are **bare `https://app.pollenpal.com` links with no query params / no
GA linker / no `gclid` forwarding today.** Locations: `index.html:109` (login nav-cta);
`hobbyist.html:54,55,68,158,195,242` (login + multiple "Start free trial"); none on
`investors.html` (its CTA is the in-page `#ask`). **Plan:** once GA4 is in GTM, enable GA4
**cross-domain linking** for `app.pollenpal.com` so the linker auto-appends the `_gl` param, and
ensure ad-click IDs (`gclid`) ride along to the app. This is the hook Phase 2 consumes.

### Work items (Phase 1)
1. **Paste the GTM container snippet** (`<head>` + `<noscript>` after `<body>`) into `index.html`,
   `hobbyist.html`, `investors.html`. Use a placeholder `GTM-XXXXXXX` until the real container ID
   exists, then one-line swap.
2. **`noindex` the two `archive/` pages** and leave them un-instrumented.
3. **Wire conversion events in `/scripts.js`**: in the form success path (after guards), branch on
   the form element and `dataLayer.push({event: 'pilot_lead' | 'investor_lead' | 'newsletter_signup'})`.
4. **In GTM (dashboard, not code):** add the GA4 config tag (fires all pages), a Google Ads base
   tag, GA4 + Ads conversion triggers bound to the three dataLayer events, and enable GA4
   cross-domain linking to `app.pollenpal.com`.
5. **Verify:** GTM Preview mode + Google Tag Assistant confirm the container + GA4 fire; GA4
   Realtime shows hits; each form submit fires its event once (and does NOT fire on a blocked
   spam/bot submit). Record GA4 Measurement ID + Ads ID + conversion labels in a **private** store
   (NOT this public repo).

---

## Phase 2 — app.pollenpal.com (outline only; own spec later)

Repo `PollenPal/pollenpal-app`, `webapp/` — **Next.js 16.2.9 + React 19, App Router, next-intl,
Amplify-hosted.** Root layout: **`webapp/app/layout.tsx`** (async server component, already
renders a `<head>`) — the only global mount point for the GTM/GA4 tag (`next/script`).

**Existing first-party funnel to piggyback on (PR #268):** `webapp/app/lib/funnel.ts`
(`trackFunnel` → `POST /api/funnel-events`, anon id in localStorage `pp_anon_id`). Co-locate each
ad-conversion fire with the matching `trackFunnel` call.

- **GA4:** same property as the site, **cross-domain linked** so site↔app is one funnel.
- **Signup-complete conversion (`CompleteRegistration` / Ads signup):** fire at **both** exits —
  the email-code path `webapp/app/signup/page.tsx:211` (next to `trackFunnel("signup_confirmed")`)
  AND the **auto-confirm** path `signup/page.tsx:130-135` (else auto-confirmed users are
  under-counted; the existing funnel has this same blind spot).
- **Subscribe conversion:** client-side, fire on the success page `webapp/app/onboarding/complete/page.tsx`
  **when `sub.access === "full"` is first observed (`:44-46`)** — NOT on page mount (trial
  activation lags the redirect; the page polls) and dedupe against the "Check again" retry (`:67`).
  Server-side alternative: the `checkout.session.completed` webhook (`api/routes/billing.py:234-244`)
  / `api/billing_events.py` for Google Ads offline/enhanced conversion uploads.
- **DECISION DEFERRED — what counts as the "subscribe" conversion:** the flow is a **30-day free
  trial** (`$0` at `checkout.session.completed`). "Conversion" can mean **trial-start** (more
  volume, Google learns fast, some never pay) or **first paid invoice** (true paying customer,
  ~30-day learning delay). Decide at Phase 2 build. Also add a funnel-parity event
  (`onboarding_completed` / `subscription_active`) — today the funnel stops at
  `onboarding_trial_started` (`onboarding/page.tsx:334`, pre-Stripe-redirect).
- **Cross-domain ad-click ID:** the app captures **nothing** today (only `?promo=` at
  `signup/page.tsx:72-80` — copy that pattern to capture `gclid`/`utm_*` into storage so they
  survive the Cognito confirm round-trip + Stripe redirect). For server-side conversions, thread
  `gclid` into Stripe Checkout metadata at session creation (`api/stripe_client.py:78-81`).
- **Privacy:** conversion moments sit on **authenticated** pages with email/name in scope. Scope
  pixels to signup/checkout routes (do NOT inject a blanket pageview pixel globally in
  `layout.tsx`), use Google **Enhanced Conversions** with **hashed** email only, and match the
  funnel's existing no-raw-PII discipline (`funnel.py` stores no PII; `billing_events.data` is
  already flagged for a PII-purge pass).

---

## Privacy / consent — DECIDED: defer (no banner now)

- Audience is mostly US beekeepers. Ship without a consent banner initially (common for early US
  marketing sites; accept the EU gap).
- **Revisit before launching paid EU/UK traffic** — then add a lightweight consent banner +
  Google Consent Mode v2 (GTM makes this much easier) and a short privacy/cookie note.
- App-side: keep ad tags to conversion moments + hashed PII regardless of banner (see Phase 2).

## Product analytics (in-app behavior) — SEPARATE future project, OUT of scope here

Tracking what users *do inside* the app (feature usage, onboarding drop-off, retention, session
replay) is a **different job** from ad-conversion tracking and is explicitly **not** part of this
work. Notes for when we pick it up:
- GA4 (going into the app anyway) gives a basic in-app behavior layer for free, but is weak at
  per-user retention / feature-adoption / replay questions.
- Right tool is a product-analytics platform — **PostHog** (free tier, **self-hostable** → fits
  Robert's data-ownership preference, funnels + retention + session replay).
- We already have a narrow first-party funnel (`funnel_events`, no dashboard) — not zero today.
- Privacy: a self-hosted tool avoids piping logged-in beekeepers' behavior to Google.
- **Action:** logged as its own Backlog item; do NOT entangle with the ad-tracking build.

## Account-creation guide (Robert's part — the only blocker)

Create these **three free** accounts (Google login; Meta deferred). Capture each ID into a
**private** store (NOT this repo):

1. **Google Analytics 4** — analytics.google.com → create Account + Property → add a **Web data
   stream** for `pollenpal.com` (add `app.pollenpal.com` as a second stream later) → copy the
   **Measurement ID** `G-XXXXXXXXXX`.
2. **Google Ads** — ads.google.com → create account (asks for a card during setup; creating it is
   free, no spend required) → Tools → Conversions → create conversion actions (pilot lead;
   newsletter; later signup/subscribe). Note the **Ads ID** `AW-XXXXXXXXXX` + each conversion's
   **label**. Link Ads ↔ GA4 to import GA4 conversions.
3. **Google Tag Manager** — tagmanager.google.com → create a **Web container** for `pollenpal.com`
   → copy the **Container ID** `GTM-XXXXXXX`. (GA4 + Ads tags get configured inside it.)

(GA/Ads/GTM web IDs are public-by-design, but keep account *access* controlled.)

## Resolved decisions (was the open checklist)
- [x] Architecture: **GTM**
- [x] Scope now: **Google only (GA4 + Google Ads)**; Meta deferred
- [x] Consent banner: **defer** (US-only launch)
- [x] GA4 property: **one, shared** site + app
- [x] Primary site conversion: **pilot lead**
- [ ] **(Phase 2)** App "subscribe" conversion = trial-start vs first paid invoice
- [ ] **(Robert)** Create the 3 accounts (GA4, Google Ads, GTM) + capture IDs
- [ ] Verify site hosting method (GitHub Pages) out-of-band

## Audit corrections (what the first draft got wrong — fixed above)
- `/how-it-works` page does **not** exist (it's the `/#how` anchor).
- **Two live `archive/` pages** exist and are publicly reachable — first draft ignored them.
- **Pilot + investor forms share one Google Form** → differentiate by form id, not action URL.
- **Success fires on a 600ms timer, not on confirmed save**, and is skipped when honeypot/Turnstile
  block — fire the conversion inside the success path, after the guards.
- **GitHub Pages hosting is unconfirmed** from the repo — verify out-of-band.
- App CTAs carry **no gclid/linker** today; Next.js is **16.2.9 / React 19**; app has **no consent
  infra** and **two** signup-complete exits; billing is **trial-first** (changes "subscribe"
  semantics).

## Backlog entry (for the Backlog Sheet)
> **Item:** Set up Google Analytics + Google Ads tracking via GTM on pollenpal.com (Phase 1), then
> app.pollenpal.com (Phase 2). **Category:** Marketing/Infra. **Owner:** software.
> **Source/Context:** Robert ask 2026-06-18 (resumed). **Notes:** Design locked (GTM, Google-only,
> consent deferred) at `docs/superpowers/specs/2026-06-18-analytics-ads-pixels-design.md` in
> pollenpal-website. Blocked on Robert creating 3 accounts (GA4, Google Ads, GTM). Meta deferred.
> Real conversion is in-app → Phase 2 closes the loop.
>
> **Separate item:** Product analytics for the app (self-hosted PostHog) — understand in-app
> behavior/retention. Distinct from ad tracking; do not entangle.
