import secrets

from django.db import models
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone

from .validators import valider_document, valider_image, valider_position_image

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

    POLES = [
        ('projet-universitaire', 'Projet universitaire'),
        ('cercle-des-leaders', 'Cercle des leaders'),
        ('jeune-porteur-idee', "Jeune porteur d'idée"),
    ]

    nom = models.CharField('nom et prénom', max_length=120)
    email = models.EmailField('adresse e-mail')
    telephone = models.CharField('téléphone', max_length=30, blank=True)
    choix = models.CharField('souhaite', max_length=20, choices=CHOIX)
    pole = models.CharField('pôle', max_length=30, choices=POLES, blank=True)
    structure = models.CharField('université ou structure', max_length=160, blank=True)
    conditions_acceptees = models.BooleanField('conditions acceptées', default=False)
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
                             help_text="Ex. app/assets/img/groupe-nb.webp ; ignoré si une image est téléversée.")
    image_televersee = models.ImageField('image téléversée', upload_to='articles/', blank=True,
                                         validators=valider_image)
    image_alt = models.CharField('texte alternatif de l\'image', max_length=200, blank=True)
    image_legende = models.CharField('légende de l\'image', max_length=200, blank=True)
    image_position = models.CharField(
        'cadrage de l\'image', max_length=40, default='center', validators=[valider_position_image],
        help_text="Zone qui reste visible quand l'image est recadrée. Ex. « center 20% » (plus haut), « 60% center » "
                  "(plus à droite).")

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
    fichier = models.FileField(upload_to='ressources/', blank=True, validators=valider_document)
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
    prefixe = models.CharField('préfixe', max_length=3, blank=True,
                               help_text='Affiché devant le chiffre, ex. « + » pour « +1 800 ».')
    valeur = models.PositiveIntegerField(null=True, blank=True,
                                         help_text='Laisser vide tant que le chiffre n\'est pas vérifié.')
    ordre = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'indicateur'
        ordering = ['ordre', 'id']

    def __str__(self):
        return self.libelle

    @property
    def valeur_affichee(self):
        """Chiffre affiché sur le site : préfixe et séparateur de milliers (« +1 800 »), vide si non renseigné."""
        if self.valeur is None:
            return ''
        return f'{self.prefixe}{self.valeur:,}'.replace(',', ' ')


def _nouveau_jeton():
    return secrets.token_urlsafe(24)


class Abonne(models.Model):
    """Abonné à la lettre d'information (formulaire du pied de page).

    Le site ne fait que collecter les adresses : l'équipe exporte la liste des abonnés
    actifs depuis l'administration (action « Exporter en CSV ») et envoie la lettre avec
    son outil d'envoi. Le jeton sert au lien de désinscription personnel.
    """
    email = models.EmailField('adresse e-mail', unique=True)
    actif = models.BooleanField('abonné', default=True)
    jeton = models.CharField(max_length=40, unique=True, default=_nouveau_jeton, editable=False)
    inscrit_le = models.DateTimeField('inscription', auto_now_add=True)
    desinscrit_le = models.DateTimeField('désinscription', null=True, blank=True)

    class Meta:
        verbose_name = "abonné à la lettre d'information"
        verbose_name_plural = "abonnés à la lettre d'information"
        ordering = ('-inscrit_le',)

    def __str__(self):
        return self.email

    @property
    def email_masque(self):
        """Adresse affichée sur la page de désinscription : « a••••@gmail.com »."""
        nom, _, domaine = self.email.partition('@')
        return f'{nom[:1]}••••@{domaine}'


class Visite(models.Model):
    """Une page vue (mesure d'audience sans cookie, voir app/mesure.py). Affichée dans Statistiques."""

    APPAREILS = [('ordinateur', 'Ordinateur'), ('mobile', 'Mobile'), ('tablette', 'Tablette')]

    date = models.DateTimeField('date', default=timezone.now, db_index=True)
    chemin = models.CharField('page', max_length=300)
    visiteur = models.CharField('code visiteur du jour', max_length=20, db_index=True,
                                help_text="Anonyme : change chaque jour, ne permet pas de retrouver l'adresse IP.")
    referent = models.CharField("provenance (domaine)", max_length=120, blank=True)
    appareil = models.CharField(max_length=12, choices=APPAREILS, default='ordinateur')
    duree = models.PositiveIntegerField('temps passé (secondes)', null=True, blank=True)

    class Meta:
        verbose_name = 'statistiques de visites'
        verbose_name_plural = 'statistiques'
        ordering = ['-date']
        indexes = [models.Index(fields=['date', 'chemin'])]

    def __str__(self):
        return f'{self.chemin} ({self.date:%d/%m/%Y %H:%M})'


class EvenementSecurite(models.Model):
    """Une attaque ou un comportement suspect vu par le site (voir app/mesure.py). Affiché dans Sécurité, conservé 90 jours."""

    TYPES = [
        ('sonde', 'Sonde de robot'),
        ('injection', "Tentative d'injection"),
        ('limite', 'Trop de demandes (429)'),
        ('piege', 'Robot piégé dans un formulaire'),
        ('connexion', "Échec de connexion à l'administration"),
        ('refus', 'Requête refusée (400 / 403)'),
    ]

    date = models.DateTimeField('date', default=timezone.now, db_index=True)
    type = models.CharField(max_length=12, choices=TYPES, db_index=True)
    chemin = models.CharField('adresse demandée', max_length=300, blank=True)
    detail = models.CharField(max_length=200, blank=True)
    ip = models.CharField('adresse IP', max_length=45, db_index=True)

    class Meta:
        verbose_name = 'événements de sécurité'
        verbose_name_plural = 'sécurité'
        ordering = ['-date']

    def __str__(self):
        return f'{self.get_type_display()} depuis {self.ip}'
