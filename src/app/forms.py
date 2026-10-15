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


class EngagementForm(forms.Form):
    nom = forms.CharField(label='Nom et prénom', max_length=120)
    email = forms.EmailField(label='Adresse e-mail', max_length=254)
    telephone = forms.CharField(label='Téléphone', max_length=30, required=False)
    choix = forms.ChoiceField(label='Je souhaite', choices=CHOIX, widget=forms.RadioSelect)
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
