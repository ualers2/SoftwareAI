# Detalhes dos Módulos

Este documento lista todos os módulos do pacote `softwareai_engine_library` e detalha classes e funções contidas em cada módulo.

## softwareai_engine_library.__init__

**Descrição do Módulo:** Módulo de inicialização do pacote `softwareai_engine_library`. Prepara o namespace principal do pacote e expõe diretamente os submódulos AgentDestilation, AgentFiles, AutenticateAgent, Chat, EngineProcess, Handler, Inicializer, PythonFunctions e ResponseAgent para facilitar importações.

## softwareai_engine_library.AgentDestilation.Agent_destilation

**Descrição do Módulo:** Módulo de destilação de respostas de agentes. Contém a classe `Agent_destilation` com o método `DestilationResponseAgent`, que registra entradas (input), saídas (output) e instruções do assistente em arquivos JSON e JSONL organizados por data e nome do assistente, facilitando o rastreamento do histórico de conversas.

### Classes
- **Agent_destilation**: Nenhuma docstring de classe.
  - DestilationResponseAgent: Destilação de agentes, com essa funcao voce pode armazenar todos os input, output e instructionsassistant

## softwareai_engine_library.AgentDestilation.__init__

**Descrição do Módulo:** Módulo de inicialização do subpacote `AgentDestilation`. Prepara o namespace para a classe `Agent_destilation` e seu método de destilação de respostas.

## softwareai_engine_library.AgentFiles.AgentFiles

**Descrição do Módulo:** Módulo para gerenciamento de arquivos em stores vetoriais de agentes. Contém a classe `Agent_files`, que oferece métodos para autenticar e criar vector stores, fazer upload de múltiplos arquivos, recuperar listas de arquivos já armazenados e atualizar vector stores existentes por meio de operações sincronizadas com o Firebase e a API de vector stores do cliente OpenAI.

### Classes
- **Agent_files**: Nenhuma docstring de classe.
  - auth_vectorstoreAdvanced: Uploads multiple files to an existing Vector Store or creates a new one if it doesn't exist.

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
  - auth_or_upload_multiple_files: This function attempts to retrieve a list of file IDs from the database under the key 'auth_or_upload_multiple_files/User_{name_for}'.

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
  - auth_or_create_vector_store_with_multiple_files: This function creates or retrieves an existing vector store based on the provided name and a list of file IDs.

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
  - auth_or_create_vectorstore: Authenticates with the database or creates a new vector store based on the provided name.

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

## softwareai_engine_library.AgentFiles.AgentFilesUpdate

**Descrição do Módulo:** Nenhum docstring de módulo.

### Classes
- **Agent_files_update**: Nenhuma docstring de classe.
  - update_vectorstore_in_agent: Updates the vector store IDs for an assistant's file search tool.

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
  - del_all_and_upload_files_in_vectorstore: Nenhuma docstring de método.

## softwareai_engine_library.AgentFiles.__init__

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.AutenticateAgent.AuthAgent

**Descrição do Módulo:** Nenhum docstring de módulo.

### Classes
- **AutenticateAgent**: Nenhuma docstring de classe.
  - create_or_auth_vectorstoreadvanced: This function checks if a user's vectorstore advanced settings exist in the database.

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
  - create_or_auth_AI: :param key: this is the key that represents the agent in the database
    
:param instructionsassistant: This argument is the instruction of the agent's behavior The maximum length is 256,000 characters.

:param nameassistant: This argument is the name of the agent The maximum length is 256 characters.

:param model_select: This argument is the AI model that the agent will use
    
:param tools: This argument is the agent's tools  There can be a maximum of 128 tools per assistant. Tools can be of types code_interpreter, file_search, vectorstore, or function.
    
:param vectorstore: This argument is the vector storage id desired when creating or authenticating the agent
response_format: Optional[str] = "json_object",
response_format: Optional[str] = "json_schema_TitleAndPreface",
response_format: Optional[str] = "text",
  - create_or_auth_thread: Nenhuma docstring de método.

## softwareai_engine_library.AutenticateAgent.__init__

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.Chat._init_chat_

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.Chat.auth.autenticar_usuario

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **autenticar_usuario**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.auth.dynamic_rate_limit

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **dynamic_rate_limit**: Define o limite de requisições com base no e-mail do usuário.
Substitui "." por "_" para usar como identificador único.

## softwareai_engine_library.Chat.history.fix_all_conversations

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **fix_all_conversations**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.history.get_conversation_history

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **get_conversation_history**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.history.save_assistant_message

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **save_assistant_message**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.history.save_conversation_history

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **save_conversation_history**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.history.save_history_system

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **save_history_system**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.history.save_history_user

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **save_history_user**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.session.create_or_auth_AI

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **create_or_auth_AI**: :param key: this is the key that represents the agent in the database
    
:param instructionsassistant: This argument is the instruction of the agent's behavior The maximum length is 256,000 characters.

:param nameassistant: This argument is the name of the agent The maximum length is 256 characters.

:param model_select: This argument is the AI model that the agent will use
    
:param tools: This argument is the agent's tools  There can be a maximum of 128 tools per assistant. Tools can be of types code_interpreter, file_search, vectorstore, or function.
    
:param vectorstore: This argument is the vector storage id desired when creating or authenticating the agent
response_format: Optional[str] = "json_object",
response_format: Optional[str] = "json_schema_TitleAndPreface",
response_format: Optional[str] = "text",

## softwareai_engine_library.Chat.session.create_or_auth_thread

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **create_or_auth_thread**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.session.get_agent_for_session

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **get_agent_for_session**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.session.login_required

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **login_required**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.session.save_agent_for_session

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **save_agent_for_session**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.session.store_github

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **store_github_session_in_firebase**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.stream.process_stream

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.Chat.stream.process_stream_and_save_history

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.Chat.stream.send_to_webhook

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **send_to_webhook**: Envia uma mensagem para o webhook.

## softwareai_engine_library.Chat.tokens._o3_mini

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.Chat.tokens.calculate_dollar_value

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **calculate_dollar_value**: Calcula o custo total com base nos tokens de entrada, cache (opcional) e saída.

:param tokens_entrada: Quantidade de tokens de entrada.
:param tokens_saida: Quantidade de tokens de saída.
:param tokens_cache: Quantidade de tokens de entrada em cache (padrão é 0).
:return: Custo total em dólares.

## softwareai_engine_library.Chat.utils.build_image_messages

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **build_image_messages**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.utils.encode_image_to_base64

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **encode_image_to_base64**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.utils.find_invalid_conversations

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **find_invalid_conversations**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.utils.format_instruction

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **format_instruction**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.utils.generate_api_key

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **generate_api_key**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.utils.get_api_key

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **get_api_key**: Nenhuma docstring de função.

## softwareai_engine_library.Chat.utils.get_user_data_from_firebase

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **get_user_data_from_firebase**: Função que obtém os dados do usuário no Firebase Realtime Database
a partir da chave da API, na referência 'Users_Control_Panel'.

## softwareai_engine_library.Chat.utils.key_func

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **key_func**: Nenhuma docstring de função.

## softwareai_engine_library.EngineProcess.EValidWebhook

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **valid**: Nenhuma docstring de função.

## softwareai_engine_library.EngineProcess.EgetMetadataAgent

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **EgetMetadataAgent**: Nenhuma docstring de função.

## softwareai_engine_library.EngineProcess.EgetTools

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **download_tools_zip**: Faz o download do ZIP contendo os arquivos .py de múltiplas ferramentas.
Após o download, extrai para a pasta 'Functions'.

:param tool_ids: Lista com os IDs das ferramentas.
:param output_path: Caminho de saída do arquivo ZIP.
:param base_url: URL base da API.
:return: True se tudo foi bem-sucedido, False caso contrário.
- **import_tool**: Importa dinamicamente o módulo da ferramenta e retorna o objeto decorado com @function_tool.
- **Egetoolsv2**: Nenhuma docstring de função.

## softwareai_engine_library.EngineProcess.__init__

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.Handler.EventHandler

**Descrição do Módulo:** Nenhum docstring de módulo.

### Classes
- **EventHandler**: Nenhuma docstring de classe.
  - __init__: Nenhuma docstring de método.
  - list_runs: Nenhuma docstring de método.
  - on_text_created: Nenhuma docstring de método.
  - on_text_delta: Nenhuma docstring de método.
  - on_tool_call_created: Nenhuma docstring de método.
  - log_message: Nenhuma docstring de método.
  - on_tool_call_delta: Nenhuma docstring de método.

## softwareai_engine_library.Handler.FirebaseKeysinit

**Descrição do Módulo:** Nenhum docstring de módulo.

### Classes
- **FirebaseKeysinit**: Nenhuma docstring de classe.
  - _init_app_: Nenhuma docstring de método.

## softwareai_engine_library.Handler.OpenAIKeysinit

**Descrição do Módulo:** Nenhum docstring de módulo.

### Classes
- **OpenAIKeysinit**: Nenhuma docstring de classe.
  - _init_client_: Nenhuma docstring de método.

## softwareai_engine_library.Handler.TitleAndPreface

**Descrição do Módulo:** Nenhum docstring de módulo.

### Classes
- **TitleAndPreface**: Nenhuma docstring de classe.

## softwareai_engine_library.Handler.__init__

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.Inicializer.__init__

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.Inicializer._init_core_

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.Inicializer._init_functions_

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.Inicializer._init_keys_fb

**Descrição do Módulo:** Nenhum docstring de módulo.

### Funções
- **init_fb**: Nenhuma docstring de função.

## softwareai_engine_library.Inicializer._init_libs_

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.Inicializer._init_submit_outputs_

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.PythonFunctions.__init__

**Descrição do Módulo:** Nenhum docstring de módulo.

## softwareai_engine_library.PythonFunctions.python_functions

**Descrição do Módulo:** Nenhum docstring de módulo.

### Classes
- **python_functions**: Nenhuma docstring de classe.
  - ignore_python_code: Nenhuma docstring de método.
  - format_message: Nenhuma docstring de método.
  - ignore_python_code: Nenhuma docstring de método.
  - create_env: Cria um arquivo .env com as variáveis fornecidas.
Se o arquivo já existir, ele será sobrescrito.

Args:
    variables (dict): Um dicionário com chave-valor representando as variáveis de ambiente.
  - update_multiple_env_variables: Nenhuma docstring de método.
  - update_env_variable: Update the environment variable `key` with the given `value`.

Parameters:
----------
key (str): The name of the environment variable to update.
value (str): The new value for the environment variable.

Returns:
-------
None
  - execute_python_code_created: Execute the Python code stored in the specified file.

Parameters:
----------
filename (str): The name of the Python file to execute.

Returns:
-------
str: The standard output of the executed script.
  - save_data_frame_planilha: Save the data frame to a CSV file.

Parameters:
----------
planilha_json (dict): The dictionary representing the data frame.
path_nome_da_planilha (str): The path where the CSV file will be saved.

Returns:
-------
None
  - save_python_code: Save the provided Python code string to a file.

Parameters:
----------
code_string (str): The Python code to save.
name_script (str): The name of the file where the code will be saved.

Returns:
-------
None
  - save_csv: Salva o DataFrame em um arquivo CSV no caminho especificado.

:param dataframe: O DataFrame a ser salvo.
:param path_nome_do_cronograma: O caminho e nome do arquivo CSV onde o DataFrame será salvo.
  - save_TXT: Save a string to a text file.

Parameters:
- string (str): The content to be saved.
- filexname (str): The path to the output text file.
- letra (str): The mode in which to open the file ('a' for append, 'w' for write).

Returns:
- None
  - save_json: Save a JSON string to a JSON file.

Parameters:
- string (dict): The dictionary to be saved as JSON.
- filexname (str): The path to the output JSON file.

Returns:
- None
  - delete_all_lines_in_txt: Delete all lines from a text file.

Parameters:
- filepath (str): The path to the text file.

Returns:
- None
  - move_arquivos: Move files from one directory to another.

Parameters:
- a (str): The source directory.
- b (str): The destination directory.

Returns:
- None
  - executar_agentes: Execute an agent script using Python.

Parameters:
- mensagem (str): The message to be passed to the agent.
- name_for_script (str): The name of the agent script.
- nome_agente (str): The name of the agent.

Returns:
- None
  - analyze_txt_0: Read the last line of a text file.

Parameters:
- file (str): The path to the text file.

Returns:
- str: The last line of the text file.
  - analyze_file: Read the entire content of a file.

Parameters:
- file_path (str): The path to the file.

Returns:
- str: The content of the file.
  - analyze_txt: Read the entire content of a text file.

Parameters:
- file_path (str): The path to the text file.

Returns:
- str: The content of the file.
  - analyze_csv: Read the contents of a CSV file.

Parameters:
- file_path (str): The path to the CSV file.

Returns:
- list: A list of lists containing the rows of the CSV file.
  - analyze_json: Load a JSON file and print its contents.

Parameters:
- file_path (str): The path to the JSON file.

Returns:
- dict: The loaded JSON data.

## softwareai_engine_library.ResponseAgent.ResponseAgent

**Descrição do Módulo:** Nenhum docstring de módulo.

### Classes
- **ResponseAgent**: Nenhuma docstring de classe.
  - ResponseAgent_message_completions: Envia uma mensagem para o modelo de chat da OpenAI e retorna a resposta.

Parâmetros:
- instruction (str): O texto ao qual o assistente responderá.
- sistema (str, opcional): Instrução de sistema para o assistente. Padrão é uma string vazia.
- json_format (bool, opcional): Define se a resposta será JSON ou texto simples. Padrão é True.
- store (bool, opcional): Define se a interação será armazenada.

Retorno:
- str: Resposta do assistente.

Exceções:
- Exception: Se houver erro durante a requisição à API.
  - ResponseAgent_message_with_assistants: Nenhuma docstring de método.
  - calculate_dollar_value: Calcula o custo total com base nos tokens de entrada, cache (opcional) e saída.

:param tokens_entrada: Quantidade de tokens de entrada.
:param tokens_saida: Quantidade de tokens de saída.
:param tokens_cache: Quantidade de tokens de entrada em cache (padrão é 0).
:return: Custo total em dólares.

## softwareai_engine_library.ResponseAgent.__init__

**Descrição do Módulo:** Nenhum docstring de módulo.

