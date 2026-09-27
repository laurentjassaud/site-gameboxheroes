<?php
/**
 * Traitement du formulaire de contact GameBoxHeroes.
 *
 * - Appel AJAX (en-tete Accept: application/json) : repond en JSON.
 * - Envoi classique sans JavaScript : redirige vers contact.html?status=...
 *
 * Reponse JSON : { ok: bool, error?: code, fields?: { champ: code } }
 * Les codes sont traduits cote navigateur (contact-i18n.js).
 */

declare(strict_types=1);

$config = require __DIR__ . '/contact-config.php';

const SUBJECTS = ['general', 'module', 'bug', 'press'];

$wantsJson = str_contains($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json');
$lang = ($_POST['lang'] ?? '') === 'en' ? 'en' : 'fr';

/** Termine la requete avec le bon format de reponse. */
function respond(bool $ok, int $status, ?string $error = null, array $fields = []): never
{
    global $wantsJson, $lang;

    if ($wantsJson) {
        http_response_code($status);
        header('Content-Type: application/json; charset=utf-8');
        header('Cache-Control: no-store');
        $body = ['ok' => $ok];
        if ($error !== null) $body['error'] = $error;
        if ($fields) $body['fields'] = $fields;
        echo json_encode($body, JSON_UNESCAPED_UNICODE);
        exit;
    }

    $query = ['status' => $ok ? 'sent' : ($error ?? 'invalid'), 'lang' => $lang];
    header('Location: contact.html?' . http_build_query($query) . '#form', true, 303);
    exit;
}

/** Nettoie une valeur sur une ligne (protege les en-tetes mail). */
function oneLine(string $value): string
{
    return trim(preg_replace('/[\r\n\t\0]+/', ' ', $value));
}

/* ---------------------------------------------------------------------
   Controles de la requete
   --------------------------------------------------------------------- */

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    header('Allow: POST');
    respond(false, 405, 'method');
}

// Refuse les envois depuis un autre site
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($origin !== '' && parse_url($origin, PHP_URL_HOST) !== parse_url('//' . ($_SERVER['HTTP_HOST'] ?? ''), PHP_URL_HOST)) {
    respond(false, 403, 'origin');
}

// Pot de miel : champ invisible pour un humain
if (($_POST['website'] ?? '') !== '') {
    respond(true, 200); // on fait croire au robot que tout s'est bien passe
}

// Formulaire rempli trop vite (horodatage pose par le JS au chargement)
$startedAt = (int) ($_POST['t'] ?? 0);
if ($startedAt > 0 && (time() - intdiv($startedAt, 1000)) < $config['min_fill_seconds']) {
    respond(false, 400, 'spam');
}

// Limite d'envois par adresse IP (fichier dans le dossier temporaire)
$ipKey = hash('sha256', ($_SERVER['REMOTE_ADDR'] ?? 'unknown') . __DIR__);
$rateFile = sys_get_temp_dir() . '/gbh-contact-' . $ipKey . '.json';
$now = time();
$hits = is_file($rateFile) ? (json_decode((string) file_get_contents($rateFile), true) ?: []) : [];
$hits = array_values(array_filter($hits, fn ($ts) => is_int($ts) && $ts > $now - $config['rate_window']));
if (count($hits) >= $config['rate_limit']) {
    respond(false, 429, 'rate_limited');
}

/* ---------------------------------------------------------------------
   Validation des champs
   --------------------------------------------------------------------- */

$name    = oneLine((string) ($_POST['name'] ?? ''));
$email   = oneLine((string) ($_POST['email'] ?? ''));
$subject = (string) ($_POST['subject'] ?? '');
$message = trim(str_replace("\r\n", "\n", (string) ($_POST['message'] ?? '')));
$consent = ($_POST['consent'] ?? '') !== '';

$errors = [];

if ($name === '')                       $errors['name'] = 'required';
elseif (mb_strlen($name) < 2)           $errors['name'] = 'too_short';
elseif (mb_strlen($name) > 100)         $errors['name'] = 'too_long';

if ($email === '')                      $errors['email'] = 'required';
elseif (mb_strlen($email) > 254 || !filter_var($email, FILTER_VALIDATE_EMAIL)) $errors['email'] = 'invalid_email';

if (!in_array($subject, SUBJECTS, true)) $errors['subject'] = 'invalid_subject';

if ($message === '')                    $errors['message'] = 'required';
elseif (mb_strlen($message) < 10)       $errors['message'] = 'too_short';
elseif (mb_strlen($message) > 5000)     $errors['message'] = 'too_long';

if (!$consent)                          $errors['consent'] = 'consent_required';

if ($errors) {
    respond(false, 422, 'invalid', $errors);
}

/* ---------------------------------------------------------------------
   Envoi
   --------------------------------------------------------------------- */

$subjectLabels = [
    'general' => 'Question générale',
    'module'  => 'Proposition de module',
    'bug'     => 'Signalement de bug',
    'press'   => 'Presse & partenariats',
];

$mailSubject = mb_encode_mimeheader(
    sprintf('%s %s — %s', $config['subject_prefix'], $subjectLabels[$subject], $name),
    'UTF-8', 'B', "\r\n"
);

$body = implode("\n", [
    'Nouveau message depuis le formulaire de contact',
    str_repeat('-', 48),
    'Nom     : ' . $name,
    'E-mail  : ' . $email,
    'Sujet   : ' . $subjectLabels[$subject],
    'Langue  : ' . strtoupper($lang),
    'Date    : ' . date('d/m/Y H:i'),
    str_repeat('-', 48),
    '',
    $message,
    '',
]);

$fromName = mb_encode_mimeheader($config['from_name'], 'UTF-8', 'B', "\r\n");
$replyName = mb_encode_mimeheader($name, 'UTF-8', 'B', "\r\n");

$headers = implode("\r\n", [
    'From: ' . $fromName . ' <' . $config['from_email'] . '>',
    'Reply-To: ' . $replyName . ' <' . $email . '>',
    'MIME-Version: 1.0',
    'Content-Type: text/plain; charset=UTF-8',
    'Content-Transfer-Encoding: 8bit',
    'X-Mailer: GameBoxHeroes contact form',
]);

$to = $config['to_name'] !== ''
    ? mb_encode_mimeheader($config['to_name'], 'UTF-8', 'B', "\r\n") . ' <' . $config['to_email'] . '>'
    : $config['to_email'];

// -f fixe l'enveloppe (Return-Path) sur l'expediteur du domaine
$sent = mail($to, $mailSubject, $body, $headers, '-f' . $config['from_email']);

if (!$sent) {
    error_log('[contact] mail() a echoue pour ' . $config['to_email']);
    respond(false, 500, 'send_failed');
}

$hits[] = $now;
@file_put_contents($rateFile, json_encode($hits), LOCK_EX);

respond(true, 200);
