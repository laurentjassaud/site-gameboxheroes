# Genere index.html + index-i18n.js (accueil, maquette Figma node 127:127).
# Usage : python tools/gen_home.py
from layout import Page, topbar, render, boxes, covers, COVERS, CREDIT

p = Page()

top = f'''{topbar(home=True)}

    <div class="hero cols">
      <div class="hero__lead">
        <h1 class="wordmark">Game<span>Box</span>Heroes</h1>
        {p.t('home.lead',
             # Espace avant chaque <br> : sur mobile home.css masque les <br>,
             # sans elle les mots se colleraient
             'est un site personnel dans lequel je développe <br>l’adaptation de classiques du wargame <br>pour jouer en solo ou en direct <br>et à plusieurs',
             'is a personal site where I build <br>adaptations of classic wargames <br>to play solo, or live <br>with other players',
             cls='hero__text')}
      </div>
      <section class="latest" id="modules" aria-labelledby="latest-title">
        {p.t('home.latest', 'Dernières boîtes', 'Latest boxes', tag='h2', cls='latest__title', attrs='id="latest-title"')}
        {boxes(p)}
      </section>
    </div>
    {CREDIT}'''

# ---------- Travail en cours ----------
WORK = [
    ('assets/home/work-1.webp', ('Carte de jeu', 'Game map'), ('Test public', 'Public test'),
     ('Le jeu <a href="actualites.html#arnhem-tests-publics">Arnhem</a> publié en 1976 par SPI est prêt à être testé&nbsp;: ouverture de la bêta publique.',
      'The <a href="actualites.html#arnhem-tests-publics">Arnhem</a> game published in 1976 by SPI is ready for testing: the public beta is open.')),
    ('assets/home/work-2.webp', ('Pions sur la carte', 'Counters on the map'), ('Sur la table', 'On the table'),
     ('Enemy Action: Kharkov', 'Enemy Action: Kharkov')),
    ('assets/home/work-3.webp', ('Partie en cours sur une carte', 'Game in progress on a map'), ('Mise en ligne', 'Going live'),
     ('Accès public du site GameBoxHeroes. L’aventure commence&nbsp;!', 'The GameBoxHeroes site is now public. The adventure begins!')),
]

work = []
for i, (img, alt, title, text) in enumerate(WORK, 1):
    p.k(f'work{i}.alt', *alt)
    work.append(f'''          <li class="work__item reveal">
            <img class="work__img" src="{img}" data-i18n-attr="alt:work{i}.alt" alt="{alt[0]}" width="386" height="288" loading="lazy">
            {p.t(f'work{i}.title', *title, tag='h3', cls='work__title')}
            {p.t(f'work{i}.text', *text, cls='work__text')}
          </li>''')

# ---------- Particularites des boites ----------
SPECS = [
    (('Mode assisté', 'Assisted mode'),
     [('Toutes les boîtes auront la possibilité de jouer dans un mode assisté qui vérifiera la légalité des actions. Les règles seront implémentées en incluant les <em>Questions &amp; Answers</em> du forum BoardGameGeek. Bien sûr, un mode libre permettra aux joueurs de jouer sans assistance.',
       'Every box will offer an assisted mode that checks every action is legal. Rules will be implemented including the <em>Questions &amp; Answers</em> from the BoardGameGeek forum. Of course, a free mode will let players play without assistance.')]),
    (('Parties optimisées en «&nbsp;face à face&nbsp;»', 'Better head-to-head games'),
     [('Amélioration de l’expérience de jeu par <em>double aveugle</em>, partie chronométrée type <em>blitz</em> et ajout de toutes les <em>variantes</em>, notamment celles créées par les fans.',
       'A richer experience with <em>double-blind</em> play, <em>blitz</em>-style timed games and every <em>variant</em>, including fan-made ones.')]),
    (('Jeu solo', 'Solo play'),
     [('Pour les <strong>jeux solos</strong>, l’interface de la boîte active rigoureusement tout le système du <em>moteur solo</em>. Différents niveaux de contrôle permettent soit de tirer soi-même les dés sur les différents <em>flowcharts</em>, soit de laisser l’interface résoudre les réponses du moteur de jeu pour ne se consacrer qu’à la stratégie.',
       'For <strong>solo games</strong>, the box interface runs the whole <em>solo engine</em> faithfully. Several levels of control let you roll the dice yourself on the various <em>flowcharts</em>, or let the interface resolve the engine’s responses so you can focus on strategy.'),
      ('Pour les jeux prévus à <strong>deux joueurs</strong>, un travail sur une IA symbolique est en cours&nbsp;: il permettra d’avoir un adversaire compétent sur tous les jeux.',
       'For games designed for <strong>two players</strong>, work on a symbolic AI is under way: it will provide a capable opponent in every game.')]),
]

specs = []
for i, (title, paras) in enumerate(SPECS, 1):
    body = '\n'.join(f'            {p.t(f"spec{i}.p{j}", *para, cls="spec__text")}' for j, para in enumerate(paras, 1))
    specs.append(f'''          <div class="spec reveal">
            {p.t(f'spec{i}.title', *title, tag='h3', cls='spec__title')}
{body}
          </div>''')

body = f'''  <div class="wrap cols home-sec">
    <section class="work ruled" aria-labelledby="work-title">
      <div class="sec-head">
        {p.t('home.work', 'Travail en cours', 'Work in progress', tag='h2', cls='sec-title', attrs='id="work-title"')}
        {p.t('home.more', 'En voir plus', 'See more', tag='a', cls='link-more', attrs='href="actualites.html"')}
      </div>
      <ul class="work__list">
{chr(10).join(work)}
      </ul>
    </section>
    <section class="specs ruled" aria-labelledby="specs-title">
      {p.t('home.specs', 'Particularités des boîtes', 'What makes the boxes special', tag='h2', cls='sec-title', attrs='id="specs-title"')}
{chr(10).join(specs)}
    </section>
  </div>

  <section class="prep" aria-labelledby="prep-title">
    <div class="wrap cols">
      <div class="ruled">
        {p.t('home.prep', 'Les boîtes en préparation', 'Boxes in the works', tag='h2', cls='prep__title', attrs='id="prep-title"')}
      </div>
      <div class="ruled" aria-hidden="true"></div>
    </div>
{covers(p, COVERS[:4])}
  </section>

  <section class="about wrap reveal">
    <p class="wordmark" aria-hidden="true">Game<span>Box</span>Heroes</p>
    {p.t('home.about',
         '<span class="sr-only">GameBoxHeroes </span>est un site personnel et non commercial, développé en temps libre par passion des wargames et des jeux en solo',
         '<span class="sr-only">GameBoxHeroes </span>is a personal, non-commercial site, built in spare time out of a passion for wargames and solo games',
         cls='about__text')}
  </section>'''

render(p, file='index.html',
       meta_title=('Wargames classiques en ligne, en solo ou à deux — GameBoxHeroes',
                   'Classic wargames online, solo or head-to-head — GameBoxHeroes'),
       meta_desc=('GameBoxHeroes adapte les classiques du wargame (Arnhem, Ambush!, Patton’s Best…) pour jouer en ligne, en solo ou à deux, avec un mode assisté qui vérifie les règles.',
                  'GameBoxHeroes adapts classic wargames (Arnhem, Ambush!, Patton’s Best…) for online play, solo or head-to-head, with an assisted mode that checks the rules.'),
       top=top, body=body, css=['home.css'], body_class='home', generator='tools/gen_home.py')
