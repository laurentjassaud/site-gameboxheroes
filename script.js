(() => {
  'use strict';

  document.documentElement.classList.add('js');

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------------
     Traductions FR / EN
     Textes communs a toutes les pages : en-tete, menu, bouton compte,
     lettre d'information, pied de page. Les textes propres a une page sont
     dans son fichier *-i18n.js (window.GBH_I18N), fusionne ci-dessous.
     --------------------------------------------------------------------- */

  const translations = {
    fr: {
      'brand.tagline': 'Les <strong>boîtes</strong> de jeux<br>des classiques du <strong>wargame</strong>',
      'credit': 'Carte et pions provenant du jeu <strong>Normandy ’44</strong><br>dans un but illustratif uniquement - <strong>Tous droits GMT Games</strong>',
      'rm.back': 'Retour à l’accueil',

      'menu.open': 'Ouvrir le menu',
      'menu.close': 'Fermer le menu',
      'menu.label': 'Menu principal',
      'menu.boxes': 'Les boîtes',
      'menu.news': 'Actualités',
      'menu.roadmap': 'Road Map',
      'menu.about': 'Qui sommes-nous',
      'menu.contact': 'Contact',
      'menu.account': 'Mon compte',
      'menu.language': 'Langue',

      'account.label': 'Mon compte',
      'account.pitch': 'Un compte pour sauvegarder vos parties et jouer à plusieurs.',
      'account.signin': 'Se connecter',
      'account.signup': 'Créer un compte',
      'account.manage': 'Gérer mon compte',
      'account.logout': 'Se déconnecter',
      'account.delete': 'Supprimer mon compte',
      'account.unverified': 'E-mail non vérifié.',
      'account.resend': 'Renvoyer le lien',
      'account.resent': 'Lien envoyé',
      'account.soon': 'Les comptes joueurs arrivent bientôt.',

      'del.label': 'Suppression du compte',
      'del.title': 'Supprimer définitivement votre compte&nbsp;?',
      'del.text': 'Votre pseudo, votre e-mail et votre progression seront effacés. Cette action est irréversible.',
      'del.password': 'Confirmez avec votre mot de passe',
      'del.cancel': 'Annuler',
      'del.confirm': 'Supprimer mon compte',
      'del.working': 'Suppression…',
      'del.doneTitle': 'Compte supprimé',
      'del.doneText': 'Toutes vos données ont été effacées. Merci d’avoir joué avec nous.',
      'del.home': 'Retour à l’accueil',

      'nl.title': 'Rester au courant de l’avancement des projets',
      'nl.label': 'Votre e-mail',
      'nl.placeholder': 'Votre e-mail',
      'nl.submit': 'Envoyer',
      'nl.consent': 'J’accepte que mon e-mail soit utilisé uniquement pour recevoir des nouvelles des projets. <a href="mentions-legales.html#newsletter">En savoir plus</a>',
      'nl.ok': 'C’est noté&nbsp;! Vous recevrez nos prochaines nouvelles.',
      'nl.consentRequired': 'Cochez la case pour confirmer votre accord.',
      'nl.soon': 'La lettre d’information arrive bientôt.',

      'foot.legal': 'Mentions légales',
      'foot.privacy': 'Confidentialité',

      'error.required': 'Ce champ est obligatoire.',
      'error.invalid_email': 'Cette adresse e-mail ne semble pas valide.',
      'error.username_short': 'Le pseudo doit faire au moins 3 caractères.',
      'error.username_long': 'Le pseudo doit faire 20 caractères au plus.',
      'error.username_chars': 'Lettres sans accent, chiffres, « - » et « _ » uniquement.',
      'error.username_reserved': 'Ce pseudo est réservé.',
      'error.password_short': 'Au moins 8 caractères.',
      'error.password_long': '128 caractères au plus.',
      'error.password_weak': 'Mélangez au moins une lettre et un chiffre.',
      'error.password_mismatch': 'Les deux mots de passe ne correspondent pas.',
      'error.consent': 'Votre accord est nécessaire pour créer le compte.',

      'auth.err.credentials': 'E-mail ou mot de passe incorrect.',
      'auth.err.email': 'Cette adresse e-mail ne semble pas valide.',
      'auth.err.emailTaken': 'Un compte existe déjà avec cet e-mail.',
      'auth.err.usernameTaken': 'Ce pseudo vient d’être pris. Choisissez-en un autre.',
      'auth.err.weak': 'Mot de passe trop faible.',
      'auth.err.tooMany': 'Trop de tentatives. Patientez quelques minutes.',
      'auth.err.network': 'Connexion impossible. Vérifiez votre réseau.',
      'auth.err.recent': 'Par sécurité, reconnectez-vous puis réessayez.',
      'auth.err.disabled': 'Ce compte a été désactivé.',
      'auth.err.notConfigured': 'Les comptes ne sont pas encore ouverts.',
      'auth.err.generic': 'Une erreur est survenue. Réessayez.'
    },
    en: {
      'brand.tagline': 'The game <strong>boxes</strong><br>of classic <strong>wargames</strong>',
      'credit': 'Map and counters from <strong>Normandy ’44</strong><br>for illustration only - <strong>All rights GMT Games</strong>',
      'rm.back': 'Back to home',

      'menu.open': 'Open menu',
      'menu.close': 'Close menu',
      'menu.label': 'Main menu',
      'menu.boxes': 'The boxes',
      'menu.news': 'News',
      'menu.roadmap': 'Road Map',
      'menu.about': 'About us',
      'menu.contact': 'Contact',
      'menu.account': 'My account',
      'menu.language': 'Language',

      'account.label': 'My account',
      'account.pitch': 'An account to save your games and play with others.',
      'account.signin': 'Sign in',
      'account.signup': 'Create an account',
      'account.manage': 'Manage my account',
      'account.logout': 'Sign out',
      'account.delete': 'Delete my account',
      'account.unverified': 'Email not verified.',
      'account.resend': 'Resend link',
      'account.resent': 'Link sent',
      'account.soon': 'Player accounts are coming soon.',

      'del.label': 'Account deletion',
      'del.title': 'Permanently delete your account?',
      'del.text': 'Your username, email and progress will be erased. This cannot be undone.',
      'del.password': 'Confirm with your password',
      'del.cancel': 'Cancel',
      'del.confirm': 'Delete my account',
      'del.working': 'Deleting…',
      'del.doneTitle': 'Account deleted',
      'del.doneText': 'All your data has been erased. Thanks for playing with us.',
      'del.home': 'Back to home',

      'nl.title': 'Keep up with the projects',
      'nl.label': 'Your email',
      'nl.placeholder': 'Your email',
      'nl.submit': 'Send',
      'nl.consent': 'I agree that my email will be used only to send me project news. <a href="mentions-legales.html#newsletter">Learn more</a>',
      'nl.ok': 'Got it! You’ll receive our next update.',
      'nl.consentRequired': 'Tick the box to confirm you agree.',
      'nl.soon': 'The newsletter is coming soon.',

      'foot.legal': 'Legal notice',
      'foot.privacy': 'Privacy',

      'error.required': 'This field is required.',
      'error.invalid_email': 'This email address doesn’t look valid.',
      'error.username_short': 'Usernames need at least 3 characters.',
      'error.username_long': 'Usernames can be 20 characters at most.',
      'error.username_chars': 'Unaccented letters, digits, “-” and “_” only.',
      'error.username_reserved': 'This username is reserved.',
      'error.password_short': 'At least 8 characters.',
      'error.password_long': '128 characters at most.',
      'error.password_weak': 'Use at least one letter and one digit.',
      'error.password_mismatch': 'The two passwords don’t match.',
      'error.consent': 'We need your consent to create the account.',

      'auth.err.credentials': 'Wrong email or password.',
      'auth.err.email': 'This email address doesn’t look valid.',
      'auth.err.emailTaken': 'An account already exists with this email.',
      'auth.err.usernameTaken': 'This username was just taken. Pick another one.',
      'auth.err.weak': 'Password too weak.',
      'auth.err.tooMany': 'Too many attempts. Wait a few minutes.',
      'auth.err.network': 'Could not connect. Check your network.',
      'auth.err.recent': 'For security, sign in again and retry.',
      'auth.err.disabled': 'This account has been disabled.',
      'auth.err.notConfigured': 'Accounts are not open yet.',
      'auth.err.generic': 'Something went wrong. Please try again.'
    }
  };

  // Traductions propres a une page (ex. roadmap-i18n.js), chargees avant ce script
  const pageTranslations = window.GBH_I18N || {};
  Object.keys(translations).forEach((lang) => Object.assign(translations[lang], pageTranslations[lang]));

  // Une page par langue : le francais a la racine, l'anglais dans en/. La
  // langue est celle du fichier charge (<html lang>), on en change par les
  // liens FR / EN du menu.
  const currentLang = document.documentElement.lang === 'en' ? 'en' : 'fr';

  // Acces aux traductions pour les modules (account.js, compte.js, newsletter.js)
  window.GBH_T = (key) => {
    const value = translations[currentLang][key];
    return value == null ? key : value;
  };

  // Le HTML est deja dans la bonne langue ; on repasse le dictionnaire pour
  // les textes ecrits par les scripts et on previent les pages (gbh:lang).
  const applyLang = (lang) => {
    const dict = translations[lang];

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

    document.dispatchEvent(new CustomEvent('gbh:lang', { detail: { lang, dict } }));
  };

  applyLang(currentLang);

  /* ---------------------------------------------------------------------
     Menu lateral
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
    closeTimer = setTimeout(() => { menu.hidden = true; }, reduceMotion ? 0 : 400);
    burger.focus({ preventScroll: true });
  };

  if (menu && burger) {
    burger.addEventListener('click', openMenu);
    menu.querySelectorAll('[data-close]').forEach((el) => el.addEventListener('click', closeMenu));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !menu.hidden) closeMenu();
    });
  }

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
    }, { threshold: 0.15 });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('is-in'));
  }
})();
