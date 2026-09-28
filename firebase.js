// Acces Firebase partage par l'en-tete (account.js) et la page compte (compte.js).
// Tout passe par ce module : si la configuration est vide, `configured` vaut
// false et aucune requete n'est envoyee.
import { firebaseConfig } from './firebase-config.js';

const SDK = 'https://www.gstatic.com/firebasejs/10.12.2';

export const configured = Boolean(firebaseConfig.apiKey && firebaseConfig.projectId);

let ready = null;

// Firestore reessaie longtemps quand le reseau manque : on abandonne apres 10 s
const withTimeout = (promise, ms = 10000) => Promise.race([
  promise,
  new Promise((_, reject) => setTimeout(() => reject(Object.assign(new Error('timeout'), { code: 'unavailable' })), ms))
]);

// Chargement paresseux du SDK : les pages ne le telechargent que si le compte est configure.
const load = () => {
  if (!configured) return Promise.reject(Object.assign(new Error('not-configured'), { code: 'app/not-configured' }));
  if (!ready) {
    ready = Promise.all([
      import(`${SDK}/firebase-app.js`),
      import(`${SDK}/firebase-auth.js`),
      import(`${SDK}/firebase-firestore.js`)
    ]).then(([appMod, authMod, fsMod]) => {
      const app = appMod.initializeApp(firebaseConfig);
      const auth = authMod.getAuth(app);
      const db = fsMod.getFirestore(app);
      return { auth, db, A: authMod, F: fsMod };
    });
  }
  return ready;
};

/* -------------------------------------------------------------------------
   Regles de saisie (reprises a l'identique dans firestore.rules)
   ------------------------------------------------------------------------- */

export const USERNAME_RE = /^[A-Za-z0-9_-]{3,20}$/;
export const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
export const PASSWORD_MIN = 8;

const RESERVED = new Set(['admin', 'administrateur', 'moderateur', 'moderator', 'support', 'root',
  'gamebox', 'gameboxhero', 'gameboxheroes', 'contact', 'staff', 'system']);

export const checkUsername = (v) => {
  if (!v) return 'required';
  if (v.length < 3) return 'username_short';
  if (v.length > 20) return 'username_long';
  if (!USERNAME_RE.test(v)) return 'username_chars';
  if (RESERVED.has(v.toLowerCase())) return 'username_reserved';
  return null;
};

export const checkEmail = (v) => (!v ? 'required' : v.length > 254 || !EMAIL_RE.test(v) ? 'invalid_email' : null);

export const checkPassword = (v) => {
  if (!v) return 'required';
  if (v.length < PASSWORD_MIN) return 'password_short';
  if (v.length > 128) return 'password_long';
  if (!/[A-Za-z]/.test(v) || !/\d/.test(v)) return 'password_weak';
  return null;
};

/* -------------------------------------------------------------------------
   Session
   ------------------------------------------------------------------------- */

// Appelle cb(user|null) a chaque changement de session (et une fois au demarrage).
export const watchUser = async (cb) => {
  if (!configured) { cb(null); return () => {}; }
  const { auth, A } = await load();
  return A.onAuthStateChanged(auth, cb);
};

export const signIn = async (email, password) => {
  const { auth, A } = await load();
  return A.signInWithEmailAndPassword(auth, email, password);
};

export const signOut = async () => {
  const { auth, A } = await load();
  return A.signOut(auth);
};

export const resetPassword = async (email, lang) => {
  const { auth, A } = await load();
  auth.languageCode = lang;
  return A.sendPasswordResetEmail(auth, email);
};

export const resendVerification = async (lang) => {
  const { auth, A } = await load();
  auth.languageCode = lang;
  return A.sendEmailVerification(auth.currentUser);
};

/* -------------------------------------------------------------------------
   Pseudos
   ------------------------------------------------------------------------- */

// true si le pseudo est libre. Indicatif : la garantie reelle est l'ecriture en lot.
export const isUsernameFree = async (username) => {
  const { db, F } = await load();
  const snap = await withTimeout(F.getDoc(F.doc(db, 'usernames', username.toLowerCase())));
  return !snap.exists();
};

/* -------------------------------------------------------------------------
   Inscription
   ------------------------------------------------------------------------- */

export const register = async ({ username, email, password, lang }) => {
  const { auth, db, A, F } = await load();
  const lower = username.toLowerCase();

  // 1. Compte d'authentification : Firebase refuse un e-mail deja utilise.
  const { user } = await A.createUserWithEmailAndPassword(auth, email, password);

  // 2. Reservation du pseudo + profil, dans un seul lot : tout ou rien.
  try {
    const batch = F.writeBatch(db);
    batch.set(F.doc(db, 'users', user.uid), {
      username,
      usernameLower: lower,
      email: user.email,
      lang,
      createdAt: F.serverTimestamp(),
      consentAt: F.serverTimestamp()
    });
    batch.set(F.doc(db, 'usernames', lower), { uid: user.uid });
    await batch.commit();
  } catch (err) {
    // Pseudo pris entre la verification et l'envoi : on annule le compte cree.
    await user.delete().catch(() => {});
    throw Object.assign(new Error('username-taken'), { code: err.code === 'permission-denied' ? 'app/username-taken' : err.code });
  }

  await A.updateProfile(user, { displayName: username });

  auth.languageCode = lang;
  await A.sendEmailVerification(user).catch(() => {});
  return user;
};

/* -------------------------------------------------------------------------
   Suppression du compte
   ------------------------------------------------------------------------- */

export const deleteAccount = async (password) => {
  const { auth, db, A, F } = await load();
  const user = auth.currentUser;
  if (!user) throw Object.assign(new Error('no-user'), { code: 'auth/no-current-user' });

  // Firebase exige une connexion recente pour supprimer : on redemande le mot de passe.
  await A.reauthenticateWithCredential(user, A.EmailAuthProvider.credential(user.email, password));

  const ref = F.doc(db, 'users', user.uid);
  const snap = await F.getDoc(ref);
  const lower = snap.exists() ? snap.data().usernameLower : (user.displayName || '').toLowerCase();

  const batch = F.writeBatch(db);
  batch.delete(ref);
  if (lower) batch.delete(F.doc(db, 'usernames', lower));
  await batch.commit();

  await A.deleteUser(user);
};

/* -------------------------------------------------------------------------
   Lettre d'information : newsletter/{e-mail en minuscules}
   Creation seule (regles Firestore) ; une adresse deja inscrite est refusee
   par les regles, ce qu'on traite comme un succes pour ne pas reveler
   quelles adresses sont inscrites.
   ------------------------------------------------------------------------- */

export const subscribe = async (email, lang) => {
  const { db, F } = await load();
  const lower = email.trim().toLowerCase();
  try {
    await withTimeout(F.setDoc(F.doc(db, 'newsletter', lower), { email: lower, lang, createdAt: F.serverTimestamp() }));
  } catch (err) {
    if (err.code !== 'permission-denied') throw err;
  }
};

/* -------------------------------------------------------------------------
   Codes d'erreur Firebase -> cles de traduction
   ------------------------------------------------------------------------- */

export const errorKey = (err) => {
  const code = (err && err.code) || '';
  const map = {
    'auth/invalid-credential': 'auth.err.credentials',
    'auth/invalid-login-credentials': 'auth.err.credentials',
    'auth/wrong-password': 'auth.err.credentials',
    'auth/user-not-found': 'auth.err.credentials',
    'auth/invalid-email': 'auth.err.email',
    'auth/email-already-in-use': 'auth.err.emailTaken',
    'auth/weak-password': 'auth.err.weak',
    'auth/too-many-requests': 'auth.err.tooMany',
    'auth/network-request-failed': 'auth.err.network',
    'auth/requires-recent-login': 'auth.err.recent',
    'auth/user-disabled': 'auth.err.disabled',
    'app/username-taken': 'auth.err.usernameTaken',
    'app/not-configured': 'auth.err.notConfigured',
    'unavailable': 'auth.err.network'
  };
  return map[code] || 'auth.err.generic';
};
