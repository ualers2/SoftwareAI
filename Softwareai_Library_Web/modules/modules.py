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

from flask import Flask, request, Response, stream_with_context
from openai.types.responses import ResponseTextDeltaEvent
from firebase_admin import credentials, db
from typing_extensions import TypedDict, Any, Union
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
import zipfile
import asyncio
from typing_extensions import TypedDict, Any
from agents import Agent, ItemHelpers, ModelSettings, function_tool, FileSearchTool, WebSearchTool, Runner, handoff
from dotenv import load_dotenv, find_dotenv
import importlib
import time
import uuid
import base64
import asyncio
import secrets
import inspect
import hmac
import hashlib
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
from openai.types.responses import ResponseTextDeltaEvent

from modules.Egetoolsv2 import *
from modules.EgetMetadataAgent import *
                  

def json_load(response):
    try:
        json_parse = json.load(response)
        return json_parse
    except: 
        try:
            json_parse = json.loads()
            return json_parse
        except:
            json_parse = response
            return json_parse

tool_outputs = []

def execute_function(function_name, args):
    global tool_outputs
    # Recuperar os parâmetros da função dinamicamente
    func = globals().get(function_name)
    if func:
        signature = inspect.signature(func)
        # Mapear os argumentos automaticamente
        mapped_args = {param.name: args.get(param.name, None) for param in signature.parameters.values()}
        result = func(**mapped_args)
        return result
    else:
        raise ValueError(f"Função {function_name} não encontrada")

def mappingtool(function_name, function_arguments, tool_call):
    global tool_outputs
    
    args = json.loads(function_arguments)
    result = execute_function(function_name, args)

    tool_outputs.append({
        "tool_call_id": tool_call["id"],
        "output": json.dumps(result)
    })

def submit_output(threead_id,
                client,
                run
                ):
    global tool_outputs
    # Submit all tool outputs at once after collecting them in a list
    if tool_outputs:
        try:
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=threead_id,
            run_id=run.id,
            tool_outputs=tool_outputs
            )
            print("Tool outputs submitted successfully.")
            tool_outputs = []
            return True
        except Exception as e:
            print("Failed to submit tool outputs:", e)
            try:
                client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=threead_id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
                tool_outputs = []
                return True
            except:
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=threead_id,
                    run_id=run,
                    tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
                tool_outputs = []
                return True
    else:
        print("No tool outputs to submit.")

class Run:
    def __init__(self, run_id):
        self.id = run_id



                  
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
    

async def process_stream(agent, attach_message, WEBHOOK_URL,
                            session_id,
                            user_email,
                            appcompany
                         ):

    save_history_user(
        session_id,
        user_email,
        attach_message,
        appcompany
            
        )

    result = Runner.run_streamed(
        agent,
        attach_message,
        max_turns=100
    )
    print("=== Run starting ===")

    async for event in result.stream_events():
        # We'll ignore the raw responses event deltas
        if event.type == "raw_response_event":
            continue
        # When the agent updates, print that
        elif event.type == "agent_updated_stream_event":
            message_to_send = f"Agent: {event.new_agent.name}"
            send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
            save_history_system(
                session_id,
                user_email,
                message_to_send,
                appcompany
                    
                )
            continue
        # When items are generated, print them
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                message_to_send = f"{event.item.agent.name} -- Tool was called"

                send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
                save_history_system(
                    session_id,
                    user_email,
                    message_to_send,
                    appcompany
                        
                    )

            elif event.item.type == "tool_call_output_item":
                message_to_send = f"{event.item.agent.name} -- Tool output: {event.item.raw_item}"

                send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
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
                    send_to_webhook(WEBHOOK_URL, "Chat Agent", "info", f"file_path: {file_path}")
                    send_to_webhook(WEBHOOK_URL, "Chat Agent", "info", f"parsed_output: {parsed_output}")
                    send_to_webhook(WEBHOOK_URL, "Chat Agent", "info", f"output_data: {output_data}")

                    if file_path and os.path.exists(file_path):
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
                    send_to_webhook(WEBHOOK_URL, "Chat Agent", "info", f"Erro ao processar o output: {str(e)}")
                
                    
            elif event.item.type == "reasoning_item":
                message_to_send = f"{event.item.agent.name} -- Reasoning"
                send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info",  message=message_to_send)
                save_history_system(
                    session_id,
                    user_email,
                    message_to_send,
                    appcompany
                        
                    )
            elif event.item.type == 'handoff_call_item':
                message_to_send = f"{event.item.agent.name} -- handoff was called"
                send_to_webhook(WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
                save_history_system(
                    session_id,
                    user_email,
                    message_to_send,
                    appcompany
                    )
                
            elif event.item.type == "message_output_item":
                message_to_send = f"{event.item.agent.name} -- {ItemHelpers.text_message_output(event.item)}"
                send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info",  message=message_to_send)
                save_history_system(
                    session_id,
                    user_email,
                    message_to_send,
                    appcompany
                        
                    )
            else:
                pass  # Ignore other event types

    print("=== Run complete ===")

async def process_stream_and_save_history(
                            agent_,
                            message,
                            WEBHOOK_URL,
                            session_id,
                            user_email,
                            number,
                            appcompany
                            
                            
                            ):
    
    # conversation_history = get_conversation_history(session_id, user_email=user_email, appcompany=appcompany)

    # # Criar a nova mensagem do usuário com timestamp
    # user_message_obj = {
    #     "role": "user",
    #     "content": message,
    #     "timestamp": int(time.time() * 1000)
    # }

    # # Prepara o input do agente: histórico + nova mensagem do usuário
    # agent_input = conversation_history + [user_message_obj]


    # agent_input_final = [
    #     {"role": msg["role"], "content": msg["content"]}
    #     for msg in message
    # ]

    await process_stream(agent_, message, WEBHOOK_URL,
                            session_id,
                            user_email,
                            appcompany
                                              
                        )
    
    print(f"🤖Sistema {number}")

    # send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=f"{agent_name} -- Message output: {result}")

    # assistant_message_obj = {
    #     "role": "system",
    #     "content": result,
    #     "timestamp": int(time.time() * 1000)
    # }
    # save_conversation_history(
    #     session_id=session_id,
    #     history=[user_message_obj, assistant_message_obj],
    #     user_email=user_email, 
    #     appcompany=appcompany
    # )
    



def valid(GITHUB_WEBHOOK_SECRET_CodeReview, signature, payload):
    computed_signature = 'sha256=' + hmac.new(
        GITHUB_WEBHOOK_SECRET_CodeReview.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    Payloaddecode = payload.decode('utf-8', errors='ignore')
    print(f"Signature from GitHub: {signature}")
    print(f"Computed Signature: {computed_signature}")

    if not hmac.compare_digest(signature, computed_signature):
        return "Assinatura inválida", 403

    try:
        data = json.loads(payload)
        return data
    except json.JSONDecodeError:
        return "Payload inválido", 400

def get_settings_agents(path_metadata = os.path.join(os.path.dirname(__file__), "metadata.json")):
    with open(path_metadata, encoding='utf-8') as f:
        metadata = json.load(f)
        instruction_property = metadata.get("instruction_property")
        instruction_path = metadata.get("instruction_path")
        model_agent = metadata.get("model")
        tools_agent = metadata.get("tools")
        name_agent = metadata.get("name")

    path_instruction = os.path.join(os.path.dirname(__file__), instruction_path)
    with open(path_instruction, 'r', encoding='utf-8') as f:
        instruction_original = f.read()

    return name_agent, model_agent, instruction_original, tools_agent 


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

def format_instruction(instruction: str, context: dict) -> str:
    pattern = re.compile(r'\{(\w+)\}')
    def repl(match):
        var_name = match.group(1)
        if var_name in context:
            return str(context[var_name])
        else:
            raise KeyError(f"Variável '{var_name}' não encontrada no contexto.")
    return pattern.sub(repl, instruction)

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
        base_ref = db.reference(f'conversations/{user_email.replace(".", "_")}/{session_id}', app=appcompany)
        
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
        base_ref = db.reference(f'conversations/{user_email.replace(".", "_")}/{session_id}', app=appcompany)
        
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
    ref = db.reference(f'conversations/{user_email.replace(".", "_")}/{session_id}', app=appcompany)
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
    """
    Função para validar a API Key.
    Retorna os dados do usuário caso a API Key seja válida,
    ou uma resposta de erro caso contrário.
    """
    api_key = get_api_key()
    if not api_key:
        response = jsonify({"error": "API Não fornecida."})
        response.status_code = 401  # Unauthorized
        return None, response

    user_email = request.form.get("user_email") or request.args.get("user_email") or request.args.get("userEmail") or request.headers.get("X-User-Email")
    if user_email:
        user_id = user_email.replace(".", "_")
        user_data = get_user_data_from_firebase(user_id, appcompany)
        if not user_data:
            response = jsonify({"error": "Usuário não encontrado."})
            response.status_code = 401  # Unauthorized
            return None, response
        else:
            return user_data, None
    # response = jsonify({"error": "API Key invalida."})
    # response.status_code = 401  # Unauthorized
    # return None, response


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


def find_agent_paths(agent_id, AGENTS_DIR, BASE_DIR):
    """
    Retorna lista de (root_folder, agent_root) onde agent_id foi encontrado,
    buscando recursivamente em AGENTS_DIR.
    """
    paths = []
    for root_folder in AGENTS_DIR:
        start = os.path.join(BASE_DIR, root_folder)
        for dirpath, dirnames, _ in os.walk(start):
            if os.path.basename(dirpath) == agent_id:
                paths.append((root_folder, dirpath))
    return paths
