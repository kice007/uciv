"""Images du site converties en WebP (outils/convertir_images.py) : les articles déjà enregistrés pointent
encore vers les anciens fichiers .jpg / .png, qui ne sont plus servis."""
from django.db import migrations, models

CONVERTIES = {
    'affiche-leadership-jaune', 'experience-lab', 'go-du-digital', 'groupe-couleur', 'groupe-nb',
    'logo-uciv-leadership', 'marshall-kouame', 'partenariat-paipro', 'rencontre-galerie', 'volontaires-terrain',
}
PREFIXE = 'app/assets/img/'


def vers_webp(apps, schema_editor):
    Article = apps.get_model('app', 'Article')
    for article in Article.objects.filter(image__startswith=PREFIXE):
        nom, _, extension = article.image[len(PREFIXE):].rpartition('.')
        if nom in CONVERTIES and extension in ('jpg', 'png'):
            article.image = f'{PREFIXE}{nom}.webp'
            article.save(update_fields=['image'])


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_date_lancement_leadership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.CharField(blank=True, help_text='Ex. app/assets/img/groupe-nb.webp ; ignoré si une image est téléversée.', max_length=300, verbose_name='image (chemin statique)'),
        ),
        # Pas de retour en arrière utile : les anciens fichiers ne sont plus dans le dossier servi.
        migrations.RunPython(vers_webp, migrations.RunPython.noop),
    ]
