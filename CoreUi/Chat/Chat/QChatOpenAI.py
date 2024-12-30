
import sys
import os


import struct
import re
import platform
import json
import ast
from firebase_admin import credentials, initialize_app, storage, db, delete_app
from datetime import datetime


# Caminho absoluto para o diretório onde SoftwareAI está localizado (raiz do projeto)
caminho_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SoftwareAI'))
sys.path.append(caminho_raiz)

from softwareai.CoreApp._init_core_ import OpenAIKeysinit,AutenticateAgent,Agent_files,  ResponseAgent, python_functions 


from softwareai.CoreUi.Chat.Chat.Formatmessage import format_message



from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


from typing import Optional, List, Union
from typing_extensions import override


class QChatOpenAi(QObject):
    chat = Signal(str)
    code = Signal(str)
    new_message = Signal(str)
    new_image = Signal(str)
    new_file = Signal(str)
    new_file_thread = Signal(list)
    new_file_codeinterpreter_mensage = Signal(str)
    new_file_codeinterpreter_thread = Signal(list)

    tokens = Signal(int)

    finished = Signal()
    
    def __init__(self,
                message,
                image,
                file,
                filethread,
                filecodeinterpreter_mensage,
                filecodeinterpreter_thread,
                keyAssistant,
                StorageAgentCompletions,
                StorageAgentOutput_,
                StoreFormatJsonAndJsonl,    
                key_api,
                appx
                ):
        super().__init__()
        
        self.message = message
        self.image = image
        self.file = file
        self.filecodeinterpreter_mensage = filecodeinterpreter_mensage
        self.filecodeinterpreter_thread = filecodeinterpreter_thread
        self.filethread = filethread

        self.StorageAgentCompletions = StorageAgentCompletions
        self.StorageAgentOutput_ = StorageAgentOutput_
        self.StoreFormatJsonAndJsonl = StoreFormatJsonAndJsonl

        self.keyAssistant = keyAssistant
        self.key_api = key_api
        self.appx = appx

        self.running = True
        self.cancelled = False

        self.new_message.connect(self.update_message)
        self.new_image.connect(self.update_image)
        self.new_file.connect(self.update_file)
        self.new_file_thread.connect(self.update_new_file_thread)
        self.new_file_codeinterpreter_mensage.connect(self.update_new_file_codeinterpreter_mensage)
        self.new_file_codeinterpreter_thread.connect(self.update_new_file_codeinterpreter_thread)


    def run(self):

        while self.running:

            if self.cancelled:
                self.finished.emit()

            if self.message:
                
                self.client = OpenAIKeysinit._init_client_(self.key_api)

                AI, instructionsassistant, nameassistant, model_select  = AutenticateAgent.create_or_auth_AI(
                    app1=self.appx,
                    client=self.client,
                    key=self.keyAssistant
                    
                )
                
                self.emit_message("user", self.message)

                mensaxgem = f"""{self.message} \n       
                
                """  
          
                mensaxgemfinal = mensaxgem 
                if self.image:
                    response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                            mensagem=mensaxgemfinal,
                                                                            agent_id=AI,
                                                                            key=self.keyAssistant,
                                                                            client=self.client,
                                                                            stream=True,
                                                                            streamLogger=self.chat,
                                                                            streamLoggerCode=self.code,
                                                                            Upload_1_image_for_vision_in_thread=self.image,
                                                                            model_select=model_select
                                                                            )
                elif self.file:
                    
                    response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                            mensagem=mensaxgemfinal,
                                                                            agent_id=AI,
                                                                            key=self.keyAssistant,
                                                                            client=self.client,
                                                                            stream=True,
                                                                            streamLogger=self.chat,
                                                                            streamLoggerCode=self.code,
                                                                            Upload_1_file_in_message=self.file,
                                                                            model_select=model_select
                                                                            )
                elif self.filethread:
                    
                    response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                            mensagem=mensaxgemfinal,
                                                                            agent_id=AI,
                                                                            key=self.keyAssistant,
                                                                            client=self.client,
                                                                            stream=True,
                                                                            streamLogger=self.chat,
                                                                            streamLoggerCode=self.code,
                                                                            Upload_multiples_file_in_thread=self.filethread,
                                                                            model_select=model_select
                                                                            )
                elif self.filecodeinterpreter_mensage:
                    
                    response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                            mensagem=mensaxgemfinal,
                                                                            agent_id=AI,
                                                                            key=self.keyAssistant,
                                                                            client=self.client,
                                                                            stream=True,
                                                                            streamLogger=self.chat,
                                                                            streamLoggerCode=self.code,
                                                                            Upload_1_file_for_code_interpreter_in_message=self.filecodeinterpreter_mensage,
                                                                            model_select=model_select
                                                                            )
                    
                elif self.filecodeinterpreter_thread:
                    
                    response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                            mensagem=mensaxgemfinal,
                                                                            agent_id=AI,
                                                                            key=self.keyAssistant,
                                                                            client=self.client,
                                                                            stream=True,
                                                                            streamLogger=self.chat,
                                                                            streamLoggerCode=self.code,
                                                                            Upload_list_for_code_interpreter_in_thread=self.filecodeinterpreter_thread,
                                                                            model_select=model_select
                                                                            )

                elif self.image == "" and self.file == "" and self.filethread == "" and self.filecodeinterpreter_mensage == "" and self.filecodeinterpreter_thread == "":

                    response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                            mensagem=mensaxgemfinal,
                                                                            agent_id=AI,
                                                                            key=self.keyAssistant,
                                                                            client=self.client,
                                                                            stream=True,
                                                                            streamLogger=self.chat,
                                                                            streamLoggerCode=self.code,
                                                                            model_select=model_select


                                                                            )


                if self.StorageAgentOutput_:

                    date = datetime.now().strftime('%Y-%m-%d')
                    output_path_jsonl = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/Destilation/{self.keyAssistant}/Jsonl'))
                    output_path_json = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/Destilation/{self.keyAssistant}/Json'))
                    os.makedirs(output_path_json, exist_ok=True)
                    os.makedirs(output_path_jsonl, exist_ok=True)
                    datasetjson = {
                        "input": mensaxgemfinal.strip(),
                        "output": response.strip()
                    }
                    datasetjsonl = {
                        "messages": [
                            {"role": "system", "content": f"{instructionsassistant}"},
                            {"role": "user", "content": f"{mensaxgemfinal.strip()}"},
                            {"role": "assistant", "content": f"{response.strip()}"}
                        ]
                    }
                    
                   

                    finaloutputjson = os.path.join(output_path_json, f"DestilationDateTime_{date.replace('-', '_').replace(':', '_')}.json")
                    with open(finaloutputjson, 'a', encoding='utf-8') as json_file:
                        json.dump(datasetjson, json_file, indent=4, ensure_ascii=False)
                    
                    finaloutputjsonl = os.path.join(output_path_jsonl, f"DestilationDateTime_{date.replace('-', '_').replace(':', '_')}.jsonl")
                    with open(finaloutputjsonl, 'a', encoding='utf-8') as json_file:
                        json_file.write(json.dumps(datasetjsonl, ensure_ascii=False) + '\n')


                refai_org_thread_Id = db.reference(f'ai_org_thread_Id/User_{self.keyAssistant}', app=self.appx)
                datarefai_org_thread_Id = refai_org_thread_Id.get()
                thread_Id = datarefai_org_thread_Id['thread_id']

                run_status = self.client.beta.threads.runs.list(
                    thread_id=thread_Id
                )
                jsonmodel = run_status.model_dump_json()
                with open("Cache/model_dump.json", 'w') as file:
                    file.write(jsonmodel)
                with open("Cache/model_dump.json", "r") as file:
                    data = json.load(file)  
                total_tokens_list = []
                prompt_tokens_list = []
                completion_tokens_list = []
                for run in data['data']:
                    total_tokens = run['usage']['total_tokens']
                    total_tokens_list.append(total_tokens)
                
                total_tokens = sum(total_tokens_list)
                self.tokens.emit(total_tokens)
                #self.emit_message("matrix", response)
                
                
                self.message = None
                self.image = None
                self.file = None
                self.filethread = None
                self.filecodeinterpreter_mensage = None
                self.filecodeinterpreter_thread = None


    def extract_python_code(self, text: str) -> Optional[str]:
        """
        Extract Python code from markdown code blocks.
        
        Args:
            text: String containing markdown-style code blocks
            
        Returns:
            Extracted code if found, None otherwise
        """
        # Pattern matches ```python followed by code and closing ```
        pattern = r"```python\s*(.*?)\s*```"
        match = re.search(pattern, text, re.DOTALL)
        
        if match:
            code = match.group(1).strip()
            self.code.emit(code)
            return code
        return None
    
    def emit_message(self, sender, message):
        """Emite a mensagem formatada com base no remetente, incluindo quebras de linha e formatação de código."""
        # Formata a mensagem com código
        self.extract_python_code(message)
        formatted_message = format_message(message)

        if sender == "user":
            formatted_message = (
                f'<div style="display: flex; justify-content: flex-end;">'
                f'<div style="background-color: #e0dddc; color: black; padding: 8px; border-radius: 8px; '
                f'margin: 5px; max-width: 70%;"><br><br><b>You:</b> {formatted_message} <br><br></div>'
                f'</div>'
            )
        elif sender == "matrix":
            formatted_message = (
                f'<div style="display: flex; justify-content: flex-start;">'
                f'<div style="color: black; padding: 8px; border-radius: 8px; '
                f'margin: 5px; max-width: 70%;"><b>MatrixAI:</b> {formatted_message}</div>'
                f'</div>'
            )

        self.chat.emit(formatted_message)

    def update_message(self, message):
        self.message = message
    
    def update_image(self, image):
        self.image = image
    
    def update_file(self, file):
        self.file = file

    def update_new_file_thread(self, filethread):
        self.filethread = filethread


    def update_new_file_codeinterpreter_mensage(self, filecodeinterpreter_mensage):
        self.filecodeinterpreter_mensage = filecodeinterpreter_mensage

    def update_new_file_codeinterpreter_thread(self, filecodeinterpreter_thread):
        self.filecodeinterpreter_thread = filecodeinterpreter_thread

    def cancel(self):
        self.running = False
        self.cancelled = True
        self.finished.emit()
        

    def stop(self):
        """Encerra a thread."""
        self.running = False
        


