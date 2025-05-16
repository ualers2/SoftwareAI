# server.py
from flask import Flask, request, jsonify
from datetime import datetime
import pytz
import os
import logging
from celery import Celery
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app, db
from modules.modules import * 

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


dotenv_path = os.path.join(os.path.dirname(__file__), "Keys", "keys.env")
load_dotenv(dotenv_path=dotenv_path)

firebase_json_path = os.getenv("firebase_json_path")
firebase_db_url = os.getenv("firebase_db_url")



# --- Inicialização Celery ---
celery_app = Celery('scheduler',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)
celery_app.conf.timezone = 'America/Sao_Paulo'
celery_app.conf.enable_utc = False

# --- Initialize Firebase ---
cred = credentials.Certificate(firebase_json_path)
appcompanyx = initialize_app(cred, {
    'databaseURL': firebase_db_url
},name="appcompanyx")

# import tasks

# --- Flask API ---
api = Flask(__name__, static_folder='static', template_folder='templates')
CORS(api, supports_credentials=True, resources={r"/*": {"origins": "*"}})


@api.route('/schedule-agent', methods=['POST'])
def schedule_agent():
    data = request.json
    agent_name = data['agent']
    params = data.get('params', {})
    run_at_str = data['run_at']  # ex: "2025-05-15T14:00:00"
    tz = pytz.timezone('America/Sao_Paulo')
    run_at = tz.localize(datetime.fromisoformat(run_at_str))

    # 1) persista no Firebase
    ref = db.reference(f'users/{params.get("user_email")}/tasks_user', app=appcompanyx)
    task_ref = ref.push({
        'agent': agent_name,
        'params': params,
        'scheduled_time': run_at_str,
        'status': 'SCHEDULED',
        'db_task_id': 'none',
        'celery_task_id': 'none'
    })
    task_id = task_ref.key

    params['db_task_id'] = task_id
    
    ref.update({
                "db_task_id": task_id,
            })

    # 2) envie para Celery
    result = celery_app.send_task(
        agent_name,
        args=[params],
        eta=run_at
    )

    ref.update({
                "celery_task_id": result.id,
            })

    return jsonify({
        'db_task_id': task_id,
        'celery_task_id': result.id,
        'scheduled_for': run_at_str
    }), 201

@api.route('/task-status/<user_email>/<task_id>')
def task_status(user_email, task_id):
    snapshot = db.reference(f'users/{user_email}/tasks_user/{task_id}', app=appcompanyx).get()
    if not snapshot:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(snapshot)


@api.route('/tasks/<user_email>', methods=['GET'])
def list_tasks(user_email):
    """Retorna todas as tarefas agendadas de um usuário."""
    user_email_filter = user_email.replace(".", "_")
    snapshot = db.reference(f'users/{user_email_filter}/tasks_user', app=appcompanyx).get() or {}
    tasks = []
    for key, val in snapshot.items():
        # Se val for string, tenta desserializar JSON; senão assume que já é dict
        if isinstance(val, str):
            try:
                val_dict = json.loads(val)
            except json.JSONDecodeError:
                # Se não for JSON válido, encapsula como valor bruto
                val_dict = {'raw': val}
        else:
            val_dict = val

        tasks.append({
            'id': key,
            'agent':           val_dict.get('agent'),
            'user_email':      user_email,
            'scheduled_for':   val_dict.get('scheduled_time'),
            'status':          val_dict.get('status'),
            'celery_task_id':  val_dict.get('celery_task_id'),
        })

        logger.info(f'Task loaded: {key} -> {val_dict}')

    return jsonify({'tasks': tasks}), 200

@api.route('/tasks/<user_email>/<task_id>/cancel', methods=['POST'])
def cancel_task(user_email, task_id):
    """Revoga a tarefa do Celery e atualiza o status no Firebase."""
    user_email_filter = user_email.replace(".", "_")
    ref = db.reference(f'users/{user_email_filter}/tasks_user/{task_id}', app=appcompanyx)
    task = ref.get()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    celery_id = task.get('celery_task_id')
    if celery_id:
        celery_app.control.revoke(celery_id, terminate=True)
    ref.update({'status': 'CANCELLED'})
    return jsonify({'status': 'CANCELLED'}), 200


if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5100)
