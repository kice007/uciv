from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from app import views as app_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Page « introuvable » du site (utilisée quand DEBUG=False).
handler404 = 'app.views.page_introuvable'

if settings.DEBUG:
    # Aperçu de la page 404 en local (avec DEBUG=True, Django affiche sa propre page d'erreur).
    urlpatterns += [path('404/', app_views.page_introuvable, {'exception': None})]
