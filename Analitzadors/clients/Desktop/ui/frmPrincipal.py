# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\frmPrincipal.ui'
#
# Created: Wed May 20 01:40:26 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_finestraPrincipal(object):
    def setupUi(self, finestraPrincipal):
        finestraPrincipal.setObjectName("finestraPrincipal")
        finestraPrincipal.resize(1161, 812)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(finestraPrincipal.sizePolicy().hasHeightForWidth())
        finestraPrincipal.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(finestraPrincipal)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.arbreAnalitzadors = QtWidgets.QTreeWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arbreAnalitzadors.sizePolicy().hasHeightForWidth())
        self.arbreAnalitzadors.setSizePolicy(sizePolicy)
        self.arbreAnalitzadors.setMinimumSize(QtCore.QSize(256, 0))
        self.arbreAnalitzadors.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.arbreAnalitzadors.setAutoExpandDelay(1)
        self.arbreAnalitzadors.setUniformRowHeights(True)
        self.arbreAnalitzadors.setObjectName("arbreAnalitzadors")
        self.splitter_2 = QtWidgets.QSplitter(self.splitter)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.tabWidget = QtWidgets.QTabWidget(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.zonaDisplays = QtWidgets.QMdiArea(self.tab)
        self.zonaDisplays.setObjectName("zonaDisplays")
        self.verticalLayout_7.addWidget(self.zonaDisplays)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout_4.addWidget(self.tableWidget)
        self.tabWidget.addTab(self.tab_2, "")
        self.horizontalLayout.addWidget(self.splitter)
        finestraPrincipal.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(finestraPrincipal)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1161, 21))
        self.menubar.setObjectName("menubar")
        self.menu_Fitxer = QtWidgets.QMenu(self.menubar)
        self.menu_Fitxer.setObjectName("menu_Fitxer")
        self.menuAjuda = QtWidgets.QMenu(self.menubar)
        self.menuAjuda.setObjectName("menuAjuda")
        self.menuLector = QtWidgets.QMenu(self.menubar)
        self.menuLector.setObjectName("menuLector")
        finestraPrincipal.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(finestraPrincipal)
        self.statusbar.setObjectName("statusbar")
        finestraPrincipal.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(finestraPrincipal)
        self.toolBar.setIconSize(QtCore.QSize(32, 32))
        self.toolBar.setObjectName("toolBar")
        finestraPrincipal.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSobre_el_programa = QtWidgets.QAction(finestraPrincipal)
        self.actionSobre_el_programa.setObjectName("actionSobre_el_programa")
        self.actionConfiguracio = QtWidgets.QAction(finestraPrincipal)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icones/Icones/preferencies.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConfiguracio.setIcon(icon)
        self.actionConfiguracio.setObjectName("actionConfiguracio")
        self.actionSortir = QtWidgets.QAction(finestraPrincipal)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icones/Icones/sortir.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSortir.setIcon(icon1)
        self.actionSortir.setObjectName("actionSortir")
        self.actionIniciar = QtWidgets.QAction(finestraPrincipal)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icones/Icones/iniciarCaptura.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionIniciar.setIcon(icon2)
        self.actionIniciar.setObjectName("actionIniciar")
        self.actionAturar = QtWidgets.QAction(finestraPrincipal)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icones/Icones/aturarCaptura.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAturar.setIcon(icon3)
        self.actionAturar.setObjectName("actionAturar")
        self.actionIniciar_servei = QtWidgets.QAction(finestraPrincipal)
        self.actionIniciar_servei.setObjectName("actionIniciar_servei")
        self.actionConnectar = QtWidgets.QAction(finestraPrincipal)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icones/Icones/connectar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConnectar.setIcon(icon4)
        self.actionConnectar.setObjectName("actionConnectar")
        self.actionDesconnectar = QtWidgets.QAction(finestraPrincipal)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icones/Icones/desconnectar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDesconnectar.setIcon(icon5)
        self.actionDesconnectar.setObjectName("actionDesconnectar")
        self.actionExportaGrafiques = QtWidgets.QAction(finestraPrincipal)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icones/Icones/guardar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExportaGrafiques.setIcon(icon6)
        self.actionExportaGrafiques.setObjectName("actionExportaGrafiques")
        self.actionExportaHistoric = QtWidgets.QAction(finestraPrincipal)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icones/Icones/llibreta.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExportaHistoric.setIcon(icon7)
        self.actionExportaHistoric.setObjectName("actionExportaHistoric")
        self.actionBuidaLectures = QtWidgets.QAction(finestraPrincipal)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icones/Icones/buidar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBuidaLectures.setIcon(icon8)
        self.actionBuidaLectures.setObjectName("actionBuidaLectures")
        self.actionFor_ar_lectura = QtWidgets.QAction(finestraPrincipal)
        self.actionFor_ar_lectura.setObjectName("actionFor_ar_lectura")
        self.menu_Fitxer.addAction(self.actionExportaHistoric)
        self.menu_Fitxer.addAction(self.actionExportaGrafiques)
        self.menu_Fitxer.addAction(self.actionConfiguracio)
        self.menu_Fitxer.addSeparator()
        self.menu_Fitxer.addAction(self.actionSortir)
        self.menuAjuda.addAction(self.actionSobre_el_programa)
        self.menuLector.addAction(self.actionConnectar)
        self.menuLector.addAction(self.actionDesconnectar)
        self.menuLector.addSeparator()
        self.menuLector.addAction(self.actionAturar)
        self.menuLector.addAction(self.actionIniciar)
        self.menuLector.addAction(self.actionFor_ar_lectura)
        self.menuLector.addSeparator()
        self.menuLector.addAction(self.actionBuidaLectures)
        self.menuLector.addSeparator()
        self.menubar.addAction(self.menu_Fitxer.menuAction())
        self.menubar.addAction(self.menuLector.menuAction())
        self.menubar.addAction(self.menuAjuda.menuAction())
        self.toolBar.addAction(self.actionSortir)
        self.toolBar.addAction(self.actionConfiguracio)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionConnectar)
        self.toolBar.addAction(self.actionDesconnectar)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionIniciar)
        self.toolBar.addAction(self.actionAturar)

        self.retranslateUi(finestraPrincipal)
        self.tabWidget.setCurrentIndex(0)
        self.actionSortir.triggered.connect(finestraPrincipal.close)
        QtCore.QMetaObject.connectSlotsByName(finestraPrincipal)

    def retranslateUi(self, finestraPrincipal):
        _translate = QtCore.QCoreApplication.translate
        finestraPrincipal.setWindowTitle(_translate("finestraPrincipal", "VisorLector 2.0"))
        self.arbreAnalitzadors.setSortingEnabled(True)
        self.arbreAnalitzadors.headerItem().setText(0, _translate("finestraPrincipal", "Analitzador"))
        self.arbreAnalitzadors.headerItem().setText(1, _translate("finestraPrincipal", "Descripció"))
        self.arbreAnalitzadors.headerItem().setText(2, _translate("finestraPrincipal", "Mostrar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("finestraPrincipal", "Valors instantànis"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("finestraPrincipal", "Històric"))
        self.menu_Fitxer.setTitle(_translate("finestraPrincipal", "&Fitxer"))
        self.menuAjuda.setTitle(_translate("finestraPrincipal", "Ajuda"))
        self.menuLector.setTitle(_translate("finestraPrincipal", "Lector"))
        self.toolBar.setWindowTitle(_translate("finestraPrincipal", "toolBar"))
        self.actionSobre_el_programa.setText(_translate("finestraPrincipal", "Sobre el programa..."))
        self.actionConfiguracio.setText(_translate("finestraPrincipal", "Configuració"))
        self.actionSortir.setText(_translate("finestraPrincipal", "Sortir"))
        self.actionIniciar.setText(_translate("finestraPrincipal", "Iniciar captura"))
        self.actionAturar.setText(_translate("finestraPrincipal", "&Pausar captura"))
        self.actionIniciar_servei.setText(_translate("finestraPrincipal", "Iniciar servei"))
        self.actionConnectar.setText(_translate("finestraPrincipal", "Connectar"))
        self.actionDesconnectar.setText(_translate("finestraPrincipal", "Desconnectar"))
        self.actionExportaGrafiques.setText(_translate("finestraPrincipal", "Exporta &Gràfiques"))
        self.actionExportaHistoric.setText(_translate("finestraPrincipal", "Exporta H&istòric Local"))
        self.actionBuidaLectures.setText(_translate("finestraPrincipal", "Buida lectures locals"))
        self.actionFor_ar_lectura.setText(_translate("finestraPrincipal", "Forçar lectura"))

import recursos_rc
