// Formulaire « Rester au courant » du pied de page.
import { configured, subscribe, checkEmail, errorKey } from './firebase.js';

const form = document.querySelector('.news-form');

if (form) {
  const email = form.elements.email;
  const consent = form.elements.consent;
  const submit = form.querySelector('.news-form__submit');
  const msg = form.querySelector('.news-form__msg');
  const t = (key) => (window.GBH_T ? window.GBH_T(key) : key);

  let msgKey = null;
  let ok = false;

  const show = (key, success = false) => {
    msgKey = key;
    ok = success;
    msg.classList.toggle('news-form__msg--ok', success);
    msg.innerHTML = key ? t(key) : '';
    form.classList.toggle('is-invalid', Boolean(key) && !success);
  };

  email.addEventListener('input', () => { if (msgKey && !ok) show(null); });
  consent.addEventListener('change', () => {
    consent.closest('.field').classList.remove('is-invalid');
    if (msgKey === 'nl.consentRequired') show(null);
  });

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (submit.disabled) return;

    const error = checkEmail(email.value.trim());
    if (error) {
      show(`error.${error}`);
      email.focus();
      return;
    }
    if (!consent.checked) {
      consent.closest('.field').classList.add('is-invalid');
      show('nl.consentRequired');
      consent.focus();
      return;
    }
    if (!configured) {
      show('nl.soon');
      return;
    }

    submit.disabled = true;
    submit.setAttribute('aria-busy', 'true');
    try {
      await subscribe(email.value, document.documentElement.lang === 'en' ? 'en' : 'fr');
      form.reset();
      show('nl.ok', true);
    } catch (err) {
      show(errorKey(err));
    } finally {
      submit.disabled = false;
      submit.removeAttribute('aria-busy');
    }
  });

  document.addEventListener('gbh:lang', () => { if (msgKey) msg.innerHTML = t(msgKey); });
}
