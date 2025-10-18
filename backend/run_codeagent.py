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

title = ""
description = ""
category = ""
price = ""
technologies = ""
early_bonus = ""
deadline = ""
user_id = 1
tipo_app = "automacao"
local_to_save = os.path.join(os.path.dirname(__file__), 'WorkEnv')

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
        local_to_save = local_to_save
    ))
print(f"saved_files {saved_files}")