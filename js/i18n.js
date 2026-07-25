/* =========================================================
   AutoCAD Guía — i18n.js
   Sistema de internacionalización ES ↔ EN.
   ========================================================= */

(function(){
  'use strict';

  var STORAGE_KEY = 'autocad-guia-lang';

  var I18N = {
    es: {
      /* ---- Navbar ---- */
      'brand.sub': 'Guía · Teoría &amp; Práctica',
      'nav.home': 'Inicio',
      'nav.levels': 'Niveles',
      'nav.commands': 'Comandos',
      'nav.resources': 'Recursos gratis',
      'nav.faq': 'FAQ',
      'nav.lang': 'EN',

      /* ---- Common UI ---- */
      'ui.search': 'Buscar',
      'ui.theme': 'Cambiar tema',
      'ui.lang': 'Cambiar idioma',
      'ui.back': 'Volver arriba',
      'ui.nextLevel': 'Siguiente nivel',
      'ui.next': 'Siguiente',
      'ui.prev': 'Anterior',
      'ui.markDone': 'Marcar tema como visto',
      'ui.done': 'Tema completado',
      'ui.copy': 'Copiar',
      'ui.copied': '¡Copiado!',
      'ui.command': 'Comando:',
      'ui.hide': 'Ocultar',
      'ui.inThisLevel': 'En este nivel',
      'ui.showing': 'Mostrando',
      'ui.commands': 'comandos',
      'ui.command_single': 'comando',
      'ui.noCommands': 'No se encontraron comandos con ese nombre o atajo.',
      'ui.noResults': 'No se encontraron resultados para',
      'ui.typeToSearch': 'Escribe al menos 2 caracteres para buscar...',
      'ui.searchUnavailable': 'Buscador no disponible.',
      'ui.searchPlaceholder': 'Buscar comandos, temas, conceptos...',
      'ui.cmdPlaceholder': 'Escribe un comando o atajo (LINE, OFFSET, TRIM...)',
      'ui.downloadTxt': 'Descargar .TXT',
      'ui.downloadDesc': 'Descarga esta tabla en formato de texto plano',

      /* ---- Progress ---- */
      'progress.xOfY': '{done} de {total} temas completados · {pct}%',

      /* ---- Command line tips ---- */
      'tip.1': 'Consejo: pulsa la tecla ORTO (F8) para dibujar líneas perfectamente horizontales o verticales.',
      'tip.2': 'Consejo: usa OFFSET (O) para duplicar muros o líneas a una distancia exacta.',
      'tip.3': 'Consejo: activa las referencias a objetos (F3) para hacer clic con precisión sobre puntos existentes.',
      'tip.4': 'Consejo: guarda tus capas base en una plantilla .DWT para no repetir configuración en cada proyecto.',
      'tip.5': 'Consejo: el comando MATRIZ (AR) repite objetos en filas, columnas o de forma circular.',
      'tip.6': 'Consejo: revisa la sección de Comandos para buscar cualquier herramienta por nombre o atajo.',
      'tip.7': 'Consejo: usa LAYISO para aislar una capa y trabajar sin distracciones visuales.',
      'tip.8': 'Consejo: el comando PURGE elimina elementos no usados y reduce el tamaño del archivo.',

      /* ---- Footer ---- */
      'footer.levels': 'Niveles',
      'footer.guide': 'Guía',
      'footer.follow': 'Síguenos',
      'footer.disclaimer': 'Contenido educativo independiente. No es un sitio oficial de Autodesk®; AutoCAD® es una marca registrada de Autodesk, Inc.',
      'footer.copyright': '© 2026 AutoCAD Guía. Proyecto educativo de aprendizaje libre.',

      /* ---- Home page ---- */
      'home.brand.sub': 'Guía · Teoría & Práctica',
      'home.hero.eyebrow': 'Guía completa · Nivel 1 a Nivel 5',
      'home.hero.title': 'Domina AutoCAD desde <em>la primera línea</em> hasta el plano maestro.',
      'home.hero.desc': 'Teoría clara, comandos explicados y una ruta de aprendizaje ordenada para dibujar en 2D, modelar en 3D y trabajar como un profesional del CAD. Ideal para aprender desde cero o repasar un tema puntual.',
      'home.hero.start': 'Empezar desde cero',
      'home.hero.goCmds': 'Ir a comandos',
      'home.preview.eyebrow': 'Diccionario de comandos',
      'home.preview.title': 'Los comandos más usados, a un clic',
      'home.preview.all': 'Ver todos los comandos',
      'home.roadmap.eyebrow': 'Ruta de aprendizaje',
      'home.roadmap.title': 'Cinco niveles, un mismo dibujo cada vez más preciso',
      'home.roadmap.desc': 'Sigue el orden si empiezas desde cero, o salta directo al nivel que necesitas repasar.',
      'home.features.eyebrow': 'Por qué esta guía',
      'home.features.title': 'Pensada tanto para aprender como para consultar',
      'home.feature1.title': 'Ruta ordenada',
      'home.feature1.desc': 'Contenido dividido en niveles progresivos, sin saltos ni supuestos previos.',
      'home.feature2.title': 'Búsqueda rápida',
      'home.feature2.desc': 'Encuentra un comando o un concepto puntual sin leer todo el temario.',
      'home.feature3.title': 'Recursos gratuitos',
      'home.feature3.desc': 'Bloques, plantillas y cursos gratuitos seleccionados y clasificados.',
      'home.res.eyebrow': 'Recursos gratuitos',
      'home.res.title': 'Bloques, plantillas y cursos sin costo',
      'home.cta.eyebrow': 'Empieza ahora',
      'home.cta.title': 'Tu primer plano puede empezar hoy mismo',
      'home.cta.desc': 'Sin cuentas, sin costos. Solo abre el Nivel 1 y comienza.',
      'home.cta.btn': 'Ir al Nivel 1',

      /* ---- Level cards ---- */
      'lvl1.card.tag': 'Básico',
      'lvl1.card.title': 'Fundamentos',
      'lvl1.card.desc': 'Interfaz, instalación, coordenadas y configuración inicial del programa.',
      'lvl2.card.tag': 'Básico–Intermedio',
      'lvl2.card.title': 'Dibujo 2D',
      'lvl2.card.desc': 'Herramientas de dibujo, modificación, precisión, capas, cotas y texto.',
      'lvl3.card.tag': 'Intermedio',
      'lvl3.card.title': 'Organización y productividad',
      'lvl3.card.desc': 'Presentaciones, ventanas gráficas, plantillas, impresión y Xref.',
      'lvl4.card.tag': 'Avanzado',
      'lvl4.card.title': 'Modelado 3D',
      'lvl4.card.desc': 'Sólidos, operaciones booleanas, extrusión, superficies y render básico.',
      'lvl5.card.tag': 'Experto',
      'lvl5.card.title': 'Nivel experto',
      'lvl5.card.desc': 'Personalización, AutoLISP, estándares CAD y flujo con otros programas.',
      'lvlCmd.card.tag': 'Consulta',
      'lvlCmd.card.title': 'Diccionario de comandos',
      'lvlCmd.card.desc': 'Busca cualquier comando, su atajo y su uso en segundos.',

      /* ---- Level 1 ---- */
      'lvl1.breadcrumb': 'Inicio',
      'lvl1.eyebrow': 'Nivel 01 · Básico',
      'lvl1.title': 'Fundamentos de AutoCAD',
      'lvl1.subtitle': 'Antes de dibujar una sola línea, entiende qué es el programa, cómo instalarlo, cómo está organizada su interfaz y cómo funciona su sistema de coordenadas. Esta base evita el 80% de los errores de un principiante.',
      'lvl1.s1.title': '¿Qué es AutoCAD y para qué se usa?',
      'lvl1.s1.p1': '<strong>AutoCAD</strong> es un programa de diseño asistido por computadora (CAD, por sus siglas en inglés) desarrollado por Autodesk, usado para crear dibujos técnicos precisos en dos dimensiones (2D) y modelos en tres dimensiones (3D). A diferencia de un programa de dibujo artístico, AutoCAD trabaja con coordenadas exactas y unidades reales: un muro de 3 metros se dibuja midiendo exactamente 3 metros dentro del archivo.',
      'lvl1.s1.p2': 'Se utiliza principalmente en cuatro grandes áreas:',
      'lvl1.s1.li1': '<strong>Arquitectura:</strong> planos de plantas, cortes, fachadas y detalles constructivos.',
      'lvl1.s1.li2': '<strong>Ingeniería civil y estructural:</strong> planos de cimentación, estructuras metálicas y de concreto.',
      'lvl1.s1.li3': '<strong>Ingeniería mecánica e industrial:</strong> piezas, ensambles y planos de fabricación.',
      'lvl1.s1.li4': '<strong>Diseño eléctrico y de instalaciones:</strong> diagramas unifilares, redes eléctricas, sanitarias y de gas.',
      'lvl1.s1.callout.title': 'Idea clave',
      'lvl1.s1.callout.body': 'Todo lo que dibujas en AutoCAD se hace a <strong>escala real 1:1</strong> en el "espacio modelo". La escala solo se aplica después, al momento de imprimir o presentar el plano.',
      'lvl1.s2.title': 'Instalación, requisitos y tipos de licencia',
      'lvl1.s3.title': 'Interfaz de usuario',
      'lvl1.s4.title': 'Sistema de coordenadas',
      'lvl1.s5.title': 'Configuración inicial de un dibujo',
      'lvl1.nav.next': 'Siguiente nivel · Dibujo 2D',

      /* ---- Level 2 ---- */
      'lvl2.eyebrow': 'Nivel 02 · Básico–Intermedio',
      'lvl2.title': 'Dibujo 2D',
      'lvl2.subtitle': 'El corazón de AutoCAD: cómo crear geometría, modificarla con precisión, organizarla en capas, reutilizarla con bloques y documentarla con cotas, texto y sombreados.',
      'lvl2.s1.title': 'Herramientas de dibujo',
      'lvl2.s2.title': 'Herramientas de modificación',
      'lvl2.s3.title': 'Precisión: referencias, rastreo y cuadrícula',
      'lvl2.s4.title': 'Capas (Layers)',
      'lvl2.s5.title': 'Bloques y atributos',
      'lvl2.s6.title': 'Acotación (dimensiones)',
      'lvl2.s7.title': 'Texto, estilos de texto y tablas',
      'lvl2.s8.title': 'Sombreado y rellenos (Hatch)',
      'lvl2.nav.prev': 'Nivel 1 · Fundamentos',
      'lvl2.nav.next': 'Nivel 3 · Organización',

      /* ---- Level 3 ---- */
      'lvl3.eyebrow': 'Nivel 03 · Intermedio',
      'lvl3.title': 'Organización y productividad',
      'lvl3.subtitle': 'Cómo preparar un dibujo para imprimirlo o compartirlo correctamente: presentaciones, escalas, plantillas, exportación, archivos externos y los atajos que aceleran todo el flujo de trabajo.',
      'lvl3.s1.title': 'Espacio modelo vs. espacio papel (Layouts)',
      'lvl3.s2.title': 'Ventanas gráficas (Viewports) y escalas',
      'lvl3.s3.title': 'Plantillas (.DWT) y estándares de dibujo',
      'lvl3.s4.title': 'Impresión y exportación',
      'lvl3.s5.title': 'Gestión de archivos externos (Xref)',
      'lvl3.s6.title': 'Atajos de teclado y comandos rápidos',
      'lvl3.nav.prev': 'Nivel 2 · Dibujo 2D',
      'lvl3.nav.next': 'Nivel 4 · Modelado 3D',

      /* ---- Level 4 ---- */
      'lvl4.eyebrow': 'Nivel 04 · Avanzado',
      'lvl4.title': 'Modelado 3D',
      'lvl4.subtitle': 'Del plano a la maqueta virtual: navegación tridimensional, sólidos primitivos, operaciones booleanas, herramientas de creación avanzada y un primer acercamiento al render.',
      'lvl4.s1.title': 'Espacio de trabajo 3D y navegación',
      'lvl4.s2.title': 'Sólidos básicos (primitivas)',
      'lvl4.s3.title': 'Operaciones booleanas',
      'lvl4.s4.title': 'Extrusión, revolución, barrido y solevación',
      'lvl4.s5.title': 'Edición de sólidos y superficies',
      'lvl4.s6.title': 'Renderizado básico',
      'lvl4.nav.prev': 'Nivel 3 · Organización',
      'lvl4.nav.next': 'Nivel 5 · Avanzado',

      /* ---- Level 5 ---- */
      'lvl5.eyebrow': 'Nivel 05 · Experto',
      'lvl5.title': 'Nivel experto',
      'lvl5.subtitle': 'Personaliza AutoCAD a tu medida, automatiza tareas con scripts, aplica estándares profesionales y integra el programa con otros flujos de trabajo del mundo real.',
      'lvl5.s1.title': 'Personalización de la interfaz (CUI)',
      'lvl5.s2.title': 'AutoLISP y scripts básicos',
      'lvl5.s3.title': 'Estándares CAD profesionales',
      'lvl5.s4.title': 'Buenas prácticas de dibujo profesional',
      'lvl5.s5.title': 'Integración con otros programas',
      'lvl5.s6.title': 'Optimización de archivos y solución de errores',
      'lvl5.nav.prev': 'Nivel 4 · Modelado 3D',
      'lvl5.nav.next': 'Diccionario de comandos',

      /* ---- Commands page ---- */
      'cmd.eyebrow': 'Diccionario de comandos',
      'cmd.hero.title': 'Busca cualquier comando',
      'cmd.hero.desc': 'Escribe el nombre o el atajo de un comando y encuentra al instante su uso, categoría y nivel.',
      'cmd.filter.all': 'Todos',
      'cmd.filter.dibujo': 'Dibujo',
      'cmd.filter.modificacion': 'Modificación',
      'cmd.filter.precision': 'Precisión',
      'cmd.filter.capas': 'Capas',
      'cmd.filter.acotacion': 'Acotación',
      'cmd.filter.texto': 'Texto',
      'cmd.filter.bloques': 'Bloques',
      'cmd.filter.3d': '3D',
      'cmd.filter.edicion': 'Edición',
      'cmd.filter.consulta': 'Consulta',

      /* ---- Command descriptions ---- */
      'cmd.line.desc': 'Dibuja segmentos de línea recta entre puntos definidos por coordenadas o clics.',
      'cmd.line.es': 'LÍNEA',
      'cmd.pline.desc': 'Serie de segmentos rectos y curvos unidos como un solo objeto polilínea.',
      'cmd.pline.es': 'POLILÍNEA',
      'cmd.circle.desc': 'Dibuja un círculo por centro-radio, dos puntos, tres puntos u otras opciones.',
      'cmd.circle.es': 'CÍRCULO',
      'cmd.arc.desc': 'Tramo curvo definido por 3 puntos, centro-inicio-fin, u otras combinaciones.',
      'cmd.arc.es': 'ARCO',
      'cmd.rectang.desc': 'Dibuja un rectángulo a partir de dos esquinas opuestas.',
      'cmd.rectang.es': 'RECTÁNGULO',
      'cmd.polygon.desc': 'Polígono regular inscrito o circunscrito en un círculo.',
      'cmd.polygon.es': 'POLÍGONO',
      'cmd.ellipse.desc': 'Curva elíptica definida por eje mayor/menor o por centro.',
      'cmd.ellipse.es': 'ELIPSE',
      'cmd.spline.desc': 'Curva suave que pasa por una serie de puntos de control.',
      'cmd.move.desc': 'Traslada objetos de un punto base a un punto destino.',
      'cmd.move.es': 'MOVER',
      'cmd.copy.desc': 'Crea copias de objetos sin eliminar el original.',
      'cmd.copy.es': 'COPIAR',
      'cmd.rotate.desc': 'Gira objetos un ángulo respecto a un punto base.',
      'cmd.rotate.es': 'ROTAR',
      'cmd.scale.desc': 'Aumenta o reduce el tamaño de objetos respecto a un punto base.',
      'cmd.scale.es': 'ESCALAR',
      'cmd.trim.desc': 'Recorta objetos hasta el límite de otro objeto de referencia.',
      'cmd.trim.es': 'RECORTAR',
      'cmd.extend.desc': 'Extiende un objeto hasta tocar un límite de referencia.',
      'cmd.extend.es': 'EXTENDER',
      'cmd.offset.desc': 'Crea una copia paralela de un objeto a una distancia exacta.',
      'cmd.offset.es': 'DESFASE',
      'cmd.mirror.desc': 'Refleja objetos respecto a un eje simétrico definido por dos puntos.',
      'cmd.mirror.es': 'ESPEJO',
      'cmd.array.desc': 'Repite objetos en filas/columnas, en círculo o a lo largo de una ruta.',
      'cmd.array.es': 'MATRIZ',
      'cmd.fillet.desc': 'Une dos líneas con un arco de radio definido (empalme).',
      'cmd.fillet.es': 'EMPALME',
      'cmd.chamfer.desc': 'Une dos líneas con un corte recto en la esquina (chaflán).',
      'cmd.chamfer.es': 'CHAFLETE',
      'cmd.stretch.desc': 'Estira o comprime objetos moviendo vértices dentro de una selección cruzada.',
      'cmd.stretch.es': 'ESTIRAR',
      'cmd.explode.desc': 'Descompone un bloque, polilínea o array en sus objetos individuales.',
      'cmd.explode.es': 'DESCOMPONER',
      'cmd.join.desc': 'Une líneas o arcos contiguos en un solo objeto (lo opuesto a EXPLODE).',
      'cmd.join.es': 'UNIR',
      'cmd.break.desc': 'Rompe un objeto en dos partes o elimina un segmento entre dos puntos.',
      'cmd.break.es': 'ROMPER',
      'cmd.matchprop.desc': 'Copia propiedades (capa, color, tipo de línea) de un objeto a otro.',
      'cmd.matchprop.es': 'COPYPROP',
      'cmd.osnap.desc': 'Alterna las referencias a objetos: extremo, medio, centro, intersección, etc.',
      'cmd.osnap.es': 'REFERENCIA A OBJETOS',
      'cmd.layer.desc': 'Abre el Administrador de capas para crear, editar y gestionar capas.',
      'cmd.layer.es': 'CAPA',
      'cmd.layiso.desc': 'Aísla la capa de un objeto seleccionado, ocultando todas las demás.',
      'cmd.layuniso.desc': 'Restaura el estado de visibilidad de capas anterior a LAYISO.',
      'cmd.block.desc': 'Crea un bloque a partir de objetos seleccionados, definiendo nombre y punto base.',
      'cmd.block.es': 'BLOQUE',
      'cmd.insert.desc': 'Inserta un bloque existente en el dibujo actual.',
      'cmd.insert.es': 'INSERTAR',
      'cmd.bedit.desc': 'Abre el editor de bloques para modificar el contenido de un bloque definido.',
      'cmd.dimlinear.desc': 'Crea una cota lineal horizontal o vertical entre dos puntos.',
      'cmd.dimaligned.desc': 'Cota paralela a una línea inclinada.',
      'cmd.dim.desc': 'Cota inteligente que detecta automáticamente el tipo según el objeto seleccionado.',
      'cmd.dimstyle.desc': 'Administra estilos de cota: tamaño de texto, flechas, unidades y precisión.',
      'cmd.text.desc': 'Texto de una sola línea, útil para etiquetas cortas y títulos.',
      'cmd.text.es': 'TEXTO',
      'cmd.mtext.desc': 'Texto multilínea con formato rich text dentro de un cuadro definido.',
      'cmd.mtext.es': 'TEXTO MULTILÍNEA',
      'cmd.style.desc': 'Define fuente, altura y estilo por defecto para los textos del dibujo.',
      'cmd.table.desc': 'Inserta tablas de datos con filas y columnas (cuadro de acabados, áreas, etc.).',
      'cmd.hatch.desc': 'Rellena un área cerrada con un patrón de sombreado (rayado, sólido, material).',
      'cmd.hatch.es': 'SOMBREADO',
      'cmd.pedit.desc': 'Edita polilíneas: unir segmentos, abrir/cerrar, suavizar o asignar ancho.',
      'cmd.properties.desc': 'Abre la paleta de propiedades para ver y editar atributos de objetos seleccionados.',
      'cmd.properties.es': 'PROPIEDADES',
      'cmd.box.desc': 'Crea un sólido rectangular definido por largo, ancho y alto.',
      'cmd.box.es': 'CAJA',
      'cmd.cylinder.desc': 'Crea un sólido cilíndrico por radio de base y altura.',
      'cmd.cylinder.es': 'CILINDRO',
      'cmd.extrude.desc': 'Empuja un perfil 2D cerrado en línea recta para crear un sólido.',
      'cmd.extrude.es': 'EXTRUIR',
      'cmd.revolve.desc': 'Gira un perfil 2D alrededor de un eje para generar un sólido de revolución.',
      'cmd.revolve.es': 'REVOLVER',
      'cmd.sweep.desc': 'Desplaza un perfil a lo largo de una trayectoria curva (tubería, moldura).',
      'cmd.sweep.es': 'BARRIDO',
      'cmd.loft.desc': 'Genera una forma suave conectando dos o más perfiles entre sí (solevación).',
      'cmd.loft.es': 'SOLEVACIÓN',
      'cmd.union.desc': 'Fusiona dos o más sólidos en un solo objeto (unión booleana).',
      'cmd.union.es': 'UNIÓN',
      'cmd.subtract.desc': 'Resta el volumen de un sólido de otro (perforar, recortar volumen).',
      'cmd.subtract.es': 'RESTA',
      'cmd.intersect.desc': 'Conserva únicamente el volumen común entre dos o más sólidos.',
      'cmd.intersect.es': 'INTERSECCIÓN',
      'cmd.3dorbit.desc': 'Órbita libre alrededor del modelo 3D para visualizar desde cualquier ángulo.',
      'cmd.render.desc': 'Genera una imagen renderizada del modelo 3D con materiales, luces y cámara.',
      'cmd.dist.desc': 'Mide la distancia y ángulo entre dos puntos del dibujo.',
      'cmd.list.desc': 'Muestra propiedades detalladas de un objeto seleccionado (capa, tipo, área, longitud).',
      'cmd.area.desc': 'Calcula el área y perímetro de un polígono o selección de puntos.',
      'cmd.measure.desc': 'Coloca puntos o bloques a lo largo de un objeto a intervalos iguales.',
      'cmd.zoom.desc': 'Amplía o reduce la vista del área de dibujo (opciones: E, W, P, All).',
      'cmd.purge.desc': 'Elimina elementos no utilizados del archivo: capas, bloques, estilos, tipos de línea.',
      'cmd.audit.desc': 'Detecta y corrige errores internos del archivo DWG.',
      'cmd.wblock.desc': 'Exporta objetos o el dibujo completo a un archivo DWG separado.',

      /* ---- Resources page ---- */
      'res.eyebrow': 'Recursos gratuitos',
      'res.hero.title': 'Bloques, cursos y plantillas sin costo',
      'res.hero.desc': 'Selección de bibliotecas de bloques, canales de YouTube, foros y herramientas gratuitas para potenciar tu trabajo en AutoCAD.',
      'res.filter.all': 'Todos',
      'res.filter.bloques': 'Bloques DWG',
      'res.filter.cursos': 'Cursos y tutoriales',
      'res.filter.comunidades': 'Comunidades y foros',
      'res.filter.plantillas': 'Plantillas',
      'res.filter.youtube': 'Canales YouTube',
      'res.filter.herramientas': 'Herramientas',
      'res.visit': 'Visitar sitio',
      'res.forum': 'Visitar foro',
      'res.subreddit': 'Visitar subreddit',
      'res.channel': 'Visitar canal',
      'res.download': 'Descargar',
      'res.searchYT': 'Buscar en YouTube',

      /* ---- FAQ page ---- */
      'faq.eyebrow': 'Preguntas frecuentes',
      'faq.hero.title': 'Dudas comunes sobre AutoCAD',
      'faq.hero.desc': 'Respuestas a las preguntas más frecuentes de quienes empiezan o quieren profundizar en AutoCAD.',
      'faq.cta.eyebrow': '¿Tienes más dudas?',
      'faq.cta.title': 'Revisa los niveles o el diccionario de comandos',
      'faq.cta.desc': 'Si tu pregunta no está aquí, probablemente encuentres la respuesta en nuestro contenido o buscando el comando específico.',
      'faq.cta.cmds': 'Ver comandos',
      'faq.cta.start': 'Empezar desde cero',

      /* ---- Spanish command names for comandos page ---- */
      'cmd.cat.dibujo': 'Dibujo',
      'cmd.cat.modificacion': 'Modificación',
      'cmd.cat.precision': 'Precisión',
      'cmd.cat.capas': 'Capas',
      'cmd.cat.acotacion': 'Acotación',
      'cmd.cat.texto': 'Texto',
      'cmd.cat.bloques': 'Bloques',
      'cmd.cat.3d': '3D',
      'cmd.cat.edicion': 'Edición',
      'cmd.cat.consulta': 'Consulta',
      'cmd.level.basico': 'Básico',
      'cmd.level.intermedio': 'Intermedio',
      'cmd.level.avanzado': 'Avanzado'
    },

    en: {
      /* ---- Navbar ---- */
      'brand.sub': 'Guide · Theory &amp; Practice',
      'nav.home': 'Home',
      'nav.levels': 'Levels',
      'nav.commands': 'Commands',
      'nav.resources': 'Free Resources',
      'nav.faq': 'FAQ',
      'nav.lang': 'ES',

      /* ---- Common UI ---- */
      'ui.search': 'Search',
      'ui.theme': 'Toggle theme',
      'ui.lang': 'Toggle language',
      'ui.back': 'Back to top',
      'ui.nextLevel': 'Next level',
      'ui.next': 'Next',
      'ui.prev': 'Previous',
      'ui.markDone': 'Mark topic as completed',
      'ui.done': 'Topic completed',
      'ui.copy': 'Copy',
      'ui.copied': 'Copied!',
      'ui.command': 'Command:',
      'ui.hide': 'Hide',
      'ui.inThisLevel': 'In this level',
      'ui.showing': 'Showing',
      'ui.commands': 'commands',
      'ui.command_single': 'command',
      'ui.noCommands': 'No commands found with that name or shortcut.',
      'ui.noResults': 'No results found for',
      'ui.typeToSearch': 'Type at least 2 characters to search...',
      'ui.searchUnavailable': 'Search unavailable.',
      'ui.searchPlaceholder': 'Search commands, topics, concepts...',
      'ui.cmdPlaceholder': 'Type a command or shortcut (LINE, OFFSET, TRIM...)',
      'ui.downloadTxt': 'Download .TXT',
      'ui.downloadDesc': 'Download this table as plain text',

      /* ---- Progress ---- */
      'progress.xOfY': '{done} of {total} topics completed · {pct}%',

      /* ---- Command line tips ---- */
      'tip.1': 'Tip: press ORTHO (F8) to draw perfectly horizontal or vertical lines.',
      'tip.2': 'Tip: use OFFSET (O) to duplicate walls or lines at an exact distance.',
      'tip.3': 'Tip: enable object snapping (F3) to click precisely on existing points.',
      'tip.4': 'Tip: save your base layers in a .DWT template to avoid repeating setup in every project.',
      'tip.5': 'Tip: the ARRAY (AR) command repeats objects in rows, columns, or in a circle.',
      'tip.6': 'Tip: check the Commands section to search for any tool by name or shortcut.',
      'tip.7': 'Tip: use LAYISO to isolate a layer and work without visual distractions.',
      'tip.8': 'Tip: the PURGE command removes unused elements and reduces file size.',

      /* ---- Footer ---- */
      'footer.levels': 'Levels',
      'footer.guide': 'Guide',
      'footer.follow': 'Follow us',
      'footer.disclaimer': 'Independent educational content. Not an official Autodesk® site; AutoCAD® is a registered trademark of Autodesk, Inc.',
      'footer.copyright': '© 2026 AutoCAD Guide. Free learning educational project.',

      /* ---- Home page ---- */
      'home.brand.sub': 'Guide · Theory & Practice',
      'home.hero.eyebrow': 'Complete guide · Level 1 to Level 5',
      'home.hero.title': 'Master AutoCAD from <em>the first line</em> to the master plan.',
      'home.hero.desc': 'Clear theory, explained commands, and an organized learning path for 2D drafting, 3D modeling, and professional CAD work. Perfect for learning from scratch or reviewing a specific topic.',
      'home.hero.start': 'Start from scratch',
      'home.hero.goCmds': 'Go to commands',
      'home.preview.eyebrow': 'Command dictionary',
      'home.preview.title': 'Most used commands, one click away',
      'home.preview.all': 'View all commands',
      'home.roadmap.eyebrow': 'Learning path',
      'home.roadmap.title': 'Five levels, one drawing getting more precise each time',
      'home.roadmap.desc': 'Follow the order if you\'re starting from scratch, or jump directly to the level you need to review.',
      'home.features.eyebrow': 'Why this guide',
      'home.features.title': 'Designed for both learning and reference',
      'home.feature1.title': 'Organized path',
      'home.feature1.desc': 'Content divided into progressive levels, with no gaps or assumed prior knowledge.',
      'home.feature2.title': 'Quick search',
      'home.feature2.desc': 'Find a command or specific concept without reading the entire curriculum.',
      'home.feature3.title': 'Free resources',
      'home.feature3.desc': 'Blocks, templates, and free courses selected and categorized.',
      'home.res.eyebrow': 'Free resources',
      'home.res.title': 'Blocks, templates, and courses at no cost',
      'home.cta.eyebrow': 'Start now',
      'home.cta.title': 'Your first drawing can start today',
      'home.cta.desc': 'No accounts, no costs. Just open Level 1 and begin.',
      'home.cta.btn': 'Go to Level 1',

      /* ---- Level cards ---- */
      'lvl1.card.tag': 'Basic',
      'lvl1.card.title': 'Fundamentals',
      'lvl1.card.desc': 'Interface, installation, coordinates, and initial program setup.',
      'lvl2.card.tag': 'Basic–Intermediate',
      'lvl2.card.title': '2D Drafting',
      'lvl2.card.desc': 'Drawing tools, modification, precision, layers, dimensions, and text.',
      'lvl3.card.tag': 'Intermediate',
      'lvl3.card.title': 'Organization & productivity',
      'lvl3.card.desc': 'Layouts, viewports, templates, printing, and Xrefs.',
      'lvl4.card.tag': 'Advanced',
      'lvl4.card.title': '3D Modeling',
      'lvl4.card.desc': 'Solids, boolean operations, extrusion, surfaces, and basic rendering.',
      'lvl5.card.tag': 'Expert',
      'lvl5.card.title': 'Expert level',
      'lvl5.card.desc': 'Customization, AutoLISP, CAD standards, and workflow integration.',
      'lvlCmd.card.tag': 'Reference',
      'lvlCmd.card.title': 'Command dictionary',
      'lvlCmd.card.desc': 'Search any command, its shortcut, and its use in seconds.',

      /* ---- Level 1 ---- */
      'lvl1.breadcrumb': 'Home',
      'lvl1.eyebrow': 'Level 01 · Basic',
      'lvl1.title': 'AutoCAD Fundamentals',
      'lvl1.subtitle': 'Before drawing a single line, understand what the program is, how to install it, how its interface is organized, and how its coordinate system works. This foundation prevents 80% of beginner errors.',
      'lvl1.s1.title': 'What is AutoCAD and what is it used for?',
      'lvl1.s1.p1': '<strong>AutoCAD</strong> is a computer-aided design (CAD) program developed by Autodesk, used to create precise technical drawings in two dimensions (2D) and models in three dimensions (3D). Unlike an artistic drawing program, AutoCAD works with exact coordinates and real units: a 3-meter wall is drawn measuring exactly 3 meters within the file.',
      'lvl1.s1.p2': 'It is mainly used in four major areas:',
      'lvl1.s1.li1': '<strong>Architecture:</strong> floor plans, sections, facades, and construction details.',
      'lvl1.s1.li2': '<strong>Civil and structural engineering:</strong> foundation plans, steel and concrete structures.',
      'lvl1.s1.li3': '<strong>Mechanical and industrial engineering:</strong> parts, assemblies, and manufacturing drawings.',
      'lvl1.s1.li4': '<strong>Electrical and installation design:</strong> single-line diagrams, electrical, plumbing, and gas networks.',
      'lvl1.s1.callout.title': 'Key idea',
      'lvl1.s1.callout.body': 'Everything you draw in AutoCAD is done at <strong>real 1:1 scale</strong> in "model space". Scale is only applied later, when printing or presenting the drawing.',
      'lvl1.s2.title': 'Installation, requirements, and license types',
      'lvl1.s3.title': 'User interface',
      'lvl1.s4.title': 'Coordinate system',
      'lvl1.s5.title': 'Initial drawing setup',
      'lvl1.nav.next': 'Next level · 2D Drafting',

      /* ---- Level 2 ---- */
      'lvl2.eyebrow': 'Level 02 · Basic–Intermediate',
      'lvl2.title': '2D Drafting',
      'lvl2.subtitle': 'The heart of AutoCAD: how to create geometry, modify it precisely, organize it into layers, reuse it with blocks, and document it with dimensions, text, and hatches.',
      'lvl2.s1.title': 'Drawing tools',
      'lvl2.s2.title': 'Modification tools',
      'lvl2.s3.title': 'Precision: snaps, tracking, and grid',
      'lvl2.s4.title': 'Layers',
      'lvl2.s5.title': 'Blocks and attributes',
      'lvl2.s6.title': 'Dimensioning',
      'lvl2.s7.title': 'Text, text styles, and tables',
      'lvl2.s8.title': 'Hatches and fills',
      'lvl2.nav.prev': 'Level 1 · Fundamentals',
      'lvl2.nav.next': 'Level 3 · Organization',

      /* ---- Level 3 ---- */
      'lvl3.eyebrow': 'Level 03 · Intermediate',
      'lvl3.title': 'Organization & Productivity',
      'lvl3.subtitle': 'How to prepare a drawing for printing or sharing correctly: layouts, scales, templates, exporting, external files, and the shortcuts that speed up the entire workflow.',
      'lvl3.s1.title': 'Model space vs. paper space (Layouts)',
      'lvl3.s2.title': 'Viewports and scales',
      'lvl3.s3.title': 'Templates (.DWT) and drawing standards',
      'lvl3.s4.title': 'Printing and exporting',
      'lvl3.s5.title': 'External references (Xref)',
      'lvl3.s6.title': 'Keyboard shortcuts and quick commands',
      'lvl3.nav.prev': 'Level 2 · 2D Drafting',
      'lvl3.nav.next': 'Level 4 · 3D Modeling',

      /* ---- Level 4 ---- */
      'lvl4.eyebrow': 'Level 04 · Advanced',
      'lvl4.title': '3D Modeling',
      'lvl4.subtitle': 'From plan to virtual model: 3D navigation, primitive solids, boolean operations, advanced creation tools, and an introduction to rendering.',
      'lvl4.s1.title': '3D workspace and navigation',
      'lvl4.s2.title': 'Basic solids (primitives)',
      'lvl4.s3.title': 'Boolean operations',
      'lvl4.s4.title': 'Extrusion, revolve, sweep, and loft',
      'lvl4.s5.title': 'Solid and surface editing',
      'lvl4.s6.title': 'Basic rendering',
      'lvl4.nav.prev': 'Level 3 · Organization',
      'lvl4.nav.next': 'Level 5 · Expert',

      /* ---- Level 5 ---- */
      'lvl5.eyebrow': 'Level 05 · Expert',
      'lvl5.title': 'Expert Level',
      'lvl5.subtitle': 'Customize AutoCAD to your needs, automate tasks with scripts, apply professional standards, and integrate the program with other real-world workflows.',
      'lvl5.s1.title': 'Interface customization (CUI)',
      'lvl5.s2.title': 'AutoLISP and basic scripts',
      'lvl5.s3.title': 'Professional CAD standards',
      'lvl5.s4.title': 'Professional drafting best practices',
      'lvl5.s5.title': 'Integration with other programs',
      'lvl5.s6.title': 'File optimization and troubleshooting',
      'lvl5.nav.prev': 'Level 4 · 3D Modeling',
      'lvl5.nav.next': 'Command dictionary',

      /* ---- Commands page ---- */
      'cmd.eyebrow': 'Command dictionary',
      'cmd.hero.title': 'Search any command',
      'cmd.hero.desc': 'Type a command name or shortcut to instantly find its use, category, and level.',
      'cmd.filter.all': 'All',
      'cmd.filter.dibujo': 'Drawing',
      'cmd.filter.modificacion': 'Modification',
      'cmd.filter.precision': 'Precision',
      'cmd.filter.capas': 'Layers',
      'cmd.filter.acotacion': 'Dimensioning',
      'cmd.filter.texto': 'Text',
      'cmd.filter.bloques': 'Blocks',
      'cmd.filter.3d': '3D',
      'cmd.filter.edicion': 'Editing',
      'cmd.filter.consulta': 'Inquiry',

      /* ---- Command descriptions (English) ---- */
      'cmd.line.desc': 'Draws straight line segments between points defined by coordinates or clicks.',
      'cmd.pline.desc': 'A series of straight and curved segments joined as a single polyline object.',
      'cmd.circle.desc': 'Draws a circle by center-radius, two points, three points, or other options.',
      'cmd.arc.desc': 'A curved segment defined by 3 points, center-start-end, or other combinations.',
      'cmd.rectang.desc': 'Draws a rectangle from two opposite corners.',
      'cmd.polygon.desc': 'A regular polygon inscribed in or circumscribed about a circle.',
      'cmd.ellipse.desc': 'An elliptical curve defined by major/minor axis or by center.',
      'cmd.spline.desc': 'A smooth curve passing through a series of control points.',
      'cmd.move.desc': 'Moves objects from a base point to a destination point.',
      'cmd.copy.desc': 'Creates copies of objects without removing the original.',
      'cmd.rotate.desc': 'Rotates objects by an angle around a base point.',
      'cmd.scale.desc': 'Increases or decreases the size of objects relative to a base point.',
      'cmd.trim.desc': 'Trims objects to the boundary of another reference object.',
      'cmd.extend.desc': 'Extends an object until it meets a reference boundary.',
      'cmd.offset.desc': 'Creates a parallel copy of an object at an exact distance.',
      'cmd.mirror.desc': 'Reflects objects across a symmetry axis defined by two points.',
      'cmd.array.desc': 'Repeats objects in rows/columns, in a circle, or along a path.',
      'cmd.fillet.desc': 'Joins two lines with an arc of a defined radius (fillet).',
      'cmd.chamfer.desc': 'Joins two lines with a straight cut at the corner (chamfer).',
      'cmd.stretch.desc': 'Stretches or compresses objects by moving vertices within a crossing selection.',
      'cmd.explode.desc': 'Decomposes a block, polyline, or array into individual objects.',
      'cmd.join.desc': 'Joins contiguous lines or arcs into a single object (opposite of EXPLODE).',
      'cmd.break.desc': 'Breaks an object into two parts or removes a segment between two points.',
      'cmd.matchprop.desc': 'Copies properties (layer, color, linetype) from one object to another.',
      'cmd.osnap.desc': 'Toggles object snaps: endpoint, midpoint, center, intersection, etc.',
      'cmd.layer.desc': 'Opens the Layer Manager to create, edit, and manage layers.',
      'cmd.layiso.desc': 'Isolates the layer of a selected object, hiding all others.',
      'cmd.layuniso.desc': 'Restores layer visibility to the state before LAYISO.',
      'cmd.block.desc': 'Creates a block from selected objects, defining name and base point.',
      'cmd.insert.desc': 'Inserts an existing block into the current drawing.',
      'cmd.bedit.desc': 'Opens the block editor to modify the content of a defined block.',
      'cmd.dimlinear.desc': 'Creates a linear horizontal or vertical dimension between two points.',
      'cmd.dimaligned.desc': 'A dimension parallel to an angled line.',
      'cmd.dim.desc': 'Smart dimension that automatically detects the type based on the selected object.',
      'cmd.dimstyle.desc': 'Manages dimension styles: text size, arrows, units, and precision.',
      'cmd.text.desc': 'Single-line text, useful for short labels and titles.',
      'cmd.mtext.desc': 'Multiline rich text within a defined box.',
      'cmd.style.desc': 'Defines the default font, height, and style for drawing text.',
      'cmd.table.desc': 'Inserts data tables with rows and columns (finishes, areas, etc.).',
      'cmd.hatch.desc': 'Fills a closed area with a hatch pattern (hatching, solid, material).',
      'cmd.pedit.desc': 'Edits polylines: join segments, open/close, smooth, or assign width.',
      'cmd.properties.desc': 'Opens the Properties palette to view and edit attributes of selected objects.',
      'cmd.box.desc': 'Creates a rectangular solid defined by length, width, and height.',
      'cmd.cylinder.desc': 'Creates a cylindrical solid by base radius and height.',
      'cmd.extrude.desc': 'Pushes a closed 2D profile in a straight line to create a solid.',
      'cmd.revolve.desc': 'Rotates a 2D profile around an axis to generate a solid of revolution.',
      'cmd.sweep.desc': 'Moves a profile along a curved path (pipe, molding).',
      'cmd.loft.desc': 'Generates a smooth shape connecting two or more profiles (loft).',
      'cmd.union.desc': 'Merges two or more solids into a single object (boolean union).',
      'cmd.subtract.desc': 'Subtracts one solid\'s volume from another (drilling, volume trimming).',
      'cmd.intersect.desc': 'Keeps only the common volume between two or more solids.',
      'cmd.3dorbit.desc': 'Free orbit around the 3D model to view from any angle.',
      'cmd.render.desc': 'Generates a rendered image of the 3D model with materials, lights, and camera.',
      'cmd.dist.desc': 'Measures the distance and angle between two points in the drawing.',
      'cmd.list.desc': 'Shows detailed properties of a selected object (layer, type, area, length).',
      'cmd.area.desc': 'Calculates the area and perimeter of a polygon or point selection.',
      'cmd.measure.desc': 'Places points or blocks along an object at equal intervals.',
      'cmd.zoom.desc': 'Zooms in or out of the drawing area (options: E, W, P, All).',
      'cmd.purge.desc': 'Removes unused elements from the file: layers, blocks, styles, linetypes.',
      'cmd.audit.desc': 'Detects and corrects internal errors in the DWG file.',
      'cmd.wblock.desc': 'Exports objects or the entire drawing to a separate DWG file.',

      /* ---- Resources page ---- */
      'res.eyebrow': 'Free resources',
      'res.hero.title': 'Blocks, courses, and templates at no cost',
      'res.hero.desc': 'A selection of block libraries, YouTube channels, forums, and free tools to boost your AutoCAD work.',
      'res.filter.all': 'All',
      'res.filter.bloques': 'DWG Blocks',
      'res.filter.cursos': 'Courses & tutorials',
      'res.filter.comunidades': 'Communities & forums',
      'res.filter.plantillas': 'Templates',
      'res.filter.youtube': 'YouTube channels',
      'res.filter.herramientas': 'Tools',
      'res.visit': 'Visit site',
      'res.forum': 'Visit forum',
      'res.subreddit': 'Visit subreddit',
      'res.channel': 'Visit channel',
      'res.download': 'Download',
      'res.searchYT': 'Search on YouTube',

      /* ---- FAQ page ---- */
      'faq.eyebrow': 'Frequently asked questions',
      'faq.hero.title': 'Common questions about AutoCAD',
      'faq.hero.desc': 'Answers to the most frequent questions from those starting out or wanting to go deeper into AutoCAD.',
      'faq.cta.eyebrow': 'Have more questions?',
      'faq.cta.title': 'Check the levels or the command dictionary',
      'faq.cta.desc': 'If your question isn\'t here, you\'ll probably find the answer in our content or by searching for the specific command.',
      'faq.cta.cmds': 'View commands',
      'faq.cta.start': 'Start from scratch',

      /* ---- Command names for categories/levels ---- */
      'cmd.cat.dibujo': 'Drawing',
      'cmd.cat.modificacion': 'Modification',
      'cmd.cat.precision': 'Precision',
      'cmd.cat.capas': 'Layers',
      'cmd.cat.acotacion': 'Dimensioning',
      'cmd.cat.texto': 'Text',
      'cmd.cat.bloques': 'Blocks',
      'cmd.cat.3d': '3D',
      'cmd.cat.edicion': 'Editing',
      'cmd.cat.consulta': 'Inquiry',
      'cmd.level.basico': 'Basic',
      'cmd.level.intermedio': 'Intermediate',
      'cmd.level.avanzado': 'Advanced'
    }
  };

  /* ---------- Idioma actual ---------- */
  var currentLang = localStorage.getItem(STORAGE_KEY) || 'es';

  function t(key) {
    return (I18N[currentLang] && I18N[currentLang][key]) || (I18N['es'] && I18N['es'][key]) || key;
  }

  function getLang() { return currentLang; }

  /* ---------- Aplicar traducciones al DOM ---------- */
  function applyTranslations() {
    /* data-i18n → textContent */
    document.querySelectorAll('[data-i18n]').forEach(function(el) {
      var key = el.getAttribute('data-i18n');
      var val = t(key);
      if (val) el.textContent = val;
    });

    /* data-i18n-html → innerHTML */
    document.querySelectorAll('[data-i18n-html]').forEach(function(el) {
      var key = el.getAttribute('data-i18n-html');
      var val = t(key);
      if (val) el.innerHTML = val;
    });

    /* data-i18n-placeholder → placeholder */
    document.querySelectorAll('[data-i18n-placeholder]').forEach(function(el) {
      var key = el.getAttribute('data-i18n-placeholder');
      var val = t(key);
      if (val) el.placeholder = val;
    });

    /* data-i18n-title → title */
    document.querySelectorAll('[data-i18n-title]').forEach(function(el) {
      var key = el.getAttribute('data-i18n-title');
      var val = t(key);
      if (val) el.title = val;
    });

    /* data-i18n-aria → aria-label */
    document.querySelectorAll('[data-i18n-aria]').forEach(function(el) {
      var key = el.getAttribute('data-i18n-aria');
      var val = t(key);
      if (val) el.setAttribute('aria-label', val);
    });

    /* html lang */
    document.documentElement.lang = currentLang === 'es' ? 'es' : 'en';

    /* Actualizar botón de idioma */
    document.querySelectorAll('.lang-toggle-text').forEach(function(el) {
      el.textContent = t('nav.lang');
    });

    /* Actualizar bandera/icono del botón */
    document.querySelectorAll('.lang-toggle-flag').forEach(function(el) {
      el.className = 'lang-toggle-flag bi ' + (currentLang === 'es' ? 'bi-translate' : 'bi-translate');
    });
  }

  /* ---------- Cambiar idioma ---------- */
  function setLang(lang) {
    currentLang = lang;
    localStorage.setItem(STORAGE_KEY, lang);
    applyTranslations();
  }

  function toggleLang() {
    setLang(currentLang === 'es' ? 'en' : 'es');
  }

  /* ---------- Init ---------- */
  function initI18n() {
    applyTranslations();

    /* Bind toggle buttons */
    document.querySelectorAll('#langToggle').forEach(function(btn) {
      btn.removeEventListener('click', btn._langHandler);
      btn._langHandler = function(e) {
        e.preventDefault();
        toggleLang();
      };
      btn.addEventListener('click', btn._langHandler);
    });
  }

  /* Expose globally */
  window.I18N_SYSTEM = {
    t: t,
    getLang: getLang,
    setLang: setLang,
    toggleLang: toggleLang,
    applyTranslations: applyTranslations,
    init: initI18n
  };

  /* Auto-init on DOMContentLoaded */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initI18n);
  } else {
    initI18n();
  }

})();
