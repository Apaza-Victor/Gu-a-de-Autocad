/* =========================================================
   AutoCAD Guía — three-hero.js
   Héroe 3D decorativo de la portada (Three.js).
   Dibuja una pequeña "maqueta 3D" detrás de la hoja de
   dibujo del hero. El plano 2D original se conserva siempre.
   ========================================================= */
(function(){
  'use strict';

  var canvas = document.getElementById('hero3dCanvas');
  if (!canvas || typeof THREE === 'undefined') return;

  var reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

  function supportsWebGL(){
    try {
      var c = document.createElement('canvas');
      return !!(window.WebGLRenderingContext && (c.getContext('webgl') || c.getContext('experimental-webgl')));
    } catch (e) {
      return false;
    }
  }
  if (!supportsWebGL()) return;

  function cssVar(name){
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }
  function color(name, fallback){
    var v = cssVar(name);
    if (v) return new THREE.Color(v.trim());
    return new THREE.Color(fallback || '#35D6CB');
  }
  function themeColors(){
    return {
      bg: cssVar('--bg-panel-2') || '#0D1526',
      cyan: color('--layer-cyan', '#35D6CB'),
      green: color('--layer-green', '#7BD87F'),
      amber: color('--amber', '#FF9142'),
      magenta: color('--layer-magenta', '#E36BFF'),
      blue: color('--layer-blue', '#5B8CFF'),
      red: color('--layer-red', '#FF5D5D'),
      yellow: color('--layer-yellow', '#FFD166')
    };
  }

  var scene = new THREE.Scene();

  var camera = new THREE.PerspectiveCamera(40, 1, 0.1, 100);
  camera.position.set(5, 4, 7);
  camera.lookAt(0, -0.4, 0);

  var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);
  canvas.parentNode.appendChild(renderer.domElement);

  scene.add(new THREE.HemisphereLight(0xffffff, 0x223344, 1.15));
  var dir = new THREE.DirectionalLight(0xffffff, 1.5);
  dir.position.set(4, 8, 3);
  scene.add(dir);
  var fill = new THREE.DirectionalLight(0x88ccff, 0.4);
  fill.position.set(-4, 2, -5);
  scene.add(fill);

  var group = new THREE.Group();
  scene.add(group);

  var grid = new THREE.GridHelper(16, 16, themeColors().cyan, themeColors().cyan);
  grid.material.transparent = true;
  grid.material.opacity = 0.3;
  grid.position.y = -2;
  scene.add(grid);

  function solid(geo, col){
    var m = new THREE.MeshPhongMaterial({ color: col, flatShading: true, side: THREE.DoubleSide, transparent: true, opacity: 0.96 });
    return new THREE.Mesh(geo, m);
  }
  function axisLine(start, end, col){
    return new THREE.Line(
      new THREE.BufferGeometry().setFromPoints([start, end]),
      new THREE.LineBasicMaterial({ color: col })
    );
  }

  var c = themeColors();

  /* UCS pequeño */
  var ucs = new THREE.Group();
  ucs.add(axisLine(new THREE.Vector3(0,0,0), new THREE.Vector3(1,0,0), c.red));
  ucs.add(axisLine(new THREE.Vector3(0,0,0), new THREE.Vector3(0,1,0), c.green));
  ucs.add(axisLine(new THREE.Vector3(0,0,0), new THREE.Vector3(0,0,1), c.blue));
  ucs.position.set(-4.2, -2, 4);
  scene.add(ucs);

  /* Muro en L extruido */
  var lShape = new THREE.Shape();
  lShape.moveTo(-1.1, -0.4);
  lShape.lineTo(-1.1, 0.4);
  lShape.lineTo(-0.3, 0.4);
  lShape.lineTo(-0.3, -0.1);
  lShape.lineTo(1.1, -0.1);
  lShape.lineTo(1.1, -0.4);
  lShape.closePath();
  var lMesh = solid(new THREE.ExtrudeGeometry(lShape, { depth: 0.9, bevelEnabled: false }), c.cyan);
  lMesh.position.set(-1.4, -1.55, -1.3);
  group.add(lMesh);

  /* Cilindro */
  var cyl = solid(new THREE.CylinderGeometry(0.34, 0.34, 2.1, 28), c.amber);
  cyl.position.set(1.55, -0.95, -1.4);
  group.add(cyl);

  /* Vasija de revolución */
  var pts = [];
  for (var i = 0; i <= 22; i++) {
    var t = i / 22;
    pts.push(new THREE.Vector2(0.16 + Math.sin(t * Math.PI) * 0.5, t * 1.15));
  }
  var lathe = solid(new THREE.LatheGeometry(pts, 28), c.magenta);
  lathe.position.set(0.2, -1.45, 1.0);
  group.add(lathe);

  /* Caja con perforación */
  var box = solid(new THREE.BoxGeometry(1.3, 0.85, 1.0), c.green);
  box.position.set(-1.0, -1.55, 1.7);
  group.add(box);
  var hole = solid(new THREE.CylinderGeometry(0.3, 0.3, 1.4, 24), c.red);
  hole.rotation.x = Math.PI / 2;
  hole.position.set(-1.0, -1.55, 1.7);
  group.add(hole);

  /* Anillo de acotación */
  var ring = solid(new THREE.TorusGeometry(0.62, 0.14, 14, 36), c.yellow);
  ring.position.set(1.5, -1.8, 1.2);
  ring.rotation.x = Math.PI / 2;
  group.add(ring);

  /* ---------- Interacción: arrastrar ---------- */
  var dragging = false, prevX = 0, prevY = 0;
  canvas.addEventListener('pointerdown', function(e){
    dragging = true;
    prevX = e.clientX; prevY = e.clientY;
  });
  window.addEventListener('pointermove', function(e){
    if (!dragging) return;
    var dx = e.clientX - prevX;
    var dy = e.clientY - prevY;
    prevX = e.clientX; prevY = e.clientY;
    group.rotation.y += dx * 0.008;
    group.rotation.x += dy * 0.004;
    group.rotation.x = Math.max(-1.1, Math.min(1.1, group.rotation.x));
  });
  window.addEventListener('pointerup', function(){ dragging = false; });

  /* ---------- Resize ---------- */
  function resize(){
    var wrap = canvas.parentNode;
    var w = wrap.clientWidth || 1;
    var h = wrap.clientHeight || 1;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  }
  window.addEventListener('resize', resize);
  if (window.ResizeObserver) new ResizeObserver(resize).observe(canvas.parentNode);
  resize();

  /* ---------- Bucle ---------- */
  var rafId = null, last = 0, running = false;
  function tick(now){
    var dt = Math.min((now - last) / 1000, 0.05);
    last = now;
    if (!reduced && !dragging) group.rotation.y += dt * 0.18;
    renderer.render(scene, camera);
  }
  function start(){
    if (running) return;
    running = true;
    last = performance.now();
    (function step(now){ tick(now); rafId = requestAnimationFrame(step); })(last);
  }
  function stop(){
    running = false;
    cancelAnimationFrame(rafId);
    rafId = null;
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if (en.isIntersecting) start(); else stop();
      });
    }).observe(canvas.parentNode);
  } else {
    start();
  }

  /* ---------- Tema claro/oscuro ---------- */
  var themeObserver = new MutationObserver(function(){
    var nc = themeColors();
    grid.material.color.set(nc.cyan);
  });
  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  /* ---------- Limpieza ---------- */
  window.addEventListener('pagehide', function(){
    stop();
    themeObserver.disconnect();
    renderer.dispose();
    if (renderer.domElement && renderer.domElement.parentNode) {
      renderer.domElement.parentNode.removeChild(renderer.domElement);
    }
  });
})();
