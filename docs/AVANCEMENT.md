# Avancement du projet UCIV

Point de reprise : ce qui est fait, ce qui ne l'est pas, et par où continuer.
Dernière mise à jour : 20 octobre 2026.

Documents liés : [PLAN.md](PLAN.md) (ce qu'il faut construire),
[ARCHITECTURE.md](ARCHITECTURE.md) (structure), [CLAUDE.md](../CLAUDE.md) (règles agents),
[CONTRIBUTING.md](../CONTRIBUTING.md) (workflow).

## État en un coup d'œil

| Domaine | État |
|---|---|
| Structure du projet (`src/core`, `src/app`) | Fait |
| Dépendances | Fait : Django 6.1.2 et Pillow 13.0.0 (images) |
| Page d'accueil | Faite, alignée sur la maquette |
| Pages intérieures (17) | **17 faites** : les 14 précédentes + « De la vision à l'action », « Les RH ont la parole » (programmes d'UCIV Leadership) et Rechercher |
| Pages légales et 404 | **Faites** (desktop et mobile) : mentions légales, politique de confidentialité, conditions d'utilisation, page introuvable |
| Modèles de données et administration | 8 modèles administrables : `Abonne` (lettre d'information), 3 de formulaires (`SoumissionEngagement`, `SoumissionPartenariat`, `SoumissionContact`) et 4 de contenu (`Article`, `Opportunite`, `Ressource`, `Indicateur`) ; `MembreEquipe`, `Programme` et `Partenaire` restent dans `content.py` |
| Formulaires | 4 faits : engagement, partenariat, contact, lettre d'information (pied de page) |
| Responsive mobile (390 px) | **Fait pour les 15 pages**, aligné sur les écrans « … — Mobile » de la maquette ; tablette déduite (720–1099 px) |
| Dashboard de l'équipe | **Maquette faite et validée** (desktop et mobile, branche `feature/dashboard`) ; implémentation pas commencée |
| Documentation | Faite (voir ci-dessus) |
| Mise en ligne | **En ligne sur https://uciv.org** (19 octobre 2026) ; compte administrateur et durcissement du serveur à faire |

## Ce qui est fait


### Partenaires : visages visibles dans le bandeau (21 octobre 2026)
- La photo du bandeau (`partenariat-paipro`, un portrait dont les visages sont en haut) était recadrée au centre : en cercle (bureau, tablette) comme en rectangle (mobile), le haut des têtes était coupé et, sur téléphone, le visage de l'homme à droite sortait du cadre. `object-position: center top` : les deux visages sont entiers à 1440, 1100, 768 et 390 px. Test `BandeauPartenairesTests`.

### Cache du navigateur : adresses statiques avec empreinte (21 octobre 2026)
- **Problème en production** : Nginx garde les fichiers statiques 30 jours dans le navigateur et `main.css` gardait le même nom après chaque mise en ligne. Un visiteur déjà venu recevait le nouveau HTML avec l'ancien CSS : style incomplet, formes du logo absentes. Un navigateur neuf affichait le site correctement.
- **Correctif** : `core/storage.py` (`StatiqueAvecEmpreinte`, déclaré dans `STORAGES` de `settings.py`) ajoute `?v=<empreinte du contenu>` à chaque `{% static %}` : l'adresse change dès que le fichier change, donc le navigateur recharge. Aucune configuration Nginx à toucher. Limite : les `url()` écrits dans le CSS lui-même (masque `forme-uciv.svg`, polices) ne sont pas versionnés.
- Tests : `StatiqueAvecEmpreinteTests`.

### Boutons du bandeau d'accueil (21 octobre 2026)
- **Forme du logo dans les sections** : les anneaux et demi-cercles décoratifs des sections prennent la forme du logo des bandeaux (`forme-uciv.svg` en masque CSS, section 29 de `main.css`) : appels à l'action (`np-appel__anneau`), vision de l'accueil, inscriptions Go du Digital / Experience Lab / programmes Leadership, cartes de Notre impact, coordonnées du contact, « Une question ? » des pages légales et « Pourquoi rejoindre » de Leadership. Même position et même teinte qu'avant, forme pleine au lieu d'un anneau. Également : la carte « Notre vision » et la citation de Qui sommes-nous ? (et de Notre impact), anneaux posés en `::before`. Les anciens anneaux `::before` des bandeaux en mobile (Opportunités, Engagement, Partenaires, Go du Digital, Contact, article) doublaient la forme du logo : supprimés. Non modifiés : les pages d'erreur (404, 429, désinscription). Test `FormeLogoSectionsTests`.
- Accueil, section « Nos programmes » : la carte UCIV Leadership utilise la photo de couverture détourée `leadership-couverture` (quatre membres du réseau, fond transparent sur le jaune de la carte) à la place de `groupe-nb`. Test `CarteLeadershipAccueilTests`.
- **Correctif** : sur grand écran, le bloc décoratif de la photo (`.hero__visuel`) recouvrait tout le bandeau et avalait les clics : les deux boutons ne s'ouvraient pas. Il ne capte plus les clics (`pointer-events: none`) et le texte passe au-dessus (`z-index: 2`). Vérifié par un clic réel dans Chrome à 1920, 1536, 1440, 1280, 1100, 768 et 390 px, et aucun lien bloqué sur les 16 pages principales.
- « Je veux m'engager » mène à la page `/engagement/` ; « Découvrir UCIV » mène à `/qui-sommes-nous/` (il ne faisait que défiler vers la section « Pourquoi UCIV ? » de l'accueil). Test `BoutonsHeroAccueilTests`.
- UCIV Leadership : « Découvrir nos programmes » du bandeau défile vers la section « Les programmes d'UCIV Leadership » (`#programmes-du-reseau`) au lieu d'ouvrir la page Nos programmes. Test `BoutonProgrammesLeadershipTests`.

### Cadrage des images d'articles (21 octobre 2026)
- Les cartes et les pages d'article recadraient toutes les photos au centre, ce qui coupait des visages. Le modèle `Article` a un nouveau champ **`image_position`** (valeur de `object-position`, « center » par défaut, validée : mots-clés ou pourcentages seulement), modifiable dans l'administration (section Image, « Cadrage de l'image »).
- Il est appliqué partout : cartes d'actualités, article à la une, cartes de l'accueil, « Nos histoires » et image de la page de l'article.
- Migration `0014_cadrage_images_articles` : ajoute le champ et règle chaque photo existante (PAIPRO `center 10%`, affiche jaune `center 35%`, rencontre `center 25%`, Go du Digital et Experience Lab `60% center`, volontaires `center 56%`), sans écraser un cadrage déjà choisi.
- Tests : `CadrageImagesTests` (cadrages posés, rendu dans les cartes, l'accueil et l'article, valeurs refusées).

### Leticia BOSSON dans Notre impact et dans les actualités (21 octobre 2026)
- **Notre impact, « Nos histoires »** : la carte de la lauréate montre la photo de Leticia BOSSON et son nom dans la description (« Leticia BOSSON, lauréate des Go du Digital : … » à la place de « [Nom de la lauréate] »). Migration `0012_laureate_nom_dans_la_description`.
- **Actualités** : l'article « La Reine du Digital » devient « … : le parcours de Leticia BOSSON », avec sa photo, son nom et son témoignage (migration `0013_actualite_laureate`). Le lien de l'article ne change pas. Les deux migrations ne touchent que les articles non retravaillés depuis l'administration.
- Les deux autres histoires (volontaire, participant) gardent leurs textes d'attente.

### Lancement d'UCIV Leadership : deux affiches (20 octobre 2026)
- La section « Lancement » affiche deux affiches qui se chevauchent comme dans la maquette : `affiche-leadership-orange` à gauche (inclinée de +4°) et `affiche-leadership-jaune` par-dessus à droite (−3°), coins arrondis, cotes de la maquette en bureau (cadre 520 × 420) et en mobile (350 × 283). La maquette montre une affiche « sauge » à la place de la jaune : elle n'a pas été fournie.
- Base du travail : la branche `feature/maj-client-octobre` (mise à jour d'octobre d'UCIV : recherche, galerie, témoignages, nouvelles photos), avancée en local dans `main`. Mon travail local antérieur (chiffres, photos, équipe) est conservé dans le stash `travail-local-avant-base-maj-client-octobre`, la branche faisant la même chose.

### Mise à jour d'octobre 2026 (consignes UCIV, branche `feature/maj-client-octobre`)
Consignes du client : `UCIV/info/uciv_update.md` ; maquette mise à jour (copie dans `maquette/design_uciv.pen`).
- **Forme UCIV** : la forme du logo remplace les cercles de tous les heros. Positions de la maquette dans
  `content.FORMES_HEROS`, rendues par la balise `{% formes_hero 'cle' %}` (`includes/_formes_uciv.html`, masque
  `img/forme-uciv.svg`, CSS section 27). Les anciens cercles des heros sont retirés des gabarits.
- **Chiffres clés** : champ `Indicateur.prefixe` (migration `0010`, « + » de « +1 800 », modifiable dans l'administration)
  et valeurs remplies par la migration `0011` (seulement si encore vides). Mention « en cours de consolidation » masquée
  quand tous les chiffres sont renseignés.
- **Leticia BOSSON** : lauréate mise en avant sur Les Go du Digital et première histoire de Notre impact (migration `0011`,
  uniquement si l'histoire n'avait pas été rédigée).
- **Couvertures** : accueil (photo détourée), Go du Digital, Experience Lab, UCIV Leadership (avec la plaque du logo
  sur fond vert profond, proposition à valider par Marshall) ; vraies photos sur les cartes programme.
- **Témoignages** (`includes/_temoignages.html`) sur chaque page programme ; la section ne s'affiche que si un
  témoignage est renseigné dans `content.py` (aujourd'hui : Leticia seulement). **Galerie** « En images » sur Go du Digital.
- **Programmes d'UCIV Leadership** : 2 pages (`programme_leadership.html`, URL `vision_action` et `rh_parole`), section
  sur la page Leadership, liens « Au sein du réseau » sur Nos programmes, menu (en retrait) et pied de page, SEO, FAQ.
- **Partenaires** : photo de la collaboration et nom en dessous (accueil et page Partenaires).
- **Équipe** : biographie de Marshall Kouamé, nouveaux portraits, groupes Bureau exécutif (5), Responsables (10),
  Ambassadrices (2). L'ancienne liste « Médias & communication » est retirée.
- **Liens** : plus aucun lien `#` (recherche de l'en-tête → page Rechercher, « Découvrir UCIV » → Qui sommes-nous,
  « S'inscrire » des programmes → formulaire de contact objet « Programme », fiches sans lien sans bouton).
  Test `test_no_dead_links` : chaque lien interne des pages répond.
- **Actualités** : photos cadrées vers le haut pour garder les visages.
- Images : originaux dans `sources/images/`, WebP générés par `outils/convertir_images.py` (+ 2 images de partage).
- 11 tests ajoutés (174 au total).
- **Heros alignés sur la maquette** (desktop 1440 et mobile 390) : hauteurs, positions, tailles de texte, photos, logo
  Leadership et textes manuscrits relevés dans la maquette et vérifiés au pixel près (mesures puppeteer). À partir de 1100 px,
  les heros reprennent la maquette à l'échelle de l'écran (`--u`, CSS sections 29 et 30).


### Projet
- Structure `django-init` : `src/core` (réglages, URLs, utilitaires) et `src/app` (contenu éditorial), gabarits dans `src/templates/app/`, statiques dans `src/static/app/assets/`.
- Dépendances : Django, puis Pillow (ajouté pour le traitement des images). Les réglages lisent `os.environ` (pas de fichier `.env` chargé automatiquement).
- L'historique git a été nettoyé : `main` contient 2 commits propres et est synchronisé avec `origin/main`.

### Page d'accueil (`/`)
- 12 blocs : bandeau d'annonce, en-tête (menu déroulant et menu mobile), hero, manifeste, engagement en expérience, domaines d'action, programmes, vision et chiffres, rejoindre UCIV, fondateur, actualités, partenaires, pied de page.
- Contenu dans `src/app/content.py`, variables communes (navigation, pied de page) via `app/context_processors.py`.
- 2 tests (`python manage.py test app`) : la page répond et affiche les contenus clés.
- Comparée à la maquette : textes, ordre, palette et polices identiques ; tailles de titres corrigées (programmes 52 px, vision et fondateur 48 px, partenaires 46 px).

### Page UCIV Leadership (`/programmes/uciv-leadership/`)
- 8 sections : hero (fil d'Ariane, logo, photo), repères, vision et mission, intégrer le réseau (4 étapes), pourquoi rejoindre, principes (5), thème, lancement.
- Contenu dans `content.LEADERSHIP` ; vue `uciv_leadership` ; gabarit `layout/uciv_leadership.html` ; styles `lead-*` dans `main.css` (section 12).
- Les liens « UCIV Leadership » (bandeau, navigation, pied de page, carte programme de l'accueil) pointent vers la page.
- Lancement d'UCIV Leadership : **24 octobre 2026**, à l'American Corner ; l'heure reste à confirmer (bandeau d'annonce, repères, section « Lancement » et article TEDx). L'affiche du lancement indique encore « octobre 2026 » (image).
- 3 tests ajoutés (5 au total).
- Écart : la maquette montre 2 affiches dans « Lancement », une seule est disponible (`affiche-leadership-jaune.jpg`). Rendu à valider visuellement dans un navigateur.

### Page Qui sommes-nous ? (`/qui-sommes-nous/`)
- 6 sections : hero, ambition, vision et mission (2 cartes), valeurs (6), citation, fondateur.
- Contenu dans `content.QUI_SOMMES_NOUS` ; vue `qui_sommes_nous` ; gabarit `layout/qui_sommes_nous.html` ; styles `qs-*` dans `main.css` (section 13).
- Les liens « Qui sommes-nous ? » (navigation, pied de page) pointent vers la page ; la section fondateur réutilise le bloc de l'accueil.
- 3 tests ajoutés (8 au total). Rendu à valider visuellement dans un navigateur.

### Page Nos programmes (`/programmes/`)
- 4 sections : hero (vert, disque orange « apprendre en faisant »), méthode (3 étapes colorées), les 3 programmes en alternance, bandeau « D'autres programmes à venir », appel à l'engagement.
- Contenu dans `content.NOS_PROGRAMMES` ; vue `nos_programmes` ; gabarit `layout/nos_programmes.html` ; styles `np-*` dans `main.css` (section 14).
- Les liens « Nos programmes » (navigation, accueil, page Leadership) pointent vers la page ; la carte UCIV Leadership mène à sa page, les deux autres à `#` (pages à venir).
- 3 tests ajoutés (11 au total). Rendu à valider visuellement dans un navigateur.
- Le hero des 2 pages accueil et UCIV Leadership occupe 90 vh à partir de 1100 px.

### Page Les Go du Digital (`/programmes/go-du-digital/`)
- 8 sections : hero orange, repères (4), volets (4 cartes avec icônes), apprentissages (5), pédagogie (90 % et La Reine du Digital), public et suivi, partenaires du programme, inscriptions.
- Contenu dans `content.GO_DU_DIGITAL` ; vue `go_du_digital` ; gabarit `layout/go_du_digital.html` ; styles `gd-*` dans `main.css` (section 15).
- Les liens « Les Go du Digital » (navigation, pied de page, accueil, page Nos programmes) pointent vers la page.
- 3 tests ajoutés (14 au total).
- Aligné sur la maquette (valeurs lues dans Pencil) : hero avec cercle jaune, disque crème et photo ronde, pastille « 90 % de pratique », volets en grille 2 × 2 avec icônes, apprentissages en 3 colonnes, bloc « 90 % » et carte « La Reine du Digital », inscriptions sur fond orange. Rendu à valider dans un navigateur.

### Page Experience Lab (`/programmes/experience-lab/`)
- 4 sections : hero vert (disque crème, photo ronde, cercles jaune et orange), approche (« Know yourself before showing yourself. » et 4 questions), objectifs (6), inscriptions.
- Contenu dans `content.EXPERIENCE_LAB` ; vue `experience_lab` ; gabarit `layout/experience_lab.html` ; styles `el-*` dans `main.css` (section 16), hero et inscriptions réutilisent les classes `gd-*`.
- Les liens « Experience Lab » (navigation, pied de page, accueil, page Nos programmes) pointent vers la page.
- 3 tests ajoutés (17 au total). Valeurs lues dans la maquette (positions, tailles, interlignes, espacements et rotations relevés à 1440 px, appliqués en `vw` en dessous) ; rendu à valider dans un navigateur.

### Sécurité du code (audit du 17 octobre 2026)
- Audit : aucune injection SQL ni XSS trouvée (ORM seul, aucun `|safe`, `corps_article` échappé, CSRF actif, champ piège anti-robots).
- **Réglages de production** : le site refuse de démarrer hors `DEBUG` sans `SECRET_KEY` d'au moins 50 caractères ni `ALLOWED_HOSTS` explicites (plus de valeurs de développement par défaut en production). HSTS activé (`HSTS_SECONDS`, 1 jour au départ), cookies `SameSite=Lax`, réglage `SECURE_BROWSER_XSS_FILTER` retiré (sans effet).
- **Téléversements** (`app/validators.py`) : l'image d'article est un `ImageField` limité à jpg/png/webp/gif ; les fichiers de ressources à des documents ; 10 Mo maximum ; SVG et HTML refusés. Migration `0009`.
- **Données structurées** : les caractères `<`, `>` et `&` sont écrits en séquences Unicode (u003c, u003e, u0026) dans le JSON-LD.
- 6 tests ajoutés (96 au total, classe `SecuriteTests`).
- Reste côté serveur : mot de passe root et SSH par mot de passe, `ufw`, fail2ban, mises à jour automatiques, `limit_req` Nginx (formulaires et `/admin/login/`), en-têtes Nginx (`server_tokens off`, CSP sur `/media/`), phpMyAdmin limité à une IP, sauvegardes. Côté projet : HSTS à 1 an avec `includeSubDomains` une fois le HTTPS vérifié, 2FA de l'administration (nouveau paquet : accord requis), page de confidentialité.

### Liens « Rejoindre UCIV Leadership » vers le formulaire (19 octobre 2026)
- Tous les boutons et liens « Rejoindre UCIV Leadership » (bandeau d'annonce, menu « S'engager » sur ordinateur et mobile, cartes de l'accueil, page Nos programmes, page Je veux m'engager, deux boutons de la page du programme) ouvrent maintenant `/engagement/?choix=leadership#formulaire` : le formulaire d'engagement, déjà positionné sur la section, avec l'option « Rejoindre UCIV Leadership » cochée.
- Même ancre pour « Devenir volontaire » (`?choix=volontaire`) et « Proposer mes compétences » (`?choix=competences`). Liens définis dans `content.py` (`URL_REJOINDRE_LEADERSHIP`, `LEADERSHIP['url_rejoindre']`) ; une valeur de `choix` inconnue ne coche rien.
- Le bouton « Rejoindre » de la page du programme, qui pointait vers `#` (lien mort), est corrigé.
- 7 tests ajoutés (`RejoindreLeadershipTests`, 163 au total). **Pas encore commité ni déployé.**
- Restent des boutons sans destination : « S'inscrire » (Go du Digital, Experience Lab) et « Découvrir UCIV » (accueil).

### Loader du site (19 octobre 2026)
- Loader fourni (logo UCIV : trois volontaires qui arrivent en spirale, ronde pendant le chargement, puis deux rideaux qui dévoilent la page), intégré tel quel et découpé selon les règles du projet : `static/app/assets/css/loader.css`, `static/app/assets/js/loader.js`, balisage dans `templates/app/includes/_loader.html`, inclus au début du `<body>` de `base/base.html` (le CSS dans l'en-tête, avec un `<noscript>` qui le masque sans JavaScript).
- Réglages dans l'attribut des `#uciv-loader` : animation complète **une fois par session** (`data-once="session"` ; « always » pour chaque page), durée minimale (`data-min`), sortie forcée après 15 s (`data-max`), attente manuelle (`data-wait="manual"` puis `UCIVLoader.done()`). Événement `uciv:loaded` à la fin ; respecte `prefers-reduced-motion`.
- Ajouts pour le site : les animations d'entrée du bandeau (`hero__entree`…) restent en pause tant que le loader est affiché, et l'apparition au défilement (`main.js`) démarre à sa sortie, pour qu'on les voie après le rideau. Le loader n'apparaît pas dans l'administration.
- Couleurs du loader : orange `#da8121` et fond `#fffaf3`, légèrement différents de la charte (`#E17F1C`, `#FBF5EA`) ; ce sont celles du fichier fourni. Poids : environ 15 Ko de balisage ajoutés à chaque page (retirés du DOM dès la sortie).
- 6 tests ajoutés (`LoaderTests`, 156 au total). Contrôlé avec Chrome sans interface (logo animé dans la vraie page, page visible après la sortie). **Pas encore déployé ni commité.**

### Mise en ligne sur le VPS (19 octobre 2026)
- Déployé avec `deploy/deployer.sh` par SSH (clé `uciv_deploy`) : Gunicorn + Nginx + HTTPS Let's Encrypt (certificat pour `uciv.org` et `www.uciv.org`, valable jusqu'au 16 janvier 2027, renouvelé seul), MySQL, 10 articles et 6 opportunités d'exemple issus des migrations.
- Contrôlé après déploiement : les 17 pages publiques, `robots.txt`, `sitemap.xml` et `llms.txt` répondent 200 ; `/back-office/login/` 200 ; `/admin/` et les adresses inconnues 404 ; redirection HTTP vers HTTPS ; en-têtes HSTS (1 jour), `X-Frame-Options`, `nosniff` ; limite Nginx des envois active ; cache partagé du limiteur de débit fonctionnel.
- Incident corrigé au premier passage : `uciv-manage` utilisait `sudo -E`, ignoré par le sudo-rs du serveur, donc les migrations visaient SQLite et pas MySQL (500 sur les pages qui lisent la base). La commande passe maintenant les variables avec `runuser` et `env` ; les erreurs 500 sont écrites dans `journalctl -u uciv` (réglage `LOGGING`).
- **Reste à faire sur le serveur** : créer le compte administrateur (`ssh -t uciv-vps uciv-manage createsuperuser`, interactif) ; désactiver la connexion SSH par mot de passe (`passwordauthentication yes` et `permitrootlogin yes` sont encore actifs) et changer le mot de passe root ; activer `ufw` (inactif) ; fail2ban et mises à jour automatiques ; configurer `EMAIL_*` pour recevoir les messages des formulaires par e-mail (sinon ils ne sont que dans la base) ; passer `HSTS_SECONDS` à 31536000 une fois le HTTPS validé ; Google Search Console.

### Adresse de l'administration : `/back-office/` (19 octobre 2026)
- L'administration n'est plus à `/admin/` mais à **`/back-office/`**. Le réglage `ADMIN_URL` (variable d'environnement) permet d'en choisir une autre, plus difficile à deviner, sans toucher au code.
- `admin` est refusé en production ; l'adresse ne peut contenir que lettres, chiffres, `-` et `_`. `/admin/` répond 404.
- `deploy/deployer.sh` lit `ADMIN_URL` dans `/etc/uciv/uciv.env` (sinon `back-office`), l'affiche à la fin et vérifie que `/admin/` répond 404.
- `robots.txt` ne cite plus l'administration (ses pages portent déjà `noindex`).
- Remarque : « back-office » reste facile à deviner ; la protection repose sur le mot de passe et le limiteur de débit (10 essais par IP et 5 par identifiant toutes les 15 minutes).
- 5 tests (`AdresseAdministrationTests`, 149 au total).

### Limiteur de débit des formulaires (18 octobre 2026)
- **Python** (`app/ratelimit.py`, sans paquet de plus) : au plus **5 envois par formulaire et par adresse IP toutes les 10 minutes** pour Contact, Je veux m'engager, Partenaires et la lettre d'information ; au-delà, réponse **429** avec `Retry-After` et une page « Doucement, trop de demandes » (`layout/429.html`, texte dans `content.PAGE_429`, non indexée). Seuls les envois (POST) sont comptés : afficher une page n'est jamais limité.
- **Connexion à l'administration** : 10 essais par adresse IP et 5 par identifiant toutes les 15 minutes (l'identifiant bloque aussi une attaque répartie sur plusieurs adresses).
- **Adresse du visiteur** : derrière Nginx, l'en-tête `X-Real-IP` (écrit par Nginx) ; en développement (`DEBUG=True`) il est ignoré pour qu'on ne puisse pas le falsifier.
- **Compteurs** : cache en mémoire en développement ; **dossier partagé `cache_cdn/`** en production (`CACHE_DIR` pour le changer), car chaque processus Gunicorn compterait à part avec un cache en mémoire. Le dossier est ignoré par Git.
- **Nginx** (`deploy/nginx-uciv.conf`) : seconde barrière, 20 envois (POST) par minute et par adresse IP avec une rafale de 10, réponse 429. À appliquer en relançant `deploy/deployer.sh`.
- 11 tests ajoutés (`LimiteurDeDebitTests`, 144 au total) ; les tests existants repartent d'un cache vide.

### Clé SSH de déploiement
- Clé ed25519 dédiée créée sur le poste de déploiement (`~/.ssh/uciv_deploy`, hors du dépôt), installée sur le VPS ; connexion testée sans mot de passe ; raccourci `ssh uciv-vps`. Procédure, ajout d'un développeur, retrait d'accès et durcissement du serveur dans [DEPLOIEMENT.md](DEPLOIEMENT.md).
- À faire : désactiver la connexion par mot de passe sur le serveur (après un second test de la clé), changer le mot de passe `root`, activer `ufw`.

### GEO : être cité par les moteurs de réponse IA (ChatGPT, Claude, Perplexity, Google AI)
- **Section « Questions fréquentes »** visible sur chacune des 14 pages (`app/includes/_faq.html`, contenu dans `content.FAQ`) : titres en forme de question, réponses autonomes avec chiffres et noms exacts, sans information inventée (dates et tarifs inconnus annoncés « à confirmer »). Pas de balisage `FAQPage` (réservé par Google aux sites publics et de santé).
- **`/robots.txt`** : `GPTBot`, `OAI-SearchBot`, `ChatGPT-User`, `ClaudeBot` et `PerplexityBot` nommés et autorisés ; **`/llms.txt`** enrichi (faits clés, pages, 5 dernières actualités, réseaux).
- **Données structurées** : les 9 membres de l'équipe déclarés en `Person` sur la page Équipe ; `dateModified` sur les pages alimentées par la base ; dates d'article dans des balises `<time>`.
- Score GEO estimé : 51 → 71 sur 100 (à refaire sur le site publié). Rapport, règles de rédaction et actions hors du site (YouTube, LinkedIn, Wikidata, Search Console) : [GEO.md](GEO.md).
- 8 tests ajoutés (90 au total).

### Images allégées (WebP)
- Les 10 photos et le logo UCIV Leadership sont servis en **WebP**, tous sous 200 Ko (de 2,2 Mo à 195 Ko pour la plus lourde) : 7,9 Mo avant, 1,4 Mo après pour l'ensemble des images du site. `logo-uciv.png` (24 Ko) reste en PNG (icône du navigateur, logo des données structurées).
- Les **originaux** sont conservés dans `sources/images/` (hors du dossier servi au public). L'outil `outils/convertir_images.py` (Pillow) reconstruit les WebP : déposer l'original dans `sources/images/`, puis `python outils/convertir_images.py`.
- **Images de partage** (Open Graph) : 5 JPEG de 1200 × 630 (`og-*.jpg`, moins de 150 Ko) pour l'accueil, UCIV Leadership, Experience Lab, Je veux m'engager et Partenaires, en JPEG car LinkedIn et d'autres réseaux n'affichent pas toujours le WebP.
- Migration `0007_images_webp` : met à jour les chemins des articles déjà en base (`.jpg`/`.png` vers `.webp`).
- 3 tests ajoutés (82 au total) : chaque image référencée existe et pèse moins de 200 Ko, les pages servent les WebP, aucun article ne pointe vers un ancien fichier.
- À faire : `python manage.py migrate` (migration `0007`) ; pour un article avec image téléversée depuis l'administration, privilégier un fichier déjà allégé (WebP, moins de 200 Ko).

### Référencement (SEO) de chaque page
- **Balises par page** (`content.SEO_PAGES`, rendues par `app/seo.py`) : titre de 47 à 58 caractères, description de 138 à 159 caractères, uniques ; balise `canonical`, `robots`, Open Graph (`og:*`) et Twitter Card ; `og:image` propre à la page quand elle en a une. Le titre et la description d'un article viennent de l'article (titre, résumé, image, dates `article:*`).
- **Données structurées JSON-LD** : accueil = `NGO` (organisation, fondateur, réseaux, contact) + `WebSite` ; pages intérieures = `WebPage`/`AboutPage`/`CollectionPage`/`ContactPage` + `BreadcrumbList` ; UCIV Leadership = `Event` (lancement le 24 octobre 2026, American Corner) ; Go du Digital et Experience Lab = `Course` ; Nos programmes = `ItemList` ; articles = `Article` (éditeur, image, dates). Aucun `FAQPage` ni `HowTo` (restreint / abandonné par Google).
- **Indexation** : `/robots.txt` (tout autorisé sauf `/admin/`, adresse du sitemap), `/sitemap.xml` (14 pages + articles publiés, `lastmod` seulement quand une vraie date existe, sans `priority` ni `changefreq`), `/llms.txt` (présentation du site pour les moteurs de réponse), page 404 en `noindex`.
- **Doublons évités** : les pages filtrées (`?categorie=`, `?type=`, `?theme=`, `?choix=`, `?objet=`) sont en `noindex, follow` avec une adresse canonique propre ; chaque page de la pagination des actualités a sa propre adresse canonique.
- **`SITE_URL`** (ex. `https://uciv.org`) fixe l'adresse publique utilisée par les adresses canoniques, le sitemap et les données structurées : à renseigner en production (déjà dans `deploy/deployer.sh`).
- 17 tests ajoutés (79 au total) : longueur des titres et descriptions, unicité, un seul `h1`, texte alternatif sur chaque image, JSON-LD valide, fil d'Ariane, événement, article, `noindex` des variantes, `robots.txt`, sitemap, `llms.txt`, 404.
- **Recommandations restantes** : (1) après la mise en ligne, déclarer le site dans Google Search Console et lui soumettre `sitemap.xml` ; (2) remplacer le lien Facebook de partage par l'adresse réelle de la page ; (3) rédiger les pages légales.

### Passage sur MySQL (préparé, pas encore appliqué au site)
- Serveur : MySQL 8.4 et phpMyAdmin (https://bd.uciv.org, double authentification, HTTPS) installés ; base `uciv` et utilisateur `uciv_user` créés ; script `deploy/phpmyadmin.sh`.
- Code : réglages MySQL corrigés (utf8mb4, SSL facultatif via `MYSQL_SSL_MODE`, connexions persistantes), en-tête proxy HTTPS et `CSRF_TRUSTED_ORIGINS` pour la production, `requirements-mysql.txt` (ajoute `mysqlclient`, `requirements.txt` reste Django seul), `.env.example` complété.
- Procédure complète : [DEPLOIEMENT.md](DEPLOIEMENT.md). 3 tests ajoutés (62 au total).
- **Déploiement préparé** (pas encore lancé) : `deploy/deployer.sh` (Git, environnement Python, variables d'environnement, migrations, statiques, service Gunicorn `uciv`, Nginx, HTTPS Let's Encrypt, commande `uciv-manage`), `deploy/gunicorn-uciv.service`, `deploy/nginx-uciv.conf`, `requirements-prod.txt` (ajoute `gunicorn`). Relançable pour mettre à jour. Détail dans [DEPLOIEMENT.md](DEPLOIEMENT.md).

### Administration aux couleurs d'UCIV (`/admin/`)
- Habillage sans dépendance : gabarit `templates/admin/base_site.html` (logo, « Une Côte d'Ivoire *Volontaire* », badge « Administration ») et feuille `static/app/assets/css/admin.css`.
- Palette et typographies du site (vert profond, orange, jaune, crème ; Bricolage Grotesque, Instrument Serif, Plus Jakarta Sans), cartes arrondies, boutons en pastille, page de connexion sur fond vert profond. Thème clair fixe (le sélecteur clair/sombre est masqué).
- Titres : « Administration UCIV », « Gestion du site » ; l'application s'affiche sous le nom « Site UCIV ».
- 2 tests ajoutés (59 au total). Rendu à valider dans un navigateur.
- **Refonte d'après la maquette du dashboard (18 octobre 2026)** : barre latérale verte (Pilotage, Contenu du site, Suivi, Technique) avec compteur de messages non traités, « Voir le site », utilisateur et déconnexion ; menu replié derrière un bouton sous 1024 px (`static/app/assets/js/admin.js`).
  - **Tableau de bord** (`templates/admin/index.html`, balises `app/templatetags/uciv_admin.py`) : salutation et date, recherche d'article, 4 chiffres clés, « À faire » (messages, fiches d'exemple, chiffres d'impact à renseigner, brouillons), raccourcis, derniers contenus modifiés, messages récents.
  - **Connexion** en deux panneaux (« Espace équipe. »), icônes Lucide (`templates/admin/_icones.html`), listes en cartes blanches.
  - **Listes** : colonne « Statut » en pastilles (Publié, Brouillon, Fiche d'exemple ; Nouveau et Traité pour les messages), actions « Publier », « Repasser en brouillon », « Marquer comme traité » ; titres lisibles (« Articles »). Le champ `publish` d'un message sert de « traité » ; le champ n'est plus modifiable en ligne dans les listes (utiliser les actions).
  - **Mise en conformité avec les écrans de la maquette (18 octobre 2026)** : plus de panneau de filtres ni de fil d'Ariane Django ; listes Articles, Opportunités et Ressources avec description, recherche, boutons de filtre (Tous, Publiés, Brouillons, À la une, Nos histoires… ; catégories et « Fiches d'exemple » pour les opportunités ; Guides, Vidéos, Podcasts pour les ressources), tableau en carte, icônes Modifier / Voir sur le site / menu « … » (publier ou repasser en brouillon, supprimer) et pagination ronde « N articles sur M ».
  - **Formulaires en cartes** (gabarits `admin/uciv/formulaire.html` et `_carte.html`) : retour « ← Articles », titre et pastille de statut, boutons « Voir sur le site » et « Enregistrer », sections Contenu / Repères à gauche, Publication (interrupteurs) / Image à droite, bouton « Supprimer… ». Les libellés, aides et sections sont décrits dans `app/admin.py`.
  - **Messages reçus** : une seule boîte réunit les demandes d'engagement, propositions de partenariat et messages de contact (liste à gauche, détail à droite, boutons de filtre Tous / Nouveaux / Engagement / Partenariat / Contact, « Répondre par e-mail », « Marquer comme traité »). **Abonnés** : trois chiffres, recherche, liste, « Exporter en CSV ». **Chiffres d'impact** : les valeurs se saisissent dans la liste, avec le bandeau « N'affichez que des chiffres vérifiés ».
  - Barre latérale limitée aux entrées de la maquette ; les comptes (« Comptes ») restent accessibles aux super-utilisateurs depuis le bloc utilisateur.
  - `admin.css` est chargée en dernier (après les feuilles de Django). 24 tests d'administration (133 au total). Rendu contrôlé avec Chrome sans interface à 1440 px et 700 px ; à valider sur un vrai téléphone.

### Pages de contenu : Opportunités, Actualités, Article, Notre impact, Ressources
- **Modèles administrables** (`Article`, `Opportunite`, `Ressource`, `Indicateur`, migration `0004`) : tout nouveau contenu est non publié par défaut ; la case « publié » (`publish`) le met en ligne.
- **Contenu de départ** (migration de données `0005_contenu_initial`) : 7 articles + 3 « histoires » tirés de la maquette et de l'accueil, 6 indicateurs sans valeur, 6 opportunités et 8 ressources **d'exemple** (cases « fiche d'exemple » cochées, textes « À renseigner »). L'équipe les remplace ou les dépublie depuis l'administration ; la mention « emplacements » disparaît quand plus aucune fiche d'exemple n'est affichée.
- **Opportunités** `/opportunites/` : bandeau, 5 catégories, fiches filtrables (`?categorie=`), appel « Devenir partenaire ».
- **Actualités** `/actualites/` : article à la une, fil filtrable par catégorie (`?categorie=`), pagination de 6 ; **Article** `/actualites/<slug>/` : bandeau, image, corps mis en forme, partage Facebook / LinkedIn / WhatsApp, « À lire aussi ».
- **Notre impact** `/impact/` : 6 indicateurs (« 000 » tant que la valeur est vide), « Nos histoires » (articles cochés `histoire`), citation. **Ressources** `/ressources/` : bibliothèque filtrable par type et thème (`?type=&theme=`).
- **Texte d'un article** (champ « corps », sans HTML) : un bloc par ligne vide ; `!! ` chapô, `## ` sous-titre, `> ` citation (ligne `— Nom` pour la signature), lignes `- ` liste de points, sinon paragraphe. Filtre `corps_article`, texte échappé.
- **Accueil** : la section « L'actualité d'UCIV » et les chiffres de « Vision & chiffres » lisent la base, avec repli sur `content.py` tant qu'elle est vide.
- **Bandeaux** : composant commun `_hero_page.html` (formes en disques ou anneaux relevées dans la maquette, converties en `vw`).
- Écarts : seule l'image principale d'un article est gérée (la maquette montre une 2e image avec légende) ; les images « générées » de la maquette sont remplacées par les photos du site.
- 17 tests ajoutés (56 au total). Rendu à valider dans un navigateur.
- À faire : `python manage.py migrate` (migrations `0004` et `0005`), puis ouvrir `/admin/` pour gérer le contenu.

### Page Contact (`/contact/`)
- 2 parties : hero orange (anneau crème, disque vert profond avec « on vous répond ! », anneau jaune), formulaire « Écrivez-nous » et carte « Coordonnées officielles » (téléphones, e-mail, adresse, réseaux sociaux).
- Contenu dans `content.CONTACT` ; vue `contact` ; gabarit `layout/contact.html` ; styles `con-*` dans `main.css` (section 21), contrôles de formulaire partagés (`eng-*`).
- Formulaire fonctionnel : `ContactForm`, modèle `SoumissionContact` (migration `0003`), administration, champ piège, e-mail à l'équipe si `EMAIL_HOST` est configuré avec réponse directe à l'expéditeur (`reply_to` ajouté à `send_customize_email`, appliqué aussi à l'engagement et au partenariat).
- Le champ « Objet » est une liste déroulante pilotée aussi par des pastilles (JavaScript, `main.js` bloc 6), comme dans la maquette. `?objet=` préremplit le choix.
- Le lien « Contact » du pied de page et la note « Écris-nous » de la page d'engagement mènent à la page.
- 6 tests ajoutés (39 au total). Valeurs et anneaux lus dans la maquette ; rendu à valider dans un navigateur.
- Écart : dans la maquette le texte du hero dépasse la hauteur de 500 px et serait rogné ; le hero s'agrandit ici pour tout afficher.
- À faire : `python manage.py migrate` (migration `0003`).

### Page Partenaires (`/partenaires/`)
- 4 sections : hero orange (disque crème, photo ronde PAIPRO, anneaux jaune et vert), « Ils nous accompagnent » (3 cartes), « Formes de collaboration » (10 lignes sur fond vert profond), formulaire « Proposer un partenariat ».
- Contenu dans `content.PAGE_PARTENAIRES` ; vue `partenaires` ; gabarit `layout/partenaires.html` ; styles `par-*` dans `main.css` (section 20), contrôles de formulaire partagés avec la page d'engagement (`eng-*`).
- Formulaire fonctionnel : `PartenariatForm`, modèle `SoumissionPartenariat` (migration `0002`), administration, champ piège, e-mail à l'équipe si `EMAIL_HOST` est configuré (gabarit `emails/partenariat.html`).
- Les boutons « Devenir partenaire » et la carte « Votre organisation ? » de l'accueil, ainsi que le lien « Nos partenaires » du pied de page, mènent à la page.
- 6 tests ajoutés (33 au total). Valeurs et anneaux lus dans la maquette ; rendu à valider dans un navigateur.
- À faire : `python manage.py migrate` (migration `0002`).

### Page Je veux m'engager (`/engagement/`)
- 3 sections : hero (disque orange, photo ronde, anneaux jaune et vert, « il y a une place pour toi ! »), trois façons de nous rejoindre (cartes blanche, jaune, vert profond), formulaire d'engagement.
- Formulaire fonctionnel : `app/forms.py` (`EngagementForm`, champ piège anti-robots), modèle `SoumissionEngagement` (migration `0001_initial`), administration Django, message de confirmation, e-mail à l'équipe si `EMAIL_HOST` est configuré (`CONTACT_EMAIL`, gabarit `emails/engagement.html`).
- Les boutons « Devenir volontaire » et « Proposer mes compétences » préremplissent le choix (`?choix=`) ; tous les boutons « Je veux m'engager » du site (en-tête, pied de page, accueil, pages Qui sommes-nous ?, Nos programmes, Équipe) mènent à la page.
- 7 tests ajoutés (27 au total). Valeurs lues dans la maquette ; rendu à valider dans un navigateur.
- À faire : `python manage.py migrate` en local et en production ; le lien « politique de confidentialité » pointe encore vers `#`.

### Page Équipe (`/qui-sommes-nous/equipe/`)
- 5 sections : hero vert profond (anneau jaune, disque orange, anneau vert), président (arche orange et portrait de Marshall Kouamé), bureau exécutif (4 cartes en arche), médias et communication (4 lignes avec initiales), appel orange « Envie de rejoindre l'équipe ? ».
- Contenu dans `content.EQUIPE` ; vue `equipe` ; gabarit `layout/equipe.html` ; styles `eq-*` dans `main.css` (section 18) ; l'appel réutilise `np-appel` en variante orange.
- Les boutons « Découvrir UCIV » de la section fondateur (accueil et Qui sommes-nous ?) mènent à la page.
- 3 tests ajoutés (20 au total). Valeurs et anneaux (innerRadius) lus dans la maquette ; rendu à valider dans un navigateur.
- **Manquant** : les 4 portraits du bureau exécutif (`bureau-executif.jpg` dans la maquette, non fourni) : les cartes affichent les initiales ; renseigner `photo` dans `content.EQUIPE['bureau']` pour les afficher. Bio du président à transmettre.

### Cercles creux de la maquette
- Les ellipses du bandeau et de plusieurs sections sont des anneaux (propriété `innerRadius` de Pencil : 0,7 à 0,8), pas des disques pleins. Ils sont reproduits par un dégradé radial (section 17 de `main.css`) sur les pages Go du Digital, Experience Lab, UCIV Leadership, Qui sommes-nous ?, Nos programmes ; l'anneau de la section « Vision & chiffres » de l'accueil est ajusté (57 px).
- Les cercles pleins restent pleins là où la maquette n'a pas de rayon intérieur (disques crème, orange, blanc).

### Responsive mobile (16 octobre 2026)
- **Maquette mise à jour** : `maquette/design_uciv.pen` remplacée par la version de travail (écrans desktop **et** les 15 écrans « … — Mobile » à 390 px).
- **Méthode** : chaque écran mobile a été exporté de Pencil, puis comparé au site à 390 px (tailles, interlignes, graisses de chaque texte, puis hauteur de chaque section). Toutes les sections sont alignées à quelques pixels près, sauf les écarts de contenu listés plus bas.
- **Fichiers modifiés** :
  - `static/app/assets/css/main.css` : nouvelle **section 23** « Mobile : valeurs de la maquette 390 px », un seul bloc `@media (max-width: 719px)`. Rien ne change au-dessus de 720 px (tablette et ordinateur).
  - `templates/app/includes/_hero_page.html` et `app/content.py` : taille mobile du titre des bandeaux (`taille_mobile` : 40, 48, 40, 44 px selon la page).
- **Ce qui change en mobile** : échelle typographique de la maquette (titres 32 à 44 px, textes 16/26 px), sections à 56 px de marge, bandeaux à un seul anneau avec la note manuscrite sous le texte, photos des bandeaux en rectangle arrondi (engagement, partenaires, programmes), bureau exécutif en grille 2 × 2, valeurs avec le numéro à gauche, indicateurs d'impact en 2 colonnes, programmes avec numéro et étiquette sur une ligne, portrait du fondateur au-dessus du texte, pied de page resserré.
- **Débordements horizontaux corrigés** : Nos programmes (disque jaune) et Je veux m'engager (cartes).
- **Menu mobile** : le panneau affiche maintenant le logo complet (image + nom), lien vers l'accueil (`includes/_header.html`).
- **UCIV Leadership** : le logo posé sur la photo du hero est masqué en mobile, comme dans la maquette.

### Autres changements du 16 octobre 2026
- **Notre impact** : la citation n'a plus de bouton « Je veux m'engager » (modification de la maquette desktop et mobile) ; `templates/app/layout/impact.html`.
- **Équipe** : les 4 portraits du bureau exécutif sont découpés dans l'affiche `bureau-executif.jpg` avec les cadrages de la maquette (`static/app/assets/img/bureau-*.jpg`, chemins dans `content.EQUIPE['bureau']`). L'affiche est en basse résolution : des photos HD restent à fournir.

### Pages légales et page 404 (16 octobre 2026)
- **Maquette** : 4 nouveaux écrans desktop + mobile dans `maquette/design_uciv.pen` (Mentions légales, Politique de confidentialité, Conditions d'utilisation, Page introuvable (404)), validés avant l'implémentation.
- **Pages** : `/mentions-legales/`, `/politique-de-confidentialite/`, `/conditions-d-utilisation/` ; une seule vue `page_legale` et un seul gabarit `layout/legal.html` (bandeau, sommaire, sections numérotées, encart « Une question ? », « Les autres documents »). Textes dans `content.LEGAL` ; blocs `p`, `fiche`, `liste`, `encadre`.
- **Textes à compléter** : tout passage `[entre crochets]` s'affiche en orange (filtre `crochets`) : forme juridique, récépissé, hébergeur, prestataire, adresse du site, durées de conservation, date de mise à jour (`LEGAL_MAJ`). À faire relire par UCIV avant la mise en ligne.
- **404** : `layout/404.html` (visuel « 4 ● 4 », retour à l'accueil, contact, 4 liens utiles), branchée par `handler404` (active quand `DEBUG=False`). En local, aperçu sur `/404/`.
- **Liens connectés** : pied de page (3 documents, toutes les pages), « Voir la politique de confidentialité » des formulaires Engagement et Contact, cartes « Les autres documents », sommaire (ancres + mise en évidence de la section lue, `main.js` bloc 7).
- **Fichiers** : `app/content.py`, `app/views.py`, `app/urls.py`, `core/urls.py`, `app/templatetags/custom_tags.py`, `templates/app/layout/legal.html` et `404.html`, `includes/_hero_page.html` (pastille « Dernière mise à jour »), `includes/_icons.html` (4 icônes), `contact.html`, `engagement.html`, `main.css` (section 24), `main.js`.
- **Formes concentriques** : dans les bandeaux, chaque forme est désormais placée par son centre (`.ph-forme`), si bien qu'un disque reste au centre de son anneau à toutes les largeurs d'écran ; anneaux orange des pages légales aux dimensions exactes de la maquette (légèrement ovales, `h` dans `content.py`), disque orange de la 404 centré dans l'anneau jaune (desktop et mobile).
- 5 tests ajoutés (61 au total).

### Lettre d'information (16 octobre 2026)
- **Maquette** : écrans « Lettre d'information — états du formulaire » (desktop, mobile), « Désinscription » et « Désinscription confirmée » (desktop, mobile), validés avant l'implémentation.
- **Choix** : inscription directe (pas de double confirmation) ; le site collecte les adresses, l'équipe envoie la lettre avec son propre outil (Brevo, Mailchimp…) à partir d'un export CSV.
- **Modèle** `Abonne` (migration `0006`) : e-mail unique, actif, jeton de désinscription, dates d'inscription et de désinscription. **Administration** : filtre actifs / désinscrits, action « Exporter en CSV les abonnés actifs sélectionnés » (séparateur `;`, compatible Excel).
- **Pied de page** : le formulaire envoie vers `/newsletter/inscription/` (champ piège anti-robots) puis revient sur la même page, au niveau de la carte (`#lettre`), qui affiche l'état : inscription réussie, déjà inscrit·e, adresse invalide (l'adresse saisie est conservée). Réinscription possible après une désinscription.
- **Désinscription** : lien personnel `/newsletter/desinscription/<jeton>/`, page en deux étapes (confirmer en un clic, puis « C'est noté ») ; la désinscription se fait en POST pour qu'une messagerie qui ouvre les liens ne désinscrive personne. Jeton inconnu : 404. Page non indexée.
- **E-mail de bienvenue** avec le lien de désinscription, envoyé si `EMAIL_HOST` est configuré (`emails/newsletter_bienvenue.html`).
- **Disques** : sur la page de désinscription, anneau, disque et pictogramme ont le même centre (vérifié : 1083 ; 433 en desktop, 208 ; 241 en mobile).
- **Fichiers** : `models.py`, `forms.py`, `views.py`, `urls.py`, `admin.py`, `content.py` (`NEWSLETTER`, `DESINSCRIPTION`), `context_processors.py`, `templatetags/custom_tags.py` (`get_item`), `includes/_footer.html`, `includes/_icons.html`, `layout/desinscription.html`, `emails/newsletter_bienvenue.html`, `main.css` (section 25), `main.js` (suppression du formulaire provisoire).
- 10 tests ajoutés (71 au total).
- À faire en production : `python manage.py migrate` (migration `0006`).

### Maquette du dashboard de l'équipe (16-17 octobre 2026)
- **Objectif** : un espace privé, distinct de l'admin Django, pour gérer et alimenter le contenu des pages Opportunités, Actualités, Article, Notre impact et Ressources.
- **Choix validés** : le dashboard couvre le contenu **et** le suivi (messages reçus des formulaires, abonnés avec export CSV) ; un seul type de compte (toute l'équipe a les mêmes droits) ; l'admin Django reste pour le technique.
- **Écrans** (27 cadres dans la maquette, desktop sur la ligne y = 22 400, mobile sur y = 24 400, composants sur y = 21 200) :
  - Planche de composants : barre latérale (Pilotage / Contenu du site / Suivi, compteur de messages, « Voir le site », utilisateur et déconnexion), barre mobile, pastilles de statut (Publié, Brouillon, Fiche d'exemple, Nouveau, Lu).
  - Connexion (et état d'erreur) ; Tableau de bord (chiffres clés, « À faire », raccourcis, derniers contenus, messages récents).
  - Listes Articles, Opportunités, Ressources (recherche, filtres, tableau en desktop, cartes en mobile) et formulaires Modifier l'article, Nouvelle opportunité, Modifier la ressource (contenu à gauche, publication et image ou fichier à droite ; barre d'actions fixe en mobile).
  - Chiffres d'impact (6 indicateurs, ordre, « À venir » si vide), Messages reçus (liste + détail, « Répondre par e-mail », « Marquer comme traité »), Abonnés (chiffres, liste, export CSV), menu mobile ouvert.
- Les champs des formulaires reprennent ceux des modèles existants (`Article`, `Opportunite`, `Ressource`, `Indicateur`, `Abonne`). Implémentation à faire sur une nouvelle branche partie de `feature/dashboard`.

### Maquette
- `maquette/design_uciv.pen` : 20 écrans desktop et 19 écrans mobiles pour le site public, 6 écrans de la lettre d'information, 27 cadres pour le dashboard. Le fichier de travail est `UCIV/design_uciv.pen` (ouvert dans Pencil) ; il est recopié dans `maquette/` avant chaque commit.

## Écarts connus avec la maquette (volontaires ou à trancher)

| Élément | Maquette | Site | Décision |
|---|---|---|---|
| Chiffres d'impact | `000` | « à venir » | Garder le site : pas de faux chiffres |
| Bouton de recherche en-tête | absent | présent, sans destination | À valider ou retirer |
| Sous-menus (Programmes, S'engager) | non dessinés | présents | À valider |

## Branches fusionnées dans `main` (18 octobre 2026)

Quatre branches empilées, chacune partie de la précédente, fusionnées en une seule fois depuis `feature/dashboard`. Conflits résolus : `content.py`, `views.py`, `tests.py`, `main.css` (les deux côtés gardés), l'ancienne page 404 de `main` remplacée par celle de la branche, migration `Abonne` renumérotée `0008` :

| Branche | Contenu |
|---|---|
| `feature/responsive-mobile` | Responsive mobile des 15 pages, maquette mise à jour, `.gitattributes`, portraits du bureau, citation de Notre impact, logo du menu mobile |
| `feature/pages-legales` | Mentions légales, politique de confidentialité, conditions d'utilisation, page 404 (maquette + code) |
| `feature/newsletter` | Lettre d'information : modèle `Abonne` (migration `0008`), inscription, désinscription, export CSV (maquette + code) |
| `feature/dashboard` | Maquette du dashboard de l'équipe (pas de code) |

## Prochaines étapes (par ordre)

0. **Mise à jour d'octobre** : faire relire la branche `feature/maj-client-octobre`, la fusionner, puis `migrate` en
   production (migrations `0010` et `0011`). À confirmer avec UCIV : logo Leadership, Emmanuel Fieni Kouassi (retiré
   de l'équipe, pas de photo), prénom de « Goho Auxane », 4ᵉ partenaire, logos des partenaires, témoignages des
   autres programmes, dates des 2 nouveaux programmes.

1. **Créer le compte administrateur** sur le serveur : `ssh -t uciv-vps uciv-manage createsuperuser` (les migrations sont appliquées, les 4 branches fusionnées).
2. **Implémenter le dashboard de l'équipe** à partir de la maquette validée (nouvelle branche partie de `feature/dashboard`) : connexion, tableau de bord, gestion des articles, opportunités, ressources et chiffres d'impact, messages reçus, abonnés.
3. **Valider le mobile dans un vrai téléphone** (menu, formulaires, défilement des cartes) et décider de la tablette (720–1099 px, déduite du desktop, pas d'écran dans la maquette).
4. **Écarts de contenu restants en mobile** : 2ᵉ photo d'article (non gérée par le modèle), pagination des actualités (s'affichera avec plus d'articles), images des « histoires » de Notre impact (articles sans image en base), une seule affiche pour le lancement de Leadership (la maquette en montre deux).
5. **Bouton de recherche de l'en-tête** : décider (page de recherche ou retrait), c'est le dernier lien `#`.
6. **Textes légaux** : faire compléter et relire les passages entre crochets par UCIV.
7. **Images à fournir** : portraits HD du bureau exécutif, photos générées de la maquette, 2ᵉ image d'article.
8. **Contenus à remplacer** : fiches d'exemple (opportunités, ressources), chiffres d'impact, bios, dates et tarifs des programmes, textes des articles.
9. **Finitions** : accessibilité, Google Search Console (SEO, GEO et images WebP faits).
10. **Après la mise en ligne** : créer le compte administrateur, durcir le serveur (SSH par mot de passe, mot de passe root, `ufw`, fail2ban), configurer l'envoi des e-mails, Google Search Console (voir « Mise en ligne sur le VPS »).

Le détail de chaque page, composant, modèle et formulaire est dans [PLAN.md](PLAN.md).

## Décisions en attente

- Tablette : garder la mise en page déduite du desktop ou produire des écrans dédiés ?
- Textes légaux : compléter les passages entre crochets (forme juridique, récépissé, hébergeur, prestataire, adresse du site, durées de conservation) et faire relire.
- Bouton de recherche de l'en-tête : page de recherche ou retrait ?
- Contenus à recevoir : dates, tarifs et modalités des programmes, chiffres d'impact, bios de l'équipe, photos, URLs des réseaux sociaux.

## Reprendre le travail

```bash
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
cd src
python manage.py test app
python manage.py runserver
```

Pour lire ou modifier la maquette, ouvrir `maquette/design_uciv.pen` dans l'application
Pencil : le fichier est chiffré et ne se lit que via ses outils MCP.


