#!/usr/bin/python

from PyQt5 import QtCore, QtGui, QtWidgets

class finestraVisor(QtWidgets.QMdiSubWindow):
      def __init__(self, descVar, valorsVar):
          QtWidgets.QMdiSubWindow.__init__(self)
          self.setWindowTitle(descVar)          
          self.setWidget(visorVariable(descVar, QtWidgets.QBoxLayout.TopToBottom, valorsVar))
      
      def closeEvent(self, QCloseEvent):
          print "Tancam visor"

class visorVariable(QtWidgets.QWidget):
      def __init__(self, titol, dir, valorsDef = []):
          QtWidgets.QWidget.__init__(self)

          self.valors = valorsDef
          self.titol = titol
          self.displays = []

          self.layout = QtWidgets.QBoxLayout(dir, self)

          fontTitol = QtGui.QFont()
          fontTitol.setFamily("Arial")
          fontTitol.setPointSize(16)

          titolObj = QtWidgets.QLabel(titol)
          titolObj.setFont(fontTitol)
          titolObj.setAlignment(QtCore.Qt.AlignCenter)

          sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
          sizePolicy.setHorizontalStretch(0)
          sizePolicy.setVerticalStretch(0)
          sizePolicy.setHeightForWidth(titolObj.sizePolicy().hasHeightForWidth())
          titolObj.setSizePolicy(sizePolicy)

          self.layout.addWidget(titolObj)

          for val in self.valors:
              self.__afegeixDisplay__(val)                   

      def __afegeixDisplay__(self, valDef):
          lcd = QtWidgets.QLCDNumber()
          lcd.setNumDigits(9)
          lcd.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
          lcd.display(valDef)

          self.displays.append(lcd)
          self.layout.addWidget(lcd)

      def setBlur(self, blur):
          efecteColor = QtWidgets.QGraphicsColorizeEffect()
          efecteColor.setColor(QtGui.QColor("black"))
          self.setGraphicsEffect(efecteColor)

          if blur:
             efecte = QtWidgets.QGraphicsBlurEffect()
             self.setGraphicsEffect(efecte)
            
      def actualitza(self, nousValors):
          i=0
          self.valors = nousValors
          for disp in self.displays:
              disp.display(self.valors[i])
              i=i+1
