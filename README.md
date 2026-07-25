# AutoCAD — Guía de Aprendizaje: De Cero a Experto

> Sitio web educativo interactivo para aprender AutoCAD desde cero hasta nivel avanzado.

**Ver en vivo:** [apaza-victor.github.io/Gu-a-de-Autocad](https://apaza-victor.github.io/Gu-a-de-Autocad/)

---

## Contenido

### Niveles de aprendizaje

| Nivel | Tema | Contenido |
|-------|------|-----------|
| 1 | Fundamentos | Interfaz, comandos, coordenadas, SNAP, configuración |
| 2 | Dibujo 2D | 8 herramientas de dibujo, modificaciones, selección, organización |
| 3 | Organización | Capas, bloques, plantillas, dimensiones, estilos de texto, escala |
| 4 | Modelado 3D | UCS,实体, extrusión, revolución, booleanos, mallas, render |
| 5 | Avanzado | Diseño paramétrico, Dynamic Blocks, AutoLISP, XREF, rendimiento |

### Secciones complementarias

- **Diccionario de comandos** — 47+ comandos con búsqueda, filtros por categoría y teclas de acceso rápido
- **Recursos** — 18 recursos descargables: bloques, cursos, comunidades, plantillas, canales de YouTube, herramientas
- **Preguntas frecuentes** — 15 respuestas sobre instalación, rendimiento, compatibilidad, funciones y aprendizaje
- **Tabla de atajos de teclado** — 55+ atajos descargables en archivo TXT

---

## Funcionalidades

- **Tema oscuro/claro** — toggle con persistencia en localStorage
- **Progreso de aprendizaje** — cada tema se puede marcar como visto, con barra de progreso global
- **Buscador global** — búsqueda inteligente con fuzzy matching (Fuse.js), atajo `Ctrl+K`
- **Carruseles** — galerías interactivas con Swiper.js
- **Bloques de código** — con resaltado de sintaxis (Prism.js) y botón de copiar
- **Navegación por teclado** — FAQ accesible con Enter/Espacio, filtros con flechas
- **Tabla de atajos descargable** — exporta los atajos a un archivo TXT
- **Diseño responsive** — funciona en desktop, tablet y móvil

---

## Tecnologías

| Tecnología | Uso |
|------------|-----|
| HTML5 | Estructura semántica |
| CSS3 | Diseño personalizado con variables CSS |
| Bootstrap 5.3 | Grid, componentes, utilidades |
| Bootstrap Icons | Iconografía |
| JavaScript vanilla | Lógica, interacción, almacenamiento local |
| Fuse.js 7.0 | Búsqueda fuzzy en el diccionario de comandos |
| Swiper.js 11 | Carruseles de ejemplos |
| Prism.js 1.29 | Resaltado de código y sintaxis |
| AOS 2.3 | Animaciones al hacer scroll |

---

## Estructura del proyecto

```
Guía de Autocad/
├── index.html              # Página principal
├── css/
│   └── style.css           # Estilos completos del sitio
├── js/
│   └── main.js             # Toda la funcionalidad JS
├── paginas/
│   ├── nivel-1-fundamentos.html
│   ├── nivel-2-dibujo-2d.html
│   ├── nivel-3-organizacion.html
│   ├── nivel-4-modelado-3d.html
│   ├── nivel-5-avanzado.html
│   ├── comandos.html
│   ├── recursos.html
│   └── faq.html
├── img/                    # Imágenes (pendiente)
└── README.md
```

---

## Despliegue

El sitio está desplegado en **GitHub Pages** desde la rama `main`.

Para ejecutarlo localmente, simplemente abre `index.html` en tu navegador.

---

## Autor

**Victor Apaza** — [GitHub](https://github.com/Apaza-Victor)
