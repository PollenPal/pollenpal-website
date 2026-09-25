# Social launch: GA4 checklist and baseline (2026-09-25)

Written the day before the first PollenPal short goes out on Instagram Reels, TikTok and YouTube Shorts. Two purposes: the GA4 dashboard steps Robert does by hand, and the before numbers so there is a before/after.

## Bio links (live once PR #25 is merged)

| Platform | Bio link | Lands on |
| --- | --- | --- |
| Instagram | `pollenpal.com/ig` | homepage tagged `utm_source=instagram` |
| TikTok | `pollenpal.com/tt` | homepage tagged `utm_source=tiktok` |
| YouTube | `pollenpal.com/yt` | homepage tagged `utm_source=youtube` |

All three use `utm_medium=social` and `utm_campaign=shorts`.

## GA4 checklist (done 2026-09-25 in robert@pollenpal.com, driven by Claude; kept as the reference for redoing any step)

Status: 1 cross-domain saved (pollenpal.com exact, app.pollenpal.com contains). 2 `sign_up` and `trial_started` are key events; `pilot_lead`, `investor_lead`, `newsletter_signup` had not fired in the last 28 days so GA4 would not list them, star them under Admin > Events > Recent events once they fire. 3 Exploration `Social sign-ups by source` exists with tabs `sign_up by source` and `trial_started by source`. 4 baseline filled in below.

1. **Cross-domain linking.** Admin (gear, bottom left) > Data collection and modification > Data streams > click the `pollenpal.com` web stream > Configure tag settings > Configure your domains > Add condition: Contains `app.pollenpal.com` > Save. Check that `pollenpal.com` is already listed; add it if not.
   Verify afterwards: Reports > Realtime, open `pollenpal.com/tt` in a private window, click Get started, sign in. The Realtime view should show one user whose first user source is `tiktok`, and the app pageviews should not appear as a new session with source `pollenpal.com / referral`.
2. **Key events.** Admin > Data display > Events. In the list, flip the "Mark as key event" toggle for `sign_up` and `trial_started`. Do the same for `pilot_lead`, `investor_lead` and `newsletter_signup` if they are not already on. An event only appears in this list after it has fired at least once; if `trial_started` is missing, wait for the first trial or use Admin > Data display > Key events > New key event and type the name.
   Verify afterwards: Reports > Engagement > Key events lists all five.
3. **Source split for sign-ups and trials.** Explore (left nav) > Blank. Name it `Social sign-ups by source`. Under Variables: Dimensions > add `Session source / medium`; Metrics > add `Key events` (or `Event count`). Under Settings: drag `Session source / medium` to Rows, `Event count` to Values, and under Filters add `Event name` exactly matches `sign_up`. Duplicate the tab (tab menu > Duplicate) and change the filter to `trial_started`. Explorations save automatically and appear under Explore for one click later.
4. **Baseline in GA4.** Reports > Reports snapshot, date picker top right > Last 28 days. Note Users and, from Reports > Engagement > Events, the count for `sign_up`. Add both numbers to the table below with the date.

## Baseline, day before the first post

| Measure | Value | Source | As of |
| --- | --- | --- | --- |
| Accounts created, last 28 days, external | 6 | prod admin API, users created since 2026-08-28 excluding pollenpal.com and plus-addressed test accounts | 2026-09-25 20:50 UTC |
| Accounts created, last 28 days, all | 7 | same, including 1 internal | 2026-09-25 20:50 UTC |
| Total accounts | 53 | same | 2026-09-25 20:50 UTC |
| GA4 total users, Aug 28 to Sep 24 | 394 | GA4 Reports > User acquisition, custom range | 2026-09-25 |
| GA4 `sign_up` events, Aug 28 to Sep 24 | 4 (4 users) | GA4 Reports > Events | 2026-09-25 |
| GA4 `trial_started` events, Aug 28 to Sep 24 | 2 (2 users) | GA4 Reports > Events | 2026-09-25 |
| `sign_up` by session source, same range | all 4 are (direct) / (none) | Exploration `Social sign-ups by source` | 2026-09-25 |

The GA4 sign-ups reading (direct) is expected: before cross-domain linking, every app.pollenpal.com session started fresh. After 2026-09-25 the source should carry over from the website.

## Platform reminders (by hand)

- Instagram: switch the account to Professional (Creator or Business) before the first post; Insights only accrue from the switch. Bio link: `pollenpal.com/ig`, the single link.
- TikTok: switch to a Business account (analytics plus a clickable bio link). Bio link: `pollenpal.com/tt`.
- YouTube: put `pollenpal.com/yt` in the channel header link and the About page.
- No Meta or TikTok pixels for now; organic only. GTM makes them a dashboard job later.
- X is out unless Robert says otherwise. Adding `/x` later is one folder plus a README row.
