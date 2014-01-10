#!/usr/bin/python

import time, threading, math, Queue
import logging, logging.config

from dataExport import dataExport

class lector(threading.Thread):
    def __init__(self, equip, dExports, nodeConf):
        self.equip = equip
        self.nodeConf = nodeConf
        self.idEquip = ''
        self.dExports = dExports
        self.logger = logging.getLogger('lector.gen') 
        self.forceReq = False
        self.errorComm = False
        self.ready = False
        self.pause = False
        self.acabar = False

        self.tempsGravacio = 15
        self.tempsLectura = 60        

        self.initFraccions() 
        threading.Thread.__init__(self, name=self.__class__.__name__)

    def initFraccions(self):
        lMinuts = [(sec * self.tempsGravacio) % 60 for sec in range(60 / self.tempsGravacio)]
        self.lHores = ["%(h)02d:%(m)02d" % {"h":i, "m": j} for i in range(24) for j in lMinuts]
    
    def setMaxLectures(self, maxLect, tempLectura):
        self.tempsGravacio = maxLect
        self.tempsLectura = tempLectura 
        self.initFraccions()
     
    def identifyEquip(self):
        if self.ready:
           self.equip.clearCache()
           self.dataExp.idEquip = self.idEquip = self.equip.getConfig()

    def detectEquip(self):
        idEquip = self.equip.getConfig()
	k = 0
        while not idEquip:
	      if self.acabar:
		 return
 
              time.sleep(int(math.exp(k)))

              idEquip = self.equip.getConfig()              
              self.errorComm = not idEquip
              
              k = (k + 1) % 30

	return idEquip

    def doPause(self):
	self.logger.info("Pausing lector of: %s" % self.idEquip)
        self.equip.devComm.close()

        while self.pause:
              time.sleep(1)

        self.logger.info("Resuming lector of: %s" % self.idEquip)
        self.equip.devComm.resetConnection()

    def statusEquip(self):
        if self.ready:
           self.equip.status()

    def run(self):
        self.logger.info("Starting lectorGen ...")
        self.logger.debug("Detecting power-meter device ...")

        self.idEquip = self.detectEquip() 

        self.logger.info("Power-meter detected: %s" % self.idEquip)

        qOut = Queue.Queue(0)
        self.dataExp = dataExport(qOut, self.dExports, self.equip, self.nodeConf)
        self.dataExp.setDaemon(True)       
        self.dataExp.start()

        tempsInicial = time.time()
        horaGravacio = ''
        self.ready = self.forceReq = True
        lectures = 0
        k = 0

        while not self.acabar:
            if self.pause:
	       self.doPause()

            horaActual = time.strftime("%H:%M")
            diffT = int(int(time.time()) - tempsInicial)

            # Gravacio de la mitja de les lectures fetes

            if horaActual in self.lHores:
                if ((horaActual != horaGravacio) and lectures > 0):
                    self.logger.info("Sending %d sample(s) to dataExport ..." % (lectures+1))
                    qOut.put(self.equip.darreraLectura)
                    self.equip.resetValues()
                 
                    horaGravacio = time.strftime("%H:%M")
                    lectures = 0

            # Lectura del analitzador

            if ((diffT > self.tempsLectura) or self.forceReq):                
                self.logger.debug("%(hora)s Sample number %(nLect)d" % {"hora": time.strftime("%H:%M"), "nLect": lectures})

                response = self.equip.query()
                if response:
                   tempsInicial = time.time()
                   lectures += 1    
                   k = 0
                else:
                   self.logger.error("Communications error with %s" % self.idEquip)
                   tempsInicial = int(time.time()) + int(math.exp(k))
                   k = (k + 1) % 10

                self.errorComm = not response
                self.forceReq = False

            time.sleep(0.5)

        self.logger.info("Stopping lectorGen of: %s" % self.idEquip)
        self.dataExp.aturar = True
        qOut.join()
        self.logger.info("LectorGen of %s is stopped!" % self.idEquip)
