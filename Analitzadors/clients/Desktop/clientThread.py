#!/usr/bin/python

import time
from PyQt4.QtCore import *
from api.client import *

REFRESH_TIME=5

class clientThread(QThread): 
    def __init__(self, ui, addr):
        QThread.__init__(self)
        self.values = {}
        #self.vars = []
        self.ui = ui
        self.seguir = True
        self.connectat = False
        self.addr = addr
        self.tempsRefresc = REFRESH_TIME

    def __del__(self):
        self.seguir = False
        if self.connectat:
           self.cliLector.desconnecta()

    def getStatus(self, idEquipCfg):
        idEquip = int(idEquipCfg)

        (estatLector, estatComm) = self.cliLector.getStatus(idEquip)

        self.ui.statusbar.showMessage("Llegint ID de %d ..." % idEquip)
        idEquipStr = self.cliLector.getId(idEquip).rstrip()
        
        if not idEquipStr or idEquipStr == "INT_ERR":
           self.ui.statusbar.showMessage("No connectat ...")
           return False
                
        self.ui.statusbar.showMessage("Llegint definicions de %d ..." % idEquip)
        defs = self.cliLector.getDefs(idEquip)
        self.ui.statusbar.showMessage("Llegint variables de %d ..." % idEquip)
        try:
            vars = self.cliLector.getVars(idEquip)["values"]
        except:
            vars = {}
        self.values[idEquipCfg] = {"id": "%d: %s" % (idEquip, idEquipStr), "defs": defs, "vars": vars, "estatLector": estatLector, "estatComm": estatComm }
        return True
    
    def connectar(self):
        self.ui.statusbar.showMessage("Connectant amb %s:%d ..." % self.addr)
        try: 
           self.cliLector = ctrlLector(self.addr)
           self.connectat = True
        except Exception, err:
           raise

        self.ui.statusbar.showMessage("Llegint configuracio del servidor ...")
        self.conf = self.cliLector.getConf()

        equips = self.conf.get("equips")
        tl = 0
        for idEquip, params in equips.iteritems():
            self.getStatus(idEquip)
            tl += int(params["config"]["params"]["tempslectura"])

        if len(self.values)<1:
           return False

        if tl > 0 and len(equips.keys()) > 0:
           self.tempsRefresc = int(tl/len(equips.keys()))/2

        print "Temps de refresc = ",self.tempsRefresc

        if self.cliLector.connectat:
           self.ui.statusbar.showMessage("Servidor de lectures actiu ...")
           self.ui.actionConnectar.setEnabled(0)
           #self.emit(SIGNAL("defColsHist()"))
           for id, values in self.values.iteritems():
               self.emit(SIGNAL("pintaEstat(int)"), id)
               if values["estatLector"] == STA_PAUSED:
                  self.ui.actionIniciar.setEnabled(1)
                  break
        else:
           self.ui.statusbar.showMessage("Servidor de lectures actiu i esperant ...")
           self.ui.actionConnectar.setEnabled(1)
           self.ui.actionIniciar.setEnabled(1)

	return True

    def iniciar(self):
        for id, values in self.values.iteritems():
            if values["estatLector"] == STA_STOPPED:    
               self.cliLector.start(id)
            elif values["estatLector"] == STA_PAUSED:  
               self.cliLector.resume(id)
               
    def pausar(self):
        for id, values in self.values.iteritems():
            if values["estatLector"] == STA_STARTED:
               print "Possant en pausa: ", id
               self.cliLector.pause(id)
               (self.values[id]["estatLector"], self.values[id]["estatComm"]) = self.cliLector.getStatus(id)
               self.emit(SIGNAL("pintaEstat(int)"), id)
      
    def run(self):
        print "Thread running ..."
        while self.seguir:
              k=0
              for id in self.values.keys():
                  (self.values[id]["estatLector"], self.values[id]["estatComm"]) = self.cliLector.getStatus(id)
                  if self.values[id]["estatLector"] == STA_STARTED and self.values[id]["estatComm"] == STA_COMM:
                     try:
                        self.values[id]["vars"] = self.cliLector.getVars(id)["values"]
                        self.emit(SIGNAL("pintaVars(int)"), id)
                     except:
                        k=10 
                     
                  self.emit(SIGNAL("pintaEstat(int)"), id)
                  
              self.sleep(self.tempsRefresc+k)

        self.cliLector.desconnecta()
