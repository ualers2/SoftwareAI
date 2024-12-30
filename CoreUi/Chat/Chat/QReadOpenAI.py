
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

from softwareai.CoreUi.Chat.Chat.Formatmessage import format_message



from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


from typing import Optional, List, Union
from typing_extensions import override



class QReadOpenAi(QThread):
    Threadlabel = Signal(str)
    Tokenslabel = Signal(int)
    htmlchat = Signal(str)
    code = Signal(str)
    messagesignal = Signal(str)
    finish = Signal()
    def __init__(self, agent, appx, client
                ):
        super().__init__()
        
        self.agent = agent
        self.appx = appx
        self.client = client

    def run(self):
        agent = self.agent
        appx = self.appx
        client = self.client
        refai_org_assistant_id = db.reference(f'ai_org_assistant_id/User_{agent}', app=appx)
        dataai_org_assistant_id = refai_org_assistant_id.get()
        assistant_id = dataai_org_assistant_id['assistant_id']
        assistant_idstr =  str(assistant_id)
        self.messagesignal.emit("Agent fetched\nfrom firebase")
        refai_org_thread_Id = db.reference(f'ai_org_thread_Id/User_{agent}', app=appx)
        datarefai_org_thread_Id = refai_org_thread_Id.get()
        thread_Id = datarefai_org_thread_Id['thread_id']
        self.Threadlabel.emit(thread_Id)
        self.messagesignal.emit("Thread fetched\nfrom firebase")
        run_status = client.beta.threads.runs.list(
            thread_id=thread_Id
        )
        jsonmodel = run_status.model_dump_json()
        with open("Cache/model_dump_json.json", 'w') as file:
            file.write(jsonmodel)
        with open("Cache/model_dump_json.json", "r") as file:
            data = json.load(file)  
        total_tokens_list = []
        prompt_tokens_list = []
        completion_tokens_list = []
        for run in data['data']:
            total_tokens = run['usage']['total_tokens']
            prompt_tokens = run['usage']['prompt_tokens']
            completion_tokens = run['usage']['completion_tokens']
            total_tokens_list.append(total_tokens)
            prompt_tokens_list.append(prompt_tokens)
            completion_tokens_list.append(completion_tokens)

        self.messagesignal.emit("Thread\nRemembered")

        total_tokens = sum(total_tokens_list)
        self.Tokenslabel.emit(total_tokens)
        prompt_tokens = sum(prompt_tokens_list)
        completion_tokens = sum(completion_tokens_list)
        contador_1 = 0
        ids = [item['id'] for item in data['data']]
        for id in ids:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_Id,
                run_id=id
            )

            messages = client.beta.threads.messages.list(
                thread_id=thread_Id
            )
            for message in messages:
                for mensagem_contexto in message.content:
                    valor_texto = mensagem_contexto.text.value
                    print(valor_texto)
                    self.emit_message("messagethread", valor_texto)
                    contador_1 += 1
                    if contador_1 == 5:
                        break
                break
            break
        self.finish.emit()

    def extract_python_code(self, text: str) -> Optional[str]:
        pattern = r"```python\s*(.*?)\s*```"
        match = re.search(pattern, text, re.DOTALL)
        
        if match:
            code = match.group(1).strip()
            self.code.emit(code)
            return code
        return None
    
    def emit_message(self, sender, message):
        self.extract_python_code(message)
        formatted_message = format_message(message)

        if sender == "Chat":
            formatted_message = (
                f'<div style="display: flex; justify-content: flex-end;">'
                f'<div style="background-color: #d4f4dd; color: black; padding: 8px; border-radius: 8px; '
                f'margin: 5px; max-width: 70%;"><b>user:</b> {formatted_message}</div>'
                f'</div>'
            )
        elif sender == "messagethread":
            formatted_message = (
                f'<div style="display: flex; justify-content: flex-start;">'
                f'<div style=color: black; padding: 8px; border-radius: 8px; '
                f'margin: 5px; max-width: 70%;"><b>Message Remembered From Thread:</b> <br>{formatted_message}<br></div>'
                f'</div>'
            )

        self.htmlchat.emit(formatted_message)

    def stop(self):
        self.running = False
        


