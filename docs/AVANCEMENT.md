# Avancement du projet UCIV

Point de reprise : ce qui est fait, ce qui ne l'est pas, et par où continuer.
Dernière mise à jour : 16 octobre 2026.

Documents liés : [PLAN.md](PLAN.md) (ce qu'il faut construire),
[ARCHITECTURE.md](ARCHITECTURE.md) (structure), [CLAUDE.md](../CLAUDE.md) (règles agents),
[CONTRIBUTING.md](../CONTRIBUTING.md) (workflow).

## État en un coup d'œil

| Domaine | État |
|---|---|
| Structure du projet (`src/core`, `src/app`) | Fait |
| Dépendances | Fait : Django 6.1.2 uniquement |
| Page d'accueil | Faite, alignée sur la maquette |
| Pages intérieures (14) | **14 faites** : les 9 précédentes + Opportunités, Actualités, Article, Notre impact, Ressources |
| Pages légales et 404 | **Faites** (desktop et mobile) : mentions légales, politique de confidentialité, conditions d'utilisation, page introuvable |
| Modèles de données et administration | 7 modèles administrables : 3 de formulaires (`SoumissionEngagement`, `SoumissionPartenariat`, `SoumissionContact`) et 4 de contenu (`Article`, `Opportunite`, `Ressource`, `Indicateur`) ; `MembreEquipe`, `Programme` et `Partenaire` restent dans `content.py` |
| Formulaires | 3 faits (engagement, partenariat, contact) ; newsletter à faire |
| Responsive mobile (390 px) | **Fait pour les 15 pages**, aligné sur les écrans « … — Mobile » de la maquette ; tablette déduite (720–1099 px) |
| Documentation | Faite (voir ci-dessus) |
| Mise en ligne | Non commencée |

## Ce qui est fait

### Projet
- Structure `django-init` : `src/core` (réglages, URLs, utilitaires) et `src/app` (contenu éditorial), gabarits dans `src/templates/app/`, statiques dans `src/static/app/assets/`.
- Seule dépendance : Django. Les réglages lisent `os.environ` (pas de fichier `.env` chargé automatiquement).
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

### Maquette
- `maquette/design_uciv.pen` : 16 écrans desktop et 15 écrans mobiles ; le plan de réalisation en est tiré.

## Écarts connus avec la maquette (volontaires ou à trancher)

| Élément | Maquette | Site | Décision |
|---|---|---|---|
| Chiffres d'impact | `000` | « à venir » | Garder le site : pas de faux chiffres |
| Bouton de recherche en-tête | absent | présent, sans destination | À valider ou retirer |
| Sous-menus (Programmes, S'engager) | non dessinés | présents | À valider |

## Non commité

Le travail du 16 octobre est sur `feature/responsive-mobile` (demande de fusion). Les pages légales et la 404 sont sur `feature/pages-legales`, partie de cette branche.

## Prochaines étapes (par ordre)

1. **Valider le mobile dans un vrai téléphone** (menu, formulaires, défilement des cartes) et décider de la tablette (720–1099 px, déduite du desktop, pas d'écran dans la maquette).
2. **Écarts de contenu restants en mobile** : 2ᵉ photo d'article (non gérée par le modèle), pagination des actualités (s'affichera avec plus d'articles), images des « histoires » de Notre impact (articles sans image en base), une seule affiche pour le lancement de Leadership (la maquette en montre deux).
3. **Newsletter** : brancher le formulaire du pied de page (enregistrement des adresses, désinscription).
4. **Textes légaux** : faire compléter et relire les passages entre crochets par UCIV.
5. **Images à fournir** : portraits HD du bureau exécutif, photos générées de la maquette, 2ᵉ image d'article.
6. **Contenus à remplacer** : fiches d'exemple (opportunités, ressources), chiffres d'impact, bios, dates et tarifs des programmes, textes des articles.
7. **Finitions** : accessibilité, SEO (métadonnées, `sitemap.xml`), optimisation des images.
8. **Mise en ligne** : réglages de production, `collectstatic`, hébergement.

Le détail de chaque page, composant, modèle et formulaire est dans [PLAN.md](PLAN.md).

## Décisions en attente

- Tablette : garder la mise en page déduite du desktop ou produire des écrans dédiés ?
- Newsletter : service d'envoi externe ou simple collecte d'adresses ?
- Pillow pour les images téléversées, ou chemins statiques ?
- Pages à rédiger : politique de confidentialité, mentions légales, conditions d'utilisation.
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
