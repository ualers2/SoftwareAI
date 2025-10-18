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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
from Agents.AppAI.CodeBackend.ai import CodeBackEndAgent

tipo_app = "automação"
title = "Automação de Backup de Arquivos para Nuvem"
description = "Criar uma aplicação em Python que monitore uma pasta local e faça backup automático de arquivos novos ou modificados para um serviço de nuvem (como Google Drive ou Dropbox). O sistema deve gerar logs das transferências, enviar notificações por e-mail em caso de erro, e permitir configuração de periodicidade e pastas monitoradas. Deve ser fácil de instalar e executar em segundo plano."
category = "automação e manutenção de sistemas"
price = "650"
technologies = "python, watchdog, smtplib, google-api-python-client"
early_bonus = "50"
deadline = "2025-10-19 18:12:00"
user_id = 1
local_to_save = os.path.join(os.path.dirname(__file__), 'WorkEnv')
model = "gpt-5-nano"

total_usage, saved_files = asyncio.run(CodeBackEndAgent(
        OPENAI_API_KEY,
        user_id,
        tipo_app,
        title,
        description,
        category,
        price,
        technologies,
        early_bonus,
        deadline,
        model=model,
        local_to_save = local_to_save
    ))
print(f"saved_files {saved_files}")
