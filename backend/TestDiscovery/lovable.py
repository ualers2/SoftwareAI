import os
import threading
import requests
import json
import logging
from dotenv import load_dotenv
import asyncio
import stripe
from decimal import Decimal
from bson.json_util import dumps
from datetime import datetime, timedelta, timezone
import hmac
import hashlib
from flask import g, Flask, Response, request, jsonify, send_file, abort, redirect
from flask_cors import CORS
from asgiref.wsgi import WsgiToAsgi
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'Keys', 'keys.env'))

from Agents.AppAI.PredictedTypeApp.ai import GeneratePredictedTypeAppAgent
from Agents.AppAI.SprintsPlanner.ai import SprintsPlannerAppAgent
from Agents.AppAI.CodeBackend.ai import CodeBackEndAgent
from Agents.AppAI.RequirementsPlanner.ai import RequirementsPlannerAppAgent
from Agents.AppAI.SprintsSheduler.ai import SprintsShedulerAppAgent

from Agents.AppAI.CodeFrontend.ai import CodeFrontendAgent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
user_id = 1
model = "gpt-5-nano"
commit_language = "pt"
type_devlopment = 'create'
project_name = "Agendmedi"
tipo_app = "SaaS: Agenda de Consultas com Pagamento"
descricao = "sistema multiusuário (médicos e pacientes) para agendamento online de consultas com pagamento integrado via Stripe. Backend em Flask, PostgreSQL, Redis; Front-end em Vite + React; Observabilidade com MongoDB; Orquestração de tarefas com Celery + Redis; CI/CD com GitHub Actions."
user_task = "Quero um sistema onde médicos e pacientes possam agendar consultas online e pagar pelo site."
BACKEND_URL = "http://localhost:5910/api/tasks/add"
ACCESS_TOKEN = "IJGpuZxIP0eIJRfpzUsuCMbOEkq0dwR-Lq8sY2Uo-o0" 
local_to_save = os.path.join(os.path.dirname(__file__), 'WorkEnv')


# type_app, justificativa, total_usage = asyncio.run(GeneratePredictedTypeAppAgent(
#         OPENAI_API_KEY,
#         user_id,
#         user_task,
#         commit_language = commit_language,
#         model = model,
#     ))

# print(f"type_app {type_app}")
# print(f"justificativa {justificativa}")
# print(f"total_usage {total_usage}")



# user_content = f"""
# user request: {user_task}\n

# Predicted Type App:\n
# type_app: {type_app}\n
# justificativa: {justificativa}


# """

# user_content = """
# Descrição do produto: sistema multiusuário (médicos e pacientes) para agendamento online de consultas com pagamento integrado via Stripe. Backend em Flask, PostgreSQL, Redis; Front-end em Vite + React; Observabilidade com MongoDB; Orquestração de tarefas com Celery + Redis; CI/CD com GitHub Actions.

# """
# total_usage, saved_files = asyncio.run(RequirementsPlannerAppAgent(
#         OPENAI_API_KEY,
#         user_id,
#         tipo_app,
#         descricao,
#         user_content,
#         commit_language = commit_language,
#         model = model,
#         local_to_save = local_to_save,
#         type_requirements="frontend"

#     ))
# print(f"saved_files {saved_files}")


saved_files = ['e:\\Users\\Media Cuts DeV\\Downloads\\WorkEnv\\SoftwareAI\\Back-End\\WorkEnv/docs/technical-requirements.md', 'e:\\Users\\Media Cuts DeV\\Downloads\\WorkEnv\\SoftwareAI\\Back-End\\WorkEnv/docs/adr/001-architecture-decision.md', 'e:\\Users\\Media Cuts DeV\\Downloads\\WorkEnv\\SoftwareAI\\Back-End\\WorkEnv/docs/adr/002-api-client.md', 'e:\\Users\\Media Cuts DeV\\Downloads\\WorkEnv\\SoftwareAI\\Back-End\\WorkEnv/docs/adr/003-state-management.md', 'e:\\Users\\Media Cuts DeV\\Downloads\\WorkEnv\\SoftwareAI\\Back-End\\WorkEnv/docs/adr/004-security.md', 'e:\\Users\\Media Cuts DeV\\Downloads\\WorkEnv\\SoftwareAI\\Back-End\\WorkEnv/docs/requirements-summary.md']

total_usage, saved_files = asyncio.run(CodeFrontendAgent(
        OPENAI_API_KEY,
        user_id,
        tipo_app,
        descricao,
        saved_files,
        model = model,
        local_to_save = local_to_save,
        type_devlopment=type_devlopment,
        project_name=project_name,

    ))
print(f"saved_files {saved_files}")





# saved_files = ['docs/technical-requirements.md', 'docs/adr/001-architecture-decision.md', 'docs/adr/002-architecture-decision.md', 'docs/adr/003-architecture-decision.md', 'docs/requirements-summary.md']

# total_usage, caminho_do_arquivo =  asyncio.run(SprintsPlannerAppAgent(
#     OPENAI_API_KEY,
#     user_id,
#     tipo_app,
#     descricao,
#     saved_files,
#     commit_language = commit_language,
#     model = model,
#     local_to_save=local_to_save
# ))

# print(f"total_usage {total_usage}")
# print(f"caminho_do_arquivo {caminho_do_arquivo}")

# os.chdir(os.path.join(os.path.dirname(__file__)))



# with open(os.path.join(local_to_save, "sprint_plan.md"), "r") as content:
#     user_content = content.read()

# total_usage, total_de_tasks =  asyncio.run(SprintsShedulerAppAgent(
#     OPENAI_API_KEY,
#     user_id,
#     ACCESS_TOKEN,
#     user_content,
#     BACKEND_URL,
#     commit_language = commit_language,
#     model = model,
# ))

# print(f"total_usage {total_usage}")
# print(f"total_de_tasks {total_de_tasks}")

# with open(os.path.join(local_to_save, "sprint_1.md"), "r") as content:
#     user_content = content.read()

# total_usage, saved_files = asyncio.run(CodeBackEndAgent(
#         OPENAI_API_KEY,
#         user_id,
#         tipo_app,
#         descricao,
#         user_content,
#         commit_language = commit_language,
#         model = model,
#         local_to_save = local_to_save
#     ))
# print(f"saved_files {saved_files}")
