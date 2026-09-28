(() => {
  'use strict';

  // La page contient le texte en francais et en anglais ; la CSS n'affiche que
  // la langue courante. Ce script construit le sommaire de la version visible,
  // suit la section lue et fait pointer les ancres (#newsletter...) vers la
  // bonne version.

  const list = document.querySelector('[data-toc]');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let observer;

  const visibleArticle = () =>
    document.querySelector(document.documentElement.lang === 'en' ? '.legal--en' : '.legal--fr');

  const build = () => {
    const article = visibleArticle();
    const heads = [...article.querySelectorAll('h2[id], h3[id]')];

    list.innerHTML = heads.map((h) => {
      const cls = h.tagName === 'H2' ? 'legal-toc__part' : '';
      return `<li class="${cls}"><a href="#${h.id}">${h.textContent}</a></li>`;
    }).join('');

    // Section courante mise en evidence dans le sommaire
    if (observer) observer.disconnect();
    if (!('IntersectionObserver' in window)) return;
    const links = new Map([...list.querySelectorAll('a')].map((a) => [a.hash.slice(1), a]));
    observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        list.querySelectorAll('a[aria-current]').forEach((a) => a.removeAttribute('aria-current'));
        links.get(entry.target.id)?.setAttribute('aria-current', 'true');
      });
    }, { rootMargin: '0px 0px -70% 0px' });
    heads.forEach((h) => observer.observe(h));
  };

  // #newsletter en anglais -> #newsletter-en (et inversement)
  const followHash = (smooth) => {
    const id = decodeURIComponent(location.hash.slice(1));
    if (!id) return;
    const en = document.documentElement.lang === 'en';
    const base = id.replace(/-en$/, '');
    const target = document.getElementById(en ? `${base}-en` : base);
    if (target) target.scrollIntoView({ behavior: smooth && !reduceMotion ? 'smooth' : 'auto', block: 'start' });
  };

  document.addEventListener('gbh:lang', () => { build(); });
  window.addEventListener('hashchange', () => followHash(true));

  build();
  requestAnimationFrame(() => followHash(false));
})();
