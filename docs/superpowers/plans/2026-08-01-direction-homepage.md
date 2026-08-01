# Plan: direction-first homepage (PR 1) + hobbyist copy pass (PR 2)

Spec: `docs/superpowers/specs/2026-08-01-direction-homepage-design.md`.

## PR 1 (branch `direction-homepage`)

1. `git mv index.html commercial.html`, then in commercial.html:
   - Keep title/meta/og (page keeps its commercial identity).
   - Add `.audience-band` under the header: "Keeping a few hives at home?" link to
     `/hobbyist`.
   - Number sync to deck v10: advantage card 3 "3.5M+ ... 450,000" becomes
     "14.25M+ ... 570,000"; traction tiles 3.5M+ to 14.25M+, 450k+ to 570k+,
     "4 Devices live in the field" to "3 Commercial yards running devices".
     Keep "4 Master Beekeeper advisors" (flagged in report).
2. New index.html (direction homepage):
   - Head: GTM + GA4 snippets, new title/meta/og, inline stale-anchor forward
     script (problem/how/advantage/traction/roadmap/founders/pilot to
     /commercial#hash via location.replace).
   - Header: logo, Stay in touch (#newsletter), Beekeeper login. No pilot CTA
     before the split.
   - Centered hero: h1 "Every bee. Every hive. Every day." + short lede.
   - Two door cards (`.door-grid`/`.door-card`, new CSS): Commercial (hardware +
     full suite, CTA /commercial) and Hobbyist (the app, $4.99/mo annual, up to
     10 hives, free stickers, CTA /hobbyist).
   - Proof strip (stat-strip): 14.25M+ bee observations, 570k+ hive images,
     24/7 continuous monitoring.
   - Footer: same skeleton; Product links Commercial/The app/Merch; newsletter
     band unchanged.
3. hobbyist.html: footer links `/#how` `/#advantage` `/#pilot` `/#founders`
   become `/commercial#...`.
4. styles.css: append `.audience-band`, `.direction-hero`, `.door-grid`,
   `.door-card` styles; responsive stack under 900px.
5. Verify: `py -3.13 -m http.server` in the worktree, browser screenshots of /,
   /commercial, /hobbyist at desktop + 390px mobile; check doors, band, anchors
   (e.g. /#pilot forwards), no layout breaks. Then push, PR.

## PR 2 (branch off updated main after PR 1, or stacked on `direction-homepage`)

Reword hobbyist.html per spec claim list (Hobbyist App Sales Ready deck voice;
verified claims only; add commercial cross-link). Same local verification.
