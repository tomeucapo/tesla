#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import pickle 
from xml.dom.minidom import parse

class Configurador:
    def __init__(self):
        self.params = {"disp": "/dev/ttyS0", "baud": "9600"}
        self.fitxer = "config.xml"    
        self.cPeticions = []
        self.cAnalitzador = {}
     
   
    def llegeix(self):
        retval = True
        try:
            self.dom = parse(self.fitxer)
            rootConf = self.dom.getElementsByTagName('configuracio')[0]	
        except Exception, e:
            print "Error al llegir el fitxer de configuració config.xml: ", str(e)
            return False
      
        nodeConf = rootConf.getElementsByTagName('node')
        if not nodeConf:
           raise Exception, "No s'ha especificat la configuracio del node en el config.xml!"
        
        self.node = {"id": nodeConf[0].getAttribute("id"),
                     "name": nodeConf[0].getAttribute("name"),
                     "location": nodeConf[0].getAttribute("location") }
        
        devices = rootConf.getElementsByTagName('devices')[0]

        self.devices = {}
        for device in devices.getElementsByTagName('device'):
            if device.getAttribute("enabled") == 'false':
               continue
           
            devId = device.getAttribute("id") 
            devType = device.getAttribute("type")
            devParams = {}
            for attr in device.childNodes:
                if attr.nodeType == attr.ELEMENT_NODE:
                   devParams[attr.localName] = attr.firstChild.data.encode('UTF-8')

            self.devices[devId] = {"type": devType, "config": devParams} 

        equips = rootConf.getElementsByTagName('equips')[0]
      
        self.equips = {} 
        for equip in equips.getElementsByTagName('analitzador'):
            equiId = int(equip.getAttribute("id"))
            devId = equip.getAttribute("device")
              
            if not self.devices.get(devId):
               raise KeyError, "El dispositiu assignat no esta definit anteriorment"
 
            driver = equip.getAttribute("driver")
            dataDriver = equip.getAttribute("dataDriver")

            conf_params = equip.getElementsByTagName('params')[0]
            params = {} 
            for node in conf_params.childNodes:
               if node.nodeType == node.ELEMENT_NODE:
                  params[node.localName] = node.firstChild.data.encode('UTF-8')

            dataExports = {}
            for dExport in equip.getElementsByTagName('dataexport'): 
                dType = dExport.getAttribute("type")
                dTarget = dExport.getAttribute("target")
                dataExports[dType] = dTarget 

            conf_peticions = equip.getElementsByTagName('peticions')[0]
            cPeticions = []
            for nodeP in conf_peticions.childNodes:
                if nodeP.nodeType == nodeP.ELEMENT_NODE:
                   cPeticions.append(nodeP.firstChild.data.encode('UTF-8'))

            self.equips[equiId] = {"config": {"device": devId, "driver": driver, "dataDriver": dataDriver,
                                              "params": params },
                                   "requests": cPeticions,
                                   "dataexport": dataExports }  
        return True 

    def getParamsAnalitzador(self):
        return self.cAnalitzador 
 
    def getParamsPeticions(self):
        return self.cPeticions

    def __str__(self):
       conf = {"devices": self.devices, "equips": self.equips}
       return pickle.dumps(conf)
         
if __name__ == "__main__":
   conf = Configurador()
   conf.llegeix()

   for id, confDev in conf.devices.iteritems():
       if confDev["type"] == "serial":
          print "Serie"
          for p, value in confDev["config"].iteritems():
              print p, value
  
   for id, confEqui in conf.equips.iteritems():
       print confEqui["config"]
       print confEqui["requests"]
       print confEqui["dataexport"] 
