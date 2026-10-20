"""
Vues de l'application `app`.

Une vue reçoit la requête du navigateur, prépare les données (le « contexte »)
et les envoie à un gabarit HTML qui produit la page.
"""
import unicodedata

from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme, urlencode
from django.views.decorators.http import require_POST

from core.utils import send_customize_email

from . import content
from . import seo as referencement
from .ratelimit import limiter
from .forms import ContactForm, EngagementForm, NewsletterForm, PartenariatForm
from .models import (
    Abonne, Article, Indicateur, Opportunite, Ressource, SoumissionContact, SoumissionEngagement,
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
        context['indicateurs'] = [{'valeur': i.valeur_affichee, 'label': i.libelle} for i in indicateurs]
    context['indicateurs_incomplets'] = any(not i['valeur'] for i in context['indicateurs'])
    return render(request, 'app/layout/index.html', context)


def uciv_leadership(request):
    """Page du programme UCIV Leadership."""
    return render(request, 'app/layout/uciv_leadership.html', {'leadership': content.LEADERSHIP})


def programme_leadership(request, cle):
    """Page d'un programme d'UCIV Leadership (« De la vision à l'action », « Les RH ont la parole »)."""
    return render(request, 'app/layout/programme_leadership.html', {'pl': content.PROGRAMMES_LEADERSHIP[cle]})


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


@limiter('engagement', 5, 10 * 60)
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


@limiter('partenariat', 5, 10 * 60)
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


@limiter('contact', 5, 10 * 60)
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
        'seo': referencement.pour_article(request, fiche),
    })


def impact(request):
    """Page « Notre impact » : indicateurs et histoires."""
    couleurs = content.IMPACT_PAGE['couleurs']
    indicateurs = [
        {'libelle': i.libelle, 'valeur': i.valeur_affichee, 'couleur': couleurs[n % len(couleurs)]}
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


def _sans_accents(texte):
    return ''.join(c for c in unicodedata.normalize('NFD', texte.lower()) if not unicodedata.combining(c))


def recherche(request):
    """Page « Rechercher » : pages du site, actualités, opportunités et ressources contenant les mots cherchés."""
    requete = ' '.join(request.GET.get('q', '').split())[:100]
    resultats = []
    if requete:
        mots = _sans_accents(requete).split()
        for nom in content.PAGES_INDEXABLES:
            page = content.SEO_PAGES[nom]
            texte = ' '.join([page['titre'], page['description']] + [q + ' ' + r for q, r in content.FAQ.get(nom, [])])
            if all(mot in _sans_accents(texte) for mot in mots):
                resultats.append({'type': 'Page', 'titre': page['titre'].split(' — ')[0].split(' | ')[0],
                                  'texte': page['description'], 'url': reverse('app:' + nom)})
        filtre_article, filtre_opportunite, filtre_ressource = Q(), Q(), Q()
        for mot in requete.split():
            filtre_article &= Q(titre__icontains=mot) | Q(chapo__icontains=mot) | Q(corps__icontains=mot)
            filtre_opportunite &= (Q(intitule__icontains=mot) | Q(description__icontains=mot)
                                   | Q(structure__icontains=mot))
            filtre_ressource &= Q(titre__icontains=mot) | Q(meta__icontains=mot)
        for a in Article.objects.filter(filtre_article, publish=True)[:10]:
            resultats.append({'type': a.etiquette_affichee, 'titre': a.titre, 'texte': a.chapo,
                              'url': a.get_absolute_url()})
        for o in Opportunite.objects.filter(filtre_opportunite, publish=True, modele=False)[:10]:
            resultats.append({'type': 'Opportunité', 'titre': o.intitule, 'texte': o.description,
                              'url': o.lien or reverse('app:opportunites')})
        for r in Ressource.objects.filter(filtre_ressource, publish=True, modele=False)[:10]:
            resultats.append({'type': 'Ressource', 'titre': r.titre, 'texte': r.meta,
                              'url': r.url or reverse('app:ressources')})
    return render(request, 'app/layout/recherche.html', {
        'page': content.RECHERCHE_PAGE, 'requete': requete, 'resultats': resultats,
    })


def robots_txt(request):
    """robots.txt : tout est exploré sauf l'administration ; le sitemap est annoncé."""
    return HttpResponse(referencement.texte_robots(request), content_type='text/plain; charset=utf-8')


def llms_txt(request):
    """llms.txt : présentation du site pour les moteurs de réponse (IA)."""
    return HttpResponse(referencement.texte_llms(request), content_type='text/plain; charset=utf-8')


def page_legale(request, cle):
    """Pages légales : mentions légales, politique de confidentialité, conditions d'utilisation."""
    page = content.LEGAL[cle]
    documents = [dict(doc, actuel=doc['cle'] == cle) for doc in content.LEGAL_DOCUMENTS]
    return render(request, 'app/layout/legal.html', {'page': page, 'documents': documents})


def page_introuvable(request, exception=None):
    """Page d'erreur 404 (branchée par `handler404` dans core/urls.py)."""
    return render(request, 'app/layout/404.html', {'page': content.PAGE_404}, status=404)


@require_POST
@limiter('newsletter', 5, 10 * 60)
def newsletter_inscription(request):
    """Formulaire « Lettre d'information » du pied de page.

    Enregistre l'adresse, puis revient sur la page d'origine, au niveau de la carte
    (#lettre), qui affiche l'état : inscription réussie, déjà inscrit ou adresse invalide.
    """
    retour = request.POST.get('suivant') or request.META.get('HTTP_REFERER') or ''
    if not url_has_allowed_host_and_scheme(retour, allowed_hosts={request.get_host()},
                                           require_https=request.is_secure()):
        retour = reverse('app:home')
    retour = retour.split('#')[0] + '#lettre'

    form = NewsletterForm(request.POST)
    if not form.is_valid():
        if form.has_error('site_web'):
            # Robot : on fait comme si tout s'était bien passé, sans rien enregistrer.
            request.session['newsletter'] = {'etat': 'reussie'}
        else:
            request.session['newsletter'] = {'etat': 'invalide', 'email': request.POST.get('email', '')[:254]}
        return redirect(retour)

    email = form.cleaned_data['email'].strip().lower()
    abonne, cree = Abonne.objects.get_or_create(email=email)
    if not cree and abonne.actif:
        request.session['newsletter'] = {'etat': 'deja'}
        return redirect(retour)
    if not cree:
        # Réinscription après une désinscription.
        abonne.actif, abonne.desinscrit_le = True, None
        abonne.save(update_fields=['actif', 'desinscrit_le'])
    if settings.EMAIL_HOST:
        lien = request.build_absolute_uri(reverse('app:newsletter_desinscription', args=[abonne.jeton]))
        send_customize_email("Bienvenue dans la lettre d'information d'UCIV", [abonne.email],
                             'emails/newsletter_bienvenue.html', {'lien_desinscription': lien})
    request.session['newsletter'] = {'etat': 'reussie'}
    return redirect(retour)


def newsletter_desinscription(request, jeton):
    """Lien personnel de désinscription : une confirmation en un clic, puis « C'est noté ».

    La désinscription se fait en POST : certaines messageries ouvrent les liens des e-mails
    automatiquement, ce qui désinscrirait les abonnés sans qu'ils le veuillent.
    """
    abonne = get_object_or_404(Abonne, jeton=jeton)
    if request.method == 'POST' and abonne.actif:
        abonne.actif, abonne.desinscrit_le = False, timezone.now()
        abonne.save(update_fields=['actif', 'desinscrit_le'])
    etape = 'fait' if not abonne.actif else 'confirmer'
    page = content.DESINSCRIPTION[etape]
    return render(request, 'app/layout/desinscription.html', {
        'abonne': abonne, 'etape': etape, 'page': page,
        'texte': page['texte'].format(email=abonne.email_masque),
    })
