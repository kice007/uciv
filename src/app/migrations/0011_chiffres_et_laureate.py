"""Contenus transmis par UCIV en octobre 2026 (UCIV/info/uciv_update.md).

- Chiffres clés de l'accueil et de Notre impact.
- Première histoire de Notre impact : Leticia BOSSON, lauréate des Go du Digital.

Seuls les emplacements encore vides sont remplis : une valeur déjà saisie dans l'administration
n'est jamais écrasée.
"""
from django.db import migrations

CHIFFRES = {
    'Jeunes mobilisés': ('+', 1800),
    'Volontaires': ('', 40),
    'Programmes réalisés': ('', 5),
    'Participants formés': ('', 50),
    'Partenaires': ('', 4),
    'Projets réalisés': ('', 5),
}

SLUG_LAUREATE = 'histoire-la-laureate-de-la-reine-du-digital'
TEMOIGNAGE = (
    "Ces six semaines de formation m'ont beaucoup appris. Nous avons été sérieusement formées à la "
    "création de contenu, avec beaucoup de pratique et d'exercices, ce qui m'a permis de monter très vite "
    "en compétence. Je sors de cette formation très heureuse, d'autant plus que j'ai été couronnée Reine. "
    "Je recommande à 100 % le programme Les Go du Digital."
)
LAUREATE = dict(
    titre='Leticia BOSSON, Reine du Digital',
    chapo="« Ces six semaines de formation m'ont beaucoup appris. […] Je recommande à 100 % le programme "
          "Les Go du Digital. »",
    corps=f"!! Leticia BOSSON a été couronnée Reine du Digital à la fin de son édition des Go du Digital.\n\n"
          f"> « {TEMOIGNAGE} »\n— Leticia BOSSON, lauréate des Go du Digital",
    image='app/assets/img/leticia-bosson.webp',
    image_alt='Leticia BOSSON, couronnée Reine du Digital, pose avec sa couronne.',
)


def remplir(apps, schema_editor):
    Indicateur = apps.get_model('app', 'Indicateur')
    for libelle, (prefixe, valeur) in CHIFFRES.items():
        Indicateur.objects.filter(libelle=libelle, valeur__isnull=True).update(prefixe=prefixe, valeur=valeur)
    Article = apps.get_model('app', 'Article')
    # L'histoire de départ commence par « [Nom de la lauréate] » tant qu'elle n'a pas été rédigée.
    Article.objects.filter(slug=SLUG_LAUREATE, chapo__startswith='[').update(**LAUREATE)


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_indicateur_prefixe'),
    ]

    # Pas de retour en arrière : on ne sait pas distinguer ces valeurs de celles saisies ensuite par l'équipe.
    operations = [migrations.RunPython(remplir, migrations.RunPython.noop)]
