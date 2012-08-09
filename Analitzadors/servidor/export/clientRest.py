import time, logging
import urllib2, urllib, json

class clientRest:
      def __init__(self, target, equip):         
          self.equip = equip
          self.URLDest = target         
          self.mitjaDades = {}
          self.logger = logging.getLogger('lector.dataexport')
                    
      def save(self, timeS, dades):
          campsWS = { "DATA_HORA" : time.strftime("%d/%m/%Y %H:%M:%S", timeS),
                      "LECTURA"   : json.dumps(dades),
                      "MODEL"     : self.equip.model }
          
          dataWS = urllib.urlencode(campsWS)
          urlReq = "%s/history/save/%s/%s" % (self.URLDest, self.nodeConf["id"], self.equip.id)
          
          self.logger.debug("Enviant lectura a: %s" % urlReq)
          
          try:
             req = urllib2.Request(url=urlReq, data=dataWS)
             f = urllib2.urlopen(req)
             self.lastResponse = f.read()
          except urllib2.HTTPError, e:
             self.logger.error(str(e))
             raise IOError, "Error enviant lectura: %s" % str(e)
          except IOError, e:
             self.logger.error(str(e))
             raise IOError, "Error de connexio: %s" % str(e)

