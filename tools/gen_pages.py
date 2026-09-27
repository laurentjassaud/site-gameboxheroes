# Genere actualites.html et qui-sommes-nous.html (+ leurs fichiers de traduction)
# a partir des donnees ci-dessous.
# Usage : python tools/gen_pages.py (depuis n importe quel dossier)
import html
import json
import os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MONTHS_FR = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
             'août', 'septembre', 'octobre', 'novembre', 'décembre']
MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             'August', 'September', 'October', 'November', 'December']


def date_fr(iso):
    y, m, d = iso.split('-')
    return f'{d} {MONTHS_FR[int(m) - 1]} {y[2:]}'


def date_en(iso):
    y, m, d = iso.split('-')
    return f'{d} {MONTHS_EN[int(m) - 1]} {y[2:]}'


# ===========================================================================
#  ACTUALITES
# ===========================================================================

NEWS_CATS = {
    'modules':   ('Modules', 'Modules'),
    'platform':  ('Plateforme', 'Platform'),
    'community': ('Communauté', 'Community'),
}

# id, date, categorie, (titre FR, titre EN), (chapo FR, chapo EN), [(paragraphe FR, paragraphe EN), ...]
ARTICLES = [
    ('arnhem-tests-publics', '2026-10-01', 'modules',
     ('Arnhem&nbsp;: ouverture des tests publics', 'Arnhem: public testing opens'),
     ('Mise en ligne des tests publics pour le jeu <span class="news__hl">Arnhem</span> publié en 1976 par SPI.',
      'Public testing opens for <span class="news__hl">Arnhem</span>, published in 1976 by SPI.'),
     [('Le module Arnhem entre en test public. Tous les joueurs inscrits peuvent lancer une partie complète de l’opération Market-Garden, en solo contre l’IA ou à deux.',
       'The Arnhem module is now in public testing. Every registered player can run a full game of Operation Market-Garden, solo against the AI or head-to-head.'),
      ('Cette version couvre le scénario principal et le mode assisté. Vos retours nous aideront à finaliser l’équilibrage et l’ergonomie avant la sortie.',
       'This build covers the main scenario and assisted mode. Your feedback will help us fine-tune balance and usability before release.'),
      ('Un bug, une règle mal interprétée&nbsp;? Écrivez-nous depuis la page <a href="contact.html?subject=bug">Contact</a> en précisant le tour concerné.',
       'Found a bug or a misread rule? Write to us from the <a href="contact.html?subject=bug">Contact</a> page and tell us which turn it happened on.')]),

    ('mode-assiste', '2026-09-15', 'platform',
     ('Le mode assisté arrive dans tous les modules', 'Assisted mode comes to every module'),
     ('Chaque coup joué est vérifié en temps réel&nbsp;: déplacements, empilements, zones de contrôle et ravitaillement.',
      'Every move is checked in real time: movement, stacking, zones of control and supply.'),
     [('Le mode assisté signale immédiatement un coup non conforme aux règles et explique pourquoi, avec la référence de la règle concernée.',
       'Assisted mode flags any illegal move straight away and explains why, citing the relevant rule.'),
      ('Il reste optionnel&nbsp;: les joueurs expérimentés peuvent le désactiver pour retrouver la liberté de la table, comme avec la boîte d’origine.',
       'It stays optional: experienced players can switch it off and enjoy the freedom of the tabletop, just like with the original box.')]),

    ('ambush-missions', '2026-09-02', 'modules',
     ('Ambush!&nbsp;: les missions 1 à 5 en préparation', 'Ambush!: missions 1 to 5 in the works'),
     ('Le classique solo de 1983 arrive sur la plateforme, avec ses paragraphes et ses événements entièrement gérés.',
      'The 1983 solo classic is coming to the platform, with its paragraphs and events fully handled.'),
     [('Dans Ambush!, chaque case peut cacher un événement. La plateforme se charge de consulter les paragraphes au bon moment, sans rien dévoiler à l’avance.',
       'In Ambush!, any hex may hide an event. The platform looks up the paragraphs at the right moment, without spoiling anything ahead of time.'),
      ('Les cinq premières missions sont en cours de développement. Suivez leur avancement sur notre <a href="roadmap.html">road map</a>.',
       'The first five missions are in development. Follow their progress on our <a href="roadmap.html">road map</a>.')]),

    ('double-aveugle-blitz', '2026-07-20', 'platform',
     ('Double aveugle et blitz pour les parties à deux', 'Double-blind and blitz for head-to-head games'),
     ('Deux nouveaux modes pour renouveler les parties entre adversaires, et bientôt les variantes créées par les fans.',
      'Two new modes to refresh head-to-head games, with fan-made variants on the way.'),
     [('En double aveugle, chaque joueur ne voit que les unités repérées par ses propres forces&nbsp;: le brouillard de guerre, sans arbitre.',
       'In double-blind play, each player only sees the units spotted by their own forces: fog of war, no umpire needed.'),
      ('Le mode blitz ajoute une pendule à chaque tour, pour des parties plus nerveuses qui tiennent en une soirée.',
       'Blitz mode adds a clock to every turn, for tenser games that fit into a single evening.')]),

    ('road-map-2026', '2026-06-10', 'community',
     ('Notre road map 2026 est en ligne', 'Our 2026 road map is live'),
     ('24 points à venir, trimestre par trimestre&nbsp;: nouveaux modules, sauvegarde des parties, classement des joueurs…',
      '24 milestones, quarter by quarter: new modules, game saving, player rankings…'),
     [('Nous publions notre feuille de route pour que chacun sache sur quoi nous travaillons et dans quel ordre.',
       'We are publishing our road map so everyone knows what we are working on, and in what order.'),
      ('Elle évoluera avec vos retours. <a href="roadmap.html">Consulter la road map</a>.',
       'It will evolve with your feedback. <a href="roadmap.html">See the road map</a>.')]),

    ('lancement', '2026-05-05', 'community',
     ('GameBoxHeroes se lance', 'GameBoxHeroes is launching'),
     ('Un projet d’adaptation des classiques du wargame, pour jouer en solo ou en direct à plusieurs.',
      'A project adapting classic wargames to play solo or live with others.'),
     [('GameBoxHeroes est né d’une envie simple&nbsp;: rejouer les grands classiques sans passer des heures à préparer la table, et partager ces parties avec d’autres passionnés.',
       'GameBoxHeroes started from a simple wish: to replay the great classics without spending hours setting up the table, and to share those games with fellow enthusiasts.'),
      ('Pour en savoir plus sur le projet et l’équipe, rendez-vous sur la page <a href="qui-sommes-nous.html">Qui sommes-nous</a>.',
       'To learn more about the project and the team, visit the <a href="qui-sommes-nous.html">About us</a> page.')]),
]

# ===========================================================================
#  QUI SOMMES-NOUS
# ===========================================================================

PILLARS = [
    (('Fidélité aux règles', 'Faithful to the rules'),
     ('Nous adaptons les règles d’origine telles qu’elles ont été écrites, errata compris. Pas de simplification cachée.',
      'We adapt the original rules as written, errata included. No hidden simplifications.')),
    (('Le jeu d’abord', 'The game comes first'),
     ('La plateforme gère la mécanique&nbsp;: tirages, tables, résultats. Vous gardez la tête dans la stratégie.',
      'The platform runs the mechanics: dice, tables, results. You keep your mind on strategy.')),
    (('Solo comme à plusieurs', 'Solo or with others'),
     ('Moteurs d’IA pour les jeux solos, parties en direct ou par correspondance pour les jeux à deux.',
      'AI engines for solo games, live or correspondence play for two-player games.')),
    (('Respect des auteurs', 'Respect for the designers'),
     ('Chaque module est développé en accord avec les ayants droit des jeux d’origine.',
      'Every module is developed in agreement with the rights holders of the original games.')),
]

TEAM = [
    (('Game design', 'Game design'),
     ('Lecture des règles, adaptation des scénarios et arbitrage des cas limites.',
      'Reading the rules, adapting scenarios and ruling on edge cases.')),
    (('Développement', 'Development'),
     ('La plateforme, la carte interactive et le jeu en ligne.',
      'The platform, the interactive map and online play.')),
    (('IA & moteurs solo', 'AI & solo engines'),
     ('Les adversaires artificiels et l’automatisation des jeux solos.',
      'AI opponents and the automation of solo games.')),
    (('Communauté & tests', 'Community & testing'),
     ('Les tests publics, vos retours et l’organisation des parties.',
      'Public testing, your feedback and organising games.')),
]

TIMELINE = [
    (('2025', '2025'), ('L’idée', 'The idea'),
     ('Des joueurs lassés de ranger les pions avant la fin de la partie imaginent une table de wargame en ligne.',
      'Players tired of packing up counters before the game is over imagine an online wargame table.')),
    (('Mai 2026', 'May 2026'), ('Lancement du projet', 'Project launch'),
     ('GameBoxHeroes est présenté publiquement avec ses deux premiers modules en chantier.',
      'GameBoxHeroes is publicly announced with its first two modules under way.')),
    (('Juin 2026', 'June 2026'), ('Road map publiée', 'Road map published'),
     ('24 points à venir, partagés avec la communauté.',
      '24 milestones, shared with the community.')),
    (('Octobre 2026', 'October 2026'), ('Premiers tests publics', 'First public tests'),
     ('Arnhem (SPI, 1976) ouvre les tests à tous les joueurs.',
      'Arnhem (SPI, 1976) opens testing to all players.')),
]


# ===========================================================================
#  Outils communs
# ===========================================================================

class Page:
    """Accumule les textes FR / EN d'une page et produit le HTML correspondant."""

    def __init__(self):
        self.fr, self.en = {}, {}

    def k(self, key, fr, en):
        self.fr[key], self.en[key] = fr, en
        return key

    def t(self, key, fr, en, tag='p', cls='', attrs=''):
        """Element traduisible : le HTML statique contient le francais."""
        self.k(key, fr, en)
        c = f' class="{cls}"' if cls else ''
        a = f' {attrs}' if attrs else ''
        return f'<{tag}{c}{a} data-i18n-html="{key}">{fr}</{tag}>'


def chrome(p, *, file, meta_title, meta_desc, intro, right, body, css, scripts, current):
    p.k('meta.title', *meta_title)
    p.k('meta.description', *meta_desc)
    p.k('hero.title', 'Modules jouables de wargames classiques', 'Playable modules of classic wargames')
    p.k('rm.back', 'Retour à l’accueil', 'Back to home')

    def menu_link(href, key, label):
        cur = ' aria-current="page" data-close' if href == current else ''
        return f'      <li><a href="{href}"{cur} data-i18n="{key}">{label}</a></li>'

    links = '\n'.join([
        menu_link('index.html#modules', 'menu.modules', 'Modules'),
        menu_link('actualites.html', 'menu.news', 'Actualités'),
        menu_link('roadmap.html', 'menu.roadmap', 'Road Map'),
        menu_link('qui-sommes-nous.html', 'menu.about', 'Qui sommes-nous'),
        menu_link('contact.html', 'menu.contact', 'Contact'),
    ])
    css_links = '\n'.join(f'<link rel="stylesheet" href="{c}">' for c in css)
    js_tags = '\n'.join(f'<script src="{j}"></script>' for j in scripts)

    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title data-i18n="meta.title">{meta_title[0]}</title>
<meta name="description" data-i18n-attr="content:meta.description" content="{html.escape(meta_desc[0])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Red+Hat+Text:wght@300;400;500;600;700&display=swap" rel="stylesheet">
{css_links}
</head>
<body>
<!-- Fichier genere par tools/gen_pages.py : modifier les donnees la-bas, pas ce HTML -->
<div class="page">
  <div class="stage rm-top">

    <div class="map" aria-hidden="true">
      <img src="assets/map.png" alt="">
    </div>

    <header class="header">
      <div class="brand">
        <a class="brand__logo" href="index.html" data-i18n-attr="aria-label:rm.back" aria-label="Retour à l’accueil">
          <img class="brand__logo-hex" src="assets/logo-hex.svg" alt="" width="139" height="156">
          <img class="brand__logo-text" src="assets/logo-text.svg" alt="GameBoxHeroes" width="78" height="55">
        </a>
        <p class="brand__title" data-i18n="hero.title">Modules jouables de wargames classiques</p>
      </div>
      <button class="burger" type="button" aria-expanded="false" aria-controls="menu" data-i18n-attr="aria-label:menu.open" aria-label="Ouvrir le menu">
        <span></span><span></span><span></span>
      </button>
    </header>

    <div class="hero-photo" aria-hidden="true">
      <img src="assets/hero-photo.png" alt="" width="600" height="465">
    </div>

{intro}

{right}
  </div>

  <main class="rm-body">
{body}

    <footer class="rm-foot">
      <span class="rule-line rule-line--main" aria-hidden="true"></span>
      <span class="rule-line rule-line--side" aria-hidden="true"></span>
      <a class="rm-back" href="index.html" data-i18n="rm.back">Retour à l’accueil</a>
      <div class="rm-sign">
        <p class="year">2026</p>
        <a class="mark" href="index.html" aria-label="GameBoxHeroes">
          <img src="assets/logo-mark.svg" alt="" width="65" height="73">
        </a>
      </div>
    </footer>
  </main>
</div>

<div class="menu" id="menu" hidden>
  <div class="menu__backdrop" data-close></div>
  <nav class="menu__panel" data-i18n-attr="aria-label:menu.label" aria-label="Menu principal">
    <button class="menu__close" type="button" data-close data-i18n-attr="aria-label:menu.close" aria-label="Fermer le menu">
      <span></span><span></span>
    </button>
    <ul class="menu__links">
{links}
    </ul>
    <div class="lang" role="group" data-i18n-attr="aria-label:menu.language" aria-label="Langue">
      <button type="button" class="lang__btn" data-lang="fr" lang="fr">FR</button>
      <span class="lang__sep" aria-hidden="true">/</span>
      <button type="button" class="lang__btn" data-lang="en" lang="en">EN</button>
    </div>
  </nav>
</div>

<script src="{file.replace('.html', '-i18n.js')}"></script>
<script src="script.js"></script>
{js_tags}
</body>
</html>
'''


def intro_block(p, headline, label, text):
    return f'''    <section class="intro">
      {p.t('pg.headline', *headline, tag='h1', cls='intro__headline')}
      <div class="intro__news">
        {p.t('pg.label', *label, cls='intro__label')}
        {p.t('pg.text', *text, cls='intro__text')}
      </div>
    </section>'''


def write(file, page_html, p):
    with open(os.path.join(OUT, file), 'w', encoding='utf-8', newline='\n') as f:
        f.write(page_html)
    i18n = file.replace('.html', '-i18n.js')
    with open(os.path.join(OUT, i18n), 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'// Fichier genere par tools/gen_pages.py : textes FR / EN de {file}.\n')
        f.write('window.GBH_I18N = ' + json.dumps({'fr': p.fr, 'en': p.en}, ensure_ascii=False, indent=2) + ';\n')


# ===========================================================================
#  Page Actualites
# ===========================================================================

def build_news():
    p = Page()
    for c, (f, e) in NEWS_CATS.items():
        p.k(f'cat.{c}', f, e)
    p.k('news.all', 'Tout', 'All')
    p.k('news.more', 'Lire la suite', 'Read more')
    p.k('news.less', 'Réduire', 'Show less')
    p.k('news.count.one', '{n} article', '{n} article')
    p.k('news.count.other', '{n} articles', '{n} articles')
    p.k('news.filters', 'Filtrer par thème', 'Filter by theme')
    p.k('news.featured', 'À la une', 'Featured')

    intro = intro_block(
        p,
        ('Le journal<br>du projet', 'The<br>project log'),
        ('Actualités', 'News'),
        ('Sorties de modules, tests publics, nouveautés de la plateforme&nbsp;: toutes les nouvelles du projet, de la plus récente à la plus ancienne.',
         'Module releases, public tests, platform updates: all the project news, newest first.'))

    # Colonne de droite : les deux modules a la une (memes cartes que l'accueil)
    right = f'''    <section class="modules" data-i18n-attr="aria-label:news.featured" aria-label="À la une">
      <a class="module" href="#arnhem-tests-publics" data-open>
        <div class="module__cover module__cover--center">
          <img src="assets/cover-arnhem.jpg" alt="Arnhem: Operation Market-Garden" width="210" height="266">
        </div>
        <div class="module__card">
          <h2 class="module__title">A Bridge Too Far: Arnhem (1976)</h2>
          {p.t('feat.arnhem', 'Tests publics ouverts à tous les joueurs&nbsp;: scénario principal et mode assisté.', 'Public testing open to all players: main scenario and assisted mode.', cls='module__desc')}
          <img class="module__arrow" src="assets/arrow.svg" alt="" width="30" height="31">
        </div>
      </a>
      <a class="module" href="#ambush-missions" data-open>
        <div class="module__cover module__cover--top">
          <img src="assets/cover-ambush.jpg" alt="Ambush!" width="150" height="206">
        </div>
        <div class="module__card">
          <h2 class="module__title">Ambush! (1983)</h2>
          {p.t('feat.ambush', 'Les missions 1 à 5 sont en préparation.', 'Missions 1 to 5 are in the works.', cls='module__desc module__desc--low')}
          <img class="module__arrow" src="assets/arrow.svg" alt="" width="30" height="31">
        </div>
      </a>
    </section>'''

    chips = ['        <button type="button" class="chip" data-filter="all" aria-pressed="true" data-i18n="news.all">Tout</button>']
    for c, (f, _) in NEWS_CATS.items():
        chips.append(f'        <button type="button" class="chip" data-filter="{c}" aria-pressed="false" data-i18n="cat.{c}">{f}</button>')

    articles = []
    for i, (aid, iso, cat, title, lede, paras) in enumerate(ARTICLES, 1):
        p.k(f'a{i}.date', date_fr(iso), date_en(iso))
        body = '\n'.join(f'            {p.t(f"a{i}.p{j}", fr, en)}' for j, (fr, en) in enumerate(paras, 1))
        articles.append(f'''      <article class="article reveal" id="{aid}" data-cat="{cat}">
        <div class="article__meta">
          <time datetime="{iso}" data-i18n="a{i}.date">{date_fr(iso)}</time>
          <span class="tag" data-i18n="cat.{cat}">{NEWS_CATS[cat][0]}</span>
        </div>
        <div class="article__main">
          {p.t(f'a{i}.title', *title, tag='h2', cls='article__title')}
          {p.t(f'a{i}.lede', *lede, cls='article__lede')}
          <div class="article__body" id="{aid}-body" hidden>
{body}
          </div>
          <button class="article__toggle" type="button" aria-expanded="false" aria-controls="{aid}-body">
            <span data-i18n="news.more">Lire la suite</span>
            <img src="assets/arrow.svg" alt="" width="30" height="31">
          </button>
        </div>
      </article>''')

    body = f'''    <div class="rm-toolbar">
      <span class="rule-line rule-line--main" aria-hidden="true"></span>
      <span class="rule-line rule-line--side" aria-hidden="true"></span>
      <div class="chips" role="group" data-i18n-attr="aria-label:news.filters" aria-label="Filtrer par thème">
{chr(10).join(chips)}
      </div>
      <p class="rm-count" aria-live="polite">{len(ARTICLES)} articles</p>
    </div>

    <div class="articles">
{chr(10).join(articles)}
    </div>'''

    page = chrome(p, file='actualites.html',
                  meta_title=('GameBoxHeroes — Actualités', 'GameBoxHeroes — News'),
                  meta_desc=('Toutes les nouvelles de GameBoxHeroes : modules, tests publics et nouveautés de la plateforme.',
                             'All the GameBoxHeroes news: modules, public tests and platform updates.'),
                  intro=intro, right=right, body=body,
                  css=['style.css', 'roadmap.css', 'pages.css'], scripts=['news.js'],
                  current='actualites.html')
    write('actualites.html', page, p)


# ===========================================================================
#  Page Qui sommes-nous
# ===========================================================================

def build_about():
    p = Page()

    intro = intro_block(
        p,
        ('Des joueurs<br>au service du jeu', 'Players<br>serving the game'),
        ('Qui sommes-nous', 'About us'),
        ('GameBoxHeroes est né d’une envie simple&nbsp;: rejouer les grands classiques du wargame sans passer des heures à préparer la table, et partager ces parties avec d’autres passionnés.',
         'GameBoxHeroes started from a simple wish: to replay the great wargame classics without spending hours setting up the table, and to share those games with fellow enthusiasts.'))

    stats = [
        ('2', ('Modules en développement', 'Modules in development')),
        ('24', ('Points à la road map 2026', 'Milestones on the 2026 road map')),
        ('2', ('Langues&nbsp;: français et anglais', 'Languages: French and English')),
    ]
    right = '    <ul class="rm-stats" data-i18n-attr="aria-label:about.figures" aria-label="Chiffres clés">\n'
    p.k('about.figures', 'Chiffres clés', 'Key figures')
    for i, (val, label) in enumerate(stats, 1):
        right += f'''      <li class="stat">
        <span class="stat__value">{val}</span>
        {p.t(f'stat{i}', *label, tag='span', cls='stat__label')}
      </li>
'''
    right += '    </ul>'

    pillars = '\n'.join(f'''        <li class="pillar reveal" style="--i:{i - 1}">
          <img class="pillar__hex" src="assets/hex-bullet.svg" alt="" width="31" height="34">
          <span class="pillar__num">{i:02d}</span>
          {p.t(f'pillar{i}.title', *title, tag='h3', cls='pillar__title')}
          {p.t(f'pillar{i}.text', *text, cls='pillar__text')}
        </li>''' for i, (title, text) in enumerate(PILLARS, 1))

    team = '\n'.join(f'''        <li class="member reveal" style="--i:{i - 1}">
          <span class="member__hex" aria-hidden="true">{i:02d}</span>
          {p.t(f'team{i}.role', *role, tag='h3', cls='member__role')}
          {p.t(f'team{i}.text', *text, cls='member__text')}
        </li>''' for i, (role, text) in enumerate(TEAM, 1))

    timeline = '\n'.join(f'''        <li class="step reveal" style="--i:{i - 1}">
          {p.t(f'step{i}.when', *when, tag='span', cls='step__when')}
          {p.t(f'step{i}.title', *title, tag='h3', cls='step__title')}
          {p.t(f'step{i}.text', *text, cls='step__text')}
        </li>''' for i, (when, title, text) in enumerate(TIMELINE, 1))

    body = f'''    <section class="block block--split">
      <span class="rule-line rule-line--main" aria-hidden="true"></span>
      <span class="rule-line rule-line--side" aria-hidden="true"></span>
      <div class="block__main reveal">
        {p.t('mission.label', 'Notre mission', 'Our mission', tag='h2', cls='block__label')}
        {p.t('mission.title', 'Rendre les classiques du wargame jouables, fidèlement, par tous.', 'Making classic wargames playable, faithfully, by everyone.', cls='block__statement')}
        {p.t('mission.p1', 'Beaucoup de grands wargames dorment dans des boîtes faute de temps, de place ou d’adversaire. Nous les adaptons en modules jouables en ligne, en conservant leurs règles, leurs cartes et leurs pions.', 'Many great wargames sit in their boxes for lack of time, space or an opponent. We adapt them into modules you can play online, keeping their rules, maps and counters.', cls='block__text')}
        {p.t('mission.p2', 'La plateforme s’occupe de tout ce qui ralentit une partie sur table&nbsp;: mise en place, tirages, consultation des tables, vérification des coups. Il ne reste que les décisions.', 'The platform takes care of everything that slows down a tabletop game: set-up, dice, table look-ups, move checking. Only the decisions are left.', cls='block__text')}
      </div>
      <aside class="block__side reveal">
        {p.t('mission.side.label', 'Ce que nous ne faisons pas', 'What we don’t do', tag='h3', cls='side__label')}
        {p.t('mission.side.text', 'Nous ne réécrivons pas les jeux. Quand une règle est ambiguë, nous suivons les errata officiels et documentons nos choix.', 'We don’t rewrite the games. When a rule is ambiguous, we follow the official errata and document our choices.', cls='side__text')}
      </aside>
    </section>

    <section class="block">
      {p.t('pillars.label', 'Ce qui nous guide', 'What guides us', tag='h2', cls='block__label block__label--head')}
      <ul class="pillars">
{pillars}
      </ul>
    </section>

    <section class="block">
      {p.t('team.label', 'L’équipe', 'The team', tag='h2', cls='block__label block__label--head')}
      {p.t('team.intro', 'Une petite équipe de joueurs et de développeurs, réunis autour des mêmes boîtes de jeu.', 'A small team of players and developers, brought together by the same game boxes.', cls='block__intro')}
      <ul class="team">
{team}
      </ul>
    </section>

    <section class="block">
      {p.t('story.label', 'Notre histoire', 'Our story', tag='h2', cls='block__label block__label--head')}
      <ol class="timeline">
{timeline}
      </ol>
    </section>

    <section class="cta reveal">
      {p.t('cta.title', 'Envie de participer&nbsp;?', 'Want to get involved?', tag='h2', cls='cta__title')}
      {p.t('cta.text', 'Testeurs, joueurs, auteurs de variantes&nbsp;: la plateforme se construit avec vous.', 'Testers, players, variant designers: the platform is being built with you.', cls='cta__text')}
      <div class="cta__actions">
        <a class="btn btn--red" href="contact.html"><span data-i18n="cta.contact">Nous écrire</span><img src="assets/arrow.svg" alt="" width="30" height="31"></a>
        <a class="btn" href="roadmap.html" data-i18n="cta.roadmap">Voir la road map</a>
      </div>
    </section>'''
    p.k('cta.contact', 'Nous écrire', 'Write to us')
    p.k('cta.roadmap', 'Voir la road map', 'See the road map')

    page = chrome(p, file='qui-sommes-nous.html',
                  meta_title=('GameBoxHeroes — Qui sommes-nous', 'GameBoxHeroes — About us'),
                  meta_desc=('GameBoxHeroes adapte les classiques du wargame pour jouer en solo ou en direct à plusieurs. Notre mission, nos principes, notre équipe.',
                             'GameBoxHeroes adapts classic wargames to play solo or live with others. Our mission, principles and team.'),
                  intro=intro, right=right, body=body,
                  css=['style.css', 'roadmap.css', 'pages.css'], scripts=[],
                  current='qui-sommes-nous.html')
    write('qui-sommes-nous.html', page, p)


build_news()
build_about()
print('ok')
