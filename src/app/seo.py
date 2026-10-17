"""Référencement : balises par page, données structurées (schema.org), robots.txt, sitemap.xml et llms.txt.

Les titres et descriptions sont centralisés dans `content.SEO_PAGES`. Le processeur de contexte `seo` les rend
disponibles à tous les gabarits (`seo.titre`, `seo.description`, `seo.canonique`, `seo.balisage`…).
"""
import json
from urllib.parse import quote, urlparse

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import Truncator

from . import content
from .models import Article, Indicateur, Opportunite, Ressource

NOM_SITE = "Une Côte d'Ivoire Volontaire"
SLOGAN = "Mobiliser la jeunesse, développer les compétences et créer des opportunités par le volontariat et " \
         "l'engagement citoyen."


def base_url(request):
    """Adresse du site sans « / » final : SITE_URL en production, sinon celle de la requête."""
    return (settings.SITE_URL or request.build_absolute_uri('/')).rstrip('/')


def url_statique(request, chemin):
    url = static(chemin)
    return url if url.startswith('http') else base_url(request) + url


def _json(donnees):
    # « </ » est neutralisé pour qu'une valeur ne puisse jamais refermer la balise <script>.
    return json.dumps(donnees, ensure_ascii=False).replace('</', '<\\/')


def _balisage(blocs):
    return mark_safe(''.join(f'<script type="application/ld+json">{_json(bloc)}</script>' for bloc in blocs))


def organisation(request, complet=True):
    base = base_url(request)
    ref = {'@type': 'NGO', '@id': base + '/#organisation', 'name': NOM_SITE, 'alternateName': 'UCIV',
           'url': base + '/',
           'logo': {'@type': 'ImageObject', 'url': url_statique(request, 'app/assets/img/logo-uciv.png')}}
    if not complet:
        return ref
    telephone = content.COORDONNEES['telephones'][0]['href'].replace('tel:', '')
    ref.update({
        '@context': 'https://schema.org',
        'description': SLOGAN,
        'email': content.COORDONNEES['email'],
        'telephone': telephone,
        'address': {'@type': 'PostalAddress', 'postOfficeBoxNumber': '04 BP 2087', 'addressLocality': 'Abidjan',
                    'addressCountry': 'CI'},
        'areaServed': {'@type': 'Country', 'name': "Côte d'Ivoire"},
        'founder': {'@type': 'Person', 'name': 'Marshall Kouamé', 'jobTitle': 'Président et fondateur'},
        'sameAs': [quote(r['url'], safe=":/?#[]@!$&'()*+,;=%") for r in content.RESEAUX],
        'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': telephone,
                         'email': content.COORDONNEES['email'], 'availableLanguage': 'fr'},
    })
    return ref


def _site(request):
    base = base_url(request)
    return {'@context': 'https://schema.org', '@type': 'WebSite', '@id': base + '/#site', 'url': base + '/',
            'name': NOM_SITE, 'inLanguage': 'fr', 'publisher': {'@id': base + '/#organisation'}}


def _fil(request, elements, url_courante, titre_courant=None):
    """Fil d'Ariane (BreadcrumbList) à partir de [(libellé, nom d'URL ou None), …]."""
    base = base_url(request)
    items = []
    for position, (libelle, nom) in enumerate(elements, start=1):
        url = base + reverse('app:' + nom) if nom else url_courante
        nom_affiche = libelle if nom else (titre_courant or libelle)
        items.append({'@type': 'ListItem', 'position': position, 'name': nom_affiche, 'item': url})
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': items}


def _derniere_modification(nom):
    """Date de dernière mise à jour des pages alimentées par la base (None pour les pages rédigées à la main)."""
    modele, filtres = {'actualites': (Article, {'histoire': False}), 'opportunites': (Opportunite, {}),
                       'ressources': (Ressource, {}), 'impact': (Indicateur, {})}.get(nom, (None, None))
    if modele is None:
        return None
    objet = modele.objects.filter(publish=True, **filtres).order_by('-update_at').first()
    return objet.update_at if objet else None


def _page(request, nom, page, url, type_page='WebPage'):
    base = base_url(request)
    donnees = {'@context': 'https://schema.org', '@type': type_page, '@id': url + '#page', 'url': url,
              'name': page['titre'], 'description': page['description'], 'inLanguage': 'fr',
              'isPartOf': {'@id': base + '/#site'}, 'about': {'@id': base + '/#organisation'}}
    modifie = _derniere_modification(nom)
    if modifie:
        donnees['dateModified'] = modifie.isoformat()
    return donnees


def _blocs_specifiques(request, nom, page, url):
    """Données structurées propres au type de page."""
    base = base_url(request)
    blocs = []
    if page['type'] == 'evenement':
        lancement = content.LANCEMENT_LEADERSHIP
        blocs.append({
            '@context': 'https://schema.org', '@type': 'Event',
            'name': "Conférence de lancement d'UCIV Leadership (format TEDx)",
            'description': "Conférence de lancement du réseau UCIV Leadership, au format TEDx. L'heure sera confirmée.",
            'startDate': lancement['date'],
            'eventStatus': 'https://schema.org/EventScheduled',
            'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
            'location': {'@type': 'Place', 'name': lancement['lieu'],
                         'address': {'@type': 'PostalAddress', 'addressLocality': lancement['ville'],
                                     'addressCountry': 'CI'}},
            'image': [url_statique(request, page['image'])],
            'organizer': organisation(request, complet=False),
            'url': url, 'inLanguage': 'fr',
        })
    elif page['type'] == 'cours':
        blocs.append({
            '@context': 'https://schema.org', '@type': 'Course', 'name': page['cours']['nom'],
            'description': page['description'], 'url': url, 'inLanguage': 'fr',
            'provider': organisation(request, complet=False),
            'audience': {'@type': 'Audience', 'audienceType': page['cours']['public']},
        })
    elif nom == 'equipe':
        membres = [('Marshall Kouamé', 'Président et fondateur')]
        membres += [(m['nom'], m['role']) for m in content.EQUIPE['bureau']]
        membres += [(m['nom'], m['role']) for m in content.EQUIPE['medias']]
        blocs.append({
            '@context': 'https://schema.org', '@type': 'ItemList', 'name': "Équipe d'UCIV",
            'itemListElement': [
                {'@type': 'ListItem', 'position': n,
                 'item': {'@type': 'Person', 'name': nom_membre, 'jobTitle': role,
                          'worksFor': {'@id': base + '/#organisation'}}}
                for n, (nom_membre, role) in enumerate(membres, start=1)],
        })
    elif page['type'] == 'programmes':
        programmes = [('Les Go du Digital', 'go_du_digital'), ('UCIV Leadership', 'uciv_leadership'),
                      ('Experience Lab', 'experience_lab')]
        blocs.append({
            '@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Programmes d\'UCIV',
            'itemListElement': [{'@type': 'ListItem', 'position': n, 'name': libelle,
                                 'url': base + reverse('app:' + cible)}
                                for n, (libelle, cible) in enumerate(programmes, start=1)],
        })
    return blocs


def construire(request, nom):
    """Dictionnaire SEO d'une page, d'après son nom d'URL."""
    page = content.SEO_PAGES.get(nom)
    base = base_url(request)
    if page is None:      # page d'erreur, administration… : pas d'indexation
        return {'titre': NOM_SITE, 'description': SLOGAN, 'robots': 'noindex, nofollow',
                'canonique': base + request.path, 'og_type': 'website', 'balisage': '',
                'og_image': url_statique(request, content.IMAGE_PAR_DEFAUT), 'nom_site': NOM_SITE}
    filtre = any(request.GET.get(cle) for cle in content.PARAMETRES_FILTRES)
    chemin = reverse('app:' + nom)
    canonique = base + chemin
    numero = request.GET.get('page', '')
    if nom == 'actualites' and numero.isdigit() and int(numero) > 1 and not filtre:
        canonique += f'?page={int(numero)}'
    url = base + chemin

    blocs = []
    if nom == 'home':
        blocs += [organisation(request), _site(request), _page(request, nom, page, url)]
    else:
        blocs.append(_page(request, nom, page, url, 'ContactPage' if page['type'] == 'contact'
                           else 'AboutPage' if page['type'] == 'a_propos'
                           else 'CollectionPage' if page['type'] in ('collection', 'programmes') else 'WebPage'))
        blocs.append(_fil(request, page['fil'], url))
    blocs += _blocs_specifiques(request, nom, page, url)
    return {
        'titre': page['titre'], 'description': page['description'],
        'robots': 'noindex, follow' if filtre else 'index, follow',
        'canonique': canonique, 'og_type': 'website', 'nom_site': NOM_SITE,
        'og_image': url_statique(request, page.get('image', content.IMAGE_PAR_DEFAUT)),
        'balisage': _balisage(blocs),
    }


def pour_article(request, article):
    """Dictionnaire SEO d'un article (type Article, fil d'Ariane, image et dates)."""
    base = base_url(request)
    url = base + article.get_absolute_url()
    suffixe = ' — Actualités UCIV'
    titre = article.titre if len(article.titre) + len(suffixe) > 60 else article.titre + suffixe
    description = Truncator(strip_tags(article.chapo or article.titre)).chars(157)
    image = article.image_url
    if image and not image.startswith('http'):
        image = base + image
    image = image or url_statique(request, content.IMAGE_PAR_DEFAUT)
    donnees = {
        '@context': 'https://schema.org', '@type': 'Article', 'headline': Truncator(article.titre).chars(110),
        'description': description, 'image': [image], 'inLanguage': 'fr',
        'datePublished': article.date_publication.isoformat(),
        'dateModified': article.update_at.date().isoformat(),
        'author': {'@type': 'Organization', 'name': NOM_SITE, 'url': base + '/'},
        'publisher': organisation(request, complet=False),
        'mainEntityOfPage': {'@type': 'WebPage', '@id': url},
    }
    fil = [('Accueil', 'home'), ('Actualités', 'actualites')]
    fil_json = _fil(request, fil + [(article.titre, None)], url, titre_courant=article.titre)
    return {
        'titre': titre, 'description': description, 'robots': 'index, follow', 'canonique': url,
        'og_type': 'article', 'og_image': image, 'nom_site': NOM_SITE,
        'publie': article.date_publication.isoformat(), 'modifie': article.update_at.isoformat(),
        'balisage': _balisage([donnees, fil_json]),
    }


def seo(request):
    """Processeur de contexte : `seo` pour les gabarits (la vue d'un article le remplace par `pour_article`)."""
    correspondance = getattr(request, 'resolver_match', None)
    nom = correspondance.url_name if correspondance and correspondance.namespace == 'app' else ''
    return {'seo': construire(request, nom), 'faq': content.FAQ.get(nom), 'faq_titre': content.FAQ_TITRE}


# --- robots.txt, llms.txt ------------------------------------------------------------------------------------

# Robots des moteurs de recherche et de réponse IA, autorisés pour être cités par ChatGPT, Claude, Perplexity…
ROBOTS_IA = ['GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'PerplexityBot']


def texte_robots(request):
    """robots.txt : tout est exploré sauf l'administration ; les robots IA sont nommés et autorisés."""
    lignes = ['User-agent: *', 'Allow: /', 'Disallow: /admin/', '',
              '# Robots des moteurs de réponse IA : autorisés (le site doit pouvoir y être cité).',
              '# Un groupe nommé remplace le groupe « * » : la règle sur /admin/ est donc répétée.']
    lignes += [f'User-agent: {robot}' for robot in ROBOTS_IA]
    lignes += ['Allow: /', 'Disallow: /admin/', '', f'Sitemap: {base_url(request)}/sitemap.xml', '']
    return '\n'.join(lignes)


def texte_llms(request):
    """llms.txt : présentation du site, faits clés, pages et dernières actualités pour les moteurs de réponse IA."""
    base = base_url(request)
    lancement = content.LANCEMENT_LEADERSHIP
    telephones = ' ou '.join(t['label'] for t in content.CONTACT['telephones'])
    lignes = [f'# {NOM_SITE} (UCIV)', '', f'> {SLOGAN}', '',
              "UCIV est une initiative citoyenne ivoirienne, basée à Abidjan, qui mobilise la jeunesse autour du "
              "volontariat, du bénévolat et de l'engagement citoyen. Le site est en français.", '',
              '## Faits clés', '',
              f'- Nom : {NOM_SITE} (UCIV)',
              '- Fondateur et président : Marshall Kouamé',
              f"- Siège : Abidjan, Côte d'Ivoire ({content.COORDONNEES['adresse']})",
              f"- Contact : {content.COORDONNEES['email']} ; téléphone {telephones}",
              "- Programmes : Les Go du Digital (6 samedis, jeunes femmes, pratique à 90 %) ; UCIV Leadership "
              "(réseau sélectif de 30 à 50 membres) ; Experience Lab (personal branding et pitch)",
              f"- Lancement d'UCIV Leadership : 24 octobre 2026, {lancement['lieu']}, {lancement['ville']} "
              "(conférence au format TEDx, heure à confirmer)",
              "- Partenaires : BonixUp, PAIPRO-JEUNES, ONG Light for All CI", '',
              '## Pages principales', '']
    for nom in content.PAGES_INDEXABLES:
        page = content.SEO_PAGES[nom]
        lignes.append(f"- [{page['titre']}]({base}{reverse('app:' + nom)}): {page['description']}")
    articles = Article.objects.filter(publish=True, histoire=False)[:5]
    if articles:
        lignes += ['', '## Dernières actualités', '']
        lignes += [f"- [{a.titre}]({base}{a.get_absolute_url()}): {a.date_publication.isoformat()}"
                   + (f' — {Truncator(strip_tags(a.chapo)).chars(140)}' if a.chapo else '') for a in articles]
    lignes += ['', '## Réseaux et profils', '']
    lignes += [f"- {r['label']} : {r['url']}" for r in content.RESEAUX]
    lignes.append('')
    return '\n'.join(lignes)


# --- sitemap.xml -------------------------------------------------------------------------------------------------


def _dernier(modele, champ='update_at', **filtres):
    objet = modele.objects.filter(publish=True, **filtres).order_by('-' + champ).first()
    return getattr(objet, champ) if objet else None


class SitemapUCIV(Sitemap):
    """Base commune : l'adresse du sitemap est SITE_URL (jamais www ou l'adresse IP de la requête)."""

    @property
    def protocol(self):
        if settings.SITE_URL:
            return urlparse(settings.SITE_URL).scheme
        return 'http' if settings.DEBUG else 'https'

    def get_domain(self, site=None):
        return urlparse(settings.SITE_URL).netloc or super().get_domain(site)


class PagesSitemap(SitemapUCIV):
    """Pages du site. `lastmod` n'est renseigné que lorsqu'une vraie date existe (pages alimentées par la base)."""

    def items(self):
        return content.PAGES_INDEXABLES

    def location(self, nom):
        return reverse('app:' + nom)

    def lastmod(self, nom):
        if nom == 'actualites':
            return _dernier(Article, histoire=False)
        if nom == 'opportunites':
            return _dernier(Opportunite)
        if nom == 'ressources':
            return _dernier(Ressource)
        if nom == 'impact':
            return _dernier(Indicateur)
        return None


class ArticlesSitemap(SitemapUCIV):
    def items(self):
        return Article.objects.filter(publish=True)

    def lastmod(self, article):
        return article.update_at


SITEMAPS = {'pages': PagesSitemap, 'articles': ArticlesSitemap}
