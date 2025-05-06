######################################### SoftwareAI Core #########################################
# IMPORT SoftwareAI Functions
from softwareai_engine_library.Inicializer._init_functions_ import *
#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Libs 
# from Library.softwareai_engine_library.Inicializer._init_submit_outputs_ import _init_output_
#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################

# 
from firebase_admin import App
class ResponseAgent:

    def ResponseAgent_message_completions(prompt, 
                                        key_api, 
                                        lang: Optional[str] = "pt",
                                        model: Optional[str] = "gpt-4o-mini-2024-07-18", 
                                        Debug: Optional[bool] = True,
                                        json_format: Optional[bool] = True, 
                                        store: Optional[bool] = True, 
                                        AgentDestilation: Optional[bool] = False,
                                        AgentName: Optional[str] = None,
                                        AgentInstruction: Optional[str] = ""
                                        ):
        """
        Envia uma mensagem para o modelo de chat da OpenAI e retorna a resposta.

        Parâmetros:
        - instruction (str): O texto ao qual o assistente responderá.
        - sistema (str, opcional): Instrução de sistema para o assistente. Padrão é uma string vazia.
        - json_format (bool, opcional): Define se a resposta será JSON ou texto simples. Padrão é True.
        - store (bool, opcional): Define se a interação será armazenada.

        Retorno:
        - str: Resposta do assistente.

        Exceções:
        - Exception: Se houver erro durante a requisição à API.
        """
        def log_message(message_pt, message_en, color, bold=False):
            if Debug:
                attrs = ['bold'] if bold else []
                cprint(message_pt if lang == "pt" else message_en, color, attrs=attrs)

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {key_api}",
            "Content-Type": "application/json"
        }

        log_message("🔑 Configurando cabeçalhos da requisição...", 
                    "🔑 Setting up request headers...", 'blue')

        formato = "text"
        if json_format:
            formato = "json_object"
        
        log_message(f'📦 Formato de resposta definido como: {formato}', 
                    f'📦 Response format set as: {formato}', 'cyan')

        mensagem = []
        if AgentInstruction != "":
            log_message(f'⚙️ Adicionando instrução de sistema: {AgentInstruction}', 
                        f'⚙️ Adding system instruction: {AgentInstruction}', 'cyan')
            mensagem.append({"role": "system", "content": AgentInstruction})

        mensagem.append({"role": "user", "content": prompt})

        log_message(f'📝 Montando mensagem do usuário: {prompt}', 
                    f'📝 Building user message: {prompt}', 'cyan')

        data = {
            "model": model,
            "messages": mensagem,
            "store": store,
            "max_tokens": 16_384,
            "response_format": {"type": formato},
        }

        log_message("🚀 Enviando requisição para a API...", 
                    "🚀 Sending request to the API...", 'blue')

        try:
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                log_message("✅ Requisição bem-sucedida! Processando resposta...", 
                            "✅ Request successful! Processing response...", 'green')
                
                response_json = response.json()
                if json_format:
                    log_message("📄 Retornando resposta em formato JSON.", 
                                "📄 Returning response in JSON format.", 'cyan')
                    return json.loads(response_json['choices'][0]['message']['content'])
                
                if AgentDestilation == True: 

                    log_message("📄 Storing response with Agent Distillation", 
                                "📄 Returning response in text format.", 'cyan')
                    
                    Agent_destilation.DestilationResponseAgent(prompt, response_json['choices'][0]['message']['content'], AgentInstruction, AgentName)
                                    
                log_message("📄 Retornando resposta em formato texto.", 
                            "📄 Returning response in text format.", 'cyan')
                                        

                return response_json['choices'][0]['message']['content']
            else:
                log_message(f'❌ Erro na requisição: {response.status_code}, {response.text}', 
                            f'❌ Request error: {response.status_code}, {response.text}', 'red', bold=True)
                return None

        except Exception as e:
            log_message(f'🔥 Exceção durante a requisição: {str(e)}', 
                        f'🔥 Exception during request: {str(e)}', 'red', bold=True)
            return None
        
    def ResponseAgent_message_with_assistants(
                                            mensagem: str,
                                            agent_id: str,
                                            key: str,
                                            app1, 
                                            client,
                                            app_product: Optional[App] = None,
                                            user_id: Optional[str] = None,
                                            tools: Optional[List] = None,
                                            model_select: Optional[str] = None,
                                            aditional_instructions: Optional[str] = None,
                                            streamflag: bool = False,
                                            QstreamLogger: Optional[bool] = None,
                                            QstreamLoggerCode: Optional[bool] = None,
                                            Debug: Optional[bool] = True,
                                            DebugTokens: Optional[bool] = True,
                                            AgentDestilation: Optional[bool] = True,
                                            Moderation: Optional[bool] = False,
                                            lang: Optional[str] = "pt",
                                            OPENAI_API_KEY: Optional[str] = "",
                                            Upload_multiples_file_in_thread: Optional[List[str]] = None,
                                            Upload_1_file_in_message: Optional[str] = None,
                                            Upload_1_image_for_vision_in_thread: Optional[str] = None,
                                            Upload_list_for_code_interpreter_in_thread: Optional[list] = None,
                                            Upload_1_file_for_code_interpreter_in_message: Optional[str] = None,
                                            vectorstore_in_Thread: Optional[List] = None

                                                                        
                                        ):


        def log_message(message_pt, message_en, color, bold=False):
            if Debug:
                attrs = ['bold'] if bold else []
                cprint(message_pt if lang == "pt" else message_en, color, attrs=attrs)


        if Upload_1_image_for_vision_in_thread is not None and Upload_1_image_for_vision_in_thread != "":
            log_message("🖼️ Iniciando upload de imagem para visão computacional...", "🖼️ Starting image upload for computer vision...", "blue")
            for i in range(8):
                    
                code_interpreter_in_thread = None
                with open(Upload_1_image_for_vision_in_thread, "rb") as image_file:
                    file = client.files.create(file=image_file, purpose="vision")

                    log_message(f"📤 Imagem enviada com sucesso. ID do arquivo: {file.id}",
                                f"📤 Image uploaded successfully. File ID: {file.id}", "green")
                    if user_id is not None:
                        threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key, vectorstore_in_Thread, code_interpreter_in_thread, user_id)
                    else:
                        threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key, vectorstore_in_Thread, code_interpreter_in_thread)

                    log_message(f"🧵 Thread criada/autenticada. ID da thread: {threead_id}",
                                f"🧵 Thread created/authenticated. Thread ID: {threead_id}", "cyan")

                    try:
                        message = client.beta.threads.messages.create(
                            thread_id=threead_id,
                            role="user",
                            content=[
                                {"type": "text", "text": f"""{mensagem}"""},
                                {"type": "image_file", "image_file": {"file_id": file.id}}
                            ]
                        )

                        log_message("✅ Mensagem com imagem enviada com sucesso.",
                                    "✅ Message with image sent successfully.", "green")
                        break
                    except Exception as e:
                        try:
                            ref1 = db.reference(f'ai_org_thread_Id/User_{key}', app=app1)
                            ref1.delete()                                
                            client.beta.threads.delete(threead_id)
                        except Exception as e2:
                            print(e2)
                        continue

        elif Upload_1_file_in_message is not None :
            log_message("📄 Iniciando upload de arquivo para a mensagem...",
                        "📄 Starting file upload for the message...", "blue")
            for i in range(8):
                    
                code_interpreter_in_thread = None
                message_file = client.files.create(file=open(Upload_1_file_in_message, "rb"), purpose="assistants")

                log_message(f"📤 Arquivo enviado. ID do arquivo: {message_file.id}",
                            f"📤 File uploaded. File ID: {message_file.id}", "green")
                if user_id is not None:
                    threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key, vectorstore_in_Thread, code_interpreter_in_thread, user_id)
                else:
                    threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key, vectorstore_in_Thread, code_interpreter_in_thread)

                log_message(f"🧵 Thread criada/autenticada. ID da thread: {threead_id}",
                            f"🧵 Thread created/authenticated. Thread ID: {threead_id}", "cyan")


                try:
                    message = client.beta.threads.messages.create(
                        thread_id=threead_id,
                        role="user",
                        content=mensagem,
                        attachments=[{"file_id": message_file.id, "tools": [{"type": "file_search"}]}
                                     
                                     ]
                    )
                    
                    log_message("✅ Mensagem com arquivo enviada com sucesso.",
                                "✅ Message with file sent successfully.", "green")
                    break
                except Exception as e:
                    try:
                        ref1 = db.reference(f'ai_org_thread_Id/User_{key}', app=app1)
                        ref1.delete()                                
                        client.beta.threads.delete(threead_id)
                    except Exception as e2:
                        print(e2)
                    continue

        elif Upload_multiples_file_in_thread is not None :
            log_message("📂 Iniciando upload de múltiplos arquivos para a thread...",
                        "📂 Starting upload of multiple files to the thread...", "blue")
            for i in range(8):
                    
                code_interpreter_in_thread = None
                list_as_string = json.dumps(Upload_multiples_file_in_thread)
                namehash = hashlib.sha256(list_as_string.encode()).hexdigest()
                vector_store = client.beta.vector_stores.create(name=f"Upload_{namehash[:5]}")

                log_message(f"📦 Vector store criado: {vector_store.id}",
                            f"📦 Vector store created: {vector_store.id}", "cyan")

                file_streams = [open(path, "rb") for path in Upload_multiples_file_in_thread]
                file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=vector_store.id, files=file_streams
                )

                log_message(f"📤 Arquivos enviados: {file_batch.status}",
                            f"📤 Files uploaded: {file_batch.status}", "green")
                if user_id is not None:
                    threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key,  [vector_store.id], code_interpreter_in_thread, user_id)
                else:
                    threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key,  [vector_store.id], code_interpreter_in_thread)

                log_message(f"🧵 Thread criada/autenticada. ID da thread: {threead_id}",
                            f"🧵 Thread created/authenticated. Thread ID: {threead_id}", "cyan")


                try:
                    message = client.beta.threads.messages.create(thread_id=threead_id, role="user", content=mensagem)

                        
                    log_message("✅ Mensagem com múltiplos arquivos enviada com sucesso.",
                                "✅ Message with multiple files sent successfully.", "green")

                    break
                except Exception as e:
                    try:
                        ref1 = db.reference(f'ai_org_thread_Id/User_{key}', app=app1)
                        ref1.delete()                                
                        client.beta.threads.delete(threead_id)
                    except Exception as e2:
                        print(e2)
                    continue

        elif Upload_list_for_code_interpreter_in_thread is not None:
            log_message("📁 Iniciando upload de arquivos para o interpretador de código...",
                        "📁 Starting file upload for the code interpreter...", "blue")
            for i in range(8):
                        
                list_file_id = []
                for path in Upload_list_for_code_interpreter_in_thread:
                    file = client.files.create(file=open(path, "rb"), purpose='assistants')
                    list_file_id.append(file.id)

                    log_message(f"📤 Arquivo enviado. ID: {file.id}",
                                f"📤 File uploaded. ID: {file.id}", "green")

                code_interpreter_in_thread = list_file_id
                if user_id is not None:
                    threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key, vectorstore_in_Thread, code_interpreter_in_thread, user_id)
                else:
                    threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key, vectorstore_in_Thread, code_interpreter_in_thread)

                log_message(f"🧵 Thread criada/autenticada. ID da thread: {threead_id}",
                            f"🧵 Thread created/authenticated. Thread ID: {threead_id}", "cyan")

                try:
                    message = client.beta.threads.messages.create(thread_id=threead_id, role="user", content=mensagem)
                    log_message("✅ Mensagem com arquivos para o interpretador de código enviada com sucesso.",
                                "✅ Message with files for the code interpreter sent successfully.", "green")
                    break
                except Exception as e:
                    try:
                        ref1 = db.reference(f'ai_org_thread_Id/User_{key}', app=app1)
                        ref1.delete()                                
                        client.beta.threads.delete(threead_id)
                    except Exception as e2:
                        print(e2)
                    continue

        elif Upload_1_file_for_code_interpreter_in_message is not None:
            log_message("📄 Iniciando upload de arquivo para o interpretador de código na mensagem...",
                        "📄 Starting file upload for the code interpreter in the message...", "blue")
            for i in range(8):
                            
                code_interpreter_in_thread = None
                file = client.files.create(file=open(Upload_1_file_for_code_interpreter_in_message, "rb"), purpose='assistants')

                log_message(f"📤 Arquivo enviado. ID: {file.id}",
                            f"📤 File uploaded. ID: {file.id}", "green")
                if user_id is not None:
                    threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key, vectorstore_in_Thread, code_interpreter_in_thread, user_id)
                else:
                    threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key, vectorstore_in_Thread, code_interpreter_in_thread)

                log_message(f"🧵 Thread criada/autenticada. ID da thread: {threead_id}",
                            f"🧵 Thread created/authenticated. Thread ID: {threead_id}", "cyan")


                try:
                    message = client.beta.threads.messages.create(
                        thread_id=threead_id,
                        role="user",
                        content=mensagem,
                        attachments=[{"file_id": file.id, "tools": [{"type": "code_interpreter"}]}]
                    )
                    log_message("✅ Mensagem com arquivo para interpretador de código enviada com sucesso.",
                                "✅ Message with file for the code interpreter sent successfully.", "green")

                    break
                except Exception as e:
                    try:
                        ref1 = db.reference(f'ai_org_thread_Id/User_{key}', app=app1)
                        ref1.delete()                                
                        client.beta.threads.delete(threead_id)
                    except Exception as e2:
                        print(e2)
                    continue

        else:
            log_message("📝 Enviando mensagem sem anexos...",
                        "📝 Sending message without attachments...", "blue")
            for i in range(8):
                                
                code_interpreter_in_thread = None
                if user_id is not None:
                    threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key, vectorstore_in_Thread, code_interpreter_in_thread, user_id)
                else:
                    threead_id = AutenticateAgent.create_or_auth_thread(app1, client, key, vectorstore_in_Thread, code_interpreter_in_thread)

                log_message(f"🧵 Thread criada/autenticada. ID da thread: {threead_id}",
                            f"🧵 Thread created/authenticated. Thread ID: {threead_id}", "cyan")


                try:

                    message = client.beta.threads.messages.create(thread_id=threead_id, role="user", content=mensagem)
                    log_message("✅ Mensagem enviada com sucesso.",
                                "✅ Message sent successfully.", "green")
                    break
                except Exception as e:
                    try:
                        ref1 = db.reference(f'ai_org_thread_Id/User_{key}', app=app1)
                        ref1.delete()                                
                        client.beta.threads.delete(threead_id)
                    except Exception as e2:
                        print(e2)
                    continue


                        
        code_buffer = None 
        formatted_output = ""

        if streamflag == True:
            log_message('🚀 Iniciando execução em modo streaming...',
                        '🚀 Starting execution in streaming mode...', 'blue')

            accumulated_text = ""
            total_text = ""

            log_message('📡 Conectando ao stream...',
                        '📡 Connecting to the stream...', 'cyan')


            with client.beta.threads.runs.stream(
                thread_id=threead_id,
                assistant_id=agent_id,
                event_handler=EventHandler(OPENAI_API_KEY,
                                            Debug, 
                                            lang, 
                                            app_product,
                                            threead_id,
                                            client,
                                            app1,
                ),
                tools=tools,
                additional_instructions=aditional_instructions,
                model=model_select
            ) as stream:

                log_message('✅ Conectado ao stream. Recebendo dados...',
                            '✅ Connected to the stream. Receiving data...', 'green')

                for text in stream.text_deltas:

                    total_text += text
                    if QstreamLogger is not None:
                        accumulated_text += text
                        while len(accumulated_text) >= 100:
                            match = re.search(r"[ \n.,!?]+", accumulated_text[100:])
                            cut_index = 100 + match.start() if match else len(accumulated_text)
                            chunk = accumulated_text[:cut_index]
                            accumulated_text = accumulated_text[cut_index:]

                            log_message(f'✂️ Processando chunk: {chunk[:50]}...',
                                        f'✂️ Processing chunk: {chunk[:50]}...', 'yellow')

                            if code_buffer is not None:
                                code_buffer += chunk
                                if "```" in code_buffer:
                                    code_content, _, remainder = code_buffer.partition("```")
                                    QstreamLoggerCode.emit(code_content.strip())

                                    log_message(f'💻 Código detectado no buffer: {code_content[:50]}...',
                                                f'💻 Code detected in the buffer: {code_content[:50]}...', 'magenta')

                                    formatted_output += '<pre style="margin: 0; padding: 0; white-space: pre-wrap; background-color: #F7F7F7; color: #0e6303;"><b>[CÓDIGO NO QUADRO]</b>'
                                    code_buffer = None
                                    chunk = remainder
                                else:
                                    continue

                            while "```python" in chunk:
                                pre_code, _, rest = chunk.partition("```python")

                                log_message('🔎 Bloco de código Python detectado.',
                                            '🔎 Python code block detected.', 'magenta')

                                formatted_output += ""  # format_message(pre_code)
                                chunk = rest

                                if "```" in chunk:
                                    code_content, _, remainder = chunk.partition("```")
                                    QstreamLoggerCode.emit(code_content.strip())

                                    log_message(f'📄 Emitindo código Python: {code_content[:50]}...',
                                                f'📄 Emitting Python code: {code_content[:50]}...', 'magenta')

                                    formatted_output += ""  # python_functions.ignore_python_code(code_content)
                                    chunk = remainder
                                else:
                                    code_buffer = chunk
                                    break

                            formatted_output += python_functions.format_message(chunk)
                            QstreamLogger.emit(
                                f'<div style="display: flex; justify-content: flex-start;">'
                                f'<div style="color: black; padding: 8px; border-radius: 8px; margin: 5px; max-width: 70%;">'
                                f'{formatted_output}</div></div>'
                            )

                            log_message('📤 Chunk emitido para a interface.',
                                        '📤 Chunk sent to the interface.', 'green')

                            formatted_output = ""


                        if accumulated_text:
                            log_message('📄 Processando texto restante no buffer...',
                                        '📄 Processing remaining text in buffer...', 'cyan')

                            formatted_output += python_functions.format_message(accumulated_text)
                            QstreamLogger.emit(
                                f'<div style="display: flex; justify-content: flex-start;">'
                                f'<div style="color: black; padding: 8px; border-radius: 8px; margin: 5px; max-width: 70%;">'
                                f'{formatted_output}</div></div>'
                            )

                    else:
                        sys.stdout.write(text)
                        sys.stdout.flush()  # Garante que o texto seja exibido imediatamente

                        # log_message(f'{text}',
                        #             f'{text}', 'green')



                log_message(f'✅ Transmissão concluída. Total de texto processado: {len(total_text)} caracteres.',
                            f'✅ Transmission completed. Total text processed: {len(total_text)} characters.', 'green')

                return total_text, 0, 0, 0
       
        elif streamflag == False:
            log_message('🚀 Iniciando execução sem streaming...', '🚀 Starting execution without streaming...', 'blue')

            if tools:
                if aditional_instructions and model_select:
                    log_message('🛠️ Executando com ferramentas, instruções adicionais e modelo selecionado.',
                                '🛠️ Running with tools, additional instructions, and selected model.', 'blue')
                    run = client.beta.threads.runs.create(
                        thread_id=threead_id,
                        assistant_id=agent_id,
                        tools=tools,
                        additional_instructions=aditional_instructions,
                        model=model_select,
                    )
                else:
                    log_message('🛠️ Executando com ferramentas, sem instruções adicionais.',
                                '🛠️ Running with tools, without additional instructions.', 'blue')
                    run = client.beta.threads.runs.create(
                        thread_id=threead_id,
                        assistant_id=agent_id,
                        tools=tools
                    )
            else:
                if aditional_instructions and model_select:
                    log_message('📄 Executando sem ferramentas, com instruções adicionais e modelo selecionado.',
                                '📄 Running without tools, with additional instructions and selected model.', 'blue')
                    run = client.beta.threads.runs.create(
                        thread_id=threead_id,
                        assistant_id=agent_id,
                        additional_instructions=aditional_instructions,
                        model=model_select,
                    )
                else:
                    log_message('📄 Executando sem ferramentas e sem instruções adicionais.',
                                '📄 Running without tools and without additional instructions.', 'blue')
                    run = client.beta.threads.runs.create(
                        thread_id=threead_id,
                        assistant_id=agent_id
                    )

            contador = 0
            log_message('⏳ Monitorando status da execução...', '⏳ Monitoring execution status...', 'cyan')
            i = 0
            for irg in range(900):
                time.sleep(2)
                
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=threead_id,
                    run_id=run.id
                )
    
                if run_status.status == 'requires_action':
                    log_message('⚙️ Ação requerida. Processando chamadas de ferramentas...',
                                '⚙️ Action required. Processing tool calls...', 'yellow')
                    for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                        if tool_call.type == 'function':
                            function_name = tool_call.function.name
                            function_arguments = tool_call.function.arguments

                            log_message(f'🔧 Função chamada: {function_name}',
                                        f'🔧 Function called: {function_name}', 'yellow')
                            log_message(f'📥 Argumentos: {function_arguments}',
                                        f'📥 Arguments: {function_arguments}', 'yellow')
                            log_message(f'🆔 Tool Call ID: {tool_call.id}',
                                        f'🆔 Tool Call ID: {tool_call.id}', 'yellow')


                            # _init_output_(function_name,
                            #             function_arguments,
                            #             tool_call,
                            #             threead_id,
                            #             client,
                            #             run,
                            #             app1,
                            #             )
                            
                            import requests

                            url = "https://softwareai-library-hub.rshare.io/api/submit-tool-output"

                            data = {
                                "function_name": function_name,
                                "tool_call": tool_call,
                                "thread_id": threead_id,
                                "run": run,
                                "OPENAI_API_KEY": OPENAI_API_KEY
                                
                            }

                            response = requests.post(url, json=data)

                            if response.status_code == 200:
                                data = request.json()
                                message_rp = data.get('message')
                                print(message_rp)
                            else:
                                print("Erro:", response.json())




                elif run_status.status == 'completed':
                    log_message('✅ Execução concluída com sucesso.',
                                '✅ Execution completed successfully.', 'green')
                    break
                elif run_status.status == 'failed':
                    log_message('❌ Execução falhou.',
                                '❌ Execution failed.', 'red')
                    break
                elif run_status.status == 'in_progress':
                    pontos = '.' * i 
                    log_message(f'💭 Pensando{pontos}',
                                f'💭 Thinking{pontos}', 'cyan')
                    i = i + 1 if i < 3 else 1  # Reinicia o contador após 3

                else:
                    contador += 1
                    if contador == 15:
                        log_message('⚠️ Tempo limite atingido. Finalizando monitoramento.',
                                    '⚠️ Timeout reached. Stopping monitoring.', 'red')
                        break
                    log_message('⏳ Aguardando a execução ser completada...',
                                '⏳ Waiting for execution to complete...', 'cyan')

            log_message('📨 Recuperando mensagens do thread...',
                        '📨 Retrieving messages from the thread...', 'blue')

            messages = client.beta.threads.messages.list(thread_id=threead_id)

            file_id = None
            contador23 = 0

            for message in messages:
                for mensagem_contexto in message.content:
                    log_message(f'📩 Mensagem recebida: {mensagem_contexto.text.value}',
                                f'📩 Message received: {mensagem_contexto.text.value}', 'blue')

                    valor_texto = mensagem_contexto.text.value

                    if DebugTokens:
                        price = ResponseAgent.calculate_dollar_value(run_status.usage.prompt_tokens, run_status.usage.completion_tokens)
                        if lang == "en":
                            log_message(f'📜 Tokens consumed : {run_status.usage.total_tokens} 💸${price:.4f}',
                                        f'📜 Tokens consumed : {run_status.usage.total_tokens} 💸${price:.4f}', 'yellow', bold=True)
                        elif lang == "pt":
                            log_message(f'📜 Tokens Consumidos: {run_status.usage.total_tokens} 💸 ${price:.4f}',
                                        f'📜 Tokens Consumidos: {run_status.usage.total_tokens} 💸 ${price:.4f}', 'yellow', bold=True)

                    if AgentDestilation == True: 

                        log_message("📄 Storing response with Agent Distillation", 
                                    "📄 Returning response in text format.", 'cyan')
                        
                        ref1 = db.reference(f'ai_org_assistant_id/User_{key}', app=app1)
                        data1 = ref1.get()
                        instructionsassistant = data1['instructionsassistant']
                        nameassistant = data1['nameassistant']

                        Agent_destilation.DestilationResponseAgent(mensagem, valor_texto, instructionsassistant, nameassistant)
                                        
                    return valor_texto, run_status.usage.total_tokens, run_status.usage.prompt_tokens, run_status.usage.completion_tokens
                
    def calculate_dollar_value(tokens_entrada, tokens_saida, tokens_cache=0):
        """
        Calcula o custo total com base nos tokens de entrada, cache (opcional) e saída.
        
        :param tokens_entrada: Quantidade de tokens de entrada.
        :param tokens_saida: Quantidade de tokens de saída.
        :param tokens_cache: Quantidade de tokens de entrada em cache (padrão é 0).
        :return: Custo total em dólares.
        """
        # Custos por 1 milhão de tokens
        custo_por_milhao_entrada = 0.150
        custo_por_milhao_cache = 0.075
        custo_por_milhao_saida = 0.600
        
        # Cálculo dos custos individuais
        custo_entrada = (tokens_entrada / 1_000_000) * custo_por_milhao_entrada
        custo_cache = (tokens_cache / 1_000_000) * custo_por_milhao_cache
        custo_saida = (tokens_saida / 1_000_000) * custo_por_milhao_saida
        
        # Cálculo do custo total
        custo_total = custo_entrada + custo_cache + custo_saida
        
        return round(custo_total, 6)
    