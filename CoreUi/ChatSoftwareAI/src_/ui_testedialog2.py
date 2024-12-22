# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_testedialog2.ui'
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

class Ui_Dialogs(object):
    def setupUi(self, Dialogs):
        if not Dialogs.objectName():
            Dialogs.setObjectName(u"Dialogs")
        Dialogs.resize(400, 300)
        self.pushButton = QPushButton(Dialogs)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(70, 40, 75, 23))

        self.retranslateUi(Dialogs)

        QMetaObject.connectSlotsByName(Dialogs)
    # setupUi

    def retranslateUi(self, Dialogs):
        Dialogs.setWindowTitle(QCoreApplication.translate("Dialogs", u"Dialog", None))
        self.pushButton.setText(QCoreApplication.translate("Dialogs", u"PushButton", None))
    # retranslateUi

