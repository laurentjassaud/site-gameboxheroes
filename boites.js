(() => {
  'use strict';

  /* =====================================================================
     Bande de boites de la page Les boîtes : une seule ligne horizontale qui
     boucle sans fin. Mecanique et valeurs reprises de mschristensen.com
     (liste « Selected work ») :
       - derive permanente de 1 px par image, dans le sens du dernier geste ;
       - molette / glisser au doigt = impulsion, amortie de 6 % par image ;
       - les boites s'elargissent avec la vitesse, puis reviennent en ressort ;
       - les couvertures glissent un peu dans leur cadre (parallaxe).

     Sans JavaScript, ou si l'utilisateur demande moins d'animations, la
     bande reste une liste a defilement horizontal natif (boites.css).
     ===================================================================== */

  const reel = document.querySelector('.reel');
  const track = reel && reel.querySelector('.reel__track');
  if (!track || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const FRAME = 1000 / 60;        // les vitesses sont en px par image a 60 i/s
  const FRICTION = 0.94;          // amortissement de l'impulsion, par image
  const MAX_SPEED = 70;           // plafond de l'impulsion
  const WHEEL_GAIN = 0.08;
  const TOUCH_GAIN = 0.34;
  const DRAG_THRESHOLD = 12;      // au-dela, un glisser n'est plus un clic
  const STRETCH_FWD = 0.14;       // +14 % de largeur a pleine vitesse
  const STRETCH_BACK = -0.1;      // -10 % en sens inverse
  const STRETCH_FOLLOW = 450;     // ms, courbe power3.out
  const STRETCH_RETURN = 1100;    // ms, retour elastique
  const SLOW = 3;                 // sous cette vitesse la largeur revient a la normale
  const DRIFT = 40;               // parallaxe max des couvertures (80 px sur le site
                                  // modele ; reduit pour ne pas rogner les boites)
  const HOLD = 1600;              // ms sans derive, le temps de l'apparition

  const originals = [...track.children];
  const count = originals.length;
  // Sa hauteur ne depend pas de l'etirement : sert a reperer un changement de taille
  const visual = originals[0].querySelector('.reel__visual');

  let visualHeight = 0;
  let width = 0;                  // largeur d'une boite au repos
  let live = 0;                   // largeur courante (etiree)
  let view = 0;                   // largeur visible de la bande
  let images = [];
  let position = 0;               // defilement, en nombre de boites
  let impulse = 0;
  let direction = 1;
  let stretch = 0;
  let returning = false;
  let returnFrom = 0;
  let returnStart = 0;
  let last = 0;
  let frame = 0;
  let visible = false;
  const holdUntil = performance.now() + HOLD;

  const clamp = (v, min, max) => Math.min(max, Math.max(min, v));
  const mod = (v, m) => ((v % m) + m) % m;

  // elastic.out(0.62, 0.32) de GSAP
  const elasticOut = (p) => {
    if (p >= 1) return 1;
    const period = 0.32 / 0.62;
    return Math.pow(2, -10 * p) * Math.sin((p - period / 4) * (2 * Math.PI / period)) + 1;
  };

  /* ---------------------------------------------------------------------
     Mise en place : copies pour la boucle, mesures
     --------------------------------------------------------------------- */

  const build = () => {
    track.querySelectorAll('[data-clone]').forEach((el) => el.remove());
    track.style.removeProperty('--reel-live');

    width = originals[0].getBoundingClientRect().width;
    view = reel.clientWidth;
    visualHeight = visual.offsetHeight;
    live = width * (1 + stretch);

    // Assez de copies pour couvrir la bande meme quand les boites retrecissent
    const copies = Math.ceil(view / (count * width * (1 + STRETCH_BACK))) + 1;
    for (let c = 1; c < copies; c++) {
      originals.forEach((item) => {
        const clone = item.cloneNode(true);
        clone.dataset.clone = '';
        clone.setAttribute('aria-hidden', 'true');
        clone.querySelectorAll('a').forEach((a) => { a.tabIndex = -1; });
        track.appendChild(clone);
      });
    }
    images = [...track.querySelectorAll('.reel__visual img')];
  };

  // Apparition en cascade des boites visibles au chargement (boites.css)
  const enter = () => {
    const x = -mod(position, count) * width;
    let rank = 0;
    [...track.children].forEach((item, i) => {
      const left = x + i * width;
      if (left + width > 0 && left < view) {
        item.style.setProperty('--i', rank++);
        item.dataset.enter = '';
      }
    });
  };

  /* ---------------------------------------------------------------------
     Boucle d'animation
     --------------------------------------------------------------------- */

  const tick = (now) => {
    frame = requestAnimationFrame(tick);
    const dt = Math.min(50, now - last);
    const frames = dt / FRAME;
    last = now;

    const speed = impulse + (now < holdUntil ? 0 : direction);
    const pace = Math.min(1, Math.abs(speed) / MAX_SPEED);

    // Largeur des boites : suit la vitesse, puis revient en ressort
    const target = (speed >= 0 ? STRETCH_FWD : STRETCH_BACK) * pace;
    if (Math.abs(speed) >= SLOW) returning = false;
    else if (!returning && Math.abs(stretch) > 0.002) {
      returning = true;
      returnFrom = stretch;
      returnStart = now;
    }
    if (returning) {
      stretch = returnFrom * (1 - elasticOut((now - returnStart) / STRETCH_RETURN));
    } else {
      stretch += (target - stretch) * (1 - Math.pow(1 - Math.min(1, dt / STRETCH_FOLLOW), 4));
    }
    const next = width * (1 + stretch);
    if (Math.abs(next - live) > 0.05) {
      live = next;
      track.style.setProperty('--reel-live', `${live}px`);
    }

    position += (speed * frames) / live;
    const x = -mod(position, count) * live;
    track.style.transform = `translate3d(${x}px,0,0)`;

    // Parallaxe : chaque couverture glisse vers le centre de la bande
    const depth = DRIFT * (0.5 + 0.5 * pace);
    for (let i = 0; i < images.length; i++) {
      const left = x + i * live;
      if (left > view || left + live < 0) continue;
      const offset = (view / 2 - (left + live / 2)) / view;
      images[i].style.transform = `translate3d(${offset * depth}px,0,0)`;
    }

    impulse *= Math.pow(FRICTION, frames);
    if (Math.abs(impulse) < 0.01) impulse = 0;
  };

  const run = () => {
    const on = visible && !document.hidden;
    if (on && !frame) {
      last = performance.now();
      frame = requestAnimationFrame(tick);
    } else if (!on && frame) {
      cancelAnimationFrame(frame);
      frame = 0;
    }
  };

  const push = (amount) => {
    impulse = clamp(impulse + amount, -MAX_SPEED, MAX_SPEED);
    direction = amount > 0 ? 1 : -1;
  };

  /* ---------------------------------------------------------------------
     Molette : fait tourner la bande sans bloquer le defilement de la page.
     Seul un geste horizontal au-dessus de la bande est retenu, pour ne pas
     declencher le « page precedente » du navigateur.
     --------------------------------------------------------------------- */

  window.addEventListener('wheel', (e) => {
    if (!visible) return;
    let delta = Math.abs(e.deltaX) >= Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
    if (e.deltaMode === 1) delta *= 16;
    else if (e.deltaMode === 2) delta *= window.innerHeight;
    if (delta) push(delta * WHEEL_GAIN);
  }, { passive: true });

  reel.addEventListener('wheel', (e) => {
    if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) e.preventDefault();
  }, { passive: false });

  /* ---------------------------------------------------------------------
     Doigt : glisser horizontalement (le defilement vertical reste natif)
     --------------------------------------------------------------------- */

  let touchId = null;
  let touchX = 0;
  let dragged = 0;

  reel.addEventListener('pointerdown', (e) => {
    if (e.pointerType === 'mouse') return;
    touchId = e.pointerId;
    touchX = e.clientX;
    dragged = 0;
  });

  reel.addEventListener('pointermove', (e) => {
    if (e.pointerId !== touchId) return;
    const dx = e.clientX - touchX;
    touchX = e.clientX;
    dragged += Math.abs(dx);
    if (dx) push(-dx * TOUCH_GAIN);
  });

  const release = (e) => { if (e.pointerId === touchId) touchId = null; };
  reel.addEventListener('pointerup', release);
  reel.addEventListener('pointercancel', release);

  reel.addEventListener('click', (e) => {
    if (dragged > DRAG_THRESHOLD) e.preventDefault();
    dragged = 0;
  }, true);

  /* ---------------------------------------------------------------------
     Clavier : la boite qui recoit le focus vient au centre, sans animation
     --------------------------------------------------------------------- */

  track.addEventListener('focusin', (e) => {
    const index = originals.indexOf(e.target.closest('.reel__item'));
    if (index < 0 || !e.target.matches(':focus-visible')) return;
    position = index - (view - live) / (2 * live);
    impulse = 0;
  });

  /* ---------------------------------------------------------------------
     Demarrage
     --------------------------------------------------------------------- */

  reel.classList.add('is-live');
  build();
  // La premiere boite demarre alignee sur la marge de la page
  position = -document.querySelector('.topbar').getBoundingClientRect().left / width;
  enter();

  let resizeFrame = 0;
  new ResizeObserver(() => {
    cancelAnimationFrame(resizeFrame);
    resizeFrame = requestAnimationFrame(() => {
      if (reel.clientWidth !== view || visual.offsetHeight !== visualHeight) build();
    });
  }).observe(reel);

  new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    run();
  }).observe(reel);

  document.addEventListener('visibilitychange', run);
})();
