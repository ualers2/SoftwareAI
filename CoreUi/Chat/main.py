
import os
import sys
caminho_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI'))
sys.path.append(caminho_raiz)
#########################################
# IMPORT SoftwareAI Libs 
from CoreApp._init_libs_ import *
#########################################
# IMPORT CoreApp
from CoreUi.Chat.Chat.QChatOpenAI import QChatOpenAi
from CoreUi.Chat.Chat.QReadOpenAI import QReadOpenAi
from CoreUi.Chat.Chat.QListAgent import QListAgents
from CoreUi.Chat.Chat.QAiRunnable import QAIRunnable
from CoreUi.Chat.Chat.HandleTextEdit import setup_plain_text_qtextedit
from CoreApp._init_core_ import(
        AutenticateAgent,
        ResponseAgent,
        python_functions,
        Agent_files,
        Agent_files_update,
        OpenAIKeysinit,
        FirebaseKeysinit
)
#########################################
# IMPORT .qrc
from src_ import icons_interpreter
#########################################
# IMPORT GUI 
from src_.ui_cliente_and_chat import *
from src_.ui_testedialog3 import Ui_Formtesete
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



# appx = keys_app_x()

# key_api = OpenAIKeys.keys_openai()
# client = OpenAI(
#     api_key=key_api,
# )



class CustomTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.container_widget = None
        self.editor = None

    def insert_code_editor(self, code):
        self.setStyleSheet("""QTextEdit {
                
                            border: 1px solid #E0E0E0;
                            padding: 10px;
                            border-radius: 10px;
                            background-color: #F7F7F7;
                            color: black;  /* Cor do texto preto */
                            font-family: Arial;
                            font-size: 14px;
                        }
                        """)

        # Remove o editor existente se já estiver inserido
        if self.editor is not None:
            self.editor.setParent(None)
            self.editor = None

        # Cria um arquivo temporário para o código
        temp_file_path = os.path.join(os.path.dirname(__file__), "temp_code.py")
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(code)

        # Cria o QCustomCodeEditor para exibir o arquivo de código temporário
        self.editor = QCustomCodeEditor()
        self.editor.setTheme("default")
        self.editor.setLang("python")
        self.editor.loadFile(temp_file_path)

        # Insere o editor diretamente no layout
        cursor = self.textCursor()
        cursor.insertBlock()  # Garante um bloco isolado
        self.setTextCursor(cursor)

        # Exibe o editor em uma janela separada
        container = QWidget(self)
        container.setLayout(QVBoxLayout())
        container.layout().addWidget(self.editor)

        self.container_widget = container

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

        loadJsonStyle(self, self.ui, jsonFiles = {"JsonStyle/style.json"})
        self.liveCompileQss = True
        self.checkForMissingicons = False # do not generate new icons

        self.AI_thread = None
        self.thread_pool = QThreadPool()

        Menu = self.ui.pushButton_16
        Menu.setObjectCustomTheme("#FFFAFA", "#7FFFD4")
        Menu.setObjectAnimateOn("hover")

        Send_mensage = self.ui.send_mensage
        # Send_mensage.setObjectCustomTheme("#FFFAFA", "#F0F8FF")
        # Send_mensage.setObjectAnimateOn("hover")
        Send_mensage.clicked.connect(self.send_message)

        self.AgentKeysOpenAI = self.ui.AgentKeysOpenAI
        self.StorageAgentCompletions = self.ui.StorageAgentCompletions
        self.StorageAgentOutput_ = self.ui.StorageAgentOutput_
        self.StoreFormatJsonAndJsonl = self.ui.StoreFormatJsonAndJsonl
        self.chat_area = self.ui.html_chat
        self.widget_frame_4 = self.ui.frame_4
        # layoutspinner = QVBoxLayout()
        # self.widget_frame_4.setLayout(layoutspinner)
        self.spinner =  QCustomPerlinLoader(
            parent=self.widget_frame_4,
            size=QSize(720, 720),
            message="LOADING...",
            color=QColor("white"),
            fontFamily="Ebrima",
            fontSize=25,
            rayon=200,
            duration=60 * 1000,
            noiseOctaves=0.8,
            noiseSeed=int(time.time()),
            backgroundColor=QColor("transparent"),
            circleColor1=QColor("#ff2e63"),
            circleColor2=QColor("#082e63"),
            circleColor3=QColor(57, 115, 171, 100)
        )
        self.spinner.show()
        
        self.load_AgentKeysOpenAI()
        # layoutspinner.addWidget(self.spinner)
        # layoutspinner.setAlignment(self.spinner, Qt.AlignCenter)

        self.sliddemenulousa = self.ui.sliddemenulousa
        self.widget_lousa = self.ui.widget_lousa
        layout = QVBoxLayout()
        self.widget_lousa.setLayout(layout)
        self.Blackboard = QCustomCodeEditor() #themes = ["default", "one-light", "one-dark", "monokai", "oceanic", "zenburn"]
        self.Blackboard.setTheme("one-dark")
        self.Blackboard.setLang("python")
        layout.addWidget(self.Blackboard)

        self.widget_lousa.close()
        self.sliddemenulousa.close()
        self.ui.widget.close()
        self.ui.pushButton_16.close()
        self.ui.mensage_input.close()
        self.ui.openLousa.close()
        self.ui.send_mensage.close()
        self.ui.pushButton_6.close()
        self.ui.atach_file.close()
        self.ui.html_chat.close()
        self.spinner.focusWidget()

        self.selected_image = None
        self.message_signal.connect(self.display_user_message)  
        self.chat_area.setReadOnly(True)
        self.message_input = self.ui.mensage_input
        setup_plain_text_qtextedit(self.message_input)
        self.message_input.textChanged.connect(lambda: self.adjust_height(increase=True))
        #self.message_input.keyPressEvent = self.keyPressEvent
        
        self.image_input = self.ui.pushButton
        self.image_input.clicked.connect(self.upload1imageforvisioninMensage)
        self.file_input = self.ui.atach_file
        self.file_input.clicked.connect(self.Update_Mensageatach)
        self.atachfilethread = self.ui.AtachFilesToThread_Benchmark
        self.atachfilethread.clicked.connect(self.clickatachfileinthread)
        self.AgentSelector = self.ui.SoftwareAIAgentsChat
        self.AgentSelector.currentTextChanged.connect(lambda: self.list_threads(agent=self.AgentSelector.currentText()))
        self.AgentSelector.currentTextChanged.connect(lambda: self.init_qchat_for_agent(agentkey=self.AgentSelector.currentText()))
        self.uploadfilestothread_file_search = self.ui.pushButton_3
        self.uploadfilestothread_file_search.clicked.connect(self.uploadfilesinthread)
        self.uploadfilestothread_Codeinterpreter = self.ui.pushButton_4
        self.uploadfilestothread_Codeinterpreter.clicked.connect(self.uploadfilestoCdeinterpreterinThread)
        self.uploadfilestomensage_file_search = self.ui.pushButton_7
        self.uploadfilestomensage_file_search.clicked.connect(self.uploadfilesinMensage)
        self.uploadfilestomensage_Codeinterpreter = self.ui.pushButton_8
        self.uploadfilestomensage_Codeinterpreter.clicked.connect(self.uploadfilestoCdeinterpreterinMensage)
        self.Threadlabel = self.ui.label_19
        self.Tokenslabel = self.ui.label_20

        #self.message_input.keyPressEvent(Qt.Key_Enter).connect(self.send_message)
        self.frame_4 = self.ui.frame_4
        self.widget_3 = self.ui.widget_3
        self.widget_4 = self.ui.widget_4

        self.QListAgentsThread = QListAgents()
        self.QListAgentsThread.AgentSelector.connect(self.update_QListAgentsThread)
        self.QListAgentsThread.messagesignal.connect(self.update_spinner)
        self.QListAgentsThread.start()

        self.AgentKeysOpenAI = self.ui.AgentKeysOpenAI
        self.AgentKeysFirebase = self.ui.AgentKeysFirebase
        
        self.load_AgentKeysOpenAI()
        
        self.load_AgentKeysFirebase()

        key_api = self.AgentKeysOpenAI.currentText()
        name_app = self.AgentKeysFirebase.currentText()
        self.client = OpenAIKeysinit._init_client_(key_api)
        self.app1 = FirebaseKeysinit._init_app_(name_app)

        #self.load_config()
    

        ########################################################################

        self.show()


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

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.send_message()  # Chama a função ao pressionar Enter

    def list_threads(self, agent):
        self.QRead_thread = QReadOpenAi(agent, self.app1, self.client)
        self.QRead_thread.Threadlabel.connect(self.update_Threadlabel)
        self.QRead_thread.Tokenslabel.connect(self.update_Tokenslabel)
        self.QRead_thread.htmlchat.connect(self.update_htmlchat)
        self.QRead_thread.code.connect(self.update_codeeditor)
        self.QRead_thread.messagesignal.connect(self.update_spinner)
        self.QRead_thread.finish.connect(self.finish_QReadOpenAi)
        self.QRead_thread.start()

    def init_qchat_for_agent(self, agentkey):

        if self.AI_thread:
            self.AI_thread.cancel()  
            QTimer.singleShot(1000, self.check_task_status)
        
        StorageAgentCompletions = self.StorageAgentCompletions.isChecked()
        StorageAgentOutput_ = self.StorageAgentOutput_.isChecked()
        StoreFormatJsonAndJsonl = self.StoreFormatJsonAndJsonl.isChecked()
        key_api = self.AgentKeysOpenAI.currentText()
        self.AI_thread = QChatOpenAi("", "", "", "", "", "", 
                                    agentkey, 
                                    StorageAgentCompletions,
                                    StorageAgentOutput_,
                                    StoreFormatJsonAndJsonl,
                                    key_api, self.app1
                                    )
        self.AI_thread.chat.connect(self.message_signal.emit)
        self.AI_thread.code.connect(self.update_codeeditor)
        self.AI_thread.finished.connect(self.update_finished)
        self.AI_thread.tokens.connect(self.update_tokens)
        runnable = QAIRunnable(self.AI_thread)
        self.thread_pool.start(runnable)

    def update_codeeditor(self, code):
        temp_file_path = os.path.join(os.path.dirname(__file__), "Cache", "temp_code.py")
        with open(temp_file_path, "w") as temp_file:
            temp_file.write(code)
        self.Blackboard.loadFile(temp_file_path)

    def display_user_message(self, message):
        self.chat_area.append(message)

    def load_AgentKeysOpenAI(self, chave = "str_key"):
        caminho_arquivo = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../CoreApp/KeysOpenAI/keys.py'))
        linhas_encontradas = []
        self.spinner.message = "Loading\nOpenAI keys"
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            for numero_linha, conteudo in enumerate(arquivo, start=1):
                if chave in conteudo:
                    strkey = conteudo.strip()
                    filterstrkey = strkey.replace('return', "").replace('"', "").replace(' ', "").replace('str_key', "").replace('=', "").replace("return str_key", "")
                    self.AgentKeysOpenAI.addItem(filterstrkey)

    def update_spinner(self, str):
        self.spinner.message = str

    def update_finished(self):
        print("thread finalizada")
 
    def finish_QReadOpenAi(self):
        self.spinner.close()
        self.sliddemenulousa.show()
        self.widget_lousa.show()
        self.ui.widget.show()
        self.ui.pushButton_16.show()
        self.ui.mensage_input.show()
        self.ui.openLousa.show()
        self.ui.send_mensage.show()
        self.ui.pushButton_6.show()
        self.ui.atach_file.show()
        self.ui.html_chat.show()

    def send_message(self):
        message = self.message_input.toPlainText()
        if message.strip():
            myModal = QCustomModals.InformationModal(
                title="Message Sent!!!", 
                parent=self,
                position='top-left',
                closeIcon=":/feather/icons/feather/window_close.png",
                modalIcon=":/feather/icons/feather/info.png",
                description="Your message has been sent",
                isClosable=False,
                duration=3000
            )
            myModal.show()

            self.AI_thread.new_message.emit(message)  

            self.message_input.clear()
        else:
            myModal = QCustomModals.ErrorModal(
                title="Message !!!", 
                parent=self,
                position='top-left',
                closeIcon=":/feather/icons/feather/window_close.png",
                modalIcon=":/feather/icons/feather/info.png",
                description="Your message is empty",
                isClosable=False,
                duration=3000
            )
            myModal.show()


    def upload1imageforvisioninMensage(self):
        dialog = QFileDialog()
        dialog.setStyleSheet("""
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
        """)
        dialog.setFileMode(QFileDialog.ExistingFile) 
        dialog.setWindowTitle("Select the image")
        dialog.setNameFilter("Imagens (*.png *.jpg *.jpeg);;Todos os Arquivos (*)")  # Filtro
        if dialog.exec_():
            self.selected_image = dialog.selectedFiles()[0]
            self.update_custommodals_SuccessModal2(f"Your image has been attributed to the message")
            html = f'<img src="{self.selected_image}" width="300" height="300">'
            self.chat_area.append(html)
            self.AI_thread.new_image.emit(self.selected_image)  

    def uploadfilesinthread(self):
        dialog = QFileDialog()
        dialog.setStyleSheet("""
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
        """)
        dialog.setFileMode(QFileDialog.ExistingFiles) 
        dialog.setWindowTitle("Select the File")
        dialog.setNameFilter("Todos os Arquivos (*)")  # Filtro
        if dialog.exec_():
            self.selected_file = dialog.selectedFiles()
            file_names = [os.path.basename(file) for file in self.selected_file]
            self.update_custommodals_SuccessModal2(f"Your File(s) have been attributed to the Thread")
            file_list_html = ''.join(
                f'<p><b>File:</b> <span style="color: #003366;"><b>{file_name}</b></span> <b>in Thread</b></p>' 
                for file_name in file_names
            )
            self.chat_area.append(file_list_html)
            self.AI_thread.new_file_thread.emit(self.selected_file)  
            self.custom_dialog.close()

    def uploadfilesinMensage(self):

        dialog = QFileDialog()
        dialog.setStyleSheet("""
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
        """)
        dialog.setFileMode(QFileDialog.ExistingFile) 
        dialog.setWindowTitle("Select the File")
        dialog.setNameFilter("Todos os Arquivos (*)")  # Filtro
        if dialog.exec_():
            self.selected_file = dialog.selectedFiles()[0]
            self.update_custommodals_SuccessModal2(f"Your File(s) have been attributed to the message")
            file_list_html = (
                f'<p><b>File:</b> <span style="color: #003366;"><b>{self.selected_file}</b></span> <b>in Mensage</b></p>' 
            )
            self.chat_area.append(file_list_html)
            self.AI_thread.new_file.emit(self.selected_file)  
            self.custom_dialogMensageatach.close()

    def uploadfilestoCdeinterpreterinMensage(self):

        dialog = QFileDialog()
        dialog.setStyleSheet("""
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
        """)
        dialog.setFileMode(QFileDialog.ExistingFile) 
        dialog.setWindowTitle("Select the File")
        dialog.setNameFilter("Todos os Arquivos (*)")  # Filtro
        if dialog.exec_():
            self.selected_file = dialog.selectedFiles()[0]
            self.update_custommodals_SuccessModal2(f"Your File(s) have been attributed to the message in context Code interpreter")
            file_list_html = (
                f'<p><b>File:</b> <span style="color: #003366;"><b>{os.path.basename(self.selected_file)}</b></span> <b>in message | Context Code Interpreter </b></p>' 
            )
            self.chat_area.append(file_list_html)
            self.AI_thread.new_file_codeinterpreter_mensage.emit(self.selected_file)  
            self.custom_dialogMensageatach.close()

    def uploadfilestoCdeinterpreterinThread(self):
        dialog = QFileDialog()
        dialog.setStyleSheet("""
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
        """)
        dialog.setFileMode(QFileDialog.ExistingFiles) 
        dialog.setWindowTitle("Select the File")
        dialog.setNameFilter("Todos os Arquivos (*)")  # Filtro
        if dialog.exec_():
            selected_files = dialog.selectedFiles()
            if len(selected_files) > 5:
                QMessageBox.warning(
                    dialog,
                    "Limite Excedido",
                    "Por favor, selecione no máximo 5 arquivos."
                )
            else:
                self.selected_files = selected_files
                self.update_custommodals_SuccessModal2(f"Your File(s) have been attributed to the Thread in context Code interpreter")
                file_names = [os.path.basename(file) for file in self.selected_files]
                file_list_html = ''.join(
                    f'<p><b>File:</b> <span style="color: #003366;"><b>{file_name}</b></span> <b>in Thread</b> | Context Code Interpreter </p>' 
                    for file_name in file_names
                )
                self.chat_area.append(file_list_html)
                self.AI_thread.new_file_codeinterpreter_thread.emit(self.selected_files)  
                self.custom_dialog.close()

    def Update_Mensageatach(self):
        from Custom_Widgets.QCustomQDialog import QCustomQDialog
        self.custom_dialogMensageatach = QCustomQDialog(
            title="Mensage Atach file",
            #description="This is a custom dialog.",
            showYesButton=False,
            showCancelButton=True,
            padding=20,
            margin=60,
            animationDuration=500,
            setModal=True,
            frameless=True,
            windowMovable=True,
            #showForm=Ui_Formtesete, #display a ui form inside the dialog box ie importing your form(from ui_form import myFormWidget)
            # to access the widgets inside your form (custom_dialog.shownForm.myWidgetName)
            parent=self.frame_4,
            addWidget=self.widget_4 #append another widget or widget container to the dialog
        )
        self.custom_dialogMensageatach.show()

    def adjust_height(self, increase=True):
        """
        Ajusta a altura do widget de entrada de mensagem com base no comprimento do texto atual.

        Parâmetros:
            increase (bool): Determina se a altura deve ser aumentada com base no comprimento do texto.
        """
        base_height = 48  # Altura base do widget
        max_height = 150  # Altura máxima permitida

        # Obtém o comprimento do texto atual
        current_text_length = len(self.message_input.toPlainText())

        # Se o texto for nulo, reseta à altura base
        if current_text_length == 0:
            self.message_input.setFixedHeight(base_height)
            return

        # Calcula a nova altura
        extra_lines = (current_text_length // 40) * 15  # Incrementa a altura a cada 40 caracteres
        if increase:
            new_height = min(base_height + extra_lines, max_height)
        else:
            new_height = max(base_height, max_height - extra_lines)

        # Aplica a nova altura
        self.message_input.setFixedHeight(new_height)

    def clickatachfileinthread(self):
        from Custom_Widgets.QCustomQDialog import QCustomQDialog
        self.custom_dialog = QCustomQDialog(
            title="Thread Atach file",
            #description="This is a custom dialog.",
            showYesButton=False,
            showCancelButton=True,
            padding=20,
            margin=60,
            animationDuration=500,
            setModal=True,
            frameless=True,
            windowMovable=True,
            #showForm=Ui_Formtesete, #display a ui form inside the dialog box ie importing your form(from ui_form import myFormWidget)
            # to access the widgets inside your form (custom_dialog.shownForm.myWidgetName)
            parent=self.frame_4,
            addWidget=self.widget_3 #append another widget or widget container to the dialog
        )
        self.custom_dialog.show()

    def update_custommodals_SuccessModal2(self, description, pos='top-right'):

        myModal = QCustomModals.SuccessModal(
            title="Information", 
            parent=self.ui.frame_4,
            position=pos,
            closeIcon=":/feather/icons/feather/window_close.png",
            modalIcon=":/material_design/icons/material_design/info.png",
            description=description,
            isClosable=False,
            duration=5000
        )
        myModal.show()

    def update_tokens(self, new_tokens):
        self.Tokenslabel.setText(f"{new_tokens} Tokens")

    def update_Tokenslabel(self, total_tokens):
        self.Tokenslabel.setText(f"{total_tokens} Tokens")

    def update_Threadlabel(self, thread_Id):
        self.Threadlabel.setText(f"Thread: {thread_Id[:23]}...")

    def update_htmlchat(self, chat):
        self.chat_area.append(chat)

    def init_paths_agents(self):
        paths_agents = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Software_Requirements_Analysis')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Software_Planning')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Software_Documentation')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Software_Development')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Pre_Project')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Company_Managers')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI/CoreApp/Agents/Company_CEO')),
        ]
        return paths_agents
    
    def update_QListAgentsThread(self, text):
        self.AgentSelector.addItem(text)

    def is_image_file(self, file_name):
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        return file_name.lower().endswith(image_extensions)
    
    def get_machine_info(self):
        system_info = platform.uname()
        machine = system_info.node
        return machine

    @Slot()
    def check_task_status(self):
        if self.AI_thread:
            QTimer.singleShot(1000, self.check_task_status) 
        else:
            print("check_task_status Tarefa concluída.")

    def closeEvent(self, event):
        try:
            self.AI_thread.stop()
        except:
            pass
        try:
            self.QListAgentsThread.stop()
        except:
            pass
        try:
            self.QRead_thread.stop()
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
