#!/usr/bin/python
# -*- coding: utf-8 -*-

import Queue, serial, sys, pickle, time
import logging, threading

from server import server
from lectorGen import lector
from configurador import Configurador

def loadDriverModule(classname):
    ''' returns a class of "classname" from module "modname". '''
    module = __import__("drivers."+classname)
    classobj = getattr(module, classname)
    return classobj

class srvLector:
    
    # Constructor 
    
    def __init__(self):
        self.my_logger = logging.getLogger('lector.srv')
        self.acabar = False
        self.device = {}
        self.lectors = {}
        self.qRequest = Queue.Queue(100)
        self.qResponse = Queue.Queue(100)
        
        self.mutexC =  threading.Semaphore()
        
        self.my_logger.info("*** Lector de dades v.3.0 ***************************************")

        # Llegim la configuracio del fitxer config.xml

        self.my_logger.info("Carregant el fitxer de configuracio...")
        self.conf = Configurador()
        if not self.conf.llegeix():
           self.my_logger.error("Error al carregar la configuracio!")
           raise Exception, "Error al carregar la configuracio"  

        # Inicialitzam els dispositius i instanciam els lectors

        self.my_logger.info("Inicialitzant dispositius ...")
        self.__initDevices__()
        self.my_logger.info("Carregant drivers i instanciam els lectors ...")
        self.__initLectors__()
       
        # Instanciam el servidor de connexions TCP/IP
       
        self.my_logger.info("Instanciant servidor TCP/IP ...")
        
        try: 
            self.srv = server(self.qRequest, self.qResponse)
            self.srv.setDaemon(True)
        except IOError, err:
            self.my_logger.error(str(err))
            raise IOError, str(err)

        for t in range(3):
            w = threading.Thread(target = self.dispatchMessages, args=[t])
            w.setDaemon(1)
            w.start()
            
        self.srv.start()

 
    def __initDevices__(self):
        for idDev, confDev in self.conf.devices.iteritems():
            if confDev["type"] == "serial":
               config = confDev["config"]
               try:
                   self.device[idDev] = (serial.Serial(config["port"], config["baud"], timeout=float(config["timeout"]), bytesize=int(config["bits"])),
                                         threading.Semaphore())
               except serial.serialutil.SerialException, err:
                   raise serial.serialutil.SerialException, "Error initializing device %s: %s" % ( idDev, str(err) )
 
    def __initLectors__(self):
        for idEquip, confEquip in self.conf.equips.iteritems():
            self.my_logger.info("\tCarregant driver analitzador %s ..." % idEquip)
            equip = self.loadDriver(idEquip, confEquip)
            self.lectors[idEquip] = self.initLector(equip, confEquip);

    """
       Metode que empram per carregar els drivers
    """

    def loadDriver(self, idEquip, pConfig):
        config = pConfig["config"]
        requests = pConfig["requests"]
        params = config["params"]

        equipCommC = loadDriverModule(config["driver"])
        device = self.device.get(config["device"])
       
        if not device:
           raise Exception, "El dispositiu asociat no s'ha definit be"
        
        try:
            equipComm = equipCommC(idEquip, device)
        except Exception, err:
            self.my_logger.error(str(err))
            raise Exception, str(err)
        
        equipDadesC = loadDriverModule(config["dataDriver"])
        equipDades = equipDadesC(equipComm, requests, params["model"])
            
        equipComm.logger = logging.getLogger('lector.comm') 
        equipDades.logger = self.my_logger
        
        return equipDades

    """
       Metode que ens instancia un thread per lector
    """

    def initLector(self, equip, pConfig):
        config = pConfig["config"]
        params = config["params"]
        Tgravacio = int(params["tempsgravacio"])
        Tlectura = int(params["tempslectura"])

        # Instanciam el servidor de lectures
        try:
            myLector = lector(equip, pConfig["dataexport"], self.conf.node)
        except Exception, e:
            self.my_logger.error(str(e))
            raise Exception, str(e)
           
        myLector.setMaxLectures(Tgravacio, Tlectura)
        myLector.setDaemon(True)

        self.my_logger.info("*****************************************************************")
        self.my_logger.info("    Analitzador = "+params["fabricant"]+" model "+params["model"])
        self.my_logger.info("    Interval de lectura  = "+params["tempslectura"]+" segons")
        self.my_logger.info("    Interval de gravacio = "+params["tempsgravacio"]+" minuts")
        self.my_logger.info("*****************************************************************")
         
        return myLector 

    """
        Metodes referents a cada comanda valida del servidor
    """
    
    def reloadConf(self, id=None):
        retval = "RELOAD\tOK"
        self.my_logger.info("Reloading config file ...")
        
        self.mutexC.acquire()
        if not self.conf.llegeix():
           self.mutexC.release()
           return 'SRV_CONF_ERR'
        
        for idEquip, confEquip in self.conf.equips.iteritems():
            parmAnalitza = confEquip["config"]["params"]
            try:     
                lector = self.lectors.get(idEquip)
            except Exception, e:
                self.mutexC.release()
                return "SRV_ERR: %s" % str(e)
            
            lector.setMaxLectures(int(parmAnalitza["tempsgravacio"]), int(parmAnalitza["tempslectura"]))
            lector.equip.variables = confEquip["requests"]
        
        self.mutexC.release()            
        return retval
    
    def start(self, idLector):
        lector = self.lectors.get(idLector)
        if not lector.isAlive():
           lector.start()
           return("START\tOK")

        return("ALLREADY START") 
        
    def startAll(self, idLector=None):
        for lector in self.lectors.values():
            lector.start()

        return("STARTING")       

    def shutdown(self, idLector=None):
        self.acabar = True
        self.srv.aturaTot = True
        return("DONE")

    def getDefs(self, idLector):
        lector = self.lectors.get(idLector)
        return pickle.dumps(lector.equip.definitions)

    def getID(self, idLector):
        lector = self.lectors.get(idLector)
        if lector and lector.ready:
           return lector.equip.idStr
        
        return ("INT_ERR")

    def getVars(self, idLector):
        lector = self.lectors.get(idLector)
        return (pickle.dumps(lector.equip.lastValues))

    def getStatus(self, idLector):
        lector = self.lectors.get(idLector)
        if not lector.errorComm:
           lector.statusEquip()

        return (pickle.dumps(lector.equip.lastStatus))
        
    def forceReq(self, idLector):
        lector = self.lectors.get(idLector)	
        lector.forceReq = True
        return("FORCE REQUESTED")

    def readConf(self, typeConf):
        if typeConf == 'XML':
           return pickle.dumps(self.conf.dom)
        
        return self.conf

    def status(self, idLector):
        lector = self.lectors.get(idLector)
        
        msgComm = "NOCOMM\t%s" % lector.equip.lastError if lector.errorComm else "COMM\t"
        msgStatus = "STARTED" if lector.isAlive() else "STOPPED"
        msgStatus = "PAUSED" if lector.isAlive() and lector.pause else msgStatus
        
        return("%s\t%s" % (msgStatus, msgComm))

    def identify(self, idLector):
        lector = self.lectors.get(idLector)
        lector.identifyEquip()
        if lector.equip.idStr:
           return lector.equip.idStr

        return("IDENT ERROR")      
            
    def pause(self, idLector):
        lector = self.lectors.get(idLector)
        if lector.isAlive():
           lector.pause = True 
           return("PAUSED") 

        return("IS STOPPED")

    def resume(self, idLector):
        lector = self.lectors.get(idLector)
        if lector.isAlive():
           lector.pause = False 
           return("RESUMED") 

        return("IS STOPPED")

    def donothing(self, idLector=None):
        pass

    def errorCmd(self, idLector=None):
        return("NOT IMPLEMENTED")

    # Accions valides del servidor
    
    validActions = {"GETID"   : getID,
                    "GETVARS" : getVars,
                    "GETCONF" : readConf,
                    "GETDEFS" : getDefs,
                    "GETSTATUS": getStatus,
                    "IDENT"   : identify,
                    "FORCEREQ": forceReq,
                    "SHUTDOWN": shutdown,
                    "START"   : start,
                    "STARTALL": startAll,
                    "PAUSE"   : pause,
                    "RESUME"  : resume,
                    "RELOAD"  : reloadConf,
                    "STATUS"  : status,
                    "QUIT"    : donothing,
                    "HELP"    : donothing}
    
    # Metode que cridarem cada vegada que volem processar una comanda rebuda
    
    def dispatchMessages(self, idWorker):
        self.my_logger.info("Worker %d: Starting..." % idWorker)
        while not self.acabar:
            try:               
                self.my_logger.debug("Worker %d: Waiting for new task ..." % idWorker)
                task = self.qRequest.get(block=True)                
                ((cmd, args), sockCli) = task
                self.my_logger.debug("Worker %d: Received task %s ..." % (idWorker, cmd))
                if not cmd:
                   continue
                
                try:
                    arg = int(args) if args else 0
                except ValueError:
                    arg = args
            
                self.my_logger.debug("Worker %d: Execute %s command. (Qu = %d)" % (idWorker, cmd, self.qRequest.qsize()))
                retval = self.validActions.get(cmd, self.errorCmd)(self, arg)

                if retval:
                    self.my_logger.debug("Worker %d: Sending response ..." % idWorker)
                    self.qResponse.put((cmd, sockCli, retval))
                    
            except Queue.Empty, e:
                self.my_logger.error("Worker %d: %s" % (idWorker, str(e)))                
            except ValueError, e:
                self.my_logger.error("Worker %d: %s" % (idWorker, str(e)))
            except Exception, e:
                self.my_logger.error(str(e))
                self.qResponse.put( (cmd, sockCli, "SRV_ERR %d:\t%s" % (idWorker, str(e))) )
            
            self.qRequest.task_done()

        self.my_logger.info("Worker %d: Finished..." % idWorker)
