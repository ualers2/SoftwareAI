import os
import yaml
import subprocess
import json
from dotenv import load_dotenv
from modules.services.check_service_running import check_service_running
from firebase_admin import credentials, db

def load_agents_from_firebase(appcompany):
    ref = db.reference('agents', app=appcompany)
    all_agents = ref.get() or {}

    agents = []
    for agent_id, agent_data in all_agents.items():
        metadata = agent_data.get('metadata', {})

        info = {
            "id": agent_id,
            "type_plan": metadata.get("type_plan"),
            "name": metadata.get("name"),
            "icon": metadata.get("icon"),
            "shortDescription": metadata.get("shortDescription"),
            "fullDescription": metadata.get("fullDescription"),
            "UseCases": metadata.get("UseCases"),
            "instruction": metadata.get("instruction"),
            "model": metadata.get("model"),
            "tools": metadata.get("tools"),
            "tutorial": metadata.get("tutorial"),
            "about": metadata.get("about", " "),
        }

        agents.append(info)
    
    return agents

def load_agents(AGENTS_DIR):
    agents = []
    
    for agent_id in os.listdir(AGENTS_DIR):
        agent_path = os.path.join(AGENTS_DIR, agent_id)
        if os.path.isdir(agent_path):
            info_path = os.path.join(agent_path, "softwareai-compose.yml")
            about_path = os.path.join(agent_path, "about.md")
            tutorial_path = os.path.join(agent_path, "tutorial.md")
            # keys_path = os.path.join(agent_path, "Keys", "keys.env")
            metadata_path = os.path.join(agent_path, "metadata.json")

            path_metadata = os.path.join(os.path.dirname(__file__), )
            with open(path_metadata, encoding='utf-8') as f:
                metadata = json.load(f)
                agent_id_compose = metadata.get("id")
                agent_name = metadata.get("name")
                agent_icon = metadata.get("icon")
                agent_shortDescription = metadata.get('shortDescription')
                agent_fullDescription = metadata.get('fullDescription')
                agent_UseCases = metadata.get('UseCases')

                # if os.path.exists(info_path):
                #     with open(info_path, "r", encoding="utf-8") as file:
                #         config = yaml.safe_load(file)

                # agent_compose = config.get('agent_compose', {})

                # agent_id_compose = agent_compose.get('id')
                # agent_name = agent_compose.get('name')
                # agent_icon = agent_compose.get('icon')
                # agent_shortDescription = agent_compose.get('shortDescription')
                # agent_fullDescription = agent_compose.get('fullDescription')
                # agent_UseCases = agent_compose.get('UseCases')
                # agent_key = agent_compose.get('key')
                # agent_companyname = agent_compose.get('companyname')
                # agent_modelSelect = agent_compose.get('modelSelect')
                # agent_private_project = agent_compose.get('private_project')
                # agent_service_name = agent_compose.get('service_name', agent_id)  # fallback para o ID

                with open(about_path, "r", encoding="utf-8") as f:
                    about = f.read()
                    
                with open(tutorial_path, "r", encoding="utf-8") as f:
                    tutorial = f.read()
                
                # load_dotenv(dotenv_path=keys_path)

                is_running = True #check_service_running(agent_service_name)

                info = {
                    "id": agent_id_compose,
                    "name": agent_name,
                    "icon": agent_icon,
                    "shortDescription": agent_shortDescription,
                    "fullDescription": agent_fullDescription,
                    "UseCases": agent_UseCases,
                    "tutorial": tutorial,
                    "about": about,
                    "apikey": os.getenv("OPENAI_API_KEY"),
                    "agent_key": "agent_key",
                    "companyname": "agent_companyname",
                    "modelSelect": "agent_modelSelect",
                    "private_project": "agent_private_project",
                    "status": "running" if is_running else "stopped"
                }

                agents.append(info)

                # load_dotenv(dotenv_path="keys.env")

    return agents