
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################

from softwareai_engine_library.Chat.utils.get_user_data_from_firebase import get_user_data_from_firebase


def dynamic_rate_limit(appcompany):
    """
    Define o limite de requisições com base no e-mail do usuário.
    Substitui "." por "_" para usar como identificador único.
    """
    try:
        user_email = request.form.get("user_email") or request.args.get("user_email") or request.args.get("userEmail") or request.headers.get("X-User-Email")
        if user_email:
            user_id = user_email.replace(".", "_")
            user_data = get_user_data_from_firebase(user_id, appcompany)
            if user_data:
                return user_data.get("limit", "10 per minute")
            
    except Exception as e:
        print(f"[Rate Limit Error] {e}")
    return "10 per minute"


