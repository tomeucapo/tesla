from django.conf.urls.defaults import patterns, include, url

from lectures.views import *
from lectures.calculs import *

import settings,os 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # URLs referents al contingut estatic (No funciona amb Apache)
    (r'^static/js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, "js") }),
    (r'^static/css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, "css") }),
  
    (r'^admin/', include(admin.site.urls)),
    
    # URL del webservice
    (r'^central/ws/', include('gestioEnergetica.ws.urls')),

    # URLs del frontal web    
    (r'^node/sQuery=(?P<sQuery>[^/]+)$', listNodes),
    (r'^node/(?P<nodeId>[^/]+)/analizers$', listAnalizers),
    (r'^costs/(?P<nodeAnalitzadorId>[^/]+)/(?P<dataInici>[^/]+)/(?P<dataFi>[^/]+)$', 'lectures.calculs.costsTarifes'),
    (r'^costs$', 'lectures.calculs.inici'),
    (r'^visor$', 'lectures.views.realTime'),
    (r'^$', 'lectures.views.inici'),
)
