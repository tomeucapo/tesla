#!/usr/bin/python

import matplotlib

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import *
from matplotlib.font_manager import FontProperties
from datetime import datetime
import pylab

from PyQt4 import QtCore, QtGui 

timeLine = []

class canvasGrafic(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=80):
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = self.fig.add_subplot(111)
        self.axes.hold(False)


        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


        self.axes.grid(True)
        self.axes.autoscale_view()

    def compute_initial_figure(self):
        pass

class graficaValors(canvasGrafic):
    def __init__(self, *args, **kwargs):
        canvasGrafic.__init__(self, *args, **kwargs) 
        self.vvars = []
        self.timeLine = []
        self.xTitol = ""
        self.yTitol = ""

    def guarda(self, nomFitxer):
        self.print_figure(nomFitxer, dpi=None, facecolor='w', edgecolor='w', orientation='portrait', format="pdf")    

    def paintFigure(self):
        self.axes.xaxis.set_minor_locator(SecondLocator(interval=15))
        self.axes.xaxis.set_major_locator(HourLocator())

        for v in self.vvars:
             self.axes.plot_date(self.timeLine, v, '-')

        self.axes.set_xlabel(self.xTitol)
        self.axes.set_ylabel(self.yTitol)
        self.axes.xaxis.set_major_formatter(DateFormatter("%H:%M"))

        for label in self.axes.get_xticklabels():
            label.set_fontsize(9)

        for label in self.axes.get_yticklabels():
            label.set_fontsize(9)

        self.axes.autoscale_view()
        self.axes.grid(True)

        self.fig.autofmt_xdate(rotation=90)

        self.draw()

class finestraGrafica(QtGui.QMdiSubWindow):
      def __init__(self, maxVars):
          QtGui.QMdiSubWindow.__init__(self)

          widgetGrafica = QtGui.QWidget()
           
          self.grafica = graficaValors(widgetGrafica, width=8, height=4, dpi=90)
          self.grafica.vvars=[False]*maxVars
          self.setWidget(widgetGrafica)
      
      def setTitols(self, xTitol, yTitol):
          self.grafica.xTitol = xTitol
          self.grafica.yTitol = yTitol 

      def afegirValor(self, valors):
          k=0
	  if len(self.grafica.vvars)>0:
   	     for v in valors:
                 if not self.grafica.vvars[k]:
	   	    self.grafica.vvars[k]=[v]
	         else:
                    self.grafica.vvars[k].append(v)
	         k=k+1

          self.grafica.timeLine.append(pylab.date2num(datetime.now()))
          self.grafica.paintFigure()

