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

    def statusEquip(self):
        if self.ready:
           self.equip.status()

    def run(self):
        qOut = Queue.Queue(0)
        lectures = 0
        k = 0 

        self.logger.info("Iniciant lector ...")
        self.logger.debug("Identificant analitzador ...")
        
        idEquip = self.equip.getConfig()
        while not idEquip:
              time.sleep(int(math.exp(k)))

              idEquip = self.equip.getConfig()              
              self.errorComm = not idEquip
              
              k = (k + 1) % 30

        self.idEquip = idEquip

        self.dataExp = dataExport(qOut, self.dExports, self.equip, self.nodeConf)
        self.dataExp.setDaemon(True)       
        self.dataExp.start()

        self.logger.info("Identificat analitzador: %s" % self.idEquip)

        tempsInicial = time.time()
        horaGravacio = ''
        self.ready = self.forceReq = True

        k = 0
        while True:
            if self.pause:
               self.logger.info("Possat en pausa el lector per %s" % self.idEquip)
               while self.pause:
                     time.sleep(1)
               self.logger.info("Seguint llegint el %s" % self.idEquip)

            horaActual = time.strftime("%H:%M")
            diffT = int(int(time.time()) - tempsInicial)

            # Gravacio de la mitja de les lectures fetes

            if horaActual in self.lHores:
                if ((horaActual != horaGravacio) and lectures > 0):
                    #self.logger.info("%(hora)s Gravant %(nLect)d lectures " % {"hora": horaActual, "nLect": lectures})
                    qOut.put(self.equip.darreraLectura)
                    self.equip.resetValues()
                 
                    horaGravacio = time.strftime("%H:%M")
                    lectures = 0

            # Lectura del analitzador

            if ((diffT > self.tempsLectura) or self.forceReq):
                
                self.logger.info("%(hora)s Lectura numero %(nLect)d" % {"hora": time.strftime("%H:%M"), "nLect": lectures})

                request = self.equip.query()
                if request:
                   tempsInicial = time.time()
                   lectures += 1    
                   k = 0
                else:
                   self.logger.error("Error en la comunicacio")
                   tempsInicial = int(time.time()) + int(math.exp(k))
                   k = (k + 1) % 10

                self.errorComm = not request
                self.forceReq = False

            time.sleep(0.5)
