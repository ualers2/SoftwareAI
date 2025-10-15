from Models.postgreSQL import db 
from Models.postgreSQL import BackendTask, TaskStatus

def get_next_task():
    """
    Seleciona a próxima tarefa pendente baseado em prioridade
    """
    task = (
        BackendTask.query
        .filter_by(status=TaskStatus.PENDING.value)
        .order_by(BackendTask.priority.desc())
        .first()
    )
    if task:
        task.status = TaskStatus.SHEDULED.value
        db.session.commit()
    return task
