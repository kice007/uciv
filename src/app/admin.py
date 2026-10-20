"""
Administration aux couleurs d'UCIV (maquette « Dashboard »).

Les listes, formulaires, messages reçus, abonnés et chiffres d'impact sont rendus par les gabarits
`templates/admin/uciv/` ; ce module décrit ce que chaque écran affiche (colonnes, boutons de filtre, sections).
"""
import csv

from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils import timezone
from django.utils.formats import date_format
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import (
    Abonne, Article, Indicateur, Opportunite, Ressource, SoumissionContact, SoumissionEngagement,
    SoumissionPartenariat,
)
from .ratelimit import limiter_connexion
from .templatetags.uciv_admin import _initiales

admin.site.site_header = "Une Côte d'Ivoire Volontaire"
admin.site.site_title = "Administration UCIV"
admin.site.index_title = "Gestion du site"
# La barre latérale d'UCIV (templates/admin/base_site.html) remplace celle de Django.
admin.site.enable_nav_sidebar = False
# Connexion : au plus 10 essais par adresse IP et 5 par identifiant toutes les 15 minutes (voir app/ratelimit.py).
admin.site.login = limiter_connexion(admin.site.login)


def pastille(genre, libelle):
    """Pastille de statut (Publié, Brouillon, Fiche d'exemple, Nouveau, Traité…), voir admin.css."""
    return format_html('<span class="pastille pastille--{}">{}</span>', genre, libelle)


def genre_statut(objet):
    """(genre, libellé) du statut d'un contenu publiable."""
    if not objet.publish:
        return 'brouillon', 'Brouillon'
    if getattr(objet, 'modele', False):
        return 'exemple', "Fiche d'exemple"
    return 'publie', 'Publié'


def date_jj_mm_aaaa(valeur):
    return date_format(valeur, 'd/m/Y') if valeur else '—'


class UcivAdmin(admin.ModelAdmin):
    """Contenus publiables (articles, opportunités, ressources) : liste à boutons de filtre et formulaire en cartes."""

    change_list_template = 'admin/uciv/liste.html'
    change_form_template = 'admin/uciv/formulaire.html'
    list_per_page = 10
    actions = ['publier', 'mettre_en_brouillon']

    # Liste
    description = ''
    nom_ajout = 'Nouvel élément'
    en_tetes = ()
    chips = ()            # (libellé, {paramètre de filtre: valeur}) ; le premier est « Tous »
    # Formulaire
    titre_modif = 'Modifier'
    titre_ajout = 'Nouveau'
    libelle_suppression = 'Supprimer'
    cote = ('Publication', 'Image')   # sections affichées dans la colonne de droite
    labels = {}
    aides = {}

    @admin.display(description='Statut', ordering='publish')
    def statut(self, objet):
        return pastille(*genre_statut(objet))

    @admin.action(description='Publier les éléments sélectionnés')
    def publier(self, request, queryset):
        n = queryset.update(publish=True)
        self.message_user(request, f'{n} élément(s) publié(s).', messages.SUCCESS)

    @admin.action(description='Repasser les éléments sélectionnés en brouillon')
    def mettre_en_brouillon(self, request, queryset):
        n = queryset.update(publish=False)
        self.message_user(request, f'{n} élément(s) repassé(s) en brouillon.', messages.SUCCESS)

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs.setdefault('labels', self.labels)
        kwargs.setdefault('help_texts', self.aides)
        return super().get_form(request, obj, change=change, **kwargs)

    # À surcharger : adresse publique de l'élément, et contenu d'une ligne de la liste.
    def url_site(self, objet):
        return ''

    def ligne(self, objet):
        raise NotImplementedError

    def _ligne_complete(self, objet):
        ligne = self.ligne(objet)
        genre, libelle = genre_statut(objet)
        ligne.update(
            pk=objet.pk, statut=(genre, libelle), publie=objet.publish,
            url_modif=reverse(f'admin:{self.opts_nom}_change', args=[objet.pk]),
            url_suppression=reverse(f'admin:{self.opts_nom}_delete', args=[objet.pk]),
            url_site=self.url_site(objet),
        )
        return ligne

    @property
    def opts_nom(self):
        return f'{self.model._meta.app_label}_{self.model._meta.model_name}'

    def changelist_view(self, request, extra_context=None):
        reponse = super().changelist_view(request, extra_context)
        if not hasattr(reponse, 'context_data') or 'cl' not in reponse.context_data:
            return reponse
        cl = reponse.context_data['cl']
        filtres = {k: v for k, v in request.GET.items() if k not in ('q', 'p', 'o', 'e', '_changelist_filters')}
        recherche = request.GET.get('q', '')
        chips = []
        for libelle, params in self.chips:
            requete = dict(params)
            if recherche:
                requete['q'] = recherche
            chips.append({'libelle': libelle, 'url': '?' + urlencode(requete) if requete else '?',
                          'actif': {k: str(v) for k, v in params.items()} == filtres})
        pages = []
        if cl.paginator.num_pages > 1:
            pages = [{'numero': n, 'url': cl.get_query_string({'p': n}), 'actif': n == cl.page_num}
                     for n in cl.paginator.page_range]
        nom = self.model._meta.verbose_name_plural
        reponse.context_data.update({
            'has_change_permission': self.has_change_permission(request),
            'has_delete_permission': self.has_delete_permission(request),
            'title': nom.capitalize(), 'description': self.description, 'nom_ajout': self.nom_ajout,
            'en_tetes': self.en_tetes, 'chips': chips, 'recherche': recherche, 'filtres': filtres,
            'lignes': [self._ligne_complete(o) for o in cl.result_list], 'total': cl.result_count,
            'nom_pluriel': nom, 'pages': pages,
            'page_precedente': cl.get_query_string({'p': cl.page_num - 1}) if cl.page_num > 1 else '',
            'page_suivante': (cl.get_query_string({'p': cl.page_num + 1})
                              if cl.page_num < cl.paginator.num_pages else ''),
        })
        return reponse

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context['uciv'] = {
            'retour': self.model._meta.verbose_name_plural.capitalize(),
            'titre': self.titre_ajout if add else self.titre_modif,
            'statut': genre_statut(obj) if obj else ('brouillon', 'Brouillon'),
            'url_site': self.url_site(obj) if obj else self.url_site(None),
            'suppression': self.libelle_suppression,
            'cote': self.cote,
        }
        return super().render_change_form(request, context, add, change, form_url, obj)


@admin.register(Article)
class ArticleAdmin(UcivAdmin):
    list_display = ('titre', 'categorie', 'date_publication', 'a_la_une', 'dans_nos_histoires', 'statut')
    list_filter = ('publish', 'categorie', 'a_la_une', 'histoire')
    search_fields = ('titre', 'chapo', 'corps')
    prepopulated_fields = {'slug': ('titre',)}
    readonly_fields = ('created_at', 'update_at')

    description = "Ils alimentent la page Actualités, la page de chaque article et « Nos histoires » de Notre impact."
    nom_ajout = 'Nouvel article'
    en_tetes = ('Titre', 'Catégorie', 'Date')
    chips = (
        ('Tous', {}), ('Publiés', {'publish__exact': 1}), ('Brouillons', {'publish__exact': 0}),
        ('À la une', {'a_la_une__exact': 1}), ('Nos histoires', {'histoire__exact': 1}),
    )
    titre_modif = "Modifier l'article"
    titre_ajout = 'Nouvel article'
    libelle_suppression = "Supprimer l'article"
    fieldsets = (
        ('Contenu', {'fields': ('titre', 'slug', ('categorie', 'etiquette'), 'chapo', 'corps')}),
        ('Repères', {'fields': (('auteur', 'temps_lecture'), 'meta')}),
        ('Publication', {'fields': ('publish', 'a_la_une', 'histoire', 'date_publication', 'theme')}),
        ('Image', {'fields': ('image_televersee', 'image_alt', 'image_legende', 'image')}),
    )
    labels = {
        'titre': 'Titre', 'slug': "Adresse de l'article (slug)", 'categorie': 'Catégorie', 'etiquette': 'Étiquette',
        'chapo': 'Résumé', 'corps': "Texte de l'article", 'auteur': 'Auteur', 'temps_lecture': 'Temps de lecture (minutes)',
        'meta': 'Repère', 'publish': 'Publié', 'a_la_une': 'À la une', 'histoire': 'Nos histoires',
        'date_publication': 'Date de publication', 'theme': "Couleur de l'étiquette",
        'image_televersee': 'Image principale', 'image_alt': 'Texte alternatif', 'image_legende': 'Légende',
        'image': 'Image du site (chemin statique)',
    }
    aides = {
        'etiquette': 'Remplace la catégorie.', 'chapo': "Affiché sur les cartes d'article et en chapô.",
        'corps': "Mise en forme : « !! » chapô · « ## » sous-titre · « > » citation · « - » liste. "
                 "Une ligne vide entre deux blocs.",
        'meta': "Petit texte affiché à côté de l'étiquette (date, lieu, thème…).",
        'publish': 'Visible sur le site.', 'a_la_une': "Grand article en tête de la page Actualités.",
        'histoire': 'Affiché dans Notre impact.', 'image_televersee': 'JPG ou PNG, 10 Mo maximum.',
        'image': "Ex. app/assets/img/groupe-nb.webp ; ignoré si une image est téléversée.",
    }

    @admin.display(description='Histoire', boolean=True, ordering='histoire')
    def dans_nos_histoires(self, article):
        return article.histoire

    def url_site(self, objet):
        return objet.get_absolute_url() if objet and objet.pk else ''

    def ligne(self, article):
        tag = 'À la une' if article.a_la_une else 'Nos histoires' if article.histoire else 'Article'
        return {'titre': article.titre, 'sous': f'{tag} · {article.temps_lecture} min',
                'colonnes': [article.get_categorie_display(), date_jj_mm_aaaa(article.date_publication)]}


@admin.register(Opportunite)
class OpportuniteAdmin(UcivAdmin):
    list_display = ('intitule', 'categorie', 'source', 'structure', 'date_limite', 'statut')
    list_filter = ('publish', 'modele', 'categorie', 'source')
    search_fields = ('intitule', 'structure', 'lieu', 'description')
    readonly_fields = ('created_at', 'update_at')

    description = "Offres de volontariat, formations, stages, emplois et appels à candidatures de la page Opportunités."
    nom_ajout = 'Nouvelle opportunité'
    en_tetes = ('Intitulé', 'Catégorie', 'Date limite')
    chips = (('Toutes', {}),) + tuple((libelle, {'categorie__exact': cle}) for cle, libelle in Opportunite.CATEGORIES) + (
        ('Fiches d\'exemple', {'modele__exact': 1}),)
    titre_modif = "Modifier l'opportunité"
    titre_ajout = 'Nouvelle opportunité'
    libelle_suppression = "Supprimer l'opportunité"
    cote = ('Publication',)
    fieldsets = (
        ("L'opportunité", {'fields': ('intitule', ('categorie', 'source'), ('structure', 'lieu'), 'description')}),
        ('Candidature', {'fields': (('date_limite', 'lien'),)}),
        ('Publication', {'fields': ('publish', 'modele')}),
    )
    labels = {
        'intitule': 'Intitulé', 'categorie': 'Catégorie', 'source': 'Source', 'structure': 'Structure', 'lieu': 'Lieu',
        'description': 'Description', 'date_limite': 'Date limite', 'lien': 'Lien pour candidater',
        'publish': 'Publiée', 'modele': "Fiche d'exemple",
    }
    aides = {
        'source': 'UCIV ou Partenaire.', 'publish': 'Visible sur la page Opportunités.',
        'modele': 'Emplacement à remplacer.',
    }

    def url_site(self, objet):
        return reverse('app:opportunites')

    def ligne(self, opportunite):
        return {'titre': opportunite.intitule,
                'sous': ' · '.join(x for x in (opportunite.source, opportunite.lieu or opportunite.structure) if x),
                'colonnes': [opportunite.get_categorie_display(), date_jj_mm_aaaa(opportunite.date_limite)]}


@admin.register(Ressource)
class RessourceAdmin(UcivAdmin):
    list_display = ('titre', 'type', 'theme', 'meta', 'statut')
    list_filter = ('publish', 'modele', 'type', 'theme')
    search_fields = ('titre',)
    readonly_fields = ('created_at', 'update_at')

    description = "Guides, manuels, supports, articles, vidéos et podcasts de la bibliothèque Ressources."
    nom_ajout = 'Nouvelle ressource'
    en_tetes = ('Titre', 'Type', 'Thème')
    chips = (('Toutes', {}), ('Guides', {'type__exact': 'guide'}), ('Vidéos', {'type__exact': 'video'}),
             ('Podcasts', {'type__exact': 'podcast'}), ("Fiches d'exemple", {'modele__exact': 1}))
    titre_modif = 'Modifier la ressource'
    titre_ajout = 'Nouvelle ressource'
    libelle_suppression = 'Supprimer la ressource'
    cote = ('Publication',)
    fieldsets = (
        ('La ressource', {'fields': ('titre', ('type', 'theme'), 'meta')}),
        ('Accès', {'fields': ('fichier', 'lien')}),
        ('Publication', {'fields': ('publish', 'modele')}),
    )
    labels = {
        'titre': 'Titre', 'type': 'Type', 'theme': 'Thème', 'meta': 'Format / durée', 'fichier': 'Fichier',
        'lien': 'Ou lien externe', 'publish': 'Publiée', 'modele': "Fiche d'exemple",
    }
    aides = {
        'meta': 'Ex. « PDF · 24 pages », « Vidéo · 18 min ».', 'fichier': 'PDF ou document, 10 Mo maximum.',
        'lien': "Utilisé si aucun fichier n'est déposé (vidéo YouTube, podcast…).",
        'publish': 'Visible dans la bibliothèque Ressources.', 'modele': 'Emplacement à remplacer.',
    }

    def url_site(self, objet):
        return reverse('app:ressources')

    def ligne(self, ressource):
        return {'titre': ressource.titre, 'sous': ressource.meta,
                'colonnes': [ressource.get_type_display(), ressource.get_theme_display()]}


@admin.register(Indicateur)
class IndicateurAdmin(admin.ModelAdmin):
    """Chiffres d'impact : une seule page, les valeurs se saisissent dans la liste."""

    change_list_template = 'admin/uciv/indicateurs.html'
    list_display = ('libelle', 'prefixe', 'valeur', 'ordre', 'publish')
    list_editable = ('prefixe', 'valeur')
    list_per_page = 50
    readonly_fields = ('created_at', 'update_at')

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        champ = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'valeur':
            champ.widget.attrs['placeholder'] = 'À renseigner'
        if db_field.name == 'prefixe':
            champ.widget.attrs.update(placeholder='+', size=2, title='Préfixe, ex. « + »')
        return champ

    def changelist_view(self, request, extra_context=None):
        reponse = super().changelist_view(request, extra_context)
        if hasattr(reponse, 'context_data') and 'cl' in reponse.context_data:
            n = reponse.context_data['cl'].result_count
            reponse.context_data.update({
                'title': "Chiffres d'impact",
                'description': f"Les {n} indicateurs de la page Notre impact. Un chiffre laissé vide s'affiche "
                               "« à venir » sur le site.",
            })
        return reponse


class MessageAdmin(admin.ModelAdmin):
    """Messages reçus : « Nouveau » tant qu'ils ne sont pas marqués comme traités (champ `publish`)."""
    actions = ['marquer_traite', 'marquer_a_traiter']

    @admin.display(description='Statut', ordering='publish')
    def statut(self, objet):
        return pastille('lu', 'Traité') if objet.publish else pastille('nouveau', 'Nouveau')

    @admin.action(description='Marquer comme traité')
    def marquer_traite(self, request, queryset):
        n = queryset.update(publish=True)
        self.message_user(request, f'{n} message(s) marqué(s) comme traité(s).', messages.SUCCESS)

    @admin.action(description='Remettre à traiter')
    def marquer_a_traiter(self, request, queryset):
        n = queryset.update(publish=False)
        self.message_user(request, f'{n} message(s) remis à traiter.', messages.SUCCESS)


@admin.register(SoumissionEngagement)
class SoumissionEngagementAdmin(MessageAdmin):
    list_display = ('nom', 'email', 'telephone', 'choix', 'created_at', 'statut')
    list_filter = ('publish', 'choix', 'created_at')
    search_fields = ('nom', 'email', 'telephone', 'message')
    readonly_fields = ('created_at', 'update_at')


@admin.register(SoumissionPartenariat)
class SoumissionPartenariatAdmin(MessageAdmin):
    list_display = ('organisation', 'nom', 'email', 'type_collaboration', 'created_at', 'statut')
    list_filter = ('publish', 'type_collaboration', 'created_at')
    search_fields = ('organisation', 'nom', 'email', 'message')
    readonly_fields = ('created_at', 'update_at')


def _date_courte(date):
    """« Il y a 2 h », « Hier », « 14 oct. » : repère de date des listes de messages."""
    maintenant = timezone.localtime()
    date = timezone.localtime(date)
    ecart = maintenant - date
    if date.date() == maintenant.date():
        minutes = max(int(ecart.total_seconds() // 60), 0)
        if minutes < 1:
            return "À l'instant"
        return 'Il y a ' + (f'{minutes} min' if minutes < 60 else f'{minutes // 60} h')
    if (maintenant.date() - date.date()).days == 1:
        return 'Hier'
    return date_format(date, 'j N')


def _date_reception(date):
    maintenant = timezone.localtime()
    date = timezone.localtime(date)
    heure = date.strftime('%H h %M')
    if date.date() == maintenant.date():
        return f"aujourd'hui à {heure}"
    if (maintenant.date() - date.date()).days == 1:
        return f'hier à {heure}'
    return f"le {date_format(date, 'd/m/Y')} à {heure}"


def messages_recus():
    """Demandes d'engagement, propositions de partenariat et messages de contact, du plus récent au plus ancien."""
    boite = []

    def ajouter(objet, genre, libelle_genre, nom, sujet, details, initiales=None):
        lignes = [('E-mail', objet.email)]
        if objet.telephone:
            lignes.append(('Téléphone', objet.telephone))
        lignes += [d for d in details if d[1]]
        boite.append({
            'id': f'{genre}-{objet.pk}', 'pk': objet.pk, 'genre': genre, 'libelle_genre': libelle_genre,
            'nom': nom, 'initiales': initiales or _initiales(nom), 'sujet': sujet, 'date': objet.created_at,
            'quand': _date_courte(objet.created_at), 'recu': _date_reception(objet.created_at),
            'nouveau': not objet.publish, 'email': objet.email, 'details': lignes, 'message': objet.message,
        })

    for o in SoumissionEngagement.objects.all():
        ajouter(o, 'engagement', 'Engagement', o.nom, f"Je veux m'engager · {o.get_choix_display()}",
                [('Je souhaite', o.get_choix_display()), ('Compétences', o.competences)])
    for o in SoumissionPartenariat.objects.all():
        ajouter(o, 'partenariat', 'Partenariat', f'{o.organisation} · {o.nom}', f'Partenariat · {o.type_collaboration}',
                [('Organisation', o.organisation), ('Type de collaboration', o.type_collaboration)],
                initiales=_initiales(f'{o.organisation} {o.nom}'))
    for o in SoumissionContact.objects.all():
        ajouter(o, 'contact', 'Contact', o.nom, f'Contact · {o.objet}',
                [('Objet', o.objet), ('Organisation', o.organisation)])
    boite.sort(key=lambda m: m['date'], reverse=True)
    return boite


MODELES_MESSAGES = {'engagement': SoumissionEngagement, 'partenariat': SoumissionPartenariat,
                    'contact': SoumissionContact}


@admin.register(SoumissionContact)
class SoumissionContactAdmin(MessageAdmin):
    """« Messages reçus » : la boîte réunit les trois formulaires du site (liste à gauche, détail à droite)."""

    list_display = ('nom', 'email', 'objet', 'organisation', 'created_at', 'statut')
    list_filter = ('publish', 'objet', 'created_at')
    search_fields = ('nom', 'email', 'organisation', 'message')
    readonly_fields = ('created_at', 'update_at')

    def changelist_view(self, request, extra_context=None):
        if not self.has_view_or_change_permission(request):
            raise PermissionDenied
        if request.method == 'POST' and 'message' in request.POST:
            return self._changer_etat(request)
        if request.method == 'POST' or request.GET.get('_changelist_filters'):
            return super().changelist_view(request, extra_context)
        boite = messages_recus()
        filtre = request.GET.get('f', 'tous')
        if filtre == 'nouveaux':
            visibles = [m for m in boite if m['nouveau']]
        elif filtre in MODELES_MESSAGES:
            visibles = [m for m in boite if m['genre'] == filtre]
        else:
            filtre, visibles = 'tous', boite
        choisi = next((m for m in visibles if m['id'] == request.GET.get('m')), visibles[0] if visibles else None)
        nouveaux = sum(m['nouveau'] for m in boite)
        chips = [('tous', f'Tous ({len(boite)})'), ('nouveaux', f'Nouveaux ({nouveaux})'),
                 ('engagement', 'Engagement'), ('partenariat', 'Partenariat'), ('contact', 'Contact')]
        contexte = {
            **self.admin_site.each_context(request), 'title': 'Messages reçus', 'opts': self.model._meta,
            'description': "Demandes d'engagement, propositions de partenariat et messages de contact envoyés "
                           "depuis le site.",
            'chips': [{'libelle': libelle, 'actif': cle == filtre, 'url': '?' + urlencode({'f': cle})}
                      for cle, libelle in chips],
            'messages_recus': [dict(m, actif=bool(choisi) and m['id'] == choisi['id'],
                                    url='?' + urlencode({'f': filtre, 'm': m['id']})) for m in visibles],
            'choisi': choisi, 'filtre': filtre, 'peut_modifier': self.has_change_permission(request),
            'detail_ouvert': bool(choisi) and 'm' in request.GET, 'retour_liste': urlencode({'f': filtre}),
        }
        return TemplateResponse(request, 'admin/uciv/messages.html', contexte)

    def _changer_etat(self, request):
        if not self.has_change_permission(request):
            raise PermissionDenied
        genre, _, pk = request.POST.get('message', '').partition('-')
        modele = MODELES_MESSAGES.get(genre)
        if modele and pk.isdigit():
            traite = request.POST.get('etat') == 'traite'
            modele.objects.filter(pk=pk).update(publish=traite)
            self.message_user(request, 'Message marqué comme traité.' if traite else 'Message remis à traiter.',
                              messages.SUCCESS)
        retour = {'f': request.POST.get('f', 'tous'), 'm': request.POST.get('message', '')}
        return HttpResponseRedirect(reverse('admin:app_soumissioncontact_changelist') + '?' + urlencode(retour))


def _csv_abonnes(queryset):
    """Liste à importer dans l'outil d'envoi de la lettre (Brevo, Mailchimp…)."""
    reponse = HttpResponse(content_type='text/csv; charset=utf-8')
    reponse['Content-Disposition'] = f'attachment; filename="abonnes-uciv-{timezone.localdate():%Y-%m-%d}.csv"'
    reponse.write('﻿')  # BOM : Excel ouvre correctement les accents
    ecrivain = csv.writer(reponse, delimiter=';')
    ecrivain.writerow(['email', 'inscrit_le'])
    for abonne in queryset.filter(actif=True):
        ecrivain.writerow([abonne.email, timezone.localtime(abonne.inscrit_le).strftime('%d/%m/%Y')])
    return reponse


@admin.register(Abonne)
class AbonneAdmin(admin.ModelAdmin):
    list_display = ('email', 'actif', 'inscrit_le', 'desinscrit_le')
    list_filter = ('actif', 'inscrit_le')
    search_fields = ('email',)
    readonly_fields = ('inscrit_le', 'desinscrit_le')
    actions = ['exporter_csv']

    @admin.action(description='Exporter en CSV les abonnés actifs sélectionnés')
    def exporter_csv(self, request, queryset):
        return _csv_abonnes(queryset)

    def get_urls(self):
        return [path('export/', self.admin_site.admin_view(self.exporter_tout), name='app_abonne_export')] \
            + super().get_urls()

    def exporter_tout(self, request):
        if not self.has_view_or_change_permission(request):
            raise PermissionDenied
        return _csv_abonnes(Abonne.objects.all())

    def changelist_view(self, request, extra_context=None):
        if request.method == 'POST' or request.GET.get('_changelist_filters'):
            return super().changelist_view(request, extra_context)
        if not self.has_view_or_change_permission(request):
            raise PermissionDenied
        recherche = request.GET.get('q', '').strip()
        abonnes = Abonne.objects.order_by('-inscrit_le')
        if recherche:
            abonnes = abonnes.filter(email__icontains=recherche)
        page = Paginator(abonnes, 20).get_page(request.GET.get('p'))
        debut_mois = timezone.localtime().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        contexte = {
            **self.admin_site.each_context(request), 'title': 'Abonnés', 'opts': self.model._meta,
            'description': "Inscrits à la lettre d'information depuis le pied de page. Exportez la liste pour "
                           "l'importer dans votre outil d'envoi (Brevo, Mailchimp…).",
            'actifs': Abonne.objects.filter(actif=True).count(),
            'ce_mois': Abonne.objects.filter(inscrit_le__gte=debut_mois).count(),
            'desinscrits': Abonne.objects.filter(actif=False).count(),
            'recherche': recherche, 'page': page, 'url_export': reverse('admin:app_abonne_export'),
            'abonnes': [{
                'email': a.email, 'actif': a.actif,
                'quand': (f"Inscrit le {date_format(timezone.localtime(a.inscrit_le), 'd/m/Y')}" if a.actif else
                          f"Désinscrit le {date_format(timezone.localtime(a.desinscrit_le), 'd/m/Y')}"
                          if a.desinscrit_le else 'Désinscrit'),
                'url': reverse('admin:app_abonne_change', args=[a.pk]),
            } for a in page],
            'page_precedente': f'?p={page.previous_page_number()}' + (f'&q={recherche}' if recherche else '')
            if page.has_previous() else '',
            'page_suivante': f'?p={page.next_page_number()}' + (f'&q={recherche}' if recherche else '')
            if page.has_next() else '',
            'pages': [{'numero': n, 'actif': n == page.number,
                       'url': f'?p={n}' + (f'&q={recherche}' if recherche else '')}
                      for n in page.paginator.page_range] if page.paginator.num_pages > 1 else [],
        }
        return TemplateResponse(request, 'admin/uciv/abonnes.html', contexte)
