(() => {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const form = document.querySelector('.ct-form');
  const success = document.querySelector('.ct-success');
  const statusBox = form.querySelector('.form-status');
  const submit = form.querySelector('.submit');
  const submitLabel = submit.querySelector('.submit__label');
  const counter = form.querySelector('.field__count');
  const SUBJECTS = ['general', 'module', 'bug', 'press'];
  const MAX_MESSAGE = 5000;

  let dict = (window.GBH_I18N || {})[document.documentElement.lang] || {};
  let statusCode = null;
  let sending = false;

  const t = (key) => dict[key] || key;

  // Le JS prend le relais de la validation native (messages traduits)
  form.noValidate = true;
  form.elements.t.value = String(Date.now());
  form.elements.lang.value = document.documentElement.lang;

  /* ---------------------------------------------------------------------
     Validation (memes regles que contact.php)
     --------------------------------------------------------------------- */

  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  const rules = {
    name: (v) => (!v ? 'required' : v.length < 2 ? 'too_short' : v.length > 100 ? 'too_long' : null),
    email: (v) => (!v ? 'required' : v.length > 254 || !EMAIL_RE.test(v) ? 'invalid_email' : null),
    subject: (v) => (SUBJECTS.includes(v) ? null : 'invalid_subject'),
    message: (v) => (!v ? 'required' : v.length < 10 ? 'too_short' : v.length > MAX_MESSAGE ? 'too_long' : null),
    consent: (_, el) => (el.checked ? null : 'consent_required')
  };

  const fieldBox = (name) => form.querySelector(`[data-field="${name}"]`);

  const setFieldError = (name, code) => {
    const box = fieldBox(name);
    const input = form.elements[name];
    const out = box.querySelector('.field__error');
    box.dataset.error = code || '';
    box.classList.toggle('is-invalid', Boolean(code));
    input.setAttribute('aria-invalid', String(Boolean(code)));
    out.textContent = code ? t(`error.${code}`) : '';
  };

  const validateField = (name) => {
    const el = form.elements[name];
    const code = rules[name](el.value.trim(), el);
    setFieldError(name, code);
    return code;
  };

  const setStatus = (code) => {
    statusCode = code;
    statusBox.hidden = !code;
    statusBox.textContent = code ? t(`status.${code}`) : '';
    if (code && !reduceMotion) {
      statusBox.classList.remove('is-shown');
      void statusBox.offsetWidth;
      statusBox.classList.add('is-shown');
    }
  };

  Object.keys(rules).forEach((name) => {
    const el = form.elements[name];
    // Premier controle a la sortie du champ, puis en direct tant qu'il est en erreur
    el.addEventListener('blur', () => {
      if (el.value.trim() !== '' || fieldBox(name).dataset.error) validateField(name);
    });
    el.addEventListener(el.type === 'checkbox' || el.tagName === 'SELECT' ? 'change' : 'input', () => {
      if (fieldBox(name).dataset.error) validateField(name);
    });
  });

  /* ---------------------------------------------------------------------
     Compteur de caracteres
     --------------------------------------------------------------------- */

  const updateCounter = () => {
    const n = form.elements.message.value.length;
    counter.textContent = `${n} / ${MAX_MESSAGE}`;
    counter.classList.toggle('is-near', n > MAX_MESSAGE * 0.9);
  };

  form.elements.message.addEventListener('input', updateCounter);

  /* ---------------------------------------------------------------------
     Envoi
     --------------------------------------------------------------------- */

  const setSending = (on) => {
    sending = on;
    submit.disabled = on;
    submit.classList.toggle('is-loading', on);
    form.setAttribute('aria-busy', String(on));
    submitLabel.textContent = t(on ? 'form.sending' : 'form.submit');
  };

  const showSuccess = () => {
    const done = () => {
      form.hidden = true;
      form.classList.remove('is-leaving');
      success.hidden = false;
      success.focus({ preventScroll: true });
    };
    if (reduceMotion) return done();
    form.classList.add('is-leaving');
    setTimeout(done, 250);
  };

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (sending) return;

    const invalid = Object.keys(rules).filter((name) => validateField(name));
    if (invalid.length) {
      setStatus('invalid');
      form.elements[invalid[0]].focus();
      return;
    }

    setStatus(null);
    setSending(true);

    try {
      const response = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { Accept: 'application/json' }
      });
      const data = await response.json();

      if (data.ok) {
        form.reset();
        updateCounter();
        showSuccess();
        return;
      }

      if (data.fields) {
        Object.entries(data.fields).forEach(([name, code]) => {
          if (fieldBox(name)) setFieldError(name, code);
        });
        const first = Object.keys(data.fields).find((name) => form.elements[name]);
        if (first) form.elements[first].focus();
      }
      setStatus(data.error || 'send_failed');
    } catch {
      // Pas de reseau, ou page ouverte sans serveur PHP
      setStatus('network');
    } finally {
      setSending(false);
    }
  });

  success.querySelector('.ct-again').addEventListener('click', () => {
    success.hidden = true;
    form.hidden = false;
    form.elements.t.value = String(Date.now());
    Object.keys(rules).forEach((name) => setFieldError(name, null));
    setStatus(null);
    form.elements.name.focus();
  });

  /* ---------------------------------------------------------------------
     Raccourcis du haut de page : choisissent le sujet
     --------------------------------------------------------------------- */

  const selectSubject = (subject, focus = true) => {
    if (!SUBJECTS.includes(subject)) return;
    const select = form.elements.subject;
    select.value = subject;
    setFieldError('subject', null);

    const box = fieldBox('subject');
    box.classList.remove('is-flash');
    void box.offsetWidth;
    box.classList.add('is-flash');

    if (!focus) return;
    form.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
    setTimeout(() => form.elements.message.focus({ preventScroll: true }), reduceMotion ? 0 : 500);
  };

  document.querySelectorAll('.shortcut').forEach((link) => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      if (!success.hidden) success.querySelector('.ct-again').click();
      selectSubject(link.dataset.subject);
    });
  });

  /* ---------------------------------------------------------------------
     Retour d'un envoi sans JavaScript (contact.php redirige avec ?status=)
     et lien direct avec ?subject=
     --------------------------------------------------------------------- */

  const params = new URLSearchParams(location.search);
  const returned = params.get('status');

  if (returned === 'sent') {
    form.hidden = true;
    success.hidden = false;
  } else if (returned) {
    setStatus(dict[`status.${returned}`] ? returned : 'send_failed');
  }

  if (params.get('subject')) selectSubject(params.get('subject'), false);

  if (returned) {
    params.delete('status');
    const query = params.toString();
    history.replaceState(null, '', location.pathname + (query ? `?${query}` : '') + location.hash);
  }

  /* ---------------------------------------------------------------------
     Changement de langue : on retraduit les messages en cours
     --------------------------------------------------------------------- */

  document.addEventListener('gbh:lang', (e) => {
    dict = e.detail.dict;
    form.elements.lang.value = e.detail.lang;
    Object.keys(rules).forEach((name) => {
      const code = fieldBox(name).dataset.error;
      if (code) setFieldError(name, code);
    });
    if (statusCode) statusBox.textContent = t(`status.${statusCode}`);
    submitLabel.textContent = t(sending ? 'form.sending' : 'form.submit');
  });

  updateCounter();
})();
