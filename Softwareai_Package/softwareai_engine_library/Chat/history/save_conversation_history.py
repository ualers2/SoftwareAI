# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
def save_conversation_history(session_id, history, user_email, appcompany):
    try:
        user_email_filtred = user_email.replace(".", "_")
        base_ref = db.reference(f'users/{user_email_filtred}/conversations/{session_id}', app=appcompany)
        
        # Garante que o _meta seja criado apenas uma vez
        meta_ref = base_ref.child('_meta')
        if not meta_ref.get():
            meta_ref.set({
                "title": "Nova conversa",
                "created_at": datetime.now().isoformat()
            })

        # Verifica quantas mensagens já existem
        current_data = base_ref.get()
        existing_messages = {k: v for k, v in current_data.items() if k != "_meta"} if current_data else {}
        next_index = len(existing_messages)

        # Adiciona apenas novas mensagens
        for i, msg in enumerate(history[-2:]):  # As duas últimas são user + system
            base_ref.child(str(next_index + i)).set(msg)

        return True
    except Exception as e:
        print(f"Error saving conversation history: {e}")
        return False
