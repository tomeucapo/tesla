from datetime import *
import time, logging, os.path

class localFile:
      def __init__(self, target, equip):
          self.idPM = equip.idStr
          self.mitjaDades = {}
          self.dirFitxer = target
          self.lastValues = {}
          self.logger = logging.getLogger('lector.dataexport')

          if not os.path.exists(target):
             raise Exception, "El path %s no existeix!" % target

          if equip.id:
             self.dirFitxer = os.path.join(self.dirFitxer, str(equip.id))

          if not os.path.exists(self.dirFitxer):   
             os.mkdir(self.dirFitxer)

      def setDir(self, directori):
          self.dirFitxer = directori

      def createFile(self, fitxerLog, lectura):
          flog = open(fitxerLog, "w")
          flog.write("HORA\t")
          for lect in lectura:
              for i in range(len(lectura[lect])):
                  flog.write(lect+"%(#)d\t" % {"#": i})
          flog.write("\n")
          return flog
      
      def save(self, timeS, lectura=None):            
          fitxerLog = os.path.join(self.dirFitxer, "%s.txt" % time.strftime("%Y%m%d", timeS))
          fitxerEstat = os.path.join(self.dirFitxer,"analitzador.dat")

          self.logger.info("Gravant lectura a fitxer: %s" % fitxerLog)           

          if not lectura:
             lectura = self.mitjaDades
          else:
             self.mitjaDades = lectura
             
          if os.path.exists(fitxerLog):
             if len(self.lastValues) > 0 and len(lectura) != len(self.lastValues):
                flog = self.createFile(fitxerLog, lectura)  
             else:
                flog = open(fitxerLog, "a")
          else:            
             flog = self.createFile(fitxerLog, lectura)
          
          flog.write("%s\t" % time.strftime("%H:%M:%S", timeS))

          for variable, valors in lectura.iteritems():
              for valor in valors:
                  flog.write("%(v)9.2f\t" % {"v": valor})

          flog.write("\n")
          flog.close()

          festat = open(fitxerEstat, "w")
          festat.write(self.idPM+"\t")
          festat.write(datetime.ctime(datetime.today()))
          festat.close()
          
          self.lastValues = lectura
