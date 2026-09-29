(() => {
  'use strict';

  // La page contient le texte en francais et en anglais ; la CSS n'affiche que
  // la langue courante. Ce script construit le sommaire de la version visible,
  // suit la section lue et fait pointer les ancres (#newsletter...) vers la
  // bonne version.

  const list = document.querySelector('[data-toc]');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let items = new Map();

  const visibleArticle = () =>
    document.querySelector(document.documentElement.lang === 'en' ? '.legal--en' : '.legal--fr');

  const build = () => {
    const article = visibleArticle();
    const heads = [...article.querySelectorAll('h2[id], h3[id]')];

    list.innerHTML = heads.map((h) => {
      const cls = h.tagName === 'H2' ? 'legal-toc__part' : '';
      return `<li class="${cls}"><a href="#${h.id}">${h.textContent}</a></li>`;
    }).join('');

    items = new Map([...list.querySelectorAll('li')].map((li) => [li.querySelector('a').hash.slice(1), li]));
    track();
  };

  // Section courante : le dernier titre passe au-dessus du tiers haut de
  // l'ecran. Son <li> recoit aria-current="location" (lu par les lecteurs
  // d'ecran, et utilise par la CSS pour le surligner).
  const track = () => {
    const heads = [...items.keys()].map((id) => document.getElementById(id)).filter(Boolean);
    if (!heads.length) return;
    const limit = window.innerHeight * 0.3;
    const atBottom = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2;
    let current = heads[0];
    if (atBottom) current = heads[heads.length - 1];
    else heads.forEach((h) => { if (h.getBoundingClientRect().top <= limit) current = h; });

    const li = items.get(current.id);
    if (li.hasAttribute('aria-current')) return;
    list.querySelectorAll('li[aria-current]').forEach((el) => el.removeAttribute('aria-current'));
    li.setAttribute('aria-current', 'location');
  };

  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { ticking = false; track(); });
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
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);

  build();
  requestAnimationFrame(() => followHash(false));
})();
