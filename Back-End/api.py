# app.py
import os
import threading
import requests
import json
import logging
from dotenv import load_dotenv
import asyncio
import stripe
from decimal import Decimal
from bson.json_util import dumps
from datetime import datetime, timedelta, timezone
import hmac
import hashlib
from flask import g, Flask, Response, request, jsonify, send_file, abort, redirect
from flask_cors import CORS
from asgiref.wsgi import WsgiToAsgi
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from Models.postgreSQL import *
from Modules.Resolvers.pr_process import process_pull_request
from Modules.Resolvers.generate_invoice_pdf import generate_invoice_pdf
from Modules.Resolvers.user_identifier import auth_user, require_user_token, resolve_user_identifier
from Modules.Geters.systemsettings import *
from Modules.Geters.user_by_access_token import get_user_by_access_token

from Models.mongoDB import ( 
                                Log,
                                AuditTrail, 
                                logs_collection, 
                                mongo_client,
                                mongo_db, 
                            ) 

from Modules.Geters.logs import get_recent_logs

from Modules.Savers.log_system_health import log_system_health
from Modules.Savers.log_action import log_action
from Modules.Resolvers.send_email import SendEmail
from Modules.Geters.user_by_email import get_user_by_email
from Modules.Geters.plans_data import get_plans_data
from Modules.Resolvers.verify_signature import verify_signature
from Agents.GitContextLayer.ai import GenerateCommitMessageAgent

diretorio_script = os.path.dirname(os.path.abspath(__file__)) 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
os.makedirs(os.path.join(diretorio_script, 'Logs'), exist_ok=True)
file_handler = logging.FileHandler(os.path.join(diretorio_script, 'Logs', 'api.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'keys.env'))


INVOICES_DIR = os.path.join(os.path.dirname(__file__), 'Invoices')
os.makedirs(INVOICES_DIR, exist_ok=True)
ADMIN_API_KEY = "apikey-Api-Landingpage-ZBQ2x5m_ae8Ubke9cI664PeCkerEp6EMHDyeriFFjq8"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
host = os.getenv('SMTP_HOST')
port = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
use_tls = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
createcheckout = os.getenv("createcheckout")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
success_url = os.getenv("success_url")
cancel_url = os.getenv("cancel_url")

APP_ID = os.getenv("GITHUB_APP_ID")
PRIVATE_KEY_PATH = os.getenv("GITHUB_PRIVATE_KEY_PATH") 
GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET") 
# PRIVATE_KEY_CONTENT = load_private_key(PRIVATE_KEY_PATH) 
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 
    'postgresql://postgres:postgres@meu_postgres2:5412/meubanco'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt = JWTManager(app)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)


if os.getenv("FLASK_ENV") == "development":
    CORS(app, origins=os.getenv("FRONTEND_ORIGINS", "*").split(","), supports_credentials=True)

db.init_app(app)



@app.route('/')
def index():
    return jsonify({
        "message": "Backend Flask - API Principal",
        "version": "3.0",
        "database": "PostgreSQL + MongoDB",
        "status": "running"
    })

@app.route('/api/public/plans-features', methods=['GET'])
@limiter.limit("5 per minute")
def public_plans_features():
    return jsonify({
        "message": "Lista pública de planos e features",
        "payload": get_plans_data()
    }), 200


@app.route('/api/plans-features', methods=['GET'])
def user_plan_limit():
    user, _, status = auth_user(logs_collection, app)
    if status != "success" or not user:
        return jsonify({"error": "Credenciais inválidas"}), 401

    plans = get_plans_data()
    plan_name = user.plan_name

    if plan_name not in plans:
        return jsonify({"error": "Plano não encontrado"}), 404

    return jsonify({
        "message": "Plano do usuário",
        "payload": plans[plan_name],
    }), 200

@app.route('/api/register', methods=['POST'])
def register():
    """
    Registro simples: cria usuário, seta senha e cria acess_token, persiste.
    """
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    expires_days = data.get("expires_days", None)  # opcional

    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Usuário já existe"}), 400
    try:
        new_user = User(email=email)
        new_user.set_password(password)
        acess_token = new_user.create_access_token_for_user(expires_days if expires_days is not None else TOKEN_DEFAULT_EXPIRES_DAYS)
        db.session.add(new_user)
        db.session.commit()
        log_action(logs_collection, 'user_registered', {'message': "Usuário criado com sucesso", 'username': email})
        
        return jsonify({
            "message": "Usuário criado com sucesso",
            "acess_token": acess_token,
            "user_id": new_user.id,
            "expires_at": new_user.expires_at.isoformat() if new_user.expires_at else None
        }), 201
    except Exception as e:
        db.session.rollback()
        log_action(logs_collection, 'register_error', {'username': email, 'message': str(e)}, level='error')
        return jsonify({'error': 'Failed to register user', 'detail': str(e)}), 500

@app.route('/api/login', methods=['GET'])
# @require_user_token(optional=True)
def login():
    try:
        email = request.args.get('email')
        password = request.args.get('password')
        user, access_token_to_return, status = auth_user(logs_collection, app, email, password)

        if status == "invalid" or not user:
            return jsonify({"error": "Credenciais inválidas"}), 401

        log_action(logs_collection, 'login_success', {'message': f"Bem-vindo, {user.email}!"}, user=user.id)
        return jsonify({
            "message": f"Bem-vindo, {user.email}!",
            "acess_token": user.acess_token,
            "user_id": user.id,
            "plan_name": user.plan_name,
            "limit_monthly_tokens": user.limit_monthly_tokens,
            "tokens_used": user.tokens_used,
            "expires_at": user.expires_at.isoformat() if user.expires_at else None
        }), 200

    except Exception as error_login:
        db.session.rollback()
        log_action(logs_collection, f'login_error {error_login}', {'message': 'Erro no login'}, level='error')
        return jsonify({"error": "Erro no login"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Verifica a saúde do sistema.
    Exige autenticação via Bearer/X-API-TOKEN.
    Usa o usuário autenticado (g.current_user).
    """
    try:

        user, _, status = auth_user( logs_collection, app)

        if status != "success" or not user:
            return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

        numeric_user_id = user.id
        
        GITHUB_TOKEN, OPENAI_API_KEY, GITHUB_SECRET, REPOSITORY_NAME = get_tokens(numeric_user_id, log_action, logs_collection, SystemSettings, db)

        health_status = {
            'status': 'ok',
            'timestamp': datetime.utcnow().isoformat(),
            'postgres_connected': False,
            'mongodb_connected': False,
            'github_token_configured': bool(GITHUB_TOKEN),
            'openai_token_configured': bool(OPENAI_API_KEY),
            'github_api_reachable': False,
            'openai_api_reachable': False
        }
        
        try:
            db.session.execute(db.text('SELECT 1'))
            health_status['postgres_connected'] = True
        except Exception as e:
            health_status['postgres_error'] = str(e)
        
        try:
            mongo_client.admin.command('ping')
            health_status['mongodb_connected'] = True
        except Exception as e:
            health_status['mongodb_error'] = str(e)
        
        if GITHUB_TOKEN:
            try:
                response = requests.get(
                    'https://api.github.com/rate_limit',
                    headers={'Authorization': f'Bearer {GITHUB_TOKEN}'},
                    timeout=5
                )
                health_status['github_api_reachable'] = response.status_code == 200
                if response.status_code == 200:
                    health_status['github_rate_limit'] = response.json()
            except Exception as e:
                health_status['github_error'] = str(e)
        
        if OPENAI_API_KEY:
            try:
                response = requests.get(
                    'https://api.openai.com/v1/models',
                    headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
                    timeout=5
                )
                if response.status_code == 200:
                    health_status['openai_api_reachable'] = response.status_code == 200
            except Exception as e:
                health_status['openai_error'] = str(e)
        

        critical_checks = [
            health_status['postgres_connected'],
            health_status['mongodb_connected']
        ]
        
        if not all(critical_checks):
            health_status['status'] = 'error'
            health_status['message'] = 'Critical services are down'
        elif not health_status['github_token_configured']:
            health_status['status'] = 'warning'
            health_status['message'] = 'GitHub token not configured'
        else:
            health_status['message'] = 'System is operating normally'
        
        try:
            health_record = SystemHealth(
                user_id=numeric_user_id,
                postgres_status=health_status['postgres_connected'],
                mongodb_status=health_status['mongodb_connected'],
                github_status=health_status['github_api_reachable'],
                openai_status=health_status['openai_api_reachable'],
                last_check=datetime.utcnow().replace(tzinfo=timezone.utc) 

            )
            db.session.add(health_record)
            db.session.commit()
        except Exception as e:
            pass  
        
        log_system_health(numeric_user_id, health_status)

        log_action(logs_collection, 'health_check', health_status, user=numeric_user_id)
        
        status_code = 200 if health_status['status'] == 'ok' else 503
        return jsonify(health_status), status_code


    except Exception as e:
        log_action(logs_collection, 'health_check_error', {'error': str(e)}, level='error')
        return jsonify({"error": "Erro ao executar health_check", "detail": str(e)}), 500

@app.route('/api/rate-limits', methods=['GET'])
def get_rate_limits():
    """Obter informações de rate limits"""
    
    

    user, _, status = auth_user( logs_collection, app)

    if status != "success" or not user:
        return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

    numeric_user_id = user.id
    
    fixed_ratelimiting = {
                'note': 'API está sujeito a limites de taxa aplicados a tokens por minuto (TPM), solicitações por minuto ou dia (RPM/RPD) ',
                'TPM': '200.000',
                'RPM': '500',
                'RPD': '2.000.000',
                'model': 'gpt-5-nano'
            }

    rate_limits = {
        'github': None,
        'openai': fixed_ratelimiting,
        'timestamp': datetime.utcnow().isoformat()
    }

    GITHUB_TOKEN, OPENAI_API_KEY, GITHUB_SECRET, REPOSITORY_NAME = get_tokens(numeric_user_id, log_action, logs_collection, SystemSettings, db)
    
    # GitHub Rate Limits
    if GITHUB_TOKEN:
        try:
            response = requests.get(
                'https://api.github.com/rate_limit',
                headers={'Authorization': f'Bearer {GITHUB_TOKEN}'},
                timeout=10
            )
            if response.status_code == 200:
                github_data = response.json()
                rate_limits['github'] = {
                    'limit': github_data['rate']['limit'],
                    'remaining': github_data['rate']['remaining'],
                    'reset': github_data['rate']['reset'],
                    'reset_datetime': datetime.fromtimestamp(github_data['rate']['reset']).isoformat()
                }
        except Exception as e:
            rate_limits['github'] = {'error': str(e)}
    
    # OpenAI Rate Limits
    if OPENAI_API_KEY:
        try:

            rate_limits['openai'] = fixed_ratelimiting
        except Exception as e:
            rate_limits['openai'] = {'error': str(e)}
    
    log_action(logs_collection, 'rate_limits_checked', rate_limits, user=numeric_user_id)
    
    return jsonify(rate_limits)

@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Recuperar configurações do sistema (com valores mascarados)"""
    email = request.args.get("email")  
    password = request.args.get("password")  
    

    user, _, status = auth_user( logs_collection, app, email, password)

    if status != "success" or not user:
        return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

    numeric_user_id = user.id
    
    
    try:
        settings = SystemSettings.query.filter_by(user_id=numeric_user_id).first()

        if not settings:
            settings = SystemSettings(
                user_id=numeric_user_id,
            )
            db.session.add(settings)
            db.session.commit()
        
        response_data = {
            'githubToken': settings.github_token,
            'githubSecret': settings.github_secret,
            'repositoryName': settings.repository_name or '',
            'openaiApiKey': settings.openai_api_key,
            'webhookUrl': settings.webhook_url or '',
            'autoProcessPRs': settings.auto_process_prs,
            'enableLogging': settings.enable_logging,
            'logLevel': settings.log_level or 'INFO'
        }
        
        log_action(logs_collection, 'settings_accessed', {
            'status': 'sucess', 
            'repository_name': settings.repository_name,
            'log_level': settings.log_level or 'INFO'
            }, user=numeric_user_id)
        
        return jsonify(response_data)
        
    except Exception as e:
        log_action(logs_collection, 'settings_access_error', {'error': str(e)}, user=numeric_user_id, level='error')
        return jsonify({'error': 'Failed to fetch settings'}), 500

@app.route('/api/settings', methods=['PUT'])
def update_settings():
    """Atualizar configurações do sistema"""
    data = request.get_json()
    email = data.get("email")  
    password = data.get("password")  
    

    user, _, status = auth_user( logs_collection, app, email, password)

    if status != "success" or not user:
        return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

    numeric_user_id = user.id
    try:

        settings = SystemSettings.query.filter_by(user_id=numeric_user_id).first()

        if not settings:
            settings = SystemSettings(
                user_id=numeric_user_id,
            )
            db.session.add(settings)

        settings.github_token = data.get('githubToken')
        settings.github_secret = data.get('githubSecret')
        settings.repository_name = data.get('repositoryName')
        settings.openai_api_key = data.get('openaiApiKey')
        settings.webhook_url = data.get('webhookUrl')
        settings.auto_process_prs = data.get('autoProcessPRs')
        settings.enable_logging = data.get('enableLogging')
        settings.log_level = data.get('logLevel')
        
        settings.updated_at = datetime.utcnow()
        db.session.commit()
        
        log_action(logs_collection, 'settings_updated', {
            'status': 'sucess',
            'updated_fields': list(data.keys()),
            'repository_name': settings.repository_name,
            'log_level': settings.log_level
        }, user=numeric_user_id)
        
        return jsonify({
            'status': 'success',
            'message': 'Settings updated successfully'
        })
        
    except Exception as e:
        db.session.rollback()
        log_action(logs_collection, 'settings_update_error', {'error': str(e)}, user=numeric_user_id, level='error')
        return jsonify({'error': 'Failed to update settings'}), 500

@app.route('/api/test-connection/<service>', methods=['GET'])
def test_connection(service):
    """Testar conexão com serviços externos"""


    user, _, status = auth_user( logs_collection, app)

    if status != "success" or not user:
        return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

    numeric_user_id = user.id
    try:
        settings = SystemSettings.query.filter_by(user_id=numeric_user_id).first()

        
        if service == 'github':
            if not settings or not settings.github_token:
                log_action(logs_collection, 'settings_github_token_error', {
                    'status': 'error',
                    'message': f'GitHub token not configured'
                }, user=numeric_user_id)
                
                return jsonify({
                    'status': 'error',
                    'message': 'GitHub token not configured'
                }), 400
            
            # 
            response = requests.get(
                'https://api.github.com/user',
                headers={'Authorization': f'Bearer {settings.github_token}'},
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
         
                log_action(logs_collection, 'github_connection_test_success', {
                    'status': 'success',
                    'service': service,
                    'message': f'Only Success'
                }, user=numeric_user_id)
                
                return jsonify({
                    'status': 'success',
                    'message': f'GitHub connection OK. Authenticated as: {user_data.get("login")}'
                })
            else:
                log_action(logs_collection, 'github_connection_test_error', {
                    'status': 'error',
                    'service': service,
                    'message': f'GitHub API error: {response.status_code} - {response.text}'
                }, user=numeric_user_id)
                
                return jsonify({
                    'status': 'error',
                    'message': f'GitHub API error: {response.status_code} - {response.text[:100]}'
                }), 400
        
        elif service == 'openai':
            if not settings or not settings.openai_api_key:
                log_action(logs_collection, 'settings_openai_api_key_error', {
                    'status': 'error',
                    'service': service,
                    'message': f'OpenAI API key not configured'
                }, user=numeric_user_id)
                
                return jsonify({
                    'status': 'error',
                    'message': 'OpenAI API key not configured'
                }), 400
            
            response = requests.get(
                'https://api.openai.com/v1/models',
                headers={'Authorization': f'Bearer {settings.openai_api_key}'},
                timeout=10
            )
            
            if response.status_code == 200:
                log_action(logs_collection, 'openai_connection_test_success', {
                    'status': 'success',
                    'service': service,
                    'message': f'OpenAI API connection OK'
                }, user=numeric_user_id)

                return jsonify({
                    'status': 'success',
                    'message': 'OpenAI API connection OK'
                })
            else:
                log_action(logs_collection, 'settings_openai_test_error', {
                    'status': 'error',
                    'service': service,
                    'message': f'OpenAI API error: {response.status_code} - {response.text}'
                }, user=numeric_user_id)
                
                return jsonify({
                    'status': 'error',
                    'message': f'OpenAI API error: {response.status_code} - {response.text[:100]}'
                }), 400
    
    except requests.RequestException as e:
        log_action(logs_collection, 'connection_test_error', {
            'status': 'error',
            'service': service,
            'message': str(e)
        }, user=numeric_user_id, level='error')
        
        return jsonify({
            'status': 'error',
            'message': f'Connection failed: {str(e)}'
        }), 500
    
    except Exception as e:
        log_action(logs_collection, 'connection_test_error', {
            'status': 'error',
            'service': service,
            'message': str(e)
        }, user=numeric_user_id, level='error')
        
        return jsonify({
            'status': 'error',
            'message': f'Unexpected error: {str(e)}'
        }), 500

@app.route("/api/logs", methods=["GET"])
def get_logs():
    
    
    level = request.args.get("level")
    search_term = request.args.get("searchTerm")
    limit = int(request.args.get("limit", 200))

    user, _, status = auth_user( logs_collection, app)

    if status != "success" or not user:
        return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

    numeric_user_id = user.id

    query = {"$or": [{"user_id": numeric_user_id}, {"user": numeric_user_id}]}

    if level and level != "all":
        query["level"] = level.upper()
    if search_term:
        # procura em details.message ou em action
        query["$or"] = query.get("$or", []) + [
            {"details.message": {"$regex": search_term, "$options": "i"}},
            {"action": {"$regex": search_term, "$options": "i"}}
        ]

    raw_logs = list(logs_collection.find(query).sort("timestamp", -1).limit(limit))

    # Adaptar para o frontend (serializar datetime -> ISO)
    adapted_logs = []
    for log in raw_logs:
        ts = log.get("timestamp")
        if hasattr(ts, "isoformat"):
            ts_iso = ts.isoformat()
        else:
            ts_iso = str(ts)
        adapted_logs.append({
            "id": str(log.get("_id")),
            "timestamp": ts_iso,
            "level": log.get("level"),
            "action": log.get("action"),
            "details": log.get("details", {}),  # Mantém dict
            "prNumber": log.get("prNumber") or (log.get("details", {}) or {}).get("pr_number") or (log.get("details", {}) or {}).get("prNumber"),
            "user": log.get("user"),
            "user_id": log.get("user_id")
        })

    return jsonify(adapted_logs)

@app.route("/api/logs/export", methods=["GET"])
def export_logs():
    """
    Exporta logs filtrados em formato .txt
    Requer `user_id` (query param).
    """
    
    
    level = request.args.get("level")
    search_term = request.args.get("searchTerm")

    user, _, status = auth_user( logs_collection, app)

    if status != "success" or not user:
        return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

    numeric_user_id = user.id

    query = {"$or": [{"user_id": numeric_user_id}, {"user": numeric_user_id}]}

    if level:
        query["level"] = level.upper()

    if search_term:
        query = {
            "$and": [
                query,
                {
                    "$or": [
                        {"details.message": {"$regex": search_term, "$options": "i"}},
                        {"action": {"$regex": search_term, "$options": "i"}}
                    ]
                }
            ]
        }
    logs = list(logs_collection.find(query).sort("timestamp", -1))

    # Gera conteúdo TXT
    export_content = []
    for log in logs:
        message = log.get("details", {}).get("message", "")
        ts = log.get("timestamp")
        if hasattr(ts, "isoformat"):
            ts_str = ts.isoformat()
        else:
            ts_str = str(ts)
        line = f"[{ts_str}] {log.get('level')} - {message} (User: {log.get('user')})"
                
        if log.get("prNumber"):
            line += f" | PR #{log['prNumber']}"
        export_content.append(line)

    export_text = "\n".join(export_content)

    return Response(
        export_text,
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment; filename=logs-{numeric_user_id}.txt"},
    )

@app.route('/api/pull-requests', methods=['GET'])
def get_pull_requests():
    """Listar PRs processados com filtros e busca"""
    
    
    page = request.args.get("page", 1)
    search_term = request.args.get("searchTerm", None)
    limit = int(request.args.get("limit", 50))

    user, _, status = auth_user( logs_collection, app)

    if status != "success" or not user:
        return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

    numeric_user_id = user.id
    
    GITHUB_TOKEN, OPENAI_API_KEY, GITHUB_SECRET, REPOSITORY_NAME = get_tokens(numeric_user_id, log_action, logs_collection, SystemSettings, db)
    

    try:
        query = PullRequest.query.filter_by(user_id=numeric_user_id)

        # Filtrar por termo de busca se fornecido
        if search_term:
            query = query.filter(
                db.or_(
                    PullRequest.title.ilike(f'%{search_term}%'),
                    PullRequest.pr_number == int(search_term) if search_term.isdigit() else False,
                    PullRequest.processed_by.ilike(f'%{search_term}%')
                )
            )
        
        # Paginação
        prs = query.order_by(PullRequest.updated_at.desc()).paginate(
            page=page, per_page=limit, error_out=False
        )
        
        # Formatar para o frontend
        formatted_prs = []
        for pr in prs.items:
    
            author = pr.author
            ai_generated_content = pr.ai_generated_content
            original_diff = pr.original_diff
            error_message = pr.error_message  
            
            formatted_prs.append({
                'id': str(pr.id),
                'number': pr.pr_number,
                'title': pr.title,
                'status': pr.status,
                'processedAt': pr.updated_at.isoformat(),
                'githubUrl': f'https://github.com/{REPOSITORY_NAME}/pull/{pr.pr_number}',
                'author': author,
                'aiGeneratedContent': ai_generated_content,
                'originalDiff': original_diff,
                'total_tokens': pr.total_tokens,
                'errorMessage': error_message if pr.status == 'error' else None
            })
        
        log_action(logs_collection, 'prs_listed', {
            'search_term': search_term,
            'page': page,
            'limit': limit,
            'total_found': prs.total
        }, user=numeric_user_id)
        
        return jsonify(formatted_prs)
        
    except Exception as e:
        log_action(logs_collection, 'prs_list_error', {'error': str(e)}, user=numeric_user_id, level='error')
        return jsonify({'error': 'Failed to fetch pull requests'}), 500

@app.route('/api/pull-requests/<pr_id>', methods=['GET'])
def get_pull_request_details(pr_id):
    """Obter detalhes completos de um PR específico"""
    
    

    user, _, status = auth_user( logs_collection, app)

    if status != "success" or not user:
        return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

    numeric_user_id = user.id

    GITHUB_TOKEN, OPENAI_API_KEY, GITHUB_SECRET, REPOSITORY_NAME = get_tokens(numeric_user_id, log_action, logs_collection, SystemSettings, db)
    
    try:
        pr = PullRequest.query.filter_by(id=pr_id, user_id=numeric_user_id).first_or_404()

                
        # Buscar dados do GitHub se necessário
        github_url = f'https://github.com/{REPOSITORY_NAME}/pull/{pr.pr_number}'
        api_github_url = f'https://api.github.com/repos/{REPOSITORY_NAME}/pulls/{pr.pr_number}'
        author = pr.author
        ai_generated_content = pr.body or pr.ai_generated_content
        original_diff = pr.original_diff
        
        if GITHUB_TOKEN:
            try:
                response = requests.get(
                    api_github_url,
                    headers={'Authorization': f'Bearer {GITHUB_TOKEN}'},
                    timeout=10
                )
                if response.status_code == 200:
                    pr_data = response.json()
                    author = pr_data.get('user', {}).get('login', 'unknown')
                    
                    # Buscar diff
                    diff_response = requests.get(pr.diff_url or pr_data.get('diff_url', ''))
                    if diff_response.status_code == 200:
                        original_diff = diff_response.text
            except Exception as e:
                log_action(logs_collection, 'pr_details_github_error', {
                    'pr_number': pr.pr_number,
                    'error': str(e)
                }, user=numeric_user_id, level='warning')
        
        pr_details = {
            'id': str(pr.id),
            'number': pr.pr_number,
            'title': pr.title,
            'status': pr.status,
            'processedAt': pr.updated_at.isoformat(),
            'githubUrl': github_url,
            'author': author,
            'aiGeneratedContent': ai_generated_content,
            'originalDiff': original_diff,
            'total_tokens': pr.total_tokens,
            'errorMessage': None if pr.status != 'error' else f'Error processing PR #{pr.pr_number}'
        }
        
        log_action(logs_collection, 'pr_details_accessed', {
            'pr_id': pr_id,
            'pr_number': pr.pr_number
        }, user=numeric_user_id)
        
        return jsonify(pr_details)
        
    except Exception as e:
        log_action(logs_collection, 'pr_details_error', {
            'pr_id': pr_id,
            'error': str(e)
        }, user=numeric_user_id, level='error')
        return jsonify({'error': 'Failed to fetch PR details'}), 500

def parse_to_aware(dt):
    """
    Recebe dt (datetime | str | None) e retorna um datetime c/ tzinfo=UTC.
    Retorna None se não puder interpretar.
    """
    if dt is None:
        return None

    # se for string, tenta parse ISO (aceita "Z" e offsets)
    if isinstance(dt, str):
        s = dt.strip()
        # Normaliza "Z" -> +00:00 para fromisoformat
        if s.endswith('Z'):
            s = s[:-1] + '+00:00'
        try:
            parsed = datetime.fromisoformat(s)
        except Exception:
            # fallback curto para strings sem microssegundos (ex: 2025-09-23T20:17:26)
            try:
                parsed = datetime.strptime(s, "%Y-%m-%dT%H:%M:%S")
            except Exception:
                return None
        dt = parsed

    # se for datetime, garante timezone UTC
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        # converte qualquer timezone para UTC
        return dt.astimezone(timezone.utc)

    return None

@app.route('/api/dashboard-data', methods=['GET'])
#  
def get_dashboard_data():
    """Obter dados agregados para o dashboard (correção focada: apenas aqui)."""

    user, _, status = auth_user( logs_collection, app)
    if status != "success" or not user:
        return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

    numeric_user_id = user.id

    try:
        # --- Estatísticas dos PRs (mesma lógica que já tinha) ---
        total_prs = PullRequest.query.filter_by(user_id=numeric_user_id).count()
        successful_prs = PullRequest.query.filter_by(user_id=numeric_user_id, status='completed').count()
        failed_prs = PullRequest.query.filter_by(user_id=numeric_user_id, status='error').count()
        pending_prs = PullRequest.query.filter_by(user_id=numeric_user_id, status='processing').count()

        # --- Uptime / último SystemHealth (tratando datetimes inconsistentes) ---
        latest_health = SystemHealth.query.filter_by(user_id=numeric_user_id).order_by(SystemHealth.last_check.desc()).first()
        uptime = "N/A"
        if latest_health and latest_health.last_check:
            latest_check = parse_to_aware(latest_health.last_check)
            if latest_check:
                now_utc = datetime.now(timezone.utc)
                uptime_delta = now_utc - latest_check
                days = uptime_delta.days
                hours, remainder = divmod(uptime_delta.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                uptime = f"{days}d {hours}h {minutes}m"

        # --- Recuperar atividades recentes diretamente do Mongo (apenas para o dashboard) ---
        recent_activities = []
        try:
            # filtro compatível com logs que usam "user_id" ou "user"
            query = {"$or": [{"user_id": numeric_user_id}, {"user": numeric_user_id}]}
            raw_logs = list(logs_collection.find(query).sort("timestamp", -1).limit(10))
        except Exception as e:
            raw_logs = []
            # registrar erro sem interferir no retorno
            log_action(logs_collection, 'dashboard_logs_query_error', {'error': str(e)}, user=numeric_user_id, level='warning')

        # calcula lastActivity (a partir do primeiro log mais recente)
        last_activity = "N/A"
        if raw_logs:
            first_ts = raw_logs[0].get('timestamp')
            first_ts_aware = parse_to_aware(first_ts) if first_ts is not None else None
            if first_ts_aware:
                now_utc = datetime.now(timezone.utc)
                diff = now_utc - first_ts_aware
                if diff.total_seconds() < 60:
                    last_activity = f"{int(diff.total_seconds())} segundos atrás"
                elif diff.total_seconds() < 3600:
                    last_activity = f"{int(diff.total_seconds() // 60)} minutos atrás"
                else:
                    last_activity = f"{int(diff.total_seconds() // 3600)} horas atrás"

        # montar lista de atividades legíveis
        for i, log_entry in enumerate(raw_logs):
            timestamp_raw = log_entry.get('timestamp')
            timestamp = parse_to_aware(timestamp_raw) if timestamp_raw is not None else None

            # fallback: se timestamp inválido, usar agora (UTC)
            if not timestamp:
                timestamp = datetime.now(timezone.utc)

            now_utc = datetime.now(timezone.utc)
            time_diff = now_utc - timestamp
            secs = int(time_diff.total_seconds())

            if secs < 60:
                time_ago = f"{secs} seg atrás"
            elif secs < 3600:
                time_ago = f"{secs // 60} min atrás"
            elif secs < 86400:
                time_ago = f"{secs // 3600}h atrás"
            else:
                time_ago = f"{secs // 86400}d atrás"

            # extrair mensagem com segurança
            details = log_entry.get('details') or {}
            message = details.get('message') or log_entry.get('action') or 'Atividade do sistema'

            # status (normalizar para front)
            lvl = (log_entry.get('level') or 'info').lower()
            if lvl not in ('info', 'warning', 'error', 'success'):
                lvl = 'info'

            recent_activities.append({
                'id': str(log_entry.get('_id', i)),
                'type': log_entry.get('action', 'unknown'),
                'message': message,
                'timestamp': time_ago,
                'status': lvl
            })

        tokens_used = user.tokens_used or 0
        limit_tokens = user.limit_monthly_tokens or 0

        percent_used = 0
        if limit_tokens > 0:
            percent_used = round((tokens_used / limit_tokens) * 100, 1)

        expires_at_str = "N/A"
        days_left = None
        if user.expires_at:
            now_utc = datetime.now(timezone.utc)
            expires_utc = parse_to_aware(user.expires_at)
            if expires_utc:
                diff = expires_utc - now_utc
                days_left = max(diff.days, 0)
                expires_at_str = expires_utc.strftime("%d/%m/%Y %H:%M")

        dashboard_data = {
            'stats': {
                'totalPRs': total_prs,
                'successfulPRs': successful_prs,
                'failedPRs': failed_prs,
                'pendingPRs': pending_prs,
                'uptime': uptime,
                'lastActivity': last_activity,
                'tokensUsed': tokens_used,
                'tokenLimit': limit_tokens,
                'tokenPercentUsed': percent_used,
                'planName': user.plan_name,
                'planExpiresAt': expires_at_str,
                'planDaysLeft': days_left
            },
            'recentActivity': recent_activities
        }

        # registrar acesso ao dashboard (mantém comportamento existente)
        log_action(logs_collection, 'dashboard_accessed', {'user': numeric_user_id}, user=numeric_user_id)
        print(dashboard_data)
        return jsonify(dashboard_data)

    except Exception as e:
        # registra o erro e retorna 500
        log_action(logs_collection, 'dashboard_error', {'error': str(e)}, user=numeric_user_id, level='error')
        return jsonify({'error': 'Failed to fetch dashboard data'}), 500


@app.route('/api/workflows', methods=['GET'])

def list_workflows():
    """
    Lista workflows (arquivos .yml/.yaml) a partir de WORKFLOWS_PATH (env) ou ./workflows.
    Retorna JSON: { "workflows": [ { id, name, category, createdAt, yaml, git }, ... ] }
    """
    try:
        
        

        user, _, status = auth_user( logs_collection, app)
        if status != "success" or not user:
            return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

        numeric_user_id = user.id

        # diretório de workflows 
        workflows_dir = os.path.join(os.path.dirname(__file__), 'Workflows')


        workflows = []

        if os.path.isdir(workflows_dir):
            for root, _, files in os.walk(workflows_dir):
                for fname in files:
                    if fname.lower().endswith(('.yml', '.yaml')):
                        path = os.path.join(root, fname)
                        try:
                            with open(path, 'r', encoding='utf-8') as f:
                                content = f.read()
                            stat = os.stat(path)
                            created = datetime.utcfromtimestamp(stat.st_mtime).isoformat() + 'Z'
                            rel_id = os.path.relpath(path, workflows_dir).replace('\\', '/')
                            category = os.path.relpath(root, workflows_dir)
                            if category == '.':
                                category = ''
                            wf = {
                                'id': rel_id,
                                'name': os.path.splitext(fname)[0],
                                'category': category,
                                'createdAt': created,
                                'yaml': content,
                            }
                            workflows.append(wf)
                        except Exception as e:
                            log_action(logs_collection, 'workflow_read_error', {'file': path, 'error': str(e)}, user=numeric_user_id, level='error')
        else:
            # Se o diretório não existe, retorna lista vazia (com log)
            log_action(logs_collection, 'workflows_dir_missing', {'path': workflows_dir}, user=numeric_user_id)

        log_action(logs_collection, 'workflows_listed', {'count': len(workflows)}, user=numeric_user_id)
        return jsonify({'workflows': workflows}), 200

    except Exception as e:
        log_action(logs_collection, 'workflows_list_error', {'error': str(e)}, user=(getattr(g, 'current_user', None) or None), level='error')
        return jsonify({'error': 'Failed to list workflows', 'detail': str(e)}), 500

@app.route('/api/myaccount', methods=['GET'])

def my_account():
    """
    Retorna informações da conta do usuário autenticado.
    Inclui plano, limites e status de expiração.
    """
    try:
        user, _, status = auth_user( logs_collection, app)
        if status != "success" or not user:
            return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

        numeric_user_id = user.id
        response = {
            "user_id": user.id,
            "email": user.email,
            "planName": user.plan_name,
            "planExpiresAt": user.expires_at.isoformat() if user.expires_at else None,
            "tokensUsed": user.tokens_used or 0,
            "tokenLimit": user.limit_monthly_tokens or 0,
            "remainingTokens": (user.limit_monthly_tokens or 0) - (user.tokens_used or 0),
            "accessToken": user.acess_token,
            "createdAt": user.created_at.isoformat() if user.created_at else None,
        }

        log_action(logs_collection, 'myaccount_accessed', response, user=user.id)
        return jsonify(response), 200

    except Exception as e:
        log_action(logs_collection, 'myaccount_error', {'error': str(e)}, level='error')
        return jsonify({"error": "Erro ao recuperar informações da conta", "detail": str(e)}), 500


@app.route('/api/invoices', methods=['GET'])

def list_invoices():
    """
    Listar faturas paginadas.
    Query params: page, limit, status, q, email, password (compatibilidade com auth_user)
    Retorna: { invoices: [...], total: N }
    """
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 12))
        status = request.args.get('status')
        q = request.args.get('q', '').strip()

        # autentica (compatível com existing pattern)
        
        
        user, _, status_auth = auth_user( logs_collection, app)

        if status_auth != "success" or not user:
            return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

        numeric_user_id = user.id

        query = Invoice.query.filter_by(user_id=numeric_user_id)

        if status:
            query = query.filter(Invoice.status == status)

        if q:
            like = f"%{q}%"
            query = query.filter(db.or_(Invoice.number.ilike(like), Invoice.plan_name.ilike(like)))

        total = query.count()

        invoices_page = query.order_by(Invoice.date.desc()).offset((page - 1) * limit).limit(limit).all()

        invoices_data = [inv.to_dict(include_lines=False) for inv in invoices_page]

        log_action(logs_collection, 'invoices_listed', {'count': len(invoices_data), 'page': page}, user=numeric_user_id)
        return jsonify({"invoices": invoices_data, "total": total})
    except Exception as e:
        log_action(logs_collection, 'invoices_list_error', {'error': str(e)}, user=(getattr(g, 'current_user', None) or None), level='error')
        return jsonify({'error': 'Failed to list invoices', 'detail': str(e)}), 500


@app.route('/api/invoices/<int:invoice_id>', methods=['GET'])

def get_invoice_detail(invoice_id):
    """
    Detalhe da fatura (inclui linhas / itens).
    """
    try:
        
        
        user, _, status_auth = auth_user( logs_collection, app)

        if status_auth != "success" or not user:
            return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

        numeric_user_id = user.id

        inv = Invoice.query.filter_by(id=invoice_id, user_id=numeric_user_id).first()
        if not inv:
            return jsonify({'error': 'Invoice not found'}), 404

        inv_data = inv.to_dict(include_lines=True)

        log_action(logs_collection, 'invoice_detail_accessed', {'invoice_id': invoice_id}, user=numeric_user_id)
        return jsonify(inv_data)
    except Exception as e:
        log_action(logs_collection, 'invoice_detail_error', {'error': str(e), 'invoice_id': invoice_id}, user=(getattr(g, 'current_user', None) or None), level='error')
        return jsonify({'error': 'Failed to fetch invoice detail', 'detail': str(e)}), 500


@app.route('/api/invoices/<int:invoice_id>/download', methods=['GET'])

def download_invoice(invoice_id):
    """
    Download do PDF da fatura.
    Se Invoice.pdf_url estiver setado como URL externa, redireciona para ela.
    Se Invoice.pdf_path estiver configurado, serve o arquivo do diretório INVOICES_DIR.
    """
    try:
        
        
        user, _, status_auth = auth_user( logs_collection, app)

        if status_auth != "success" or not user:
            return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

        numeric_user_id = user.id

        inv = Invoice.query.filter_by(id=invoice_id, user_id=numeric_user_id).first()
        if not inv:
            return jsonify({'error': 'Invoice not found'}), 404

        # Prioriza URL externa
        if inv.pdf_url:
            log_action(logs_collection, 'invoice_download_redirect', {'invoice_id': invoice_id, 'url': inv.pdf_url}, user=numeric_user_id)
            return jsonify({'pdfUrl': inv.pdf_url}), 200

        # Se tiver path relativo, tenta servir o arquivo
        if inv.pdf_path:
            # garante que não escape o diretório
            file_path = os.path.join(INVOICES_DIR, inv.pdf_path)
            if not os.path.exists(file_path):
                log_action(logs_collection, 'invoice_download_missing_file', {'invoice_id': invoice_id, 'path': file_path}, user=numeric_user_id, level='warning')
                return jsonify({'error': 'Arquivo de fatura não encontrado no servidor'}), 404

            # usa send_file com attachment_filename (flask >=2)
            try:
                log_action(logs_collection, 'invoice_download_served', {'invoice_id': invoice_id, 'file': inv.pdf_path}, user=numeric_user_id)
                return send_file(file_path, mimetype='application/pdf', as_attachment=True, download_name=f"invoice-{inv.number}.pdf")
            except Exception as e:
                log_action(logs_collection, 'invoice_download_error', {'invoice_id': invoice_id, 'error': str(e)}, user=numeric_user_id, level='error')
                return jsonify({'error': 'Erro ao servir arquivo de fatura', 'detail': str(e)}), 500

        # nenhum arquivo nem url configurado
        return jsonify({'error': 'Nenhum arquivo de fatura disponível'}), 404

    except Exception as e:
        log_action(logs_collection, 'invoice_download_exception', {'error': str(e), 'invoice_id': invoice_id}, user=(getattr(g, 'current_user', None) or None), level='error')
        return jsonify({'error': 'Failed to download invoice', 'detail': str(e)}), 500



@app.route('/api/reprocess-pr/<int:pr_number>', methods=['POST'])
 
def reprocess_pr(pr_number):
    """Reprocessar um Pull Request específico"""
    data = request.get_json()
    redo_merge = data.get("redo_merge") 

    user, _, status = auth_user( logs_collection, app)

    if status != "success" or not user:
        return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

    numeric_user_id = user.id

    model = "gpt-5-nano"
    GITHUB_TOKEN, OPENAI_API_KEY, GITHUB_SECRET, REPOSITORY_NAME = get_tokens(numeric_user_id, log_action, logs_collection, SystemSettings, db)
    thread = threading.Thread(target=process_pull_request, args=(
                                                    app,
                                                    numeric_user_id, 
                                                    GITHUB_TOKEN, 
                                                    OPENAI_API_KEY, 
                                                    logs_collection,
                                                    pr_number,
                                                    REPOSITORY_NAME, 
                                                    model, 
                                                    redo_merge,
                                                    ))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'message': 'Processing started',
        'pr_number': pr_number,
        'triggered_by': numeric_user_id
    }), 202

@app.route('/api/prai/gen', methods=['POST']) 
def prai():
    data = request.get_json()
    repository = data.get("repository")
    pr_number = data.get("pr_number")

    user, _, status = auth_user( logs_collection, app)

    if status != "success" or not user:
        return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

    numeric_user_id = user.id
    model = "gpt-5-nano"
    GITHUB_TOKEN, _, GITHUB_SECRET, REPOSITORY_NAME = get_tokens(numeric_user_id, log_action, logs_collection, SystemSettings, db)

    threading.Thread(target=process_pull_request, args=(
                                                    app,
                                                    numeric_user_id, 
                                                    GITHUB_TOKEN, 
                                                    OPENAI_API_KEY, 
                                                    logs_collection,
                                                    pr_number,
                                                    repository, 
                                                    model, 
                                                    )).start()

    return jsonify({
        'message': 'Processing started',
        'pr_number': pr_number,
        'triggered_by': numeric_user_id
    }), 202




@app.route('/api/prai/diff_context', methods=['POST']) 
def diff_context():
    data = request.get_json()
    diff = data.get("diff")
    files = data.get("files")
    user, _, status = auth_user( logs_collection, app)

    if status != "success" or not user:
        return jsonify({"error": "Usuário não autenticado ou inválido"}), 401

    numeric_user_id = user.id
    model = "gpt-5-nano"
    GITHUB_TOKEN, _, GITHUB_SECRET, REPOSITORY_NAME = get_tokens(numeric_user_id, log_action, logs_collection, SystemSettings, db)

    commit_output, total_input, total_cached, total_output, total_reasoning, total_usage = asyncio.run(GenerateCommitMessageAgent(
                            OPENAI_API_KEY,
                            numeric_user_id, 
                            diff, 
                            files, 
                    
                            ))
    commit_message = f"{commit_output.subject}\n\n{commit_output.body}"
    
    return jsonify({
        'commit_message': f'{commit_message}',
        'tokens': {
            'total_input': total_input,
            'total_cached': total_cached,
            'total_output': total_output,
            'total_reasoning': total_reasoning,
            'total_usage': total_usage,
        },
        'triggered_by': numeric_user_id
    }), 202





@app.route("/api/billing/checkout", methods=["POST"])
def create_checkout():
    data = request.get_json()
    try:
       
        plan = data["plan"]
        billingCycle = data["billingCycle"]
        if billingCycle == "monthly":
            if plan == "Premium":
                SUBSCRIPTION_PRICE_ID = os.getenv("STRIPE_SUBSCRIPTION_PRICE_ID_Premium")
            elif plan == "Pro":
                SUBSCRIPTION_PRICE_ID = os.getenv("STRIPE_SUBSCRIPTION_PRICE_ID_Pro")
        
        elif billingCycle == "annual":
            if plan == "Premium":
                SUBSCRIPTION_PRICE_ID = os.getenv("STRIPE_SUBSCRIPTION_PRICE_ID_Premium_anual")
            elif plan == "Pro":
                SUBSCRIPTION_PRICE_ID = os.getenv("STRIPE_SUBSCRIPTION_PRICE_ID_Pro_anual")

        session = stripe.checkout.Session.create(
            line_items=[{
                "price": SUBSCRIPTION_PRICE_ID,  
                "quantity": 1
            }],
            mode="subscription",
            payment_method_types=["card"],
            success_url=success_url, 
            cancel_url=cancel_url,  
            metadata={"email": data["email"],
                      "password": data["password"],
                      "SUBSCRIPTION_PLAN": data["plan"],
                    },
        )
        print("Sessão criada:", session.id)
        return jsonify({"sessionId": session.id})
    except Exception as e:
        print("Erro ao criar a sessão de checkout:", e)
        return jsonify({"error": str(e)}), 500

@app.route('/proxy-checkout', methods=['POST'])
def proxy_checkout():
    try:
        data = request.get_json()
        headers = {
            "Content-Type": "application/json",
            "Api-Landingpage-API-KEY": ADMIN_API_KEY
        }
        response = requests.post(createcheckout, json=data, headers=headers)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        logger.info(f"Erro no servidor {e}")
        return jsonify({"error": f"Erro no servidor {e}"}), 500

@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    """
    Endpoint para tratar os webhooks enviados pela Stripe.
    """
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except ValueError as e:
        return jsonify({"message": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({"message": "Invalid signature"}), 400

    # Processa o evento conforme o seu tipo
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        email_metadata = session["metadata"].get("email")
        password_metadata = session["metadata"].get("password")
        SUBSCRIPTION_PLAN = session["metadata"].get("SUBSCRIPTION_PLAN")
            
        user = get_user_by_email(email_metadata)
        if not user: 
            new_user = User(email=email_metadata)
            new_user.set_password(password_metadata)
            acess_token = new_user.create_access_token_for_user(TOKEN_DEFAULT_EXPIRES_DAYS)
            db.session.add(new_user)
            db.session.commit()
            log_action(logs_collection, 'user_registered', {'message': "Usuário criado com sucesso"})
            numeric_user_id = user.id
        else:
            numeric_user_id = user.id
                
        if session.get("payment_status") == "paid":

            log_action(logs_collection, 
                'payment_system',
                {'message': f"Pagamento por cartão com sucesso: {SUBSCRIPTION_PLAN} {email_metadata}"},
                user=numeric_user_id
                )

            plans = get_plans_data()
            payload  =  plans[SUBSCRIPTION_PLAN]
            user.limit_monthly_tokens = payload.get('limit_monthly_tokens')
            user.tokens_used = 0
            user.plan_name = SUBSCRIPTION_PLAN
            user.expires_at  = datetime.utcnow() + timedelta(days=30)
            user.revoked_at = None
            invoice = Invoice(
                user_id=numeric_user_id,
                number=f"INV-{int(datetime.utcnow().timestamp())}",  # um número único simples
                date=datetime.utcnow(),
                amount=Decimal(payload.get('price', 0.0)), 
                currency='USD',
                status='paid',
                plan_name=SUBSCRIPTION_PLAN,
                lines=json.dumps([{"description": "PR-AI Subscription paid", "qty": 1, "price": payload.get('price', 0.0)}])
            )
            db.session.add(invoice)
            db.session.commit()
                        
            pdf_path = generate_invoice_pdf(invoice, output_dir=INVOICES_DIR)
            invoice.pdf_path = pdf_path
            db.session.commit()

            SendEmail(
                user_email_origin=email_metadata,
                html_attach_flag=True,
                email_type="Sucess Upgrated Account",
                SMTP_ADM=SMTP_USER,
                SMTP_PASSWORD=SMTP_PASSWORD,
                SMTP_HOST=host,
                SMTP_PORT=port,
                use_tls=use_tls,
                erro_project="",
                title_origin="",
                new_scheduled_time="",
                planname=SUBSCRIPTION_PLAN
            )


        elif session.get("payment_status") == "unpaid" and session.get("payment_intent"):
            payment_intent = stripe.PaymentIntent.retrieve(session["payment_intent"])
            hosted_voucher_url = (
                payment_intent.next_action
                and payment_intent.next_action.get("boleto_display_details", {})
                .get("hosted_voucher_url")
            )
            if hosted_voucher_url:
                user_email = session.get("customer_details", {}).get("email")
                print("Gerou o boleto e o link é", hosted_voucher_url)
                log_action(logs_collection, 
                    'payment_system',
                    {'message': f"Gerou o boleto e o link é {hosted_voucher_url}"},
                    user=numeric_user_id
                    )
            


    elif event["type"] == "checkout.session.expired":
        session = event["data"]["object"]
        if session.get("payment_status") == "unpaid":
            teste_id = session["metadata"].get("testeId")
            print("Checkout expirado", teste_id)
            log_action(logs_collection, 
                'payment_system',
                {'message': f"Checkout expirado {teste_id}"},
                )
            
    elif event["type"] == "checkout.session.async_payment_succeeded":
        session = event["data"]["object"]
        if session.get("payment_status") == "paid":
            teste_id = session["metadata"].get("testeId")
            print("Pagamento boleto confirmado", teste_id)
            log_action(logs_collection, 
                'payment_system',
                {'message': f"Pagamento boleto confirmado {teste_id}"},
                )
            
    elif event["type"] == "checkout.session.async_payment_failed":
        session = event["data"]["object"]
        if session.get("payment_status") == "unpaid":
            teste_id = session["metadata"].get("testeId")
            print("Pagamento boleto falhou", teste_id)
            log_action(logs_collection, 
                'payment_system',
                {'message': f"Pagamento boleto falhou {teste_id}"},
                )
            
    elif event["type"] == "customer.subscription.deleted":
        print("Cliente cancelou o plano")
        log_action(logs_collection, 
            'payment_system',
            {'message': f"Cliente cancelou o plano"},
            )
        
    return jsonify({"result": event, "ok": True})



@app.route('/api/github/callback', methods=['GET'])
def github_app_callback():
    """
    Callback após instalação/autorização do GitHub App.
    - Se receber installation_id e houver user_token (query param ou header), associa a instalação ao usuário.
    - Se receber 'code' (fluxo OAuth), troca por access_token e tenta associar ao usuário pelo e-mail retornado.
    """
    try:
        installation_id = request.args.get('installation_id')
        setup_action = request.args.get('setup_action')
        code = request.args.get('code')
        user_token = request.args.get('X-API-TOKEN')
        if installation_id:
            user = None
            if user_token:
                user = get_user_by_access_token(user_token)
            if user:
                settings = SystemSettings.query.filter_by(user_id=user.id).first()
                if not settings:
                    settings = SystemSettings(user_id=user.id)
                    db.session.add(settings)
                settings.installation_id = int(installation_id)
                settings.updated_at = datetime.utcnow()
                db.session.commit()

                log_action(logs_collection, 'github_installation_linked', {
                    'message': f'installation {installation_id} linked to user {user.id}',
                    'installation_id': installation_id,
                    'setup_action': setup_action
                }, user=user.id)

                return jsonify({
                    "status": "success",
                    "message": f"Instalação do GitHub (installation_id={installation_id}) vinculada ao usuário.",
                    "installation_id": installation_id
                }), 200
            else:
                log_action(logs_collection, 'github_installation_unbound', {
                    'message': f"Installation {installation_id} received but no user token provided.",
                    'installation_id': installation_id,
                    'setup_action': setup_action
                }, level='warning')

                return jsonify({
                    "status": "success",
                    "message": f"GitHub App instalado (installation_id={installation_id}). Vincule a instalação no painel do usuário para ativar integrações.",
                    "installation_id": installation_id
                }), 200

        if code:
            if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
                return jsonify({"status": "error", "message": "GITHUB_CLIENT_ID/GITHUB_CLIENT_SECRET não configurados"}), 500
            token_resp = requests.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                json={"client_id": GITHUB_CLIENT_ID, "client_secret": GITHUB_CLIENT_SECRET, "code": code},
                timeout=10
            )
            if token_resp.status_code != 200:
                logger.error("Erro ao trocar code por token: %s", token_resp.text)
                return jsonify({"status": "error", "message": "Erro ao obter access_token do GitHub"}), 500

            token_data = token_resp.json()
            access_token = token_data.get("access_token")
            if not access_token:
                return jsonify({"status": "error", "message": "access_token não recebido do GitHub"}), 500

            user_resp = requests.get("https://api.github.com/user", headers={"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github+json"}, timeout=10)
            if user_resp.status_code != 200:
                logger.error("Erro ao buscar usuário GitHub: %s", user_resp.text)
                return jsonify({"status": "error", "message": "Não foi possível obter dados do usuário no GitHub"}), 500

            gh_user = user_resp.json()
            gh_email = gh_user.get("email")

            if not gh_email:
                emails_resp = requests.get("https://api.github.com/user/emails", headers={"Authorization": f"Bearer {access_token}", "Accept": "application/vnd.github+json"}, timeout=10)
                if emails_resp.status_code == 200:
                    emails = emails_resp.json()
                    primary = next((e for e in emails if e.get("primary") and e.get("verified")), None)
                    if primary:
                        gh_email = primary.get("email")

            if gh_email:
                local_user = get_user_by_email(gh_email)
                if local_user:
                    settings = SystemSettings.query.filter_by(user_id=local_user.id).first()
                    if not settings:
                        settings = SystemSettings(user_id=local_user.id)
                        db.session.add(settings)
                    settings.github_token = access_token
                    settings.updated_at = datetime.utcnow()
                    db.session.commit()
                    log_action(logs_collection, 'github_oauth_linked', {
                        'message': f'GitHub OAuth linked for user {local_user.id}',
                        'github_login': gh_user.get("login"),
                        'email': gh_email
                    }, user=local_user.id)
                    return jsonify({"status": "success", "message": "Conta GitHub vinculada ao usuário local."}), 200

            return jsonify({
                "status": "success",
                "message": "Token GitHub recebido. Vincule manualmente no painel do usuário se necessário.",
                "github_access_token": access_token
            }), 200

        return jsonify({"status": "error", "message": "Callback inválido. Forneça installation_id ou code."}), 400

    except Exception as e:
        logger.exception("Erro em github_app_callback: %s", e)
        log_action(logs_collection, 'github_callback_error', {'error': str(e)}, level='error')
        return jsonify({"status": "error", "message": "Erro interno no callback do GitHub", "detail": str(e)}), 500


@app.route("/webhook/github", methods=["POST"])
def github_webhook():
    try:
        signature_header = request.headers.get("X-Hub-Signature-256") or ""
        if not signature_header or not verify_signature(request.data, signature_header, GITHUB_WEBHOOK_SECRET):
            logger.warning("Assinatura inválida do webhook do GitHub")
            abort(400, "Assinatura inválida")

        event = request.headers.get("X-GitHub-Event", "ping")
        payload = request.get_json(force=True, silent=True) or {}

        if event == "ping":
            return jsonify({"msg": "pong"}), 200

        user_token = request.headers.get("X-API-TOKEN") or request.args.get("X-API-TOKEN")
        user = None
        if user_token:
            try:
                user = get_user_by_access_token(user_token)
            except Exception:
                user = None

        if event == "installation":
            action = payload.get("action")
            installation = payload.get("installation", {})
            installation_id = installation.get("id")
            account = installation.get("account", {}).get("login")

            if not installation_id:
                logger.warning("Evento de instalação sem installation.id")
                return "", 204

            if action == "created":
                if user:
                    settings = SystemSettings.query.filter_by(user_id=user.id).first()
                    if not settings:
                        settings = SystemSettings(user_id=user.id)
                        db.session.add(settings)
                    settings.installation_id = int(installation_id)
                    settings.updated_at = datetime.utcnow()
                    db.session.commit()

                    log_action(logs_collection, 'github_installation_created', {
                        'message': f'installation {installation_id} associated to user {user.id}',
                        'installation_id': installation_id,
                        'account': account
                    }, user=user.id)
                    logger.info("Installation %s associated to user %s", installation_id, user.id)
                else:
                    log_action(logs_collection, 'github_installation_created_unbound', {
                        'message': f'installation {installation_id} received with no associated user',
                        'installation_id': installation_id,
                        'account': account
                    }, level='warning')
                    logger.info("Installation %s received but not bound to any user", installation_id)

            elif action == "deleted":
                settings = SystemSettings.query.filter_by(installation_id=installation_id).first()
                if settings:
                    settings.installation_id = None
                    settings.updated_at = datetime.utcnow()
                    db.session.commit()
                    log_action(logs_collection, 'github_installation_deleted', {
                        'message': f'installation {installation_id} removed',
                        'installation_id': installation_id,
                        'account': account
                    })
                    logger.info("Installation %s removed from settings", installation_id)
                else:
                    logger.info("Received installation.deleted for %s but no settings found", installation_id)

            return "", 204

        if event == "pull_request":
            action = payload.get("action")
            if action in ("opened", "synchronize", "reopened"):
                try:
                    threading.Thread(target=process_pull_request, args=(payload,)).start()
                    log_action(logs_collection, 'pull_request_received', {
                        'message': 'Pull request event queued for processing',
                        'action': action,
                        'pr': (payload.get("pull_request") or {}).get("number")
                    }, user=(user.id if user else None))
                except Exception as e:
                    logger.exception("Erro ao enfileirar processamento de PR: %s", e)
                    log_action(logs_collection, 'pull_request_processing_error', {'error': str(e)}, level='error')
            return "", 204

        log_action(logs_collection, 'github_webhook_received', {
            'event': event,
            'payload_summary': {'keys': list(payload.keys())[:10]}
        }, user=(user.id if user else None))

        return "", 204

    except Exception as e:
        logger.exception("Erro no webhook do GitHub: %s", e)
        log_action(logs_collection, 'github_webhook_error', {'error': str(e)}, level='error')
        return "", 500


def initialize_database():
    """Inicializar banco de dados"""
    with app.app_context():
        db.create_all()

initialize_database()
