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


def qui_sommes_nous(request):
    """Page « Qui sommes-nous ? »."""
    return render(request, 'app/layout/qui_sommes_nous.html', {'qui': content.QUI_SOMMES_NOUS})


def nos_programmes(request):
    """Page « Nos programmes »."""
    return render(request, 'app/layout/nos_programmes.html', {'np': content.NOS_PROGRAMMES})


def go_du_digital(request):
    """Page du programme Les Go du Digital."""
    return render(request, 'app/layout/go_du_digital.html', {'gd': content.GO_DU_DIGITAL})


def experience_lab(request):
    """Page du programme Experience Lab."""
    return render(request, 'app/layout/experience_lab.html', {'el': content.EXPERIENCE_LAB})


def equipe(request):
    """Page « Équipe »."""
    return render(request, 'app/layout/equipe.html', {'eq': content.EQUIPE})
