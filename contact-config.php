<?php
/**
 * Configuration du formulaire de contact.
 * A adapter avant la mise en ligne.
 */

return [
    // Adresse qui recoit les messages du formulaire
    'to_email' => 'contact@votre-domaine.fr',
    'to_name'  => 'GameBoxHeroes',

    // Expediteur technique : doit appartenir au domaine du site (SPF / DKIM),
    // sinon les messages risquent de finir en spam. L'adresse du visiteur
    // est placee en Reply-To.
    'from_email' => 'no-reply@votre-domaine.fr',
    'from_name'  => 'Site GameBoxHeroes',

    // Prefixe ajoute a l'objet des e-mails recus
    'subject_prefix' => '[GameBoxHeroes]',

    // Anti-abus : nombre d'envois autorises par visiteur sur la fenetre donnee
    'rate_limit'        => 3,
    'rate_window'       => 600,  // secondes
    'min_fill_seconds'  => 3,    // un humain met plus de 3 s a remplir le formulaire
];
