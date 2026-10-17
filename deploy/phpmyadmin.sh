#!/bin/bash
# Installe et sécurise phpMyAdmin sur bd.uciv.org (Ubuntu, MySQL 8.4, Nginx, PHP-FPM déjà installés).
#
# Usage, en root sur le serveur :
#   bash phpmyadmin.sh [adresse_e-mail_pour_le_certificat]
#
# - crée la base « uciv », l'utilisateur du site « uciv_user » et le compte d'administration « admin_pma »
#   (mots de passe aléatoires, enregistrés dans /root/identifiants-mysql.txt, lisible par root seulement) ;
# - publie phpMyAdmin sur https://bd.uciv.org derrière une première barrière (mot de passe Nginx) ;
# - obtient un certificat Let's Encrypt (renouvellement automatique) ;
# - interdit la connexion « root » à phpMyAdmin.
#
# Le script ne contient aucun mot de passe : tout est généré sur le serveur.
set -euo pipefail

DOMAINE="bd.uciv.org"
EMAIL="${1:-}"
PHP_SOCKET="$(ls /run/php/php*-fpm.sock | grep -v 'php-fpm.sock' | head -1)"

gen() { openssl rand -base64 96 | tr -dc 'A-Za-z0-9' | head -c "${1:-28}"; }
PW_SITE=$(gen 28)
PW_PMA=$(gen 28)
PW_WEB=$(gen 24)

echo "== 1/6 Base, utilisateur du site et compte d'administration"
mysql <<SQL
CREATE DATABASE IF NOT EXISTS uciv CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'uciv_user'@'localhost' IDENTIFIED BY '${PW_SITE}';
GRANT ALL PRIVILEGES ON uciv.* TO 'uciv_user'@'localhost';
CREATE USER IF NOT EXISTS 'admin_pma'@'localhost' IDENTIFIED BY '${PW_PMA}';
GRANT ALL PRIVILEGES ON *.* TO 'admin_pma'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
SQL
mysql -u uciv_user -p"${PW_SITE}" uciv -e "SELECT 'uciv_user OK' AS test;" 2>/dev/null
mysql -u admin_pma -p"${PW_PMA}" -e "SELECT 'admin_pma OK' AS test;" 2>/dev/null

echo "== 2/6 Durcissement de phpMyAdmin"
mkdir -p /etc/phpmyadmin/conf.d
cat > /etc/phpmyadmin/conf.d/securite.php <<PHP
<?php
\$cfg['blowfish_secret'] = '$(gen 48)';
\$cfg['Servers'][1]['AllowRoot'] = false;
\$cfg['Servers'][1]['AllowNoPassword'] = false;
\$cfg['LoginCookieValidity'] = 1800;
\$cfg['ExecTimeLimit'] = 300;
PHP
chgrp www-data /etc/phpmyadmin/conf.d/securite.php
chmod 640 /etc/phpmyadmin/conf.d/securite.php

echo "== 3/6 Première barrière : mot de passe Nginx"
htpasswd -bc /etc/nginx/.htpasswd_pma uciv "${PW_WEB}" >/dev/null

echo "== 4/6 Configuration Nginx pour ${DOMAINE}"
cat > /etc/nginx/sites-available/phpmyadmin <<NGINX
server {
    listen 80;
    listen [::]:80;
    server_name ${DOMAINE};

    root /usr/share/phpmyadmin;
    index index.php;

    auth_basic "Zone protégée UCIV";
    auth_basic_user_file /etc/nginx/.htpasswd_pma;
    add_header X-Robots-Tag "noindex, nofollow" always;

    location / {
        try_files \$uri \$uri/ =404;
    }

    location ~ ^/(libraries|templates|setup/lib)/ {
        deny all;
    }

    location ~ \.php\$ {
        include snippets/fastcgi-php.conf;
        fastcgi_pass unix:${PHP_SOCKET};
    }

    location ~ /\.ht {
        deny all;
    }
}
NGINX
rm -f /etc/nginx/sites-enabled/phpmyadmin
ln -s /etc/nginx/sites-available/phpmyadmin /etc/nginx/sites-enabled/phpmyadmin
nginx -t
systemctl reload nginx
systemctl restart "$(basename "${PHP_SOCKET}" .sock)"

echo "== 5/6 Certificat HTTPS (Let's Encrypt)"
apt-get install -y certbot python3-certbot-nginx >/dev/null
if [ -n "${EMAIL}" ]; then
    CERT_OPTS="-m ${EMAIL}"
else
    CERT_OPTS="--register-unsafely-without-email"
fi
certbot --nginx -d "${DOMAINE}" --non-interactive --agree-tos ${CERT_OPTS} --redirect
systemctl list-timers 2>/dev/null | grep -i certbot || true

echo "== 6/6 Vérifications"
sleep 2
curl -s -o /dev/null -w "HTTPS sans mot de passe  : HTTP %{http_code} (401 attendu)\n" "https://${DOMAINE}/"
curl -s -o /dev/null -u "uciv:${PW_WEB}" -w "HTTPS avec mot de passe  : HTTP %{http_code} (200 attendu)\n" "https://${DOMAINE}/"
curl -s -o /dev/null -w "HTTP redirigé vers HTTPS : HTTP %{http_code} (301 attendu)\n" "http://${DOMAINE}/"
ss -tlnp | grep -E ":3306 " | awk '{print "MySQL écoute sur : " $4}'

umask 077
cat > /root/identifiants-mysql.txt <<CRED
MySQL du site UCIV
  base            : uciv
  utilisateur     : uciv_user
  mot de passe    : ${PW_SITE}
  hôte            : localhost  (port 3306)

phpMyAdmin : https://${DOMAINE}
  1re barrière (fenêtre du navigateur)
    utilisateur   : uciv
    mot de passe  : ${PW_WEB}
  2e barrière (page de connexion phpMyAdmin)
    utilisateur   : admin_pma
    mot de passe  : ${PW_PMA}
CRED
chmod 600 /root/identifiants-mysql.txt
echo
echo "Identifiants enregistrés dans /root/identifiants-mysql.txt (lecture : cat /root/identifiants-mysql.txt)"
