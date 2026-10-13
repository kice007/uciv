"""URL de l'application `pages` (les pages publiques du site)."""
from django.urls import path

from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
]
