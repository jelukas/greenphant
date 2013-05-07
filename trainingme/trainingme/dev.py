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


"Paypal Details"
PAYPAL_RECEIVER_EMAIL = "turico_1350147627_biz@gmail.com"


#Requires:  aptitude install swig, pip install M2Crypto
PAYPAL_PRIVATE_CERT = SITE_ROOT + '/certs/paypal.pem'
PAYPAL_PUBLIC_CERT = SITE_ROOT + '/certs/pubpaypal.pem'
PAYPAL_CERT = SITE_ROOT + '/certs/paypal_cert.pem'
PAYPAL_CERT_ID = 'PXKA9Y3MH3RHJ'
# Paypal
PAYPAL_TEST = False           # Testing mode on
PAYPAL_WPP_USER = "api.pi"      # Get from PayPal
PAYPAL_WPP_PASSWORD = "5PPASSSSSS24LFM8UN"
PAYPAL_WPP_SIGNATURE = "AwxJzVOjZFIRMAaVpwEBhwJ3E84fAw5l"