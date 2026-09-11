# -*- coding: utf-8 -*-
"""
build_level5_content.py
Enriquece el Nivel 5 (Avanzado / Experto):
  - Añade contenido nuevo (tablas de comandos, pasos paso a paso, callouts,
    atajos y mini ejercicios) a las 14 lecciones existentes.
  - Crea 3 lecciones nuevas: campos-tablas (campos y tablas de datos),
    georreferenciacion (coordenadas y mapas) y colaboracion (nube y AutoCAD Web).
  - Regenera las 17 páginas de lección y la portada index.html del nivel.
  - Actualiza search-index.js, sitemap.xml, main.js (total 82) e index.html.

Ejecutar desde la raíz:  python scripts/build_level5_content.py
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

FOLDER = "nivel-5-avanzado"
DST = os.path.join(ROOT, "paginas", FOLDER)
NUM = 5
TOTAL = 17
EYEBROW = LEVELS[5][3]
FULL_TITLE = LEVELS[5][2]
SCHEMA_NAME = LEVELS[5][5]
SCHEMA_DESC = LEVELS[5][6]


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
    ("nivel5-personalizacion",      "personalizacion.html",    "Personalización de la interfaz (CUI)",        "Personalización de la interfaz", "Crear espacios de trabajo y comandos propios con el editor de personalización (CUI)."),
    ("nivel5-autolisp",             "autolisp.html",           "AutoLISP y scripts básicos",                  "AutoLISP y scripts",            "Automatizar tareas repetitivas con scripts .scr y programas AutoLISP .lsp."),
    ("nivel5-estandares",           "estandares.html",         "Estándares CAD profesionales",                "Estándares CAD",                "Normas de capas, textos, acotación y archivos de dibujo en entornos profesionales."),
    ("nivel5-buenas-practicas",     "buenas-practicas.html",   "Buenas prácticas de dibujo profesional",      "Buenas prácticas",              "Flujos de trabajo limpios: orden, limpieza, copias de seguridad y versionado."),
    ("nivel5-campos-tablas",        "campos-tablas.html",      "Campos y tablas de datos",                    "Campos y tablas de datos",      "Campos dinámicos, tablas de AutoCAD y extracción de datos a Excel (DATAEXTRACTION)."),
    ("nivel5-integracion",          "integracion.html",        "Integración con otros programas",             "Integración con otros programas", "Conectar AutoCAD con Excel, SketchUp, Revit y otras aplicaciones de diseño."),
    ("nivel5-optimizacion",         "optimizacion.html",       "Optimización de archivos y solución de errores", "Optimización y solución de errores", "Reducir el peso del dibujo, purgar, auditar y resolver errores comunes."),
    ("nivel5-dynamo",               "dynamo.html",             "Dynamo para AutoCAD",                         "Dynamo para AutoCAD",           "Programación visual con nodos para crear geometría y automatizar el modelado."),
    ("nivel5-python",               "python.html",             "Automatización con Python (pyautocad)",       "Automatización con Python",     "Controlar AutoCAD desde Python con la librería pyautocad."),
    ("nivel5-bim",                  "bim.html",                "AutoCAD y BIM",                               "AutoCAD y BIM",                 "Cómo encaja AutoCAD en el flujo de información BIM y sus módulos verticales."),
    ("nivel5-interoperabilidad",    "interoperabilidad.html",  "Interoperabilidad CAD-BIM",                  "Interoperabilidad CAD-BIM",     "Formatos de intercambio (DXF, IFC, STEP, PDF...) y herramientas de conversión."),
    ("nivel5-georreferenciacion",   "georreferenciacion.html", "Georreferenciación y mapas",                  "Georreferenciación y mapas",    "Ubicar el dibujo en coordenadas reales y conectarlo con cartografía GIS."),
    ("nivel5-dynamic-blocks",       "dynamic-blocks.html",     "Bloques dinámicos (Dynamic Blocks)",          "Bloques dinámicos",             "Parámetros y acciones para crear bloques que se adaptan al instante."),
    ("nivel5-diseno-parametrico",   "diseno-parametrico.html", "Diseño paramétrico y restricciones",          "Diseño paramétrico",            "Restricciones geométricas y de cota para controlar la geometría con parámetros."),
    ("nivel5-cad-standards",        "cad-standards.html",      "Verificador de estándares CAD",               "Verificador de estándares",     "Contratar estándares .dws y comprobar que todo el dibujo los cumple."),
    ("nivel5-publish",              "publish.html",            "Publicación de planos y lotes (PUBLISH)",     "Publicación por lotes",         "Imprimir o exportar decenas de láminas en un solo lote."),
    ("nivel5-colaboracion",         "colaboracion.html",       "Colaboración en la nube y AutoCAD Web",       "Colaboración y nube",           "Compartir, editar y coordinar proyectos en la nube desde cualquier dispositivo."),
]

TOPIC_META = {t[0]: t for t in TOPICS}
FILE_TO_TOPIC = {t[1]: t[0] for t in TOPICS}

# ----------------------------------------------------------------------------
# 2) Contenido de enriquecimiento para las lecciones existentes
# ----------------------------------------------------------------------------
# Cada fragmento se inserta antes del botón "Marcar tema como visto".
ENRICH = {}

ENRICH["nivel5-personalizacion"] = [
"""<h3>Qué puedes personalizar en dos minutos</h3>
<table class="table-cad">
  <thead><tr><th>Elemento</th><th>Dónde personalizarlo</th></tr></thead>
  <tbody>
    <tr><td>Acceso rápido (Quick Access)</td><td>Botón derecho en la barra superior → <strong>Personalizar</strong>.</td></tr>
    <tr><td>Barra de herramientas/ribbon</td><td><span class="cmd-inline">CUI</span> → pestaña <em>Personalizar interfaz</em> → pestañas y paneles.</td></tr>
    <tr><td>Atajos de teclado (alias)</td><td><span class="cmd-inline">CUI</span> → categoría <em>Teclas de acceso rápido</em> → asigna o modifica enseguida.</td></tr>
    <tr><td>Espacio de trabajo propio</td><td><span class="cmd-inline">CUI</span> → clic derecho sobre <em>Espacios de trabajo</em> → <strong>Nuevo</strong>.</td></tr>
    <tr><td>Paleta de herramientas</td><td>Cinta <em>Vista → Paletas → Herramientas</em>, arrastra tus comandos favoritos.</td></tr>
  </tbody>
</table>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Crea tu espacio de trabajo</h4>
    <p>Con <span class="cmd-inline">CUI</span>, duplica <em>Modelado 3D</em> y actívalo como base.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Agrega tus paneles</h4>
    <p>Arrastra los paneles de cinta que uses a diario y quita los que estorben.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Guarda el perfil</h4>
    <p>Exporta el archivo de personalización (<em>.cuix</em>) y compártelo con tu equipo para que todos trabajen igual.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Personalizar sin exportar el .cuix: cualquier actualización o cambio de instalación borra tus ajustes. Guarda una copia del perfil y restáurala con <em>Transferir</em> (pestaña en <span class="cmd-inline">CUI</span>).</span>
</div>""",
]

ENRICH["nivel5-autolisp"] = [
"""<h3>Carga y ejecuta tu primera automatización</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Escribe un script de texto</h4>
    <p>Crea un archivo de texto con líneas de comandos terminadas en Enter, p. ej. <span class="cmd-inline">LINE</span>, coordenadas y <span class="cmd-inline">C</span> para cerrar. Guárdalo con extensión <em>.scr</em>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Ejecútalo</h4>
    <p>Con <span class="cmd-inline">SCRIPT</span> selecciona el .scr y AutoCAD reproduce cada línea como si la escribieras tú.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Carga una función AutoLISP</h4>
    <p>Con <span class="cmd-inline">APPLOAD</span> carga el archivo .lsp y escribe el nombre de la función para ejecutarla.</p>
  </div>
</div>
<h3>Funciones AutoLISP de uso diario</h3>
<table class="table-cad">
  <thead><tr><th>Función</th><th>Qué hace</th></tr></thead>
  <tbody>
    <tr><td><span class="cmd-inline">(getpoint)</span></td><td>Pide un punto al usuario.</td></tr>
    <tr><td><span class="cmd-inline">(getdist)</span></td><td>Pide una distancia.</td></tr>
    <tr><td><span class="cmd-inline">(getreal)</span></td><td>Pide un número real.</td></tr>
    <tr><td><span class="cmd-inline">(command "RECTANG" p1 p2)</span></td><td>Ejecuta un comando con argumentos.</td></tr>
    <tr><td><span class="cmd-inline">(if ... )</span></td><td>Condicional para decisiones dentro de la rutina.</td></tr>
  </tbody>
</table>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>En <span class="cmd-inline">(command ...)</span> todo lo literal va entre <strong>comillas</strong> dentro del paréntesis. Olvidarlas produce errores de "too few arguments". Compara: <span class="cmd-inline">(command "LINE" p1 p2)</span> funciona; <span class="cmd-inline">(command LINE p1)</span> no.</span>
</div>""",
]

ENRICH["nivel5-estandares"] = [
"""<h3>Capas y textos con normas claras</h3>
<table class="table-cad">
  <thead><tr><th>Convención</th><th>Ejemplo</th></tr></thead>
  <tbody>
    <tr><td>Capas por función</td><td><em>A-Muros</em>, <em>A-Puertas</em>, <em>A-Acotacion</em> (prefijo que agrupa disciplina).</td></tr>
    <tr><td>Capas por color/tipo de línea</td><td><em>A-Muros-ELEM</em> con color y tipo de línea definidos en la capa, no a nivel de objeto.</td></tr>
    <tr><td>Texto por altura</td><td>Texto 2.5 mm para notas, 3.5 mm para etiquetas, 5 mm para títulos (escala 1:100).</td></tr>
    <tr><td>Acotación normada</td><td>Estilo de cota único con flechas 2.5, texto centrado y formato decimal.</td></tr>
  </tbody>
</table>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Crea la plantilla base</h4>
    <p>En un dibujo nuevo define capas, estilos de texto, de cota y de tablas con la norma de tu oficina.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Guárdala como plantilla</h4>
    <p>Guarda el archivo con extensión <em>.dwt</em> en la carpeta de plantillas para tenerla en <span class="cmd-inline">NUEVO</span>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Guárdala como estándar</h4>
    <p>Guárdala también como <em>.dws</em> y actívala con <span class="cmd-inline">STANDARDS</span> para que el verificador la controle.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Una norma no es un capricho: cuando todos usan las mismas capas y estilos, un compañero abre tu dibujo y sabe al instante dónde está cada cosa. La norma <strong>se aplica a medida que dibujas</strong>, no al final.</span>
</div>""",
]

ENRICH["nivel5-buenas-practicas"] = [
"""<h3>Rutina diaria de un dibujo limpio</h3>
<table class="table-cad">
  <thead><tr><th>Práctica</th><th>Qué evita</th></tr></thead>
  <tbody>
    <tr><td>Trabajar "sobre 0" y mantener el origen</td><td>Dibujos desplazados fuera de la lámina y referencias rotas.</td></tr>
    <tr><td>Capillas y estilos con nombre claro</td><td>Capas "Capa1", "Defpoints" llenas de basura.</td></tr>
    <tr><td>Escrutinio periódico con PURGE</td><td>Bloques y estilos fantasma que inflan el archivo.</td></tr>
    <tr><td>Guardar versiones numeradas</td><td>Perder semanas de trabajo en un archivo corrupto.</td></tr>
    <tr><td>Simbolos como bloques, nunca dibujados sueltos</td><td>Inconsistencias y redibujos manuales.</td></tr>
  </tbody>
</table>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Antes de empezar</h4>
    <p>Carga la plantilla .dwt de la oficina y confirma unidades y capa "0" activa.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Mientras dibujas</h4>
    <p>Dibuja usando capas, bloqueos y referencias externas; evita dibujar dos veces lo mismo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Antes de entregar</h4>
    <p>Ejecuta <span class="cmd-inline">PURGE</span> (hasta la raíz), <span class="cmd-inline">AUDIT</span> y revisa la lista de capas; guarda como versión "final" y en PDF.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Guardar "FINAL", "FINAL2", "FINAL_REAL": sin versionado claro no sabrás cuál está vigente. Usa una estructura de carpetas por fecha y un número de versión, no apodos.</span>
</div>""",
]

ENRICH["nivel5-integracion"] = [
"""<h3>Llevar datos de AutoCAD a Excel</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Lanza la extracción</h4>
    <p>Con <span class="cmd-inline">DATAEXTRACTION</span> se abre el asistente para crear una tabla de datos del dibujo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Elige qué extraer</h4>
    <p>Selecciona bloques o atributos (por ejemplo puertas: nombre, dimensiones, cantidad).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>El destino</h4>
    <p>Escoge insertar la tabla en el dibujo o <strong>exportarla a .xls</strong> para seguir trabajando en Excel.</p>
  </div>
</div>
<h3>Integraciones típicas</h3>
<table class="table-cad">
  <thead><tr><th>Programa</th><th>Cómo integra</th></tr></thead>
  <tbody>
    <tr><td><strong>Excel</strong></td><td><span class="cmd-inline">DATALINK</span> vincula tablas en vivo; DATAEXTRACTION exporta información.</td></tr>
    <tr><td><strong>SketchUp</strong></td><td>Importa/exporta DXF o 3DS para bocetos de presentación.</td></tr>
    <tr><td><strong>Revit</strong></td><td>Flujo BIM: IFC / DWG convertido como base topológica.</td></tr>
    <tr><td><strong>GIS</strong></td><td><span class="cmd-inline">MAPCONNECT</span> conecta capas SHP/WMS y exporta geometría con datos.</td></tr>
  </tbody>
</table>
<div class="callout">
  <span class="callout-title">Consejo</span>
  <span>Cuando integres con otro programa, usa <strong>formatos neutros</strong> (DXF, IFC, PDF) salvo que el flujo admita DWG nativo. Así evitas incompatibilidades de versión entre aplicaciones.</span>
</div>""",
]

ENRICH["nivel5-optimizacion"] = [
"""<h3>Limpieza completa en 5 pasos</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Audita el archivo</h4>
    <p>Con <span class="cmd-inline">AUDIT</span> corrige errores de estructura del DWG al abrirlo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Purgar hasta la raíz</h4>
    <p>Con <span class="cmd-inline">PURGE</span> marca todo, y repite el comando hasta que diga "nada que purgar".</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Revisa la lista de escalas</h4>
    <p>Con <span class="cmd-inline">SCALELISTEDIT</span> quita las escalas de anotación fantasma (las que se acumulan al abrir XREF).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Guarda en la versión actual</h4>
    <p>Con <span class="cmd-inline">SAVEAS</span> guarda el DWG 2018 o superior; evita versiones viejas que inflan el archivo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">5</span>
  <div class="lesson-body">
    <h4>Mide el resultado</h4>
    <p>Compara el peso final: una limpieza completa suele reducir el archivo a menos de la mitad.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Borrar capas con <strong>contenido real</strong> solo para "adelgazar" el archivo. Si una capa tiene objetos visibles, vacía primero el contenido correcto; la purga de capas vacías no quita nada útil.</span>
</div>""",
]

ENRICH["nivel5-dynamo"] = [
"""<h3>Conceptos clave de Dynamo</h3>
<table class="table-cad">
  <thead><tr><th>Concepto</th><th>En Dynamo</th></tr></thead>
  <tbody>
    <tr><td>Programa</td><td>Un <em>grafo</em>: una red de nodos conectados por cables.</td></tr>
    <tr><td>Dato</td><td>Cada nodo recibe entradas y devuelve salidas.</td></tr>
    <tr><td>Iteración</td><td>Un nodo se repite sobre listas de datos (borde a borde).</td></tr>
    <tr><td>Geometría</td><td>Puntos, curvas, superficies generadas y devueltas a AutoCAD.</td></tr>
  </tbody>
</table>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Abre Dynamo</h4>
    <p>Escribe <span class="cmd-inline">DYNAMO</span> o usa el panel de <em>Empaquetado/Aplicaciones</em> en la cinta.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Prueba un nodo</h4>
    <p>Busca el nodo <em>Point.ByCoordinates</em>, conéctalo a un <em>Number Slider</em> y pulsa <strong>Ejecutar</strong>: verás llegar el punto a AutoCAD.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Automatiza la serie</h4>
    <p>Con <em>Sequence</em> e <em>Instance</em> repite el punto sobre una lista para generar una cuadrícula al instante.</p>
  </div>
</div>
<div class="callout">
  <span class="callout-title">Aprendizaje</span>
  <span>No necesitas programar para empezar: copia el grafo de ejemplo, cambia un Number Slider y mira qué pasa. La lógica "flujo de datos" se aprende jugando; luego lo aplicas en patrones de fachada, topografías y generación paramétrica.</span>
</div>""",
]

ENRICH["nivel5-python"] = [
"""<h3>Primer script con pyautocad</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Instala la librería</h4>
    <p>Desde la consola: <span class="cmd-inline">pip install pyautocad</span>.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Conecta con AutoCAD</h4>
    <p>Escribe <span class="cmd-inline">a = Autocad()</span> en Python; si AutoCAD está abierto, se conecta por COM.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Dibuja una línea</h4>
    <p>Con <span class="cmd-inline">a.model.AddLine(p1, p2)</span> creas geometría directamente en el dibujo activo.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Automatiza en bucle</h4>
    <p>Un <span class="cmd-inline">for</span> sobre una lista de puntos genera una serie de líneas o círculos sin tocar AutoCAD.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>La conexión COM exige que AutoCAD tenga el componente <em>ActiveX</em> (Activación COM) y que ambos procesos puedan hablarse. Si salta "no se pudo conectar", cierra AutoCAD, ejecuta Python como administrador y vuelve a abrirlo.</span>
</div>""",
]

ENRICH["nivel5-bim"] = [
"""<h3>De AutoCAD a BIM en pasos</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Modela con disciplina</h4>
    <p>Dibuja cada disciplina en capas y bloques bien nombrados para que los datos se transfieran limpios.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Exporta al formato BIM</h4>
    <p>Con <span class="cmd-inline">EXPORT</span> genera <em>IFC</em> (o DXF 3D) para OpenBIM/Revit y herramienta de coordinación.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Verifica con los modelos</h4>
    <p>Importa el IFC de vuelta o cruza con el modelo de MEP/estructura en un visor IFC para detectar choques.</p>
  </div>
</div>
<table class="table-cad">
  <thead><tr><th>Término BIM</th><th>Qué significa</th></tr></thead>
  <tbody>
    <tr><td>LOD</td><td>Nivel de desarrollo: cuánta información tiene la geometría en cada fase.</td></tr>
    <tr><td>IFC</td><td>Formato estándar abierto de intercambio de modelos.</td></tr>
    <tr><td>Clash detection</td><td>Detección de interferencias entre disciplinas.</td></tr>
    <tr><td>CDE</td><td>Entorno común de datos: la nube donde se comparte el proyecto.</td></tr>
  </tbody>
</table>
<div class="callout">
  <span class="callout-title">Tendencia</span>
  <span>AutoCAD no es una herramienta BIM, pero es la fábrica de geometría de muchos proyectos: la clave está en <strong>cómo nombras y exportas</strong> para que el modelo llegue bien a Revit, ArchiCAD o Navisworks.</span>
</div>""",
]

ENRICH["nivel5-interoperabilidad"] = [
"""<h3>Convierte entre formatos sin sorpresas</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Trae un PDF</h4>
    <p>Con <span class="cmd-inline">PDFIMPORT</span> importa planos escaneados como geometría vectorial editable; revisa escala al insertar.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Saca un neutral</h4>
    <p>Con <span class="cmd-inline">EXPORT</span> elige <em>DXF</em> (universal 2D/3D), <em>STEP</em> (sólidos para mecánica) o <em>IFC</em> (BIM).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Comprueba el resultado</h4>
    <p>Abre el archivo exportado en el programa destino y valida medida, capas y geometría antes de entregar.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Convertir curvas complejas a <strong>IGES/STEP</strong> y luego a DXF: cada salto puede deformar splines NURBS y erosionar precisión. Reduce conversiones al mínimo y guarda el DWG original como respaldo para siempre.</span>
</div>""",
]

ENRICH["nivel5-dynamic-blocks"] = [
"""<h3>Mini ejercicio: una puerta que se estira</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Entra al editor</h4>
    <p>Con <span class="cmd-inline">BEDIT</span> abre la definición del bloque (por ejemplo, una puerta básica).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Añade el parámetro</h4>
    <p>En la paleta <em>Definición de bloque</em>, inserta <strong>Parámetro</strong> → <em>Lineal</em> sobre la línea base de la puerta.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Conecta la acción</h4>
    <p>Añade la <strong>Acción</strong> <em>Estirar</em> y selecciona la parte de la geometría que debe moverse.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Guarda y prueba</h4>
    <p>Con <span class="cmd-inline">BSAVE</span>/<span class="cmd-inline">BCLOSE</span> cierra el editor e inserta el bloque: aparecerá el pinzamiento de estirado.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Crear la acción antes de definir su <em>conjunto de selección</em> completo. Si seleccionas medio bloque, el estirado deforma la mitad. Vuelve a <span class="cmd-inline">BACTIONSET</span> y re-selecciona toda la geometría afectada.</span>
</div>""",
]

ENRICH["nivel5-diseno-parametrico"] = [
"""<h3>Mini ejercicio: una cota que conduce la pieza</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Dibuja el perfil</h4>
    <p>Con <span class="cmd-inline">RECTANG</span> crea un rectángulo cualquiera.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Fija la geometría</h4>
    <p>Con <span class="cmd-inline">GEOMCONSTRAINT</span> añade <em>Horizontal/Vertical</em> a los lados y <em>Fijar</em> a un vértice.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Acota como parámetro</h4>
    <p>Con <span class="cmd-inline">DIMCONSTRAINT</span> convierte el ancho en una cota paramétrica (echa nombre y valor, p. ej. <em>ancho=100</em>).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Cambia el valor</h4>
    <p>En <span class="cmd-inline">PARAMETERS</span> edita <em>ancho</em> a 150 y mira cómo el rectángulo se actualiza solo.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Sobre-restreñir: dos cotas que fijan lo mismo o restricciones redundantes dejan el modelo sin grados de libertad y cualquier propuesta falla. Si el dibujo "se traba" al cambiar un valor, elimina restricciones con <span class="cmd-inline">DELCONSTRAINT</span> y empieza con las justas.</span>
</div>""",
]

ENRICH["nivel5-cad-standards"] = [
"""<h3>Contratar y verificar estándares</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Crea el estándar</h4>
    <p>Guarda tu plantilla (capas, estilos, tipos de línea) como <em>.dws</em>: es el archivo que será la norma.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Conecta el dibujo</h4>
    <p>Con <span class="cmd-inline">STANDARDS</span> añade el .dws a la lista de estándares del dibujo actual.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Verifica</h4>
    <p>Con <span class="cmd-inline">CHECKSTANDARDS</span> el comparador lista las violaciones y puedes corregirlas a una o corregir en lotes.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Hazlo automático</h4>
    <p>En <span class="cmd-inline">STANDARDS</span> marca <em>Comprobar automáticamente al abrir</em> para detectar infracciones desde el primer día.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Flujo en la oficina</span>
  <span>El .dws debe vivir en una carpeta compartida de solo lectura: si cada usuario guarda su copia, unos corren contra una norma vieja y el chequeo es inútil. El administrador actualiza la plantilla y la norma juntas.</span>
</div>""",
]

ENRICH["nivel5-publish"] = [
"""<h3>Arma el lote de impresión</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Abre la publicación</h4>
    <p>Con <span class="cmd-inline">PUBLISH</span> se abre el gestor de impresión por lotes.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Define las láminas</h4>
    <p>Añade las presentaciones (pasos de impresión) que quieres: elige "Archivo actual" y marca las láminas.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Ordena y configura</h4>
    <p>Reordena las láminas como irán en el plano y revisa que cada una tenga su plot style correcto.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Exporta en un clic</h4>
    <p>Elige salida a PDF o impresora y pulsa <em>Publicar</em>: se genera el lote completo en orden.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Publicar el lote sin revisar reconejo de una lámina: un plot style mal asignado "mancha" todo el plano. Guarda el lote con <em>Guardar lista de pasos de impresión</em> (.dsd) para reutilizarlo y auditar antes de producir.</span>
</div>""",
]

# ----------------------------------------------------------------------------
# 3) Lecciones nuevas (contenido completo)
# ----------------------------------------------------------------------------
NEW_SECTIONS = {}

NEW_SECTIONS["nivel5-campos-tablas"] = """
<h2><span class="sec-num">N</span>Campos y tablas de datos</h2>
<p>Los <strong>campos</strong> muestran texto que se actualiza solo (áreas, fechas, propiedades del bloque), y las <strong>tablas</strong> organizan datos como una hoja de cálculo dentro del dibujo. Combinados con <span class="cmd-inline">DATAEXTRACTION</span>, AutoCAD se convierte en un gestor de listados: contar puertas, sumar áreas o generar inventarios sin teclear nada.</p>

<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Un campo no es texto fijo: es una <em>fórmula viva</em>. Cambia la geometría y el campo se refresca. Una tabla de datos tampoco es estática: puede leer de Excel (DATALINK) o de la propiedad de los objetos del dibujo.</span>
</div>

<h3>Campos: texto que se actualiza solo</h3>
<table class="table-cad">
  <thead><tr><th>Comando / elemento</th><th>Qué hace</th></tr></thead>
  <tbody>
    <tr><td><span class="cmd-inline">FIELD</span></td><td>Inserta un campo (área, perímetro, fecha, autor, nombre de bloque...).</td></tr>
    <tr><td>Clic derecho → <em>Actualizar campos</em></td><td>Refresca todos los campos del dibujo tras un cambio.</td></tr>
    <tr><td>Campo en el texto del bloque</td><td>Numeración de puertas que se recalcula sola.</td></tr>
  </tbody>
</table>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Inserta un campo de área</h4>
    <p>Con <span class="cmd-inline">TEXT</span>/<span class="cmd-inline">MTEXT</span> crea un texto y, al escribirlo, pulsa <span class="cmd-inline">FIELD</span> y elige <em>Objeto</em> → área de una polilínea.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Actualízalo</h4>
    <p>Después de cambiar la polilínea, pulsa <span class="cmd-inline">REA</span> o clic derecho → <em>Actualizar campos</em> para que el número cambie solo.</p>
  </div>
</div>
<h3>Tablas y extracción de datos</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Crea una tabla</h4>
    <p>Con <span class="cmd-inline">TABLE</span> (o <span class="cmd-inline">TABLE</span> desde la cinta <em>Anotar</em>) dibuja una tabla con cabecera y celdas.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Vincula a Excel</h4>
    <p>Con <span class="cmd-inline">DATALINK</span> crea un enlace a una hoja de cálculo: la tabla dibujada refleja en vivo los valores del archivo .xlsx.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Extrae el inventario</h4>
    <p>Con <span class="cmd-inline">DATAEXTRACTION</span> el asistente recorre bloques y atributos y genera el listado (cantidad, referencias, dimensiones) como tabla o .xls.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Actualiza la tabla</h4>
    <p>Clic derecho sobre la tabla → <em>Actualizar tabla de datos</em> para volver a calcular tras cada cambio del dibujo.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Insertar un campo de área sobre una polilínea abierta: AutoCAD reporta el área cerrada proyectada o cero. Verifica que la polilínea sea cerrada (<span class="cmd-inline">PEDIT</span> → <span class="cmd-inline">C</span>) antes de confiar en el campo.</span>
</div>
<h3>Mini ejercicio: listado de puertas al instante</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Inserta bloques con atributos</h4>
    <p>Asegúrate de que tus puertas son bloques con atributos (<em>REFERENCIA</em>, <em>DIMENSION</em>).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Extrae</h4>
    <p>Con <span class="cmd-inline">DATAEXTRACTION</span> selecciona el bloque de puerta y sus atributos.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Coloca la tabla</h4>
    <p>Inserta el resultado como tabla en la lámina: cada puerta de tu plano aparece con su referencia y medida.</p>
  </div>
</div>
"""

NEW_SECTIONS["nivel5-georreferenciacion"] = """
<h2><span class="sec-num">N</span>Georreferenciación y mapas</h2>
<p><strong>Georreferenciar</strong> es dar a tu dibujo coordenadas reales: latitud/longitud o UTM de la zona del proyecto. Con <span class="cmd-inline">GEOGRAPHICLOCATION</span> AutoCAD ubica el modelo sobre el planeta (visible en la vista 3D), y con <span class="cmd-inline">MAPCONNECT</span> puedes cargar capas GIS (SHP, WMS) y exportar tu geometría a cartografía.</p>

<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Un dibujo con coordenadas reales se combina con mapas, se contrasta con levantamientos topográficos y sirve a otros equipos (GIS, urbanismo, topografía) sin re-procesar. Un dibujo "a mano" no tiene dónde encajar con el mundo.</span>
</div>

<h3>Ubicar el proyecto en coordenadas reales</h3>
<table class="table-cad">
  <thead><tr><th>Herramienta</th><th>Qué hace</th></tr></thead>
  <tbody>
    <tr><td><span class="cmd-inline">GEOGRAPHICLOCATION</span></td><td>Asigna latitud/longitud al dibujo y ofrece un mapa de fondo.</td></tr>
    <tr><td><span class="cmd-inline">GEO</span></td><td>Muestra/oculta la barra de localización geográfica.</td></tr>
    <tr><td><span class="cmd-inline">MAPCONNECT</span></td><td>Conecta fuentes SHP, WFS, WMS y tablas GIS.</td></tr>
    <tr><td><span class="cmd-inline">MAPIMPORT</span> / <span class="cmd-inline">MAPEXPORT</span></td><td>Importa/exporta capas con sus datos de atributos.</td></tr>
  </tbody>
</table>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Ubica el dibujo</h4>
    <p>Con <span class="cmd-inline">GEOGRAPHICLOCATION</span> indica el lugar (ciudad o coordenadas) y define el punto de inserción sobre tu plano.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Carga un mapa de fondo</h4>
    <p>En <span class="cmd-inline">GEOGRAPHICLOCATION</span> activa el mapa; se coloca detrás del proyecto para contrastar manzanas, calles y colindancias.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Conecta una capa GIS</h4>
    <p>Con <span class="cmd-inline">MAPCONNECT</span> añade un SHP de parcelas o de redes: cada objeto trae sus atributos (código, área).</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Exporta tu geometría con datos</h4>
    <p>Con <span class="cmd-inline">MAPEXPORT</span> guarda tu dibujo en SHP junto con los campos que eliges; el programa GIS lo abre con esa información.</p>
  </div>
</div>
<h3>Sistemas de coordenadas que debes reconocer</h3>
<table class="table-cad">
  <thead><tr><th>Sistema</th><th>Qué es</th></tr></thead>
  <tbody>
    <tr><td>Lat/Long (WGS84)</td><td>Coordenadas geográficas en grados, usado por GPS y mapas web.</td></tr>
    <tr><td>UTM</td><td>Coordenadas métricas por zonas de 6 grados; el estándar en topografía local.</td></tr>
    <tr><td>ZONA UTM local</td><td>La clave: tu zona (p. ej. 18S) define el datum y la unidad; usarla mal desplaza el dibujo decenas de metros.</td></tr>
  </tbody>
</table>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Combinar el datum del dibujo con el del mapa: si tu DWG está en UTM y el mapa en WGS84, todo se desvía. Define el sistema de coordenadas del dibujo al ubicarlo y usa siempre el mismo en la capa de fondo.</span>
</div>
"""

NEW_SECTIONS["nivel5-colaboracion"] = """
<h2><span class="sec-num">N</span>Colaboración en la nube y AutoCAD Web</h2>
<p>El trabajo CAD moderno no vive solo en la máquina local: <strong>guardar en la nube</strong>, <strong>compartir vistas</strong> y <strong>editar desde el navegador</strong> forman parte del flujo diario. AutoCAD Web y aplicaciones móviles permiten abrir, revisar, acotar y enviar un DWG desde cualquier dispositivo, y las referencias externas por URL mantienen el equipo sincronizado.</p>

<div class="callout">
  <span class="callout-title">Idea clave</span>
  <span>Colaborar no es solo "pasar el archivo por mail": es tener <strong>una única fuente de verdad</strong> (la nube), versiones claras y la capacidad de revisar el dibujo sin instalar AutoCAD. Menos archivos duplicados, menos versiones perdidas.</span>
</div>

<h3>Compartir y revisar sin instalar nada</h3>
<table class="table-cad">
  <thead><tr><th>Herramienta</th><th>Qué hace</th></tr></thead>
  <tbody>
    <tr><td>Autodesk Docs / Autodesk Web</td><td>Alojan DWG, personas lo abren desde el navegador o móvil.</td></tr>
    <tr><td><span class="cmd-inline">SHARE</span> (Design Share)</td><td>Crea un enlace temporal para que alguien vea y acote el dibujo sin cuenta ni instalación.</td></tr>
    <tr><td>Guardado en nube</td><td>DWG en OneDrive/Drive con versado automático.</td></tr>
    <tr><td>XREF por URL</td><td>Referencias externas que se cargan de la nube y se actualizan solas.</td></tr>
  </tbody>
</table>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Guarda en la nube</h4>
    <p>Configura la carpeta local sincronizada (OneDrive/Drive) y guarda el proyecto ahí; cada guardado crea una versión recuperable.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Comparte la vista</h4>
    <p>Con <span class="cmd-inline">SHARE</span> genera un enlace de Design Share: el destinatario ve el dibujo 3D/2D en el navegador y puede añadir comentarios anclados.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Edita desde el navegador</h4>
    <p>En AutoCAD Web abre el archivo, marcas capas, acotas y envías correcciones sin abrir el escritorio.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">4</span>
  <div class="lesson-body">
    <h4>Sincroniza XREF por URL</h4>
    <p>Enlaza las XREF desde la nube para que todos vean la misma base actualizada al abrir.</p>
  </div>
</div>
<div class="callout warn">
  <span class="callout-title">Error común</span>
  <span>Compartir por correo archivos DWG con XREF vinculadas a rutas locales: el destinatario abre el dibujo "hueco". Publica las XREF en una carpeta compartida o usa rutas relativas/URL antes de enviar.</span>
</div>
<h3>Mini ejercicio: revisa un plano desde el móvil</h3>
<div class="lesson-step">
  <span class="lesson-num">1</span>
  <div class="lesson-body">
    <h4>Sube el DWG</h4>
    <p>Guarda el archivo en la carpeta sincronizada y sube una copia a Autodesk Web/Drive.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">2</span>
  <div class="lesson-body">
    <h4>Acota en el móvil</h4>
    <p>Desde la app abre el DWG, súbete a una cota y comprueba una medida sobre el terreno con la cámara.</p>
  </div>
</div>
<div class="lesson-step">
  <span class="lesson-num">3</span>
  <div class="lesson-body">
    <h4>Envía la corrección</h4>
    <p>Crea un comentario anclado en el punto observado; el equipo del escritorio lo ve marcado al abrir archivo.</p>
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
    next_btn = '<a href="../comandos.html" class="btn-cad-outline w-100 text-center d-block">Diccionario de comandos <i class="bi bi-arrow-right"></i></a>'
    nav_next = """<a href="../comandos.html" class="nav-next">
            <span class="nav-label">Siguiente</span>
            <span class="nav-title">Diccionario de comandos <i class="bi bi-arrow-right"></i></span>
          </a>"""
    page = f"""<!DOCTYPE html>
<html lang="es" data-theme="dark">
{build_head(f"Nivel {NUM} · {FULL_TITLE} — AutoCAD Guía", f"/paginas/{FOLDER}/index.html", LEVELS[5][4], include_3d=False, schema_name=SCHEMA_NAME, schema_desc=SCHEMA_DESC)}

<body>

<a href="#main-content" class="skip-link">Saltar al contenido principal</a>

{build_navbar(NUM)}

<header class="page-header" id="main-content">
  <div class="container container-xl">
    <p class="crumb"><a href="../../index.html">Inicio</a> / <a href="../../index.html#niveles">Niveles</a> / {FULL_TITLE}</p>
    <span class="eyebrow" data-i18n="lvl{NUM}.eyebrow">{EYEBROW}</span>
    <h1 data-i18n="lvl{NUM}.title">{FULL_TITLE}</h1>
    <p class="subtitle" data-i18n="lvl{NUM}.subtitle">{LEVELS[5][4]}</p>
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
    "nivel5-campos-tablas":        "nivel-5-avanzado/buenas-practicas.html",
    "nivel5-georreferenciacion":   "nivel-5-avanzado/interoperabilidad.html",
    "nivel5-colaboracion":         "nivel-5-avanzado/publish.html",
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
                 '    "path": "Nivel 5 · Avanzado"\n'
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
    src_79 = "const total = 79; // 12 + 18 + 16 + 19 + 14"
    dst_82 = "const total = 82; // 12 + 18 + 16 + 19 + 17"
    if src_79 in mj:
        mj = mj.replace(src_79, dst_82)
        write(mp, mj)
        print("main.js: total 79 -> 82")
    else:
        print("main.js: total 79 no encontrado (revisar)")


def update_index_label():
    ip = os.path.join(ROOT, "index.html")
    idx = read(ip)
    if "0 de 79 temas completados" in idx:
        idx = idx.replace("0 de 79 temas completados", "0 de 82 temas completados")
        write(ip, idx)
        print("index.html: label 79 -> 82")
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