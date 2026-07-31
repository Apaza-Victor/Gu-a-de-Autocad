/* =========================================================
   AutoCAD Guía — main.js
   Funcionalidades compartidas por todas las páginas del sitio.
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {
  initAOS();
  initThemeToggle();
  initCoordReadout();
  initCommandLine();
  initBackToTop();
  initScrollSpy();
  initMarkDone();
  initFaqAccordion();
  initCommandFilters();
  initCommandSearch();
  initResourceFilters();
  initGlobalSearch();
  initSwiperCarousel();
  initPrism();
  initHomeProgress();
  initKeyboardAccessibility();
  initNavbarToggler();
  initCopyButtons();
});

/* ---------- Animaciones al hacer scroll ---------- */
function initAOS(){
  if (window.AOS){
    AOS.init({ duration: 600, easing: 'ease-out-quart', once: true, offset: 60 });
  }
}

/* ---------- Modo claro / oscuro con persistencia ---------- */
function initThemeToggle(){
  const root = document.documentElement;
  const btn = document.getElementById('themeToggle');
  const saved = localStorage.getItem('autocad-guia-theme');

  if (saved) {
    root.setAttribute('data-theme', saved);
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
    root.setAttribute('data-theme', 'light');
  }

  updateThemeIcon();

  if (btn){
    btn.addEventListener('click', () => {
      const current = root.getAttribute('data-theme') === 'light' ? 'light' : 'dark';
      const next = current === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next);
      localStorage.setItem('autocad-guia-theme', next);
      updateThemeIcon();
    });
  }

  function updateThemeIcon(){
    if (!btn) return;
    const icon = btn.querySelector('i');
    const isLight = root.getAttribute('data-theme') === 'light';
    icon.className = isLight ? 'bi bi-sun' : 'bi bi-moon-stars';
  }
}

/* ---------- Lectura de coordenadas tipo barra de estado de AutoCAD ---------- */
function initCoordReadout(){
  const xEl = document.getElementById('coordX');
  const yEl = document.getElementById('coordY');
  if (!xEl || !yEl) return;

  window.addEventListener('mousemove', (e) => {
    const x = (e.clientX * 0.35).toFixed(2);
    const y = ((window.innerHeight - e.clientY) * 0.35).toFixed(2);
    xEl.textContent = x.padStart(6, '0');
    yEl.textContent = y.padStart(6, '0');
  }, { passive: true });
}

/* ---------- Barra de línea de comandos con "tips" tipo máquina de escribir ---------- */
function initCommandLine(){
  const bar = document.getElementById('cmdBar');
  const typedEl = document.getElementById('cmd-typed');
  const closeBtn = document.getElementById('cmdClose');
  if (!bar || !typedEl) return;

  function t(key){ return window.I18N_SYSTEM ? window.I18N_SYSTEM.t(key) : key; }

  const tips = [
    t('tip.1'), t('tip.2'), t('tip.3'), t('tip.4'),
    t('tip.5'), t('tip.6'), t('tip.7'), t('tip.8')
  ];

  let tipIndex = 0;
  let charIndex = 0;
  let deleting = false;

  function tick(){
    const current = tips[tipIndex];

    if (!deleting){
      charIndex++;
      typedEl.textContent = current.slice(0, charIndex);
      if (charIndex === current.length){
        deleting = true;
        setTimeout(tick, 2600);
        return;
      }
    } else {
      charIndex--;
      typedEl.textContent = current.slice(0, charIndex);
      if (charIndex === 0){
        deleting = false;
        tipIndex = (tipIndex + 1) % tips.length;
      }
    }
    setTimeout(tick, deleting ? 18 : 28);
  }
  tick();

  if (closeBtn){
    closeBtn.addEventListener('click', () => bar.classList.add('hidden'));
  }
}

/* ---------- Botón volver arriba ---------- */
function initBackToTop(){
  const btn = document.createElement('button');
  btn.innerHTML = '<i class="bi bi-arrow-up"></i>';
  btn.setAttribute('aria-label', window.I18N_SYSTEM ? I18N_SYSTEM.t('ui.back') : 'Volver arriba');
  btn.style.cssText = `
    position:fixed; right:1.1rem; bottom:4.2rem; z-index:1035;
    width:40px; height:40px; border-radius:8px;
    background:var(--bg-elevated); color:var(--cyan);
    border:1px solid var(--border); display:none; place-items:center;
    cursor:pointer;
  `;
  btn.className = 'back-to-top-btn';
  document.body.appendChild(btn);

  window.addEventListener('scroll', () => {
    btn.style.display = window.scrollY > 500 ? 'grid' : 'none';
  }, { passive: true });

  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

/* ---------- Scroll-spy para sidebar de niveles ---------- */
function initScrollSpy(){
  const tocLinks = document.querySelectorAll('.toc-list a[data-toc]');
  if (!tocLinks.length) return;

  const sections = [];
  tocLinks.forEach(link => {
    const id = link.getAttribute('data-toc');
    const section = document.querySelector('[data-topic="' + id + '"]');
    if (section) sections.push({ el: section, link: link });
  });

  if (!sections.length) return;

  function updateSpy(){
    const scrollPos = window.scrollY + 120;
    let current = sections[0];

    for (const s of sections) {
      if (s.el.offsetTop <= scrollPos) current = s;
    }

    tocLinks.forEach(l => l.classList.remove('active'));
    if (current) current.link.classList.add('active');
  }

  window.addEventListener('scroll', updateSpy, { passive: true });
  updateSpy();
}

/* ---------- Marcar temas como completados ---------- */
function initMarkDone(){
  const buttons = document.querySelectorAll('.mark-done-btn');
  if (!buttons.length) return;

  buttons.forEach(btn => {
    const section = btn.closest('section');
    if (!section) return;
    const topicId = section.getAttribute('data-topic');
    if (!topicId) return;

    if (isTopicComplete(topicId)) {
      btn.classList.add('completed');
      btn.innerHTML = '<i class="bi bi-check-circle-fill"></i> ' + (window.I18N_SYSTEM ? I18N_SYSTEM.t('ui.done') : 'Tema completado');
      const tocLink = document.querySelector('.toc-list a[data-toc="' + topicId + '"]');
      if (tocLink) tocLink.classList.add('done');
    }

    btn.addEventListener('click', () => {
      if (isTopicComplete(topicId)) {
        markTopicIncomplete(topicId);
        btn.classList.remove('completed');
        btn.innerHTML = '<i class="bi bi-check-circle"></i> ' + (window.I18N_SYSTEM ? I18N_SYSTEM.t('ui.markDone') : 'Marcar tema como visto');
        const tocLink = document.querySelector('.toc-list a[data-toc="' + topicId + '"]');
        if (tocLink) tocLink.classList.remove('done');
      } else {
        markTopicComplete(topicId);
        btn.classList.add('completed');
        btn.innerHTML = '<i class="bi bi-check-circle-fill"></i> ' + (window.I18N_SYSTEM ? I18N_SYSTEM.t('ui.done') : 'Tema completado');
        const tocLink = document.querySelector('.toc-list a[data-toc="' + topicId + '"]');
        if (tocLink) tocLink.classList.add('done');
      }
      updateLevelProgress();
    });
  });

  updateLevelProgress();
}

function updateLevelProgress(){
  const label = document.querySelector('.level-progress-label');
  const fill = document.querySelector('.level-progress-bar .fill');
  if (!label || !fill) return;

  const allTopics = document.querySelectorAll('[data-topic]');
  const total = allTopics.length;
  if (total === 0) return;

  let done = 0;
  allTopics.forEach(s => {
    const id = s.getAttribute('data-topic');
    if (isTopicComplete(id)) done++;
  });

  const pct = Math.round((done / total) * 100);
  fill.style.width = pct + '%';
  label.textContent = (function(){
    if (window.I18N_SYSTEM){
      return I18N_SYSTEM.t('progress.xOfY').replace('{done}', done).replace('{total}', total).replace('{pct}', pct);
    }
    return done + ' de ' + total + ' temas completados · ' + pct + '%';
  })();
}

function markTopicComplete(id){
  const done = JSON.parse(localStorage.getItem('autocad-guia-progreso') || '[]');
  if (!done.includes(id)) done.push(id);
  localStorage.setItem('autocad-guia-progreso', JSON.stringify(done));
}
function isTopicComplete(id){
  const done = JSON.parse(localStorage.getItem('autocad-guia-progreso') || '[]');
  return done.includes(id);
}
function markTopicIncomplete(id){
  let done = JSON.parse(localStorage.getItem('autocad-guia-progreso') || '[]');
  done = done.filter(t => t !== id);
  localStorage.setItem('autocad-guia-progreso', JSON.stringify(done));
}

/* ---------- FAQ acordeón ---------- */
function initFaqAccordion(){
  const items = document.querySelectorAll('.faq-item');
  if (!items.length) return;

  items.forEach(item => {
    const question = item.querySelector('.faq-question');
    if (!question) return;

    question.addEventListener('click', () => {
      const wasOpen = item.classList.contains('open');
      items.forEach(i => i.classList.remove('open'));
      if (!wasOpen) item.classList.add('open');
    });
  });
}

/* ---------- Filtros de comandos ---------- */
function initCommandFilters(){
  const filtersContainer = document.getElementById('cmdFilters');
  const grid = document.getElementById('cmdGrid');
  const countEl = document.getElementById('cmdCount');
  const emptyEl = document.getElementById('cmdEmpty');
  if (!filtersContainer || !grid) return;

  const buttons = filtersContainer.querySelectorAll('.cmd-filter-btn');
  const cards = grid.querySelectorAll('.cmd-full-card');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.getAttribute('data-filter');
      let visible = 0;

      cards.forEach(card => {
        const cat = card.getAttribute('data-cat');
        const show = filter === 'todos' || cat === filter;
        card.style.display = show ? '' : 'none';
        if (show) visible++;
      });

      if (countEl) countEl.textContent = (window.I18N_SYSTEM ? I18N_SYSTEM.t('ui.showing') : 'Mostrando') + ' ' + visible + ' ' + (window.I18N_SYSTEM ? I18N_SYSTEM.t(visible !== 1 ? 'ui.commands' : 'ui.command_single') : 'comando' + (visible !== 1 ? 's' : ''));
      if (emptyEl) emptyEl.style.display = visible === 0 ? '' : 'none';
    });
  });
}

/* ---------- Búsqueda de comandos ---------- */
function initCommandSearch(){
  const input = document.getElementById('cmdSearchInput');
  const grid = document.getElementById('cmdGrid');
  const countEl = document.getElementById('cmdCount');
  const emptyEl = document.getElementById('cmdEmpty');
  if (!input || !grid) return;

  const cards = grid.querySelectorAll('.cmd-full-card');
  const allFilters = document.querySelectorAll('#cmdFilters .cmd-filter-btn');

  input.addEventListener('input', () => {
    const q = input.value.toLowerCase().trim();

    allFilters.forEach(b => b.classList.remove('active'));
    allFilters[0].classList.add('active');

    let visible = 0;
    cards.forEach(card => {
      const name = (card.getAttribute('data-cmd') || '').toLowerCase();
      const keys = (card.getAttribute('data-keys') || '').toLowerCase();
      const desc = (card.querySelector('.cmd-desc')?.textContent || '').toLowerCase();
      const cat = (card.getAttribute('data-cat') || '').toLowerCase();

      const match = !q || name.includes(q) || keys.includes(q) || desc.includes(q) || cat.includes(q);
      card.style.display = match ? '' : 'none';
      if (match) visible++;
    });

    if (countEl) countEl.textContent = (window.I18N_SYSTEM ? I18N_SYSTEM.t('ui.showing') : 'Mostrando') + ' ' + visible + ' ' + (window.I18N_SYSTEM ? I18N_SYSTEM.t(visible !== 1 ? 'ui.commands' : 'ui.command_single') : 'comando' + (visible !== 1 ? 's' : ''));
    if (emptyEl) emptyEl.style.display = visible === 0 ? '' : 'none';
  });
}

/* ---------- Filtros de recursos ---------- */
function initResourceFilters(){
  const filtersContainer = document.getElementById('resFilters');
  const grid = document.getElementById('resGrid');
  if (!filtersContainer || !grid) return;

  const buttons = filtersContainer.querySelectorAll('.res-filter-btn');
  const cards = grid.querySelectorAll('.res-full-card');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.getAttribute('data-filter');

      cards.forEach(card => {
        const cat = card.getAttribute('data-cat');
        card.style.display = (filter === 'todos' || cat === filter) ? '' : 'none';
      });
    });
  });
}

/* ---------- Buscador global con Fuse.js ---------- */
function initGlobalSearch(){
  const overlay = document.getElementById('searchOverlay');
  const input = document.getElementById('globalSearchInput');
  const resultsContainer = document.getElementById('globalSearchResults');
  if (!overlay || !input || !resultsContainer) return;

  // Base de datos de búsqueda (se llena al cargar)
  const searchData = buildSearchData();
  let fuse = null;

  if (typeof Fuse !== 'undefined' && searchData.length) {
    fuse = new Fuse(searchData, {
      keys: [
        { name: 'title', weight: 0.4 },
        { name: 'command', weight: 0.3 },
        { name: 'shortcut', weight: 0.2 },
        { name: 'description', weight: 0.1 }
      ],
      threshold: 0.4,
      includeScore: true,
      minMatchCharLength: 2
    });
  }

  // Abrir/cerrar overlay
  function openSearch(){
    overlay.classList.add('active');
    input.value = '';
    resultsContainer.innerHTML = '<div class="search-empty">Escribe al menos 2 caracteres para buscar...</div>';
    setTimeout(() => input.focus(), 100);
  }
  function closeSearch(){
    overlay.classList.remove('active');
    input.value = '';
  }

  // Abrir con botón de búsqueda
  document.querySelectorAll('#searchToggle').forEach(btn => {
    btn.removeEventListener('click', btn._searchHandler);
    btn._searchHandler = (e) => {
      e.preventDefault();
      openSearch();
    };
    btn.addEventListener('click', btn._searchHandler);
  });

  // Cerrar con ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && overlay.classList.contains('active')) {
      closeSearch();
    }
    // Ctrl+K para abrir búsqueda global
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      openSearch();
    }
  });

  // Cerrar al hacer clic fuera
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeSearch();
  });

  // Buscar al escribir
  let debounceTimer;
  input.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const query = input.value.trim();
      if (query.length < 2) {
        resultsContainer.innerHTML = '<div class="search-empty">' + (window.I18N_SYSTEM ? I18N_SYSTEM.t('ui.typeToSearch') : 'Escribe al menos 2 caracteres para buscar...') + '</div>';
        return;
      }
      if (!fuse) {
        resultsContainer.innerHTML = '<div class="search-empty">' + (window.I18N_SYSTEM ? I18N_SYSTEM.t('ui.searchUnavailable') : 'Buscador no disponible.') + '</div>';
        return;
      }

      const results = fuse.search(query).slice(0, 12);
      if (results.length === 0) {
        resultsContainer.innerHTML = '<div class="search-empty">' + (window.I18N_SYSTEM ? I18N_SYSTEM.t('ui.noResults') : 'No se encontraron resultados para') + ' "' + escapeHtml(query) + '"</div>';
        return;
      }

      resultsContainer.innerHTML = results.map(r => {
        const d = r.item;
        const icon = d.type === 'command' ? 'bi-terminal' : d.type === 'resource' ? 'bi-gift' : 'bi-book';
        return '<a href="' + d.url + '" class="search-result-item">' +
          '<div class="sr-icon"><i class="bi ' + icon + '"></i></div>' +
          '<div class="sr-info">' +
            '<div class="sr-title">' + highlightMatch(d.title, query) + '</div>' +
            '<div class="sr-path">' + (d.path || '') + '</div>' +
          '</div>' +
        '</a>';
      }).join('');
    }, 200);
  });
}

function buildSearchData(){
  const data = [];
  const isHome = !window.location.pathname.includes('/paginas/');
  const prefix = isHome ? 'paginas/' : '';

  // Comandos de la página de comandos
  const cmdCards = document.querySelectorAll('.cmd-full-card[data-cmd]');
  cmdCards.forEach(card => {
    data.push({
      type: 'command',
      title: card.getAttribute('data-cmd').toUpperCase(),
      command: card.getAttribute('data-cmd'),
      shortcut: card.getAttribute('data-keys') || '',
      description: (card.querySelector('.cmd-desc') || {}).textContent || '',
      url: prefix + 'comandos.html',
      path: 'Comandos'
    });
  });

  // Secciones de niveles
  const sections = document.querySelectorAll('[data-topic]');
  sections.forEach(s => {
    const h2 = s.querySelector('h2');
    const title = h2 ? h2.textContent.trim() : s.getAttribute('data-topic');
    const level = s.closest('[class*="content-layout"]') ?
      (document.querySelector('.eyebrow') || {}).textContent || '' : '';
    data.push({
      type: 'topic',
      title: title,
      description: (s.querySelector('p') || {}).textContent || '',
      url: prefix + determinePage(s),
      path: level
    });
  });

  // Recursos
  const resCards = document.querySelectorAll('.res-full-card');
  resCards.forEach(card => {
    const h4 = card.querySelector('h4');
    data.push({
      type: 'resource',
      title: h4 ? h4.textContent : '',
      description: (card.querySelector('p') || {}).textContent || '',
      url: prefix + 'recursos.html',
      path: 'Recursos'
    });
  });

  // FAQ
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const q = item.querySelector('.faq-question');
    data.push({
      type: 'faq',
      title: q ? q.textContent.trim() : '',
      description: (item.querySelector('.faq-answer') || {}).textContent || '',
      url: prefix + 'faq.html',
      path: 'FAQ'
    });
  });

  // Si estamos en home, agregar links a niveles
  if (isHome) {
    const levels = [
      { name: 'Nivel 1 · Fundamentos', url: 'paginas/nivel-1-fundamentos.html' },
      { name: 'Nivel 2 · Dibujo 2D', url: 'paginas/nivel-2-dibujo-2d.html' },
      { name: 'Nivel 3 · Organización', url: 'paginas/nivel-3-organizacion.html' },
      { name: 'Nivel 4 · Modelado 3D', url: 'paginas/nivel-4-modelado-3d.html' },
      { name: 'Nivel 5 · Avanzado', url: 'paginas/nivel-5-avanzado.html' },
      { name: 'Comandos', url: 'paginas/comandos.html' },
      { name: 'Recursos', url: 'paginas/recursos.html' },
      { name: 'FAQ', url: 'paginas/faq.html' }
    ];
    levels.forEach(l => {
      data.push({ type: 'page', title: l.name, url: l.url, path: '', description: '' });
    });
  }

  return data;
}

function determinePage(section){
  const topic = section.getAttribute('data-topic') || '';
  if (topic.startsWith('nivel1')) return 'nivel-1-fundamentos.html';
  if (topic.startsWith('nivel2')) return 'nivel-2-dibujo-2d.html';
  if (topic.startsWith('nivel3')) return 'nivel-3-organizacion.html';
  if (topic.startsWith('nivel4')) return 'nivel-4-modelado-3d.html';
  if (topic.startsWith('nivel5')) return 'nivel-5-avanzado.html';
  return 'nivel-1-fundamentos.html';
}

function highlightMatch(text, query){
  if (!query) return escapeHtml(text);
  const escaped = escapeHtml(text);
  const re = new RegExp('(' + escapeRegex(query) + ')', 'gi');
  return escaped.replace(re, '<mark style="background:var(--cyan-dim);color:var(--cyan);border-radius:2px;padding:0 2px">$1</mark>');
}

function escapeHtml(str){
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function escapeRegex(str){
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/* ---------- Swiper carousel ---------- */
function initSwiperCarousel(){
  const el = document.querySelector('.swiper-carousel');
  if (!el || typeof Swiper === 'undefined') return;

  new Swiper('.swiper-carousel', {
    slidesPerView: 1,
    spaceBetween: 16,
    loop: false,
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev'
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true
    },
    breakpoints: {
      640: { slidesPerView: 2 },
      992: { slidesPerView: 3 }
    }
  });
}

/* ---------- Prism.js highlight ---------- */
function initPrism(){
  if (typeof Prism !== 'undefined') {
    Prism.highlightAll();
  }
}

/* ---------- Barra de progreso en home ---------- */
function initHomeProgress(){
  const fill = document.getElementById('homeProgressFill');
  const label = document.getElementById('homeProgressLabel');
  if (!fill || !label) return;

  const allTopics = document.querySelectorAll('[data-topic]');
  const total = allTopics.length || 51; // fallback al total conocido
  let done = 0;

  allTopics.forEach(s => {
    const id = s.getAttribute('data-topic');
    if (isTopicComplete(id)) done++;
  });

  // También contar desde localStorage directamente
  const saved = JSON.parse(localStorage.getItem('autocad-guia-progreso') || '[]');
  done = Math.max(done, saved.length);

  const pct = Math.round((done / total) * 100);
  fill.style.width = pct + '%';
  label.textContent = (function(){
    if (window.I18N_SYSTEM){
      return I18N_SYSTEM.t('progress.xOfY').replace('{done}', done).replace('{total}', total).replace('{pct}', pct);
    }
    return done + ' de ' + total + ' temas completados · ' + pct + '%';
  })();
}

/* ---------- Navegación por teclado ---------- */
function initKeyboardAccessibility(){
  // FAQ: Enter y Espacio abren/cierran
  document.querySelectorAll('.faq-question').forEach(btn => {
    btn.setAttribute('tabindex', '0');
    btn.setAttribute('role', 'button');
    btn.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        btn.click();
      }
    });
  });

  // Filtros: flechas para navegar
  ['cmdFilters', 'resFilters'].forEach(containerId => {
    const container = document.getElementById(containerId);
    if (!container) return;
    const buttons = container.querySelectorAll('.cmd-filter-btn, .res-filter-btn');
    buttons.forEach((btn, i) => {
      btn.setAttribute('tabindex', '0');
      btn.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
          e.preventDefault();
          const next = buttons[(i + 1) % buttons.length];
          next.focus();
          next.click();
        }
        if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
          e.preventDefault();
          const prev = buttons[(i - 1 + buttons.length) % buttons.length];
          prev.focus();
          prev.click();
        }
      });
    });
  });

  // Marcar tema: Enter activa el botón
  document.querySelectorAll('.mark-done-btn').forEach(btn => {
    btn.setAttribute('tabindex', '0');
    btn.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        btn.click();
      }
    });
  });
}

/* ---------- Botón hamburguesa: cambia de icono al abrir/cerrar ---------- */
function initNavbarToggler(){
  const collapseEl = document.getElementById('navCad');
  const btn = document.querySelector('.navbar-toggler');
  if (!collapseEl || !btn) return;
  const icon = btn.querySelector('i');
  if (!icon) return;

  const setIcon = (open) => {
    icon.classList.toggle('bi-list', !open);
    icon.classList.toggle('bi-x', open);
  };

  collapseEl.addEventListener('show.bs.collapse', () => setIcon(true));
  collapseEl.addEventListener('hide.bs.collapse', () => setIcon(false));

  // Al volver a escritorio el menú queda expandido y visible: restaurar hamburguesa
  const mq = window.matchMedia('(min-width: 992px)');
  const onDesktop = () => { if (mq.matches) setIcon(false); };
  if (mq.addEventListener) mq.addEventListener('change', onDesktop);
  else if (mq.addListener) mq.addListener(onDesktop);
}

/* ---------- Botones copiar código ---------- */
function initCopyButtons(){
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const code = btn.closest('.code-block').querySelector('code');
      if (!code) return;
      navigator.clipboard.writeText(code.textContent).then(() => {
        const original = btn.textContent;
        btn.textContent = window.I18N_SYSTEM ? I18N_SYSTEM.t('ui.copied') : '¡Copiado!';
        btn.style.color = 'var(--layer-green)';
        setTimeout(() => {
          btn.textContent = original;
          btn.style.color = '';
        }, 1500);
      });
    });
  });
}

/* ---------- Descargar tabla de atajos ---------- */
function downloadShortcuts(){
  const table = document.getElementById('shortcutsTable');
  if (!table) return;

  const rows = table.querySelectorAll('tr');
  let text = 'ATAJOS DE TECLADO - AutoCAD Guía\n';
  text += '='.repeat(50) + '\n\n';

  rows.forEach((row, i) => {
    if (i === 0) return; // skip header
    const cells = row.querySelectorAll('td');
    if (cells.length >= 4) {
      const cat = cells[0].textContent.trim();
      const cmd = cells[1].textContent.trim();
      const key = cells[2].textContent.trim();
      const desc = cells[3].textContent.trim();
      text += '[' + cat + '] ' + cmd + ' (' + key + ') — ' + desc + '\n';
    }
  });

  text += '\n' + '='.repeat(50) + '\n';
  text += 'Fuente: AutoCAD Guía — https://apaza-victor.github.io/Gu-a-de-Autocad/\n';
  text += 'Generado: ' + new Date().toLocaleDateString('es') + '\n';

  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'atajos-autocad-guia.txt';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}