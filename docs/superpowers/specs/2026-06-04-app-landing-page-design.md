# PollenPal App Landing Page — Design Spec

Date: 2026-06-04
Status: Approved for planning
Page: `/hobbyist` (content replaced; URL and nav/footer links retained)

## Goal

Sell the **PollenPal app on its own** — the digital hive-inspection software that
needs **no hardware device**. We start selling this today (free 30-day trial, then
$6.99/month). The current `/hobbyist` page sells the backyard *camera hardware*; its
content is replaced by this app-focused page. The old camera version is preserved in
the archive so nothing is lost.

## Audience & tone

Hobbyist / sideliner beekeepers. Warm, simple, phone-first, no jargon. Someone deciding
in 60 seconds on their phone whether to start the trial. This is a focused conversion
page, not the long magazine-style commercial homepage or investor memo.

## Primary action

**Start free trial** → `https://app.pollenpal.com` signup. This is the single goal of the
page. Every CTA points there. No waitlist form (unlike the old hobbyist page), because
signup is self-serve and live today.

## Offer / pricing

- Free for 30 days, no credit card.
- Then **$6.99/month**.
- Up to **10 hives**.

## Design system (reuse, do not reinvent)

Reuse the existing site verbatim: `styles.css` palette (`--gold #E8A43A`,
`--gold-dark #C2851A`, cream tints, `--ink`), Inter type, Instrument Serif reserved for
big flourishes only, the stylized-SVG bee cursor, 1240px wrap, the `.section`,
`.eyebrow`, `.btn`/`.btn-primary`, `.how-grid`/`.step` components, the testimonial band,
and the shared header/footer. The page must feel native to pollenpal.com. No new color
system, no glassmorphism, no honeycomb patterns. Honor every "things that break easily"
note in the existing design (eyebrow flex-centering, nav-toggle margin, hero padding,
etc.).

The one new visual ingredient is **real app screenshots** (see below), shown large and
often. This is an image-heavy page by intent: the screenshots are the main selling tool.

## Screenshots (the centerpiece)

**Source:** captured from the live app logged in as `robert@pollenpal.com`, framing
**only Bill's (B005 / OCBS) hives that have NO device attached.** Bill has ~150
deviceless hives across 4 yards, so there is ample device-free data.

**Hard constraint:** screenshots must show **only the deviceless inspection software**.
NO PollenPal-device data of any kind — no camera/entrance feeds, no activity charts, no
mite counts, no colony-strength telemetry, no "Calibrating" tiles. If a screen shows any
device chrome, it does not go on this page. (This is why we use Bill's deviceless hives,
not the demo account, which is wired to device-equipped hives B004/B005.)

**Capture conventions:**
- Phone-width viewport (e.g. ~390px) so shots read as a real mobile app.
- Consistent device frame/treatment across all shots (a simple phone bezel or the
  existing `.visual-frame` rounded-dark frame; pick one and use it everywhere).
- Scrub anything that looks like internal/admin-only UI; show what a normal trial user
  sees.
- Save optimized images via the existing `scripts/prep_assets.py` flow (Pillow); drop
  sources in the gitignored `.superpowers/deck_media/`, output to `images/`.

**Shots needed (one per feature pillar + hero):**
1. Hero — a clean hive/inspection screen (the most attractive single screen).
2. Inspection form — the structured logging UI (frames of bees/brood/honey/pollen, queen
   status, temperament, feeding, swarm signs).
3. Next-inspection reminder — the schedule / "next visit" UI.
4. Apiary + hive list — Bill's yard with multiple deviceless hives listed.
5. History & photos — a hive's inspection timeline with attached photos.

If signup/login or any screen can't be reached self-serve, pause and ask Robert rather
than substituting a device screenshot.

## Page structure

All sections use existing components; copy is placeholder-quality here and will be
finalized in the build.

1. **Header** (reused). Nav CTAs change to: **Start free trial** (primary) and **Log in**
   (`app.pollenpal.com`). Nav link to this page stays labeled for hobbyists.
2. **Hero** — `hero-grid`: copy left, phone-framed app screenshot right.
   - Eyebrow: "For backyard beekeepers"
   - Headline: paper-notebook → app angle (e.g. "Every inspection, finally in one place.")
   - Lede: log inspections on your phone, never forget what a hive needs, no hardware.
   - Primary CTA: "Start your free trial →"
   - Subnote under CTA: "Free for 30 days. No credit card. Just your phone."
3. **Four feature pillars — alternating screenshot rows.** Each row is text on one side,
   a large real screenshot on the other, flipping sides each row:
   - Digital inspection forms
   - Next-inspection reminders
   - Apiaries + multiple hives
   - History & photos
4. **Testimonial band** — reuse Karen's existing quote verbatim
   ("For my first 4 years, I spent $600 on lost hives, and I didn't know why I was losing
   them." — Karen · Backyard beekeeper, South Florida).
5. **Pricing section** — small, clear block: "Free for 30 days, then $6.99/month. Up to
   10 hives." + Start-trial button.
6. **FAQ** — 3-4 short Q&As:
   - "Do I need the PollenPal device?" → No. The app works on its own, just your phone.
   - "What do I need to get started?" → A phone and your hives.
   - "Can I cancel anytime?" → Yes.
   - "Is my data mine?" → Yes; your records are yours.
7. **Final CTA band** — dark `--ink` section, one more "Start your free trial →".
8. **Footer** (reused).

## Cross-page cleanup (in scope)

Because `/hobbyist` is no longer a waitlist:
- Update footer links in `index.html` and `investors.html` that read "Hobbyist waitlist"
  so they no longer say "waitlist" (e.g. "PollenPal app" or "For hobbyists").
- Update any nav/footer copy that frames `/hobbyist` as the camera-hardware page.
- Preserve the old camera-hobbyist page in the archive (e.g.
  `archive/hobbyist-hardware/index.html`) so the prior version is recoverable.

## Out of scope

- No changes to the commercial homepage hero/story or investor memo content.
- No new backend, no new form endpoint (primary action is a link to existing signup).
- No ML accuracy numbers, no hardware pricing (existing claim-policy still applies).
- No em-dashes (site-wide rule).

## Success criteria

- A hobbyist on a phone understands within one screen that this is software, needs no
  device, and can start a free trial.
- Every screenshot is genuinely device-free (no camera/telemetry anywhere).
- The page is visually indistinguishable in style from the rest of pollenpal.com.
- Pricing ($6.99/mo after a free 30-day trial, up to 10 hives) is stated once, clearly.
- All CTAs land on `app.pollenpal.com` signup.
