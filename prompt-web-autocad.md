# Prompt: Desarrollo de Web Guía/Teoría de AutoCAD (De Cero a Experto)

Copia y usa este prompt completo para pedirle a una IA (o para guiar tu propio desarrollo) la creación de la página web.

---

## PROMPT

Actúa como un desarrollador web full-stack senior especializado en diseño educativo y UX/UI. Necesito que crees una página web completa que funcione como **guía y enciclopedia teórica de AutoCAD**, pensada para llevar a cualquier usuario **de cero a experto**, sirviendo tanto para **aprender desde el inicio** como para **consultar y repasar** conceptos puntuales.

### 1. Objetivo del proyecto
Crear un sitio web educativo, ordenado, visualmente atractivo y 100% responsivo, que explique todo lo necesario para dominar AutoCAD (2D y 3D), incluyendo teoría, comandos, atajos, buenas prácticas y una sección de recursos gratuitos.

### 2. Tecnologías a utilizar
- **HTML5** semántico (header, nav, main, section, article, aside, footer).
- **CSS3** con variables (custom properties), Flexbox y Grid.
- **Bootstrap 5** para el sistema de grillas, componentes (navbar, cards, accordion, tabs, modals, offcanvas) y responsividad base.
- **JavaScript (Vanilla)** para interactividad: buscador interno, filtros, modo oscuro/claro, scroll-spy, acordeones de comandos, sistema de progreso de aprendizaje (localStorage).
- Librerías adicionales opcionales:
  - **AOS (Animate On Scroll)** para animaciones al hacer scroll.
  - **Prism.js o Highlight.js** para mostrar comandos/código con formato tipo consola.
  - **Font Awesome / Bootstrap Icons** para iconografía técnica (planos, capas, herramientas).
  - **Swiper.js** para carruseles de imágenes/ejemplos de dibujos.
  - **Fuse.js** para un buscador inteligente de comandos y temas.

### 3. Estructura y arquitectura de la información
La web debe organizarse en niveles progresivos, tipo "ruta de aprendizaje":

1. **Inicio / Home**
   - Hero con explicación breve de qué es AutoCAD y para qué sirve.
   - Botones CTA: "Empezar desde cero", "Ir a Comandos", "Ver Recursos Gratuitos".
   - Barra de progreso o roadmap visual del curso.

2. **Nivel 1 — Fundamentos (Básico)**
   - ¿Qué es AutoCAD y para qué se usa? (arquitectura, ingeniería, diseño industrial).
   - Instalación, requisitos del sistema y tipos de licencia.
   - Interfaz de usuario: cinta de opciones (ribbon), barra de herramientas, línea de comandos, espacio de trabajo.
   - Sistema de coordenadas (cartesianas, polares, absolutas, relativas).
   - Configuración inicial: unidades, formato de dibujo, capas base.

3. **Nivel 2 — Dibujo 2D**
   - Herramientas de dibujo: línea, polilínea, círculo, arco, rectángulo, polígono, spline, elipse.
   - Herramientas de modificación: mover, copiar, rotar, escalar, recortar, alargar, desfase (offset), simetría (mirror), matriz (array), empalme (fillet), chaflán (chamfer).
   - Precisión: referencia a objetos (OSNAP), rastreo polar, orto, cuadrícula (grid/snap).
   - Capas (layers): creación, propiedades, colores, tipos de línea, grosores.
   - Bloques y atributos.
   - Acotación (dimensiones) y estilos de cota.
   - Texto y estilos de texto, tablas.
   - Sombreado (hatch) y rellenos.

4. **Nivel 3 — Organización y productividad**
   - Espacio modelo vs espacio papel (layouts).
   - Ventanas gráficas (viewports) y escalas.
   - Plantillas (.dwt) y estándares de dibujo.
   - Impresión y exportación (PDF, DWF, DXF).
   - Gestión de archivos externos (Xref).
   - Atajos de teclado y comandos rápidos (tabla completa descargable).

5. **Nivel 4 — Modelado 3D**
   - Espacio de trabajo 3D y navegación (orbit, pan, zoom, vistas).
   - Sólidos básicos (caja, cilindro, esfera, cono, cuña, pirámide).
   - Operaciones booleanas (unión, resta, intersección).
   - Extrusión, revolución, barrido (sweep), solevación (loft).
   - Edición de sólidos y superficies.
   - Renderizado básico: materiales, luces, cámaras.

6. **Nivel 5 — Nivel experto / Avanzado**
   - Personalización de la interfaz (CUI), creación de comandos personalizados.
   - Introducción a AutoLISP y scripts básicos.
   - Estándares CAD profesionales (normas ISO, ANSI, DIN según el país).
   - Buenas prácticas de dibujo profesional (nomenclatura de capas, organización de proyectos).
   - Integración con otros programas (Revit, SketchUp, Civil 3D).
   - Optimización de archivos y solución de errores comunes.

7. **Sección: Comandos** (tipo diccionario/buscador)
   - Buscador en tiempo real.
   - Tarjetas o tabla con: nombre del comando, atajo, ícono, descripción corta, categoría (dibujo, modificación, acotación, etc.), y ejemplo visual (GIF/imagen).
   - Filtros por categoría y nivel (básico/intermedio/avanzado).

8. **Sección: Recursos Gratuitos**
   - Listado organizado (con tarjetas) de páginas web, canales de YouTube, foros y bibliotecas de bloques CAD gratuitos.
   - Categorías sugeridas: Bloques y planos DWG gratis, Cursos y tutoriales, Comunidades y foros, Plantillas descargables, Canales de YouTube recomendados, Certificaciones gratuitas.
   - Cada recurso con: nombre, breve descripción, ícono/categoría, enlace externo (target="_blank"), y etiqueta de idioma (ES/EN).

9. **Sección: Preguntas Frecuentes (FAQ)**
   - Acordeón con dudas comunes (versiones, requisitos, diferencias con otros CAD, licencias estudiantiles, etc.).

10. **Footer**
    - Enlaces rápidos, redes sociales, aviso de que es contenido educativo/no oficial, créditos.

### 4. Requisitos de diseño (UI/UX)
- Diseño moderno, limpio, tipo "documentación técnica" (inspirado en sitios como MDN Web Docs o documentaciones de Bootstrap), pero con identidad propia relacionada al mundo del dibujo técnico (colores tipo azul plano/ingeniería, grises, acentos en naranja o amarillo tipo "capas CAD").
- Modo claro y modo oscuro.
- Navbar fija con menú desplegable por niveles/secciones y buscador integrado.
- Sidebar de navegación tipo "índice" en las páginas de contenido largo (scroll-spy con Bootstrap).
- Barra de progreso de lectura/aprendizaje.
- Tarjetas (cards) para mostrar comandos, recursos y ejercicios.
- Uso de imágenes, capturas de pantalla o gifs ilustrativos en cada explicación (dejar placeholders `<!-- IMG: descripción -->` donde corresponda).
- Botones de "Anterior / Siguiente tema" al final de cada sección para guiar el recorrido de aprendizaje.
- Totalmente **responsivo**: mobile-first, adaptado a móviles, tablets, laptops y pantallas grandes, usando el sistema de grillas de Bootstrap y media queries adicionales si es necesario.
- Accesibilidad: contraste adecuado, textos alternativos en imágenes, navegación por teclado.

### 5. Funcionalidades JavaScript esperadas
- Buscador global de contenidos y comandos.
- Filtro dinámico de recursos por categoría.
- Modo oscuro/claro con persistencia en localStorage.
- Marcado de temas como "completados" (checklist de progreso guardado en localStorage).
- Scroll-spy para resaltar la sección activa en el índice lateral.
- Animaciones suaves al hacer scroll (AOS u otra librería).
- Botón "volver arriba".

### 6. Entregable esperado
- Estructura de carpetas ordenada: `/index.html`, `/paginas/`, `/css/`, `/js/`, `/img/`, `/assets/`.
- Código comentado y organizado por secciones.
- Uso de componentes reutilizables de Bootstrap adaptados con CSS propio (evitar que se vea "genérico").
- Al menos una página de ejemplo completamente desarrollada por cada nivel (Home, un tema de Nivel 1, la sección de Comandos y la sección de Recursos Gratuitos), para luego replicar el patrón en el resto de contenidos.

---

¿Quieres que ahora te genere directamente el código base (HTML + Bootstrap + CSS + JS) de esta web siguiendo este prompt?
