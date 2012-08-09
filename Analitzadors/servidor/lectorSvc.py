#!/usr/bin/python
# -*- coding: utf-8 -*-

import win32service, win32serviceutil, win32api, win32con, win32event, win32evtlogutil
import os, sys, logging, logging.handlers
import ConfigParser
import servicemanager      

from lectorSrv import *

LOG_FILENAME = 'log\\lector.log'

LEVELS = {'debug':    logging.DEBUG,
          'info':     logging.INFO,
          'warning':  logging.WARNING,
          'error':    logging.ERROR,
          'critical': logging.CRITICAL}

class lectorService(win32serviceutil.ServiceFramework):
   
   _svc_name_ = "lector"
   _svc_display_name_ = "Servidor de lectures 3.0"
   _svc_description_ = u"Sistema de monitoritzacio de mesures electriques"
         
   def __init__(self, args):
       global LEVELS
       self.arguments = args
       self.autoStart = ""
       
       if len(args) > 1:
          self.logLevel = LEVELS.get(args, logging.NOTSET)
       else:
          self.logLevel = logging.INFO

       config = ConfigParser.ConfigParser()
       try:
          config.read('lectorSvc.ini')
          self.svcPath = config.get("General","svc_path")
          self.autoStart = config.get("General","auto_start")
       except Exception, e:
          servicemanager.LogErrorMsg("No puc llegir el fitxer de configuracio lectorSvc.ini")
          sys.exit(-1)

       win32serviceutil.ServiceFramework.__init__(self, args)          
       self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)           

   def SvcStop(self):
       self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
       win32event.SetEvent(self.hWaitStop)
       self.ReportServiceStatus(win32service.SERVICE_STOPPED)
         
   def SvcDoRun(self):
       servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, '')) 
       os.chdir(self.svcPath)
       
       try:
          logging.config.fileConfig("logging.ini")
       except Exception, e:
          servicemanager.LogErrorMsg("Error al obrir el fitxer: %s" % str(e))
          sys.exit(-1)

       my_logger = logging.getLogger('lector.main')

       try:
          srvLec = srvLector()
       except Exception, err:
          servicemanager.LogErrorMsg(str(err))
          return       
       servicemanager.LogInfoMsg("*** Iniciat el servidor de lectures i esperant ...")

       my_logger.info(self.arguments)
       
       if self.autoStart.upper() == "YES":
          srvLec.startAll()

       win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

       msg = "*** Servidor de lectures aturat"
       my_logger.info(msg)
       servicemanager.LogInfoMsg(msg)
                     
def ctrlHandler(ctrlType):
   return True

if __name__ == '__main__':   
   win32api.SetConsoleCtrlHandler(ctrlHandler, True)   
   win32serviceutil.HandleCommandLine(lectorService)

