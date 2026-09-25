# pollenpal.com

Static site on GitHub Pages (CNAME `pollenpal.com`). GitHub `main` and the live site are the source of truth.

## Short links for social bios

GitHub Pages has no server-side redirects, so each short link is a folder with one `index.html` that forwards to the tagged homepage (instant `location.replace`, `meta refresh` fallback, `canonical` to the destination, `noindex`, no analytics tag of its own).

| Path | Forwards to |
| --- | --- |
| `/ig` | `https://pollenpal.com/?utm_source=instagram&utm_medium=social&utm_campaign=shorts` |
| `/tt` | `https://pollenpal.com/?utm_source=tiktok&utm_medium=social&utm_campaign=shorts` |
| `/yt` | `https://pollenpal.com/?utm_source=youtube&utm_medium=social&utm_campaign=shorts` |

### Adding a short link

Copy `ig/index.html` to a new lowercase folder (for example `x/index.html`), replace `instagram` with the new `utm_source` in all four places, and add a row to the table above.

## Campaign tags reaching the app

`utm.js` (loaded on the homepage, `/hobbyist`, `/commercial`, and `/merch`) stores any `utm_*` values from the landing URL for the browser session and appends them to every link that points at `app.pollenpal.com`, so the app can record where a sign-up came from. `/signup/` forwards its query string for the same reason.
