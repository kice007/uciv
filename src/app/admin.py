import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone

from .models import (
    Abonne, Article, Indicateur, Opportunite, Ressource, SoumissionContact, SoumissionEngagement,
    SoumissionPartenariat,
)

admin.site.site_header = "Une Côte d'Ivoire Volontaire"
admin.site.site_title = "Administration UCIV"
admin.site.index_title = "Gestion du site"


@admin.register(SoumissionEngagement)
class SoumissionEngagementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'choix', 'created_at', 'publish')
    list_filter = ('choix', 'publish', 'created_at')
    search_fields = ('nom', 'email', 'telephone', 'message')
    readonly_fields = ('created_at', 'update_at')


@admin.register(SoumissionPartenariat)
class SoumissionPartenariatAdmin(admin.ModelAdmin):
    list_display = ('organisation', 'nom', 'email', 'type_collaboration', 'created_at', 'publish')
    list_filter = ('type_collaboration', 'publish', 'created_at')
    search_fields = ('organisation', 'nom', 'email', 'message')
    readonly_fields = ('created_at', 'update_at')


@admin.register(SoumissionContact)
class SoumissionContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'objet', 'organisation', 'created_at', 'publish')
    list_filter = ('objet', 'publish', 'created_at')
    search_fields = ('nom', 'email', 'organisation', 'message')
    readonly_fields = ('created_at', 'update_at')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'date_publication', 'a_la_une', 'histoire', 'publish')
    list_filter = ('categorie', 'a_la_une', 'histoire', 'publish')
    list_editable = ('publish',)
    search_fields = ('titre', 'chapo', 'corps')
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_publication'
    readonly_fields = ('created_at', 'update_at')


@admin.register(Opportunite)
class OpportuniteAdmin(admin.ModelAdmin):
    list_display = ('intitule', 'categorie', 'source', 'structure', 'date_limite', 'modele', 'publish')
    list_filter = ('categorie', 'source', 'publish')
    list_editable = ('publish',)
    search_fields = ('intitule', 'structure', 'lieu', 'description')
    readonly_fields = ('created_at', 'update_at')


@admin.register(Ressource)
class RessourceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type', 'theme', 'meta', 'modele', 'publish')
    list_filter = ('type', 'theme', 'publish')
    list_editable = ('publish',)
    search_fields = ('titre',)
    readonly_fields = ('created_at', 'update_at')


@admin.register(Indicateur)
class IndicateurAdmin(admin.ModelAdmin):
    list_display = ('libelle', 'valeur', 'ordre', 'publish')
    list_editable = ('valeur', 'ordre', 'publish')
    readonly_fields = ('created_at', 'update_at')


@admin.register(Abonne)
class AbonneAdmin(admin.ModelAdmin):
    list_display = ('email', 'actif', 'inscrit_le', 'desinscrit_le')
    list_filter = ('actif', 'inscrit_le')
    search_fields = ('email',)
    readonly_fields = ('inscrit_le', 'desinscrit_le')
    actions = ['exporter_csv']

    @admin.action(description='Exporter en CSV les abonnés actifs sélectionnés')
    def exporter_csv(self, request, queryset):
        """Liste à importer dans l'outil d'envoi de la lettre (Brevo, Mailchimp…)."""
        reponse = HttpResponse(content_type='text/csv; charset=utf-8')
        reponse['Content-Disposition'] = (
            f'attachment; filename="abonnes-uciv-{timezone.localdate():%Y-%m-%d}.csv"')
        reponse.write('\ufeff')  # BOM : Excel ouvre correctement les accents
        ecrivain = csv.writer(reponse, delimiter=';')
        ecrivain.writerow(['email', 'inscrit_le'])
        for abonne in queryset.filter(actif=True):
            ecrivain.writerow([abonne.email, timezone.localtime(abonne.inscrit_le).strftime('%d/%m/%Y')])
        return reponse
