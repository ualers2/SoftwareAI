# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_interface.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from Custom_Widgets.QCustomQStackedWidget import QCustomQStackedWidget
from Custom_Widgets.QCustomSlideMenu import QCustomSlideMenu
from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
from Custom_Widgets.Theme import QPushButton
from Custom_Widgets.Theme import QLabel

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(716, 457)
        MainWindow.setStyleSheet(u"background:white")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.close_window_button = QPushButton(self.centralwidget)
        self.close_window_button.setObjectName(u"close_window_button")
        icon = QIcon()
        icon.addFile(u":/feather/icons/feather/window_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.close_window_button.setIcon(icon)

        self.gridLayout_2.addWidget(self.close_window_button, 0, 3, 1, 1)

        self.restore_window_button = QPushButton(self.centralwidget)
        self.restore_window_button.setObjectName(u"restore_window_button")
        icon1 = QIcon()
        icon1.addFile(u":/feather/icons/feather/maximize-2.png", QSize(), QIcon.Normal, QIcon.Off)
        self.restore_window_button.setIcon(icon1)

        self.gridLayout_2.addWidget(self.restore_window_button, 0, 2, 1, 1)

        self.minimize_window_button = QPushButton(self.centralwidget)
        self.minimize_window_button.setObjectName(u"minimize_window_button")
        icon2 = QIcon()
        icon2.addFile(u":/feather/icons/feather/window_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimize_window_button.setIcon(icon2)

        self.gridLayout_2.addWidget(self.minimize_window_button, 0, 1, 1, 1)

        self.open_close_side_bar_btn = QCustomQPushButton(self.centralwidget)
        self.open_close_side_bar_btn.setObjectName(u"open_close_side_bar_btn")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_close_side_bar_btn.sizePolicy().hasHeightForWidth())
        self.open_close_side_bar_btn.setSizePolicy(sizePolicy)
        self.open_close_side_bar_btn.setMinimumSize(QSize(35, 0))
        self.open_close_side_bar_btn.setMaximumSize(QSize(35, 16777215))
        icon3 = QIcon()
        icon3.addFile(u":/feather/icons/feather/chevrons-left.png", QSize(), QIcon.Normal, QIcon.Off)
        self.open_close_side_bar_btn.setIcon(icon3)

        self.gridLayout_2.addWidget(self.open_close_side_bar_btn, 0, 0, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 0, 2, 1, 1)

        self.menu_widget = QCustomSlideMenu(self.centralwidget)
        self.menu_widget.setObjectName(u"menu_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.menu_widget.sizePolicy().hasHeightForWidth())
        self.menu_widget.setSizePolicy(sizePolicy1)
        self.menu_widget.setMinimumSize(QSize(42, 0))
        self.menu_widget.setMaximumSize(QSize(42, 16777215))
        self.verticalLayout = QVBoxLayout(self.menu_widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.page1ss = QPushButton(self.menu_widget)
        self.page1ss.setObjectName(u"page1ss")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.page1ss.sizePolicy().hasHeightForWidth())
        self.page1ss.setSizePolicy(sizePolicy2)
        icon4 = QIcon()
        icon4.addFile(u":/material_design/icons/material_design/chat.png", QSize(), QIcon.Normal, QIcon.Off)
        self.page1ss.setIcon(icon4)

        self.verticalLayout.addWidget(self.page1ss)

        self.page2ssss = QPushButton(self.menu_widget)
        self.page2ssss.setObjectName(u"page2ssss")
        sizePolicy2.setHeightForWidth(self.page2ssss.sizePolicy().hasHeightForWidth())
        self.page2ssss.setSizePolicy(sizePolicy2)
        icon5 = QIcon()
        icon5.addFile(u":/feather/icons/feather/edit-2.png", QSize(), QIcon.Normal, QIcon.Off)
        self.page2ssss.setIcon(icon5)

        self.verticalLayout.addWidget(self.page2ssss)

        self.pushButton = QPushButton(self.menu_widget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.verticalSpacer = QSpacerItem(20, 300, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addWidget(self.menu_widget, 2, 0, 1, 1)

        self.myStackedWidget = QCustomQStackedWidget(self.centralwidget)
        self.myStackedWidget.setObjectName(u"myStackedWidget")
        sizePolicy1.setHeightForWidth(self.myStackedWidget.sizePolicy().hasHeightForWidth())
        self.myStackedWidget.setSizePolicy(sizePolicy1)
        self.myStackedWidget.setMinimumSize(QSize(650, 400))
        self.myStackedWidget.setStyleSheet(u"\n"
"QWidget {\n"
"    background-color: white;\n"
"}\n"
"")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.myStackedWidget.addWidget(self.page_2)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_3 = QGridLayout(self.page)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.html_chat = QTextEdit(self.page)
        self.html_chat.setObjectName(u"html_chat")
        self.html_chat.setMinimumSize(QSize(0, 547))
        self.html_chat.setMaximumSize(QSize(16777215, 16777215))
        self.html_chat.setStyleSheet(u"            QTextEdit {\n"
"          \n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 10px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto preto */\n"
"                font-family: Arial;\n"
"                font-size: 14px;\n"
"            }")

        self.gridLayout_3.addWidget(self.html_chat, 0, 0, 1, 4)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 1, 1, 1, 1)

        self.atach_file = QCustomQPushButton(self.page)
        self.atach_file.setObjectName(u"atach_file")
        self.atach_file.setStyleSheet(u"            QPushButton {\n"
"                background-color: #F7F7F7;\n"
"                border: 1px solid #E0E0E0;\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 13px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }")
        icon6 = QIcon()
        icon6.addFile(u":/font_awesome_solid/icons/font_awesome/solid/file-arrow-down.png", QSize(), QIcon.Normal, QIcon.Off)
        self.atach_file.setIcon(icon6)
        self.atach_file.setIconSize(QSize(22, 26))

        self.gridLayout_3.addWidget(self.atach_file, 2, 0, 1, 1)

        self.mensage_input = QTextEdit(self.page)
        self.mensage_input.setObjectName(u"mensage_input")
        self.mensage_input.setMinimumSize(QSize(0, 50))
        self.mensage_input.setMaximumSize(QSize(16777215, 16777215))
        self.mensage_input.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 10px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_3.addWidget(self.mensage_input, 2, 1, 1, 1)

        self.send_mensage = QCustomQPushButton(self.page)
        self.send_mensage.setObjectName(u"send_mensage")
        self.send_mensage.setStyleSheet(u"            QPushButton {\n"
"                background-color: #F7F7F7;\n"
"                border: 1px solid #E0E0E0;\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }")
        icon7 = QIcon()
        icon7.addFile(u":/feather/icons/feather/send.png", QSize(), QIcon.Normal, QIcon.Off)
        self.send_mensage.setIcon(icon7)
        self.send_mensage.setIconSize(QSize(27, 27))

        self.gridLayout_3.addWidget(self.send_mensage, 2, 2, 1, 1)

        self.pushButton_6 = QCustomQPushButton(self.page)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setStyleSheet(u"            QPushButton {\n"
"                background-color: #F7F7F7;\n"
"                border: 1px solid #E0E0E0;\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }")
        icon8 = QIcon()
        icon8.addFile(u":/feather/icons/feather/mic.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_6.setIcon(icon8)
        self.pushButton_6.setIconSize(QSize(27, 27))

        self.gridLayout_3.addWidget(self.pushButton_6, 2, 3, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.gridLayout_3.addItem(self.verticalSpacer_4, 3, 1, 1, 1)

        self.myStackedWidget.addWidget(self.page)

        self.gridLayout.addWidget(self.myStackedWidget, 2, 1, 1, 2)

        self.horizontalSpacer = QSpacerItem(580, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.myStackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.close_window_button.setText("")
        self.restore_window_button.setText("")
        self.minimize_window_button.setText("")
        self.open_close_side_bar_btn.setText("")
        self.page1ss.setText("")
        self.page2ssss.setText("")
        self.pushButton.setText("")
        self.atach_file.setText("")
        self.mensage_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Mensagem...", None))
        self.send_mensage.setText("")
        self.pushButton_6.setText("")
    # retranslateUi

