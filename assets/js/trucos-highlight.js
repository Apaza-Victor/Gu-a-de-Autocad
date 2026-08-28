/* ============================================================
   Trucos: Auto-resaltado de atajos de teclado y comandos
   Envuelve teclas (ESC, TAB, F12, Ctrl+...) en <kbd> (ámbar)
   y comandos conocidos en <span class="hl-cmd"> (cian).
   Se ejecuta tras cada traducción (ver hook en i18n.js).
   ============================================================ */
(function () {
  'use strict';

  /* Teclas individuales y combinaciones (atajos de teclado) */
  var KEY_NAMED = [
    'ESC', 'TAB', 'ENTER', 'SHIFT', 'DEL', 'SUPR', 'BACKSPACE',
    'RETROCESO', 'HOME', 'END', 'PGUP', 'PGDN',
    'PAGE UP', 'PAGE DOWN', 'RE PÁG', 'AV PÁG',
    'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
    '\u2190', '\u2191', '\u2192', '\u2193'
  ];

  /* Comandos conocidos (mayúsculas/minúsculas) — el texto los escribe en inglés o español */
  var CMDS = [
    'LINE', 'LÍNEA', 'CIRCLE', 'CÍRCULO', 'ARC', 'ARCO', 'RECTANG',
    'RECTANGLE', 'RECTÁNGULO', 'POLYGON', 'POLÍGONO', 'ELLIPSE',
    'ELIPSE', 'SPLINE', 'PLINE', 'POLILÍNEA', 'OFFSET', 'DESFASA',
    'TRIM', 'RECORTA', 'RECORTAR', 'EXTEND', 'ALARGA', 'FILLET',
    'EMPALME', 'CHAMFER', 'CHANFRO', 'CHAFLÁN', 'ARRAY', 'MATRIZ',
    'SCALE', 'ESCALA', 'ESCALAR', 'ROTATE', 'GIRAR', 'ROTA',
    'MOVE', 'DESPLAZA', 'DESPLAZAR', 'MOVER', 'COPY', 'COPIAR', 'COPIA',
    'MIRROR', 'SIMETRÍA', 'SIMETRIA', 'ESPEJO', 'STRETCH',
    'ESTIRAR', 'BREAK', 'PARTE', 'JOIN', 'UNE', 'UNIR', 'EXPLODE',
    'DESCOMPONE', 'HATCH', 'SOMBREADO', 'GRADIENT', 'DEGRADADO',
    'TEXT', 'MTEXT', 'DIM', 'ACOTA', 'DIMLINEAR', 'ACOLINEAL',
    'DIMALIGNED', 'ACOLINEADA', 'DIMANGULAR', 'ACOANGULO',
    'DIMRADIUS', 'ACORADIO', 'MEASUREGEOM', 'MEDIRGEOM', 'DIST',
    'AREA', 'LIST', 'PURGE', 'LIMPIA', 'AUDIT', 'REVISIÓN',
    'REVISION', 'OVERKILL', 'LAYER', 'CAPA', 'LTYPE', 'TIPOLIN',
    'REVOLVE', 'REVOLUCIONA', 'EXTRUDE', 'EXTRUYE', 'SWEEP',
    'BARRIDO', 'LOFT', 'SOLEVACIÓN', 'SOLEVACION', 'UNION', 'UNIÓN',
    'SUBTRACT', 'RESTA', 'INTERSECT', 'INTERSECCIÓN', 'INTERSECCION',
    'MULTIPLE'
  ];

  /* Combinación Ctrl+... (atajo de teclado) */
  var CTRL_RE = /(Ctrl(?:\+[A-Za-z0-9]+)+)/gi;

  function escapeRe(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  function buildRegex(words) {
    var tagged = words.map(function (w) {
      return escapeRe(w).replace(/ /g, '\\s+');
    });
    tagged.sort(function (a, b) { return b.length - a.length; });
    return new RegExp('(?<!\\p{L})(?:' + tagged.join('|') + ')(?!\\p{L})', 'giu');
  }

  var KEY_RE = buildRegex(KEY_NAMED);
  var CMD_RE = buildRegex(CMDS);

  function isUpperFirst(s) {
    var c = s.charAt(0);
    return c === c.toUpperCase() && c !== c.toLowerCase();
  }

  /* Tecla: se admite si empieza en MAYÚSCULA (ESC, TAB, Enter, F8, Ctrl+...)
     o si su primer carácter NO es una letra (flechas →←↑↓). Así la palabra
     española "del" (minúscula) NO se resalta como la tecla DEL. */
  function isKeyStart(s) {
    var c = s.charAt(0);
    if (c.toLowerCase() !== c.toUpperCase()) return c === c.toUpperCase();
    return true;
  }

  function esc(s) {
    return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function wrap(container) {
    if (!container) return;
    container.innerHTML = highlight(container.textContent);
  }

  function highlight(text) {
    if (!text) return text;
    var len = text.length;
    var out = '';
    var i = 0;
    var ctrl, key, cmd;

    while (i < len) {
      var slice = text.slice(i);
      CTRL_RE.lastIndex = 0;
      KEY_RE.lastIndex = 0;
      CMD_RE.lastIndex = 0;

      ctrl = CTRL_RE.exec(slice);
      key = KEY_RE.exec(slice);
      cmd = CMD_RE.exec(slice);

      var cands = [];
      if (ctrl && isKeyStart(ctrl[0])) cands.push({ i: ctrl.index, len: ctrl[0].length, k: 'kbd', r: ctrl[0] });
      if (key && isKeyStart(key[0])) cands.push({ i: key.index, len: key[0].length, k: 'kbd', r: key[0] });
      /* Los comandos solo se resaltan si empiezan en MAYÚSCULA, para no marcar
         verbos españoles en minúscula (mover, copiar, girar...) como comandos. */
      if (cmd && isUpperFirst(cmd[0])) cands.push({ i: cmd.index, len: cmd[0].length, k: 'cmd', r: cmd[0] });

      if (cands.length === 0) {
        out += esc(text.slice(i));
        break;
      }
      cands.sort(function (a, b) { return a.i - b.i || a.len - b.len; });
      var best = cands[0];
      out += esc(text.slice(i, i + best.i));
      out += best.k === 'kbd' ? '<kbd>' + esc(best.r) + '</kbd>' : '<span class="hl-cmd">' + esc(best.r) + '</span>';
      i += best.i + best.len;
    }
    return out;
  }

  function run() {
    var targets = document.querySelectorAll(
      '.diagram-card-body > p[data-i18n], ' +
      '.diagram-card-body .callout > span[data-i18n]:not(.callout-title), ' +
      '.pasos-block li[data-i18n]'
    );
    for (var i = 0; i < targets.length; i++) {
      wrap(targets[i]);
    }
  }

  window.TrucoHighlight = { run: run };
})();
