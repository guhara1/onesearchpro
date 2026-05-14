// OneSearchPro :: interactions
(function () {
  // Year
  document.querySelectorAll('#year').forEach(el => (el.textContent = new Date().getFullYear()));

  // Mobile nav toggle
  const toggle = document.getElementById('navToggle');
  const nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => nav.classList.toggle('open'));
    nav.addEventListener('click', (e) => {
      if (e.target.tagName === 'A') nav.classList.remove('open');
    });
  }

  // Highlight current nav item
  const path = window.location.pathname.replace(/\/index\.html$/, '/').replace(/\/+$/, '/') || '/';
  document.querySelectorAll('.nav a, .dropdown a').forEach(a => {
    const href = a.getAttribute('href');
    if (!href) return;
    const norm = href.replace(/\/index\.html$/, '/').replace(/\/+$/, '/');
    if (norm === path && path !== '/') a.classList.add('active');
  });

  // Contact form
  const form = document.getElementById('contactForm');
  const note = document.getElementById('formNote');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const data = new FormData(form);
      if (!data.get('name') || !data.get('email') || !data.get('message')) {
        alert('이름, 이메일, 문의 내용을 입력해 주세요.');
        return;
      }
      try {
        const inquiries = JSON.parse(localStorage.getItem('osp_inquiries') || '[]');
        inquiries.push({ ...Object.fromEntries(data.entries()), at: new Date().toISOString() });
        localStorage.setItem('osp_inquiries', JSON.stringify(inquiries));
      } catch (_) {}
      form.reset();
      if (note) {
        note.hidden = false;
        note.scrollIntoView({ behavior: 'smooth', block: 'center' });
        setTimeout(() => (note.hidden = true), 8000);
      }
    });
  }

  // Reveal-on-scroll
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          en.target.style.opacity = '1';
          en.target.style.transform = 'none';
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12 });
    document.querySelectorAll('.svc, .price, .steps li, .feat, .card, .section-head, .page-hero-stats > div').forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(14px)';
      el.style.transition = 'opacity .5s ease, transform .5s ease';
      io.observe(el);
    });
  }
})();
