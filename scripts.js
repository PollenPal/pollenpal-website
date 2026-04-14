// PollenPal — minimal interactive layer
// (1) Mobile nav toggle
// (2) Form submission feedback
// (3) Smooth scroll for in-page anchors

(function () {
  // ===== MOBILE NAV =====
  const toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      const open = toggle.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // ===== FORM FEEDBACK =====
  // Google Forms POST into a hidden iframe; we can't read the response,
  // but we can swap the form for a thank-you message after submit.
  document.querySelectorAll('form[target^="hidden_iframe"]').forEach(function (form) {
    form.addEventListener('submit', function () {
      setTimeout(function () {
        const card = form.closest('.form-card');
        if (!card) return;
        card.innerHTML =
          '<div class="form-success">' +
          '<h3>Thanks — we\'ll be in touch.</h3>' +
          '<p>We\'ll respond within 2 business days.</p>' +
          '</div>';
      }, 600);
    });
  });

  // ===== SMOOTH ANCHOR SCROLL =====
  // Header is sticky, so account for its height when scrolling to anchors.
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      const id = link.getAttribute('href');
      if (id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const headerOffset = 72;
      const top = target.getBoundingClientRect().top + window.pageYOffset - headerOffset;
      window.scrollTo({ top: top, behavior: 'smooth' });
    });
  });
})();
