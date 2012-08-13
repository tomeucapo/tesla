# -*- coding: utf-8 -*-
##########################################################################################
# @file dataExport.py
# Data exporter module. This module manages different submodules export of data 
# that can be charged based on the general configuration file config.xml.
#
# @author Tomeu Capó
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

          self.logger.info("Starting data exporters ...")
          
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
          while not self.queuePending.empty():
                (timeS, expP, data) = self.queuePending.get()
                self.pendingSamples.append((time.mktime(timeS), expP.__class__.__name__, pickle.dumps(data)))
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

          self.logger.info("Storing %d sample(s) to disk ..." % len(self.pendingSamples))
          persistDb = lite.connect(DB_BULK)

          try:
              cur = persistDb.cursor()
              cur.executemany("INSERT INTO SAMPLES VALUES(?, ?, ?)", self.pendingSamples)
              persistDb.commit()
          except lite.DataError, e:
              self.logger.error("Persistence store error: %s" % str(e))
          else:
              self.pendingSamples = []


          persistDb.close()

      def loadBulk(self):
          self.logger.info("Loading bulk from disk ...")
          persistDb = lite.connect(DB_BULK)

          try:
              cur = persistDb.cursor()
              cur.execute("select time, module, data from samples")
              for row in cur:
                  self.pendingSamples.append(row)                                        
          except lite.DatabaseError, e:
              self.logger.error("Persistence store error: %s" % str(e))

          persistDb.close()

      def sendPending(self):
          self.logger.info("Starting pending processor sender ...")          
          while True:
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
                      except Exception, e:
                         self.logger.error("Pluggin %s error: %s" % (expP.__class__.__name__, str(e))
                         self.queuePending.put((timeS, expP, mitjaDades))
                         break
                
                      self.queuePending.task_done()
                
      def run(self):
          while True:
                mitjaDades = self.dataAverage(self.queueOut.get(block=True))
                self.logger.info("Storing sample data ...")

                for mName, expP in self.lExport.iteritems():
                    timeS = time.localtime()
                    try:
                        expP.save(timeS, mitjaDades)
                    except ClientError, e:
                        self.logger.error("Pluggin %s error: %s" % (expP.__class__.__name__, str(e)))
                        self.queuePending.put((timeS, expP, mitjaDades))
                    except Exception, e:
                        self.logger.fatal("Pluggin %s unexpected error: %s" % (expP.__class__.__name__, str(e)))
                                            
                self.queueOut.task_done()
