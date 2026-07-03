// Год в подвале
var y = document.getElementById('year');
if (y) y.textContent = new Date().getFullYear();

// Мобильное меню
(function () {
  var t = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.head-nav');
  if (t && nav) {
    t.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      t.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
})();

// Плавное появление блоков при прокрутке
(function () {
  var items = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    items.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add('in');
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  items.forEach(function (el) { io.observe(el); });
})();
