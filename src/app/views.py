"""
Vues de l'application `app`.

Une vue reçoit la requête du navigateur, prépare les données (le « contexte »)
et les envoie à un gabarit HTML qui produit la page.
"""
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils.http import urlencode

from core.utils import send_customize_email

from . import content
from .forms import ContactForm, EngagementForm, PartenariatForm
from .models import (
    Article, Indicateur, Opportunite, Ressource, SoumissionContact, SoumissionEngagement,
    SoumissionPartenariat,
)


def _carte_article(article):
    """Article de la base, au format attendu par le gabarit de l'accueil."""
    return {
        'categorie': article.etiquette_affichee, 'theme': article.theme, 'meta': article.meta,
        'titre': article.titre, 'chapo': article.chapo, 'image_url': article.image_url,
        'image_alt': article.image_alt, 'position': 'center', 'detouree': False,
        'url': reverse('app:article', args=[article.slug]),
    }


def _carte_contenu(carte):
    """Article provisoire de content.py (utilisé tant que la base ne contient aucun article publié)."""
    return dict(carte, image_url=static(carte['image']))


def home(request):
    """Page d'accueil."""
    context = {
        'parcours': content.PARCOURS,
        'preuves': content.PREUVES,
        'domaines': content.DOMAINES,
        'programmes': content.PROGRAMMES,
        'indicateurs': content.INDICATEURS,
        'facons': content.FACONS_DE_S_ENGAGER,
        'article_une': _carte_contenu(content.ARTICLE_A_LA_UNE),
        'articles': [_carte_contenu(a) for a in content.AUTRES_ARTICLES],
        'partenaires': content.PARTENAIRES,
    }
    publies = Article.objects.filter(publish=True, histoire=False)
    une = publies.filter(a_la_une=True).first() or publies.first()
    if une:
        context['article_une'] = _carte_article(une)
        context['articles'] = [_carte_article(a) for a in publies.exclude(pk=une.pk)[:3]]
    indicateurs = Indicateur.objects.filter(publish=True)
    if indicateurs:
        context['indicateurs'] = [{'valeur': i.valeur, 'label': i.libelle} for i in indicateurs]
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

# --- Pages alimentées par la base -------------------------------------------


def _pastilles(request, cle, choix, actuel, conserver=()):
    """Pastilles de filtre : « Toutes » puis un lien par choix, en gardant les autres filtres."""
    base = {k: request.GET[k] for k in conserver if request.GET.get(k)}

    def lien(valeur):
        params = dict(base)
        if valeur:
            params[cle] = valeur
        return '?' + urlencode(params) if params else '?'

    pastilles = [{'label': 'Toutes', 'url': lien(''), 'actif': not actuel}]
    pastilles += [{'label': libelle, 'url': lien(valeur), 'actif': valeur == actuel} for valeur, libelle in choix]
    return pastilles


def opportunites(request):
    """Page « Opportunités » : catégories et fiches filtrables."""
    categorie = request.GET.get('categorie', '')
    if categorie not in dict(Opportunite.CATEGORIES):
        categorie = ''
    fiches = Opportunite.objects.filter(publish=True)
    if categorie:
        fiches = fiches.filter(categorie=categorie)
    fiches = list(fiches)
    return render(request, 'app/layout/opportunites.html', {
        'page': content.OPPORTUNITES_PAGE,
        'opportunites': fiches,
        'chips': _pastilles(request, 'categorie', Opportunite.CATEGORIES, categorie),
        'modele': any(f.modele for f in fiches),
    })


def actualites(request):
    """Page « Actualités » : article à la une, fil filtrable par catégorie et pagination."""
    categorie = request.GET.get('categorie', '')
    if categorie not in dict(Article.CATEGORIES):
        categorie = ''
    articles = Article.objects.filter(publish=True, histoire=False)
    if categorie:
        articles = articles.filter(categorie=categorie)
    une = articles.filter(a_la_une=True).first()
    reste = articles.exclude(pk=une.pk) if une else articles
    paginateur = Paginator(reste, content.ACTUALITES_PAGE['par_page'])
    page_obj = paginateur.get_page(request.GET.get('page'))

    def lien_page(numero):
        params = {'categorie': categorie} if categorie else {}
        if numero > 1:
            params['page'] = numero
        return '?' + urlencode(params) if params else '?'

    pagination = []
    if paginateur.num_pages > 1:
        pagination = [{'numero': n, 'url': lien_page(n), 'actif': n == page_obj.number}
                      for n in paginateur.page_range]
    return render(request, 'app/layout/actualites.html', {
        'page': content.ACTUALITES_PAGE,
        'une': une,
        'page_obj': page_obj,
        'pagination': pagination,
        'suivant': lien_page(page_obj.next_page_number()) if page_obj.has_next() else '',
        'chips': _pastilles(request, 'categorie', Article.CATEGORIES, categorie),
    })


def article(request, slug):
    """Page d'un article, avec trois suggestions « À lire aussi »."""
    fiche = get_object_or_404(Article, slug=slug, publish=True)
    autres = Article.objects.filter(publish=True, histoire=False).exclude(pk=fiche.pk)[:3]
    return render(request, 'app/layout/article.html', {
        'page': content.ARTICLE_PAGE,
        'article': fiche,
        'autres': autres,
        'url_complete': request.build_absolute_uri(),
    })


def impact(request):
    """Page « Notre impact » : indicateurs et histoires."""
    couleurs = content.IMPACT_PAGE['couleurs']
    indicateurs = [
        {'libelle': i.libelle, 'valeur': i.valeur, 'couleur': couleurs[n % len(couleurs)]}
        for n, i in enumerate(Indicateur.objects.filter(publish=True))
    ]
    histoires = Article.objects.filter(publish=True, histoire=True)[:3]
    return render(request, 'app/layout/impact.html', {
        'page': content.IMPACT_PAGE, 'indicateurs': indicateurs, 'histoires': histoires,
    })


def ressources(request):
    """Page « Ressources » : bibliothèque filtrable par type et par thème."""
    type_ = request.GET.get('type', '')
    theme = request.GET.get('theme', '')
    if type_ not in dict(Ressource.TYPES):
        type_ = ''
    if theme not in dict(Ressource.THEMES):
        theme = ''
    fiches = Ressource.objects.filter(publish=True)
    if type_:
        fiches = fiches.filter(type=type_)
    if theme:
        fiches = fiches.filter(theme=theme)
    fiches = list(fiches)
    for fiche in fiches:
        fiche.picto = content.RESSOURCES_PAGE['types'][fiche.type]
    return render(request, 'app/layout/ressources.html', {
        'page': content.RESSOURCES_PAGE,
        'ressources': fiches,
        'chips_type': _pastilles(request, 'type', Ressource.TYPES, type_, conserver=('theme',)),
        'chips_theme': _pastilles(request, 'theme', Ressource.THEMES, theme, conserver=('type',)),
        'modele': any(f.modele for f in fiches),
    })


def page_legale(request, cle):
    """Pages légales : mentions légales, politique de confidentialité, conditions d'utilisation."""
    page = content.LEGAL[cle]
    documents = [dict(doc, actuel=doc['cle'] == cle) for doc in content.LEGAL_DOCUMENTS]
    return render(request, 'app/layout/legal.html', {'page': page, 'documents': documents})


def page_introuvable(request, exception=None):
    """Page d'erreur 404 (branchée par `handler404` dans core/urls.py)."""
    return render(request, 'app/layout/404.html', {'page': content.PAGE_404}, status=404)
