"""URL de l'application `app` (les pages publiques du site)."""
from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('qui-sommes-nous/', views.qui_sommes_nous, name='qui_sommes_nous'),
    path('programmes/uciv-leadership/', views.uciv_leadership, name='uciv_leadership'),
]
