# Genere roadmap.html + roadmap-i18n.js a partir d une seule source de donnees.
# Usage : python tools/gen_roadmap.py (depuis n importe quel dossier)
import json, html, os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CATS = {
    "modules":   ("Modules", "Modules"),
    "platform":  ("Plateforme", "Platform"),
    "community": ("Communauté", "Community"),
    "solo":      ("Solo & IA", "Solo & AI"),
}
STATUS = {
    "progress": ("En cours", "In progress"),
    "planned":  ("Planifié", "Planned"),
    "study":    ("À l’étude", "Exploring"),
}
QUARTERS = [
    ("T1", "Q1", "Janvier – Mars 2026", "January – March 2026"),
    ("T2", "Q2", "Avril – Juin 2026", "April – June 2026"),
    ("T3", "Q3", "Juillet – Septembre 2026", "July – September 2026"),
    ("T4", "Q4", "Octobre – Décembre 2026", "October – December 2026"),
]

# (trimestre, categorie, statut, titre FR, texte FR, titre EN, texte EN)
ITEMS = [
    # T1
    (0, "modules", "progress",
     "Ambush! — missions 1 à 5",
     "Les cinq premières missions d’Ambush! jouables en solo, avec paragraphes, événements et tirages entièrement gérés par la plateforme.",
     "Ambush! — missions 1 to 5",
     "The first five Ambush! missions playable solo, with paragraphs, events and draws fully handled by the platform."),
    (0, "platform", "progress",
     "Mémorisation des parties",
     "Sauvegarde automatique à chaque action&nbsp;: reprenez une partie exactement où vous l’avez laissée, sur n’importe quel appareil.",
     "Game saving",
     "Automatic save on every action: pick a game up exactly where you left it, on any device."),
    (0, "solo", "progress",
     "Aide de jeu pour modules solo",
     "Un assistant de règles contextuel qui explique chaque étape, rappelle les tables à consulter et signale les oublis.",
     "Play aid for solo modules",
     "A contextual rules assistant that explains each step, points to the right tables and flags anything you missed."),
    (0, "modules", "planned",
     "A Bridge Too Far&nbsp;: Arnhem complet",
     "Tous les scénarios d’Arnhem 1976, du largage du 17 septembre au repli sur le Rhin.",
     "Full A Bridge Too Far: Arnhem",
     "Every Arnhem 1976 scenario, from the 17 September drop to the withdrawal across the Rhine."),
    (0, "platform", "planned",
     "Historique et replay",
     "Rejouez une partie tour par tour pour revoir chaque décision, chaque tir et chaque résultat de dés.",
     "History and replay",
     "Replay a game turn by turn to review every decision, every shot and every die roll."),
    (0, "community", "planned",
     "Profils joueurs",
     "Un profil public avec vos modules favoris, vos parties terminées et vos factions de prédilection.",
     "Player profiles",
     "A public profile with your favourite modules, completed games and preferred factions."),
    # T2
    (1, "community", "planned",
     "Classement des joueurs",
     "Un classement Elo par module et un classement général, calculés uniquement sur les parties classées.",
     "Player rankings",
     "An Elo ranking per module plus an overall leaderboard, based on ranked games only."),
    (1, "modules", "planned",
     "Ambush! — nouvelles missions 6 à 11",
     "Six nouvelles missions en Normandie et dans le bocage, avec de nouveaux profils d’ennemis.",
     "Ambush! — new missions 6 to 11",
     "Six new missions in Normandy and the bocage, featuring new enemy profiles."),
    (1, "solo", "planned",
     "Niveaux de difficulté de l’IA",
     "Trois réglages pour les moteurs d’IA solo&nbsp;: recrue, vétéran et élite.",
     "AI difficulty levels",
     "Three settings for the solo AI engines: recruit, veteran and elite."),
    (1, "solo", "planned",
     "Tutoriel interactif",
     "Une première partie guidée pour apprendre les bases du wargame sans ouvrir le livret de règles.",
     "Interactive tutorial",
     "A guided first game to learn wargame basics without opening the rulebook."),
    (1, "platform", "planned",
     "Parties asynchrones",
     "Jouez par correspondance à votre rythme, avec notification quand c’est votre tour.",
     "Asynchronous games",
     "Play by correspondence at your own pace, with a notification when it’s your turn."),
    (1, "modules", "study",
     "Nouveau module&nbsp;: Normandie 1944",
     "Un module opérationnel consacré à la bataille de Normandie, de Caen à la poche de Falaise.",
     "New module: Normandy 1944",
     "An operational module on the Normandy campaign, from Caen to the Falaise pocket."),
    # T3
    (2, "modules", "planned",
     "Ambush!&nbsp;: campagne liée",
     "Enchaînez les missions avec la même escouade&nbsp;: expérience, blessures et promotions conservées.",
     "Ambush!: linked campaign",
     "Chain missions with the same squad, keeping experience, wounds and promotions."),
    (2, "community", "planned",
     "Tournois et saisons",
     "Des saisons classées de trois mois et des tournois à élimination organisés sur la plateforme.",
     "Tournaments and seasons",
     "Three-month ranked seasons and knockout tournaments run on the platform."),
    (2, "platform", "study",
     "Éditeur de scénarios",
     "Créez vos propres scénarios à partir des cartes et des pions existants, puis partagez-les.",
     "Scenario editor",
     "Build your own scenarios from existing maps and counters, then share them."),
    (2, "platform", "planned",
     "Statistiques de partie",
     "Un bilan après chaque partie&nbsp;: pertes, moments clés, probabilités et comparaison avec la moyenne.",
     "Game statistics",
     "An after-action report for every game: losses, key moments, odds and how you compare."),
    (2, "community", "study",
     "Mode spectateur",
     "Suivez en direct les parties de tournoi et les rencontres entre joueurs classés.",
     "Spectator mode",
     "Watch tournament games and matches between ranked players live."),
    (2, "modules", "study",
     "Nouveau module&nbsp;: front de l’Est",
     "Un module opérationnel sur le front de l’Est, pensé pour le jeu à deux comme contre l’IA.",
     "New module: Eastern Front",
     "An operational Eastern Front module, designed for two players as well as against the AI."),
    # T4
    (3, "platform", "planned",
     "Version tablette et mobile",
     "Une interface pensée pour le tactile, avec zoom sur la carte et manipulation des pions au doigt.",
     "Tablet and mobile version",
     "A touch-first interface with map zoom and finger-friendly counter handling."),
    (3, "platform", "study",
     "Mode hors ligne",
     "Continuez vos parties solo sans connexion&nbsp;; la synchronisation se fait au retour du réseau.",
     "Offline mode",
     "Keep playing solo games without a connection; everything syncs when you’re back online."),
    (3, "community", "planned",
     "Succès et médailles",
     "Des décorations à gagner par module, inspirées des citations et médailles historiques.",
     "Achievements and medals",
     "Decorations to earn in each module, inspired by historical citations and medals."),
    (3, "solo", "study",
     "IA adverse pour modules à deux joueurs",
     "Affrontez un adversaire artificiel dans les modules conçus à l’origine pour deux joueurs.",
     "AI opponent for two-player modules",
     "Face an AI opponent in modules originally designed for two players."),
    (3, "platform", "study",
     "Nouvelles langues",
     "Modules et interface traduits en allemand et en espagnol.",
     "More languages",
     "Modules and interface translated into German and Spanish."),
    (3, "modules", "study",
     "Nouveau module&nbsp;: guerre du Pacifique",
     "Un module consacré aux opérations amphibies et à la guerre dans les îles du Pacifique.",
     "New module: Pacific War",
     "A module on amphibious operations and island warfare in the Pacific."),
]
assert len(ITEMS) == 24

fr, en = {}, {}

def key(k, f, e):
    fr[k], en[k] = f, e


# ---------- Textes de page ----------
key("meta.title", "GameBoxHeroes — Road Map 2026", "GameBoxHeroes — 2026 Road Map")
key("meta.description", "Les 24 prochaines étapes de GameBoxHeroes&nbsp;: nouveaux modules, sauvegarde des parties, classement des joueurs, aide au jeu solo.".replace("&nbsp;", "\u00a0"),
    "GameBoxHeroes’ next 24 milestones: new modules, game saving, player rankings, solo play aids.")
key("hero.title", "Modules jouables de wargames classiques", "Playable modules of classic wargames")
key("rm.headline", "24 points<br>à venir en 2026", "24 milestones<br>coming in 2026")
key("rm.label", "Road Map", "Road Map")
key("rm.text",
    "Nouveaux modules, mémorisation des parties, classement des joueurs, aide pour les modules solo, nouvelles missions Ambush!&nbsp;: voici ce que nous préparons, trimestre par trimestre.<br>Les dates sont indicatives et évolueront avec vos retours.",
    "New modules, game saving, player rankings, solo play aids, new Ambush! missions: here is what we are building, quarter by quarter.<br>Dates are indicative and will evolve with your feedback.")
key("rm.stats", "Chiffres clés", "Key figures")
key("rm.filters", "Filtrer par thème", "Filter by theme")
key("rm.all", "Tout", "All")
key("rm.count.one", "{n} point affiché", "{n} milestone shown")
key("rm.count.other", "{n} points affichés", "{n} milestones shown")
key("rm.back", "Retour à l’accueil", "Back to home")

n_modules = sum(1 for i in ITEMS if i[1] == "modules")
n_progress = sum(1 for i in ITEMS if i[2] == "progress")
STATS = [
    ("24", "stat.total", "Points à venir d’ici fin 2026", "Milestones before the end of 2026"),
    (str(n_modules), "stat.modules", "Chantiers modules et missions", "Module and mission projects"),
    (str(n_progress), "stat.progress", "Déjà en cours de développement", "Already in development"),
]
for _, k, f, e in STATS:
    key(k, f, e)

for c, (f, e) in CATS.items():
    key(f"cat.{c}", f, e)
for s_, (f, e) in STATUS.items():
    key(f"status.{s_}", f, e)
for i, (qf, qe, pf, pe) in enumerate(QUARTERS):
    key(f"q{i+1}.code", qf, qe)
    key(f"q{i+1}.period", pf, pe)
for n, it in enumerate(ITEMS, 1):
    key(f"item{n}.title", it[3], it[5])
    key(f"item{n}.text", it[4], it[6])

# ---------- HTML ----------
def stat_html():
    out = []
    for val, k, f, _ in STATS:
        out.append(f'''      <li class="stat">
        <span class="stat__value">{val}</span>
        <span class="stat__label" data-i18n="{k}">{f}</span>
      </li>''')
    return "\n".join(out)

def filters_html():
    out = ['        <button type="button" class="chip" data-filter="all" aria-pressed="true" data-i18n="rm.all">Tout</button>']
    for c, (f, _) in CATS.items():
        out.append(f'        <button type="button" class="chip" data-filter="{c}" aria-pressed="false" data-i18n="cat.{c}">{html.escape(f)}</button>')
    return "\n".join(out)

def quarters_html():
    out = []
    n = 0
    for qi, (qf, _, pf, _) in enumerate(QUARTERS):
        items = [it for it in ITEMS if it[0] == qi]
        cards = []
        for it in items:
            n += 1
            _, cat, st, tf, xf, _, _ = it
            cards.append(f'''          <li class="item reveal" data-cat="{cat}" style="--i:{len(cards)}">
            <span class="item__num">{n:02d}</span>
            <h3 class="item__title" data-i18n-html="item{n}.title">{tf}</h3>
            <p class="item__text" data-i18n-html="item{n}.text">{xf}</p>
            <p class="item__meta">
              <span class="tag" data-i18n="cat.{cat}">{html.escape(CATS[cat][0])}</span>
              <span class="status status--{st}" data-i18n="status.{st}">{STATUS[st][0]}</span>
            </p>
          </li>''')
        out.append(f'''      <section class="quarter" aria-labelledby="q{qi+1}">
        <header class="quarter__head reveal">
          <h2 class="quarter__code" id="q{qi+1}" data-i18n="q{qi+1}.code">{qf}</h2>
          <p class="quarter__period" data-i18n="q{qi+1}.period">{pf}</p>
        </header>
        <ol class="items" start="{n - len(items) + 1}">
{chr(10).join(cards)}
        </ol>
      </section>''')
    return "\n\n".join(out)

page = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title data-i18n="meta.title">{fr["meta.title"]}</title>
<meta name="description" data-i18n-attr="content:meta.description" content="{html.escape(fr["meta.description"])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Red+Hat+Text:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="roadmap.css">
</head>
<body class="page-roadmap">
<!-- Fichier genere par tools/gen_roadmap.py : modifier les donnees la-bas, pas ce HTML -->
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
        <p class="brand__title" data-i18n="hero.title">{fr["hero.title"]}</p>
      </div>
      <button class="burger" type="button" aria-expanded="false" aria-controls="menu" data-i18n-attr="aria-label:menu.open" aria-label="Ouvrir le menu">
        <span></span><span></span><span></span>
      </button>
    </header>

    <div class="hero-photo" aria-hidden="true">
      <img src="assets/hero-photo.png" alt="" width="600" height="465">
    </div>

    <section class="intro">
      <h1 class="intro__headline" data-i18n-html="rm.headline">{fr["rm.headline"]}</h1>
      <div class="intro__news">
        <p class="intro__label" data-i18n="rm.label">Road Map</p>
        <p class="intro__text" data-i18n-html="rm.text">{fr["rm.text"]}</p>
      </div>
    </section>

    <ul class="rm-stats" data-i18n-attr="aria-label:rm.stats" aria-label="Chiffres clés">
{stat_html()}
    </ul>
  </div>

  <main class="rm-body">
    <div class="rm-toolbar">
      <span class="rule-line rule-line--main" aria-hidden="true"></span>
      <span class="rule-line rule-line--side" aria-hidden="true"></span>
      <div class="chips" role="group" data-i18n-attr="aria-label:rm.filters" aria-label="Filtrer par thème">
{filters_html()}
      </div>
      <p class="rm-count" aria-live="polite">24 points affichés</p>
    </div>

{quarters_html()}

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
      <li><a href="index.html#modules" data-i18n="menu.modules">Modules</a></li>
      <li><a href="actualites.html" data-i18n="menu.news">Actualités</a></li>
      <li><a href="roadmap.html" aria-current="page" data-close data-i18n="menu.roadmap">Road Map</a></li>
      <li><a href="qui-sommes-nous.html" data-i18n="menu.about">Qui sommes-nous</a></li>
      <li><a href="contact.html" data-i18n="menu.contact">Contact</a></li>
    </ul>
    <div class="lang" role="group" data-i18n-attr="aria-label:menu.language" aria-label="Langue">
      <button type="button" class="lang__btn" data-lang="fr" lang="fr">FR</button>
      <span class="lang__sep" aria-hidden="true">/</span>
      <button type="button" class="lang__btn" data-lang="en" lang="en">EN</button>
    </div>
  </nav>
</div>

<script src="roadmap-i18n.js"></script>
<script src="script.js"></script>
<script src="roadmap.js"></script>
</body>
</html>
'''

with open(os.path.join(OUT, "roadmap.html"), "w", encoding="utf-8", newline="\n") as f:
    f.write(page)

js = ("// Fichier genere : textes FR / EN de la page Road Map.\n"
      "window.GBH_I18N = " + json.dumps({"fr": fr, "en": en}, ensure_ascii=False, indent=2) + ";\n")
with open(os.path.join(OUT, "roadmap-i18n.js"), "w", encoding="utf-8", newline="\n") as f:
    f.write(js)

print("ok", n_modules, n_progress)
