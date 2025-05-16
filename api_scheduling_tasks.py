from api_scheduling import celery_app  # ajusta o path conforme seu projeto
import os
import requests
import threading
import traceback
from dotenv import load_dotenv
import asyncio
from softwareai_engine_library.Chat._init_chat_ import *
from firebase_admin import credentials, initialize_app, storage, db, delete_app
       
from AgentsWorkFlow.Saas.Decisions.TypeProject.Integration import TriageAgent
from AgentsWorkFlow.Saas.Code.CodeReview.CodeReview_Preproject.Integration import CodeReview_Preproject
from AgentsWorkFlow.Saas.Code.ProjectManager.Timeline.Integration import CodeRequirementsAndTimeline
from AgentsWorkFlow.Saas.Code.CodeReview.CodeReview_Timeline.Integration import CodeReview_Timeline

dotenv_path = os.path.join(os.path.dirname(__file__), "Keys", "keys.env")
load_dotenv(dotenv_path=dotenv_path)

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

firebase_json_path = os.getenv("firebase_json_path")
firebase_db_url = os.getenv("firebase_db_url")

# --- Initialize Firebase ---
cred = credentials.Certificate(firebase_json_path)
appcompany2 = initialize_app(cred, {
    'databaseURL': firebase_db_url
},name="appcompany2")


@celery_app.task(name="AgentsWorkFlow.Saas.teams.ProjectManager")
def run_project_manager_task(task_params):
    """
    Task Celery para o fluxo de trabalho do Project Manager.
    task_params deve incluir:
      - session_id, user_email, user_message, type_stream,
      - path_ProjectWeb, path_html, path_js, path_css, doc_md, path_Keys,
      - prompt_continuous
    """
    session_id = task_params.get("session_id")
    user_email = task_params.get("user_email")
    user_message = task_params.get("user_message")
    api_key = task_params.get("type_stream")
    db_task_id = task_params.get("db_task_id")
    repo_git = task_params.get("repo_git")

    # Execução síncrona do fluxo
    try:

        # URL base da sua API
        API_AgentsWorkFlowSaas = "https://softwareai.rshare.io/api/AgentsWorkFlow/Saas"
        headers = {
        "X-API-KEY": f"{api_key}",
        "X-User-Email": f"{user_email}",
        }
        body = {
        "repo_git": f"{repo_git}",
        "session_id": f"{session_id}",
        "user_email": f"{user_email}",
        "user_message": f"{user_message}",
        "name_project": "Nome_Gerado_Por_Voce",
        }
        resp = requests.post(API_AgentsWorkFlowSaas, headers=headers, json=body)
        resp.raise_for_status()
        data = resp.json()
        print(":")

        ref = db.reference(f'users/{user_email}/tasks_user/{db_task_id}', app=appcompany2)
        tasks = ref.get() or {}
        if tasks.get('db_task_id') == db_task_id:
            ref.update({"status": "SUCCESS"})
        return {"status": "SUCCESS", "session_id": session_id}
    except Exception as e:
        ref = db.reference(f'users/{user_email}/tasks_user/{db_task_id}', app=appcompany2)
        tasks = ref.get() or {}
        if tasks.get('db_task_id') == db_task_id:
            ref.update({"status": "FAILED"})
        return {"status": "FAILED", "error": str(e), "session_id": session_id}
