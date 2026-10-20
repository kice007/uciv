# Architecture — UCIV

Site de l'association Une Côte d'Ivoire Volontaire (UCIV). Projet Django 6.1,
sans dépendance tierce : `requirements.txt` ne contient que Django.

```
.
├── .gitignore
├── .env.example          # variables d'environnement (lues via os.environ)
├── requirements.txt      # Django et Pillow
├── requirements-mysql.txt  # + mysqlclient (production)
├── deploy/               # scripts serveur (phpMyAdmin)
├── outils/               # convertir_images.py : originaux vers WebP (Pillow)
├── sources/images/       # images originales (non servies)
├── README.md · CLAUDE.md · CONTRIBUTING.md
├── docs/             # ARCHITECTURE.md, PLAN.md, AVANCEMENT.md
├── maquette/         # design_uciv.pen (maquette Pencil)
└── src/
    ├── manage.py
    ├── core/             # configuration du projet
    │   ├── settings.py   # réglages ; config() lit os.environ
    │   ├── urls.py       # admin + app.urls + médias/statiques, handler404 (aperçu /404/ en DEBUG)
    │   ├── wsgi.py / asgi.py
    │   ├── constants.py  # constantes (chemins d'upload…)
    │   └── utils.py      # envoi d'e-mails, get_ip()
    ├── app/              # contenu éditorial du site
    │   ├── content.py            # textes, navigation, programmes (dont PROGRAMMES_LEADERSHIP), équipe, formes des heros (FORMES_HEROS)
    │   ├── context_processors.py # variables communes (navigation, pied de page)
    │   ├── models.py             # Convention (abstrait), 3 modèles de formulaires, Article, Opportunite, Ressource, Indicateur, Abonne (lettre d'information)
    │   ├── forms.py              # formulaires (Engagement, Partenariat, Contact, Newsletter)
    │   ├── migrations/           # migrations de la base
    │   ├── admin.py              # administration Django
    │   ├── validators.py         # contrôle des fichiers téléversés (extensions, 10 Mo)
    │   ├── ratelimit.py          # limiteur de débit des formulaires et de la connexion (429)
    │   ├── seo.py                # SEO et GEO : balises, JSON-LD, robots.txt, sitemap, llms.txt
    │   ├── views.py / urls.py    # toutes les pages, namespace « app » ; programme_leadership (2 pages), recherche, page_legale, page_introuvable (404)
    │   ├── templatetags/custom_tags.py  # filtres corps_article et crochets ; balise formes_hero (forme UCIV des heros)
    │   ├── templatetags/uciv_admin.py   # menu et chiffres du tableau de bord de l'administration
    │   └── tests.py
    ├── templates/
    │   ├── app/base/base.html     # gabarit de base
    │   ├── app/layout/            # une page par gabarit ; legal.html (3 pages légales), programme_leadership.html (2 programmes), recherche.html, 404.html, desinscription.html
    │   ├── app/includes/          # en-tête, pied de page, icônes, _formes_uciv, _temoignages, _galerie
    │   ├── admin/base_site.html   # habillage UCIV de l'administration
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
