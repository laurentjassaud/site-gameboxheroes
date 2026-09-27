(() => {
  'use strict';

  document.documentElement.classList.add('js');

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------------
     Traductions FR / EN
     --------------------------------------------------------------------- */

  const translations = {
    fr: {
      'meta.title': 'GameBoxHeroes — Modules jouables de wargames classiques',
      'meta.description': 'GameBoxHeroes adapte les classiques du wargame pour jouer en solo ou en direct à plusieurs.',
      'hero.title': 'Modules jouables de wargames classiques',
      'lead.sub': 'est un projet d’adaptation<br>des classiques du wargame pour jouer en solo ou en direct à plusieurs',
      'feat.assist.title': 'Mode assisté',
      'feat.assist.text': 'Les modules ont une version assistée<br>qui vérifie la conformité des coups joués.',
      'feat.versus.title': 'Parties entre adversaires optimisées',
      'feat.versus.text': 'Amélioration de l’expérience de jeu par <strong>double aveugle</strong>, partie chronométrée type <strong>blitz</strong>, ajout des <strong>variantes</strong> créées par les fans',
      'modules.label': 'Modules',
      'modules.arnhem': 'Arnhem&nbsp;: Operation Market-Garden, septembre 1944, est un wargame de plateau pour deux joueurs, de niveau opérationnel, faisant à l’origine partie du <span>quad Westwall</span>.',
      'modules.ambush': 'Menez une escouade dans une série de combats tactiques de 39-45, tout droit sortis d’Hollywood\u00a0!',
      'news.title': 'Actualités',
      'news.all': 'Voir toutes les actualités',
      'news.date': '01 octobre 26',
      'news.item1': 'Mise en ligne des tests publics pour le jeu <span class="news__hl">Arnhem</span> publié en 1976 par SPI.',
      'news.item2': 'Mise en ligne des tests publics du jeu <span class="news__hl">Arnhem</span> publié en 1976 par SPI.',
      'news.more': 'Lire la suite',
      'menu.open': 'Ouvrir le menu',
      'menu.close': 'Fermer le menu',
      'menu.label': 'Menu principal',
      'menu.modules': 'Modules',
      'menu.news': 'Actualités',
      'menu.roadmap': 'Road Map',
      'menu.about': 'Qui sommes-nous',
      'menu.contact': 'Contact',
      'menu.language': 'Langue'
    },
    en: {
      'meta.title': 'GameBoxHeroes — Playable modules of classic wargames',
      'meta.description': 'GameBoxHeroes adapts classic wargames to play solo or live with others.',
      'hero.title': 'Playable modules of classic wargames',
      'lead.sub': 'is a project adapting<br>classic wargames to play solo or live with others',
      'feat.assist.title': 'Assisted mode',
      'feat.assist.text': 'Every module has an assisted version<br>that checks each move is legal.',
      'feat.versus.title': 'Better head-to-head games',
      'feat.versus.text': 'A richer experience with <strong>double-blind</strong> play, <strong>blitz</strong>-style timed games and fan-made <strong>variants</strong>',
      'modules.label': 'Modules',
      'modules.arnhem': 'Arnhem: Operation Market-Garden, September 1944, is a two-player Operational level board-wargame originally part of the <span>Westwall quad</span>.',
      'modules.ambush': 'Lead a squad through a series of WWII tactical engagements straight outta Hollywood!',
      'news.title': 'News',
      'news.all': 'See all news',
      'news.date': '01 October 26',
      'news.item1': 'Public testing opens for <span class="news__hl">Arnhem</span>, published in 1976 by SPI.',
      'news.item2': 'Public testing opens for <span class="news__hl">Arnhem</span>, published in 1976 by SPI.',
      'news.more': 'Read more',
      'menu.open': 'Open menu',
      'menu.close': 'Close menu',
      'menu.label': 'Main menu',
      'menu.modules': 'Modules',
      'menu.news': 'News',
      'menu.roadmap': 'Road Map',
      'menu.about': 'About us',
      'menu.contact': 'Contact',
      'menu.language': 'Language'
    }
  };

  // Traductions propres a une page (ex. roadmap-i18n.js), chargees avant ce script
  const pageTranslations = window.GBH_I18N || {};
  Object.keys(translations).forEach((lang) => Object.assign(translations[lang], pageTranslations[lang]));

  const STORAGE_KEY = 'gbh-lang';

  const readStoredLang = () => {
    try { return localStorage.getItem(STORAGE_KEY); } catch { return null; }
  };

  const storeLang = (lang) => {
    try { localStorage.setItem(STORAGE_KEY, lang); } catch { /* stockage indisponible */ }
  };

  const detectLang = () => {
    const fromUrl = new URLSearchParams(location.search).get('lang');
    if (fromUrl && translations[fromUrl]) return fromUrl;
    const stored = readStoredLang();
    if (stored && translations[stored]) return stored;
    return (navigator.language || 'fr').toLowerCase().startsWith('fr') ? 'fr' : 'en';
  };

  const applyLang = (lang) => {
    const dict = translations[lang];

    document.documentElement.lang = lang;

    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const value = dict[el.dataset.i18n];
      if (value != null) el.textContent = value;
    });

    document.querySelectorAll('[data-i18n-html]').forEach((el) => {
      const value = dict[el.dataset.i18nHtml];
      if (value != null) el.innerHTML = value;
    });

    // Format : "attribut:cle" (plusieurs paires separees par ";")
    document.querySelectorAll('[data-i18n-attr]').forEach((el) => {
      el.dataset.i18nAttr.split(';').forEach((pair) => {
        const [attr, key] = pair.split(':');
        if (dict[key] != null) el.setAttribute(attr, dict[key]);
      });
    });

    document.querySelectorAll('.lang__btn').forEach((btn) => {
      btn.setAttribute('aria-pressed', String(btn.dataset.lang === lang));
    });

    document.dispatchEvent(new CustomEvent('gbh:lang', { detail: { lang, dict } }));
  };

  let currentLang = detectLang();
  applyLang(currentLang);

  const switchLang = (lang) => {
    if (lang === currentLang || !translations[lang]) return;
    currentLang = lang;
    storeLang(lang);

    if (reduceMotion) {
      applyLang(lang);
      return;
    }

    // Fondu sortant, echange du texte, fondu entrant
    document.body.classList.add('is-switching');
    setTimeout(() => {
      applyLang(lang);
      requestAnimationFrame(() => document.body.classList.remove('is-switching'));
    }, 180);
  };

  document.querySelectorAll('.lang__btn').forEach((btn) => {
    btn.addEventListener('click', () => switchLang(btn.dataset.lang));
  });

  /* ---------------------------------------------------------------------
     Menu
     --------------------------------------------------------------------- */

  const menu = document.getElementById('menu');
  const burger = document.querySelector('.burger');
  let closeTimer;

  const openMenu = () => {
    clearTimeout(closeTimer);
    menu.hidden = false;
    // Laisse le navigateur peindre l'etat ferme avant de lancer la transition
    requestAnimationFrame(() => requestAnimationFrame(() => menu.classList.add('is-open')));
    burger.setAttribute('aria-expanded', 'true');
    menu.querySelector('.menu__close').focus({ preventScroll: true });
  };

  const closeMenu = () => {
    menu.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    closeTimer = setTimeout(() => { menu.hidden = true; }, reduceMotion ? 0 : 450);
    burger.focus({ preventScroll: true });
  };

  burger.addEventListener('click', openMenu);
  menu.querySelectorAll('[data-close]').forEach((el) => el.addEventListener('click', closeMenu));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !menu.hidden) closeMenu();
  });

  /* ---------------------------------------------------------------------
     Apparition au scroll
     --------------------------------------------------------------------- */

  const reveals = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.2 });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('is-in'));
  }

  /* ---------------------------------------------------------------------
     Parallaxe legere de la photo au mouvement de la souris
     --------------------------------------------------------------------- */

  const photo = document.querySelector('.hero-photo img');
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  if (photo && finePointer && !reduceMotion) {
    const AMPLITUDE = 10;
    let frame = 0;

    window.addEventListener('pointermove', (e) => {
      if (frame) return;
      frame = requestAnimationFrame(() => {
        const x = (e.clientX / window.innerWidth - 0.5) * 2;
        const y = (e.clientY / window.innerHeight - 0.5) * 2;
        photo.style.setProperty('--px', `${(x * AMPLITUDE).toFixed(2)}px`);
        photo.style.setProperty('--py', `${(y * AMPLITUDE * 0.6).toFixed(2)}px`);
        frame = 0;
      });
    });

    document.addEventListener('pointerleave', () => {
      photo.style.setProperty('--px', '0px');
      photo.style.setProperty('--py', '0px');
    });
  }
})();
