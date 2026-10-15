from django.contrib import admin
from .models import SoumissionContact, SoumissionEngagement, SoumissionPartenariat


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
