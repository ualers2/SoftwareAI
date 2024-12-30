
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *





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
