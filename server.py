# server.py
from flask import Flask, request, jsonify
from datetime import datetime
import pytz
import os
from celery import Celery
from dotenv import load_dotenv
from firebase_admin import credentials, initialize_app, db

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
appcompany = initialize_app(cred, {
    'databaseURL': firebase_db_url
},name="appcompany")


# --- Flask API ---
api = Flask(__name__)

@api.route('/schedule-agent', methods=['POST'])
def schedule_agent():
    data = request.json
    agent_name = data['agent']
    params = data.get('params', {})
    run_at_str = data['run_at']  # ex: "2025-05-15T14:00:00"
    tz = pytz.timezone('America/Sao_Paulo')
    run_at = tz.localize(datetime.fromisoformat(run_at_str))

    # 1) persista no Firebase
    ref = db.reference(f'save_tasks_users/{params.get("user_email")}')
    task_ref = ref.push({
        'agent': agent_name,
        'params': params,
        'scheduled_time': run_at_str,
        'status': 'SCHEDULED'
    })
    task_id = task_ref.key

    # 2) envie para Celery
    result = celery_app.send_task(
        f'internal_celery_worker.{agent_name}',
        args=[params],
        eta=run_at
    )

    return jsonify({
        'task_id': task_id,
        'celery_id': result.id,
        'scheduled_for': run_at_str
    }), 201

@api.route('/task-status/<user_email>/<task_id>')
def task_status(user_email, task_id):
    snapshot = db.reference(f'save_tasks_users/{user_email}/{task_id}').get()
    if not snapshot:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(snapshot)

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=5100)
