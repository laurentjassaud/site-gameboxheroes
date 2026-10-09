# Gabarit commun a toutes les pages : <head>, en-tete (bande creme), pied de
# page, menu lateral et scripts. Les generateurs (gen_home, gen_pages,
# gen_roadmap, gen_static) n'ecrivent que le contenu propre a chaque page.
#
# Les textes de ce gabarit sont traduits par script.js (dictionnaire commun).
# En fin de fichier : ecriture des pages dans les deux langues et referencement.
import html
import json
import os
import re

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FONTS = ('https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700;800;900'
         '&family=Red+Hat+Text:wght@300;400;500;600;700&display=swap')

MENU = [
    ('boites.html', 'menu.boxes', 'Les boîtes'),
    ('actualites.html', 'menu.news', 'Actualités'),
    ('roadmap.html', 'menu.roadmap', 'Road Map'),
    ('qui-sommes-nous.html', 'menu.about', 'Qui sommes-nous'),
    ('contact.html', 'menu.contact', 'Contact'),
    ('compte.html', 'menu.account', 'Mon compte'),
]

def credit(game, rights):
    """Mention de droits de l'illustration du bandeau (texte EN : cle 'credit'
    de script.js, ou du *-i18n.js de la page si elle a sa propre image)."""
    return (f'<p class="credit" data-i18n-html="credit">Carte et pions provenant du jeu <strong>{game}</strong><br>'
            f'dans un but illustratif uniquement - <strong>Tous droits {rights}</strong></p>')


CREDIT = credit('Normandy ’44', 'GMT Games')


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


def _paths(name, fill):
    """Traces d'un SVG de assets/ ayant la couleur de remplissage donnee."""
    with open(os.path.join(OUT, 'assets', name), encoding='utf-8') as f:
        found = re.findall(r'<path[^>]*\bd="([^"]+)"[^>]*\bfill="([^"]+)"', f.read())
    return [d for d, c in found if c == fill]


def _logo():
    """Logo anime de l'en-tete, en SVG en ligne pour que style.css anime chaque
    trace : hexagone, monogramme GBH (repos) et nom (survol). Les traces
    viennent des SVG de assets/, ramenes au repere 139 x 156 de l'hexagone ;
    --i est le rang du trace, qui decale son depart dans la cascade."""
    def group(cls, paths, transform):
        rows = '\n'.join(f'              <path style="--i:{i}" fill="#fff" d="{d}"/>' for i, d in enumerate(paths))
        return f'            <g class="{cls}" transform="{transform}">\n{rows}\n            </g>'

    hex_path = _paths('logo-hex.svg', '#FF0000')[0]
    return '\n'.join([
        '          <svg viewBox="0 0 139 156" aria-hidden="true">',
        f'            <path fill="#f00" d="{hex_path}"/>',
        # logo-mark.svg est dessine en 65 x 73
        group('brand__logo-mark', _paths('logo-mark.svg', 'white'), 'scale(2.1385 2.137)'),
        # logo-text.svg ne contient que le texte, place a (12, 47.06) dans l'hexagone
        group('brand__logo-name', _paths('logo-text.svg', 'white'), 'translate(12 47.06)'),
        '          </svg>',
    ])


LOGO = _logo()


def topbar(home=False):
    label = 'GameBoxHeroes' if home else 'Retour à l’accueil'
    label_attr = '' if home else ' data-i18n-attr="aria-label:rm.back"'
    return f'''    <div class="topbar">
      <div class="brand">
        <a class="brand__logo" href="index.html"{label_attr} aria-label="{label}">
{LOGO}
        </a>
        <p class="brand__tagline" data-i18n-html="brand.tagline">Les <strong>boîtes</strong> de jeux<br>des classiques du <strong>wargame</strong></p>
      </div>
      <div class="topbar__actions">
        <div class="account">
          <a class="account__btn" href="compte.html" data-i18n-attr="aria-label:account.label" aria-label="Mon compte">
            <svg class="account__icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8.5" r="4"/><path d="M4.5 20.5c.8-3.9 3.9-6.3 7.5-6.3s6.7 2.4 7.5 6.3"/></svg>
            <span class="account__initial" aria-hidden="true"></span>
          </a>
        </div>
        <button class="burger" type="button" aria-expanded="false" aria-controls="menu" data-i18n-attr="aria-label:menu.open" aria-label="Ouvrir le menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>'''


# Dernieres boites : accueil et colonne laterale de Contact (dont les textes
# sont a reporter a la main dans contact-i18n.js)
BOXES = [
    ('assets/cover-arnhem.webp', 'Arnhem: Operation Market-Garden',
     ('A Bridge Too Far&nbsp;: Arnhem', 'A Bridge Too Far: Arnhem'),
     'badge--red', ('Bêta publique', 'Public beta'),
     ('Un jeu pour 2 joueurs de SPI Games publié en 1976 et designé par Jay A. Nelson pour la série West Wall',
      'A two-player game from SPI Games, published in 1976 and designed by Jay A. Nelson for the West Wall series'),
     'actualites.html#arnhem-tests-publics'),
    ('assets/cover-ambush.webp', 'Ambush!',
     ('Ambush!', 'Ambush!'),
     '', ('Alpha privée', 'Private alpha'),
     ('Un jeu solitaire de Victory Games publié en 1983 et designé par John H. Butterfield et Eric Lee Smith',
      'A solitaire game from Victory Games, published in 1983 and designed by John H. Butterfield and Eric Lee Smith'),
     'actualites.html#ambush-missions'),
]


# Fleche des cartes, en SVG en ligne pour que style.css la colore au survol
def arrow(cls='box__arrow'):
    return (f'<svg class="{cls}" viewBox="0 0 30 31" aria-hidden="true">'
            f'<path d="{_paths("arrow.svg", "black")[0]}"/></svg>')


ARROW = arrow()


def boxes(p):
    """Liste des dernieres boites (cartes .box de style.css)."""
    items = []
    for i, (img, alt, title, badge_cls, badge, desc, href) in enumerate(BOXES, 1):
        cls = f'badge {badge_cls}'.strip()
        items.append(f'''          <li>
            <a class="box" href="{href}">
              <img class="box__cover" src="{img}" alt="{alt}" width="150" height="184">
              <div class="box__body">
                {p.t(f'box{i}.title', *title, tag='h3', cls='box__title')}
                {p.t(f'box{i}.badge', *badge, tag='span', cls=cls)}
                {p.t(f'box{i}.desc', *desc, cls='box__desc')}
                {ARROW}
              </div>
            </a>
          </li>''')
    return '<ul class="boxes">\n' + '\n'.join(items) + '\n        </ul>'


# Boites en preparation : (couverture, titre, editeur, annee, lien). Les quatre
# premieres forment le bandeau de l'accueil, la page Les boîtes les montre
# toutes. Annee vide : date de parution pas encore connue.
COVERS = [
    ('assets/home/prep-arnhem.webp', 'Arnhem: Operation Market-Garden', 'SPI', '1976', 'actualites.html#arnhem-tests-publics'),
    ('assets/home/prep-ambush.webp', 'Ambush!', 'Victory Games', '1983', 'actualites.html#ambush-missions'),
    ('assets/home/prep-pattons-best.webp', 'Patton’s Best', 'The Avalon Hill Game Company', '1987', 'roadmap.html'),
    ('assets/home/prep-carrier-battle.webp', 'Carrier Battle: South Pacific', 'Compass Games', '', 'roadmap.html'),
    ('assets/home/prep-kharkov.webp', 'Enemy Action: Kharkov', 'Compass Games', '2020', 'roadmap.html'),
    ('assets/home/prep-open-fire.webp', 'Open Fire', 'Victory Games', '1988', 'roadmap.html'),
    ('assets/home/prep-combat.webp', 'Combat! Eastern Front', 'Compass Games', '2026', 'roadmap.html'),
    ('assets/home/prep-carrier.webp', 'Carrier', 'Victory Games', '1990', 'roadmap.html'),
    ('assets/home/prep-tokyo-express.webp', 'Tokyo Express', 'Victory Games', '1988', 'roadmap.html'),
    ('assets/home/prep-raid-st-nazaire.webp', 'Raid on St. Nazaire', 'The Avalon Hill Game Company', '1987', 'roadmap.html'),
]


def sticker(p):
    """Hexagone flechee « Voir la boîte » (texte reserve aux lecteurs d'ecran)."""
    return (f'<span class="prep__sticker">{p.t("prep.see", "Voir la boîte", "View the box", tag="span", cls="sr-only")}'
            f'{arrow("prep__arrow")}</span>')


def covers(p, items=COVERS):
    """Bandeau de couvertures de l'accueil (.prep__strip de style.css). Les
    images sont en couleur : le CSS les grise au repos et les revele au survol,
    avec l'hexagone."""
    rows = '\n'.join(f'''      <li>
        <a class="prep__box" href="{href}">
          <img src="{src}" alt="{title}" loading="lazy">
          {sticker(p)}
        </a>
      </li>''' for src, title, _, _, href in items)
    return f'    <ul class="prep__strip">\n{rows}\n    </ul>'


def reel(p, items=COVERS):
    """Ligne horizontale de boites de la page Les boîtes (.reel de boites.css,
    animee par boites.js) : titre, couverture, puis editeur et annee."""
    rows = '\n'.join(f'''      <li class="reel__item">
        <a class="reel__link" href="{href}">
          <h3 class="reel__title"><span class="reel__line">{title}</span></h3>
          <span class="reel__visual">
            <img src="{src}" alt="" draggable="false">
            {sticker(p)}
          </span>
          <span class="reel__meta"><span class="reel__pub">{pub}</span><span class="reel__year">{year or '&nbsp;'}</span></span>
        </a>
      </li>''' for src, title, pub, year, href in items)
    return f'    <ul class="reel__track">\n{rows}\n    </ul>'


def intro(p, title, sub):
    """Titre + sous-titre des pages internes (maquette node 129:237)."""
    return f'''    <div class="top__intro">
      {p.t('pg.title', *title, tag='h1', cls='top__title')}
      {p.t('pg.sub', *sub, cls='top__sub')}
    </div>'''


FOOTER = '''<footer class="foot wrap">
  <div class="foot__cols cols">
    <form class="news-form" novalidate>
      <h2 class="sec-title sec-title--plain" data-i18n="nl.title">Rester au courant de l’avancement des projets</h2>
      <div class="news-form__row">
        <div>
          <div class="news-form__input">
            <label class="sr-only" for="nl-email" data-i18n="nl.label">Votre e-mail</label>
            <input id="nl-email" name="email" type="email" autocomplete="email" inputmode="email" spellcheck="false" maxlength="254" data-i18n-attr="placeholder:nl.placeholder" placeholder="Votre e-mail" required aria-describedby="nl-msg">
            <button class="news-form__submit" type="submit"><span data-i18n="nl.submit">Envoyer</span></button>
          </div>
          <p class="news-form__msg" id="nl-msg" role="status"></p>
        </div>
        <div class="field field--check">
          <input id="nl-consent" name="consent" type="checkbox" value="1" required>
          <label for="nl-consent" data-i18n-html="nl.consent">J’accepte que mon e-mail soit utilisé uniquement pour recevoir des nouvelles des projets. <a href="mentions-legales.html#newsletter">En savoir plus</a></label>
        </div>
      </div>
    </form>
    <div class="sign">
      <a class="sign__mark" href="index.html" aria-label="GameBoxHeroes">
        <img src="assets/logo-mark.svg" alt="" width="65" height="73">
      </a>
      <div>
        <p class="sign__name">GameBoxHeroes 2026</p>
        <p class="sign__links">
          <a href="mentions-legales.html" data-i18n="foot.legal">Mentions légales</a>
          <a href="mentions-legales.html#confidentialite" data-i18n="foot.privacy">Confidentialité</a>
          <a href="contact.html" data-i18n="menu.contact">Contact</a>
        </p>
      </div>
    </div>
  </div>
</footer>'''


def menu(current, lang='fr'):
    links = []
    for href, key, label in MENU:
        cur = ' aria-current="page" data-close' if href == current else ''
        close = ' data-close' if href.startswith('index.html#') and current == 'index.html' else ''
        links.append(f'      <li><a href="{href}"{cur}{close} data-i18n="{key}">{label}</a></li>')
    # Chaque langue a sa propre page : le choix de langue est un lien vers
    # la meme page dans l'autre dossier (racine = francais, en/ = anglais)
    switch = []
    for code in LANGS:
        href = current if code == lang else (f'en/{current}' if code == 'en' else f'../{current}')
        cur = ' aria-current="true"' if code == lang else ''
        switch.append(f'<a class="lang__btn" href="{href}" lang="{code}" hreflang="{code}"{cur}>{code.upper()}</a>')
    switch = '\n        <span class="lang__sep" aria-hidden="true">/</span>\n        '.join(switch)
    return f'''<div class="menu" id="menu" hidden>
  <div class="menu__backdrop" data-close></div>
  <nav class="menu__panel" data-i18n-attr="aria-label:menu.label" aria-label="Menu principal">
    <button class="menu__close" type="button" data-close data-i18n-attr="aria-label:menu.close" aria-label="Fermer le menu">
      <span></span><span></span>
    </button>
    <ul class="menu__links">
{chr(10).join(links)}
    </ul>
    <div class="menu__foot">
      <a class="menu__legal" href="mentions-legales.html" data-i18n="foot.legal">Mentions légales</a>
      <div class="lang" role="group" data-i18n-attr="aria-label:menu.language" aria-label="Langue">
        {switch}
      </div>
    </div>
  </nav>
</div>'''


# ===========================================================================
#  Referencement : une page par langue, en-tete <head>, donnees structurees
# ===========================================================================
#
# Chaque page existe en deux fichiers : page.html (francais, a la racine) et
# en/page.html (anglais). Les generateurs ecrivent le francais ; la version
# anglaise est la meme page dont les textes reperes par data-i18n* sont
# remplaces par leur traduction (localize), pour que les moteurs de recherche
# lisent de l'anglais sans executer de JavaScript.

SITE = 'https://www.gameboxheroes.com'
LANGS = ('fr', 'en')
LOCALES = {'fr': 'fr_FR', 'en': 'en_US'}
HOME = {'fr': 'Accueil', 'en': 'Home'}
OG_ALT = {'fr': 'GameBoxHeroes — les boîtes de jeux des classiques du wargame',
          'en': 'GameBoxHeroes — the game boxes of classic wargames'}

# Pages du plan du site (sitemap.xml), dans l'ordre. Mon compte n'y figure
# pas : la page est en noindex.
SITEMAP = ['index.html', 'boites.html', 'actualites.html', 'roadmap.html',
           'qui-sommes-nous.html', 'contact.html', 'mentions-legales.html']


def url(file, lang='fr'):
    """Adresse publique d'une page (l'accueil est la racine du dossier)."""
    return f"{SITE}/{'en/' if lang == 'en' else ''}{'' if file == 'index.html' else file}"


def plain(text):
    """Texte brut d'un fragment HTML (pour les donnees structurees)."""
    return html.unescape(re.sub(r'<[^>]+>', '', text)).replace(' ', ' ').strip()


def _js_texts(path, lang):
    """Textes d'une langue dans un fichier de traductions ecrit a la main
    (script.js, contact-i18n.js) : une entree 'cle': 'valeur' par ligne."""
    texts, current = {}, None
    with open(path, encoding='utf-8') as f:
        for line in f:
            block = re.match(r'\s*(fr|en): \{', line)
            if block:
                current = block.group(1)
                continue
            entry = re.match(r"\s*'([^']+)':\s*'(.*)',?\s*$", line)
            if entry and current == lang:
                texts[entry.group(1)] = entry.group(2)
    return texts


def _closing(page, start, tag):
    """Position de la balise fermante de l'element <tag> dont le contenu
    commence en start (les elements de meme nom imbriques sont sautes)."""
    depth = 1
    for m in re.compile(rf'<(/?){tag}\b[^<>]*>').finditer(page, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.start()
    raise ValueError(f'<{tag}> non ferme')


def localize(page, texts):
    """Applique un dictionnaire de traductions au HTML, comme le fait
    applyLang() de script.js dans le navigateur : data-i18n (texte),
    data-i18n-html (HTML) et data-i18n-attr (attributs)."""

    def attributes(m):
        tag = m.group(0)
        for pair in m.group(1).split(';'):
            attr, key = pair.split(':')
            if key in texts:
                value = html.escape(texts[key])
                tag = re.sub(rf'(?<![\w-]){attr}="[^"]*"', lambda _: f'{attr}="{value}"', tag, count=1)
        return tag

    page = re.sub(r'<[^<>]*\bdata-i18n-attr="([^"]+)"[^<>]*>', attributes, page)

    def text(m):
        key = m.group(3)
        inner = html.escape(texts[key], quote=False) if key in texts else m.group(4)
        return m.group(1) + inner + m.group(5)

    page = re.sub(r'(<(\w+)\b[^<>]*\bdata-i18n="([^"]+)"[^<>]*>)(.*?)(</\2>)', text, page, flags=re.S)

    # De la fin vers le debut : les positions deja trouvees restent valables
    for m in reversed(list(re.finditer(r'<(\w+)\b[^<>]*\bdata-i18n-html="([^"]+)"[^<>]*>', page))):
        if m.group(2) in texts:
            page = page[:m.end()] + texts[m.group(2)] + page[_closing(page, m.end(), m.group(1)):]
    return page


def _to_root(page):
    """Dans en/, les fichiers partages (assets, scripts, contact.php) sont un
    dossier plus haut ; les liens vers les pages restent dans en/."""
    def fix(m):
        value = m.group(2)
        if re.search(r'\.html([?#]|$)', value):
            return m.group(0)
        return f'{m.group(1)}="../{value}"'
    return re.sub(r'(?<![\w-])(src|href|action)="(?!https?:|mailto:|#|/|\.\./)([^"]+)"', fix, page)


def _ld(file, lang, title, desc, page_type, crumb, extra):
    """Donnees structurees schema.org de la page (JSON-LD)."""
    org = {'@type': 'Organization', '@id': f'{SITE}/#organization', 'name': 'GameBoxHeroes',
           'url': f'{SITE}/', 'logo': f'{SITE}/assets/logo-mark.svg'}
    site = {'@type': 'WebSite', '@id': f'{SITE}/#website', 'name': 'GameBoxHeroes', 'url': f'{SITE}/',
            'inLanguage': list(LANGS), 'publisher': {'@id': org['@id']}}
    here = url(file, lang)
    page = {'@type': page_type, '@id': f'{here}#webpage', 'url': here, 'name': title,
            'description': desc, 'inLanguage': lang, 'isPartOf': {'@id': site['@id']}}
    graph = [org, site, page]
    if crumb:
        page['breadcrumb'] = {'@id': f'{here}#breadcrumb'}
        graph.append({'@type': 'BreadcrumbList', '@id': f'{here}#breadcrumb', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': HOME[lang], 'item': url('index.html', lang)},
            {'@type': 'ListItem', 'position': 2, 'name': plain(crumb), 'item': here}]})
    graph += extra
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, indent=1)
    return '<script type="application/ld+json">\n' + data.replace('</', '<\\/') + '\n</script>'


def _head(file, lang, title, desc, noindex, ld):
    """Balises de referencement : titre, description, adresse canonique,
    versions linguistiques, apercu de partage (Open Graph) et JSON-LD."""
    e = html.escape
    here = url(file, lang)
    image = f'{SITE}/assets/og-{lang}.jpg'
    other = 'en' if lang == 'fr' else 'fr'
    lines = [
        f'<title>{e(title, quote=False)}</title>',
        f'<meta name="description" content="{e(desc)}">',
    ]
    if noindex:
        lines.append('<meta name="robots" content="noindex, follow">')
    lines += [
        f'<link rel="canonical" href="{here}">',
        *(f'<link rel="alternate" hreflang="{code}" href="{url(file, code)}">' for code in LANGS),
        f'<link rel="alternate" hreflang="x-default" href="{url(file)}">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="GameBoxHeroes">',
        f'<meta property="og:locale" content="{LOCALES[lang]}">',
        f'<meta property="og:locale:alternate" content="{LOCALES[other]}">',
        f'<meta property="og:title" content="{e(title)}">',
        f'<meta property="og:description" content="{e(desc)}">',
        f'<meta property="og:url" content="{here}">',
        f'<meta property="og:image" content="{image}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{e(OG_ALT[lang])}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{e(title)}">',
        f'<meta name="twitter:description" content="{e(desc)}">',
        f'<meta name="twitter:image" content="{image}">',
        ld,
    ]
    return '\n'.join(lines)


def render(p, *, file, meta_title, meta_desc, top, body, css=(), scripts=(), modules=(),
           body_class='', generator='tools/gen_*.py', i18n_file=None,
           body_en=None, noindex=False, page_type='WebPage', ld=None):
    """Assemble une page complete et l'ecrit dans les deux langues, avec son
    fichier de traduction.

    body_en   : corps propre a la version anglaise (sinon celui de body, traduit)
    noindex   : page a ne pas referencer
    page_type : type schema.org de la page (WebPage, CollectionPage...)
    ld        : fonction lang -> donnees structurees supplementaires
    """
    p.k('meta.title', *meta_title)
    p.k('meta.description', *meta_desc)

    css_links = '\n'.join(f'<link rel="stylesheet" href="assets/css/{c}">' for c in ('style.css', *css))
    # i18n_file : fichier de traduction ecrit a la main (sinon genere ici)
    write_i18n = i18n_file is None
    i18n_file = i18n_file or file.replace('.html', '-i18n.js')
    js = [f'<script src="{i18n_file}"></script>']
    js += ['<script src="script.js"></script>']
    js += [f'<script src="{s}"></script>' for s in scripts]
    js += [f'<script type="module" src="{m}"></script>' for m in ('account.js', 'newsletter.js', *modules)]
    cls = f' class="{body_class}"' if body_class else ''

    # Anglais : textes communs (script.js) + textes de la page
    english = _js_texts(os.path.join(OUT, 'script.js'), 'en')
    english.update(p.en if write_i18n else _js_texts(os.path.join(OUT, i18n_file), 'en'))
    french = p.fr if write_i18n else _js_texts(os.path.join(OUT, i18n_file), 'fr')
    crumb = None if file == 'index.html' else {'fr': french.get('pg.title'), 'en': english.get('pg.title')}

    def page(lang):
        n = LANGS.index(lang)
        head = _head(file, lang, meta_title[n], meta_desc[n], noindex,
                     _ld(file, lang, meta_title[n], meta_desc[n], page_type,
                         crumb and crumb[lang], ld(lang) if ld else []))
        return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{head}
<link rel="icon" href="assets/logo-mark.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
{css_links}
</head>
<body{cls}>
<!-- Fichier genere par {generator} : modifier la source la-bas, pas ce HTML -->
<header class="top">
  <div class="wrap">
{top}
  </div>
</header>

<main>
{body_en if lang == 'en' and body_en else body}
</main>

{FOOTER}

{menu(file, lang)}

{chr(10).join(js)}
</body>
</html>
'''

    with open(os.path.join(OUT, file), 'w', encoding='utf-8', newline='\n') as f:
        f.write(page('fr'))

    os.makedirs(os.path.join(OUT, 'en'), exist_ok=True)
    with open(os.path.join(OUT, 'en', file), 'w', encoding='utf-8', newline='\n') as f:
        f.write(_to_root(localize(page('en'), english)))

    if write_i18n:
        with open(os.path.join(OUT, i18n_file), 'w', encoding='utf-8', newline='\n') as f:
            f.write(f'// Fichier genere par {generator} : textes FR / EN de {file}.\n')
            f.write('window.GBH_I18N = ' + json.dumps({'fr': p.fr, 'en': p.en}, ensure_ascii=False, indent=2) + ';\n')
    print('ecrit', file, '+ en/' + file)


def write_seo_files():
    """sitemap.xml (pages des deux langues, liees entre elles) et robots.txt."""
    entries = []
    for file in SITEMAP:
        links = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{code}" href="{url(file, code)}"/>'
                        for code in LANGS)
        links += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{url(file)}"/>'
        entries += [f'  <url>\n    <loc>{url(file, lang)}</loc>{links}\n  </url>' for lang in LANGS]
    with open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + '\n'.join(entries) + '\n</urlset>\n')
    with open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('User-agent: *\nDisallow: /tools/\nDisallow: /prototype-logo.html\n\n'
                f'Sitemap: {SITE}/sitemap.xml\n')
    print('ecrit sitemap.xml, robots.txt')
