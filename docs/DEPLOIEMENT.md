# Déploiement : passage sur MySQL

Le site tourne par défaut sur SQLite (développement). En production, il utilise MySQL.
Ce document décrit le passage sur la base installée sur le VPS (`uciv`, accessible seulement en local sur le serveur).

## Ce qui est déjà en place sur le serveur

- MySQL 8.4, écoute sur `127.0.0.1:3306` uniquement (non exposé à Internet).
- Base `uciv` (utf8mb4) et utilisateur `uciv_user` (droits sur cette base seulement).
- phpMyAdmin : https://bd.uciv.org (voir `deploy/phpmyadmin.sh`).
- Identifiants : `/root/identifiants-mysql.txt` sur le serveur. **Ne jamais les mettre dans git.**

## Préparer le serveur (une fois)

```bash
sudo apt install -y python3-venv python3-dev default-libmysqlclient-dev build-essential pkg-config
cd /chemin/du/projet
python3 -m venv venv
venv/bin/pip install -r requirements-mysql.txt     # Django + mysqlclient
```

`requirements.txt` reste limité à Django ; `requirements-mysql.txt` ajoute `mysqlclient`, nécessaire seulement avec MySQL.

## Variables d'environnement

Le site ne lit pas de fichier `.env` tout seul : les variables doivent être fournies au service qui lance Django
(par exemple `EnvironmentFile=/etc/uciv/uciv.env` dans systemd, fichier lisible par root seulement : `chmod 600`).

```
SECRET_KEY=<longue clé aléatoire : python -c "import secrets; print(secrets.token_urlsafe(50))">
DEBUG=False
ALLOWED_HOSTS=uciv.org,www.uciv.org
CSRF_TRUSTED_ORIGINS=https://uciv.org,https://www.uciv.org
USE_MYSQL=True
MYSQL_DB=uciv
MYSQL_USER=uciv_user
MYSQL_PASSWORD=<mot de passe de uciv_user>
MYSQL_HOST=localhost
MYSQL_PORT=3306
CONTACT_EMAIL=organisationuciv@gmail.com
```

`MYSQL_SSL_MODE` reste vide : la base est sur la même machine. Si elle devient distante, mettre `REQUIRED`.
Les variables `EMAIL_*` activent l'envoi des messages des formulaires (voir `.env.example`).

## Créer les tables

Avec les variables chargées, depuis `src/` :

```bash
../venv/bin/python manage.py check --database default      # vérifie la connexion et les réglages
../venv/bin/python manage.py migrate                        # crée les tables + contenu de départ
../venv/bin/python manage.py createsuperuser                # compte pour /admin/
../venv/bin/python manage.py collectstatic --noinput
```

`migrate` charge aussi le contenu de départ (articles, indicateurs, fiches d'exemple) : inutile de reprendre la base
SQLite de développement, qui ne contient que des données de test.

## Vérifier

1. `/admin/` : connexion avec le compte créé, les modèles « Site UCIV » sont visibles.
2. Envoyer le formulaire de contact : la ligne apparaît dans phpMyAdmin (table `app_soumissioncontact`).
3. Les pages Actualités, Opportunités, Ressources et Notre impact affichent le contenu de départ.

## Reprendre des données de SQLite (seulement si nécessaire)

```bash
# sur la machine de développement, avec la base SQLite
python manage.py dumpdata app auth.user --natural-foreign --natural-primary --indent 2 > donnees.json
# sur le serveur, après migrate
../venv/bin/python manage.py loaddata donnees.json
```

Attention : le contenu de départ créé par `migrate` existe déjà côté MySQL ; chargez de préférence un export limité à
ce qui a été saisi à la main (messages de formulaires, articles ajoutés) pour éviter les doublons.

## Sauvegardes

```bash
mysqldump -u uciv_user -p --single-transaction uciv > uciv_$(date +%F).sql
```

À automatiser (cron, une fois par nuit) et à copier **hors du serveur**. Restauration : `mysql -u uciv_user -p uciv < sauvegarde.sql`.

## Incidents fréquents

| Symptôme | Cause probable |
|---|---|
| `ModuleNotFoundError: No module named 'MySQLdb'` | `requirements-mysql.txt` non installé dans l'environnement virtuel |
| Échec de `pip install mysqlclient` | Paquets système manquants (`default-libmysqlclient-dev`, `build-essential`) |
| `Access denied for user 'uciv_user'` | Mauvais mot de passe dans `MYSQL_PASSWORD` |
| `Can't connect to MySQL server` | Service arrêté (`systemctl status mysql`) ou mauvais `MYSQL_HOST` |
| Boucle de redirections HTTPS | `DEBUG=False` sans l'en-tête `X-Forwarded-Proto` transmis par Nginx |
| Erreur 403 CSRF sur les formulaires | `CSRF_TRUSTED_ORIGINS` absent ou sans le schéma `https://` |

## Étape suivante (pas encore préparée)

Servir le site lui-même sur `uciv.org` : service Gunicorn, bloc Nginx (fichiers statiques et médias), HTTPS.
