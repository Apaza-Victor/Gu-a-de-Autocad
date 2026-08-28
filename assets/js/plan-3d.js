/* =========================================================
   AutoCAD Guía — plan-3d.js
   Plano de planta (2D) animado y modelado 3D de la vivienda:
   1. Muros · 2. Cotas · 3. Puertas · 4. Ventanas · 5. Mobiliario
   6. Construcción 3D por fases: losa, muros con vanos reales,
   puertas, ventanas, mobiliario y cubierta.
   Requiere anime.js y Three.js (cargados en index.html).
   ========================================================= */
(function(){
  'use strict';

  var svg2d     = document.getElementById('plan2d');
  var canvas3d  = document.getElementById('plan3dCanvas');
  var hudText   = document.getElementById('planHudText');
  var replayBtn = document.getElementById('planReplay');
  var btn2D     = document.getElementById('planView2D');
  var btn3D     = document.getElementById('planView3D');
  if (!svg2d || !canvas3d || !hudText || !replayBtn || typeof anime === 'undefined') return;

  var NS = 'http://www.w3.org/2000/svg';
  var K  = 0.04;                 // 25 mm = 1 px
  var OX = 30, OY = 26;          // origen en px
  function px(v){ return OX + v * K; }
  function py(v){ return OY + v * K; }
  var TH  = 5;                   // grosor muro (px)
  var W   = 6200, H = 4200;      // dimensiones planta (mm)

  var reduced = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);

  var C = {
    amber:   'var(--amber)',
    red:     'var(--layer-red)',
    green:   'var(--layer-green)',
    cyan:    'var(--layer-cyan)',
    magenta: 'var(--layer-magenta)'
  };

  /* ------------------------------------------------------------------
     Datos del plano (mm). Muros como línea central + vanos {d0,d1,...}
     donde d se mide desde el punto a -> b de cada muro.
     ------------------------------------------------------------------ */
  var WALLS = [
    { a:[0,0],     b:[W,0],    kind:'outer',
      vanos:[ {d0:4000,d1:4800, kind:'win',  sill:950, top:2400},
              {d0:700, d1:1500, kind:'win',  sill:950, top:2400} ] },
    { a:[W,4200],  b:[0,4200], kind:'outer',
      vanos:[ {d0:3800,d1:4600, kind:'door', top:2100},
              {d0:5200,d1:6000, kind:'win',  sill:950, top:2400} ] },
    { a:[0,0],     b:[0,H],    kind:'outer',
      vanos:[ {d0:3000,d1:3600, kind:'win', sill:950, top:2400} ] },
    { a:[W,0],     b:[W,H],    kind:'outer',
      vanos:[ {d0:600, d1:1400, kind:'win', sill:950, top:2400} ] },
    { a:[3400,200], b:[3400,H], kind:'inner',
      vanos:[ {d0:2700,d1:3500, kind:'door', top:2100} ] },
    { a:[200,2000], b:[3200,2000], kind:'inner',
      vanos:[ {d0:1500,d1:2300, kind:'door', top:2100} ] },
    { a:[3600,2000], b:[6000,2000], kind:'inner',
      vanos:[ {d0:4800,d1:5600, kind:'door', top:2100} ] },
    { a:[200,2600], b:[1200,2600], kind:'inner',
      vanos:[ {d0:500,d1:900, kind:'door', top:2100} ] },
    { a:[1200,2600], b:[1200,H], kind:'inner', vanos:[] }
  ];

  var DOORS = [
    { hinge:[3800,4200,0], edge:[4600,4200,0], w:800, h:2100 },
    { hinge:[1500,2000,0], edge:[2300,2000,0], w:800, h:2100 },
    { hinge:[4800,2000,0], edge:[5600,2000,0], w:800, h:2100 },
    { hinge:[500,2600,0],  edge:[900,2600,0],  w:400, h:2100 },
    { hinge:[3400,2700,0], edge:[3400,3500,0], w:800, h:2100 }
  ];

  var FURN = {
    bed:    { x:340,  y:340,  w:2200, h:1500 },
    dresser:{ x:530,  y:1650, w:1500, h:280 },
    sofa:   { x:4000, y:380,  w:1400, h:520 },
    coffee: { x:4400, y:1000, w:700,  h:380 },
    tv:     { x:3340, y:520,  w:900,  h:120 },
    dining: { x:5200, y:1000, r:620 },
    kcount: { x:3600, y:2300, w:900,  h:600 },
    stove:  { x:4800, y:2300, w:700,  h:600 },
    fridge: { x:5800, y:3600, w:300,  h:600 },
    sink:   { x:5450, y:3350, w:500,  h:500 },
    toilet: { x:360,  y:3800, w:450,  h:360 },
    tub:    { x:1050, y:3300, w:300,  h:1500 },
    basin:  { x:400,  y:2900, w:420,  h:300 },
    plant1: { x:3500, y:900,  r:150 },
    plant2: { x:6100, y:380,  r:150 }
  };

  var STEP_LABELS = [
    'Paso 1/6 · Muros',
    'Paso 2/6 · Cotas',
    'Paso 3/6 · Puertas',
    'Paso 4/6 · Ventanas',
    'Paso 5/6 · Mobiliario',
    'Paso 6/6 · Construcción 3D'
  ];
  function setStep(i){ if (hudText && STEP_LABELS[i]) hudText.textContent = STEP_LABELS[i]; }

  function el(tag, attrs){
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    return e;
  }
  function pencil(a, b, col, w){
    var e = el('line', { x1:a[0], y1:a[1], x2:b[0], y2:b[1], stroke:col,
      'stroke-width':w||1.5, 'stroke-linecap':'round', 'pathLength':1,
      'stroke-dasharray':1, 'stroke-dashoffset':1 });
    svg2d.appendChild(e);
    return e;
  }
  function grp(){
    var e = el('g', { opacity:0 });
    svg2d.appendChild(e);
    return e;
  }
  function rectIn(g, x, y, w, h, fill, rx, op){
    var e = el('rect', { x:x, y:y, width:w, height:h, rx:rx||2, fill:fill,
      opacity: op==null?1:op });
    g.appendChild(e); return e;
  }
  function circIn(g, cx, cy, r, fill){
    var e = el('circle', { cx:cx, cy:cy, r:r, fill:fill });
    g.appendChild(e); return e;
  }

  var anims = [];
  function addAnim(o){ anims.push(o); return o; }
  function hudAt(i, at){
    var d = { v:0 };
    addAnim(anime({ targets:d, v:1, duration:1, delay:at, update:function(){ setStep(i); } }));
  }

  /* ===================== 2D ===================== */
  function build2D(){
    svg2d.innerHTML = '';
    svg2d.style.opacity = '1';
    setStep(0);

    var defs = el('defs');

    var pat = el('pattern', { id:'planGrid', width:20, height:20, patternUnits:'userSpaceOnUse' });
    pat.appendChild(el('path', { d:'M20 0H0V20', fill:'none', stroke:'var(--border)', 'stroke-width':0.5 }));
    defs.appendChild(pat);

    var glow = el('radialGradient', { id:'planGlow', cx:'50%', cy:'42%', r:'78%' });
    glow.appendChild(el('stop', { offset:'0%',   'stop-color':'var(--layer-cyan)', 'stop-opacity':0.12 }));
    glow.appendChild(el('stop', { offset:'70%',  'stop-color':'var(--layer-cyan)', 'stop-opacity':0.04 }));
    glow.appendChild(el('stop', { offset:'100%', 'stop-color':'var(--layer-cyan)', 'stop-opacity':0 }));
    defs.appendChild(glow);

    var arrow = el('marker', { id:'arrowN', markerWidth:8, markerHeight:8, refX:4, refY:2, orient:'auto' });
    arrow.appendChild(el('path', { d:'M0 0 L4 7 L8 0', fill:'none', stroke:'var(--layer-red)', 'stroke-width':1.2 }));
    defs.appendChild(arrow);
    svg2d.appendChild(defs);

    svg2d.appendChild(el('rect', { width:320, height:240, fill:'url(#planGrid)' }));
    svg2d.appendChild(el('rect', { x:0, y:0, width:320, height:240, fill:'url(#planGlow)' }));

    var els = { walls:[], dims:[], doors:[], wins:[], furn:null, rooms:[], fade:[], floors:[] };

    /* losa / huella exterior */
    function rectFade(x, y, w, h, fill, stroke, sw, rx){
      var r = el('rect', { x:x, y:y, width:w, height:h, rx:rx||3, fill:fill,
        stroke:stroke||'none', 'stroke-width':sw||0.6, opacity:0 });
      svg2d.appendChild(r);
      els.floors.push(r);
      return r;
    }
    rectFade(px(0)-6, py(0)-6, W*K+12, H*K+12, 'var(--bg-panel-2)', 'var(--border)', 0.8, 3);

    /* relleno suave por estancia */
    var ROOMS = [
      { x:120,  y:120,  w:2600, h:1400, label:'HABITACIÓN', fill:'rgba(79,214,232,.07)' },
      { x:3700, y:260,  w:2100, h:1200, label:'SALÓN',      fill:'rgba(255,145,66,.07)' },
      { x:3600, y:2300, w:2200, h:1500, label:'COCINA',     fill:'rgba(123,216,127,.07)' },
      { x:260,  y:2800, w:950,  h:1200, label:'BAÑO',       fill:'rgba(79,214,232,.055)' },
      { x:1500, y:2500, w:1500, h:1100, label:'HALL',       fill:'rgba(227,107,255,.05)' }
    ];
    els.furn = grp();
    ROOMS.forEach(function(r){
      rectFade(px(r.x)-6, py(r.y)-6, r.w*K+12, r.h*K+12, r.fill, 'var(--border-soft)', 0.5, 3);
    });

    /* brújula N */
    var north = grp();
    var nShadow = el('circle', { cx:298, cy:32, r:16, fill:'var(--bg-panel)', stroke:'var(--border)', 'stroke-width':0.6, opacity:0.7 });
    north.appendChild(nShadow);
    north.appendChild(el('line', { x1:298, y1:24, x2:298, y2:46, stroke:'var(--layer-red)',
      'stroke-width':1.4, 'marker-end':'url(#arrowN)' }));
    var nT = el('text', { x:298, y:19, fill:'var(--layer-red)', 'font-family':"JetBrains Mono,monospace",
      'font-size':6.5, 'text-anchor':'middle', 'font-weight':700 });
    nT.textContent = 'N';
    north.appendChild(nT);
    els.fade.push(north);

    /* título y escala */
    var titleGrp = grp();
    var t1 = el('text', { x:12, y:14, fill:'var(--text)', 'font-family':"JetBrains Mono,monospace",
      'font-size':7, 'font-weight':700, 'letter-spacing':'0.12em' });
    t1.textContent = 'PLANTA 1:50';
    var t2 = el('text', { x:12, y:22, fill:'var(--text-faint)', 'font-family':"JetBrains Mono,monospace", 'font-size':5.5 });
    t2.textContent = 'VIVIENDA 6200×4200 mm';
    titleGrp.appendChild(t1); titleGrp.appendChild(t2);
    els.fade.push(titleGrp);

    /* muros (línea gruesa dibujada) */
    WALLS.forEach(function(w){
      var col = w.kind==='outer' ? C.amber : C.red;
      els.walls.push(pencil([px(w.a[0]),py(w.a[1])],[px(w.b[0]),py(w.b[1])], col, TH));
    });

    /* Cotas (verde) */
    var DIMS = [
      { kind:'h', y:12,  a:24, b:312, txt:'6200' },
      { kind:'h', y:19,  a:24, b:78,  txt:'2000' },
      { kind:'h', y:232, a:24, b:312, txt:'6200' },
      { kind:'h', y:60,  a:24, b:156, txt:'3200' },
      { kind:'v', x:16,  a:26, b:194, txt:'4200' },
      { kind:'v', x:326, a:26, b:194, txt:'4200' }
    ];
    DIMS.forEach(function(d){
      var g = C.green, cell=[];
      if (d.kind==='h'){
        cell.push(pencil([d.a,py(0)],[d.a,d.y],g,0.8));
        cell.push(pencil([d.b,py(0)],[d.b,d.y],g,0.8));
        cell.push(pencil([d.a,d.y],[d.b,d.y],g,0.8));
        cell.push(pencil([d.a,d.y-4],[d.a,d.y+4],g,1));
        cell.push(pencil([d.b,d.y-4],[d.b,d.y+4],g,1));
        var tx=el('text',{ x:(d.a+d.b)/2, y:d.y-3, fill:g, 'font-family':"JetBrains Mono,monospace",
          'font-size':7, 'text-anchor':'middle', opacity:0 });
        tx.textContent=d.txt; svg2d.appendChild(tx);
        cell.push(tx);
      } else {
        cell.push(pencil([px(0),d.a],[d.x,d.a],g,0.8));
        cell.push(pencil([px(0),d.b],[d.x,d.b],g,0.8));
        cell.push(pencil([d.x,d.a],[d.x,d.b],g,0.8));
        cell.push(pencil([d.x-4,d.a],[d.x+4,d.a],g,1));
        cell.push(pencil([d.x-4,d.b],[d.x+4,d.b],g,1));
        var ty=(d.a+d.b)/2;
        var tv=el('text',{ x:d.x+4, y:ty, fill:g, 'font-family':"JetBrains Mono,monospace",
          'font-size':7, 'text-anchor':'middle', opacity:0 });
        tv.textContent=d.txt; svg2d.appendChild(tv);
        cell.push(tv);
      }
      els.dims.push(cell);
    });

    /* rótulos de estancias (chip) */
    ROOMS.forEach(function(r){
      var cx=px(r.x+r.w/2), cy=py(r.y+r.h/2);
      var t=el('text',{ x:cx, y:cy+1, fill:'var(--text)', 'font-family':"JetBrains Mono,monospace",
        'font-size':8, 'text-anchor':'middle', 'letter-spacing':'0.10em', 'font-weight':700,
        opacity:0 });
      t.textContent=r.label;
      svg2d.appendChild(t);
      var chip=el('rect',{ x:cx-30, y:cy-6, width:60, height:13, rx:3,
        fill:'var(--bg-panel)', stroke:'var(--border-soft)', 'stroke-width':0.5, opacity:0 });
      svg2d.appendChild(chip);
      els.rooms.push(t); els.rooms.push(chip);
    });

    /* puertas */
    DOORS.forEach(function(d){
      var g=grp();
      var leaf=el('line',{ x1:px(d.hinge[0]),y1:py(d.hinge[1]),x2:px(d.edge[0]),y2:py(d.edge[1]),
        stroke:C.cyan,'stroke-width':2.5,'stroke-linecap':'round' });
      var arc=el('path',{ d:'M '+px(d.hinge[0])+' '+py(d.hinge[1])+' A '+(d.w*K)+' '+(d.w*K)+' 0 0 1 '+px(d.edge[0])+' '+py(d.edge[1]),
        fill:'none',stroke:C.cyan,'stroke-width':1.2,opacity:0.7 });
      g.appendChild(leaf); g.appendChild(arc);
      els.doors.push(g);
    });

    /* ventanas (marco + vidrio) */
    var WIN_DATA = [
      { a:[4000,-90], b:[4800,-90], c:[4000,90],  d:[4800,90],  f:[4000,-90,800,180] },
      { a:[700,-90],  b:[1500,-90], c:[700,90],   d:[1500,90],  f:[700,-90,800,180]  },
      { a:[-90,3000], b:[-90,3600], c:[90,3000],  d:[90,3600],  f:[-90,3000,180,600] },
      { a:[W+90,600], b:[W+90,1400],c:[W-90,600], d:[W-90,1400],f:[W-90,600,180,800] },
      { a:[5200,H+90],b:[6000,H+90],c:[5200,H-90],d:[6000,H-90],f:[5200,H-90,800,180] }
    ];
    WIN_DATA.forEach(function(wd){
      var g=grp();
      var l1=el('line',{x1:px(wd.a[0]),y1:py(wd.a[1]),x2:px(wd.b[0]),y2:py(wd.b[1]),stroke:C.cyan,'stroke-width':3});
      var l2=el('line',{x1:px(wd.c[0]),y1:py(wd.c[1]),x2:px(wd.d[0]),y2:py(wd.d[1]),stroke:C.cyan,'stroke-width':3});
      g.appendChild(l1); g.appendChild(l2);
      var midX=(px(wd.a[0])+px(wd.b[0]))/2, midY=(py(wd.a[1])+py(wd.b[1]))/2;
      g.appendChild(el('line',{x1:midX,y1:midY-7,x2:midX,y2:midY+7,stroke:C.cyan,'stroke-width':0.8,opacity:0.6}));
      var glass=el('rect',{x:px(wd.f[0]),y:py(wd.f[1]),width:wd.f[2]*K,height:wd.f[3]*K,fill:C.cyan,opacity:0});
      g.appendChild(glass);
      els.wins.push(g);
      g._glass = glass;
    });

    /* mobiliario */
    var fur = els.furn;
    var MG = 'rgba(227,107,255,.85)';      // trazo magenta (muebles)
    var FAC = 'rgba(227,107,255,.22)';     // relleno magenta
    function rr(x, y, w, h, col, rx, o){
      rectIn(fur, x, y, w, h, col, rx==null?2:rx, o);
    }
    function ov(cx, cy, rx, ry, col, o){
      var e=el('ellipse',{ cx:cx, cy:cy, rx:rx, ry:ry, fill:col, opacity:o==null?1:o });
      fur.appendChild(e); return e;
    }
    var F=FURN;

    /* cama */
    rr(px(F.bed.x), py(F.bed.y), F.bed.w*K, F.bed.h*K, FAC, 3);
    rr(px(F.bed.x+60), py(F.bed.y+70), (F.bed.w-120)*K, (F.bed.h-140)*K, 'rgba(227,107,255,.12)', 2);
    rr(px(F.bed.x+260), py(F.bed.y+90), (F.bed.w-520)*K, 170*K, C.magenta, 4);          // almohada
    rr(px(F.bed.x+260), py(F.bed.y+F.bed.h-250), (F.bed.w-520)*K, 170*K, 'rgba(227,107,255,.3)', 4, 0.6); // cobija

    /* armario */
    rr(px(F.dresser.x), py(F.dresser.y), F.dresser.w*K, F.dresser.h*K, FAC, 1.5);
    var dressX=px(F.dresser.x), dressY=py(F.dresser.y);
    for(var di=1; di<=3; di++){
      fur.appendChild(el('line',{ x1:dressX+F.dresser.w*K*di/4, y1:dressY, x2:dressX+F.dresser.w*K*di/4,
        y2:dressY+F.dresser.h*K, stroke:MG, 'stroke-width':0.7, opacity:0.5 }));
    }
    fur.appendChild(el('line',{ x1:dressX+4, y1:dressY, x2:dressX+4, y2:dressY+F.dresser.h*K,
      stroke:MG, 'stroke-width':1.6, opacity:0.7 }));

    /* sofá */
    rr(px(F.sofa.x), py(F.sofa.y), F.sofa.w*K, F.sofa.h*K, FAC, 4);
    rr(px(F.sofa.x), py(F.sofa.y+90), (F.sofa.w-90)*K, (F.sofa.h-120)*K, 'rgba(227,107,255,.16)', 3);
    rr(px(F.sofa.x+80), py(F.sofa.y+16), (F.sofa.w-160)/2*K, 74*K, 'rgba(227,107,255,.32)', 3);   // cojín 1
    rr(px(F.sofa.x+F.sofa.w-80-(F.sofa.w-160)/2), py(F.sofa.y+16), (F.sofa.w-160)/2*K, 74*K, 'rgba(227,107,255,.32)', 3); // cojín 2

    /* mesa centro */
    rr(px(F.coffee.x), py(F.coffee.y), F.coffee.w*K, F.coffee.h*K, FAC, 6);
    ov(px(F.coffee.x+F.coffee.w/2), py(F.coffee.y+F.coffee.h/2), F.coffee.w*K*0.32, F.coffee.h*K*0.36, 'rgba(227,107,255,.3)');

    /* TV + mueble */
    rr(px(F.tv.x), py(F.tv.y), F.tv.w*K, F.tv.h*K, 'rgba(120,140,180,.5)', 1);
    rr(px(F.tv.x+8), py(F.tv.y+10), (F.tv.w-16)*K, 34*K, 'rgba(79,214,232,.55)', 1);
    fur.appendChild(el('line',{ x1:px(F.tv.x+F.tv.w/2), y1:py(F.tv.y+F.tv.h), x2:px(F.tv.x+F.tv.w/2),
      y2:py(F.tv.y+F.tv.h)+14, stroke:'rgba(120,140,180,.7)', 'stroke-width':1.6 }));

    /* cocina: encimera */
    rr(px(F.kcount.x), py(F.kcount.y), F.kcount.w*K, F.kcount.h*K, FAC, 2);
    fur.appendChild(el('line',{ x1:px(F.kcount.x), y1:py(F.kcount.y+F.kcount.h/2),
      x2:px(F.kcount.x+F.kcount.w), y2:py(F.kcount.y+F.kcount.h/2),
      stroke:'rgba(120,140,180,.5)', 'stroke-width':6 }));
    /* vitrocerámica */
    rr(px(F.stove.x), py(F.stove.y), F.stove.w*K, F.stove.h*K, 'rgba(120,140,180,.5)', 3);
    [[0.3,0.3],[0.7,0.3],[0.3,0.7],[0.7,0.7]].forEach(function(b){
      circIn(fur, px(F.stove.x)+F.stove.w*K*b[0], py(F.stove.y)+F.stove.h*K*b[1], 7, 'rgba(227,107,255,.5)');
    });
    /* nevera */
    rr(px(F.fridge.x), py(F.fridge.y), F.fridge.w*K, F.fridge.h*K, FAC, 2);
    fur.appendChild(el('line',{ x1:px(F.fridge.x+F.fridge.w), y1:py(F.fridge.y),
      x2:px(F.fridge.x+F.fridge.w), y2:py(F.fridge.y+F.fridge.h), stroke:MG, 'stroke-width':0.8, opacity:0.6 }));
    fur.appendChild(el('line',{ x1:px(F.fridge.x+F.fridge.w/2), y1:py(F.fridge.y+F.fridge.h*0.38),
      x2:px(F.fridge.x+F.fridge.w/2), y2:py(F.fridge.y+F.fridge.h*0.38), stroke:MG, 'stroke-width':0.8, opacity:0.5 }));
    /* fregadero */
    rr(px(F.sink.x), py(F.sink.y), F.sink.w*K, F.sink.h*K, FAC, 2);
    ov(px(F.sink.x+F.sink.w/2), py(F.sink.y+F.sink.h/2), F.sink.w*K*0.3, F.sink.h*K*0.26, 'rgba(79,214,232,.4)');

    /* baño */
    rr(px(F.toilet.x), py(F.toilet.y), F.toilet.w*K, F.toilet.h*K, FAC, 4);                  // tanque
    ov(px(F.toilet.x+F.toilet.w/2), py(F.toilet.y+F.toilet.h), F.toilet.w*K*0.3, 20, FAC, 1); // taza
    rr(px(F.tub.x) , py(F.tub.y),  F.tub.h*K, F.tub.w*K, FAC, 12);
    rr(px(F.tub.x)+8, py(F.tub.y)+10, (F.tub.h-20)*K, (F.tub.w-22)*K, 'rgba(79,214,232,.35)', 10); // agua
    rr(px(F.basin.x), py(F.basin.y), F.basin.w*K, F.basin.h*K, FAC, 2);
    ov(px(F.basin.x+F.basin.w/2), py(F.basin.y+F.basin.h/2), F.basin.w*K*0.26, F.basin.h*K*0.22, 'rgba(79,214,232,.4)');
    circIn(fur, px(F.basin.x+F.basin.w/2), py(F.basin.y+F.basin.h/2), 4, MG);

    /* comedor */
    circIn(fur, px(F.dining.x), py(F.dining.y), F.dining.r*K*0.78, 'rgba(227,107,255,.22)');
    circIn(fur, px(F.dining.x), py(F.dining.y), F.dining.r*K*0.62, 'rgba(120,140,180,.35)');
    circIn(fur, px(F.dining.x), py(F.dining.y), 24, C.magenta);
    circIn(fur, px(F.dining.x), py(F.dining.y), 12, 'var(--bg-panel)');
    [[-1,-1],[1,-1],[-1,1],[1,1]].forEach(function(s){
      var sx=px(F.dining.x)+s[0]/Math.SQRT2*F.dining.r*K*0.95;
      var sy=py(F.dining.y)+s[1]/Math.SQRT2*F.dining.r*K*0.95;
      circIn(fur, sx, sy, 24, 'rgba(227,107,255,.5)');
      circIn(fur, sx+8, sy, 12, 'rgba(227,107,255,.35)');
    });

    /* plantas */
    circIn(fur, px(F.plant1.x), py(F.plant1.y), F.plant1.r*K, 'rgba(110,210,140,.45)');
    circIn(fur, px(F.plant1.x), py(F.plant1.y), 7, 'rgba(110,210,140,.8)');
    circIn(fur, px(F.plant2.x), py(F.plant2.y), F.plant2.r*K, 'rgba(110,210,140,.45)');
    circIn(fur, px(F.plant2.x), py(F.plant2.y), 7, 'rgba(110,210,140,.8)');

    els.fade.push(fur);

    return els;
  }

  function run2D(els){
    var D = function(v){ return reduced ? 0 : v; };
    var t = 0;

    hudAt(0, 0);
    els.floors.forEach(function(f){
      addAnim(anime({ targets:f, opacity:[0,1], duration:D(500)+2, delay:D(150), easing:'easeOutQuad' }));
    });

    els.walls.forEach(function(l){
      addAnim(anime({ targets:l, strokeDashoffset:[1,0], duration:D(650)+2, delay:t, easing:'easeInOutSine' }));
      t += D(95);
    });

    t += D(150); hudAt(1, t);
    els.dims.forEach(function(cell){
      cell.slice(0,5).forEach(function(e,i){
        addAnim(anime({ targets:e, strokeDashoffset:[1,0], duration:D(340)+2, delay:t+D(i*60), easing:'easeInOutSine' }));
      });
      addAnim(anime({ targets:cell[5], opacity:[0,1], duration:D(260)+2, delay:t+D(220), easing:'easeOutQuad' }));
      t += D(120);
    });

    t += D(200); hudAt(2, t);
    els.doors.forEach(function(g){
      addAnim(anime({ targets:g.childNodes[0], strokeDashoffset:[1,0], duration:D(380)+2, delay:t, easing:'easeOutQuad' }));
      addAnim(anime({ targets:g.childNodes[1], opacity:[0,0.7], duration:D(320)+2, delay:t, easing:'easeOutQuad' }));
      t += D(230);
    });

    t += D(200); hudAt(3, t);
    els.wins.forEach(function(g){
      Array.prototype.forEach.call(g.childNodes, function(e){
        if (e.tagName==='line') addAnim(anime({ targets:e, strokeDashoffset:[1,0], duration:D(340)+2, delay:t, easing:'easeInOutSine' }));
      });
      addAnim(anime({ targets:g._glass, opacity:[0,0.18], duration:D(360)+2, delay:t+D(140), easing:'easeOutQuad' }));
      t += D(170);
    });

    t += D(200); hudAt(4, t);
    els.rooms.forEach(function(r){
      addAnim(anime({ targets:r, opacity:[0,1], duration:D(320)+2, delay:t+D(110), easing:'easeOutQuad' }));
    });
    els.fade.forEach(function(f){
      if (f===els.furn) addAnim(anime({ targets:f, opacity:[0,1], duration:D(650)+2, delay:t, easing:'easeOutQuad' }));
      else addAnim(anime({ targets:f, opacity:[0,1], duration:D(260)+2, delay:t+D(40), easing:'easeOutQuad' }));
    });

    t += D(300);
    return t;
  }

  /* ===================== 3D (Three.js) ===================== */
  var renderer=null, scene=null, camera=null, group=null;
  var allWalls=[], allRisers=[], glassMats=[], doorLeaves=[], roofMesh=null, slabMesh=null;
  var matFrame, matAccent, matFurn, matPlant, matGlass;
  var running=false, rafId=null, autorotate=false, last=0;
  var mode='build';
  var zoom=1, zoomMin=0.6, zoomMax=2.6;

  var BASE   = { x:7.6, y:6.2, z:9.2 };
  var TARGET = { x:0,   y:1.15, z:0 };

  function cssVar(n){ return (window.getComputedStyle(document.documentElement).getPropertyValue(n)||'').trim(); }
  function tcol(n, fb){ var v=cssVar(n); return v ? new THREE.Color(v) : new THREE.Color(fb); }
  function supportsWebGL(){
    try { var c=document.createElement('canvas');
      return !!(window.WebGLRenderingContext && (c.getContext('webgl')||c.getContext('experimental-webgl'))); }
    catch(e){ return false; }
  }
  function box(w,h,d,mat){
    var g=new THREE.BoxGeometry(w,h,d); g.translate(0,h/2,0);
    return new THREE.Mesh(g, mat);
  }

  /* Muro con vanos reales (antepecho + dintel). */
  function makeWall(w, mat, M2){
    var HGT=2.8, THK=0.2;
    var x0=w.a[0]*M2, z0=w.a[1]*M2, x1=w.b[0]*M2, z1=w.b[1]*M2;
    var L=Math.sqrt((x1-x0)*(x1-x0)+(z1-z0)*(z1-z0));
    var ux=(x1-x0)/L, uz=(z1-z0)/L;
    var opens=[];
    (w.vanos||[]).forEach(function(v){
      opens.push({ d0:v.d0*M2, d1:v.d1*M2, sill:(v.sill||0)*M2, top:(v.top||2.1)*M2 });
    });
    var cuts=[0, L];
    opens.forEach(function(o){ cuts.push(o.d0); cuts.push(o.d1); });
    cuts=cuts.filter(function(v,i,a){ return a.indexOf(v)===i; }).sort(function(a,b){return a-b;});
    var meshes=[];
    function solid(da, db, fh, th){
      var len=db-da; if (len<=0.001||th<=fh+0.001) return;
      var g=new THREE.BoxGeometry(len, th-fh, THK);
      g.translate(0,(th+fh)/2,0);
      g.rotateY(Math.atan2(-uz,ux));
      g.translate(x0+ux*(da+db)/2, 0, z0+uz*(da+db)/2);
      meshes.push(new THREE.Mesh(g,mat));
    }
    for (var i=0;i<cuts.length-1;i++){
      var ca=cuts[i], cb=cuts[i+1];
      var inside=false;
      opens.forEach(function(o){ if(ca>=o.d0-1e-3 && cb<=o.d1+1e-3) inside=true; });
      if(inside) continue;
      solid(ca, cb, 0, HGT);
    }
    opens.forEach(function(o){
      if(o.sill>0.01) solid(o.d0, o.d1, 0, o.sill);      // antepecho
      if(o.top<HGT-0.001) solid(o.d0, o.d1, o.top, HGT); // dintel
    });
    return { meshes:meshes, ux:ux, uz:uz, x0:x0, z0:z0, x1:x1, z1:z1, opens:opens };
  }

  function build3D(){
    if (typeof THREE==='undefined' || !supportsWebGL()) return false;
    var M2=0.001;

    scene=new THREE.Scene();
    camera=new THREE.PerspectiveCamera(40, 1, 0.1, 100);
    camera.position.set(BASE.x, BASE.y, BASE.z);
    camera.lookAt(TARGET.x, TARGET.y, TARGET.z);

    renderer=new THREE.WebGLRenderer({ canvas:canvas3d, antialias:true, alpha:true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
    renderer.setClearColor(0x000000,0);
    renderer.shadowMap.enabled=true;
    renderer.shadowMap.type=THREE.PCFSoftShadowMap;

    scene.add(new THREE.HemisphereLight(0xfff3e0,0x33404f,1.0));
    var key=new THREE.DirectionalLight(0xfff0dc,2.1);
    key.position.set(7,12,6); key.castShadow=true;
    key.shadow.mapSize.set(2048,2048);
    key.shadow.camera.near=0.5; key.shadow.camera.far=40;
    key.shadow.camera.left=-10; key.shadow.camera.right=10;
    key.shadow.camera.top=10; key.shadow.camera.bottom=-10;
    scene.add(key);
    var fill=new THREE.DirectionalLight(0xa8d4ff,0.6);
    fill.position.set(-6,6,-7); scene.add(fill);
    scene.add(new THREE.AmbientLight(0x8b98b8,0.4));

    group=new THREE.Group();
    scene.add(group);

    var matGround=new THREE.ShadowMaterial(); matGround.opacity=0.6;
    var ground=new THREE.Mesh(new THREE.CircleGeometry(16,48), matGround);
    ground.rotation.x=-Math.PI/2; ground.position.y=0.001; ground.receiveShadow=true;
    scene.add(ground);

    var grid=new THREE.GridHelper(12,12,tcol('--layer-cyan','#35D6CB'),tcol('--layer-cyan','#35D6CB'));
    grid.material.transparent=true; grid.material.opacity=0.12; grid.position.y=0.015;
    scene.add(grid);

    var matFloor=new THREE.MeshStandardMaterial({ color:0xd9cdbb, roughness:0.9, metalness:0 });   // suelo hormigón claro
    var matPlith=new THREE.MeshStandardMaterial({ color:0x8c9aa8, roughness:0.6, metalness:0.25 }); // zócalo
    var matWall =new THREE.MeshStandardMaterial({ color:0xf0e6d8, roughness:0.92, metalness:0 });   // fachada yeso
    var matPart =new THREE.MeshStandardMaterial({ color:0xeae0d0, roughness:0.92, metalness:0 });   // tabiques
    var matRoof =new THREE.MeshStandardMaterial({ color:0x5a4635, roughness:0.75, metalness:0.15 }); // cubierta teja
    matRoof.side=THREE.DoubleSide;
    var matDoor =new THREE.MeshStandardMaterial({ color:0x8a5a2e, roughness:0.55, metalness:0.25 });
    matFrame =new THREE.MeshStandardMaterial({ color:0xeef2f7, roughness:0.3, metalness:0.5 });
    matGlass =new THREE.MeshStandardMaterial({ color:0x7fd4e8, transparent:true, opacity:0, roughness:0.05, metalness:0.85, side:THREE.DoubleSide });
    matFurn  =new THREE.MeshStandardMaterial({ color:0x4c3a28, roughness:0.75, metalness:0.05 });   // madera muebles
    matAccent=new THREE.MeshStandardMaterial({ color:0xe8e2d6, roughness:0.55, metalness:0.2 });
    matPlant =new THREE.MeshStandardMaterial({ color:0x5aa86a, roughness:0.9, metalness:0 });

    /* losa + zócalo (centrados en la huella: muros 0..6.2 X, 0..4.2 Z => centro 3.1,2.1) */
    var CX=6.2/2, CZ=4.2/2;
    slabMesh=box(6.6,0.2,4.6,matFloor);
    slabMesh.position.set(CX,-0.1,CZ);              // top en y=0 = base de los muros
    slabMesh.receiveShadow=true; slabMesh.castShadow=true;
    group.add(slabMesh);
    var plinth=box(6.9,0.5,4.9,matPlith);
    plinth.position.set(CX,-0.7,CZ);                // top en -0.2 = fondo de la losa
    plinth.receiveShadow=true; plinth.castShadow=true;
    group.add(plinth);

    function addRiser(m){ allRisers.push(m); m.castShadow=true; m.receiveShadow=true; group.add(m); }

    /* muros con vanos */
    var openings=[];
    WALLS.forEach(function(w){
      var r=makeWall(w, w.kind==='outer'?matWall:matPart, M2);
      r.meshes.forEach(addRiser);
      r.meshes.forEach(function(m){ allWalls.push(m); });
      r.opens.forEach(function(o){
        openings.push({ wall:r, o:o,
          cx:r.x0+r.ux*(o.d0+o.d1)/2,
          cz:r.z0+r.uz*(o.d0+o.d1)/2,
          span:o.d1-o.d0 });
      });
    });

    /* puertas (hoja) y marcos */
    DOORS.forEach(function(d){
      var ax=d.hinge[0]*M2, az=d.hinge[1]*M2, bx=d.edge[0]*M2, bz=d.edge[1]*M2;
      var ww=Math.sqrt((bx-ax)*(bx-ax)+(bz-az)*(bz-az));
      var leaf=box(ww, 0.05, d.h*M2, matDoor);
      leaf.position.set((ax+bx)/2, d.h*M2/2, (az+bz)/2);
      leaf.rotation.y=Math.atan2(bz-az, bx-ax);
      doorLeaves.push(leaf); addRiser(leaf);
      var fr=box(0.08, d.h*M2, 0.06, matFrame);
      fr.position.set(ax, d.h*M2/2, az);
      addRiser(fr);
    });

    /* ventanas: marcos + vidrio */
    openings.forEach(function(o){
      var horiz = Math.abs(o.wall.ux) > 0.5;                 // muro horizontal (corre en X)
      var glassBox = horiz ? box(o.span,(o.o.top-o.o.sill),0.03,matGlass)
                           : box(0.03,(o.o.top-o.o.sill),o.span,matGlass);
      glassBox.position.set(o.cx,(o.o.sill+o.o.top)/2,o.cz);
      var fr = horiz ? box(o.span+0.1,(o.o.top-o.o.sill)+0.1,0.08,matFrame)
                     : box(0.08,(o.o.top-o.o.sill)+0.1,o.span+0.1,matFrame);
      fr.position.set(o.cx,(o.o.sill+o.o.top)/2,o.cz);
      addRiser(fr);
      glassMats.push(glassBox.material);
      addRiser(glassBox);
    });

    /* mobiliario */
    function F3(rt, w, h, d, mat, opts){
      opts=opts||{};
      var m=box(w,h,d,mat);
      var cx=((rt.x+(opts.cx||rt.w/2))*M2);
      var cz=((rt.y+(opts.cz||rt.h/2))*M2);
      m.position.set(cx, opts.y!=null?opts.y:(h/2), cz);
      if(opts.ry) m.rotation.y=opts.ry;
      addRiser(m);
      if (opts.store!==undefined) opts.store.push(m);
      return m;
    }
    (function(){
      var F=FURN;
      F3(F.bed, F.bed.w*M2, 0.24, F.bed.h*M2, matFurn);                                   // base
      F3(F.bed, F.bed.w*M2*0.97, 0.14, F.bed.h*M2*0.97, matAccent, { y:0.31 });            // colchón
      F3(F.bed, 0.14, 0.9, F.bed.h*M2*0.9, matAccent, { cx:0.06, y:0.45 });               // cabecero
      F3({x:F.bed.x+150,y:F.bed.y+250,w:520,h:400}, 0.5, 0.07, 0.4, matAccent, { y:0.4 });
      F3({x:F.bed.x+150,y:F.bed.y+F.bed.h-650,w:520,h:400}, 0.5, 0.07, 0.4, matAccent, { y:0.4 });

      F3(F.dresser, F.dresser.w*M2, 2.1, F.dresser.h*M2, matFurn);                         // armario

      F3(F.sofa, F.sofa.w*M2, 0.72, F.sofa.h*M2, matFurn);                                // sofá
      F3(F.sofa, F.sofa.w*M2, 0.75, 0.16, matAccent, { cy:F.sofa.h-40, y:0.72 });

      F3(F.coffee, F.coffee.w*M2, 0.4, F.coffee.h*M2, matFurn);                           // mesa centro

      F3(F.tv, F.tv.w*M2, 0.7, F.tv.h*M2, matAccent);                                     // TV
      F3(F.tv, F.tv.w*M2, 0.5, 0.4, matFurn, { y:0.25 });                                 // mueble TV

      var tab=box(1.3,0.06,1.3,matFurn); tab.position.set(F.dining.x*M2,0.76,F.dining.y*M2); addRiser(tab);
      [[-1,-1],[1,-1],[-1,1],[1,1]].forEach(function(s){
        var lg=box(0.1,0.76,0.1,matAccent);
        lg.position.set(F.dining.x*M2+s[0]*0.55, 0.38, F.dining.y*M2+s[1]*0.55); addRiser(lg);
      });
      [[-1,-1],[1,-1],[-1,1],[1,1]].forEach(function(s){
        var ch=box(0.44,0.5,0.44,matFurn);
        ch.position.set(F.dining.x*M2+s[0]*0.95, 0.25, F.dining.y*M2+s[1]*0.95); addRiser(ch);
      });

      F3(F.kcount, 1.0,0.9,0.6, matFurn);
      F3(F.stove,  F.stove.w*M2,0.9,F.stove.h*M2, matFurn);
      F3(F.fridge, F.fridge.w*M2,1.9,F.fridge.h*M2, matAccent);
      F3(F.fridge, F.fridge.w*M2,0.5,0.06, matFrame, { cy:F.fridge.h+40, y:1.9 });
      F3(F.sink,   F.sink.w*M2,0.85,F.sink.h*M2, matAccent);

      F3(F.toilet, 0.34,0.75,0.3, matAccent);                                             // tanque
      F3({x:F.toilet.x+40,y:F.toilet.y-70,w:250,h:250}, 0.2,0.45,0.2, matAccent);          // inodoro
      F3(F.tub, F.tub.h*M2,0.55,F.tub.w*M2, matAccent);                                   // bañera
      F3(F.basin, F.basin.w*M2,0.85,F.basin.h*M2, matAccent);                             // lavabo

      [F.plant1,F.plant2].forEach(function(p){
        var pot=box(0.2,0.24,0.2,matFurn); pot.position.set(p.x*M2,0.12,p.y*M2); addRiser(pot);
        var bush=new THREE.Mesh(new THREE.SphereGeometry(0.22,12,10), matPlant);
        bush.position.set(p.x*M2,0.42,p.y*M2); addRiser(bush);
      });
    })();

    /* cubierta con vuelo (alero) — apoyada en los muros y centrada en la huella */
    var RLX=7.0, RDZ=5.0;
    roofMesh=box(RLX,0.16,RDZ,matRoof);
    roofMesh.position.set(CX,2.8,CZ);               // apoya en y=0..2.8 (techo en 2.8..2.96)
    roofMesh.castShadow=true; roofMesh.receiveShadow=true;
    addRiser(roofMesh);
    function eave(len, y, dep, x, z){               // borde/perfil de la cubierta
      var p=box(len,0.3,dep,matFrame);
      p.position.set(x,y,z);
      addRiser(p);
    }
    eave(RLX, 2.8, 0.3, CX,      CZ+RDZ/2);          // frontal
    eave(RLX, 2.8, 0.3, CX,      CZ-RDZ/2);          // trasero
    eave(0.3, 2.8, RDZ, CX-RLX/2, CZ);               // lateral izq
    eave(0.3, 2.8, RDZ, CX+RLX/2, CZ);               // lateral der

    group.position.x=-CX; group.position.z=-CZ;
    group.rotation.y=0.35;

    resize();
    return true;
  }

  /* fases de construcción */
  function animate3DIntro(offset){
    if (!group) return;
    allRisers.forEach(function(m){ m.scale.set(0.01,0.01,0.01); });
    glassMats.forEach(function(m){ m.opacity=0; });
    if (slabMesh) slabMesh.scale.set(1,1,1);

    if (reduced){
      allRisers.forEach(function(m){ m.scale.set(1,1,1); });
      glassMats.forEach(function(m){ m.opacity=0.55; });
      autorotate=true;
      return;
    }

    var t=offset+300;
    var isFurn=function(m){
      if (m===roofMesh||m===slabMesh) return false;
      if (allWalls.indexOf(m)!==-1) return false;
      if (doorLeaves.indexOf(m)!==-1) return false;
      if (m.material===matFrame) return false;          // marcos/aleros: se animan aparte
      if (glassMats.indexOf(m.material)!==-1) return false;
      return true;
    };

    allWalls.forEach(function(m,i){
      addAnim(anime({ targets:m.scale, x:1, y:1, z:1, duration:750, delay:t+i*26, easing:'easeOutBack' }));
    });
    t+=900;

    doorLeaves.forEach(function(m,i){
      addAnim(anime({ targets:m.scale, x:1, y:1, z:1, duration:500, delay:t+i*80, easing:'easeOutBack' }));
    });
    t+=500;

    glassMats.forEach(function(m,i){
      addAnim(anime({ targets:m, opacity:0.55, duration:450, delay:t+i*60, easing:'easeOutQuad' }));
    });
    var frameMeshes=allRisers.filter(function(m){
      return m!==slabMesh && m!==roofMesh && m.material===matFrame &&
             allWalls.indexOf(m)===-1 && glassMats.indexOf(m.material)===-1;
    });
    frameMeshes.forEach(function(m,i){
      addAnim(anime({ targets:m.scale, x:1, y:1, z:1, duration:400, delay:t+i*40, easing:'easeOutBack' }));
    });
    t+=450;

    var furnMeshes=allRisers.filter(isFurn);
    furnMeshes.forEach(function(m,i){
      addAnim(anime({ targets:m.scale, x:1, y:1, z:1, duration:520, delay:t+i*25, easing:'easeOutBack' }));
    });
    t+=800;

    addAnim(anime({ targets:roofMesh.scale, x:1, y:1, z:1, duration:650, delay:t, easing:'easeOutBack' }));

    addAnim(anime({
      targets:camera.position, x:7.6, y:5.6, z:9.2,
      duration:2200, delay:t+400, easing:'easeInOutCubic',
      update:function(){ camera.lookAt(TARGET.x,TARGET.y,TARGET.z); },
      complete:function(){ autorotate=true; }
    }));
  }

  function resize(){
    if(!renderer) return;
    var w=svg2d.parentNode.clientWidth||300;
    var h=svg2d.parentNode.clientHeight||225;
    camera.aspect=w/h; camera.updateProjectionMatrix();
    renderer.setSize(w,h);
  }
  window.addEventListener('resize', resize);
  if (window.ResizeObserver && window.ResizeObserver.prototype && window.ResizeObserver.prototype.observe){
    new window.ResizeObserver(resize).observe(svg2d.parentNode);
  }

  function renderLoop(now){
    if(!running) return;
    if(now && last){
      var dt=Math.min((now-last)/1000,0.05);
      if(autorotate && group) group.rotation.y+=dt*0.05;
    }
    last=now;
    if(renderer&&scene&&camera) renderer.render(scene,camera);
    rafId=requestAnimationFrame(renderLoop);
  }
  function startRaf(){ if(running||!renderer) return; running=true; last=0; rafId=requestAnimationFrame(renderLoop); }
  function stopRaf(){ running=false; if(rafId) cancelAnimationFrame(rafId); rafId=null; }
  if (window.IntersectionObserver){
    new window.IntersectionObserver(function(es){ es.forEach(function(en){ if(en.isIntersecting) startRaf(); else stopRaf(); }); }).observe(svg2d.parentNode);
  } else startRaf();

  /* interacción: rotar + zoom */
  var dragging=false, dpx=0, dpy=0;
  canvas3d.addEventListener('pointerdown', function(e){ dragging=true; dpx=e.clientX; dpy=e.clientY; });
  window.addEventListener('pointermove', function(e){
    if(!dragging||!group) return;
    group.rotation.y+=(e.clientX-dpx)*0.006;
    group.rotation.x+=(e.clientY-dpy)*0.0035;
    group.rotation.x=Math.max(-0.9,Math.min(1.1,group.rotation.x));
    dpx=e.clientX; dpy=e.clientY;
  });
  window.addEventListener('pointerup', function(){ dragging=false; });
  window.addEventListener('pointercancel', function(){ dragging=false; });
  canvas3d.addEventListener('wheel', function(e){
    if(!camera) return;
    e.preventDefault();
    zoom=Math.max(zoomMin,Math.min(zoomMax,zoom*(e.deltaY>0?0.9:1.1)));
    camera.position.set(BASE.x*zoom, 5.0+ (1-zoom)*1.4, BASE.z*zoom);
    camera.lookAt(TARGET.x,TARGET.y,TARGET.z);
  }, { passive:false });

  function resetView(){
    if(!camera) return;
    zoom=1;
    camera.position.set(BASE.x,5.0,BASE.z);
    camera.lookAt(TARGET.x,TARGET.y,TARGET.z);
    if(group) group.rotation.set(0,0,0);
    autorotate=true;
  }

  function setMode(m){
    mode=m;
    if(btn2D) btn2D.classList.toggle('active', m==='2d');
    if(btn3D) btn3D.classList.toggle('active', m==='3d'||m==='build');
    var stg=svg2d.parentNode.querySelector('.plan-stage');
    if(m==='2d'){ svg2d.style.opacity='1'; canvas3d.style.display='none'; if(stg) stg.style.display='none'; }
    else { canvas3d.style.display='block'; svg2d.style.opacity='0'; if(stg) stg.style.display='block'; }
  }

  function start(){
    var els=build2D();
    var t=run2D(els);
    var ok=build3D();
    if(ok){
      hudAt(5, t+(reduced?0:300));
      setMode('build');
      animate3DIntro(t+(reduced?0:300));
    } else {
      setMode('2d');
    }
  }

  function stop3D(){
    anims.forEach(function(a){ try{ a.pause(); }catch(e){} });
    anims.length=0;
    if(renderer){
      stopRaf();
      try{ renderer.dispose(); }catch(e){}
      allWalls=[]; allRisers=[]; glassMats=[]; doorLeaves=[];
      renderer=null; scene=null; camera=null; group=null;
      canvas3d.style.display='none';
    }
    autorotate=false;
  }

  replayBtn.addEventListener('click', function(){ stop3D(); start(); });
  if(btn2D) btn2D.addEventListener('click', function(){ setMode('2d'); stopRaf(); });
  if(btn3D) btn3D.addEventListener('click', function(){
    if(!renderer){ stop3D(); start(); return; }
    setMode('3d'); startRaf(); autorotate=true;
  });

  var started=false;
  function boot(){ if(started) return; started=true; start(); }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();

  window.addEventListener('pagehide', function(){ stop3D(); });
})();
