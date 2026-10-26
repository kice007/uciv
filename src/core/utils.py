import hashlib
import logging
import re
import socket
from html import unescape
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.cache import cache
from django.templatetags.static import static
from django.utils import timezone
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

URL_SITE_PAR_DEFAUT = 'https://uciv.org'


def contexte_email(contexte: dict) -> dict:
    """Variables communes à tous les e-mails (cadre emails/_base.html) : adresse de l'équipe, adresse du site, logo, année."""
    site = (settings.SITE_URL or URL_SITE_PAR_DEFAUT).rstrip('/')
    return {
        'contact_email': settings.CONTACT_EMAIL, 'site_url': site,
        'logo_url': site + static('app/assets/img/logo-uciv.png'), 'annee': timezone.now().year,
        **contexte,
    }


def texte_brut(html: str) -> str:
    """Version texte d'un e-mail HTML (les liens deviennent « texte (adresse) »). Un e-mail sans texte brut est plus souvent classé en indésirable."""
    def lien(m):
        adresse, texte = unescape(m.group(1)), strip_tags(m.group(2)).strip()
        if not texte:   # lien porté par une image (logo) : rien à écrire en texte brut
            return ''
        if adresse.startswith('mailto:') or texte == adresse:
            return texte
        return f'{texte} ({adresse})'

    html = re.sub(r'<(head|style|title)[^>]*>.*?</\1>', '', html, flags=re.S | re.I)
    html = re.sub(r'<div style="display:none[^>]*>.*?</div>', '', html, flags=re.S)   # texte d'aperçu masqué
    html = re.sub(r'<a [^>]*?href="([^"]+)"[^>]*>(.*?)</a>', lien, html, flags=re.S | re.I)
    html = re.sub(r'<br\s*/?>|</(p|tr|h1|h2|li|table)>', chr(10), html, flags=re.I)
    html = re.sub(r'</td>', ' ', html, flags=re.I)
    lignes = [re.sub(r'[ \t\xa0]+', ' ', ligne).strip() for ligne in unescape(strip_tags(html)).splitlines()]
    return re.sub(r'\n{3,}', chr(10) * 2, chr(10).join(lignes)).strip()


def send_customize_email(subject: str, receivers: list, template: str, context: dict,
                         reply_to: list | None = None) -> bool:
    try:
        html_message = render_to_string(template, contexte_email(context))
        message = EmailMultiAlternatives(
            subject, texte_brut(html_message), settings.DEFAULT_FROM_EMAIL, receivers, reply_to=reply_to,
        )
        message.attach_alternative(html_message, 'text/html')
        message.send()
        return True
    except Exception as e:
        logger.error(f"Email error: {e}")
        return False


def envoyer_accuse_reception(destinataire: str, sujet: str, template: str, contexte: dict) -> bool:
    """Accusé de réception envoyé à la personne qui a rempli un formulaire.

    Les réponses vont à CONTACT_EMAIL (l'adresse d'envoi est une adresse « noreply »). Pour qu'on ne puisse pas se servir d'un formulaire
    pour inonder la boîte d'un tiers en saisissant son adresse, une même adresse ne reçoit qu'un accusé par heure ; la notification à
    l'équipe, elle, part toujours. Retourne True si le message est parti.
    """
    cle = 'accuse:' + hashlib.sha256(destinataire.strip().lower().encode('utf-8')).hexdigest()
    if not cache.add(cle, 1, 3600):
        return False
    envoye = send_customize_email(sujet, [destinataire], template, contexte, reply_to=[settings.CONTACT_EMAIL])
    if not envoye:
        cache.delete(cle)   # l'envoi a échoué : la prochaine tentative doit pouvoir réessayer
    return envoye


def get_ip() -> str:
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return '127.0.0.1'
