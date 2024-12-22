# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_testedialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from Custom_Widgets.Theme import QPushButton
from Custom_Widgets.Theme import QLabel

class Ui_DialogTeste(object):
    def setupUi(self, DialogTeste):
        if not DialogTeste.objectName():
            DialogTeste.setObjectName(u"DialogTeste")
        DialogTeste.resize(255, 226)
        self.centralwidget = QWidget(DialogTeste)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(120, 60, 75, 23))
        DialogTeste.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(DialogTeste)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 255, 21))
        DialogTeste.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(DialogTeste)
        self.statusbar.setObjectName(u"statusbar")
        DialogTeste.setStatusBar(self.statusbar)

        self.retranslateUi(DialogTeste)

        QMetaObject.connectSlotsByName(DialogTeste)
    # setupUi

    def retranslateUi(self, DialogTeste):
        DialogTeste.setWindowTitle(QCoreApplication.translate("DialogTeste", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("DialogTeste", u"PushButton", None))
    # retranslateUi

