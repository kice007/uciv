"""Date de lancement d'UCIV Leadership : le 24 octobre 2026."""
from django.db import migrations


def mettre_a_jour(apps, schema_editor):
    Article = apps.get_model('app', 'Article')
    Article.objects.filter(
        slug='uciv-leadership-la-conference-de-lancement-au-format-tedx', meta='Octobre 2026',
    ).update(meta='24 octobre 2026')


def annuler(apps, schema_editor):
    Article = apps.get_model('app', 'Article')
    Article.objects.filter(
        slug='uciv-leadership-la-conference-de-lancement-au-format-tedx', meta='24 octobre 2026',
    ).update(meta='Octobre 2026')


class Migration(migrations.Migration):
    dependencies = [('app', '0005_contenu_initial')]
    operations = [migrations.RunPython(mettre_a_jour, annuler)]
