# -*- coding: utf-8 -*-
"""
build_level1_content.py
Enriquece el Nivel 1 (Fundamentos):
  - Añade contenido nuevo (conceptos, tablas de comandos, ejemplos paso a paso,
    callouts, atajos y mini ejercicios) a las 9 lecciones existentes.
  - Crea 3 lecciones nuevas: osnap-basico, gestion-dibujo, atajos-esenciales.
  - Regenera las 12 páginas de lección y la portada index.html del nivel.
  - Actualiza search-index.js, sitemap.xml, main.js (total 70) e index.html.

Ejecutar desde la raíz:  python scripts/build_level1_content.py
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

FOLDER = "nivel-1-fundamentos"
DST = os.path.join(ROOT, "paginas", FOLDER)
NUM = 1
TOTAL = 12
EYEBROW = LEVELS[1][3]
FULL_TITLE = LEVELS[1][2]
SCHEMA_NAME = LEVELS[1][5]
SCHEMA_DESC = LEVELS[1][6]


def indent(text, n):
    pad = " " * n
    return "\n".join((pad + ln if ln.strip() else ln) for ln in text.split("\n"))


def esc(x):
    return x.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ----------------------------------------------------------------------------
# 1) Catálogo de temas del nivel (orden de estudio)
# ----------------------------------------------------------------------------
# data_topic --> (archivo, título del h2/h1, etiqueta TOC, descripción)
TOPICS = [
    ("nivel1-que-es",            "que-es.html",            "¿Qué es AutoCAD y para qué se usa?",          "Qué es AutoCAD",              "AutoCAD es un programa de diseño asistido por computadora (CAD) desarrollado por Autodesk, usado para crear dibujos técnicos precisos en 2D y 3D."),
    ("nivel1-instalacion",       "instalacion.html",       "Instalación, requisitos y tipos de licencia", "Instalación y licencias",     "Cómo instalar AutoCAD, requisitos mínimos orientativos y los distintos tipos de licencia disponibles."),
    ("nivel1-interfaz",          "interfaz.html",          "Interfaz de usuario",                          "Interfaz de usuario",         "Zonas de la ventana de AutoCAD, espacios de trabajo y las tres formas de ejecutar un comando."),
    ("nivel1-coordenadas",       "coordenadas.html",       "Sistema de coordenadas",                       "Sistema de coordenadas",      "Coordenadas absolutas, relativas y polares, más la entrada dinámica para dibujar con precisión."),
    ("nivel1-osnap-basico",      "osnap-basico.html",      "Referencia a objetos (OSNAP) y rastreo",       "Referencia a objetos (OSNAP)", "Referencia a objetos (OSNAP): cómo enganchar el cursor a puntos geométricos y rastrear alineaciones."),
    ("nivel1-configuracion",     "configuracion.html",     "Configuración inicial de un dibujo",          "Configuración inicial",       "Unidades, límites, rejilla, captura y plantillas: todo lo que conviene configurar antes de dibujar."),
    ("nivel1-archivos",          "archivos.html",          "Gestión de archivos DWG",                      "Gestión de archivos",         "Guardar, versiones y compatibilidad, autoguardado y recuperación de archivos DWG."),
    ("nivel1-tipos-archivo",     "tipos-archivo.html",     "Tipos de archivo",                             "Tipos de archivo",            "DWG, DWT, DXF, DWF, copias de seguridad y cómo elegir el formato correcto."),
    ("nivel1-gestion-dibujo",    "gestion-dibujo.html",    "Deshacer, purgar y mantener tu dibujo",        "Mantener el dibujo sano",     "UNDO/REDO, PURGE, AUDIT y RECOVER para corregir errores y mantener archivos rápidos y fiables."),
    ("nivel1-zoom",              "zoom.html",              "Zoom y navegación",                            "Zoom y navegación",           "Zoom al mouse, window, extents y pan para moverte con agilidad por el área de dibujo."),
    ("nivel1-atajos-esenciales", "atajos-esenciales.html", "Comandos y atajos esenciales del nivel 1",     "Comandos y atajos esenciales", "Teclas de función, combinaciones de teclado y el hábito de escribir comandos en la línea."),
    ("nivel1-primer-dibujo",     "primer-dibujo.html",     "Tu primer dibujo: práctica guiada",            "Primer dibujo guiado",        "Práctica que reúne todo el nivel dibujando la planta de un cuarto de 3 x 2 metros paso a paso."),
]

TOPIC_META = {t[0]: t for t in TOPICS}
FILE_TO_TOPIC = {t[1]: t[0] for t in TOPICS}

# ----------------------------------------------------------------------------
# 2) Contenido de enriquecimiento para las lecciones existentes
# ----------------------------------------------------------------------------
# Cada fragmento se inserta antes del botón "Marcar tema como visto".
ENRICH = {}

ENRICH["nivel1-que-es"] = [
    """
    <h3>Conceptos que conviene dominar desde el primer día</h3>
    <ul>
      <li><strong>Dibujo vectorial:</strong> AutoCAD no guarda una imagen, guarda objetos definidos matemáticamente (líneas, círculos, arcos). Por eso puedes hacer zoom infinito sin que el dibujo pierda nitidez.</li>
      <li><strong>Escala real 1:1:</strong> dibujas las cosas con su tamaño real y aplicas la escala solo al imprimir o presentar.</li>
      <li><strong>Formato .DWG:</strong> es el archivo nativo de AutoCAD. Casi toda la industria CAD lo reconoce.</li>
      <li><strong>La línea de comandos:</strong> es el "cerebro" del programa: AutoCAD te informa en cada paso de qué espera que hagas.</li>
    </ul>

    <div class="callout">
      <span class="callout-title">Idea clave</span>
      <span>Los objetos de AutoCAD son <strong>editables en cualquier momento</strong>: una línea se puede alargar, mover, rotar, recortar o borrar sin redibujar. Eso es lo que lo diferencia de un programa de dibujo artístico.</span>
    </div>

    <h3>AutoCAD frente a otras herramientas de diseño</h3>
    <p>Elegir herramienta depende del objetivo: no es lo mismo hacer un plano 2D, modelar una pieza o coordinar un edificio completo.</p>
    <table class="table-cad">
      <thead><tr><th>Herramienta</th><th>Enfoque</th><th>Cuándo usarla en lugar de AutoCAD</th></tr></thead>
      <tbody>
        <tr><td><span class="cmd-inline">AutoCAD</span></td><td>Dibujo técnico 2D y modelado 3D libre</td><td>Planos de detalle, sectores mecánicos, instalaciones y plantas.</td></tr>
        <tr><td><span class="cmd-inline">Revit</span></td><td>BIM (modelo informado de edificación)</td><td>Proyectos arquitectónicos donde hay que coordinar estructuras e instalaciones entre equipos.</td></tr>
        <tr><td><span class="cmd-inline">ArchiCAD</span></td><td>CAD + BIM</td><td>Alternativa BIM con flujo de trabajo cercano al dibujo clásico.</td></tr>
        <tr><td><span class="cmd-inline">SketchUp</span></td><td>Modelado 3D rápido</td><td>Maquetas conceptuales y visualizaciones rápidas, no planos de precisión.</td></tr>
        <tr><td><span class="cmd-inline">LibreCAD / FreeCAD</span></td><td>CAD de código abierto</td><td>Aprender sin coste o proyectos sencillos; compatibilidad parcial de formatos.</td></tr>
      </tbody>
    </table>

    <h3>Mini ejercicio: tu primera orden al programa</h3>
    <div class="lesson-step">
      <span class="lesson-num">1</span>
      <div class="lesson-body">
        <h4>Abre un dibujo nuevo</h4>
        <p>Pulsa <span class="key-inline">Ctrl+N</span> y elige la plantilla por defecto (<code>acad.dwt</code>).</p>
      </div>
    </div>
    <div class="lesson-step">
      <span class="lesson-num">2</span>
      <div class="lesson-body">
        <h4>Escribe un comando en la línea de comandos</h4>
        <p>Teclea <span class="cmd-inline">LINE</span> y pulsa <span class="key-inline">Enter</span>. Fíjate en el mensaje de abajo: AutoCAD está esperando que definas el <em>primer punto</em>.</p>
      </div>
    </div>
    <div class="lesson-step">
      <span class="lesson-num">3</span>
      <div class="lesson-body">
        <h4>Cancela con un clic derecho o Esc</h4>
        <p>Pulsa <span class="key-inline">Esc</span> para terminar. Repite el ritual con <span class="cmd-inline">CIRCLE</span>: verás que cada comando tiene su propia secuencia de preguntas en la línea de comandos.</p>
      </div>
    </div>
    <div class="callout">
      <span class="callout-title">Para recordar</span>
      <span>Si alguna vez "no sabes qué hacer", mira siempre la <strong>línea de comandos</strong>: ella te dice exactamente qué dato está esperando AutoCAD.</span>
    </div>
    """,
]

ENRICH["nivel1-instalacion"] = [
    """
    <h3>Dónde y cómo descargar AutoCAD</h3>
    <ol>
      <li>Crea una cuenta en el portal de Autodesk y verifica tu correo.</li>
      <li>Entra en <em>Productos y servicios</em> y elige tu versión de AutoCAD.</li>
      <li>Descarga el instalador (varios GB) y ejecútalo con permisos de administrador.</li>
      <li>Sigue el asistente aceptando la licencia y los componentes por defecto.</li>
      <li>Al abrir AutoCAD por primera vez, inicia sesión con tu cuenta Autodesk.</li>
    </ol>
    <div class="callout">
      <span class="callout-title">Versión de prueba (Trial)</span>
      <span>Si aún no decides, la <strong>versión de prueba</strong> es la misma aplicación completa por tiempo limitado: sirve para comprobar el rendimiento con tus propios archivos antes de pagar.</span>
    </div>

    <h3>Licencia educativa gratuita</h3>
    <p>Autodesk ofrece <strong>acceso gratuito</strong> a estudiantes, docentes e instituciones a través de su portal de educación. El acceso se gestiona por año lectivo y requiere verificación.</p>
    <div class="lesson-step">
      <span class="lesson-num">1</span>
      <div class="lesson-body">
        <h4>Solicita tu acceso educativo</h4>
        <p>Entra al programa de educación de Autodesk y registra tu correo institucional (.edu o el que tu centro reconozca).</p>
      </div>
    </div>
    <div class="lesson-step">
      <span class="lesson-num">2</span>
      <div class="lesson-body">
        <h4>Descarga AutoCAD dentro de Education</h4>
        <p>Una vez verificado, el portal te permite descargar la licencia de estudiante, que funciona como la versión comercial.</p>
      </div>
    </div>
    <div class="lesson-step">
      <span class="lesson-num">3</span>
      <div class="lesson-body">
        <h4>Renueva cada año</h4>
        <p>La licencia educativa se renueva anualmente mientras sigas activo como estudiante o docente. Recuerda renovarla antes de que expire.</p>
      </div>
    </div>

    <h3>AutoCAD frente a AutoCAD LT</h3>
    <table class="table-cad">
      <thead><tr><th>Característica</th><th>AutoCAD</th><th>AutoCAD LT</th></tr></thead>
      <tbody>
        <tr><td>Dibujo 2D y anotación</td><td>Sí</td><td>Sí</td></tr>
        <tr><td>Modelado y sólidos 3D</td><td>Sí</td><td>No (solo visualiza archivos 3D)</td></tr>
        <tr><td>Personalización con LISP / scripts</td><td>Sí</td><td>No</td></tr>
        <tr><td>Herramientas de automatización avanzadas</td><td>Sí</td><td>Limitadas</td></tr>
        <tr><td>Precio</td><td>Mayor</td><td>Menor</td></tr>
      </tbody>
    </table>
    <div class="callout">
      <span class="callout-title">Consejo</span>
      <span>Si tu trabajo es solo 2D y no requieres LISP, LT puede ser suficiente. Para seguir esta guía (incluye 3D) necesitas <strong>AutoCAD completo</strong> o la licencia educativa.</span>
    </div>

    <h3>Mini ejercicio: conoce tu instalación</h3>
    <div class="lesson-step">
      <span class="lesson-num">1</span>
      <div class="lesson-body">
        <h4>Comprueba tu versión</h4>
        <p>Escribe <span class="cmd-inline">ABOUT</span> en la línea de comandos y observa la versión, build y tipo de licencia.</p>
      </div>
    </div>
    <div class="lesson-step">
      <span class="lesson-num">2</span>
      <div class="lesson-body">
        <h4>Comprueba los requisitos reales</h4>
        <p>Compara los requisitos de tu equipo (Windows + RAM + tarjeta gráfica) con los oficiales y anota cuál de tus componentes es el "cuello de botella".</p>
      </div>
    </div>
    """,
]

ENRICH["nivel1-interfaz"] = [
    """
    <h3>Espacios de trabajo (workspaces)</h3>
    <p>Un <strong>espacio de trabajo</strong> cambia qué cintas y paletas se muestran según la tarea. AutoCAD trae varios; puedes alternarlos en todo momento.</p>
    <table class="table-cad">
      <thead><tr><th>Espacio de trabajo</th><th>Para qué sirve</th></tr></thead>
      <tbody>
        <tr><td><span class="cmd-inline">Drafting &amp; Annotation</span></td><td>El predeterminado para dibujo 2D y acotación.</td></tr>
        <tr><td><span class="cmd-inline">3D Basics</span></td><td>Pocas herramientas enfocadas a empezar en 3D.</td></tr>
        <tr><td><span class="cmd-inline">3D Modeling</span></td><td>Ribbon 3D completo: sólidos, mallas, superficies y render.</td></tr>
        <tr><td><span class="cmd-inline">AutoCAD Classic</span></td><td>Distribución con menús desplegables y barras de herramientas clásicas.</td></tr>
      </tbody>
    </table>
    <div class="lesson-step">
      <span class="lesson-num">1</span>
      <div class="lesson-body">
        <h4>Cambia de espacio de trabajo</h4>
        <p>En la barra de estado inferior haz clic en el icono de <em>engranaje</em> y elige "3D Modeling". Prueba después volver a "Drafting &amp; Annotation".</p>
      </div>
    </div>
    <div class="lesson-step">
      <span class="lesson-num">2</span>
      <div class="lesson-body">
        <h4>También por comando</h4>
        <p>Escribe <span class="cmd-inline">WORKSPACE</span> y usa las opciones de la línea de comandos para cambiar de espacio sin tocar el mouse.</p>
      </div>
    </div>

    <h3>Limpiar la pantalla para dibujar a fondo perdido</h3>
    <table class="table-cad">
      <thead><tr><th>Atajo</th><th>Efecto</th></tr></thead>
      <tbody>
        <tr><td><span class="key-inline">Ctrl+0</span></td><td>Pantalla limpia: oculta la cinta y las paletas, dejando solo el área de dibujo.</td></tr>
        <tr><td><span class="key-inline">Ctrl+1</span></td><td>Muestra/oculta la paleta de propiedades del objeto seleccionado.</td></tr>
        <tr><td><span class="key-inline">Ctrl+9</span></td><td>Muestra/oculta la línea de comandos.</td></tr>
        <tr><td><span class="key-inline">Ctrl+B</span></td><td>Alterna el estado de la cinta de opciones (ribbon).</td></tr>
      </tbody>
    </table>
    <div class="callout">
      <span class="callout-title">Consejo</span>
      <span>Muchos usuarios dibujan con <span class="key-inline">Ctrl+0</span> activado y salen de la pantalla limpia con la misma combinación cuando necesitan la cinta.</span>
    </div>

    <h3>Personaliza el tamaño del cursor</h3>
    <p>El cursor en cruz (<em>crosshair</em>) te ayuda a alinear el dibujo. Puedes agrandarlo para visualizar mejor horizontal y vertical.</p>
    <ul>
      <li>Escribe <span class="cmd-inline">OPTIONS</span> (<span class="key-inline">OP</span>) y entra en la pestaña <strong>Display</strong>.</li>
      <li>En <em>Crosshair size</em>, sube el valor al 100% si te gusta ver las líneas guía en toda la pantalla.</li>
      <li>En la pestaña <strong>Selection</strong>, <em>Pickbox size</em> controla el tamaño del cuadrado al seleccionar objetos.</li>
    </ul>

    <h3>Mini ejercicio: explora sin miedo</h3>
    <div class="lesson-step">
      <span class="lesson-num">1</span>
      <div class="lesson-body">
        <h4>Recorre las pestañas de la cinta</h4>
        <p>Abre cada pestaña (Inicio, Insertar, Anotar, Vista...) y pasa el mouse por los grupos para leer las descripciones.</p>
      </div>
    </div>
    <div class="lesson-step">
      <span class="lesson-num">2</span>
      <div class="lesson-body">
        <h4>Prueba los atajos de pantalla</h4>
        <p>Alterna con <span class="key-inline">Ctrl+0</span> y <span class="key-inline">Ctrl+1</span> para ver cómo cambia tu área de trabajo.</p>
      </div>
    </div>
    """,
]

ENRICH["nivel1-coordenadas"] = [
    """
    <h3>Entrada dinámica: escribe las coordenadas junto al cursor</h3>
    <p>Con la <strong>entrada dinámica</strong> activa (<span class="key-inline">F12</span>), los valores no se escriben en la línea de comandos sino en un pequeño recuadro junto al cursor. AutoCAD la usa por defecto.</p>
    <div class="lesson-step">
      <span class="lesson-num">1</span>
      <div class="lesson-body">
        <h4>Actívala</h4>
        <p>Pulsa <span class="key-inline">F12</span> o haz clic en el botón "DYNMODE" de la barra de estado. Escribe el comando <span class="cmd-inline">DYNMODE</span> y usa el valor <code>1</code>.</p>
      </div>
    </div>
    <div class="lesson-step">
      <span class="lesson-num">2</span>
      <div class="lesson-body">
        <h4>Escribe una coordenada relativa</h4>
        <p>Inicia el comando <span class="cmd-inline">LINE</span>, haz clic en cualquier punto y escribe <span class="cmd-inline">@50,30</span>. Verás aparecer el valor exacto junto al cursor antes de confirmar con Enter.</p>
      </div>
    </div>

    <h3>Ejemplo resuelto: dibujar una "L" por coordenadas</h3>
    <div class="lesson-step">
      <span class="lesson-num">1</span>
      <div class="lesson-body">
        <h4>Trazo horizontal</h4>
        <p><span class="cmd-inline">LINE</span> → primer punto <span class="cmd-inline">0,0</span> → segundo punto <span class="cmd-inline">@100,0</span>. Línea horizontal de 100 unidades.</p>
      </div>
    </div>
    <div class="lesson-step">
      <span class="lesson-num">2</span>
      <div class="lesson-body">
        <h4>Trazo vertical</h4>
        <p>Desde el punto final ahora escribe <span class="cmd-inline">@0,60</span>: subes 60 unidades en vertical sin moverte en X. Pulsa <span class="key-inline">Enter</span> para terminar el comando.</p>
      </div>
    </div>
    <div class="lesson-step">
      <span class="lesson-num">3</span>
      <div class="lesson-body">
        <h4>Misma figura con polares</h4>
        <p>Deshaz (<span class="key-inline">Ctrl+Z</span>) y repite usando polares: <span class="cmd-inline">@100&lt;0</span> y <span class="cmd-inline">@60&lt;90</span>. El resultado es el mismo: distancia y ángulo en lugar de X e Y.</p>
      </div>
    </div>
    <div class="callout">
      <span class="callout-title">Error común</span>
      <span>Olvidar el símbolo <span class="cmd-inline">@</span>: sin él, AutoCAD interpreta la coordenada como <strong>absoluta</strong> (medida desde el origen 0,0) y la figura termina en un lugar inesperado.</span>
    </div>

    <h3>Mini ejercicio: cuadrado por coordenadas</h3>
    <div class="lesson-step">
      <span class="lesson-num">1</span>
      <div class="lesson-body">
        <h4>Dibuja los cuatro lados</h4>
        <p>Con <span class="cmd-inline">LINE</span>, dibuja: <span class="cmd-inline">0,0</span> → <span class="cmd-inline">@50&lt;0</span> → <span class="cmd-inline">@50&lt;90</span> → <span class="cmd-inline">@50&lt;180</span> → cierra con <span class="cmd-inline">C</span> (cerrar) en la línea de comandos.</p>
      </div>
    </div>
    <div class="lesson-step">
      <span class="lesson-num">2</span>
      <div class="lesson-body">
        <h4>Comprueba lo dibujado</h4>
        <p>Usa <span class="cmd-inline">DIST</span> y haz clic en dos esquinas consecutivas: debe devolver exactamente 50.</p>
      </div>
    </div>
    """,
]

ENRICH["nivel1-archivos"] = [
    """<h3>Versiones y compatibilidad</h3>
<p>Cada versión de AutoCAD abre los <span class="cmd-inline">.DWG</span> de versiones anteriores, pero no al revés: un archivo guardado en la versión más nueva no se abre en una versión anterior. Por eso, cuando debas enviar un plano a un colega con un AutoCAD más antiguo, guárdalo con <span class="cmd-inline">SAVEAS</span> y elige el formato de versión que necesite (por ejemplo "AutoCAD 2018 Drawing").</p>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Pulsar <span class="key-inline">Ctrl+S</span> una sola vez al final del día. Guarda cada 10–15 minutos: la función <strong>deshacer</strong> solo conserva los últimos pasos en memoria hasta que cierras, y un fallo de energía los borra para siempre.</span>
</div>

<h3>Proteger tu trabajo</h3>
<ul>
  <li><strong>Repositorios/copias:</strong> guarda cada versión importante como <span class="cmd-inline">proyecto_v2.dwg</span> o en otra carpeta; los dibujos con historial son difíciles de sobrescribir por accidente.</li>
  <li><strong>Purgar antes de guardar:</strong> si el archivo pesa mucho, ejecuta <span class="cmd-inline">PURGE</span> y guarda de nuevo; se comprime.</li>
  <li><strong>E-mail/trucos:</strong> envía un .PDF o .DWF a clientes; solo comparte el .DWG cuando quieras que lo editen.</li>
</ul>

<h3>Mini ejercicio: guarda tu primera copia de seguridad</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Crea un dibujo y guárdalo</h4>
    <p>Dibuja una línea cualquiera, pulsa <span class="cmd-inline">SAVEAS</span> y guárdalo como <code>mi_primer_plano.dwg</code>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Comprueba el .BAK</h4>
    <p>Guarda de nuevo (<span class="key-inline">Ctrl+S</span>) y localiza en la carpeta el archivo <code>.bak</code>. Es tu respaldo automático: si el .DWG se corrompe, cambia el .BAK a extensión .DWG y ábrelo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Revisa el autoguardado</h4>
    <p>Escribe <span class="cmd-inline">SAVETIME</span> y pon el valor en <strong>10</strong> minutos. Ahora AutoCAD guardará la copia temporal .SV$ cada 10 minutos mientras trabajas.</p>
  </div>
</div>""",
]

ENRICH["nivel1-tipos-archivo"] = [
    """<h3>¿Cuál formato elegir?</h3>
<table class="table-cad">
  <thead><tr><th>Situación</th><th>Formato recomendado</th></tr></thead>
  <tbody>
    <tr><td>Tu propio trabajo diario</td><td><span class="cmd-inline">.DWG</span></td></tr>
    <tr><td>Comenzar un dibujo con la configuración habitual</td><td><span class="cmd-inline">.DWT</span> (plantilla rica en capas y estilos)</td></tr>
    <tr><td>Enviar a otro programa de CAD</td><td><span class="cmd-inline">.DXF</span></td></tr>
    <tr><td>Compartir para revisión sin que lo editen</td><td><span class="cmd-inline">.DWF</span> o <span class="cmd-inline">.PDF</span></td></tr>
    <tr><td>Entregar a imprenta o visualizador externo</td><td><span class="cmd-inline">.PDF</span></td></tr>
  </tbody>
</table>

<h3>Crear tu propia plantilla</h3>
<p>Vale la pena invertir 10 minutos: con los parámetros de <span class="cmd-inline">UNITS</span>, tus capas preferidas y un formato de hoja (layout) listo, guarda como <span class="cmd-inline">SAVEAS</span> → tipo <strong>AutoCAD Drawing Template (*.dwt)</strong>. Desde entonces cada dibujo nuevo empezará "con la casa ordenada".</p>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Confundir .DWF con .DXF. El primero es solo para <strong>ver y marcar</strong>; el segundo es un formato de intercambio <strong>editable</strong> entre programas CAD.</span>
</div>

<h3>Mini ejercicio: exporta un plano a DXF y PDF</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Exporta a DXF</h4>
    <p>Abre cualquier dibujo y usa <span class="cmd-inline">SAVEAS</span> → tipo "AutoCAD 2018 DXF". Ábrelo con doble clic: debe verse igual.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Exporta a PDF</h4>
    <p>Usa <span class="cmd-inline">PLOT</span> (o <span class="key-inline">Ctrl+P</span>) y elige "DWG to PDF" como impresora. Así envías un plano que cualquiera puede leer sin AutoCAD.</p>
  </div>
</div>""",
]

ENRICH["nivel1-zoom"] = [
    """<h3>Atajos que aceleran el día a día</h3>
<ul>
  <li><span class="key-inline">Ctrl + botón rueda</span> arrastrando: <strong>órbita/dinámico</strong> en 3D, en 2D hace pan rápido.</li>
  <li><span class="cmd-inline">ZOOM OBJECT</span> (<span class="cmd-inline">Z + O</span>): selecciona un objeto y lo centra en pantalla.</li>
  <li><span class="cmd-inline">DOBLECLICK en la rueda</span>: hace <strong>ZOOM EXTENTS</strong> automáticamente (muestra todo el dibujo).</li>
  <li>Al escribir <span class="cmd-inline">Z</span>, observa en la línea de comandos las opciones: <strong>E</strong> (extents), <strong>W</strong> (window), <strong>P</strong> (previous), <strong>A</strong> (all), <strong>O</strong> (object), <strong>D</strong> (dynamic).</li>
</ul>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>El zoom NUNCA modifica el dibujo: solo cambia la vista. Puedes acercarte y alejarte sin miedo; la geometría queda intacta.</span>
</div>

<h3>Mini ejercicio: navega una figura grande</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Aleja todo</h4>
    <p>Haz <span class="cmd-inline">Z + E</span> para ver el dibujo completo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Acércate con window</h4>
    <p>Haz <span class="cmd-inline">Z + W</span> y arrastra un rectángulo alrededor de una zona concreta; verás ese detalle ampliado.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Regresa</h4>
    <p>Pulsa <span class="cmd-inline">Z + P</span> varias veces para volver a las vistas anteriores y comprueba cómo AutoCAD recuerda tu historial de zoom.</p>
  </div>
</div>""",
]

# ----------------------------------------------------------------------------
# 3) Lecciones nuevas (contenido completo)
# ----------------------------------------------------------------------------
NEW_SECTIONS = {}

NEW_SECTIONS["nivel1-osnap-basico"] = """
<h2><span class="sec-num">N</span>Referencia a objetos (OSNAP) y rastreo</h2>
<p><strong>OSNAP</strong> (Object Snap) y <strong>OTrack</strong> (Object Snap Tracking) son dos ayudas que "enganchan" el cursor a puntos geométricos de los objetos que ya dibujaste: esquinas, puntos medios, centros de círculos, intersecciones, perpendiculares... Con ellos dejas de apuntar "a ojo" y dibujas sobre posiciones exactas.</p>

<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>SNAP (con rejilla) atrapa al cursor sobre una cuadrícula; OSNAP atrapa al cursor <strong>sobre los objetos</strong>. Son diferentes y se activan con teclas distintas (<span class="key-inline">F9</span> frente a <span class="key-inline">F3</span>).</span>
</div>

<h3>Modificadores de referencia más usados</h3>
<p>Cada referencia tiene un nombre y una abreviatura que puedes teclear directamente mientras dibujas:</p>
<table class="table-cad">
  <thead><tr><th>Modificador</th><th>Qué referencia</th><th>Ejemplo de uso</th></tr></thead>
  <tbody>
    <tr><td><span class="cmd-inline">END</span></td><td>Punto final de línea o arco</td><td>Continuar un muro desde una esquina.</td></tr>
    <tr><td><span class="cmd-inline">MID</span></td><td>Punto medio de un segmento</td><td>Colocar una división a la mitad de un muro.</td></tr>
    <tr><td><span class="cmd-inline">CEN</span></td><td>Centro de círculo, arco o elipse</td><td>Anexar una línea desde el centro de un círculo.</td></tr>
    <tr><td><span class="cmd-inline">QUA</span></td><td>Cuadrante (punto cardinal) de círculo/elipse</td><td>Dibujar un eje horizontal que cruce un cilindro.</td></tr>
    <tr><td><span class="cmd-inline">INT</span></td><td>Intersección de dos objetos</td><td>Unir el punto donde se cruzan dos líneas.</td></tr>
    <tr><td><span class="cmd-inline">PER</span></td><td>Punto perpendicular a un objeto</td><td>Bajar una perpendicular desde un punto a un muro.</td></tr>
    <tr><td><span class="cmd-inline">TAN</span></td><td>Punto tangente a círculo/arco</td><td>Dibujar una línea tangente a un círculo.</td></tr>
    <tr><td><span class="cmd-inline">NEA</span></td><td>Punto más cercano del objeto</td><td>Apoyar un texto cerca de una línea.</td></tr>
    <tr><td><span class="cmd-inline">NOD</span></td><td>Punto (nodo) insertado a mano</td><td>Referenciar un punto de división (DIVIDE/POINT).</td></tr>
    <tr><td><span class="cmd-inline">INS</span></td><td>Punto de inserción de un bloque o texto</td><td>Alinear un bloque sobre su punto base.</td></tr>
  </tbody>
</table>

<h3>Cómo activar y configurar las referencias</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Activa OSNAP</h4>
    <p>Pulsa <span class="key-inline">F3</span> o haz clic en "OSNAP" en la barra de estado. Cuando está encendido, verás un cuadrado de color flotando sobre cada punto que reconoces.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Elige qué referencias usar</h4>
    <p>Clic derecho sobre el botón OSNAP → <em>Ajustes (Drafting Settings)</em>. Marca solo las que usas: <strong>Endpoint, Midpoint, Center, Intersection, Quadrant</strong> son las 5 básicas.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Referencia puntual con la línea de comandos</h4>
    <p>Mientras estás en un comando escribe el modificador directamente: por ejemplo, al dibujar una línea teclea <span class="cmd-inline">MID</span> y AutoCAD buscará solo puntos medios, aunque los demás modificadores estén desactivados.</p>
  </div>
</div>

<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Activar <strong>todos</strong> los modificadores a la vez hace que el cursor "salte" entre demasiados puntos. Deja activos solo los que usas y activa el resto bajo demanda escribiendo el modificador.</span>
</div>

<h3>Rastreo de referencia a objetos (Object Snap Tracking)</h3>
<p>Con <span class="key-inline">F11</span> (OTrack) activado, AutoCAD dibuja líneas guía punteadas a partir de los puntos de referencia, para colocarte <strong>alineado</strong> con ellos sin dibujar una línea temporal.</p>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Activa OTrack</h4>
    <p>Pulsa <span class="key-inline">F11</span>. Activa también de antemano algoritmo Endpoint o Midpoint.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Alinea con una guía</h4>
    <p>Coloca el cursor sobre una esquina (sin pinchar) y aléjalo lentamente: aparecerá una línea punteada. Aléjala hasta coincidir con la guía de otra esquina y aparece una <strong>X</strong>: ese punto está alineado con ambas.</p>
  </div>
</div>

<h3>Ejemplo guiado: centro de un rectángulo sin calcular</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Dibuja un rectángulo</h4>
    <p>Comando <span class="cmd-inline">RECTANG</span>, primer punto <span class="cmd-inline">0,0</span>, opuesto <span class="cmd-inline">@200,140</span>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Pide los puntos medios de dos lados opuestos</h4>
    <p>Comando <span class="cmd-inline">LINE</span> → teclea <span class="cmd-inline">MID</span> y toca el lado izquierdo → teclea <span class="cmd-inline">MID</span> y toca el lado derecho. Has dibujado el eje horizontal exacto.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Coloca un círculo en el centro</h4>
    <p>Comando <span class="cmd-inline">CIRCLE</span> → teclea <span class="cmd-inline">INT</span> y pincha el cruce entre el eje y otra línea, por ejemplo con el eje vertical. Radio <span class="cmd-inline">30</span>.</p>
  </div>
</div>

<h3>Mini ejercicio: "encastre" de dos piezas</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Dibuja dos rectángulos separados</h4>
    <p><span class="cmd-inline">RECTANG</span> 0,0 → @100,60 ; y <span class="cmd-inline">RECTANG</span> a 150,10 → @100,60.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Une su punto medio por una línea</h4>
    <p><span class="cmd-inline">LINE</span> + <span class="cmd-inline">MID</span> del primer rectángulo + <span class="cmd-inline">MID</span> del segundo. Con <span class="cmd-inline">DIST</span> verifica el resultado: los dos centros quedan alineados.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Resumen</span>
  <span>OSNAP (<span class="key-inline">F3</span>) para puntos exactos de objetos, OTrack (<span class="key-inline">F11</span>) para alineaciones y la abreviatura del modificador para usos puntuales. Con estas tres herramientas dibujas sin medir nada dos veces.</span>
</div>
"""

NEW_SECTIONS["nivel1-gestion-dibujo"] = """
<h2><span class="sec-num">N</span>Deshacer, purgar y mantener tu dibujo</h2>
<p>Un dibujo poco cuidado se vuelve lento, pesado y propenso a errores. Los comandos de esta lección forman tu "kit de mantenimiento": deshacer sobre la marcha, quitar lo que sobra y reparar lo que se rompe.</p>

<h3>Deshacer y rehacer</h3>
<table class="table-cad">
  <thead><tr><th>Comando / Atajo</th><th>Qué hace</th></tr></thead>
  <tbody>
    <tr><td><span class="cmd-inline">U</span> / <span class="key-inline">Ctrl+Z</span></td><td>Deshace el último paso. Puedes repetirlo muchas veces.</td></tr>
    <tr><td><span class="cmd-inline">REDO</span> / <span class="key-inline">Ctrl+Y</span></td><td>Rehace lo que acabas de deshacer (si no hiciste nada intermedio).</td></tr>
    <tr><td><span class="cmd-inline">MREDO</span></td><td>Deshace/rehace varios pasos a la vez (pide un número o lista).</td></tr>
    <tr><td><span class="cmd-inline">UNDO</span></td><td>Versión extendida con opciones: marcar, pausa, inicio/fin, número de pasos.</td></tr>
  </tbody>
</table>
<p>Si acabas de cometer un error, no busques el comando que lo causó: <strong>deshaz y sigue</strong>. Abusar de deshacer es raro que ocurra; no temer usarlo te hace más rápido.</p>

<h3>Purgar los elementos sin usar</h3>
<p>Con el tiempo el dibujo acumula bloques, capas, estilos de cota, de texto o de tabla que ya no se utilizan. No se ven, pero inflan el archivo.</p>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Ejecuta PURGE</h4>
    <p>Teclea <span class="cmd-inline">PURGE</span> (<span class="key-inline">PU</span>). Marca <em>Purgar todo</em> y confirma con Sí a la pregunta de confirmar cada elemento.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Repite una vez</h4>
    <p>Algunos objetos dependen de otros; ejecuta <span class="cmd-inline">PURGE</span> una segunda vez para eliminar lo que quedó huerfano tras la primera pasada.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Consejo</span>
  <span>Purga <strong>antes</strong> de enviar un archivo por correo o subirlo: un DWG puede bajar de peso enormemente sin perder nada útil.</span>
</div>

<h3>Auditar y recuperar archivos</h3>
<table class="table-cad">
  <thead><tr><th>Comando</th><th>Qué hace</th><th>Cuándo usarlo</th></tr></thead>
  <tbody>
    <tr><td><span class="cmd-inline">AUDIT</span></td><td>Revisa el archivo y corrige errores internos de datos.</td><td>Si notas lentitud, geometría rara o mensajes de error.</td></tr>
    <tr><td><span class="cmd-inline">RECOVER</span></td><td>Abre un archivo dañado o que no quiere abrir, intentando repararlo.</td><td>Cuando un DWG no abre o AutoCAD avisa que está dañado.</td></tr>
    <tr><td><span class="cmd-inline">DWGPROPS</span></td><td>Muestra los metadatos del archivo (autor, título, comentarios).</td><td>Para documentar cada dibujo de tu proyecto.</td></tr>
    <tr><td><span class="cmd-inline">REGEN</span> / <span class="cmd-inline">REGENALL</span></td><td>Reconstruye la vista desde los datos del dibujo.</td><td>Cuando aparecen círculos "poligonales" o la vista se ve corrupta.</td></tr>
  </tbody>
</table>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Audita un archivo</h4>
    <p>Cierra el dibujo, teclea <span class="cmd-inline">AUDIT</span> y pulsa <span class="key-inline">Enter</span> ante la pregunta de corregir errores. Revisa el resumen que AutoCAD te devuelve en la línea de comandos.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Recupera un archivo que no abre</h4>
    <p>Con el programa sin el archivo cargado, escribe <span class="cmd-inline">RECOVER</span>, localiza el DWG y deja que AutoCAD lo repare. Guarda después con “Guardar como” un nuevo nombre.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Un archivo "corrompido" suele ser culpa de guardados interrumpidos o de copiarlo mientras aún se escribía. Ante la duda, recupera siempre desde la <strong>copia .BAK</strong> o el autoguardado antes de tocar el original.</span>
</div>

<h3>Reglas de oro del mantenimiento</h3>
<ul>
  <li>Ejecuta <span class="cmd-inline">PURGE</span> + <span class="cmd-inline">AUDIT</span> antes de cerrar un entregable.</li>
  <li>Guarda con <span class="cmd-inline">QSAVE</span> (<span class="key-inline">Ctrl+S</span>) cada pocos minutos.</li>
  <li>Mantén el autoguardado activo y copia tus .BAK a una carpeta de respaldo.</li>
  <li>Usa <strong>capas</strong> y nombres descriptivos desde el inicio: un archivo ordenado es un archivo reparable.</li>
</ul>

<h3>Mini ejercicio: protege una copia de trabajo</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Crea un dibujo sencillo y "ensúcialo"</h4>
    <p>Inserta un bloque de la biblioteca que no vayas a usar, dibuja un par de líneas y crea un estilo de cota que tampoco necesites.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Purgalos y compara el peso</h4>
    <p>Guarda el archivo, anota su tamaño; ejecuta <span class="cmd-inline">PURGE</span> + <span class="cmd-inline">AUDIT</span>, vuelve a guardar y mira el nuevo tamaño. Después localiza el archivo <span class="cmd-inline">.BAK</span> que se generó al lado de tu DWG.</p>
  </div>
</div>
"""

NEW_SECTIONS["nivel1-atajos-esenciales"] = """
<h2><span class="sec-num">N</span>Comandos y atajos esenciales del nivel 1</h2>
<p>AutoCAD premia al que escribe: conocer las teclas y los alias correctos hace que tus manos dejen el mouse para lo que de verdad lo necesitan. Esta lección resume lo esencial del nivel.</p>

<h3>Teclas de función (F1–F12)</h3>
<table class="table-cad">
  <thead><tr><th>Tecla</th><th>Alterna…</th></tr></thead>
  <tbody>
    <tr><td><span class="key-inline">F1</span></td><td>Ayuda contextual de AutoCAD.</td></tr>
    <tr><td><span class="key-inline">F3</span></td><td>Referencia a objetos OSNAP (puntos exactos de objetos).</td></tr>
    <tr><td><span class="key-inline">F7</span></td><td>Rejilla (GRID) — guía visual.</td></tr>
    <tr><td><span class="key-inline">F8</span></td><td>ORTO — restringe el cursor a horizontal/vertical.</td></tr>
    <tr><td><span class="key-inline">F9</span></td><td>Captura o forzado (SNAP) sobre la rejilla.</td></tr>
    <tr><td><span class="key-inline">F10</span></td><td>Rastreo polar (POLAR) — guías en ángulos (ej. 15°, 30°).</td></tr>
    <tr><td><span class="key-inline">F11</span></td><td>Rastreo de objetos (OTrack) — alineaciones con guías.</td></tr>
    <tr><td><span class="key-inline">F12</span></td><td>Entrada dinámica — coordenadas junto al cursor.</td></tr>
  </tbody>
</table>

<h3>Atajos generales de teclado</h3>
<table class="table-cad">
  <thead><tr><th>Atajo</th><th>Acción</th></tr></thead>
  <tbody>
    <tr><td><span class="key-inline">Ctrl+S</span></td><td>Guardar rápidamente (QSAVE).</td></tr>
    <tr><td><span class="key-inline">Ctrl+N</span></td><td>Nuevo dibujo (elige plantilla).</td></tr>
    <tr><td><span class="key-inline">Ctrl+O</span></td><td>Abrir un archivo.</td></tr>
    <tr><td><span class="key-inline">Ctrl+Z</span> / <span class="key-inline">Ctrl+Y</span></td><td>Deshacer / Rehacer.</td></tr>
    <tr><td><span class="key-inline">Esc</span></td><td>Cancelar el comando o selección actual.</td></tr>
    <tr><td><span class="key-inline">Enter</span></td><td>Aceptar; si no hay comando activo, repite el último utilizado.</td></tr>
    <tr><td><span class="key-inline">Espacio</span></td><td>Equivale a Enter en la línea de comandos.</td></tr>
    <tr><td><span class="key-inline">Clic derecho</span></td><td>Abre el menú contextual; durante un comando, entra en las opciones.</td></tr>
  </tbody>
</table>

<h3>Alias esenciales que ya conoces</h3>
<table class="table-cad">
  <thead><tr><th>Alias</th><th>Comando completo</th></tr></thead>
  <tbody>
    <tr><td><span class="cmd-inline">L</span></td><td>LINE — dibuja líneas.</td></tr>
    <tr><td><span class="cmd-inline">C</span></td><td>CIRCLE — dibuja círculos.</td></tr>
    <tr><td><span class="cmd-inline">REC</span></td><td>RECTANG — dibuja rectángulos.</td></tr>
    <tr><td><span class="cmd-inline">Z</span></td><td>ZOOM — gestiona la vista.</td></tr>
    <tr><td><span class="cmd-inline">P</span></td><td>PAN — desplaza la vista.</td></tr>
    <tr><td><span class="cmd-inline">E</span></td><td>ERASE — borra objetos.</td></tr>
    <tr><td><span class="cmd-inline">PU</span></td><td>PURGE — limpia elementos sin uso.</td></tr>
    <tr><td><span class="cmd-inline">OP</span></td><td>OPTIONS — opciones del programa.</td></tr>
  </tbody>
</table>

<h3>El hábito de escribir comandos</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Escribe y lee</h4>
    <p>Antes de pinchar, mira la línea de comandos: te dicta los pasos del comando y sus opciones entre corchetes.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Aprovecha las opciones con el menú contextual</h4>
    <p>Durante un comando, haz clic derecho para ver sus opciones (por ejemplo <em>Undo</em> dentro de LINE) sin soltar el flujo de trabajo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Entrena el reflejo Enter</h4>
    <p>Cuando termines de dibujar un comando, entérate de que <span class="key-inline">Enter</span> o <span class="key-inline">Espacio</span> repite el último comando: es de los atajos que más tiempo ahorra.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>No hace falta memorizar todo el diccionario de comandos. Basta dominar 15–20 alias de uso frecuente para moverte con soltura; el resto llega solo con la práctica.</span>
</div>

<h3>Mini ejercicio: ronda de comandos sin mouse</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Lanza cinco comandos seguidos</h4>
    <p>En un dibujo nuevo ejecuta por teclado: <span class="cmd-inline">L</span>, <span class="cmd-inline">C</span>, <span class="cmd-inline">REC</span>, <span class="cmd-inline">Z</span> (y opción <span class="cmd-inline">E</span>) y <span class="cmd-inline">PU</span>. Si con el cursor en blanco escribes <span class="key-inline">Espacio</span>, AutoCAD repite el último comando.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Combina con las teclas de función</h4>
    <p>Dibuja una línea con <span class="key-inline">F8</span> (ORTO) encendido y observa la diferencia con <span class="key-inline">F12</span> (dinámica) activa. Alterna <span class="key-inline">F7</span> para ver la rejilla aparecer y desaparecer.</p>
  </div>
</div>
"""

# ----------------------------------------------------------------------------
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
    next_btn = '<a href="../nivel-2-dibujo-2d/index.html" class="btn-cad-outline w-100 text-center d-block">Siguiente nivel <i class="bi bi-arrow-right"></i></a>'
    nav_next = """<a href="../nivel-2-dibujo-2d/index.html" class="nav-next">
            <span class="nav-label">Siguiente</span>
            <span class="nav-title">Siguiente nivel <i class="bi bi-arrow-right"></i></span>
          </a>"""
    page = f"""<!DOCTYPE html>
<html lang="es" data-theme="dark">
{build_head(f"Nivel {NUM} · {FULL_TITLE} — AutoCAD Guía", f"/paginas/{FOLDER}/index.html", LEVELS[1][4], include_3d=False, schema_name=SCHEMA_NAME, schema_desc=SCHEMA_DESC)}

<body>

<a href="#main-content" class="skip-link">Saltar al contenido principal</a>

{build_navbar(NUM)}

<header class="page-header" id="main-content">
  <div class="container container-xl">
    <p class="crumb"><a href="../../index.html">Inicio</a> / <a href="../../index.html#niveles">Niveles</a> / {FULL_TITLE}</p>
    <span class="eyebrow" data-i18n="lvl{NUM}.eyebrow">{EYEBROW}</span>
    <h1 data-i18n="lvl{NUM}.title">{FULL_TITLE}</h1>
    <p class="subtitle" data-i18n="lvl{NUM}.subtitle">{LEVELS[1][4]}</p>
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
    "nivel1-osnap-basico":      "nivel-1-fundamentos/coordenadas.html",
    "nivel1-gestion-dibujo":    "nivel-1-fundamentos/tipos-archivo.html",
    "nivel1-atajos-esenciales": "nivel-1-fundamentos/zoom.html",
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
                 '    "path": "Nivel 1 · Fundamentos"\n'
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
    src_67 = "const total = 67; // 9 + 15 + 13 + 16 + 14"
    dst_70 = "const total = 70; // 12 + 15 + 13 + 16 + 14"
    if src_67 in mj:
        mj = mj.replace(src_67, dst_70)
        write(mp, mj)
        print("main.js: total 67 -> 70")
    else:
        print("main.js: total 67 no encontrado (revisar)")


def update_index_label():
    ip = os.path.join(ROOT, "index.html")
    idx = read(ip)
    if "0 de 67 temas completados" in idx:
        idx = idx.replace("0 de 67 temas completados", "0 de 70 temas completados")
        write(ip, idx)
        print("index.html: label 67 -> 70")
    else:
        print("index.html: label 67 no encontrado (revisar)")


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