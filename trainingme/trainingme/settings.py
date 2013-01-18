# Django settings for trainingme project.

import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
SITE_NAME = "trainingme.net"
SITE_URL = 'http://192.168.1.202'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '/home/luks/Escritorio/django/estable/greenphant/trainingme/dbtrainingme',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Madrid'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-es'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/luks/Escritorio/django/estable/greenphant/trainingme/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/luks/Escritorio/django/estable/greenphant/trainingme/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'lc#k=o=5!xbk^92k0_(*1srjv47#eq68b!ut^9oqflo$k%+xm('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

#Locale Path
LOCALE_PATHS = (
    '/home/luks/Escritorio/django/estable/greenphant/trainingme/locale',
)

#Localizacion
LANGUAGES = (
    ('en', 'English'),
    ('es', 'Spanish'),
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'trainingme.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'trainingme.wsgi.application'

TEMPLATE_DIRS = (
    '/home/luks/Escritorio/django/estable/greenphant/trainingme/templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'django.contrib.humanize',
    'registration',
    'social_auth',
    'widget_tweaks',
    'django_countries',
    'paypal.standard.ipn',
    'validatedfile', #Requires python-magic
    'personal',
    'financial',
    'elearning',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Social Authentication

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
    )

TWITTER_CONSUMER_KEY         = 'YyLFIRiVZv1ksLGW1aw'
TWITTER_CONSUMER_SECRET      = 'c8Gwdwd3hdM31Eyjii0IAkA1MOY4sWkgjK88GsCI'
FACEBOOK_APP_ID              = '560302190653717'
FACEBOOK_API_SECRET          = '5a7a46d0f6c60d83b37e356fe8f7d323'

LOGIN_URL          = '/accounts/login/'
LOGIN_REDIRECT_URL = '/elearning/'
LOGIN_ERROR_URL    = '/login-error/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/personal/profile/edit/'


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'social_auth.context_processors.social_auth_login_redirect',
)


SOCIAL_AUTH_EXPIRATION = 'expires'

#Settings for  Registration app

ACCOUNT_ACTIVATION_DAYS=7



#Email

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER ='guadaluxfoundation@gmail.com'
EMAIL_HOST_PASSWORD = 'g74d4l7x'
EMAIL_USE_TLS = True

"""
Para indicar que este modelo es el modelo de
 perfil de usuario para un sitio determinado, rellene el AUTH_PROFILE_MODULE
  ajuste con una cadena que consta de los siguientes elementos, separados por un punto: nombre_aplicacion.Modelo_del_perfil
 """
AUTH_PROFILE_MODULE = 'personal.Profile'


"Paypal Details"
PAYPAL_RECEIVER_EMAIL = "turico_1350147627_biz@gmail.com"


#Requires:  aptitude install swig, pip install M2Crypto
PAYPAL_PRIVATE_CERT = SITE_ROOT + '/certs/paypal.pem'
PAYPAL_PUBLIC_CERT = SITE_ROOT + '/certs/pubpaypal.pem'
PAYPAL_CERT = SITE_ROOT + '/certs/paypal_cert.pem'
PAYPAL_CERT_ID = 'PXKA9Y3MH3RHJ'