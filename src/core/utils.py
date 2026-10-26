import hashlib
import logging
import socket
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

def send_customize_email(subject: str, receivers: list, template: str, context: dict,
                         reply_to: list | None = None) -> bool:
    try:
        html_message = render_to_string(template, context)
        message = EmailMultiAlternatives(
            subject, '', settings.DEFAULT_FROM_EMAIL, receivers, reply_to=reply_to,
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
