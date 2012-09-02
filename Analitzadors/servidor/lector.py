#!/usr/bin/python
# -*- coding: utf-8 -*-

import time, sys, os
import logging, logging.handlers, logging.config
import ConfigParser

from lectorSrv import *

LEVELS = {'debug':    logging.DEBUG,
          'info':     logging.INFO,
          'warning':  logging.WARNING,
          'error':    logging.ERROR,
          'critical': logging.CRITICAL}

try:
    logging.config.fileConfig("logging.ini")
except Exception, e:
    print "Error al obrir el fitxer de la configuracio de logs: ",str(e)
    sys.exit(-1)

def getConfig():
    global logLevel, autoStart, logDir

    config = ConfigParser.ConfigParser()
    try:
        config.read('lector.ini')
        logLevel = config.get("General","log_level")
        autoStart = config.get("General","auto_start")
        logDir = config.get("General", "log_dir")
    except Exception, e:
        raise Exception, "No puc llegir el fitxer de configuracio lector.ini"
        
if __name__ == '__main__':
   try:
      getConfig()
   except Exception, e:
      print "Error llegint lector.ini: ",str(e)
      sys.exit(-1)

   if len(sys.argv) > 1:
      logLevel = sys.argv[1]

   my_logger = logging.getLogger('lector.main')
   level = LEVELS.get(logLevel, logging.NOTSET)
   my_logger.setLevel(level)

   my_logger.info("*** Instanciant servidor de central de mesures ...")

   try:
       srvLec = srvLector()
   except Exception, err:
       print "Error al LectorSrv: ",str(err)
       my_logger.error(str(err))
       sys.exit(-2)
 
   my_logger.info("Arracam els lectors ...")

   if autoStart.upper() == "YES":
      srvLec.startAll()

   while not srvLec.acabar: 
         try:
             time.sleep(0.05)
         except KeyboardInterrupt, e:
             break

   msg = "*** Programa finalitzat ..."
   my_logger.info(msg)
   print msg
   sys.exit(0)
