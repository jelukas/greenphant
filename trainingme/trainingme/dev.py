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

MIDDLEWARE_CLASSES += 'debug_toolbar.middleware.DebugToolbarMiddleware',
INTERNAL_IPS = ('127.0.0.2',)
INSTALLED_APPS += 'debug_toolbar',
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
    )