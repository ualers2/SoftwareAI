######################################### SoftwareAI Core #########################################

# IMPORT SoftwareAI Functions
from softwareai.CoreApp.SoftwareAI.Functions._init_functions_ import *
#########################################
# IMPORT SoftwareAI Functions Submit Outputs
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs._init_submit_outputs_ import _init_output_
#########################################
# IMPORT SoftwareAI Agents 
from softwareai.CoreApp._init_agents_ import *
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Keys 
from softwareai.CoreApp._init_keys_ import *
#########################################
# IMPORT Formatmessage
from softwareai.CoreUi.Chat.Chat.Formatmessage import format_message


class FirebaseKeysinit:
    def _init_app_(name_app):
        module_path = "softwareai.CoreApp.KeysFirebase.keys"
        keys_module = importlib.import_module(module_path)
        imported_name_app = getattr(keys_module, name_app)
        appfb = imported_name_app()
        return appfb

class OpenAIKeysinit:
    
    def _init_client_(key_api):
        client = OpenAI(
            api_key=key_api,
        )
        return client


class AutenticateAgent:

    def create_or_auth_vectorstoreadvanced(key, UseVectorstoreToGenerateFiles, app1):
        """
        This function checks if a user's vectorstore advanced settings exist in the database.

        Parameters:
        ----------
        key : str
            The unique identifier for the user.
        UseVectorstoreToGenerateFiles : bool
            The boolean indicating whether vectorstore advanced features should be used.

        Returns:
        --------
        str
            A string representing the value of the 'UseVectorstoreToGenerateFiles' setting.

        Raises:
        -------
        Exception
            If an error occurs during the process.

        Example:
        --------
        >>> create_or_auth_vectorstoreadvanced('user123', True)
        'True'

        Note:
        -----
        - The function first attempts to retrieve the current 'UseVectorstoreToGenerateFiles' setting for the specified user from the database.
        - If the setting does not exist, it adds the setting to the database with the provided value and returns that value.
        
        """

        try:
            ref1 = db.reference(f'ai_org_vectorstoreadvanced/User_{key}', app=app1)
            data1 = ref1.get()
            UseVectorstoreToGenerateFiles = data1['UseVectorstoreToGenerateFiles']
            return str(UseVectorstoreToGenerateFiles)
        except Exception as err234:
            ref1 = db.reference(f'ai_org_vectorstoreadvanced', app=app1)
            controle_das_funcao2 = f"User_{key}"
            controle_das_funcao_info_2 = {
                "UseVectorstoreToGenerateFiles": f'{UseVectorstoreToGenerateFiles}'
            }
            ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)
            return str(UseVectorstoreToGenerateFiles)

    def create_or_auth_AI(
        app1,
        client,
        key: str, 
        instructionsassistant: Optional[str] = None,
        nameassistant: Optional[str] = None, 
        model_select: Optional[str] = "gpt-4o-mini-2024-07-18", 
        tools: Optional[List] = None,
        vectorstore: Optional[List] = None,
        codeinterpreter: Optional[List] = None,
        ):
        """ 
        :param key: this is the key that represents the agent in the database
            
        :param instructionsassistant: This argument is the instruction of the agent's behavior The maximum length is 256,000 characters.
        
        :param nameassistant: This argument is the name of the agent The maximum length is 256 characters.
        
        :param model_select: This argument is the AI model that the agent will use
            
        :param tools: This argument is the agent's tools  There can be a maximum of 128 tools per assistant. Tools can be of types code_interpreter, file_search, vectorstore, or function.
            
        :param vectorstore: This argument is the vector storage id desired when creating or authenticating the agent
            
        """


        try:
            ref1 = db.reference(f'ai_org_assistant_id/User_{key}', app=app1)
            data1 = ref1.get()
            assistant_id = data1['assistant_id']
            instructionsassistant = data1['instructionsassistant']
            nameassistant = data1['nameassistant']
            model_select = data1['model_select']
            
            if tools:
                client.beta.assistants.update(
                    assistant_id=str(assistant_id),
                    tools=tools
                    
                )

            if vectorstore:
                client.beta.assistants.update(
                    assistant_id=str(assistant_id),
                    tool_resources={"file_search": {"vector_store_ids": vectorstore}},
                )

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
                    assistant_id=str(assistant_id),
                    tool_resources={
                    "code_interpreter": {
                        "file_ids": code_interpreter_in_agent
                        }
                    }
                )

            return str(assistant_id), str(instructionsassistant), str(nameassistant), str(model_select)
        except Exception as err234:
            if tools:
                assistant = client.beta.assistants.create(
                    name=nameassistant,
                    tools=tools,
                    instructions=instructionsassistant,
                    model=model_select,
                )
                if vectorstore:
                    client.beta.assistants.update(
                        assistant_id=assistant.id,
                        tool_resources={"file_search": {"vector_store_ids": vectorstore}},
                    )

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
            else:

                assistant = client.beta.assistants.create(
                    name=nameassistant,
                    tools=[{"type": "file_search"}, {"type": "code_interpreter"}],
                    instructions=instructionsassistant,
                    model=model_select,
                )
                if vectorstore:
                    client.beta.assistants.update(
                        assistant_id=assistant.id,
                        tool_resources={"file_search": {"vector_store_ids": vectorstore}},
                    )

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

                    

            ref1 = db.reference(f'ai_org_assistant_id', app=app1)
            controle_das_funcao2 = f"User_{key}"
            controle_das_funcao_info_2 = {
                "assistant_id": f'{assistant.id}',
                "instructionsassistant": f'{instructionsassistant}',
                "nameassistant": f'{nameassistant}',
                "model_select": f'{model_select}',
                "tools": f'{tools}',
                "key": f'{key}',
            }
            ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)
            return str(assistant.id), str(instructionsassistant), str(nameassistant), str(model_select)
        
    def create_or_auth_thread(app1, client, key, 
                            attachavectorstoretoThreads: Optional[List] = None,
                            code_interpreter_in_thread=None
                            ):
        """ 
        :param key: this is the key that represents the agent in the database
        :param file_in_thread: This argument is the id of the desired file in the thread
        :param attachavectorstoretoThreads: attach a vector store to Threads "vector_store_ids": ["vs_2"]

        """

        
        try:
            ref1 = db.reference(f'ai_org_thread_Id/User_{key}', app=app1)
            data1 = ref1.get()
            thread_Id = data1['thread_id']
            print(thread_Id)
            if attachavectorstoretoThreads:
                client.beta.threads.update(
                    thread_id=str(thread_Id),
                    tool_resources={
                        "file_search": {
                        "vector_store_ids": attachavectorstoretoThreads
                        }
                    }
                    
                )
            if code_interpreter_in_thread:    
                thread = client.beta.threads.update(
                    thread_id=str(thread_Id),
                    tool_resources={"code_interpreter": {
                        "file_ids": code_interpreter_in_thread
                        }
                    }
                )

            return str(thread_Id)
        except Exception as err234z:
            print(err234z)
            tool_resources = {}
            if attachavectorstoretoThreads:
                tool_resources["file_search"] = {"vector_store_ids": attachavectorstoretoThreads}

            if code_interpreter_in_thread:
                tool_resources["code_interpreter"] = {"file_ids": code_interpreter_in_thread}


            thread = client.beta.threads.create(
                tool_resources=tool_resources
            )

            ref1 = db.reference(f'ai_org_thread_Id', app=app1)
            controle_das_funcao2 = f"User_{key}"
            controle_das_funcao_info_2 = {
                "thread_id": f'{thread.id}',
                "key": f'{key}'
            }
            ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)

            return str(thread.id)

class ResponseAgent:

    def ResponseAgent_message_completions(prompt, key_api, sistema = "", json_format = True, store=True):
        """
        Sends a message to an OpenAI chat model and returns the completion.

        Parameters:
        - prompt (str): The text that the assistant will respond to.
        - sistema (str, optional): A system instruction for the assistant. Defaults to an empty string.
        - json_format (bool, optional): Whether the response should be returned as a JSON object or plain text. Defaults to True.

        Returns:
        - str: The response from the assistant.

        Raises:
        - Exception: If there is an error during the API request.

        Example:
        >>> ResponseAgent_message_completions("Hello, how are you?")
        'I am good, thank you!'

        Note:
        - The API key `key_api` must be set before calling this function.
        """
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {key_api}",
            "Content-Type": "application/json"
        }

        formato = "text"
        if json_format:
            formato = "json_object"

        mensagem = []
        if sistema != "":
            mensagem.append({"role": "system", "content": sistema})
        mensagem.append({"role": "user", "content": prompt})

        data = {
            "model": "gpt-4o-mini",  
            "messages": mensagem,
            "store": store,
            "max_tokens": 16_384,
            "response_format": { "type": formato },
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            response_json = response.json()
            if json_format:
                return json.loads(response_json['choices'][0]['message']['content'])
            return response_json['choices'][0]['message']['content']
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
        
    def ResponseAgent_message_with_assistants(
                                            mensagem: str,
                                            agent_id: str,
                                            key: str,
                                            app1, 
                                            client,
                                            stream: bool = False,
                                            streamLogger: Optional[Signal] = None,
                                            streamLoggerCode: Optional[Signal] = None,
                                            tools: Optional[List] = None,
                                            model_select: Optional[str] = None,
                                            aditional_instructions: Optional[str] = None,
                                            Upload_multiples_file_in_thread: Optional[List[str]] = None,
                                            Upload_1_file_in_message: Optional[str] = None,
                                            Upload_1_image_for_vision_in_thread: Optional[str] = None,
                                            Upload_list_for_code_interpreter_in_thread: Optional[list] = None,
                                            Upload_1_file_for_code_interpreter_in_message: Optional[str] = None,
                                            vectorstore_in_Thread: Optional[List] = None,

                                            
                                        ):
        
        """ 
        :param mensagem: This argument is the desired message that the agent responds to | If not use = None
            
        :param Upload_multiples_file_in_thread: This argument is the location of the file that will be uploaded to the thread | If not use = None
        
        :param Upload_1_file_in_message: This argument is the location of the file that will be uploaded along with the message | If not use = None
        
        :param Upload_1_image_for_vision_in_thread: This argument is the location of the image that will be loaded into the thread along with the message with the aim of vision | If not use = None
        
        :param Upload_list_for_code_interpreter_in_thread: This argument is the list of files that will be loaded into the thread along with the message for the purpose of code interpreter| If not use = None
        
        :param Upload_1_file_for_code_interpreter_in_message: This argument is the 1 of file that will be loaded into the thread along with the message for the purpose of code interpreter| If not use = None
        
        :param vectorstore_in_Thread: This argument is a storage list of vectors that will be loaded into the thread along with the message | If not use = None
        
        :param tools: This argument is the tools that will be used | If not use = None
        
        :param agent_id: This argument is the id of the authenticated or created agent
            
        :param model_select: This argument is the AI model that the agent will use
        
        :param aditional_instructions: This argument is an additional instruction to the agent's behavior | If not use = None

        :param key: this is the key that represents the agent in the database


        
        """

        
        if Upload_1_image_for_vision_in_thread is not None and Upload_1_image_for_vision_in_thread != "":
            code_interpreter_in_thread = None
            with open(Upload_1_image_for_vision_in_thread, "rb") as image_file:
                file = client.files.create(
                    file=image_file,
                    purpose="vision"
                )

                threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key,  vectorstore_in_Thread, code_interpreter_in_thread)

                message = client.beta.threads.messages.create(
                    thread_id=threead_id,
                    role="user",
                    content=[
                            {
                                "type": "text",
                                "text": f"""{mensagem}"""
             
                            },
                            {
                                "type": "image_file",
                                "image_file": {"file_id": file.id} 
                            }
                        ]
                )

        elif Upload_1_file_in_message is not None:
            code_interpreter_in_thread = None
            message_file = client.files.create(
                file=open(Upload_1_file_in_message, "rb"), purpose="assistants"
            )
            threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key, vectorstore_in_Thread, code_interpreter_in_thread)

            message = client.beta.threads.messages.create(
                thread_id=threead_id,
                role="user",
                content=mensagem,
                attachments=[{"file_id": message_file.id, "tools": [{"type": "file_search"}]}]
            )

        elif Upload_multiples_file_in_thread is not None:
            code_interpreter_in_thread = None
            list_as_string = json.dumps(Upload_multiples_file_in_thread)
            namehash = hashlib.sha256(list_as_string.encode()).hexdigest()
            vector_store = client.beta.vector_stores.create(name=f"Upload_{namehash[:5]}")
            file_streams = [open(path, "rb") for path in Upload_multiples_file_in_thread]
            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id, files=file_streams
            )
            print(file_batch.status)
            print(file_batch.file_counts)
            threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key,  [vector_store.id], code_interpreter_in_thread)
            message = client.beta.threads.messages.create(
                thread_id=threead_id,
                role="user",
                content=mensagem,
            )   
        elif Upload_list_for_code_interpreter_in_thread is not None:
            list_file_id = []
            for path in Upload_list_for_code_interpreter_in_thread:
                file = client.files.create(
                    file=open(path, "rb"),
                    purpose='assistants'
                )
                list_file_id.append(file.id)
            code_interpreter_in_thread = list_file_id
            threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key,  vectorstore_in_Thread, code_interpreter_in_thread)

            message = client.beta.threads.messages.create(
                thread_id=threead_id,
                role="user",
                content=mensagem,
            )   
        elif Upload_1_file_for_code_interpreter_in_message is not None:
            code_interpreter_in_thread = None
            file = client.files.create(
                file=open(Upload_1_file_for_code_interpreter_in_message, "rb"),
                purpose='assistants'
            )
            threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key,  vectorstore_in_Thread, code_interpreter_in_thread)

            message = client.beta.threads.messages.create(
                thread_id=threead_id,
                role="user",
                content=mensagem,
                attachments=[{"file_id": file.id, "tools": [{"type": "code_interpreter"}]}]
            )
              
        elif Upload_1_image_for_vision_in_thread is None and Upload_1_image_for_vision_in_thread != "" and Upload_1_file_in_message is None and Upload_multiples_file_in_thread is None and Upload_list_for_code_interpreter_in_thread is None:
            code_interpreter_in_thread = None
            threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key,  vectorstore_in_Thread, code_interpreter_in_thread)
   
            message = client.beta.threads.messages.create(
                thread_id=threead_id,
                role="user",
                content=mensagem,
                
            )   

        code_buffer = None 
        formatted_output = ""

        if stream:
            accumulated_text = ""
            total_text = ""
            with client.beta.threads.runs.stream(
                thread_id=threead_id,
                assistant_id=agent_id,
                event_handler=EventHandler(),
                tools=[{"type": "file_search"}],
                model=model_select
            ) as stream:

                for text in stream.text_deltas:
                    accumulated_text += text
                    total_text += text
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
                                streamLoggerCode.emit(code_content.strip())  
                                formatted_output += '<pre style="margin: 0; padding: 0; white-space: pre-wrap; background-color: #F7F7F7; color: #0e6303;"><b>[CODE ON THE BOARD]</b>'
                                code_buffer = None  
                                chunk = remainder
                            else:
                                continue

                        while "```python" in chunk:
                            pre_code, _, rest = chunk.partition("```python")
                            print(pre_code)
                            formatted_output += ""#format_message(pre_code)
                            chunk = rest

                            if "```" in chunk:
                                code_content, _, remainder = chunk.partition("```")
                                streamLoggerCode.emit(code_content.strip()) 

                                formatted_output += ""#python_functions.ignore_python_code(code_content)
                                # (
                                #     '<div style="position: relative; background-color: #1E1E1E; color: #D4D4D4; padding: 12px; border-radius: 8px; '
                                #     'border: 1px solid #3C3C3C; font-family: Consolas, \'Courier New\', monospace; font-size: 14px; overflow: auto;">'
                                #     '<div style="position: absolute; top: 8px; right: 8px; background-color: #022740; '
                                #     'color: #FFFFFF; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 12px;">'
                                #     f'<b>#Python Code With {len(code_content.splitlines())} Lines</b>'
                                #     '</div>'
                                #     '<pre style="margin: 0; padding: 0; white-space: pre-wrap; background-color: #1E1E1E; color: #D4D4D4;">' +
                                #     ''.join(
                                #         f'{line}\n'
                                #         for i, line in enumerate(code_content.splitlines())
                                #     ).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>") +
                                #     '</pre>'
                                #     '</div>'
                                # )
                                chunk = remainder
                            else:
                                code_buffer = chunk
                                break

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

                return total_text, 0, 0, 0















                            
        elif stream == False:
            if tools:
                if aditional_instructions and model_select:
                    run = client.beta.threads.runs.create(
                        thread_id=threead_id,
                        assistant_id=agent_id,
                        tools=tools,
                        additional_instructions=aditional_instructions,
                        model=model_select,
                    )
                else:
                    run = client.beta.threads.runs.create(
                        thread_id=threead_id,
                        assistant_id=agent_id,
                        tools=tools
                    )

            else:
                if aditional_instructions and model_select:
                    run = client.beta.threads.runs.create(
                        thread_id=threead_id,
                        assistant_id=agent_id,
                        additional_instructions=aditional_instructions,
                        model=model_select,
                    )
                else:
    
                    run = client.beta.threads.runs.create(
                        thread_id=threead_id,
                        assistant_id=agent_id
                    )


            contador = 0
            while True:
                time.sleep(2)
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=threead_id,
                    run_id=run.id
                )
                if run_status.status == 'requires_action':
                    for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                        if tool_call.type == 'function':
                            
                            function_name = tool_call.function.name
                            function_arguments = tool_call.function.arguments
                            print(function_name)
                            print(function_arguments)
                            print(tool_call)
                            print(tool_call.id)
                            
                            _init_output_(function_name,
                                    function_arguments,
                                    tool_call,
                                    threead_id,
                                    client,
                                    run)

                elif run_status.status == 'completed':
                    break
                elif run_status.status == 'failed':
                    pass
                elif run_status.status == 'in_progress':
                    print("thinking...")
                else:
                    contador += 1 
                    if contador == 15:
                        break
                    print("Aguardando a execução ser completada...")

            messages = client.beta.threads.messages.list(
                thread_id=threead_id
            )
            file_id = None
            contador23  = 0
            for message in messages:
                
                for mensagem_contexto in message.content:
                    print(message.content)
                    valor_texto = mensagem_contexto.text.value
                    
                    # try:
                        
                    #     try:
                    #         annotations = mensagem_contexto.text.annotations
                    #     except:
                    #         annotations = None
                    # except:
                    #     try:
                    #         valor_texto = message.content.index(1)
                    #     except:
                    #         valor_texto = None
                    #     try:
                    #         annotations = mensagem_contexto.image_file.file_id
                    #     except:
                    #         annotations = None



                    return valor_texto, run_status.usage.total_tokens, run_status.usage.prompt_tokens, run_status.usage.completion_tokens
                # contador23 += 1
                # if 
                #break


class Agent_files_update:

    def update_vectorstore_in_agent(client, assistant_id: str, vector_store_id: list):
        """
        Updates the vector store IDs for an assistant's file search tool.

        Parameters:
        ----------
        assistant_id (str): The ID of the assistant to update.
        vector_store_id (List[str]): A list of vector store IDs to set for the assistant.

        Returns:
        -------
        str: The updated assistant ID.

        Raises:
        -------
        Exception: If there is an error updating the assistant.

        Example:
        --------
        >>> assistant_id = '12345'
        >>> vector_store_id = ['store1', 'store2']
        >>> updated_assistant_id = update_vectorstore_in_agent(assistant_id, vector_store_id)
        >>> print(updated_assistant_id)
        '12345'

        Note:
        -----
        - This function assumes that the `client` object is properly configured with the necessary credentials to interact with the assistant management API.
        """
        try:
            assistant = client.beta.assistants.update(
                assistant_id=assistant_id,
                tools=[{"type": "file_search"}],
                tool_resources={"file_search": {"vector_store_ids": vector_store_id}},
            )
            return assistant.id
        except Exception as e:
            raise Exception(f"Error updating assistant: {e}")
    
class Agent_files:

    def auth_vectorstoreAdvanced(app1, client, name_for_vectorstore, file_paths):
        """
        Uploads multiple files to an existing Vector Store or creates a new one if it doesn't exist.

        Parameters:
        - name_for_vectorstore (str): The name of the vector store.
        - file_paths (list): A list of file paths to be uploaded.

        Returns:
        - str: The ID of the created or updated vector store.

        Raises:
        - Exception: If there is an error during the upload process.

        Example:
        ```python
        example of how to use the auth_vectorstoreAdvanced function...
        ```

        Note:
        - This function handles both existing and new vector stores based on the existence of the vector store with the given name.
        - It uses the `beta` API endpoint for uploading files and handling batch uploads.
        - If the vector store does not exist, it creates a new one and updates the database reference accordingly.
        """


        try:
            ref1 = db.reference(f'ai_org_vector_store/User_{name_for_vectorstore}', app=app1)
            data1 = ref1.get()
            vector_store_id = data1['vector_store_id']
            for update1newfiles in file_paths:
                update1newfile = open(update1newfiles, "rb")
                client.beta.vector_stores.files.upload(
                    vector_store_id=vector_store_id, file=update1newfile
                )
            return str(vector_store_id)
        except Exception as err:
            print(err)
            vector_store = client.beta.vector_stores.create(name=name_for_vectorstore)
            file_streams = [open(path, "rb") for path in file_paths]
            client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id, files=file_streams
            )
            ref1 = db.reference(f'ai_org_vector_store', app=app1)
            controle_das_funcao2 = f"User_{name_for_vectorstore}"
            controle_das_funcao_info_2 = {
                "name_for_vectorstore": f'{name_for_vectorstore}',
                "vector_store_id": f'{vector_store.id}'
            }
            ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)
            return vector_store.id

    def auth_or_upload_multiple_files(app1, client, name_for: str, list_files_path: list):
        """
        This function attempts to retrieve a list of file IDs from the database under the key 'auth_or_upload_multiple_files/User_{name_for}'.

        Parameters:
        -----------
        name_for : str
            The name associated with the user's data in the database.
        list_files_path : list
            A list of file paths that need to be uploaded.

        Returns:
        --------
        list
            A list of file IDs if the data retrieval is successful, otherwise, it uploads the files and returns the list of file IDs.

        Raises:
        -------
        Exception
            If there is an error during the retrieval or upload process.

        Example:
        --------
        ```python
        file_paths = ['file1.txt', 'file2.txt']
        file_ids = auth_or_upload_multiple_files('user123', file_paths)
        print(file_ids)  # Output: [file_id1, file_id2]
        ```

        Note:
        -----
        - This function uses the `db.reference` method to interact with the Firebase Realtime Database.
        - If the data for the specified user does not exist, it creates a new entry with the list of file IDs.
        - It handles exceptions that may occur during the database operations.
        """
        
        try:
            ref1 = db.reference(f'auth_or_upload_multiple_files/User_{name_for}', app=app1)
            data1 = ref1.get()
            list_return = data1['list']
            return list(list_return)
        except:
            lista_de_file_id = []
            for file in list_files_path:
                message_file = client.files.create(
                    file=open(file, "rb"), purpose="assistants"
                )
                lista_de_file_id.append(message_file.id)

            ref1 = db.reference(f'auth_or_upload_multiple_files', app=app1)
            controle_das_funcao2 = f"User_{name_for}"
            controle_das_funcao_info_2 = {
                "list": lista_de_file_id,
            }
            ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)
            return lista_de_file_id

    def auth_or_create_vector_store_with_multiple_files(app1, client, name_for_vectorstore: str, file_ids: list): 
        """
        This function creates or retrieves an existing vector store based on the provided name and a list of file IDs.

        Parameters:
        - name_for_vectorstore (str): The name of the vector store to be created or retrieved.
        - file_ids (list): A list of file IDs to be added to the vector store.

        Returns:
        - str: The ID of the vector store.

        Raises:
        - Exception: If there is an error during the creation or retrieval process.

        Example:
        >>> auth_or_create_vector_store_with_multiple_files("my_vectorstore", ["file1.txt", "file2.txt"])
        'vs_abc123'

        Note:
        - The function uses Firebase Firestore to manage vector stores and their associated file batches.
        - It checks if a vector store with the given name already exists. If it does, it retrieves its ID; otherwise, it creates a new one.
        - It adds the specified file IDs to the vector store using batch operations.
        """
        try:
            ref1 = db.reference(f'auth_or_create_vector_store_with_multiple_files/User_{name_for_vectorstore}', app=app1)
            data1 = ref1.get()
            vector_store_return = data1['vectorstore']
            return str(vector_store_return)
        except:
            vector_store = client.beta.vector_stores.create(name=name_for_vectorstore)
            client.beta.vector_stores.file_batches.create_and_poll(
                vector_store_id=vector_store.id,
                file_ids=file_ids
            )
            ref1 = db.reference(f'auth_or_create_vector_store_with_multiple_files', app=app1)
            controle_das_funcao2 = f"User_{name_for_vectorstore}"
            controle_das_funcao_info_2 = {
                "vectorstore": vector_store.id,
            }
            ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)

            return vector_store.id

    def auth_or_create_vectorstore(app1, client, name_for_vectorstore: str, file_paths=None, update1newfiles=None):
        """
        Authenticates with the database or creates a new vector store based on the provided name.

        Parameters:
        -----------
        name_for_vectorstore (str): The name of the vector store to authenticate or create.
        file_paths (list of str, optional): A list of file paths to upload to the vector store.
        update1newfiles (str, optional): The path to an updated file to upload to the vector store.

        Returns:
        --------
        str: The ID of the authenticated or created vector store.

        Raises:
        -------
        Exception: If there is an error during authentication or creation.

        Example:
        --------
        vector_store_id = auth_or_create_vectorstore("my_vector_store", file_paths=["path/to/file1.txt", "path/to/file2.txt"])
        print(vector_store_id)

        Note:
        -----
        - This function handles both authentication and creation of a vector store.
        - It uploads files to the vector store if specified.
        - It stores the vector store ID in the database after successful creation.
        """
        try:
            ref1 = db.reference(f'ai_org_vector_store/User_{name_for_vectorstore}', app=app1)
            data1 = ref1.get()
            vector_store_id = data1['vector_store_id']
            if update1newfiles:
                update1newfile = open(update1newfiles, "rb")
                client.beta.vector_stores.files.upload(
                    vector_store_id=vector_store_id, file=update1newfile
                )
            return str(vector_store_id)
        except Exception as err1:
            print(err1)
            vector_store = client.beta.vector_stores.create(name=name_for_vectorstore)
            if update1newfiles:
                update1newfile = open(update1newfiles, "rb")
                client.beta.vector_stores.files.upload(
                    vector_store_id=vector_store.id, file=update1newfile
                )
            elif file_paths:
                file_streams = [open(path, "rb") for path in file_paths]
                client.beta.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=vector_store.id, files=file_streams
                )
                
            ref1 = db.reference(f'ai_org_vector_store', app=app1)
            controle_das_funcao2 = f"User_{name_for_vectorstore}"
            controle_das_funcao_info_2 = {
                "name_for_vectorstore": f'{name_for_vectorstore}',
                "vector_store_id": f'{vector_store.id}'
            }
            ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)
            return vector_store.id
        
class Agent_destilation:
                                                
    def DestilationResponseAgent(input, output, instructionsassistant, nameassistant):                        
         
        date = datetime.now().strftime('%Y-%m-%d')
        output_path_jsonl = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../Destilation/{nameassistant}/Jsonl/DestilationAgent{date}.jsonl'))
        output_path_json = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../Destilation/{nameassistant}/Json/DestilationAgent{date}.json'))
        os.makedirs(output_path_json, exist_ok=True)
        os.makedirs(output_path_jsonl, exist_ok=True)
            
        datasetjson = {
            "input": input,
            "output": output
        }
        datasetjsonl = {
            "messages": [
                {"role": "system", "content": f"{instructionsassistant}"},
                {"role": "user", "content": f"{input}"},
                {"role": "assistant", "content": f"{output}"}
            ]
        }

        finaloutputjson = os.path.join(output_path_json, f"DestilationDateTime_{date.replace('-', '_').replace(':', '_')}.json")
        with open(finaloutputjson, 'a', encoding='utf-8') as json_file:
            json.dump(datasetjson, json_file, indent=4, ensure_ascii=False)
        
        finaloutputjsonl = os.path.join(output_path_jsonl, f"DestilationDateTime_{date.replace('-', '_').replace(':', '_')}.jsonl")
        with open(finaloutputjsonl, 'a', encoding='utf-8') as json_file:
            json_file.write(json.dumps(datasetjsonl, ensure_ascii=False) + "\n")
        
        return True




class python_functions:

    def ignore_python_code(text: str, replacement: str = "[CODE ON THE BOARD]") -> str:
        padrão = r"```python\n[\s\S]*?```"
        texto_limpo = re.sub(padrão, replacement, text, flags=re.DOTALL)
        texto_limpo = re.sub(r'\n{3,}', '\n\n', texto_limpo)
        return texto_limpo.strip()


    def create_env(variables, env):
        """
        Cria um arquivo .env com as variáveis fornecidas.
        Se o arquivo já existir, ele será sobrescrito.

        Args:
            variables (dict): Um dicionário com chave-valor representando as variáveis de ambiente.
        """
        with open(env, "w") as file:
            for key, value in variables.items():
                file.write(f"{key}={value}\n")
        return True

    def update_multiple_env_variables(updates, env):
        # Lê o conteúdo atual do .env
        with open(env, "r") as file:
            lines = file.readlines()
        
        # Abre o .env para escrita e modifica as linhas conforme necessário
        with open(env, "w") as file:
            for line in lines:
                # Extrai a chave de cada linha no .env
                key = line.split("=")[0]
                
                # Verifica se a chave precisa ser atualizada
                if key in updates:
                    file.write(f"{key}={updates[key]}\n")
                else:
                    file.write(line)
        return True

    def update_env_variable(key, value):
        """
        Update the environment variable `key` with the given `value`.

        Parameters:
        ----------
        key (str): The name of the environment variable to update.
        value (str): The new value for the environment variable.

        Returns:
        -------
        None
        """
        with open(".env", "r") as file:
            lines = file.readlines()
        
        # Modifies the line that contains the environment variable
        with open(".env", "w") as file:
            for line in lines:
                if line.startswith(key + "="):
                    file.write(f"{key}={value}\n")
                else:
                    file.write(line)

    def execute_python_code_created(filename):
        """
        Execute the Python code stored in the specified file.

        Parameters:
        ----------
        filename (str): The name of the Python file to execute.

        Returns:
        -------
        str: The standard output of the executed script.
        """
        try:
            result = subprocess.run(['python', filename], capture_output=True, text=True)
            return f"Saída padrão: {result.stdout}"
        except Exception as e:
            pass

    def save_data_frame_planilha(planilha_json, path_nome_da_planilha):
        """
        Save the data frame to a CSV file.

        Parameters:
        ----------
        planilha_json (dict): The dictionary representing the data frame.
        path_nome_da_planilha (str): The path where the CSV file will be saved.

        Returns:
        -------
        None
        """
        df = pd.DataFrame(planilha_json)
        df.to_csv(path_nome_da_planilha, index=False)

    def save_python_code(code_string, name_script):
        """
        Save the provided Python code string to a file.

        Parameters:
        ----------
        code_string (str): The Python code to save.
        name_script (str): The name of the file where the code will be saved.

        Returns:
        -------
        None
        """
        with open(name_script, 'w', encoding="utf-8") as file:
            file.write(code_string)

    def save_csv(dataframe, path_nome_do_cronograma):
        """
        Salva o DataFrame em um arquivo CSV no caminho especificado.

        :param dataframe: O DataFrame a ser salvo.
        :param path_nome_do_cronograma: O caminho e nome do arquivo CSV onde o DataFrame será salvo.
        """
        try:
            dataframe.to_csv(path_nome_do_cronograma, index=False, encoding='utf-8')
            print(f"Arquivo salvo com sucesso em: {path_nome_do_cronograma}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo CSV: {e}")


    def save_TXT(string, filexname, letra):
        """
        Save a string to a text file.

        Parameters:
        - string (str): The content to be saved.
        - filexname (str): The path to the output text file.
        - letra (str): The mode in which to open the file ('a' for append, 'w' for write).

        Returns:
        - None
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filexname), exist_ok=True)
        
        # Save the content to the file
        with open(filexname, letra, encoding="utf-8") as file:
            file.write(f'{string}')


    def save_json(string, filexname):
        """
        Save a JSON string to a JSON file.

        Parameters:
        - string (dict): The dictionary to be saved as JSON.
        - filexname (str): The path to the output JSON file.

        Returns:
        - None
        """
        with open(filexname, 'w', encoding='utf-8') as json_file:
            json.dump(string, json_file, ensure_ascii=False, indent=4)
        print("JSON salvo em 'documento_pre_projeto.json'")


    def delete_all_lines_in_txt(filepath):
        """
        Delete all lines from a text file.

        Parameters:
        - filepath (str): The path to the text file.

        Returns:
        - None
        """
        with open(filepath, 'w') as file:
            pass  


    def move_arquivos(a, b):
        """
        Move files from one directory to another.

        Parameters:
        - a (str): The source directory.
        - b (str): The destination directory.

        Returns:
        - None
        """
        pasta1 = os.listdir(a)
        for arquivo in pasta1:
            caminho_arquivo_origem = os.path.join(a, arquivo)
            caminho_arquivo_destino = os.path.join(b, arquivo)
            shutil.move(caminho_arquivo_origem, caminho_arquivo_destino)
            print(f'{arquivo} movido para {b}')


    def executar_agentes(mensagem, name_for_script, nome_agente):
        """
        Execute an agent script using Python.

        Parameters:
        - mensagem (str): The message to be passed to the agent.
        - name_for_script (str): The name of the agent script.
        - nome_agente (str): The name of the agent.

        Returns:
        - None
        """
        comando_terminal = ['start', 'python', f'{nome_agente}.py', mensagem, name_for_script]
        subprocess.Popen(comando_terminal, shell=True)


    def analyze_txt_0(file):
        """
        Read the last line of a text file.

        Parameters:
        - file (str): The path to the text file.

        Returns:
        - str: The last line of the text file.
        """
        with open(file, 'r') as file:
            linhas = file.readlines()
            ultima_linha = linhas[-1].strip()
            return ultima_linha


    def analyze_file(file_path):
        """
        Read the entire content of a file.

        Parameters:
        - file_path (str): The path to the file.

        Returns:
        - str: The content of the file.
        """
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return content
        except:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    return content
            except:
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        content = file.read()
                        return content
                except UnicodeDecodeError:
                    return None


    def analyze_txt(file_path):
        """
        Read the entire content of a text file.

        Parameters:
        - file_path (str): The path to the text file.

        Returns:
        - str: The content of the file.
        """
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return content
        except:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    return content
            except:
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        content = file.read()
                        return content
                except UnicodeDecodeError:
                    try:
                        file_path = file_path.replace(" ", "").replace("\n", "")
                        with open(file_path, 'r', ) as file:
                            content = file.read()
                            return content
                    except UnicodeDecodeError:
                        pass


    def analyze_csv(file_path):
        """
        Read the contents of a CSV file.

        Parameters:
        - file_path (str): The path to the CSV file.

        Returns:
        - list: A list of lists containing the rows of the CSV file.
        """
        import csv
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)


    def analyze_json(file_path):
        """
        Load a JSON file and print its contents.

        Parameters:
        - file_path (str): The path to the JSON file.

        Returns:
        - dict: The loaded JSON data.
        """
        import json
        with open(file_path, 'r') as file:
            data = json.load(file)
        print(f"Dados JSON: {data}")
        
class EventHandler(AssistantEventHandler):
  @override
  def on_text_created(self, text: Text) -> None:
    print(f"\nassistant > ", end="", flush=True)

  @override
  def on_text_delta(self, delta: TextDelta, snapshot: Text):
    print(delta.value, end="", flush=True)

  @override
  def on_tool_call_created(self, tool_call: ToolCall):
    print(f"\nassistant > {tool_call.type}\n", flush=True)

  @override
  def on_tool_call_delta(self, delta: ToolCallDelta, snapshot: ToolCall):
    if delta.type == "code_interpreter" and delta.code_interpreter:
      if delta.code_interpreter.input:
        print(delta.code_interpreter.input, end="", flush=True)
      if delta.code_interpreter.outputs:
        print(f"\n\noutput >", flush=True)
        for output in delta.code_interpreter.outputs:
          if output.type == "logs":
            print(f"\n{output.logs}", flush=True)
