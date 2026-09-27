(() => {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const chips = document.querySelectorAll('.chip');
  const items = [...document.querySelectorAll('.item')];
  const quarters = document.querySelectorAll('.quarter');
  const count = document.querySelector('.rm-count');

  let dict = (window.GBH_I18N || {})[document.documentElement.lang] || {};
  let current = 'all';
  let hideTimer;

  const renderCount = () => {
    const n = items.filter((item) => !item.hidden && !item.classList.contains('is-out')).length;
    const template = dict[n === 1 ? 'rm.count.one' : 'rm.count.other'] || '{n}';
    count.textContent = template.replace('{n}', n);
  };

  const applyFilter = (filter) => {
    current = filter;
    clearTimeout(hideTimer);

    chips.forEach((chip) => chip.setAttribute('aria-pressed', String(chip.dataset.filter === filter)));

    const match = (item) => filter === 'all' || item.dataset.cat === filter;

    // 1. Fondu de sortie des points ecartes
    items.forEach((item) => item.classList.toggle('is-out', !match(item)));
    renderCount();

    // 2. Une fois le fondu termine : on retire du flux, on fait revenir les autres
    hideTimer = setTimeout(() => {
      items.forEach((item) => { item.hidden = !match(item); });

      quarters.forEach((quarter) => {
        const visible = [...quarter.querySelectorAll('.item')].filter((item) => !item.hidden);
        quarter.hidden = visible.length === 0;
        visible.forEach((item, i) => item.style.setProperty('--i', i));
      });

      items.forEach((item) => {
        if (item.hidden) return;
        item.classList.remove('is-in');
        void item.offsetWidth; // relance la transition d'entree
        item.classList.add('is-in');
      });
    }, reduceMotion ? 0 : 200);
  };

  chips.forEach((chip) => {
    chip.addEventListener('click', () => {
      if (chip.dataset.filter !== current) applyFilter(chip.dataset.filter);
    });
  });

  document.addEventListener('gbh:lang', (e) => {
    dict = e.detail.dict;
    renderCount();
  });

  renderCount();
})();
