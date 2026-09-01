(function () {
  var slider = document.getElementById('houseSlider');
  if (!slider) return;

  var slides = slider.querySelectorAll('.house-slide');
  var nav = slider.querySelector('.house-slider-nav');
  var total = slides.length;
  if (total < 2) return;

  var current = 0;
  var timer = null;
  var INTERVAL = 4500;

  function buildNav() {
    if (!nav) return;
    for (var i = 0; i < total; i++) {
      var dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'house-dot' + (i === 0 ? ' active' : '');
      dot.setAttribute('aria-label', 'Ir a la vista ' + (i + 1));
      dot.addEventListener('click', function (e) {
        var idx = Array.prototype.indexOf.call(nav.children, e.currentTarget);
        show(idx);
        restart();
      });
      nav.appendChild(dot);
    }
  }

  function show(idx) {
    slides[current].classList.remove('active');
    current = (idx + total) % total;
    slides[current].classList.add('active');
    if (nav) {
      var dots = nav.children;
      for (var i = 0; i < dots.length; i++) {
        dots[i].classList.toggle('active', i === current);
      }
    }
  }

  function next() { show(current + 1); }

  function start() {
    timer = setInterval(next, INTERVAL);
  }

  function stop() {
    if (timer) { clearInterval(timer); timer = null; }
  }

  function restart() {
    stop();
    start();
  }

  buildNav();
  start();

  slider.addEventListener('mouseenter', stop);
  slider.addEventListener('mouseleave', start);
  slider.addEventListener('touchstart', stop, { passive: true });
  slider.addEventListener('touchend', function () {
    restart();
  }, { passive: true });
})();
