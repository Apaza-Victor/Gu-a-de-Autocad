# -*- coding: utf-8 -*-
"""
build_level4_content.py
Enriquece el Nivel 4 (Modelado 3D):
  - Añade contenido nuevo (tablas de comandos, pasos paso a paso, callouts,
    atajos y mini ejercicios) a las 16 lecciones existentes.
  - Crea 3 lecciones nuevas: ucs (Sistema de coordenadas 3D), recorridos
    (cámaras, recorridos y animaciones) e impresion3d (exportar a STL).
  - Regenera las 19 páginas de lección y la portada index.html del nivel.
  - Actualiza search-index.js, sitemap.xml, main.js (total 79) e index.html.

Ejecutar desde la raíz:  python scripts/build_level4_content.py
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

FOLDER = "nivel-4-modelado-3d"
DST = os.path.join(ROOT, "paginas", FOLDER)
NUM = 4
TOTAL = 19
EYEBROW = LEVELS[4][3]
FULL_TITLE = LEVELS[4][2]
SCHEMA_NAME = LEVELS[4][5]
SCHEMA_DESC = LEVELS[4][6]


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
    ("nivel4-navegacion",    "navegacion.html",    "Espacio de trabajo 3D y navegación",      "Navegación 3D",                 "Espacio de trabajo 3D y comandos para moverse, orbitar y cambiar la vista del modelo."),
    ("nivel4-ucs",           "ucs.html",           "Sistema de coordenadas (UCS) en 3D",       "Sistema de coordenadas (UCS)",  "El UCS dinámico 3D: reorientar el plano de trabajo para dibujar y acotar en cualquier cara."),
    ("nivel4-solidos",       "solidos.html",       "Sólidos básicos (primitivas)",             "Sólidos básicos",               "Caja, cilindro, esfera, cono, cuña, pirámide y toroide en un solo clic."),
    ("nivel4-booleanas",     "booleanas.html",     "Operaciones booleanas",                    "Operaciones booleanas",         "UNION, SUBTRACT e INTERSECT para combinar sólidos y crear piezas complejas."),
    ("nivel4-creacion",      "creacion.html",      "Extrusión, revolución, barrido y solevación", "De perfil a volumen",        "Convertir perfiles 2D en volumen: EXTRUDE, REVOLVE, SWEEP y LOFT."),
    ("nivel4-edicion",       "edicion.html",       "Edición de sólidos y superficies",         "Edición de sólidos",            "Redondear aristas, chaflanes, vaciado, secciones y conversiones de superficie."),
    ("nivel4-render",        "render.html",        "Renderizado básico",                       "Renderizado básico",            "Generar imágenes realistas con materiales, luces y cámaras."),
    ("nivel4-recorridos",    "recorridos.html",    "Cámaras, recorridos y animaciones",        "Recorridos y animaciones",      "Cámaras, recorridos a pie/vuelo y animaciones sobre trayectoria con ANIPATH."),
    ("nivel4-nav-3d-detalle", "nav-3d-detalle.html", "Navegación 3D avanzada",                 "Navegación avanzada",           "ViewCube, SteeringWheels, vistas predefinidas, cámara y perspectiva."),
    ("nivel4-mallas",        "mallas.html",        "Mallas (Mesh)",                            "Mallas (Mesh)",                 "Modelado de superficies orgánicas por caras: crear, refinar y suavizar mallas."),
    ("nivel4-superficies",   "superficies.html",   "Superficies y NURBS",                      "Superficies y NURBS",           "Caras sin volumen para formas libres: NETWORKSURF, EDGESURF y curvas NURBS."),
    ("nivel4-seccion",       "seccion.html",       "Secciones sólidas",                        "Secciones sólidas",             "Generar cortes 2D y planos de sección a partir del modelo 3D."),
    ("nivel4-interferencia", "interferencia.html", "Interferencia y análisis",                 "Interferencia y análisis",      "Detectar choques entre sólidos y medir propiedades de masa y geometría."),
    ("nivel4-cotado3d",      "cotado3d.html",      "Cotado 3D y anotaciones",                  "Cotado 3D",                     "Acotar en el espacio 3D según la orientación del UCS y añadir llamadas."),
    ("nivel4-materiales",    "materiales.html",    "Materiales, texturas y mapeado",           "Materiales y mapeado",          "Asignar materiales, crear acabados propios y controlar el mapeado UV."),
    ("nivel4-iluminacion",   "iluminacion.html",   "Iluminación y escenas",                    "Iluminación y escenas",         "Luces puntuales, focales, direccionales y sol real con escenas guardadas."),
    ("nivel4-vistas-2d",     "vistas-2d.html",     "Extracción de vistas 2D desde el modelo 3D", "Vistas 2D desde el 3D",       "FLATSHOT, SOLVIEW/SOLDRAW y VIEWBASE para documentar el modelo en 2D."),
    ("nivel4-massprop",      "massprop.html",      "Análisis de masa y volumen (MASSPROP)",    "MASSPROP",                      "Volumen, centro de masa, momentos de inercia y propiedades de regiones."),
    ("nivel4-impresion3d",   "impresion3d.html",   "Impresión 3D: exportar a STL",             "Impresión 3D (STL)",            "Preparar el modelo y exportarlo a STL para imprimirlo en 3D."),
]

TOPIC_META = {t[0]: t for t in TOPICS}
FILE_TO_TOPIC = {t[1]: t[0] for t in TOPICS}

# ----------------------------------------------------------------------------
# 2) Contenido de enriquecimiento para las lecciones existentes
# ----------------------------------------------------------------------------
# Cada fragmento se inserta antes del botón "Marcar tema como visto".
ENRICH = {}

ENRICH["nivel4-navegacion"] = [
"""<h3>Atajos rápidos para moverse en 3D</h3>
<table class="table-cad">
  <thead><tr><th>Acción</th><th>Atajo / control</th></tr></thead>
  <tbody>
    <tr><td>Órbita libre (orbit)</td><td><span class="key-inline">Shift + rueda</span> o mantener <span class="key-inline">Shift</span> y arrastrar con botón central.</td></tr>
    <tr><td>Encuadre (pan)</td><td>Rueda presionada o <span class="cmd-inline">PAN</span>.</td></tr>
    <tr><td>Zoom</td><td><span class="key-inline">Rueda</span> o <span class="cmd-inline">ZOOM</span>.</td></tr>
    <tr><td>Estilos visuales en secuencia</td><td>Pulsa <span class="key-inline">Ctrl+1</span> con la vista activa o usa <span class="cmd-inline">VSCURRENT</span>: alámbrico → oculto → sombreado → conceptual → realista.</td></tr>
    <tr><td>Vista anterior / posterior</td><td><span class="cmd-inline">VIEWBACK</span> / <span class="cmd-inline">VIEWFWD</span> o <span class="key-inline">Ctrl+Shift+P</span>.</td></tr>
  </tbody>
</table>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Activa el espacio 3D</h4>
    <p>En la barra inferior, clic sobre el icono de espacio de trabajo → <strong>Modelado 3D</strong>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Orbita a tu alrededor del modelo</h4>
    <p>Pulsa <span class="key-inline">Shift</span> y arrastra con la rueda presionada, o escribe <span class="cmd-inline">3DORBIT</span>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Cambia el estilo visual para revisar</h4>
    <p>Alterna con <span class="cmd-inline">VSCURRENT</span> a <strong>Iluminado con bordes</strong> para ver las caras sin el peso del render.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Intrusar el zoom del mouse con estilo alámbrico y no darte cuenta de que estás dentro del modelo. Activa <strong>Iluminado con bordes</strong> y usa el ViewCube para orientarte antes de editar.</span>
</div>""",
]

ENRICH["nivel4-solidos"] = [
"""<h3>Detalles que aceleran el trabajo con primitivas</h3>
<ul>
  <li><strong>BOX con centro:</strong> la opción <span class="cmd-inline">C</span> (Center) crea la caja desde su centro, no desde una esquina; ideal para centrar piezas en el origen.</li>
  <li><strong>Cilindro sobre caras:</strong> si el plano de trabajo (UCS) está sobre una cara, la base del cilindro nace en esa cara automáticamente.</li>
  <li><strong>Alturas con arrastre:</strong> escribe la primera medida y arrastra para ver la altura en tiempo real; pulsa <span class="key-inline">Tab</span> para fijarla.</li>
  <li><strong>Combinar patrones:</strong> las primitivas se crean en la capa actual; colócalas todas en <em>0</em> y conviértelas en bloque para reutilizar la pieza.</li>
</ul>
<h3>Mini ejercicio: un bloque sencillo</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>La base</h4>
    <p>Con <span class="cmd-inline">BOX</span> crea una caja de 200 x 100 x 40 en el origen.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>El cilindro sobre ella</h4>
    <p>Con <span class="cmd-inline">CYLINDER</span>, coloca la base en el centro de la cara superior (usa OSNAP <span class="cmd-inline">MID</span>) con radio 30 y altura 60.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Revisa en 3D</h4>
    <p>Orbita con <span class="key-inline">Shift+rueda</span> y activa <span class="cmd-inline">VSCURRENT</span> → <em>Iluminado con bordes</em> para ver las dos piezas encajadas.</p>
  </div>
</div>""",
]

ENRICH["nivel4-booleanas"] = [
"""<h3>Mini ejercicio: la arandela, paso a paso</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Cilindro exterior</h4>
    <p>Con <span class="cmd-inline">CYLINDER</span> crea un cilindro de radio 50 y altura 10.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Cilindro interior</h4>
    <p>Crea un segundo cilindro concéntrico de radio 25 y altura 10 (usa OSNAP <span class="cmd-inline">CEN</span> sobre la base del primero).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Resta</h4>
    <p>Con <span class="cmd-inline">SUBTRACT</span> selecciona el cilindro grande, <span class="key-inline">Enter</span>, y luego el pequeño: queda la arandela hueca.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>El orden importa: en <span class="cmd-inline">SUBTRACT</span>, primero se elige lo que <strong>queda</strong> y después lo que se <strong>quita</strong>. En <span class="cmd-inline">INTERSECT</span> y <span class="cmd-inline">UNION</span> el orden no afecta el resultado.</span>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Intentar <span class="cmd-inline">UNION</span> de dos sólidos que no se tocan: se unen igual, pero el resultado tiene dos volúmenes sin conexión. Comprueba el contacto con un render o estilo oculto antes de asumir que son una sola pieza.</span>
</div>""",
]

ENRICH["nivel4-creacion"] = [
"""<h3>Opciones que cambian el resultado</h3>
<table class="table-cad">
  <thead><tr><th>Herramienta</th><th>Opción práctica</th><th>Cuándo usarla</th></tr></thead>
  <tbody>
    <tr><td><span class="cmd-inline">EXTRUDE</span></td><td>Trayectoria (<span class="cmd-inline">T</span>) y ángulo de conicidad (<span class="cmd-inline">A</span>)</td><td>Extruir un perfil a lo largo de una polilínea o darle una ligera inclinación a un muro.</td></tr>
    <tr><td><span class="cmd-inline">REVOLVE</span></td><td>Ángulo de revolución (grados) y dirección del eje</td><td>Revolucionar solo 180° para crear un objeto asimétrico, o 360° para piezas simétricas.</td></tr>
    <tr><td><span class="cmd-inline">SWEEP</span></td><td>Alineación (<span class="cmd-inline">A</span>) para mantener la sección perpendicular a la curva</td><td>Tuberías, molduras y rieles: la sección no se deforma al recorrer la ruta.</td></tr>
    <tr><td><span class="cmd-inline">LOFT</span></td><td>Perfiles múltiples + guías (<span class="cmd-inline">G</span>)</td><td>Transiciones suaves entre plantas de distinta forma (chimeneas, carenados).</td></tr>
  </tbody>
</table>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>El perfil 2D debe estar <strong>cerrado</strong> para generar un sólido; si está abierto, la misma herramienta crea una superficie. Compruébalo con <span class="cmd-inline">BOUNDARY</span> si tienes dudas.</span>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Dibujar el perfil y la trayectoria en capas distintas sin comprobar que ambos estén en el mismo plano o que la trayectoria toque el perfil. Con <span class="cmd-inline">SWEEP</span> y <span class="cmd-inline">EXTRUDE</span> la referencia de inicio importa.</span>
</div>""",
]

ENRICH["nivel4-edicion"] = [
"""<h3>Edita caras, no solo aristas</h3>
<p>En <span class="cmd-inline">SOLIDEDIT</span> (cinta <em>Sólidos → Editar sólidos</em>) puedes modificar <strong>caras, aristas y cuerpo</strong>: mover una cara, estirar una cara, rotar caras, desfasar, taper (inclinar) y separar caras. Es el comodín para corregir el modelo sin releerlo.</p>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Redondea una arista</h4>
    <p>Con <span class="cmd-inline">FILLETEDGE</span> selecciona una arista de la caja, escribe el radio (por ejemplo 5) y <span class="key-inline">Enter</span>. Puedes añadir más aristas antes de aceptar.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Vacía una pieza</h4>
    <p>Con <span class="cmd-inline">SOLIDEDIT</span> → <strong>Vaciar</strong>, selecciona el sólido, elige una cara de la que se extrae el material y define el espesor de pared (por ejemplo 2).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Secciona para ver el interior</h4>
    <p>Con <span class="cmd-inline">SECTIONPLANE</span> coloca un plano de corte y desplázalo: el interior se muestra al instante sin destruir el sólido.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">¿Superficie o sólido?</span>
  <span>Una superficie cerrada no es un volumen: para darle cuerpo usa <span class="cmd-inline">THICKEN</span> (añade espesor) o <span class="cmd-inline">CONVTOSOLID</span> (la convierte en sólido si está cerrada).</span>
</div>""",
]

ENRICH["nivel4-render"] = [
"""<h3>Prepara el render final en orden</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Asigna materiales</h4>
    <p>Con <span class="cmd-inline">MAT</span> aplica los materiales a los objetos o caras (recuerda <span class="key-inline">Ctrl</span> para seleccionar caras individuales).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Enciende la luz</h4>
    <p>Activa la luz solar (<span class="cmd-inline">SUN</span>) o añade <span class="cmd-inline">POINTLIGHT</span> con la intensidad que prefieras.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Encuadra con cámara</h4>
    <p>Crea una cámara con <span class="cmd-inline">CAMERA</span> y usa <span class="cmd-inline">VSCURRENT</span> para ponerla como vista activa.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Render de prueba y final</h4>
    <p>Haz primero un render en <strong>borrador</strong>, revisa, y después configura <span class="cmd-inline">RPREF</span> (calidad media/alta y tamaño de salida) y ejecuta <span class="cmd-inline">RENDER</span>.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Renderizar en estilo "borrador" y asustarse con la imagen: la baja calidad no refleja el resultado final. Configura calidad alta y usa <strong>iluminación artificial compensatoria</strong> (icono de bombilla en la vista) para pruebas rápidas.</span>
</div>""",
]

ENRICH["nivel4-nav-3d-detalle"] = [
"""<h3>Saca partido al ViewCube y a las vistas guardadas</h3>
<ul>
  <li><strong>ViewCube:</strong> clic para vistas principales, arrastra para orientación libre, y clic derecho sobre el cubo para fijar la vista actual como "Home".</li>
  <li><strong>SteeringWheels:</strong> al activar <span class="cmd-inline">NAVSWHEEL</span>, mantén pulsado cada sector para Zoom, Orbit, Pan, Center y Look.</li>
  <li><strong>Guardar vistas:</strong> con la orientación elegida, escribe <span class="cmd-inline">VIEW</span> y crea una vista con nombre: reaparecerá en cualquier momento sin volver a orbitar.</li>
</ul>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Coloca una cámara</h4>
    <p>Escribe <span class="cmd-inline">CAMERA</span>, elige posición, objetivo y campo de visión, y confirma la vista.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Actívala para revisar</h4>
    <p>Clic derecho sobre la cámara → <strong>Ver cámara</strong>. Para volver al 3D, usa <span class="cmd-inline">VIEW</span> → <em>Vista isométrica</em>.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Paralelo vs. Perspectiva</span>
  <span>Usa <strong>Paralela</strong> para documentación técnica (sin deformación de la distancia) y <strong>Perspectiva</strong> para presentaciones. Alterna con <span class="cmd-inline">PERSPECTIVE</span> a ON/OFF.</span>
</div>""",
]

ENRICH["nivel4-mallas"] = [
"""<h3>Flujo típico con mallas</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Crea la forma base</h4>
    <p>Con <span class="cmd-inline">MESH</span> crea una esfera (o una caja) de malla.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Refina el detalle</h4>
    <p>Selecciona las caras y usa <span class="cmd-inline">MESHREFINE</span> para subdividirlas: más polígonos, más control.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Moldea con suavizado</h4>
    <p>Aplica <span class="cmd-inline">SMOOTHMESH</span> para alisar la forma, o mueve vértices/aristas individuales seleccionándolos en el subobjeto de malla.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Convierte si hace falta</h4>
    <p>Si el modelo debe comportarse como pieza sólida, conviértela con <span class="cmd-inline">CONVTOSOLID</span> (o a superficie con <span class="cmd-inline">CONVTOSURFACE</span>).</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Refinar una malla entera "por si acaso": cada <span class="cmd-inline">MESHREFINE</span> multiplica el número de caras y el archivo crece sin que se note. Refina solo las zonas donde vas a trabajar.</span>
</div>""",
]

ENRICH["nivel4-superficies"] = [
"""<h3>Mini ejercicio: tapiz NURBS entre dos curvas</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Crea dos splines guía</h4>
    <p>Dibuja dos <span class="cmd-inline">SPLINE</span> separadas en el espacio (usa puntos 3D o planos distintos de UCS).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Genera el tapiz</h4>
    <p>Con <span class="cmd-inline">NETWORKSURF</span> selecciona ambas curvas: se interpola una superficie entre ellas.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Da espesor si es producto</h4>
    <p>Con <span class="cmd-inline">THICKEN</span> conviertes la superficie en un sólido de espesor definido (por ejemplo 1.5).</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">NURBS vs. spline clásica</span>
  <span>AutoCAD usa <strong>NURBS</strong> para superficies matemáticamente exactas: se editan arrastrando los <em>puntos de control</em> (opción <span class="cmd-inline">N</span> de <span class="cmd-inline">SPLINE</span>). La curva clásica se puede convertir a NURBS al crearla.</span>
</div>""",
]

ENRICH["nivel4-seccion"] = [
"""<h3>Controles del plano de sección</h3>
<p>El plano de sección creado con <span class="cmd-inline">SECTIONPLANE</span> es un objeto interactivo con pinzamientos: puedes <strong>arrastrarlo</strong> para moverlo, <strong>girar</strong> su orientación y elegir el <strong>modo de visualización</strong> con clic derecho (<em>Recortar a esta sección</em>, <em>Recortar a la caja</em>, <em>Sección completa</em>).</p>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Crea el plano</h4>
    <p>Con <span class="cmd-inline">SECTIONPLANE</span> traza un plano que corte la pieza donde quieras el detalle.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Ajusta</h4>
    <p>Usa los pinzamientos para desplazar y girar; activa el modo <em>Recortar</em> para ver la pieza seccionada en vivo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Genera el corte 2D</h4>
    <p>Clic derecho → <strong>Generar sección</strong> y elige crear un bloque de sección en el dibujo o en un archivo nuevo.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Atención</span>
  <span>El corte generado es una <strong>instantánea</strong>: si modificas el modelo después, regenera la sección. Para cortes asociativos que se actualicen solos, usa <span class="cmd-inline">VIEWBASE</span> (AutoCAD moderno).</span>
</div>""",
]

ENRICH["nivel4-interferencia"] = [
"""<h3>Detectar choques antes de construir</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Ejecuta la comprobación</h4>
    <p>Escribe <span class="cmd-inline">INTERFERE</span> y selecciona el primer conjunto de sólidos, <span class="key-inline">Enter</span>, y luego el segundo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Revisa los choques</h4>
    <p>AutoCAD resalta las zonas de superposición y las contabiliza; usa <em>Siguiente/Anterior</em> para recorrerlas.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Crea el sólido de interferencia</h4>
    <p>Si respondes <span class="cmd-inline">S</span> (Sí) a "Crear sólidos de interferencia", obtienes el volumen del choque como objeto: úsalo para medirlo o mostrarlo en la lámina.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Caso de uso</span>
  <span>En coordinación MEP/estructura: cruzas los conductos (primer conjunto) con las vigas (segundo conjunto) y en segundos sabes qué zonas deben reubicarse antes de la obra.</span>
</div>""",
]

ENRICH["nivel4-cotado3d"] = [
"""<h3>Acotar bien en 3D: el UCS primero</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Orienta el plano de trabajo</h4>
    <p>Sitúa el UCS sobre la cara que vas a acotar: en la cinta <em>Inicio → Coordenadas</em>, <strong>UCS → Cara</strong>, y haz clic en la cara (o usa <span class="cmd-inline">UCS</span> → <span class="cmd-inline">OB</span> con el plano 2D).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Acota sobre él</h4>
    <p>Con <span class="cmd-inline">DIMLINEAR</span> o <span class="cmd-inline">DIMALIGNED</span> coloca la cota en ese plano; se imprimirá correctamente en el 2D.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Anota con llamadas</h4>
    <p>Para marcar un vértice o una cara en 3D, usa <span class="cmd-inline">LEADER</span> (multileader) que apunta a coordenadas 3D reales.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Acotar en 3D sin fijar el plano: la cota queda con la orientación del UCS anterior y se ve "flotando" o mal al girar la vista. Si el plano de cota está desviado, la cifra puede ser la distancia proyectada y no la real.</span>
</div>""",
]

ENRICH["nivel4-materiales"] = [
"""<h3>Asignar material a una cara concreta</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Abre el editor</h4>
    <p>Con <span class="cmd-inline">MAT</span> abre el Editor de materiales y elige uno de la biblioteca (o crea uno personalizado).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Selecciona por cara</h4>
    <p>Con el material activo, mantén <span class="key-inline">Ctrl</span> al seleccionar el sólido: arrastra el ratón sobre la cara concreta antes de soltar.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Ajusta el mapeado</h4>
    <p>Con <span class="cmd-inline">MATERIALMAP</span> elige la proyección (planar, caja, cilíndrico, esférico) y usa los pinzamientos para reencuadrar la textura sin deformarla.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Consejo</span>
  <span>Si la textura "se mueve" entre renders, revisa que el mapeado esté fijado con <em>Bloquear proporción</em> (aspect ratio 1:1) y que el objeto esté a escala real. Guarda el material con <strong>Exportar como hoja de estilo externa</strong> para reutilizarlo en otros proyectos.</span>
</div>""",
]

ENRICH["nivel4-iluminacion"] = [
"""<h3>Una escena de luz en cinco pasos</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Define la hora y el lugar</h4>
    <p>Con <span class="cmd-inline">GEOGRAPHICLOCATION</span> ubica el proyecto y con <span class="cmd-inline">SUN</span> activa la luz solar.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Mueve el sol</h4>
    <p>En las propiedades del sol, ajusta <em>Hora del día</em>: entre las 9:00 y las 16:00 tienes sombras suaves y direccionables.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Añade relleno interior</h4>
    <p>Para interiores, coloca una <span class="cmd-inline">POINTLIGHT</span> cerca de la cámara con intensidad baja (0.5–1) que rellene sin quemar.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Guarda la escena</h4>
    <p>Con <span class="cmd-inline">VIEW</span> → pestaña <em>Escenas</em>, crea "Exterior día" con la cámara y estos parámetros de luz.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">5</span>
  <div class="lesson-body">
    <h4>Prueba barato</h4>
    <p>Render en <strong>borrador</strong> para validar sombras y posición de la luz antes del render final.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Menos luz es más realista: empieza con intensidades bajas y sube solo lo necesario. El exceso de luz "quema" el render y aplana los materiales.</span>
</div>""",
]

ENRICH["nivel4-vistas-2d"] = [
"""<h3>Vistas base y proyectadas con VIEWBASE</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Ve al layout</h4>
    <p>Pasa a una presentación y activa la pestaña <em>Dibujo base</em> → <strong>Desde el modelo 3D</strong> (o escribe <span class="cmd-inline">VIEWBASE</span>).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Coloca la vista base</h4>
    <p>Selecciona el sólido y sitúa la vista en el layout; elige escala y orientación (superior, frontal...).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Proyecta las vistas</h4>
    <p>Con <span class="cmd-inline">VIEWPROJ</span> arrastra las vistas proyectadas (planta, alzado, perfiles) desde la base.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Trabaja asociativo</h4>
    <p>Si cambias el modelo, las vistas se actualizan: clic derecho → <strong>Actualizar</strong>. Esto es lo que NO conseguías con FLATSHOT.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">¿Cuándo usar cada método, resumen?</span>
  <ul class="mb-0">
    <li><strong>FLATSHOT:</strong> vista rápida 2D en espacio modelo, sin asociatividad.</li>
    <li><strong>SOLVIEW/SOLDRAW:</strong> AutoCAD clásico, ideal para secciones y líneas ocultas en layouts.</li>
    <li><strong>VIEWBASE/VIEWPROJ:</strong> AutoCAD moderno, asociativas y la vía recomendada para planos de taller.</li>
  </ul>
</div>""",
]

ENRICH["nivel4-massprop"] = [
"""<h3>Mini ejercicio: volumen y centro de masa de una pieza</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Unifica la pieza</h4>
    <p>Si la pieza tiene varias partes, únelas con <span class="cmd-inline">UNION</span> para que cuente como un único sólido.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Consulta las propiedades</h4>
    <p>Con <span class="cmd-inline">MASSPROP</span> selecciona el sólido: volumen, área, centro de masa y momentos de inercia.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Expórtalo</h4>
    <p>Responde <span class="cmd-inline">S</span> (Sí) a "Escribir análisis en un archivo" y guarda el .txt, o copia los valores del historial con <span class="key-inline">F2</span>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Verifica las unidades</h4>
    <p>Comprueba con <span class="cmd-inline">UNITS</span> que el dibujo está en la unidad que crees (mm, cm, m): 0.0024 m³ y 2400 cm³ son lo mismo, pero el número cambia.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Creer que MASSPROP "recuerda" los valores. Ejecútalo de nuevo tras cada modificación del sólido; los datos anteriores no se actualizan solos.</span>
</div>""",
]

# ----------------------------------------------------------------------------
# 3) Lecciones nuevas (contenido completo)
# ----------------------------------------------------------------------------
NEW_SECTIONS = {}

NEW_SECTIONS["nivel4-ucs"] = """
<h2><span class="sec-num">N</span>Sistema de coordenadas (UCS) en 3D</h2>
<p>El <strong>UCS</strong> (Sistema de Coordenadas de Usuario) es el plano de trabajo que usan AutoCAD para dibujar, extruir y acotar. En 3D puedes reorientarlo sobre cualquier cara o plano: así dibujas una ventana en la cara inclinada de un techo, o acotas una pieza sin deformarla. Toda la geometría que creas nace en el plano del UCS activo.</p>

<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Cada comando de dibujo (línea, rectángulo, círculo, extrusión...) dibuja sobre el plano del <strong>UCS actual</strong>. Orienta el UCS a la cara que necesitas y el trabajo "2D" se vuelve posible en cualquier rincón del 3D.</span>
</div>

<h3>Formas de orientar el UCS</h3>
<table class="table-cad">
  <thead><tr><th>Método</th><th>Cómo se usa</th><th>Cuándo</th></tr></thead>
  <tbody>
    <tr><td>UCS → Cara (<span class="cmd-inline">UCS</span> → <span class="cmd-inline">F</span>)</td><td>Haz clic sobre una cara del sólido; el plano se alinea con ella.</td><td>Trabajar sobre una pared, un techo o una cara inclinada.</td></tr>
    <tr><td>UCS → Objeto (<span class="cmd-inline">UCS</span> → <span class="cmd-inline">OB</span>)</td><td>Selecciona una línea, polilínea o círculo: el plano se alinea con ella.</td><td>Reboces, tubos, pasamanos que siguen una curva.</td></tr>
    <tr><td>UCS → 3 puntos</td><td>Defines origen, punto X y punto Y.</td><td>Planos arbitrarios que no son ni cara ni objeto.</td></tr>
    <tr><td>UCS → Mundial (<span class="cmd-inline">W</span>)</td><td>Devuelve el plano base X-Y del origen del dibujo.</td><td>Siempre que te pierdas: resetea la orientación.</td></tr>
  </tbody>
</table>

<h3>El icono del UCS te lo dice todo</h3>
<p>Mantén visible el <strong>icono del UCS</strong> (esquina inferior izquierda): su orientación y las flechas de color rojo (X), verde (Y) y azul (Z) te indican dónde está el plano de trabajo. Si las X e Y forman el plano "de frente" y la Z sube perpendicular, estás trabajando en el plano correcto.</p>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Sitúa el plano sobre una cara</h4>
    <p>Con <span class="cmd-inline">UCS</span> → opción <span class="cmd-inline">F</span> (Cara), haz clic en la cara del sólido donde quieras dibujar.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Dibuja en 2D sobre el 3D</h4>
    <p>Con <span class="cmd-inline">RECTANG</span> o <span class="cmd-inline">LINE</span> crea el perfil: nace plano sobre la cara, listo para extruir.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Devuelve el sistema mundial</h4>
    <p>Escribe <span class="cmd-inline">UCS</span> → <span class="cmd-inline">W</span> (Mundial) y <span class="key-inline">Enter</span>: el plano se realinea al origen.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Dibujar "de puro air" sin mirar el icono del UCS y acabar creando líneas en un plano aleatorio. Fija la vista en <em>Perpendicular</em> a la cara (ViewCube) y comprueba el icono antes de empezar.</span>
</div>
<h3>Mini ejercicio: una ventana sobre un techo inclinado</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Crear el plano</h4>
    <p>Orienta el UCS a la cara del techo (UCS → Cara, clic sobre ella).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Dibuja el perfil</h4>
    <p>Con <span class="cmd-inline">RECTANG</span> traza la ventana de 120 x 80 sobre la cara.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Extrae el volumen</h4>
    <p>Con <span class="cmd-inline">EXTRUDE</span> dale 5 de espesor hacia fuera del tejado: la ventana queda a plomo con la pendiente.</p>
  </div>
</div>
"""

NEW_SECTIONS["nivel4-recorridos"] = """
<h2><span class="sec-num">N</span>Cámaras, recorridos y animaciones</h2>
<p>Además de renderizar una imagen, AutoCAD permite <strong>recorridos a pie</strong> (<span class="cmd-inline">3DWALK</span>), <strong>vuelos</strong> (<span class="cmd-inline">3DFLY</span>) y <strong>animaciones de cámara</strong> sobre una trayectoria (<span class="cmd-inline">ANIPATH</span>). Son la forma más directa de presentar un proyecto 3D en movimiento sin salir del programa.</p>

<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Un <strong>recorrido</strong> es navegar en tiempo real por el modelo (muy útil para revisar choques o proporciones). Una <strong>animación de trayectoria</strong> es un video generado donde la cámara se mueve sola siguiendo una polilínea y mirando a un punto.</span>
</div>

<h3>Cómo moverse a pie y en vuelo</h3>
<table class="table-cad">
  <thead><tr><th>Modo</th><th>Comando</th><th>Controles</th></tr></thead>
  <tbody>
    <tr><td>Recorrido a pie</td><td><span class="cmd-inline">3DWALK</span></td><td><span class="key-inline">W/S/A/D</span> para moverte, <span class="key-inline">Flechas</span> para girar, <span class="key-inline">Ctrl</span> para bajar y <span class="key-inline">Shift</span> para correr.</td></tr>
    <tr><td>Vuelo</td><td><span class="cmd-inline">3DFLY</span></td><td>Igual que 3DWALK, pero puedes subir y bajar libremente en vertical.</td></tr>
    <tr><td>Velocidad</td><td><span class="cmd-inline">3DSPEED</span></td><td>Ajusta la velocidad de movimiento en la navegación.</td></tr>
  </tbody>
</table>
<h3>Animación sobre trayectoria</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Dibuja la trayectoria</h4>
    <p>Crea una <span class="cmd-inline">SPLINE</span> o polilínea que recorra el camino que hará la cámara (por ejemplo, por la pasarela de un edificio).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Elige el punto de mira</h4>
    <p>Con <span class="cmd-inline">ANIPATH</span>, en pestaña <em>Cámara</em> selecciona la trayectoria de posición y en <em>Objetivo</em> elige un punto fijo o un objeto (p. ej. el centro de la sala).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Configura el video</h4>
    <p>Define número de fotogramas, velocidad (FPS) y duración. La animación se genera como video (.avi/.wmv) o como serie de imágenes.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Prueba antes de exportar</h4>
    <p>Juega primero con la variable <span class="cmd-inline">TAVEL</span> y render de baja calidad para validar el recorrido; el render final tarda varios minutos.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Olvidar que la cámara "mira" siempre al objetivo: si el objetivo está fijo y la trayectoria es larga, la cámara gira bruscamente. Añade varios objetivos o usa recorrido libre (<span class="cmd-inline">3DFLY</span>) para la revisión.</span>
</div>
<h3>Mini ejercicio: un vuelo de 6 segundos</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Trayectoria en espiral</h4>
    <p>Con <span class="cmd-inline">SPLINE</span> dibuja una espiral ascendente alrededor del modelo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Anímalo</h4>
    <p>Con <span class="cmd-inline">ANIPATH</span> asigna la espiral como cámara y el centro del modelo como objetivo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Genera y revisa</h4>
    <p>Exporta el video y repite 3DFLY para comprobar las alturas por las que pasa la cámara.</p>
  </div>
</div>
"""

NEW_SECTIONS["nivel4-impresion3d"] = """
<h2><span class="sec-num">N</span>Impresión 3D: exportar a STL</h2>
<p>Para imprimir un modelo con una impresora 3D (FDM, resina o SLS) el archivo debe convertirse a un formato de malla como <strong>STL</strong>. En AutoCAD el proceso es sencillo: preparas un sólido cerrado, ajustas la resolución de la malla y lo exportas con <span class="cmd-inline">STLOUT</span> o <span class="cmd-inline">3DPRINT</span>.</p>

<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>STL describe la superficie del modelo como una nube de triángulos. Cuantos más triángulos, más preciso el archivo, pero también más pesado. El equilibrio depende de la geometría y de la resolución de tu impresora.</span>
</div>

<h3>Requisitos para una impresión limpia</h3>
<ul>
  <li><strong>Sólidos cerrados:</strong> el modelo debe ser un volumen sin huecos. Revisa con <span class="cmd-inline">MASSPROP</span> que exista y con <span class="cmd-inline">UNION</span> une las partes tocantes.</li>
  <li><strong>Normales bien orientadas:</strong> la superficie debe verse desde el exterior; corrige orientaciones con los comandos de malla si está invertida.</li>
  <li><strong>Unidades coherentes:</strong> decide si el modelo está en milímetros o centímetros Y configúralo en el diálogo de exportación; es la causa más común de piezas 10x o 100x más pequeñas.</li>
  <li><strong>Resolución suficiente:</strong> para caras curvas usa resolución alta; para cajas, media basta.</li>
</ul>

<h3>Exportar el STL paso a paso</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Prepara el modelo</h4>
    <p>Une las partes con <span class="cmd-inline">UNION</span> y verifica el volumen con <span class="cmd-inline">MASSPROP</span>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Exporta</h4>
    <p>Escribe <span class="cmd-inline">STLOUT</span>, selecciona el sólido, elige <em>Unidades</em> (mm o cm) y guarda el archivo con extensión .stl.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Ajusta la resolución</h4>
    <p>En el diálogo de STL, usa la opción de generar el archivo <strong>de faceta/resolución</strong> que prefieras (baja/media/alta). A medida que sube, el archivo pesa más.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Valída el STL</h4>
    <p>Ábrelo en tu laminador (slicer) y comprueba: escala (medida), orientación de la impresión, espesores de pared y soportes.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Exportar con unidades equivocadas: un modelo en milímetros exportado "en centímetros" genera una pieza 10 veces menor. Anota la unidad al guardar y verifícala en el laminador antes de imprimir.</span>
</div>
<h3>Mini ejercicio: imprime una arandela</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Modela la arandela</h4>
    <p>Con <span class="cmd-inline">CYLINDER</span> (radio 50, altura 10) menos <span class="cmd-inline">CYLINDER</span> interior (radio 25) vía <span class="cmd-inline">SUBTRACT</span>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Exporta</h4>
    <p>Con <span class="cmd-inline">STLOUT</span> guárdala en milímetros con resolución alta.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Comprueba en STL</h4>
    <p>Carga el archivo en el laminador: verifica 50 mm de diámetro exterior y el agujero de 25 mm.</p>
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
    next_btn = '<a href="../nivel-5-avanzado/index.html" class="btn-cad-outline w-100 text-center d-block">Siguiente nivel <i class="bi bi-arrow-right"></i></a>'
    nav_next = """<a href="../nivel-5-avanzado/index.html" class="nav-next">
            <span class="nav-label">Siguiente</span>
            <span class="nav-title">Siguiente nivel <i class="bi bi-arrow-right"></i></span>
          </a>"""
    page = f"""<!DOCTYPE html>
<html lang="es" data-theme="dark">
{build_head(f"Nivel {NUM} · {FULL_TITLE} — AutoCAD Guía", f"/paginas/{FOLDER}/index.html", LEVELS[4][4], include_3d=False, schema_name=SCHEMA_NAME, schema_desc=SCHEMA_DESC)}

<body>

<a href="#main-content" class="skip-link">Saltar al contenido principal</a>

{build_navbar(NUM)}

<header class="page-header" id="main-content">
  <div class="container container-xl">
    <p class="crumb"><a href="../../index.html">Inicio</a> / <a href="../../index.html#niveles">Niveles</a> / {FULL_TITLE}</p>
    <span class="eyebrow" data-i18n="lvl{NUM}.eyebrow">{EYEBROW}</span>
    <h1 data-i18n="lvl{NUM}.title">{FULL_TITLE}</h1>
    <p class="subtitle" data-i18n="lvl{NUM}.subtitle">{LEVELS[4][4]}</p>
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
    "nivel4-ucs":          "nivel-4-modelado-3d/navegacion.html",
    "nivel4-recorridos":   "nivel-4-modelado-3d/render.html",
    "nivel4-impresion3d":  "nivel-4-modelado-3d/massprop.html",
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
                 '    "path": "Nivel 4 · Modelado 3D"\n'
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
    src_76 = "const total = 76; // 12 + 18 + 16 + 16 + 14"
    dst_79 = "const total = 79; // 12 + 18 + 16 + 19 + 14"
    if src_76 in mj:
        mj = mj.replace(src_76, dst_79)
        write(mp, mj)
        print("main.js: total 76 -> 79")
    else:
        print("main.js: total 73 no encontrado (revisar)")


def update_index_label():
    ip = os.path.join(ROOT, "index.html")
    idx = read(ip)
    if "0 de 76 temas completados" in idx:
        idx = idx.replace("0 de 76 temas completados", "0 de 79 temas completados")
        write(ip, idx)
        print("index.html: label 76 -> 79")
    else:
        print("index.html: label 73 no encontrado (revisar)")


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