from Models.postgreSQL import db 
from Models.postgreSQL import BackendTask, TaskStatus
from datetime import datetime
import pytz

def create_task(user_id, content, priority=1, hours="1.2", lang="pt", eta_str='', EMPLOYER_CATEGORY=''):
    """
    Cria uma tarefa no banco Flask-SQLAlchemy.
    """
    tz = pytz.timezone("America/Sao_Paulo")

    task = BackendTask(
        user_id=user_id,
        category=EMPLOYER_CATEGORY,
        user_content=content,
        priority=priority,
        estimated_hours=hours,
        commit_language=lang,
        status=TaskStatus.PENDING.value,
        created_at=datetime.now(tz),
        eta_str=eta_str
    )
    db.session.add(task)
    db.session.commit()
    print(f"Tarefa criada: {task.id}")
    return task.id

# # Exemplo
# create_task("user_001", "Gerar endpoints para autenticação", priority=5, capacity="1.2")
