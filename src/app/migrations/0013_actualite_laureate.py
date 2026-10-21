"""Actualité « La Reine du Digital » : photo, nom et témoignage de Leticia BOSSON, comme dans Notre impact.

Ne modifie l'article que s'il n'a pas été retravaillé : il garde encore la photo de remplacement des Go du Digital et n'a pas
de texte. Le lien de l'article (slug) ne change pas.
"""
from django.db import migrations

SLUG = 'la-reine-du-digital-le-parcours-d-une-laureate'
ANCIENNE_IMAGE = 'app/assets/img/go-du-digital.webp'
TEMOIGNAGE = (
    "Ces six semaines de formation m'ont beaucoup appris. Nous avons été sérieusement formées à la "
    "création de contenu, avec beaucoup de pratique et d'exercices, ce qui m'a permis de monter très vite "
    "en compétence. Je sors de cette formation très heureuse, d'autant plus que j'ai été couronnée Reine. "
    "Je recommande à 100 % le programme Les Go du Digital."
)
ACTUALITE = dict(
    titre="« La Reine du Digital » : le parcours de Leticia BOSSON",
    chapo="Leticia BOSSON, lauréate des Go du Digital : « Ces six semaines de formation m'ont beaucoup appris. […] "
          "Je recommande à 100 % le programme Les Go du Digital. »",
    corps=f"!! Leticia BOSSON a été couronnée Reine du Digital à la fin de son édition des Go du Digital.\n\n"
          f"> « {TEMOIGNAGE} »\n— Leticia BOSSON, lauréate des Go du Digital",
    image='app/assets/img/leticia-bosson.webp',
    image_alt='Leticia BOSSON, couronnée Reine du Digital, pose avec sa couronne.',
)


def mettre_a_jour(apps, schema_editor):
    Article = apps.get_model('app', 'Article')
    article = Article.objects.filter(slug=SLUG).first()
    if article and article.image == ANCIENNE_IMAGE and not article.corps.strip():
        for champ, valeur in ACTUALITE.items():
            setattr(article, champ, valeur)
        article.save(update_fields=list(ACTUALITE))


class Migration(migrations.Migration):
    dependencies = [('app', '0012_laureate_nom_dans_la_description')]
    operations = [migrations.RunPython(mettre_a_jour, migrations.RunPython.noop)]
