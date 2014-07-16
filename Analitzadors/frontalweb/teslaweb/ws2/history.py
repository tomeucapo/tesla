from django.conf.urls import patterns, url 
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from tastypie.utils import trailing_slash
from tastypie.resources import Resource
from tastypie.cache import SimpleCache
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpNotFound, HttpForbidden, HttpApplicationError, HttpBadRequest, HttpConflict, HttpCreated

from teslaweb.lectures.models import  Node, Analitzador, Lectura, LecturaParametre, Parametre, NodeAnalitzador

from datetime import datetime
import time, logging, logging.handlers
import pickle, json

class HistoryResource(Resource):
	class Meta:
            cache = SimpleCache(varies=["Accept", "Cookie"])
            resource_name='history'

        def prepend_urls(self):
            return [
                    url(r"^(?P<resource_name>%s)/load/(?P<idNode>[0-9]+)/(?P<idAnalitzador>[0-9]+)/(?P<varName>[A-Z]+)/(?P<dateFrom>[0-9]{2}\-[0-9]{2}\-[0-9]{4})/(?P<dateUntil>[0-9]{2}\-[0-9]{2}\-[0-9]{4})%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('load'), name="api_history"),
                    url(r"^(?P<resource_name>%s)/save/(?P<idNode>[0-9]+)/(?P<idAnalitzador>[0-9]+)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('save'), name="api_history"),
                   ]

        def save(self, request, **kwargs):
            self.method_check(request, allowed=['post'])
            self.throttle_check(request)
            logger = logging.getLogger(__name__)
            
            try:
                  nodeId = kwargs.pop("idNode")
                  addrE = kwargs.pop("idAnalitzador")
	          dataHora = datetime.strptime(request.POST.get("DATA_HORA") , "%d/%m/%Y %H:%M:%S")
        	  dades = json.loads(request.POST.get("LECTURA"))
	          modelS = request.POST.get("MODEL")
	    except Exception, e:
	          logger.error("Error interpretant lectura: %s" % str(e))
		  raise ImmediateHttpResponse(HttpBadRequest("1#"+str(e)))

            logger.info("Lectura %s" % dataHora)
            logger.debug("Obtenint informacio del analitzador ... Model = %s" % modelS)
          
            try:          
               analitzador = Analitzador.objects.get(model=modelS)
               nodeAnalitzador = NodeAnalitzador.objects.get(node=nodeId, analitzador=analitzador.id, addr=addrE)
            except ObjectDoesNotExist, e:
               logger.warn("L'analitzador que vol guardar no es el que tenim configurat per aquest node")
               raise ImmediateHttpResponse(HttpNotFound("#" % str(e)))
            
            logger.debug("Analitzador %d, NodeAnalitzador %d" % (analitzador.id, nodeAnalitzador.id))
            
            try:
               lectura = Lectura()
               lectura.dataHora = dataHora
               lectura.node = nodeAnalitzador
               lectura.save()
            except Exception, e:
               logger.error(str(e))
               raise ImmediateHttpResponse(HttpConflict("#"+str(e)))

            for varName, values in dades.iteritems():         
                try:
                   parametre = Parametre.objects.get(analitzador=nodeAnalitzador.analitzador, nom=varName)
                except ObjectDoesNotExist, e:
                   logger.error("La variable per aquest analitzador no esta definida: %s" % str(e))
                   continue
               
                lParametre = LecturaParametre()
                lParametre.lectura = lectura
                lParametre.parametre = parametre
                lenValors = len(values)
              
                if not parametre.compost and lenValors != parametre.num_regs:
                   logger.warn("La variable %s te la longitud %d i esta definida com %d" % (varName, lenValors, parametre.num_regs))
                   continue
               
                if lenValors == 1:
                   lParametre.valor = values[0]
                elif lenValors > 1:
                   lParametre.valor = 0.0
                   lParametre.vectorValors = json.dumps(values)
               
                logger.debug("Guardant variable %s: %s" % (varName, values))
                lParametre.save()
                 
            logger.info("Guardada lectura a hitoric ...")
       
            node = nodeAnalitzador.node
            node.darreraLectura = dataHora
            node.save()
 	    
            return self.create_response(request, "#Saved:%d" % lectura.id, response_class = HttpCreated)


	def load(self, request, **kwargs):
            self.method_check(request, allowed=['get'])
            self.throttle_check(request)
            logger = logging.getLogger(__name__)

            varName = kwargs.pop('varName')
            di = datetime.strptime(kwargs.pop('dateFrom')+" 00:00:00", '%d-%m-%Y %H:%M:%S')
            df = datetime.strptime(kwargs.pop('dateUntil')+" 23:59:59", '%d-%m-%Y %H:%M:%S')
            tdelta = (df - di)

            if tdelta.days < 0:
               raise ImmediateHttpResponse(HttpBadRequest("La fecha inicial tiene que ser menor que la fecha final"))

            try:
                nodeAnalitzador = NodeAnalitzador.objects.get(node=kwargs.pop('idNode'), addr=kwargs.pop("idAnalitzador"))
            except ObjectDoesNotExist, e:
                logger.warn("L'analitzador que vol guardar no es el que tenim configurat per aquest node")
                raise ImmediateHttpResponse(HttpBadRequest("L'analitzador que vol guardar no es el que tenim configurat per aquest node"))
            lectures = LecturaParametre.objects.filter(lectura__node=nodeAnalitzador.id).filter(lectura__dataHora__range=(di, df)).order_by("lectura__dataHora")

            if varName.upper() != 'ALL':
               lectures = lectures.filter(parametre__nom=varName)

            mostres = []           
            try:
               for lectura in lectures:
                   if lectura.parametre.num_regs > 1:
                      try:
                         valor = [float("%9.2f" % v) for v in json.loads(lectura.vectorValors)]
                      except ValueError, e:
                         valor = float("%9.2f" % lectura.valor)
                   else:
                      valor = float("%9.2f" % lectura.valor)
                   mostres.append({"dataHora": lectura.lectura.dataHora, "variable": lectura.parametre.nom, "descripcio": lectura.parametre.descripcio, "valor": valor, "unitats": lectura.parametre.unitats})
            except Exception, e:
               logger.error("En la peticio de historic: %s" % str(e))
               raise ImmediateHttpResponse(HttpNotFound(str(e)))         
 
            logger.debug("Loaded %d registers from history" % len(mostres))
            results = {"ResultSet": {"Lectures": mostres, }}

            return self.create_response(request, results) 
