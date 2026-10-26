import os
import re
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


def config(key, default=None, cast=None):
    """Lit une variable d'environnement (sans dépendance externe)."""
    value = os.environ.get(key, default)
    if cast is bool and isinstance(value, str):
        return value.strip().lower() in ('1', 'true', 'yes', 'on')
    return cast(value) if cast else value


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = config('DEBUG', default=True, cast=bool)
# En production (DEBUG=False), le site refuse de démarrer sans clé secrète propre ni noms de domaine explicites :
# mieux vaut une erreur au lancement qu'un site ouvert avec des réglages de développement.
SECRET_KEY = config('SECRET_KEY', default='')
ALLOWED_HOSTS = [h.strip() for h in config('ALLOWED_HOSTS', default='*' if DEBUG else '').split(',') if h.strip()]
if DEBUG:
    SECRET_KEY = SECRET_KEY or 'cle-de-developpement-uniquement'
else:
    if len(SECRET_KEY) < 50 or SECRET_KEY.startswith(('change-me', 'django-insecure', 'your-secret')):
        raise ImproperlyConfigured('SECRET_KEY doit être définie en production (50 caractères aléatoires au minimum).')
    if not ALLOWED_HOSTS or '*' in ALLOWED_HOSTS:
        raise ImproperlyConfigured('ALLOWED_HOSTS doit lister les noms de domaine du site (pas « * ») en production.')
# Adresse de l'administration : https://uciv.org/back-office/ par défaut ; ADMIN_URL permet d'en choisir une autre
# (par exemple plus difficile à deviner, à garder hors du code et de git).
ADMIN_URL = config('ADMIN_URL', default='back-office').strip('/ ')
if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', ADMIN_URL):
    raise ImproperlyConfigured('ADMIN_URL ne peut contenir que des lettres, chiffres, tirets et tirets bas (pas de « / »).')
if not DEBUG and ADMIN_URL.lower() == 'admin':
    raise ImproperlyConfigured('ADMIN_URL ne peut pas valoir « admin » en production (adresse la plus attaquée).')
# Après une connexion sans page d'origine, on arrive sur l'administration (le site n'a pas de page de profil).
LOGIN_URL = f'/{ADMIN_URL}/login/'
LOGIN_REDIRECT_URL = f'/{ADMIN_URL}/'
# Adresse publique du site (ex. https://uciv.org) : fixe les URL canoniques, du sitemap et des données structurées.
SITE_URL = config('SITE_URL', default='')

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
]

LOCAL_APPS = [
    'app',
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Variables communes à toutes les pages (navigation, pied de page…)
                'app.context_processors.site',
                # Balises de référencement (titre, description, canonique, données structurées)
                'app.seo.seo',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Base de données — SQLite par défaut ; MySQL avec USE_MYSQL=True (voir docs/DEPLOIEMENT.md).
if config('USE_MYSQL', default=False, cast=bool):
    _options_mysql = {
        'charset': 'utf8mb4',
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    }
    # SSL seulement si la base est sur une autre machine (ex. MYSQL_SSL_MODE=REQUIRED) ;
    # sur le même serveur (localhost), la connexion ne sort pas de la machine.
    if config('MYSQL_SSL_MODE'):
        _options_mysql['ssl_mode'] = config('MYSQL_SSL_MODE')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': config('MYSQL_DB'),
            'USER': config('MYSQL_USER'),
            'PASSWORD': config('MYSQL_PASSWORD'),
            'HOST': config('MYSQL_HOST', default='localhost'),
            'PORT': config('MYSQL_PORT', default='3306'),
            'CONN_MAX_AGE': config('MYSQL_CONN_MAX_AGE', default=60, cast=int),
            'OPTIONS': _options_mysql,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'static_cdn'
# Adresses statiques avec empreinte (?v=…) : voir core/storage.py
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'core.storage.StatiqueAvecEmpreinte'},
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media_cdn'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Journalisation : les erreurs 500 (avec leur trace) vont sur la sortie d'erreur, donc dans « journalctl -u uciv ».
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'loggers': {'django.request': {'handlers': ['console'], 'level': 'ERROR', 'propagate': False}},
}

# Cache : mémoire locale en développement ; en production, un dossier partagé entre les processus Gunicorn
# (le limiteur de débit de app/ratelimit.py y compte les envois de formulaires).
if DEBUG:
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
else:
    CACHES = {'default': {'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
                          'LOCATION': config('CACHE_DIR', default=str(BASE_DIR / 'cache_cdn'))}}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
# Port 587 : STARTTLS (EMAIL_USE_TLS) ; port 465 : SSL direct (EMAIL_USE_SSL). Les deux s'excluent.
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool) and not EMAIL_USE_SSL
# Sans délai, un serveur SMTP qui ne répond pas bloquerait un worker Gunicorn (et la page du formulaire) indéfiniment.
EMAIL_TIMEOUT = config('EMAIL_TIMEOUT', default=10, cast=int)
# Adresse d'expéditeur : celle de la connexion SMTP par défaut ; à renseigner si le fournisseur impose un autre identifiant de connexion.
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='') or EMAIL_HOST_USER or 'webmaster@localhost'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
CONTACT_EMAIL = config('CONTACT_EMAIL', default='organisationuciv@gmail.com')

# Sécurité production
CSRF_TRUSTED_ORIGINS = [o for o in config('CSRF_TRUSTED_ORIGINS', default='').split(',') if o]
if not DEBUG:
    # Nginx termine le HTTPS et transmet le schéma : sans cet en-tête, la redirection HTTPS boucle.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    # HSTS : le navigateur n'ouvre plus le site qu'en HTTPS. Durée courte au départ (1 jour) ; une fois le HTTPS
    # vérifié, passer HSTS_SECONDS à 31536000 (1 an). Irréversible tant que la durée n'est pas écoulée.
    SECURE_HSTS_SECONDS = config('HSTS_SECONDS', default=86400, cast=int)
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SAMESITE = 'Lax'
