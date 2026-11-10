"""
Mesure d'audience sans cookie et suivi des attaques, affichés dans l'administration (Statistiques et Sécurité).

Principes :
- Aucun cookie, aucun script tiers. Un visiteur est un code (SHA-256 de l'adresse IP, du navigateur, du jour et de la clé secrète) qui
  change chaque jour : on compte les visiteurs d'une journée, jamais une personne d'un jour à l'autre, et l'adresse IP n'est pas conservée.
- Les robots (navigateur absent ou déclaré), l'équipe connectée à l'administration et les personnes qui envoient « Do Not Track »
  ou « Global Privacy Control » ne sont pas comptées.
- Les attaques (sondes de robots, tentatives d'injection, trop de demandes, pièges des formulaires, échecs de connexion) sont
  enregistrées avec leur adresse IP, 90 jours au plus : c'est une donnée de sécurité, utile pour bloquer l'adresse (voir `purger_statistiques`).
- La mesure ne doit jamais gêner une page : toute erreur ici est journalisée puis ignorée.
"""
import hashlib
import logging
import re
from urllib.parse import unquote_plus, urlsplit

from django.conf import settings
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
from django.utils import timezone

from .models import EvenementSecurite, Visite
from .ratelimit import adresse_client, attente

logger = logging.getLogger(__name__)

# Chemins qui ne sont pas des pages vues.
CHEMINS_IGNORES = ('/static/', '/media/', '/mesure/', '/favicon', '/robots.txt', '/sitemap', '/llms.txt', '/.well-known/', '/404/')

# Navigateurs de robots, d'outils en ligne de commande et de services de surveillance.
ROBOTS = re.compile(
    r'bot\b|bot/|crawl|spider|slurp|curl|wget|python|java/|httpclient|okhttp|libwww|scrapy|headless|phantom|monitor|uptime|'
    r'facebookexternalhit|preview|fetch|go-http|axios|postman|lighthouse|pingdom|gtmetrix|semrush|ahrefs|mj12|dotbot|petalbot|bytespider',
    re.I)

# Chemins qu'un site Django comme celui-ci n'a pas : ceux qu'un robot teste en cherchant WordPress, des fichiers oubliés ou des consoles.
SONDES = re.compile(
    r'wp-|wordpress|xmlrpc|\.php\b|\.env\b|\.git(/|$)|\.svn|\.ht(access|passwd)|phpmyadmin|/pma\b|/vendor/|/cgi-bin|/boaform|/actuator|'
    r'/solr|/jenkins|\.aspx?\b|\.jsp\b|/etc/passwd|/shell|/backup|\.sql\b|\.bak\b|\.tar|\.zip$|^/admin\b|/administrator|/owa/|/ecp/|/console\b|'
    r'/config\.|/\.aws|/\.ssh|/server-status|/telescope|/debug', re.I)

# Motifs d'injection dans l'adresse demandée (chemin ou paramètres).
INJECTIONS = re.compile(
    r'union(\s|%20|\+)+select|select(\s|%20|\+).{1,40}from|<script|javascript:|\.\./|%2e%2e|/etc/passwd|(\s|%20|\+)or(\s|%20|\+)1=1|'
    r'sleep\(|benchmark\(|base64_decode|eval\(|\$\{jndi', re.I)

LIBELLES_EVENEMENTS = dict(EvenementSecurite.TYPES)


def est_robot(agent):
    return not agent or bool(ROBOTS.search(agent))


def appareil(agent):
    if re.search(r'iPad|Tablet', agent) or (re.search(r'Android', agent) and not re.search(r'Mobile', agent)):
        return 'tablette'
    if re.search(r'Mobi|iPhone|Android', agent):
        return 'mobile'
    return 'ordinateur'


def code_visiteur(request, jour=None):
    """Code anonyme du visiteur pour un jour donné : change tous les jours, ne permet pas de retrouver l'adresse IP."""
    jour = jour or timezone.localdate()
    brut = f"{settings.SECRET_KEY}|{jour.isoformat()}|{adresse_client(request)}|{request.META.get('HTTP_USER_AGENT', '')}"
    return hashlib.sha256(brut.encode('utf-8')).hexdigest()[:20]


def domaine_referent(request):
    """Domaine d'où vient la personne (sans « www »), vide pour un accès direct ou depuis le site lui-même."""
    adresse = request.META.get('HTTP_REFERER', '')
    if not adresse:
        return ''
    domaine = (urlsplit(adresse).hostname or '').lower().removeprefix('www.')
    propre = request.get_host().split(':')[0].lower().removeprefix('www.')
    return '' if not domaine or domaine == propre else domaine[:120]


def vie_privee_respectee(request):
    """Vrai si la personne demande à ne pas être suivie (Do Not Track ou Global Privacy Control)."""
    return request.META.get('HTTP_DNT') == '1' or request.META.get('HTTP_SEC_GPC') == '1'


def signaler(request, type_, detail=''):
    """Enregistre un événement de sécurité. Au plus 30 par adresse IP et par heure, pour qu'une attaque ne remplisse pas la base."""
    try:
        ip = adresse_client(request)
        if attente('evenement', ip, 30, 3600):
            return
        EvenementSecurite.objects.create(type=type_, chemin=request.get_full_path()[:300], detail=detail[:200], ip=ip)
    except Exception:    # la sécurité ne doit jamais casser une page
        logger.exception('Événement de sécurité non enregistré')


def signaler_piege(request):
    """Un robot a rempli le champ invisible d'un formulaire."""
    signaler(request, 'piege', f'formulaire {request.path}')


@receiver(user_login_failed)
def echec_de_connexion(sender, credentials=None, request=None, **kwargs):
    if request is None:
        return
    existe = False
    try:
        from django.contrib.auth import get_user_model
        nom = (credentials or {}).get('username') or ''
        existe = bool(nom) and get_user_model().objects.filter(username=nom).exists()
    except Exception:
        pass
    # On n'enregistre jamais l'identifiant saisi (il peut contenir un mot de passe tapé au mauvais endroit).
    signaler(request, 'connexion', 'compte existant' if existe else 'compte inconnu')


class MesureMiddleware:
    """À placer en premier dans MIDDLEWARE : voit aussi les réponses d'erreur (400) produites par les middlewares suivants."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        reponse = self.get_response(request)
        if getattr(settings, 'MESURE_ACTIVE', True):
            try:
                self.enregistrer(request, reponse)
            except Exception:
                logger.exception('Mesure non enregistrée')
        return reponse

    def enregistrer(self, request, reponse):
        chemin = request.path
        if chemin.startswith(CHEMINS_IGNORES):
            return
        etat = reponse.status_code
        espace_admin = chemin.startswith(f'/{settings.ADMIN_URL}/')

        # --- Attaques (toujours enregistrées, même pour un robot) ---
        if etat == 429:
            signaler(request, 'limite', f'{request.method} {chemin}')
        elif etat in (400, 403) and not espace_admin:
            signaler(request, 'refus', f'{request.method} {etat}')
        # Les attaquants encodent leurs requêtes (%3Cscript%3E, ..%2F) : on cherche dans l'adresse décodée, deux fois (double encodage).
        decodee = unquote_plus(unquote_plus(request.get_full_path()))
        if INJECTIONS.search(request.get_full_path()) or INJECTIONS.search(decodee):
            signaler(request, 'injection', f'{request.method} {etat}')
        elif etat == 404 and SONDES.search(chemin):
            signaler(request, 'sonde', f'{request.method} {etat}')

        # --- Pages vues ---
        if request.method != 'GET' or etat != 200 or espace_admin:
            return
        if 'text/html' not in reponse.get('Content-Type', ''):
            return
        agent = request.META.get('HTTP_USER_AGENT', '')
        if est_robot(agent) or vie_privee_respectee(request):
            return
        utilisateur = getattr(request, 'user', None)
        if utilisateur is not None and utilisateur.is_authenticated and utilisateur.is_staff:
            return
        visiteur = code_visiteur(request)
        if attente('vue', visiteur, 600, 86400):    # plafond par visiteur et par jour
            return
        Visite.objects.create(chemin=chemin[:300], visiteur=visiteur, referent=domaine_referent(request),
                              appareil=appareil(agent))
