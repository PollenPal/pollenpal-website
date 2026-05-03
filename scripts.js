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

  // ===== MEMO: TOC ACTIVE-SECTION OBSERVER =====
  // Highlights the current section in the left-rail TOC as the user scrolls.
  // Only active on /investors (where .toc-rail exists).
  const tocRail = document.querySelector('.toc-rail');
  if (tocRail) {
    const tocLinks = tocRail.querySelectorAll('a');
    const sectionMap = new Map();
    tocLinks.forEach(function (link) {
      const id = link.getAttribute('href').slice(1);
      const section = document.getElementById(id);
      if (section) sectionMap.set(section, link);
    });
    const tocObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          tocLinks.forEach(function (l) { l.classList.remove('active'); });
          const link = sectionMap.get(entry.target);
          if (link) link.classList.add('active');
        }
      });
    }, { rootMargin: '-20% 0px -65% 0px', threshold: 0 });
    sectionMap.forEach(function (_link, section) { tocObserver.observe(section); });
  }

  // ===== MEMO: TOC SCROLL PROGRESS BAR =====
  const tocProgress = document.querySelector('.toc-progress');
  const memoMain = document.querySelector('.memo-main');
  if (tocProgress && memoMain) {
    let ticking = false;
    function updateProgress() {
      const rect = memoMain.getBoundingClientRect();
      const totalScrollable = memoMain.offsetHeight - window.innerHeight;
      const scrolled = -rect.top;
      const ratio = totalScrollable > 0
        ? Math.max(0, Math.min(1, scrolled / totalScrollable))
        : 0;
      tocProgress.style.transform = 'scaleY(' + ratio + ')';
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) {
        window.requestAnimationFrame(updateProgress);
        ticking = true;
      }
    }, { passive: true });
    updateProgress();
  }

  // ===== MEMO: MOBILE TOC DROPDOWN =====
  const tocMobileToggle = document.querySelector('.toc-mobile-toggle');
  const tocMobileList = document.querySelector('.toc-mobile-list');
  if (tocMobileToggle && tocMobileList) {
    tocMobileToggle.addEventListener('click', function () {
      const open = tocMobileList.classList.toggle('open');
      tocMobileToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    // Close after navigating to a section
    tocMobileList.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        tocMobileList.classList.remove('open');
        tocMobileToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

})();
