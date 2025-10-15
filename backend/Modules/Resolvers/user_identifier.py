# Back-End\Modules\Resolvers\user_identifier.py
from Models.postgreSQL import db, User
from datetime import datetime, timedelta
from functools import wraps
from flask import g, Flask, Response, request, jsonify
import logging
from Modules.Savers.log_action import log_action
from Modules.Geters.user_by_access_token import get_user_by_access_token
from Models.mongoDB import ( 
                                Log,
                                AuditTrail, 
                                logs_collection, 
                                mongo_client,
                                mongo_db, 
                            ) 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def auth_user(logs_collection, app, email='', password=''):
    with app.app_context():
        header_token = request.headers.get('X-API-TOKEN')

        user = None
        if header_token:
            try:
                user = get_user_by_access_token(header_token)
                if user:
                    logger.info(f"auth_user login sucess")
                    return user, user.id, "success"
                else:
                    logger.info(f"auth_user invalid token")

                    user = resolve_user_identifier(email)
                    # evita usar user.id quando user é None (corrige crash no log)
                    if not user or not user.check_password(password):
                        log_action(logs_collection, 'login_failed', {'message': 'login_failed in if not user or not user.check_password(password):'}, level='warning', user=(user.id if user else None))
                        return None, None, "invalid"
                    else:
                        logger.info(f"auth_user login sucess")
                        return user, user.id, "success"
                    
            except Exception as e:
                logger.info(f"auth_user_error {e}")
                log_action(
                    logs_collection,
                    'auth_user_error',
                    {'message': str(e)},
                    level='warning'
                )
                return None, None, "invalid"

        if not user:
            return None, None, "invalid"

        return user, user.id, "success"
    
def resolve_user_identifier(identifier):
    """
    Aceita:
     - None -> retorna None
     - número (string ou int) -> busca por id
     - string com @ -> busca por email
     - string sem @ -> tenta converter para int, senão retorna None
    Retorna User instance ou None.
    """
    if not identifier:
        return None

    try:
        uid = int(identifier)
        return User.query.get(uid)
    except (ValueError, TypeError):
        pass

    if isinstance(identifier, str) and "@" in identifier:
        return User.query.filter_by(email=identifier).first()

    return User.query.filter_by(email=str(identifier).strip()).first()

def is_token_revoked_or_expired(user: User):
    if not user:
        log_action(logs_collection, 'is_token_revoked_or_expired', {'message': "Usuário não encontrado"}, user=None)
    
        return True, "Usuário não encontrado"
    if user.revoked_at is not None:
        log_action(logs_collection, 'is_token_revoked_or_expired', {'username': user.email, 'message': "Token revogado"}, user=user.id)
    
        return True, "Token revogado"
    if user.expires_at is not None:
        try:
            if datetime.utcnow() > user.expires_at:
                log_action(logs_collection, 'is_token_revoked_or_expired', {'username': user.email, 'message': "Token expirado"}, user=user.id)
            
                return True, "Token expirado"
        except Exception as err_unkwnow:
            log_action(logs_collection, 'is_token_revoked_or_expired', {'username': user.email, 'message': f"err_unkwnow {err_unkwnow}"}, user=user.id)
        
    if not user.acess_token:
        log_action(logs_collection, 'is_token_revoked_or_expired', {'username': user.email, 'message': "Usuário sem access token"}, user=user.id)
    
        return True, "Usuário sem access token"
    return False, None

def check_user_quota(user: User, required_tokens: int):
    remaining = (user.limit_monthly_tokens or 0) - (user.tokens_used or 0)
    return remaining >= required_tokens, remaining