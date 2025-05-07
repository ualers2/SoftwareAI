import os
import time
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler
from firebase_admin import credentials, db, initialize_app
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response, Response
from flask_cors import CORS
from datetime import timedelta
import os
import json
import yaml
from dotenv import load_dotenv
import logging
import sys
import importlib.util
import inspect
import hashlib
import io
from modules.calculate_tool_hash import *
from modules.register_tool_version import *

import os
import json
import logging
import time
import sys
from dotenv import load_dotenv
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler
from firebase_admin import credentials, initialize_app, db

load_dotenv(dotenv_path="Keys/keys.env")

BASE_DIR = os.path.join(os.path.dirname(__file__), 'FunctionsAndTools', 'Functions') 

# Caminho para credenciais Firebase
env_path = os.getenv('FIREBASE_CREDENTIALS', '/app/Keys/appcompany.json')
firebase_URL = os.getenv('FIREBASE_URL')
with open(env_path) as f:
    cred_json = f.read()
cred = credentials.Certificate(json.loads(cred_json))
appcompany = initialize_app(cred, {
    'databaseURL': firebase_URL
}, name='appcompany')

# Configura o logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)  # ou INFO, WARNING etc.

# Cria um handler para a saída padrão (stdout)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# Formato dos logs
formatter = logging.Formatter(
    fmt='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

# Evita adicionar múltiplos handlers
if not logger.hasHandlers():
    logger.addHandler(handler)

# Diretórios onde ficam os agentes definidores\BASE_DIR = os.getenv('AGENTS_BASE_DIR', 'Agents')
WATCHED_DIRS = [os.path.join(BASE_DIR, agent) for agent in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, agent))]

class ToolChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        try:
                
            # considera modificações em arquivo de metadados (.md/.yml/.yaml/.json)
            if not event.is_directory and event.src_path.endswith(('.py', '.md', '.yml', '.yaml', '.json')):
                tool_path = os.path.dirname(event.src_path)
                tool_id = os.path.basename(tool_path)

                with open(os.path.join(tool_path, "metadata.json"), encoding='utf-8') as f:
                    tool_metadata = json.load(f)

                with open(os.path.join(tool_path, f"{tool_id}.py"), encoding='utf-8') as f:
                    tool_code = f.read()

                with open(os.path.join(tool_path, f"tool-compose.yml"), encoding='utf-8') as f:
                    tool_compose = f.read()

                new_hash = calculate_tool_hash(tool_path)
                register_tool_version(
                                    tool_id, 
                                    new_hash, 
                                    appcompany,
                                    tool_metadata,
                                    tool_code,
                                    tool_compose
                                    )
                logger.info(f"[tools_watcher] Atualização em {tool_id}: hash {new_hash}")
        except Exception as err:
            logger.info(f"[tools_watcher] {err}")
            
class ToolsFolderChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            logger.info(f"[tools_watcher] Novo Tool detectado: {event.src_path}")
            observer.schedule(ToolChangeHandler(), event.src_path, recursive=True)

if __name__ == '__main__':
    observer = Observer()

    observer.schedule(ToolsFolderChangeHandler(), BASE_DIR, recursive=False)

    for path in WATCHED_DIRS:
        observer.schedule(ToolChangeHandler(), path, recursive=True)

    observer.start()
    logger.info("[tools_watcher] Observando alterações em functions...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()