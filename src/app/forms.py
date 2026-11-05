from django import forms

CHOIX = [
    ('volontaire', 'Devenir volontaire'),
    ('leadership', 'Rejoindre UCIV Leadership'),
    ('competences', 'Proposer mes compétences'),
]

COMPETENCES = [
    'Communication', 'Graphisme', 'Audiovisuel', 'Photographie', 'Formation',
    'Événementiel', 'Ressources humaines', 'Gestion de projet', 'Numérique',
    'Développement web',
]

POLES = [
    ('projet-universitaire', 'Projet universitaire'),
    ('cercle-des-leaders', 'Cercle des leaders'),
    ('jeune-porteur-idee', "Jeune porteur d'idée"),
]


class EngagementForm(forms.Form):
    nom = forms.CharField(label='Nom et prénom', max_length=120)
    email = forms.EmailField(label='Adresse e-mail', max_length=254)
    telephone = forms.CharField(label='Téléphone (WhatsApp)', max_length=30, required=False)
    choix = forms.ChoiceField(label='Je souhaite', choices=CHOIX, widget=forms.RadioSelect)
    pole = forms.ChoiceField(
        label='Mon pôle', required=False,
        choices=[('', 'Choisis ton pôle')] + POLES,
    )
    structure = forms.CharField(label='Mon université ou ma structure', max_length=160, required=False)
    conditions = forms.BooleanField(
        label="J'ai lu les conditions d'adhésion et de cotisation de mon pôle.",
        required=False,
    )
    competences = forms.MultipleChoiceField(
        label='Mes domaines de compétences', required=False,
        choices=[(c, c) for c in COMPETENCES], widget=forms.CheckboxSelectMultiple,
    )
    message = forms.CharField(label="Ce que tu as envie d'apporter", required=False,
                              max_length=2000, widget=forms.Textarea)
    # Champ piège : invisible pour les personnes, rempli par les robots.
    site_web = forms.CharField(required=False)

    def clean_site_web(self):
        if self.cleaned_data.get('site_web'):
            raise forms.ValidationError('Envoi refusé.')
        return ''

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('choix') == 'leadership':
            if not cleaned.get('pole'):
                self.add_error('pole', 'Choisis ton pôle.')
            if not cleaned.get('conditions'):
                self.add_error(
                    'conditions',
                    "Merci de confirmer que tu as lu les conditions d'adhésion et de cotisation de ton pôle.",
                )
        else:
            # Ces champs ne concernent que les candidatures à UCIV Leadership.
            cleaned['pole'] = ''
            cleaned['structure'] = ''
            cleaned['conditions'] = False
        return cleaned


TYPES_COLLABORATION = [
    'Partenariats institutionnels', 'Partenariats techniques', 'Partenariats financiers',
    'Sponsoring', 'Mécénat', 'Collaborations sur des programmes', 'Formations',
    'Opportunités de stage', 'Opportunités professionnelles', 'Projets communs',
]


class PartenariatForm(forms.Form):
    nom = forms.CharField(label='Nom et prénom', max_length=120)
    organisation = forms.CharField(label='Organisation', max_length=160)
    email = forms.EmailField(label='Adresse e-mail', max_length=254)
    telephone = forms.CharField(label='Téléphone', max_length=30, required=False)
    type_collaboration = forms.ChoiceField(
        label='Type de collaboration envisagée', choices=[(t, t) for t in TYPES_COLLABORATION],
    )
    message = forms.CharField(label='Présentation et idée de collaboration', max_length=3000,
                              widget=forms.Textarea)
    # Champ piège : invisible pour les personnes, rempli par les robots.
    site_web = forms.CharField(required=False)

    def clean_site_web(self):
        if self.cleaned_data.get('site_web'):
            raise forms.ValidationError('Envoi refusé.')
        return ''


OBJETS = [
    'Devenir volontaire', 'Programme', 'UCIV Leadership', 'Partenariat',
    'Proposition de compétences', 'Presse-média', 'Autre',
]


class ContactForm(forms.Form):
    nom = forms.CharField(label='Nom et prénom', max_length=120)
    email = forms.EmailField(label='Adresse e-mail', max_length=254)
    telephone = forms.CharField(label='Téléphone', max_length=30, required=False)
    organisation = forms.CharField(label='Organisation', max_length=160, required=False)
    objet = forms.ChoiceField(label='Objet', choices=[(o, o) for o in OBJETS])
    message = forms.CharField(label='Message', max_length=3000, widget=forms.Textarea)
    # Champ piège : invisible pour les personnes, rempli par les robots.
    site_web = forms.CharField(required=False)

    def clean_site_web(self):
        if self.cleaned_data.get('site_web'):
            raise forms.ValidationError('Envoi refusé.')
        return ''


class NewsletterForm(forms.Form):
    email = forms.EmailField(label='Votre adresse e-mail', max_length=254)
    # Champ piège : invisible pour les personnes, rempli par les robots.
    site_web = forms.CharField(required=False)

    def clean_site_web(self):
        if self.cleaned_data.get('site_web'):
            raise forms.ValidationError('Envoi refusé.')
        return ''
