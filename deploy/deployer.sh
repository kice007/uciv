#!/bin/bash
# Déploie (ou met à jour) le site UCIV sur le VPS : Gunicorn + Nginx + HTTPS, base MySQL locale.
#
# Usage, en root sur le serveur (relançable à volonté : une mise à jour = relancer le script) :
#   bash deployer.sh [adresse_e-mail_pour_le_certificat]
#
# Variables facultatives :
#   DEPOT_URL   dépôt git à cloner (défaut : https://github.com/kice007/uciv.git ;
#               dépôt privé : https://UTILISATEUR:JETON@github.com/kice007/uciv.git)
#   BRANCHE     branche à déployer (défaut : main)
#   DOMAINE     domaine principal (défaut : uciv.org)
#
# Prérequis : MySQL installé avec la base « uciv » (voir deploy/phpmyadmin.sh) et le fichier
# /root/identifiants-mysql.txt. Le script ne contient aucun secret : la clé Django est générée ici
# et le mot de passe de la base est lu dans ce fichier.
set -euo pipefail

DEPOT_URL="${DEPOT_URL:-https://github.com/kice007/uciv.git}"
BRANCHE="${BRANCHE:-main}"
DOMAINE="${DOMAINE:-uciv.org}"
EMAIL="${1:-}"
RACINE=/srv/uciv
ENV_FILE=/etc/uciv/uciv.env
export DEBIAN_FRONTEND=noninteractive

echo "== 1/9 Paquets système"
apt-get update -qq
apt-get install -y git python3-venv python3-dev default-libmysqlclient-dev build-essential pkg-config \
    nginx certbot python3-certbot-nginx >/dev/null

echo "== 2/9 Utilisateur système « uciv » et code source"
id uciv >/dev/null 2>&1 || adduser --system --group --home "${RACINE}" --shell /usr/sbin/nologin uciv
mkdir -p "${RACINE}" && chown uciv:uciv "${RACINE}"
if [ -d "${RACINE}/.git" ]; then
    sudo -u uciv git -C "${RACINE}" fetch --quiet origin "${BRANCHE}"
    sudo -u uciv git -C "${RACINE}" checkout --quiet "${BRANCHE}"
    sudo -u uciv git -C "${RACINE}" pull --quiet --ff-only origin "${BRANCHE}"
else
    sudo -u uciv git clone --quiet --branch "${BRANCHE}" "${DEPOT_URL}" "${RACINE}"
fi
echo "   version déployée : $(sudo -u uciv git -C "${RACINE}" log -1 --format='%h %s')"

echo "== 3/9 Environnement Python"
[ -x "${RACINE}/venv/bin/python" ] || sudo -u uciv python3 -m venv "${RACINE}/venv"
sudo -u uciv "${RACINE}/venv/bin/pip" install -q --upgrade pip
sudo -u uciv "${RACINE}/venv/bin/pip" install -q -r "${RACINE}/requirements-prod.txt"

echo "== 4/9 Variables d'environnement (${ENV_FILE})"
if [ ! -f "${ENV_FILE}" ]; then
    [ -f /root/identifiants-mysql.txt ] || { echo "Fichier /root/identifiants-mysql.txt introuvable."; exit 1; }
    PW_SITE=$(awk '/uciv_user/{f=1} f&&/mot de passe/{print $NF; exit}' /root/identifiants-mysql.txt)
    [ -n "${PW_SITE}" ] || { echo "Mot de passe de uciv_user introuvable."; exit 1; }
    CLE=$(openssl rand -base64 96 | tr -dc 'A-Za-z0-9' | head -c 64)
    HOTES="${DOMAINE}"
    ORIGINES="https://${DOMAINE}"
    if getent hosts "www.${DOMAINE}" >/dev/null; then
        HOTES="${HOTES},www.${DOMAINE}"
        ORIGINES="${ORIGINES},https://www.${DOMAINE}"
    fi
    mkdir -p /etc/uciv
    umask 077
    cat > "${ENV_FILE}" <<ENV
SECRET_KEY=${CLE}
DEBUG=False
ALLOWED_HOSTS=${HOTES}
CSRF_TRUSTED_ORIGINS=${ORIGINES}
SITE_URL=https://${DOMAINE}
USE_MYSQL=True
MYSQL_DB=uciv
MYSQL_USER=uciv_user
MYSQL_PASSWORD=${PW_SITE}
MYSQL_HOST=localhost
MYSQL_PORT=3306
CONTACT_EMAIL=organisationuciv@gmail.com
ENV
    chown root:root "${ENV_FILE}" && chmod 600 "${ENV_FILE}"
    echo "   fichier créé (lisible par root seulement)"
else
    echo "   fichier existant conservé"
fi
# Adresse de l'administration : ADMIN_URL du fichier d'environnement si elle existe, sinon /back-office/
ADMIN_URL=$(grep '^ADMIN_URL=' "${ENV_FILE}" | cut -d= -f2 || true)
ADMIN_URL=${ADMIN_URL:-back-office}

echo "== 5/9 Commande d'administration « uciv-manage »"
cat > /usr/local/bin/uciv-manage <<'MANAGE'
#!/bin/bash
# Lance manage.py avec l'environnement de production : uciv-manage createsuperuser, uciv-manage migrate, ...
set -a; . /etc/uciv/uciv.env; set +a
cd /srv/uciv/src
exec sudo -E -u uciv /srv/uciv/venv/bin/python manage.py "$@"
MANAGE
chmod 755 /usr/local/bin/uciv-manage

echo "== 6/9 Vérification, migrations, fichiers statiques"
uciv-manage check --database default
uciv-manage migrate --noinput
uciv-manage collectstatic --noinput | tail -1
install -d -o uciv -g www-data -m 750 "${RACINE}/src/media_cdn"
chmod 755 "${RACINE}" "${RACINE}/src"
chmod -R a+rX "${RACINE}/src/static_cdn"

echo "== 7/9 Service Gunicorn"
cp "${RACINE}/deploy/gunicorn-uciv.service" /etc/systemd/system/uciv.service
systemctl daemon-reload
systemctl enable uciv >/dev/null 2>&1
systemctl restart uciv
sleep 2
systemctl is-active uciv

echo "== 8/9 Nginx"
if [ ! -f /etc/nginx/sites-available/uciv ]; then
    NOMS="${DOMAINE}"
    getent hosts "www.${DOMAINE}" >/dev/null && NOMS="${NOMS} www.${DOMAINE}"
    sed "s/__NOMS_DU_SITE__/${NOMS}/" "${RACINE}/deploy/nginx-uciv.conf" > /etc/nginx/sites-available/uciv
else
    echo "   configuration existante conservée (elle contient déjà les réglages HTTPS de certbot)"
fi
ln -sf /etc/nginx/sites-available/uciv /etc/nginx/sites-enabled/uciv
nginx -t
systemctl reload nginx

echo "== 9/9 HTTPS"
if [ -d "/etc/letsencrypt/live/${DOMAINE}" ]; then
    echo "   certificat déjà présent, rien à faire (certbot le renouvelle seul)"
else
    CERT_OPTS="--register-unsafely-without-email"
    [ -n "${EMAIL}" ] && CERT_OPTS="-m ${EMAIL}"
    DOMAINES="-d ${DOMAINE}"
    getent hosts "www.${DOMAINE}" >/dev/null && DOMAINES="${DOMAINES} -d www.${DOMAINE}"
    certbot --nginx ${DOMAINES} --non-interactive --agree-tos ${CERT_OPTS} --redirect
fi

echo
echo "== Vérifications"
sleep 2
curl -s -o /dev/null -w "https://${DOMAINE}/             : HTTP %{http_code} (200 attendu)\n" "https://${DOMAINE}/"
curl -s -o /dev/null -w "administration                : HTTP %{http_code} (200 attendu)\n" "https://${DOMAINE}/${ADMIN_URL}/login/"
curl -s -o /dev/null -w "ancienne adresse /admin/      : HTTP %{http_code} (404 attendu)\n" "https://${DOMAINE}/admin/login/"
curl -s -o /dev/null -w "https://${DOMAINE}/actualites/  : HTTP %{http_code} (200 attendu)\n" "https://${DOMAINE}/actualites/"
curl -s -o /dev/null -w "feuille de style             : HTTP %{http_code} (200 attendu)\n" "https://${DOMAINE}/static/app/assets/css/main.css"
curl -s -o /dev/null -w "http -> https                : HTTP %{http_code} (301 attendu)\n" "http://${DOMAINE}/"
echo
echo "Site déployé. Étape suivante (une seule fois) : créer le compte administrateur :"
echo "    uciv-manage createsuperuser"
echo "Administration : https://${DOMAINE}/${ADMIN_URL}/"
echo "Mise à jour ultérieure : relancer « bash deployer.sh »."
echo "Journaux : journalctl -u uciv -f"
