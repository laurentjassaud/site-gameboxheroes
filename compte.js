// Page Mon compte : connexion, inscription en trois etapes
// (saisie -> verification et acceptation -> confirmation) et resume du compte.
import {
  configured, watchUser, signIn, signOut, register, resetPassword, resendVerification,
  isUsernameFree, checkUsername, checkEmail, checkPassword, errorKey
} from './firebase.js';

const auth = document.querySelector('.auth');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const t = (key) => (window.GBH_T ? window.GBH_T(key) : key);
const lang = () => (document.documentElement.lang === 'en' ? 'en' : 'fr');
const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

/* -------------------------------------------------------------------------
   Page de retour (?retour=page.html) : uniquement une page du site
   ------------------------------------------------------------------------- */

const params = new URLSearchParams(location.search);
const back = (() => {
  const r = params.get('retour') || '';
  return /^[a-z0-9-]+\.html([?#][^\s]*)?$/i.test(r) && !r.startsWith('compte.html') ? r : null;
})();
if (back) document.querySelector('[data-back-link]').href = back;

/* -------------------------------------------------------------------------
   Outils de formulaire
   ------------------------------------------------------------------------- */

// Erreurs affichees sous les champs ; cle retenue pour retraduire au changement de langue
const setError = (form, name, key) => {
  const box = form.querySelector(`[data-field="${name}"]`);
  const input = form.elements[name];
  const out = box.querySelector('.field__error');
  box.dataset.error = key || '';
  box.classList.toggle('is-invalid', Boolean(key));
  input.setAttribute('aria-invalid', String(Boolean(key)));
  out.textContent = key ? t(key) : '';
};

const setStatus = (form, key, ok = false, vars = {}) => {
  const box = form.querySelector('.form-status');
  box.dataset.key = key || '';
  box.hidden = !key;
  box.classList.toggle('form-status--ok', ok);
  box.innerHTML = key ? fill(t(key), vars) : '';
  if (key && !reduceMotion) {
    box.classList.remove('is-shown');
    void box.offsetWidth;
    box.classList.add('is-shown');
  }
};

const fill = (text, vars) => text.replace(/\{(\w+)\}/g, (_, k) => esc(vars[k] ?? ''));

const busy = (btn, labelKey) => {
  const label = btn.querySelector('span');
  const prev = label.dataset.i18n;
  btn.disabled = true;
  label.textContent = t(labelKey);
  const spin = document.createElement('i');
  spin.className = 'spinner';
  btn.append(spin);
  return () => {
    btn.disabled = false;
    label.textContent = t(prev);
    spin.remove();
  };
};

// Bouton afficher / masquer le mot de passe
document.querySelectorAll('.pwd__toggle').forEach((btn) => {
  const input = document.getElementById(btn.getAttribute('aria-controls'));
  btn.addEventListener('click', () => {
    const show = input.type === 'password';
    input.type = show ? 'text' : 'password';
    btn.setAttribute('aria-pressed', String(show));
    btn.setAttribute('aria-label', t(show ? 'auth.hide' : 'auth.show'));
    btn.dataset.i18nAttr = `aria-label:${show ? 'auth.hide' : 'auth.show'}`;
    input.focus();
  });
});

/* -------------------------------------------------------------------------
   Onglets Connexion / Creer un compte
   ------------------------------------------------------------------------- */

const tabs = [...document.querySelectorAll('.tabs__tab')];
const ink = document.querySelector('.tabs__ink');

const moveInk = (tab) => {
  ink.style.setProperty('--ink-x', `${tab.offsetLeft}px`);
  ink.style.setProperty('--ink-s', String(tab.offsetWidth / 100));
};

const selectTab = (tab, { focus = false, updateHash = true } = {}) => {
  tabs.forEach((other) => {
    const on = other === tab;
    other.setAttribute('aria-selected', String(on));
    other.tabIndex = on ? 0 : -1;
    document.getElementById(other.getAttribute('aria-controls')).hidden = !on;
  });
  moveInk(tab);
  if (focus) tab.focus();
  if (updateHash) history.replaceState(null, '', `${location.pathname}${location.search}#${tab.id === 'tab-signup' ? 'inscription' : 'connexion'}`);
};

tabs.forEach((tab, i) => {
  tab.addEventListener('click', () => selectTab(tab));
  tab.addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    e.preventDefault();
    selectTab(tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length], { focus: true });
  });
});

const tabFromHash = () => selectTab(location.hash === '#inscription' ? tabs[1] : tabs[0], { updateHash: false });

window.addEventListener('hashchange', tabFromHash);
window.addEventListener('resize', () => moveInk(tabs.find((x) => x.getAttribute('aria-selected') === 'true')));

/* -------------------------------------------------------------------------
   Connexion
   ------------------------------------------------------------------------- */

const login = document.getElementById('login-form');

const validateLogin = () => {
  const e1 = checkEmail(login.elements.email.value.trim());
  setError(login, 'email', e1 && `error.${e1}`);
  const e2 = login.elements.password.value ? null : 'required';
  setError(login, 'password', e2 && `error.${e2}`);
  return !e1 && !e2;
};

['email', 'password'].forEach((name) => {
  login.elements[name].addEventListener('input', () => {
    if (login.querySelector(`[data-field="${name}"]`).dataset.error) validateLogin();
  });
});

login.addEventListener('submit', async (e) => {
  e.preventDefault();
  setStatus(login, null);
  if (!validateLogin()) {
    login.querySelector('.is-invalid input').focus();
    return;
  }
  const done = busy(login.querySelector('[type="submit"]'), 'auth.signingIn');
  try {
    await signIn(login.elements.email.value.trim(), login.elements.password.value);
    if (back) location.href = back;
  } catch (err) {
    setStatus(login, errorKey(err));
    login.elements.password.select();
  } finally {
    done();
  }
});

login.querySelector('[data-action="reset"]').addEventListener('click', async () => {
  const email = login.elements.email.value.trim();
  if (checkEmail(email)) {
    setError(login, 'email', null);
    setStatus(login, 'auth.resetNeedsEmail');
    login.elements.email.focus();
    return;
  }
  try {
    await resetPassword(email, lang());
    setStatus(login, 'auth.resetSent', true);
  } catch (err) {
    // Adresse inconnue : meme message, pour ne pas reveler quels comptes existent
    if (err.code === 'auth/user-not-found') setStatus(login, 'auth.resetSent', true);
    else setStatus(login, errorKey(err));
  }
});

/* -------------------------------------------------------------------------
   Inscription
   ------------------------------------------------------------------------- */

const signup = document.getElementById('signup-form');
const avail = document.getElementById('s-username-avail');
const meter = signup.querySelector('.meter');
let step = 1;
let registering = false;

const goStep = (n) => {
  step = n;
  signup.querySelectorAll('.step').forEach((el) => { el.hidden = Number(el.dataset.step) !== n; });
  signup.querySelectorAll('[data-step-dot]').forEach((dot) => {
    const d = Number(dot.dataset.stepDot);
    dot.classList.toggle('is-current', d === n);
    dot.classList.toggle('is-done', d < n);
  });
  setStatus(signup, null);
  const heading = signup.querySelector(`.step[data-step="${n}"] [tabindex="-1"]`);
  if (heading) heading.focus({ preventScroll: true });
  if (n !== 1) signup.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'nearest' });
};

// --- Disponibilite du pseudo (verification en direct, la derniere reponse gagne)
let availToken = 0;
let availTimer;
let availState = null; // 'free' | 'taken' | null

const setAvail = (state) => {
  availState = state === 'checking' ? null : state;
  if (state) avail.dataset.state = state;
  else delete avail.dataset.state;
  avail.textContent = state ? t({ checking: 'auth.checking', free: 'auth.free', taken: 'auth.taken' }[state]) : '';
};

const checkAvailability = async (name) => {
  const token = ++availToken;
  setAvail('checking');
  try {
    const free = await isUsernameFree(name);
    if (token !== availToken) return null;
    setAvail(free ? 'free' : 'taken');
    return free;
  } catch {
    if (token === availToken) setAvail(null);
    return null;
  }
};

signup.elements.username.addEventListener('input', () => {
  const v = signup.elements.username.value.trim();
  clearTimeout(availTimer);
  availToken++;
  const err = checkUsername(v);
  if (signup.querySelector('[data-field="username"]').dataset.error || (v.length >= 3 && err)) {
    setError(signup, 'username', err && `error.${err}`);
  }
  if (err || !configured) { setAvail(null); return; }
  setAvail(null);
  availTimer = setTimeout(() => checkAvailability(v), 400);
});

// --- Robustesse du mot de passe (indicative ; la regle minimale est checkPassword)
const score = (v) => {
  if (!v) return 0;
  let s = 0;
  if (v.length >= 8) s++;
  if (v.length >= 12) s++;
  if (/[a-z]/.test(v) && /[A-Z]/.test(v)) s++;
  if (/\d/.test(v) && /[^A-Za-z0-9]/.test(v)) s++;
  if (checkPassword(v)) s = Math.min(s, 1);
  return Math.max(1, s);
};

const paintMeter = () => {
  const s = score(signup.elements.password.value);
  meter.dataset.score = String(s);
  meter.querySelector('em').textContent = t(`auth.strength${s}`);
};

signup.elements.password.addEventListener('input', () => {
  paintMeter();
  if (signup.querySelector('[data-field="password"]').dataset.error) validateField('password');
  if (signup.elements.password2.value) validateField('password2');
});

// --- Validation de l'etape 1
const rules = {
  username: () => checkUsername(signup.elements.username.value.trim()),
  email: () => checkEmail(signup.elements.email.value.trim()),
  password: () => checkPassword(signup.elements.password.value),
  password2: () => {
    const v = signup.elements.password2.value;
    if (!v) return 'required';
    return v === signup.elements.password.value ? null : 'password_mismatch';
  }
};

const validateField = (name) => {
  const code = rules[name]();
  setError(signup, name, code && `error.${code}`);
  return code;
};

Object.keys(rules).forEach((name) => {
  const el = signup.elements[name];
  el.addEventListener('blur', () => { if (el.value) validateField(name); });
  if (name !== 'username' && name !== 'password') {
    el.addEventListener('input', () => {
      if (signup.querySelector(`[data-field="${name}"]`).dataset.error) validateField(name);
    });
  }
});

signup.querySelector('[data-action="next"]').addEventListener('click', async (e) => {
  const invalid = Object.keys(rules).filter((name) => validateField(name));
  if (invalid.length) {
    setStatus(signup, 'auth.fix');
    signup.elements[invalid[0]].focus();
    return;
  }

  // Pseudo : on (re)verifie la disponibilite avant d'afficher le recapitulatif
  if (availState !== 'free') {
    const done = busy(e.currentTarget, 'auth.checking');
    const free = await checkAvailability(signup.elements.username.value.trim());
    done();
    if (free === false) {
      setError(signup, 'username', 'auth.taken');
      signup.elements.username.focus();
      return;
    }
    if (free === null) {
      setStatus(signup, 'auth.err.network');
      return;
    }
  }

  signup.querySelector('[data-recap="username"]').textContent = signup.elements.username.value.trim();
  signup.querySelector('[data-recap="email"]').textContent = signup.elements.email.value.trim();
  goStep(2);
});

signup.querySelector('[data-action="back"]').addEventListener('click', () => {
  goStep(1);
  signup.elements.username.focus();
});

['consent', 'age'].forEach((name) => {
  signup.elements[name].addEventListener('change', () => {
    if (signup.elements[name].checked) setError(signup, name, null);
  });
});

// --- Etape 2 : acceptation puis creation
signup.addEventListener('submit', async (e) => {
  e.preventDefault();
  if (step === 1) { signup.querySelector('[data-action="next"]').click(); return; }
  if (step !== 2) return;

  const missing = ['consent', 'age'].filter((name) => !signup.elements[name].checked);
  setError(signup, 'consent', signup.elements.consent.checked ? null : 'error.consent');
  setError(signup, 'age', signup.elements.age.checked ? null : 'error.consent');
  if (missing.length) {
    signup.elements[missing[0]].focus();
    return;
  }

  const username = signup.elements.username.value.trim();
  const email = signup.elements.email.value.trim();
  const done = busy(signup.querySelector('[type="submit"]'), 'auth.creating');
  registering = true;
  setStatus(signup, null);

  try {
    await register({ username, email, password: signup.elements.password.value, lang: lang() });
    document.dispatchEvent(new CustomEvent('gbh:profile'));
    signup.querySelector('[data-welcome]').innerHTML = fill(t('auth.welcome'), { name: username });
    signup.querySelector('[data-sent]').innerHTML = fill(t('auth.sentTo'), { email });
    signup.querySelector('[data-welcome]').dataset.name = username;
    signup.querySelector('[data-sent]').dataset.email = email;
    ['password', 'password2'].forEach((n) => { signup.elements[n].value = ''; });
    goStep(3);
  } catch (err) {
    const key = errorKey(err);
    // Retour a l'etape 1 sur le champ concerne
    if (key === 'auth.err.emailTaken' || key === 'auth.err.email') {
      goStep(1);
      setError(signup, 'email', key);
      signup.elements.email.focus();
    } else if (key === 'auth.err.usernameTaken') {
      goStep(1);
      setAvail('taken');
      setError(signup, 'username', key);
      signup.elements.username.focus();
    } else {
      setStatus(signup, key);
    }
  } finally {
    registering = false;
    done();
  }
});

/* -------------------------------------------------------------------------
   Compte connecte
   ------------------------------------------------------------------------- */

const member = document.querySelector('.auth__member');
let current = null;

const paintMember = () => {
  if (!current) return;
  member.querySelector('[data-member="name"]').textContent = current.displayName || current.email;
  member.querySelector('[data-member="email"]').textContent = current.email;
  const status = member.querySelector('[data-member="status"]');
  status.className = `member-status ${current.emailVerified ? 'is-ok' : 'is-warn'}`;
  status.innerHTML = current.emailVerified
    ? t('auth.verified')
    : `${t('auth.unverified')} · <button type="button" class="account__link" data-action="verify">${t('account.resend')}</button>`;
  const created = current.metadata && current.metadata.creationTime;
  member.querySelector('[data-member="since"]').textContent = created
    ? fill(t('auth.memberSince'), { date: new Intl.DateTimeFormat(lang(), { dateStyle: 'long' }).format(new Date(created)) })
    : '';
};

member.addEventListener('click', async (e) => {
  const action = e.target.closest('[data-action]')?.dataset.action;
  if (action === 'logout') await signOut().catch(() => {});
  if (action === 'delete') document.dispatchEvent(new CustomEvent('gbh:delete-account'));
  if (action === 'verify') {
    e.target.disabled = true;
    try {
      await resendVerification(lang());
      e.target.textContent = t('account.resent');
    } catch (err) {
      e.target.textContent = t(errorKey(err));
    }
  }
});

/* -------------------------------------------------------------------------
   Etat de la page
   ------------------------------------------------------------------------- */

const setState = (state) => {
  auth.dataset.state = state;
  if (state === 'out') requestAnimationFrame(tabFromHash);
};

if (!configured) {
  setState('off');
} else {
  watchUser((user) => {
    current = user;
    // Pendant l'inscription, on reste sur l'etape 3 (confirmation)
    if (registering || (step === 3 && user)) return;
    if (user) {
      paintMember();
      setState('in');
    } else {
      if (step !== 1) goStep(1);
      setState('out');
    }
  }).catch(() => setState('off'));
}

/* -------------------------------------------------------------------------
   Changement de langue : on retraduit les messages dynamiques
   ------------------------------------------------------------------------- */

document.addEventListener('gbh:lang', () => {
  [login, signup].forEach((form) => {
    form.querySelectorAll('[data-field]').forEach((box) => {
      const key = box.dataset.error;
      if (key) box.querySelector('.field__error').textContent = t(key);
    });
    const status = form.querySelector('.form-status');
    if (status.dataset.key) status.innerHTML = t(status.dataset.key);
  });
  if (avail.dataset.state) setAvail(avail.dataset.state);
  paintMeter();
  const welcome = signup.querySelector('[data-welcome]');
  if (welcome.dataset.name) {
    welcome.innerHTML = fill(t('auth.welcome'), { name: welcome.dataset.name });
    signup.querySelector('[data-sent]').innerHTML = fill(t('auth.sentTo'), { email: signup.querySelector('[data-sent]').dataset.email });
  }
  paintMember();
  const sel = tabs.find((x) => x.getAttribute('aria-selected') === 'true');
  if (sel) requestAnimationFrame(() => moveInk(sel));
});

paintMeter();
