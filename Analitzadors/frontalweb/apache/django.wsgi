import os
import sys

path = '/var/pywww/tesla'
if path not in sys.path:
    sys.path.append(path)

path = '/var/pywww'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'gestioEnergetica.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


