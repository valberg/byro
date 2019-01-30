"""
Django settings for byro project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from contextlib import suppress

from django.utils.translation import ugettext_lazy as _
from pkg_resources import iter_entry_points

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, 'byro/logs')
STATIC_ROOT = os.path.join(BASE_DIR, 'static.dist')
MEDIA_ROOT = os.path.join(BASE_DIR, 'byro/media')

for directory in (BASE_DIR, LOG_DIR, STATIC_ROOT, MEDIA_ROOT):
    if not os.path.exists(directory):
        os.mkdir(directory)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'byro', 'static')]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'wcc($o)pj5vcy4r0wv2f*c(ws@92^f&p*1r+hsojg*qn7uzuge'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'compressor',
    'bootstrap4',
    'djangoformsetjs',
    'solo.apps.SoloAppConfig',
    'django_select2',

    'byro.common.apps.CommonConfig',
    'byro.bookkeeping.apps.BookkeepingConfig',
    'byro.documents.apps.DocumentsConfig',
    'byro.mails.apps.MailsConfig',
    'byro.members.apps.MemberConfig',
    'byro.office.apps.OfficeConfig',
    'byro.plugins.profile.ProfilePluginConfig',
    'byro.plugins.sepa.SepaPluginConfig',

    'annoying',
    'django_db_constraints',
]

with suppress(ImportError):
    import django_extensions  # noqa
    INSTALLED_APPS.append('django_extensions')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'byro.common.middleware.PermissionMiddleware',
    'byro.common.middleware.SettingsMiddleware',
]

with suppress(ImportError):
    import django_securebox
    INSTALLED_APPS.append('django_securebox')
    MIDDLEWARE.insert(2, 'django_securebox.middleware.SecureBoxMiddleware')

with suppress(ImportError):
    import debug_toolbar
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(2, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'byro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'byro.common.context_processors.byro_information',
                'byro.common.context_processors.sidebar_information',
            ],
        },
    },
]

WSGI_APPLICATION = 'byro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'byro',
    }
}

if os.getenv('TRAVIS'):
    DATABASES['default']['USER'] = 'postgres'
    DATABASES['default']['HOST'] = 'localhost'
    DATABASES['default']['PASSWORD'] = ''


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [
    ('en', _('English')),
    ('de', _('German')),
]
LANGUAGES_NATURAL_NAMES = [
    ('en', 'English'),
    ('de', 'Deutsch'),
]
LANGUAGE_CODE = 'en'
LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), 'locale'),
)
FORMAT_MODULE_PATH = [
    'byro.common.formats',
]



# ######### MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
# ######### END MEDIA CONFIGURATION

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

COMPRESS_ENABLED = COMPRESS_OFFLINE = not DEBUG

COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'django_libsass.SassCompiler'),
)

COMPRESS_CSS_FILTERS = (
    # CssAbsoluteFilter is incredibly slow, especially when dealing with our _flags.scss
    # However, we don't need it if we consequently use the static() function in Sass
    # 'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSCompressorFilter',
)

# Plugin magic

PLUGINS = []
for entry_point in iter_entry_points(group='byro.plugin', name=None):
    PLUGINS.append(entry_point.module_name)
    INSTALLED_APPS.append(entry_point.module_name)


## LOGGING SETTINGS
loglevel = 'DEBUG' if DEBUG else 'INFO'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(name)s %(module)s %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': loglevel,
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        'file': {
            'level': loglevel,
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'byro.log'),
            'formatter': 'default',
        },
    },
    'loggers': {
        '': {'handlers': ['file', 'console'], 'level': loglevel, 'propagate': True},
        'django.request': {
            'handlers': ['file', 'console'],
            'level': loglevel,
            'propagate': True,
        },
        'django.security': {
            'handlers': ['file', 'console'],
            'level': loglevel,
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['file', 'console'],
            'level': 'INFO',  # Do not output all the queries
            'propagate': True,
        },
    },
}


## EMAIL SETTINGS
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    MAIL_FROM = SERVER_EMAIL = DEFAULT_FROM_EMAIL = ''
    EMAIL_HOST = ''
    EMAIL_PORT = ''
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_USE_TLS = True  # Only one of these
    EMAIL_USE_SSL = False  # Only one of these

## SELECT2 SETTINGS

SELECT2_JS = ''
SELECT2_CSS = ''
SELECT2_I18N_PATH = '/static/vendored/select2/js/i18n'

try:
    from .local_settings import *
except ImportError:
    pass
