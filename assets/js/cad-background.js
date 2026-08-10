/* =========================================================
   AutoCAD Guía — cad-background.js
   Fondo animado de la portada: partículas estilo "croquis CAD"
   (crucetas de cursor, puntos, anillos y ticks de acotación)
   que flotan lentamente sobre la rejilla, más un cursor
   cruzado que vaga por la escena y una línea de escaneo sutil.
   Canvas 2D, cero dependencias, respeta prefers-reduced-motion.
   ========================================================= */
(function(){
  'use strict';

  var canvas = document.getElementById('cadbgCanvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  if (!ctx) return;

  var reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

  function cssVar(name, fallback){
    var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v ? v : fallback;
  }
  function hexToRgb(hex, a){
    var s = hex.replace('#', '');
    if (s.length === 3) s = s.split('').map(function(ch){ return ch + ch; }).join('');
    var n = parseInt(s, 16);
    return 'rgba(' + ((n >> 16) & 255) + ',' + ((n >> 8) & 255) + ',' + (n & 255) + ',' + a + ')';
  }

  function palette(){
    return {
      cyan: cssVar('--layer-cyan', '#35D6CB'),
      magenta: cssVar('--layer-magenta', '#E36BFF'),
      green: cssVar('--layer-green', '#7BD87F'),
      amber: cssVar('--amber', '#FF9142'),
      blue: cssVar('--layer-blue', '#5B8CFF'),
      faint: cssVar('--text-faint', '#8296B0')
    };
  }
  var P = palette();

  var W = 0, H = 0, DPR = 1;
  var particles = [];
  var cross = null;
  var scanY = 0, scanOn = true;
  var rafId = null, running = false, last = 0;
  var t0 = performance.now();

  function rand(min, max){ return min + Math.random() * (max - min); }

  function makeParticles(){
    var target = Math.min(150, Math.max(40, Math.round((W * H) / 16000)));
    while (particles.length < target) {
      var roll = Math.random();
      var type = roll < 0.4 ? 'dot' : (roll < 0.62 ? 'plus' : (roll < 0.8 ? 'ring' : 'tick'));
      var colorPool = [P.cyan, P.magenta, P.green, P.amber, P.blue];
      particles.push({
        type: type,
        x: Math.random() * W,
        y: Math.random() * H,
        vx: rand(-3, 3),
        vy: rand(-11, -3),
        sway: rand(0.4, 1.6),
        phase: rand(0, Math.PI * 2),
        size: rand(1, 2.4),
        alpha: rand(0.1, 0.34),
        color: colorPool[Math.floor(Math.random() * colorPool.length)]
      });
    }
    if (!cross) {
      cross = {
        x: Math.random() * W,
        y: Math.random() * H,
        vx: rand(6, 14) * (Math.random() < 0.5 ? -1 : 1),
        vy: rand(4, 10) * (Math.random() < 0.5 ? -1 : 1),
        size: rand(13, 20),
        color: P.cyan
      };
    }
  }

  function drawPlus(x, y, s, a, color){
    ctx.strokeStyle = hexToRgb(color, a);
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x - s, y); ctx.lineTo(x + s, y);
    ctx.moveTo(x, y - s); ctx.lineTo(x, y + s);
    ctx.stroke();
  }

  function drawTick(x, y, s, a, color){
    ctx.strokeStyle = hexToRgb(color, a);
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(x - s, y + s); ctx.lineTo(x + s, y - s);
    ctx.stroke();
  }

  function drawParticle(p, t){
    var wob = Math.sin(t * 0.001 * p.sway + p.phase);
    var x = p.x + wob * 6;
    var y = p.y;
    switch (p.type) {
      case 'dot':
        ctx.fillStyle = hexToRgb(p.color, p.alpha);
        ctx.beginPath();
        ctx.arc(x, y, p.size * 0.5, 0, Math.PI * 2);
        ctx.fill();
        break;
      case 'ring':
        ctx.strokeStyle = hexToRgb(p.color, p.alpha);
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(x, y, p.size * 1.7, 0, Math.PI * 2);
        ctx.stroke();
        break;
      case 'plus':
        drawPlus(x, y, p.size * 1.6, p.alpha, p.color);
        break;
      default:
        drawTick(x, y, p.size * 1.5, p.alpha, p.color);
    }
  }

  function drawCross(t){
    if (!cross) return;
    var glow = 0.5 + Math.sin(t * 0.002) * 0.15;
    ctx.save();
    ctx.globalCompositeOperation = 'lighter';
    drawPlus(cross.x, cross.y, cross.size, 0.05 * glow, cross.color);
    drawPlus(cross.x, cross.y, cross.size * 0.45, 0.3 * glow, cross.color);
    ctx.restore();
  }

  function drawScan(t){
    if (!scanOn) return;
    ctx.save();
    var g = ctx.createLinearGradient(0, scanY - 60, 0, scanY + 60);
    g.addColorStop(0, 'rgba(53,214,203,0)');
    g.addColorStop(0.5, 'rgba(53,214,203,0.05)');
    g.addColorStop(1, 'rgba(53,214,203,0)');
    ctx.fillStyle = g;
    ctx.fillRect(0, scanY - 60, W, 120);
    ctx.strokeStyle = 'rgba(53,214,203,0.08)';
    ctx.beginPath();
    ctx.moveTo(0, scanY); ctx.lineTo(W, scanY);
    ctx.stroke();
    ctx.restore();
    if (scanY > H + 120) scanY = -120;
    void t;
  }

  function update(dt){
    particles.forEach(function(p){
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      if (p.y < -30) { p.y = H + 30; p.x = Math.random() * W; }
      if (p.x < -30) p.x = W + 30;
      if (p.x > W + 30) p.x = -30;
    });
    if (cross) {
      cross.x += cross.vx * dt;
      cross.y += cross.vy * dt;
      if (cross.x < 0 || cross.x > W) cross.vx *= -1;
      if (cross.y < 0 || cross.y > H) cross.vy *= -1;
      cross.x = Math.max(0, Math.min(W, cross.x));
      cross.y = Math.max(0, Math.min(H, cross.y));
    }
    scanY += 26 * dt;
  }

  function render(t){
    ctx.clearRect(0, 0, W, H);
    particles.forEach(function(p){ drawParticle(p, t); });
    drawCross(t);
    drawScan(t);
  }

  function frame(now){
    var dt = Math.min((now - last) / 1000, 0.05);
    last = now;
    update(dt);
    render(now);
  }

  function loop(){
    rafId = requestAnimationFrame(function(now){ frame(now); loop(); });
  }

  function start(){
    if (running) return;
    running = true;
    last = performance.now();
    loop();
  }

  function stop(){
    running = false;
    cancelAnimationFrame(rafId);
    rafId = null;
  }

  function resize(){
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = Math.round(W * DPR);
    canvas.height = Math.round(H * DPR);
    canvas.style.width = W + 'px';
    canvas.style.height = H + 'px';
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    if (scanY === 0) scanY = rand(0, H);
    makeParticles();
  }

  window.addEventListener('resize', resize);
  resize();

  if (reduced) {
    render(t0);
    return;
  }

  document.addEventListener('visibilitychange', function(){
    if (document.hidden) stop();
    else if (rafId === null) start();
  });
  start();

  new MutationObserver(function(){
    var np = palette();
    if (np.cyan !== P.cyan) { P = np; makeParticles(); }
  }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  window.addEventListener('pagehide', stop);
})();
