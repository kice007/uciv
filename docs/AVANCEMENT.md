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
| Pages intérieures (14) | 3 faites (UCIV Leadership, Qui sommes-nous ?, Nos programmes), 11 à faire |
| Modèles de données et administration | Non commencés |
| Formulaires | Non commencés |
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
