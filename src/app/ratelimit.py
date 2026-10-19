"""
Limiteur de débit des formulaires : au-delà d'un nombre d'envois par adresse IP et par fenêtre de temps, la requête
reçoit une réponse 429 (« Trop de demandes ») avec l'en-tête `Retry-After`.

Les compteurs vivent dans le cache de Django. En production, le cache est un dossier partagé entre les processus Gunicorn
(voir `CACHES` dans core/settings.py) : un compteur en mémoire locale laisserait chaque processus compter à part.
Seuls les envois (POST) sont comptés ; l'affichage des pages n'est jamais limité.
"""
import hashlib
import math
import re
import time
from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render

from . import content
from . import seo as referencement


def adresse_client(request):
    """Adresse IP de la personne. Derrière Nginx, `X-Real-IP` (écrit par Nginx lui-même) remplace l'adresse du socket."""
    adresse = request.META.get('REMOTE_ADDR', '')
    if not settings.DEBUG:
        adresse = request.META.get('HTTP_X_REAL_IP') or adresse
    return re.sub(r'[^0-9a-fA-F:.]', '', adresse)[:45] or 'inconnue'


def _cle(portee, identifiant):
    return 'rl:' + portee + ':' + hashlib.sha256(identifiant.encode('utf-8')).hexdigest()[:32]


def attente(portee, identifiant, maximum, fenetre):
    """Compte un envoi. Renvoie 0 s'il est accepté, sinon le nombre de secondes à attendre avant de réessayer."""
    cle = _cle(portee, identifiant)
    maintenant = time.time()
    cache.add(cle + ':debut', maintenant, fenetre)
    cache.add(cle, 0, fenetre)
    try:
        n = cache.incr(cle)
    except ValueError:      # compteur expiré entre-temps
        cache.set(cle, 1, fenetre)
        cache.set(cle + ':debut', maintenant, fenetre)
        n = 1
    if n <= maximum:
        return 0
    debut = cache.get(cle + ':debut', maintenant)
    return max(1, math.ceil(fenetre - (maintenant - debut)))


def _duree(secondes):
    if secondes < 60:
        return 'quelques secondes'
    minutes = math.ceil(secondes / 60)
    return f'{minutes} minute{"s" if minutes > 1 else ""}'


def reponse_trop_de_demandes(request, secondes):
    page = dict(content.PAGE_429)
    page['texte'] = page['texte'].format(duree=_duree(secondes))
    reponse = render(request, 'app/layout/429.html', {'page': page, 'seo': referencement.construire(request, None)},
                     status=429)
    reponse['Retry-After'] = str(secondes)
    return reponse


def limiter(portee, maximum, fenetre):
    """Décorateur de vue : au plus `maximum` envois (POST) par adresse IP et par `fenetre` secondes."""
    def decorateur(vue):
        @wraps(vue)
        def enveloppe(request, *args, **kwargs):
            if request.method == 'POST':
                secondes = attente(portee, adresse_client(request), maximum, fenetre)
                if secondes:
                    return reponse_trop_de_demandes(request, secondes)
            return vue(request, *args, **kwargs)
        return enveloppe
    return decorateur


# Connexion à l'administration : par adresse IP (essais en rafale) et par identifiant (attaque répartie sur plusieurs IP)
CONNEXION_PAR_IP = (10, 15 * 60)
CONNEXION_PAR_IDENTIFIANT = (5, 15 * 60)


def limiter_connexion(vue):
    @wraps(vue)
    def enveloppe(request, *args, **kwargs):
        if request.method == 'POST':
            secondes = attente('connexion-ip', adresse_client(request), *CONNEXION_PAR_IP)
            identifiant = request.POST.get('username', '').strip().lower()[:150]
            if identifiant:
                secondes = max(secondes, attente('connexion-id', identifiant, *CONNEXION_PAR_IDENTIFIANT))
            if secondes:
                return reponse_trop_de_demandes(request, secondes)
        return vue(request, *args, **kwargs)
    return enveloppe
