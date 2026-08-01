# Direction-first homepage: hobbyist vs commercial split

Date: 2026-08-01. Approved by Robert in-session.

## Copy sources (added 2026-08-01 after Robert dropped two new decks)

- **Investor deck v10** (`C:\projects\pollenpal\PollenPal v10.pdf`, 2026-08-01)
  supersedes v9 as the source for commercial numbers and claims. The deck is
  confidential; only marketing-safe claims go on the public site (traction stats,
  design-variation count, roadmap). Never P&L, ACV, unit costs, or market sizing.
- **Hobbyist sales deck** (`C:\projects\pollenpal\Hobbyist App Sales Ready.pdf`,
  2026-07-22) supersedes the 2026-07-13 v1 deck as the voice/flow source for
  `/hobbyist`.

## Goal

A beekeeper landing on pollenpal.com today gets the full commercial pitch; the only
path to the hobbyist app is a footer link labeled "The app". Restructure the site so
the homepage routes each audience to the right page immediately. The investors page
is already gone (removed 2026-06-29, PRs #10/#11); no work there.

## Sitemap after the change

```
/            index.html       NEW direction-first homepage (rebuilt)
/commercial  commercial.html  NEW file; current homepage content moved here nearly as-is
/hobbyist    hobbyist.html    stays; deck-informed copy pass (PR 2)
/merch       merch.html       untouched
/signup      signup/          untouched (redirect to app.pollenpal.com/signup)
/archive/*                    untouched
```

## Page: `/` (new direction-first homepage)

Same visual system: shared `styles.css`, Inter, gold/cream palette, bee cursor,
1240px wrap. One new CSS component for the audience door cards.

Section order:

1. **Header**: logo, nav (Commercial, The app, Stay in touch), Beekeeper login CTA.
2. **Hero**: short positioning headline covering both audiences plus one supporting
   sentence. May lean on "hive operating system" language; never "management
   system". Final copy at implementation; nothing ships with placeholder text.
3. **Audience doors** (above the fold, side by side, stack on mobile):
   - **Commercial**: camera hardware plus the full suite; CTA "See the system" to
     `/commercial`.
   - **Hobbyist**: the inspection app, no hardware, from $4.99/mo; CTA "See the
     app" to `/hobbyist`.
4. **Proof strip**: audience-neutral stats only, at v10 values (14.25M+ individual
   bee observations, 570K+ hive images). No Wendy quote here; it is
   commercial-specific and stays with the commercial content.
5. **Stay in touch** newsletter band (existing component, `#newsletter` anchor stays
   on `/`).
6. **Footer**: updated links (Commercial, The app, Merch, contact).

**Stale-anchor forwarding**: tiny inline script on `/`. If `location.hash` is one of
the commercial anchors that used to live on the homepage (`#problem`, `#how`,
`#advantage`, `#traction`, `#roadmap`, `#founders`, `#pilot`), redirect to
`/commercial` with the same hash. `#newsletter` and `#main` stay on `/`.

## Page: `/commercial` (content move)

- New `commercial.html` holding the current `index.html` content nearly as-is:
  hero "Inspect every hive. Every day.", problem, Kristen quote, Wendy band, how it
  works, why PollenPal, traction, roadmap, founders, pilot form, newsletter band,
  footer. All section anchors keep their ids (`#how`, `#advantage`, `#traction`,
  `#roadmap`, `#founders`, `#pilot`).
- Changes limited to: `<title>` and meta description; header nav (add a way back to
  `/` and to the app page); one new cross-link, a slim band directly under the
  header: "Keeping a few hives at home? See the app" to `/hobbyist`.
- The pilot request form stays here, same Google Form endpoint and field names.
- **Number sync to deck v10** (audit finding, Robert asked for consistency before
  building): 3.5M+ bee observations becomes 14.25M+; 450k/450,000 hive images
  becomes 570K+ (advantage card 3 and the traction strip); the "4 devices live in
  the field" traction tile becomes "3 commercial yards running PollenPal devices"
  per the v10 traction slide. The "4 Master Beekeeper advisors" tile and founders
  footnote stay (previously Robert-approved, not contradicted by v10, which names
  one Master Beekeeper advisor without a count); flagged in the report.
- No other copy revisions in this pass. Everything already consistent with v10 was
  verified 2026-08-01: problem stats (40%+, $577B), 25 design variations, CA+FL
  multiple seasons, roadmap stages/years, "Physical AI" eyebrow.

## Page: `/hobbyist` (copy pass, PR 2)

Reword following the **Hobbyist App Sales Ready deck** (2026-07-22): built by
beekeepers who like tech; notebook pain ("a notebook never tells you: it's time to
inspect, your mite test is due"); what PollenPal is (hives, inspections, records,
reports, alerts); tap-inspect-done NFC story; customize your hives (colors,
photos); reminders that fit your climate; "your future self will thank you";
"the best beekeepers don't rely on memory, they rely on data"; coffee-price close.

- Page structure (screenshot feature rows, NFC perk, pricing, FAQ, CTAs to
  app.pollenpal.com) stays. This is a wording and sequencing pass, not a rebuild.
- Claim verification done 2026-08-01. TRUE and usable: custom reminders with dates,
  annual repeat, seasonal presets, day-14 mite retest prompt, push notifications,
  overdue-inspection alert (all shipped, PRs #260/#432/#433/#435); season-end
  "Annual report" (shipped #489; NEVER the word "Almanac"); mite counts in the
  inspection form; queen names and performance tracking; hive colors and photos;
  free NFC stickers plus a phone stylus mailed (insert built 2026-08-01);
  up to 10 hives; $7.99/mo or $4.99/mo annual.
- FALSE or unverified, do NOT use: "syncs automatically when you're back in range"
  (only local draft autosave is verified; soften to "every tap is saved as you go");
  the deck's "$59.99/year" (Stripe truth is one $59.88/yr charge; site keeps
  $59.88); the deck's "Hive Management System" tagline (banned phrase; the app's
  approved self-description is "The hive operating system for beekeepers", and the
  marketing-site tagline "The hive inspection app" stays unless Robert says
  otherwise).
- Deck typos ("CHALLANGE", "figer tips", "Pollen Pal") are not carried over; deck
  em dashes are not carried over.
- Add cross-link: "Running a commercial operation? See the system" to `/commercial`.

## Link updates

- `hobbyist.html` footer: `/#how`, `/#advantage`, `/#pilot`, `/#founders` become
  `/commercial#...`.
- `index.html` (new): nav and footer links per the section list above.
- `merch.html`: links only to `/` and `/hobbyist`; no change needed.
- `archive/*`: untouched, stale links there are acceptable.

## SEO, meta, analytics

- Each page gets a distinct `<title>` and meta description; `/commercial` reuses the
  current homepage's meta since the content moved there, `/` gets new copy.
- GA4 + GTM snippet (already on every page) is copied onto the new pages. No new
  custom events; page paths alone now segment hobbyist vs commercial traffic.

## Standing rules (apply throughout)

- Claim policy: no ML accuracy numbers, no hardware pricing on our side, no
  interview counts.
- No em dashes or en dashes anywhere.
- Forms keep the existing Google Form action and entry field names verbatim.
- Names: Daniel, never Danny.
- GitHub main plus the live site are the source of truth; after merge, remind
  Robert to sync or reset the Pi mirror.

## Delivery

- **PR 1 (restructure)**: new `/`, content move to `/commercial`, link updates,
  anchor forwarding, meta.
- **PR 2 (hobbyist copy)**: deck-informed rewording of `/hobbyist`.
- **Audit** (done 2026-08-01, pre-build per Robert): stale v10 numbers are fixed in
  PR 1. Remaining open items go in the final report: the deck's $59.99 vs Stripe's
  $59.88; the "4 Master Beekeeper advisors" count absent from v10; the optional
  yellow jacket case study (v10 slide 8) as a future commercial-page addition.

## Out of scope

- Any merch, signup, or archive changes.
- Reviving any investor content.
- New analytics events or ad work (blocked on Robert separately).
- Implementing audit-list fixes (decided separately).
