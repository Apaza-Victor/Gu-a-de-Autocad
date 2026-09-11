#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_new_lessons.py
Añade 14 lecciones nuevas repartidas en los niveles y aplica mejoras de UI:
  - Nivel 1:  configurar-espacio-trabajo
  - Nivel 2:  crear-capas, configurar-capas, cambiar-tipo-linea, escalar-bloques,
              agrupar-objetos, texturas-bloques, anadir-hatch, configurar-cotas,
              leyendas, limites-unidades, wblock-biblioteca
  - Nivel 3:  importar-exportar, zapatas-machones, muros-detalle,
              planos-estructurales
  - Nivel 5:  scripts-automatizacion

El contenido de cada lección se lee de los fragmentos en scripts/lessons_data/.
Además:
  - Actualiza cada portada index.html (TOC, tarjetas, totales).
  - Convierte las autoevaluaciones (.quiz-section) en contenedores desplegables
    que por defecto están contraídos.
  - Actualiza search-index.js, sitemap.xml, main.js (total 99) e index.html.

Ejecutar desde la raíz del repositorio:  python scripts/add_new_lessons.py
"""
import os
import re
import sys

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
sys.path.insert(0, SCRIPTS)

from build_level_folders import (  # noqa: E402
    BASE_URL, read, write, strip_tags,
    build_head, build_navbar, build_footer, build_scripts, build_end_block, LEVELS,
)

NEW_TOTAL = {1: 13, 2: 29, 3: 20, 4: 19, 5: 18}
TOTAL_GLOBAL = sum(NEW_TOTAL.values())  # 99

LEVEL_PARAMS = {}
for num, (folder, name, full, eyebrow, head_desc, schema_name, schema_desc) in LEVELS.items():
    LEVEL_PARAMS[num] = (folder, name, full, eyebrow, schema_name, schema_desc)

PATH = {num: os.path.join(ROOT, "paginas", LEVEL_PARAMS[num][0]) for num in NEW_TOTAL}

PATH_LABEL = {
    1: "Nivel 1 · Fundamentos",
    2: "Nivel 2 · Dibujo 2D",
    3: "Nivel 3 · Organización",
    4: "Nivel 4 · Modelado 3D",
    5: "Nivel 5 · Avanzado",
}


def indent(text, n):
    pad = " " * n
    return "\n".join((pad + ln if ln.strip() else ln) for ln in text.split("\n"))


# ----------------------------------------------------------------------------
# Catálogo de lecciones nuevas (el body se lee de scripts/lessons_data/)
# ----------------------------------------------------------------------------
FRAGMENTS = os.path.join(SCRIPTS, "lessons_data")

LESSON_CATALOG = [
    # Nivel 1
    dict(num=1, dt="nivel1-espacio-trabajo", file="configurar-espacio-trabajo.html",
         title="Configurar el espacio de trabajo", label="Configurar el espacio de trabajo",
         desc="Personalizar la cinta, los espacios de trabajo y el entorno para dibujar como un profesional.",
         anchor="configuracion.html", frag="nivel1-configurar-espacio-trabajo.html"),
    # Nivel 2 (después de capas)
    dict(num=2, dt="nivel2-crear-capas", file="crear-capas.html",
         title="Crear, renombrar y eliminar capas", label="Crear y eliminar capas",
         desc="Crear, renombrar, reordenar y eliminar capas de forma segura, con trucos de productividad.",
         anchor="capas.html", frag="nivel2-crear-capas.html"),
    dict(num=2, dt="nivel2-configurar-capas", file="configurar-capas.html",
         title="Configurar capas: color, tipo de línea y estados", label="Configurar capas",
         desc="Configurar color, tipo de línea, grosor, transparencia y estados (On/Off, Freeze, Lock) de cada capa.",
         anchor="capas.html", frag="nivel2-configurar-capas.html"),
    # Nivel 2 (después de precisión)
    dict(num=2, dt="nivel2-limites-unidades", file="limites-unidades.html",
         title="Límites y unidades del dibujo", label="Límites y unidades",
         desc="Configurar las unidades (UNITS) y los límites (LIMITS) antes de dibujar para que todo escale bien.",
         anchor="precision.html", frag="nivel2-limites-unidades.html"),
    # Nivel 2 (después de bloques)
    dict(num=2, dt="nivel2-escalar-bloques", file="escalar-bloques.html",
         title="Escalar bloques", label="Escalar bloques",
         desc="Escalar bloques con SCALE, escala por referencia y escala no uniforme al insertar.",
         anchor="bloques.html", frag="nivel2-escalar-bloques.html"),
    dict(num=2, dt="nivel2-agrupar-objetos", file="agrupar-objetos.html",
         title="Agrupar objetos: GROUP y grupos con nombre", label="Agrupar objetos (GROUP)",
         desc="Agrupar objetos y bloques con nombre mediante GROUP, y solucionar los problemas típicos al agrupar.",
         anchor="bloques.html", frag="nivel2-agrupar-objetos.html"),
    dict(num=2, dt="nivel2-texturas-bloques", file="texturas-bloques.html",
         title="Texturas de imagen en bloques", label="Texturas en bloques",
         desc="Añadir texturas de imagen a bloques con IMAGEATTACH y materiales para que se vean realistas.",
         anchor="bloques.html", frag="nivel2-texturas-bloques.html"),
    dict(num=2, dt="nivel2-wblock-biblioteca", file="wblock-biblioteca.html",
         title="WBLOCK y bibliotecas de bloques", label="WBLOCK y bibliotecas",
         desc="Guardar bloques como archivos .DWG con WBLOCK y crear bibliotecas reutilizables de símbolos.",
         anchor="bloques.html", frag="nivel2-wblock-biblioteca.html"),
    # Nivel 2 (después de acotación)
    dict(num=2, dt="nivel2-configurar-cotas", file="configurar-cotas.html",
         title="Configurar estilos de cota", label="Configurar cotas",
         desc="Crear y ajustar estilos de cota: DIMSTYLE, escala, precisión, flechas, texto y unidades.",
         anchor="acotacion.html", frag="nivel2-configurar-cotas.html"),
    # Nivel 2 (después de texto)
    dict(num=2, dt="nivel2-leyendas", file="leyendas.html",
         title="Crear leyendas de plano", label="Leyendas de plano",
         desc="Crear leyendas y simbología de plano con bloques, MTEXT y tablas profesionales.",
         anchor="texto.html", frag="nivel2-leyendas.html"),
    # Nivel 2 (después de hatch)
    dict(num=2, dt="nivel2-anadir-hatch", file="anadir-hatch.html",
         title="Añadir sombreados (Hatch) personalizados", label="Añadir Hatch",
         desc="Añadir patrones de sombreado nuevos a AutoCAD desde archivos .pat y aplicarlos en tus planos.",
         anchor="hatch.html", frag="nivel2-anadir-hatch.html"),
    # Nivel 2 (después de tipos de línea)
    dict(num=2, dt="nivel2-cambiar-tipo-linea", file="cambiar-tipo-linea.html",
         title="Cambiar el tipo de línea de un objeto", label="Cambiar el tipo de línea",
         desc="Cambiar el tipo de línea de varias formas: Propiedades, MATCHPROP, LINETYPE y propiedades de capa.",
         anchor="lineas.html", frag="nivel2-cambiar-tipo-linea.html"),
    # Nivel 3 (después de etransmit)
    dict(num=3, dt="nivel3-importar-exportar", file="importar-exportar.html",
         title="Importar y exportar planos", label="Importar y exportar",
         desc="Importar y exportar planos entre formatos: DWG, DXF, PDF y referencias externas.",
         anchor="etransmit.html", frag="nivel3-importar-exportar.html"),
    # Nivel 3 (después de cajetines)
    dict(num=3, dt="nivel3-zapatas-machones", file="zapatas-machones.html",
         title="Zapatas, machones y cimentaciones", label="Zapatas y machones",
         desc="Qué son las zapatas y los machones (columnas de amarre) y sus medidas típicas en construcción.",
         anchor="cajetines.html", frag="nivel3-zapatas-machones.html"),
    dict(num=3, dt="nivel3-muros-detalle", file="muros-detalle.html",
         title="Muros y detalles constructivos", label="Muros y detalles constructivos",
         desc="Tipos de muro, espesores habituales y cómo dibujar detalles constructivos a escala.",
         anchor="cajetines.html", frag="nivel3-muros-detalle.html"),
    dict(num=3, dt="nivel3-planos-estructurales", file="planos-estructurales.html",
         title="Planos estructurales", label="Planos estructurales",
         desc="Qué incluye un juego de planos estructurales: plantas, cimentación, rejillas, armado y simbología.",
         anchor="cajetines.html", frag="nivel3-planos-estructurales.html"),
    # Nivel 5 (después de autolisp)
    dict(num=5, dt="nivel5-scripts-automatizacion", file="scripts-automatizacion.html",
         title="Scripts de automatización (.SCR)", label="Scripts de automatización",
         desc="Automatizar tareas repetitivas con scripts .SCR: crear capas, imprimir en lote y estandarizar la revisión.",
         anchor="autolisp.html", frag="nivel5-scripts-automatizacion.html"),
]


def lesson_bodies():
    bodies = {}
    for lesson in LESSON_CATALOG:
        path = os.path.join(FRAGMENTS, lesson["frag"])
        if not os.path.exists(path):
            raise SystemExit("Falta el fragmento: " + path)
        bodies[lesson["dt"]] = read(path).rstrip()
    return bodies


BODIES = lesson_bodies()


# ----------------------------------------------------------------------------
# Utilidades de análisis de las páginas existentes
# ----------------------------------------------------------------------------

def parse_index_cards(html):
    """Devuelve la lista ordenada de lecciones existentes de la portada: [file,label,desc]."""
    pat = re.compile(
        r'<a href="([^"]+)" class="text-decoration-none">\s*'
        r'<div class="level-card">\s*'
        r'<div class="level-index">\d+</div>\s*'
        r'<span class="level-tag">Tema \d+</span>\s*'
        r'<h3>(.*?)</h3>\s*'
        r'<p>(.*?)</p>', re.S)
    out = []
    for m in pat.finditer(html):
        out.append([m.group(1), strip_tags(m.group(2)), strip_tags(m.group(3))])
    return out


def parse_toc_items(html):
    """Devuelve los elementos de la lista TOC: [(href, data-toc, label)] en orden."""
    m = re.search(r'<ul class="toc-list">(.*?)</ul>', html, re.S)
    if not m:
        return []
    items = []
    for li in re.finditer(
            r'<li><a href="([^"]+)" data-toc="([^"]*)"><span class="toc-check"></span>\s*(.*?)\s*</a></li>',
            m.group(1), re.S):
        items.append((li.group(1), li.group(2), li.group(3).strip()))
    return items


def find_div_end(html, i):
    """Devuelve el índice justo después del </div> que cierra el <div> que empieza en i."""
    depth = 0
    j = i
    tag_re = re.compile(r'<div\b|</div\s*>')
    while j < len(html):
        mch = tag_re.search(html, j)
        if not mch:
            return None
        if mch.group(0).startswith("</"):
            depth -= 1
            if depth == 0:
                return mch.end()
        else:
            depth += 1
        j = mch.end()
    return None


def ordered_lessons(num):
    """Lista ordenada final de lecciones del nivel: [dict(file,label,desc,dt,new)]."""
    html = read(os.path.join(PATH[num], "index.html"))
    cards = parse_index_cards(html)
    existing = {c[0] for c in cards}
    ordered = []
    for file, label, desc in cards:
        dt = ""
        for lesson in LESSON_CATALOG:
            if lesson["num"] == num and lesson["file"] == file:
                dt = lesson["dt"]
                label = lesson["label"]
                desc = lesson["desc"]
                break
        ordered.append(dict(file=file, label=label, desc=desc, dt=dt, new=False))
        for lesson in [l for l in LESSON_CATALOG if l["num"] == num and l["anchor"] == file]:
            if lesson["file"] not in existing:
                ordered.append(dict(file=lesson["file"], label=lesson["label"],
                                    desc=lesson["desc"], dt=lesson["dt"], new=True))
    return ordered


def toc_item(dt, fname, label):
    if dt:
        return f'<li><a href="{fname}" data-toc="{dt}"><span class="toc-check"></span> {label}</a></li>'
    return f'<li><a href="{fname}"><span class="toc-check"></span> {label}</a></li>'


def build_toc(ordered):
    lis = [toc_item(o["dt"], o["file"], o["label"]) for o in ordered]
    lis.append('<li><a href="index.html#autoevaluacion"><span class="toc-check"></span> Autoevaluación</a></li>')
    return "\n".join("            " + x for x in lis)


def build_cards(ordered):
    cards = []
    for idx, o in enumerate(ordered, 1):
        cards.append(
            '                    <div class="col-md-6 col-lg-4" data-aos="fade-up" data-aos-delay="%d">\n'
            '                      <a href="%s" class="text-decoration-none">\n'
            '                        <div class="level-card">\n'
            '                          <div class="level-index">%s</div>\n'
            '                          <span class="level-tag">Tema %d</span>\n'
            '                          <h3>%s</h3>\n'
            '                          <p>%s</p>\n'
            '                        </div>\n'
            '                      </a>\n'
            '                    </div>' % (((idx - 1) % 3) * 80, o["file"], str(idx).zfill(2), idx, o["label"], o["desc"]))
    return "\n".join(cards)


def make_quiz_collapsible(html):
    """Convierte cada .quiz-section en un acordeón contraído por defecto."""
    if 'class="quiz-toggle"' in html:
        return html
    pat = re.compile(r'(<section class="quiz-section"[^>]*>)(.*?)(</section\s*>?)', re.S)

    def rep(m):
        opening, inner, closing = m.group(1), m.group(2), m.group(3)
        idm = re.search(r'id="([^"]+)"', opening)
        sec_id = (idm.group(1) if idm else "autoevaluacion") + "-cuerpo"
        hm = re.search(r'<h2[^>]*>(.*?)</h2>', inner, re.S)
        if not hm:
            return m.group(0)
        title_html = hm.group(1).strip()
        inner_rest = inner[:hm.start()] + inner[hm.end():]
        nq = inner_rest.count('class="quiz-q"')
        sub = (f"{nq} preguntas de repaso" if nq else "Pon a prueba lo aprendido")
        return (opening + "\n"
                "  <button class=\"quiz-toggle\" type=\"button\" aria-expanded=\"false\" aria-controls=\"" + sec_id + "\">\n"
                "    <span class=\"quiz-toggle-icon\"><i class=\"bi bi-chevron-down\"></i></span>\n"
                "    <span class=\"quiz-toggle-title\">\n"
                "      <span class=\"quiz-toggle-title-main\">" + title_html + "</span>\n"
                "      <span class=\"quiz-toggle-title-sub\">" + sub + "</span>\n"
                "    </span>\n"
                "  </button>\n"
                "  <div class=\"quiz-collapse\" id=\"" + sec_id + "\">\n"
                + inner_rest.strip() +
                "\n  </div>\n</section>")

    return pat.sub(rep, html)


# ----------------------------------------------------------------------------
# Construcción de páginas de lección nuevas
# ----------------------------------------------------------------------------

def build_section(lesson, idx):
    folder, *_ = LEVEL_PARAMS[lesson["num"]]
    slug = lesson["file"].replace(".html", "")
    title = lesson["title"]
    body = BODIES[lesson["dt"]]
    body = body.replace("<span class=\"sec-num\">N</span>", "<span class=\"sec-num\">%d</span>" % (idx + 1))
    parts = [
        '<section id="%s" data-topic="%s">' % (slug, lesson["dt"]),
        '  <h2><span class="sec-num">%d</span>%s</h2>' % (idx + 1, title),
        indent(body, 2),
        '<button class="mark-done-btn"><i class="bi bi-check-circle"></i> Marcar tema como visto</button>',
        "</section>",
    ]
    return "\n".join(parts)


def build_lesson_page(lesson, idx, ordered):
    num = lesson["num"]
    folder, name, full, eyebrow, schema_name, schema_desc = LEVEL_PARAMS[num]
    total = NEW_TOTAL[num]
    section = build_section(lesson, idx)
    toc = build_toc(ordered)

    prev_t = ordered[idx - 1] if idx > 0 else None
    next_t = ordered[idx + 1] if idx + 1 < len(ordered) else None
    if prev_t:
        nav_prev = ('<a href="%s">\n'
                    '            <span class="nav-label">Anterior</span>\n'
                    '            <span class="nav-title"><i class="bi bi-arrow-left"></i> %s</span>\n'
                    '          </a>' % (prev_t["file"], prev_t["label"]))
    else:
        nav_prev = "<span></span>"
    if next_t:
        nav_next = ('<a href="%s" class="nav-next">\n'
                    '            <span class="nav-label">Siguiente</span>\n'
                    '            <span class="nav-title">%s <i class="bi bi-arrow-right"></i></span>\n'
                    '          </a>' % (next_t["file"], next_t["label"]))
    else:
        nav_next = ('<a href="index.html#autoevaluacion" class="nav-next">\n'
                    '            <span class="nav-label">Siguiente</span>\n'
                    '            <span class="nav-title">Autoevaluación <i class="bi bi-arrow-right"></i></span>\n'
                    '          </a>')

    head = build_head("%s · %s — AutoCAD Guía" % (lesson["title"], full),
                      "/paginas/%s/%s" % (folder, lesson["file"]),
                      lesson["desc"], include_3d=False,
                      schema_name=schema_name, schema_desc=schema_desc)

    page = """<!DOCTYPE html>
<html lang="es" data-theme="dark">
%s

<body>

<a href="#main-content" class="skip-link">Saltar al contenido principal</a>

%s

<header class="page-header" id="main-content">
  <div class="container container-xl">
    <p class="crumb"><a href="../../index.html">Inicio</a> / <a href="../../index.html#niveles">Niveles</a> / <a href="index.html">%s</a> / Tema %d</p>
    <span class="eyebrow" data-i18n="lvl%d.eyebrow">%s</span>
    <h1>%s</h1>
    <div class="level-progress-bar" data-level-prefix="nivel%d" data-level-total="%d"><div class="fill"></div></div>
    <p class="level-progress-label">0 de %d temas completados · 0%%</p>
  </div>
</header>

<div class="content-layout">
  <div class="container container-xl">
    <div class="row">

      <aside class="col-lg-3 mb-5 mb-lg-0">
        <div class="toc-sidebar">
          <h6 data-i18n="ui.inThisLevel">En este nivel</h6>
          <ul class="toc-list">
%s
          </ul>
          <hr style="border-color:var(--border-soft)" class="my-4">
          <a href="index.html" class="btn-cad-outline w-100 text-center d-block"><i class="bi bi-arrow-left"></i> Volver al índice</a>
        </div>
      </aside>

      <div class="col-lg-9">
        <article class="content-article">

%s

        </article>

        <nav class="level-nav">
          %s
          %s
        </nav>
      </div>
    </div>
  </div>
</div>

%s

%s

%s

</body>
</html>
""" % (head, build_navbar(num), name, idx + 1, num, eyebrow, lesson["title"], num, total,
       total, toc, indent(section, 10), nav_prev, nav_next, build_footer(),
       build_end_block(), build_scripts(num, include_quiz=False, include_babylon=False))
    write(os.path.join(PATH[num], lesson["file"]), page)
    print("  lección nueva:", lesson["file"])


# ----------------------------------------------------------------------------
# Actualización de las portadas index.html
# ----------------------------------------------------------------------------

def update_index(num, ordered):
    path = os.path.join(PATH[num], "index.html")
    html = read(path)
    total = NEW_TOTAL[num]
    folder = LEVEL_PARAMS[num][0]

    # 1) TOC
    m = re.search(r'<ul class="toc-list">(.*?)</ul>', html, re.S)
    if not m:
        raise SystemExit("TOC no encontrado en " + path)
    html = html[:m.start(1)] + build_toc(ordered) + html[m.end(1):]

    # 2) Tarjetas dentro de level-intro
    intro = re.search(r'<section class="level-intro">(.*?)</section>', html, re.S)
    if intro:
        row_start = html.find('<div class="row g-4 mt-1">', intro.start())
        if row_start != -1:
            row_end = find_div_end(html, row_start)
            if row_end:
                new_grid = ('            <div class="row g-4 mt-1">\n'
                            + build_cards(ordered) + '\n            </div>')
                html = html[:row_start] + new_grid + html[row_end:]

    # 3) Texto "Este nivel se divide en X temas"
    html = re.sub(r'Este nivel se divide en \d+ temas',
                  'Este nivel se divide en %d temas' % total, html)

    # 4) Total del progreso (barra + etiqueta) en la portada
    html = re.sub(r'data-level-total="\d+"', 'data-level-total="%d"' % total, html)
    html = re.sub(r'0 de \d+ temas completados · 0%',
                  '0 de %d temas completados · 0%%' % total, html)

    # 5) Quiz colapsable
    html = make_quiz_collapsible(html)

    write(path, html)
    print("  portada actualizada:", folder + "/index.html")


def update_all_level_totals():
    """Actualiza data-level-total y la etiqueta de progreso en TODAS las páginas de nivel."""
    for num, total in NEW_TOTAL.items():
        folder = LEVEL_PARAMS[num][0]
        for fname in sorted(os.listdir(PATH[num])):
            if not fname.endswith(".html"):
                continue
            p = os.path.join(PATH[num], fname)
            txt = read(p)
            txt = re.sub(r'data-level-total="\d+"', 'data-level-total="%d"' % total, txt)
            txt = re.sub(r'0 de \d+ temas completados', '0 de %d temas completados' % total, txt)
            write(p, txt)
        print("  totales de", folder, "->", total)


# ----------------------------------------------------------------------------
# Actualizaciones globales: search-index, sitemap, main.js, index.html
# ----------------------------------------------------------------------------

def update_search_index():
    path = os.path.join(ROOT, "assets", "js", "search-index.js")
    txt = read(path)
    inserted = 0
    # insertar de atrás hacia adelante para no descolocar los marcardores
    for lesson in reversed(LESSON_CATALOG):
        marker = "%s/%s" % (LEVEL_PARAMS[lesson["num"]][0], lesson["anchor"])
        own = '    "file": "%s/%s",' % (LEVEL_PARAMS[lesson["num"]][0], lesson["file"])
        if own in txt:
            continue
        needle = '    "file": "%s",' % marker
        if needle not in txt:
            raise SystemExit("No se encontró en search-index.js el ancla: " + marker)
        i = txt.index(needle)
        j = txt.index("  },", i) + len("  },")
        block = ('  {\n'
                 '    "type": "topic",\n'
                 '    "title": "%s",\n'
                 '    "description": "%s",\n'
                 '    "file": "%s/%s",\n'
                 '    "anchor": "",\n'
                 '    "path": "%s"\n'
                 '  },' % (lesson["title"], lesson["desc"],
                          LEVEL_PARAMS[lesson["num"]][0], lesson["file"],
                          PATH_LABEL[lesson["num"]]))
        txt = txt[:j] + "\n" + block + txt[j:]
        inserted += 1
    write(path, txt)
    print("search-index.js: entradas nuevas insertadas:", inserted)


def update_sitemap():
    urls = ["/", "/paginas/comandos.html", "/paginas/ejemplos-visuales.html",
            "/paginas/trucos.html", "/paginas/tips.html", "/paginas/recursos.html",
            "/paginas/faq.html", "/404.html"]
    for num in sorted(LEVEL_PARAMS):
        folder = LEVEL_PARAMS[num][0]
        urls.append("/paginas/%s/index.html" % folder)
        for fname in sorted(os.listdir(PATH[num])):
            if fname.endswith(".html") and fname != "index.html":
                urls.append("/paginas/%s/%s" % (folder, fname))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append("  <url>")
        lines.append("    <loc>%s%s</loc>" % (BASE_URL, u))
        lines.append("    <lastmod>2026-09-10</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append("    <priority>0.8</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    write(os.path.join(ROOT, "sitemap.xml"), "\n".join(lines) + "\n")
    print("sitemap.xml regenerado con", len(urls), "URLs")


def update_main_js_and_home():
    # main.js: total global de temas
    mp = os.path.join(ROOT, "assets", "js", "main.js")
    mj = read(mp)
    src = "const total = 96; // 13 + 27 + 20 + 19 + 17"
    dst = "const total = 99; // 13 + 29 + 20 + 19 + 18"
    if src in mj:
        mj = mj.replace(src, dst)
        write(mp, mj)
        print("main.js: total 96 -> 99")
    else:
        print("main.js: total 96 no encontrado (revisar)")

    # portada index.html: etiqueta de progreso global
    ip = os.path.join(ROOT, "index.html")
    idx = read(ip)
    if "0 de 96 temas completados" in idx:
        idx = idx.replace("0 de 96 temas completados", "0 de %d temas completados" % TOTAL_GLOBAL)
        write(ip, idx)
        print("index.html: etiqueta 96 ->", TOTAL_GLOBAL)
    else:
        print("index.html: etiqueta 96 no encontrada (revisar)")


def main():
    for num in sorted(NEW_TOTAL):
        ordered = ordered_lessons(num)
        assert len(ordered) == NEW_TOTAL[num], (num, len(ordered), NEW_TOTAL[num])
        # genera las páginas nuevas del nivel (también regenera si cambió su fragmento)
        for idx, o in enumerate(ordered):
            if o["dt"]:
                lesson = next(l for l in LESSON_CATALOG if l["dt"] == o["dt"])
                build_lesson_page(lesson, idx, ordered)
        update_index(num, ordered)
    update_all_level_totals()
    update_search_index()
    update_sitemap()
    update_main_js_and_home()
    print("OK · total global:", TOTAL_GLOBAL)


if __name__ == "__main__":
    main()