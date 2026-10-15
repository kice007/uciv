# Avancement du projet UCIV

Point de reprise : ce qui est fait, ce qui ne l'est pas, et par où continuer.
Dernière mise à jour : 14 octobre 2026.

Documents liés : [PLAN.md](PLAN.md) (ce qu'il faut construire),
[ARCHITECTURE.md](ARCHITECTURE.md) (structure), [CLAUDE.md](../CLAUDE.md) (règles agents),
[CONTRIBUTING.md](../CONTRIBUTING.md) (workflow).

## État en un coup d'œil

| Domaine | État |
|---|---|
| Structure du projet (`src/core`, `src/app`) | Fait |
| Dépendances | Fait : Django 6.1.2 uniquement |
| Page d'accueil | Faite, alignée sur la maquette |
| Pages intérieures (14) | 9 faites (UCIV Leadership, Qui sommes-nous ?, Nos programmes, Les Go du Digital, Experience Lab, Équipe, Je veux m'engager, Partenaires, Contact), 5 à faire |
| Modèles de données et administration | 3 modèles (`SoumissionEngagement`, `SoumissionPartenariat`, `SoumissionContact`) et leur administration ; le reste à faire |
| Formulaires | 3 faits (engagement, partenariat, contact) ; newsletter à faire |
| Responsive mobile/tablette | Fait pour l'accueil seulement |
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

### Maquette
- `maquette/design_uciv.pen` : 16 écrans desktop analysés ; le plan de réalisation en est tiré.

## Écarts connus avec la maquette (volontaires ou à trancher)

| Élément | Maquette | Site | Décision |
|---|---|---|---|
| Chiffres d'impact | `000` | « à venir » | Garder le site : pas de faux chiffres |
| Bouton de recherche en-tête | absent | présent, sans destination | À valider ou retirer |
| Sous-menus (Programmes, S'engager) | non dessinés | présents | À valider |

## Non commité

Les fichiers suivants sont dans le dossier de travail mais pas dans git :
`README.md`, `CLAUDE.md`, `CONTRIBUTING.md`, le dossier `docs/` (`PLAN.md`, `AVANCEMENT.md`), le dossier `maquette/`
(le `.pen` pèse 1,6 Mo), et les modifications des titres dans `main.css` et `index.html`.

## Prochaines étapes (par ordre)

1. **Commiter** les documents et la correction des titres.
2. **Socle des pages intérieures** : gabarit `app/base/page.html` (hero + contenu + appel), fil d'Ariane, état « page active » de la navigation, includes (appel, citation, repères, liste numérotée).
3. **Pages statiques** : Qui sommes-nous, Nos programmes, Les Go du Digital, UCIV Leadership, Experience Lab.
4. **Modèles et administration** : `Article`, `Opportunite`, `Ressource`, `MembreEquipe`, `Indicateur` ; migrer `content.py`.
5. **Pages dynamiques** : Actualités, Article, Opportunités, Ressources, Équipe, Notre impact.
6. **Formulaires** : engagement, partenariat, contact, newsletter (et envoi d'e-mails).
7. **Finitions** : accessibilité, SEO, images, page 404, pages légales.
8. **Mise en ligne** : réglages de production, `collectstatic`, hébergement.

Le détail de chaque page, composant, modèle et formulaire est dans [PLAN.md](PLAN.md).

## Décisions en attente

- Responsive : produire des écrans mobile/tablette ou déduire du desktop ?
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
