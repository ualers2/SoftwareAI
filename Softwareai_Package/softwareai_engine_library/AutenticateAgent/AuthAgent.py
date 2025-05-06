#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################



class AutenticateAgent:
    """
    Manages authentication and initialization for agent settings.
    Includes methods to configure advanced vector store options and to create or authenticate AI assistants
    in the database and OpenAI.
    """

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
        tools: Optional[List] = [{"type": "file_search"},{"type": "code_interpreter"}],
        vectorstore: Optional[List] = None,
        codeinterpreter: Optional[List] = None,
        response_format: Optional[str] = "text",

        
        ):
        """ 
        :param key: this is the key that represents the agent in the database
            
        :param instructionsassistant: This argument is the instruction of the agent's behavior The maximum length is 256,000 characters.
        
        :param nameassistant: This argument is the name of the agent The maximum length is 256 characters.
        
        :param model_select: This argument is the AI model that the agent will use
            
        :param tools: This argument is the agent's tools  There can be a maximum of 128 tools per assistant. Tools can be of types code_interpreter, file_search, vectorstore, or function.
            
        :param vectorstore: This argument is the vector storage id desired when creating or authenticating the agent
        response_format: Optional[str] = "json_object",
        response_format: Optional[str] = "json_schema_TitleAndPreface",
        response_format: Optional[str] = "text",
        """

        
        try:
            ref1 = db.reference(f'ai_org_assistant_id/User_{key}', app=app1)
            data1 = ref1.get()
            assistant_iddb = data1['assistant_id']
            instructionsassistantdb = data1['instructionsassistant']
            nameassistantdb = data1['nameassistant']
            model_selectdb = data1['model_select']
            
            if instructionsassistant:
                client.beta.assistants.update(
                    assistant_id=str(assistant_iddb),
                    instructions=instructionsassistant
                    
                )
                ref1 = db.reference(f'ai_org_assistant_id', app=app1)
                controle_das_funcao2 = f"User_{key}"
                controle_das_funcao_info_2 = {
                    "assistant_id": f'{assistant_iddb}',
                    "instructionsassistant": f'{instructionsassistant}',
                    "nameassistant": f'{nameassistantdb}',
                    "model_select": f'{model_selectdb}',
                    "tools": f'{tools}',
                    "key": f'{key}',
                }
                ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)

            if response_format == "json_object":
                client.beta.assistants.update(
                    assistant_id=str(assistant_iddb),
                    response_format={ "type": "json_object" }
                    
                )
            elif response_format == "json_schema_TitleAndPreface":
                client.beta.assistants.update(
                    assistant_id=str(assistant_iddb),
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": "book_schema",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "title": {
                                        "type": "string",
                                        "description": "Título do Livro"
                                    },
                                    "preface": {
                                        "type": "string",
                                        "description": "Texto detalhado do prefácio, com no mínimo 500 palavras."
                                    }
                                },
                                "required": [
                                    "title",
                                    "preface"
                                ],
                                "additionalProperties": False  # Deve ser booleano
                            },
                            "strict": True  # Deve ser booleano
                        }
                    }
                )
            elif response_format == "text":

                client.beta.assistants.update(
                    assistant_id=str(assistant_iddb),
                    tools=tools
                    
                )


            if vectorstore:
                client.beta.assistants.update(
                    assistant_id=str(assistant_iddb),
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
                    assistant_id=str(assistant_iddb),
                    tool_resources={
                    "code_interpreter": {
                        "file_ids": code_interpreter_in_agent
                        }
                    }
                )
                

            return str(assistant_iddb), str(instructionsassistantdb), str(nameassistantdb), str(model_selectdb)
        except Exception as err234:
            if tools:
           
                assistant = client.beta.assistants.create(
                    name=nameassistant,
                    instructions=instructionsassistant,
                    model=model_select
                )


                if response_format == "json_object":
                    client.beta.assistants.update(
                        assistant_id=assistant.id,
                        response_format={ "type": "json_object" }
                        
                    )
                elif response_format == "json_schema_TitleAndPreface":
                    client.beta.assistants.update(
                        assistant_id=assistant.id,
                        response_format={
                            "type": "json_schema",
                            "json_schema": {
                                "name": "book_schema",
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "title": {
                                            "type": "string",
                                            "description": "Título do Livro"
                                        },
                                        "preface": {
                                            "type": "string",
                                            "description": "Texto detalhado do prefácio, com no mínimo 500 palavras."
                                        }
                                    },
                                    "required": [
                                        "title",
                                        "preface"
                                    ],
                                    "additionalProperties": False  # Deve ser booleano
                                },
                                "strict": True  # Deve ser booleano
                            }
                        }
                        
                    )
                elif response_format == "text":
                 
                    client.beta.assistants.update(
                        assistant_id=assistant.id,
                        tools=tools
                        
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
                    instructions=instructionsassistant,
                    model=model_select,
                )
                if response_format == "json_object":
                    client.beta.assistants.update(
                        assistant_id=assistant.id,
                        response_format={ "type": "json_object" }
                        
                    )
                elif response_format == "json_schema_TitleAndPreface":
                    client.beta.assistants.update(
                        assistant_id=assistant.id,
                        response_format={
                            "type": "json_schema",
                            "json_schema": {
                                "name": "book_schema",
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "title": {
                                            "type": "string",
                                            "description": "Título do Livro"
                                        },
                                        "preface": {
                                            "type": "string",
                                            "description": "Texto detalhado do prefácio, com no mínimo 500 palavras."
                                        }
                                    },
                                    "required": [
                                        "title",
                                        "preface"
                                    ],
                                    "additionalProperties": False  # Deve ser booleano
                                },
                                "strict": True  # Deve ser booleano
                            }
                        }
                        
                    )
                elif response_format == "text":
                    client.beta.assistants.update(
                        assistant_id=assistant.id,
                        tools=[{"type": "file_search"}, {"type": "code_interpreter"}],
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
                            code_interpreter_in_thread: Optional[List] = None,
                            user_id: Optional[str] = None
                            
                            ):

        if user_id is not None:
                
            try:
                ref1 = db.reference(f'ai_org_thread_Id/User_{user_id}', app=app1)
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
                controle_das_funcao2 = f"User_{user_id}"
                controle_das_funcao_info_2 = {
                    "thread_id": f'{thread.id}',
                    "user_id": f'{user_id}'
                }
                ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)

                return str(thread.id)
        
        else:
                
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

