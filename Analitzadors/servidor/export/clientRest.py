##########################################################################################
#
# @file   clientRest.py
#         Plugin per gravar les dades de cap al webservice REST.
#
# @author Tomeu Capo
#

from exceptions import * 
import time, logging
import urllib2, urllib, json

class clientRest:
      def __init__(self, target, equip):         
          self.equip = equip
          self.URLDest = target     
          self.available = False
          self.logger = logging.getLogger('lector.dataexport')
                    
      def save(self, timeS, dades):
          campsWS = { "DATA_HORA" : time.strftime("%d/%m/%Y %H:%M:%S", timeS),
                      "LECTURA"   : json.dumps(dades),
                      "MODEL"     : self.equip.model }
          
          dataWS = urllib.urlencode(campsWS)
          urlReq = "%s/history/save/%s/%s" % (self.URLDest, self.nodeConf["id"], self.equip.id)
          
          self.logger.info("Sending sample to %s" % urlReq)
          
          self.available = False

          try:
             req = urllib2.Request(url=urlReq, data=dataWS)
             f = urllib2.urlopen(req)
             self.lastResponse = f.read()
          except urllib2.HTTPError, e:
             dataR = e.read().split('#')
             strError = str(dataR[1]) if len(dataR) > 0 else str(e)
             if e.code == 409:
                raise ClientDuplicateEntry, "Registre ja existent: %s" % strError
             else:
                raise ClientError, "Error enviant lectura: %s" % strError
          except urllib2.URLError, e:
             raise ClientError, e.reason
                    
          self.available = True

