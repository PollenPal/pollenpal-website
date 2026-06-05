# Free NFC Hive Stickers Perk — Design Spec

Date: 2026-06-05
Status: Approved for planning
Surfaces: `pollenpal-website` `/hobbyist` + `pollenpal-app` signup page

## Goal

Advertise a retention perk on two surfaces: **after a member's first paid month, PollenPal
mails them free custom NFC stickers, one per hive, each pre-linked to that hive.** Tapping a
sticker with a phone opens that hive's inspection form. This builds on the already-shipped NFC
hive-tags feature (PR #237): a sticker carries a remappable token at
`app.pollenpal.com/t/<token>` that resolves server-side to a hive and lands on the hive
overview with inspect one tap away.

## Offer mechanics (locked — copy must match exactly)

- **When:** "After your first paid month." (Free 30-day trial, then one paid month, then the
  stickers ship.)
- **What:** Free custom NFC stickers carrying the **full PollenPal logo**.
- **How many:** **One per hive**, each **pre-assigned** to that hive (up to the plan's 10-hive
  cap; cap language kept light).
- **What it does:** Tap with a phone → that hive's inspection form opens. No typing, no
  searching.
- Do not overclaim: the perk is mailed physical stickers; the tap behavior is the existing
  `/t/<token>` resolver (lands on hive overview, inspect one tap away).

## Surface 1 — Website `/hobbyist` (pollenpal-website)

### New "Free perk" section
A dedicated highlighted band, visually distinct from the four screenshot feature rows, placed
**immediately before the pricing section** so it reads as a bonus leading into the price.

- Eyebrow: "Free perk"
- Headline: "Tap a hive. Log a visit."
- Body: "After your first paid month, we mail you free PollenPal NFC stickers, one for each
  hive, already linked to it. Tap a sticker with your phone and that hive's inspection form
  opens. No typing, no searching."
- **Visual:** a clean CSS/SVG **sticker mockup** rendered in the site palette: a rounded
  NFC sticker bearing the **full PollenPal logo** (`/images/logo-full.png`) plus a tap/NFC
  motif (concentric tap arcs or a small phone-tapping-sticker cue). No photograph; generated
  with site CSS + inline SVG so it ships now and stays on-brand. Decorative
  (`aria-hidden`-friendly); the headline/body carry the meaning.

### Pricing-card bonus line
Add one line to the existing `.price-card` (under the `.price-note`):
"Plus free custom NFC hive stickers after your first paid month."

### Constraints
- Reuse the existing design system (palette, `.section`, `.eyebrow`, type, spacing). No new
  color system. No em-dashes. The section must feel native to the page built in the prior
  spec (`2026-06-04-app-landing-page-design.md`).
- New CSS lives appended in `styles.css` (e.g. a `.perk` / `.nfc-sticker` block); do not edit
  existing rules.

## Surface 2 — Signup page (pollenpal-app `webapp/app/signup/page.tsx`)

### Side "what you get" benefits panel
The signup page is a centered two-step form (register → confirm) using `next-intl`
(`useTranslations("signup")`). Add a **benefits panel beside the form**: two-column on
desktop (form + panel), the panel **stacks above the form on mobile**.

Panel = a short "What you get" list:
- Free for 30 days, then $6.99/month
- Up to 10 hives
- Free NFC hive stickers mailed after your first paid month — tap to open a hive's inspection
  form

### i18n
All new strings are added as `next-intl` keys under the `signup` namespace in BOTH
`webapp/messages/en.json` and `webapp/messages/es.json` (Spanish translated, not English
placeholders). Reuse existing key-naming conventions in those files.

### Constraints
- Match the signup page's existing styling/components; do not restructure the auth/confirm
  logic. The panel is presentational only.
- Keep the form the primary focus; the panel must not push the form below the fold on mobile
  (panel above form on mobile is acceptable and intended, kept compact).
- Don't introduce new dependencies.

## Out of scope

- No fulfillment/back-end work: this is messaging only. Minting/binding tokens and mailing
  stickers is an existing manual operational process (see NFC tags feature). No new API,
  schema, or billing logic.
- No homepage (`/`) change; only `/hobbyist` on the website.
- No changes to the `/t/<token>` resolver or `/admin/tags`.

## Success criteria

- `/hobbyist` shows a clear, on-brand "free NFC stickers after your first paid month" section
  (with the logo sticker mockup) plus a one-line bonus on the pricing card; renders cleanly
  desktop + mobile; no console errors; no em-dashes.
- The signup page shows a benefits panel including the NFC perk, in EN and ES, two-column on
  desktop and stacked on mobile, without disrupting signup.
- Copy on both surfaces matches the locked offer mechanics (after first paid month, one
  pre-assigned sticker per hive, tap opens the inspection form).
- Two separate PRs (one per repo).
