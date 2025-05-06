# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################

from softwareai_engine_library.Chat.utils.get_api_key import get_api_key
from softwareai_engine_library.Chat.utils.get_user_data_from_firebase import get_user_data_from_firebase

def autenticar_usuario(appcompany):
    api_key = get_api_key()
    if not api_key:
        response = jsonify({"error": "API Não fornecida."})
        response.status_code = 401
        return None, response

    user_email = (
        request.form.get("user_email")
        or request.args.get("user_email")
        or request.args.get("userEmail")
        or request.headers.get("X-User-Email")
    )

    if user_email:
        user_id = user_email.replace(".", "_")
        user_data = get_user_data_from_firebase(user_id, appcompany)
        if not user_data:
            response = jsonify({"error": "Usuário não encontrado."})
            response.status_code = 401
            return None, response
        return user_data, None

    # ⚠️ Adicione esse retorno padrão se `user_email` não for fornecido
    response = jsonify({"error": "user_email não informado nos headers ou parâmetros."})
    response.status_code = 400
    return None, response

   