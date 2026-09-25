// Carry campaign tags from the landing page into the app.
//
// The bio links (/ig, /tt, /yt) land on pollenpal.com with utm_* in the URL.
// GA4 reads them on that first pageview, but every sign-up and login link on
// the site points at a bare https://app.pollenpal.com, so the app would never
// learn where the visitor came from. This script remembers the tags for the
// browser session and appends them to every app link on the page. It makes
// no GA4 or GTM calls; the tagged landing pageview is the only one that counts.
(function () {
  var KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
  var STORE = 'pp_utm';
  var APP = 'https://app.pollenpal.com';

  function fromUrl() {
    var params = new URLSearchParams(location.search);
    var out = {};
    KEYS.forEach(function (k) {
      var v = params.get(k);
      if (v) out[k] = v.slice(0, 256);
    });
    return out;
  }

  function load() {
    try { return JSON.parse(sessionStorage.getItem(STORE) || '{}'); } catch (e) { return {}; }
  }

  function save(tags) {
    try { sessionStorage.setItem(STORE, JSON.stringify(tags)); } catch (e) { /* private mode: links still get tagged on this page */ }
  }

  // Most recent tagged landing wins. Ordinary internal navigation (no utm in
  // the URL) keeps whatever was stored earlier in the session.
  var tags = fromUrl();
  if (Object.keys(tags).length) save(tags); else tags = load();
  if (!Object.keys(tags).length) return;

  function decorate() {
    document.querySelectorAll('a[href^="' + APP + '"]').forEach(function (a) {
      try {
        var u = new URL(a.getAttribute('href'));
        KEYS.forEach(function (k) {
          if (tags[k] && !u.searchParams.has(k)) u.searchParams.set(k, tags[k]);
        });
        a.setAttribute('href', u.toString());
      } catch (e) { /* leave the link as it was */ }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', decorate);
  } else {
    decorate();
  }
})();
