# -*- coding: utf-8 -*-
"""
build_level3_content.py
Enriquece el Nivel 3 (Organización · Dibujo 2D avanzado / gestión de planos):
  - Añade contenido nuevo (tablas de comandos, pasos paso a paso, callouts,
    atajos y mini ejercicios) a las 13 lecciones existentes.
  - Crea 3 lecciones nuevas: designcenter (DesignCenter/paletas), publish
    (publicación por lotes) y etransmit (transmisión y empaquetado).
  - Regenera las 16 páginas de lección y la portada index.html del nivel.
  - Actualiza search-index.js, sitemap.xml, main.js (total 76) e index.html.

Ejecutar desde la raíz:  python scripts/build_level3_content.py
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

FOLDER = "nivel-3-organizacion"
DST = os.path.join(ROOT, "paginas", FOLDER)
NUM = 3
TOTAL = 16
EYEBROW = LEVELS[3][3]
FULL_TITLE = LEVELS[3][2]
SCHEMA_NAME = LEVELS[3][5]
SCHEMA_DESC = LEVELS[3][6]


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
    ("nivel3-espacios",          "espacios.html",          "Espacio modelo vs. espacio papel (Layouts)", "Espacio modelo vs. papel",         "Los dos entornos de AutoCAD: el modelo a escala real y las presentaciones que preparan la hoja impresa."),
    ("nivel3-viewports",         "viewports.html",         "Ventanas gráficas (Viewports) y escalas",    "Ventanas gráficas y escalas",       "Ventanas gráficas dentro de un layout, su escala y cómo congelar capas por ventana."),
    ("nivel3-plantillas",        "plantillas.html",        "Plantillas (.DWT) y estándares de dibujo",  "Plantillas (.DWT)",                 "Guardar capas, estilos y layouts en una plantilla para no reconfigurar cada proyecto."),
    ("nivel3-designcenter",      "designcenter.html",      "DesignCenter y paletas de herramientas",     "DesignCenter y paletas",            "Reutilizar bloques, capas y estilos de otros dibujos con DesignCenter y las paletas de herramientas."),
    ("nivel3-impresion",         "impresion.html",         "Impresión y exportación",                    "Impresión y exportación",           "PLOT, PDF, DWF y DXF: cómo preparar y generar el plano final desde el layout."),
    ("nivel3-publish",           "publish.html",           "Publicación por lotes (PUBLISH)",            "Publicación por lotes (PUBLISH)",   "Imprimir o exportar varios layouts y archivos a la vez con una sola orden."),
    ("nivel3-xref",              "xref.html",              "Gestión de archivos externos (Xref)",         "Referencias externas (Xref)",       "Vincular otros dibujos sin fusionarlos: adjuntar, administrar y recortar Xrefs."),
    ("nivel3-atajos",            "atajos.html",            "Atajos de teclado y comandos rápidos",        "Atajos de teclado",                 "Los atajos y alias que más aceleran el trabajo diario en AutoCAD."),
    ("nivel3-plotstyles",        "plotstyles.html",        "Estilos de trazado (Plot Styles)",            "Estilos de trazado",                "Traducir colores a grosores y tonos de impresión con archivos .CTB y .STB."),
    ("nivel3-campos",            "campos.html",            "Campos (Fields)",                             "Campos (Fields)",                   "Textos que se actualizan solos: fecha, autor, área, número de lámina."),
    ("nivel3-xref-avanzado",     "xref-avanzado.html",     "Gestión avanzada de referencias externas",    "Xref avanzado",                     "Adjuntar vs. enlazar, Overlay vs. Attach, recortes y cadenas de referencias."),
    ("nivel3-cajetines",         "cajetines.html",         "Cajetines y bloques de título",               "Cajetines y bloques de título",     "El recuadro de identificación del plano como bloque con atributos y campos."),
    ("nivel3-escala-anotativa",  "escala-anotativa.html",  "Escala anotativa (Annotative)",               "Escala anotativa",                  "Una sola cota o texto que se muestra correcto en todas las escalas de la lámina."),
    ("nivel3-estandares-capas",  "estandares-capas.html",  "Estándares de capas (ISO/AIA)",               "Estándares de capas",               "Convenciones de nombres y organización de capas para trabajar en equipo."),
    ("nivel3-sheet-sets",        "sheet-sets.html",        "Conjuntos de planos (Sheet Sets)",            "Conjuntos de planos",               "Organizar, numerar y publicar todas las láminas de un proyecto desde un panel."),
    ("nivel3-etransmit",         "etransmit.html",         "Transmitir y empaquetar (ETRANSMIT)",         "Transmitir y empaquetar",           "Empaquetar el dibujo con sus Xrefs, fuentes y estilos en un solo archivo para entregar."),
]

TOPIC_META = {t[0]: t for t in TOPICS}
FILE_TO_TOPIC = {t[1]: t[0] for t in TOPICS}

# ----------------------------------------------------------------------------
# 2) Contenido de enriquecimiento para las lecciones existentes
# ----------------------------------------------------------------------------
# Cada fragmento se inserta antes del botón "Marcar tema como visto".
ENRICH = {}

ENRICH["nivel3-espacios"] = [
"""<h3>Comandos para moverse entre modelo y presentación</h3>
<table class="table-cad">
  <thead><tr><th>Comando</th><th>Qué hace</th></tr></thead>
  <tbody>
    <tr><td class="cmd-inline">MSPACE</td><td>Entra a trabajar dentro de una ventana gráfica del layout (estás editando el modelo a través de ella).</td></tr>
    <tr><td class="cmd-inline">PSPACE</td><td>Sale de la ventana gráfica y vuelve a trabajar con la hoja (papel).</td></tr>
    <tr><td class="cmd-inline">PAGESETUP</td><td>Configura la hoja de cada layout: tamaño, margen, escala de impresión y estilo de trazado.</td></tr>
    <tr><td class="cmd-inline">LAYOUT</td><td>Crea, nombra, copia o elimina pestañas de presentación.</td></tr>
    <tr><td class="cmd-inline">-PLOT</td><td>Imprime SOLO el layout activo con una configuración definida, sin abrir el diálogo completo.</td></tr>
  </tbody>
</table>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>El modelo se dibuja <strong>una sola vez</strong> y cada layout es una "cámara" distinta sobre el mismo proyecto. Por eso un cambio en el modelo se refleja en todos los layouts automáticamente.</span>
</div>
<h3>Mini ejercicio: prepara el layout de tu plano</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Nombra la presentación</h4>
    <p>Clic derecho sobre la pestaña <strong>Presentación 1</strong> → <em>Cambiar nombre de página</em> y llámala "PLANTA A-1".</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Configura la hoja</h4>
    <p>Con <span class="cmd-inline">PAGESETUP</span> elige papel A3 horizontal y, en la sección <em>Escala de impresión</em>, activa "Ajustar a la ventana" de momento (luego fijas la escala real del viewport).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Comprueba el flujo</h4>
    <p>Doble clic dentro del marco de la ventana gráfica (entras con <span class="cmd-inline">MSPACE</span>), haz zoom para encuadrar y vuelve al papel con doble clic fuera (sale con <span class="cmd-inline">PSPACE</span>).</p>
  </div>
</div>""",
]

ENRICH["nivel3-viewports"] = [
"""<h3>Tipos de ventanas gráficas</h3>
<table class="table-cad">
  <thead><tr><th>Tipo</th><th>Cómo se crea</th><th>Cuándo usarlo</th></tr></thead>
  <tbody>
    <tr><td>Rectangular</td><td><span class="cmd-inline">MVIEW</span> → arrastrar un rectángulo</td><td>La ventana estándar de una planta o detalle.</td></tr>
    <tr><td>Poligonal</td><td><span class="cmd-inline">MVIEW</span> → opción <span class="cmd-inline">P</span> (Polygonal)</td><td>Recortar la ventana con la forma del detalle (por ejemplo una esquina del plano).</td></tr>
    <tr><td>Objeto</td><td><span class="cmd-inline">MVIEW</span> → opción <span class="cmd-inline">O</span> (Object)</td><td>Usar una polilínea o círculo existente como borde de la ventana.</td></tr>
    <tr><td>Varias a la vez</td><td><span class="cmd-inline">VPORTS</span> en el layout</td><td>Crear una cuadrícula de ventanas (2, 3 o 4) en un paso.</td></tr>
  </tbody>
</table>
<h3>La escala correcta, en 4 pasos</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Activa la ventana</h4>
    <p>Doble clic dentro de la ventana gráfica (entras con <span class="cmd-inline">MSPACE</span>).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Asigna la escala</h4>
    <p>En la barra de estado inferior elige la escala deseada, por ejemplo <strong>1:50</strong>, y encuadra con <span class="cmd-inline">PAN</span>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Bloquea la escala</h4>
    <p>Selecciona el marco de la ventana, clic derecho → <strong>Bloquear visualización</strong>. Así ya no se desencuadra ni cambia la escala por accidente.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Congela capas por ventana</h4>
    <p>Con la ventana activa, abre <span class="cmd-inline">LAYER</span> y usa el icono de copo de nieve de <strong>ventana actual</strong>: congela una capa solo en ese viewport y el detalle se limpia sin afectar a los demás.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Hacer zoom con la rueda DENTRO de la ventana y creer que cambiaste la escala. Sin <span class="cmd-inline">PSPACE</span> + bloqueo, el zoom aleatorio desencuadra la lámina. Usa siempre la lista de escalas de la barra de estado y bloquea después.</span>
</div>""",
]

ENRICH["nivel3-plantillas"] = [
"""<h3>Cómo crear tu propia plantilla</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Prepara un dibujo base</h4>
    <p>Parte de un dibujo donde ya estén las capas, los estilos de texto y de cota, y el layout con el cajetín definidos.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Guarda como plantilla</h4>
    <p>Escribe <span class="cmd-inline">SAVEAS</span> y en <em>Tipo de archivo</em> elige <strong>Plantilla de dibujo (*.dwt)</strong>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Define un nombre y unidades</h4>
    <p>Ponle un nombre claro (por ejemplo "A3-Plantilla-Metrico.dwt") y confirma la unidad de medida (milímetros) en el diálogo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Apúntala como predeterminada</h4>
    <p>En <span class="cmd-inline">Opciones</span> (<span class="key-inline">OP</span>) → pestaña <em>Archivos</em> → <strong>Ubicación de plantillas</strong>, añade la carpeta donde guardas tus .DWT. Todo dibujo nuevo nacerá con tu base.</p>
  </div>
</div>
<table class="table-cad">
  <thead><tr><th>Qué guardar</th><th>Qué olvidar</th></tr></thead>
  <tbody>
    <tr><td>Capas con colores, grosor y tipo de línea (ByLayer).</td><td>Objetos de un proyecto concreto (muros, textos de esa obra).</td></tr>
    <tr><td>Estilos de texto, cota, tabla y multilínea.</td><td>Referencias externas de un proyecto puntual.</td></tr>
    <tr><td>Layout con cajetín, atributos y campos.</td><td>Capas y estilos que no usas (aplica <span class="cmd-inline">PURGE</span> antes de guardar).</td></tr>
    <tr><td>Unidades, límites y configuración de trazado.</td><td>Historial de comandos o estados de capa temporales.</td></tr>
  </tbody>
</table>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Guardar una plantilla con geometría del proyecto. Una .DWT debe estar limpia: si quien la abre encuentra "residuos" de otra obra, dejará de usarla y el estándar muere.</span>
</div>""",
]

ENRICH["nivel3-impresion"] = [
"""<h3>El orden correcto al imprimir</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Estás en el layout correcto</h4>
    <p>Abre la pestaña de la presentación que vas a imprimir y verifica el área: recuadro grande (papel) y rectángulo del viewport (ventana gráfica).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Configura la página</h4>
    <p>Dentro de <span class="cmd-inline">PLOT</span> (o <span class="cmd-inline">Ctrl+P</span>): elige <strong>Impresora/plotter</strong> (física o PDF, p. ej. <span class="cmd-inline">DWG To PDF.pc3</span>), <strong>tamaño de papel</strong> y <strong>área de impresión</strong> = Layout.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Revisa escala y estilo</h4>
    <p>Marca <strong>1:1</strong> si imprimes la hoja del tamaño exacto, asigna el estilo de trazado (<span class="cmd-inline">monochrome.ctb</span> para negro con grosores) y previsualiza con <em>Vista preliminar</em>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Guarda la configuración</h4>
    <p>Aplica la configuración a una <strong>configuración de página</strong> (nombre arriba del diálogo). Así la próxima impresión usa los mismos valores sin reconfigurar.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>El orden de capas "de visualización" no importa en el dibujo: lo que define el resultado final es <strong>PLOT → qué configuración de página + qué estilo de trazado</strong> está activo en cada layout.</span>
</div>""",
]

ENRICH["nivel3-xref"] = [
"""<h3>Adjuntar una Xref paso a paso</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Inicia el vínculo</h4>
    <p>Escribe <span class="cmd-inline">XATTACH</span> y selecciona el .DWG de base (por ejemplo el plano de arquitectura).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Elige el tipo</h4>
    <p>En el diálogo marca <strong>Adjuntar</strong> (tipo de referencia) y deja <em>Ubicación</em> en <strong>Relativa a ruta</strong>: así funciona para cualquier colaborador que tenga la misma estructura de carpetas.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Señala el punto base</h4>
    <p>Define el punto de inserción (0,0 normalmente) y la escala/rotación, y Acepta.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Gestiónala</h4>
    <p>Con <span class="cmd-inline">XREF</span> (paleta) puedes recargar, retirar (desvincular) o recortar cada referencia cuando el archivo original cambie.</p>
  </div>
</div>
<table class="table-cad">
  <thead><tr><th>Tipo de ruta</th><th>Qué significa</th><th>Recomendación</th></tr></thead>
  <tbody>
    <tr><td>Absoluta</td><td>Guarda la ruta completa desde el disco (<span class="cmd-inline">C:\\...\\Proyecto\\Base.dwg</span>).</td><td>Solo útil en tu puesto; rompe al enviar el archivo.</td></tr>
    <tr><td>Relativa</td><td>Guarda la ruta desde la carpeta del archivo actual (<span class="cmd-inline">..\\Base.dwg</span>).</td><td>La más segura para equipos y entregas.</td></tr>
    <tr><td>Sin ruta</td><td>Solo busca el nombre en las bibliotecas/adjuntos.</td><td>Útil si todo vive en la misma carpeta.</td></tr>
  </tbody>
</table>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Enviar solo el .DWG "principal" olvidando las Xrefs. El receptor verá el archivo descargado con las referencias rotas. Usa <span class="cmd-inline">ETRANSMIT</span> o revisa el tema "Transmitir y empaquetar" antes de entregar.</span>
</div>""",
]

ENRICH["nivel3-atajos"] = [
"""<h3>Personaliza tus propios alias</h3>
<p>Los atajos de dos o tres letras se llaman <strong>alias</strong> y se guardan en el archivo <span class="cmd-inline">acad.pgp</span>. Edítalos sin miedo:</p>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Abre el editor de alias</h4>
    <p>Herramientas → <strong>Personalizar</strong> → <em>Parámetros de alias</em> (o escribe <span class="cmd-inline">ALIASEDIT</span>).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Busca el comando</h4>
    <p>Filtra por nombre, por ejemplo BUSCAR "DIMSTYLE" para ver qué alias tiene asignado "D".</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Crea o modifica el alias</h4>
    <p>Haz clic en <em>Nuevo</em> o editar: cada alias debe ser único. Guarda y acepta la pregunta de "reescalar" (no, a menos que quieras cambiarla).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Compruébalo</h4>
    <p>El alias estará activo de inmediato en la línea de comandos. Si no responde, escribe <span class="cmd-inline">REINIT</span> → marca <strong>PGP File</strong>.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Consejo</span>
  <ul class="mb-0">
    <li>Respeta las <strong>mayúsculas iniciales</strong> de los grupos de comandos (dibujo con <span class="key-inline">L</span>, modificación con dos letras como <span class="key-inline">TR</span>, <span class="key-inline">CO</span>, <span class="key-inline">MI</span>).</li>
    <li>No "asaltes" alias ya instalados; asigna solo los que repites a diario.</li>
    <li>Haz una copia de <span class="cmd-inline">acad.pgp</span> cuando lo personalices mucho: es el archivo de tu flujo de trabajo.</li>
  </ul>
</div>""",
]

ENRICH["nivel3-plotstyles"] = [
"""<h3>Crea tu propio estilo .CTB</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Abre el gestor</h4>
    <p>Escribe <span class="cmd-inline">STYLESMANAGER</span>: se abre la carpeta de estilos de trazado.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Duplica monochrome</h4>
    <p>Haz clic derecho sobre <span class="cmd-inline">monochrome.ctb</span> → copiar y pega en la misma carpeta. Así conservas el original.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Edítalo</h4>
    <p>Doble clic sobre la copia y configura cada rango de colores (1-9, 10-19, ...) o color a color: grosor de salida, screening (atenuación) y trama.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Asígnale colores a grosores típicos</h4>
    <p>Regla práctica: color 1-9 (colores vivos) → pluma gruesa para muros; 10-19 → media para muebles y detalles; 20-29 → fina para cotas y textos; 30+ → muy fina para ejes y rellenos.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Con un .CTB dominas la impresión con el tradicional "negro + grosores por color". Si prefieres que el grosor viaje en la capa/usuario, cambia la lámina a <strong>cómo usar .STB</strong> (conversión en <span class="cmd-inline">CONVERTPSTYLES</span>).</span>
</div>
<h3>Mini ejercicio: atenúa las Xrefs al imprimir</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Crea un screening</h4>
    <p>En tu .CTB, selecciona el color de la capa donde vive la Xref (por ejemplo color 8 gris) y baja <em>Densidad de tinta (screening)</em> al <strong>25%</strong>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Imprime la planta</h4>
    <p>Haz una vista preliminar: la referencia externa sale más clara que tu geometría, destacando el contenido propio.</p>
  </div>
</div>""",
]

ENRICH["nivel3-campos"] = [
"""<h3>Otras categorías de campos útiles</h3>
<table class="table-cad">
  <thead><tr><th>Campo</th><th>Categoría</th><th>Qué muestra</th></tr></thead>
  <tbody>
    <tr><td>Número de lámina / Nombre de lámina</td><td>Conjunto de planos (Sheet Set)</td><td>El dato del Sheet Set asignado a esa hoja.</td></tr>
    <tr><td>Fecha / Hora</td><td>Sistema</td><td>Fecha y hora del sistema al actualizar el campo.</td></tr>
    <tr><td>Escala de la ventana gráfica</td><td>Objeto</td><td>La escala activa del viewport (ej. "1:50").</td></tr>
    <tr><td>Perímetro</td><td>Objeto</td><td>El perímetro cerrado de una polilínea o región.</td></tr>
  </tbody>
</table>
<h3>Mini ejercicio: cajetín con área automática</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Inserta el campo</h4>
    <p>Dentro de un <span class="cmd-inline">MTEXT</span> en el cajetín, clic derecho → <strong>Insertar campo</strong> → categoría <em>Objeto</em> → <strong>Área</strong>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Selecciona la geometría</h4>
    <p>Con el botón de selección elige la polilínea cerrada que limita la planta (define antes el contorno con <span class="cmd-inline">BOUNDARY</span> si no existe).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Actualiza con el campo</h4>
    <p>Acepta y, al cambiar la geometría, ejecuta <span class="cmd-inline">UPDATEFIELD</span> o recarga el campo con clic derecho → <em>Actualizar campo</em>: el área se recalcula sola.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Pensar que el campo se actualiza en cada guardado por sí mismo. Se actualiza al <span class="cmd-inline">REGEN</span>, al imprimir o con <span class="cmd-inline">UPDATEFIELD</span>; si el plano muestra un dato viejo, comprueba primero que el campo esté reciente.</span>
</div>""",
]

ENRICH["nivel3-xref-avanzado"] = [
"""<h3>Recortar una Xref con forma poligonal</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Activa el recorte</h4>
    <p>Escribe <span class="cmd-inline">XCLIP</span> y selecciona la referencia que quieres recortar.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Define el límite</h4>
    <p>Elige <strong>Nuevo límite</strong> y la opción <span class="cmd-inline">P</span> (Poligonal); dibuja el polígono sobre la zona de la Xref que debe verse.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Ajusta o quita el límite</h4>
    <p>Para corregir usa <em>Editar límite</em>; para volver a mostrar toda la Xref usa <span class="cmd-inline">XCLIP</span> → <em>Borrar</em>. La Xref no se modifica: solo su vista.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Buenas prácticas</span>
  <ul class="mb-0">
    <li>Usa <strong>Overlay</strong> (no hereda) por defecto; reserva <strong>Attach</strong> para cadenas realmente necesarias.</li>
    <li>Configura <strong>rutas relativas</strong> y la misma estructura de carpetas en todo el equipo.</li>
    <li>Al terminar una fase, elimina referencias sin uso con <span class="cmd-inline">XREF</span> → <em>Desvincular</em> y <span class="cmd-inline">PURGE</span> para adelgazar el archivo.</li>
    <li>Congela las capas de la Xref en el viewport si la ves "sucia": así la referencia no se imprime sin necesidad.</li>
  </ul>
</div>""",
]

ENRICH["nivel3-cajetines"] = [
"""<h3>Mini ejercicio: cajetín con atributos en 5 pasos</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Dibuja el marco</h4>
    <p>En el layout, dibuja con <span class="cmd-inline">RECTANG</span> o <span class="cmd-inline">POLYLINE</span> el rectángulo del cajetín según tu norma (por ejemplo ISO 7200 o el formato de tu país).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Define los atributos</h4>
    <p>Escribe <span class="cmd-inline">ATTDEF</span> y crea los campos variables: ESCALA, NUMERO-LAMINA, REVISION. Deja "PROYECTO" y "AUTOR" como texto fijo o campo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Forma el bloque</h4>
    <p>Con <span class="cmd-inline">BLOCK</span> selecciona marco + líneas + atributos y define el punto base en la esquina inferior derecha (o la que marque tu norma).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Insértalo</h4>
    <p>Con <span class="cmd-inline">INSERT</span> colócalo en cada lámina; AutoCAD te pedirá los valores de atributo al insertar (escala, número de lámina...).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">5</span>
  <div class="lesson-body">
    <h4>Edítalo sin explotar</h4>
    <p>Para cambiar un valor de una inserción usa <span class="cmd-inline">EATTEDIT</span> (o doble clic sobre el bloque). El cajetín sigue siendo un bloque: nadie lo dibuja dos veces.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Referencia rápida</span>
  <span>ISO 7200 define las zonas del cajetín (título, identificación, sellos de revisión). Añade también un campo de <em>escala</em> que lea la escala del viewport: se actualizará solo si usas escala anotativa.</span>
</div>""",
]

ENRICH["nivel3-escala-anotativa"] = [
"""<h3>Flujo de trabajo anotativo desde cero</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Estilos anotativos</h4>
    <p>Crea un estilo de texto y otro de cota con la casilla <strong>Annotative</strong> activada (pestaña <em>Ajustar</em>) y su altura de papel (por ejemplo 2.5 mm de texto).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Marcar objetos anotativos</h4>
    <p>Asigna el estilo a tus cotas, textos, hatches o bloque de nube de revisión; los bloques se marcan al crearlos o desde <span class="cmd-inline">BEDIT</span>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Dale las escalas</h4>
    <p>Con el objeto seleccionado usa <span class="cmd-inline">OBJECTSCALE</span> para añadir las escalas en las que debe aparecer (1:50 y 1:100, por ejemplo).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>El viewport hace el resto</h4>
    <p>En cada ventana gráfica, asigna la escala correspondiente en la barra de estado. El mismo texto se mostrará correcto en ambas, sin duplicarlo.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Activar <strong>Annote a escala Automático</strong> sin revisar: AutoCAD crea representaciones de escala por cada zoom y el dibujo se llena de copias invisibles que inflan el archivo. Revisa las escalas con <span class="cmd-inline">OBJECTSCALE</span> y borra las que no usas.</span>
</div>""",
]

ENRICH["nivel3-estandares-capas"] = [
"""<h3>Pon en marcha un estándar de capas</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Define la nomenclatura</h4>
    <p>Fija el prefijo de disciplina (A arquitectura, S estructura, M mecánico, E eléctrico) y el separador con guion: <span class="cmd-inline">A-Muros</span>, <span class="cmd-inline">E-Salidas</span>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Fija colores, grosores y tipos</h4>
    <p>Asigna a cada capa un color, un grosor de línea (pluma) y un tipo de línea (contorno, oculta, centrada) pensando en el estilo de trazado.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Guárdala en la plantilla</h4>
    <p>Crea las capas en tu .DWT para que todo dibujo nuevo ya las tenga.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Aplica LAYERSTATES</h4>
    <p>Guarda estados de capa (qué se ve, qué se congela) con <span class="cmd-inline">LAYERSTATES</span> para alternar entre plantas y detalles sin tocar nada a mano.</p>
  </div>
</div>
<table class="table-cad">
  <thead><tr><th>Comando</th><th>Qué hace</th></tr></thead>
  <tbody>
    <tr><td class="cmd-inline">LAYISO</td><td>Aísla la capa del objeto seleccionado (oculta las demás).</td></tr>
    <tr><td class="cmd-inline">LAYUNISO</td><td>Restaura las capas que habías aislado.</td></tr>
    <tr><td class="cmd-inline">LAYOFF</td><td>Apaga la capa (no se muestra ni se imprime).</td></tr>
    <tr><td class="cmd-inline">LAYON</td><td>Enciende todas las capas apagadas.</td></tr>
    <tr><td class="cmd-inline">LAYMC</td><td>Cambia el objeto seleccionado a la capa actual.</td></tr>
  </tbody>
</table>
<div class="callout">
  <span class="callout-title">Regla de oro</span>
  <span>Todo se dibuja <strong>ByLayer</strong>. Los filtros y estados (<span class="cmd-inline">LAYERSTATES</span>) dependen de que la capa sea la fuente de verdad de color, grosor y tipo de línea.</span>
</div>""",
]

ENRICH["nivel3-sheet-sets"] = [
"""<h3>Del Sheet Set a la entrega</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Estructura el conjunto</h4>
    <p>En <span class="cmd-inline">SSM</span> crea subcategorías por disciplina o por fase y arrastra las láminas dentro de cada una.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Numera desde el panel</h4>
    <p>Selecciona las láminas y elige <em>Renumerar</em>: los números se actualizan en orden y los campos del cajetín los reflejan.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Publica el conjunto</h4>
    <p>Clic derecho sobre el conjunto → <strong>Publicar</strong> → <em>Publicar en PDF</em>. Obtienes un solo PDF con todas las láminas ordenadas y numeradas.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Respáldalo</h4>
    <p>El conjunto vive en un archivo <span class="cmd-inline">.dst</span>: guárdalo junto al proyecto o en la plantilla del equipo para no perder la estructura.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Los campos de lámina (número, nombre, revisión, fecha) pueden leerse desde el Sheet Set: cambias un valor en el panel y el cajetín se actualiza sin tocar cada dibujo.</span>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>No mantener sincronizados los archivos .DWG con el Sheet Set. Si mueves, renombras o borras una lámina desde el explorador de Windows (fuera de SSM), el conjunto pierde el vínculo: gestiona siempre desde <span class="cmd-inline">SSM</span>.</span>
</div>""",
]

# ----------------------------------------------------------------------------
# 3) Lecciones nuevas (contenido completo)
# ----------------------------------------------------------------------------
NEW_SECTIONS = {}

NEW_SECTIONS["nivel3-designcenter"] = """
<h2><span class="sec-num">N</span>DesignCenter y paletas de herramientas</h2>
<p><strong>DesignCenter</strong> (<span class="cmd-inline">ADCENTER</span>, <span class="key-inline">Ctrl+2</span>) es el "explorador de contenido" de AutoCAD: navega entre las carpetas y archivos .DWG de tu equipo y arrastra bloques, capas, tipos de línea, estilos y layouts de UN dibujo a OTRO sin redibujarlos. Es la vía más rápida para reutilizar el contenido de proyectos anteriores.</p>

<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>DesignCenter no "importa" el archivo completo: copia solo los objetos que arrastras. Ideal para estandarizar: el equipo comparte una carpeta de <em>biblioteca</em> con los bloques y estilos aprobados.</span>
</div>

<h3>Qué puedes arrastrar al dibujo</h3>
<table class="table-cad">
  <thead><tr><th>Contenido</th><th>Cómo llega al dibujo</th></tr></thead>
  <tbody>
    <tr><td>Bloques</td><td>Se insertan en el punto que elijas (puedes predefinir escala y rotación).</td></tr>
    <tr><td>Capas</td><td>Se copian sus propiedades y nombres; si ya existen, se fusionan.</td></tr>
    <tr><td>Tipos de línea y estilos de texto/cota</td><td>Se copian completos a los estilos del dibujo actual.</td></tr>
    <tr><td>Layouts</td><td>Se copian tal cual, incluida la configuración de página.</td></tr>
    <tr><td>Imágenes y bloques externos</td><td>Se adjuntan o insertan manteniendo su ruta original.</td></tr>
  </tbody>
</table>

<h3>Usarlo paso a paso</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Abre el panel</h4>
    <p>Escribe <span class="cmd-inline">ADCENTER</span> o pulsa <span class="key-inline">Ctrl+2</span>. A la izquierda navega por las carpetas; a la derecha ves el contenido de la carpeta o archivo elegido.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Localiza el bloque</h4>
    <p>En la carpeta de bibliotecas abre el .DWG que contiene el bloque (o usa la pestaña <em>Bloques</em> de <span class="cmd-inline">ADCENTER</span>).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Arrastra o inserta</h4>
    <p>Arrastra el bloque desde el panel hasta el dibujo, o doble clic para insertarlo en el origen con prefijo estándar.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Copia o estilos</h4>
    <p>Para capas, tipos de línea o estilos: clic derecho → <strong>Copiar</strong>, o arrastra de la misma manera. Verifica en <span class="cmd-inline">LAYER</span> que ya están disponibles.</p>
  </div>
</div>

<h3>Paletas de herramientas: tu biblioteca personal</h3>
<p>La <strong>paleta de herramientas</strong> (<span class="cmd-inline">TOOLPALETTES</span>, <span class="key-inline">Ctrl+3</span>) guarda accesos directos a tus bloques, sombreados y comandos favoritos. Crea una pestaña "Mi empresa", arrastra un bloque desde DesignCenter hasta la paleta y se quedará ahí para siempre: un clic (o arrastre) lo inserta sin abrir el panel.</p>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Copiar un bloque con "Ctrl+C / Ctrl+V" de un dibujo a otro funciona, pero con DesignCenter es más limpio: importas el bloque sin arrastrar capas fantasma ni estilos sobrantes del archivo de origen.</span>
</div>
<h3>Mini ejercicio: monta tu biblioteca de bloques</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Crea la carpeta base</h4>
    <p>Mantén una carpeta del equipo (por ejemplo en la red) con .DWG de símbolos: mobiliario, simbología, detalles.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Fija DesignCenter</h4>
    <p>En <span class="cmd-inline">ADCENTER</span> clic derecho → <em>Opción Inicio</em> → añade esa carpeta a las <strong>bibliotecas</strong>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Puebla una paleta</h4>
    <p>Arrastra los bloques que usas a diario hasta la paleta "Mi empresa" y ordénalos por categorías (Pilares, Mobiliario, Sanitario).</p>
  </div>
</div>
"""

NEW_SECTIONS["nivel3-publish"] = """
<h2><span class="sec-num">N</span>Publicación por lotes (PUBLISH)</h2>
<p>Cuando el proyecto tiene varios layouts o varios archivos, imprimir uno a uno es lento y propenso a olvidos. <strong>PUBLISH</strong> (<span class="cmd-inline">PUBLISH</span>, <span class="key-inline">Ctrl+P</span> con la lista de hojas) crea una <em>lista de hojas</em> con todos los layouts y archivos que quieres y genera de una sola vez el PDF completo, los plotters o los archivos DWF.</p>

<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Antes de publicar, cada layout debe tener su <strong>configuración de página</strong> correcta (papel, escala, estilo de trazado). PUBLISH solo ejecuta esas configuraciones: si una hoja está mal definida, sale mal.</span>
</div>

<h3>Qué incluye la lista de hojas</h3>
<table class="table-cad">
  <thead><tr><th>Elemento</th><th>Qué hace</th></tr></thead>
  <tbody>
    <tr><td>Layouts del archivo actual</td><td>Cada pestaña de presentación se añade como hoja independiente.</td></tr>
    <tr><td>Otros archivos .DWG</td><td>Con el botón <em>Agregar hojas</em> añades archivos completos (todas sus layouts).</td></tr>
    <tr><td>Modelo</td><td>La pestaña Modelo se imprime con su configuración de espacio modelo si la marcas.</td></tr>
    <tr><td>Conjuntos de planos</td><td>Se pueden publicar todas las láminas de un Sheet Set en bloque.</td></tr>
  </tbody>
</table>

<h3>Publicar a PDF paso a paso</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Abre el diálogo</h4>
    <p>Fichero → <strong>Publicar</strong> (o escribe <span class="cmd-inline">PUBLISH</span>).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Completa la lista</h4>
    <p>Marca los layouts a publicar o usa <em>Agregar hojas / Importar</em> para traer layouts de otros archivos del proyecto.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Elige el destino</h4>
    <p>En <em>Lista de plotters</em> selecciona un destino: <span class="cmd-inline">DWG To PDF.pc3</span>, <span class="cmd-inline">PDF</span>, plotter física o <span class="cmd-inline">DWF</span>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Configura el PDF</h4>
    <p>Activa "Publicar hojas en orden inverso" si tu gráfica lo requiere y define <em>Opciones de PDF</em>: capas (capa por hoja), calidad y marcado de impresión.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">5</span>
  <div class="lesson-body">
    <h4>Publica</h4>
    <p>Pulsa <em>Publicar</em>, guarda el archivo .DWF de cola (opcional) y revisa el resultado: un único PDF con todas las hojas del proyecto.</p>
  </div>
</div>

<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Publicar con hojas que no tienen configuración de página definida. Revisa cada layout con <span class="cmd-inline">PAGESETUP</span> antes de publicar; si no, "Hojas No insertadas" producirá un PDF con blancos o escalas equivocadas.</span>
</div>
<h3>Mini ejercicio: publica tu proyecto de prueba</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Prepara dos layouts</h4>
    <p>Configura dos presentaciones (Planta 1:50 y Detalle 1:20) con su <span class="cmd-inline">PAGESETUP</span> y estilo de trazado monochrome.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Publícalas</h4>
    <p>Con <span class="cmd-inline">PUBLISH</span> añade ambas hojas y publica a <strong>DWG To PDF.pc3</strong>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Reordena</h4>
    <p>En la lista, arrastra el Detalle antes de la Planta y vuelve a publicar: el orden del PDF cambia sin tocar los dibujos.</p>
  </div>
</div>
"""

NEW_SECTIONS["nivel3-etransmit"] = """
<h2><span class="sec-num">N</span>Transmitir y empaquetar (ETRANSMIT)</h2>
<p><strong>ETRANSMIT</strong> (<span class="cmd-inline">ETRANSMIT</span>) reúne el dibujo actual —o un conjunto de archivos— y <strong>todo lo que necesita para abrirse correctamente</strong> en un solo paquete: referencias externas, imágenes, fuentes, estilos de trazado y los archivos dependientes. Entrega un .zip o un archivo de datos de transmisión y el destinatario lo abre sin rutas rotas ni fuentes faltantes.</p>

<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Enviar solo el .DWG "principal" es la causa número uno de archivos rotos: el receptor abre el dibujo con las Xrefs en rojo y los grosores de la lámina desaparecidos. ETRANSMIT resuelve eso en un clic.</span>
</div>

<h3>Qué puede incluir el paquete</h3>
<table class="table-cad">
  <thead><tr><th>Opción</th><th>Qué incluye</th><th>Cuándo marcarla</th></tr></thead>
  <tbody>
    <tr><td>Referencias externas</td><td>Todos los .DWG adjuntados y las imágenes/PDF vinculados.</td><td>Siempre que el dibujo use Xrefs.</td></tr>
    <tr><td>Fuentes de texto</td><td>Tipos de letra .shx/.ttf usados por TEXT/MTEXT.</td><td>Si usas fuentes no estándar de AutoCAD.</td></tr>
    <tr><td>Estilos de trazado</td><td>Archivos .ctb/.stb usados en layout.</td><td>Para que el plano conserve sus grosores al imprimir.</td></tr>
    <tr><td>Configuración de dibujo</td><td>Ajustes, unidades y variables de sistema.</td><td>Por defecto; mantiene el archivo coherente.</td></tr>
    <tr><td>Especificación del conjunto</td><td>Los archivos de un Sheet Set (.dst) y sus planos.</td><td>Cuando entregas un proyecto completo.</td></tr>
  </tbody>
</table>

<h3>Crear la transmisión paso a paso</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Abre la herramienta</h4>
    <p>Fichero → <strong>Transmitir</strong> (o escribe <span class="cmd-inline">ETRANSMIT</span>).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Añade archivos</h4>
    <p>Arrastra otros .DWG del proyecto a la lista si quieres entregar más de uno en el mismo paquete.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Configura el informe</h4>
    <p>Revisa el <em>Informe de transmisión</em>: muestra qué archivos, rutas y dependencias entran. Copia el texto si quieres adjuntarlo como Readme.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Elige el formato</h4>
    <p>En <em>Opciones de transmisión</em> elige tipo de archivo: <strong>Zip</strong> (.zip), carpeta o <strong>archivo de datos de transmisión</strong> (.dws).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">5</span>
  <div class="lesson-body">
    <h4>Opciones de organización</h4>
    <p>Marca "Mantener estructura de carpetas" si el conjunto lo necesita, o plana si quieres un único nivel de carpetas. Guarda el .zip y entrégalo.</p>
  </div>
</div>

<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Generar la transmisión y entregar el .zip desde una carpeta con las Xrefs "parcheadas" por casualidad. Comprueba siempre el <strong>informe</strong>: cualquier archivo que falte aparece listado allí antes de empaquetar.</span>
</div>
<h3>Mini ejercicio: empaqueta un dibujo con Xref</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Prepara el lío</h4>
    <p>En un archivo de prueba adjunta una Xref con ruta relativa y una imagen vinculada.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Transmite</h4>
    <p>Ejecuta <span class="cmd-inline">ETRANSMIT</span>, revisa el informe y guarda el .zip.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Verifica</h4>
    <p>Descomprime en otra carpeta (o copia el .zip a otra máquina), abre el .DWG y comprueba que la Xref y la imagen cargan sin buscar rutas.</p>
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
    next_btn = '<a href="../nivel-4-modelado-3d/index.html" class="btn-cad-outline w-100 text-center d-block">Siguiente nivel <i class="bi bi-arrow-right"></i></a>'
    nav_next = """<a href="../nivel-4-modelado-3d/index.html" class="nav-next">
            <span class="nav-label">Siguiente</span>
            <span class="nav-title">Siguiente nivel <i class="bi bi-arrow-right"></i></span>
          </a>"""
    page = f"""<!DOCTYPE html>
<html lang="es" data-theme="dark">
{build_head(f"Nivel {NUM} · {FULL_TITLE} — AutoCAD Guía", f"/paginas/{FOLDER}/index.html", LEVELS[3][4], include_3d=False, schema_name=SCHEMA_NAME, schema_desc=SCHEMA_DESC)}

<body>

<a href="#main-content" class="skip-link">Saltar al contenido principal</a>

{build_navbar(NUM)}

<header class="page-header" id="main-content">
  <div class="container container-xl">
    <p class="crumb"><a href="../../index.html">Inicio</a> / <a href="../../index.html#niveles">Niveles</a> / {FULL_TITLE}</p>
    <span class="eyebrow" data-i18n="lvl{NUM}.eyebrow">{EYEBROW}</span>
    <h1 data-i18n="lvl{NUM}.title">{FULL_TITLE}</h1>
    <p class="subtitle" data-i18n="lvl{NUM}.subtitle">{LEVELS[3][4]}</p>
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
    "nivel3-designcenter": "nivel-3-organizacion/plantillas.html",
    "nivel3-publish":      "nivel-3-organizacion/impresion.html",
    "nivel3-etransmit":    "nivel-3-organizacion/sheet-sets.html",
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
                 '    "path": "Nivel 3 · Organización"\n'
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
    src_73 = "const total = 73; // 12 + 18 + 13 + 16 + 14"
    dst_76 = "const total = 76; // 12 + 18 + 16 + 16 + 14"
    if src_73 in mj:
        mj = mj.replace(src_73, dst_76)
        write(mp, mj)
        print("main.js: total 73 -> 76")
    else:
        print("main.js: total 73 no encontrado (revisar)")


def update_index_label():
    ip = os.path.join(ROOT, "index.html")
    idx = read(ip)
    if "0 de 73 temas completados" in idx:
        idx = idx.replace("0 de 73 temas completados", "0 de 76 temas completados")
        write(ip, idx)
        print("index.html: label 73 -> 76")
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