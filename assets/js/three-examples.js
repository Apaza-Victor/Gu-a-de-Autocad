/* =========================================================
   AutoCAD Guía — three-examples.js
   Mini visores 3D (Three.js) en ejemplos-visuales.html.
   Cada panel con data-mini3d construye una geometría 3D
   (extrude / revolve / boolean) con auto-rotación y drag.
   ========================================================= */
(function(){
  'use strict';

  if (typeof THREE === 'undefined') return;

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

  var panels = document.querySelectorAll('[data-mini3d]');
  if (!panels.length) return;

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
      red: color('--layer-red', '#FF5D5D')
    };
  }

  function makeSolid(geo, base){
    var m = new THREE.MeshPhongMaterial({ color: base, transparent: true, opacity: 0.94, flatShading: true, side: THREE.DoubleSide });
    return new THREE.Mesh(geo, m);
  }

  function buildObject(kind, group, c){
    if (kind === 'extrude') {
      var shape = new THREE.Shape();
      shape.moveTo(0, 0.85);
      shape.lineTo(0.22, 0.26);
      shape.lineTo(0.85, 0.26);
      shape.lineTo(0.34, -0.1);
      shape.lineTo(0.55, -0.7);
      shape.lineTo(0, -0.34);
      shape.lineTo(-0.55, -0.7);
      shape.lineTo(-0.34, -0.1);
      shape.lineTo(-0.85, 0.26);
      shape.lineTo(-0.22, 0.26);
      shape.closePath();
      var m = makeSolid(new THREE.ExtrudeGeometry(shape, { depth: 1.2, bevelEnabled: false }), c.cyan);
      m.position.y = -0.6;
      group.add(m);
    } else if (kind === 'revolve') {
      var pts = [];
      for (var i = 0; i <= 28; i++) {
        var t = i / 28;
        pts.push(new THREE.Vector2(0.15 + Math.sin(t * Math.PI) * 0.65, t * 1.6));
      }
      var vase = makeSolid(new THREE.LatheGeometry(pts, 40), c.magenta);
      vase.position.y = -0.8;
      group.add(vase);
    } else if (kind === 'boolean') {
      var box = makeSolid(new THREE.BoxGeometry(1.7, 0.95, 1.2), c.green);
      box.position.y = -0.475;
      group.add(box);
      var hole = makeSolid(new THREE.CylinderGeometry(0.36, 0.36, 1.8, 28), c.red);
      hole.rotation.x = Math.PI / 2;
      hole.position.y = -0.475;
      group.add(hole);
    }
  }

  panels.forEach(function(panel){
    var host = panel.querySelector('.cad3d-mini-canvas');
    if (!host) return;
    var kind = panel.getAttribute('data-mini3d');

    var c = themeColors();
    var scene = new THREE.Scene();
    scene.background = new THREE.Color(c.bg);

    var camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100);
    camera.position.set(3.2, 2.7, 4.2);
    camera.lookAt(0, 0, 0);

    var renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setClearColor(new THREE.Color(c.bg));
    host.appendChild(renderer.domElement);

    scene.add(new THREE.HemisphereLight(0xffffff, 0x223344, 1.2));
    var dir = new THREE.DirectionalLight(0xffffff, 1.5);
    dir.position.set(3, 5, 4);
    scene.add(dir);

    var group = new THREE.Group();
    scene.add(group);

    var grid = new THREE.GridHelper(6, 6, c.cyan, c.cyan);
    grid.material.transparent = true;
    grid.material.opacity = 0.26;
    grid.position.y = -1.15;
    scene.add(grid);

    buildObject(kind, group, c);

    var rafId = null;
    var dragging = false, prevX = 0, prevY = 0;
    var autoRotate = !reduced;
    var last = 0;

    var el = renderer.domElement;
    el.addEventListener('pointerdown', function(e){
      dragging = true;
      prevX = e.clientX; prevY = e.clientY;
    });
    window.addEventListener('pointermove', function(e){
      if (!dragging) return;
      var dx = e.clientX - prevX;
      var dy = e.clientY - prevY;
      prevX = e.clientX; prevY = e.clientY;
      group.rotation.y += dx * 0.01;
      group.rotation.x += dy * 0.005;
      group.rotation.x = Math.max(-1.2, Math.min(1.2, group.rotation.x));
    });
    window.addEventListener('pointerup', function(){ dragging = false; });
    el.addEventListener('wheel', function(e){
      e.preventDefault();
      var s = e.deltaY > 0 ? 1.08 : 0.92;
      camera.position.multiplyScalar(s);
      camera.position.y = Math.max(1.2, Math.min(8, camera.position.y));
    }, { passive: false });

    function resize(){
      var w = host.clientWidth || 1;
      var h = host.clientHeight || 1;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    }
    if (window.ResizeObserver) new ResizeObserver(resize).observe(host);
    resize();

    function loop(now){
      if (autoRotate && !dragging) group.rotation.y += ((now - last) / 1000) * 0.35;
      last = now;
      renderer.render(scene, camera);
    }
    function start(){
      cancelAnimationFrame(rafId);
      last = performance.now();
      (function step(now){ loop(now); rafId = requestAnimationFrame(step); })(last);
    }
    function stop(){ cancelAnimationFrame(rafId); rafId = null; }

    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if (entry.isIntersecting) start();
        else stop();
      });
    });
    io.observe(host);

    var themeObs = new MutationObserver(function(){
      var nc = themeColors();
      scene.background.set(nc.bg);
      renderer.setClearColor(new THREE.Color(nc.bg));
      grid.material.color.set(nc.cyan);
    });
    themeObs.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

    window.addEventListener('pagehide', function(){
      stop();
      io.disconnect();
      themeObs.disconnect();
      if (renderer) {
        renderer.dispose();
        if (renderer.domElement && renderer.domElement.parentNode) {
          renderer.domElement.parentNode.removeChild(renderer.domElement);
        }
      }
    });
  });
})();
