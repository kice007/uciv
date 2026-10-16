from django.contrib import admin
from .models import (
    Article, Indicateur, Opportunite, Ressource, SoumissionContact, SoumissionEngagement,
    SoumissionPartenariat,
)


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
