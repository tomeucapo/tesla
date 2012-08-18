# -*- coding: iso-8859-1 -*-
##########################################################################
#
# cvmData.py
# Classe que s'encarrega de realitzar consultes i tractar les dades
# d'analitzadors CVMk del fabricant Circutor.
#
# Tomeu Capó
#

from params import cvmCmds 
import pickle

class cvmData:
      def __init__(self, cvmComm, vars, model):
          self.cvmComm = cvmComm
          self.mutex = cvmComm.mutex
          self.variables = vars
          self.logger = None
          self.model = model
          self.regsQuery = cvmCmds.cmdsCVMk 
          self.lastError = ""
          self.lastStatus = {}
          self.lectura = {}
          self.resetValues()
      
      def setVariables(self, vars):
          self.variables = vars
  
      def getDefs(self):
          return pickle.dumps(self.regsQuery)

      def resetValues(self):
          self.darreraLectura = {}
          for cmd in self.variables:
              self.darreraLectura[cmd] = []

      def __chunks__(self, var):
          i=0
          chunks=[]
          longChunk = self.regsQuery[var]["numDigits"] 		# pos: 4
          infoFrame = self.cvmComm.lastResponse

          while i<len(infoFrame):
                chunks.append(infoFrame[i:i+longChunk])
                i+=longChunk

          return chunks
 
      def query(self):
          rebut = False
          for var in self.variables:
              params = self.regsQuery[var]
              self.mutex.acquire()
              if not self.cvmComm.enviar(params["registre"], 0):
                 self.mutex.release()
                 continue
              rebut = self.cvmComm.rebre()
              self.mutex.release()

              if not rebut:
                 self.logger.error(self.cvmComm.msgError())
                 self.lastError = self.cvmComm.msgError()
                 break

              dades = [ float(chunk)*float(params["valEscala"]) if chunk else 0.0 for chunk in self.__chunks__(var) ]
              self.darreraLectura[var].append(dades)
              self.lectura[var] = dades

          return(rebut)  

      def identify(self):
          retval='CVMk'

          self.mutex.acquire() 
          if not self.cvmComm.enviar("VER", 0):
             self.mutex.release()
             return retval
          rebut = self.cvmComm.rebre()
          self.mutex.release()
 
          if rebut:
             retval = self.model+" Ver. "+self.cvmComm.lastResponse
          else:
             self.lastError = self.cvmComm.msgError() 
             self.logger.error(self.lastError)
                       
          return(retval)

      def status(self):
          pass

      def __str__(self):
          return pickle.dumps(self.lectura)
