# Mapeig de les accions de la API

from django.conf.urls import *
from piston.resource import Resource
from teslaweb.ws.handlers import *

lector_handler = Resource(LectorHandler)
history_handler = Resource(HistoryHandler)

urlpatterns = patterns('',
   url(r'^rt/get/(?P<operation>[^/]+)/(?P<nodeId>[^/]+)/(?P<analitzadorId>[^/]+)$', lector_handler),
   url(r'^rt/get/(?P<operation>[^/]+)/(?P<nodeId>[^/]+)', lector_handler),
   url(r'^history/load/(?P<nodeAnalitzadorId>[^/]+)/(?P<varName>[^/]+)/(?P<dataInici>[^/]+)/(?P<dataFi>[^/]+)$', history_handler),
   url(r'^history/save/(?P<nodeId>[^/]+)/(?P<analitzadorId>[^/]+)$', history_handler), 
)


