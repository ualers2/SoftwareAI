from flask import Blueprint, request, jsonify
from Models.postgreSQL.user import User, TOKEN_DEFAULT_EXPIRES_DAYS
from Modules.Savers.log_action import log_action
from Models.mongoDB.logs import ( 
                                Log,
                                logs_collection, 
                                mongo_client,
                                mongo_db, 
                            ) 
from Modules.Resolvers.user_identifier import auth_user


from api import db, app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
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

@auth_bp.route('/login', methods=['GET'])
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
