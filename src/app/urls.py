"""URL de l'application `app` (les pages publiques du site)."""
from django.contrib.sitemaps.views import sitemap
from django.urls import path

from . import seo, views

app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('robots.txt', views.robots_txt, name='robots'),
    path('llms.txt', views.llms_txt, name='llms'),
    path('sitemap.xml', sitemap, {'sitemaps': seo.SITEMAPS}, name='sitemap'),
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
]
