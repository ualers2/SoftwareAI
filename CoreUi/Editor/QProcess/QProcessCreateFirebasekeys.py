
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *




class QProcessCreateFirebasekeys(QThread):
    ModalSucess = Signal(str)
    ModalInfo = Signal(str)
    uploadcredentials = Signal(str)
    finish = Signal()
    def __init__(self,
                appname_AgentKeys,
                Databaseurl_AgentKeys,
                Storagebucket_AgentKeys,
                credentialsapp_AgentKeys
            ):
        super().__init__()
        self.appname_AgentKeys = appname_AgentKeys
        self.credentialsapp_AgentKeys = credentialsapp_AgentKeys
        self.Databaseurl_AgentKeys = Databaseurl_AgentKeys
        self.Storagebucket_AgentKeys = Storagebucket_AgentKeys


    def run(self):


        PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/KeysFirebase'))
        file_path = os.path.join(PATH_caminho, f"keys.py")


        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(F'''
                    
def keys_{self.appname_AgentKeys.replace(" ", "_")}():
    cred1 = {self.credentialsapp_AgentKeys}
    credt1 = credentials.Certificate(cred1)
    app{self.appname_AgentKeys.replace(" ", "_")} = initialize_app(credt1, {{
            'storageBucket': '{self.Storagebucket_AgentKeys}',
            'databaseURL': '{self.Databaseurl_AgentKeys}'
    }}, name='{self.appname_AgentKeys.replace(" ", "_")}')
    return app{self.appname_AgentKeys.replace(" ", "_")}
    
            ''')
            file.close()


        self.ModalSucess.emit(f"Your Key has been created")
        self.finish.emit()




    def update_uploadcredentials(self, uploadcredentials_AgentKeys):
        self.uploadcredentials_AgentKeys = uploadcredentials_AgentKeys
    


