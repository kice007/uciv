from django.contrib import admin
from .models import SoumissionEngagement


@admin.register(SoumissionEngagement)
class SoumissionEngagementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'telephone', 'choix', 'created_at', 'publish')
    list_filter = ('choix', 'publish', 'created_at')
    search_fields = ('nom', 'email', 'telephone', 'message')
    readonly_fields = ('created_at', 'update_at')
