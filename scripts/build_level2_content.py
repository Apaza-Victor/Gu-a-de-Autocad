# -*- coding: utf-8 -*-
"""
build_level2_content.py
Enriquece el Nivel 2 (Dibujo 2D):
  - Añade contenido nuevo (conceptos, tablas de comandos, ejemplos paso a paso,
    callouts, atajos y mini ejercicios) a las 12 lecciones existentes que lo
    necesitan (capas y acotación ya son completas).
  - Crea 3 lecciones nuevas: matrices, grips, consulta.
  - Regenera las 18 páginas de lección y la portada index.html del nivel.
  - Actualiza search-index.js, sitemap.xml, main.js (total 73) e index.html.

Ejecutar desde la raíz:  python scripts/build_level2_content.py
"""
import os
import re
import sys
import json

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
sys.path.insert(0, SCRIPTS)

from build_level_folders import (  # noqa: E402
    LEVELS, BASE_URL, read, write, strip_tags,
    build_head, build_navbar, build_footer, build_scripts, build_end_block,
)

FOLDER = "nivel-2-dibujo-2d"
DST = os.path.join(ROOT, "paginas", FOLDER)
NUM = 2
TOTAL = 18
EYEBROW = LEVELS[2][3]
FULL_TITLE = LEVELS[2][2]
SCHEMA_NAME = LEVELS[2][5]
SCHEMA_DESC = LEVELS[2][6]


def indent(text, n):
    pad = " " * n
    return "\n".join((pad + ln if ln.strip() else ln) for ln in text.split("\n"))


def esc(x):
    return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ----------------------------------------------------------------------------
# 1) Catálogo de temas del nivel (orden de estudio)
# ----------------------------------------------------------------------------
# data_topic --> (archivo, título h2/h1, etiqueta TOC/card, descripción)
TOPICS = [
    ("nivel2-dibujo",          "dibujo.html",          "Herramientas de dibujo",                   "Herramientas de dibujo",       "Comandos que crean geometría: línea, polilínea, círculo, arco, rectángulo, polígono, elipse y spline."),
    ("nivel2-modificacion",    "modificacion.html",    "Herramientas de modificación",             "Herramientas de modificación", "Mover, copiar, rotar, escalar, recortar, desfasar, simetría, matrices, empalme y chaflán."),
    ("nivel2-matrices",        "matrices.html",        "Matrices: repite objetos en patrón (ARRAY)", "Matrices (ARRAY)",          "Tipos de matriz rectangular, polar y de ruta: filas, columnas, ángulo, asociatividad y edición."),
    ("nivel2-precision",       "precision.html",       "Precisión: referencias, rastreo y cuadrícula", "Precisión: referencias y rastreo", "Ayudas de precisión: OSNAP, rastreo polar, ORTO, rejilla y SNAP, y cómo configurarlas."),
    ("nivel2-capas",           "capas.html",           "Capas (Layers)",                           "Capas (Layers)",               "Organizar el dibujo en capas: crear, nombrar, controlar visibilidad y trabajar con ByLayer."),
    ("nivel2-bloques",         "bloques.html",         "Bloques y atributos",                      "Bloques y atributos",          "Agrupar objetos en bloques reutilizables y enriquecerlos con atributos editables."),
    ("nivel2-acotacion",       "acotacion.html",       "Acotación (dimensiones)",                  "Acotación",                    "Tipos de cota, estilos de cota, DIMSCALE y cómo acotar un plano con precisión."),
    ("nivel2-texto",           "texto.html",           "Texto, estilos de texto y tablas",         "Texto y tablas",               "TEXT, MTEXT, estilos de texto y tablas para notas y cuadros del plano."),
    ("nivel2-hatch",           "hatch.html",           "Sombreado y rellenos (Hatch)",             "Sombreado (Hatch)",            "Rellenar contornos cerrados con patrones de material: HATCH, contornos, islas y HATCHEDIT."),
    ("nivel2-seleccion",       "seleccion.html",       "Selección de objetos",                     "Selección de objetos",         "Métodos de selección: ventana, cruzante, lasso, polígonos, filtros y selección por nombre."),
    ("nivel2-grips",           "grips.html",           "Pinzamientos (GRIPS): edición rápida sin comandos", "Pinzamientos (GRIPS)",   "Editar objetos con los grips: estirar, mover, rotar, escalar y multiplicar sin teclear comandos."),
    ("nivel2-lineas",          "lineas.html",          "Tipos de línea",                           "Tipos de línea",               "Tipos de línea continua, discontinua y ejes; cómo cargarlos y escalarlos con LTSCALE."),
    ("nivel2-puntos",          "puntos.html",          "Puntos y división",                        "Puntos y división",            "DIVIDE y MEASURE para colocar puntos o bloques a intervalos regulares."),
    ("nivel2-auxiliares",      "auxiliares.html",      "Geometría auxiliar",                       "Geometría auxiliar",           "XLINE y RAY como líneas de construcción temporales para alinear y ubicar el dibujo."),
    ("nivel2-consulta",        "consulta.html",        "Medición y verificación del dibujo",       "Medición y verificación",      "DIST, AREA, MEASUREGEOM, LIST e ID para medir y verificar el dibujo antes de entregar."),
    ("nivel2-propiedades",     "propiedades.html",     "Propiedades de objeto",                    "Propiedades de objeto",        "Controlar capa, color, tipo y grosor de línea; paleta PROPIEDADES y MATCHPROP."),
    ("nivel2-pedit",           "pedit.html",           "Edición de polilíneas (PEDIT)",            "Edición de polilíneas",        "Unir, cerrar y editar polilíneas con PEDIT y JOIN."),
    ("nivel2-splines",         "splines.html",         "Splines y curvas",                         "Splines y curvas",             "Curvas libres con SPLINE: control de la forma, tolerancia y edición."),
]

TOPIC_META = {t[0]: t for t in TOPICS}
FILE_TO_TOPIC = {t[1]: t[0] for t in TOPICS}

# ----------------------------------------------------------------------------
# 2) Contenido de enriquecimiento para las lecciones existentes
# ----------------------------------------------------------------------------
# Cada fragmento se inserta antes del botón "Marcar tema como visto".
ENRICH = {}

ENRICH["nivel2-dibujo"] = [
"""<h3>Opciones ocultas de las herramientas básicas</h3>
<p>Los comandos de dibujo tienen opciones que pocos usan y que ahorran pasos:</p>
<table class="table-cad">
  <thead><tr><th>Comando</th><th>Opción</th><th>Qué hace</th></tr></thead>
  <tbody>
    <tr><td><span class="cmd-inline">RECTANG</span></td><td><span class="cmd-inline">W</span> (Width)</td><td>Dibuja el rectángulo ya con grosor de línea (piezas con ancho real).</td></tr>
    <tr><td><span class="cmd-inline">RECTANG</span></td><td><span class="cmd-inline">C</span> (Chamfer) / <span class="cmd-inline">F</span> (Fillet)</td><td>Redondea o achaflana las esquinas al instante, sin FILLET posterior.</td></tr>
    <tr><td><span class="cmd-inline">POLYGON</span></td><td>Centro → inscrito / circunscrito</td><td>El radio se mide al borde interior de los lados o a las esquinas: elige según la referencia.</td></tr>
    <tr><td><span class="cmd-inline">POLYGON</span></td><td><span class="cmd-inline">E</span> (Edge)</td><td>Crea el polígono a partir de la longitud de un lado.</td></tr>
    <tr><td><span class="cmd-inline">CIRCLE</span></td><td><span class="cmd-inline">T</span> (Tan Tan Radius) / <span class="cmd-inline">3P</span> / <span class="cmd-inline">2P</span></td><td>Círculos tangentes a dos objetos o definidos por puntos, sin calcular el centro.</td></tr>
    <tr><td><span class="cmd-inline">ARC</span></td><td><span class="cmd-inline">C</span> (Center) y <span class="cmd-inline">A</span> (Angle)</td><td>Arcos definidos por centro o ángulo de barrido, más predecibles que "3 puntos".</td></tr>
  </tbody>
</table>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Cuando un comando está activo, la línea de comandos y las opciones del menú contextual (<span class="key-inline">clic derecho</span> o flecha <span class="key-inline">↑</span>) muestran sus modificadores. Aprender los de las 8 herramientas de dibujo es el mayor multiplicador de velocidad del 2D.</span>
</div>

<h3>Mini ejercicio: figura combinada de 60 segundos</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Rectángulo con esquinas redondeadas</h4>
    <p>Escribe <span class="cmd-inline">RECTANG</span>, opción <span class="cmd-inline">F</span>, radio <span class="cmd-inline">15</span>, y dibuja un rectángulo de <span class="cmd-inline">200 x 120</span>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Polígono circunscrito</h4>
    <p>Con <span class="cmd-inline">POLYGON</span>, lados <span class="cmd-inline">6</span>, centro en el del rectángulo y opción <strong>Circumscribed about circle</strong> con radio <span class="cmd-inline">60</span>. Observa cómo encaja por fuera.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Círculo tangente</h4>
    <p>Con <span class="cmd-inline">CIRCLE</span> → <span class="cmd-inline">T</span>, toca dos lados del polígono y escribe radio <span class="cmd-inline">25</span>. Sin calcular nada, tienes un círculo pegado a ambos.</p>
  </div>
</div>""",
]

ENRICH["nivel2-modificacion"] = [
"""<h3>Opciones que cambian el resultado</h3>
<p>Detalles de los modificadores que más diferencias marcan en planos reales:</p>
<ul>
  <li><strong>MIRROR y texto:</strong> la variable <span class="cmd-inline">MIRRTEXT</span> en <strong>0</strong> hace que los textos no se inviertan al reflejar; en <strong>1</strong> los copia en espejo.</li>
  <li><strong>FILLET con radio 0:</strong> une dos líneas cortando las esquinas sobrantes. Es la vía más rápida para "limpiar" vértices que no tocan.</li>
  <li><strong>OFFSET en modo múltiple:</strong> la opción <span class="cmd-inline">O</span> (Multiple) repite el desfase sin reiniciar el comando (ideal para muros paralelos).</li>
  <li><strong>ROTATE y SCALE con referencia:</strong> la opción <span class="cmd-inline">R</span> (Reference) alinea el objeto a una medida conocida sin calcular ángulos.</li>
</ul>
<table class="table-cad">
  <thead><tr><th>Comando</th><th>Opción práctica</th><th>Uso típico</th></tr></thead>
  <tbody>
    <tr><td><span class="cmd-inline">ARRAY</span></td><td>Rectangular / Polar / Path</td><td>Repetir pilares en retícula, luminares en círculo o muros a lo largo de un eje curvo.</td></tr>
    <tr><td><span class="cmd-inline">TRIM</span> / <span class="cmd-inline">EXTEND</span></td><td>Pulsa <span class="key-inline">Enter</span> tras seleccionar</td><td>Recorta/extiende contra todos los objetos como límite.</td></tr>
    <tr><td><span class="cmd-inline">COPY</span></td><td>Modo múltiple + desplazamiento</td><td>Copiar una pieza a varias posiciones sin repetir el comando.</td></tr>
  </tbody>
</table>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Olvidar el <strong>punto base</strong> en COPY/MOVE/ROTATE/SCALE. Si eliges un punto lejano, el objeto "salta" a un destino inesperado. Usa siempre un punto apoyado en el objeto (esquina u OSNAP <span class="cmd-inline">END</span>).</span>
</div>

<h3>Mini ejercicio: simetría de puertas con MIRRTEXT=0</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Prepara el conjunto</h4>
    <p>Dibuja una puerta con <span class="cmd-inline">RECTANG</span> más un texto <span class="cmd-inline">TEXT</span> "Puerta 01" junto a ella.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Refleja correctamente</h4>
    <p>Pon <span class="cmd-inline">MIRRTEXT</span> en <strong>0</strong>, selecciona puerta y texto, haz <span class="cmd-inline">MIRROR</span> con eje vertical y comprueba que el texto queda legible.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Limpia con radio 0</h4>
    <p>Haz <span class="cmd-inline">FILLET</span> → <span class="cmd-inline">R</span> → <span class="cmd-inline">0</span> entre las dos líneas de cada esquina para cerrar el contorno sin arcos sobrantes.</p>
  </div>
</div>""",
]

ENRICH["nivel2-precision"] = [
"""<h3>Configurar las ayudas (DSETTINGS)</h3>
<p>Con <span class="cmd-inline">DSETTINGS</span> (o <span class="key-inline">clic derecho</span> sobre el icono OSNAP de la barra de estado) abres la ventana de <strong>Modos de referencia a objetos</strong>. Conviene activar solo 4–5 referencias (Extremo, Medio, Centro, Intersección, Perpendicular) para que AutoCAD no "salte" a una referencia equivocada cuando hay varias cerca.</p>
<ul>
  <li><strong>Rastreo polar (<span class="key-inline">F10</span>):</strong> define los ángulos que disparan la línea guía (15°, 30°, 45°, 90°...).</li>
  <li><strong>Referencia a objetos con rastreo (<span class="key-inline">F11</span>):</strong> muestra guías temporales desde el punto de referencia mientras dibujas el siguiente; clave para alinear sin cálculos.</li>
  <li><strong>ORTO (<span class="key-inline">F8</span>) y polar (<span class="key-inline">F10</span>):</strong> complementarios: ORTO bloquea a 0°/90°; polar permite ángulos adicionales con la misma precisión.</li>
</ul>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Tener todas las ayudas activas a la vez. El cursor "da saltos" que parecen errores: suele ser SNAP (<span class="key-inline">F9</span>) o una referencia no deseada. Cuando algo se mueve de forma rara, desactiva SNAP o limpia las referencias en DSETTINGS.</span>
</div>

<h3>Mini ejercicio: dibujar con rastreo polar a 45°</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Activa la polar</h4>
    <p>Enciende <span class="key-inline">F10</span> y, con <span class="cmd-inline">LINE</span>, mueve el cursor cerca de 45°: verás la guía naranja con "45°".</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Lanza la distancia</h4>
    <p>Mientras ves la guía, escribe <span class="cmd-inline">150</span> y pulsa Enter: AutoCAD dibuja exactamente 150 unidades en esa dirección sin que escribas la coordenada completa.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Combina con OSNAP</h4>
    <p>Con <span class="key-inline">F3</span> activo, apoya una segunda línea en el punto medio (<span class="cmd-inline">MID</span>) del trazo anterior y comprueba que el cursor "chupa" ese punto exacto.</p>
  </div>
</div>""",
]

ENRICH["nivel2-bloques"] = [
"""<h3>Crear, guardar y reutilizar bloques</h3>
<p>El flujo profesional completo de bloques usa cuatro comandos:</p>
<table class="table-cad">
  <thead><tr><th>Comando</th><th>Qué hace</th><th>Cuándo usarlo</th></tr></thead>
  <tbody>
    <tr><td><span class="cmd-inline">BLOCK</span></td><td>Crea un bloque dentro del dibujo actual.</td><td>Elemento que solo usará este archivo.</td></tr>
    <tr><td><span class="cmd-inline">WBLOCK</span></td><td>Guarda el bloque como un .DWG independiente.</td><td>Una librería reutilizable entre proyectos (puertas, mobiliario, símbolos).</td></tr>
    <tr><td><span class="cmd-inline">INSERT</span></td><td>Inserta un bloque (o archivo) con escala, rotación y repetición.</td><td>Colocar la definición en el plano.</td></tr>
    <tr><td><span class="cmd-inline">DCENTER</span></td><td>Centro de diseño: biblioteca de bloques del dibujo y de carpetas.</td><td>Arrastrar bloques de una librería sin escribir comandos.</td></tr>
  </tbody>
</table>
<ul>
  <li><strong>Editar:</strong> haz <strong>doble clic</strong> en un bloque y se abre <span class="cmd-inline">BEDIT</span>. Los cambios se propagan a todas las inserciones.</li>
  <li><strong>Atributos:</strong> define campos editables con <span class="cmd-inline">ATTDEF</span>; al insertar, AutoCAD te pide los valores. Se editan con <span class="cmd-inline">EATTEDIT</span> y se re-sincronizan con <span class="cmd-inline">ATTSYNC</span>.</li>
  <li><strong>Limpiar:</strong> los bloques no usados engordan el archivo; elimínalos con <span class="cmd-inline">PURGE</span>.</li>
</ul>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>El bloque es una <strong>definición</strong>: al cambiar la definición, cambian todas sus inserciones a la vez. Por eso NUNCA rompas un bloque con <span class="cmd-inline">EXPLODE</span> salvo que sea imprescindible: pierdes esa inteligencia.</span>
</div>

<h3>Mini ejercicio: bloque de puerta con atributo de numeración</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Dibuja y define</h4>
    <p>Dibuja una puerta simple (hoja + arco de giro) y crea el bloque con <span class="cmd-inline">BLOCK</span>, nombre "PUERTA" y punto base en la bisagra.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Añade el atributo</h4>
    <p>Descompón (<span class="cmd-inline">EXPLODE</span>), escribe <span class="cmd-inline">ATTDEF</span>, etiqueta <strong>NUMERO</strong>, y redefine el bloque. Insertar te pedirá el número.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Inserta tres puertas</h4>
    <p>Inserta PUERTA en tres huecos con los números 01, 02 y 03. Edita uno con EATTEDIT y comprueba que el resto no se altera.</p>
  </div>
</div>""",
]

ENRICH["nivel2-texto"] = [
"""<h3>Texto de una línea frente a texto multilínea</h3>
<p><span class="cmd-inline">TEXT</span> crea líneas sueltas; <span class="cmd-inline">MTEXT</span> crea un párrafo dentro de un rectángulo. Regla práctica: <strong>etiquetas cortas con TEXT, notas y párrafos con MTEXT</strong>. El multilínea permite columnas, listas, símbolos, subrayados y fuentes mixtas en un solo objeto fácil de mover.</p>
<ul>
  <li><strong>Estilo con STYLE:</strong> define la fuente y la altura; el texto hereda el estilo. Nunca cambies la fuente objeto a objeto.</li>
  <li><strong>Revisión de ortografía:</strong> <span class="cmd-inline">SPELL</span> (<span class="key-inline">SP</span>) revisa todo el dibujo.</li>
  <li><strong>Tablas:</strong> <span class="cmd-inline">TABLE</span> crea cuadros de datos que se rellenan y expanden; ideal para cuadros de acabados o de áreas.</li>
  <li><strong>Campos:</strong> dentro de MTEXT, clic derecho → Insertar campo → <strong>Objeto</strong> → área de polígono: el valor se actualiza solo (ver ejercicio).</li>
  <li><strong>Anotativo:</strong> marca el estilo como anotativo si el texto debe escalarse con el layout (Nivel 3).</li>
</ul>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Aplanar textos a líneas (TXTEXP o similar). En planos editables los textos deben seguir siendo texto; solo "aplanar" cuando el archivo ya no se va a modificar.</span>
</div>

<h3>Mini ejercicio: cuadro de áreas que se actualiza solo</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Crea un campo de área</h4>
    <p>Dibuja un rectángulo de 300 x 200 y, dentro de un MTEXT, inserta el campo <strong>Objeto → área de polígono</strong> seleccionando el rectángulo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Cambia la geometría</h4>
    <p>Mueve una esquina del rectángulo y escribe <span class="cmd-inline">REGEN</span> (<span class="key-inline">RE</span>): el campo se actualiza a la nueva área.</p>
  </div>
</div>""",
]

ENRICH["nivel2-hatch"] = [
"""<h3>Dos formas de crear el contorno</h3>
<ul>
  <li><strong>Punto interior (Pick points):</strong> clic dentro del área; AutoCAD detecta el contorno cerrado. Rápido, pero exige un borde perfectamente sellado.</li>
  <li><strong>Seleccionar objetos (Select):</strong> eliges los objetos del borde. Más tolerante con fronteras intermedias.</li>
  <li><strong>Islas:</strong> si el relleno contiene un hueco cerrado (por ejemplo un círculo), la detección de islas lo respeta y deja el interior limpio.</li>
  <li><strong>Origen:</strong> punto desde el que empieza a repetirse el patrón; útil para alinear zonas rellenas consecutivas.</li>
</ul>
<p>El patrón <strong>SOLID</strong> rellena de color plano; los patrones con nombre (ANSI31, AR-CONC, GRAVEL...) representan materiales. La <strong>escala</strong> debe acompañar a la escala del plano: un ladrillo diminuto en un plano a 1:100 se vuelve una mancha gris.</p>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>"Boundary definition error": el contorno no está cerrado. Acércate con zoom, sella las esquinas con <span class="cmd-inline">FILLET</span> radio 0 o <span class="cmd-inline">JOIN</span>, y vuelve a intentarlo.</span>
</div>

<h3>Mini ejercicio: rellenar un pilar y dejar su hueco</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Dibuja la pieza</h4>
    <p>Dibuja un rectángulo de 200 x 200 y dentro un círculo de radio 50.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Aplica el hatch con isla</h4>
    <p>Con <span class="cmd-inline">HATCH</span>, patrón ANSI31, escala <span class="cmd-inline">1</span>, haz clic dentro del rectángulo (fuera del círculo). Queda el área rellena y el círculo intacto.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Edítalo</h4>
    <p>Doble clic en el hatch y cambia escala a <span class="cmd-inline">2</span> y ángulo a <span class="cmd-inline">45°</span>: todo el relleno se actualiza al instante.</p>
  </div>
</div>""",
]

ENRICH["nivel2-seleccion"] = [
"""<h3>Selecciones que se dibujan, no se arrastran</h3>
<p>Además de la ventana y la cruzante rectangulares, AutoCAD permite polígonos y lazos:</p>
<table class="table-cad">
  <thead><tr><th>Modo</th><th>Palabra clave</th><th>Qué selecciona</th></tr></thead>
  <tbody>
    <tr><td>Ventana poligonal</td><td><span class="cmd-inline">WP</span></td><td>Objetos dentro de un polígono que dibujas a mano.</td></tr>
    <tr><td>Cruzante poligonal</td><td><span class="cmd-inline">CP</span></td><td>Todo lo que toca o cruza tu polígono.</td></tr>
    <tr><td>Lazo (lasso)</td><td>Sostener el clic al arrastrar</td><td>Rectángulo que se convierte en lazo; izquierda–derecha = ventana, al revés = cruzante.</td></tr>
    <tr><td>Todo / Último</td><td><span class="cmd-inline">ALL</span> / <span class="cmd-inline">LAST</span></td><td>Todo el modelo o solo el último objeto creado.</td></tr>
    <tr><td>Añadir / Quitar</td><td><span class="cmd-inline">A</span> / <span class="cmd-inline">R</span></td><td>Sumar o restar objetos a la selección actual.</td></tr>
  </tbody>
</table>
<p>Escribe estas palabras mientras AutoCAD te pide "Select objects" y combínalas con <span class="key-inline">Shift</span> para descartar casos concretos.</p>
<div class="callout">
  <span class="callout-title">Truco encadenado</span>
  <span>Una buena selección es la mitad del comando: tras mover/copiar, la tecla <span class="cmd-inline">P</span> recupera la <strong>selección anterior</strong> para el siguiente comando.</span>
</div>

<h3>Mini ejercicio: retícula de pilares en un clic</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Prepara la retícula</h4>
    <p>Dibuja 20 círculos como columnas y mézclalos con líneas de ejes.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Selecciona solo los círculos</h4>
    <p>Ejecuta <span class="cmd-inline">ERASE</span> y, cuando pida selección, escribe <span class="cmd-inline">CP</span> y rodea toda la retícula. Comprueba que se eliminan los círculos y se quedan las líneas.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Corrige con filtro</h4>
    <p>Pulsa <span class="key-inline">Escape</span>, usa <span class="cmd-inline">SELECTSIMILAR</span> sobre un círculo restante y borra; el filtro respeta el tipo de objeto.</p>
  </div>
</div>""",
]

ENRICH["nivel2-lineas"] = [
"""<h3>Escala del tipo de línea: de dónde vienen los "fallos"</h3>
<p>Un tipo de línea discontinua se ve "continua" cuando su escala no coincide con el tamaño del dibujo. Tres variables lo controlan:</p>
<table class="table-cad">
  <thead><tr><th>Variable</th><th>Alcance</th><th>Uso</th></tr></thead>
  <tbody>
    <tr><td><span class="cmd-inline">LTSCALE</span> (<span class="key-inline">LTS</span>)</td><td>Todo el dibujo</td><td>Multiplica la escala global de todos los tipos de línea.</td></tr>
    <tr><td><span class="cmd-inline">CELTSCALE</span></td><td>Objetos nuevos</td><td>Escala adicional para lo que dibujas a partir de ahora.</td></tr>
    <tr><td>Escala por objeto</td><td>Objeto seleccionado</td><td>En PROPIEDADES (<span class="key-inline">Ctrl+1</span>), campo "Escala de tipo de línea".</td></tr>
  </tbody>
</table>
<p>Regla rápida: un plano en metros suele funcionar con <span class="cmd-inline">LTS</span> próximo a 1; uno en milímetros necesita valores grandes (por ejemplo 1000) para que las rayas se distingan.</p>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Asignar el tipo de línea objeto a objeto en lugar de a la capa. Un objeto "a mano" con línea continua dentro de una capa de ejes rompe el sistema: si cambias la capa, ese objeto no obedece. Usa cualidades ByLayer.</span>
</div>

<h3>Mini ejercicio: ejes que se ven y se ocultan</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Carga CENTER</h4>
    <p>Con <span class="cmd-inline">LINETYPE</span>, carga <strong>CENTER</strong> y asígnalo a la capa de ejes.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Escala a la vista</h4>
    <p>Dibuja el eje y prueba <span class="cmd-inline">LTS</span> con valores 1, 10 y 100. Elige el punto donde las rayas se distingan con claridad.</p>
  </div>
</div>""",
]

ENRICH["nivel2-puntos"] = [
"""<h3>Puntos con bloque: la versión profesional</h3>
<p>DIVIDE y MEASURE también pueden colocar un <strong>bloque</strong> (opción Block) en cada intervalo: la forma correcta de distribuir pilares, postes o barandillas a lo largo de un eje.</p>
<table class="table-cad">
  <thead><tr><th>Valor PDMODE</th><th>Apariencia</th></tr></thead>
  <tbody>
    <tr><td>0</td><td>Punto invisible (causa habitual del "no veo los puntos").</td></tr>
    <tr><td>1</td><td>Punto nulo.</td></tr>
    <tr><td>2</td><td>X.</td></tr>
    <tr><td>3</td><td>Barra vertical.</td></tr>
    <tr><td>4</td><td>Cuadrado.</td></tr>
    <tr><td>35</td><td>Cuadrado relleno con centro (el más visible).</td></tr>
  </tbody>
</table>
<p><span class="cmd-inline">PDSIZE</span> define el tamaño: <strong>negativo</strong> = porcentaje del alto de pantalla (se mantiene al hacer zoom); <strong>positivo</strong> = unidades fijas del dibujo.</p>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>"Escribí DIVIDE y no veo nada": casi siempre es PDMODE en 0 o PDSIZE diminuto. Configúralos ANTES de dividir.</span>
</div>

<h3>Mini ejercicio: postes cada 2 m con MEASURE</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Prepara la plantilla</h4>
    <p>Dibuja un poste (cuadrado de 0.2) y conviértelo en bloque "POSTE".</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Distribuye</h4>
    <p>Con <span class="cmd-inline">MEASURE</span>, elige la polilínea del eje, opción <strong>Block</strong> → POSTE y distancia <span class="cmd-inline">2</span>. AutoCAD reparte postes cada 2 m hasta el final.</p>
  </div>
</div>""",
]

ENRICH["nivel2-auxiliares"] = [
"""<h3>Opciones del comando XLINE</h3>
<p><span class="cmd-inline">XLINE</span> (<span class="key-inline">XL</span>) crea líneas infinitas con varias opciones:</p>
<ul>
  <li><strong>Horizontal (H) / Vertical (V):</strong> ejes rectos a 0° o 90°.</li>
  <li><strong>Ángulo (A):</strong> línea infinita con un ángulo dado; útil para piezas giradas.</li>
  <li><strong>Bisectriz (B):</strong> divide el ángulo entre dos puntos.</li>
  <li><strong>Offset (O):</strong> duplica la xline a una distancia exacta.</li>
</ul>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>La geometría auxiliar NO debe imprimirse. La forma garantizada de lograrlo es ponerla en una capa "Aux" con impresión desactivada (ver capas), no borrarla a mano.</span>
</div>

<h3>Mini ejercicio: ejes de un plano de muros</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Traza los ejes</h4>
    <p>Crea la capa "Aux" (color 8, no imprimible) y traza tres <span class="cmd-inline">XLINE</span> verticales a 0, 3000 y 6000, y dos horizontales a 0 y 4000.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Dibuja sobre ellas</h4>
    <p>Con <span class="cmd-inline">PLINE</span> en la capa de muros, usa las intersecciones (OSNAP <span class="cmd-inline">INT</span>) como guía y traza el cerco.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Limpia la vista</h4>
    <p>Congela la capa Aux o apágala y el plano queda solo con los muros, sin borrar nada.</p>
  </div>
</div>""",
]

ENRICH["nivel2-propiedades"] = [
"""<h3>Ver y copiar propiedades al vuelo</h3>
<ul>
  <li><strong>Propiedades rápidas:</strong> con ellas, un clic en un objeto muestra capa/color/tipo sin abrir el panel completo.</li>
  <li><strong>LIST (<span class="cmd-inline">LI</span>):</strong> vuelca en la línea de comandos un informe detallado (coordenadas, área, longitud, capa...); ideal para verificar geometría.</li>
  <li><strong>MATCHPROP por zona:</strong> con <span class="cmd-inline">MA</span> arrastra <strong>sobre varios objetos</strong> y todos adoptan el formato de origen de una sola pasada.</li>
</ul>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Cambiar color o tipo de línea de un objeto a mano en lugar de usar la capa. Ese objeto deja de obedecer al sistema y el plano se vuelve imposible de agrupar. Mantén ByLayer como hábito.</span>
</div>

<h3>Mini ejercicio: da formato a una serie de objetos</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Prepara el origen</h4>
    <p>Dibuja una línea en la capa "Muros" (color ByLayer) y otra suelta en la capa "Aux".</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Aplica el formato</h4>
    <p>Con <span class="cmd-inline">MA</span>, selecciona la línea de Muros como origen y haz clic en la otra: adopta capa y color de Muros al instante.</p>
  </div>
</div>""",
]

ENRICH["nivel2-pedit"] = [
"""<h3>Unir varias polilíneas a la vez</h3>
<p>Si terminas una sesión con decenas de segmentos sueltos, <span class="cmd-inline">JOIN</span> (<span class="key-inline">J</span>) une <strong>todos</strong> los objetos seleccionados en una sola polilínea cuando están conectados por los extremos.</p>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>JOIN falla en silencio cuando los extremos no coinciden exactamente: líneas que "parecen" tocarse pero no comparten punto. Acércate con zoom, usa OSNAP <span class="cmd-inline">END</span>, une el hueco con un trazo corto o aplica <span class="cmd-inline">FILLET</span> con radio 0.</span>
</div>

<h3>Mini ejercicio: contorno de muro rellenable en 3 pasos</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Segmentos sueltos</h4>
    <p>Dibuja un cuadrado de 400 con <span class="cmd-inline">LINE</span> (4 trazos) y déjalo abierto en una esquina.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Une y cierra</h4>
    <p>Con <span class="cmd-inline">PEDIT</span>: selecciona el primer trazo → <span class="cmd-inline">S</span> (convertir) → <span class="cmd-inline">J</span> (join) → <span class="cmd-inline">C</span> (cerrar).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Rellena</h4>
    <p>Aplica <span class="cmd-inline">HATCH</span> con punto interior: ahora sí reconoce el contorno cerrado.</p>
  </div>
</div>""",
]

ENRICH["nivel2-splines"] = [
"""<h3>Puntos de ajuste frente a puntos de control</h3>
<p>Al dibujar con <span class="cmd-inline">SPLINE</span>, AutoCAD pregunta por el método: <em>Control</em> arrastra la curva por puntos tensores (más matemática) y <em>Fit</em> hace que pase por los puntos que tocas (más intuitiva, preferida en topografía).</p>
<ul>
  <li><strong>Cerrada:</strong> la opción <span class="cmd-inline">Close</span> une el final con el inicio formando un lazo continuo.</li>
  <li><strong>Tolerancia:</strong> 0 pasa por los puntos exactos; subirla suaviza y aleja la curva del punteo (útil con curvas muy ruidosas).</li>
  <li><strong>De polilínea a spline:</strong> <span class="cmd-inline">PEDIT</span> → Spline; y al revés con <span class="cmd-inline">SPLINEDIT</span> → Decurve.</li>
</ul>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>La spline no se acota con ángulos fijos; en fabricación se prefiere polilínea con arcos tangentes. Reserva la spline para curvas de terreno o diseño libre.</span>
</div>

<h3>Mini ejercicio: curva de nivel cerrada</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Traza</h4>
    <p>Con <span class="cmd-inline">SPLINE</span>, método Fit, toca 6 puntos formando un bucle irregular.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Cierra y suaviza</h4>
    <p>Elige <span class="cmd-inline">Close</span> y luego edita con <span class="cmd-inline">SPLINEDIT</span> subiendo la tolerancia hasta 5; compara el resultado.</p>
  </div>
</div>""",
]

# ----------------------------------------------------------------------------
# 3) Lecciones nuevas (contenido completo)
# ----------------------------------------------------------------------------

NEW_SECTIONS = {}

NEW_SECTIONS["nivel2-matrices"] = """
<h2><span class="sec-num">N</span>Matrices: repite objetos en patrón (ARRAY)</h2>
<p>Una <strong>matriz</strong> (<span class="cmd-inline">ARRAY</span>, <span class="key-inline">AR</span>) repite un objeto o grupo siguiendo un patrón. Es la herramienta más rápida para retículas de pilares, gradas, luminares, barandillas o muros repetidos, y al ser <strong>asociativa</strong> puedes retocar todo el patrón después con un solo clic.</p>

<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Desde AutoCAD 2012 la matriz es asociativa: vive como un solo objeto y sus parámetros (filas, columnas, ángulo...) se editan después sin borrar nada. Si la descompones con <span class="cmd-inline">EXPLODE</span>, pierdes esa inteligencia.</span>
</div>

<h3>Los tres tipos de matriz</h3>
<table class="table-cad">
  <thead><tr><th>Tipo</th><th>Cómo se define</th><th>Uso típico</th></tr></thead>
  <tbody>
    <tr><td>Rectangular</td><td>Filas y columnas, su separación y el ángulo de la rejilla.</td><td>Retícula de pilares, sillas de auditorio, módulos de fachada.</td></tr>
    <tr><td>Polar (circular)</td><td>Centro + número de elementos + ángulo total (360° = círculo completo).</td><td>Radios de ruedas, palas, gradas radiales, luminares alrededor de una columna.</td></tr>
    <tr><td>De ruta (path)</td><td>Seleccionas la polilínea/curva guía y la separación.</td><td>Barandillas, bordillos, postes a lo largo de un vial curvo.</td></tr>
  </tbody>
</table>

<h3>Parámetros que definen el resultado</h3>
<ul>
  <li><strong>Filas y columnas:</strong> cuántas repeticiones en cada dirección.</li>
  <li><strong>Separación entre filas y columnas:</strong> en unidades del dibujo.</li>
  <li><strong>Ángulo (rectangular):</strong> rota toda la rejilla respecto al eje global.</li>
  <li><strong>Ángulo total (polar):</strong> 360 coloca los elementos alrededor del círculo completo.</li>
  <li><strong>Rellenar ruta (path):</strong> reparte N objetos a lo largo de toda la curva o define la distancia exacta entre ellos.</li>
</ul>

<h3>Editar y descomponer</h3>
<p>Al crear la matriz aparece la cinta <strong>ARRAY</strong> con todos los valores editables. También puedes seleccionar la matriz y estirar su rango con los <strong>pinzamientos</strong>. Cuando el patrón ya no deba cambiar, descompón con <span class="cmd-inline">EXPLODE</span> para obtener copias independientes.</p>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Pensar que COPY a mano es lo mismo. COPY sirve para pocas copias dispersas; ARRAY es para patrones regulares. Además, al editar el objeto original de una matriz asociativa, TODAS las copias se actualizan.</span>
</div>

<h3>Mini ejercicio: retícula de pilares 5 x 4</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>El pilar base</h4>
    <p>Dibuja un cuadrado de 0.5 x 0.5 y conviértelo en bloque "PILAR" (también funciona sin bloque).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Matriz rectangular</h4>
    <p>Con <span class="cmd-inline">ARRAY</span> → <strong>Rectangular</strong>: 5 columnas, 4 filas, separación 5 en X y 4 en Y.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Corrige en vivo</h4>
    <p>Abre la cinta ARRAY, cambia las columnas a 6 y la separación a 6; observa la retícula recomponerse al instante.</p>
  </div>
</div>
"""

NEW_SECTIONS["nivel2-grips"] = """
<h2><span class="sec-num">N</span>Pinzamientos (GRIPS): edición rápida sin comandos</h2>
<p>Al seleccionar un objeto sin ejecutar ningún comando, AutoCAD muestra unos <strong>cuadraditos azules</strong> en sus puntos clave: son los <strong>pinzamientos (grips)</strong>. Con ellos estiras, mueves, rotas, escalas o copias sin teclear un solo comando.</p>

<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Pinzamiento cálido (azul) frente a <strong>activo</strong> (rojo): haz clic una vez en el grip para activarlo. A partir de ahí, pulsa <span class="key-inline">Espacio</span> o clic derecho para recorrer el menú <strong>Estirar / Mover / Rotar / Escalar / Copiar</strong>.</span>
</div>

<h3>El flujo de edición con grips</h3>
<ol>
  <li><strong>Selecciona</strong> el objeto (sin comando).</li>
  <li>Haz clic en el <strong>pinzamiento</strong> del punto que quieres controlar (se activa en rojo).</li>
  <li>Pulsa <span class="key-inline">Espacio</span> o clic derecho para alternar el modo de edición.</li>
  <li>Teclea el valor o usa OSNAP/referencia y Enter.</li>
  <li><span class="key-inline">Escape</span> cuando termines (una vez suelta el grip, otra quita el marco).</li>
</ol>

<h3>Comportamiento por tipo de objeto</h3>
<table class="table-cad">
  <thead><tr><th>Objeto</th><th>Qué controla el grip</th></tr></thead>
  <tbody>
    <tr><td>Línea</td><td>Extremos (estiran) y punto medio (mueve).</td></tr>
    <tr><td>Polilínea</td><td>Cada vértice (estira) y el punto medio de cada segmento.</td></tr>
    <tr><td>Círculo</td><td>Centro (mueve) y cuadrantes (escalan el radio).</td></tr>
    <tr><td>Rectángulo</td><td>Esquinas (estiran) y centro de cada lado.</td></tr>
    <tr><td>Texto</td><td>Punto de inserción y de alineación.</td></tr>
  </tbody>
</table>

<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Esperar que un grip estire todo el objeto. El grip de extremo estira esa esquina; el <strong>grip central</strong> (por ejemplo el del rectángulo) mueve el objeto completo. Si quieres moverlo todo con precisión, activa el grip central y escribe la distancia.</span>
</div>

<h3>Mini ejercicio: escalar una puerta con un grip</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Prepara</h4>
    <p>Dibuja la hoja de una puerta (rectángulo de 100 x 20).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Escala por grip</h4>
    <p>Selecciona el rectángulo, activa el grip inferior izquierdo, pulsa <span class="key-inline">Espacio</span> hasta <strong>Escalar</strong> y escribe <span class="cmd-inline">1.5</span>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Copia en cadena</h4>
    <p>Vuelve a activar el grip, elige el modo <strong>Copiar</strong> y haz clic en 3 posiciones: el cuadrado se multiplica sin borrar el original.</p>
  </div>
</div>
"""

NEW_SECTIONS["nivel2-consulta"] = """
<h2><span class="sec-num">N</span>Medición y verificación del dibujo</h2>
<p>Antes de imprimir o entregar un plano hay que <strong>verificar</strong>: distancias, áreas, coordenadas y datos de los objetos. Estas herramientas son de las más usadas del día a día (<span class="cmd-inline">DIST</span>, <span class="cmd-inline">AREA</span>, <span class="cmd-inline">MEASUREGEOM</span>, <span class="cmd-inline">LIST</span>, <span class="cmd-inline">ID</span>).</p>

<h3>Comandos de consulta</h3>
<table class="table-cad">
  <thead><tr><th>Comando</th><th>Atajo</th><th>Qué devuelve</th></tr></thead>
  <tbody>
    <tr><td><span class="cmd-inline">DIST</span></td><td><span class="key-inline">DI</span></td><td>Distancia entre dos puntos, ángulo y deltas X/Y.</td></tr>
    <tr><td><span class="cmd-inline">AREA</span></td><td><span class="key-inline">AREA</span></td><td>Área y perímetro de un contorno (por puntos u objeto).</td></tr>
    <tr><td><span class="cmd-inline">MEASUREGEOM</span></td><td><span class="key-inline">MEA</span></td><td>Todo en uno: distancia, radio, ángulo, área y volumen.</td></tr>
    <tr><td><span class="cmd-inline">AREA</span> → <span class="cmd-inline">O</span></td><td>—</td><td>Área de una polilínea o región cerrada.</td></tr>
    <tr><td><span class="cmd-inline">LIST</span></td><td><span class="key-inline">LI</span></td><td>Informe completo del objeto: capa, coordenadas, longitud, área, identidad.</td></tr>
    <tr><td><span class="cmd-inline">ID</span></td><td><span class="key-inline">ID</span></td><td>Coordenadas X, Y, Z del punto elegido.</td></tr>
  </tbody>
</table>

<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>La medición en AutoCAD es digital y exacta: no "aproxima". Si DIST devuelve 1234,5678 esa es la medida real, aunque el plano tenga decimales ocultos. Verifica antes de acotar.</span>
</div>

<h3>Verificar un plano: checklist rápido</h3>
<ul>
  <li><strong>Distancias de muro a ventana:</strong> DIST entre los puntos de referencia.</li>
  <li><strong>Áreas de locales:</strong> AREA → O sobre el contorno; compárala con la del cuadro de áreas.</li>
  <li><strong>Radio de un arco:</strong> MEA → Radio.</li>
  <li><strong>Coordenada de un punto:</strong> ID para saber dónde está exactamente.</li>
  <li><strong>Geometría dudosa:</strong> LIST para revisar que la línea "recta" no tenga vértices ocultos.</li>
</ul>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Medir con la regla visual (contando rayas de la rejilla). Las ayudas visuales pueden estar desescaladas; la única medida fiable es la del comando.</span>
</div>

<h3>Mini ejercicio: auditoría de 5 minutos</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Objeto a auditar</h4>
    <p>Dibuja una polilínea cerrada (un módulo de 400 x 300) y un círculo de radio 50 en su interior.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Mide el módulo</h4>
    <p>Con <span class="cmd-inline">AREA</span> → <span class="cmd-inline">O</span> selecciona la polilínea: debe devolver 120000 (400 x 300).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Cruza datos</h4>
    <p>Mide el lado con <span class="cmd-inline">DIST</span>, el centro del círculo con <span class="cmd-inline">ID</span> y usa <span class="cmd-inline">LIST</span> para comprobar que el área del anillo (módulo − círculo) coincide con el dato del plano.</p>
  </div>
</div>
"""

# 4) Construcción de las páginas
# ----------------------------------------------------------------------------

def extract_existing_block(file):
    """Devuelve el contenido del <section data-topic> de una lección existente,
    incluyendo el botón "marcar visto" final."""
    path = os.path.join(DST, file)
    html = read(path)
    i = html.find('<section id="')
    if i < 0:
        raise SystemExit("No se encontró sección en " + file)
    j = html.find("</section", i)
    return html[i:j].rstrip()


SENT_START = "<!-- ENRIQ START -->"
SENT_END = "<!-- ENRIQ END -->"


def build_section(data_topic, idx, title):
    """Construye el <section> completo de una lección (nueva o enriquecida)."""
    if data_topic in NEW_SECTIONS:
        body = NEW_SECTIONS[data_topic].replace("<span class=\"sec-num\">N</span>", "<span class=\"sec-num\">%d</span>" % (idx + 1))
        body = body.rstrip()
        btn_html = '\n\n<button class="mark-done-btn"><i class="bi bi-check-circle"></i> Marcar tema como visto</button>'
        if "mark-done-btn" not in body:
            body = body + btn_html
    else:
        body = extract_existing_block(TOPIC_META[data_topic][1])
        body = re.sub(r'<span class="sec-num">\d+</span>', '<span class="sec-num">%d</span>' % (idx + 1), body)
        # quita un enriquecimiento previo (idempotencia)
        if SENT_START in body and SENT_END in body:
            i = body.index(SENT_START)
            j = body.index(SENT_END) + len(SENT_END)
            body = body[:i].rstrip() + "\n" + body[j:].lstrip()
        extra = "\n".join(ENRICH.get(data_topic, []))
        if extra.strip():
            # inserta el enriquecimiento antes del botón "marcar visto"
            btn = '<button class="mark-done-btn">'
            if btn in body:
                head, _, tail = body.partition(btn)
                wrapped = SENT_START + "\n" + extra.lstrip() + "\n" + SENT_END + "\n" + btn
                body = head.rstrip() + "\n\n" + wrapped + tail
            else:
                body = body + "\n\n" + SENT_START + "\n" + extra.lstrip() + "\n" + SENT_END
    body = body.rstrip()
    opening = '<section id="%s" data-topic="%s">' % (TOPIC_META[data_topic][1].replace(".html", ""), data_topic)
    # si el bloque ya trae el <section>, lo normalizamos; si no, lo envolvemos
    if body.strip().startswith("<section"):
        body = re.sub(r"<section\b[^>]*>", opening, body, count=1)
        if not body.rstrip().endswith("</section"):
            body = body + "\n</section>"
    else:
        opening_txt = opening + "\n"
        body = opening_txt + indent(body, 14) + "\n</section>"
    return body


def first_para_desc(block):
    m = re.search(r"<p(?![^>]*class)[^>]*>(.*?)</p>", block, re.S)
    if not m:
        return ""
    text = re.sub(r"<[^>]+>", "", m.group(1))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:150] + ("…" if len(text) > 150 else "")


def build_toc(lessons, autoeval_href):
    lis = []
    for dt, fname, title, label, desc in lessons:
        lis.append(f'            <li><a href="{fname}" data-toc="{dt}"><span class="toc-check"></span> {label}</a></li>')
    lis.append(f'            <li><a href="{autoeval_href}"><span class="toc-check"></span> Autoevaluación</a></li>')
    return "\n".join(lis)


def build_lesson_page(dt, idx, lessons):
    fname = TOPIC_META[dt][1]
    title = TOPIC_META[dt][2]
    section = build_section(dt, idx, title)
    block = section
    desc = TOPIC_META[dt][4]
    toc = build_toc(lessons, "index.html#autoevaluacion")

    prev_t = lessons[idx - 1] if idx > 0 else None
    next_t = lessons[idx + 1] if idx + 1 < len(lessons) else None

    if prev_t:
        nav_prev = f"""<a href="{prev_t[1]}">
            <span class="nav-label">Anterior</span>
            <span class="nav-title"><i class="bi bi-arrow-left"></i> {prev_t[3]}</span>
          </a>"""
    else:
        nav_prev = "<span></span>"
    if next_t:
        nav_next = f"""<a href="{next_t[1]}" class="nav-next">
            <span class="nav-label">Siguiente</span>
            <span class="nav-title">{next_t[3]} <i class="bi bi-arrow-right"></i></span>
          </a>"""
    else:
        nav_next = """<a href="index.html#autoevaluacion" class="nav-next">
            <span class="nav-label">Siguiente</span>
            <span class="nav-title">Autoevaluación <i class="bi bi-arrow-right"></i></span>
          </a>"""

    page = f"""<!DOCTYPE html>
<html lang="es" data-theme="dark">
{build_head(f"{title} · Nivel {NUM} — AutoCAD Guía", f"/paginas/{FOLDER}/{fname}", desc, include_3d=False, schema_name=SCHEMA_NAME, schema_desc=SCHEMA_DESC)}

<body>

<a href="#main-content" class="skip-link">Saltar al contenido principal</a>

{build_navbar(NUM)}

<header class="page-header" id="main-content">
  <div class="container container-xl">
    <p class="crumb"><a href="../../index.html">Inicio</a> / <a href="../../index.html#niveles">Niveles</a> / <a href="index.html">{FULL_TITLE}</a> / Tema {idx+1}</p>
    <span class="eyebrow" data-i18n="lvl{NUM}.eyebrow">{EYEBROW}</span>
    <h1>{title}</h1>
    <div class="level-progress-bar" data-level-prefix="nivel{NUM}" data-level-total="{TOTAL}"><div class="fill"></div></div>
    <p class="level-progress-label">0 de {TOTAL} temas completados · 0%</p>
  </div>
</header>

<div class="content-layout">
  <div class="container container-xl">
    <div class="row">

      <aside class="col-lg-3 mb-5 mb-lg-0">
        <div class="toc-sidebar">
          <h6 data-i18n="ui.inThisLevel">En este nivel</h6>
          <ul class="toc-list">
{toc}
          </ul>
          <hr style="border-color:var(--border-soft)" class="my-4">
          <a href="index.html" class="btn-cad-outline w-100 text-center d-block"><i class="bi bi-arrow-left"></i> Volver al índice</a>
        </div>
      </aside>

      <div class="col-lg-9">
        <article class="content-article">

{indent(block, 10)}

        </article>

        <nav class="level-nav">
          {nav_prev}
          {nav_next}
        </nav>
      </div>
    </div>
  </div>
</div>

{build_footer()}

{build_end_block()}

{build_scripts(NUM, include_quiz=False, include_babylon=False)}

</body>
</html>
"""
    write(os.path.join(DST, fname), page)


def build_portada(lessons, visuals, quiz):
    toc = build_toc(lessons, "#autoevaluacion")
    cards = []
    for idx, (dt, fname, title, label, desc) in enumerate(lessons, 1):
        cards.append(f"""                    <div class="col-md-6 col-lg-4" data-aos="fade-up" data-aos-delay="{((idx-1)%3)*80}">
                      <a href="{fname}" class="text-decoration-none">
                        <div class="level-card">
                          <div class="level-index">{str(idx).zfill(2)}</div>
                          <span class="level-tag">Tema {idx}</span>
                          <h3>{label}</h3>
                          <p>{desc}</p>
                        </div>
                      </a>
                    </div>""")
    next_btn = '<a href="../nivel-3-organizacion/index.html" class="btn-cad-outline w-100 text-center d-block">Siguiente nivel <i class="bi bi-arrow-right"></i></a>'
    nav_next = """<a href="../nivel-3-organizacion/index.html" class="nav-next">
            <span class="nav-label">Siguiente</span>
            <span class="nav-title">Siguiente nivel <i class="bi bi-arrow-right"></i></span>
          </a>"""
    page = f"""<!DOCTYPE html>
<html lang="es" data-theme="dark">
{build_head(f"Nivel {NUM} · {FULL_TITLE} — AutoCAD Guía", f"/paginas/{FOLDER}/index.html", LEVELS[2][4], include_3d=False, schema_name=SCHEMA_NAME, schema_desc=SCHEMA_DESC)}

<body>

<a href="#main-content" class="skip-link">Saltar al contenido principal</a>

{build_navbar(NUM)}

<header class="page-header" id="main-content">
  <div class="container container-xl">
    <p class="crumb"><a href="../../index.html">Inicio</a> / <a href="../../index.html#niveles">Niveles</a> / {FULL_TITLE}</p>
    <span class="eyebrow" data-i18n="lvl{NUM}.eyebrow">{EYEBROW}</span>
    <h1 data-i18n="lvl{NUM}.title">{FULL_TITLE}</h1>
    <p class="subtitle" data-i18n="lvl{NUM}.subtitle">{LEVELS[2][4]}</p>
    <div class="level-progress-bar" data-level-prefix="nivel{NUM}" data-level-total="{TOTAL}"><div class="fill"></div></div>
    <p class="level-progress-label">0 de {TOTAL} temas completados · 0%</p>
  </div>
</header>

<div class="content-layout">
  <div class="container container-xl">
    <div class="row">

      <aside class="col-lg-3 mb-5 mb-lg-0">
        <div class="toc-sidebar">
          <h6 data-i18n="ui.inThisLevel">En este nivel</h6>
          <ul class="toc-list">
{toc}
          </ul>
          <hr style="border-color:var(--border-soft)" class="my-4">
          {next_btn}
        </div>
      </aside>

      <div class="col-lg-9">
        <article class="content-article">
          <section class="level-intro">
            <h2>Contenido del nivel</h2>
            <p>Este nivel se divide en {TOTAL} temas. Sigue el orden recomendado o salta directamente al que necesites.</p>
            <div class="row g-4 mt-1">
{chr(10).join(cards)}
            </div>
          </section>

{indent(visuals, 10)}
{indent(quiz, 10)}

        </article>

        <nav class="level-nav">
          <span></span>
          {nav_next}
        </nav>
      </div>
    </div>
  </div>
</div>

{build_footer()}

{build_end_block()}

{build_scripts(NUM, include_quiz=True, include_babylon=False)}

</body>
</html>
"""
    write(os.path.join(DST, "index.html"), page)


def extract_portada_parts():
    """Extrae secciones visuales y quiz de la portada actual."""
    html = read(os.path.join(DST, "index.html"))
    visuals = quiz = ""
    tag_re = re.compile(r"<(/?)\s*section\b")
    depth = 0
    start = None
    for m in tag_re.finditer(html):
        if m.group(1) == "":
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0 and start is not None:
                block = html[start:m.end()]
                if "inline-visual-examples" in block and "quiz-section" not in block:
                    visuals = block
                elif "quiz-section" in block:
                    quiz = block
                start = None
    return visuals, quiz


# ----------------------------------------------------------------------------
# 5) main()
# ----------------------------------------------------------------------------

# Orden de las lecciones nuevas: se insertan justo después de la lección previa
# (que ya existe en search-index.js).
NEW_ANCHOR = {
    "nivel2-matrices":   "nivel-2-dibujo-2d/modificacion.html",
    "nivel2-grips":      "nivel-2-dibujo-2d/seleccion.html",
    "nivel2-consulta":   "nivel-2-dibujo-2d/auxiliares.html",
}


def update_search_index(topics):
    path = os.path.join(ROOT, "assets", "js", "search-index.js")
    txt = read(path)
    blocks = []
    for dt, fname, title, label, desc in topics:
        if dt not in NEW_SECTIONS:
            continue
        # idempotente: no duplicar una entrada ya insertada
        own = f'    "file": "{FOLDER}/{fname}",'
        if own in txt:
            continue
        prev_file = NEW_ANCHOR[dt]
        block = ('  {\n'
                 '    "type": "topic",\n'
                 f'    "title": "{title}",\n'
                 f'    "description": "{desc}",\n'
                 f'    "file": "{FOLDER}/{fname}",\n'
                 '    "anchor": "",\n'
                 '    "path": "Nivel 2 · Dibujo 2D"\n'
                 '  },')
        blocks.append((prev_file, block))
    for marker, block in blocks:
        needle = f'    "file": "{marker}",'
        if needle not in txt:
            raise SystemExit("No se encontró el ancla para insertar tras: " + marker)
        i = txt.index(needle)
        j = txt.index("  },", i) + len("  },")
        txt = txt[:j] + "\n" + block + txt[j:]
    write(path, txt)
    print("search-index.js: entradas nuevas insertadas:", len(blocks))


def update_sitemap():
    urls = ["/", "/paginas/comandos.html", "/paginas/ejemplos-visuales.html", "/paginas/trucos.html", "/paginas/tips.html", "/paginas/recursos.html", "/paginas/faq.html", "/404.html"]
    for num, (folder, *_rest) in LEVELS.items():
        urls.append(f"/paginas/{folder}/index.html")
        fd = os.path.join(ROOT, "paginas", folder)
        for fname in sorted(os.listdir(fd)):
            if fname.endswith(".html") and fname != "index.html":
                urls.append(f"/paginas/{folder}/{fname}")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{BASE_URL}{u}</loc>")
        lines.append("    <lastmod>2026-08-15</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append("    <priority>0.8</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    write(os.path.join(ROOT, "sitemap.xml"), "\n".join(lines) + "\n")
    print("sitemap.xml regenerado con", len(urls), "URLs")


def update_js_totals():
    mp = os.path.join(ROOT, "assets", "js", "main.js")
    mj = read(mp)
    src_70 = "const total = 70; // 12 + 15 + 13 + 16 + 14"
    dst_73 = "const total = 73; // 12 + 18 + 13 + 16 + 14"
    if src_70 in mj:
        mj = mj.replace(src_70, dst_73)
        write(mp, mj)
        print("main.js: total 70 -> 73")
    else:
        print("main.js: total 70 no encontrado (revisar)")


def update_index_label():
    ip = os.path.join(ROOT, "index.html")
    idx = read(ip)
    if "0 de 70 temas completados" in idx:
        idx = idx.replace("0 de 70 temas completados", "0 de 73 temas completados")
        write(ip, idx)
        print("index.html: label 70 -> 73")
    else:
        print("index.html: label 70 no encontrado (revisar)")


def main():
    lessons = [(t[0], t[1], t[2], t[3], t[4]) for t in TOPICS]

    visuals, quiz = extract_portada_parts()
    assert visuals and quiz, "No se encontraron visuales o quiz en la portada actual"

    total_new = sum(1 for t in lessons if t[0] in NEW_SECTIONS)
    print(f"Lecciones existentes: {len(lessons) - total_new} · Nuevas: {total_new} · Total: {len(lessons)}")

    for idx, (dt, *_rest) in enumerate(lessons):
        build_lesson_page(dt, idx, lessons)
        print("  lección:", TOPIC_META[dt][1])

    build_portada(lessons, visuals, quiz)
    print("  portada index.html")

    update_search_index(lessons)
    update_sitemap()
    update_js_totals()
    update_index_label()

    # asegura que el archivo JS siga siendo válido (firma)
    import subprocess
    for f in ["search-index.js", "main.js"]:
        r = subprocess.run(["node", "--check", os.path.join(ROOT, "assets", "js", f)], capture_output=True)
        if r.returncode != 0:
            raise SystemExit(f"{f}: sintaxis inválida:\n{r.stderr.decode('utf-8', 'replace')}")
    print("JS válidos (node --check OK)")


if __name__ == "__main__":
    main()