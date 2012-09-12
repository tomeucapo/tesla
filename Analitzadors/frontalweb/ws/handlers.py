
import time, logging, logging.handlers
from datetime import datetime, date, time
import pickle, json

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from piston.handler import BaseHandler
from piston.utils import rc

from lectures.models import Node, Analitzador, Lectura, LecturaParametre, Parametre, NodeAnalitzador
from api.client import ctrlLector 

logging.config.fileConfig("/home/tomeu/devel/gestioEnergetica/logging.conf")

class HistoryHandler(BaseHandler):
   allowed_methods = ('GET','POST',)

   def __init__(self):
       self.logger = logging.getLogger('ws.history')

   def read(self, request, nodeAnalitzadorId, varName, dataInici, dataFi):
       try:
          dataIniciP = datetime.strptime(dataInici+" 00:00:00", "%d-%m-%Y %H:%M:%S")         
          dataFiP = datetime.strptime(dataFi+" 23:59:59", "%d-%m-%Y %H:%M:%S")         
       except Exception, e:
          self.logger.error("Error interpretant la peticio de historic: %s" % str(e))
          retval = rc.BAD_REQUEST
          retval.write("#"+str(e))
          return retval

       lectures = LecturaParametre.objects.filter(lectura__node=nodeAnalitzadorId).filter(lectura__dataHora__range=(dataIniciP, dataFiP)).order_by("lectura__dataHora")
       
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
              mostres.append({"dataHora": lectura.lectura.dataHora,"variable": lectura.parametre.nom, "valor": valor, "unitats": lectura.parametre.unitats})
       except Exception, e:
           self.logger.error("En la peticio de historic: %s" % str(e))
           retval = rc.NOT_FOUND
           retval.write("#"+str(e))
           return retval
         
       return {"ResultSet": {"Lectures": mostres, }}
      
   def create(self, request, nodeId, analitzadorId):
       try:
          dataHora = datetime.strptime(request.POST.get("DATA_HORA") , "%d/%m/%Y %H:%M:%S")         
          dades = json.loads(request.POST.get("LECTURA"))
          modelS = request.POST.get("MODEL")
       except Exception, e:
          self.logger.error("Error interpretant lectura: %s" % str(e))
          retval = rc.BAD_REQUEST
          retval.write("#"+str(e))
          return retval
                           
       self.logger.info("Lectura %s" % dataHora)
       self.logger.debug("Obtenint informacio del analitzador ... Model = %s" % modelS)
          
       try:          
          analitzador = Analitzador.objects.get(model=modelS)
          nodeAnalitzador = NodeAnalitzador.objects.get(node=nodeId, analitzador=analitzador.id, addr=analitzadorId)
       except ObjectDoesNotExist, e:
          self.logger.warn("L'analitzador que vol guardar no es el que tenim configurat per aquest node")
          retval = rc.NOT_FOUND
          retval.write("#" % str(e))
          return retval
            
       self.logger.debug("Analitzador %d, NodeAnalitzador %d" % (analitzador.id, nodeAnalitzador.id))
         
       try: 
           lectura = Lectura()
           lectura.dataHora = dataHora
           lectura.node = nodeAnalitzador
           lectura.save()
       except Exception, e:
           self.logger.error(str(e))
           retval = rc.DUPLICATE_ENTRY
           retval.write("#"+str(e))
           return retval
   
       for varName, values in dades.iteritems():         
           try:
              parametre = Parametre.objects.get(analitzador=nodeAnalitzador.analitzador, nom=varName)
           except ObjectDoesNotExist, e:
              self.logger.error("La variable per aquest analitzador no esta definida: %s" % str(e))
              continue
               
           lParametre = LecturaParametre()
           lParametre.lectura = lectura
           lParametre.parametre = parametre
           lenValors = len(values)
              
           if not parametre.compost and lenValors != parametre.num_regs:
              self.logger.warn("La variable %s te la longitud %d i esta definida com %d" % (varName, lenValors, parametre.num_regs))
              continue
               
           if lenValors == 1:
              lParametre.valor = values[0]
           elif lenValors > 1:
              lParametre.valor = 0.0
              lParametre.vectorValors = json.dumps(values)
               
           self.logger.debug("Guardant variable %s: %s" % (varName, values))
           lParametre.save()
                 
       self.logger.info("Guardada lectura a hitoric ...")
       
       node = nodeAnalitzador.node
       node.darreraLectura = dataHora
       node.save()
       
       retval = rc.CREATED
       retval.write("#Saved:%d" % lectura.id)        
       return retval
              

class AnalitzadorsHandler(BaseHandler):
   allowed_methods = ('GET',)

   def read(self, request, nodeId):
       return Node.objects.all()

"""
   Classe del recurs per fer una peticio
"""

class LectorHandler(BaseHandler):
   allowed_methods = ('GET',)
   validOperations = ["Vars", "Defs", "Conf", "Status"]

   def __init__(self):
       self.logger = logging.getLogger('ws.lector')

   def read(self, request, operation, nodeId=None, analitzadorId=None):
       if not nodeId:
          return rc.BAD_REQUEST

       if operation not in self.validOperations:
          retval = rc.BAD_REQUEST
          retval.write("No ha especificat la operacio!")
          return retval

       try: 
          node = Node.objects.get(id=nodeId)
          cliLector = ctrlLector((node.host,50007))
          retval = getattr(cliLector, "get"+operation)(analitzadorId)
          cliLector.desconnecta()
       except ObjectDoesNotExist:
          retval = rc.NOT_FOUND
          retval.write("Node no existent")
       except Exception, e:
          retval = rc.BAD_REQUEST
          retval.write(str(e))
       
       return retval

