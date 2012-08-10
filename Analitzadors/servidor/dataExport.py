
import time, threading, logging, logging.config, Queue
import sqlite3 as lite

from os import path

MAX_QUEUE_SIZE=10
MAX_BULK_SIZE=20

def loadExporter(classname):
    module = __import__("export."+classname)
    classobj = getattr(module, classname)
    return classobj

class dataExport(threading.Thread):
      def __init__(self, qOut, dExports, equip, nodeConf):
          self.queueOut = qOut
          self.queuePending = Queue.Queue(MAX_QUEUE_SIZE)
          self.logger = logging.getLogger('lector.dataexport')

          self.idEquip = equip.id
          self.lExport = {}
          self.pendingSamples = []

          self.logger.info("Instanciam els exportardors ...")
          
          for modName,target in dExports.iteritems():
              self.logger.info("%s: a %s" % (modName, target))
              try:
                 modulExpM = loadExporter(modName)
                 modulExp = modulExpM(target, equip)
                 modulExp.nodeConf = nodeConf
                 self.lExport[modulExp.__class__.__name__] = modulExp
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

      def moveToBulk(self):
          self.logger.info("Move %d samples to bulk store ..." % self.queuePending.qsize())
          while not self.queuePending.empty():
                (timeS, expP, data) = self.queuePending.get()
                if not expP.available:
                   self.pendingSamples.append((timeS, expP.__class__.__name__, lectura))
                else:
                   try:
                       expP.save(timeS, data)
                   except:
                       self.pendingSamples.append((timeS, expP.__class__.__name__, lectura))

                self.queuePending.task_done()

      def moveToQueue(self, pModuleName):
          self.logger.info("Move samples of %s module, from bulk to queue ..." % pModuleName)

          for sample in self.pendingSamples:
              (timeS, moduleName, data) = sample
              if moduleName == pModuleName:
                 self.queuePending.put((timeS, self.lExport.get(module), data))
                 self.pendingSamples.remove(sample)

      def storeBulk(self):
          if len(self.pendingSamples) == 0:
             return

          self.logger.info("Storing bulk to disk ...")
          persistDb = lite.connect("dataExport.db")

          try:
              cur = persistDb.cursor()
              cur.executemany("INSERT INTO SAMPLES VALUES(?, ?, ?)", self.pendingSamples)
              self.pendingSamples = []
          except DatabaseError, e:
              self.logger.error("Persistence store error: %s" % str(e))

          persistDb.close()

      def loadBulk(self):
          self.logger.info("Loading bulk from disk ...")
          persistDb = lite.connect("dataExport.db")

          try:
              cur = persistDb.cursor()
              cur.execute("select time, module, data from samples")
              for row in cur:
                  self.pendingSamples.append(row)                                        
          except DatabaseError, e:
              self.logger.error("Persistence store error: %s" % str(e))

          persistDb.close()

      def sendPending(self):
          self.logger.info("Starting pending processor sender ...")          
          while True:
                time.sleep(60)
                if self.queuePending.empty():
                   continue
                 
                if self.queuePending.full():
                   self.moveToBulk()

                if len(self.pendingSamples) > MAX_BULK_SIZE:
                   for mName, expP in self.lExport.iteritems():
                       if expP.available:
                          self.logger.debug("Module %s is now available, move samples to queue ...")
                          self.moveToQueue(mName)
                   self.storeBulk()
   
                self.logger.info("%d pending samples to send ..." % self.queuePending.qsize())
                
                while not self.queuePending.empty():
                      (timeS, expP, mitjaDades) = self.queuePending.get()
    
                      self.logger.info("Storing sample pending to send: %s ..." % time.strftime("%d/%m/%Y %H:%M:%S", timeS))
                      try:
                         expP.save(timeS, mitjaDades)                                                  
                      except:
                         self.logger.error("Pluggin sending error: %s" % expP.__class__.__name__)
                         self.queuePending.put((timeS, expP, mitjaDades))
                         break
                
                      self.queuePending.task_done()
                

      def run(self):
          while True:
                mitjaDades = self.ferMitja(self.queueOut.get(block=True))
                self.logger.info("Storing sample data ...")

                for mName, expP in self.lExport.iteritems():
                    timeS = time.localtime()
                    try:
                        expP.save(timeS, mitjaDades)
                    except Exception, e:
                        self.logger.error("Pluggin store error %s: %s" % (expP.__class__.__name__, str(e)))
                        self.queuePending.put((timeS, expP, mitjaDades))

                self.queueOut.task_done()
                time.sleep(0.5) 
