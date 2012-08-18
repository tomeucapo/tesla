##########################################################################################
# @file dataExport.py
#
# Data exporter module. This module manages different submodules export of data 
# that can be charged based on the general configuration file config.xml.
#
# @author Tomeu Capo
#

import time, threading, logging, logging.config, Queue
import pickle
import sqlite3 as lite
from os import path

from export.exceptions import *

MAX_QUEUE_SIZE=100
DB_BULK="dataExport.db"

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
          self.aturar = False

          self.logger.info("Loading data exporters ...")
          
          for modName,target in dExports.iteritems():
              self.logger.info("%s: a %s" % (modName, target))
              try:
                 modulExpM = loadExporter(modName)
                 modulExp = modulExpM(target, equip)
                 modulExp.nodeConf = nodeConf
                 self.lExport[modulExp.__class__.__name__] = modulExp
              except ImportError, e:
                 self.logger.error("Error carregant el modul %s: %s" % (modName, str(e)))

          threading.Thread.__init__(self, name=self.__class__.__name__)
          
          w = threading.Thread(target = self.sendPending)
          w.setDaemon(1)
          w.start()

      def dataAverage(self, data):
          mitja = {}
          for variable, valors in data.iteritems():
              mitja[variable] = [float(0) for v in valors[0]]
              for v in valors:
                  mitja[variable] = map(lambda x,y:x+y, mitja[variable],[float(e) for e in v])

              mitja[variable] = [float(v)/len(valors) for v in mitja[variable]]

          return mitja

      def moveToBulk(self):
          self.logger.info("Move %d samples to bulk store ..." % self.queuePending.qsize())
          while self.queuePending.qsize() > int(self.queuePending.maxsize/2):
                (timeS, expP, data) = self.queuePending.get()
                self.pendingSamples.append((time.mktime(timeS), expP.__class__.__name__, pickle.dumps(data, pickle.HIGHEST_PROTOCOL)))
                self.queuePending.task_done()

      def storeBulk(self):
          if len(self.pendingSamples) == 0:
             return

          self.logger.info("Storing %d sample(s) to disk ..." % len(self.pendingSamples))
          try:
              cur = self.persistDb.cursor()
              cur.executemany("INSERT INTO SAMPLES VALUES(?, ?, ?)", self.pendingSamples)
              self.persistDb.commit()
          except lite.DataError, e:
              self.logger.error("Persistence store error: %s" % str(e))
          else:
              self.pendingSamples = []

      def deleteFromBulk(self, module, timeS):
          #self.logger.debug("Deleting record: %s ..." % time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(time.mktime(timeS)) ) )
          try:
              cur = self.persistDb.cursor()              
              query = "delete from samples where module='%s' and time=%d" % (module, time.mktime(timeS))
              cur.execute(query)
              
              self.logger.debug(query)
              self.persistDb.commit()
          except Exception, e:
              self.logger.error("Persistence delete error: %s" % str(e))

      def loadBulk(self):          
          try:
              cur = self.persistDb.cursor()
              cur.execute("select time, module, data from samples")
              
              for (timeS, moduleName, data) in cur:
                  module = self.lExport.get(str(moduleName))
                  pendTask = (time.localtime(timeS), module,  pickle.loads(str(data)))
                  self.queuePending.put(pendTask)           
                                                                 
              cur.close()
          except Exception, e:
              self.logger.error("Persistence load error: %s" % str(e))

      def sendPending(self):
          self.logger.info("Starting pending processor sender ...")    

          try:
                self.persistDb = lite.connect(DB_BULK)
          except lite.DatabaseError, e:
                self.logger.fatal(str(e))
                return

          self.loadBulk()                                                                                                        

          while not self.aturar:
                time.sleep(60)
                if self.queuePending.empty():
                   continue
                
                # Si la coa s'ha omplit ho gravam a persistencia

                if self.queuePending.full():
                   self.moveToBulk()
                   self.storeBulk()
                   continue

                self.logger.info("%d pending samples to send ..." % self.queuePending.qsize())
                
                while not self.queuePending.empty():
                      (timeS, expP, mitjaDades) = self.queuePending.get()
    
                      self.logger.info("Storing sample pending to send: %s ..." % time.strftime("%d/%m/%Y %H:%M:%S", timeS))
                      try:
                         expP.save(timeS, mitjaDades)                         
                      except ClientDuplicateEntry, e:
                         self.logger.warn(str(e))
                      except Exception, e:
                         self.logger.error("Pluggin %s error: %s" % (expP.__class__.__name__, str(e)))
                         self.queuePending.put((timeS, expP, mitjaDades))
                         break
                      
                      self.deleteFromBulk(expP.__class__.__name__, timeS)
                      self.queuePending.task_done()

          self.logger.info("Stopped pending processor sender ...")         

      #
      # Process principal que grava les lectures de cap als plugins
      #       
         
      def run(self):
          self.logger.info("Entering dataExport main loop ...")         
          
          while not self.aturar:
                mitjaDades = self.dataAverage(self.queueOut.get(block=True))
                self.logger.info("Storing sample data ...")

                for mName, expP in self.lExport.iteritems():
                    timeS = time.localtime()
                    try:
                        expP.save(timeS, mitjaDades)
                    except ClientDuplicateEntry, e:
                        self.logger.warn(str(e))
                    except ClientError, e:
                        self.logger.error("Pluggin %s error: %s" % (expP.__class__.__name__, str(e)))
                        self.queuePending.put((timeS, expP, mitjaDades))
                    except Exception, e:
                        self.logger.fatal("Pluggin %s unexpected error: %s" % (expP.__class__.__name__, str(e)))
                                            
                self.queueOut.task_done()
   
          self.dataExp.moveToBulk()
          self.dataExp.storeBulk()

          self.logger.info("Stopped dataExport ...")         