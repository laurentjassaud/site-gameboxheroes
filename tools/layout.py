# Gabarit commun a toutes les pages : <head>, en-tete (bande creme), pied de
# page, menu lateral et scripts. Les generateurs (gen_home, gen_pages,
# gen_roadmap, gen_static) n'ecrivent que le contenu propre a chaque page.
#
# Les textes de ce gabarit sont traduits par script.js (dictionnaire commun).
import html
import json
import os

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FONTS = ('https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@300;400;500;600;700;800;900'
         '&family=Red+Hat+Text:wght@300;400;500;600;700&display=swap')

MENU = [
    ('index.html#modules', 'menu.modules', 'Modules'),
    ('actualites.html', 'menu.news', 'Actualités'),
    ('roadmap.html', 'menu.roadmap', 'Road Map'),
    ('qui-sommes-nous.html', 'menu.about', 'Qui sommes-nous'),
    ('contact.html', 'menu.contact', 'Contact'),
    ('compte.html', 'menu.account', 'Mon compte'),
]

CREDIT = ('<p class="credit" data-i18n-html="credit">Carte et pions provenant du jeu <strong>Normandy ’44</strong><br>'
          'dans un but illustratif uniquement - <strong>Tous droits GMT Games</strong></p>')


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


def topbar(home=False):
    label = 'GameBoxHeroes' if home else 'Retour à l’accueil'
    label_attr = '' if home else ' data-i18n-attr="aria-label:rm.back"'
    return f'''    <div class="topbar">
      <div class="brand">
        <a class="brand__logo" href="index.html"{label_attr} aria-label="{label}">
          <img class="brand__logo-hex" src="assets/logo-hex.svg" alt="" width="139" height="156">
          <img class="brand__logo-text" src="assets/logo-text.svg" alt="" width="78" height="55">
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


def menu(current):
    links = []
    for href, key, label in MENU:
        cur = ' aria-current="page" data-close' if href == current else ''
        close = ' data-close' if href.startswith('index.html#') and current == 'index.html' else ''
        links.append(f'      <li><a href="{href}"{cur}{close} data-i18n="{key}">{label}</a></li>')
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
        <button type="button" class="lang__btn" data-lang="fr" lang="fr">FR</button>
        <span class="lang__sep" aria-hidden="true">/</span>
        <button type="button" class="lang__btn" data-lang="en" lang="en">EN</button>
      </div>
    </div>
  </nav>
</div>'''


def render(p, *, file, meta_title, meta_desc, top, body, css=(), scripts=(), modules=(),
           body_class='', generator='tools/gen_*.py', i18n_file=None):
    """Assemble une page complete et l'ecrit, avec son fichier de traduction."""
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

    page = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title data-i18n="meta.title">{meta_title[0]}</title>
<meta name="description" data-i18n-attr="content:meta.description" content="{html.escape(meta_desc[0])}">
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
{body}
</main>

{FOOTER}

{menu(file)}

{chr(10).join(js)}
</body>
</html>
'''
    with open(os.path.join(OUT, file), 'w', encoding='utf-8', newline='\n') as f:
        f.write(page)
    if write_i18n:
        with open(os.path.join(OUT, i18n_file), 'w', encoding='utf-8', newline='\n') as f:
            f.write(f'// Fichier genere par {generator} : textes FR / EN de {file}.\n')
            f.write('window.GBH_I18N = ' + json.dumps({'fr': p.fr, 'en': p.en}, ensure_ascii=False, indent=2) + ';\n')
    print('ecrit', file)
