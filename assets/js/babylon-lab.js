/* =========================================================
   AutoCAD Guía — babylon-lab.js
   Laboratorio 3D interactivo del Nivel 4 (Babylon.js).
   Demuestra BOX, EXTRUSIÓN, REVOLUCIÓN, UNIÓN y SUSTRACCIÓN
   con cámara orbital, auto-rotación y temas del sitio.
   ========================================================= */
(function(){
  'use strict';

  var canvas = document.getElementById('babylonCanvas');
  if (!canvas || typeof BABYLON === 'undefined') return;

  var reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

  function supportsWebGL(){
    try {
      return !!(window.WebGLRenderingContext && (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
    } catch (e) {
      return false;
    }
  }
  if (!supportsWebGL()) {
    var stage = canvas.closest('.lab-stage');
    if (stage) {
      stage.innerHTML = '<div class="cad3d-hud">Tu navegador no soporta WebGL. El laboratorio 3D no está disponible.</div>';
    }
    return;
  }

  function cssVar(name){
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }
  function hexToColor4(hex, a){
    hex = (hex || '').replace('#', '');
    if (hex.length !== 6) hex = '0D1526';
    var r = parseInt(hex.substring(0, 2), 16) / 255;
    var g = parseInt(hex.substring(2, 4), 16) / 255;
    var b = parseInt(hex.substring(4, 6), 16) / 255;
    return new BABYLON.Color4(r, g, b, a == null ? 1 : a);
  }
  function themeColors(){
    return {
      bg: cssVar('--bg-panel-2') || '#0D1526',
      cyan: '#35D6CB',
      green: '#7BD87F',
      amber: '#FF9142',
      magenta: '#E36BFF',
      red: '#FF5D5D',
      grid: cssVar('--grid-line-strong') || 'rgba(124,168,230,0.14)'
    };
  }

  function t(key){
    return (window.I18N_SYSTEM && window.I18N_SYSTEM.t) ? I18N_SYSTEM.t(key) : key;
  }

  var engine = new BABYLON.Engine(canvas, true, { preserveDrawingBuffer: false, stencil: false, disableWebGL2Support: false });
  var scene = createScene();
  var current = [];
  var currentOp = 'box';

  function createScene(){
    var sc = new BABYLON.Scene(engine);
    sc.clearColor = hexToColor4(themeColors().bg);

    var camera = new BABYLON.ArcRotateCamera('cam', -Math.PI / 3.4, Math.PI / 2.7, 8, BABYLON.Vector3.Zero(), sc);
    camera.attachControl(canvas, true);
    camera.lowerRadiusLimit = 3;
    camera.upperRadiusLimit = 15;
    camera.minZ = 0.1;
    camera.wheelPrecision = 25;
    if (!reduced) {
      camera.autoRotate = true;
      camera.autoRotateSpeed = 1.1;
    }

    var hemi = new BABYLON.HemisphericLight('hemi', new BABYLON.Vector3(0, 1, 0.4), sc);
    hemi.intensity = 0.95;
    var dir = new BABYLON.DirectionalLight('dir', new BABYLON.Vector3(1, 2, 1.2), sc);
    dir.intensity = 0.85;

    buildGrid(sc);
    return sc;
  }

  function buildGrid(sc){
    var c = themeColors();
    var ground = BABYLON.MeshBuilder.CreateGround('ground', { width: 14, height: 14, subdivisions: 14 }, sc);
    ground.position.y = -1.5;
    var mat = new BABYLON.StandardMaterial('gridMat', sc);
    mat.diffuseColor = new BABYLON.Color3(0.49, 0.66, 0.9);
    mat.emissiveColor = new BABYLON.Color3(0.22, 0.34, 0.5);
    mat.wireframe = true;
    mat.alpha = 0.55;
    ground.material = mat;

    var axes = [
      { pts: [new BABYLON.Vector3(0, -1.5, 0), new BABYLON.Vector3(1.6, -1.5, 0)], color: new BABYLON.Color3(1, 0.36, 0.36) },
      { pts: [new BABYLON.Vector3(0, -1.5, 0), new BABYLON.Vector3(0, 0.1, 0)], color: new BABYLON.Color3(0.48, 0.85, 0.5) },
      { pts: [new BABYLON.Vector3(0, -1.5, 0), new BABYLON.Vector3(0, -1.5, 1.6)], color: new BABYLON.Color3(0.31, 0.55, 1) }
    ];
    axes.forEach(function(a){
      var line = BABYLON.MeshBuilder.CreateLines('axis', { points: a.pts }, sc);
      line.color = a.color;
    });
  }

  function material(name, hex){
    var m = new BABYLON.StandardMaterial(name, scene);
    m.diffuseColor = BABYLON.Color3.FromHexString(hex);
    m.specularColor = new BABYLON.Color3(0.18, 0.18, 0.2);
    m.backFaceCulling = false;
    return m;
  }

  function grow(mesh){
    try {
      BABYLON.Animation.CreateAndStartAnimation(
        'grow', mesh, 'scaling', 30, 20,
        new BABYLON.Vector3(0.001, 0.001, 0.001),
        new BABYLON.Vector3(1, 1, 1),
        BABYLON.Animation.ANIMATIONLOOPMODE_CONSTANT
      );
    } catch (e) {
      mesh.scaling = BABYLON.Vector3.One();
    }
  }

  function clearDemo(){
    current.forEach(function(m){
      if (m.dispose) m.dispose();
    });
    current = [];
  }

  function add(mesh){
    current.push(mesh);
    grow(mesh);
  }

  /* ---------- Operaciones ---------- */
  var OPERATIONS = {
    box: function(){
      var mesh = BABYLON.MeshBuilder.CreateBox('box', { size: 1.9 }, scene);
      mesh.material = material('boxMat', '#35D6CB');
      mesh.position.y = -0.55;
      add(mesh);
    },
    extrude: function(){
      var shape = [
        new BABYLON.Vector3(-0.6, 0, -0.6),
        new BABYLON.Vector3(0.6, 0, -0.6),
        new BABYLON.Vector3(0.6, 0, 0.6),
        new BABYLON.Vector3(-0.6, 0, 0.6)
      ];
      var path = [
        new BABYLON.Vector3(0, -0.5, 0),
        new BABYLON.Vector3(0, 1.6, 0)
      ];
      var mesh = BABYLON.MeshBuilder.CreateExtrudedShape('ext', {
        shape: shape,
        path: path,
        sideOrientation: BABYLON.Mesh.DOUBLESIDE
      }, scene);
      mesh.material = material('extMat', '#FF9142');
      mesh.position.y = -1.0;
      add(mesh);
    },
    revolve: function(){
      var points = [
        new BABYLON.Vector3(0.2, -1.3, 0),
        new BABYLON.Vector3(0.7, -0.9, 0),
        new BABYLON.Vector3(0.95, -0.3, 0),
        new BABYLON.Vector3(0.75, 0.4, 0),
        new BABYLON.Vector3(0.35, 0.9, 0),
        new BABYLON.Vector3(0.2, 1.15, 0)
      ];
      var mesh = BABYLON.MeshBuilder.CreateLathe('rev', {
        shape: points,
        sideOrientation: BABYLON.Mesh.DOUBLESIDE
      }, scene);
      mesh.material = material('revMat', '#E36BFF');
      mesh.position.y = -0.2;
      add(mesh);
    },
    union: function(){
      var a = BABYLON.MeshBuilder.CreateBox('ua', { size: 1.7 }, scene);
      a.position.set(-0.45, 0, 0);
      var b = BABYLON.MeshBuilder.CreateBox('ub', { size: 1.7 }, scene);
      b.position.set(0.45, 0, 0);
      var result = BABYLON.CSG.FromMesh(a).union(BABYLON.CSG.FromMesh(b));
      a.dispose(); b.dispose();
      var mesh = result.toMesh('unionMesh', material('unionMat', '#7BD87F'), scene);
      mesh.position.y = -0.65;
      add(mesh);
    },
    subtract: function(){
      var base = BABYLON.MeshBuilder.CreateBox('subBase', { width: 2.3, height: 1.1, depth: 1.7 }, scene);
      var cutter = BABYLON.MeshBuilder.CreateCylinder('subCutter', { height: 2.4, diameter: 0.62 }, scene);
      cutter.rotation.x = Math.PI / 2;
      var result = BABYLON.CSG.FromMesh(base).subtract(BABYLON.CSG.FromMesh(cutter));
      base.dispose(); cutter.dispose();
      var mesh = result.toMesh('subMesh', material('subMat', '#4FD6E8'), scene);
      mesh.position.y = -0.95;
      add(mesh);
    }
  };

  /* ---------- Controles ---------- */
  var captionEl = document.getElementById('labCaption');
  var buttons = document.querySelectorAll('.lab-btn');

  function runOperation(op){
    clearDemo();
    currentOp = op;
    OPERATIONS[op]();
    if (captionEl) captionEl.textContent = t('lab.caption.' + op);
    canvas.classList.remove('cad3d-fade-in');
    void canvas.offsetWidth; /* reiniciar animación */
    canvas.classList.add('cad3d-fade-in');
  }

  buttons.forEach(function(btn){
    btn.addEventListener('click', function(){
      buttons.forEach(function(b){ b.classList.remove('active'); });
      btn.classList.add('active');
      runOperation(btn.getAttribute('data-lab'));
    });
  });

  runOperation(currentOp);

  /* ---------- Bucle, resize y tema ---------- */
  engine.runRenderLoop(function(){ scene.render(); });

  window.addEventListener('resize', function(){ engine.resize(); });

  new MutationObserver(function(){
    scene.clearColor = hexToColor4(themeColors().bg);
  }).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

  window.addEventListener('pagehide', function(){
    engine.stopRenderLoop();
    engine.dispose();
  });
})();
