
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################

def find_invalid_conversations(appcompany):
    ref = db.reference('conversations', app=appcompany)
    all_data = ref.get()
    
    for session_id, messages in all_data.items():
        if not isinstance(messages, list):
            print(f"⚠️ Sessão {session_id} não contém uma lista.")
            continue
        for m in messages:
            if not isinstance(m, dict):
                print(f"❌ Sessão {session_id} contém item inválido: {m}")
