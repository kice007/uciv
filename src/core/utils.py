import logging
import socket
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = logging.getLogger(__name__)

def send_customize_email(subject: str, receivers: list, template: str, context: dict,
                         reply_to: list | None = None) -> bool:
    try:
        html_message = render_to_string(template, context)
        message = EmailMultiAlternatives(
            subject, '', settings.EMAIL_HOST_USER, receivers, reply_to=reply_to,
        )
        message.attach_alternative(html_message, 'text/html')
        message.send()
        return True
    except Exception as e:
        logger.error(f"Email error: {e}")
        return False


def get_ip() -> str:
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return '127.0.0.1'
