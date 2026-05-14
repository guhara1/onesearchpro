// OneSearchPro :: interactions
(function () {
  // Year
  const y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Mobile nav toggle
  const toggle = document.getElementById('navToggle');
  const nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => nav.classList.toggle('open'));
    nav.addEventListener('click', (e) => {
      if (e.target.tagName === 'A') nav.classList.remove('open');
    });
  }

  // Contact form (client-side mock submit)
  const form = document.getElementById('contactForm');
  const note = document.getElementById('formNote');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const data = new FormData(form);
      if (!data.get('name') || !data.get('email')) {
        alert('이름과 이메일을 입력해 주세요.');
        return;
      }
      // Persist locally so user sees something happen even without backend
      try {
        const inquiries = JSON.parse(localStorage.getItem('osp_inquiries') || '[]');
        inquiries.push({ ...Object.fromEntries(data.entries()), at: new Date().toISOString() });
        localStorage.setItem('osp_inquiries', JSON.stringify(inquiries));
      } catch (_) {}
      form.reset();
      if (note) {
        note.hidden = false;
        setTimeout(() => (note.hidden = true), 6000);
      }
    });
  }

  // Reveal-on-scroll
  const io = ('IntersectionObserver' in window) ? new IntersectionObserver((entries) => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        en.target.style.opacity = '1';
        en.target.style.transform = 'none';
        io.unobserve(en.target);
      }
    });
  }, { threshold: 0.12 }) : null;

  if (io) {
    document.querySelectorAll('.svc, .price, .steps li, .feat, .card, .section-head').forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(14px)';
      el.style.transition = 'opacity .5s ease, transform .5s ease';
      io.observe(el);
    });
  }
})();
