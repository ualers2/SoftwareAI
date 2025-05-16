
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################

from softwareai_engine_library.Chat.history.save_assistant_message import save_assistant_message


def save_history_system(
    session_id,
    user_email,
    message_to_send,
    appcompany
        
    ):
    # conversation_history = get_conversation_history(session_id, user_email=user_email, appcompany=appcompany)
    assistant_message_obj = {
        "role": "system",
        "content": message_to_send,
        "timestamp": int(time.time() * 1000)
    }
    save_assistant_message(
        session_id=session_id,
        message_obj=assistant_message_obj,
        user_email=user_email, 
        appcompany=appcompany
    )
