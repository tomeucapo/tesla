#!/usr/bin/python

from comm import *
import sys, pickle, re

STA_NOCOMM = 0xf0
STA_COMM = 0xff
STA_PAUSED = 2
STA_STARTED = 1
STA_STOPPED = 0

class ctrlLector(commLector):
      def __init__(self, addr):
          self.idEquip = ''
          self.connectat = False
          self.vars = {}
          self.config = {}
          self.started = False

          try:
             commLector.__init__(self, addr)
          except Exception, e:
             raise Exception, str(e) #"No hem puc connectar al servidor!"
             return 

          if not self.connectar():
             raise IOError, "No he pogut iniciar la sessio amb el servidor"
             return
          else:
             self.connectat = True   
             #self.status = self.getStatus(1)
             #self.started = (self.status == STA_STARTED)
            
      def setEquip(self, idEquip):
          self.idEquip = idEquip
          
      def getId(self, pIdEquip=None):
          idEquip = pIdEquip if pIdEquip else self.idEquip
          res = ''
          if self.connectat:
             if self.enviar("GETID@%s" % idEquip):
                res = self.rebre()
                try:
                   data = pickle.loads(res)
                   if not data is None:
                      res = ''
                except:
                   self.idEquip = res
                   pass
            
          if res == 'MAX_CLIENTS':
             raise Exception, "Numero maxim de clients excedits!"
            
          return self.idEquip               
 
      def getConf(self):
          if self.connectat:
             if self.enviar("GETCONF"):
                self.config = pickle.loads(self.rebre())
         
          return self.config

      def getVars(self, pIdEquip=None):
          idEquip = pIdEquip if pIdEquip else self.idEquip
          if self.connectat:
             if self.enviar("GETVARS@%s" % idEquip):
                res = self.rebre()
                try:
                   self.vars = pickle.loads(res)
                except: 
                   if res == 'MAX_CLIENTS':
                      raise Exception, "Numero maxim de clients excedits!"
            
          return self.vars
 
      def getDefs(self, pIdEquip=None):
          idEquip = pIdEquip if pIdEquip else self.idEquip
          if self.connectat:
             if self.enviar("GETDEFS@%s" % idEquip):
                self.defs = pickle.loads(self.rebre())

          return self.defs
 
      def startAll(self):
           retval = False

           if self.connectat:
              if self.enviar("STARTALL"):
                 resp = self.rebre()
                 retval = (resp=="START\tOK\r")
                 self.started = True
           return retval

      def pause(self, pIdEquip=None):
          retval = False
          idEquip = pIdEquip if pIdEquip else self.idEquip

          if self.connectat:
             if self.enviar("PAUSE@%s" % idEquip):
                resp = self.rebre()
                retval = (resp=="PAUSED\r")
                self.started = False
          return retval

      def resume(self, pIdEquip=None):
          retval = False
          idEquip = pIdEquip if pIdEquip else self.idEquip

          if self.connectat:
             if self.enviar("RESUME@%s" % idEquip):
                resp = self.rebre()
                retval = (resp=="RESUMED\r")
                self.started = False
          return retval
      
      def start(self, pIdEquip=None):
          retval = False
          idEquip = pIdEquip if pIdEquip else self.idEquip
          
          if self.connectat:
             if self.enviar("START@%s" % idEquip):
                resp = self.rebre()
                retval = (resp=="START\tOK\r")
                
                self.started = True
                        
          return retval
        
      def getStatus(self, pIdEquip=None):
          retval = (-1, -1)
          idEquip = pIdEquip if pIdEquip else self.idEquip
          if not self.connectat:
             return retval

          if not self.enviar("STATUS@%s" % idEquip):
             return retval

          resp = self.rebre() 
          if resp.startswith("STARTED"):
             status = STA_STARTED
          elif resp.startswith("PAUSED"):
             status = STA_PAUSED
          else:
             status = STA_STOPPED

          if "NOCOMM" in resp:
             retval = (status, STA_NOCOMM)
          else:
             retval = (status, STA_COMM)

          return retval 

      def desconnecta(self):
          if self.connectat:
             if self.enviar("QUIT"):
                resp = self.rebre()
                if (resp=="DISCONNECTED!\r"):
                   self.s.close()
                   self.connectat = False
