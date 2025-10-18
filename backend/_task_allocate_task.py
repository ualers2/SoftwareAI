import os
import json
from datetime import datetime
from api import db, app
from Models.postgreSQL import BackendTask  # importe seu modelo correto

# Configurações iniciais
TASK_ID = 3  # ID da tarefa que você quer atualizar
AGENT_NAME = "CodAgent"  # Nome do agente a ser alocado

# Exemplo de project_files compatível com FileItem do front-end
PROJECT_FILES = [
    {"name": "server.js", "language": "javascript", "lines": 120, "status": "completed"},
    {"name": "auth.js", "language": "javascript", "lines": 45, "status": "in_progress"},
    {"name": "README.md", "language": "markdown", "lines": 10, "status": "completed"},
]

def allocate_task(task_id: int, agent_name: str, project_files: list):
    with app.app_context():

        task = db.session.query(BackendTask).filter_by(id=task_id).first()
        if not task:
            print(f"Tarefa {task_id} não encontrada.")
            return

        task.allocated_agent = agent_name
        task.project_files = project_files
        task.status = "running" 
        task.progress = 20 
        task.updated_at = datetime.utcnow() if hasattr(task, "updated_at") else None

        db.session.commit()
        print(f"Tarefa {task_id} atualizada com sucesso!")
        print(f"Agente: {agent_name}")
        print(f"Arquivos: {json.dumps(project_files, indent=2)}")

if __name__ == "__main__":
    allocate_task(TASK_ID, AGENT_NAME, PROJECT_FILES)
