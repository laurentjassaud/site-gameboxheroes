# Genere contact.html, compte.html et mentions-legales.html avec le gabarit
# commun (tools/layout.py). Les textes de la page Contact restent dans
# contact-i18n.js (ecrit a la main) ; ceux de Compte et des Mentions legales
# sont definis ici.
# Usage : python tools/gen_static.py
from layout import Page, topbar, intro, render, credit, boxes, CREDIT
from legal import LEGAL_FR, LEGAL_EN


def top_block(p, title, sub, credit_html=CREDIT):
    return f'''{topbar()}
{intro(p, title, sub)}
    {credit_html}'''


# ===========================================================================
#  Contact
# ===========================================================================

def build_contact():
    p = Page()
    top = top_block(p, ('Contact', 'Contact'),
                    ('Parlons wargames&nbsp;:<br>une idée, une question, un jeu original à adapter',
                     'Let’s talk wargames:<br>an idea, a question, a classic game to adapt'),
                    credit('Thunder at Cassino', 'The Avalon Hill Game Co'))

    body = '''  <div class="wrap ct-body cols split" id="form">
    <div class="ct-form-wrap">
      <form class="ct-form" action="contact.php" method="post">
        <h2 class="ct-title" data-i18n="ct.formTitle">Écrivez-nous</h2>

        <div class="form-status" role="alert" hidden></div>

        <div class="field-row">
          <div class="field" data-field="name">
            <label for="f-name" data-i18n="field.name">Nom</label>
            <input id="f-name" name="name" type="text" autocomplete="name" required minlength="2" maxlength="100" aria-describedby="e-name">
            <p class="field__error" id="e-name"></p>
          </div>
          <div class="field" data-field="email">
            <label for="f-email" data-i18n="field.email">E-mail</label>
            <input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" required maxlength="254" spellcheck="false" aria-describedby="e-email">
            <p class="field__error" id="e-email"></p>
          </div>
        </div>

        <div class="field" data-field="subject">
          <label for="f-subject" data-i18n="field.subject">Sujet</label>
          <div class="select">
            <select id="f-subject" name="subject" required aria-describedby="e-subject">
              <option value="general" data-i18n="subject.general">Question générale</option>
              <option value="module" data-i18n="subject.module">Proposer un module</option>
              <option value="bug" data-i18n="subject.bug">Signaler un bug</option>
            </select>
          </div>
          <p class="field__error" id="e-subject"></p>
        </div>

        <div class="field" data-field="message">
          <div class="field__top">
            <label for="f-message" data-i18n="field.message">Message</label>
            <span class="field__count" aria-hidden="true">0 / 5000</span>
          </div>
          <textarea id="f-message" name="message" rows="8" required minlength="10" maxlength="5000" aria-describedby="e-message"></textarea>
          <p class="field__error" id="e-message"></p>
        </div>

        <div class="field field--check" data-field="consent">
          <input id="f-consent" name="consent" type="checkbox" value="1" required aria-describedby="e-consent">
          <label for="f-consent" data-i18n="field.consent">J’accepte que mes informations soient utilisées uniquement pour répondre à ma demande.</label>
          <p class="field__error" id="e-consent"></p>
        </div>

        <!-- Pot de miel anti-robots : laisse vide par les humains -->
        <div class="hp" aria-hidden="true">
          <label for="f-website">Website</label>
          <input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off">
        </div>
        <input type="hidden" name="t" value="">
        <input type="hidden" name="lang" value="fr">

        <button class="submit" type="submit">
          <span class="submit__label" data-i18n="form.submit">Envoyer le message</span>
          <img class="submit__arrow" src="assets/arrow.svg" alt="" width="30" height="31">
          <span class="submit__spinner" aria-hidden="true"></span>
        </button>
      </form>

      <div class="ct-success" tabindex="-1" hidden>
        <p class="ct-success__label" data-i18n="success.label">Message envoyé</p>
        <h2 class="ct-success__title" data-i18n-html="success.title">Merci,<br>c’est bien reçu&nbsp;!</h2>
        <p class="ct-success__text" data-i18n="success.text">Nous vous répondons sous 48 heures ouvrées à l’adresse indiquée.</p>
        <button class="btn ct-again" type="button" data-i18n="success.again">Envoyer un autre message</button>
      </div>
    </div>

    <aside class="ct-aside" aria-labelledby="latest-title">
        <h2 class="ct-title" id="latest-title" data-i18n-html="home.latest">Dernières boîtes</h2>
        ''' + boxes(p) + '''
    </aside>
  </div>'''

    render(p, file='contact.html',
           meta_title=('Contact : proposer un wargame, signaler un bug — GameBoxHeroes',
                       'Contact: suggest a wargame, report a bug — GameBoxHeroes'),
           meta_desc=('Une question, une idée de wargame à adapter, un bug à signaler ? Écrivez à GameBoxHeroes : nous répondons sous 48 heures ouvrées.',
                      'A question, a wargame you’d like to see adapted, a bug to report? Write to GameBoxHeroes: we reply within two business days.'),
           page_type='ContactPage',
           top=top, body=body, css=['roadmap.css', 'contact.css'], scripts=['contact.js'],
           body_class='page-contact', generator='tools/gen_static.py', i18n_file='contact-i18n.js')
    return p


# ===========================================================================
#  Compte : connexion / inscription / gestion
# ===========================================================================

def build_account():
    p = Page()
    top = top_block(p, ('Mon compte', 'My account'),
                    ('Connectez-vous pour retrouver vos parties,<br>ou créez votre compte en une minute.',
                     'Sign in to get back to your games,<br>or create your account in a minute.'))

    T = p.t
    K = p.k

    # Textes utilises par compte.js
    K('auth.checking', 'Vérification…', 'Checking…')
    K('auth.free', 'Pseudo disponible', 'Username available')
    K('auth.taken', 'Ce pseudo est déjà pris', 'This username is taken')
    K('auth.strength0', '', '')
    K('auth.strength1', 'Faible', 'Weak')
    K('auth.strength2', 'Moyen', 'Fair')
    K('auth.strength3', 'Bon', 'Good')
    K('auth.strength4', 'Excellent', 'Strong')
    K('auth.show', 'Afficher le mot de passe', 'Show password')
    K('auth.hide', 'Masquer le mot de passe', 'Hide password')
    K('auth.fix', 'Certains champs sont à corriger.', 'Some fields need fixing.')
    K('auth.signingIn', 'Connexion…', 'Signing in…')
    K('auth.creating', 'Création du compte…', 'Creating account…')
    K('auth.resetSent', 'Si un compte existe pour cette adresse, un e-mail de réinitialisation vient d’être envoyé.',
      'If an account exists for this address, a reset email has just been sent.')
    K('auth.resetNeedsEmail', 'Saisissez votre e-mail ci-dessus, puis cliquez à nouveau.',
      'Enter your email above, then click again.')
    K('auth.welcome', 'Bienvenue, {name}&nbsp;!', 'Welcome, {name}!')
    K('auth.sentTo', 'Un lien de vérification a été envoyé à <strong>{email}</strong>. Pensez à regarder dans les courriers indésirables.',
      'A verification link has been sent to <strong>{email}</strong>. Check your spam folder too.')
    K('auth.verified', 'E-mail vérifié', 'Email verified')
    K('auth.unverified', 'E-mail pas encore vérifié', 'Email not verified yet')
    K('auth.signedAs', 'Connecté en tant que', 'Signed in as')
    K('auth.memberSince', 'Membre depuis le {date}', 'Member since {date}')

    body = f'''  <div class="wrap cols split auth-body">
    <div class="auth" data-state="loading">
      <p class="auth__loading" aria-live="polite"><span class="spinner" aria-hidden="true"></span></p>

      {T('auth.off', 'Les comptes joueurs ouvriront très bientôt. En attendant, suivez l’avancement du projet grâce à la lettre d’information en bas de page.',
         'Player accounts will open very soon. Meanwhile, follow the project through the newsletter at the bottom of the page.', cls='auth__off')}

      <!-- Deconnecte : onglets Connexion / Inscription -->
      <div class="auth__guest">
        <div class="tabs" role="tablist" data-i18n-attr="aria-label:auth.tabs" aria-label="Connexion ou inscription">
          <button class="tabs__tab" type="button" role="tab" id="tab-login" aria-controls="panel-login" aria-selected="true" data-i18n="auth.tab.login">Connexion</button>
          <button class="tabs__tab" type="button" role="tab" id="tab-signup" aria-controls="panel-signup" aria-selected="false" tabindex="-1" data-i18n="auth.tab.signup">Créer un compte</button>
          <span class="tabs__ink" aria-hidden="true"></span>
        </div>

        <section class="tabs__panel" id="panel-login" role="tabpanel" aria-labelledby="tab-login">
          <form class="auth-form" id="login-form" novalidate>
            <div class="form-status" role="alert" hidden></div>
            <div class="field" data-field="email">
              <label for="l-email" data-i18n="auth.email">E-mail</label>
              <input id="l-email" name="email" type="email" autocomplete="username" inputmode="email" spellcheck="false" maxlength="254" required aria-describedby="l-email-err">
              <p class="field__error" id="l-email-err"></p>
            </div>
            <div class="field" data-field="password">
              <label for="l-password" data-i18n="auth.password">Mot de passe</label>
              <div class="pwd">
                <input id="l-password" name="password" type="password" autocomplete="current-password" maxlength="128" required aria-describedby="l-password-err">
                <button class="pwd__toggle" type="button" aria-controls="l-password" aria-pressed="false" data-i18n-attr="aria-label:auth.show" aria-label="Afficher le mot de passe"></button>
              </div>
              <p class="field__error" id="l-password-err"></p>
            </div>
            <div class="auth-form__actions">
              <button class="btn btn--red" type="submit"><span data-i18n="auth.submitLogin">Se connecter</span></button>
              <button class="auth-link" type="button" data-action="reset" data-i18n="auth.forgot">Mot de passe oublié&nbsp;?</button>
            </div>
          </form>
        </section>

        <section class="tabs__panel" id="panel-signup" role="tabpanel" aria-labelledby="tab-signup" hidden>
          <form class="auth-form" id="signup-form" novalidate>
            <ol class="steps" aria-hidden="true">
              <li class="steps__item is-current" data-step-dot="1"><span>1</span><em data-i18n="auth.step1">Vos informations</em></li>
              <li class="steps__item" data-step-dot="2"><span>2</span><em data-i18n="auth.step2">Vérification</em></li>
              <li class="steps__item" data-step-dot="3"><span>3</span><em data-i18n="auth.step3">Confirmation</em></li>
            </ol>

            <div class="form-status" role="alert" hidden></div>

            <!-- Etape 1 : saisie -->
            <div class="step" data-step="1">
              <div class="field" data-field="username">
                <label for="s-username" data-i18n="auth.username">Pseudo</label>
                <input id="s-username" name="username" type="text" autocomplete="nickname" autocapitalize="off" spellcheck="false" minlength="3" maxlength="20" required aria-describedby="s-username-hint s-username-avail s-username-err">
                <p class="field__hint" id="s-username-hint" data-i18n="auth.usernameHint">3 à 20 caractères&nbsp;: lettres sans accent, chiffres, « - » et « _ ». Visible des autres joueurs.</p>
                <p class="avail" id="s-username-avail" aria-live="polite"></p>
                <p class="field__error" id="s-username-err"></p>
              </div>
              <div class="field" data-field="email">
                <label for="s-email" data-i18n="auth.email">E-mail</label>
                <input id="s-email" name="email" type="email" autocomplete="email" inputmode="email" spellcheck="false" maxlength="254" required aria-describedby="s-email-err">
                <p class="field__error" id="s-email-err"></p>
              </div>
              <div class="field" data-field="password">
                <label for="s-password" data-i18n="auth.password">Mot de passe</label>
                <div class="pwd">
                  <input id="s-password" name="password" type="password" autocomplete="new-password" maxlength="128" required aria-describedby="s-password-hint s-password-err">
                  <button class="pwd__toggle" type="button" aria-controls="s-password" aria-pressed="false" data-i18n-attr="aria-label:auth.show" aria-label="Afficher le mot de passe"></button>
                </div>
                <div class="meter" data-score="0" aria-hidden="true"><span></span><span></span><span></span><span></span><em></em></div>
                <p class="field__hint" id="s-password-hint" data-i18n="auth.passwordHint">Au moins 8 caractères, avec au moins une lettre et un chiffre.</p>
                <p class="field__error" id="s-password-err"></p>
              </div>
              <div class="field" data-field="password2">
                <label for="s-password2" data-i18n="auth.password2">Confirmez le mot de passe</label>
                <input id="s-password2" name="password2" type="password" autocomplete="new-password" maxlength="128" required aria-describedby="s-password2-err">
                <p class="field__error" id="s-password2-err"></p>
              </div>
              <div class="auth-form__actions">
                <button class="btn btn--red" type="button" data-action="next"><span data-i18n="auth.continue">Continuer</span><img src="assets/arrow.svg" alt="" width="30" height="31"></button>
              </div>
            </div>

            <!-- Etape 2 : verification et acceptation -->
            <div class="step" data-step="2" hidden>
              {T('auth.recapTitle', 'Vérifiez vos informations', 'Check your details', tag='h2', cls='step__title', attrs='tabindex="-1"')}
              <dl class="recap">
                <div><dt data-i18n="auth.username">Pseudo</dt><dd data-recap="username"></dd></div>
                <div><dt data-i18n="auth.email">E-mail</dt><dd data-recap="email"></dd></div>
                <div><dt data-i18n="auth.password">Mot de passe</dt><dd>••••••••</dd></div>
              </dl>
              {T('auth.recapNote', 'Votre pseudo sera visible des autres joueurs et ne pourra plus être modifié. Un e-mail de vérification sera envoyé à l’adresse indiquée.',
                 'Your username will be visible to other players and cannot be changed later. A verification email will be sent to the address above.', cls='step__note')}
              <div class="field field--check" data-field="consent">
                <input id="s-consent" name="consent" type="checkbox" value="1" required aria-describedby="s-consent-err">
                {T('auth.consent', 'J’ai lu les <a href="mentions-legales.html#confidentialite" target="_blank" rel="noopener">mentions légales et la politique de confidentialité</a>, et j’accepte que ces données soient utilisées pour créer et gérer mon compte.',
                   'I have read the <a href="mentions-legales.html#confidentialite" target="_blank" rel="noopener">legal notice and privacy policy</a>, and I agree that this data will be used to create and manage my account.', tag='label', attrs='for="s-consent"')}
                <p class="field__error" id="s-consent-err"></p>
              </div>
              <div class="field field--check" data-field="age">
                <input id="s-age" name="age" type="checkbox" value="1" required aria-describedby="s-age-err">
                {T('auth.age', 'J’ai 15 ans ou plus, ou j’ai l’accord d’un parent.', 'I am 15 or older, or I have a parent’s permission.', tag='label', attrs='for="s-age"')}
                <p class="field__error" id="s-age-err"></p>
              </div>
              <div class="auth-form__actions">
                <button class="btn btn--ghost" type="button" data-action="back"><span data-i18n="auth.edit">Modifier</span></button>
                <button class="btn btn--red" type="submit"><span data-i18n="auth.create">Créer mon compte</span></button>
              </div>
            </div>

            <!-- Etape 3 : compte cree -->
            <div class="step step--done" data-step="3" hidden>
              <p class="step__label" data-i18n="auth.doneLabel">Compte créé</p>
              <h2 class="step__big" tabindex="-1" data-welcome></h2>
              <p class="step__note" data-sent></p>
              <div class="auth-form__actions">
                <a class="btn btn--red" href="index.html" data-back-link><span data-i18n="auth.go">Continuer</span><img src="assets/arrow.svg" alt="" width="30" height="31"></a>
              </div>
            </div>
          </form>
        </section>
      </div>

      <!-- Connecte : resume du compte -->
      <section class="auth__member" aria-labelledby="member-name">
        <p class="step__label" data-i18n="auth.signedAs">Connecté en tant que</p>
        <h2 class="step__big" id="member-name" data-member="name"></h2>
        <p class="member-mail" data-member="email"></p>
        <p class="member-status" data-member="status"></p>
        <p class="member-since" data-member="since"></p>
        <div class="auth-form__actions">
          <button class="btn btn--ghost" type="button" data-action="logout"><span data-i18n="account.logout">Se déconnecter</span></button>
          <button class="auth-link auth-link--danger" type="button" data-action="delete" data-i18n="account.delete">Supprimer mon compte</button>
        </div>
      </section>
    </div>

    <aside class="ct-aside">
      <div class="info">
        {T('side.why.label', 'Pourquoi un compte&nbsp;?', 'Why an account?', cls='info__label')}
        {T('side.why.text', 'Sauvegarder vos parties et les reprendre sur n’importe quel appareil, jouer contre d’autres joueurs, suivre votre progression.',
           'Save your games and pick them up on any device, play against other players, track your progress.', cls='info__text')}
      </div>
      <div class="info">
        {T('side.data.label', 'Vos données', 'Your data', cls='info__label')}
        {T('side.data.text', 'Nous ne conservons que votre pseudo, votre e-mail et votre progression. Rien n’est revendu ni partagé. Détails dans les <a href="mentions-legales.html#confidentialite">mentions légales</a>.',
           'We only keep your username, email and progress. Nothing is sold or shared. Details in the <a href="mentions-legales.html#confidentialite">legal notice</a>.', cls='info__text')}
      </div>
      <div class="info">
        {T('side.delete.label', 'Supprimer votre compte', 'Deleting your account', cls='info__label')}
        {T('side.delete.text', 'À tout moment, depuis le bouton compte en haut de page&nbsp;: toutes vos données sont alors effacées immédiatement.',
           'Any time, from the account button at the top of the page: all your data is erased immediately.', cls='info__text')}
      </div>
    </aside>
  </div>'''

    for key, fr, en in [
        ('auth.tabs', 'Connexion ou inscription', 'Sign in or sign up'),
        ('auth.email', 'E-mail', 'Email'),
        ('auth.password', 'Mot de passe', 'Password'),
        ('auth.password2', 'Confirmez le mot de passe', 'Confirm password'),
        ('auth.username', 'Pseudo', 'Username'),
        ('auth.usernameHint', '3 à 20 caractères : lettres sans accent, chiffres, « - » et « _ ». Visible des autres joueurs.',
         '3 to 20 characters: unaccented letters, digits, “-” and “_”. Visible to other players.'),
        ('auth.passwordHint', 'Au moins 8 caractères, avec au moins une lettre et un chiffre.',
         'At least 8 characters, with at least one letter and one digit.'),
        ('auth.submitLogin', 'Se connecter', 'Sign in'),
        ('auth.forgot', 'Mot de passe oublié ?', 'Forgot password?'),
        ('auth.continue', 'Continuer', 'Continue'),
        ('auth.tab.login', 'Connexion', 'Sign in'),
        ('auth.tab.signup', 'Créer un compte', 'Create an account'),
        ('auth.step1', 'Vos informations', 'Your details'),
        ('auth.step2', 'Vérification', 'Review'),
        ('auth.step3', 'Confirmation', 'Done'),
        ('auth.edit', 'Modifier', 'Edit'),
        ('auth.create', 'Créer mon compte', 'Create my account'),
        ('auth.doneLabel', 'Compte créé', 'Account created'),
        ('auth.go', 'Continuer', 'Continue'),
    ]:
        K(key, fr, en)

    render(p, file='compte.html',
           meta_title=('Mon compte — GameBoxHeroes', 'My account — GameBoxHeroes'),
           meta_desc=('Connectez-vous ou créez votre compte GameBoxHeroes pour sauvegarder vos parties.',
                      'Sign in or create your GameBoxHeroes account to save your games.'),
           noindex=True,
           top=top, body=body, css=['roadmap.css', 'contact.css', 'compte.css'], modules=['compte.js'],
           body_class='page-account', generator='tools/gen_static.py')


# ===========================================================================
#  Mentions legales et politique de confidentialite
# ===========================================================================

def build_legal():
    p = Page()
    top = top_block(p, ('Mentions légales', 'Legal notice'),
                    ('Éditeur, hébergement, comptes joueurs,<br>données personnelles et cookies.',
                     'Publisher, hosting, player accounts,<br>personal data and cookies.'))
    p.k('legal.toc', 'Sur cette page', 'On this page')

    def body(lang, text):
        return f'''  <div class="wrap cols split legal-body">
    <article class="legal legal--{lang}" lang="{lang}">
{text}
    </article>

    <aside class="legal-toc">
      <nav data-i18n-attr="aria-label:legal.toc" aria-label="Sur cette page">
        <p class="info__label" data-i18n="legal.toc">Sur cette page</p>
        <ol class="legal-toc__list" data-toc></ol>
      </nav>
    </aside>
  </div>'''

    render(p, file='mentions-legales.html',
           meta_title=('Mentions légales et confidentialité — GameBoxHeroes', 'Legal notice and privacy — GameBoxHeroes'),
           meta_desc=('Mentions légales du site GameBoxHeroes : éditeur, hébergement, comptes joueurs, politique de confidentialité, données personnelles et cookies.',
                      'Legal notice for the GameBoxHeroes website: publisher, hosting, player accounts, privacy policy, personal data and cookies.'),
           top=top, body=body('fr', LEGAL_FR), body_en=body('en', LEGAL_EN),
           css=['roadmap.css', 'contact.css', 'pages.css'], scripts=['legal.js'],
           body_class='page-legal', generator='tools/gen_static.py')


build_contact()
build_account()
build_legal()
print('ok')
