(() => {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const chips = document.querySelectorAll('.chip');
  const articles = [...document.querySelectorAll('.article')];
  const count = document.querySelector('.rm-count');

  let dict = (window.GBH_I18N || {})[document.documentElement.lang] || {};
  let current = 'all';
  let hideTimer;

  /* ---------------------------------------------------------------------
     Ouvrir / refermer un article
     --------------------------------------------------------------------- */

  const setOpen = (article, open) => {
    const toggle = article.querySelector('.article__toggle');
    article.querySelector('.article__body').hidden = !open;
    article.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.querySelector('span').textContent = dict[open ? 'news.less' : 'news.more'] || '';
  };

  articles.forEach((article) => {
    article.querySelector('.article__toggle').addEventListener('click', () => {
      setOpen(article, !article.classList.contains('is-open'));
    });
  });

  /* ---------------------------------------------------------------------
     Filtres par theme (meme principe que la road map)
     --------------------------------------------------------------------- */

  const renderCount = () => {
    const n = articles.filter((a) => !a.hidden && !a.classList.contains('is-out')).length;
    const template = dict[n === 1 ? 'news.count.one' : 'news.count.other'] || '{n}';
    count.textContent = template.replace('{n}', n);
  };

  const applyFilter = (filter) => {
    current = filter;
    clearTimeout(hideTimer);
    chips.forEach((chip) => chip.setAttribute('aria-pressed', String(chip.dataset.filter === filter)));

    const match = (a) => filter === 'all' || a.dataset.cat === filter;
    articles.forEach((a) => a.classList.toggle('is-out', !match(a)));
    renderCount();

    hideTimer = setTimeout(() => {
      articles.forEach((a) => {
        a.hidden = !match(a);
        if (a.hidden) return;
        a.classList.remove('is-in');
        void a.offsetWidth; // relance la transition d'entree
        a.classList.add('is-in');
      });
    }, reduceMotion ? 0 : 200);
  };

  chips.forEach((chip) => {
    chip.addEventListener('click', () => {
      if (chip.dataset.filter !== current) applyFilter(chip.dataset.filter);
    });
  });

  /* ---------------------------------------------------------------------
     Lien direct vers un article (#id) : on l'affiche ouvert
     --------------------------------------------------------------------- */

  const openFromHash = () => {
    const target = articles.find((a) => `#${a.id}` === location.hash);
    if (!target) return;
    if (target.hidden) applyFilter('all');
    target.classList.add('is-in');
    setOpen(target, true);
    target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
  };

  window.addEventListener('hashchange', openFromHash);

  // Les cartes "A la une" pointent vers un article : meme comportement
  document.querySelectorAll('[data-open]').forEach((link) => {
    link.addEventListener('click', (e) => {
      if (link.getAttribute('href') !== location.hash) return;
      e.preventDefault();
      openFromHash();
    });
  });

  /* ---------------------------------------------------------------------
     Langue
     --------------------------------------------------------------------- */

  document.addEventListener('gbh:lang', (e) => {
    dict = e.detail.dict;
    renderCount();
    // applyLang remet "Lire la suite" partout : on retablit les articles ouverts
    articles.forEach((a) => { if (a.classList.contains('is-open')) setOpen(a, true); });
  });

  renderCount();
  openFromHash();
})();
