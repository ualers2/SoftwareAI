# celery_app.py
from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import pytz

from Models.postgreSQL import db 
from Models.postgreSQL import BackendTask, TaskStatus
from Modules.Geters.next_task import get_next_task  
from api import app

os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'Keys', 'keys.env'))

from Agents.AppAI.CodeBackend.ai import CodeBackEndAgent

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REDIS_URL = "redis://redis:6379/0"
local_to_save = os.path.join(os.path.dirname(__file__), 'WorkEnv')
os.makedirs(local_to_save, exist_ok=True)

celery_app = Celery(
    "api",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    task_track_started=True, # Permite o acompanhamento do progresso
    worker_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
    worker_task_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(taskName)s %(task_id)s %(message)s",
    loglevel='DEBUG',
    worker_concurrency=10,  
    task_always_eager=False,  
    task_acks_late=False,  # Garante que a tarefa só será confirmada após sua execução
    task_reject_on_worker_lost=True,
)
celery_app.conf.worker_prefetch_multiplier = 1
celery_app.conf.timezone = 'America/Sao_Paulo'
celery_app.conf.enable_utc = False
# celery_app.autodiscover_tasks(['.'])
# from tasks import *

# celery_app.conf.beat_schedule = {
#     "run-backend-agent-daily": {
#         "task": "tasks.run_backend_agent",
#         "schedule": crontab(hour=9, minute=0),
#         "args": ("user_123", "Implementar endpoints do backend hoje", "pt")
#     },
# }

celery_app.conf.beat_schedule = {
    "process-dynamic-queue-every-minute": {
        "task": "celery_app.process_dynamic_queue",
        "schedule": crontab(minute="*/1"),
    },
}
@celery_app.task
def process_dynamic_queue():
    """
    Verifica o banco e envia a próxima tarefa para execução.
    """
    with app.app_context():
            
        task = get_next_task()
        if not task:
            print("🚫 Nenhuma tarefa pendente.")
            return

        print(f"🚀 Executando tarefa #{task.id} | Prioridade: {task.priority}")

        async def execute_task():
            try:
                eta_str = task.eta_str
                eta_dt = None
                if eta_str:
                    try:
                        eta_dt = datetime.fromisoformat(eta_str)
                    except ValueError:
                        print(f"Formato de 'eta' inválido. Use ISO 8601")
                        task.status = TaskStatus.FAILED.value
                        db.session.commit()

                if task.category == "desenvolvimento":
                    result = run_backend_agent.apply_async(
                        args=(
                            task.id,
                            task.user_id, 
                            task.user_content, 
                            task.commit_language
                        ),
                        eta=eta_dt
                    )
                    print(f"Tarefa #{task.id} enviada com sucesso.")
                return result
            except Exception as e:
                print(f"Erro ao enviar tarefa #{task.id}: {e}")
                # Atualiza status para FAILED
                task.status = TaskStatus.FAILED.value
                db.session.commit()

        asyncio.run(execute_task())

@celery_app.task
def run_backend_agent(task_id, user_id: str, user_content: str, commit_language: str = "pt"):
    """Task Celery para executar o CodeBackEndAgent."""
    with app.app_context():

        print(f"🚀 Executando tarefa CodeBackEndAgent")

        # total_tokens, saved_files = asyncio.run(
        #     CodeBackEndAgent(
        #         OPENAI_API_KEY=OPENAI_API_KEY,
        #         user_id=user_id,
        #         user_content=user_content,
        #         commit_language=commit_language,
        #         local_to_save=local_to_save
        #     )
        # )
        total_tokens = 7800
        saved_files = ''
        tz = pytz.timezone("America/Sao_Paulo")
        if task_id:
            task = BackendTask.query.get(task_id)
            if task:
                task.status = TaskStatus.DONE.value
                task.completed_at = datetime.now(tz)
                task.total_tokens = total_tokens
                db.session.commit()

        return {"total_tokens": total_tokens, "saved_files": saved_files}