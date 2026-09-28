// Bouton compte de l'en-tete (a gauche du menu) : menu deroulant
// connexion / inscription, ou deconnexion / suppression une fois connecte.
import {
  configured, watchUser, signOut, deleteAccount, resendVerification, errorKey
} from './firebase.js';

const root = document.querySelector('.account');

if (root) {
  const btn = root.querySelector('.account__btn');
  const initial = root.querySelector('.account__initial');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const t = (key) => (window.GBH_T ? window.GBH_T(key) : key);
  const lang = () => document.documentElement.lang || 'fr';
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

  let user = null;
  let closeTimer;

  // Le lien mene a compte.html sans JavaScript ; avec, il ouvre le menu.
  btn.setAttribute('role', 'button');
  btn.setAttribute('aria-haspopup', 'true');
  btn.setAttribute('aria-expanded', 'false');

  const menu = document.createElement('div');
  menu.className = 'account__menu';
  menu.id = 'account-menu';
  menu.hidden = true;
  root.append(menu);
  btn.setAttribute('aria-controls', menu.id);

  /* -----------------------------------------------------------------------
     Contenu du menu
     ----------------------------------------------------------------------- */

  const back = encodeURIComponent(location.pathname.split('/').pop() + location.search + location.hash);

  const render = () => {
    if (!configured) {
      menu.innerHTML = `<p class="account__hint">${t('account.soon')}</p>`;
      return;
    }
    if (!user) {
      menu.innerHTML = `
        <p class="account__hint">${t('account.pitch')}</p>
        <a class="account__item account__item--primary" href="compte.html?retour=${back}#connexion">${t('account.signin')}</a>
        <a class="account__item" href="compte.html?retour=${back}#inscription">${t('account.signup')}</a>`;
      return;
    }
    menu.innerHTML = `
      <div class="account__who">
        <span class="account__pseudo">${esc(user.displayName || '')}</span>
        <span class="account__email">${esc(user.email || '')}</span>
      </div>
      ${user.emailVerified ? '' : `<p class="account__warn">${t('account.unverified')} <button type="button" class="account__link" data-action="verify">${t('account.resend')}</button></p>`}
      <a class="account__item" href="compte.html">${t('account.manage')}</a>
      <button type="button" class="account__item" data-action="logout">${t('account.logout')}</button>
      <button type="button" class="account__item account__item--danger" data-action="delete">${t('account.delete')}</button>`;
  };

  const paint = () => {
    const name = user && user.displayName;
    root.classList.toggle('is-signed', Boolean(user));
    initial.textContent = name ? name[0].toUpperCase() : '';
    btn.setAttribute('aria-label', name ? `${t('account.label')} — ${name}` : t('account.label'));
    render();
  };

  /* -----------------------------------------------------------------------
     Ouverture / fermeture (origine en haut a droite, sous le bouton)
     ----------------------------------------------------------------------- */

  const items = () => [...menu.querySelectorAll('a, button')];

  const open = () => {
    clearTimeout(closeTimer);
    menu.hidden = false;
    requestAnimationFrame(() => requestAnimationFrame(() => menu.classList.add('is-open')));
    btn.setAttribute('aria-expanded', 'true');
  };

  const close = (focusBtn = false) => {
    if (menu.hidden) return;
    menu.classList.remove('is-open');
    btn.setAttribute('aria-expanded', 'false');
    closeTimer = setTimeout(() => { menu.hidden = true; }, reduceMotion ? 0 : 140);
    if (focusBtn) btn.focus({ preventScroll: true });
  };

  btn.addEventListener('click', (e) => {
    e.preventDefault();
    if (menu.hidden || !menu.classList.contains('is-open')) {
      open();
      // Clavier : le focus passe sur le premier element du menu
      if (e.detail === 0) setTimeout(() => items()[0]?.focus(), 0);
    } else {
      close();
    }
  });

  document.addEventListener('click', (e) => {
    if (!root.contains(e.target)) close();
  });

  root.addEventListener('keydown', (e) => {
    if (menu.hidden) return;
    const list = items();
    const i = list.indexOf(document.activeElement);
    if (e.key === 'Escape') { e.stopPropagation(); close(true); }
    else if (e.key === 'ArrowDown') { e.preventDefault(); list[(i + 1) % list.length]?.focus(); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); list[(i - 1 + list.length) % list.length]?.focus(); }
  });

  root.addEventListener('focusout', (e) => {
    if (!root.contains(e.relatedTarget)) close();
  });

  /* -----------------------------------------------------------------------
     Actions
     ----------------------------------------------------------------------- */

  menu.addEventListener('click', async (e) => {
    const action = e.target.closest('[data-action]')?.dataset.action;
    if (!action) return;

    if (action === 'logout') {
      close(true);
      await signOut().catch(() => {});
    } else if (action === 'delete') {
      close();
      openDeleteDialog();
    } else if (action === 'verify') {
      const link = e.target;
      link.disabled = true;
      try {
        await resendVerification(lang());
        link.textContent = t('account.resent');
      } catch (err) {
        link.textContent = t(errorKey(err));
      }
    }
  });

  /* -----------------------------------------------------------------------
     Fenetre de suppression du compte (modale, centree)
     ----------------------------------------------------------------------- */

  let dialog;

  const buildDialog = () => {
    dialog = document.createElement('dialog');
    dialog.className = 'dialog';
    dialog.setAttribute('aria-labelledby', 'dlg-del-title');
    document.body.append(dialog);

    dialog.addEventListener('click', (e) => {
      // Clic sur le voile (en dehors de la boite) : fermeture
      if (e.target === dialog && !dialog.classList.contains('is-busy')) closeDialog();
    });
    dialog.addEventListener('cancel', (e) => {
      e.preventDefault();
      if (!dialog.classList.contains('is-busy')) closeDialog();
    });
  };

  const closeDialog = () => {
    dialog.classList.remove('is-open');
    setTimeout(() => dialog.close(), reduceMotion ? 0 : 150);
  };

  function openDeleteDialog() {
    if (!dialog) buildDialog();
    dialog.innerHTML = `
      <form class="dialog__box" method="dialog" novalidate>
        <p class="dialog__label">${t('del.label')}</p>
        <h2 class="dialog__title" id="dlg-del-title">${t('del.title')}</h2>
        <p class="dialog__text">${t('del.text')}</p>
        <div class="field">
          <label for="dlg-del-pwd">${t('del.password')}</label>
          <input id="dlg-del-pwd" type="password" autocomplete="current-password" required>
          <p class="field__error" id="dlg-del-err" role="alert"></p>
        </div>
        <div class="dialog__actions">
          <button type="button" class="btn btn--ghost" data-dlg="cancel">${t('del.cancel')}</button>
          <button type="submit" class="btn btn--red">${t('del.confirm')}</button>
        </div>
      </form>`;

    const form = dialog.querySelector('form');
    const pwd = form.querySelector('input');
    const err = form.querySelector('.field__error');
    const submit = form.querySelector('[type="submit"]');

    form.querySelector('[data-dlg="cancel"]').addEventListener('click', closeDialog);

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!pwd.value) {
        err.textContent = t('error.required');
        pwd.focus();
        return;
      }
      err.textContent = '';
      dialog.classList.add('is-busy');
      submit.disabled = true;
      submit.textContent = t('del.working');
      try {
        await deleteAccount(pwd.value);
        dialog.innerHTML = `
          <div class="dialog__box">
            <p class="dialog__label">${t('del.label')}</p>
            <h2 class="dialog__title" id="dlg-del-title">${t('del.doneTitle')}</h2>
            <p class="dialog__text">${t('del.doneText')}</p>
            <div class="dialog__actions">
              <a class="btn btn--red" href="index.html">${t('del.home')}</a>
            </div>
          </div>`;
        dialog.querySelector('a').focus();
      } catch (ex) {
        err.textContent = t(errorKey(ex));
        submit.disabled = false;
        submit.textContent = t('del.confirm');
        pwd.select();
      } finally {
        dialog.classList.remove('is-busy');
      }
    });

    dialog.showModal();
    requestAnimationFrame(() => dialog.classList.add('is-open'));
    pwd.focus();
  }

  // Ouverture depuis une autre partie du site (page compte)
  document.addEventListener('gbh:delete-account', openDeleteDialog);

  /* -----------------------------------------------------------------------
     Demarrage
     ----------------------------------------------------------------------- */

  document.addEventListener('gbh:lang', paint);
  // Le pseudo (displayName) est enregistre juste apres la creation du compte
  document.addEventListener('gbh:profile', paint);
  paint();
  watchUser((u) => {
    user = u;
    paint();
    document.dispatchEvent(new CustomEvent('gbh:user', { detail: { user: u } }));
  }).catch(() => paint());
}
