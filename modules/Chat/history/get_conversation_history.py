# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
def get_conversation_history(session_id, user_email, appcompany, limit=100):
    user_email_filtred = user_email.replace(".", "_")
    ref = db.reference(f'users/{user_email_filtred}/conversations/{session_id}', app=appcompany)
    history = ref.get()
    
    if not history:
        return []

    clean_history = []
    for message in history:
        if isinstance(message, dict):
            if 'timestamp' not in message:
                message['timestamp'] = 0
            clean_history.append(message)
        else:
            print(f"[WARN] Mensagem ignorada por estar em formato inválido: {message}")

    sorted_history = sorted(clean_history, key=lambda x: x.get('timestamp', 0))
    return sorted_history[-limit:]
