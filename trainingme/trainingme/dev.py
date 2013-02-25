from .settings import *

SITE_NAME = "testing.guadalux.org"
SITE_URL = 'http://testing.guadalux.org'

#Debugging
DEBUG = True
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = False

STATIC_ROOT = ''

STATICFILES_DIRS = (
    PROJECT_ROOT.child('media'),
)