"""
Vues de l'application `app`.

Une vue reçoit la requête du navigateur, prépare les données (le « contexte »)
et les envoie à un gabarit HTML qui produit la page.
"""
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse

from core.utils import send_customize_email

from . import content
from .forms import ContactForm, EngagementForm, PartenariatForm
from .models import SoumissionContact, SoumissionEngagement, SoumissionPartenariat


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


def engagement(request):
    """Page « Je veux m'engager » : présentation des 3 façons et formulaire d'engagement."""
    if request.method == 'POST':
        form = EngagementForm(request.POST)
        if form.is_valid():
            donnees = form.cleaned_data
            soumission = SoumissionEngagement.objects.create(
                nom=donnees['nom'], email=donnees['email'], telephone=donnees['telephone'],
                choix=donnees['choix'], competences=', '.join(donnees['competences']),
                message=donnees['message'],
            )
            if settings.EMAIL_HOST:
                send_customize_email(
                    f"Nouvelle demande d'engagement : {soumission.nom}",
                    [settings.CONTACT_EMAIL], 'emails/engagement.html', {'soumission': soumission},
                    reply_to=[soumission.email],
                )
            messages.success(request, content.ENGAGEMENT['merci'])
            return redirect(reverse('app:engagement') + '#formulaire')
    else:
        form = EngagementForm(initial={'choix': request.GET.get('choix')})
    return render(request, 'app/layout/engagement.html', {'eng': content.ENGAGEMENT, 'form': form})


def partenaires(request):
    """Page « Partenaires » : collaborations existantes, formes de partenariat et formulaire."""
    if request.method == 'POST':
        form = PartenariatForm(request.POST)
        if form.is_valid():
            soumission = SoumissionPartenariat.objects.create(
                **{cle: form.cleaned_data[cle] for cle in
                   ('nom', 'organisation', 'email', 'telephone', 'type_collaboration', 'message')}
            )
            if settings.EMAIL_HOST:
                send_customize_email(
                    f'Nouvelle proposition de partenariat : {soumission.organisation}',
                    [settings.CONTACT_EMAIL], 'emails/partenariat.html', {'soumission': soumission},
                    reply_to=[soumission.email],
                )
            messages.success(request, content.PAGE_PARTENAIRES['merci'])
            return redirect(reverse('app:partenaires') + '#proposer')
    else:
        form = PartenariatForm()
    return render(request, 'app/layout/partenaires.html', {'par': content.PAGE_PARTENAIRES, 'form': form})


def contact(request):
    """Page « Contact » : formulaire et coordonnées officielles."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            soumission = SoumissionContact.objects.create(
                **{cle: form.cleaned_data[cle] for cle in
                   ('nom', 'email', 'telephone', 'organisation', 'objet', 'message')}
            )
            if settings.EMAIL_HOST:
                send_customize_email(
                    f'Message de contact : {soumission.objet} — {soumission.nom}',
                    [settings.CONTACT_EMAIL], 'emails/contact.html', {'soumission': soumission},
                    reply_to=[soumission.email],
                )
            messages.success(request, content.CONTACT['merci'])
            return redirect(reverse('app:contact') + '#ecrire')
    else:
        form = ContactForm(initial={'objet': request.GET.get('objet')})
    return render(request, 'app/layout/contact.html', {'ct': content.CONTACT, 'form': form})
