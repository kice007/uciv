"""Envoie un e-mail de test avec la configuration SMTP en vigueur et affiche l'erreur exacte en cas d'échec.

Usage (en production : `uciv-manage tester_email adresse@exemple.org`) :
    python manage.py tester_email [destinataire]

Sans destinataire, le message part vers CONTACT_EMAIL. Les formulaires du site, eux, n'affichent jamais d'erreur d'envoi au visiteur
(`core.utils.send_customize_email` l'écrit dans les journaux) : cette commande sert à vérifier la configuration avant de compter dessus.
Le mot de passe n'est jamais affiché.
"""
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Envoie un e-mail de test avec la configuration SMTP actuelle."

    def add_arguments(self, parser):
        parser.add_argument('destinataire', nargs='?', default=None,
                            help="Adresse qui reçoit le test (par défaut : CONTACT_EMAIL).")

    def handle(self, *args, **options):
        destinataire = options['destinataire'] or settings.CONTACT_EMAIL
        if not settings.EMAIL_HOST:
            raise CommandError("EMAIL_HOST est vide : aucun e-mail n'est envoyé. Renseignez les variables EMAIL_* "
                               "(en production : bash configurer_email.sh).")
        chiffrement = 'SSL' if settings.EMAIL_USE_SSL else 'STARTTLS' if settings.EMAIL_USE_TLS else 'aucun'
        self.stdout.write(f"Serveur : {settings.EMAIL_HOST}:{settings.EMAIL_PORT} ({chiffrement})")
        self.stdout.write(f"Connexion : {settings.EMAIL_HOST_USER or '(sans identifiant)'}"
                          f" | mot de passe {'renseigné' if settings.EMAIL_HOST_PASSWORD else 'VIDE'}")
        self.stdout.write(f"Expéditeur : {settings.DEFAULT_FROM_EMAIL} | destinataire : {destinataire}")
        try:
            send_mail(
                "Test d'envoi — site UCIV",
                "Ce message confirme que le site d'Une Côte d'Ivoire Volontaire sait envoyer des e-mails.\n\n"
                "Les messages des formulaires (contact, engagement, partenariat) arriveront à cette adresse.",
                settings.DEFAULT_FROM_EMAIL, [destinataire], fail_silently=False,
            )
        except Exception as erreur:   # on veut le message exact du serveur SMTP
            raise CommandError(f"Échec de l'envoi : {erreur.__class__.__name__} : {erreur}")
        self.stdout.write(self.style.SUCCESS(f"E-mail envoyé à {destinataire}. Vérifiez la boîte de réception (et les indésirables)."))
