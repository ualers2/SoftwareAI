from datetime import datetime
from api import db, app
from Models.postgreSQL import BackendTask, TaskLog

TASK_ID = 3
NEW_LOGS = [
    {"id": "log1", "type": "info", "message": "Tarefa iniciada pelo agente CodAgent", "timestamp": datetime.utcnow()},
    {"id": "log2", "type": "success", "message": "Estrutura inicial do projeto carregada", "timestamp": datetime.utcnow()},
]

def allocate_logs(task_id: int, logs: list):
    with app.app_context():
        task = db.session.query(BackendTask).filter_by(id=task_id).first()
        if not task:
            print(f"Tarefa {task_id} não encontrada.")
            return

        for log in logs:
            new_log = TaskLog(
                task_id=task.id,
                type=log["type"],
                message=log["message"],
                task_metadata={},  # se precisar de dados extras
                created_at=log["timestamp"]
            )
            db.session.add(new_log)

        task.updated_at = datetime.utcnow() if hasattr(task, "updated_at") else None
        db.session.commit()
        print(f"Logs alocados com sucesso na tarefa {task_id}!")

if __name__ == "__main__":
    allocate_logs(TASK_ID, NEW_LOGS)
