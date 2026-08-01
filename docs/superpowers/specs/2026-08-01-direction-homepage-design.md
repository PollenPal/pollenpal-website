# Direction-first homepage: hobbyist vs commercial split

Date: 2026-08-01. Approved by Robert in-session.

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
4. **Proof strip**: audience-neutral stats only (3.5M+ bee observations, 450k+ hive
   images). No Wendy quote here; it is commercial-specific and stays with the
   commercial content.
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
- No copy revisions in this pass. Content fixes go on the audit list (below).

## Page: `/hobbyist` (copy pass, PR 2)

Reword following the hobbyist selling deck v1
(`C:\projects\pollenpal\hobbyist-deck\`, spec `2026-07-13-hobbyist-deck-design.md`):
records pain, Karen quote, what PollenPal is, NFC "tap the hive, see its story",
"a season with PollenPal" steps 0-4 (including "hand your phone to your mentor"),
coffee-price close.

- Page structure (screenshot feature rows, NFC perk, pricing, FAQ, CTAs to
  app.pollenpal.com) stays. This is a wording and sequencing pass, not a rebuild.
- Deck hard rules carry over: software only, zero hardware mentions; no timing
  promises ("under a minute" banned); no claims for unshipped features.
- Verify every claim against the live app before writing it: badges shipped since
  the deck was written (#550), so the no-badge rule may have relaxed; the
  no-push-reminders rule and current pricing ($4.99/mo annual, $7.99/mo monthly,
  up to 10 hives) must be re-confirmed against the live app.
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
- **Audit list** delivered alongside PR 1: stale claims and content fixes found on
  both pages (for example the "4 devices live" traction stat) for Robert to
  green-light as follow-ups. Not implemented in either PR without approval.

## Out of scope

- Any merch, signup, or archive changes.
- Reviving any investor content.
- New analytics events or ad work (blocked on Robert separately).
- Implementing audit-list fixes (decided separately).
