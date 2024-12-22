
## 🔄 Update

### QReadOpenAi: V 0.2.0.0
***(13/12/2024)***
Updates for version 0.2.0.0:
* **QReadOpenAi**: We created a Q Class to extract information from thread tokens and run.id that will be used to remember messages
```
├── 📁 CoreUi
    ├── 📁 ChatSoftwareAI
        ├── 📁 Chat
            ├── 🐍 AIQthread.py
                ├── 🔄 QReadOpenAi

Now:
```python



class QReadOpenAi(QThread):
    Threadlabel = Signal(str)
    Tokenslabel = Signal(int)
    htmlchat = Signal(str)
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

        print(agent)
        refai_org_assistant_id = db.reference(f'ai_org_assistant_id/User_{agent}', app=appx)
        dataai_org_assistant_id = refai_org_assistant_id.get()
        assistant_id = dataai_org_assistant_id['assistant_id']
        assistant_idstr =  str(assistant_id)

        refai_org_thread_Id = db.reference(f'ai_org_thread_Id/User_{agent}', app=appx)
        datarefai_org_thread_Id = refai_org_thread_Id.get()
        thread_Id = datarefai_org_thread_Id['thread_id']
        self.Threadlabel.emit(thread_Id)


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

    def emit_message(self, sender, message):
        """Emite a mensagem formatada com base no remetente, incluindo quebras de linha e formatação de código."""
        # Formata a mensagem com código
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
        """Encerra a thread."""
        self.running = False
        







```

#
### QChatOpenAi: V 0.2.0.0
***(13/12/2024)***
Updates for version 0.2.0.0:
* **QChatOpenAi**: We created a Q Class to receive and send messages, files and images provided by the user
```
├── 📁 CoreUi
    ├── 📁 ChatSoftwareAI
        ├── 📁 Chat
            ├── 🐍 AIQthread.py
                ├── 🔄 QChatOpenAi

Now:
```python


class QChatOpenAi(QObject):
    chat = Signal(str)
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
                client,
                appx
                ):
        super().__init__()
        
        self.message = message
        self.image = image
        self.file = file
        self.filecodeinterpreter_mensage = filecodeinterpreter_mensage
        self.filecodeinterpreter_thread = filecodeinterpreter_thread

        self.filethread = filethread

        self.keyAssistant = keyAssistant
        self.client = client
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
                AI, instructionsassistant, nameassistant, model_select  = AutenticateAgent.create_or_auth_AI(
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
                                                                            stream=True,
                                                                            streamLogger=self.chat,
                                                                            Upload_1_image_for_vision_in_thread=self.image,
                                                                            model_select=model_select
                                                                            )
                elif self.file:
                    
                    response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                            mensagem=mensaxgemfinal,
                                                                            agent_id=AI,
                                                                            key=self.keyAssistant,
                                                                            stream=True,
                                                                            streamLogger=self.chat,
                                                                            Upload_1_file_in_message=self.file,
                                                                            model_select=model_select
                                                                            )
                elif self.filethread:
                    
                    response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                            mensagem=mensaxgemfinal,
                                                                            agent_id=AI,
                                                                            key=self.keyAssistant,
                                                                            stream=True,
                                                                            streamLogger=self.chat,
                                                                            Upload_multiples_file_in_thread=self.filethread,
                                                                            model_select=model_select
                                                                            )
                elif self.filecodeinterpreter_mensage:
                    
                    response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                            mensagem=mensaxgemfinal,
                                                                            agent_id=AI,
                                                                            key=self.keyAssistant,
                                                                            stream=True,
                                                                            streamLogger=self.chat,
                                                                            Upload_1_file_for_code_interpreter_in_message=self.filecodeinterpreter_mensage,
                                                                            model_select=model_select
                                                                            )
                    
                elif self.filecodeinterpreter_thread:
                    
                    response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                            mensagem=mensaxgemfinal,
                                                                            agent_id=AI,
                                                                            key=self.keyAssistant,
                                                                            stream=True,
                                                                            streamLogger=self.chat,
                                                                            Upload_list_for_code_interpreter_in_thread=self.filecodeinterpreter_thread,
                                                                            model_select=model_select
                                                                            )

                elif self.image == "" and self.file == "" and self.filethread == "" and self.filecodeinterpreter_mensage == "" and self.filecodeinterpreter_thread == "":

                    response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                            mensagem=mensaxgemfinal,
                                                                            agent_id=AI,
                                                                            key=self.keyAssistant,
                                                                            stream=True,
                                                                            streamLogger=self.chat,
                                                                            model_select=model_select


                                                                            )

                refai_org_thread_Id = db.reference(f'ai_org_thread_Id/User_{self.keyAssistant}', app=self.appx)
                datarefai_org_thread_Id = refai_org_thread_Id.get()
                thread_Id = datarefai_org_thread_Id['thread_id']

                run_status = self.client.beta.threads.runs.list(
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
                    total_tokens_list.append(total_tokens)
                
                total_tokens = sum(total_tokens_list)
                self.tokens.emit(total_tokens)
                #self.emit_message("matrix", response)
                
                
                self.message = None
                self.image = None
                self.file = None


    def emit_message(self, sender, message):
        """Emite a mensagem formatada com base no remetente, incluindo quebras de linha e formatação de código."""
        # Formata a mensagem com código
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
        





```

#
### Core: V 0.1.9.9
***(13/12/2024)***
Updates for version 0.1.9.9:
* **codeinterpreter**: It is now possible to attach a list of files to the agent
```
├── 📁 CoreApp
    ├── 🐍 Core.py
        ├── 🔄 AutenticateAgent/create_or_auth_AI

Now:
```python
                if codeinterpreter:
                    list_file_id = []
                    for path in codeinterpreter:
                        file = client.files.create(
                            file=open(path, "rb"),
                            purpose='assistants'
                        )
                        list_file_id.append(file.id)
                    code_interpreter_in_agent = list_file_id

                    client.beta.assistants.update(
                        assistant_id=assistant.id,
                        tool_resources={
                        "code_interpreter": {
                            "file_ids": code_interpreter_in_agent
                            }
                        }
                    )


```

#
### formatmessage: V 0.1.9.8
***(13/12/2024)***
Updates for version 0.1.9.8:
* **formatmessage**: We create a regex for each parameter that symbolizes code, titles, etc., and add a styled html block
```
├── 📁 CoreUi
    ├── 📁 ChatSoftwareAI
        ├── 📁 Chat
            ├── 🐍 formatmessage.py
        

Now:
```python
import re
def format_message(message):
    """Formata a mensagem para detectar e estilizar código, palavras e títulos."""

    # Regex para blocos de código em Python
    code_pattern = r'```python(.*?)```'
    # Regex para palavras de destaque
    highlight_pattern = r'`(.*?)`'
    # Regex para títulos
    title_pattern = r'### (.+?):'
    # Regex para títulos 2
    title_pattern2 = r'(###\s.*)'

    # Regex para numeros antes do .
    numberbeforcepoint_pattern = r'(\d+\.)'

    # Regex para -
    list_pattern = r'(\s{3}-\s.*)'


    # Regex para palavras de minititulo
    minititulo_pattern = r'\*\*(.*?)\*\*'
    # Regex para listas seguidas de frases (ajustado para lidar com quebras de linha)
    list_with_phrase_pattern = r"(\d+\.\s?\*\*`.*?`(?:\*\*)?\s*):\s*(.*)"




    # Substitui blocos de código por HTML estilizado
    message = re.sub(
        code_pattern,
        lambda m: (
            '<div style="position: relative; background-color: #1E1E1E; color: #D4D4D4; padding: 12px; border-radius: 8px; '
            'border: 1px solid #3C3C3C; font-family: Consolas, \'Courier New\', monospace; font-size: 14px; overflow: auto;">'
            '<div style="position: absolute; top: 8px; right: 8px; background-color: #022740; '
            'color: #FFFFFF; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 12px;">'
            f'<b>#Python Code With {len(m.group(1).splitlines())} Lines</b>'
            '</div>'
            '<pre style="margin: 0; padding: 0; white-space: pre-wrap; background-color: #1E1E1E; color: #D4D4D4;">' +
            ''.join(
                f'{line}\n'
                for i, line in enumerate(m.group(1).splitlines())
            ).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>") +
            '</pre>'
            '</div>'
        ),
        message,
        flags=re.DOTALL
    )

    # Substitui listas seguidas de frases, garantindo que as quebras de linha sejam tratadas
    message = re.sub(
        list_with_phrase_pattern,
        lambda m: (
            f'<li style="background-color: #F7F7F7; color: #000000; padding: 8px 12px; '
            f'border-radius: 6px; margin: 6px 0;"><b>' + m.group(1).replace("\n", "").replace("**", "").replace(":", "-").strip() + '</b>:<span style="color: #3b302c;">' + m.group(2).replace("\n", "").strip() + '</span></li>'
        ),
        message
    )

    # # Substitui palavras de listas destacadas
    # message = re.sub(
    #     list_highlight_pattern,
    #     lambda m: (
    #         f'<li style="background-color: #F7F7F7; color: #000000; padding: 4px 8px; '
    #         f'border-radius: 4px; margin: 4px 0;"><b>' + m.group(1).replace("\n", "") + '</b></li>'
    #     ),
    #     message
    # )

    # Substitui palavras de destaque por um estilo específico
    message = re.sub(
        highlight_pattern,
        lambda m: (
            f'<span style="background-color: #F7F7F7; color: #000000; padding: 2px 4px; '
            f'border-radius: 3px;"><b>{m.group(1)}</b></span>'
        ),
        message
    )

    message = re.sub(
        minititulo_pattern,
        lambda m: (
            f'<span style="background-color: #F7F7F7; color: #022740; padding: 2px 4px; '
            f'border-radius: 3px;"><b>{m.group(1)}</b></span>'
        ),
        message
    )
   
   
    message = re.sub(
        numberbeforcepoint_pattern,
        lambda m: (
            f'<span style="background-color: #F7F7F7; color: #243096; padding: 2px 4px; '
            f'border-radius: 3px;"><b>{m.group(1).replace(".", ")")}</b></span>'
        ),
        message
    )

   
    message = re.sub(
        list_pattern,
        lambda m: (
            f'<span style="color: #1a0e03; padding: 2px 4px; '
            f'border-radius: 3px;">     {m.group(1)}</span>'
        ),
        message
    )


    message = re.sub(
        title_pattern,
        lambda m: (
            f'<h3 style="background-color: #F7F7F7; color: #000000; margin: 5px 0; font-size: 1.2em;"><b>{m.group(1)}</b></h3>'
        ),
        message
    )


    message = re.sub(
        title_pattern2,
        lambda m: (
            f'<h3 style="background-color: #F7F7F7; color: #000000; margin: 5px 0; font-size: 1.2em;"><b>{m.group(1).replace("### ", "")}</b></h3>'
        ),
        message
    )

    # Converte quebras de linha simples para `<br>` para manter parágrafos
    message = message.replace("\n", "<br>")

    return message



```

#

### improvement Core: V 0.1.9.7
***(13/12/2024)***
Updates for version 0.1.9.7:
* **Core**: Now it is possible to send a file for the purpose of code interpreter to Thread
```
├── 📁 CoreApp
    ├── 🐍 Core.py
        ├── 🔄 ResponseAgent/ResponseAgent_message_with_assistants

Now:
```python

        elif Upload_1_file_for_code_interpreter_in_message is not None:
            code_interpreter_in_thread = None
            file = client.files.create(
                file=open(Upload_1_file_for_code_interpreter_in_message, "rb"),
                purpose='assistants'
            )
        
            threead_id = AutenticateAgent.create_or_auth_thread(key, vectorstore_in_Thread, code_interpreter_in_thread)

            message = client.beta.threads.messages.create(
                thread_id=threead_id,
                role="user",
                content=mensagem,
                attachments=[{"file_id": file.id, "tools": [{"type": "code_interpreter"}]}]
                
            )
              


```

#

### improvement Core: V 0.1.9.6
***(13/12/2024)***
Updates for version 0.1.9.6:
* **Core**: ResponseAgent now has stream mode with logger for a QSignal
```
├── 📁 CoreApp
    ├── 🐍 Core.py
        ├── 🔄 ResponseAgent/ResponseAgent_message_with_assistants

Now:
```python

    code_buffer = None 
    formatted_output = ""

    if stream:
        accumulated_text = ""

        with client.beta.threads.runs.stream(
            thread_id=threead_id,
            assistant_id=agent_id,
            event_handler=EventHandler(),
            tools=[{"type": "file_search"}],
            model=model_select
        ) as stream:

            for text in stream.text_deltas:
                accumulated_text += text
                while len(accumulated_text) >= 100:
                    match = re.search(r"[ \n.,!?]+", accumulated_text[100:])
                    if match:
                        cut_index = 100 + match.start()
                    else:
                        cut_index = len(accumulated_text) 
                    chunk = accumulated_text[:cut_index]
                    accumulated_text = accumulated_text[cut_index:]

                    if code_buffer is not None:
                        code_buffer += chunk
                        if "```" in code_buffer:
                            code_content, _, remainder = code_buffer.partition("```")
                            formatted_output += (
                                '<div style="position: relative; background-color: #1E1E1E; color: #D4D4D4; padding: 12px; border-radius: 8px; '
                                'border: 1px solid #3C3C3C; font-family: Consolas, \'Courier New\', monospace; font-size: 14px; overflow: auto;">'
                                '<div style="position: absolute; top: 8px; right: 8px; background-color: #022740; '
                                'color: #FFFFFF; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 12px;">'
                                f'<b>#Python Code With {len(code_content.splitlines())} Lines</b>'
                                '</div>'
                                '<pre style="margin: 0; padding: 0; white-space: pre-wrap; background-color: #1E1E1E; color: #D4D4D4;">' +
                                ''.join(
                                    f'{line}\n'
                                    for i, line in enumerate(code_content.splitlines())
                                ).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>") +
                                '</pre>'
                                '</div>'
                            )
                            code_buffer = None
                            chunk = remainder
                        else:
                            continue 

                    while "```python" in chunk:
                        pre_code, _, rest = chunk.partition("```python")
                        formatted_output += format_message(pre_code)
                        chunk = rest

                        if "```" in chunk:
                            code_content, _, remainder = chunk.partition("```")
                            formatted_output += (
                                '<div style="position: relative; background-color: #1E1E1E; color: #D4D4D4; padding: 12px; border-radius: 8px; '
                                'border: 1px solid #3C3C3C; font-family: Consolas, \'Courier New\', monospace; font-size: 14px; overflow: auto;">'
                                '<div style="position: absolute; top: 8px; right: 8px; background-color: #022740; '
                                'color: #FFFFFF; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 12px;">'
                                f'<b>#Python Code With {len(code_content.splitlines())} Lines</b>'
                                '</div>'
                                '<pre style="margin: 0; padding: 0; white-space: pre-wrap; background-color: #1E1E1E; color: #D4D4D4;">' +
                                ''.join(
                                    f'{line}\n'
                                    for i, line in enumerate(code_content.splitlines())
                                ).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>") +
                                '</pre>'
                                '</div>'
                            )
                            chunk = remainder
                        else:
                            code_buffer = chunk
                            break  #

                    formatted_output += format_message(chunk)
                    streamLogger.emit(
                        f'<div style="display: flex; justify-content: flex-start;">'
                        f'<div style="color: black; padding: 8px; border-radius: 8px; margin: 5px; max-width: 70%;">'
                        f'{formatted_output}</div></div>'
                    )
                    formatted_output = ""

            if accumulated_text:
                formatted_output += format_message(accumulated_text)
                streamLogger.emit(
                    f'<div style="display: flex; justify-content: flex-start;">'
                    f'<div style="color: black; padding: 8px; border-radius: 8px; margin: 5px; max-width: 70%;">'
                    f'{formatted_output}</div></div>'
                )

            return accumulated_text, 0, 0, 0
```

#

### change _init_paths_: V 0.1.9.5
***(18/11/2024)***
Updates for version 0.1.9.5:
* **_init_paths_**: change _init_paths_ 
```
├── 📁 CoreApp
    ├── 🐍 _init_paths_.py
```
Before:
```python
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "ambiente.env"))
load_dotenv(find_dotenv('ambiente.env'), override=True)
```
Now:
```python
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "environment.env"))
load_dotenv(find_dotenv('environment.env'), override=True)
```

#
### change AI_ByteManager_Company_CEO: V 0.1.9.4
***(18/11/2024)***
Updates for version 0.1.9.4:
* **AI_ByteManager_Company_CEO**: change AI_ByteManager_Company_CEO 
```
├── 📁 CoreApp
    ├── 📁 Agents
        ├── 📁 Company_CEO
            ├── 🐍 AI_ByteManager_Company_CEO.py
```
Before:
```python
load_dotenv(dotenv_path=r"C:\Users\Media Cuts Studio\Desktop\Saas do site\Projetos de codigo aberto\SoftwareAI\CoreApp\ambiente.env")
```
Now:
```python
def load_env(self):
    """
    Method to load the .env file located in the two folders above the script.
    """
    # Caminho relativo para o .env
    script_dir = os.path.dirname(__file__)
    env_path = os.path.abspath(os.path.join(script_dir, "../..", "environment.env"))
    
    # Carregar o arquivo .env se ele existir
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f".env carregado de: {env_path}")
    else:
        print(f"Erro: Arquivo environment.env não encontrado em {env_path}")

self.load_env()
```

#
### change name ambiente: V 0.1.9.3
***(18/11/2024)***
Updates for version 0.1.9.3:
* **ambiente**: change ambiente to  environment
```
├── 📁 CoreApp
    ├── 📑 environment.env
```
Before:
```bash
ambiente.env
```
Now:
```bash
environment.env
```

### Structure: V 0.1.9.2
***(18/11/2024)***
Updates for version 0.1.9.2:
* **Structure**: improvement 
    - [📁 Project Structure](#-softwareai-structure)
#
### SoftwareAI-Roadmap improviments: V 0.1.9.1
***(17/11/2024)***
Updates for version 0.1.9.1:
* **SoftwareAI-Roadmap**: improvement 
```
    ├── 📁 CoreApp
    │   ├── 📁Roadmaps
    │   ├── 📑 SoftwareAI-Roadmap.md

```
```bash
- [ ] name refactoring in 'Create_Cronograma_e_planilha_Projeto', 'Create_doc_Pre_Projeto', 'Create_documentation', 'Create_Roadmap_Projeto', 'Software_Development', 'Software_Requirements_Analysis'
- [ ] ask the QuantumCore to create and structure the 'Software_Development' folder according to the project
- [ ] 
```
#
### _init_paths_ improviments: V 0.1.9.0
***(17/11/2024)***
Updates for version 0.1.9.0:
* **_init_paths_**: improvement when loading dot env
```
    ├── 📁 CoreApp
    │   ├── 🐍 _init_paths_.py
```
Before:
```python
load_dotenv(dotenv_path=r"C:\Users\Media Cuts Studio\Desktop\Saas do site\Projetos de codigo aberto\SoftwareAI\CoreApp\ambiente.env")
```
Now:
```python
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "ambiente.env"))
```

#
### _init_libs_ improviments: V 0.1.8.9
***(17/11/2024)***
Updates for version 0.1.8.9:
* **_init_libs_**: duplicate imports removed
    ```
        ├── 📁 CoreApp
        │   ├── 🐍 _init_libs_.py
    ```
#
### _init_libs_ improviments: V 0.1.8.8
***(17/11/2024)***
Updates for version 0.1.8.8:
* **_init_libs_**: duplicate imports removed
    ```
        ├── 📁 CoreApp
        │   ├── 🐍 _init_libs_.py
    ```
#
### _init_agents_ improviments: V 0.1.8.7
***(17/11/2024)***
Updates for version 0.1.8.7:
* **_init_agents_**: comments in code removed
    ```
        ├── 📁 CoreApp
        │   ├── 🐍 _init_agents_.py
    ```
#

### FirebaseKeys change: V 0.1.8.6
***(17/11/2024)***
Updates for version 0.1.8.6:
* **FirebaseKeys**: FirebaseKeys Change to KeysFirebase
    ```
        ├── 📁 CoreApp
        │   ├── 📁 KeysFirebase
    ```
#

### SoftwareAI_Core change: V 0.1.8.5
***(17/11/2024)***
Updates for version 0.1.8.5:
* **SoftwareAI_Core**: SoftwareAI_Core Change to Core
    ```
        ├── 📁 CoreApp
        │   ├── 📁 SoftwareAI
        │   │   ├── 🐍 Core.py 
    ```



### KeysGitHub add: V 0.1.8.4
***(17/11/2024)***
Updates for version 0.1.8.4:
* **KeysGitHub**: the KeysGitHub folder was added for better structuring of the ​​softwareAI
    ```
        ├── 📁 CoreApp
        │   ├── 📁 KeysGitHub
        │   │   ├── 🐍 keys.py 
    ```

### KeysOpenAI add: V 0.1.8.3
***(17/11/2024)***
Updates for version 0.1.8.3:
* **KeysOpenAI**: the KeysOpenAI folder was added for better structuring of the ​​softwareAI
    ```
        ├── 📁 CoreApp
        │   ├── 📁 KeysOpenAI
        │   │   ├── 🐍 keys.py 
    ```

### Upload_image_for_vision_in_thread remove: V 0.1.8.2
***(17/11/2024)***
Updates for version 0.1.8.2:
* **upload_image_for_vision_in_thread**: the function that was deprecated was removed
    ```
        def upload_image_for_vision_in_thread(image_file_path: str, thread_id: str):
    ```

### Store added: V 0.1.8.1
***(17/11/2024)***
Updates for version 0.1.8.1:
* **Chat completion storage was added**:  enabling the evaluation and adjustment of the model for specific criteria
    ```
        data = {
            "model": "gpt-4o-mini",  
            "messages": mensagem,
            "store": True,
            "max_tokens": 16_384,
            "response_format": { "type": formato },
        }

    ```

### add Roadmaps, Docs, _init_paths_.py, Fluxogram beta v 0.1.8.pdf, Instructions, Tools ***(16/11/2024)***  SoftwareAI 0.1.8



### CoreApp completely refactored, After complications in intracommunication between teams using the QT5/pyside6  interface, we decided to postpone the interface and leave the core of the application well done so that others can create relatively good software in version 0.1.9 with one click. ***(09/11/2024)***  SoftwareAI 0.1.8


### Launch of ByteManager, initially part of the Company Owner, the objective is to control and manage all steps of all teams ***(15/10/2024)***  SoftwareAI 0.1.7



### Launch of CloudArchitect, the objective is to develop software documentation for repositories on GitHub based on documentation already created with the company's standard***(15/10/2024)*** SoftwareAI 0.1.7


### Launch of SignalMaster, The objective is to receive Python scripts or software developed by the team and improve them based on software development standards already in production at the company, which will be provided via vectorstore: ***(07/10/2024)***  SoftwareAI 0.1.7

#
### Launch of DataWeaver, The objective is to analyze current software and suggest improvements based on software projects already in production, which are stored in the vectorstore called All_Software_in_company: ***(07/10/2024)***  SoftwareAI 0.1.6

#
### Launch of QuantumCore , O objetivo é desenvolver software de alta qualidade com base nos requisitos fornecidos pelo Analista de Requisitos de Software e nos padrões de software já existentes na empresa: ***(07/10/2024)***  SoftwareAI 0.1.5

#
### Launch of SynthOperator, Software Requirements Analyst, objective is to receive and analyze Roadmap, Schedule, Spreadsheet and Pre-Project Document: ***(06/10/2024)***  SoftwareAI 0.1.4

#

### Launch of CloudArchitect, responsibility is to create technical documentation for software projects based on Roadmap, Schedule, Spreadsheet and Pre-Project Document: ***(06/10/2024)***  SoftwareAI 0.1.3 pending


#
### Launch of Dallas, The objective is to plan a Project Roadmap based on the Schedule, Spreadsheet and Pre-Project Document: ***(06/10/2024)***  SoftwareAI 0.1.2
#
### Launch of Bob, The objective is to create a Project schedule and spreadsheet based on the Pre-Project Document: ***(06/10/2024)***  SoftwareAI 0.1.1 
#
### Launch of Tigrao Software Pre Project Document Writer: ***(28/09/2024)***  SoftwareAI 0.1.1   
### Launch of the application core : ***(16/09/2024)***  SoftwareAI 0.1.0   

