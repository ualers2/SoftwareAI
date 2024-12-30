
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *




class QProcessCreateGitHubKeys(QThread):
    ModalSucess = Signal(str)
    ModalInfo = Signal(str)
    finish = Signal()
    def __init__(self,
                githuusername_AgentKeys,
                githubtoken_AgentKeys
            ):
        super().__init__()
        self.githuusername_AgentKeys = githuusername_AgentKeys
        self.githubtoken_AgentKeys = githubtoken_AgentKeys

    def run(self):


        PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/KeysGitHub'))
        file_path = os.path.join(PATH_caminho, f"keys.py")
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(F'''


class GithubKeys{self.githuusername_AgentKeys.replace(" ", "_")}:
                       
    def {self.githuusername_AgentKeys.replace(" ", "_")}_github_keys():
        github_username = "{self.githuusername_AgentKeys}"
        github_token = "{self.githubtoken_AgentKeys}"
        return github_username, github_token



            ''')
            file.close()


        self.ModalSucess.emit(f"Your Key has been created")
        self.finish.emit()
