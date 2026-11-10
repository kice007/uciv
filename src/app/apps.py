from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    verbose_name = 'Site UCIV'

    def ready(self):
        from . import mesure  # noqa: F401  (enregistre le signal des échecs de connexion)
