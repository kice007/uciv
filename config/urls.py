"""
Table de routage principale du projet.

Chaque `path()` associe une adresse (URL) à une vue ou à la table de routage
d'une application. Les URL des pages publiques vivent dans `pages/urls.py`.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
]
