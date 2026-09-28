# Texte des mentions legales et de la politique de confidentialite (FR / EN),
# insere dans mentions-legales.html par tools/gen_static.py.
#
# Les passages entre <mark class="todo">[...]</mark> sont a completer par
# l'editeur du site avant la mise en ligne (ils sont surlignes sur la page).

UPDATED_FR = '28 septembre 2026'
UPDATED_EN = '28 September 2026'


def todo(text):
    return f'<mark class="todo">[{text}]</mark>'


LEGAL_FR = f'''      <p class="legal__updated">Dernière mise à jour&nbsp;: {UPDATED_FR}</p>

      <h2 class="legal__part">Mentions légales</h2>
      <p>Conformément à l’article 6-III de la loi n° 2004-575 du 21 juin 2004 pour la confiance dans l’économie numérique (LCEN), il est précisé aux utilisateurs du site GameBoxHeroes l’identité des différents intervenants dans le cadre de sa réalisation et de son suivi.</p>

      <h3 id="editeur">1. Éditeur du site</h3>
      <ul>
        <li><strong>Nom / raison sociale&nbsp;:</strong> {todo('Votre nom, ou dénomination sociale si société')}</li>
        <li><strong>Statut&nbsp;:</strong> {todo('Particulier / Entrepreneur individuel / Micro-entrepreneur / SASU…')}</li>
        <li><strong>N° SIREN / SIRET&nbsp;:</strong> {todo('si applicable')}</li>
        <li><strong>Adresse&nbsp;:</strong> {todo('Adresse postale ou siège social')}</li>
        <li><strong>Contact&nbsp;:</strong> {todo('Adresse e-mail de contact')} ou via la page <a href="contact.html">Contact</a></li>
        <li><strong>Directeur de la publication&nbsp;:</strong> {todo('Nom')}</li>
      </ul>

      <h3 id="hebergement">2. Hébergement</h3>
      <ul>
        <li><strong>Hébergeur du site&nbsp;:</strong> {todo('Nom de l’hébergeur, ex. OVH, IONOS…')}</li>
        <li><strong>Adresse&nbsp;:</strong> {todo('Adresse de l’hébergeur')}</li>
        <li><strong>Contact&nbsp;:</strong> {todo('Téléphone / site web de l’hébergeur')}</li>
      </ul>
      <p>Les comptes joueurs et la lettre d’information reposent sur <strong>Firebase</strong> (Firebase Authentication et Cloud Firestore), service fourni par Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irlande.</p>

      <h3 id="propriete">3. Propriété intellectuelle</h3>
      <p>L’ensemble des éléments constituant le site GameBoxHeroes (textes, illustrations, logos, modules de jeu, moteurs de jeu, mise en page, code source) est protégé par le droit de la propriété intellectuelle. Toute reproduction, représentation, modification, publication, adaptation totale ou partielle des éléments du site, quel que soit le moyen ou le procédé utilisé, est interdite sans autorisation écrite préalable de l’éditeur.</p>
      <p>Les règles, cartes, pions, couvertures et références aux jeux originaux adaptés en modules restent la propriété de leurs éditeurs et ayants droit respectifs&nbsp;; GameBoxHeroes n’en revendique aucune propriété. Les visuels de jeux publiés sur le site le sont dans un but illustratif uniquement.</p>

      <h3 id="responsabilite">4. Responsabilité</h3>
      <p>L’éditeur s’efforce d’assurer l’exactitude et la mise à jour des informations diffusées sur le site, mais ne saurait garantir l’exhaustivité ou l’absence d’erreur. L’éditeur ne pourra être tenu responsable des dommages directs ou indirects résultant de l’accès ou de l’utilisation du site.</p>
      <p>Chaque joueur est responsable de la confidentialité de son mot de passe et de l’usage de son compte. Le pseudo choisi ne doit pas porter atteinte aux droits de tiers ni être injurieux&nbsp;; l’éditeur peut suspendre ou supprimer un compte qui ne respecterait pas cette règle.</p>

      <h3 id="droit">5. Droit applicable</h3>
      <p>Les présentes mentions légales sont soumises au droit français. En cas de litige et à défaut de résolution amiable, les tribunaux français seront seuls compétents.</p>

      <h2 class="legal__part" id="confidentialite">Politique de confidentialité</h2>
      <p>GameBoxHeroes («&nbsp;nous&nbsp;», «&nbsp;le site&nbsp;») attache une grande importance à la protection de vos données personnelles. Cette politique explique quelles données sont collectées, pourquoi, et comment vous pouvez exercer vos droits, conformément au Règlement général sur la protection des données (RGPD) et à la loi Informatique et Libertés.</p>

      <h3 id="responsable">1. Responsable du traitement</h3>
      <p>{todo('Votre nom / raison sociale')}, joignable à l’adresse {todo('e-mail de contact')}, est responsable du traitement des données collectées sur ce site.</p>

      <h3 id="donnees">2. Données collectées et finalités</h3>

      <h4 id="contact-form">a) Formulaire de contact</h4>
      <p>Lorsque vous utilisez le formulaire de contact, nous collectons&nbsp;: votre nom, votre adresse e-mail, le sujet et le contenu de votre message. Ces informations nous sont transmises par e-mail&nbsp;; elles ne sont pas enregistrées dans une base de données du site.</p>
      <ul>
        <li><strong>Finalité&nbsp;:</strong> répondre à votre demande.</li>
        <li><strong>Base légale&nbsp;:</strong> intérêt légitime à répondre aux sollicitations des utilisateurs.</li>
        <li><strong>Durée de conservation&nbsp;:</strong> le temps nécessaire au traitement de la demande, puis suppression, sauf échange se poursuivant dans la durée.</li>
      </ul>

      <h4 id="newsletter">b) Lettre d’information</h4>
      <p>Lorsque vous vous inscrivez à la lettre d’information (formulaire «&nbsp;Rester au courant de l’avancement des projets&nbsp;» en bas de page), nous collectons&nbsp;: votre adresse e-mail, la langue du site au moment de l’inscription et la date d’inscription.</p>
      <ul>
        <li><strong>Finalité&nbsp;:</strong> vous tenir informé de l’actualité de GameBoxHeroes (nouveaux modules, fonctionnalités, avancement du projet).</li>
        <li><strong>Base légale&nbsp;:</strong> votre consentement, donné en cochant la case prévue. Vous pouvez le retirer à tout moment via le lien de désinscription présent dans chaque e-mail, ou en nous contactant.</li>
        <li><strong>Durée de conservation&nbsp;:</strong> jusqu’à votre désinscription, ou 3 ans après le dernier contact en l’absence d’activité.</li>
      </ul>

      <h4 id="compte">c) Création et gestion d’un compte joueur</h4>
      <p>La création d’un compte est facultative&nbsp;: le site reste consultable sans compte. Lorsque vous créez un compte, nous collectons&nbsp;:</p>
      <ul>
        <li>votre <strong>pseudo</strong>, unique sur le site et <strong>visible des autres joueurs</strong>&nbsp;;</li>
        <li>votre <strong>adresse e-mail</strong>, unique elle aussi, qui sert d’identifiant de connexion et n’est jamais affichée publiquement&nbsp;;</li>
        <li>votre <strong>mot de passe</strong>, que nous ne voyons jamais&nbsp;: il est transmis de façon chiffrée puis stocké sous forme hachée par Firebase Authentication&nbsp;;</li>
        <li>la <strong>langue</strong> choisie, la <strong>date de création</strong> du compte et la <strong>date de votre acceptation</strong> de la présente politique&nbsp;;</li>
        <li>l’état de vérification de votre adresse e-mail et les dates de connexion&nbsp;;</li>
        <li>au fur et à mesure de l’ouverture des fonctionnalités&nbsp;: les données liées à votre activité sur le site (parties en cours, progression, historique de jeu).</li>
      </ul>
      <p>Avant la création du compte, un récapitulatif des informations saisies vous est présenté pour vérification, et votre accord explicite vous est demandé. Un e-mail de vérification est ensuite envoyé à l’adresse indiquée&nbsp;; un e-mail de réinitialisation peut également vous être envoyé si vous déclarez avoir oublié votre mot de passe.</p>
      <ul>
        <li><strong>Finalités&nbsp;:</strong> création et gestion de votre compte, authentification, sauvegarde de votre progression entre vos sessions et vos appareils, accès aux fonctionnalités multijoueur, sécurité du service (prévention des abus et des doublons de pseudo ou d’e-mail).</li>
        <li><strong>Base légale&nbsp;:</strong> exécution du service que vous avez demandé (article 6.1.b du RGPD)&nbsp;; intérêt légitime pour la sécurité du service.</li>
        <li><strong>Durée de conservation&nbsp;:</strong> pendant toute la durée de vie du compte. Vous pouvez supprimer votre compte à tout moment depuis le bouton compte en haut de chaque page («&nbsp;Supprimer mon compte&nbsp;»)&nbsp;: votre profil, votre pseudo, votre adresse e-mail et vos données de jeu sont alors effacés immédiatement et définitivement. Un compte inactif est supprimé {todo('délai à préciser, ex. 3 ans')} après la dernière connexion, après un e-mail d’avertissement.</li>
      </ul>

      <h4 id="journaux">d) Données techniques</h4>
      <p>Pour assurer la sécurité et le bon fonctionnement du service, nos prestataires techniques (hébergeur, Firebase) enregistrent des journaux de connexion (adresse IP, date et heure, type de navigateur). Ces journaux sont conservés pour une durée limitée, conformément aux engagements de ces prestataires.</p>

      <h3 id="destinataires">3. Destinataires des données</h3>
      <p>Vos données ne sont ni vendues, ni cédées à des tiers à des fins commerciales. Elles sont accessibles uniquement à l’éditeur et aux prestataires techniques strictement nécessaires au fonctionnement du site, agissant en qualité de sous-traitants&nbsp;:</p>
      <ul>
        <li>l’hébergeur du site ({todo('nom de l’hébergeur')})&nbsp;;</li>
        <li><strong>Google Ireland Limited (Firebase)</strong>, pour l’authentification, la base de données des comptes et des inscriptions à la lettre d’information, et l’envoi des e-mails de vérification et de réinitialisation de mot de passe. Les données sont hébergées dans la région {todo('région Firestore choisie, ex. europe-west1 (Belgique)')}. Certaines opérations peuvent impliquer un transfert vers Google LLC aux États-Unis&nbsp;; ce transfert est encadré par le cadre de protection des données UE–États-Unis (Data Privacy Framework) et par les clauses contractuelles types de la Commission européenne&nbsp;;</li>
        <li>{todo('le cas échéant : outil d’envoi de la lettre d’information (Brevo, Mailchimp…) et garanties de transfert s’il est hébergé hors UE')}.</li>
      </ul>
      <p>Seul votre pseudo est visible des autres joueurs.</p>

      <h3 id="cookies">4. Cookies et stockage local</h3>
      <p>Le site GameBoxHeroes ne dépose aucun cookie de suivi, de mesure d’audience ou publicitaire.</p>
      <p>Le site utilise le stockage de votre navigateur (localStorage et IndexedDB) uniquement pour des besoins strictement nécessaires au service que vous utilisez&nbsp;:</p>
      <ul>
        <li>mémoriser la <strong>langue</strong> choisie (français ou anglais)&nbsp;;</li>
        <li>maintenir votre <strong>session de connexion</strong> si vous avez un compte (jeton d’authentification Firebase), effacée lorsque vous vous déconnectez&nbsp;;</li>
        <li>enregistrer votre progression de jeu et vos préférences directement sur votre appareil.</li>
      </ul>
      <p>Ces éléments ne servent pas à vous suivre et ne nécessitent pas votre consentement préalable, conformément aux lignes directrices de la CNIL sur les traceurs strictement nécessaires.</p>
      <p>Les polices de caractères du site sont chargées depuis le service Google Fonts&nbsp;: à cette occasion, votre adresse IP est transmise à Google. {todo('Supprimer cette phrase si les polices sont hébergées directement sur le site.')}</p>

      <h3 id="droits">5. Vos droits</h3>
      <p>Conformément au RGPD, vous disposez d’un droit d’accès, de rectification, d’effacement, de limitation, d’opposition et de portabilité sur vos données, ainsi que du droit de retirer votre consentement à tout moment pour les traitements qui en dépendent (lettre d’information).</p>
      <ul>
        <li><strong>Effacement&nbsp;:</strong> vous pouvez supprimer vous-même votre compte à tout moment, depuis le bouton compte en haut de page.</li>
        <li><strong>Accès, rectification, portabilité&nbsp;:</strong> écrivez-nous à l’adresse {todo('e-mail de contact')} ou depuis la page <a href="contact.html">Contact</a>. Le pseudo ne pouvant pas être modifié depuis le site, nous pouvons le corriger sur demande.</li>
      </ul>
      <p>Nous répondons dans un délai d’un mois. Vous disposez également du droit d’introduire une réclamation auprès de la CNIL (<a href="https://www.cnil.fr" rel="noopener" target="_blank">www.cnil.fr</a>) si vous estimez que vos droits ne sont pas respectés.</p>

      <h3 id="mineurs">6. Mineurs</h3>
      <p>La création d’un compte est réservée aux personnes âgées d’au moins 15 ans. En dessous de cet âge, l’accord d’un titulaire de l’autorité parentale est nécessaire&nbsp;; celui-ci peut demander la suppression du compte à tout moment.</p>

      <h3 id="securite">7. Sécurité</h3>
      <p>Nous mettons en œuvre les mesures techniques et organisationnelles raisonnables pour protéger vos données contre toute perte, accès non autorisé, divulgation ou destruction&nbsp;: connexion chiffrée (HTTPS), mots de passe hachés et jamais accessibles à l’éditeur, règles d’accès à la base de données limitant chaque joueur à ses propres informations, unicité des pseudos et des adresses e-mail contrôlée côté serveur.</p>

      <h3 id="modifications">8. Modifications</h3>
      <p>Cette politique peut évoluer, notamment à l’ouverture de nouvelles fonctionnalités. La date de dernière mise à jour figure en haut de cette page&nbsp;; en cas de changement important, les titulaires d’un compte en seront informés par e-mail.</p>'''


LEGAL_EN = f'''      <p class="legal__updated">Last updated: {UPDATED_EN}</p>
      <p class="legal__note">This English version is provided for convenience. The French version is the legally binding one.</p>

      <h2 class="legal__part">Legal notice</h2>
      <p>In accordance with article 6-III of French law no. 2004-575 of 21 June 2004 on confidence in the digital economy (LCEN), users of the GameBoxHeroes website are informed of the identity of the parties involved in creating and running it.</p>

      <h3 id="editeur-en">1. Publisher</h3>
      <ul>
        <li><strong>Name / company name:</strong> {todo('Your name, or company name')}</li>
        <li><strong>Status:</strong> {todo('Individual / sole trader / company…')}</li>
        <li><strong>SIREN / SIRET no.:</strong> {todo('if applicable')}</li>
        <li><strong>Address:</strong> {todo('Postal address or registered office')}</li>
        <li><strong>Contact:</strong> {todo('Contact email')} or through the <a href="contact.html">Contact</a> page</li>
        <li><strong>Publication director:</strong> {todo('Name')}</li>
      </ul>

      <h3 id="hebergement-en">2. Hosting</h3>
      <ul>
        <li><strong>Website host:</strong> {todo('Host name, e.g. OVH, IONOS…')}</li>
        <li><strong>Address:</strong> {todo('Host address')}</li>
        <li><strong>Contact:</strong> {todo('Host phone / website')}</li>
      </ul>
      <p>Player accounts and the newsletter run on <strong>Firebase</strong> (Firebase Authentication and Cloud Firestore), provided by Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Ireland.</p>

      <h3 id="propriete-en">3. Intellectual property</h3>
      <p>All elements of the GameBoxHeroes website (texts, illustrations, logos, game modules, game engines, layout, source code) are protected by intellectual property law. Any reproduction, representation, modification, publication or adaptation of all or part of the site, by any means, is forbidden without the publisher’s prior written permission.</p>
      <p>The rules, maps, counters, covers and references to the original games adapted as modules remain the property of their respective publishers and rights holders; GameBoxHeroes claims no ownership of them. Game visuals shown on the site are for illustration only.</p>

      <h3 id="responsabilite-en">4. Liability</h3>
      <p>The publisher strives to keep the information on the site accurate and up to date, but cannot guarantee it is complete or error-free. The publisher cannot be held liable for any direct or indirect damage resulting from access to or use of the site.</p>
      <p>Each player is responsible for keeping their password confidential and for the use of their account. Usernames must not infringe third-party rights or be offensive; the publisher may suspend or delete an account that breaks this rule.</p>

      <h3 id="droit-en">5. Governing law</h3>
      <p>This legal notice is governed by French law. In the event of a dispute, and failing an amicable settlement, the French courts have sole jurisdiction.</p>

      <h2 class="legal__part" id="confidentialite-en">Privacy policy</h2>
      <p>GameBoxHeroes (“we”, “the site”) takes the protection of your personal data seriously. This policy explains what data is collected, why, and how you can exercise your rights, in accordance with the General Data Protection Regulation (GDPR) and the French Data Protection Act.</p>

      <h3 id="responsable-en">1. Data controller</h3>
      <p>{todo('Your name / company name')}, reachable at {todo('contact email')}, is the controller of the data collected on this site.</p>

      <h3 id="donnees-en">2. Data collected and purposes</h3>

      <h4 id="contact-form-en">a) Contact form</h4>
      <p>When you use the contact form, we collect your name, email address, subject and message. This information is sent to us by email; it is not stored in a database on the site.</p>
      <ul>
        <li><strong>Purpose:</strong> replying to your request.</li>
        <li><strong>Legal basis:</strong> legitimate interest in answering users’ requests.</li>
        <li><strong>Retention:</strong> as long as needed to handle the request, then deleted, unless the conversation continues.</li>
      </ul>

      <h4 id="newsletter-en">b) Newsletter</h4>
      <p>When you sign up for the newsletter (the “Keep up with the projects” form at the bottom of each page), we collect your email address, the site language at the time and the sign-up date.</p>
      <ul>
        <li><strong>Purpose:</strong> keeping you informed about GameBoxHeroes (new modules, features, project progress).</li>
        <li><strong>Legal basis:</strong> your consent, given by ticking the box. You can withdraw it at any time through the unsubscribe link in every email, or by contacting us.</li>
        <li><strong>Retention:</strong> until you unsubscribe, or 3 years after the last contact if there is no activity.</li>
      </ul>

      <h4 id="compte-en">c) Creating and managing a player account</h4>
      <p>Creating an account is optional: the site can be browsed without one. When you create an account, we collect:</p>
      <ul>
        <li>your <strong>username</strong>, unique on the site and <strong>visible to other players</strong>;</li>
        <li>your <strong>email address</strong>, also unique, used as your sign-in identifier and never shown publicly;</li>
        <li>your <strong>password</strong>, which we never see: it is sent encrypted, then stored in hashed form by Firebase Authentication;</li>
        <li>your chosen <strong>language</strong>, the account <strong>creation date</strong> and the <strong>date you accepted</strong> this policy;</li>
        <li>whether your email address is verified, and your sign-in dates;</li>
        <li>as features open up: data about your activity on the site (games in progress, progress, game history).</li>
      </ul>
      <p>Before the account is created, a summary of the details you entered is shown for review, and your explicit agreement is requested. A verification email is then sent to the address given; a reset email may also be sent if you report a forgotten password.</p>
      <ul>
        <li><strong>Purposes:</strong> creating and managing your account, authentication, saving your progress across sessions and devices, multiplayer features, service security (preventing abuse and duplicate usernames or emails).</li>
        <li><strong>Legal basis:</strong> performance of the service you requested (GDPR article 6.1.b); legitimate interest for service security.</li>
        <li><strong>Retention:</strong> for as long as the account exists. You can delete your account at any time from the account button at the top of every page (“Delete my account”): your profile, username, email address and game data are then erased immediately and permanently. Inactive accounts are deleted {todo('period to specify, e.g. 3 years')} after the last sign-in, following a warning email.</li>
      </ul>

      <h4 id="journaux-en">d) Technical data</h4>
      <p>To keep the service secure and running, our technical providers (host, Firebase) record connection logs (IP address, date and time, browser type). These logs are kept for a limited time, in line with these providers’ commitments.</p>

      <h3 id="destinataires-en">3. Recipients</h3>
      <p>Your data is never sold or shared with third parties for commercial purposes. It is only accessible to the publisher and to the technical providers strictly needed to run the site, acting as processors:</p>
      <ul>
        <li>the website host ({todo('host name')});</li>
        <li><strong>Google Ireland Limited (Firebase)</strong>, for authentication, the database of accounts and newsletter sign-ups, and sending verification and password reset emails. Data is hosted in the {todo('chosen Firestore region, e.g. europe-west1 (Belgium)')} region. Some operations may involve a transfer to Google LLC in the United States; this transfer is covered by the EU–US Data Privacy Framework and the European Commission’s standard contractual clauses;</li>
        <li>{todo('if applicable: newsletter tool (Brevo, Mailchimp…) and transfer safeguards if hosted outside the EU')}.</li>
      </ul>
      <p>Only your username is visible to other players.</p>

      <h3 id="cookies-en">4. Cookies and local storage</h3>
      <p>The GameBoxHeroes website sets no tracking, analytics or advertising cookies.</p>
      <p>The site uses your browser’s storage (localStorage and IndexedDB) only for what is strictly necessary for the service you are using:</p>
      <ul>
        <li>remembering your chosen <strong>language</strong> (French or English);</li>
        <li>keeping you <strong>signed in</strong> if you have an account (Firebase authentication token), cleared when you sign out;</li>
        <li>saving your game progress and preferences directly on your device.</li>
      </ul>
      <p>These items are not used to track you and do not require your prior consent, in line with the CNIL guidelines on strictly necessary trackers.</p>
      <p>The site’s fonts are loaded from Google Fonts: in doing so, your IP address is sent to Google. {todo('Remove this sentence if the fonts are self-hosted.')}</p>

      <h3 id="droits-en">5. Your rights</h3>
      <p>Under the GDPR, you have the right to access, rectify, erase, restrict, object to and port your data, and to withdraw your consent at any time for processing based on it (newsletter).</p>
      <ul>
        <li><strong>Erasure:</strong> you can delete your account yourself at any time, from the account button at the top of the page.</li>
        <li><strong>Access, rectification, portability:</strong> write to {todo('contact email')} or use the <a href="contact.html">Contact</a> page. Usernames cannot be changed from the site, but we can correct yours on request.</li>
      </ul>
      <p>We reply within one month. You also have the right to lodge a complaint with the CNIL, the French data protection authority (<a href="https://www.cnil.fr" rel="noopener" target="_blank">www.cnil.fr</a>), if you believe your rights are not being respected.</p>

      <h3 id="mineurs-en">6. Minors</h3>
      <p>Accounts are for people aged 15 or over. Below that age, the permission of a person with parental authority is required; they may ask for the account to be deleted at any time.</p>

      <h3 id="securite-en">7. Security</h3>
      <p>We take reasonable technical and organisational measures to protect your data against loss, unauthorised access, disclosure or destruction: encrypted connection (HTTPS), hashed passwords never accessible to the publisher, database access rules restricting each player to their own information, and server-side checks that usernames and email addresses are unique.</p>

      <h3 id="modifications-en">8. Changes</h3>
      <p>This policy may change, in particular as new features open. The date of the last update is shown at the top of this page; account holders will be informed by email of any significant change.</p>'''
