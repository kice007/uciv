"""
Vues de l'application `app`.

Une vue reçoit la requête du navigateur, prépare les données (le « contexte »)
et les envoie à un gabarit HTML qui produit la page.
"""
from django.shortcuts import render

from . import content


def home(request):
    """Page d'accueil."""
    context = {
        'parcours': content.PARCOURS,
        'preuves': content.PREUVES,
        'domaines': content.DOMAINES,
        'programmes': content.PROGRAMMES,
        'indicateurs': content.INDICATEURS,
        'facons': content.FACONS_DE_S_ENGAGER,
        'article_une': content.ARTICLE_A_LA_UNE,
        'articles': content.AUTRES_ARTICLES,
        'partenaires': content.PARTENAIRES,
    }
    return render(request, 'app/layout/index.html', context)


def uciv_leadership(request):
    """Page du programme UCIV Leadership."""
    return render(request, 'app/layout/uciv_leadership.html', {'leadership': content.LEADERSHIP})
