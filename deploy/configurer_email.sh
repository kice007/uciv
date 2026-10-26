#!/bin/bash
# Configure l'envoi des e-mails du site UCIV (formulaires, lettre d'information) puis envoie un e-mail de test.
#
# Usage, en root sur le serveur, dans un terminal interactif (relançable à volonté : il remplace les réglages précédents) :
#   scp deploy/configurer_email.sh uciv-vps:/root/configurer_email.sh
#   ssh -t uciv-vps 'bash /root/configurer_email.sh [adresse_de_test]'
#
# Le script ne contient aucun secret. Le mot de passe est demandé sans affichage : il n'apparaît ni dans le chat, ni dans git, ni dans
# l'historique du shell, et il est écrit seulement dans /etc/uciv/uciv.env (lisible par root seulement). Les mises à jour du site
# (deployer.sh) conservent ce fichier tel quel.
#
# Variables écrites : EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_USE_SSL, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_EMAIL,
# CONTACT_EMAIL (l'adresse qui reçoit les messages des formulaires, si vous la changez).
set -euo pipefail

ENV_FILE=/etc/uciv/uciv.env

[ "$(id -u)" -eq 0 ] || { echo "À lancer en root."; exit 1; }
[ -f "${ENV_FILE}" ] || { echo "${ENV_FILE} est introuvable : lancez d'abord deployer.sh."; exit 1; }
[ -t 0 ] || { echo "Terminal interactif requis (le mot de passe est saisi sans affichage) : ssh -t uciv-vps 'bash /root/configurer_email.sh'"; exit 1; }
command -v uciv-manage >/dev/null || { echo "La commande uciv-manage est absente : lancez d'abord deployer.sh."; exit 1; }

ADRESSE_TEST="${1:-}"

echo "== Fournisseur d'envoi"
echo "  1) Brevo : service d'envoi (gratuit jusqu'à 300 e-mails/jour) ; l'expéditeur est une adresse du domaine, ex. noreply@uciv.org,"
echo "             sans boîte mail à acheter (domaine authentifié par SPF/DKIM dans le DNS)"
echo "  2) Hostinger Email : boîte mail @uciv.org (offre Hostinger Email payante)"
echo "  3) Gmail (smtp.gmail.com)  : compte avec validation en deux étapes et « mot de passe d'application »"
echo "  4) Autre serveur SMTP      : Mailjet, OVH, autre hébergeur de messagerie…"
read -r -p "Votre choix [1] : " CHOIX
CHOIX="${CHOIX:-1}"

if [ "${CHOIX}" = "1" ]; then
    HOTE=smtp-relay.brevo.com; PORT=587; TLS=True; SSL=False
    echo "Brevo > SMTP et API > onglet SMTP : « Identifiant de connexion » et clé SMTP (ce n'est pas le mot de passe du compte)."
    read -r -p "Identifiant de connexion Brevo (ex. 7a1b2c001@smtp-brevo.com) : " UTILISATEUR
    read -r -s -p "Clé SMTP Brevo : " MOT_DE_PASSE; echo
    read -r -p "Expéditeur des notifications [UCIV <noreply@uciv.org>] : " EXPEDITEUR
    EXPEDITEUR="${EXPEDITEUR:-UCIV <noreply@uciv.org>}"
elif [ "${CHOIX}" = "2" ]; then
    HOTE=smtp.hostinger.com; PORT=465; TLS=False; SSL=True
    read -r -p "Adresse e-mail professionnelle qui envoie (ex. contact@uciv.org) : " UTILISATEUR
    read -r -s -p "Mot de passe de cette boîte mail : " MOT_DE_PASSE; echo
    EXPEDITEUR="${UTILISATEUR}"
elif [ "${CHOIX}" = "3" ]; then
    HOTE=smtp.gmail.com; PORT=587; TLS=True; SSL=False
    read -r -p "Adresse Gmail qui envoie [organisationuciv@gmail.com] : " UTILISATEUR
    UTILISATEUR="${UTILISATEUR:-organisationuciv@gmail.com}"
    echo "Mot de passe d'application Google (16 lettres, créé sur myaccount.google.com > Sécurité > Mots de passe d'application) :"
    read -r -s -p "Mot de passe d'application : " MOT_DE_PASSE; echo
    MOT_DE_PASSE="${MOT_DE_PASSE// /}"    # Google l'affiche par blocs de 4 séparés par des espaces : ils ne font pas partie du mot de passe
    EXPEDITEUR="${UTILISATEUR}"
elif [ "${CHOIX}" = "4" ]; then
    read -r -p "Serveur SMTP (ex. smtp.exemple.org) : " HOTE
    read -r -p "Port [587] : " PORT; PORT="${PORT:-587}"
    echo "Chiffrement : 1) STARTTLS (port 587, le plus courant)   2) SSL direct (port 465)"
    read -r -p "Votre choix [1] : " CHIFFREMENT
    if [ "${CHIFFREMENT:-1}" = "2" ]; then TLS=False; SSL=True; else TLS=True; SSL=False; fi
    read -r -p "Identifiant de connexion : " UTILISATEUR
    read -r -s -p "Mot de passe : " MOT_DE_PASSE; echo
    read -r -p "Adresse d'expéditeur [${UTILISATEUR}] : " EXPEDITEUR
    EXPEDITEUR="${EXPEDITEUR:-${UTILISATEUR}}"
else
    echo "Choix inconnu."; exit 1
fi

ACTUEL="$(grep -E '^CONTACT_EMAIL=' "${ENV_FILE}" | cut -d= -f2- || true)"
ACTUEL="${ACTUEL:-organisationuciv@gmail.com}"
read -r -p "Adresse qui reçoit les messages des formulaires [${ACTUEL}] : " CONTACT
CONTACT="${CONTACT:-${ACTUEL}}"

# Valeurs minimales et caractères qui seraient lus différemment par systemd (service) et par uciv-manage
[ -n "${HOTE}" ] && [ -n "${UTILISATEUR}" ] && [ -n "${MOT_DE_PASSE}" ] || { echo "Serveur, identifiant et mot de passe sont obligatoires."; exit 1; }
case "${MOT_DE_PASSE}${UTILISATEUR}${HOTE}${EXPEDITEUR}${CONTACT}" in
    *\"*|*\'*|*\\*) echo "Les guillemets et les barres obliques inverses ne sont pas acceptés dans ces valeurs (systemd les interpréterait)."; exit 1 ;;
esac
case "${PORT}" in ''|*[!0-9]*) echo "Le port doit être un nombre."; exit 1 ;; esac

# Sauvegarde puis remplacement des lignes concernées (le mot de passe n'est jamais affiché)
cp -p "${ENV_FILE}" "${ENV_FILE}.avant-email"
TMP="$(mktemp "${ENV_FILE}.XXXXXX")"
grep -v -E '^(EMAIL_HOST|EMAIL_PORT|EMAIL_USE_TLS|EMAIL_USE_SSL|EMAIL_HOST_USER|EMAIL_HOST_PASSWORD|DEFAULT_FROM_EMAIL|CONTACT_EMAIL)=' "${ENV_FILE}" > "${TMP}" || true
{
    printf 'EMAIL_HOST=%s\n' "${HOTE}"
    printf 'EMAIL_PORT=%s\n' "${PORT}"
    printf 'EMAIL_USE_TLS=%s\n' "${TLS}"
    printf 'EMAIL_USE_SSL=%s\n' "${SSL}"
    printf 'EMAIL_HOST_USER=%s\n' "${UTILISATEUR}"
    printf 'EMAIL_HOST_PASSWORD=%s\n' "${MOT_DE_PASSE}"
    printf 'DEFAULT_FROM_EMAIL=%s\n' "${EXPEDITEUR}"
    printf 'CONTACT_EMAIL=%s\n' "${CONTACT}"
} >> "${TMP}"
chown root:root "${TMP}"; chmod 600 "${TMP}"
mv "${TMP}" "${ENV_FILE}"
unset MOT_DE_PASSE

echo "== Réglages enregistrés dans ${ENV_FILE} (ancienne version : ${ENV_FILE}.avant-email)"
echo "   serveur ${HOTE}:${PORT} · TLS=${TLS} SSL=${SSL} · connexion ${UTILISATEUR} · expéditeur ${EXPEDITEUR} · réception des formulaires ${CONTACT}"

echo "== Redémarrage du site"
systemctl restart uciv
sleep 3
systemctl is-active --quiet uciv && echo "   site actif" || { echo "   Le site n'a pas redémarré : journalctl -u uciv -n 50"; exit 1; }

if [ "${CHOIX}" = "1" ]; then
    echo "   Rappel : authentifiez le domaine dans Brevo (Expéditeurs, domaines et IP > Domaines) en ajoutant dans le DNS de uciv.org"
    echo "   les enregistrements indiqués (Brevo, SPF/DKIM/DMARC) ; sans cela les messages risquent de finir dans les indésirables."
fi

echo "== E-mail de test"
if uciv-manage tester_email ${ADRESSE_TEST:+"${ADRESSE_TEST}"}; then
    echo
    echo "Configuration terminée. Les formulaires (contact, engagement, partenariat) et l'inscription à la lettre d'information envoient désormais des e-mails."
else
    echo
    echo "Les réglages sont enregistrés mais l'envoi de test a échoué (message ci-dessus). Causes fréquentes :"
    echo "  - Brevo : identifiant de connexion ou clé SMTP incorrects, ou compte pas encore validé par Brevo (e-mail de confirmation)"
    echo "  - Hostinger : la boîte mail n'est pas encore créée (hPanel > E-mails), ou son mot de passe est incorrect"
    echo "  - Gmail : mot de passe du compte au lieu d'un mot de passe d'application, ou validation en deux étapes désactivée"
    echo "  - identifiant, port ou chiffrement incorrects (587 = STARTTLS, 465 = SSL)"
    echo "  - le serveur bloque les connexions sortantes vers ce port"
    echo "Relancez ce script pour corriger ; l'ancienne configuration est dans ${ENV_FILE}.avant-email."
    exit 1
fi
