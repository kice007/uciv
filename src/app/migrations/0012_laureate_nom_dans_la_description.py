"""Histoire de la lauréate (Notre impact) : le nom de Leticia BOSSON figure dans la description de la carte.

Ne modifie l'article que s'il porte encore le résumé posé par la migration précédente ou le texte d'origine (« [Nom de la
lauréate] … ») : un résumé réécrit depuis l'administration n'est jamais écrasé.
"""
from django.db import migrations

SLUG = 'histoire-la-laureate-de-la-reine-du-digital'
ANCIEN = ("« Ces six semaines de formation m'ont beaucoup appris. […] Je recommande à 100 % le programme "
          "Les Go du Digital. »")
NOUVEAU = ("Leticia BOSSON, lauréate des Go du Digital : « Ces six semaines de formation m'ont beaucoup appris. […] "
           "Je recommande à 100 % le programme Les Go du Digital. »")


def nommer(apps, schema_editor):
    Article = apps.get_model('app', 'Article')
    article = Article.objects.filter(slug=SLUG).first()
    if article and (article.chapo == ANCIEN or article.chapo.startswith('[')):
        article.chapo = NOUVEAU
        article.save(update_fields=['chapo'])


class Migration(migrations.Migration):
    dependencies = [('app', '0011_chiffres_et_laureate')]
    operations = [migrations.RunPython(nommer, migrations.RunPython.noop)]
