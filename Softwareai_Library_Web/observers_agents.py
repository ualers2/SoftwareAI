import os
import json
import logging
import time
import sys
from dotenv import load_dotenv
from watchdog.observers.polling import PollingObserver as Observer
from watchdog.events import FileSystemEventHandler
from firebase_admin import credentials, initialize_app, db
from modules.calculate_agent_hash import calculate_agent_hash
from modules.register_agent_version import register_agent_version


load_dotenv(dotenv_path="Keys/keys.env")

BASE_DIR = os.path.join(os.path.dirname(__file__), 'Agents') 

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

class AgentChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        try:
                
            # considera modificações em arquivo de metadados (.md/.yml/.yaml/.json)
            if not event.is_directory and event.src_path.endswith(('.py', '.md', '.yml', '.yaml', '.json')):
                agent_path = os.path.dirname(event.src_path)

                with open(os.path.join(agent_path, "metadata.json"), encoding='utf-8') as f:
                    metadata = json.load(f)
                    type_plan = metadata.get("type_plan", "free")
                    instruction_path = metadata.get("instruction_path")
                    tutorial_path = metadata.get("tutorial_path")
                    model_agent = metadata.get("model")
                    tools_agent = metadata.get("tools")
                    name_agent = metadata.get("name")
                    shortDescription = metadata.get("shortDescription")
                    fullDescription = metadata.get("fullDescription")
                    UseCases = metadata.get("UseCases")
                    icon = metadata.get("icon")

                with open(os.path.join(agent_path, instruction_path), 'r', encoding='utf-8') as f:
                    instruction_original = f.read()

                with open(os.path.join(agent_path, tutorial_path), 'r', encoding='utf-8') as f:
                    tutorial = f.read()

                logger.info(tutorial)
                agent_id = os.path.basename(agent_path)

                new_hash = calculate_agent_hash(agent_path)
                register_agent_version(
                                        icon,
                                        type_plan,
                                        agent_id,
                                        shortDescription,
                                        fullDescription,
                                        UseCases,
                                        instruction_original,
                                        instruction_path,
                                        tutorial,
                                        model_agent,
                                        name_agent,
                                        tools_agent,
                                        new_hash, 
                                        appcompany,
                                        logger
                                        
                                        )
                logger.info(f"[agent_watcher] Atualização em {agent_id}: hash {new_hash}")
        except Exception as err:
            logger.info(f"[agent_watcher] {err}")
            
class AgentsFolderChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            logger.info(f"[agent_watcher] Novo agente detectado: {event.src_path}")
            observer.schedule(AgentChangeHandler(), event.src_path, recursive=True)

if __name__ == '__main__':
    observer = Observer()

    # Primeiro observa o diretório raiz dos agentes
    observer.schedule(AgentsFolderChangeHandler(), BASE_DIR, recursive=False)

    # Depois adiciona os agentes já existentes
    for path in WATCHED_DIRS:
        observer.schedule(AgentChangeHandler(), path, recursive=True)

    observer.start()
    logger.info("[agent_watcher] Observando alterações em agentes...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()