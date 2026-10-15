from django.db import models

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
