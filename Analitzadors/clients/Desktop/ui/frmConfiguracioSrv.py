# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\frmConfiguracioSrv.ui'
#
# Created: Wed May 20 01:40:09 2015
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_configuracio(object):
    def setupUi(self, configuracio):
        configuracio.setObjectName("configuracio")
        configuracio.resize(1427, 830)
        self.verticalLayout = QtWidgets.QVBoxLayout(configuracio)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_38 = QtWidgets.QLabel(configuracio)
        self.label_38.setObjectName("label_38")
        self.horizontalLayout_16.addWidget(self.label_38)
        self.cAddrServidor = QtWidgets.QLineEdit(configuracio)
        self.cAddrServidor.setObjectName("cAddrServidor")
        self.horizontalLayout_16.addWidget(self.cAddrServidor)
        self.bProvar = QtWidgets.QPushButton(configuracio)
        self.bProvar.setObjectName("bProvar")
        self.horizontalLayout_16.addWidget(self.bProvar)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_16)
        self.splitter = QtWidgets.QSplitter(configuracio)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.treeDevices = QtWidgets.QTreeWidget(self.splitter)
        self.treeDevices.setObjectName("treeDevices")
        self.confDispositu = QtWidgets.QTabWidget(self.splitter)
        self.confDispositu.setObjectName("confDispositu")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_7 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_7.setObjectName("groupBox_7")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_7)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout_8 = QtWidgets.QFormLayout()
        self.formLayout_8.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_8.setObjectName("formLayout_8")
        self.label_17 = QtWidgets.QLabel(self.groupBox_7)
        self.label_17.setObjectName("label_17")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.label_18 = QtWidgets.QLabel(self.groupBox_7)
        self.label_18.setObjectName("label_18")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.cModel = QtWidgets.QLineEdit(self.groupBox_7)
        self.cModel.setObjectName("cModel")
        self.formLayout_8.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cModel)
        self.label_19 = QtWidgets.QLabel(self.groupBox_7)
        self.label_19.setObjectName("label_19")
        self.formLayout_8.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_19)
        self.cNumUnitat = QtWidgets.QLineEdit(self.groupBox_7)
        self.cNumUnitat.setObjectName("cNumUnitat")
        self.formLayout_8.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cNumUnitat)
        self.cFabricant_4 = QtWidgets.QLineEdit(self.groupBox_7)
        self.cFabricant_4.setObjectName("cFabricant_4")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cFabricant_4)
        self.horizontalLayout.addLayout(self.formLayout_8)
        self.formLayout_7 = QtWidgets.QFormLayout()
        self.formLayout_7.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_7.setObjectName("formLayout_7")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.cTempsLectura_4 = QtWidgets.QSpinBox(self.groupBox_7)
        self.cTempsLectura_4.setMinimum(10)
        self.cTempsLectura_4.setObjectName("cTempsLectura_4")
        self.horizontalLayout_14.addWidget(self.cTempsLectura_4)
        self.label_34 = QtWidgets.QLabel(self.groupBox_7)
        self.label_34.setObjectName("label_34")
        self.horizontalLayout_14.addWidget(self.label_34)
        self.formLayout_7.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_14)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_7.setItem(1, QtWidgets.QFormLayout.LabelRole, spacerItem1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.formLayout_7.setItem(1, QtWidgets.QFormLayout.FieldRole, spacerItem2)
        self.label_35 = QtWidgets.QLabel(self.groupBox_7)
        self.label_35.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_35.setObjectName("label_35")
        self.formLayout_7.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_35)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.cTempsGravacio_4 = QtWidgets.QSpinBox(self.groupBox_7)
        self.cTempsGravacio_4.setMinimum(1)
        self.cTempsGravacio_4.setObjectName("cTempsGravacio_4")
        self.horizontalLayout_15.addWidget(self.cTempsGravacio_4)
        self.label_36 = QtWidgets.QLabel(self.groupBox_7)
        self.label_36.setObjectName("label_36")
        self.horizontalLayout_15.addWidget(self.label_36)
        self.formLayout_7.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_15)
        self.label_37 = QtWidgets.QLabel(self.groupBox_7)
        self.label_37.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_37.setObjectName("label_37")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_37)
        self.horizontalLayout.addLayout(self.formLayout_7)
        self.verticalLayout_4.addWidget(self.groupBox_7)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldsStayAtSizeHint)
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.cDispSerie = QtWidgets.QLineEdit(self.groupBox_2)
        self.cDispSerie.setMaximumSize(QtCore.QSize(146, 16777215))
        self.cDispSerie.setObjectName("cDispSerie")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cDispSerie)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.cVelocitat = QtWidgets.QComboBox(self.groupBox_2)
        self.cVelocitat.setEditable(True)
        self.cVelocitat.setObjectName("cVelocitat")
        self.cVelocitat.addItem("")
        self.cVelocitat.addItem("")
        self.cVelocitat.addItem("")
        self.cVelocitat.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cVelocitat)
        self.label_15 = QtWidgets.QLabel(self.groupBox_2)
        self.label_15.setObjectName("label_15")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.cBits = QtWidgets.QSpinBox(self.groupBox_2)
        self.cBits.setMinimum(7)
        self.cBits.setMaximum(8)
        self.cBits.setObjectName("cBits")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cBits)
        self.label_16 = QtWidgets.QLabel(self.groupBox_2)
        self.label_16.setObjectName("label_16")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.cTimeout = QtWidgets.QSpinBox(self.groupBox_2)
        self.cTimeout.setObjectName("cTimeout")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cTimeout)
        self.horizontalLayout_3.addLayout(self.formLayout)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.confDispositu.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.taulaParametres = QtWidgets.QTableWidget(self.tab_2)
        self.taulaParametres.setMinimumSize(QtCore.QSize(606, 0))
        self.taulaParametres.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.taulaParametres.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.taulaParametres.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.taulaParametres.setWordWrap(False)
        self.taulaParametres.setObjectName("taulaParametres")
        self.taulaParametres.setColumnCount(7)
        self.taulaParametres.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.taulaParametres.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.taulaParametres.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.taulaParametres.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.taulaParametres.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.taulaParametres.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.taulaParametres.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.taulaParametres.setHorizontalHeaderItem(6, item)
        self.taulaParametres.verticalHeader().setVisible(False)
        self.horizontalLayout_2.addWidget(self.taulaParametres)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.confDispositu.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.splitter)
        self.buttonBox = QtWidgets.QDialogButtonBox(configuracio)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(configuracio)
        self.confDispositu.setCurrentIndex(0)
        self.buttonBox.accepted.connect(configuracio.accept)
        self.buttonBox.rejected.connect(configuracio.reject)
        QtCore.QMetaObject.connectSlotsByName(configuracio)

    def retranslateUi(self, configuracio):
        _translate = QtCore.QCoreApplication.translate
        configuracio.setWindowTitle(_translate("configuracio", "Configuració del servidor"))
        self.label_38.setText(_translate("configuracio", "Servidor de lectures"))
        self.bProvar.setText(_translate("configuracio", "Provar!"))
        self.treeDevices.headerItem().setText(0, _translate("configuracio", "Dispositius"))
        self.treeDevices.headerItem().setText(1, _translate("configuracio", "Habilitat"))
        self.groupBox_7.setTitle(_translate("configuracio", "Paràmetres Generals Analitzador"))
        self.label_17.setText(_translate("configuracio", "Fabricant:"))
        self.label_18.setText(_translate("configuracio", "Model:"))
        self.label_19.setText(_translate("configuracio", "Número d\'unitat:"))
        self.label_34.setText(_translate("configuracio", "Segons"))
        self.label_35.setText(_translate("configuracio", "Interval de gravació"))
        self.label_36.setText(_translate("configuracio", "Minuts"))
        self.label_37.setText(_translate("configuracio", "Temps de lectura"))
        self.groupBox_2.setTitle(_translate("configuracio", "Comunicacions"))
        self.label_5.setText(_translate("configuracio", "Port serie:"))
        self.label_6.setText(_translate("configuracio", "Velocitat:"))
        self.cVelocitat.setItemText(0, _translate("configuracio", "2400"))
        self.cVelocitat.setItemText(1, _translate("configuracio", "4800"))
        self.cVelocitat.setItemText(2, _translate("configuracio", "9600"))
        self.cVelocitat.setItemText(3, _translate("configuracio", "19200"))
        self.label_15.setText(_translate("configuracio", "Bits:"))
        self.label_16.setText(_translate("configuracio", "Timeout:"))
        self.confDispositu.setTabText(self.confDispositu.indexOf(self.tab), _translate("configuracio", "General"))
        self.taulaParametres.setSortingEnabled(True)
        item = self.taulaParametres.horizontalHeaderItem(0)
        item.setText(_translate("configuracio", "Cons?"))
        item = self.taulaParametres.horizontalHeaderItem(1)
        item.setText(_translate("configuracio", "Abreviació"))
        item = self.taulaParametres.horizontalHeaderItem(2)
        item.setText(_translate("configuracio", "Registre"))
        item = self.taulaParametres.horizontalHeaderItem(3)
        item.setText(_translate("configuracio", "Núm. Valors"))
        item = self.taulaParametres.horizontalHeaderItem(4)
        item.setText(_translate("configuracio", "Descripció"))
        item = self.taulaParametres.horizontalHeaderItem(5)
        item.setText(_translate("configuracio", "Escala"))
        item = self.taulaParametres.horizontalHeaderItem(6)
        item.setText(_translate("configuracio", "Valor màxim"))
        self.confDispositu.setTabText(self.confDispositu.indexOf(self.tab_2), _translate("configuracio", "Paràmetres"))

