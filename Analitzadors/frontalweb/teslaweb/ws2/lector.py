from django.conf.urls import patterns, url 
from django.conf import settings

from tastypie.utils import trailing_slash
from tastypie.resources import Resource
from tastypie.cache import SimpleCache
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound, HttpForbidden, HttpApplicationError, HttpBadRequest

from teslaweb.lectures.models import  Node
from api.client import ctrlLector

from datetime import datetime
import time, logging, logging.handlers
import pickle, json

logging.config.fileConfig("/var/pywww/tesla/logging.conf")

class LectorResource(Resource):
	class Meta:
            resource_name='lector'

        # lector/get/Vars/3/1/?format=json
        def prepend_urls(self):
            return [
                    url(r"^(?P<resource_name>%s)/get/(?P<operation>\w+)/(?P<idNode>[0-9]+)/(?P<idAnalitzador>[0-9]+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('lector'), name="api_lector"),
                   ]

	def lector(self, request, **kwargs):
            self.method_check(request, allowed=['get'])
            self.throttle_check(request)
            logger = logging.getLogger('ws.lector')

	    try:
               analitzadorId = kwargs.pop("idAnalitzador")
               operation = kwargs.pop("operation")

               node = Node.objects.get(id=kwargs.pop("idNode"))
               cliLector = ctrlLector((node.host,50007))
               if operation != 'Conf':
                  retval = getattr(cliLector, "get"+operation)(analitzadorId)
               else:
                  retval = getattr(cliLector, "get"+operation)()
               cliLector.desconnecta()
            except ObjectDoesNotExist:
               raise ImmediateHttpResponse(HttpNotFound("Node no existent"))
            except Exception, e:
               raise ImmediateHttpResponse(HttpBadRequest(str(e)))
 
            return self.create_response(request, retval) 
