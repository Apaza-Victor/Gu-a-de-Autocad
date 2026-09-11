# -*- coding: utf-8 -*-
"""
build_level_folders.py
Reestructura las 5 páginas de nivel (paginas/nivel-N-slug.html) en subcarpetas:
  paginas/nivel-N-slug/index.html          -> portada del nivel
  paginas/nivel-N-slug/<tema>.html          -> una página por cada lección (data-topic)
El archivo antiguo nivel-N-slug.html queda como redirección (meta refresh).
Además:
  - actualiza enlaces en index.html, 404.html y paginas/*.html
  - regenera search-index.js (file + anchor y vacuos -> nueva ubicación)
  - actualiza main.js (determinePage, updateLevelProgress, initHomeProgress, TOC done)
  - regenera sitemap.xml

Ejecutar desde la raíz del repositorio:  python scripts/build_level_folders.py
"""
import re
import os
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGINAS = os.path.join(ROOT, "paginas")
BASE_URL = "https://apaza-victor.github.io/Gu-a-de-Autocad"

LEVELS = {
    1: ("nivel-1-fundamentos", "Fundamentos", "Fundamentos de AutoCAD", "Nivel 01 · Básico",
        "Qué es AutoCAD, instalación y licencias, interfaz de usuario, sistema de coordenadas y configuración inicial. Nivel 1 de la guía completa de AutoCAD.",
        "Nivel · Fundamentos de AutoCAD", "Qué es AutoCAD, instalación y licencias, interfaz, sistema de coordenadas y configuración inicial."),
    2: ("nivel-2-dibujo-2d", "Dibujo 2D", "Dibujo 2D", "Nivel 02 · Básico–Intermedio",
        "Herramientas de dibujo, modificación, precisión, capas, bloques, acotación, texto y sombreado en AutoCAD. Nivel 2 de la guía.",
        "Nivel · Dibujo 2D en AutoCAD", "Geometría, edición, precisión, capas, bloques, cotas, texto, hatch y splines."),
    3: ("nivel-3-organizacion", "Organización", "Organización y productividad", "Nivel 03 · Intermedio",
        "Espacio modelo vs presentación, ventanas gráficas y escalas, plantillas, impresión y exportación, Xref y atajos de teclado en AutoCAD. Nivel 3 de la guía.",
        "Nivel · Organización y productividad en AutoCAD", "Espacio modelo vs papel, viewports, plantillas, impresión, Xref, estilos de trazado y campos."),
    4: ("nivel-4-modelado-3d", "Modelado 3D", "Modelado 3D", "Nivel 04 · Avanzado",
        "Navegación 3D, sólidos básicos, operaciones booleanas, extrusión, revolución, barrido, solevación, edición de sólidos y render básico en AutoCAD. Nivel 4 de la guía.",
        "Nivel · Modelado 3D en AutoCAD", "Sólidos, booleanos, extrusión, mallas, superficies NURBS, renderizado y análisis."),
    5: ("nivel-5-avanzado", "Experto", "Nivel experto", "Nivel 05 · Experto",
        "Personalización de AutoCAD, AutoLISP, estándares CAD profesionales, buenas prácticas e integración con otros programas. Nivel 5 de la guía.",
        "Nivel · AutoCAD nivel experto", "CUI, AutoLISP, estándares CAD, integración, Dynamo, Python, BIM y optimización."),
}

NEXT_FOLDER = {
    1: "nivel-2-dibujo-2d",
    2: "nivel-3-organizacion",
    3: "nivel-4-modelado-3d",
    4: "nivel-5-avanzado",
}
NEXT_LABEL = {
    1: "Siguiente nivel",
    2: "Siguiente nivel",
    3: "Siguiente nivel",
    4: "Siguiente nivel",
    5: "Diccionario de comandos",
}


# ----------------------------------------------------------------------------
# utilidades
# ----------------------------------------------------------------------------

def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, content):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def extract_blocks(body):
    """Devuelve cada <section>...</section> de nivel superior."""
    parts = []
    tag_re = re.compile(r"<(/?)\s*section\b")
    depth = 0
    start = None
    for m in tag_re.finditer(body):
        if m.group(1) == "":
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0 and start is not None:
                parts.append(body[start:m.end()])
                start = None
    return parts


def opening_attrs(block):
    m = re.search(r"<section\b([^>]*?)>", block, re.S)
    attrs = {"id": "", "class": "", "data-topic": ""}
    if not m:
        return attrs
    tag = m.group(1)
    for key in attrs:
        mm = re.search(key + r'\s*=\s*"([^"]*)"', tag)
        if mm:
            attrs[key] = mm.group(1)
    return attrs


def h2_info(block):
    m = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.S)
    if not m:
        return "", ""
    inner = re.sub(r'<span class="sec-num">.*?</span>', "", m.group(1), flags=re.S)
    i18n = ""
    mi = re.search(r'data-i18n="([^"]+)"', inner)
    if mi:
        i18n = mi.group(1)
    text = re.sub(r"<[^>]+>", "", inner)
    text = re.sub(r"\s+", " ", text).strip()
    return text, i18n


def first_paragraph(block):
    m = re.search(r"<p(?![^>]*class=['\"][^'\"]*quiz)[^>]*>(.*?)</p>", block, re.S)
    if not m:
        return ""
    text = re.sub(r"<[^>]+>", "", m.group(1))
    text = re.sub(r"\s+", " ", text).strip()
    return text[:160] + ("…" if len(text) > 160 else "")


def strip_tags(text):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text)).strip()


def rewrite_paginas_links(html, into_folder):
    """Convierte enlaces a documentos de paginas/ según si están dentro de una subcarpeta."""
    pref = "../" if into_folder else ""
    for page in ["comandos", "ejemplos-visuales", "trucos", "tips", "recursos", "faq"]:
        html = html.replace(f'href="{page}.html"', f'href="{pref}{page}.html"')
    for num, (folder, *_rest) in LEVELS.items():
        html = html.replace(f'href="{folder}.html"', f'href="{pref}{folder}/index.html"')
    return html


def transform_nav_footer(text):
    """Reescribe enlaces de navbar/footer de una página de paginas/ a la subcarpeta del nivel."""
    text = text.replace('"../index.html"', '"../../index.html"')
    text = re.sub(r'(?<=["\'])\.\./assets/', '../../assets/', text)
    for num, (folder, *_rest) in LEVELS.items():
        text = text.replace(f'href="{folder}.html"', f'href="../{folder}/index.html"')
    for page in ["comandos", "ejemplos-visuales", "trucos", "tips", "recursos", "faq"]:
        text = text.replace(f'href="{page}.html"', f'href="../{page}.html"')
    return text


# ----------------------------------------------------------------------------
# constructores de fragmentos
# ----------------------------------------------------------------------------

def build_head(title, canonical_path, description, include_3d=False, schema_name=None, schema_desc=None):
    url = BASE_URL + canonical_path
    schema = {
        "@context": "https://schema.org",
        "@type": "Course",
        "name": schema_name or title,
        "description": schema_desc or description,
        "provider": {"@type": "Organization", "name": "AutoCAD Guía", "sameAs": BASE_URL + "/"},
        "inLanguage": "es",
        "hasCourseInstance": {
            "@type": "CourseInstance",
            "courseMode": "online",
            "learningResourceType": "tutorial",
            "inLanguage": "es",
        },
    }
    extra_css = '<link rel="stylesheet" href="../../assets/css/3d.css">\n' if include_3d else ""
    return f"""<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="AutoCAD Guía">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{BASE_URL}/assets/img/social-preview.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{BASE_URL}/assets/img/social-preview.svg">
<meta name="description" content="{description}">

<link rel="icon" type="image/svg+xml" href="../../assets/img/autocad-2.svg">

<link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.11.3/font/bootstrap-icons.min.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700;800&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
<link rel="stylesheet" href="../../assets/css/style.css">
<link rel="stylesheet" href="../../assets/css/responsive.css">
{extra_css}  <script type="application/ld+json">
  {json.dumps(schema, ensure_ascii=False, indent=2)}
  </script>
</head>"""


def build_navbar(active_level):
    drop = []
    for num, (folder, name, *_rest) in LEVELS.items():
        active = ' active' if num == active_level else ""
        drop.append(f'            <li><a class="dropdown-item{active}" href="../{folder}/index.html">Nivel {num} · {name}</a></li>')
    return f"""<nav class="navbar navbar-cad navbar-expand-lg">
  <div class="container container-xl">
    <a class="navbar-brand brand-cad" href="../../index.html">
      <img class="brand-logo" src="../../assets/img/autocad-2.svg" alt="AutoCAD">
      <span>AutoCAD<small class="d-block" data-i18n-html="brand.sub">Guía · Teoría &amp; Práctica</small></span>
    </a>
    <div class="d-flex align-items-center gap-2 nav-actions order-lg-last">
      <button class="icon-btn" id="searchToggle" title="Buscar" data-i18n-title="ui.search"><i class="bi bi-search"></i></button>
      <button class="icon-btn" id="themeToggle" title="Cambiar tema" data-i18n-title="ui.theme"><i class="bi bi-moon-stars"></i></button>
      <button class="navbar-toggler icon-btn border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navCad">
        <i class="bi bi-list fs-4"></i>
      </button>
    </div>

    <div class="collapse navbar-collapse" id="navCad">
      <ul class="navbar-nav mx-auto mt-3 mt-lg-0">
        <li class="nav-item"><a class="nav-link nav-link-cad" href="../../index.html" data-i18n="nav.home">Inicio</a></li>
        <li class="nav-item dropdown">
          <a class="nav-link nav-link-cad dropdown-toggle active" href="#" data-bs-toggle="dropdown" data-i18n="nav.levels">Niveles</a>
          <ul class="dropdown-menu">
{chr(10).join(drop)}
          </ul>
        </li>
        <li class="nav-item"><a class="nav-link nav-link-cad" href="../comandos.html" data-i18n="nav.commands">Comandos</a></li>
        <li class="nav-item"><a class="nav-link nav-link-cad" href="../ejemplos-visuales.html" data-i18n="nav.visual">Visuales</a></li>
        <li class="nav-item"><a class="nav-link nav-link-cad" href="../trucos.html" data-i18n="nav.tips">Trucos</a></li>
        <li class="nav-item"><a class="nav-link nav-link-cad" href="../tips.html" data-i18n="nav.tutorials">Tips</a></li>
        <li class="nav-item"><a class="nav-link nav-link-cad" href="../recursos.html" data-i18n="nav.resources">Recursos</a></li>
        <li class="nav-item"><a class="nav-link nav-link-cad" href="../faq.html" data-i18n="nav.faq">FAQ</a></li>
      </ul>

      <div class="d-flex align-items-center gap-2 nav-actions-menu ms-lg-auto">
        <span class="coord-readout d-none d-lg-inline-flex">X: <span id="coordX">000.00</span>&nbsp; Y: <span id="coordY">000.00</span></span>
        <button class="lang-toggle" id="langToggle" title="Cambiar idioma" data-i18n-title="ui.lang">
          <i class="bi bi-translate lang-toggle-flag"></i>
          <span class="lang-toggle-text">EN</span>
        </button>
      </div>
    </div>
  </div>
</nav>"""


def build_footer():
    levels_li = []
    for num, (folder, name, *_rest) in LEVELS.items():
        levels_li.append(f'          <li><a href="../{folder}/index.html">{name}</a></li>')
    guide_li = [
        '          <li><a href="../comandos.html">Comandos</a></li>',
        '          <li><a href="../ejemplos-visuales.html">Ejemplos</a></li>',
        '          <li><a href="../trucos.html">Trucos</a></li>',
        '          <li><a href="../tips.html" data-i18n="nav.tutorials">Tips</a></li>',
        '          <li><a href="../recursos.html">Recursos</a></li>',
        '          <li><a href="../faq.html">FAQ</a></li>',
    ]
    return f"""<footer class="site-footer">
  <div class="container container-xl">
    <div class="row gy-4">
      <div class="col-lg-4">
        <div class="brand-cad mb-2"><img class="brand-logo" src="../../assets/img/autocad-2.svg" alt="AutoCAD"><span>AutoCAD Guía</span></div>
        <p data-i18n="footer.disclaimer">Contenido educativo independiente. No es un sitio oficial de Autodesk®; AutoCAD® es una marca registrada de Autodesk, Inc.</p>
      </div>
      <div class="col-6 col-lg-2">
        <h6 class="mono text-uppercase small text-muted-custom mb-3" data-i18n="footer.levels">Niveles</h6>
        <ul class="list-unstyled">
{chr(10).join(levels_li)}
        </ul>
      </div>
      <div class="col-6 col-lg-2">
        <h6 class="mono text-uppercase small text-muted-custom mb-3" data-i18n="footer.guide">Guía</h6>
        <ul class="list-unstyled">
{chr(10).join(guide_li)}
        </ul>
      </div>
      <div class="col-lg-4">
        <h6 class="mono text-uppercase small text-muted-custom mb-3" data-i18n="footer.follow">Síguenos</h6>
        <div class="d-flex gap-2">
          <a href="https://github.com/Apaza-Victor/Gu-a-de-Autocad" class="icon-btn" target="_blank" rel="noopener"><i class="bi bi-youtube"></i></a>
          <a href="https://github.com/Apaza-Victor/Gu-a-de-Autocad" class="icon-btn" target="_blank" rel="noopener"><i class="bi bi-instagram"></i></a>
          <a href="https://github.com/Apaza-Victor/Gu-a-de-Autocad" class="icon-btn" target="_blank" rel="noopener"><i class="bi bi-github"></i></a>
        </div>
      </div>
    </div>
    <hr class="mt-5 mb-4" style="border-color:var(--border-soft)">
    <p class="mb-0 small" data-i18n="footer.copyright">© 2026 Victor Apaza. Todos los derechos reservados.</p>
  </div>
</footer>"""


def build_scripts(level_num, include_quiz, include_babylon, prefix="../../"):
    scripts = []
    scripts.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/js/bootstrap.bundle.min.js"></script>')
    scripts.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js"></script>')
    scripts.append('<script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>')
    scripts.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>')
    scripts.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>')
    if level_num == 5:
        scripts.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-lisp.min.js"></script>')
        scripts.append('<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js"></script>')
    scripts.append('<script src="https://cdn.jsdelivr.net/npm/fuse.js@7.0.0"></script>')
    scripts.append('<script src="https://cdn.jsdelivr.net/npm/animejs@3.2.2/lib/anime.min.js"></script>')
    if include_babylon:
        scripts.append('<script src="https://cdn.babylonjs.com/babylon.js"></script>')
    scripts.append(f'<script src="{prefix}assets/js/i18n.js"></script>')
    scripts.append(f'<script src="{prefix}assets/js/search-index.js"></script>')
    if include_quiz:
        scripts.append(f'<script src="{prefix}assets/js/quiz.js"></script>')
    scripts.append(f'<script src="{prefix}assets/js/animations.js"></script>')
    scripts.append(f'<script src="{prefix}assets/js/main.js"></script>')
    return "\n".join(scripts)


def build_toc_ul(toc_items, lesson_refs, autoeval_href="#autoevaluacion"):
    """toc_items: lista de (href_original, data-toc, label); lesson_refs: dict data-toc -> archivo."""
    lis = []
    for href, dt, label in toc_items:
        if dt and dt in lesson_refs:
            lis.append(f'            <li><a href="{lesson_refs[dt]}" data-toc="{dt}"><span class="toc-check"></span> {label}</a></li>')
        else:
            lis.append(f'            <li><a href="{autoeval_href}"><span class="toc-check"></span> {label}</a></li>')
    return "\n".join(lis)


def build_end_block():
    return f"""<div class="command-line-bar" id="cmdBar">
  <div class="command-line-inner">
    <span class="prompt-sign" data-i18n="ui.command">Comando:</span>
    <span id="cmd-typed"></span><span class="cursor-blink"></span>
    <button class="cl-close" id="cmdClose" title="Ocultar" data-i18n-title="ui.hide"><i class="bi bi-x-lg"></i></button>
  </div>
</div>

<div class="search-overlay" id="searchOverlay" role="dialog" aria-label="Buscar en la guía" data-i18n-aria="ui.search">
  <div class="search-box">
    <div class="search-input-wrap">
      <i class="bi bi-search"></i>
      <input type="text" id="globalSearchInput" placeholder="Buscar comandos, temas, conceptos..." autocomplete="off" aria-label="Buscar" data-i18n-placeholder="ui.searchPlaceholder">
      <kbd class="search-kbd">ESC</kbd>
    </div>
    <div class="search-results" id="globalSearchResults">
      <div class="search-empty" data-i18n="ui.typeToSearch">Escribe al menos 2 caracteres para buscar...</div>
    </div>
  </div>
</div>"""


# ----------------------------------------------------------------------------
# generación principal
# ----------------------------------------------------------------------------

def main():
    generated = []

    for num, (folder, name, full_title, eyebrow, head_desc, schema_name, schema_desc) in LEVELS.items():
        src = os.path.join(PAGINAS, folder + ".html")
        html = read(src)
        dst_dir = os.path.join(PAGINAS, folder)
        os.makedirs(dst_dir, exist_ok=True)

        # --- extraer navbar / header / aside / article / footer originales ---
        m_nav = re.search(r'<nav class="navbar navbar-cad navbar-expand-lg">.*?</nav>', html, re.S)
        m_head_el = re.search(r"<header class=\"page-header\"[^>]*>.*?</header>", html, re.S)
        m_aside = re.search(r'<aside class="col-lg-3 mb-5 mb-lg-0">.*?</aside>', html, re.S)
        m_article = re.search(r'<article class="content-article">(.*?)</article>', html, re.S)
        m_footer = re.search(r'<footer class="site-footer">.*?</footer>', html, re.S)

        header_el = m_head_el.group(0) if m_head_el else ""
        aside_el = m_aside.group(0) if m_aside else ""
        article_body = m_article.group(1) if m_article else ""

        # --- TOC original: (href_id, data-toc, label) ---
        toc_items = []
        m_toc = re.search(r'<ul class="toc-list">(.*?)</ul>', aside_el, re.S)
        if m_toc:
            for li in re.findall(r"<li>(.*?)</li>", m_toc.group(1), re.S):
                am = re.search(r'<a\s+href="#([^"]*)"\s+data-toc="([^"]*)"[^>]*>(.*?)</a>', li, re.S)
                if am:
                    toc_items.append((am.group(1), am.group(2), strip_tags(am.group(3))))
                else:
                    am2 = re.search(r'<a\s+href="#([^"]*)"[^>]*>(.*?)</a>', li, re.S)
                    if am2:
                        toc_items.append((am2.group(1), "", strip_tags(am2.group(2))))

        # --- secciones del artículo ---
        blocks = extract_blocks(article_body)
        topics = []
        visuals = ""
        quiz = ""
        for b in blocks:
            attrs = opening_attrs(b)
            if attrs["data-topic"]:
                title, i18n = h2_info(b)
                topics.append({
                    "block": rewrite_paginas_links(b, True),
                    "title": title,
                    "i18n": i18n,
                    "desc": first_paragraph(b),
                    "data_topic": attrs["data-topic"],
                    "file": re.match(r"^nivel[1-5]-(.+)$", attrs["data-topic"]).group(1) + ".html",
                })
            elif "inline-visual-examples" in attrs["class"]:
                visuals = rewrite_paginas_links(b, True)
            elif "quiz-section" in attrs["class"]:
                quiz = rewrite_paginas_links(b, True)

        if not topics:
            raise SystemExit(f"Sin temas detectados en {src}")

        total = len(topics)
        lesson_refs = {t["data_topic"]: t["file"] for t in topics}

        # --- nivel 4: laboratorio 3D (fuera del artículo) ---
        lab_html = ""
        if num == 4:
            m_lab = re.search(r'<section class="cad3d-lab"[^>]*>.*?</section>', html, re.S)
            if m_lab:
                lab_html = rewrite_paginas_links(m_lab.group(0), True)

        # ---------- PORTADA index.html ----------
        toc_portada = build_toc_ul(toc_items, lesson_refs, autoeval_href="#autoevaluacion")
        next_btn = PAGE_BTN = ""
        if num < 5:
            nfolder = NEXT_FOLDER[num]
            next_btn = f'<a href="../{nfolder}/index.html" class="btn-cad-outline w-100 text-center d-block">{NEXT_LABEL[num]} <i class="bi bi-arrow-right"></i></a>'
        else:
            next_btn = '<a href="../comandos.html" class="btn-cad-outline w-100 text-center d-block">Diccionario de comandos <i class="bi bi-arrow-right"></i></a>'

        cards = []
        for i, t in enumerate(topics, 1):
            delay = (i - 1) % 3 * 80
            cards.append(f"""                    <div class="col-md-6 col-lg-4" data-aos="fade-up" data-aos-delay="{delay}">
                      <a href="{t['file']}" class="text-decoration-none">
                        <div class="level-card">
                          <div class="level-index">{str(i).zfill(2)}</div>
                          <span class="level-tag">Tema {i}</span>
                          <h3>{t['title']}</h3>
                          <p>{t['desc']}</p>
                        </div>
                      </a>
                    </div>""")

        if num > 1:
            prev_folder = LEVELS[num - 1][0]
            nav_prev = f"""<a href="../{prev_folder}/index.html">
            <span class="nav-label">Anterior</span>
            <span class="nav-title"><i class="bi bi-arrow-left"></i> Nivel {num - 1} · {LEVELS[num - 1][1]}</span>
          </a>"""
        else:
            nav_prev = "<span></span>"

        if num < 5:
            nfolder = NEXT_FOLDER[num]
            nav_next = f"""<a href="../{nfolder}/index.html" class="nav-next">
            <span class="nav-label">Siguiente</span>
            <span class="nav-title">{NEXT_LABEL[num]} <i class="bi bi-arrow-right"></i></span>
          </a>"""
        else:
            nav_next = f"""<a href="../comandos.html" class="nav-next">
            <span class="nav-label">Siguiente</span>
            <span class="nav-title">Diccionario de comandos <i class="bi bi-arrow-right"></i></span>
          </a>"""

        portada = f"""<!DOCTYPE html>
<html lang="es" data-theme="dark">
{build_head(f"Nivel {num} · {full_title} — AutoCAD Guía", f"/paginas/{folder}/index.html", head_desc, include_3d=(num == 4), schema_name=schema_name, schema_desc=schema_desc)}

<body>

<a href="#main-content" class="skip-link">Saltar al contenido principal</a>

{build_navbar(num)}

<header class="page-header" id="main-content">
  <div class="container container-xl">
    <p class="crumb"><a href="../../index.html">Inicio</a> / <a href="../../index.html#niveles">Niveles</a> / {full_title}</p>
    <span class="eyebrow" data-i18n="lvl{num}.eyebrow">{eyebrow}</span>
    <h1 data-i18n="lvl{num}.title">{full_title}</h1>
    <p class="subtitle" data-i18n="lvl{num}.subtitle">{head_desc}</p>
    <div class="level-progress-bar" data-level-prefix="nivel{num}" data-level-total="{total}"><div class="fill"></div></div>
    <p class="level-progress-label">0 de {total} temas completados · 0%</p>
  </div>
</header>

<div class="content-layout">
  <div class="container container-xl">
    <div class="row">

      <aside class="col-lg-3 mb-5 mb-lg-0">
        <div class="toc-sidebar">
          <h6 data-i18n="ui.inThisLevel">En este nivel</h6>
          <ul class="toc-list">
{toc_portada}
          </ul>
          <hr style="border-color:var(--border-soft)" class="my-4">
          {next_btn}
        </div>
      </aside>

      <div class="col-lg-9">
        <article class="content-article">
          <section class="level-intro">
            <h2>Contenido del nivel</h2>
            <p>Este nivel se divide en {total} temas. Sigue el orden recomendado o salta directamente al que necesites.</p>
            <div class="row g-4 mt-1">
{chr(10).join(cards)}
            </div>
          </section>

{visuals}
{quiz}

        </article>

        <nav class="level-nav">
          {nav_prev}
          {nav_next}
        </nav>
      </div>
    </div>
  </div>
</div>

{lab_html}
{build_footer()}

{build_end_block()}

{build_scripts(num, include_quiz=True, include_babylon=(num == 4))}

</body>
</html>
"""
        write(os.path.join(dst_dir, "index.html"), portada)
        generated.append(f"{folder}/index.html")

        # ---------- LECCIONES ----------
        for i, t in enumerate(topics):
            toc_lesson = build_toc_ul(toc_items, lesson_refs, autoeval_href="index.html#autoevaluacion")

            prev_t = topics[i - 1] if i > 0 else None
            next_t = topics[i + 1] if i + 1 < len(topics) else None

            if prev_t:
                nav_prev = f"""<a href="{prev_t['file']}">
            <span class="nav-label">Anterior</span>
            <span class="nav-title"><i class="bi bi-arrow-left"></i> {prev_t['title']}</span>
          </a>"""
            else:
                nav_prev = '<span></span>'

            if next_t:
                nav_next = f"""<a href="{next_t['file']}" class="nav-next">
            <span class="nav-label">Siguiente</span>
            <span class="nav-title">{next_t['title']} <i class="bi bi-arrow-right"></i></span>
          </a>"""
            else:
                nav_next = f"""<a href="index.html#autoevaluacion" class="nav-next">
            <span class="nav-label">Siguiente</span>
            <span class="nav-title">Autoevaluación <i class="bi bi-arrow-right"></i></span>
          </a>"""

            lesson = f"""<!DOCTYPE html>
<html lang="es" data-theme="dark">
{build_head(f"{t['title']} · Nivel {num} — AutoCAD Guía", f"/paginas/{folder}/{t['file']}", t['desc'], include_3d=False, schema_name=schema_name, schema_desc=schema_desc)}

<body>

<a href="#main-content" class="skip-link">Saltar al contenido principal</a>

{build_navbar(num)}

<header class="page-header" id="main-content">
  <div class="container container-xl">
    <p class="crumb"><a href="../../index.html">Inicio</a> / <a href="../../index.html#niveles">Niveles</a> / <a href="index.html">{full_title}</a> / Tema {i+1}</p>
    <span class="eyebrow" data-i18n="lvl{num}.eyebrow">{eyebrow}</span>
    <h1 {"data-i18n=\"" + t['i18n'] + "\"" if t['i18n'] else ''}>{t['title']}</h1>
    <div class="level-progress-bar" data-level-prefix="nivel{num}" data-level-total="{total}"><div class="fill"></div></div>
    <p class="level-progress-label">0 de {total} temas completados · 0%</p>
  </div>
</header>

<div class="content-layout">
  <div class="container container-xl">
    <div class="row">

      <aside class="col-lg-3 mb-5 mb-lg-0">
        <div class="toc-sidebar">
          <h6 data-i18n="ui.inThisLevel">En este nivel</h6>
          <ul class="toc-list">
{toc_lesson}
          </ul>
          <hr style="border-color:var(--border-soft)" class="my-4">
          <a href="index.html" class="btn-cad-outline w-100 text-center d-block"><i class="bi bi-arrow-left"></i> Volver al índice</a>
        </div>
      </aside>

      <div class="col-lg-9">
        <article class="content-article">

{t['block']}

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

{build_scripts(num, include_quiz=False, include_babylon=(num == 4))}

</body>
</html>
"""
            write(os.path.join(dst_dir, t["file"]), lesson)
            generated.append(f"{folder}/{t['file']}")

        # ---------- REDIRECCIÓN del archivo antiguo ----------
        redirect = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Redirigiendo — Nivel {num} · {full_title} — AutoCAD Guía</title>
<meta http-equiv="refresh" content="0; url={folder}/index.html">
<link rel="canonical" href="{BASE_URL}/paginas/{folder}/index.html">
</head>
<body>
<p style="font-family:sans-serif;padding:2rem">Redirigiendo a <a href="{folder}/index.html">Nivel {num} · {full_title}</a>…</p>
</body>
</html>
"""
        write(src, redirect)

    print(f"Generadas {len(generated)} páginas de nivel.")

    # ------------------------------------------------------------------
    # 1) Enlaces en index.html / 404.html / paginas/*.html
    # ------------------------------------------------------------------
    index_path = os.path.join(ROOT, "index.html")
    idx = read(index_path)
    for num, (folder, *_rest) in LEVELS.items():
        idx = idx.replace(f"paginas/{folder}.html", f"paginas/{folder}/index.html")
    write(index_path, idx)

    notfound_path = os.path.join(ROOT, "404.html")
    if os.path.exists(notfound_path):
        nf = read(notfound_path)
        for num, (folder, *_rest) in LEVELS.items():
            nf = nf.replace(f"paginas/{folder}.html", f"paginas/{folder}/index.html")
        write(notfound_path, nf)

    for fname in os.listdir(PAGINAS):
        if not fname.endswith(".html"):
            continue
        if re.match(r"^nivel-[1-5]-", fname):
            continue  # son las redirecciones nuevas
        p = os.path.join(PAGINAS, fname)
        txt = read(p)
        for num, (folder, *_rest) in LEVELS.items():
            txt = txt.replace(f'href="{folder}.html"', f'href="{folder}/index.html"')
        write(p, txt)

    print("Enlaces de index.html, 404.html y paginas/*.html actualizados.")

    # ------------------------------------------------------------------
    # 2) search-index.js: file/anchor -> nueva ubicación
    # ------------------------------------------------------------------
    search_path = os.path.join(ROOT, "assets", "js", "search-index.js")
    sj = read(search_path)

    def fix_search(m):
        file_raw = m.group(2)          # nivel-X-xxxx.html
        anchor = m.group(4)
        folder = file_raw[:-5]
        if anchor:
            new_file = folder + "/" + anchor + ".html"
        else:
            new_file = folder + "/index.html"
        return m.group(1) + new_file + m.group(3) + '""' + m.group(5)

    pattern = re.compile(r'("file":\s*")(nivel-[1-5]-[a-z0-9-]+?\.html)("\s*,\s*"anchor":\s*")([^"]*)(")')
    new_sj = pattern.sub(fix_search, sj)
    if new_sj != sj:
        write(search_path, new_sj)
        print("search-index.js actualizado:", sj.count('"file": "nivel-'), "entradas")
    else:
        print("search-index.js: nada que cambiar")

    # ------------------------------------------------------------------
    # 3) main.js
    # ------------------------------------------------------------------
    main_path = os.path.join(ROOT, "assets", "js", "main.js")
    mj = read(main_path)

    # 3.1 lista de niveles del buscador (buildSearchData)
    old_levels_block = mj[find_idx(mj, "const levels = ["):find_idx(mj, "]\n    levels.forEach") + len("]")] if "const levels = [" in mj else ""
    if old_levels_block:
        new_lines = []
        for num, (folder, *_rest) in LEVELS.items():
            new_lines.append(f"      {{ name: 'Nivel {num} · {LEVELS[num][1]}', url: 'paginas/{folder}/index.html' }},")
        new_lines.append("      { name: 'Comandos', url: 'paginas/comandos.html' },")
        new_lines.append("      { name: 'Recursos', url: 'paginas/recursos.html' },")
        new_lines.append("      { name: 'FAQ', url: 'paginas/faq.html' }")
        new_block = "const levels = [\n" + "\n".join(new_lines) + "\n    ];"
        mj = mj.replace(old_levels_block, new_block)
        print("main.js: lista de niveles actualizada")

    # 3.2 determinePage
    old_dp = re.search(r"function determinePage\(section\)\{.*?\n\}", mj, re.S)
    if old_dp:
        map_lines = "\n".join(
            f"  const PAGES = {{ nivel{n}: '{folder}' }};" for n, (folder, *_rest) in LEVELS.items()
        )
        new_dp = """function determinePage(section){
  const topic = section.getAttribute('data-topic') || '';
  const PAGES = { nivel1: 'nivel-1-fundamentos', nivel2: 'nivel-2-dibujo-2d', nivel3: 'nivel-3-organizacion', nivel4: 'nivel-4-modelado-3d', nivel5: 'nivel-5-avanzado' };
  const m = topic.match(/^(nivel[1-5])-(.+)$/);
  if (!m) return 'nivel-1-fundamentos/index.html';
  const folder = PAGES[m[1]] || 'nivel-1-fundamentos';
  return folder + '/' + m[2] + '.html';
}"""
        mj = mj.replace(old_dp.group(0), new_dp)
        print("main.js: determinePage actualizado")

    # 3.3 updateLevelProgress con soporte de subcarpetas
    old_ulp = re.search(r"function updateLevelProgress\(\)\{.*?\n\}", mj, re.S)
    if old_ulp:
        new_ulp = """function updateLevelProgress(){
  const label = document.querySelector('.level-progress-label');
  const fill = document.querySelector('.level-progress-bar .fill');
  if (!label || !fill) return;

  const bar = document.querySelector('.level-progress-bar');
  const levelPrefix = bar && bar.getAttribute('data-level-prefix');
  const levelTotal = bar ? parseInt(bar.getAttribute('data-level-total') || '0', 10) : 0;
  const saved = JSON.parse(localStorage.getItem('autocad-guia-progreso') || '[]');

  let total, done;
  if (levelPrefix && levelTotal) {
    total = levelTotal;
    done = saved.filter(id => id.indexOf(levelPrefix) === 0).length;
  } else {
    const allTopics = document.querySelectorAll('[data-topic]');
    total = allTopics.length;
    if (total === 0) return;
    done = 0;
    allTopics.forEach(s => {
      if (isTopicComplete(s.getAttribute('data-topic'))) done++;
    });
  }

  const pct = Math.round((done / total) * 100);
  fill.style.width = pct + '%';
  label.textContent = (function(){
    if (window.I18N_SYSTEM){
      return I18N_SYSTEM.t('progress.xOfY').replace('{done}', done).replace('{total}', total).replace('{pct}', pct);
    }
    return done + ' de ' + total + ' temas completados · ' + pct + '%';
  })();
}"""
        mj = mj.replace(old_ulp.group(0), new_ulp)
        print("main.js: updateLevelProgress actualizado")

    # 3.4 initHomeProgress -> total 67
    old_hp = re.search(r"const total = allTopics\.length \|\| 51;.*?done = Math\.max\(done, saved\.length\);", mj, re.S)
    if old_hp:
        new_hp = """const savedTopics = JSON.parse(localStorage.getItem('autocad-guia-progreso') || '[]');
  const total = 67; // 9 + 15 + 13 + 16 + 14
  let done = Math.min(savedTopics.length, total);"""
        mj = mj.replace(old_hp.group(0), new_hp)
        print("main.js: initHomeProgress actualizado")

    # 3.5 helper refreshTocDone + llamadas
    if "function refreshTocDone" not in mj:
        helper = """function refreshTocDone(){
  document.querySelectorAll('.toc-list a[data-toc]').forEach(link => {
    const id = link.getAttribute('data-toc');
    link.classList.toggle('done', isTopicComplete(id));
  });
}
"""
        mj = mj.replace("function updateLevelProgress(){", helper + "function updateLevelProgress(){")
    # reemplazar actualizaciones aisladas del toc-link por refreshTocDone()
    mj = mj.replace(
        "      const tocLink = document.querySelector('.toc-list a[data-toc=\"' + topicId + '\"]');\n      if (tocLink) tocLink.classList.add('done');",
        "      refreshTocDone();")
    mj = mj.replace(
        "      const tocLink = document.querySelector('.toc-list a[data-toc=\"' + topicId + '\"]');\n      if (tocLink) tocLink.classList.remove('done');",
        "      refreshTocDone();")
    # llamar refreshTocDone() al iniciar
    mj = mj.replace("  initMarkDone();\n", "  initMarkDone();\n  refreshTocDone();\n")

    write(main_path, mj)
    print("main.js: refreshTocDone integrado")

    # ------------------------------------------------------------------
    # 4) sitemap.xml
    # ------------------------------------------------------------------
    urls = ["/", "/paginas/comandos.html", "/paginas/ejemplos-visuales.html", "/paginas/trucos.html", "/paginas/tips.html", "/paginas/recursos.html", "/paginas/faq.html", "/404.html"]
    for num, (folder, *_rest) in LEVELS.items():
        urls.append(f"/paginas/{folder}/index.html")
        for fname in sorted(os.listdir(os.path.join(PAGINAS, folder))):
            if fname.endswith(".html") and fname != "index.html":
                urls.append(f"/paginas/{folder}/{fname}")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{BASE_URL}{u}</loc>")
        lines.append("    <lastmod>2026-07-31</lastmod>")
        lines.append("    <changefreq>monthly</changefreq>")
        lines.append("    <priority>0.8</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    write(os.path.join(ROOT, "sitemap.xml"), "\n".join(lines) + "\n")
    print("sitemap.xml regenerado con", len(urls), "URLs")


def find_idx(s, sub):
    i = s.find(sub)
    return i


if __name__ == "__main__":
    main()