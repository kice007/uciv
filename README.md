# UCIV — Une Côte d'Ivoire Volontaire

Site web de l'association UCIV : mobiliser la jeunesse par le volontariat et
l'engagement citoyen. Projet Django 6.1, sans dépendance tierce.

## Démarrage

```bash
python -m venv venv
venv\Scripts\activate          # Windows (source venv/bin/activate sous Linux/macOS)
pip install -r requirements.txt
cd src
python manage.py migrate
python manage.py runserver
```

Le site est alors disponible sur http://127.0.0.1:8000/.

## Configuration

Les réglages passent par des variables d'environnement (voir `.env.example`).
Les valeurs par défaut suffisent en local (SQLite, `DEBUG=True`).

## Tests

```bash
cd src
python manage.py test app
```

## Pour aller plus loin

| Document | Contenu |
|---|---|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Structure des dossiers et conventions |
| [docs/PLAN.md](docs/PLAN.md) | Ce qu'il faut construire, d'après la maquette |
| [docs/AVANCEMENT.md](docs/AVANCEMENT.md) | Ce qui est fait, ce qui reste, point de reprise |
| [docs/GEO.md](docs/GEO.md) | Être cité par les moteurs de réponse IA : état, règles de rédaction, actions |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Workflow git, commits, relecture |
| [CLAUDE.md](CLAUDE.md) | Règles pour les agents IA (Claude Code) |

La maquette est dans `maquette/design_uciv.pen` (à ouvrir avec Pencil).
