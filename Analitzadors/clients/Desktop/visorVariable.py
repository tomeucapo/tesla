#!/usr/bin/python

from PyQt4 import QtCore, QtGui

class finestraVisor(QtGui.QMdiSubWindow):
      def __init__(self, descVar, valorsVar):
          QtGui.QMdiSubWindow.__init__(self)
          self.setWindowTitle(descVar)          
          self.setWidget(visorVariable(descVar, QtGui.QBoxLayout.TopToBottom, valorsVar))
          
class visorVariable(QtGui.QWidget):
      def __init__(self, titol, dir, valorsDef = []):
          QtGui.QWidget.__init__(self)

          self.valors = valorsDef
          self.titol = titol
          self.displays = []

          self.layout = QtGui.QBoxLayout(dir, self)

          fontTitol = QtGui.QFont()
          fontTitol.setFamily("Arial")
          fontTitol.setPointSize(16)

          titolObj = QtGui.QLabel(titol)
          titolObj.setFont(fontTitol)
          titolObj.setAlignment(QtCore.Qt.AlignCenter)

          sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
          sizePolicy.setHorizontalStretch(0)
          sizePolicy.setVerticalStretch(0)
          sizePolicy.setHeightForWidth(titolObj.sizePolicy().hasHeightForWidth())
          titolObj.setSizePolicy(sizePolicy)

          self.layout.addWidget(titolObj)

          for val in self.valors:
              self.__afegeixDisplay__(val)                   

      def __afegeixDisplay__(self, valDef):
          lcd = QtGui.QLCDNumber()
          lcd.setNumDigits(9)
          lcd.setSegmentStyle(QtGui.QLCDNumber.Filled)
          lcd.display(valDef)

          self.displays.append(lcd)
          self.layout.addWidget(lcd)

      def setBlur(self, blur):
          efecteColor = QtGui.QGraphicsColorizeEffect()
          efecteColor.setColor(QtGui.QColor("black"))
          self.setGraphicsEffect(efecteColor)

          if blur:
             efecte = QtGui.QGraphicsBlurEffect()
             self.setGraphicsEffect(efecte)
            
      def actualitza(self, nousValors):
          i=0
          self.valors = nousValors
          for disp in self.displays:
              disp.display(self.valors[i])
              i=i+1
