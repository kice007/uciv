"""URL de l'application `app` (les pages publiques du site)."""
from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('engagement/', views.engagement, name='engagement'),
    path('partenaires/', views.partenaires, name='partenaires'),
    path('contact/', views.contact, name='contact'),
    path('opportunites/', views.opportunites, name='opportunites'),
    path('actualites/', views.actualites, name='actualites'),
    path('actualites/<slug:slug>/', views.article, name='article'),
    path('impact/', views.impact, name='impact'),
    path('ressources/', views.ressources, name='ressources'),
    path('qui-sommes-nous/', views.qui_sommes_nous, name='qui_sommes_nous'),
    path('qui-sommes-nous/equipe/', views.equipe, name='equipe'),
    path('programmes/', views.nos_programmes, name='nos_programmes'),
    path('programmes/go-du-digital/', views.go_du_digital, name='go_du_digital'),
    path('programmes/experience-lab/', views.experience_lab, name='experience_lab'),
    path('programmes/uciv-leadership/', views.uciv_leadership, name='uciv_leadership'),
    path('mentions-legales/', views.page_legale, {'cle': 'mentions'}, name='mentions_legales'),
    path('politique-de-confidentialite/', views.page_legale, {'cle': 'confidentialite'},
         name='confidentialite'),
    path('conditions-d-utilisation/', views.page_legale, {'cle': 'conditions'}, name='conditions'),
]
