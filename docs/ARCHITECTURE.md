# Architecture — UCIV

Site de l'association Une Côte d'Ivoire Volontaire (UCIV). Projet Django 6.1,
sans dépendance tierce : `requirements.txt` ne contient que Django.

```
.
├── .gitignore
├── .env.example          # variables d'environnement (lues via os.environ)
├── requirements.txt      # Django uniquement
├── README.md · CLAUDE.md · CONTRIBUTING.md
├── docs/             # ARCHITECTURE.md, PLAN.md, AVANCEMENT.md
├── maquette/         # design_uciv.pen (maquette Pencil)
└── src/
    ├── manage.py
    ├── core/             # configuration du projet
    │   ├── settings.py   # réglages ; config() lit os.environ
    │   ├── urls.py       # admin + app.urls + médias/statiques
    │   ├── wsgi.py / asgi.py
    │   ├── constants.py  # constantes (chemins d'upload…)
    │   └── utils.py      # envoi d'e-mails, get_ip()
    ├── app/              # contenu éditorial du site
    │   ├── content.py            # textes, navigation, programmes, articles
    │   ├── context_processors.py # variables communes (navigation, pied de page)
    │   ├── models.py             # Convention (abstrait), SoumissionEngagement, SoumissionPartenariat, SoumissionContact
    │   ├── forms.py              # formulaires (Engagement, Partenariat, Contact)
    │   ├── migrations/           # migrations de la base
    │   ├── admin.py              # administration Django
    │   ├── views.py / urls.py    # page d'accueil, namespace « app »
    │   ├── templatetags/custom_tags.py
    │   └── tests.py
    ├── templates/
    │   ├── app/base/base.html     # gabarit de base
    │   ├── app/layout/index.html  # page d'accueil
    │   ├── app/includes/          # en-tête, pied de page, icônes
    │   └── emails/                # gabarits d'e-mails
    ├── static/app/assets/{css,js,img}
    ├── static_cdn/       # collectstatic (non versionné)
    ├── media_cdn/        # uploads (non versionné)
    └── data/
```

## Conventions

- `core/` = configuration ; `app/` = contenu éditorial. Les futures apps métier
  vivent dans leurs propres dossiers, à côté de `app/`.
- Les modèles publiables héritent de `Convention` (`created_at`, `update_at`, `publish`).
- Configuration par variables d'environnement (voir `.env.example`) : SQLite par
  défaut, MySQL avec `USE_MYSQL=True`.
- Les contenus sont pour l'instant dans `app/content.py` ; ils passeront en base
  de données (modèles + admin) quand l'équipe devra les modifier.
- Ne pas versionner `.env`, `db.sqlite3`, `static_cdn/`, `media_cdn/`.

## Lancer le projet

```bash
pip install -r requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```
