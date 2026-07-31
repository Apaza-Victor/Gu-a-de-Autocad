# Documentacion de mi Web — Guia de AutoCAD

> Documentacion tecnica del sitio web educativo interactivo para aprender AutoCAD desde cero hasta nivel avanzado.

**URL en vivo:** [apaza-victor.github.io/Gu-a-de-Autocad](https://apaza-victor.github.io/Gu-a-de-Autocad/)

**Repositorio:** [github.com/Apaza-Victor/Gu-a-de-Autocad](https://github.com/Apaza-Victor/Gu-a-de-Autocad)

---

## 1. Descripcion general

Sitio web estatico educativo que funciona como guia teorica y diccionario de comandos de AutoCAD. Contiene 5 niveles de aprendizaje progresivos, un diccionario de 95 comandos, ejemplos visuales, trucos, recursos descargables y preguntas frecuentes. Soporta dos idiomas (ES/EN) y tema oscuro/claro.

---

## 2. Arquitectura del proyecto

### Estructura de archivos

```
Guia de Autocad/
├── index.html                  # Pagina principal (hero, niveles, progreso)
├── css/
│   └── style.css               # Estilos completos del sitio (~1500 lineas)
├ js/
│   ├── main.js                 # Funcionalidad JS compartida (~755 lineas)
│   └── i18n.js                 # Sistema de traduccion ES/EN (~1170 lineas)
├ paginas/
│   ├── nivel-1-fundamentos.html    # Nivel 1: Fundamentos
│   ├── nivel-2-dibujo-2d.html      # Nivel 2: Dibujo 2D
│   ├── nivel-3-organizacion.html   # Nivel 3: Organizacion y productividad
│   ├── nivel-4-modelado-3d.html    # Nivel 4: Modelado 3D
│   ├── nivel-5-avanzado.html       # Nivel 5: Nivel experto
│   ├── comandos.html               # Diccionario de 95 comandos
│   ├── ejemplos-visuales.html      # Diagramas paso a paso
│   ├── trucos.html                 # Atajos, tips, errores comunes
│   ├── recursos.html               # 18 recursos descargables
│   └── faq.html                    # 15 preguntas frecuentes
└── README.md
```

### Archivos clave

| Archivo | Funcion | Tamano aprox |
|---------|---------|--------------|
| `index.html` | Landing page con hero, cards de niveles, progreso | ~120 lineas |
| `css/style.css` | Estilos completos, variables CSS, responsive, print, accesibilidad | ~1500 lineas |
| `js/main.js` | Theme toggle, search, filters, scroll-spy, mark-done, FAQ, Swiper, Prism | ~755 lineas |
| `js/i18n.js` | Diccionario de traducciones ES/EN para toda la interfaz | ~1200 lineas |
| `paginas/comandos.html` | 95 tarjetas de comandos con data-cmd, data-cat, data-level, data-keys | ~1414 lineas |

---

## 3. Stack tecnologico

| Tecnologia | Version | Uso |
|------------|---------|-----|
| HTML5 | - | Estructura semantica, data attributes |
| CSS3 | - | Variables CSS, Flexbox, Grid, @media print, prefers-reduced-motion |
| Bootstrap | 5.3 | Grid, componentes, utilidades |
| Bootstrap Icons | - | Iconografia (bi-*) |
| JavaScript | Vanilla | Logica, interaccion, localStorage |
| Fuse.js | 7.0 | Busqueda fuzzy (global search overlay) |
| Swiper.js | 11 | Carruseles de imagenes |
| Prism.js | 1.29 | Resaltado de codigo + boton copiar |
| AOS | 2.3 | Animaciones al hacer scroll |

---

## 4. Funcionalidades implementadas

### 4.1 Interfaz

- **Navbar fija** con links a todos los niveles y secciones
- **Sidebar de navegacion** con scroll-spy en paginas de contenido
- **Boton "volver arriba"** con clase `.back-to-top-btn`
- **Footer** con enlaces rapidos y redes sociales
- **Responsive** mobile-first con Bootstrap grid

### 4.2 Sistema de temas

- **Dark/Light toggle** con boton `#themeToggle`
- Persistencia en `localStorage` key: `autocad-guia-theme`
- Deteccion automatica de `prefers-color-scheme` en primera visita
- Variable CSS `data-theme="light|dark"` en `:root`

### 4.3 Sistema de internacionalizacion (i18n)

- Diccionario en `js/i18n.js` con secciones `es` y `en`
- Elementos traducidos via atributo `data-i18n="key"` (textContent)
- Elementos traducidos via `data-i18n-html` (innerHTML)
- Placeholders via `data-i18n-placeholder`
- Titulos via `data-i18n-title`
- Aria labels via `data-i18n-aria`
- Toggle de idioma via boton `#langToggle`
- Persistencia en `localStorage` key: `autocad-guia-lang`
- Clase `.res-lang.en` para badges de nivel en ingles

### 4.4 Diccionario de comandos (`comandos.html`)

- **95 tarjetas** de comandos HTML estaticos
- Cada tarjeta es un `div.cmd-full-card` con atributos:
  - `data-cmd`: nombre del comando (LINE, CIRCLE, etc.)
  - `data-cat`: categoria (dibujo, modificacion, precision, capas, acotacion, texto, bloques, edicion, 3d, consulta)
  - `data-level`: nivel (basico, intermedio, avanzado)
  - `data-keys`: atajos de teclado separados por coma
- **10 filtros** por categoria via `data-filter`
- **Busqueda** por nombre, descripcion, atajo o categoria
- Contador dinamico actualizado por JS

### 4.5 Buscador global

- Overlay con `#searchOverlay`
- Input `#globalSearchInput`
- Resultados en `#globalSearchResults`
- Fuse.js con keys: title (0.4), command (0.3), shortcut (0.2), description (0.1)
- Threshold: 0.4, minMatchCharLength: 2
- Atajo de teclado: `Ctrl+K`

### 4.6 Progreso de aprendizaje

- Botones "Marcar tema como visto" en cada seccion
- Almacenamiento en `localStorage` key: `autocad-guia-progreso`
- Barra de progreso en la pagina principal
- Formato: `["nivel1-que-es", "nivel2-capas", ...]` (array plano con los IDs `data-topic` de los temas completados)

### 4.7 Otros

- **Swiper.js** para carruseles de imagenes
- **Prism.js** para bloques de codigo con syntax highlighting
- **Boton copiar** en bloques de codigo
- **FAQ acordeon** con navegacion por teclado (Enter/Espacio)
- **Tabla de atajos** descargable a TXT
- **Skip-to-content link** para accesibilidad

---

## 5. Accesibilidad

| Caracteristica | Implementacion |
|----------------|----------------|
| Skip-to-content | `<a class="skip-link" href="#main-content">` en todas las paginas |
| Focus visible | `:focus-visible` en botones, links, filtros, Swiper nav, copiar |
| Contraste WCAG AA | `--text-faint` ajustado a `#8296B0` (dark) / `#6B7D9A` (light) |
| Reduced motion | `@media (prefers-reduced-motion: reduce)` desactiva animaciones |
| Print styles | `@media print` oculta navbar, sidebar, command bar, footer |
| Aria labels | Botones interactivos con `aria-label` traducidos via i18n |
| Tabindex | FAQ items con `tabindex="0"` |

---

## 6. Convenciones de codigo

### CSS
- Variables CSS en `:root` para colores, fuentes, espaciado
- Clases BEM-like: `.cmd-full-card`, `.cmd-icon`, `.cmd-info`, `.cmd-head`, `.cmd-desc`
- Responsive con `@media (max-width: 768px)` y `clamp()` para tipografia

### JavaScript
- IIFE via `DOMContentLoaded` listener
- Funciones init separadas: `initThemeToggle()`, `initSearchToggle()`, `initScrollSpy()`, etc.
- Sin frameworks, vanilla JS puro
- `window.I18N_SYSTEM` para verificar si i18n esta activo
- Fallback a ES cuando la clave no existe en EN

### HTML
- Data attributes para interactividad: `data-cmd`, `data-cat`, `data-level`, `data-keys`, `data-filter`, `data-i18n`
- Clases para i18n: `.res-lang.en` para contenido en ingles
- Cards de comandos: estructura fija `.cmd-full-card > .cmd-icon + .cmd-info > .cmd-head + .cmd-desc`
- SVG inline para imagenes de ejemplos visuales

---

## 7. Contenido del sitio

### Niveles de aprendizaje

| Nivel | Titulo | Secciones |
|-------|--------|-----------|
| 1 | Fundamentos | Interfaz, comandos, coordenadas, SNAP, configuracion |
| 2 | Dibujo 2D | Herramientas, modificaciones, precision, capas, bloques, cotas, texto, hatch |
| 3 | Organizacion | Layouts, viewports, plantillas, impresion, XREF, atajos, plot styles, fields |
| 4 | Modelado 3D | Navegacion, solidos, booleanos, extrusion, edicion, render, mallas, superficies |
| 5 | Avanzado | CUI, AutoLISP, estandares CAD, practicas, integracion, Dynamo, Python, BIM |

### Secciones complementarias

- **Diccionario de comandos**: 95 comandos en 10 categorias
- **Ejemplos visuales**: diagramas SVG paso a paso
- **Trucos**: atajos, aprendizaje, errores comunes, flujo de trabajo, avanzado
- **Recursos**: 18 recursos (bloques, cursos, comunidades, plantillas, YouTube, herramientas)
- **FAQ**: 15 preguntas frecuentes

---

## 8. Despliegue

- **Plataforma**: GitHub Pages desde rama `main`
- **URL**: https://apaza-victor.github.io/Gu-a-de-Autocad/
- **CI/CD**: push automatico a `main` despliega el sitio
- **Ejecucion local**: abrir `index.html` en navegador (no requiere servidor)

---

## 9. Autor

**Victor Apaza** — [GitHub](https://github.com/Apaza-Victor)
