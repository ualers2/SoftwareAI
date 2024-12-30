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


# Caminho absoluto para o diretório onde SoftwareAI está localizado (raiz do projeto)
caminho_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI'))
sys.path.append(caminho_raiz)

########################################################################
# IMPORT CoreApp
from CoreUi.Editor.QProcess.QProcessCreateAgent import QProcessCreateAgent
from CoreUi.Editor.QProcess.QProcessCreateFirebasekeys import QProcessCreateFirebasekeys
from CoreUi.Editor.QProcess.QProcessCreateGitHubKeys import QProcessCreateGitHubKeys
from CoreUi.Editor.QProcess.QProcessCreateOpenAItokens import QProcessCreateOpenAItokens
from CoreUi.Editor.QProcess.QProcessCreateVectorStoreByUser import QProcessCreateVectorStoreByUser
from CoreUi.Editor.QProcess.QProcessCreateVectorStoreThreadByUser import QProcessCreateVectorStoreThreadByUser

from CoreApp._init_core_ import(
        AutenticateAgent,
        ResponseAgent,
        python_functions,
        Agent_files,
        Agent_files_update,
        OpenAIKeysinit,
        FirebaseKeysinit
)
########################################################################

########################################################################

########################################################################
# IMPORT .qrc
from src_ import icons_interpreter
########################################################################

########################################################################
# IMPORT GUI 
from src_.ui_interface import *
########################################################################


########################################################################
# IMPORT Custom widgets
from Custom_Widgets import *
from Custom_Widgets.QAppSettings import QAppSettings
from Custom_Widgets.QCustomModals import QCustomModals
from Custom_Widgets.QCustomCodeEditor import QCustomCodeEditor
from Custom_Widgets.QCustomLoadingIndicators import QCustomArcLoader
from Custom_Widgets.QCustomLoadingIndicators import QCustomSpinner
from Custom_Widgets.QCustomLoadingIndicators import QCustom3CirclesLoader
from Custom_Widgets.QCustomLoadingIndicators import QCustomPerlinLoader
# IMPORT Pyside2
from PySide2extn.RoundProgressBar import roundProgressBar #IMPORT THE EXTENSION LIBRARY
from PySide2.QtCore import QTimer, Signal, QThread, QRunnable
########################################################################

########################################################################
# IMPORT Pyside2
from PySide2extn.RoundProgressBar import roundProgressBar #IMPORT THE EXTENSION LIBRARY
from PySide2.QtCore import QTimer, Signal, QThread

########################################################################


########################################################################
########################################################################
## MAIN WINDOW CLASS
########################################################################
class MainWindow(QMainWindow):
    message_signal = Signal(str)
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ########################################################################
        # APPLY JSON STYLESHEET
        ########################################################################
        # self = QMainWindow class
        # self.ui = Ui_MainWindow / user interface class
        loadJsonStyle(self, self.ui, jsonFiles = {"JsonStyle/style.json"})
        self.liveCompileQss = True
        self.checkForMissingicons = False # do not generate new icons

        ########################################################################


        self.QPlaintextedit(self.ui.Promptmain)
        self.QPlaintextedit(self.ui.PromptRules)
        self.QPlaintextedit(self.ui.PromptExample)
        self.QPlaintextedit(self.ui.InstructionAgentCreate)
        self.QPlaintextedit(self.ui.AditionalInstructionsAgentCreate)
        self.QPlaintextedit(self.ui.AgentTools)
        self.QPlaintextedit(self.ui.FunctionPython)
        self.QPlaintextedit(self.ui.FunctionPythonOutput)
        self.QPlaintextedit(self.ui.ArgsCreatetextedit)
        self.QPlaintextedit(self.ui.NameAgent)
        self.QPlaintextedit(self.ui.KeyInFirebase)
        self.QPlaintextedit(self.ui.Vectorstoreinassistant)
        self.QPlaintextedit(self.ui.VectorstoreinThread)
        self.QPlaintextedit(self.ui.Upload1fileinThread)
        self.QPlaintextedit(self.ui.Upload1fileinmessage)
        self.QPlaintextedit(self.ui.Upload1imageforvisioninThread)
        self.QPlaintextedit(self.ui.Uploadlistfileforcodeinterpreterinthread)
        self.QPlaintextedit(self.ui.textEdit_2)
        self.QPlaintextedit(self.ui.Current_instuction_html_edit)
        self.QPlaintextedit(self.ui.instruction_input_edit)
        #self.QPlaintextedit(self.ui.NameForInstruction_create)
        self.QPlaintextedit(self.ui.New_instruction_html_create)







        self.myStackedWidget = self.ui.myStackedWidget

        self.widget_ViewAgent = self.ui.widget_ViewAgent
        layout = QVBoxLayout()
        self.widget_ViewAgent.setLayout(layout)
        self.CodeEditor = QCustomCodeEditor() #themes = ["default", "one-light", "one-dark", "monokai", "oceanic", "zenburn"]
        self.CodeEditor.setTheme("one-dark")
        self.CodeEditor.setLang("python")
        layout.addWidget(self.CodeEditor)

        self.AgentViewCode = self.ui.AgentViewCode
        self.AgentViewCode.currentTextChanged.connect(lambda: self.Update_AgentViewCode(Agent=self.AgentViewCode.currentText()))

        self.CurrentInstruction = self.ui.Current_instuction_html_edit
        self.CurrentInstruction.setReadOnly(True)

        self.ArgsCreatetextedit = self.ui.ArgsCreatetextedit
        self.CurrentArgs_AgentCreate = self.ui.CurrentArgs_AgentCreate

        self.InstructionSelector = self.ui.comboBox_list_instruction_edit
        self.InstructionSelector.currentTextChanged.connect(lambda: self.on_InstructionSelector_changed(self.InstructionSelector.currentText()) )
        #self.InstructionSelector.currentTextChanged.connect(self.list_instruction)

        self.list_instruction()


        self.Instructioninput_edit = self.ui.instruction_input_edit
        self.Instructioninput_edit.textChanged.connect(lambda: self.adjust_height(self.Instructioninput_edit, max_height=170))

        self.change_instruction_button_edit = self.ui.change_instruction_button_edit
        self.change_instruction_button_edit.clicked.connect(self.change_instruction)




        self.Add_new_instructions_button_edit = self.ui.Add_new_instructions_button_edit




        self.InstructionSelector_create = self.ui.comboBox_list_agent_for_create_instruction_create
        #self.InstructionSelector_create.currentTextChanged.connect(self.list_agents)
        self.list_agents()


        self.InstructionCategory_create = self.ui.comboBox_category_instruction_create
        self.InstructionCategory_create.currentTextChanged.connect(self.list_category_instruction)
        self.list_category_instruction()


        self.UseVectorstoreToGenerateFiles = self.ui.UseVectorstoreToGenerateFiles
        #self.addShadow(self.UseVectorstoreToGenerateFiles)
    
        self.KeyInFirebase_AgentCreate = self.ui.KeyInFirebase
        self.NameAgent_AgentCreate = self.ui.NameAgent
        self.ModelSelect_AgentCreate = self.ui.ModelSelect
        self.AgentCategory_AgentCreate = self.ui.AgentCategory

        self.Vectorstoreinassistant_AgentCreate = self.ui.Vectorstoreinassistant
        self.VectorstoreinassistantByUser_AgentCreate = self.ui.VectorstoreinassistantByUser
        self.VectorstoreinassistantByUser_AgentCreate.clicked.connect(self.custom_file_dialogVectorstoreinassistant)
        
        self.VectorstoreinThread_AgentCreate = self.ui.VectorstoreinThread
        self.VectorstoreinThreadByUser_AgentCreate = self.ui.VectorstoreinThreadByUser
        self.VectorstoreinThreadByUser_AgentCreate.clicked.connect(self.custom_file_dialogVectorstoreinThread)
        
        self.Upload1fileinThread_AgentCreate = self.ui.Upload1fileinThread
        self.Upload1fileinThreadByUser_AgentCreate = self.ui.Upload1fileinThreadByUser
        self.Upload1fileinThreadByUser_AgentCreate.clicked.connect(self.upload1fileinthread)


        self.Upload1fileinmessage_AgentCreate = self.ui.Upload1fileinmessage
        self.Upload1fileinmessageByUser_AgentCreate = self.ui.Upload1fileinmessageByUser
        self.Upload1fileinmessageByUser_AgentCreate.clicked.connect(self.upload1fileinmessage)


        self.Upload1imageforvisioninThread_AgentCreate = self.ui.Upload1imageforvisioninThread
        self.Upload1imageforvisioninThreadByUser_AgentCreate = self.ui.Upload1imageforvisioninThreadByUser
        self.Upload1imageforvisioninThreadByUser_AgentCreate.clicked.connect(self.upload1imageforvisioninThread)

        self.Uploadlistfileforcodeinterpreterinthread_AgentCreate = self.ui.Uploadlistfileforcodeinterpreterinthread
        self.UploadlistfileforcodeinterpreterinthreadByUser_AgentCreate = self.ui.UploadlistfileforcodeinterpreterinthreadByUser
        self.UploadlistfileforcodeinterpreterinthreadByUser_AgentCreate.clicked.connect(self.uploadlistfileforcodeinterpreterinthread)

        self.Promptmain_AgentCreate = self.ui.Promptmain
        self.PromptExample_AgentCreate = self.ui.PromptExample
        self.PromptRules_AgentCreate = self.ui.PromptRules


        self.InstructionAgentCreate = self.ui.InstructionAgentCreate
        self.AditionalInstructionsAgentCreate = self.ui.AditionalInstructionsAgentCreate


        self.AgentToolsAgentCreate = self.ui.AgentTools
        self.FunctionPythonAgentCreate = self.ui.FunctionPython
        self.FunctionPythonOutputAgentCreate = self.ui.FunctionPythonOutput
    

        self.namefunction_agentcreate = self.ui.namefunction_agentcreate



        self.CreateAgentButton = self.ui.CreateAgent
        self.CreateAgentButton.clicked.connect(self.CreateAgentButtonClicked)
        self.list_category_Agent()


        self.createkeyopenai_AgentKeys = self.ui.createkeyopenai_AgentKeys
        self.createkeyopenai_AgentKeys.clicked.connect(self.CreateOpenAIbuttonClicked)
        

        self.myStackedWidget = self.ui.myStackedWidget
        


        self.Instructioninput_create = self.ui.New_instruction_html_create
        self.Instructioninput_create.textChanged.connect(lambda: self.adjust_height(self.Instructioninput_create, max_height=300))
        
        self.NameForInstruction_create = self.ui.NameForInstruction_create

        self.CreateInstructionbutton_create = self.ui.CreateInstructionbutton_create
        self.CreateInstructionbutton_create.clicked.connect(self.create_instruction)

        self.openaitoken_AgentKeys = self.ui.openaitoken_AgentKeys
        self.QPlaintextedit(self.openaitoken_AgentKeys)

        self.openainamefortoken_AgentKeys = self.ui.openainamefortoken_AgentKeys
        self.QPlaintextedit(self.openainamefortoken_AgentKeys)

        self.githuusername_AgentKeys = self.ui.githuusername_AgentKeys
        self.QPlaintextedit(self.githuusername_AgentKeys)

        self.githubtoken_AgentKeys = self.ui.githubtoken_AgentKeys
        self.QPlaintextedit(self.githubtoken_AgentKeys)


        self.credentialsapp_AgentKeys = self.ui.credentialsapp_AgentKeys
        self.QPlaintextedit(self.credentialsapp_AgentKeys)


        self.githuusername_AgentKeys = self.ui.githuusername_AgentKeys
        self.githubtoken_AgentKeys = self.ui.githubtoken_AgentKeys
        self.createkeygithub_AgentKeys = self.ui.createkeygithub_AgentKeys
        self.createkeygithub_AgentKeys.clicked.connect(self.CreateGitHubKeysbuttonClicked)


        self.appname_AgentKeys = self.ui.appname_AgentKeys
        self.QPlaintextedit(self.appname_AgentKeys)
        self.Databaseurl_AgentKeys = self.ui.Databaseurl_AgentKeys
        self.QPlaintextedit(self.Databaseurl_AgentKeys)
        self.Storagebucket_AgentKeys = self.ui.Storagebucket_AgentKeys
        self.QPlaintextedit(self.Storagebucket_AgentKeys)
        self.credentialsapp_AgentKeys = self.ui.credentialsapp_AgentKeys
        self.QPlaintextedit(self.credentialsapp_AgentKeys)


        self.AgentKeysOpenAI = self.ui.AgentKeysOpenAI

        self.AgentKeysGithub = self.ui.AgentKeysGithub

        self.AgentKeysFirebase = self.ui.AgentKeysFirebase

        self.CreateAgents_menu = self.ui.CreateAgents_menu
        self.CreateAgents_menu.clicked.connect(self.update_home)

        self.load_AgentKeysOpenAI()
        
        self.load_AgentKeysGithub()

        self.load_AgentKeysFirebase()


        self.createkeysfirebase_AgentKeys = self.ui.createkeysfirebase_AgentKeys
        self.createkeysfirebase_AgentKeys.clicked.connect(self.CreateFirebasekeysbuttonClicked)
        
        self.uploadcredentialapp_AgentKeys = self.ui.uploadcredentialapp_AgentKeys
        self.uploadcredentialapp_AgentKeys.clicked.connect(self.click_uploadcredentialapp_AgentKeys)
        try:
            key_api = self.AgentKeysOpenAI.currentText()
            name_app = self.AgentKeysFirebase.currentText()
            self.client = OpenAIKeysinit._init_client_(key_api)
            self.app1 = FirebaseKeysinit._init_app_(name_app)
        except Exception as e:
            print(e)

        self.show()

    def CreateAgentButtonClicked(self):
        try:
            if self.thread_processe_create_agent:
                print("Aguardando a thread finalizar...")
                self.thread_processe_create_agent.cancel()  
                QTimer.singleShot(1000, self.check_task_status)
        except:
            pass

        KeyInFirebase_AgentCreate = self.KeyInFirebase_AgentCreate.toPlainText()
        ModelSelect_AgentCreate = self.ModelSelect_AgentCreate.currentText()
        Vectorstoreinassistant_AgentCreate = self.Vectorstoreinassistant_AgentCreate.toPlainText()
        VectorstoreinThread_AgentCreate = self.VectorstoreinThread_AgentCreate.toPlainText()
        Upload1fileinThread_AgentCreate = self.Upload1fileinThread_AgentCreate.toPlainText()
        Upload1fileinmessage_AgentCreate = self.Upload1fileinmessage_AgentCreate.toPlainText()
        Upload1imageforvisioninThread_AgentCreate = self.Upload1imageforvisioninThread_AgentCreate.toPlainText()
        Uploadlistfileforcodeinterpreterinthread_AgentCreate = self.Uploadlistfileforcodeinterpreterinthread_AgentCreate.toPlainText()
        Promptmain_AgentCreate = self.Promptmain_AgentCreate.toPlainText()
        PromptRules_AgentCreate = self.PromptRules_AgentCreate.toPlainText()
        PromptExample_AgentCreate = self.PromptExample_AgentCreate.toPlainText()
        NameAgent_AgentCreate = self.NameAgent_AgentCreate.toPlainText()
        category_target = self.AgentCategory_AgentCreate.currentText()
        namefunction_agentcreate = self.namefunction_agentcreate.toPlainText()
        AgentToolsAgentCreate = self.AgentToolsAgentCreate.toPlainText()
        InstructionAgentCreate = self.InstructionAgentCreate.toPlainText()
        FunctionPythonAgentCreate = self.FunctionPythonAgentCreate.toPlainText()
        AditionalInstructionsAgentCreate = self.AditionalInstructionsAgentCreate.toPlainText()
        FunctionPythonOutputAgentCreate = self.FunctionPythonOutputAgentCreate.toPlainText()
        UseVectorstoreToGenerateFiles = self.UseVectorstoreToGenerateFiles.isChecked()
        if self.ArgsCreatetextedit.toPlainText().strip():
            ArgsCreatetextedit = self.ArgsCreatetextedit.toPlainText()
        else:
            ArgsCreatetextedit = None
        CurrentArgs_AgentCreate = self.CurrentArgs_AgentCreate.currentText()
        StorageAgentCompletions_AgentCreate = self.ui.StorageAgentCompletions.isChecked()
        StorageAgentOutput_AgentCreate = self.ui.StorageAgentOutput_.isChecked()
        StoreFormatJsonAndJsonl_AgentCreate = self.ui.StoreFormatJsonAndJsonl.isChecked()
        AgentKeysGithub = self.AgentKeysGithub.currentText()
        AgentKeysGithubName = re.findall(r'\(([^)]*)\)', AgentKeysGithub)
        AgentOpenAIelement = self.AgentKeysOpenAI.currentText()
        AgentKeyOpenAI = re.sub(r'\([^)]*\)', '', AgentOpenAIelement)
        
        AgentKeysOpenAIName = re.findall(r'\(([^)]*)\)', AgentOpenAIelement)
        name_app = self.AgentKeysFirebase.currentText()
        self.thread_processe_create_agent = QProcessCreateAgent(
            KeyInFirebase_AgentCreate,
            ModelSelect_AgentCreate,
            Vectorstoreinassistant_AgentCreate,
            VectorstoreinThread_AgentCreate,
            Upload1fileinThread_AgentCreate,
            Upload1fileinmessage_AgentCreate,
            Upload1imageforvisioninThread_AgentCreate,
            Uploadlistfileforcodeinterpreterinthread_AgentCreate,
            Promptmain_AgentCreate,
            PromptRules_AgentCreate,
            PromptExample_AgentCreate,
            NameAgent_AgentCreate,
            category_target,
            namefunction_agentcreate,
            AgentToolsAgentCreate,
            InstructionAgentCreate,
            FunctionPythonAgentCreate,
            AditionalInstructionsAgentCreate,
            FunctionPythonOutputAgentCreate,
            UseVectorstoreToGenerateFiles,
            ArgsCreatetextedit,
            CurrentArgs_AgentCreate,
            StorageAgentCompletions_AgentCreate,
            StorageAgentOutput_AgentCreate,
            StoreFormatJsonAndJsonl_AgentCreate,
            AgentKeysGithubName,
            AgentKeysOpenAIName,
            AgentKeyOpenAI.replace("  ", "").replace(" ", ""),
            name_app
        )
        self.thread_processe_create_agent.ModalSucess.connect(self.update_custommodals_SuccessModal)
        self.thread_processe_create_agent.ModalInfo.connect(self.update_custommodals_info)
        self.thread_processe_create_agent.finishedqthread.connect(self.finish_thread_processe_create_agent)
        self.thread_processe_create_agent.start()

    def CreateOpenAIbuttonClicked(self):
        openaitoken_AgentKeys = self.ui.openaitoken_AgentKeys.toPlainText()
        openainamefortoken_AgentKeys = self.ui.openainamefortoken_AgentKeys.toPlainText()
        self.thread_process_create_openaikeys = QProcessCreateOpenAItokens(
            openaitoken_AgentKeys,
            openainamefortoken_AgentKeys
        )
        self.thread_process_create_openaikeys.ModalSucess.connect(self.update_custommodals_SuccessModal)
        self.thread_process_create_openaikeys.ModalInfo.connect(self.update_custommodals_info)
        self.thread_process_create_openaikeys.finish.connect(self.finish_thread_process_create_openaikeys)
        self.thread_process_create_openaikeys.start()

    def CreateGitHubKeysbuttonClicked(self):
        githuusername_AgentKeys = self.ui.githuusername_AgentKeys.toPlainText()
        githubtoken_AgentKeys = self.ui.githubtoken_AgentKeys.toPlainText()
        self.thread_process_create_GitHubKeys = QProcessCreateGitHubKeys(
            githuusername_AgentKeys,
            githubtoken_AgentKeys
        )
        self.thread_process_create_GitHubKeys.ModalSucess.connect(self.update_custommodals_SuccessModal)
        self.thread_process_create_GitHubKeys.ModalInfo.connect(self.update_custommodals_info)
        self.thread_process_create_GitHubKeys.finish.connect(self.finish_thread_process_create_GitHubKeys)
        self.thread_process_create_GitHubKeys.start()

    def CreateFirebasekeysbuttonClicked(self):
        appname_AgentKeys = self.ui.appname_AgentKeys.toPlainText()
        Databaseurl_AgentKeys = self.ui.Databaseurl_AgentKeys.toPlainText()
        Storagebucket_AgentKeys = self.ui.Storagebucket_AgentKeys.toPlainText()
        Storagebucket_AgentKeys = Storagebucket_AgentKeys.replace("gs://", "")
        credentialsapp_AgentKeys = self.ui.credentialsapp_AgentKeys.toPlainText()
        self.thread_process_create_Firebasekeys = QProcessCreateFirebasekeys(
            appname_AgentKeys,
            Databaseurl_AgentKeys,
            Storagebucket_AgentKeys,
            credentialsapp_AgentKeys
        )
        self.thread_process_create_Firebasekeys.ModalSucess.connect(self.update_custommodals_SuccessModal)
        self.thread_process_create_Firebasekeys.ModalInfo.connect(self.update_custommodals_info)
        self.thread_process_create_Firebasekeys.finish.connect(self.finish_thread_process_create_Firebasekeys)
        self.thread_process_create_Firebasekeys.start()


    @Slot()
    def check_task_status(self):
        if self.thread_processe_create_agent:
            QTimer.singleShot(1000, self.check_task_status) 
        else:
            print("check_task_status Tarefa concluída.")

    def load_AgentKeysOpenAI(self, chave="str_key", company="companyname"):
        self.AgentKeysOpenAI.clear()
        try:
            caminho_arquivo = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../CoreApp/KeysOpenAI/keys.py'))
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                for linha in arquivo:
                    match = re.match(r'(\w+)\s*=\s*[\'\"](.*?)[\'\"]', linha.strip())
                    if match:
                        chave_encontrada, valor = match.groups()
                        if chave_encontrada == company:
                            companyname = valor
                        elif chave_encontrada == chave:
                            str_key = valor
                            self.AgentKeysOpenAI.addItem(f"({companyname}) {str_key}")
        except:
            pass

    def load_AgentKeysFirebase(self):
        self.AgentKeysFirebase.clear()
        caminho_arquivo = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../CoreApp/KeysFirebase/keys.py'))
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read() 
                pattern = re.compile(r"(\w+)\s*=\s*initialize_app\(", re.DOTALL)
                matches = pattern.findall(conteudo)  
                if matches:
                    for app_nome in matches:
                        self.AgentKeysFirebase.addItem(f"{app_nome}")

        except Exception as e:
            self.AgentKeysFirebase.addItem(f"Erro ao carregar: {str(e)}")

    def load_AgentKeysGithub(self, chave = "github_token",  user = "github_username"):
        self.AgentKeysGithub.clear()
        caminho_arquivo = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../CoreApp/KeysGitHub/keys.py'))
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                match = re.match(r'(\w+)\s*=\s*[\'\"](.*?)[\'\"]', linha.strip())
                if match:
                    chave_encontrada, valor = match.groups()
                    if chave_encontrada == user:
                        github_user = valor
                    elif chave_encontrada == chave:
                        github_token = valor
                        token = linha.replace('return', "").replace('"', "").replace(' ', "").replace('github_token', "").replace('=', "").replace("return github_token", "").strip()
                        self.AgentKeysGithub.addItem(f"({github_user}) {token}")

            self.AgentKeysGithub.addItem(f"None")



    def update_home(self):
        self.load_AgentKeysOpenAI()
        
        self.load_AgentKeysGithub()

        self.load_AgentKeysFirebase()

        self.list_category_Agent()

        self.list_agents()

        self.list_instruction()

    def Update_AgentViewCode(self, Agent):
        paths_agents = self.init_paths_agents()
        for path in paths_agents:
            agentss = os.listdir(path)
            for agent in agentss:
                if agent == "DocGitHubData":
                    pass
                elif agent == "docs_uploaded.log":
                    pass
                elif agent.replace(".py", "").replace("__pycache__", "").strip() == Agent:
                    print(Agent)
                    path_py = os.path.join(path, f"{Agent}.py")
                    # with open(path_py, "r") as f:
                    #     content = f.read()

                    self.CodeEditor.loadFile(path_py)

    def dialogsetStyleSheet(self):
        text = """
            QFileDialog {
                background-color: white;
                border: 1px solid #F7F7F7;
                border-radius: 13px;
                color: black;
                font-size: 16px;
            }
            /* Personalizar os botões */
            QPushButton {
                background-color: #F7F7F7;
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #E6E6E6;
            }
            QPushButton:pressed {
                background-color: #D6D6D6;
            }
            /* Personalizar lista de arquivos */
            QListView, QTreeView {
                background-color: white;
                border: none;
                color: black;
                font-size: 14px;
            }
            /* Barra de navegação */
            QLineEdit {
                background-color: #F7F7F7;
                border: 1px solid #CCCCCC;
                border-radius: 6px;
                padding: 3px;
            }
        """
        return text

    def click_uploadcredentialapp_AgentKeys(self):
        dialog = QFileDialog()
        dialog.setStyleSheet(self.dialogsetStyleSheet())
        dialog.setFileMode(QFileDialog.ExistingFile) 
        dialog.setWindowTitle("Select the Credentials Firebase")
        dialog.setNameFilter(
            "All Files (*)"
        )
        if dialog.exec_():
            selected_files = dialog.selectedFiles()[0]
            with open(selected_files, 'r', encoding='utf-8') as file:
                content = file.read()
            self.ui.credentialsapp_AgentKeys.setPlainText(content)



    def finish_thread_process_create_openaikeys(self):
        self.ui.openaitoken_AgentKeys.clear()
        self.ui.openainamefortoken_AgentKeys.clear()

    def finish_thread_process_create_GitHubKeys(self):
        self.ui.githuusername_AgentKeys.clear()
        self.ui.githubtoken_AgentKeys.clear()

    def finish_thread_process_create_Firebasekeys(self):
        self.ui.appname_AgentKeys.clear()
        self.ui.Databaseurl_AgentKeys.clear()
        self.ui.Storagebucket_AgentKeys.clear()
        self.ui.credentialsapp_AgentKeys.clear()

    def finish_thread_processe_create_agent(self):
        self.InstructionSelector_create.clear()

        self.list_instruction()
        self.list_category_instruction()
        self.list_agents()
        self.list_category_Agent()

    def QPlaintextedit(self, editor: QTextEdit):
        """
        Configures a QTextEdit to handle pasted text as plain text only.

        :param editor: Instance of QTextEdit to configure
        """
        editor.setAcceptRichText(False)
        def insert_plain_text_from_mime_data(self, source):
            if source.hasText():
                self.insertPlainText(source.text())
            else:
                super(QTextEdit, self).insertFromMimeData(source)
        editor.__class__.insertFromMimeData = insert_plain_text_from_mime_data



    def custom_file_dialogVectorstoreinThread(self):
        dialog = QFileDialog()
        dialog.setStyleSheet(self.dialogsetStyleSheet())
        dialog.setFileMode(QFileDialog.ExistingFiles) 
        dialog.setWindowTitle("Select the files that will go to vector storage")
        dialog.setNameFilter(
            "C Files (*.c);;C++ Files (*.cpp);;C# Files (*.cs);;CSS Files (*.css);;"
            "Word Documents (*.doc *.docx);;Go Files (*.go);;HTML Files (*.html);;"
            "Java Files (*.java);;JavaScript Files (*.js);;JSON Files (*.json);;"
            "Markdown Files (*.md);;PDF Files (*.pdf);;PHP Files (*.php);;"
            "PowerPoint Files (*.pptx);;Python Files (*.py);;Ruby Files (*.rb);;"
            "Shell Scripts (*.sh);;TeX Files (*.tex);;TypeScript Files (*.ts);;"
            "Text Files (*.txt);;All Files (*)"
        )
        if dialog.exec_():
            selected_files = dialog.selectedFiles()

            self.update_custommodals_SuccessModal2(f"Selected files!!")

            self.thread_VectorstoreinThread_AgentCreate = QProcessCreateVectorStoreThreadByUser(selected_files, self.app1, self.client)
            self.thread_VectorstoreinThread_AgentCreate.vectorsignal.connect(self.update_VectorstoreinThread_AgentCreate)
                
            self.thread_VectorstoreinThread_AgentCreate.ModalSucess.connect(self.update_custommodals_SuccessModal2)
            self.thread_VectorstoreinThread_AgentCreate.ModalInfo.connect(self.update_custommodals_info)

            self.thread_VectorstoreinThread_AgentCreate.start()



    def custom_file_dialogVectorstoreinassistant(self):
        dialog = QFileDialog()
        dialog.setStyleSheet(self.dialogsetStyleSheet())
        dialog.setFileMode(QFileDialog.ExistingFiles) 
        dialog.setWindowTitle("Select the files that will go to vector storage")
        dialog.setNameFilter(
            "C Files (*.c);;C++ Files (*.cpp);;C# Files (*.cs);;CSS Files (*.css);;"
            "Word Documents (*.doc *.docx);;Go Files (*.go);;HTML Files (*.html);;"
            "Java Files (*.java);;JavaScript Files (*.js);;JSON Files (*.json);;"
            "Markdown Files (*.md);;PDF Files (*.pdf);;PHP Files (*.php);;"
            "PowerPoint Files (*.pptx);;Python Files (*.py);;Ruby Files (*.rb);;"
            "Shell Scripts (*.sh);;TeX Files (*.tex);;TypeScript Files (*.ts);;"
            "Text Files (*.txt);;All Files (*)"
        )
        if dialog.exec_():
            selected_files = dialog.selectedFiles()

            self.update_custommodals_SuccessModal2(f"Selected files!!")

            self.thread_Vectorstoreinassistant_AgentCreate = QProcessCreateVectorStoreByUser(selected_files, self.app1, self.client)
            self.thread_Vectorstoreinassistant_AgentCreate.vectorsignal.connect(self.update_Vectorstoreinassistant_AgentCreate)
                            
            self.thread_Vectorstoreinassistant_AgentCreate.ModalSucess.connect(self.update_custommodals_SuccessModal2)
            self.thread_Vectorstoreinassistant_AgentCreate.ModalInfo.connect(self.update_custommodals_info)

            self.thread_Vectorstoreinassistant_AgentCreate.start()


    def upload1fileinthread(self):
        dialog = QFileDialog()
        dialog.setStyleSheet(self.dialogsetStyleSheet())
        dialog.setFileMode(QFileDialog.ExistingFile) 
        dialog.setWindowTitle("Select the files that will go to vector storage")
        dialog.setNameFilter(
            "C Files (*.c);;C++ Files (*.cpp);;C# Files (*.cs);;CSS Files (*.css);;"
            "Word Documents (*.doc *.docx);;Go Files (*.go);;HTML Files (*.html);;"
            "Java Files (*.java);;JavaScript Files (*.js);;JSON Files (*.json);;"
            "Markdown Files (*.md);;PDF Files (*.pdf);;PHP Files (*.php);;"
            "PowerPoint Files (*.pptx);;Python Files (*.py);;Ruby Files (*.rb);;"
            "Shell Scripts (*.sh);;TeX Files (*.tex);;TypeScript Files (*.ts);;"
            "Text Files (*.txt);;All Files (*)"
        )
        if dialog.exec_():
            selected_files = dialog.selectedFiles()[0]
            self.update_custommodals_SuccessModal2(f"Selected files!!")
            self.Upload1fileinThread_AgentCreate.clear()
            self.Upload1fileinThread_AgentCreate.setPlainText(f"'{selected_files}'")
            



    def upload1fileinmessage(self):
        dialog = QFileDialog()
        dialog.setStyleSheet(self.dialogsetStyleSheet())
        dialog.setFileMode(QFileDialog.ExistingFile) 
        dialog.setWindowTitle("Select the files that will go to vector storage")
        dialog.setNameFilter(
            "C Files (*.c);;C++ Files (*.cpp);;C# Files (*.cs);;CSS Files (*.css);;"
            "Word Documents (*.doc *.docx);;Go Files (*.go);;HTML Files (*.html);;"
            "Java Files (*.java);;JavaScript Files (*.js);;JSON Files (*.json);;"
            "Markdown Files (*.md);;PDF Files (*.pdf);;PHP Files (*.php);;"
            "PowerPoint Files (*.pptx);;Python Files (*.py);;Ruby Files (*.rb);;"
            "Shell Scripts (*.sh);;TeX Files (*.tex);;TypeScript Files (*.ts);;"
            "Text Files (*.txt);;All Files (*)"
        )

        if dialog.exec_():
            selected_files = dialog.selectedFiles()[0]
            self.update_custommodals_SuccessModal2(f"Selected files!!")
            self.Upload1fileinmessage_AgentCreate.clear()
            self.Upload1fileinmessage_AgentCreate.setPlainText(f"'{selected_files}'")
     
    def upload1imageforvisioninThread(self):
        dialog = QFileDialog()
        dialog.setStyleSheet(self.dialogsetStyleSheet())
        dialog.setFileMode(QFileDialog.ExistingFile) 
        dialog.setWindowTitle("Select the files that will go to vector storage")
        dialog.setNameFilter("Imagens (*.png *.jpg *.jpeg);;Todos os Arquivos (*)")  # Filtro
        if dialog.exec_():
            selected_files = dialog.selectedFiles()[0]
            self.update_custommodals_SuccessModal2(f"Selected files!!")
            self.Upload1imageforvisioninThread_AgentCreate.clear()
            self.Upload1imageforvisioninThread_AgentCreate.setPlainText(f"'{selected_files}'")

    def uploadlistfileforcodeinterpreterinthread(self):
        dialog = QFileDialog()
        dialog.setStyleSheet(self.dialogsetStyleSheet())
        dialog.setFileMode(QFileDialog.ExistingFiles) 
        dialog.setWindowTitle("Select the files that will go to vector storage")
        dialog.setNameFilter(
            "C Files (*.c);;C++ Files (*.cpp);;C# Files (*.cs);;CSS Files (*.css);;"
            "Word Documents (*.doc *.docx);;Go Files (*.go);;HTML Files (*.html);;"
            "Java Files (*.java);;JavaScript Files (*.js);;JSON Files (*.json);;"
            "Markdown Files (*.md);;PDF Files (*.pdf);;PHP Files (*.php);;"
            "PowerPoint Files (*.pptx);;Python Files (*.py);;Ruby Files (*.rb);;"
            "Shell Scripts (*.sh);;TeX Files (*.tex);;TypeScript Files (*.ts);;"
            "Text Files (*.txt);;All Files (*)"
        )
        if dialog.exec_():
            selected_files = dialog.selectedFiles()
            self.update_custommodals_SuccessModal2(f"Selected files!!")
            self.Uploadlistfileforcodeinterpreterinthread_AgentCreate.clear()
            self.Uploadlistfileforcodeinterpreterinthread_AgentCreate.setPlainText(f"[{selected_files}]")



    def list_category_Agent(self):
        paths_category = [
            'Software_Requirements_Analysis',
            'Software_Planning',
            'Software_Documentation',
            'Software_Development',
            'Pre_Project',
            'Company_Managers',
            'Company_CEO',
        ]
        for path in paths_category:
            self.AgentCategory_AgentCreate.addItem(path)

    def create_instruction(self):
        if self.Instructioninput_create.toPlainText().strip():
            NameForInstruction_create = self.NameForInstruction_create.text()
            agent_target =  self.InstructionSelector_create.currentText()
            category_target = self.InstructionCategory_create.currentText()
            paths_category = self.init_paths_category()
            for path in paths_category:
                if path == category_target:
                    PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../SoftwareAI/CoreApp/SoftwareAI/Instructions/{category_target}'))
                    file_path = os.path.join(PATH_caminho, f"{NameForInstruction_create}.py")
                    with open(file_path, 'w', encoding='utf-8') as file:
                        content = self.Instructioninput_create.toPlainText()
                        file.write(F'''instruction{agent_target} = """{content}"""\nadxitional_instructions_{agent_target} = None''')
                        file.close()

                    self.Instructioninput_create.clear()
                    self.update_custommodals_SuccessModal("Your Instruction Was Created", "bottom-left")
        else:
            self.update_custommodals_erro("The Instruction Field Is Empty.")

    def list_agents(self):
        paths_agents = self.init_paths_agents()
        for path in paths_agents:
            agentss = os.listdir(path)
            for agent in agentss:
                if agent == "DocGitHubData":
                    pass
                elif agent == "docs_uploaded.log":
                    pass
                else:
                    iagents_refact = agent.replace(".py", "").replace("__pycache__", "").strip()
                    if iagents_refact:
                        self.InstructionSelector_create.addItem(iagents_refact)
                        self.AgentViewCode.addItem(iagents_refact)

    def list_category_instruction(self):
        paths_category = [
            'Software_Requirements_Analysis',
            'Software_Planning',
            'Software_Documentation',
            'Software_Development',
            'Pre_Project',
            'Company_Managers',
            'Company_CEO',
        ]
        for path in paths_category:
            self.InstructionCategory_create.addItem(path)



    def change_instruction(self):
        if self.Instructioninput_edit.toPlainText().strip():
            instructionarqname = self.InstructionSelector.currentText()
            paths_instruct = self.init_paths()
            for path in paths_instruct:
                instructions = os.listdir(path)
                for instruct in instructions:
                    instruct_refact = instruct.replace(".py", "").replace("__pycache__", "").strip()
                    if instruct_refact == instructionarqname:
                        file_path = os.path.join(path, f"{instruct_refact}.py")
                        with open(file_path, 'w', encoding='utf-8') as file:
                            content = self.Instructioninput_edit.toPlainText()
                            file.write(content)
                            file.close()
                        self.update_custommodals_SuccessModal(description="Your Instruction Has Been Updated", pos="bottom-left")
                        self.Instructioninput_edit.clear()
                        self.open_and_read(file_path)
        else:
            self.update_custommodals_erro("The Instruction Field Is Empty.")


    def on_InstructionSelector_changed(self, text):
        #self.InstructionSelector.clear()
        # paths_instruct = self.init_paths()
        # for path in paths_instruct:
        #     instructions = os.listdir(path)
        #     for instruct in instructions:
        #         instruct_refact = instruct.replace(".py", "").replace("__pycache__", "").strip()
        #         if instruct_refact:
        #             self.InstructionSelector.addItem(instruct_refact)
        
        self.CurrentInstruction.clear()
        paths_instruct = self.init_paths()
        for path in paths_instruct:
            instructions = os.listdir(path)
            for instruct in instructions:
                if instruct == "__pycache__":
                    pass
                else:
                    instruct_refact = instruct.replace(".py", "").strip()
                    if instruct_refact == text:
                        file_path = os.path.join(path, f"{instruct_refact}.py")
                        with open(file_path, 'r', encoding='utf-8') as file:
                            content = file.read()
                            
                            self.CurrentInstruction.setPlainText(content)
                        return True



    def list_instruction(self):
        self.InstructionSelector.clear()
        paths_instruct = self.init_paths()
        for path in paths_instruct:
            instructions = os.listdir(path)
            for instruct in instructions:
                instruct_refact = instruct.replace(".py", "").replace("__pycache__", "").strip()
                if instruct_refact:
                    self.InstructionSelector.addItem(instruct_refact)


    def update_Vectorstoreinassistant_AgentCreate(self, VectorstoreID):
        self.Vectorstoreinassistant_AgentCreate.setPlainText(VectorstoreID)

    def update_VectorstoreinThread_AgentCreate(self, VectorstoreID):
        self.VectorstoreinThread_AgentCreate.setPlainText(VectorstoreID)

    def addShadow(self, widget):
        effect = QGraphicsDropShadowEffect(widget)
        effect.setColor(QColor(30, 30, 30, 200))
        effect.setBlurRadius(20)
        effect.setXOffset(0)
        effect.setYOffset(0)
        widget.setGraphicsEffect(effect)

        
    def adjust_height(self, element, max_height = 150, increase=True):
        base_height = 50
        current_text_length = len(element.toPlainText())
        if current_text_length == 0:
            element.setMinimumHeight(base_height)
            element.setMinimumHeight(base_height)
            element.setMaximumHeight(base_height)
            return
        if increase:
            extra_lines = (current_text_length // 40) * 15  
            new_height = base_height + extra_lines
            if new_height > max_height:
                new_height = max_height
        else:
            new_height = max(base_height, max_height - (current_text_length // 40) * 15)

        element.setMinimumHeight(new_height)
        element.setMaximumHeight(new_height)

    def init_paths_category(self):
        paths_category = [
            'Software_Requirements_Analysis',
            'Software_Planning',
            'Software_Documentation',
            'Software_Development',
            'Pre_Project',
            'Company_Managers',
            'Company_CEO',
        ]
        return paths_category
    
    def init_paths_agents(self):
        paths_instruct = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Software_Requirements_Analysis')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Software_Planning')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Software_Documentation')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Software_Development')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Pre_Project')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Company_Managers')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Company_CEO')),
        ]
        return paths_instruct
    
    def init_paths(self):
        paths_instruct = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/SoftwareAI/Instructions/Software_Requirements_Analysis')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/SoftwareAI/Instructions/Software_Planning')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/SoftwareAI/Instructions/Software_Documentation')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/SoftwareAI/Instructions/Software_Development')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/SoftwareAI/Instructions/Pre_Project')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/SoftwareAI/Instructions/Company_Managers')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/SoftwareAI/Instructions/Company_CEO')),
        ]
        return paths_instruct
    


    def open_and_read(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            self.CurrentInstruction.setPlainText(content)



    def update_custommodals_erro(self, description, pos='center-center'):

        myModal = QCustomModals.ErrorModal(
            title="Information", 
            parent=self.myStackedWidget,
            position=pos,
            closeIcon=":/feather/icons/feather/window_close.png",
            modalIcon=":/material_design/icons/material_design/info.png",
            description=description,
            isClosable=False,
            duration=3000
        )
        myModal.show()


    def update_custommodals_warning(self, description, pos='center-center'):

        myModal = QCustomModals.WarningModal(
            title="Information", 
            parent=self.myStackedWidget,
            position=pos,
            closeIcon=":/feather/icons/feather/window_close.png",
            modalIcon=":/material_design/icons/material_design/info.png",
            description=description,
            isClosable=False,
            duration=3000
        )
        myModal.show()


    def update_custommodals_info(self, description, pos='top-right'):

        myModal = QCustomModals.InformationModal(
            title="Information", 
            parent=self.myStackedWidget,
            position=pos,
            closeIcon=":/feather/icons/feather/window_close.png",
            modalIcon=":/material_design/icons/material_design/info.png",
            description=description,
            isClosable=False,
            duration=3000
        )
        myModal.show()

    def update_custommodals_SuccessModal2(self, description, pos='top-right'):

        myModal = QCustomModals.SuccessModal(
            title="Information", 
            parent=self.myStackedWidget,
            position=pos,
            closeIcon=":/feather/icons/feather/window_close.png",
            modalIcon=":/material_design/icons/material_design/info.png",
            description=description,
            isClosable=False,
            duration=5000
        )
        myModal.show()


    def update_custommodals_SuccessModal(self, description, pos='center-center'):

        myModal = QCustomModals.SuccessModal(
            title="Information", 
            parent=self.myStackedWidget,
            position=pos,
            closeIcon=":/feather/icons/feather/window_close.png",
            modalIcon=":/material_design/icons/material_design/info.png",
            description=description,
            isClosable=False,
            duration=5000
        )
        myModal.show()


    def display_user_message(self, message):
        # Adiciona a mensagem ao QTextEdit
        if self.chat_area:  # Verifique se o QTextEdit foi inicializado corretamente
            self.chat_area.append(message)  # Adiciona a mensagem ao campo de texto
        else:
            print("Erro: chat_area não está inicializado.")



    def is_image_file(self, file_name):
        # Verifica a extensão do arquivo
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        return file_name.lower().endswith(image_extensions)

    def get_machine_info(self):
        system_info = platform.uname()
        machine = system_info.node
        return machine

    
    def closeEvent(self, event):
        try:
            self.thread_processe_create_agent.stop()
        except:
            pass
        try:
            self.thread_process_create_openaikeys.stop()
        except:
            pass
        try:
            self.thread_process_create_GitHubKeys.stop()
        except:
            pass
        try:
            self.thread_process_create_Firebasekeys.stop()
        except:
            pass




        event.accept()






########################################################################
## EXECUTE APP
########################################################################
if __name__ == "__main__":
    app = QApplication(sys.argv)

    
    window = MainWindow()
    sys.exit(app.exec_())
########################################################################
## END===>
######################################################################## 
