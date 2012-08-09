# -*- coding: iso-8859-1 -*-
##########################################################################
#
# cvmComm.py
# Classe que s'encarrega de les comunicacions amb analitzadors d'energia
# de la serie CVMk del fabricant Circutor.
#
# Tomeu Capó
#

import serial
import time

STX = "$"
ETX = chr(10)
TOUT_RX = 20

E_OK = 0
E_NOT_RESPONSE = 1
E_CHKSUM_ERROR = 2
E_SND_ERROR = 3

msgErrors = {E_NOT_RESPONSE: "El dispositiu CVM no reson, ho tonare a provar",
             E_CHKSUM_ERROR: "La trama rebuda es erronea",
             E_SND_ERROR:    "No puc enviar la trama al dispositiu"}

class cvmComm:
      def __init__(self, dspNum, dsp): 
          self.id = dspNum
          self.dispositiu = dspNum
          (self.serie, self.mutex) = dsp
          self.lastCmd = ''
          self.lastResponse = ''
          self.lastError = E_OK
          self.logger = None
 
      def enviar(self, cmd, arg):
          retval = True
         
          sndtxt = STX+"%(dsp)02d%(cmd)s" % {"dsp": self.id, "cmd": cmd.upper()}
          if cmd[0] == 'W':
             sndtxt += "%(arg)02d" % {"arg": arg}

          chksum = reduce(lambda x, y: x+y, [ord(c) for c in sndtxt])%256
          sndtxt += "%(chk)02X%(etx)s" % {"chk": chksum, "etx": ETX}   

          self.logger.debug("[ TX ] "+sndtxt[:-1])
          self.lastCmd = cmd
          self.lastError = E_OK
 
          try:
             self.serie.write(sndtxt)
          except serial.serialutil.SerialException, e:
             retval = False
             self.lastError = E_SND_ERROR

          time.sleep(0.5)
          return(retval) 
                  
      def rebre(self):
          retval = True
          
          c = self.serie.read()
         
          sTime = time.time()
          while c != STX:
                if time.time()-sTime < TOUT_RX:
                   c = self.serie.read()
                else:
                   self.lastError = E_NOT_RESPONSE
                   return False
          
          inst = ''
          while c != ETX:
                inst += c
                c = self.serie.read()

          chkRx = int("0x"+inst[-2:], 16)
          frameRx = inst[:-2] 
          chkCa = reduce(lambda x, y: x+y, [ord(c) for c in frameRx])%256

          if chkRx != chkCa:
             retval = False
             self.lastError = E_CHKSUM_ERROR
          else:
             self.lastResponse = frameRx[3:]
             self.lastError = E_OK 
         
          self.serie.flushInput()
          self.serie.flushOutput()
 
          self.logger.debug("[ RX ] "+inst)
          return(retval)

      def msgError(self):
          if self.lastError>0:
             return(msgErrors[self.lastError])     
          else:
             return('')

