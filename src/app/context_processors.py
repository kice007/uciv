"""
Processeurs de contexte.

Un processeur de contexte ajoute des variables à TOUS les gabarits du site,
sans avoir à les passer depuis chaque vue. On s'en sert pour ce qui est commun
à toutes les pages : la navigation, le pied de page, les coordonnées.
Il est déclaré dans `config/settings.py` (TEMPLATES > context_processors).
"""
from . import content


def site(request):
    return {
        'annonce': content.ANNONCE,
        'navigation': content.NAVIGATION,
        'pied_colonnes': content.PIED_COLONNES,
        'coordonnees': content.COORDONNEES,
        'reseaux': content.RESEAUX,
        'mentions': content.MENTIONS,
    }
