#!/usr/bin/python
# -*- coding: utf-8 -*-
##########################################################################
#
# das8000.py
# Classe que s'encarrega de realitzar consultes i tractar les dades
# del DAS-8000 de Desin
#
# Tomeu Capó
#

import pickle, threading, hashlib, os, time
from params import das8000Regs

from modBusComm import READ_WORDS, READ_E_WORDS, REPOR_SLAVE, E_SND_ERROR, E_NOT_OPEN_COMM

class das8000:
    def __init__(self, devComm, vars, model):
        self.id = devComm.id
        self.idStr = ''
        self.devComm = devComm
        self.mutex = devComm.mutex
        self.variables = vars
        self.logger = None
        self.rangs = {}
        self.lastError = ""
        self.lastRead = ""
        self.lastStatus = {}
        self.lectura = {}
        self.model = model
        
        self.lastStatus = {}
        self.lastStatus["lastTime"] = 0
        if model in das8000Regs.tRegs.keys():
            self.regsQuery = das8000Regs.tRegs[model]
        else:
            raise KeyError, "Aquest model de dispositiu no esta soportat!"
            return 

        self.resetValues()
        
    @property
    def definitions(self):
        return self.regsQuery

    # Buida les darreres lectures fetes

    def resetValues(self):
        self.lastError = ""
        self.darreraLectura = {}
        for cmd in self.variables:
            self.darreraLectura[cmd] = []

    # Realitza una bateria de peticions a l'esclau
 
    def query(self):
        rebut = False
        self.lastError = ""
        
        for var in self.variables:
            params = self.regsQuery[var]
            #self.logger.debug("  %s:  %s" % (var, params["registre"]))
                    
            self.mutex.acquire()
            if not self.devComm.enviar(READ_E_WORDS, params["registre"], params["numRegs"]):
               self.mutex.release()
               if self.devComm.lastError in [E_NOT_OPEN_COMM, E_SND_ERROR]:
                  self.logger.error("Error enviant, reiniciarem connexio del dispositiu") 
                  self.devComm.resetConnection()                
               break
            
            rebut = self.devComm.rebre()
            self.mutex.release()
 
            if not rebut:
               self.lastError = self.devComm.msgError()
               self.logger.error(self.lastError)
               break
 
            # Agafam el valor de la lectura fet, si es un valor gran (compost)
            # llegim el darrer gran valor, si no agafam la llista de resultats simples
 
            vLectura = [self.devComm.lastBigIntValue] if params["compost"] else self.devComm.lastResponse

            # Agafam el factor d'escala el qual emprarem per calcular el valor de la lectura real
 
            factEscala = self.rangs[params["regEscala"]] if (params["regEscala"] in self.rangs) else params["valEscala"]
               
            # Darrerament, aplicam el factor d'escala i guardam la lectura

            dades = [0 if float(v) > params["valMax"] else (float(v) * factEscala) for v in vLectura]
            self.darreraLectura[var].append(dades)
            self.lectura[var] = dades
        
        if rebut:
           self.status()
           self.lastRead = time.strftime("%d/%m/%Y %H:%M:%S")
       
        return rebut  

    def clearCache(self):
        pass
 
    # Metode que ens torna el identificador del analitzador
    
    def identify(self):
        """
        self.mutex.acquire()        
        if not self.devComm.enviar(READ_E_WORDS, 1, 1):
           self.mutex.release()
           if self.devComm.lastError in [E_NOT_OPEN_COMM, E_SND_ERROR]:
              self.devComm.resetConnection()              
              self.logger.error("Error enviant, reiniciarem connexio del dispositiu")
              self.logger.debug("No s'ha pogut enviar la trama")   
           return ''
        rebut = self.devComm.rebre()
        self.mutex.release()
        """
        rebut = '' 
        if not rebut:
           self.lastError = self.devComm.msgError()
           self.logger.error("%d: %s " % (self.devComm.lastError, self.devComm.msgError()))
           return 'DAS-8000 Ver. Unknown'

        return "DAS-8000 Ver. %d" % self.devComm.lastBigIntValue   

    def getConfig(self):       
        self.logger.debug("Demanant configuracio i estat ... %d" % self.id)       
        self.logger.debug("\tLlegint configuracio del dispositiu...")
        
        self.idStr = self.identify()
        if not self.idStr:           
           return ''
                
        return self.idStr

    def status(self):
        pass
        """
        for statVar in ["HMU", "ERR"]:
            try:
                params = pmRegs.tRegs[self.model][statVar]
            except KeyError, e:
                raise KeyError, "Aquest driver de %s no te configurat el parametre %s" % (self.model, statVar)
                
            self.mutex.acquire()
            if not self.pmComm.enviar(READ_WORDS, params["registre"], params["numRegs"]):
               self.mutex.release()
               if self.pmComm.lastError in [E_NOT_OPEN_COMM, E_SND_ERROR]:
                  self.logger.error("Error enviant, reiniciarem connexio del dispositiu") 
                  self.pmComm.resetConnection()                
               continue
       
            rebut = self.pmComm.rebre()
            self.mutex.release()            

            if rebut:
               self.lastStatus[statVar] = self.pmComm.lastBigIntValue if params["compost"] else self.pmComm.lastResponse
               if statVar == 'ERR':
                  self.lastStatus["ERR_MSG"] = self.getErrorMessage()
                            
               self.lastStatus["lastTime"] = time.time()
        """    
        
    def loadRanges(self):
        pass
        """
        peticionsRng = {}
        for var in self.variables:
            if self.regsQuery[var]["regEscala"] in self.regsQuery:
                pet = self.regsQuery[var]["regEscala"]
                peticionsRng[pet] = self.regsQuery[pet]
          
        for pt in peticionsRng:
            params = self.regsQuery[pt]
            self.rangs[pt] = 0

            self.mutex.acquire()
            if not self.pmComm.enviar(READ_WORDS, params["registre"], params["numRegs"]):
               self.mutex.release()
               if self.pmComm.lastError in [E_NOT_OPEN_COMM, E_SND_ERROR]:
                  self.logger.error("Error enviant, reiniciarem connexio del dispositiu") 
                  self.pmComm.resetConnection()                
               continue
       
            if self.pmComm.rebre():
               self.rangs[pt] = pmRegs.factorEscala[str(self.pmComm.lastResponse[0])]
            self.mutex.release()
        """
        
    def getErrorMessage(self):
        if not self.lastStatus.get("ERR"):
           return 'NO_ERROR'

        retval=[]        
        bitMapError = self.lastStatus["ERR"]
        if bitMapError:
           for mask, msgError in ERROR_MASK.iteritems():            
               if bitMapError & mask:
                  retval.append(msgError)

        return retval
    
    @property
    def lastValues(self):
        return {"lastRead": self.lastRead, "values": self.lectura} 
    
    def __str__(self):
        return pickle.dumps(self.lectura)

