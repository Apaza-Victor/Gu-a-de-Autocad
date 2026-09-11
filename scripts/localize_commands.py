import re, glob, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = r'C:\Users\LENOVO IDEPAD\Downloads\Repositorio de Módulos\Guía de Autocad'

# EN -> ES (AutoCAD comandos). DIMSTYLE -> ACOESTILO (preferencia del usuario).
MAP = {
    'LINE': 'LÍNEA', 'PLINE': 'POLILÍNEA', 'POLYLINE': 'POLILÍNEA',
    'CIRCLE': 'CÍRCULO', 'ARC': 'ARCO', 'SPLINE': 'CURVA',
    'RECTANG': 'RECTÁNGULO', 'POLYGON': 'POLÍGONO', 'XLINE': 'LINEAX',
    'RAY': 'RAYO', 'POINT': 'PUNTO', 'DIVIDE': 'DIVIDIR', 'MEASURE': 'GRADUA',
    'MLINE': 'MLÍNEA',
    'ALIGN': 'ALINEAR', 'ARRAY': 'MATRIZ', 'COPY': 'COPIAR', 'ERASE': 'BORRAR',
    'EXPLODE': 'EXPLOTAR', 'EXTEND': 'EXTENDER', 'FILLET': 'REDONDEAR',
    'FILTER': 'FILTRO', 'JOIN': 'UNIR', 'MATCHPROP': 'IGUALARPROP',
    'MIRROR': 'REFLEJAR', 'MOVE': 'MOVER', 'OFFSET': 'DESFASE',
    'PEDIT': 'EDITARP', 'PROPERTIES': 'PROPIEDADES', 'QSELECT': 'ELECCIONRAPIDA',
    'SELECT': 'SELECCIONAR', 'SELECTSIMILAR': 'SELECCIONAR SIMILAR',
    'SPLINEDIT': 'EDITARSPLINE', 'STRETCH': 'ESTIRAR', 'TRIM': 'RECORTAR',
    'UNDO': 'DESHACER', 'REDO': 'REHACER', 'GROUP': 'GRUPO',
    'BOUNDARY': 'CONTORNO', 'BREAK': 'ROMPER', 'ROTATE': 'GIRAR', 'SCALE': 'ESCALAR',
    'HATCH': 'SOMBREADO',
    'LAYER': 'CAPA', 'LAYDEL': 'ELIMINARCAPA', 'LAYISO': 'AISLARCAPA',
    'LAYMRG': 'COMBINARCAPA', 'LAYOFF': 'APAGARCAPA', 'LAYON': 'TODASCAPASENCENDIDAS',
    'LAYOUT': 'PRESENTACIÓN', 'LAYTHW': 'TODASCAPAS',
    'LINETYPE': 'TIPOLÍNEA', 'LTSCALE': 'ESCALATIPO',
    'AUDIT': 'AUDITAR', 'PURGE': 'PURGAR', 'RECOVER': 'RECUPERAR', 'UCS': 'SCP',
    'DIM': 'DIMENSIÓN', 'DIMALIGNED': 'ACOALINEADA', 'DIMDIAMETER': 'ACOTDIÁMETRO',
    'DIMLINEAR': 'ACOTLINEAL', 'DIMRADIUS': 'DIMRADIO', 'DIMSTYLE': 'ACOESTILO',
    'TEXT': 'TEXTO', 'MTEXT': 'TEXTM', 'STYLE': 'ESTILO', 'TABLE': 'TABLA',
    'SPELL': 'ORTOGRAFÍA', 'FIELD': 'CAMPO', 'LEADER': 'FLECHA',
    'BLOCK': 'BLOQUE', 'INSERT': 'INSERTAR', 'WBLOCK': 'BLOQUEDISC',
    'ATTDEF': 'DEFATTRIB', 'ATTEDIT': 'EDITATRIB', 'ATTSYNC': 'SINCATRIB',
    'BEDIT': 'EDITBLOQUE', 'XREF': 'REFX', 'XATTACH': 'ENLAZARX',
    'XCLIP': 'CORTEXREF', 'ADCENTER': 'CENTRODC', 'DESIGNCENTER': 'CENTRODC',
    'DATAEXTRACTION': 'EXTRAERDATOS', 'IMPORT': 'IMPORTAR', 'EXPORT': 'EXPORTAR',
    'AREA': 'ÁREA', 'DIST': 'DISTANCIA', 'LIST': 'LISTA', 'MASSPROP': 'PROPFÍS',
    'PAN': 'DESPLAZAR', 'VIEW': 'VISTA', 'VPORTS': 'PUERTOS DE VISTA',
    'REGEN': 'REGENERAR', 'REGENALL': 'REGENT', 'OPTIONS': 'OPCIONES',
    'UNITS': 'UNIDADES', 'GRID': 'CUADRÍCULA', 'SNAP': 'ADHERENCIA',
    'PAGESETUP': 'PREPARARPÁG', 'PLOT': 'IMPRIMIR', 'PUBLISH': 'PUBLICAR',
    'SAVE': 'GUARDAR', 'SAVEAS': 'GUARDARCOMO', 'OPEN': 'ABRIR', 'CLOSE': 'CERRAR',
    'SCRIPT': 'GUION', 'PLOTSTYLE': 'ESTILOTRAMA', 'CAMERA': 'CÁMARA',
    '3DORBIT': 'ÓRBITA3D', 'BOX': 'PRISMA', 'CYLINDER': 'CILINDRO',
    'EXTRUDE': 'EXTRUIR', 'LOFT': 'SOLEVACIÓN', 'REVOLVE': 'REVOLVER',
    'SWEEP': 'BARRIDO', 'SUBTRACT': 'RESTAR', 'UNION': 'UNIÓN',
    'INTERSECT': 'INTERSECCIÓN', 'INTERFERE': 'INTERFERIR', 'SECTION': 'SECCIÓN',
    'SOLIDEDIT': 'EDITARSÓLIDO', 'RENDER': 'MODELIZAR',
}

# Tokens que ya están en español en el sitio -> su inglés.
ES2EN = {
    'UNIDADES': 'UNITS', 'NUEVO': 'NEW', 'AISLAR': 'ISOLATE',
    'ACOESTILO': 'DIMSTYLE',
    'DESHACER': 'UNDO', 'REHACER': 'REDO', 'GUARDAR': 'SAVE', 'COPIAR': 'COPY',
}

SPAN = re.compile(r'<span class="cmd-inline">([^<]+)</span>')
TD = re.compile(r'<td class="cmd-inline">([^<]+)</td>')
NORMAL = re.compile(
    r'<span class="cmd-inline">([A-Z0-9-]+)</span>\s*\(en español\s*<span class="cmd-inline">([^<]+)</span>\)'
)


def normalize(text):
    def sub(m):
        return '<span class="cmd-inline">%s</span> (en inglés: <span class="cmd-inline">%s</span>)' % (m.group(2), m.group(1))
    return NORMAL.sub(sub, text)


def transform(text):
    out = []
    pos = 0
    for m in SPAN.finditer(text):
        out.append(text[pos:m.start()])
        toke = m.group(1).strip()
        prev = text[max(0, m.start() - 40):m.start()]
        nxt = text[m.end():m.end() + 32]
        already = prev.endswith('(') or bool(re.search(r'\(en inglés:\s*$', prev)) or bool(re.match(r'\s*\(en inglés:', nxt))
        key = toke[1:] if toke.startswith('-') else toke
        es = MAP.get(key)
        en = ES2EN.get(key)
        if not already and es:
            out.append('<span class="cmd-inline">%s%s</span> (en inglés: <span class="cmd-inline">%s</span>)' % ('-' if toke.startswith('-') else '', es, toke))
        elif not already and en:
            out.append('<span class="cmd-inline">%s</span> (en inglés: <span class="cmd-inline">%s</span>)' % (key, en))
        else:
            out.append(m.group(0))
        pos = m.end()
    out.append(text[pos:])
    return ''.join(out)


def transform_td(text):
    out = []
    pos = 0
    for m in TD.finditer(text):
        out.append(text[pos:m.start()])
        raw = m.group(0)
        toke = m.group(1).strip()
        if '<span' in m.group(1):
            out.append(raw)
            pos = m.end()
            continue
        prev = text[max(0, m.start() - 40):m.start()]
        nxt = text[m.end():m.end() + 32]
        already = prev.endswith('(') or bool(re.search(r'\(en inglés:\s*$', prev)) or bool(re.match(r'\s*\(en inglés:', nxt))
        key = toke[1:] if toke.startswith('-') else toke
        es = MAP.get(key)
        en = ES2EN.get(key)
        if not already and es:
            out.append('<td class="cmd-inline"><span class="cmd-inline">%s%s</span> (en inglés: <span class="cmd-inline">%s</span>)</td>' % ('-' if toke.startswith('-') else '', es, toke))
        elif not already and en:
            out.append('<td class="cmd-inline"><span class="cmd-inline">%s</span> (en inglés: <span class="cmd-inline">%s</span>)</td>' % (key, en))
        else:
            out.append(raw)
        pos = m.end()
    out.append(text[pos:])
    return ''.join(out)


files = glob.glob(ROOT + r'\**\*.html', recursive=True)
files += glob.glob(ROOT + r'\scripts\lessons_data\*.html')
total = 0
for f in sorted(set(files)):
    try:
        src = open(f, encoding='utf-8', errors='replace').read()
    except Exception as e:
        print('ERR', f, e)
        continue
    out = transform_td(transform(normalize(src)))
    if out != src:
        n = out.count('(en inglés:') - src.count('(en inglés:')
        open(f, 'w', encoding='utf-8', newline='').write(out)
        print('OK', f.replace(ROOT + '\\', ''), '+%d pares' % n)
        total += 1
print('---')
print('archivos modificados:', total)