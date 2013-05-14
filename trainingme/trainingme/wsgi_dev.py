import os, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

sys.path.append(PROJECT_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] = 'trainingme.dev'

import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    os.environ['TRAININGME_DBPASS'] = environ['TRAININGME_DBPASS']
    os.environ['EMAIL_HOST_PASSWORD'] = environ['EMAIL_HOST_PASSWORD']
    return _application(environ, start_response)
