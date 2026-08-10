/* =========================================================
   AutoCAD Guía — animations.js
   Animaciones globales con anime.js (v3): entrada del hero y
   cabeceras de nivel, dibujo de líneas en los planos SVG,
   navbar que se compacta al hacer scroll y tilt 3D sutil en
   las tarjetas de nivel.
   ========================================================= */

(function(){
  'use strict';

  var animeOk = typeof anime !== 'undefined';
  var mq = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)');
  var reduced = !!(mq && mq.matches);

  if (!animeOk || reduced) return;

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init(){
    try {
      document.documentElement.classList.add('anime-ready');
      initHeroEntrance();
      initDiagramAnim();
      initNavbarShrink();
      initLevelTilt();
    } catch (err) { /* nunca romper el sitio */ }
  }

  /* ---------- Entrada del hero y de las cabeceras ---------- */
  function initHeroEntrance(){
    var heroEls = document.querySelectorAll('.hero-anime');
    if (heroEls.length) {
      anime({
        targets: heroEls,
        opacity: 1,
        translateY: 0,
        duration: 820,
        delay: anime.stagger(110),
        easing: 'easeOutQuart',
        complete: function(){
          heroEls.forEach(function(el){ el.classList.remove('hero-anime'); });
        }
      });
      return;
    }

    var headers = document.querySelectorAll('.header-anime');
    if (!headers.length) return;
    headers.forEach(function(header){
      var kids = header.querySelectorAll(':scope > .container > *');
      anime({
        targets: header,
        opacity: 1,
        duration: 700,
        easing: 'easeOutQuart',
        complete: function(){ header.classList.remove('header-anime'); }
      });
      if (kids.length) {
        anime({
          targets: kids,
          opacity: [0, 1],
          translateY: [18, 0],
          duration: 640,
          delay: anime.stagger(90),
          easing: 'easeOutQuart'
        });
      }
    });
  }

  /* ---------- Animación de diagramas y planos SVG ---------- */
  function initDiagramAnim(){
    var svgs = document.querySelectorAll('.diagram-card svg, .plan-sheet svg, .plan-canvas svg');
    if (!svgs.length || !('IntersectionObserver' in window)) return;

    var stepsDone = [];

    function styleOf(el, prop){
      try {
        return getComputedStyle(el).getPropertyValue(prop).trim();
      } catch (e) {
        return '';
      }
    }
    function isDashed(el){
      var d = styleOf(el, 'stroke-dasharray');
      return d && d !== 'none' && d !== '0' && d.indexOf(' ') !== -1;
    }
    function hasFill(el){
      var f = styleOf(el, 'fill');
      return f && f !== 'none' && f !== 'transparent';
    }
    function hasStroke(el){
      var s = styleOf(el, 'stroke');
      return s && s !== 'none';
    }

    function drawable(el){
      var len = 0;
      try { len = el.getTotalLength(); } catch (e) { len = 0; }
      return len > 0 && hasStroke(el) && !hasFill(el) && !isDashed(el);
    }

    function animateSvg(svg){
      var kids = svg.querySelectorAll('line, path, polyline, polygon, rect, circle, ellipse, text');
      if (!kids.length) return;

      var draw = [];
      var fade = [];

      kids.forEach(function(el){
        if (el.classList.contains('plan-cursor')) return;
        var isText = el.tagName.toLowerCase() === 'text';
        if (!isText && drawable(el)) {
          el.style.strokeDasharray = el.getTotalLength();
          el.style.strokeDashoffset = el.getTotalLength();
          draw.push(el);
        } else {
          el.style.opacity = 0;
          fade.push(el);
        }
      });

      if (draw.length) {
        anime({
          targets: draw,
          strokeDashoffset: 0,
          duration: 900,
          delay: anime.stagger(16),
          easing: 'easeInOutQuad',
          complete: function(){
            draw.forEach(function(el){
              el.style.strokeDasharray = '';
              el.style.strokeDashoffset = '';
            });
          }
        });
      }
      if (fade.length) {
        anime({
          targets: fade,
          opacity: 1,
          duration: 420,
          delay: anime.stagger(35),
          easing: 'easeOutQuad'
        });
      }
    }

    function animateSteps(steps){
      if (stepsDone.indexOf(steps) !== -1) return;
      stepsDone.push(steps);
      var cells = steps.querySelectorAll(':scope > .diagram-step');
      if (!cells.length) return;
      anime({
        targets: cells,
        opacity: [0, 1],
        translateY: [10, 0],
        duration: 500,
        delay: anime.stagger(150),
        easing: 'easeOutQuad'
      });
    }

    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        var svg = entry.target;
        animateSvg(svg);
        var steps = svg.closest('.diagram-steps');
        if (steps) animateSteps(steps);
      });
    }, { threshold: 0.25 });

    svgs.forEach(function(s){ io.observe(s); });
  }

  /* ---------- Navbar que se compacta al hacer scroll ---------- */
  function initNavbarShrink(){
    var nav = document.querySelector('.navbar-cad');
    if (!nav) return;
    function onScroll(){
      nav.classList.toggle('navbar-shrunk', window.scrollY > 60);
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- Tilt 3D sutil en las tarjetas de nivel ---------- */
  function initLevelTilt(){
    var cards = document.querySelectorAll('.level-card');
    if (!cards.length) return;

    cards.forEach(function(card){
      var target = card.closest('a') || card;
      var lock = false;

      target.addEventListener('mousemove', function(e){
        if (lock) return;
        lock = true;
        requestAnimationFrame(function(){
          var r = target.getBoundingClientRect();
          if (!r.width || !r.height) { lock = false; return; }
          var px = (e.clientX - r.left) / r.width - 0.5;
          var py = (e.clientY - r.top) / r.height - 0.5;
          anime({
            targets: target,
            rotateY: px * 8,
            rotateX: -py * 8,
            duration: 220,
            easing: 'easeOutQuad'
          });
          lock = false;
        });
      });

      target.addEventListener('mouseleave', function(){
        anime({ targets: target, rotateY: 0, rotateX: 0, duration: 340, easing: 'easeOutQuad' });
      });
    });
  }

})();
