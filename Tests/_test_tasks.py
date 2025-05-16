import requests
from datetime import datetime, timedelta
import pytz

# URL base da sua API
API_BASE = "https://softwareai-shdule.rshare.io"

def schedule_project_manager_task():
    # Parâmetros que serão enviados à task
    params = {
        "session_id": "abc123",
        "user_email": "freitasalexandre810@gmail_com",
        "user_message": "Preciso de um pré-projeto para um SaaS de marketplace",
        "type_stream": "agentworkflow",
        "prompt_continuous": "Siga Com os objetivos da instrucao",
        "path_ProjectWeb": "/app/LocalProject",
        "path_html": "templates",
        "path_js": "static/js",
        "path_css": "static/css",
        "doc_md": "docs",
        "path_Keys": "Keys"
    }

    # Agendamos para daqui a 2 minutos (exemplo)
    tz = pytz.timezone("America/Sao_Paulo")
    run_at = datetime.now(tz) + timedelta(minutes=1)
    # Formata como ISO YYYY-MM-DDTHH:MM:SS
    run_at_str = run_at.strftime("%Y-%m-%dT%H:%M:%S")

    payload = {
        "agent": "AgentsWorkFlow.Saas.teams.ProjectManager",
        "params": params,
        "run_at": run_at_str
    }

    resp = requests.post(f"{API_BASE}/schedule-agent", json=payload)
    resp.raise_for_status()

    data = resp.json()
    print("Agendamento criado:")
    print(f" • db_task_id:   {data['db_task_id']}")
    print(f" • celery_task_id: {data['celery_task_id']}")
    print(f" • run_at:    {data['scheduled_for']}")

    return params["user_email"], data["db_task_id"]


def get_task_status(user_email, task_id):
    resp = requests.get(f"{API_BASE}/task-status/{user_email}/{task_id}")
    if resp.status_code == 404:
        print("Tarefa não encontrada.")
        return
    resp.raise_for_status()
    status = resp.json().get("status")
    print(f"Status da tarefa {task_id}: {status}")
    return status


if __name__ == "__main__":
    # 1) Agendar
    email, tid = schedule_project_manager_task()

    # 2) Depois (pode esperar alguns segundos) consultar status
    import time; time.sleep(5)
    get_task_status(email, tid)
