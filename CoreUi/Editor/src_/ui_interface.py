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
from Custom_Widgets.QCustomCheckBox import QCustomCheckBox
from Custom_Widgets.Theme import QPushButton
from Custom_Widgets.Theme import QLabel

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(824, 728)
        MainWindow.setMinimumSize(QSize(781, 502))
        MainWindow.setStyleSheet(u"background:white")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.close_window_button = QPushButton(self.centralwidget)
        self.close_window_button.setObjectName(u"close_window_button")
        self.close_window_button.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon = QIcon()
        icon.addFile(u":/feather/icons/feather/window_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.close_window_button.setIcon(icon)
        self.close_window_button.setIconSize(QSize(21, 24))

        self.gridLayout_2.addWidget(self.close_window_button, 0, 3, 1, 1)

        self.restore_window_button = QPushButton(self.centralwidget)
        self.restore_window_button.setObjectName(u"restore_window_button")
        self.restore_window_button.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon1 = QIcon()
        icon1.addFile(u":/feather/icons/feather/maximize-2.png", QSize(), QIcon.Normal, QIcon.Off)
        self.restore_window_button.setIcon(icon1)
        self.restore_window_button.setIconSize(QSize(21, 24))

        self.gridLayout_2.addWidget(self.restore_window_button, 0, 2, 1, 1)

        self.minimize_window_button = QPushButton(self.centralwidget)
        self.minimize_window_button.setObjectName(u"minimize_window_button")
        self.minimize_window_button.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon2 = QIcon()
        icon2.addFile(u":/feather/icons/feather/window_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimize_window_button.setIcon(icon2)
        self.minimize_window_button.setIconSize(QSize(21, 24))

        self.gridLayout_2.addWidget(self.minimize_window_button, 0, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_2, 0, 2, 1, 1)

        self.open_close_side_bar_btn = QCustomQPushButton(self.centralwidget)
        self.open_close_side_bar_btn.setObjectName(u"open_close_side_bar_btn")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_close_side_bar_btn.sizePolicy().hasHeightForWidth())
        self.open_close_side_bar_btn.setSizePolicy(sizePolicy)
        self.open_close_side_bar_btn.setMinimumSize(QSize(35, 0))
        self.open_close_side_bar_btn.setMaximumSize(QSize(35, 16777215))
        self.open_close_side_bar_btn.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon3 = QIcon()
        icon3.addFile(u":/material_design/icons/material_design/arrow_back.png", QSize(), QIcon.Normal, QIcon.Off)
        self.open_close_side_bar_btn.setIcon(icon3)
        self.open_close_side_bar_btn.setIconSize(QSize(29, 29))

        self.gridLayout.addWidget(self.open_close_side_bar_btn, 1, 0, 1, 1)

        self.horizontalSpacer = QSpacerItem(580, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 2)

        self.menu_widget = QCustomSlideMenu(self.centralwidget)
        self.menu_widget.setObjectName(u"menu_widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.menu_widget.sizePolicy().hasHeightForWidth())
        self.menu_widget.setSizePolicy(sizePolicy1)
        self.menu_widget.setMinimumSize(QSize(39, 0))
        self.menu_widget.setMaximumSize(QSize(39, 16777215))
        self.verticalLayout = QVBoxLayout(self.menu_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.CreateAgents_menu = QPushButton(self.menu_widget)
        self.CreateAgents_menu.setObjectName(u"CreateAgents_menu")
        self.CreateAgents_menu.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon4 = QIcon()
        icon4.addFile(u":/material_design/icons/material_design/people_alt.png", QSize(), QIcon.Normal, QIcon.Off)
        self.CreateAgents_menu.setIcon(icon4)
        self.CreateAgents_menu.setIconSize(QSize(24, 26))

        self.verticalLayout.addWidget(self.CreateAgents_menu)

        self.ViewCodeAgent = QPushButton(self.menu_widget)
        self.ViewCodeAgent.setObjectName(u"ViewCodeAgent")
        self.ViewCodeAgent.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon5 = QIcon()
        icon5.addFile(u":/font_awesome_solid/icons/font_awesome/solid/code.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ViewCodeAgent.setIcon(icon5)
        self.ViewCodeAgent.setIconSize(QSize(24, 26))

        self.verticalLayout.addWidget(self.ViewCodeAgent)

        self.Editor_instructions = QPushButton(self.menu_widget)
        self.Editor_instructions.setObjectName(u"Editor_instructions")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.Editor_instructions.sizePolicy().hasHeightForWidth())
        self.Editor_instructions.setSizePolicy(sizePolicy2)
        self.Editor_instructions.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon6 = QIcon()
        icon6.addFile(u":/material_design/icons/material_design/integration_instructions.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Editor_instructions.setIcon(icon6)
        self.Editor_instructions.setIconSize(QSize(24, 27))

        self.verticalLayout.addWidget(self.Editor_instructions)

        self.Editoragentkeysongithub = QPushButton(self.menu_widget)
        self.Editoragentkeysongithub.setObjectName(u"Editoragentkeysongithub")
        self.Editoragentkeysongithub.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon7 = QIcon()
        icon7.addFile(u":/font_awesome_solid/icons/font_awesome/solid/key.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Editoragentkeysongithub.setIcon(icon7)
        self.Editoragentkeysongithub.setIconSize(QSize(24, 27))

        self.verticalLayout.addWidget(self.Editoragentkeysongithub)

        self.DestilationView = QPushButton(self.menu_widget)
        self.DestilationView.setObjectName(u"DestilationView")
        self.DestilationView.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon8 = QIcon()
        icon8.addFile(u":/font_awesome_solid/icons/font_awesome/solid/database.png", QSize(), QIcon.Normal, QIcon.Off)
        self.DestilationView.setIcon(icon8)
        self.DestilationView.setIconSize(QSize(29, 29))

        self.verticalLayout.addWidget(self.DestilationView)

        self.verticalSpacer = QSpacerItem(20, 300, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.gridLayout.addWidget(self.menu_widget, 2, 0, 1, 1)

        self.myStackedWidget = QCustomQStackedWidget(self.centralwidget)
        self.myStackedWidget.setObjectName(u"myStackedWidget")
        sizePolicy3 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.myStackedWidget.sizePolicy().hasHeightForWidth())
        self.myStackedWidget.setSizePolicy(sizePolicy3)
        self.myStackedWidget.setMinimumSize(QSize(650, 400))
        self.myStackedWidget.setStyleSheet(u"\n"
"QWidget {\n"
"    background-color: white;\n"
"}\n"
"")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_4 = QGridLayout(self.page_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_23 = QGridLayout()
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.label = QLabel(self.page_2)
        self.label.setObjectName(u"label")
        sizePolicy4 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy4)

        self.gridLayout_23.addWidget(self.label, 0, 0, 1, 1)

        self.SoftwareAIAgent_Benchmark = QComboBox(self.page_2)
        self.SoftwareAIAgent_Benchmark.setObjectName(u"SoftwareAIAgent_Benchmark")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.SoftwareAIAgent_Benchmark.sizePolicy().hasHeightForWidth())
        self.SoftwareAIAgent_Benchmark.setSizePolicy(sizePolicy5)
        self.SoftwareAIAgent_Benchmark.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 13px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 16px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_23.addWidget(self.SoftwareAIAgent_Benchmark, 0, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_23, 0, 0, 1, 1)

        self.gridLayout_33 = QGridLayout()
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.gridLayout_33.setContentsMargins(8, 0, 7, -1)
        self.label_19 = QLabel(self.page_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(600, 0))
        self.label_19.setMaximumSize(QSize(600, 16777215))

        self.gridLayout_33.addWidget(self.label_19, 0, 0, 1, 1)

        self.CleanThread_Benchmark = QCustomQPushButton(self.page_2)
        self.CleanThread_Benchmark.setObjectName(u"CleanThread_Benchmark")
        sizePolicy.setHeightForWidth(self.CleanThread_Benchmark.sizePolicy().hasHeightForWidth())
        self.CleanThread_Benchmark.setSizePolicy(sizePolicy)
        self.CleanThread_Benchmark.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"\n"
"")
        icon9 = QIcon()
        icon9.addFile(u":/material_design/icons/material_design/cleaning_services.png", QSize(), QIcon.Normal, QIcon.Off)
        self.CleanThread_Benchmark.setIcon(icon9)
        self.CleanThread_Benchmark.setIconSize(QSize(19, 18))

        self.gridLayout_33.addWidget(self.CleanThread_Benchmark, 0, 2, 1, 1)

        self.label_20 = QLabel(self.page_2)
        self.label_20.setObjectName(u"label_20")
        sizePolicy4.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy4)

        self.gridLayout_33.addWidget(self.label_20, 0, 1, 1, 1)

        self.AtachFilesToThread_Benchmark = QCustomQPushButton(self.page_2)
        self.AtachFilesToThread_Benchmark.setObjectName(u"AtachFilesToThread_Benchmark")
        sizePolicy.setHeightForWidth(self.AtachFilesToThread_Benchmark.sizePolicy().hasHeightForWidth())
        self.AtachFilesToThread_Benchmark.setSizePolicy(sizePolicy)
        self.AtachFilesToThread_Benchmark.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"\n"
"")
        self.AtachFilesToThread_Benchmark.setIcon(icon8)
        self.AtachFilesToThread_Benchmark.setIconSize(QSize(19, 18))

        self.gridLayout_33.addWidget(self.AtachFilesToThread_Benchmark, 0, 3, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_33, 1, 0, 1, 1)

        self.html_chat__Benchmark = QTextEdit(self.page_2)
        self.html_chat__Benchmark.setObjectName(u"html_chat__Benchmark")
        self.html_chat__Benchmark.setMinimumSize(QSize(0, 246))
        self.html_chat__Benchmark.setMaximumSize(QSize(16777215, 16777215))
        self.html_chat__Benchmark.setStyleSheet(u"            QTextEdit {\n"
"          \n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 10px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto preto */\n"
"                font-family: Arial;\n"
"                font-size: 14px;\n"
"            }")

        self.gridLayout_4.addWidget(self.html_chat__Benchmark, 2, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 154, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_4.addItem(self.verticalSpacer_3, 3, 0, 1, 1)

        self.gridLayout_22 = QGridLayout()
        self.gridLayout_22.setSpacing(1)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.gridLayout_22.setContentsMargins(2, 0, 7, 18)
        self.mensage_input__Benchmark = QTextEdit(self.page_2)
        self.mensage_input__Benchmark.setObjectName(u"mensage_input__Benchmark")
        sizePolicy6 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.mensage_input__Benchmark.sizePolicy().hasHeightForWidth())
        self.mensage_input__Benchmark.setSizePolicy(sizePolicy6)
        self.mensage_input__Benchmark.setMinimumSize(QSize(689, 124))
        self.mensage_input__Benchmark.setMaximumSize(QSize(607, 124))
        self.mensage_input__Benchmark.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 10px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_22.addWidget(self.mensage_input__Benchmark, 0, 4, 1, 1)

        self.Atachfiles_Benchmark = QCustomQPushButton(self.page_2)
        self.Atachfiles_Benchmark.setObjectName(u"Atachfiles_Benchmark")
        sizePolicy.setHeightForWidth(self.Atachfiles_Benchmark.sizePolicy().hasHeightForWidth())
        self.Atachfiles_Benchmark.setSizePolicy(sizePolicy)
        self.Atachfiles_Benchmark.setStyleSheet(u"            QPushButton {\n"
"                background-color: #F7F7F7;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"\n"
"")
        icon10 = QIcon()
        icon10.addFile(u":/material_design/icons/material_design/attach_file.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Atachfiles_Benchmark.setIcon(icon10)
        self.Atachfiles_Benchmark.setIconSize(QSize(27, 34))

        self.gridLayout_22.addWidget(self.Atachfiles_Benchmark, 2, 7, 1, 1)

        self.pushButton_3 = QPushButton(self.page_2)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setStyleSheet(u"            QPushButton {\n"
"                background-color: #F7F7F7;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"\n"
"")
        icon11 = QIcon()
        icon11.addFile(u":/material_design/icons/material_design/image.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_3.setIcon(icon11)
        self.pushButton_3.setIconSize(QSize(27, 40))

        self.gridLayout_22.addWidget(self.pushButton_3, 4, 7, 1, 1)

        self.send_mensage__Benchmark = QCustomQPushButton(self.page_2)
        self.send_mensage__Benchmark.setObjectName(u"send_mensage__Benchmark")
        sizePolicy.setHeightForWidth(self.send_mensage__Benchmark.sizePolicy().hasHeightForWidth())
        self.send_mensage__Benchmark.setSizePolicy(sizePolicy)
        self.send_mensage__Benchmark.setStyleSheet(u"            QPushButton {\n"
"                background-color: #F7F7F7;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"\n"
"")
        icon12 = QIcon()
        icon12.addFile(u":/material_design/icons/material_design/send.png", QSize(), QIcon.Normal, QIcon.Off)
        self.send_mensage__Benchmark.setIcon(icon12)
        self.send_mensage__Benchmark.setIconSize(QSize(34, 34))

        self.gridLayout_22.addWidget(self.send_mensage__Benchmark, 0, 7, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_22, 4, 0, 1, 1)

        self.myStackedWidget.addWidget(self.page_2)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_5 = QGridLayout(self.page)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.stackedWidget_instruction = QCustomQStackedWidget(self.page)
        self.stackedWidget_instruction.setObjectName(u"stackedWidget_instruction")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.gridLayout_3 = QGridLayout(self.page_3)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.comboBox_list_instruction_edit = QComboBox(self.page_3)
        self.comboBox_list_instruction_edit.setObjectName(u"comboBox_list_instruction_edit")
        sizePolicy7 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.comboBox_list_instruction_edit.sizePolicy().hasHeightForWidth())
        self.comboBox_list_instruction_edit.setSizePolicy(sizePolicy7)
        self.comboBox_list_instruction_edit.setMinimumSize(QSize(571, 0))
        self.comboBox_list_instruction_edit.setMaximumSize(QSize(16777215, 16777215))
        self.comboBox_list_instruction_edit.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 13px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 16px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_3.addWidget(self.comboBox_list_instruction_edit, 0, 2, 1, 1)

        self.Current_instuction_html_edit = QTextEdit(self.page_3)
        self.Current_instuction_html_edit.setObjectName(u"Current_instuction_html_edit")
        sizePolicy8 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.Current_instuction_html_edit.sizePolicy().hasHeightForWidth())
        self.Current_instuction_html_edit.setSizePolicy(sizePolicy8)
        self.Current_instuction_html_edit.setMinimumSize(QSize(0, 0))
        self.Current_instuction_html_edit.setMaximumSize(QSize(16777215, 16777215))
        self.Current_instuction_html_edit.setStyleSheet(u"            QTextEdit {\n"
"          \n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 10px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto preto */\n"
"                font-family: Arial;\n"
"                font-size: 14px;\n"
"            }")

        self.gridLayout_3.addWidget(self.Current_instuction_html_edit, 1, 0, 1, 4)

        self.Add_new_instructions_button_edit = QCustomQPushButton(self.page_3)
        self.Add_new_instructions_button_edit.setObjectName(u"Add_new_instructions_button_edit")
        sizePolicy3.setHeightForWidth(self.Add_new_instructions_button_edit.sizePolicy().hasHeightForWidth())
        self.Add_new_instructions_button_edit.setSizePolicy(sizePolicy3)
        self.Add_new_instructions_button_edit.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon13 = QIcon()
        icon13.addFile(u":/material_design/icons/material_design/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Add_new_instructions_button_edit.setIcon(icon13)
        self.Add_new_instructions_button_edit.setIconSize(QSize(30, 30))

        self.gridLayout_3.addWidget(self.Add_new_instructions_button_edit, 0, 0, 1, 1)

        self.label_2 = QLabel(self.page_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setIndent(10)

        self.gridLayout_3.addWidget(self.label_2, 0, 1, 1, 1)

        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.gridLayout_8.setHorizontalSpacing(6)
        self.gridLayout_8.setVerticalSpacing(9)
        self.gridLayout_8.setContentsMargins(-1, 9, 9, 1)
        self.instruction_input_edit = QTextEdit(self.page_3)
        self.instruction_input_edit.setObjectName(u"instruction_input_edit")
        sizePolicy6.setHeightForWidth(self.instruction_input_edit.sizePolicy().hasHeightForWidth())
        self.instruction_input_edit.setSizePolicy(sizePolicy6)
        self.instruction_input_edit.setMinimumSize(QSize(676, 52))
        self.instruction_input_edit.setMaximumSize(QSize(676, 52))
        self.instruction_input_edit.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 10px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_8.addWidget(self.instruction_input_edit, 1, 2, 1, 1)

        self.change_instruction_button_edit = QCustomQPushButton(self.page_3)
        self.change_instruction_button_edit.setObjectName(u"change_instruction_button_edit")
        sizePolicy.setHeightForWidth(self.change_instruction_button_edit.sizePolicy().hasHeightForWidth())
        self.change_instruction_button_edit.setSizePolicy(sizePolicy)
        self.change_instruction_button_edit.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon14 = QIcon()
        icon14.addFile(u":/material_design/icons/material_design/edit_note.png", QSize(), QIcon.Normal, QIcon.Off)
        self.change_instruction_button_edit.setIcon(icon14)
        self.change_instruction_button_edit.setIconSize(QSize(40, 47))

        self.gridLayout_8.addWidget(self.change_instruction_button_edit, 1, 3, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_8, 3, 0, 1, 4)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_5, 2, 0, 1, 1)

        self.stackedWidget_instruction.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.gridLayout_9 = QGridLayout(self.page_4)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_6.setHorizontalSpacing(2)
        self.label_3 = QLabel(self.page_4)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.gridLayout_6.addWidget(self.label_3, 0, 0, 1, 1)

        self.comboBox_list_agent_for_create_instruction_create = QComboBox(self.page_4)
        self.comboBox_list_agent_for_create_instruction_create.setObjectName(u"comboBox_list_agent_for_create_instruction_create")
        sizePolicy.setHeightForWidth(self.comboBox_list_agent_for_create_instruction_create.sizePolicy().hasHeightForWidth())
        self.comboBox_list_agent_for_create_instruction_create.setSizePolicy(sizePolicy)
        self.comboBox_list_agent_for_create_instruction_create.setMinimumSize(QSize(172, 0))
        self.comboBox_list_agent_for_create_instruction_create.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 13px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 16px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_6.addWidget(self.comboBox_list_agent_for_create_instruction_create, 1, 3, 1, 1)

        self.NameForInstruction_create = QLineEdit(self.page_4)
        self.NameForInstruction_create.setObjectName(u"NameForInstruction_create")
        sizePolicy.setHeightForWidth(self.NameForInstruction_create.sizePolicy().hasHeightForWidth())
        self.NameForInstruction_create.setSizePolicy(sizePolicy)
        self.NameForInstruction_create.setMinimumSize(QSize(172, 0))
        self.NameForInstruction_create.setStyleSheet(u"QLineEdit {\n"
"    background-color: #F7F7F7; /* Fundo principal */\n"
"    border: 1px solid #E0E0E0; /* Borda */\n"
"    border-radius: 13px; /* Borda arredondada */\n"
"    color: black; /* Cor do texto */\n"
"    font-size: 11px; /* Tamanho da fonte */\n"
"    padding: 5px 10px; /* Espa\u00e7amento interno */\n"
"    selection-background-color: #DCDCDC; /* Fundo da sele\u00e7\u00e3o de texto */\n"
"    selection-color: black; /* Cor do texto selecionado */\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    background-color: #FFFFFF; /* Fundo ao focar */\n"
"    border: 1px solid #A0A0A0; /* Borda ao focar */\n"
"}\n"
"\n"
"QLineEdit:disabled {\n"
"    background-color: #F0F0F0; /* Fundo quando desabilitado */\n"
"    border: 1px solid #C0C0C0; /* Borda quando desabilitado */\n"
"    color: #A0A0A0; /* Cor do texto desabilitado */\n"
"}\n"
"")

        self.gridLayout_6.addWidget(self.NameForInstruction_create, 1, 0, 1, 1)

        self.label_4 = QLabel(self.page_4)
        self.label_4.setObjectName(u"label_4")
        sizePolicy4.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy4)
        self.label_4.setIndent(34)

        self.gridLayout_6.addWidget(self.label_4, 0, 3, 1, 1)

        self.comboBox_category_instruction_create = QComboBox(self.page_4)
        self.comboBox_category_instruction_create.setObjectName(u"comboBox_category_instruction_create")
        self.comboBox_category_instruction_create.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 13px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 16px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_6.addWidget(self.comboBox_category_instruction_create, 1, 1, 1, 2)

        self.label_5 = QLabel(self.page_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setIndent(113)

        self.gridLayout_6.addWidget(self.label_5, 0, 1, 1, 2)


        self.gridLayout_9.addLayout(self.gridLayout_6, 0, 0, 1, 2)

        self.verticalSpacer_4 = QSpacerItem(20, 271, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_9.addItem(self.verticalSpacer_4, 1, 0, 1, 2)

        self.gridLayout_7 = QGridLayout()
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setHorizontalSpacing(6)
        self.BacktoEditinstruction_create = QCustomQPushButton(self.page_4)
        self.BacktoEditinstruction_create.setObjectName(u"BacktoEditinstruction_create")
        sizePolicy3.setHeightForWidth(self.BacktoEditinstruction_create.sizePolicy().hasHeightForWidth())
        self.BacktoEditinstruction_create.setSizePolicy(sizePolicy3)
        self.BacktoEditinstruction_create.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon15 = QIcon()
        icon15.addFile(u":/material_design/icons/material_design/keyboard_backspace.png", QSize(), QIcon.Normal, QIcon.Off)
        self.BacktoEditinstruction_create.setIcon(icon15)
        self.BacktoEditinstruction_create.setIconSize(QSize(27, 27))

        self.gridLayout_7.addWidget(self.BacktoEditinstruction_create, 0, 0, 1, 1)

        self.New_instruction_html_create = QTextEdit(self.page_4)
        self.New_instruction_html_create.setObjectName(u"New_instruction_html_create")
        sizePolicy6.setHeightForWidth(self.New_instruction_html_create.sizePolicy().hasHeightForWidth())
        self.New_instruction_html_create.setSizePolicy(sizePolicy6)
        self.New_instruction_html_create.setMinimumSize(QSize(641, 45))
        self.New_instruction_html_create.setMaximumSize(QSize(641, 45))
        self.New_instruction_html_create.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 10px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_7.addWidget(self.New_instruction_html_create, 0, 2, 1, 1)

        self.CreateInstructionbutton_create = QCustomQPushButton(self.page_4)
        self.CreateInstructionbutton_create.setObjectName(u"CreateInstructionbutton_create")
        sizePolicy.setHeightForWidth(self.CreateInstructionbutton_create.sizePolicy().hasHeightForWidth())
        self.CreateInstructionbutton_create.setSizePolicy(sizePolicy)
        self.CreateInstructionbutton_create.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon16 = QIcon()
        icon16.addFile(u":/material_design/icons/material_design/create.png", QSize(), QIcon.Normal, QIcon.Off)
        self.CreateInstructionbutton_create.setIcon(icon16)
        self.CreateInstructionbutton_create.setIconSize(QSize(37, 41))

        self.gridLayout_7.addWidget(self.CreateInstructionbutton_create, 0, 3, 1, 1)


        self.gridLayout_9.addLayout(self.gridLayout_7, 2, 0, 1, 2)

        self.stackedWidget_instruction.addWidget(self.page_4)

        self.gridLayout_5.addWidget(self.stackedWidget_instruction, 0, 0, 1, 1)

        self.myStackedWidget.addWidget(self.page)
        self.page_9 = QWidget()
        self.page_9.setObjectName(u"page_9")
        self.gridLayout_36 = QGridLayout(self.page_9)
        self.gridLayout_36.setObjectName(u"gridLayout_36")
        self.gridLayout_35 = QGridLayout()
        self.gridLayout_35.setObjectName(u"gridLayout_35")
        self.textEdit = QTextEdit(self.page_9)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setStyleSheet(u"            QTextEdit {\n"
"          \n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 10px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto preto */\n"
"                font-family: Arial;\n"
"                font-size: 14px;\n"
"            }")

        self.gridLayout_35.addWidget(self.textEdit, 2, 0, 1, 3)

        self.comboBox = QComboBox(self.page_9)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 13px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 16px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_35.addWidget(self.comboBox, 0, 1, 1, 2)

        self.label_24 = QLabel(self.page_9)
        self.label_24.setObjectName(u"label_24")

        self.gridLayout_35.addWidget(self.label_24, 0, 0, 1, 1)

        self.label_25 = QLabel(self.page_9)
        self.label_25.setObjectName(u"label_25")

        self.gridLayout_35.addWidget(self.label_25, 1, 0, 1, 1)

        self.comboBox_2 = QComboBox(self.page_9)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 13px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 16px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_35.addWidget(self.comboBox_2, 1, 1, 1, 2)


        self.gridLayout_36.addLayout(self.gridLayout_35, 0, 0, 1, 1)

        self.gridLayout_34 = QGridLayout()
        self.gridLayout_34.setObjectName(u"gridLayout_34")
        self.label_21 = QLabel(self.page_9)
        self.label_21.setObjectName(u"label_21")

        self.gridLayout_34.addWidget(self.label_21, 0, 0, 1, 1)

        self.label_22 = QLabel(self.page_9)
        self.label_22.setObjectName(u"label_22")

        self.gridLayout_34.addWidget(self.label_22, 1, 0, 1, 1)

        self.label_23 = QLabel(self.page_9)
        self.label_23.setObjectName(u"label_23")

        self.gridLayout_34.addWidget(self.label_23, 2, 0, 1, 1)


        self.gridLayout_36.addLayout(self.gridLayout_34, 0, 1, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 289, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_36.addItem(self.verticalSpacer_7, 1, 0, 1, 1)

        self.myStackedWidget.addWidget(self.page_9)
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_settings")
        self.gridLayout_17 = QGridLayout(self.page_settings)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.stackedWidget_SettingsCreate = QCustomQStackedWidget(self.page_settings)
        self.stackedWidget_SettingsCreate.setObjectName(u"stackedWidget_SettingsCreate")
        sizePolicy3.setHeightForWidth(self.stackedWidget_SettingsCreate.sizePolicy().hasHeightForWidth())
        self.stackedWidget_SettingsCreate.setSizePolicy(sizePolicy3)
        self.page_6 = QWidget()
        self.page_6.setObjectName(u"page_6")
        self.gridLayout_10 = QGridLayout(self.page_6)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.groupBox_3 = QGroupBox(self.page_6)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setAlignment(Qt.AlignCenter)
        self.gridLayout_16 = QGridLayout(self.groupBox_3)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.gridLayout_15 = QGridLayout()
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.gridLayout_15.setHorizontalSpacing(5)
        self.gridLayout_15.setVerticalSpacing(15)
        self.gridLayout_15.setContentsMargins(6, 1, 8, 1)
        self.AgentCategory = QComboBox(self.groupBox_3)
        self.AgentCategory.setObjectName(u"AgentCategory")
        sizePolicy.setHeightForWidth(self.AgentCategory.sizePolicy().hasHeightForWidth())
        self.AgentCategory.setSizePolicy(sizePolicy)
        self.AgentCategory.setMinimumSize(QSize(190, 23))
        self.AgentCategory.setMaximumSize(QSize(190, 23))
        self.AgentCategory.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 5px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 12px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_15.addWidget(self.AgentCategory, 5, 1, 1, 1)

        self.label_7 = QLabel(self.groupBox_3)
        self.label_7.setObjectName(u"label_7")

        self.gridLayout_15.addWidget(self.label_7, 1, 0, 1, 1)

        self.label_6 = QLabel(self.groupBox_3)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout_15.addWidget(self.label_6, 0, 0, 1, 1)

        self.label_15 = QLabel(self.groupBox_3)
        self.label_15.setObjectName(u"label_15")

        self.gridLayout_15.addWidget(self.label_15, 5, 0, 1, 1)

        self.KeyInFirebase = QTextEdit(self.groupBox_3)
        self.KeyInFirebase.setObjectName(u"KeyInFirebase")
        sizePolicy.setHeightForWidth(self.KeyInFirebase.sizePolicy().hasHeightForWidth())
        self.KeyInFirebase.setSizePolicy(sizePolicy)
        self.KeyInFirebase.setMinimumSize(QSize(190, 29))
        self.KeyInFirebase.setMaximumSize(QSize(190, 29))
        self.KeyInFirebase.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 2px;\n"
"                border-radius: 5px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_15.addWidget(self.KeyInFirebase, 0, 1, 1, 1)

        self.NameAgent = QTextEdit(self.groupBox_3)
        self.NameAgent.setObjectName(u"NameAgent")
        sizePolicy.setHeightForWidth(self.NameAgent.sizePolicy().hasHeightForWidth())
        self.NameAgent.setSizePolicy(sizePolicy)
        self.NameAgent.setMinimumSize(QSize(190, 29))
        self.NameAgent.setMaximumSize(QSize(190, 29))
        self.NameAgent.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 2px;\n"
"                border-radius: 5px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_15.addWidget(self.NameAgent, 1, 1, 1, 1)

        self.label_8 = QLabel(self.groupBox_3)
        self.label_8.setObjectName(u"label_8")

        self.gridLayout_15.addWidget(self.label_8, 4, 0, 1, 1)

        self.label_28 = QLabel(self.groupBox_3)
        self.label_28.setObjectName(u"label_28")

        self.gridLayout_15.addWidget(self.label_28, 6, 0, 1, 1)

        self.AgentKeysGithub = QComboBox(self.groupBox_3)
        self.AgentKeysGithub.setObjectName(u"AgentKeysGithub")
        self.AgentKeysGithub.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 5px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 12px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_15.addWidget(self.AgentKeysGithub, 6, 1, 1, 1)

        self.label_34 = QLabel(self.groupBox_3)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_15.addWidget(self.label_34, 7, 0, 1, 1)

        self.AgentKeysOpenAI = QComboBox(self.groupBox_3)
        self.AgentKeysOpenAI.setObjectName(u"AgentKeysOpenAI")
        self.AgentKeysOpenAI.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 5px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 12px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_15.addWidget(self.AgentKeysOpenAI, 7, 1, 1, 1)

        self.ModelSelect = QComboBox(self.groupBox_3)
        self.ModelSelect.addItem("")
        self.ModelSelect.addItem("")
        self.ModelSelect.setObjectName(u"ModelSelect")
        self.ModelSelect.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 5px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 12px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_15.addWidget(self.ModelSelect, 4, 1, 1, 1)

        self.AgentKeysFirebase = QComboBox(self.groupBox_3)
        self.AgentKeysFirebase.setObjectName(u"AgentKeysFirebase")
        self.AgentKeysFirebase.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 5px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 12px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_15.addWidget(self.AgentKeysFirebase, 8, 1, 1, 1)

        self.label_37 = QLabel(self.groupBox_3)
        self.label_37.setObjectName(u"label_37")

        self.gridLayout_15.addWidget(self.label_37, 8, 0, 1, 1)


        self.gridLayout_16.addLayout(self.gridLayout_15, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox_3, 1, 0, 2, 1)

        self.groupBox_9 = QGroupBox(self.page_6)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.gridLayout_38 = QGridLayout(self.groupBox_9)
        self.gridLayout_38.setObjectName(u"gridLayout_38")
        self.gridLayout_37 = QGridLayout()
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.verticalSpacer_10 = QSpacerItem(20, 24, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.gridLayout_37.addItem(self.verticalSpacer_10, 1, 0, 1, 1)

        self.PromptSettings = QPushButton(self.groupBox_9)
        self.PromptSettings.setObjectName(u"PromptSettings")
        font = QFont()
        self.PromptSettings.setFont(font)
        self.PromptSettings.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 11px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        icon17 = QIcon()
        icon17.addFile(u":/material_design/icons/material_design/text_snippet.png", QSize(), QIcon.Normal, QIcon.Off)
        self.PromptSettings.setIcon(icon17)
        self.PromptSettings.setIconSize(QSize(21, 18))

        self.gridLayout_37.addWidget(self.PromptSettings, 0, 0, 1, 1)

        self.ArgumentsSettings = QPushButton(self.groupBox_9)
        self.ArgumentsSettings.setObjectName(u"ArgumentsSettings")
        self.ArgumentsSettings.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 11px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        icon18 = QIcon()
        icon18.addFile(u":/material_design/icons/material_design/settings_remote.png", QSize(), QIcon.Normal, QIcon.Off)
        self.ArgumentsSettings.setIcon(icon18)
        self.ArgumentsSettings.setIconSize(QSize(23, 14))

        self.gridLayout_37.addWidget(self.ArgumentsSettings, 2, 2, 1, 1)

        self.FunctionsSettings = QPushButton(self.groupBox_9)
        self.FunctionsSettings.setObjectName(u"FunctionsSettings")
        self.FunctionsSettings.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 11px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        icon19 = QIcon()
        icon19.addFile(u":/material_design/icons/material_design/settings_input_component.png", QSize(), QIcon.Normal, QIcon.Off)
        self.FunctionsSettings.setIcon(icon19)
        self.FunctionsSettings.setIconSize(QSize(18, 18))

        self.gridLayout_37.addWidget(self.FunctionsSettings, 0, 2, 1, 1)

        self.verticalSpacer_9 = QSpacerItem(20, 32, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_37.addItem(self.verticalSpacer_9, 3, 0, 1, 1)

        self.InstructionSettings = QPushButton(self.groupBox_9)
        self.InstructionSettings.setObjectName(u"InstructionSettings")
        self.InstructionSettings.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 11px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        icon20 = QIcon()
        icon20.addFile(u":/material_design/icons/material_design/person_pin.png", QSize(), QIcon.Normal, QIcon.Off)
        self.InstructionSettings.setIcon(icon20)
        self.InstructionSettings.setIconSize(QSize(18, 18))

        self.gridLayout_37.addWidget(self.InstructionSettings, 2, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(14, 20, QSizePolicy.Maximum, QSizePolicy.Minimum)

        self.gridLayout_37.addItem(self.horizontalSpacer_3, 0, 1, 1, 1)


        self.gridLayout_38.addLayout(self.gridLayout_37, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox_9, 1, 1, 1, 1)

        self.groupBox_13 = QGroupBox(self.page_6)
        self.groupBox_13.setObjectName(u"groupBox_13")
        self.gridLayout_46 = QGridLayout(self.groupBox_13)
        self.gridLayout_46.setObjectName(u"gridLayout_46")
        self.gridLayout_47 = QGridLayout()
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.StorageAgentOutput_ = QCheckBox(self.groupBox_13)
        self.StorageAgentOutput_.setObjectName(u"StorageAgentOutput_")
        self.StorageAgentOutput_.setChecked(True)

        self.gridLayout_47.addWidget(self.StorageAgentOutput_, 1, 0, 1, 2)

        self.StoreFormatJsonAndJsonl = QRadioButton(self.groupBox_13)
        self.StoreFormatJsonAndJsonl.setObjectName(u"StoreFormatJsonAndJsonl")
        self.StoreFormatJsonAndJsonl.setChecked(True)

        self.gridLayout_47.addWidget(self.StoreFormatJsonAndJsonl, 2, 0, 1, 1)

        self.radioButton = QRadioButton(self.groupBox_13)
        self.radioButton.setObjectName(u"radioButton")

        self.gridLayout_47.addWidget(self.radioButton, 3, 0, 1, 1)

        self.StorageAgentCompletions = QCheckBox(self.groupBox_13)
        self.StorageAgentCompletions.setObjectName(u"StorageAgentCompletions")
        self.StorageAgentCompletions.setChecked(True)

        self.gridLayout_47.addWidget(self.StorageAgentCompletions, 0, 0, 1, 2)

        self.radioButton_2 = QRadioButton(self.groupBox_13)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout_47.addWidget(self.radioButton_2, 4, 0, 1, 1)

        self.verticalSpacer_14 = QSpacerItem(20, 32, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_47.addItem(self.verticalSpacer_14, 5, 0, 1, 2)


        self.gridLayout_46.addLayout(self.gridLayout_47, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox_13, 2, 1, 1, 1)

        self.groupBox = QGroupBox(self.page_6)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setAlignment(Qt.AlignCenter)
        self.gridLayout_12 = QGridLayout(self.groupBox)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.gridLayout_11.setHorizontalSpacing(15)
        self.gridLayout_11.setVerticalSpacing(23)
        self.gridLayout_11.setContentsMargins(-1, 0, 17, 9)
        self.VectorstoreinThread = QTextEdit(self.groupBox)
        self.VectorstoreinThread.setObjectName(u"VectorstoreinThread")
        sizePolicy.setHeightForWidth(self.VectorstoreinThread.sizePolicy().hasHeightForWidth())
        self.VectorstoreinThread.setSizePolicy(sizePolicy)
        self.VectorstoreinThread.setMinimumSize(QSize(201, 40))
        self.VectorstoreinThread.setMaximumSize(QSize(201, 40))
        self.VectorstoreinThread.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_11.addWidget(self.VectorstoreinThread, 2, 1, 1, 1)

        self.Vectorstoreinassistant = QTextEdit(self.groupBox)
        self.Vectorstoreinassistant.setObjectName(u"Vectorstoreinassistant")
        sizePolicy.setHeightForWidth(self.Vectorstoreinassistant.sizePolicy().hasHeightForWidth())
        self.Vectorstoreinassistant.setSizePolicy(sizePolicy)
        self.Vectorstoreinassistant.setMinimumSize(QSize(201, 40))
        self.Vectorstoreinassistant.setMaximumSize(QSize(201, 40))
        self.Vectorstoreinassistant.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_11.addWidget(self.Vectorstoreinassistant, 1, 1, 1, 1)

        self.UseVectorstoreToGenerateFiles = QCustomCheckBox(self.groupBox)
        self.UseVectorstoreToGenerateFiles.setObjectName(u"UseVectorstoreToGenerateFiles")

        self.gridLayout_11.addWidget(self.UseVectorstoreToGenerateFiles, 0, 0, 1, 3)

        self.verticalSpacer_8 = QSpacerItem(20, 86, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.gridLayout_11.addItem(self.verticalSpacer_8, 3, 0, 1, 1)

        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        sizePolicy6.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy6)

        self.gridLayout_11.addWidget(self.label_9, 1, 0, 1, 1)

        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")

        self.gridLayout_11.addWidget(self.label_10, 2, 0, 1, 1)

        self.VectorstoreinThreadByUser = QPushButton(self.groupBox)
        self.VectorstoreinThreadByUser.setObjectName(u"VectorstoreinThreadByUser")
        sizePolicy.setHeightForWidth(self.VectorstoreinThreadByUser.sizePolicy().hasHeightForWidth())
        self.VectorstoreinThreadByUser.setSizePolicy(sizePolicy)
        self.VectorstoreinThreadByUser.setStyleSheet(u"            QPushButton {\n"
"                background-color: #F7F7F7;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        self.VectorstoreinThreadByUser.setIcon(icon10)
        self.VectorstoreinThreadByUser.setIconSize(QSize(24, 27))

        self.gridLayout_11.addWidget(self.VectorstoreinThreadByUser, 2, 2, 1, 1)

        self.VectorstoreinassistantByUser = QPushButton(self.groupBox)
        self.VectorstoreinassistantByUser.setObjectName(u"VectorstoreinassistantByUser")
        sizePolicy.setHeightForWidth(self.VectorstoreinassistantByUser.sizePolicy().hasHeightForWidth())
        self.VectorstoreinassistantByUser.setSizePolicy(sizePolicy)
        self.VectorstoreinassistantByUser.setStyleSheet(u"            QPushButton {\n"
"                background-color: #F7F7F7;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        self.VectorstoreinassistantByUser.setIcon(icon10)
        self.VectorstoreinassistantByUser.setIconSize(QSize(24, 27))

        self.gridLayout_11.addWidget(self.VectorstoreinassistantByUser, 1, 2, 1, 1)


        self.gridLayout_12.addLayout(self.gridLayout_11, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox, 3, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.page_6)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setAlignment(Qt.AlignCenter)
        self.gridLayout_14 = QGridLayout(self.groupBox_2)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_13 = QGridLayout()
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.gridLayout_13.setHorizontalSpacing(78)
        self.gridLayout_13.setVerticalSpacing(8)
        self.gridLayout_13.setContentsMargins(1, 6, 5, 5)
        self.label_26 = QLabel(self.groupBox_2)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setMinimumSize(QSize(129, 0))

        self.gridLayout_13.addWidget(self.label_26, 4, 0, 1, 1)

        self.textEdit_2 = QTextEdit(self.groupBox_2)
        self.textEdit_2.setObjectName(u"textEdit_2")
        sizePolicy.setHeightForWidth(self.textEdit_2.sizePolicy().hasHeightForWidth())
        self.textEdit_2.setSizePolicy(sizePolicy)
        self.textEdit_2.setMinimumSize(QSize(230, 40))
        self.textEdit_2.setMaximumSize(QSize(230, 40))
        self.textEdit_2.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_13.addWidget(self.textEdit_2, 4, 1, 1, 2)

        self.pushButton_7 = QPushButton(self.groupBox_2)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setStyleSheet(u"            QPushButton {\n"
"                background-color: #F7F7F7;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        icon21 = QIcon()
        icon21.addFile(u":/material_design/icons/material_design/file_present.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_7.setIcon(icon21)
        self.pushButton_7.setIconSize(QSize(24, 27))

        self.gridLayout_13.addWidget(self.pushButton_7, 4, 3, 1, 1)

        self.Uploadlistfileforcodeinterpreterinthread = QTextEdit(self.groupBox_2)
        self.Uploadlistfileforcodeinterpreterinthread.setObjectName(u"Uploadlistfileforcodeinterpreterinthread")
        sizePolicy.setHeightForWidth(self.Uploadlistfileforcodeinterpreterinthread.sizePolicy().hasHeightForWidth())
        self.Uploadlistfileforcodeinterpreterinthread.setSizePolicy(sizePolicy)
        self.Uploadlistfileforcodeinterpreterinthread.setMinimumSize(QSize(230, 40))
        self.Uploadlistfileforcodeinterpreterinthread.setMaximumSize(QSize(230, 40))
        self.Uploadlistfileforcodeinterpreterinthread.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_13.addWidget(self.Uploadlistfileforcodeinterpreterinthread, 3, 1, 1, 1)

        self.label_12 = QLabel(self.groupBox_2)
        self.label_12.setObjectName(u"label_12")
        sizePolicy4.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy4)
        self.label_12.setMinimumSize(QSize(114, 0))

        self.gridLayout_13.addWidget(self.label_12, 1, 0, 1, 1)

        self.label_14 = QLabel(self.groupBox_2)
        self.label_14.setObjectName(u"label_14")
        sizePolicy4.setHeightForWidth(self.label_14.sizePolicy().hasHeightForWidth())
        self.label_14.setSizePolicy(sizePolicy4)
        self.label_14.setMinimumSize(QSize(114, 0))

        self.gridLayout_13.addWidget(self.label_14, 2, 0, 1, 1)

        self.Upload1imageforvisioninThread = QTextEdit(self.groupBox_2)
        self.Upload1imageforvisioninThread.setObjectName(u"Upload1imageforvisioninThread")
        sizePolicy.setHeightForWidth(self.Upload1imageforvisioninThread.sizePolicy().hasHeightForWidth())
        self.Upload1imageforvisioninThread.setSizePolicy(sizePolicy)
        self.Upload1imageforvisioninThread.setMinimumSize(QSize(230, 40))
        self.Upload1imageforvisioninThread.setMaximumSize(QSize(230, 40))
        self.Upload1imageforvisioninThread.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_13.addWidget(self.Upload1imageforvisioninThread, 2, 1, 1, 1)

        self.UploadlistfileforcodeinterpreterinthreadByUser = QPushButton(self.groupBox_2)
        self.UploadlistfileforcodeinterpreterinthreadByUser.setObjectName(u"UploadlistfileforcodeinterpreterinthreadByUser")
        sizePolicy.setHeightForWidth(self.UploadlistfileforcodeinterpreterinthreadByUser.sizePolicy().hasHeightForWidth())
        self.UploadlistfileforcodeinterpreterinthreadByUser.setSizePolicy(sizePolicy)
        self.UploadlistfileforcodeinterpreterinthreadByUser.setStyleSheet(u"            QPushButton {\n"
"                background-color: #F7F7F7;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        icon22 = QIcon()
        icon22.addFile(u":/material_design/icons/material_design/upload_file.png", QSize(), QIcon.Normal, QIcon.Off)
        self.UploadlistfileforcodeinterpreterinthreadByUser.setIcon(icon22)
        self.UploadlistfileforcodeinterpreterinthreadByUser.setIconSize(QSize(24, 27))

        self.gridLayout_13.addWidget(self.UploadlistfileforcodeinterpreterinthreadByUser, 3, 3, 1, 1)

        self.label_11 = QLabel(self.groupBox_2)
        self.label_11.setObjectName(u"label_11")
        sizePolicy9 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy9)
        self.label_11.setMinimumSize(QSize(114, 0))

        self.gridLayout_13.addWidget(self.label_11, 0, 0, 1, 1)

        self.Upload1fileinmessage = QTextEdit(self.groupBox_2)
        self.Upload1fileinmessage.setObjectName(u"Upload1fileinmessage")
        sizePolicy.setHeightForWidth(self.Upload1fileinmessage.sizePolicy().hasHeightForWidth())
        self.Upload1fileinmessage.setSizePolicy(sizePolicy)
        self.Upload1fileinmessage.setMinimumSize(QSize(230, 40))
        self.Upload1fileinmessage.setMaximumSize(QSize(230, 40))
        self.Upload1fileinmessage.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_13.addWidget(self.Upload1fileinmessage, 1, 1, 1, 1)

        self.label_13 = QLabel(self.groupBox_2)
        self.label_13.setObjectName(u"label_13")
        sizePolicy4.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy4)
        self.label_13.setMinimumSize(QSize(113, 0))

        self.gridLayout_13.addWidget(self.label_13, 3, 0, 1, 1)

        self.Upload1fileinThread = QTextEdit(self.groupBox_2)
        self.Upload1fileinThread.setObjectName(u"Upload1fileinThread")
        sizePolicy.setHeightForWidth(self.Upload1fileinThread.sizePolicy().hasHeightForWidth())
        self.Upload1fileinThread.setSizePolicy(sizePolicy)
        self.Upload1fileinThread.setMinimumSize(QSize(230, 40))
        self.Upload1fileinThread.setMaximumSize(QSize(230, 40))
        self.Upload1fileinThread.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_13.addWidget(self.Upload1fileinThread, 0, 1, 1, 1)

        self.Upload1fileinmessageByUser = QPushButton(self.groupBox_2)
        self.Upload1fileinmessageByUser.setObjectName(u"Upload1fileinmessageByUser")
        sizePolicy.setHeightForWidth(self.Upload1fileinmessageByUser.sizePolicy().hasHeightForWidth())
        self.Upload1fileinmessageByUser.setSizePolicy(sizePolicy)
        self.Upload1fileinmessageByUser.setStyleSheet(u"            QPushButton {\n"
"                background-color: #F7F7F7;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        self.Upload1fileinmessageByUser.setIcon(icon10)
        self.Upload1fileinmessageByUser.setIconSize(QSize(24, 27))

        self.gridLayout_13.addWidget(self.Upload1fileinmessageByUser, 1, 3, 1, 1)

        self.Upload1fileinThreadByUser = QPushButton(self.groupBox_2)
        self.Upload1fileinThreadByUser.setObjectName(u"Upload1fileinThreadByUser")
        sizePolicy.setHeightForWidth(self.Upload1fileinThreadByUser.sizePolicy().hasHeightForWidth())
        self.Upload1fileinThreadByUser.setSizePolicy(sizePolicy)
        self.Upload1fileinThreadByUser.setStyleSheet(u"            QPushButton {\n"
"                background-color: #F7F7F7;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        self.Upload1fileinThreadByUser.setIcon(icon10)
        self.Upload1fileinThreadByUser.setIconSize(QSize(24, 27))

        self.gridLayout_13.addWidget(self.Upload1fileinThreadByUser, 0, 3, 1, 1)

        self.Upload1imageforvisioninThreadByUser = QPushButton(self.groupBox_2)
        self.Upload1imageforvisioninThreadByUser.setObjectName(u"Upload1imageforvisioninThreadByUser")
        sizePolicy.setHeightForWidth(self.Upload1imageforvisioninThreadByUser.sizePolicy().hasHeightForWidth())
        self.Upload1imageforvisioninThreadByUser.setSizePolicy(sizePolicy)
        self.Upload1imageforvisioninThreadByUser.setStyleSheet(u"            QPushButton {\n"
"                background-color: #F7F7F7;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        icon23 = QIcon()
        icon23.addFile(u":/material_design/icons/material_design/image_search.png", QSize(), QIcon.Normal, QIcon.Off)
        self.Upload1imageforvisioninThreadByUser.setIcon(icon23)
        self.Upload1imageforvisioninThreadByUser.setIconSize(QSize(24, 27))

        self.gridLayout_13.addWidget(self.Upload1imageforvisioninThreadByUser, 2, 3, 1, 1)


        self.gridLayout_14.addLayout(self.gridLayout_13, 0, 0, 1, 1)


        self.gridLayout_10.addWidget(self.groupBox_2, 3, 1, 1, 1)

        self.CreateAgent = QPushButton(self.page_6)
        self.CreateAgent.setObjectName(u"CreateAgent")
        self.CreateAgent.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"	\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        icon24 = QIcon()
        icon24.addFile(u":/material_design/icons/material_design/person_add_alt_1.png", QSize(), QIcon.Normal, QIcon.Off)
        self.CreateAgent.setIcon(icon24)
        self.CreateAgent.setIconSize(QSize(26, 31))

        self.gridLayout_10.addWidget(self.CreateAgent, 0, 0, 1, 2)

        self.stackedWidget_SettingsCreate.addWidget(self.page_6)
        self.page_7 = QWidget()
        self.page_7.setObjectName(u"page_7")
        self.gridLayout_26 = QGridLayout(self.page_7)
        self.gridLayout_26.setObjectName(u"gridLayout_26")
        self.groupBox_5 = QGroupBox(self.page_7)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_19 = QGridLayout(self.groupBox_5)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.Promptmain = QTextEdit(self.groupBox_5)
        self.Promptmain.setObjectName(u"Promptmain")
        sizePolicy10 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.Promptmain.sizePolicy().hasHeightForWidth())
        self.Promptmain.setSizePolicy(sizePolicy10)
        self.Promptmain.setMinimumSize(QSize(0, 0))
        self.Promptmain.setMaximumSize(QSize(16777215, 16777215))
        self.Promptmain.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_19.addWidget(self.Promptmain, 0, 0, 1, 1)


        self.gridLayout_26.addWidget(self.groupBox_5, 0, 0, 1, 1)

        self.groupBox_7 = QGroupBox(self.page_7)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.gridLayout_21 = QGridLayout(self.groupBox_7)
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.PromptRules = QTextEdit(self.groupBox_7)
        self.PromptRules.setObjectName(u"PromptRules")
        sizePolicy10.setHeightForWidth(self.PromptRules.sizePolicy().hasHeightForWidth())
        self.PromptRules.setSizePolicy(sizePolicy10)
        self.PromptRules.setMinimumSize(QSize(0, 0))
        self.PromptRules.setMaximumSize(QSize(16777215, 16777215))
        self.PromptRules.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_21.addWidget(self.PromptRules, 0, 0, 1, 1)


        self.gridLayout_26.addWidget(self.groupBox_7, 0, 1, 1, 1)

        self.groupBox_6 = QGroupBox(self.page_7)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_20 = QGridLayout(self.groupBox_6)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.PromptExample = QTextEdit(self.groupBox_6)
        self.PromptExample.setObjectName(u"PromptExample")
        sizePolicy10.setHeightForWidth(self.PromptExample.sizePolicy().hasHeightForWidth())
        self.PromptExample.setSizePolicy(sizePolicy10)
        self.PromptExample.setMinimumSize(QSize(0, 0))
        self.PromptExample.setMaximumSize(QSize(16777215, 16777215))
        self.PromptExample.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_20.addWidget(self.PromptExample, 0, 0, 1, 1)


        self.gridLayout_26.addWidget(self.groupBox_6, 0, 2, 1, 1)

        self.BackToSettings = QPushButton(self.page_7)
        self.BackToSettings.setObjectName(u"BackToSettings")
        self.BackToSettings.setFont(font)
        self.BackToSettings.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        self.BackToSettings.setIcon(icon3)
        self.BackToSettings.setIconSize(QSize(39, 29))

        self.gridLayout_26.addWidget(self.BackToSettings, 1, 0, 1, 3)

        self.stackedWidget_SettingsCreate.addWidget(self.page_7)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.gridLayout_28 = QGridLayout(self.page_5)
        self.gridLayout_28.setObjectName(u"gridLayout_28")
        self.groupBox_8 = QGroupBox(self.page_5)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.gridLayout_24 = QGridLayout(self.groupBox_8)
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.InstructionAgentCreate = QTextEdit(self.groupBox_8)
        self.InstructionAgentCreate.setObjectName(u"InstructionAgentCreate")
        sizePolicy10.setHeightForWidth(self.InstructionAgentCreate.sizePolicy().hasHeightForWidth())
        self.InstructionAgentCreate.setSizePolicy(sizePolicy10)
        self.InstructionAgentCreate.setMinimumSize(QSize(322, 0))
        self.InstructionAgentCreate.setMaximumSize(QSize(322, 16777215))
        self.InstructionAgentCreate.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_24.addWidget(self.InstructionAgentCreate, 0, 0, 1, 1)


        self.gridLayout_28.addWidget(self.groupBox_8, 0, 0, 1, 1)

        self.groupBox_4 = QGroupBox(self.page_5)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_25 = QGridLayout(self.groupBox_4)
        self.gridLayout_25.setObjectName(u"gridLayout_25")
        self.AditionalInstructionsAgentCreate = QTextEdit(self.groupBox_4)
        self.AditionalInstructionsAgentCreate.setObjectName(u"AditionalInstructionsAgentCreate")
        sizePolicy10.setHeightForWidth(self.AditionalInstructionsAgentCreate.sizePolicy().hasHeightForWidth())
        self.AditionalInstructionsAgentCreate.setSizePolicy(sizePolicy10)
        self.AditionalInstructionsAgentCreate.setMinimumSize(QSize(322, 0))
        self.AditionalInstructionsAgentCreate.setMaximumSize(QSize(322, 16777215))
        self.AditionalInstructionsAgentCreate.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_25.addWidget(self.AditionalInstructionsAgentCreate, 0, 0, 1, 1)


        self.gridLayout_28.addWidget(self.groupBox_4, 0, 1, 1, 1)

        self.pushButton = QPushButton(self.page_5)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        self.pushButton.setIcon(icon3)
        self.pushButton.setIconSize(QSize(36, 36))

        self.gridLayout_28.addWidget(self.pushButton, 1, 0, 1, 2)

        self.stackedWidget_SettingsCreate.addWidget(self.page_5)
        self.page_8 = QWidget()
        self.page_8.setObjectName(u"page_8")
        self.gridLayout_31 = QGridLayout(self.page_8)
        self.gridLayout_31.setObjectName(u"gridLayout_31")
        self.groupBox_10 = QGroupBox(self.page_8)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.gridLayout_27 = QGridLayout(self.groupBox_10)
        self.gridLayout_27.setObjectName(u"gridLayout_27")
        self.AgentTools = QTextEdit(self.groupBox_10)
        self.AgentTools.setObjectName(u"AgentTools")
        sizePolicy10.setHeightForWidth(self.AgentTools.sizePolicy().hasHeightForWidth())
        self.AgentTools.setSizePolicy(sizePolicy10)
        self.AgentTools.setMinimumSize(QSize(0, 0))
        self.AgentTools.setMaximumSize(QSize(16777215, 16777215))
        self.AgentTools.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_27.addWidget(self.AgentTools, 0, 0, 1, 1)


        self.gridLayout_31.addWidget(self.groupBox_10, 0, 0, 1, 1)

        self.groupBox_11 = QGroupBox(self.page_8)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.gridLayout_29 = QGridLayout(self.groupBox_11)
        self.gridLayout_29.setObjectName(u"gridLayout_29")
        self.namefunction_agentcreate = QTextEdit(self.groupBox_11)
        self.namefunction_agentcreate.setObjectName(u"namefunction_agentcreate")
        self.namefunction_agentcreate.setMaximumSize(QSize(16777215, 22))
        self.namefunction_agentcreate.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 3px;\n"
"                border-radius: 3px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_29.addWidget(self.namefunction_agentcreate, 0, 1, 1, 1)

        self.label_16 = QLabel(self.groupBox_11)
        self.label_16.setObjectName(u"label_16")

        self.gridLayout_29.addWidget(self.label_16, 0, 0, 1, 1)

        self.FunctionPython = QTextEdit(self.groupBox_11)
        self.FunctionPython.setObjectName(u"FunctionPython")
        sizePolicy10.setHeightForWidth(self.FunctionPython.sizePolicy().hasHeightForWidth())
        self.FunctionPython.setSizePolicy(sizePolicy10)
        self.FunctionPython.setMinimumSize(QSize(0, 0))
        self.FunctionPython.setMaximumSize(QSize(16777215, 16777215))
        self.FunctionPython.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_29.addWidget(self.FunctionPython, 1, 0, 1, 2)


        self.gridLayout_31.addWidget(self.groupBox_11, 0, 1, 1, 1)

        self.groupBox_12 = QGroupBox(self.page_8)
        self.groupBox_12.setObjectName(u"groupBox_12")
        self.gridLayout_30 = QGridLayout(self.groupBox_12)
        self.gridLayout_30.setObjectName(u"gridLayout_30")
        self.FunctionPythonOutput = QTextEdit(self.groupBox_12)
        self.FunctionPythonOutput.setObjectName(u"FunctionPythonOutput")
        sizePolicy10.setHeightForWidth(self.FunctionPythonOutput.sizePolicy().hasHeightForWidth())
        self.FunctionPythonOutput.setSizePolicy(sizePolicy10)
        self.FunctionPythonOutput.setMinimumSize(QSize(0, 0))
        self.FunctionPythonOutput.setMaximumSize(QSize(16777215, 16777215))
        self.FunctionPythonOutput.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_30.addWidget(self.FunctionPythonOutput, 0, 0, 1, 1)


        self.gridLayout_31.addWidget(self.groupBox_12, 0, 2, 1, 1)

        self.pushButton_2 = QPushButton(self.page_8)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        self.pushButton_2.setIcon(icon3)
        self.pushButton_2.setIconSize(QSize(35, 33))

        self.gridLayout_31.addWidget(self.pushButton_2, 1, 0, 1, 3)

        self.stackedWidget_SettingsCreate.addWidget(self.page_8)
        self.page_10 = QWidget()
        self.page_10.setObjectName(u"page_10")
        self.gridLayout_18 = QGridLayout(self.page_10)
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_18.addItem(self.horizontalSpacer_2, 1, 1, 1, 1)

        self.gridLayout_32 = QGridLayout()
        self.gridLayout_32.setObjectName(u"gridLayout_32")
        self.gridLayout_32.setContentsMargins(2, 3, 9, -1)
        self.ArgsCreatetextedit = QTextEdit(self.page_10)
        self.ArgsCreatetextedit.setObjectName(u"ArgsCreatetextedit")
        sizePolicy11 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.ArgsCreatetextedit.sizePolicy().hasHeightForWidth())
        self.ArgsCreatetextedit.setSizePolicy(sizePolicy11)
        self.ArgsCreatetextedit.setMinimumSize(QSize(348, 50))
        self.ArgsCreatetextedit.setMaximumSize(QSize(347, 50))
        self.ArgsCreatetextedit.setStyleSheet(u"            QTextEdit {\n"
"          \n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 10px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto preto */\n"
"                font-family: Arial;\n"
"                font-size: 14px;\n"
"            }")

        self.gridLayout_32.addWidget(self.ArgsCreatetextedit, 1, 1, 1, 1)

        self.label_18 = QLabel(self.page_10)
        self.label_18.setObjectName(u"label_18")
        sizePolicy4.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy4)
        self.label_18.setAlignment(Qt.AlignCenter)
        self.label_18.setIndent(34)

        self.gridLayout_32.addWidget(self.label_18, 1, 0, 1, 1)

        self.CurrentArgs_AgentCreate = QComboBox(self.page_10)
        self.CurrentArgs_AgentCreate.addItem("")
        self.CurrentArgs_AgentCreate.addItem("")
        self.CurrentArgs_AgentCreate.setObjectName(u"CurrentArgs_AgentCreate")
        sizePolicy.setHeightForWidth(self.CurrentArgs_AgentCreate.sizePolicy().hasHeightForWidth())
        self.CurrentArgs_AgentCreate.setSizePolicy(sizePolicy)
        self.CurrentArgs_AgentCreate.setMinimumSize(QSize(348, 0))
        self.CurrentArgs_AgentCreate.setMaximumSize(QSize(348, 16777215))
        self.CurrentArgs_AgentCreate.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 13px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 12px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_32.addWidget(self.CurrentArgs_AgentCreate, 2, 1, 1, 1)

        self.label_17 = QLabel(self.page_10)
        self.label_17.setObjectName(u"label_17")

        self.gridLayout_32.addWidget(self.label_17, 2, 0, 1, 1)


        self.gridLayout_18.addLayout(self.gridLayout_32, 1, 0, 1, 1)

        self.verticalSpacer_6 = QSpacerItem(20, 352, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.gridLayout_18.addItem(self.verticalSpacer_6, 2, 0, 1, 1)

        self.BacktoEditinstruction_create_2 = QCustomQPushButton(self.page_10)
        self.BacktoEditinstruction_create_2.setObjectName(u"BacktoEditinstruction_create_2")
        sizePolicy3.setHeightForWidth(self.BacktoEditinstruction_create_2.sizePolicy().hasHeightForWidth())
        self.BacktoEditinstruction_create_2.setSizePolicy(sizePolicy3)
        self.BacktoEditinstruction_create_2.setMinimumSize(QSize(683, 0))
        self.BacktoEditinstruction_create_2.setMaximumSize(QSize(683, 16777215))
        self.BacktoEditinstruction_create_2.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }\n"
"")
        self.BacktoEditinstruction_create_2.setIcon(icon15)
        self.BacktoEditinstruction_create_2.setIconSize(QSize(27, 27))

        self.gridLayout_18.addWidget(self.BacktoEditinstruction_create_2, 3, 0, 1, 2)

        self.stackedWidget_SettingsCreate.addWidget(self.page_10)
        self.page_13 = QWidget()
        self.page_13.setObjectName(u"page_13")
        self.stackedWidget_SettingsCreate.addWidget(self.page_13)

        self.gridLayout_17.addWidget(self.stackedWidget_SettingsCreate, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 46, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_17.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.myStackedWidget.addWidget(self.page_settings)
        self.page_11 = QWidget()
        self.page_11.setObjectName(u"page_11")
        self.gridLayout_45 = QGridLayout(self.page_11)
        self.gridLayout_45.setObjectName(u"gridLayout_45")
        self.card1 = QGroupBox(self.page_11)
        self.card1.setObjectName(u"card1")
        self.gridLayout_43 = QGridLayout(self.card1)
        self.gridLayout_43.setObjectName(u"gridLayout_43")
        self.gridLayout_44 = QGridLayout()
        self.gridLayout_44.setObjectName(u"gridLayout_44")
        self.openaitoken_AgentKeys = QTextEdit(self.card1)
        self.openaitoken_AgentKeys.setObjectName(u"openaitoken_AgentKeys")
        sizePolicy3.setHeightForWidth(self.openaitoken_AgentKeys.sizePolicy().hasHeightForWidth())
        self.openaitoken_AgentKeys.setSizePolicy(sizePolicy3)
        self.openaitoken_AgentKeys.setMinimumSize(QSize(279, 40))
        self.openaitoken_AgentKeys.setMaximumSize(QSize(279, 40))
        self.openaitoken_AgentKeys.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_44.addWidget(self.openaitoken_AgentKeys, 1, 1, 1, 1)

        self.verticalSpacer_12 = QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Maximum)

        self.gridLayout_44.addItem(self.verticalSpacer_12, 2, 1, 1, 1)

        self.label_31 = QLabel(self.card1)
        self.label_31.setObjectName(u"label_31")

        self.gridLayout_44.addWidget(self.label_31, 1, 0, 1, 1)

        self.label_30 = QLabel(self.card1)
        self.label_30.setObjectName(u"label_30")

        self.gridLayout_44.addWidget(self.label_30, 0, 0, 1, 1)

        self.openainamefortoken_AgentKeys = QTextEdit(self.card1)
        self.openainamefortoken_AgentKeys.setObjectName(u"openainamefortoken_AgentKeys")
        sizePolicy3.setHeightForWidth(self.openainamefortoken_AgentKeys.sizePolicy().hasHeightForWidth())
        self.openainamefortoken_AgentKeys.setSizePolicy(sizePolicy3)
        self.openainamefortoken_AgentKeys.setMinimumSize(QSize(279, 40))
        self.openainamefortoken_AgentKeys.setMaximumSize(QSize(279, 40))
        self.openainamefortoken_AgentKeys.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_44.addWidget(self.openainamefortoken_AgentKeys, 0, 1, 1, 1)

        self.createkeyopenai_AgentKeys = QPushButton(self.card1)
        self.createkeyopenai_AgentKeys.setObjectName(u"createkeyopenai_AgentKeys")
        self.createkeyopenai_AgentKeys.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 11px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }")
        icon25 = QIcon()
        icon25.addFile(u":/material_design/icons/material_design/key.png", QSize(), QIcon.Normal, QIcon.Off)
        self.createkeyopenai_AgentKeys.setIcon(icon25)
        self.createkeyopenai_AgentKeys.setIconSize(QSize(22, 22))

        self.gridLayout_44.addWidget(self.createkeyopenai_AgentKeys, 3, 0, 1, 3)


        self.gridLayout_43.addLayout(self.gridLayout_44, 0, 1, 1, 1)


        self.gridLayout_45.addWidget(self.card1, 0, 0, 1, 1)

        self.card2 = QGroupBox(self.page_11)
        self.card2.setObjectName(u"card2")
        self.gridLayout_40 = QGridLayout(self.card2)
        self.gridLayout_40.setObjectName(u"gridLayout_40")
        self.gridLayout_39 = QGridLayout()
        self.gridLayout_39.setObjectName(u"gridLayout_39")
        self.githuusername_AgentKeys = QTextEdit(self.card2)
        self.githuusername_AgentKeys.setObjectName(u"githuusername_AgentKeys")
        sizePolicy3.setHeightForWidth(self.githuusername_AgentKeys.sizePolicy().hasHeightForWidth())
        self.githuusername_AgentKeys.setSizePolicy(sizePolicy3)
        self.githuusername_AgentKeys.setMinimumSize(QSize(295, 40))
        self.githuusername_AgentKeys.setMaximumSize(QSize(295, 40))
        self.githuusername_AgentKeys.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_39.addWidget(self.githuusername_AgentKeys, 0, 0, 1, 1)

        self.githubtoken_AgentKeys = QTextEdit(self.card2)
        self.githubtoken_AgentKeys.setObjectName(u"githubtoken_AgentKeys")
        sizePolicy3.setHeightForWidth(self.githubtoken_AgentKeys.sizePolicy().hasHeightForWidth())
        self.githubtoken_AgentKeys.setSizePolicy(sizePolicy3)
        self.githubtoken_AgentKeys.setMinimumSize(QSize(295, 40))
        self.githubtoken_AgentKeys.setMaximumSize(QSize(295, 40))
        self.githubtoken_AgentKeys.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_39.addWidget(self.githubtoken_AgentKeys, 1, 0, 1, 1)

        self.createkeygithub_AgentKeys = QPushButton(self.card2)
        self.createkeygithub_AgentKeys.setObjectName(u"createkeygithub_AgentKeys")
        self.createkeygithub_AgentKeys.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 11px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }")
        self.createkeygithub_AgentKeys.setIcon(icon25)
        self.createkeygithub_AgentKeys.setIconSize(QSize(22, 22))

        self.gridLayout_39.addWidget(self.createkeygithub_AgentKeys, 2, 0, 1, 2)


        self.gridLayout_40.addLayout(self.gridLayout_39, 0, 1, 1, 1)


        self.gridLayout_45.addWidget(self.card2, 0, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(13, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_45.addItem(self.horizontalSpacer_6, 0, 2, 1, 1)

        self.card3 = QGroupBox(self.page_11)
        self.card3.setObjectName(u"card3")
        self.gridLayout_41 = QGridLayout(self.card3)
        self.gridLayout_41.setObjectName(u"gridLayout_41")
        self.gridLayout_42 = QGridLayout()
        self.gridLayout_42.setObjectName(u"gridLayout_42")
        self.label_32 = QLabel(self.card3)
        self.label_32.setObjectName(u"label_32")

        self.gridLayout_42.addWidget(self.label_32, 1, 0, 1, 1)

        self.credentialsapp_AgentKeys = QTextEdit(self.card3)
        self.credentialsapp_AgentKeys.setObjectName(u"credentialsapp_AgentKeys")
        sizePolicy3.setHeightForWidth(self.credentialsapp_AgentKeys.sizePolicy().hasHeightForWidth())
        self.credentialsapp_AgentKeys.setSizePolicy(sizePolicy3)
        self.credentialsapp_AgentKeys.setMinimumSize(QSize(0, 40))
        self.credentialsapp_AgentKeys.setMaximumSize(QSize(295, 40))
        self.credentialsapp_AgentKeys.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_42.addWidget(self.credentialsapp_AgentKeys, 3, 1, 1, 1)

        self.label_29 = QLabel(self.card3)
        self.label_29.setObjectName(u"label_29")

        self.gridLayout_42.addWidget(self.label_29, 3, 0, 1, 1)

        self.label_27 = QLabel(self.card3)
        self.label_27.setObjectName(u"label_27")
        sizePolicy4.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy4)

        self.gridLayout_42.addWidget(self.label_27, 0, 0, 1, 1)

        self.createkeysfirebase_AgentKeys = QPushButton(self.card3)
        self.createkeysfirebase_AgentKeys.setObjectName(u"createkeysfirebase_AgentKeys")
        self.createkeysfirebase_AgentKeys.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 11px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"            QPushButton:hover {\n"
"                background-color: #EDEDED;\n"
"            }\n"
"            QPushButton:pressed {\n"
"                background-color: #DCDCDC;\n"
"            }")
        self.createkeysfirebase_AgentKeys.setIcon(icon25)
        self.createkeysfirebase_AgentKeys.setIconSize(QSize(22, 22))

        self.gridLayout_42.addWidget(self.createkeysfirebase_AgentKeys, 5, 0, 1, 3)

        self.uploadcredentialapp_AgentKeys = QPushButton(self.card3)
        self.uploadcredentialapp_AgentKeys.setObjectName(u"uploadcredentialapp_AgentKeys")
        self.uploadcredentialapp_AgentKeys.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 11px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        icon26 = QIcon()
        icon26.addFile(u":/font_awesome_regular/icons/font_awesome/regular/file-lines.png", QSize(), QIcon.Normal, QIcon.Off)
        self.uploadcredentialapp_AgentKeys.setIcon(icon26)
        self.uploadcredentialapp_AgentKeys.setIconSize(QSize(22, 33))

        self.gridLayout_42.addWidget(self.uploadcredentialapp_AgentKeys, 3, 2, 1, 1)

        self.appname_AgentKeys = QTextEdit(self.card3)
        self.appname_AgentKeys.setObjectName(u"appname_AgentKeys")
        sizePolicy3.setHeightForWidth(self.appname_AgentKeys.sizePolicy().hasHeightForWidth())
        self.appname_AgentKeys.setSizePolicy(sizePolicy3)
        self.appname_AgentKeys.setMinimumSize(QSize(0, 40))
        self.appname_AgentKeys.setMaximumSize(QSize(295, 40))
        self.appname_AgentKeys.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_42.addWidget(self.appname_AgentKeys, 0, 1, 1, 1)

        self.label_33 = QLabel(self.card3)
        self.label_33.setObjectName(u"label_33")

        self.gridLayout_42.addWidget(self.label_33, 2, 0, 1, 1)

        self.Databaseurl_AgentKeys = QTextEdit(self.card3)
        self.Databaseurl_AgentKeys.setObjectName(u"Databaseurl_AgentKeys")
        sizePolicy3.setHeightForWidth(self.Databaseurl_AgentKeys.sizePolicy().hasHeightForWidth())
        self.Databaseurl_AgentKeys.setSizePolicy(sizePolicy3)
        self.Databaseurl_AgentKeys.setMinimumSize(QSize(0, 40))
        self.Databaseurl_AgentKeys.setMaximumSize(QSize(295, 40))
        self.Databaseurl_AgentKeys.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_42.addWidget(self.Databaseurl_AgentKeys, 1, 1, 1, 1)

        self.Storagebucket_AgentKeys = QTextEdit(self.card3)
        self.Storagebucket_AgentKeys.setObjectName(u"Storagebucket_AgentKeys")
        sizePolicy3.setHeightForWidth(self.Storagebucket_AgentKeys.sizePolicy().hasHeightForWidth())
        self.Storagebucket_AgentKeys.setSizePolicy(sizePolicy3)
        self.Storagebucket_AgentKeys.setMinimumSize(QSize(0, 40))
        self.Storagebucket_AgentKeys.setMaximumSize(QSize(295, 40))
        self.Storagebucket_AgentKeys.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 5px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")

        self.gridLayout_42.addWidget(self.Storagebucket_AgentKeys, 2, 1, 1, 1)


        self.gridLayout_41.addLayout(self.gridLayout_42, 0, 1, 1, 1)


        self.gridLayout_45.addWidget(self.card3, 1, 0, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(13, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_45.addItem(self.horizontalSpacer_5, 1, 2, 1, 1)

        self.verticalSpacer_11 = QSpacerItem(20, 210, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_45.addItem(self.verticalSpacer_11, 2, 0, 1, 1)

        self.myStackedWidget.addWidget(self.page_11)
        self.page_12 = QWidget()
        self.page_12.setObjectName(u"page_12")
        self.gridLayoutWidget_3 = QWidget(self.page_12)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 0, 741, 231))
        self.gridLayout_48 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_48.setObjectName(u"gridLayout_48")
        self.gridLayout_48.setContentsMargins(0, 0, 0, 0)
        self.label_35 = QLabel(self.gridLayoutWidget_3)
        self.label_35.setObjectName(u"label_35")

        self.gridLayout_48.addWidget(self.label_35, 0, 0, 1, 1)

        self.AgentViewDestilation_View = QTreeView(self.gridLayoutWidget_3)
        self.AgentViewDestilation_View.setObjectName(u"AgentViewDestilation_View")
        self.AgentViewDestilation_View.setStyleSheet(u"QTreeView {\n"
"    background-color: white;  /* Cor de fundo branca */\n"
"    color: black;  /* Cor do texto preta */\n"
"    border-radius: 13px;  /* Borda arredondada */\n"
"    font-size: 16px;  /* Ajuste do tamanho da fonte */\n"
"    border: 1px solid #DCDCDC;  /* Borda sutil */\n"
"    alternate-background-color: #EDEDED;  /* Cor alternada das linhas */\n"
"    selection-background-color: #DCDCDC;  /* Cor de fundo para o item selecionado */\n"
"    selection-color: black;  /* Cor do texto do item selecionado */\n"
"    show-decoration-selected: 1;  /* Mostrar o estilo de sele\u00e7\u00e3o completo */\n"
"    outline: none;  /* Remove a borda do foco */\n"
"}\n"
"\n"
"QTreeView::item {\n"
"    height: 25px;  /* Define a altura dos itens */\n"
"    padding: 5px;  /* Espa\u00e7amento dentro de cada item */\n"
"    border-radius: 13px;  /* Borda arredondada dos itens */\n"
"}\n"
"\n"
"QTreeView::item:hover {\n"
"    background-color: #EDEDED;  /* Cor de fundo ao passar o mouse */\n"
"}\n"
"\n"
"QTreeView::"
                        "item:selected {\n"
"    background-color: #DCDCDC;  /* Cor de fundo do item selecionado */\n"
"    color: black;  /* Cor do texto do item selecionado */\n"
"}\n"
"\n"
"QTreeView::branch:open:has-children {\n"
"    image: url(':/material_design/icons/material_design/format_align_justify.png');  /* \u00cdcone de ramo aberto */\n"
"}\n"
"\n"
"QTreeView::branch:closed:has-children {\n"
"    image: url(':/material_design/icons/material_design/format_align_left.png');  /* \u00cdcone de ramo fechado */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #EDEDED;  /* Cor de fundo do cabe\u00e7alho */\n"
"    color: black;  /* Cor do texto do cabe\u00e7alho */\n"
"    padding: 4px;\n"
"    border: 1px solid #DCDCDC;  /* Borda do cabe\u00e7alho */\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    background-color: #EDEDED;\n"
"    width: 12px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background-color: #DCDCDC;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line"
                        ":vertical {\n"
"    background: none;\n"
"}\n"
"")

        self.gridLayout_48.addWidget(self.AgentViewDestilation_View, 1, 0, 1, 2)

        self.AgentViewDestilation_Selector = QComboBox(self.gridLayoutWidget_3)
        self.AgentViewDestilation_Selector.setObjectName(u"AgentViewDestilation_Selector")
        sizePolicy.setHeightForWidth(self.AgentViewDestilation_Selector.sizePolicy().hasHeightForWidth())
        self.AgentViewDestilation_Selector.setSizePolicy(sizePolicy)
        self.AgentViewDestilation_Selector.setMinimumSize(QSize(190, 23))
        self.AgentViewDestilation_Selector.setMaximumSize(QSize(190, 23))
        self.AgentViewDestilation_Selector.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 5px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 12px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_48.addWidget(self.AgentViewDestilation_Selector, 0, 1, 1, 1)

        self.myStackedWidget.addWidget(self.page_12)
        self.page_14 = QWidget()
        self.page_14.setObjectName(u"page_14")
        self.gridLayout_51 = QGridLayout(self.page_14)
        self.gridLayout_51.setObjectName(u"gridLayout_51")
        self.gridLayout_49 = QGridLayout()
        self.gridLayout_49.setObjectName(u"gridLayout_49")
        self.label_36 = QLabel(self.page_14)
        self.label_36.setObjectName(u"label_36")
        sizePolicy11.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy11)

        self.gridLayout_49.addWidget(self.label_36, 0, 0, 1, 1)

        self.AgentViewCode = QComboBox(self.page_14)
        self.AgentViewCode.setObjectName(u"AgentViewCode")
        sizePolicy.setHeightForWidth(self.AgentViewCode.sizePolicy().hasHeightForWidth())
        self.AgentViewCode.setSizePolicy(sizePolicy)
        self.AgentViewCode.setMinimumSize(QSize(190, 23))
        self.AgentViewCode.setMaximumSize(QSize(190, 23))
        self.AgentViewCode.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 5px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 12px;  /* Tamanho da fonte */\n"
"    padding: 5px 10px;  /* Espa\u00e7amento interno */\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    background-color: #EDEDED; /* Fundo ao passar o mouse */\n"
"}\n"
"\n"
"QComboBox:pressed {\n"
"    background-color: #DCDCDC; /* Fundo ao pressionar */\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    selection-background-color: #EDEDED;\n"
"    selection-color: black;\n"
"    border-radius: 10px;  /* Borda arredondada para a lista */\n"
"    font-size: 16px; /* Ajuste de fonte para itens */\n"
"}\n"
"")

        self.gridLayout_49.addWidget(self.AgentViewCode, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_49.addItem(self.horizontalSpacer_4, 0, 2, 1, 1)


        self.gridLayout_51.addLayout(self.gridLayout_49, 0, 0, 1, 1)

        self.sliddemenucodeeditor = QCustomSlideMenu(self.page_14)
        self.sliddemenucodeeditor.setObjectName(u"sliddemenucodeeditor")
        sizePolicy9.setHeightForWidth(self.sliddemenucodeeditor.sizePolicy().hasHeightForWidth())
        self.sliddemenucodeeditor.setSizePolicy(sizePolicy9)
        self.sliddemenucodeeditor.setMinimumSize(QSize(0, 0))
        self.sliddemenucodeeditor.setMaximumSize(QSize(16777215, 16777215))
        self.sliddemenucodeeditor.setStyleSheet(u"")
        self.gridLayout_50 = QGridLayout(self.sliddemenucodeeditor)
        self.gridLayout_50.setObjectName(u"gridLayout_50")
        self.widget_ViewAgent = QFrame(self.sliddemenucodeeditor)
        self.widget_ViewAgent.setObjectName(u"widget_ViewAgent")
        self.widget_ViewAgent.setMinimumSize(QSize(0, 630))
        self.widget_ViewAgent.setMaximumSize(QSize(16777215, 16777215))
        self.widget_ViewAgent.setStyleSheet(u"            QWidget {\n"
"                    \n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 1px;\n"
"                border-radius: 1px;\n"
"                background-color: #2f362e;\n"
"\n"
"            }")
        self.widget_ViewAgent.setFrameShape(QFrame.StyledPanel)
        self.widget_ViewAgent.setFrameShadow(QFrame.Raised)

        self.gridLayout_50.addWidget(self.widget_ViewAgent, 0, 0, 1, 1)


        self.gridLayout_51.addWidget(self.sliddemenucodeeditor, 1, 0, 1, 1)

        self.myStackedWidget.addWidget(self.page_14)

        self.gridLayout.addWidget(self.myStackedWidget, 1, 1, 2, 2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.myStackedWidget.setCurrentIndex(3)
        self.stackedWidget_instruction.setCurrentIndex(0)
        self.stackedWidget_SettingsCreate.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.close_window_button.setText("")
        self.restore_window_button.setText("")
        self.minimize_window_button.setText("")
        self.open_close_side_bar_btn.setText("")
        self.CreateAgents_menu.setText("")
        self.ViewCodeAgent.setText("")
        self.Editor_instructions.setText("")
        self.Editoragentkeysongithub.setText("")
        self.DestilationView.setText("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"SoftwareAI Agent", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Thread: ", None))
        self.CleanThread_Benchmark.setText("")
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"0 tokens", None))
        self.AtachFilesToThread_Benchmark.setText("")
        self.html_chat__Benchmark.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Chat....", None))
        self.mensage_input__Benchmark.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Enter Your Message...", None))
        self.Atachfiles_Benchmark.setText("")
        self.pushButton_3.setText("")
        self.send_mensage__Benchmark.setText("")
        self.Current_instuction_html_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Current Instruction", None))
        self.Add_new_instructions_button_edit.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Instruction", None))
        self.instruction_input_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"New Instruction...", None))
        self.change_instruction_button_edit.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Name For instruction", None))
        self.NameForInstruction_create.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Bob", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Instruction For Agent", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Instruction Category", None))
        self.BacktoEditinstruction_create.setText("")
        self.New_instruction_html_create.setPlaceholderText(QCoreApplication.translate("MainWindow", u"New Instruction...", None))
        self.CreateInstructionbutton_create.setText("")
        self.textEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Content Thread...", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Select Agent", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Select Thread", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Execution time", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Token consumption", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Initial Settings", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Name Agent", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Key In Firebase", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Agent Category", None))
        self.KeyInFirebase.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">AgentForPlanningDallas</p></body></html>", None))
        self.KeyInFirebase.setPlaceholderText(QCoreApplication.translate("MainWindow", u"AgentForPlanningDallas", None))
        self.NameAgent.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Dallas2</p></body></html>", None))
        self.NameAgent.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Dallas", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Model Select", None))
        self.label_28.setText(QCoreApplication.translate("MainWindow", u"Agent Keys Github", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Agent Keys OpenAI", None))
        self.ModelSelect.setItemText(0, QCoreApplication.translate("MainWindow", u"gpt-4o-mini-2024-07-18", None))
        self.ModelSelect.setItemText(1, QCoreApplication.translate("MainWindow", u"gpt-4o-2024-11-20", None))

        self.label_37.setText(QCoreApplication.translate("MainWindow", u"Agent Keys Firebase", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"Advanced Settings", None))
        self.PromptSettings.setText(QCoreApplication.translate("MainWindow", u"Prompt Settings", None))
        self.ArgumentsSettings.setText(QCoreApplication.translate("MainWindow", u"Arguments Settings", None))
        self.FunctionsSettings.setText(QCoreApplication.translate("MainWindow", u"Functions Settings", None))
        self.InstructionSettings.setText(QCoreApplication.translate("MainWindow", u"Instruction Settings", None))
        self.groupBox_13.setTitle(QCoreApplication.translate("MainWindow", u"Destilation Settings", None))
        self.StorageAgentOutput_.setText(QCoreApplication.translate("MainWindow", u"Store agent output and entries", None))
        self.StoreFormatJsonAndJsonl.setText(QCoreApplication.translate("MainWindow", u"Store Format json and jsonl", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"Store Format json", None))
        self.StorageAgentCompletions.setText(QCoreApplication.translate("MainWindow", u"Store Completions", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"Store Format jsonl", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"VectorStore", None))
        self.VectorstoreinThread.setPlaceholderText(QCoreApplication.translate("MainWindow", u"vs_USBolYuyy7cVX....", None))
        self.Vectorstoreinassistant.setPlaceholderText(QCoreApplication.translate("MainWindow", u"vs_USBolYuyy7cVX....", None))
#if QT_CONFIG(tooltip)
        self.UseVectorstoreToGenerateFiles.setToolTip(QCoreApplication.translate("MainWindow", u"When selecting you use vector storage in all files generated by the agent for example agent bob creates a .py that will be used by another dallas agent instead of dallas receiving all the text from the .py that bob created dallas simply receives the str from vectorstore with .py", None))
#endif // QT_CONFIG(tooltip)
        self.UseVectorstoreToGenerateFiles.setText(QCoreApplication.translate("MainWindow", u"Advanced Vectorstore", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Vectorstore in assistant", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Vectorstore in Thread", None))
        self.VectorstoreinThreadByUser.setText("")
        self.VectorstoreinassistantByUser.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Upload", None))
#if QT_CONFIG(tooltip)
        self.label_26.setToolTip(QCoreApplication.translate("MainWindow", u"maximum of 20 files", None))
#endif // QT_CONFIG(tooltip)
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Upload list \n"
"File for code interpreter \n"
"in Assistant", None))
#if QT_CONFIG(tooltip)
        self.textEdit_2.setToolTip(QCoreApplication.translate("MainWindow", u"maximum of 20 files", None))
#endif // QT_CONFIG(tooltip)
        self.textEdit_2.setPlaceholderText(QCoreApplication.translate("MainWindow", u"path/test.py,path/test2.txt", None))
        self.pushButton_7.setText("")
        self.Uploadlistfileforcodeinterpreterinthread.setPlaceholderText(QCoreApplication.translate("MainWindow", u"path/test.py,path/test2.txt", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"file in message", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"image for vision \n"
"in Thread", None))
        self.Upload1imageforvisioninThread.setPlaceholderText(QCoreApplication.translate("MainWindow", u"path/test.png", None))
        self.UploadlistfileforcodeinterpreterinthreadByUser.setText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"file in Thread", None))
        self.Upload1fileinmessage.setPlaceholderText(QCoreApplication.translate("MainWindow", u"path/test.py", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"List file\n"
"For code interpreter \n"
"in thread", None))
        self.Upload1fileinThread.setPlaceholderText(QCoreApplication.translate("MainWindow", u"path/test.py", None))
        self.Upload1fileinmessageByUser.setText("")
        self.Upload1fileinThreadByUser.setText("")
        self.Upload1imageforvisioninThreadByUser.setText("")
        self.CreateAgent.setText(QCoreApplication.translate("MainWindow", u"Build agent", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Prompt main", None))
#if QT_CONFIG(tooltip)
        self.Promptmain.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>If you are going to use advanced vector storage there is no need to reference the reading of the arguments with {read_path_...}, the advanced vector storage will upload the arguments to the openai vector store and then the agent is updated with the respective vector</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Promptmain.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Analise os quatro arquivos  relacionados ao projeto de software</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.Promptmain.setPlaceholderText("")
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"Prompt Rules", None))
        self.PromptRules.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.PromptRules.setPlaceholderText("")
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Sample response provided to the agent", None))
        self.PromptExample.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.PromptExample.setPlaceholderText("")
        self.BackToSettings.setText(QCoreApplication.translate("MainWindow", u"Back To Settings", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"Instructions", None))
        self.InstructionAgentCreate.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Seu nome \u00e9 SynthOperator, voc\u00ea \u00e9 um Analista de Requisitos de Software na empresa urobotsoftware. Sua fun\u00e7\u00e3o \u00e9 receber e analisar quatro arquivos relacionados a um projeto de software:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">1. **Roadmap**</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-in"
                        "dent:0px;\"><span style=\" font-size:8pt;\">2. **Cronograma do Projeto**</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">3. **Planilha do Projeto**</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">4. **Documento Pr\u00e9-Projeto**</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">### Responsabilidades:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">1. **Recep\u00e7\u00e3o dos Arquivos:**</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span styl"
                        "e=\" font-size:8pt;\">- Receber os quatro arquivos mencionados acima.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">- Garantir que todos os arquivos estejam completos e acess\u00edveis para an\u00e1lise.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">2. **An\u00e1lise dos Arquivos:**</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">- **Roadmap:** Identificar as principais etapas e objetivos de longo prazo do projeto.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">- **Cronograma do Projeto:** Examinar os prazos, marcos e cronolog"
                        "ia das atividades planejadas.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">- **Planilha do Projeto:** Avaliar a aloca\u00e7\u00e3o de recursos, or\u00e7amento e distribui\u00e7\u00e3o de tarefas.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">- **Documento Pr\u00e9-Projeto:** Extrair os requisitos iniciais, escopo do projeto e quaisquer restri\u00e7\u00f5es ou premissas estabelecidas.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">3. **Extra\u00e7\u00e3o e Organiza\u00e7\u00e3o das Informa\u00e7\u00f5es:**</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><spa"
                        "n style=\" font-size:8pt;\">- **Requisitos Funcionais:** Listar todas as funcionalidades que o software deve possuir.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">- **Requisitos N\u00e3o Funcionais:** Identificar aspectos como desempenho, seguran\u00e7a, usabilidade, etc.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">- **Depend\u00eancias:** Determinar rela\u00e7\u00f5es de depend\u00eancia entre diferentes tarefas ou m\u00f3dulos do projeto.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">- **Marcos:** Destacar os principais marcos e entreg\u00e1veis do projeto.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; mar"
                        "gin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">- **Recursos Necess\u00e1rios:** Identificar os recursos humanos, tecnol\u00f3gicos e financeiros necess\u00e1rios.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">- **Riscos:** Detectar poss\u00edveis riscos que possam impactar o sucesso do projeto e propor mitiga\u00e7\u00e3o.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">4. **Gera\u00e7\u00e3o do Relat\u00f3rio:**</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">- Organizar todas as informa\u00e7\u00f5es extra\u00eddas em uma estrutura clara e l\u00f3gica.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom"
                        ":12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">- Garantir que o relat\u00f3rio seja compreens\u00edvel para todas as partes interessadas.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">### Formato de Resposta:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Responda no formato JSON conforme o exemplo abaixo:</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">```json</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">{</span></p>\n"
"<p style=\" margin-top:12px; margin-bot"
                        "tom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;resumo&quot;: &quot;Resumo geral do projeto, destacando os objetivos principais e o escopo.&quot;,</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;requisitos_funcionais&quot;: [</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Requisito funcional 1&quot;,</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Requisito funcional 2&quot;,</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Requisito f"
                        "uncional 3&quot;</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">],</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;requisitos_nao_funcionais&quot;: [</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Requisito n\u00e3o funcional 1&quot;,</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Requisito n\u00e3o funcional 2&quot;,</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Requisito n\u00e3o f"
                        "uncional 3&quot;</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">],</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;dependencias&quot;: [</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Depend\u00eancia 1: Tarefa A depende da conclus\u00e3o da Tarefa B&quot;,</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Depend\u00eancia 2: M\u00f3dulo X depende da integra\u00e7\u00e3o com o M\u00f3dulo Y&quot;</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; "
                        "text-indent:0px;\"><span style=\" font-size:8pt;\">],</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;marcos&quot;: [</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Marco 1: Conclus\u00e3o do Design do Sistema&quot;,</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Marco 2: Finaliza\u00e7\u00e3o da Implementa\u00e7\u00e3o do M\u00f3dulo Principal&quot;,</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Marco 3: In\u00edcio dos Testes de Aceita\u00e7\u00e3o&quot;</span></p>\n"
"<p style=\" margin-top:12px; marg"
                        "in-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">],</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;recursos&quot;: [</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Recurso 1: Desenvolvedores Front-end&quot;,</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Recurso 2: Servidores de Teste&quot;,</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Recurso 3: Or\u00e7amento para Ferramentas de Desenvolvimento&quot;</span></p>\n"
"<p style=\" m"
                        "argin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">],</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;riscos&quot;: [</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Risco 1: Atrasos na entrega devido \u00e0 falta de recursos&quot;,</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Risco 2: Falhas de seguran\u00e7a no software final&quot;,</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">&quot;Risco 3: Mudan\u00e7as nos requisi"
                        "tos do cliente durante o desenvolvimento&quot;</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">]</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">}</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>", None))
        self.InstructionAgentCreate.setPlaceholderText("")
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Aditional Instructions", None))
        self.AditionalInstructionsAgentCreate.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Instru\u00e7\u00f5es Adicionais:\\n</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Precis\u00e3o: Assegure-se de que todas as informa\u00e7\u00f5es sejam precisas e derivadas diretamente dos arquivos analisados.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">\\n</span></p>\n"
"<p"
                        " style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Clareza: Utilize uma linguagem clara e concisa para facilitar a compreens\u00e3o.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">\\n</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Estrutura\u00e7\u00e3o: Mantenha a estrutura do JSON organizada, utilizando listas para categorias que contenham m\u00faltiplos itens.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">\\n</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\""
                        "><span style=\" font-size:8pt;\">Completude: Verifique se todas as \u00e1reas relevantes foram cobertas e nenhuma informa\u00e7\u00e3o importante foi omitida.</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">\\n</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Consist\u00eancia: Mantenha a consist\u00eancia no formato e na nomenclatura utilizada no JSON.</span></p></body></html>", None))
        self.AditionalInstructionsAgentCreate.setPlaceholderText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Back To Settings", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("MainWindow", u"Agent Tools", None))
        self.AgentTools.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1e1e1e;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#d4d4d4;\">{</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;type&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#d4d4d4;\">: </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;file_search&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt"
                        "; color:#d4d4d4;\">},</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">{</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc; background-color:#1f1f1f;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-siz"
                        "e:8pt; color:#ce9178;\">&quot;type&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">: </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;function&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;function&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">: {</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Co"
                        "nsolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;name&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">: </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;</span><span style=\" font-size:8pt;\">pegar_hora</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; "
                        "font-size:8pt; color:#ce9178;\">&quot;description&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">: </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;Retorna a data e hora atual no formato YYYY-MM-DD HH:MM:SS.&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;parameters&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">: {</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -"
                        "qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;type&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">: </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;object&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;properties&quot;</span><span style=\""
                        " font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">: {},</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;required&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">: []</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 }</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consola"
                        "s,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 }</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0} 	</span></p></body></html>", None))
        self.AgentTools.setPlaceholderText("")
        self.groupBox_11.setTitle(QCoreApplication.translate("MainWindow", u"Function Python", None))
        self.namefunction_agentcreate.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">pegar_hora</span></p></body></html>", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Name", None))
        self.FunctionPython.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">def pegar_hora():</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">     import datetime</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">     current_datetime = datetime.datetime.now()</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; "
                        "-qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">     formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">     return f&quot;{formatted_datetime}&quot;</span></p></body></html>", None))
        self.groupBox_12.setTitle(QCoreApplication.translate("MainWindow", u"Function Python Output", None))
        self.FunctionPythonOutput.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; line-height:19px; background-color:#1f1f1f;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#569cd6;\">def</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#dcdcaa;\">submit_output_</span><span style=\" font-size:8pt;\">pegar_hora</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">(</span><span style=\" font-family:'Consolas,Courier New"
                        ",monospace'; font-size:8pt; color:#9cdcfe;\">function_name</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">function_arguments</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0"
                        " \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">tool_call</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">threead_id</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0"
                        " \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">client</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">run</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 ):"
                        "</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#569cd6;\">global</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">tool_outputs</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#c586c0;\">if</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span st"
                        "yle=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">function_name</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#d4d4d4;\">==</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">'</span><span style=\" font-size:8pt;\">pegar_hora</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">'</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 </span><span "
                        "style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">resultado</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#d4d4d4;\">=</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#dcdcaa;\">get_current_datetime</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">()</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">tool_outputs</span><span style=\" font-family:"
                        "'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">.</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#dcdcaa;\">append</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">({</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;tool_call_id&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">: </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">tool_call</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">.id,</span></p>\n"
"<p style=\" margin-top:0px; margin-bo"
                        "ttom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;output&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">: </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">resultado</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 })</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0"
                        " \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#6a9955;\"># Submit all tool outputs at once after collecting them in a list</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#c586c0;\">if</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">tool_outputs</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Cour"
                        "ier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#c586c0;\">try</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">run</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#d4d4d4;\">=</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span style=\" font-family:'Consolas,Courier New,monospa"
                        "ce'; font-size:8pt; color:#9cdcfe;\">client</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">.beta.threads.runs.submit_tool_outputs_and_poll(</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">thread_id</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#d4d4d4;\">=</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">threead_id</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><spa"
                        "n style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">run_id</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#d4d4d4;\">=</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">run</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">.id,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">tool_outputs</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#d4d4d4"
                        ";\">=</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">tool_outputs</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 )</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#dcdcaa;\">print</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">(</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;Tool outputs submitted successfully.&quot;</span><s"
                        "pan style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">tool_outputs</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#d4d4d4;\">=</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> []</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 "
                        "\u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#c586c0;\">return</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#569cd6;\">True</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#c586c0;\">except</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#4ec9b0;\">Exception</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><spa"
                        "n style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#c586c0;\">as</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\"> </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">e</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#dcdcaa;\">print</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">(</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;Failed to submit tool outputs:&quot;</span><spa"
                        "n style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">, </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#9cdcfe;\">e</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">)</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 </span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#c586c0;\">else</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">:</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">\u00a0 \u00a0 \u00a0 \u00a0 </span><span style=\" fon"
                        "t-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#dcdcaa;\">print</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">(</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#ce9178;\">&quot;No tool outputs to submit.&quot;</span><span style=\" font-family:'Consolas,Courier New,monospace'; font-size:8pt; color:#cccccc;\">)</span></p></body></html>", None))
        self.FunctionPythonOutput.setPlaceholderText("")
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Back To Settings", None))
#if QT_CONFIG(tooltip)
        self.ArgsCreatetextedit.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>When creating arguments for your agent you can reference the arguments in the message sent to openai, this means you can pass a document to the agent and mention it in the main message of the prompt like {arg}</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ArgsCreatetextedit.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Arial'; font-size:14px; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">pathRoadmap, cronograma, planilha, PreProjeto</span></p></body></html>", None))
        self.ArgsCreatetextedit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"pathRoadmap, cronograma, planilha, PreProjeto", None))
#if QT_CONFIG(tooltip)
        self.label_18.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>When creating arguments for your agent you can reference the arguments in the message sent to openai, this means you can pass a document to the agent and mention it in the main message of the prompt like {arg}</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Args to call agent", None))
        self.CurrentArgs_AgentCreate.setItemText(0, QCoreApplication.translate("MainWindow", u"txt", None))
        self.CurrentArgs_AgentCreate.setItemText(1, QCoreApplication.translate("MainWindow", u"py", None))

        self.label_17.setText(QCoreApplication.translate("MainWindow", u"the Args will be of the type", None))
        self.BacktoEditinstruction_create_2.setText(QCoreApplication.translate("MainWindow", u"Back To Settings", None))
        self.card1.setTitle(QCoreApplication.translate("MainWindow", u"OpenAI keys", None))
        self.openaitoken_AgentKeys.setPlaceholderText(QCoreApplication.translate("MainWindow", u"OpenAI token", None))
        self.label_31.setText(QCoreApplication.translate("MainWindow", u"Key:", None))
        self.label_30.setText(QCoreApplication.translate("MainWindow", u"Name For Key", None))
        self.openainamefortoken_AgentKeys.setPlaceholderText(QCoreApplication.translate("MainWindow", u"CompanyToken1", None))
        self.createkeyopenai_AgentKeys.setText(QCoreApplication.translate("MainWindow", u"Create Key", None))
        self.card2.setTitle(QCoreApplication.translate("MainWindow", u"Git Hub keys", None))
        self.githuusername_AgentKeys.setPlaceholderText(QCoreApplication.translate("MainWindow", u"github username", None))
        self.githubtoken_AgentKeys.setPlaceholderText(QCoreApplication.translate("MainWindow", u"github token", None))
        self.createkeygithub_AgentKeys.setText(QCoreApplication.translate("MainWindow", u"Create Key", None))
        self.card3.setTitle(QCoreApplication.translate("MainWindow", u"Firebase keys", None))
        self.label_32.setText(QCoreApplication.translate("MainWindow", u"DatabaseURL", None))
        self.credentialsapp_AgentKeys.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Credentials App", None))
        self.label_29.setText(QCoreApplication.translate("MainWindow", u"Key App", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"App Name", None))
        self.createkeysfirebase_AgentKeys.setText(QCoreApplication.translate("MainWindow", u"Create Key", None))
        self.uploadcredentialapp_AgentKeys.setText("")
        self.appname_AgentKeys.setPlaceholderText(QCoreApplication.translate("MainWindow", u"AppCompany1", None))
        self.label_33.setText(QCoreApplication.translate("MainWindow", u"StorageBucket", None))
        self.Databaseurl_AgentKeys.setPlaceholderText(QCoreApplication.translate("MainWindow", u"https://app.firebaseio.com", None))
        self.Storagebucket_AgentKeys.setPlaceholderText(QCoreApplication.translate("MainWindow", u"App.appspot.com", None))
        self.label_35.setText(QCoreApplication.translate("MainWindow", u"Select Agent For View Destilation", None))
        self.label_36.setText(QCoreApplication.translate("MainWindow", u"Select Agent For View Code", None))
    # retranslateUi

