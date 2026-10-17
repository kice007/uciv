from django.db import models
from django.templatetags.static import static
from django.urls import reverse

class Convention(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    publish = models.BooleanField(default=False)

    class Meta:
        abstract = True


class SoumissionEngagement(Convention):
    """Demande envoyée depuis le formulaire « Je veux m'engager »."""

    CHOIX = [
        ('volontaire', 'Devenir volontaire'),
        ('leadership', 'Rejoindre UCIV Leadership'),
        ('competences', 'Proposer mes compétences'),
    ]

    nom = models.CharField('nom et prénom', max_length=120)
    email = models.EmailField('adresse e-mail')
    telephone = models.CharField('téléphone', max_length=30, blank=True)
    choix = models.CharField('souhaite', max_length=20, choices=CHOIX)
    competences = models.TextField('domaines de compétences', blank=True)
    message = models.TextField('ce qu\'il ou elle veut apporter', blank=True)

    class Meta:
        verbose_name = "demande d'engagement"
        verbose_name_plural = "demandes d'engagement"
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.nom} — {self.get_choix_display()}'


class SoumissionPartenariat(Convention):
    """Proposition envoyée depuis le formulaire de la page Partenaires."""

    nom = models.CharField('nom et prénom', max_length=120)
    organisation = models.CharField(max_length=160)
    email = models.EmailField('adresse e-mail')
    telephone = models.CharField('téléphone', max_length=30, blank=True)
    type_collaboration = models.CharField('type de collaboration', max_length=80)
    message = models.TextField('présentation et idée de collaboration')

    class Meta:
        verbose_name = 'proposition de partenariat'
        verbose_name_plural = 'propositions de partenariat'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.organisation} — {self.nom}'


class SoumissionContact(Convention):
    """Message envoyé depuis le formulaire de la page Contact."""

    nom = models.CharField('nom et prénom', max_length=120)
    email = models.EmailField('adresse e-mail')
    telephone = models.CharField('téléphone', max_length=30, blank=True)
    organisation = models.CharField(max_length=160, blank=True)
    objet = models.CharField(max_length=60)
    message = models.TextField()

    class Meta:
        verbose_name = 'message de contact'
        verbose_name_plural = 'messages de contact'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.nom} — {self.objet}'

# --- Contenu éditorial géré depuis l'administration --------------------------


class Article(Convention):
    """Actualité du site (liste « Actualités », page « Article », accueil)."""

    CATEGORIES = [
        ('activites', 'Nos activités'),
        ('programmes', 'Nos programmes'),
        ('evenements', 'Nos événements'),
        ('partenariats', 'Nos partenariats'),
        ('temoignages', 'Témoignages'),
        ('portraits', 'Portraits'),
        ('employabilite', 'Employabilité'),
        ('leadership', 'Leadership'),
        ('engagement', 'Engagement citoyen'),
    ]
    THEMES = [
        ('orange', 'Orange'), ('jaune', 'Jaune'), ('vert', 'Vert'),
        ('brun', 'Brun'), ('profond', 'Vert profond'),
    ]

    titre = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    categorie = models.CharField('catégorie', max_length=20, choices=CATEGORIES)
    etiquette = models.CharField('étiquette (remplace la catégorie)', max_length=40, blank=True)
    theme = models.CharField('couleur de l\'étiquette', max_length=10, choices=THEMES, default='orange')
    meta = models.CharField('repère (date, lieu, thème…)', max_length=80, blank=True)
    chapo = models.TextField('résumé', blank=True)
    corps = models.TextField('texte de l\'article', blank=True,
                             help_text='Un paragraphe par ligne vide. Pas de mise en forme.')
    auteur = models.CharField(max_length=80, default="l'équipe UCIV")
    date_publication = models.DateField('date de publication')
    temps_lecture = models.PositiveSmallIntegerField('temps de lecture (minutes)', default=3)
    a_la_une = models.BooleanField('à la une', default=False)
    histoire = models.BooleanField('afficher dans « Nos histoires » (Notre impact)', default=False)
    image = models.CharField('image (chemin statique)', max_length=300, blank=True,
                             help_text="Ex. app/assets/img/groupe-nb.png ; ignoré si une image est téléversée.")
    image_televersee = models.FileField('image téléversée', upload_to='articles/', blank=True)
    image_alt = models.CharField('texte alternatif de l\'image', max_length=200, blank=True)
    image_legende = models.CharField('légende de l\'image', max_length=200, blank=True)

    class Meta:
        verbose_name = 'article'
        ordering = ['-date_publication', '-created_at']

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('app:article', args=[self.slug])

    @property
    def etiquette_affichee(self):
        return self.etiquette or self.get_categorie_display()

    @property
    def image_url(self):
        if self.image_televersee:
            return self.image_televersee.url
        if self.image:
            return static(self.image)
        return ''


class Opportunite(Convention):
    """Opportunité proposée par UCIV ou ses partenaires (page « Opportunités »)."""

    CATEGORIES = [
        ('volontariat', 'Volontariat'),
        ('formations', 'Formations'),
        ('stages', 'Stages'),
        ('emploi', 'Emploi'),
        ('appels', 'Appels à candidatures'),
    ]

    categorie = models.CharField('catégorie', max_length=20, choices=CATEGORIES)
    intitule = models.CharField('intitulé', max_length=200)
    source = models.CharField(max_length=60, default='UCIV', help_text='UCIV, Partenaire…')
    structure = models.CharField(max_length=160, blank=True)
    lieu = models.CharField(max_length=160, blank=True)
    date_limite = models.DateField('date limite', null=True, blank=True)
    description = models.TextField(blank=True)
    lien = models.URLField('lien pour candidater', blank=True)
    modele = models.BooleanField('fiche d\'exemple (emplacement à remplacer)', default=False)

    class Meta:
        verbose_name = 'opportunité'
        ordering = ['date_limite', '-created_at']

    def __str__(self):
        return self.intitule


class Ressource(Convention):
    """Ressource de la bibliothèque (page « Ressources »)."""

    TYPES = [
        ('guide', 'Guide'),
        ('manuel', 'Manuel'),
        ('support', 'Support de formation'),
        ('article', 'Article'),
        ('video', 'Vidéo'),
        ('podcast', 'Podcast'),
    ]
    THEMES = [
        ('employabilite', 'Employabilité'),
        ('leadership', 'Leadership'),
        ('numerique', 'Numérique'),
        ('volontariat', 'Volontariat'),
    ]

    titre = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPES)
    theme = models.CharField('thème', max_length=20, choices=THEMES)
    meta = models.CharField('format / durée', max_length=120, blank=True,
                            help_text='Ex. PDF · 24 pages, 12 min de lecture, 38 min…')
    fichier = models.FileField(upload_to='ressources/', blank=True)
    lien = models.URLField(blank=True, help_text='Utilisé si aucun fichier n\'est téléversé.')
    modele = models.BooleanField('fiche d\'exemple (emplacement à remplacer)', default=False)

    class Meta:
        verbose_name = 'ressource'
        ordering = ['-created_at']

    def __str__(self):
        return self.titre

    @property
    def url(self):
        if self.fichier:
            return self.fichier.url
        return self.lien


class Indicateur(Convention):
    """Chiffre d'impact (page « Notre impact », section « Vision & chiffres » de l'accueil)."""

    libelle = models.CharField('libellé', max_length=80)
    valeur = models.PositiveIntegerField(null=True, blank=True,
                                         help_text='Laisser vide tant que le chiffre n\'est pas vérifié.')
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'indicateur'
        ordering = ['ordre', 'id']

    def __str__(self):
        return self.libelle
