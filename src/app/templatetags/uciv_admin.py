"""Données et menu de l'administration aux couleurs d'UCIV (barre latérale et tableau de bord)."""
from datetime import timedelta

from django import template
from django.urls import reverse
from django.utils import timezone
from django.utils.timesince import timesince

from ..models import (
    Abonne, Article, Indicateur, Opportunite, Ressource, SoumissionContact, SoumissionEngagement,
    SoumissionPartenariat,
)

register = template.Library()

# Messages reçus : un modèle par formulaire. `publish` à False = pas encore traité (« Nouveau »).
MODELES_MESSAGES = (SoumissionContact, SoumissionEngagement, SoumissionPartenariat)


def _url(modele, action='changelist', *args):
    return reverse(f'admin:{modele._meta.app_label}_{modele._meta.model_name}_{action}', args=args)


def _nouveaux_messages():
    return sum(m.objects.filter(publish=False).count() for m in MODELES_MESSAGES)


@register.simple_tag(takes_context=True)
def menu_lateral(context):
    """Groupes de la barre latérale (Pilotage, Contenu du site, Suivi, Technique), avec l'entrée active."""
    requete = context['request']
    utilisateur = requete.user
    nouveaux = {m: m.objects.filter(publish=False).count() for m in MODELES_MESSAGES}

    def entree(libelle, icone, modele, badge=0):
        droits = [f'{modele._meta.app_label}.{action}_{modele._meta.model_name}' for action in ('view', 'change')]
        if not any(utilisateur.has_perm(d) for d in droits):
            return None
        url = _url(modele)
        actif = requete.path.startswith(url) or (modele is SoumissionContact and requete.path.startswith(
            reverse('admin:app_soumissionengagement_changelist')[:-len('soumissionengagement/')] + 'soumission'))
        return {'libelle': libelle, 'icone': icone, 'url': url, 'badge': badge, 'actif': actif}

    accueil = reverse('admin:index')
    groupes = [
        ('Pilotage', [{'libelle': 'Tableau de bord', 'icone': 'tableau', 'url': accueil, 'badge': 0,
                       'actif': requete.path == accueil}]),
        ('Contenu du site', [
            entree('Articles', 'article', Article),
            entree('Opportunités', 'opportunite', Opportunite),
            entree('Ressources', 'ressource', Ressource),
            entree("Chiffres d'impact", 'impact', Indicateur),
        ]),
        ('Suivi', [
            entree('Messages reçus', 'message', SoumissionContact, sum(nouveaux.values())),
            entree('Abonnés', 'abonne', Abonne),
        ]),
    ]
    resultat = []
    for titre, entrees in groupes:
        entrees = [e for e in entrees if e]
        if entrees:
            resultat.append({'titre': titre, 'entrees': entrees})
    return resultat


def _initiales(nom):
    return ''.join(mot[0] for mot in nom.split()[:2]).upper() or '?'


def _il_y_a(date):
    if timezone.now() - date < timedelta(minutes=1):
        return "à l'instant"
    return 'il y a ' + timesince(date, depth=1).replace('\xa0', ' ')


def _pluriel(n, singulier, pluriel):
    return singulier if n == 1 else pluriel


@register.simple_tag
def tableau_de_bord():
    """Chiffres clés, « À faire », derniers contenus modifiés et messages récents du tableau de bord."""
    il_y_a_un_mois = timezone.now() - timedelta(days=30)
    articles = Article.objects.filter(publish=True)
    opportunites = Opportunite.objects.filter(publish=True)
    ressources = Ressource.objects.filter(publish=True)
    abonnes = Abonne.objects.filter(actif=True)

    def dont_exemples(qs):
        n = qs.filter(modele=True).count()
        return f"dont {n} {_pluriel(n, 'fiche', 'fiches')} d'exemple" if n else 'toutes réelles'

    def ce_mois(qs, champ='created_at'):
        n = qs.filter(**{f'{champ}__gte': il_y_a_un_mois}).count()
        return f'+{n} ce mois-ci' if n else 'aucun ce mois-ci'

    chiffres = [
        {'libelle': 'Articles publiés', 'valeur': articles.count(), 'sous': ce_mois(articles),
         'icone': 'article', 'couleur': 'orange'},
        {'libelle': 'Opportunités en ligne', 'valeur': opportunites.count(), 'sous': dont_exemples(opportunites),
         'icone': 'opportunite', 'couleur': 'vert'},
        {'libelle': 'Ressources', 'valeur': ressources.count(), 'sous': dont_exemples(ressources),
         'icone': 'ressource', 'couleur': 'profond'},
        {'libelle': 'Abonnés actifs', 'valeur': abonnes.count(), 'sous': ce_mois(abonnes, 'inscrit_le'),
         'icone': 'abonne', 'couleur': 'fonce'},
    ]

    a_faire = []
    n = _nouveaux_messages()
    if n:
        a_faire.append({'titre': f"{n} {_pluriel(n, 'nouveau message', 'nouveaux messages')}",
                        'sous': 'Contact, engagement et partenariat.', 'lien': 'Lire',
                        'url': _url(SoumissionContact) + '?publish__exact=0', 'icone': 'message', 'couleur': 'vert'})
    n = Opportunite.objects.filter(modele=True).count()
    if n:
        a_faire.append({'titre': f"{n} {_pluriel(n, 'opportunité est une fiche', 'opportunités sont des fiches')} d'exemple",
                        'sous': 'Remplacez-les par de vraies offres.', 'lien': 'Remplacer',
                        'url': _url(Opportunite) + '?modele__exact=1', 'icone': 'opportunite', 'couleur': 'jaune'})
    n = Indicateur.objects.filter(valeur__isnull=True).count()
    if n:
        a_faire.append({'titre': f"{n} {_pluriel(n, 'chiffre', 'chiffres')} d'impact à renseigner",
                        'sous': "Le site affiche « à venir » tant qu'aucune valeur n'est saisie.",
                        'lien': 'Renseigner', 'url': _url(Indicateur), 'icone': 'impact', 'couleur': 'vert'})
    n = Ressource.objects.filter(modele=True).count()
    if n:
        a_faire.append({'titre': f"{n} {_pluriel(n, 'ressource est une fiche', 'ressources sont des fiches')} d'exemple",
                        'sous': 'Ajoutez les vrais documents et liens.', 'lien': 'Remplacer',
                        'url': _url(Ressource) + '?modele__exact=1', 'icone': 'ressource', 'couleur': 'jaune'})
    n = Article.objects.filter(publish=False).count()
    if n:
        a_faire.append({'titre': f"{n} {_pluriel(n, 'article', 'articles')} en brouillon",
                        'sous': 'À relire puis à publier.', 'lien': 'Relire',
                        'url': _url(Article) + '?publish__exact=0', 'icone': 'article', 'couleur': 'orange'})

    contenus = []
    for modele, champ, genre in ((Article, 'titre', 'Article'), (Opportunite, 'intitule', 'Opportunité'),
                                 (Ressource, 'titre', 'Ressource')):
        for objet in modele.objects.order_by('-update_at')[:5]:
            if not objet.publish:
                statut = ('brouillon', 'Brouillon')
            elif getattr(objet, 'modele', False):
                statut = ('exemple', "Fiche d'exemple")
            else:
                statut = ('publie', 'Publié')
            contenus.append({'titre': getattr(objet, champ), 'type': genre, 'date': objet.update_at,
                             'quand': _il_y_a(objet.update_at), 'url': _url(modele, 'change', objet.pk),
                             'statut': statut})
    contenus.sort(key=lambda c: c['date'], reverse=True)

    messages = []
    for modele, genre in ((SoumissionContact, 'Contact'), (SoumissionEngagement, 'Engagement'),
                          (SoumissionPartenariat, 'Partenariat')):
        for objet in modele.objects.order_by('-created_at')[:5]:
            if modele is SoumissionContact:
                detail = objet.objet
            elif modele is SoumissionEngagement:
                detail = objet.get_choix_display()
            else:
                detail = objet.organisation
            messages.append({'nom': objet.nom, 'initiales': _initiales(objet.nom), 'sujet': f'{genre} · {detail}',
                             'date': objet.created_at, 'quand': _il_y_a(objet.created_at),
                             'url': _url(modele, 'change', objet.pk), 'nouveau': not objet.publish})
    messages.sort(key=lambda m: m['date'], reverse=True)

    return {
        'chiffres': chiffres, 'a_faire': a_faire[:4], 'contenus': contenus[:5], 'messages': messages[:4],
        'url_articles': _url(Article), 'url_messages': _url(SoumissionContact),
        'url_nouvel_article': _url(Article, 'add'), 'url_nouvelle_opportunite': _url(Opportunite, 'add'),
        'url_nouvelle_ressource': _url(Ressource, 'add'), 'url_abonnes': _url(Abonne),
    }
