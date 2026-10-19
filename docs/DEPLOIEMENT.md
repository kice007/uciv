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
SITE_URL=https://uciv.org
ADMIN_URL=back-office
USE_MYSQL=True
MYSQL_DB=uciv
MYSQL_USER=uciv_user
MYSQL_PASSWORD=<mot de passe de uciv_user>
MYSQL_HOST=localhost
MYSQL_PORT=3306
CONTACT_EMAIL=organisationuciv@gmail.com
```

En production (`DEBUG=False`), Django **refuse de démarrer** si `SECRET_KEY` fait moins de 50 caractères (ou garde une valeur
par défaut) ou si `ALLOWED_HOSTS` est vide ou contient `*`. `HSTS_SECONDS` (1 jour par défaut) règle la durée pendant laquelle
le navigateur impose le HTTPS : une fois le HTTPS vérifié sur `uciv.org`, mettre `31536000` (1 an) dans `/etc/uciv/uciv.env`.

`MYSQL_SSL_MODE` reste vide : la base est sur la même machine. Si elle devient distante, mettre `REQUIRED`.
**`ADMIN_URL`** est l'adresse de l'administration : `https://uciv.org/back-office/` quand la variable est absente ou vide. Django refuse `admin` en production (l'adresse la plus attaquée). Pour une adresse plus difficile à deviner, ajoutez par exemple `ADMIN_URL=gestion-3fa9c1d27b4e` dans `/etc/uciv/uciv.env` puis `sudo systemctl restart uciv` ; `deploy/deployer.sh` la reprend pour ses vérifications.

Les variables `EMAIL_*` activent l'envoi des messages des formulaires (voir `.env.example`).

## Limite de débit et cache

Les envois de formulaires sont limités par `app/ratelimit.py` (5 par formulaire et par adresse IP toutes les 10 minutes ; connexion à l'administration : 10 essais par IP et 5 par identifiant toutes les 15 minutes) et, devant Django, par Nginx (20 envois par minute et par IP). Les compteurs de Django sont stockés dans le dossier `src/cache_cdn/` (cache de fichiers, partagé entre les processus Gunicorn) ; `CACHE_DIR` permet de le déplacer. Le service ayant déjà le droit d'écrire dans `/srv/uciv`, rien d'autre à préparer. Pour remettre les compteurs à zéro (par exemple après un blocage par erreur) : `sudo uciv-manage shell -c "from django.core.cache import cache; cache.clear()"`.

## Créer les tables

Avec les variables chargées, depuis `src/` :

```bash
../venv/bin/python manage.py check --database default      # vérifie la connexion et les réglages
../venv/bin/python manage.py migrate                        # crée les tables + contenu de départ
../venv/bin/python manage.py createsuperuser                # compte pour l'administration
../venv/bin/python manage.py collectstatic --noinput
```

`migrate` charge aussi le contenu de départ (articles, indicateurs, fiches d'exemple) : inutile de reprendre la base
SQLite de développement, qui ne contient que des données de test.

## Vérifier

1. `/back-office/` : connexion avec le compte créé, les modèles « Site UCIV » sont visibles.
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

## Connexion au serveur par clé SSH

Le déploiement se fait avec une clé SSH dédiée, sans mot de passe.

| Élément | Valeur |
|---|---|
| Clé privée | `~/.ssh/uciv_deploy` sur le poste de déploiement (**ne jamais la copier dans git ni l'envoyer**) |
| Clé publique | `~/.ssh/uciv_deploy.pub`, installée dans `/root/.ssh/authorized_keys` du serveur |
| Type | ed25519 (empreinte `SHA256:1+ZzILt34+3B8gWt4yckYTYcACInJO6s6VciDdC2NA4`) |
| Raccourci | `ssh uciv-vps` (défini dans `~/.ssh/config`) |

Avec le raccourci, les commandes de ce document deviennent par exemple :

```bash
scp deploy/deployer.sh uciv-vps:/root/
ssh uciv-vps "bash /root/deployer.sh votre@email.com"
```

### Autoriser un autre poste ou un autre développeur

Chaque personne crée **sa propre** clé (`ssh-keygen -t ed25519 -C "prenom-uciv"`) et envoie uniquement le fichier `.pub` ;
un administrateur l'ajoute à `/root/.ssh/authorized_keys`. Ne partagez jamais une clé privée.

### Retirer un accès

Supprimer la ligne correspondante de `/root/.ssh/authorized_keys` (le commentaire en fin de ligne, par exemple
`deploiement-uciv`, identifie la clé).

### Renforcer le serveur (recommandé, une fois la connexion par clé testée)

1. Garder **une session ouverte** pendant toute l'opération, pour ne pas se retrouver bloqué.
2. Éditer `/etc/ssh/sshd_config.d/` (ou `/etc/ssh/sshd_config`) : `PasswordAuthentication no` et `PermitRootLogin prohibit-password`.
3. Vérifier la configuration (`sshd -t`), puis `systemctl reload ssh`.
4. Dans une **seconde** fenêtre, tester `ssh uciv-vps` avant de fermer la première.
5. Changer le mot de passe `root` (`passwd`) : il ne sert plus qu'en secours via la console de l'hébergeur.
6. Facultatif : activer `ufw` en autorisant d'abord `OpenSSH`, puis `Nginx Full`.

### Protéger la clé privée

La clé n'a pas de phrase secrète pour permettre un déploiement automatisé. Elle doit donc rester sur un poste de
confiance, avec un disque chiffré. Pour ajouter une phrase secrète : `ssh-keygen -p -f ~/.ssh/uciv_deploy`
(le déploiement demandera alors la phrase, ou un agent SSH la retiendra).

## Déployer le site sur uciv.org (Gunicorn + Nginx + HTTPS)

Tout est automatisé par [`deploy/deployer.sh`](../deploy/deployer.sh), à lancer **en root sur le serveur**. Il est relançable :
la première fois il installe tout, ensuite il sert de mise à jour.

### Prérequis

- Le DNS de `uciv.org` pointe vers le VPS (c'est le cas). `www.uciv.org` n'a pas d'enregistrement : ajoutez un `CNAME www -> uciv.org`
  chez votre registrar si vous voulez qu'il fonctionne ; le script l'inclut automatiquement dès qu'il existe.
- MySQL et la base `uciv` sont en place, avec `/root/identifiants-mysql.txt` (voir `deploy/phpmyadmin.sh`).
- Les ports 80 et 443 sont ouverts chez l'hébergeur et sur le serveur.
- Le dépôt GitHub est accessible depuis le serveur. S'il est privé : `DEPOT_URL=https://UTILISATEUR:JETON@github.com/kice007/uciv.git`.

### Lancer

```bash
scp deploy/deployer.sh root@213.130.144.126:/root/
ssh root@213.130.144.126 "bash /root/deployer.sh votre@email.com"
ssh root@213.130.144.126 "uciv-manage createsuperuser"      # une seule fois : compte pour /admin/
```

### Ce que fait le script

1. Installe les paquets système (Git, outils de compilation, bibliothèque MySQL, Nginx, Certbot).
2. Crée l'utilisateur système `uciv` (sans connexion) et clone le dépôt dans `/srv/uciv`.
3. Crée l'environnement Python (`/srv/uciv/venv`) et installe `requirements-prod.txt` (Django, `mysqlclient`, `gunicorn`).
4. Crée `/etc/uciv/uciv.env` (lisible par root seulement) : clé secrète générée, `DEBUG=False`, hôtes autorisés, `USE_MYSQL=True`,
   mot de passe de la base lu dans `/root/identifiants-mysql.txt`. Un fichier existant n'est jamais écrasé.
5. Installe la commande `uciv-manage` (équivalent de `manage.py` avec l'environnement de production).
6. Lance `check`, `migrate` et `collectstatic`.
7. Installe le service systemd `uciv` (Gunicorn, 3 processus, socket `/run/uciv/gunicorn.sock`), redémarré automatiquement en cas d'échec.
8. Configure Nginx : `/static/` et `/media/` servis directement, le reste transmis à Django.
9. Obtient le certificat Let's Encrypt (renouvelé automatiquement) et redirige HTTP vers HTTPS.

Il se termine par six vérifications (accueil, administration, `/admin/` qui doit répondre 404, actualités, feuille de style, redirection).

### Mettre à jour le site

Après un `git push` sur `main` : `ssh root@213.130.144.126 "bash /root/deployer.sh"`.
Le script récupère le code, installe les dépendances, applique les migrations, regroupe les fichiers statiques et redémarre Gunicorn.
La configuration Nginx et le certificat ne sont pas modifiés.

### Commandes utiles sur le serveur

| Besoin | Commande |
|---|---|
| Journaux du site | `journalctl -u uciv -f` |
| Redémarrer le site | `systemctl restart uciv` |
| Commande Django | `uciv-manage <commande>` (ex. `uciv-manage migrate`) |
| Journaux Nginx | `tail -f /var/log/nginx/error.log` |
| État du certificat | `certbot certificates` |

### Fichiers téléversés (médias)

Les images téléversées depuis l'administration vont dans `/srv/uciv/src/media_cdn/` et sont servies par Nginx sous `/media/`.
Ce dossier n'est pas dans git : **incluez-le dans vos sauvegardes**, avec la base de données.

### Si quelque chose ne marche pas

| Symptôme | Cause probable |
|---|---|
| 502 Bad Gateway | Gunicorn arrêté : `systemctl status uciv` puis `journalctl -u uciv -n 50` |
| 400 Bad Request | Domaine absent de `ALLOWED_HOSTS` dans `/etc/uciv/uciv.env` (puis `systemctl restart uciv`) |
| 403 sur un formulaire | `CSRF_TRUSTED_ORIGINS` sans le schéma `https://` |
| Page sans style | `collectstatic` non lancé, ou droits de lecture de `/srv/uciv/src/static_cdn` |
| Échec de l'étape 9 | Port 80 bloqué ou DNS pas encore propagé : corrigez, puis relancez le script |
