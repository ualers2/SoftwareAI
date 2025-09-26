# import time

# while True:
#    time.sleep(67789)
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
import os
from flask import Flask, request, send_file, make_response
import requests
import json
import yaml
import matplotlib.pyplot as plt
from agents import Agent, ModelSettings, function_tool, Runner, handoff
from flask import Flask, request, Response, stream_with_context
from openai.types.responses import ResponseTextDeltaEvent
from firebase_admin import credentials, db
from typing_extensions import TypedDict, Any, Union
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
import zipfile
import asyncio
from typing_extensions import TypedDict, Any
from agents import Agent, ItemHelpers, ModelSettings, function_tool, FileSearchTool, WebSearchTool, Runner
from dotenv import load_dotenv, find_dotenv
import importlib
import time
import uuid
import base64
import asyncio
import secrets
import threading
import tempfile
import smtplib
import unicodedata
import subprocess
import re
import matplotlib.pyplot as plt
import logging
import sys
from datetime import datetime, timedelta
from typing import Optional, List, Union
from typing_extensions import TypedDict, Any
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps
from urllib.parse import urlencode
import urllib
import urllib.parse
from werkzeug.utils import secure_filename

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response, stream_with_context
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from waitress import serve
from user_agents import parse

from firebase_admin import auth, credentials, db, initialize_app

from dotenv import load_dotenv, find_dotenv
import stripe
from openai import OpenAI
from openai.types.responses import ResponseCompletedEvent, ResponseTextDeltaEvent

from agents import Agent, ModelSettings, function_tool, FileSearchTool, WebSearchTool, Runner

from modules.Egetoolsv2 import *
from modules.EgetMetadataAgent import *



# Taxas por milhão de tokens
COST_INSTRUCTION_PER_MILLION = 1.10    # US$ por 1 000 000 de tokens de instrução
COST_OUTPUT_PER_MILLION      = 4.40    # US$ por 1 000 000 de tokens de output

# Convertendo para custo unitário
cost_instruction_token = COST_INSTRUCTION_PER_MILLION / 1_000_000
cost_output_token      = COST_OUTPUT_PER_MILLION      / 1_000_000



                  
def send_to_webhook(WEBHOOK_URL, user, type, message):
    """Envia uma mensagem para o webhook."""
    try:
        # Envia o conteúdo da mensagem como JSON; ajuste se necessário
        requests.post(WEBHOOK_URL, json={str(user): {"type": type, "message": message}})
    except Exception as e:
        # Evita erro recursivo chamando a função original de print
        print(f"Erro ao enviar mensagem para webhook:{e}")

def save_history_user(
    session_id,
    user_email,
    message_to_send,
    appcompany
        
    ):
    # Criar a nova mensagem do usuário com timestamp
    user_message_obj = {
        "role": "user",
        "content": message_to_send,
        "timestamp": int(time.time() * 1000)
    }

    save_assistant_message(
        session_id=session_id,
        message_obj=user_message_obj,
        user_email=user_email, 
        appcompany=appcompany
    )
    
def save_history_system(
    session_id,
    user_email,
    message_to_send,
    appcompany
        
    ):
    # conversation_history = get_conversation_history(session_id, user_email=user_email, appcompany=appcompany)
    assistant_message_obj = {
        "role": "system",
        "content": message_to_send,
        "timestamp": int(time.time() * 1000)
    }
    save_assistant_message(
        session_id=session_id,
        message_obj=assistant_message_obj,
        user_email=user_email, 
        appcompany=appcompany
    )

async def process_stream(type_stream,
                        agent, 
                        attach_message, 
                        WEBHOOK_URL,
                        session_id,
                        user_email,
                        appcompany
                        ):
    # global input_tokens
    # global cached_tokens
    # global reasoning_tokens
    # global completion_tokens
    # global total_tokens


    input_tokens = 0
    cached_tokens = 0
    reasoning_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    cost_instr = 0.0
    cost_out = 0.0

    save_history_user(
        session_id,
        user_email,
        attach_message,
        appcompany
            
        )

    result = Runner.run_streamed(
        agent,
        attach_message,
        max_turns=500
    )
    print("=== Run starting ===")

    try:
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                if type_stream == "real_stream":
                    send_to_webhook(
                        WEBHOOK_URL=WEBHOOK_URL,
                        user="Chat Agent",
                        type="real_stream",
                        message=event.data.delta
                    )
                else:
                    continue
            # When the agent updates, print that
            elif event.type == "agent_updated_stream_event":
                message_to_send = f"Agent: {event.new_agent.name}"
                if type_stream == "info":
                    send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
                elif type_stream == "agentworkflow":  
                    send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="agentworkflow", message=message_to_send)
                elif type_stream == "real_stream":
                    pass

                if type_stream == "real_stream":     
                    pass
                else:       
                    save_history_system(
                        session_id,
                        user_email,
                        message_to_send,
                        appcompany
                            
                    )
    
            # When items are generated, print them
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    message_to_send = f"{event.item.agent.name} -- Tool was called"
                    if type_stream == "info":
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
                    elif type_stream == "agentworkflow":  
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="agentworkflow", message=message_to_send)
                    elif type_stream == "real_stream":
                        pass


                    if type_stream == "real_stream":     
                        pass
                    else:       
                        save_history_system(
                            session_id,
                            user_email,
                            message_to_send,
                            appcompany
                                
                            )

                elif event.item.type == "tool_call_output_item":
                    message_to_send = f"{event.item.agent.name} -- Tool output: {event.item.raw_item}"
                    if type_stream == "info":
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
                    elif type_stream == "agentworkflow":  
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="agentworkflow", message=message_to_send)
                    elif type_stream == "real_stream":
                        pass


                    if type_stream == "real_stream":     
                        pass
                    else:       
                        save_history_system(
                            session_id,
                            user_email,
                            message_to_send,
                            appcompany
                                
                            )
                        output_data = event.item.raw_item.get("output", "")
                        
                        try:
                            # Substitui aspas simples por aspas duplas para garantir um formato JSON válido
                            if isinstance(output_data, str):
                                output_data = output_data.replace("'", "\"")
                                parsed_output = json.loads(output_data)  # Usando json.loads() em vez de eval
                            else:
                                parsed_output = output_data

                            print(f"parsed_output: {parsed_output}")
                            print(f"output_data: {output_data}")

                            file_path = parsed_output.get("file_path")
                            # send_to_webhook(WEBHOOK_URL, "Chat Agent", "info", f"file_path: {file_path}")
                            # send_to_webhook(WEBHOOK_URL, "Chat Agent", "info", f"parsed_output: {parsed_output}")
                            # send_to_webhook(WEBHOOK_URL, "Chat Agent", "info", f"output_data: {output_data}")

                            if file_path:
                                with open(file_path, "rb") as f:
                                    file_bytes = f.read()
                                    file_base64 = base64.b64encode(file_bytes).decode("utf-8")

                                # Envia o conteúdo do arquivo direto pro webhook
                                send_to_webhook(
                                    WEBHOOK_URL,
                                    user="Chat Agent",
                                    type="file",
                                    message={
                                        "file_name": file_path,
                                        "file_base64": file_base64
                                    }
                                )
                            else:
                                pass

                        except Exception as e:
                            print(f" Erro ao processar o output: {str(e)}")
                        
                        
                elif event.item.type == "reasoning_item":
                    message_to_send = f"{event.item.agent.name} -- Reasoning"
                    if type_stream == "info":
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
                    elif type_stream == "agentworkflow":  
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="agentworkflow", message=message_to_send)
                    elif type_stream == "real_stream":
                        pass

                    if type_stream == "real_stream":     
                        pass
                    else:      
                        save_history_system(
                            session_id,
                            user_email,
                            message_to_send,
                            appcompany
                                
                            )
                elif event.item.type == 'handoff_call_item':
                    message_to_send = f"{event.item.agent.name} -- handoff was called"
                    if type_stream == "info":
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
                    elif type_stream == "agentworkflow":  
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="agentworkflow", message=message_to_send)
                    elif type_stream == "real_stream":
                        pass

                    if type_stream == "real_stream":     
                        pass
                    else:      
                        save_history_system(
                            session_id,
                            user_email,
                            message_to_send,
                            appcompany
                            )
                    
                elif event.item.type == "message_output_item":
                    message_to_send = f"{event.item.agent.name} -- {ItemHelpers.text_message_output(event.item)}"
                    
                    if type_stream == "real_stream":
                        pass
                    elif type_stream == "agentworkflow":  
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="agentworkflow", message=message_to_send)
                    elif type_stream == "info":
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info",  message=message_to_send)

                    if type_stream == "real_stream":     
                        pass
                    else:     
                        save_history_system(
                            session_id,
                            user_email,
                            message_to_send,
                            appcompany
                                
                            )
                    

                else:
                    pass  # Ignore other event types

            # Capturar o evento final já embrulhado em RawResponsesStreamEvent:
            elif event.type == "raw_response_event" and isinstance(event.data, ResponseCompletedEvent):
                usage = event.data.response.usage
                input_tokens      += usage.input_tokens
                cached_tokens     += usage.input_tokens_details.cached_tokens
                reasoning_tokens  += usage.output_tokens_details.reasoning_tokens
                completion_tokens += usage.output_tokens
                total_tokens      += usage.total_tokens
                cost_instr += round(input_tokens * cost_instruction_token , 6)
                cost_out += round(total_tokens * cost_output_token, 6) 
                cost_total = round(cost_instr + cost_out, 6)
                
                # print(f"input_tokens: {input_tokens}")
                # print(f"cached_tokens: {cached_tokens}")
                # print(f"reasoning_tokens: {reasoning_tokens}")
                # print(f"completion_tokens: {completion_tokens}")
                # print(f"total_tokens: {total_tokens}")

                # send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="usage_summary", message={
                #     "input_tokens": usage.input_tokens,
                #     "cached_tokens": usage.input_tokens_details.cached_tokens,
                #     "reasoning_tokens": usage.output_tokens_details.reasoning_tokens,
                #     "completion_tokens": usage.output_tokens,
                #     "total_tokens": usage.total_tokens
                # })


    except Exception as e:
        # trate erros aqui, se necessário
        pass
    else:

        if type_stream == "real_stream":     
            pass
        else:   
            # 4) ao sair do loop SEM erro, envia o resumo agregado
            send_to_webhook(
                WEBHOOK_URL=WEBHOOK_URL,
                user="Chat Agent",
                type="usage_summary",
                message={
                    "cost_total": cost_total,
                    "cost_out":      cost_out,
                    "cost_instr":      cost_instr,
                    "input_tokens":      input_tokens,
                    "cached_tokens":     cached_tokens,
                    "reasoning_tokens":  reasoning_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens":      total_tokens,
                }
            )

            send_to_webhook(
                WEBHOOK_URL=WEBHOOK_URL,
                user="Chat Agent",
                type="stream_end",
                message={
                    "cost_total": cost_total,
                }
            )
    print("=== Run complete ===")

async def process_stream_and_save_history(
                            type_stream,
                            agent_,
                            message,
                            WEBHOOK_URL,
                            session_id,
                            user_email,
                            number,
                            appcompany
                            
                            
                            ):
    await process_stream(type_stream, 
                        agent_, 
                        message, 
                        WEBHOOK_URL,
                        session_id,
                        user_email,
                        appcompany
                                        
                    )
    print(f"🤖Sistema {number}")

    

def format_instruction(instruction: str, context: dict) -> str:
    pattern = re.compile(r'\{(\w+)\}')
    def repl(match):
        var_name = match.group(1)
        if var_name in context:
            return str(context[var_name])
        else:
            raise KeyError(f"Variável '{var_name}' não encontrada no contexto.")
    return pattern.sub(repl, instruction)


def get_agent_for_session(session_id, appcompany):
    # Recupera os dados do agente a partir do Firebase
    ref = db.reference(f'agents/{session_id}', app=appcompany)
    agent_data = ref.get()

    if agent_data:
        # Cria uma instância do agente a partir dos dados recuperados
        agent = Agent(
            name=agent_data.get("name"),
            instructions=agent_data.get("instructions"),
            model=agent_data.get("model")
        )
        return agent
    else:
        return None

def save_agent_for_session(session_id, agent, appcompany):
    # Converte o agente em um formato serializável (por exemplo, um dicionário)
    agent_data = {
        "name": agent.name,
        "instructions": agent.instructions,
        "model": agent.model,
    }
    
    # Salva o agente no Firebase Realtime Database
    ref = db.reference(f'agents/{session_id}', app=appcompany)
    ref.set(agent_data)

def find_invalid_conversations(appcompany):
    ref = db.reference('conversations', app=appcompany)
    all_data = ref.get()
    
    for session_id, messages in all_data.items():
        if not isinstance(messages, list):
            print(f"⚠️ Sessão {session_id} não contém uma lista.")
            continue
        for m in messages:
            if not isinstance(m, dict):
                print(f"❌ Sessão {session_id} contém item inválido: {m}")

def encode_image_to_base64(file_storage):
    return base64.b64encode(file_storage.read()).decode("utf-8")

def build_image_messages(images):
    image_messages = []
    for image in images:
        try:
            ext = image.filename.split('.')[-1].lower()
            mime_type = f"image/{ext if ext != 'jpg' else 'jpeg'}"
            base64_str = encode_image_to_base64(image)
            image_messages.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{base64_str}",
                    "detail": "high"
                }
            })
        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
    return image_messages

def create_or_auth_AI(
    appcompany,
    client,
    key: str, 
    instructionsassistant: Optional[str] = None,
    nameassistant: Optional[str] = None, 
    model_select: Optional[str] = "gpt-4o-mini-2024-07-18", 
    tools: Optional[List] = [{"type": "file_search"},{"type": "code_interpreter"}],


    
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
        ref1 = db.reference(f'ai_org_assistant_id/User_{key}', app=appcompany)
        data1 = ref1.get()
        assistant_iddb = data1['assistant_id']
        instructionsassistantdb = data1['instructionsassistant']
        nameassistantdb = data1['nameassistant']
        model_selectdb = data1['model_select']
    
        client.beta.assistants.update(
            assistant_id=str(assistant_iddb),
            instructions=instructionsassistant
        )
        ref1 = db.reference(f'ai_org_assistant_id', app=appcompany)
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


        return str(assistant_iddb), str(instructionsassistantdb), str(nameassistantdb), str(model_selectdb)
    except Exception as err234:
    
        assistant = client.beta.assistants.create(
            name=nameassistant,
            instructions=instructionsassistant,
            model=model_select,
            tools=tools
        )


        ref1 = db.reference(f'ai_org_assistant_id', app=appcompany)
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



def create_or_auth_thread(
                        client,
                        appcompany,
                        file_ids_to_upload: Optional[List] = None,
                        code_interpreter_in_thread: Optional[List] = None,
                        user_id: Optional[str] = None
                        
                        ):

            
        try:
            ref1 = db.reference(f'ai_org_thread_Id/User_{user_id}', app=appcompany)
            data1 = ref1.get()
            thread_Id = data1['thread_id']
            print(thread_Id)
            # try:
            #     vector_store_id = data1['vector_store_id']

            #     if file_ids_to_upload is not None:
            #         batch = client.vector_stores.file_batches.create_and_poll(
            #             vector_store_id=vector_store_id,
            #             file_ids=file_ids_to_upload
            #         )

            #         client.beta.threads.update(
            #             thread_id=str(thread_Id),
            #             tool_resources={
            #                 "file_search": {
            #                 "vector_store_ids": [vector_store_id]
            #                 }
            #             }
            #         )

            # except Exception as err2342z:
            #     print(f"err2342z {err2342z}")
                
            return str(thread_Id)
        except Exception as err234z:
            # print(err234z)
            # tool_resources = {}
            # if file_ids_to_upload is not None:
            #     vector_store = client.vector_stores.create(
            #         name=f"{user_id}",
            #         file_ids=file_ids_to_upload
            #     )

            #     tool_resources["file_search"] = {"vector_store_ids": [vector_store.id]}
            #     thread = client.beta.threads.create(
            #         tool_resources=tool_resources
            #     )
            #     ref1 = db.reference(f'ai_org_thread_Id', app=appcompany)
            #     controle_das_funcao2 = f"User_{user_id}"
            #     controle_das_funcao_info_2 = {
            #         "thread_id": f'{thread.id}',
            #         "user_id": f'{user_id}',
            #         "vector_store_id": f"{vector_store.id}"
            #     }
            #     ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)

            #     return str(thread.id)

            # else:
                thread = client.beta.threads.create()
                ref1 = db.reference(f'ai_org_thread_Id', app=appcompany)
                controle_das_funcao2 = f"User_{user_id}"
                controle_das_funcao_info_2 = {
                    "thread_id": f'{thread.id}',
                    "user_id": f'{user_id}',

                }
                ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)

                return str(thread.id)

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

def save_assistant_message(session_id, message_obj, user_email, appcompany):
    try:
        user_email_filtred = user_email.replace(".", "_")
        base_ref = db.reference(f'users/{user_email_filtred}/conversations/{session_id}', app=appcompany)
        
        # Garante que o _meta seja criado apenas uma vez
        meta_ref = base_ref.child('_meta')
        if not meta_ref.get():
            meta_ref.set({
                "title": "Nova conversa",
                "created_at": datetime.now().isoformat()
            })

        # Verifica quantas mensagens já existem
        current_data = base_ref.get()
        existing_messages = {k: v for k, v in current_data.items() if k != "_meta"} if current_data else {}
        next_index = len(existing_messages)

        # Adiciona apenas a nova mensagem do assistente
        base_ref.child(str(next_index)).set(message_obj)

        return True
    except Exception as e:
        print(f"Error saving assistant message: {e}")
        return False

def save_conversation_history(session_id, history, user_email, appcompany):
    try:
        user_email_filtred = user_email.replace(".", "_")
        base_ref = db.reference(f'users/{user_email_filtred}/conversations/{session_id}', app=appcompany)
        
        # Garante que o _meta seja criado apenas uma vez
        meta_ref = base_ref.child('_meta')
        if not meta_ref.get():
            meta_ref.set({
                "title": "Nova conversa",
                "created_at": datetime.now().isoformat()
            })

        # Verifica quantas mensagens já existem
        current_data = base_ref.get()
        existing_messages = {k: v for k, v in current_data.items() if k != "_meta"} if current_data else {}
        next_index = len(existing_messages)

        # Adiciona apenas novas mensagens
        for i, msg in enumerate(history[-2:]):  # As duas últimas são user + system
            base_ref.child(str(next_index + i)).set(msg)

        return True
    except Exception as e:
        print(f"Error saving conversation history: {e}")
        return False

def fix_all_conversations(appcompany):
    ref = db.reference('conversations', app=appcompany)
    all_users = ref.get()
    
    for user_id, user_convos in all_users.items():
        for session_id, convo in user_convos.items():
            if isinstance(convo, list):
                # Converte para dict com chaves numéricas
                fixed_convo = {str(i): m for i, m in enumerate(convo)}
                ref.child(f"{user_id}/{session_id}").set(fixed_convo)
                print(f"[FIXED] {user_id}/{session_id}")
 
def get_conversation_history(session_id, user_email, appcompany, limit=100):
    user_email_filtred = user_email.replace(".", "_")
    ref = db.reference(f'users/{user_email_filtred}/conversations/{session_id}', app=appcompany)
    history = ref.get()
    
    if not history:
        return []

    clean_history = []
    for message in history:
        if isinstance(message, dict):
            if 'timestamp' not in message:
                message['timestamp'] = 0
            clean_history.append(message)
        else:
            print(f"[WARN] Mensagem ignorada por estar em formato inválido: {message}")

    sorted_history = sorted(clean_history, key=lambda x: x.get('timestamp', 0))
    return sorted_history[-limit:]

def autenticar_usuario(appcompany):
    api_key = get_api_key()
    if not api_key:
        response = jsonify({"error": "API Não fornecida."})
        response.status_code = 401
        return None, response

    user_email = (
        request.form.get("user_email")
        or request.args.get("user_email")
        or request.args.get("userEmail")
        or request.headers.get("X-User-Email")
    )

    if user_email:
        user_id = user_email.replace(".", "_")
        user_data = get_user_data_from_firebase(user_id, appcompany)
        if not user_data:
            response = jsonify({"error": "Usuário não encontrado."})
            response.status_code = 401
            return None, response
        return user_data, None

    # ⚠️ Adicione esse retorno padrão se `user_email` não for fornecido
    response = jsonify({"error": "user_email não informado nos headers ou parâmetros."})
    response.status_code = 400
    return None, response

   

def get_api_key():
    return request.headers.get('X-API-KEY')

def key_func():
    api_key = get_api_key()
    return api_key if api_key else get_remote_address()

def generate_api_key(subscription_plan):
    prefix_map = {
        "free": "apikey-free",
        "premium": "apikey-premium",
    }
    prefix = prefix_map.get(subscription_plan.lower(), "apikey-default")
    unique_part = secrets.token_urlsafe(32)
    api_key = f"{prefix}-{unique_part}"
    return api_key

def get_user_data_from_firebase(email, appcompany):
    """
    Função que obtém os dados do usuário no Firebase Realtime Database
    a partir da chave da API, na referência 'Users_Control_Panel'.
    """

    ref = db.reference(f'users/{email}', app=appcompany)
    user_data = ref.get()  # Obtém os dados do usuário com a chave especificada
    return user_data


def dynamic_rate_limit(appcompany):
    """
    Define o limite de requisições com base no e-mail do usuário.
    Substitui "." por "_" para usar como identificador único.
    """
    try:
        user_email = request.form.get("user_email") or request.args.get("user_email") or request.args.get("userEmail") or request.headers.get("X-User-Email")
        if user_email:
            user_id = user_email.replace(".", "_")
            user_data = get_user_data_from_firebase(user_id, appcompany)
            if user_data:
                return user_data.get("limit", "10 per minute")
            
    except Exception as e:
        print(f"[Rate Limit Error] {e}")
    return "10 per minute"






def download_tools_zip(tool_ids: list, extract_dir = os.path.join(os.path.dirname(__file__), 'Functions')) -> bool:
   """
   Faz o download do ZIP contendo os arquivos .py de múltiplas ferramentas.
   Após o download, extrai para a pasta 'Functions'.

   :param tool_ids: Lista com os IDs das ferramentas.
   :param output_path: Caminho de saída do arquivo ZIP.
   :param base_url: URL base da API.
   :return: True se tudo foi bem-sucedido, False caso contrário.
   """
   for i in range(10):
        
    output_path = 'tools_code.zip'
    base_url = 'https://softwareai-library-hub.rshare.io'
    joined_ids = ','.join(tool_ids)
    url = f'{base_url}/api/tool-code/{joined_ids}'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)

            # Extrai o ZIP para a pasta Functions
            
            os.makedirs(extract_dir, exist_ok=True)

            with zipfile.ZipFile(output_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            return True

        else:
            print(f"Erro {response.status_code}: {response.json()}")
            time.sleep(5)
            continue

    except Exception as e:
        print(f"Erro durante o download ou extração: {e}")
        time.sleep(5)
        continue

def import_tool(tool_name: str, base_dir = os.path.join(os.path.dirname(__file__), "..", 'Functions')):
    """
    Importa dinamicamente o módulo da ferramenta e retorna o objeto decorado com @function_tool.
    """
    module_path = os.path.join(base_dir, tool_name, f"{tool_name}.py")
    spec = importlib.util.spec_from_file_location(tool_name, module_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Procura por função decorada com @function_tool (tem atributo .name)
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if hasattr(attr, "name") and hasattr(attr, "description"):
                return attr

        raise ImportError(f"Nenhuma função decorada com @function_tool encontrada em {tool_name}.py")
    else:
        raise ImportError(f"Não foi possível importar a ferramenta: {tool_name}")

