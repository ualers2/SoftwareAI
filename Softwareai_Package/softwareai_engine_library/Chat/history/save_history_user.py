
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################

from softwareai_engine_library.Chat.history.save_assistant_message import save_assistant_message


def save_history_user(
    session_id,
    user_email,
    message_to_send,
    appcompany
        
    ):
    # Criar a nova mensagem do usuário com timestamp
    user_message_obj = {
        "role": "user",
        "content": message_to_send,
        "timestamp": int(time.time() * 1000)
    }

    save_assistant_message(
        session_id=session_id,
        message_obj=user_message_obj,
        user_email=user_email, 
        appcompany=appcompany
    )
    