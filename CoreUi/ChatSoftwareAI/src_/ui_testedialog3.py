# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_testedialog3.ui'
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

class Ui_Formtesete(object):
    def setupUi(self, Formtesete):
        if not Formtesete.objectName():
            Formtesete.setObjectName(u"Formtesete")
        Formtesete.resize(400, 300)
        self.pushButton = QPushButton(Formtesete)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(150, 120, 75, 23))

        self.retranslateUi(Formtesete)

        QMetaObject.connectSlotsByName(Formtesete)
    # setupUi

    def retranslateUi(self, Formtesete):
        Formtesete.setWindowTitle(QCoreApplication.translate("Formtesete", u"Form", None))
        self.pushButton.setText(QCoreApplication.translate("Formtesete", u"PushButton", None))
    # retranslateUi

