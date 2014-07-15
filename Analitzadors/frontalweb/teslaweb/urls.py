from django.conf.urls import patterns, include, url

from lectures.views import *
from lectures.calculs import *

from ws2.history import HistoryResource
from ws2.lector import LectorResource

from tastypie.api import Api
import settings,os 

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

newApi = Api(api_name='v2')
newApi.register(HistoryResource())
newApi.register(LectorResource())

urlpatterns = patterns('',

    # URLs referents al contingut estatic (No funciona amb Apache)
    (r'^static/js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, "js") }),
    (r'^static/css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(settings.MEDIA_ROOT, "css") }),
  
    (r'^admin/', include(admin.site.urls)),
    
    # URL del webservice
    (r'^central/ws/', include('teslaweb.ws.urls')),

    # URLs del webservice v2
    (r'^ws/', include(newApi.urls)),

    # URLs del frontal web    
    (r'^nodes(?:|/)$', listNodes),
    (r'^node/sQuery=(?P<sQuery>[^/]+)$', listNodes),
    (r'^node/(?P<nodeId>[^/]+)/analizers$', listAnalizers),
    (r'^parametres/(?P<analizerId>[^/]+)$', listParametres),
    
    (r'^costs/(?P<nodeAnalitzadorId>[^/]+)/(?P<dataInici>[^/]+)/(?P<dataFi>[^/]+)$', 'lectures.calculs.costsTarifes'),
    (r'^costs$', 'lectures.calculs.inici'),
    (r'^visor$', 'lectures.views.realTime'),
    (r'^$', 'lectures.views.inici'),
)
