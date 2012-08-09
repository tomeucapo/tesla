#!/usr/bin/python

from PyQt4 import QtCore, QtGui
from ui.frmConfiguracioSrv import Ui_configuracio

class Configuracio(QtGui.QDialog):
      defaults = {"ipServidor":   "127.0.0.1",
                  "portServidor": 50007, "dirExport": ""}

      cliThr = None

      def __init__(self):
          QtGui.QDialog.__init__(self)

          self.ui = Ui_configuracio()
          self.ui.setupUi(self)

          self.settings = QtCore.QSettings("visor.ini", QtCore.QSettings.IniFormat)
          if not self.settings.contains("ipServidor"):
             for key in self.defaults.keys():
                  self.settings.setValue(key, QtCore.QVariant(self.defaults[key]))
 
      def guardar(self):
          self.settings.setValue("ipServidor", QtCore.QVariant(str(self.ui.cAddrServidor.displayText())))

      def carregar(self):
          self.ui.cAddrServidor.setText(self.settings.value("ipServidor").toString())
       
          if self.cliThr is None:
             QtGui.QMessageBox.warning(self, self.tr("Alerta"), "No es pot llegir la configuracio del servidor per\nper que no estam connectats!")
             return

          """      
          if len(self.cliThr.conf)<2:
                self.ui.cDispSerie.setText(self.cliThr.conf[0]["disp"])  
                self.ui.cVelocitat.setEditText(self.cliThr.conf[0]["baud"])
                self.ui.cBits.setValue(int(self.cliThr.conf[0]["bits"]))
                self.ui.cTimeout.setValue(int(self.cliThr.conf[0]["timeout"]))

                self.ui.cFabricant.setText(self.cliThr.conf[1]["fabricant"])
                self.ui.cModel.setText(self.cliThr.conf[1]["model"])
                self.ui.cNumUnitat.setText(self.cliThr.conf[1]["unitat"])

                self.ui.cTempsLectura.setValue(int(self.cliThr.conf[1]["tempslectura"]))
                self.ui.cTempsGravacio.setValue(int(self.cliThr.conf[1]["tempsgravacio"]))

                lin=0
                #self.ui.taulaParametres.setRowCount(len(self.cliThr.defs.keys()))
                for cmd, conf in self.cliThr.defs.iteritems():
                    col=2

                    self.ui.taulaParametres.setRowCount(lin+1)
                    nParams = len(conf)

                    if conf["regEscala"]!='E':
                       itemCheck = QtGui.QTableWidgetItem()
                       itemCheck.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
                       if cmd in self.cliThr.conf[2]:
                          itemCheck.setCheckState(QtCore.Qt.Checked)
                       else:
                          itemCheck.setCheckState(QtCore.Qt.Unchecked)

                       self.ui.taulaParametres.setItem(lin, 0, itemCheck)
                       self.ui.taulaParametres.setItem(lin, 1, QtGui.QTableWidgetItem(QtCore.QString(str(cmd))))
                       self.ui.taulaParametres.setItem(lin, 2, QtGui.QTableWidgetItem(QtCore.QString(str(conf["registre"]))))
                       self.ui.taulaParametres.setItem(lin, 3, QtGui.QTableWidgetItem(QtCore.QString(str(conf["numRegs"]))))
                       self.ui.taulaParametres.setItem(lin, 4, QtGui.QTableWidgetItem(QtCore.QString(unicode(conf["descripcio"]))))
                       self.ui.taulaParametres.setItem(lin, 5, QtGui.QTableWidgetItem(QtCore.QString(str(conf["valEscala"]))))
                       self.ui.taulaParametres.setItem(lin, 6, QtGui.QTableWidgetItem(QtCore.QString(str(conf["valMax"]))))
                       lin+=1
          """        
