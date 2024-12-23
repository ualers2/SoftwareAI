########################################################################
## IMPORTS Libs
import sys
import json
import time
import os
import subprocess
import platform
from firebase_admin import credentials, initialize_app, storage, db, delete_app
import concurrent.futures
########################################################################

########################################################################
# IMPORT Pyside2
from PySide2extn.RoundProgressBar import roundProgressBar #IMPORT THE EXTENSION LIBRARY
from PySide2.QtCore import QTimer, Signal, QThread
from PySide2.QtWidgets import QFileDialog
########################################################################

from CoreApp._init_core_ import OpenAIKeysinit,AutenticateAgent,Agent_files,  ResponseAgent, python_functions 
# IMPORT SoftwareAI Keys 
from CoreApp._init_keys_ import *
#########################################

class QProcessCreateOpenAItokens(QThread):
    ModalSucess = Signal(str)
    ModalInfo = Signal(str)
    finish = Signal()
    def __init__(self,
                openaikey,
                openainamefortoken_AgentKeys
            ):
        super().__init__()
        self.openaikey = openaikey
        self.openainamefortoken_AgentKeys = openainamefortoken_AgentKeys

    def run(self):


        PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/KeysOpenAI'))
        file_path = os.path.join(PATH_caminho, f"keys.py")
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(F'''

class OpenAIKeys{self.openainamefortoken_AgentKeys.replace(" ", "_")}:
    def keys():
        companyname = "{self.openainamefortoken_AgentKeys.replace(" ", "_")}"
        str_key = "{self.openaikey}"
        return str_key
    


            ''')
            file.close()


        self.ModalSucess.emit(f"Your Key has been created")
        self.finish.emit()
