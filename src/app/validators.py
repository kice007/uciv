"""Contrôle des fichiers téléversés depuis l'administration.

Les fichiers de `/media/` sont servis depuis le domaine du site : un HTML ou un SVG envoyé tel quel pourrait y
exécuter du code. On n'accepte donc que des formats de documents et d'images sans script.
"""
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, RegexValidator
from django.utils.deconstruct import deconstructible

TAILLE_MAX = 10 * 1024 * 1024  # 10 Mo, comme la limite de Nginx

_POSITION = r'(left|center|right|top|bottom|\d{1,3}%)'
# Cadrage d'une image : un ou deux mots-clés ou pourcentages (valeur de object-position), rien d'autre.
valider_position_image = RegexValidator(
    regex=rf'^{_POSITION}( {_POSITION})?$',
    message="Cadrage invalide. Exemples : « center », « center 20% », « 60% center ».")

EXTENSIONS_IMAGES = ['jpg', 'jpeg', 'png', 'webp', 'gif']
EXTENSIONS_DOCUMENTS = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'odt', 'ods', 'odp', 'zip',
                        'jpg', 'jpeg', 'png', 'webp']


@deconstructible
class TailleMax:
    """Refuse les fichiers de plus de `taille` octets."""

    def __init__(self, taille=TAILLE_MAX):
        self.taille = taille

    def __call__(self, fichier):
        if fichier.size > self.taille:
            raise ValidationError(f'Le fichier dépasse {self.taille // (1024 * 1024)} Mo.', code='taille')

    def __eq__(self, autre):
        return isinstance(autre, TailleMax) and self.taille == autre.taille


valider_image = [FileExtensionValidator(EXTENSIONS_IMAGES), TailleMax()]
valider_document = [FileExtensionValidator(EXTENSIONS_DOCUMENTS), TailleMax()]
