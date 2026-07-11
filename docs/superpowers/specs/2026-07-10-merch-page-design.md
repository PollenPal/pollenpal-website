# Merch page design (`/merch`)

**Date:** 2026-07-10
**Status:** implemented
**Scope:** a merch storefront page at `pollenpal.com/merch`, unlinked from the rest of the site.

## Goal

Sell PollenPal-branded apparel to the beekeeping community, and give the team a place
to order gear for gifting. Low volume. The page has to look like PollenPal, cost nothing
to run, and take as little ongoing maintenance as possible.

Explicit requirement from Robert: **no link to the store from any other page.** The page is
reachable by direct URL only. It is not hidden from Google (see "Discoverability" below).

## Decision: Printful Quick Stores, with checkout off-site

Printful fulfills the orders. The question was where checkout lives.

**Chosen: a free Printful Quick Store at `pollenpal.printful.me`.** `/merch` is a designed
page on our own site whose Buy buttons deep-link into that store, which owns the cart,
checkout, payment, sales tax, and fulfillment.

Why this and not the alternatives:

- **Printful has no embeddable store widget.** The old "Printful Embedded Ecommerce" product
  no longer exists in 2026, and Printful has been retiring integrations (Webflow was dropped
  in March 2025). There is no way to render a Printful cart inside our own page.
- **GitHub Pages cannot reverse-proxy.** The site is a static file server on the apex domain,
  so `/merch` cannot be proxied to a hosted storefront. Any store-at-a-path option has to be
  a client-side widget, and Printful does not offer one.
- **The Quick Store cannot be iframed.** `printful.me` sits behind Cloudflare bot protection
  and serves `X-Frame-Options: SAMEORIGIN`, so wrapping it inside `/merch` is not possible.
- **Shopify Starter ($5/mo) + Buy Button was the runner-up** and is the option to revisit if
  merch ever matters commercially. It keeps browsing and cart on our own page and auto-syncs
  products from Printful, so the page would never need hand-editing. Rejected for now because
  the store is a goodwill project, and Quick Stores is free *and* makes Printful the seller of
  record, so they collect and remit sales tax rather than us.

**The cost of the decision:** the customer leaves `pollenpal.com` at the moment they click Buy
and lands on a Printful-branded storefront with no theming. The page states this plainly rather
than hiding it, which is what keeps the handoff from feeling broken.

**Constraint:** Quick Stores is **US-only** (US tax residency, US shipping addresses).

## Pricing

Printful's cost (product plus fulfillment, verified against their order-estimate endpoint,
not just the catalog):

| Size | Printful cost | Retail | Net to us |
|---|---|---|---|
| S to XL | $15.29 | $28 | $12.71 |
| 2XL | $17.29 | $30 | $12.71 |
| 3XL | $19.29 | $32 | $12.71 |
| 4XL | $21.29 | $34 | $12.71 |

Printful's payout formula is `retail price - product and fulfillment cost = profit`, with no
monthly fee and no listed commission. Payouts are monthly via Stripe with a **$25 minimum**,
and profit only becomes visible after an order is delivered.

The size ladder tracks Printful's cost steps exactly, so margin is constant across sizes.
Both colorways are priced the same on purpose: they are the same blank (Comfort Colors 1717),
and pricing them differently invites the customer to buy the cheaper one for no reason.

**Do not set a low default markup.** The store's default markup governs future product pushes;
at 30% a tee would net $4.59 instead of $12.71.

## Page architecture

`merch.html`, served at `/merch` by GitHub Pages' extensionless routing (same as `/hobbyist`).
No build step, consistent with the rest of the site.

- Reuses `styles.css` for the design system: gold/cream/ink palette, Inter, the bee cursor,
  `.site-header`, `.site-footer`, `.btn`, `.eyebrow`, `.wrap`, `.section`.
- **Merch-specific CSS lives in a `<style>` block in `merch.html`, not in `styles.css`.** This
  page is a standalone surface nothing else links to, and keeping its rules local avoids
  touching the shared stylesheet that every marketing page depends on.
- Structure: compact centered hero, then a two-card product grid on a cream band, then a note
  explaining the Printful handoff, then a slim footer.
- **Product cards are plain HTML, not JS-rendered.** The page is indexable and there is no build
  step, so a JS-rendered grid would show nothing to a crawler and nothing with JS disabled.
  Two products do not need a template engine. Adding a third product is one `<article>` block.

## Gotchas

- **Printful mockups have an opaque white background**, so the product cards must be white.
  A cream card frames every shot in a visible white box. This is why `.merch-card` is `--bg`
  and the surrounding section is `.bg-cream`, rather than the reverse.
- **Mockup images are committed to `images/merch/`, not hotlinked** from `files.cdn.printful.com`.
  Those CDN URLs are content-hashed and rotate when a design is re-uploaded, which would break
  the page silently.
- **Quick Store product URLs are `https://pollenpal.printful.me/product/<slugified-name>`.**
  The slug derives from the product name, so **renaming a product in Printful breaks the Buy
  link on this page.** If the tees get renamed, update the `href`s here in the same change.
- **A product being "synced" in the Printful API is not the same as being published to the
  storefront.** Both tees reported `synced: 7/7` and `availability_status: active` while the
  storefront still showed "No products yet" and the product URLs redirected to the store root.
  Publishing is a separate dashboard action.
- **The `printful.me` slug is permanent.** It derives from the store name at creation and cannot
  be changed afterward.

## Discoverability

`/merch` is **not** added to any nav, footer, or body copy on `index.html` or `hobbyist.html`.
It is **not** blocked in `robots.txt` and carries no `noindex`.

The reasoning: an unlinked page with no inbound links ranks for essentially nothing, so blocking
it buys almost no privacy while costing the one case that matters, someone searching "PollenPal
merch" or "PollenPal shirt". That person already wants the shirt. Keeping the page out of the nav
already delivers the "no link on other pages" requirement; de-indexing it does not add to that.

## Not doing

- No cart, no cross-sell, no discount codes, no abandoned-cart email. Printful owns checkout.
- No hoodie, cap, or sticker at launch. Adding one is a product in Printful plus one `<article>`.
- No custom domain on the store. Quick Stores does not support one.
