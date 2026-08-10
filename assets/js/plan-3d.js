/* =========================================================
   AutoCAD Guía — plan-3d.js
   Convierte el plano del hero en una animación paso a paso:
   1. Líneas de muro · 2. Cotas · 3. Puertas · 4. Ventanas ·
   5. Muebles · 6. Modelado 3D (extrusión con Three.js).
   Requiere anime.js y Three.js (cargados en index.html).
   ========================================================= */
(function(){
  'use strict';

  var svg2d    = document.getElementById('plan2d');
  var canvas3d = document.getElementById('plan3dCanvas');
  var hudText  = document.getElementById('planHudText');
  var replayBtn = document.getElementById('planReplay');
  if (!svg2d || !canvas3d || !hudText || !replayBtn || typeof anime === 'undefined') return;

  var NS = 'http://www.w3.org/2000/svg';
  var K  = 0.04;             // 25 mm = 1 px
  var OX = 36, OY = 36;      // origen del plano en px
  function px(v){ return OX + v * K; }
  function py(v){ return OY + v * K; }
  var TH = 8;                // grosor de muro en px (200 mm)

  var reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

  var C = {
    amber:   'var(--amber)',
    red:     'var(--layer-red)',
    green:   'var(--layer-green)',
    cyan:    'var(--layer-cyan)',
    magenta: 'var(--layer-magenta)'
  };

  var STEP_LABELS = [
    'Paso 1/6 · Líneas de muro',
    'Paso 2/6 · Cotas',
    'Paso 3/6 · Puertas',
    'Paso 4/6 · Ventanas',
    'Paso 5/6 · Muebles',
    'Paso 6/6 · Modelado 3D'
  ];
  function setStep(i){ if (hudText && STEP_LABELS[i]) hudText.textContent = STEP_LABELS[i]; }

  function el(tag, attrs){
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }
  function pencilLine(a, b, col, w){
    var e = el('line', {
      x1: a[0], y1: a[1], x2: b[0], y2: b[1],
      stroke: col, 'stroke-width': w || 2, 'stroke-linecap': 'round',
      'pathLength': 1, 'stroke-dasharray': 1, 'stroke-dashoffset': 1
    });
    svg2d.appendChild(e);
    return e;
  }
  function pencilPath(d, col, w){
    var e = el('path', {
      d: d, fill: 'none', stroke: col, 'stroke-width': w || 1.5, 'stroke-linecap': 'round',
      'pathLength': 1, 'stroke-dasharray': 1, 'stroke-dashoffset': 1
    });
    svg2d.appendChild(e);
    return e;
  }
  function solidRect(r, col){
    var e = el('rect', { x: px(r[0]), y: py(r[1]), width: r[2]*K, height: r[3]*K, rx: 2, fill: col, opacity: 0 });
    svg2d.appendChild(e);
    return e;
  }
  function solidCircle(c){
    var e = el('circle', { cx: px(c[0]), cy: py(c[1]), r: c[2]*K, fill: c[3], opacity: 0 });
    svg2d.appendChild(e);
    return e;
  }

  var anims = [];
  function addAnim(o){ anims.push(o); return o; }
  function hudAt(i, at){
    var d = { v: 0 };
    addAnim(anime({ targets: d, v: 1, duration: 1, delay: at, update: function(){ setStep(i); } }));
  }

  /* ---------- Datos del plano (mm) ---------- */
  var outerSegs = [
    [[0,0],[1200,0]], [[2600,0],[6200,0]],            /* muro superior (hueco W1) */
    [[6200,0],[6200,1200]], [[6200,2600],[6200,4200]],/* muro derecho (hueco W2) */
    [[6200,4200],[3500,4200]], [[2500,4200],[0,4200]],/* muro inferior (hueco D2) */
    [[0,4200],[0,0]]                                  /* muro izquierdo */
  ];
  var intSegs = [
    [[3600,200],[3600,4000]],                         /* tabique A */
    [[200,2100],[2000,2100]], [[3000,2100],[3400,2100]] /* tabique B (hueco D1) */
  ];
  var doors = [
    { hinge: [2500,2100], tip: [2500,3100], edge: [3000,2100] },
    { hinge: [2500,4200], tip: [2500,3200], edge: [3500,4200] }
  ];
  var windows = [
    { a: [1200,-70], b: [2600,-70], c: [1200,70], d: [2600,70],   f: [1200,-70,1400,140] },
    { a: [6130,1200], b: [6130,2600], c: [6270,1200], d: [6270,2600], f: [6130,1200,140,1400] }
  ];
  var furnRects = [
    [400,400,2600,1100], [400,400,900,200],     /* cama + almohada */
    [4000,600,1000,500],                        /* escritorio */
    [300,2500,1200,900], [1700,2900,500,500],   /* sofá + mesita */
    [0,2200,200,1800],                          /* cocina/counter */
    [4600,2600,1000,800]                        /* mesa de comedor */
  ];
  var furnCircles = [
    [5800,3800,300,C.cyan],                     /* columna */
    [100,3200,300,C.cyan]                       /* lavabo */
  ];
  var dims = [
    { kind:'h', y:20,  a:36,  b:284, txt:'6200' },
    { kind:'h', y:27,  a:36,  b:180, txt:'3600' },
    { kind:'h', y:220, a:36,  b:284, txt:'6200' },
    { kind:'v', x:26,  a:36,  b:204, txt:'4200' },
    { kind:'v', x:292, a:36,  b:204, txt:'4200' }
  ];

  function build2D(){
    svg2d.innerHTML = '';
    svg2d.style.opacity = '1';
    setStep(0);

    var defs = el('defs', {});
    var pat = el('pattern', { id: 'planGrid', width: 20, height: 20, patternUnits: 'userSpaceOnUse' });
    pat.appendChild(el('path', { d: 'M20 0H0V20', fill: 'none', stroke: 'var(--border)', 'stroke-width': 0.4 }));
    defs.appendChild(pat);
    svg2d.appendChild(defs);
    svg2d.appendChild(el('rect', { width: 320, height: 240, fill: 'url(#planGrid)' }));

    var wallEls = [];
    outerSegs.forEach(function(s){
      wallEls.push(pencilLine([px(s[0][0]),py(s[0][1])],[px(s[1][0]),py(s[1][1])], C.amber, TH));
    });
    var intEls = [];
    intSegs.forEach(function(s){
      intEls.push(pencilLine([px(s[0][0]),py(s[0][1])],[px(s[1][0]),py(s[1][1])], C.red, TH));
    });

    var cotaEls = [];
    dims.forEach(function(d){
      var green = C.green;
      var e1, e2, dl, t1, t2;
      if (d.kind === 'h'){
        e1 = pencilLine([d.a, 36],[d.a, d.y], green, 0.8);
        e2 = pencilLine([d.b, 36],[d.b, d.y], green, 0.8);
        dl = pencilLine([d.a, d.y],[d.b, d.y], green, 0.8);
        t1 = pencilLine([d.a, d.y-6],[d.a, d.y+6], green, 1);
        t2 = pencilLine([d.b, d.y-6],[d.b, d.y+6], green, 1);
      } else {
        e1 = pencilLine([36, d.a],[d.x, d.a], green, 0.8);
        e2 = pencilLine([36, d.b],[d.x, d.b], green, 0.8);
        dl = pencilLine([d.x, d.a],[d.x, d.b], green, 0.8);
        t1 = pencilLine([d.x-6, d.a],[d.x+6, d.a], green, 1);
        t2 = pencilLine([d.x-6, d.b],[d.x+6, d.b], green, 1);
      }
      var tx = (d.kind === 'h') ? (d.a + d.b) / 2 : d.x;
      var ty = (d.kind === 'h') ? d.y - 4 : (d.a + d.b) / 2;
      var txt = el('text', { x: tx, y: ty, fill: green, 'font-family': "'JetBrains Mono',monospace", 'font-size': 8, 'text-anchor': 'middle', opacity: 0 });
      if (d.kind === 'v') txt.setAttribute('transform', 'rotate(-90 ' + tx + ' ' + ty + ')');
      txt.textContent = d.txt;
      svg2d.appendChild(txt);
      cotaEls.push({ ext: [e1,e2], dl: dl, ticks: [t1,t2], txt: txt });
    });

    var doorEls = [];
    doors.forEach(function(d){
      var leaf = pencilLine([px(d.hinge[0]),py(d.hinge[1])],[px(d.tip[0]),py(d.tip[1])], C.cyan, 2.5);
      var arc = pencilPath('M ' + px(d.tip[0]) + ' ' + py(d.tip[1]) + ' A 1000 1000 0 0 0 ' + px(d.edge[0]) + ' ' + py(d.edge[1]), C.cyan, 1.5);
      doorEls.push({ leaf: leaf, arc: arc });
    });

    var winEls = [];
    windows.forEach(function(w){
      var l1 = pencilLine([px(w.a[0]),py(w.a[1])],[px(w.b[0]),py(w.b[1])], C.cyan, 3);
      var l2 = pencilLine([px(w.c[0]),py(w.c[1])],[px(w.d[0]),py(w.d[1])], C.cyan, 3);
      var glass = el('rect', { x: px(w.f[0]), y: py(w.f[1]), width: w.f[2]*K, height: w.f[3]*K, fill: C.cyan, opacity: 0 });
      svg2d.appendChild(glass);
      winEls.push({ l1: l1, l2: l2, glass: glass });
    });

    var furnEls = [];
    furnRects.forEach(function(r){ furnEls.push(solidRect(r, C.magenta)); });
    furnCircles.forEach(function(c){ furnEls.push(solidCircle(c)); });

    return { wallEls: wallEls, intEls: intEls, cotaEls: cotaEls, doorEls: doorEls, winEls: winEls, furnEls: furnEls };
  }

  function runTimeline(els){
    var D = function(v){ return reduced ? 0 : v; };
    var t = 0;

    hudAt(0, 0);
    els.wallEls.forEach(function(l){
      addAnim(anime({ targets: l, strokeDashoffset: [1,0], duration: D(700)+2, delay: t, easing: 'easeInOutSine' }));
      t += D(130);
    });
    els.intEls.forEach(function(l){
      addAnim(anime({ targets: l, strokeDashoffset: [1,0], duration: D(700)+2, delay: t, easing: 'easeInOutSine' }));
      t += D(120);
    });

    t += D(250); hudAt(1, t);
    els.cotaEls.forEach(function(c){
      c.ext.forEach(function(e){
        addAnim(anime({ targets: e, strokeDashoffset: [1,0], duration: D(450)+2, delay: t, easing: 'easeInOutSine' }));
      });
      addAnim(anime({ targets: c.dl, strokeDashoffset: [1,0], duration: D(450)+2, delay: t + D(120), easing: 'easeInOutSine' }));
      c.ticks.forEach(function(tk){
        addAnim(anime({ targets: tk, strokeDashoffset: [1,0], duration: D(300)+2, delay: t + D(220), easing: 'easeInOutSine' }));
      });
      addAnim(anime({ targets: c.txt, opacity: [0,1], duration: D(400)+2, delay: t + D(260), easing: 'easeOutQuad' }));
      t += D(160);
    });

    t += D(250); hudAt(2, t);
    els.doorEls.forEach(function(d){
      addAnim(anime({ targets: d.leaf, strokeDashoffset: [1,0], duration: D(500)+2, delay: t, easing: 'easeOutQuad' }));
      addAnim(anime({ targets: d.arc, strokeDashoffset: [1,0], duration: D(600)+2, delay: t + D(120), easing: 'easeInOutSine' }));
      t += D(320);
    });

    t += D(250); hudAt(3, t);
    els.winEls.forEach(function(w){
      addAnim(anime({ targets: [w.l1,w.l2], strokeDashoffset: [1,0], duration: D(450)+2, delay: t, easing: 'easeInOutSine' }));
      addAnim(anime({ targets: w.glass, opacity: [0,0.14], duration: D(500)+2, delay: t + D(180), easing: 'easeOutQuad' }));
      t += D(200);
    });

    t += D(250); hudAt(4, t);
    els.furnEls.forEach(function(f, i){
      var target = f.tagName === 'circle' ? 0.45 : (i < 4 ? 0.55 : 0.85);
      addAnim(anime({ targets: f, opacity: [0, target], duration: D(500)+2, delay: t + D(i*90), easing: 'easeOutQuad' }));
    });

    t += D(400);
    return t;
  }

  /* ------------------- 3D (Three.js) ------------------- */
  var renderer = null, scene = null, camera = null, group = null;
  var walls = [], risers = [], faders = [];
  var running = false, rafId = null, autorotate = false, last = 0;

  function cssVar(name){ return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
  function threeColor(name, fb){
    var v = cssVar(name);
    return v ? new THREE.Color(v) : new THREE.Color(fb || '#35D6CB');
  }
  function supportsWebGL(){
    try {
      var c = document.createElement('canvas');
      return !!(window.WebGLRenderingContext && (c.getContext('webgl') || c.getContext('experimental-webgl')));
    } catch(e){ return false; }
  }
  function boxFromFloor(w, h, d, mat){
    var g = new THREE.BoxGeometry(w, h, d);
    g.translate(0, h/2, 0);
    return new THREE.Mesh(g, mat);
  }
  function addRiser(m){ risers.push(m); group.add(m); }

  function build3D(){
    if (typeof THREE === 'undefined' || !supportsWebGL()) return false;

    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(42, 1, 0.1, 100);
    camera.position.set(0.5, 9, 5.5);
    camera.lookAt(0, 1, 0);

    renderer = new THREE.WebGLRenderer({ canvas: canvas3d, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setClearColor(0x000000, 0);

    scene.add(new THREE.HemisphereLight(0xffffff, 0x223344, 1.1));
    var dir = new THREE.DirectionalLight(0xffffff, 1.4);
    dir.position.set(5, 9, 4); scene.add(dir);
    var fill = new THREE.DirectionalLight(0x88ccff, 0.4);
    fill.position.set(-5, 3, -6); scene.add(fill);

    group = new THREE.Group();
    scene.add(group);

    var grid = new THREE.GridHelper(9, 9, threeColor('--layer-cyan'), threeColor('--layer-cyan'));
    grid.material.transparent = true;
    grid.material.opacity = 0.25;
    grid.position.y = 0.02;
    scene.add(grid);

    var matWall  = new THREE.MeshPhongMaterial({ color: threeColor('--amber','#FF9142'), flatShading: true });
    var matInner = new THREE.MeshPhongMaterial({ color: threeColor('--layer-red','#FF5D5D'), flatShading: true });
    var matDoor  = new THREE.MeshPhongMaterial({ color: threeColor('--amber','#FF9142'), flatShading: true });
    var matGlass = new THREE.MeshPhongMaterial({ color: threeColor('--layer-cyan','#35D6CB'), transparent: true, opacity: 0, side: THREE.DoubleSide });
    var matFloor = new THREE.MeshPhongMaterial({ color: threeColor('--bg-panel','#0B1220') });
    var matFurn  = new THREE.MeshPhongMaterial({ color: threeColor('--layer-magenta','#E36BFF'), flatShading: true });
    var matCol   = new THREE.MeshPhongMaterial({ color: threeColor('--layer-cyan','#35D6CB'), flatShading: true });

    var floor = boxFromFloor(6.8, 0.12, 4.6, matFloor);
    floor.position.y = -0.12;
    group.add(floor);

    var outerWalls = [
      [-2.5,-2.1, 1.2, 0.2], [ 1.3,-2.1, 3.6, 0.2],
      [ 3.2,-1.5, 0.2, 1.2], [ 3.2, 1.3, 0.2, 1.6],
      [ 1.75, 2.1, 2.7, 0.2], [-1.85, 2.1, 2.5, 0.2],
      [-3.2, 0, 0.2, 4.2]
    ];
    outerWalls.forEach(function(w){
      var m = boxFromFloor(w[2], 2.8, w[3], matWall);
      m.position.set(w[0], 0, w[1]);
      m.scale.y = 0.01;
      walls.push(m); group.add(m);
    });
    var innerWalls = [
      [0.5, 0, 0.2, 3.8],
      [-2.0, 0, 1.8, 0.2], [0.1, 0, 0.4, 0.2]
    ];
    innerWalls.forEach(function(w){
      var m = boxFromFloor(w[2], 2.8, w[3], matInner);
      m.position.set(w[0], 0, w[1]);
      m.scale.y = 0.01;
      walls.push(m); group.add(m);
    });

    var d1 = boxFromFloor(1.0, 2.1, 0.05, matDoor);
    d1.position.set(-0.6, 0, 0); d1.rotation.y = 0.5; d1.scale.y = 0.01; addRiser(d1);
    var d2 = boxFromFloor(1.0, 2.1, 0.05, matDoor);
    d2.position.set(-0.1, 0, 2.1); d2.rotation.y = -0.5; d2.scale.y = 0.01; addRiser(d2);

    var g1 = new THREE.Mesh(new THREE.BoxGeometry(1.4, 1.2, 0.04), matGlass);
    g1.position.set(-1.2, 1.5, -2.1); faders.push(g1); group.add(g1);
    var g2 = new THREE.Mesh(new THREE.BoxGeometry(0.04, 1.2, 1.4), matGlass);
    g2.position.set(3.2, 1.5, -0.2); faders.push(g2); group.add(g2);

    var col = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 2.8, 24), matCol);
    col.geometry.translate(0, 1.4, 0);
    col.position.set(2.7, 0, 1.7);
    col.scale.y = 0.01;
    addRiser(col);

    var furn3d = [
      [-1.4, -1.15, 2.6, 1.1, 0.35],   /* cama */
      [ 1.4, -1.25, 1.0, 0.5, 0.75],   /* escritorio */
      [-2.2,  0.85, 1.2, 0.9, 0.80],   /* sofá */
      [-1.15, 1.05, 0.5, 0.5, 0.35],   /* mesita */
      [ 2.0,  0.90, 1.0, 0.8, 0.75],   /* mesa comedor */
      [-3.0,  1.00, 0.2, 1.8, 0.90]    /* cocina */
    ];
    furn3d.forEach(function(f){
      var m = boxFromFloor(f[2], f[4], f[3], matFurn);
      m.position.set(f[0], 0, f[1]);
      m.scale.y = 0.01;
      addRiser(m);
    });

    canvas3d.style.display = 'block';
    resize();
    return true;
  }

  function animate3DIntro(t){
    if (reduced){
      walls.forEach(function(m){ m.scale.y = 1; });
      risers.forEach(function(m){ m.scale.y = 1; });
      faders.forEach(function(m){ m.material.opacity = 0.4; });
      camera.position.set(7, 6.5, 8);
      camera.lookAt(0, 1, 0);
      autorotate = true;
      return;
    }
    addAnim(anime({
      targets: camera.position, x: 7, y: 6.5, z: 8,
      duration: 2400, delay: t, easing: 'easeInOutCubic',
      update: function(){ camera.lookAt(0, 1, 0); },
      complete: function(){ autorotate = true; }
    }));
    var risers3 = walls.concat(risers).map(function(m){ return m.scale; });
    addAnim(anime({
      targets: risers3, y: 1,
      duration: 1500, delay: function(el, i){ return t + 350 + i * 80; },
      easing: 'easeOutBack'
    }));
    addAnim(anime({ targets: faders.map(function(m){ return m.material; }), opacity: 0.4, duration: 1200, delay: t + 800, easing: 'easeOutQuad' }));
  }

  function resize(){
    if (!renderer) return;
    var w = svg2d.parentNode.clientWidth || 300;
    var h = svg2d.parentNode.clientHeight || 225;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  }
  window.addEventListener('resize', resize);
  if (window.ResizeObserver) new ResizeObserver(resize).observe(svg2d.parentNode);

  function renderLoop(now){
    if (!running) return;
    if (now && last){
      var dt = Math.min((now - last) / 1000, 0.05);
      if (autorotate && group) group.rotation.y += dt * 0.06;
    }
    last = now;
    if (renderer && scene && camera) renderer.render(scene, camera);
    rafId = requestAnimationFrame(renderLoop);
  }
  function startRaf(){ if (running || !renderer) return; running = true; last = 0; rafId = requestAnimationFrame(renderLoop); }
  function stopRaf(){ running = false; if (rafId) cancelAnimationFrame(rafId); rafId = null; }
  if ('IntersectionObserver' in window){
    new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if (en.isIntersecting) startRaf(); else stopRaf();
      });
    }).observe(svg2d.parentNode);
  } else {
    startRaf();
  }

  var dragging = false, dpx = 0, dpy = 0;
  canvas3d.addEventListener('pointerdown', function(e){ dragging = true; dpx = e.clientX; dpy = e.clientY; });
  window.addEventListener('pointermove', function(e){
    if (!dragging || !group) return;
    group.rotation.y += (e.clientX - dpx) * 0.008;
    group.rotation.x += (e.clientY - dpy) * 0.004;
    group.rotation.x = Math.max(-1.1, Math.min(1.1, group.rotation.x));
    dpx = e.clientX; dpy = e.clientY;
  });
  window.addEventListener('pointerup', function(){ dragging = false; });

  function stop3D(){
    anims.forEach(function(a){ try { a.pause(); } catch(e){} });
    anims.length = 0;
    if (renderer){
      stopRaf();
      walls = []; risers = []; faders = [];
      try { renderer.dispose(); } catch(e){}
      renderer = null; scene = null; camera = null; group = null;
      canvas3d.style.display = 'none';
    }
    autorotate = false;
  }

  function start(){
    var els = build2D();
    var t = runTimeline(els);
    var ok3d = build3D();
    if (ok3d){
      hudAt(5, t + (reduced ? 0 : 300));
      addAnim(anime({ targets: svg2d, opacity: 0, duration: reduced ? 2 : 800, delay: t + (reduced ? 0 : 300), easing: 'easeInOutQuad' }));
      animate3DIntro(t + (reduced ? 0 : 300));
    }
  }

  replayBtn.addEventListener('click', function(){ stop3D(); start(); });

  var started = false;
  function boot(){
    if (started) return;
    started = true;
    start();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();

  window.addEventListener('pagehide', function(){ stop3D(); });
})();
