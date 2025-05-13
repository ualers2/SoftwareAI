from server import celery_app  # ajusta o path conforme seu projeto
import os
from celery import Celery
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
appcompany = initialize_app(cred, {
    'databaseURL': firebase_db_url
},name="appcompany")


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
    type_stream = task_params.get("type_stream")
    prompt_continuous = task_params.get("prompt_continuous", "")
    path_ProjectWeb = task_params.get("path_ProjectWeb")
    path_html = task_params.get("path_html")
    path_js = task_params.get("path_js")
    path_css = task_params.get("path_css")
    doc_md = task_params.get("doc_md")
    path_Keys = task_params.get("path_Keys")


    async def _run_agent(agent, message, webhook_tag):
        # retry + fallback
        for _ in range(3):
            try:
                await process_stream(
                    type_stream, 
                    agent, 
                    message,
                    WEBHOOK_URL,
                    session_id, 
                    user_email,
                    appcompany
                )
                return True
            except Exception as e:
                if "Error streaming response" in str(e):
                    continue
                raise
        return False

    # Execução síncrona do fluxo
    try:

        # 1) Project Manager
        agent = TriageAgent(
            session_id, user_email,
            path_ProjectWeb, path_html, path_js, path_css, doc_md, path_Keys
        )
        asyncio.run(_run_agent(agent, user_message, "ProjectManager"))

        # 2) Code Review pre-projeto
        agent2, _ = CodeReview_Preproject(
            session_id, user_email,
            path_ProjectWeb, path_html, path_js, path_css, doc_md, path_Keys,
            user_message
        )
        asyncio.run(_run_agent(agent2, prompt_continuous, "CodeReview_Preproject"))

        # 3) Code Requirements and Timeline
        agent3, _ = CodeRequirementsAndTimeline(
            session_id, user_email,
            path_ProjectWeb, path_html, path_js, path_css, doc_md, path_Keys
        )
        asyncio.run(_run_agent(agent3, prompt_continuous, "CodeRequirementsAndTimeline"))

        # 4) Code Review Timeline
        agent4, _ = CodeReview_Timeline(
            session_id, user_email,
            path_ProjectWeb, path_html, path_js, path_css, doc_md, path_Keys
        )
        asyncio.run(_run_agent(agent4, prompt_continuous, "CodeReview_Timeline"))

        return {"status": "SUCCESS", "session_id": session_id}
    except Exception as e:
        # Atualiza status no Firebase em caso de falha

        ref = db.reference(f'save_tasks_users/task/{user_email}', app=appcompany)
        tasks = ref.get() or {}
        for task_id, data in tasks.items():
            if data.get('session_id') == session_id:
                ref.child(task_id).update({"status": "FAILED", "error": str(e)})
        return {"status": "FAILED", "error": str(e), "session_id": session_id}
