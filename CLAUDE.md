# CLAUDE.md

Projet Django 6.1 (site UCIV). Structure détaillée : [ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Commandes

Depuis `src/` :

- Lancer : `python manage.py runserver`
- Tester : `python manage.py test app` (à passer avant chaque commit)
- Vérifier : `python manage.py check`

## Règles

- **Dépendances** : Django et Pillow (traitement des images). N'ajoute aucun autre paquet dans `requirements.txt` sans accord explicite.
- **Configuration** : variables d'environnement via `config()` de `core/settings.py`. Pas de secret dans le code ni dans git.
- **Contenu éditorial** : textes, navigation, programmes et articles vivent dans `src/app/content.py`, pas dans les gabarits.
- **Gabarits** : héritent de `app/base/base.html`. Les fragments réutilisables vont dans `templates/app/includes/`.
- **Statiques** : `src/static/app/assets/{css,js,img}`. Référence-les avec `{% static 'app/assets/...' %}`.
- **Images** : dépose l'original dans `sources/images/` puis lance `python outils/convertir_images.py` (WebP de moins de 200 Ko servis depuis `src/static/app/assets/img/`). Ne mets jamais un original lourd dans `static/`.
- **Modèles publiables** : héritent de `Convention` (`app/models.py`).
- **Langue** : code, commentaires, messages de commit et textes du site en français.

## Maquette

- Le design est `maquette/design_uciv.pen`. Les fichiers `.pen` sont chiffrés : ne les lis jamais avec Read ou Grep, uniquement via les outils MCP Pencil.
- Les couleurs, polices et espacements viennent de l'écran « Fondations — direction artistique ». Ne les invente pas.

## Git

- Ne commite et ne pousse que sur demande explicite.
- Jamais de `--force` ni de réécriture d'historique sans confirmation.
- Ne versionne pas `.env`, `db.sqlite3`, `static_cdn/`, `media_cdn/`.

## Mise à jour de la documentation

Si tu changes la structure du projet, mets à jour `docs/ARCHITECTURE.md` dans le même commit.

À chaque étape terminée (page, modèle, formulaire…), mets à jour `docs/AVANCEMENT.md`
(tableau d'état, « Ce qui est fait », « Prochaines étapes », date). `docs/PLAN.md` décrit
ce qu'il faut construire ; `docs/AVANCEMENT.md` dit où l'on en est.
