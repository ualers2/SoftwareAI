# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_cliente_and_chat.ui'
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
        MainWindow.resize(754, 788)
        MainWindow.setMinimumSize(QSize(718, 500))
        MainWindow.setMaximumSize(QSize(838, 971))
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_9 = QGridLayout(self.centralwidget)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.stackedWidget_2 = QCustomQStackedWidget(self.centralwidget)
        self.stackedWidget_2.setObjectName(u"stackedWidget_2")
        self.stackedWidget_2.setMinimumSize(QSize(0, 0))
        self.stackedWidget_2.setStyleSheet(u"*{\n"
"	border: none;\n"
"}")
        self.stackedWidget_2.setFrameShape(QFrame.NoFrame)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.gridLayout_3 = QGridLayout(self.page_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_4 = QFrame(self.page_4)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setStyleSheet(u"background-color: white;")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_15 = QGridLayout(self.frame_4)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.pushButton_16 = QCustomQPushButton(self.frame_4)
        self.pushButton_16.setObjectName(u"pushButton_16")
        icon = QIcon()
        icon.addFile(u":/font_awesome_solid/icons/font_awesome/solid/list.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_16.setIcon(icon)

        self.gridLayout_15.addWidget(self.pushButton_16, 0, 1, 1, 1)

        self.gridLayout_14 = QGridLayout()
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.close_window_button = QPushButton(self.frame_4)
        self.close_window_button.setObjectName(u"close_window_button")
        icon1 = QIcon()
        icon1.addFile(u":/feather/icons/feather/window_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.close_window_button.setIcon(icon1)

        self.gridLayout_14.addWidget(self.close_window_button, 0, 1, 1, 1)

        self.minimize_window_button = QPushButton(self.frame_4)
        self.minimize_window_button.setObjectName(u"minimize_window_button")
        icon2 = QIcon()
        icon2.addFile(u":/feather/icons/feather/window_minimize.png", QSize(), QIcon.Normal, QIcon.Off)
        self.minimize_window_button.setIcon(icon2)

        self.gridLayout_14.addWidget(self.minimize_window_button, 0, 2, 1, 1)

        self.restore_window_button = QPushButton(self.frame_4)
        self.restore_window_button.setObjectName(u"restore_window_button")
        icon3 = QIcon()
        icon3.addFile(u":/feather/icons/feather/maximize-2.png", QSize(), QIcon.Normal, QIcon.Off)
        self.restore_window_button.setIcon(icon3)
        self.restore_window_button.setIconSize(QSize(16, 16))

        self.gridLayout_14.addWidget(self.restore_window_button, 0, 3, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)


        self.gridLayout_15.addLayout(self.gridLayout_14, 0, 3, 1, 1)

        self.line_2 = QFrame(self.frame_4)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.gridLayout_15.addWidget(self.line_2, 1, 0, 2, 2)

        self.line_6 = QFrame(self.frame_4)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setMinimumSize(QSize(0, 0))
        self.line_6.setFrameShape(QFrame.VLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.gridLayout_15.addWidget(self.line_6, 1, 2, 2, 1)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setHorizontalSpacing(1)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setContentsMargins(1, 0, 1, 1)
        self.send_mensage = QCustomQPushButton(self.frame_4)
        self.send_mensage.setObjectName(u"send_mensage")
        self.send_mensage.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 13px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        icon4 = QIcon()
        icon4.addFile(u":/feather/icons/feather/send.png", QSize(), QIcon.Normal, QIcon.Off)
        self.send_mensage.setIcon(icon4)
        self.send_mensage.setIconSize(QSize(27, 47))

        self.gridLayout_4.addWidget(self.send_mensage, 5, 5, 1, 1)

        self.atach_file = QCustomQPushButton(self.frame_4)
        self.atach_file.setObjectName(u"atach_file")
        self.atach_file.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 13px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        icon5 = QIcon()
        icon5.addFile(u":/font_awesome_solid/icons/font_awesome/solid/file-arrow-down.png", QSize(), QIcon.Normal, QIcon.Off)
        self.atach_file.setIcon(icon5)
        self.atach_file.setIconSize(QSize(22, 47))

        self.gridLayout_4.addWidget(self.atach_file, 5, 7, 1, 1)

        self.pushButton_6 = QCustomQPushButton(self.frame_4)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 13px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        icon6 = QIcon()
        icon6.addFile(u":/feather/icons/feather/mic.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_6.setIcon(icon6)
        self.pushButton_6.setIconSize(QSize(27, 47))

        self.gridLayout_4.addWidget(self.pushButton_6, 5, 6, 1, 1)

        self.openLousa = QPushButton(self.frame_4)
        self.openLousa.setObjectName(u"openLousa")
        icon7 = QIcon()
        icon7.addFile(u":/font_awesome_solid/icons/font_awesome/solid/code.png", QSize(), QIcon.Normal, QIcon.Off)
        self.openLousa.setIcon(icon7)
        self.openLousa.setIconSize(QSize(27, 47))

        self.gridLayout_4.addWidget(self.openLousa, 5, 4, 1, 1)

        self.mensage_input = QTextEdit(self.frame_4)
        self.mensage_input.setObjectName(u"mensage_input")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mensage_input.sizePolicy().hasHeightForWidth())
        self.mensage_input.setSizePolicy(sizePolicy)
        self.mensage_input.setMinimumSize(QSize(0, 48))
        self.mensage_input.setMaximumSize(QSize(16777215, 48))
        self.mensage_input.setStyleSheet(u"            QTextEdit {\n"
"                border: 1px solid #E0E0E0;\n"
"                padding: 10px;\n"
"                border-radius: 10px;\n"
"                background-color: #F7F7F7;\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"            }")
        self.mensage_input.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mensage_input.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.gridLayout_4.addWidget(self.mensage_input, 5, 0, 1, 4)

        self.gridLayout_33 = QGridLayout()
        self.gridLayout_33.setObjectName(u"gridLayout_33")
        self.gridLayout_33.setContentsMargins(8, 0, 7, -1)
        self.label_19 = QLabel(self.frame_4)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setMinimumSize(QSize(612, 0))
        self.label_19.setMaximumSize(QSize(609, 16777215))

        self.gridLayout_33.addWidget(self.label_19, 0, 0, 1, 1)

        self.label_20 = QLabel(self.frame_4)
        self.label_20.setObjectName(u"label_20")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy1)

        self.gridLayout_33.addWidget(self.label_20, 0, 1, 1, 1)

        self.AtachFilesToThread_Benchmark = QCustomQPushButton(self.frame_4)
        self.AtachFilesToThread_Benchmark.setObjectName(u"AtachFilesToThread_Benchmark")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.AtachFilesToThread_Benchmark.sizePolicy().hasHeightForWidth())
        self.AtachFilesToThread_Benchmark.setSizePolicy(sizePolicy2)
        self.AtachFilesToThread_Benchmark.setStyleSheet(u"            QPushButton {\n"
"                background-color: white;\n"
"\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 16px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"\n"
"")
        icon8 = QIcon()
        icon8.addFile(u":/font_awesome_solid/icons/font_awesome/solid/database.png", QSize(), QIcon.Normal, QIcon.Off)
        self.AtachFilesToThread_Benchmark.setIcon(icon8)
        self.AtachFilesToThread_Benchmark.setIconSize(QSize(19, 18))

        self.gridLayout_33.addWidget(self.AtachFilesToThread_Benchmark, 0, 3, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_33, 2, 0, 1, 8)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)
        self.label_5.setMinimumSize(QSize(92, 0))
        self.label_5.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_4.addWidget(self.label_5, 0, 0, 1, 1)

        self.widget_2 = QWidget(self.frame_4)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(0, 180))
        self.gridLayout_13 = QGridLayout(self.widget_2)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.html_chat = QTextEdit(self.widget_2)
        self.html_chat.setObjectName(u"html_chat")
        self.html_chat.setMinimumSize(QSize(200, 0))
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

        self.gridLayout_13.addWidget(self.html_chat, 0, 0, 1, 1)

        self.sliddemenulousa = QCustomSlideMenu(self.widget_2)
        self.sliddemenulousa.setObjectName(u"sliddemenulousa")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.sliddemenulousa.sizePolicy().hasHeightForWidth())
        self.sliddemenulousa.setSizePolicy(sizePolicy3)
        self.sliddemenulousa.setMinimumSize(QSize(0, 0))
        self.sliddemenulousa.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout_8 = QGridLayout(self.sliddemenulousa)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.widget_lousa = QFrame(self.sliddemenulousa)
        self.widget_lousa.setObjectName(u"widget_lousa")
        self.widget_lousa.setMinimumSize(QSize(0, 0))
        self.widget_lousa.setMaximumSize(QSize(16777215, 16777215))
        self.widget_lousa.setStyleSheet(u"")
        self.widget_lousa.setFrameShape(QFrame.StyledPanel)
        self.widget_lousa.setFrameShadow(QFrame.Raised)

        self.gridLayout_8.addWidget(self.widget_lousa, 0, 0, 1, 1)


        self.gridLayout_13.addWidget(self.sliddemenulousa, 0, 1, 1, 1)


        self.gridLayout_4.addWidget(self.widget_2, 3, 0, 1, 8)

        self.SoftwareAIAgentsChat = QComboBox(self.frame_4)
        self.SoftwareAIAgentsChat.setObjectName(u"SoftwareAIAgentsChat")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.SoftwareAIAgentsChat.sizePolicy().hasHeightForWidth())
        self.SoftwareAIAgentsChat.setSizePolicy(sizePolicy4)
        self.SoftwareAIAgentsChat.setMinimumSize(QSize(0, 0))
        self.SoftwareAIAgentsChat.setMaximumSize(QSize(16777215, 16777215))
        self.SoftwareAIAgentsChat.setStyleSheet(u"QComboBox {\n"
"    background-color: #F7F7F7;\n"
"    border: 1px solid #E0E0E0;\n"
"    border-radius: 13px;  /* Borda arredondada */\n"
"    color: black;  /* Cor do texto */\n"
"    font-size: 13px;  /* Tamanho da fonte */\n"
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

        self.gridLayout_4.addWidget(self.SoftwareAIAgentsChat, 0, 2, 1, 6)


        self.gridLayout_15.addLayout(self.gridLayout_4, 1, 3, 4, 1)

        self.widget = QCustomSlideMenu(self.frame_4)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(50, 698))
        self.widget.setMaximumSize(QSize(50, 698))
        self.gridLayout_10 = QGridLayout(self.widget)
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.view_threads = QCustomQPushButton(self.widget)
        self.view_threads.setObjectName(u"view_threads")
        self.view_threads.setMaximumSize(QSize(90, 30))
        self.view_threads.setStyleSheet(u"            QPushButton {\n"
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
"            }")
        icon9 = QIcon()
        icon9.addFile(u":/feather/icons/feather/activity.png", QSize(), QIcon.Normal, QIcon.Off)
        self.view_threads.setIcon(icon9)
        self.view_threads.setIconSize(QSize(24, 24))

        self.gridLayout_11.addWidget(self.view_threads, 1, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_11.addItem(self.verticalSpacer_3, 2, 0, 1, 1)

        self.settings_agent = QCustomQPushButton(self.widget)
        self.settings_agent.setObjectName(u"settings_agent")
        self.settings_agent.setMinimumSize(QSize(0, 0))
        self.settings_agent.setMaximumSize(QSize(90, 30))
        self.settings_agent.setStyleSheet(u"            QPushButton {\n"
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
"            }")
        icon10 = QIcon()
        icon10.addFile(u":/feather/icons/feather/settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.settings_agent.setIcon(icon10)
        self.settings_agent.setIconSize(QSize(24, 24))

        self.gridLayout_11.addWidget(self.settings_agent, 0, 0, 1, 1)


        self.gridLayout_10.addLayout(self.gridLayout_11, 1, 0, 1, 1)


        self.gridLayout_15.addWidget(self.widget, 2, 1, 1, 1)

        self.line_3 = QFrame(self.frame_4)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.gridLayout_15.addWidget(self.line_3, 3, 1, 1, 2)

        self.line_6.raise_()
        self.line_2.raise_()
        self.line_3.raise_()
        self.pushButton_16.raise_()
        self.widget.raise_()

        self.gridLayout_3.addWidget(self.frame_4, 1, 0, 1, 1)

        self.stackedWidget_2.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.gridLayout_7 = QGridLayout(self.page_5)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.frame_5 = QFrame(self.page_5)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setStyleSheet(u"background-color: white;")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_4 = QSpacerItem(20, 181, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.gridLayout.addItem(self.verticalSpacer_4, 2, 2, 1, 1)

        self.gridLayout_47 = QGridLayout()
        self.gridLayout_47.setObjectName(u"gridLayout_47")
        self.gridLayout_47.setContentsMargins(-1, -1, 158, -1)
        self.StorageAgentOutput_ = QCheckBox(self.frame_5)
        self.StorageAgentOutput_.setObjectName(u"StorageAgentOutput_")
        self.StorageAgentOutput_.setChecked(True)

        self.gridLayout_47.addWidget(self.StorageAgentOutput_, 3, 0, 1, 2)

        self.StorageAgentCompletions = QCheckBox(self.frame_5)
        self.StorageAgentCompletions.setObjectName(u"StorageAgentCompletions")
        self.StorageAgentCompletions.setChecked(True)

        self.gridLayout_47.addWidget(self.StorageAgentCompletions, 2, 0, 1, 2)

        self.radioButton = QRadioButton(self.frame_5)
        self.radioButton.setObjectName(u"radioButton")

        self.gridLayout_47.addWidget(self.radioButton, 5, 0, 1, 1)

        self.StoreFormatJsonAndJsonl = QRadioButton(self.frame_5)
        self.StoreFormatJsonAndJsonl.setObjectName(u"StoreFormatJsonAndJsonl")
        self.StoreFormatJsonAndJsonl.setChecked(True)

        self.gridLayout_47.addWidget(self.StoreFormatJsonAndJsonl, 4, 0, 1, 1)

        self.label_34 = QLabel(self.frame_5)
        self.label_34.setObjectName(u"label_34")

        self.gridLayout_47.addWidget(self.label_34, 0, 0, 1, 1)

        self.radioButton_2 = QRadioButton(self.frame_5)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.gridLayout_47.addWidget(self.radioButton_2, 6, 0, 1, 1)

        self.AgentKeysOpenAI = QComboBox(self.frame_5)
        self.AgentKeysOpenAI.setObjectName(u"AgentKeysOpenAI")
        sizePolicy5 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.AgentKeysOpenAI.sizePolicy().hasHeightForWidth())
        self.AgentKeysOpenAI.setSizePolicy(sizePolicy5)
        self.AgentKeysOpenAI.setMinimumSize(QSize(0, 0))
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

        self.gridLayout_47.addWidget(self.AgentKeysOpenAI, 0, 1, 1, 1)

        self.verticalSpacer_14 = QSpacerItem(20, 202, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_47.addItem(self.verticalSpacer_14, 7, 0, 1, 2)

        self.label_4 = QLabel(self.frame_5)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_47.addWidget(self.label_4, 1, 0, 1, 1)

        self.AgentKeysFirebase = QComboBox(self.frame_5)
        self.AgentKeysFirebase.setObjectName(u"AgentKeysFirebase")
        sizePolicy5.setHeightForWidth(self.AgentKeysFirebase.sizePolicy().hasHeightForWidth())
        self.AgentKeysFirebase.setSizePolicy(sizePolicy5)
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

        self.gridLayout_47.addWidget(self.AgentKeysFirebase, 1, 1, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_47, 1, 0, 1, 3)

        self.pushButton_5 = QPushButton(self.frame_5)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout.addWidget(self.pushButton_5, 0, 1, 1, 1)


        self.gridLayout_7.addWidget(self.frame_5, 0, 0, 1, 1)

        self.stackedWidget_2.addWidget(self.page_5)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_12 = QGridLayout(self.page)
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.frame_6 = QFrame(self.page)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setStyleSheet(u"background-color: white;")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.line_5 = QFrame(self.frame_6)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setGeometry(QRect(20, 320, 233, 3))
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)
        self.line_7 = QFrame(self.frame_6)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setGeometry(QRect(300, 220, 79, 3))
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)
        self.line_4 = QFrame(self.frame_6)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setGeometry(QRect(300, 229, 79, 3))
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.line = QFrame(self.frame_6)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(300, 238, 79, 3))
        self.line.setMinimumSize(QSize(0, 0))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.widget_3 = QWidget(self.frame_6)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setGeometry(QRect(20, 20, 271, 231))
        self.gridLayout_35 = QGridLayout(self.widget_3)
        self.gridLayout_35.setObjectName(u"gridLayout_35")
        self.frame = QFrame(self.widget_3)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(226, 0))
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalSpacer = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer, 1, 0, 1, 1)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setFamily(u"Microsoft Sans Serif")
        self.label.setFont(font)
        self.label.setStyleSheet(u"\n"
"QWidget {\n"
"\n"
"                color: #7a7978;  /* Cor do texto preto */\n"
"}\n"
"\n"
"")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 2)

        self.line_15 = QFrame(self.frame)
        self.line_15.setObjectName(u"line_15")
        self.line_15.setStyleSheet(u"\n"
"QWidget {\n"
"\n"
"                background: #dee0df;  /* Cor do texto preto */\n"
"}\n"
"\n"
"")
        self.line_15.setFrameShape(QFrame.HLine)
        self.line_15.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_15, 3, 0, 1, 2)

        self.line_16 = QFrame(self.frame)
        self.line_16.setObjectName(u"line_16")
        self.line_16.setStyleSheet(u"\n"
"QWidget {\n"
"\n"
"                background: #dee0df;  /* Cor do texto preto */\n"
"}\n"
"\n"
"")
        self.line_16.setFrameShape(QFrame.HLine)
        self.line_16.setFrameShadow(QFrame.Sunken)

        self.gridLayout_2.addWidget(self.line_16, 5, 0, 1, 2)

        self.pushButton_3 = QPushButton(self.frame)
        self.pushButton_3.setObjectName(u"pushButton_3")
        sizePolicy2.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy2)
        self.pushButton_3.setStyleSheet(u"            QPushButton {\n"
"                background-color: #dbd9d9;\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 11px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        icon11 = QIcon()
        icon11.addFile(u":/material_design/icons/material_design/add.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_3.setIcon(icon11)
        self.pushButton_3.setIconSize(QSize(38, 28))

        self.gridLayout_2.addWidget(self.pushButton_3, 4, 1, 1, 1)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setStyleSheet(u"")

        self.gridLayout_2.addWidget(self.label_3, 4, 0, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_2, 0, 0, 1, 1)


        self.gridLayout_35.addWidget(self.frame, 0, 0, 1, 1)

        self.widget_4 = QWidget(self.frame_6)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setGeometry(QRect(60, 300, 271, 231))
        self.gridLayout_36 = QGridLayout(self.widget_4)
        self.gridLayout_36.setObjectName(u"gridLayout_36")
        self.frame_2 = QFrame(self.widget_4)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(226, 0))
        self.frame_2.setMaximumSize(QSize(16777215, 16777215))
        self.frame_2.setStyleSheet(u"")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_2)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_37 = QGridLayout()
        self.gridLayout_37.setObjectName(u"gridLayout_37")
        self.label_12 = QLabel(self.frame_2)
        self.label_12.setObjectName(u"label_12")
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setStyleSheet(u"")

        self.gridLayout_37.addWidget(self.label_12, 8, 0, 1, 1)

        self.line_17 = QFrame(self.frame_2)
        self.line_17.setObjectName(u"line_17")
        self.line_17.setStyleSheet(u"\n"
"QWidget {\n"
"\n"
"                background: #dee0df;  /* Cor do texto preto */\n"
"}\n"
"\n"
"")
        self.line_17.setFrameShape(QFrame.HLine)
        self.line_17.setFrameShadow(QFrame.Sunken)

        self.gridLayout_37.addWidget(self.line_17, 5, 0, 1, 2)

        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setStyleSheet(u"")

        self.gridLayout_37.addWidget(self.label_9, 6, 0, 1, 1)

        self.pushButton_7 = QPushButton(self.frame_2)
        self.pushButton_7.setObjectName(u"pushButton_7")
        sizePolicy2.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy2)
        self.pushButton_7.setStyleSheet(u"            QPushButton {\n"
"                background-color: #dbd9d9;\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 11px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        self.pushButton_7.setIcon(icon11)
        self.pushButton_7.setIconSize(QSize(38, 28))

        self.gridLayout_37.addWidget(self.pushButton_7, 4, 1, 1, 1)

        self.pushButton_8 = QPushButton(self.frame_2)
        self.pushButton_8.setObjectName(u"pushButton_8")
        sizePolicy2.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy2)
        self.pushButton_8.setStyleSheet(u"            QPushButton {\n"
"                background-color: #dbd9d9;\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 11px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        self.pushButton_8.setIcon(icon11)
        self.pushButton_8.setIconSize(QSize(38, 28))

        self.gridLayout_37.addWidget(self.pushButton_8, 6, 1, 1, 1)

        self.label_10 = QLabel(self.frame_2)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setStyleSheet(u"")

        self.gridLayout_37.addWidget(self.label_10, 4, 0, 1, 1)

        self.label_11 = QLabel(self.frame_2)
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setFont(font)
        self.label_11.setStyleSheet(u"\n"
"QWidget {\n"
"\n"
"                color: #7a7978;  /* Cor do texto preto */\n"
"}\n"
"\n"
"")

        self.gridLayout_37.addWidget(self.label_11, 0, 0, 1, 2)

        self.line_18 = QFrame(self.frame_2)
        self.line_18.setObjectName(u"line_18")
        self.line_18.setStyleSheet(u"\n"
"QWidget {\n"
"\n"
"                background: #dee0df;  /* Cor do texto preto */\n"
"}\n"
"\n"
"")
        self.line_18.setFrameShape(QFrame.HLine)
        self.line_18.setFrameShadow(QFrame.Sunken)

        self.gridLayout_37.addWidget(self.line_18, 3, 0, 1, 2)

        self.verticalSpacer_2 = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_37.addItem(self.verticalSpacer_2, 1, 0, 1, 1)

        self.line_19 = QFrame(self.frame_2)
        self.line_19.setObjectName(u"line_19")
        self.line_19.setStyleSheet(u"\n"
"QWidget {\n"
"\n"
"                background: #dee0df;  /* Cor do texto preto */\n"
"}\n"
"\n"
"")
        self.line_19.setFrameShape(QFrame.HLine)
        self.line_19.setFrameShadow(QFrame.Sunken)

        self.gridLayout_37.addWidget(self.line_19, 7, 0, 1, 2)

        self.pushButton = QPushButton(self.frame_2)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy2.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy2)
        self.pushButton.setStyleSheet(u"            QPushButton {\n"
"                background-color: #dbd9d9;\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 11px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        self.pushButton.setIcon(icon11)
        self.pushButton.setIconSize(QSize(38, 28))

        self.gridLayout_37.addWidget(self.pushButton, 8, 1, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_37, 0, 0, 1, 1)


        self.gridLayout_36.addWidget(self.frame_2, 0, 0, 1, 1)

        self.label_2 = QLabel(self.frame_6)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(290, 240, 185, 28))
        self.label_2.setStyleSheet(u"")
        self.pushButton_4 = QPushButton(self.frame_6)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setGeometry(QRect(400, 240, 42, 28))
        sizePolicy2.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy2)
        self.pushButton_4.setStyleSheet(u"            QPushButton {\n"
"                background-color: #dbd9d9;\n"
"                border-radius: 13px;  /* Borda arredondada (c\u00edrculo) */\n"
"                color: black;  /* Cor do texto alterada para preto */\n"
"                font-size: 11px;  /* Ajuste do tamanho do \u00edcone */\n"
"            }\n"
"")
        self.pushButton_4.setIcon(icon11)
        self.pushButton_4.setIconSize(QSize(38, 28))

        self.gridLayout_12.addWidget(self.frame_6, 0, 0, 1, 1)

        self.stackedWidget_2.addWidget(self.page)

        self.gridLayout_9.addWidget(self.stackedWidget_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget_2.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"Menu", None))
        self.close_window_button.setText("")
        self.minimize_window_button.setText("")
        self.restore_window_button.setText("")
#if QT_CONFIG(tooltip)
        self.send_mensage.setToolTip(QCoreApplication.translate("MainWindow", u"Send message to agent", None))
#endif // QT_CONFIG(tooltip)
        self.send_mensage.setText("")
#if QT_CONFIG(tooltip)
        self.atach_file.setToolTip(QCoreApplication.translate("MainWindow", u"Send files to the agent", None))
#endif // QT_CONFIG(tooltip)
        self.atach_file.setText("")
#if QT_CONFIG(tooltip)
        self.pushButton_6.setToolTip(QCoreApplication.translate("MainWindow", u"Chat via voice chat with an agent", None))
#endif // QT_CONFIG(tooltip)
        self.pushButton_6.setText("")
        self.openLousa.setText("")
        self.mensage_input.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Message...", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Thread: ", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"0 tokens", None))
        self.AtachFilesToThread_Benchmark.setText("")
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"SoftwareAI Agent:", None))
        self.html_chat.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Arial'; font-size:14px; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.view_threads.setText("")
        self.settings_agent.setText("")
        self.StorageAgentOutput_.setText(QCoreApplication.translate("MainWindow", u"Store agent output and entries", None))
        self.StorageAgentCompletions.setText(QCoreApplication.translate("MainWindow", u"Store Completions", None))
        self.radioButton.setText(QCoreApplication.translate("MainWindow", u"Store Format json", None))
        self.StoreFormatJsonAndJsonl.setText(QCoreApplication.translate("MainWindow", u"Store Format json and jsonl", None))
        self.label_34.setText(QCoreApplication.translate("MainWindow", u"Agent Keys OpenAI:", None))
        self.radioButton_2.setText(QCoreApplication.translate("MainWindow", u"Store Format jsonl", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Agent Keys Firebase", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Back to home", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Thread's files", None))
        self.pushButton_3.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"File search", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"image for vision", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Code interpreter", None))
        self.pushButton_7.setText("")
        self.pushButton_8.setText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"File search", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Mensage files", None))
        self.pushButton.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Code interpreter", None))
        self.pushButton_4.setText("")
    # retranslateUi

