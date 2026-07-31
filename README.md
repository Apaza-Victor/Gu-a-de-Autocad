# AutoCAD — Guia de Aprendizaje: De Cero a Experto

> Sitio web educativo interactivo para aprender AutoCAD desde cero hasta nivel avanzado, con soporte para dos idiomas (ES/EN).

**Ver en vivo:** [apaza-victor.github.io/Gu-a-de-Autocad](https://apaza-victor.github.io/Gu-a-de-Autocad/)

**© 2026 Victor Apaza. Todos los derechos reservados.**

---

## Contenido

### Niveles de aprendizaje

| Nivel | Tema | Contenido |
|-------|------|-----------|
| 1 | Fundamentos | Interfaz, comandos, coordenadas, SNAP, configuracion |
| 2 | Dibujo 2D | 8 herramientas de dibujo, modificaciones, seleccion, organizacion |
| 3 | Organizacion | Capas, bloques, plantillas, cotas, estilos de texto, escala |
| 4 | Modelado 3D | UCS, solidos primitivos, extrusion, booleanos, mallas, render |
| 5 | Avanzado | Diseno parametrico, Dynamic Blocks, AutoLISP, XREF, rendimiento |

### Secciones complementarias

- **Diccionario de comandos** — 95 comandos con busqueda, filtros por categoria y teclas de acceso rapido
- **Ejemplos visuales** — diagramas paso a paso que muestran antes/despues de cada comando
- **Trucos y atajos** — tips de aprendizaje, atajos de teclado, errores comunes y flujo de trabajo
- **Recursos** — 18 recursos descargables: bloques, cursos, comunidades, plantillas, canales de YouTube, herramientas
- **Preguntas frecuentes** — 15 respuestas sobre instalacion, rendimiento, compatibilidad, funciones y aprendizaje

---

## Funcionalidades

- **Soporte bilingue (ES/EN)** — traducciones completas de interfaz, comandos y contenido via sistema i18n
- **Tema oscuro/claro** — toggle con persistencia en localStorage, deteccion automatica de preferencia del sistema (`prefers-color-scheme`)
- **Progreso de aprendizaje** — cada tema se puede marcar como visto, con barra de progreso global
- **Buscador global** — busqueda inteligente con fuzzy matching (Fuse.js), atajo `Ctrl+K`
- **Filtros de comandos** — 10 categorias: Dibujo, Modificacion, Precision, Capas, Acotacion, Texto, Bloques, Edicion, 3D, Consulta
- **Carruseles** — galerias interactivas con Swiper.js
- **Bloques de codigo** — con resaltado de sintaxis (Prism.js) y boton de copiar
- **Navegacion por teclado** — FAQ accesible con Enter/Espacio, filtros con flechas
- **Tabla de atajos descargable** — exporta los atajos a un archivo TXT
- **Accesibilidad** — skip-to-content link, estilos de foco visibles (`:focus-visible`), contraste WCAG AA, soporte `prefers-reduced-motion`
- **Impresion** — estilos `@media print` que ocultan navbar, sidebar, barra de comandos y footer
- **Diseno responsive** — funciona en desktop, tablet y movil

---

## Tecnologias

| Tecnologia | Uso |
|------------|-----|
| HTML5 | Estructura semantica |
| CSS3 | Diseno personalizado con variables CSS, `@media print`, `prefers-reduced-motion` |
| Bootstrap 5.3 | Grid, componentes, utilidades |
| Bootstrap Icons | Iconografia |
| JavaScript vanilla | Logica, interaccion, almacenamiento local |
| Fuse.js 7.0 | Busqueda fuzzy en el diccionario de comandos |
| Swiper.js 11 | Carruseles de ejemplos |
| Prism.js 1.29 | Resaltado de codigo y sintaxis |
| AOS 2.3 | Animaciones al hacer scroll |

---

## Estructura del proyecto

```
Guia de Autocad/
├── index.html                  # Pagina principal
├── css/
│   └── style.css               # Estilos completos del sitio
├── js/
│   ├── main.js                 # Funcionalidad JS compartida
│   └── i18n.js                 # Sistema de traduccion ES/EN
├── paginas/
│   ├── nivel-1-fundamentos.html
│   ├── nivel-2-dibujo-2d.html
│   ├── nivel-3-organizacion.html
│   ├── nivel-4-modelado-3d.html
│   ├── nivel-5-avanzado.html
│   ├── comandos.html           # Diccionario de 95 comandos
│   ├── ejemplos-visuales.html  # Diagramas paso a paso
│   ├── trucos.html             # Atajos y tips
│   ├── recursos.html           # Enlaces y plantillas
│   └── faq.html                # Preguntas frecuentes
└── README.md
```

---

## Despliegue

El sitio esta desplegado en **GitHub Pages** desde la rama `main`.

Para ejecutarlo localmente, simplemente abre `index.html` en tu navegador.

---

## Autor y copyright

**Autor:** Victor Apaza — [GitHub](https://github.com/Apaza-Victor)

**© 2026 Victor Apaza. Todos los derechos reservados.**

Este sitio es contenido educativo independiente. No es un sitio oficial de Autodesk®; AutoCAD® es una marca registrada de Autodesk, Inc.
