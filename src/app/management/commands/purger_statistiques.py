"""Supprime les statistiques anciennes (à lancer chaque jour : cron du serveur, voir deploy/deployer.sh).

    python manage.py purger_statistiques [--visites 395] [--evenements 90]

Visites : 395 jours (13 mois) ; événements de sécurité, qui contiennent des adresses IP : 90 jours. Ces durées figurent dans la
politique de confidentialité (app/content.py).
"""
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from app.models import EvenementSecurite, Visite


class Command(BaseCommand):
    help = "Supprime les visites et les événements de sécurité plus anciens que la durée de conservation."

    def add_arguments(self, parser):
        parser.add_argument('--visites', type=int, default=395, help="Jours de conservation des visites.")
        parser.add_argument('--evenements', type=int, default=90, help="Jours de conservation des événements de sécurité.")

    def handle(self, *args, **options):
        maintenant = timezone.now()
        visites = Visite.objects.filter(date__lt=maintenant - timedelta(days=options['visites'])).delete()[0]
        evenements = EvenementSecurite.objects.filter(date__lt=maintenant - timedelta(days=options['evenements'])).delete()[0]
        self.stdout.write(f"Visites supprimees : {visites} | evenements de securite supprimes : {evenements}")
