
import time, threading, logging, logging.config, Queue
from os import path

def loadExporter(classname):
    module = __import__("export."+classname)
    classobj = getattr(module, classname)
    return classobj

class dataExport(threading.Thread):
      def __init__(self, qOut, dExports, equip, nodeConf):
          self.queueOut = qOut
          self.queuePending = Queue.Queue(100)
          self.logger = logging.getLogger('lector.dataexport')

          self.lExport = []
          self.logger.info("Instanciam els exportardors ...")
          
          for modName,target in dExports.iteritems():
              self.logger.info("%s: a %s" % (modName, target))
              try:
                 modulExpM = loadExporter(modName)
                 modulExp = modulExpM(target, equip)
                 modulExp.nodeConf = nodeConf
                 self.lExport.append(modulExp)
              except ImportError, e:
                 self.logger.error("Error carregant el modul %s: %s" % (modName, str(e)))

          threading.Thread.__init__(self)
          
          w = threading.Thread(target = self.sendPending)
          w.setDaemon(1)
          w.start()

      def ferMitja(self, mostraLectures):
          mitja = {}
          for variable, valors in mostraLectures.iteritems():
              mitja[variable] = [float(0) for v in valors[0]]
              for v in valors:
                  mitja[variable] = map(lambda x,y:x+y, mitja[variable],[float(e) for e in v])

              mitja[variable] = [float(v)/len(valors) for v in mitja[variable]]

          return mitja

      def storePending(self):
          pendingSamples = []
          self.logger.info("Guardant totes les lectures pendents dins persistencia ...")
          while not self.queuePending.empty():
                (timeS, expP, lectura) = self.queuePending.get()
                pendingSamples.append((timeS, expP.__class__.__name__, lectura))
                self.queuePending.task_done()
          
          try:
              fPersist = open("dataExport.dat","wb")
              pickle.dump(pendingSamples, fPersist, pickle.HIGHEST_PROTOCOL)
              fPersist.close()
          except IOError, e:
              self.logger.error("Error guardant a persistencia: %s" % str(e))


      def sendPending(self):
          self.logger.info("Arrancant processador de enviaments pedents ...")
          while True:
                time.sleep(60)
                if self.queuePending.empty():
                   continue
                 
                if self.queuePending.full():
                   self.storePending()
                   continue
                
                self.logger.info("Hi ha %d lectures pendents d'enviar ..." % self.queuePending.qsize())
                
                while not self.queuePending.empty():
                      (timeS, expP, mitjaDades) = self.queuePending.get()
    
                      self.logger.info("Guardant lectura pendent de transmetre de dia: %s ..." % time.strftime("%d/%m/%Y %H:%M:%S", timeS))
                      try:
                         expP.save(timeS, mitjaDades)
                      except:
                         self.logger.error("Error re-gravant amb el pluggin: %s" % expP.__class__.__name__)
                         self.queuePending.put((timeS, expP, mitjaDades))
                         break
                
                      self.queuePending.task_done()
                
      def run(self):
          while True:
                mitjaDades = self.ferMitja(self.queueOut.get(block=True))
                self.logger.info("Guardant lectura ...")

                for expP in self.lExport:
                    timeS = time.localtime()
                    try:
                        expP.save(timeS, mitjaDades)
                    except Exception, e:
                        self.logger.error("Error gravant amb el pluggin %s: %s" % (expP.__class__.__name__, str(e)))
                        self.queuePending.put((timeS, expP, mitjaDades))

                self.queueOut.task_done()
                time.sleep(0.5) 
