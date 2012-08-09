#!/usr/bin/python
# -*- coding: utf-8 -*-
############################################################################
#
# visor.py
# Client per a connectarse al lector de dades i visualitzar les lectures
# i gràfiques.
#
# Author.......: Tomeu Capó Capó 2010 (C)
# Last Modified: 29/01/2010
# Use under terms of GNU public licence.

import time, sys, os
from PyQt4 import QtCore, QtGui

# Moduls especifics de l'aplicació

from clientThread import *
#from grafiques import *
from visorVariable import *
from configuracio import *

# Moduls de la GUI

from ui.frmPrincipal import Ui_finestraPrincipal

################################################################################
# Visor GUI

class Visor(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.visors = {}
        self.grafiques = {}
        self.analitzador = {}

        self.col = 1
        self.fila = 1
        self.lineTable = 1

        self.cliThr = None

        self.ui = Ui_finestraPrincipal()
        self.ui.setupUi(self)

        self.dConfig = Configuracio()

        self.connect(self.ui.actionConnectar, SIGNAL("triggered()"), self.onCmdConnectar)
        self.connect(self.ui.actionDesconnectar, SIGNAL("triggered()"), self.onCmdDesconnectar)
        self.connect(self.ui.actionIniciar, SIGNAL("triggered()"), self.onCmdIniciar)

        self.connect(self.ui.actionExportaGrafiques, SIGNAL("triggered()"), self.onCmdExportarGrafiques)
        self.connect(self.ui.actionSobre_el_programa, SIGNAL("triggered()"), self.onCmdAbout)
        self.connect(self.ui.actionConfiguracio, SIGNAL("triggered()"), self.onCmdConfiguracio)

        self.connect(self.ui.actionIniciar, SIGNAL("triggered()"), self.onCmdIniciar)
        self.connect(self.ui.actionAturar, QtCore.SIGNAL("triggered()"), self.onCmdPausar) 
        self.connect(self.ui.arbreAnalitzadors, SIGNAL("itemChanged(QTreeWidgetItem *, int)"), self.onSeleccioVariable)
        
        self.ui.actionIniciar.setEnabled(0)
        self.ui.actionAturar.setEnabled(0)
        self.ui.actionDesconnectar.setEnabled(0)

        self.ipServer = str(self.dConfig.settings.value("ipServidor").toString())
        self.portServer = int(self.dConfig.settings.value("portServidor").toString())
        self.dirExport = str(self.dConfig.settings.value("dirExport").toString())
 
    def defColsHist(self):
        varsAnalitza = self.cliThr.values[1]["vars"]
        defsAnalitza = self.cliThr.values[1]["defs"]
        if len(varsAnalitza)<1:
           return
                 
        titolsTaula = []
        for var in varsAnalitza:
            for i in range(len(varsAnalitza[var])):
                titolsTaula.append("%(t)s %(ind)d" % {"t": defsAnalitza[var]["descripcio"], "ind":i})

        self.ui.tableWidget.setColumnCount(len(titolsTaula))
        self.ui.tableWidget.setHorizontalHeaderLabels(titolsTaula)
        self.lineTable=0

    def pintaEstat(self, idEquip):
        status = self.cliThr.values[idEquip]["estatLector"]
        statusComm = self.cliThr.values[idEquip]["estatComm"]
        if status == STA_PAUSED:
           self.ui.actionIniciar.setEnabled(1)
           self.ui.actionAturar.setEnabled(0)
           self.ui.statusbar.showMessage("Servidor de lectures actiu i pausat ...")
        elif status == STA_STARTED:
           self.ui.actionIniciar.setEnabled(0)
           self.ui.actionAturar.setEnabled(1)
           self.ui.statusbar.showMessage("Servidor de lectures actiu i capturant dades ...")
        elif status == STA_STOPPED:
           self.ui.actionIniciar.setEnabled(1)
           self.ui.actionAturar.setEnabled(0)
           self.ui.statusbar.showMessage("Servidor de lectures aturat")
        
        if len(self.analitzador) > 0:
           if statusComm == STA_COMM:
              self.analitzador[idEquip].setForeground(0, QtGui.QBrush(QtGui.QColor("green")))
           else:
              self.analitzador[idEquip].setForeground(0, QtGui.QBrush(QtGui.QColor("red")))
           
    def pintaVars(self, idEquip):
        varAnalitza = self.cliThr.values[idEquip]["vars"]
        statusComm = self.cliThr.values[idEquip]["estatComm"]
        
        # Refresca els displays actius

        for varName, visor in self.visors.iteritems():            
            if statusComm == STA_COMM:
               visor.widget().setBlur(False)
            else:
               visor.widget().setBlur(True)
            visor.widget().actualitza(varAnalitza[varName])

        """
        # Refresca grafiques

        for varName, grafica in self.grafiques.iteritems():
            grafica.afegirValor(varAnalitza[varName])

        # Afegeix valor a la taula de historial
        
        if len(varAnalitza)>0:
           col=0
           self.ui.tableWidget.setRowCount(self.lineTable+1)

           for varName, values in varAnalitza.iteritems():
               for val in values:
                   self.ui.tableWidget.setItem(self.lineTable, col, QtGui.QTableWidgetItem(QString(str(val))))
                   col+=1

           self.lineTable+=1        
         """

    def onCmdPausar(self):
        self.cliThr.pausar()

    def onCmdConfiguracio(self):
        self.dConfig.cliThr = self.cliThr
        self.dConfig.carregar()

        if self.dConfig.exec_():
           self.dConfig.guardar()
           self.ipServidor=str(self.dConfig.settings.value("ipServidor").toString())

    def onCmdAbout(self):
        QtGui.QMessageBox.about(self,self.tr("Sobre el programa"), u"Visor 1.0\n\nClient per poder monitoritzar el servidor de lectures.\nTomeu Capó i Capó 2009 (C)")

    def onCmdExportarGrafiques(self):
        """
        for varName, finGraf in self.grafiques.iteritems():
            nomFitxer = "%s_%s%s%s.pdf" % (varName, time.localtime()[0], time.localtime()[1], time.localtime()[2])
            finGraf.grafica.guarda(os.path.join(self.dirExport, nomFitxer))
            
        QtGui.QMessageBox.information(self,self.tr("Info"),"Exportades grafiques a fitxers PDF a %s" % self.dirExport)
        """
        pass
    
    def onCmdConnectar(self):
        try:
          self.cliThr = clientThread(self.ui, (self.ipServer,self.portServer))
          self.connect(self.cliThr, SIGNAL("pintaVars(int)"), self.pintaVars)
          self.connect(self.cliThr, SIGNAL("pintaEstat(int)"), self.pintaEstat) 
          #self.connect(self.cliThr, SIGNAL("defColsHist()"), self.defColsHist)
          if not self.cliThr.connectar():
             QtGui.QMessageBox.warning(self, self.tr("Error clientThread"), u"No puc identificar els analitzadors")
             return
        except Exception, err:
          QtGui.QMessageBox.critical(self,self.tr("Error al connectar"), str(err))
          return

        self.ui.actionConnectar.setEnabled(0)
        self.ui.actionDesconnectar.setEnabled(1)
        self.dConfig.cliThr = self.cliThr

        arrel = QtGui.QTreeWidgetItem(["%s:%d" % (self.ipServer, self.portServer), ""])
        self.analitzador = {}
        for id, confs in self.cliThr.values.iteritems():
            descs = confs["defs"]    
            idEquip = confs["id"]
            equip = self.cliThr.conf["equips"][id]
            items = []
            
            self.analitzador[id] = QtGui.QTreeWidgetItem(arrel, [idEquip, ""])
            
            for p in equip["requests"]:
                item = QtGui.QTreeWidgetItem(self.analitzador[id], [p, (descs[p]["descripcio"] if p in descs.keys() else "")])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsUserCheckable) 
                item.setCheckState(2, Qt.Unchecked) 

            print self.cliThr.values[id]["estatComm"]
            self.analitzador[id].setForeground(0, QtGui.QBrush(QtGui.QColor("green")))
            self.ui.arbreAnalitzadors.expandItem(self.analitzador[id])
            
        self.ui.arbreAnalitzadors.insertTopLevelItem(0, arrel)
        self.ui.arbreAnalitzadors.expandItem(arrel)
        self.cliThr.start()

    def onCmdDesconnectar(self):
        if self.cliThr.isRunning():
           self.ui.statusbar.showMessage("Desconnectant ...", 1) 
           self.cliThr.seguir = False
           self.cliThr.terminate()
           self.ui.actionConnectar.setEnabled(1)
           self.ui.actionDesconnectar.setEnabled(0)
           self.buidaTot()

           del self.cliThr
           self.cliThr = None

    def onCmdIniciar(self):
        self.ui.actionIniciar.setEnabled(0)        
        self.cliThr.iniciar()
           
    def onSeleccioVariable(self, widgetItem, colum):
        if len(self.cliThr.values)<1:
           return

        nomVar = str(widgetItem.text(0))
        descVar = unicode(widgetItem.text(1))

        if colum != 2:
           return
        
        if widgetItem.checkState(colum) == Qt.Checked:
           print self.cliThr.values[1]['vars']
           finVisor = finestraVisor(descVar, self.cliThr.values[1]['vars'][nomVar])
           finVisor.setAttribute(Qt.WA_DeleteOnClose | Qt.WA_LayoutOnEntireRect)
           finVisor.setWindowFlags(Qt.SubWindow)
           self.ui.zonaDisplays.addSubWindow(finVisor)
           finVisor.show()
           self.visors[nomVar] = finVisor
        elif widgetItem.checkState(colum) == Qt.Unchecked:
              self.visors[nomVar].close()
              self.visors.pop(nomVar)

    def buidaTot(self):
        QtCore.qDebug("Buidant tot...")
        for varName, visor  in self.visors.iteritems():
            self.ui.zonaDisplays.removeSubWindow(visor)
            del visor
            
        self.visors = {}

        """
        for varName, finGraf in self.grafiques.iteritems():
            self.ui.zonaGrafiques.removeSubWindow(finGraf)
            del finGraf 
        """
        
        for e in range(0,self.ui.arbreAnalitzadors.topLevelItemCount()):
            children = self.ui.arbreAnalitzadors.topLevelItem(e).takeChildren()
            del children

        self.ui.arbreAnalitzadors.clear()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    v = Visor()
    v.show()
    sys.exit(app.exec_())
