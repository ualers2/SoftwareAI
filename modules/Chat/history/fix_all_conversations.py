# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
def fix_all_conversations(appcompany):
    ref = db.reference('conversations', app=appcompany)
    all_users = ref.get()
    
    for user_id, user_convos in all_users.items():
        for session_id, convo in user_convos.items():
            if isinstance(convo, list):
                # Converte para dict com chaves numéricas
                fixed_convo = {str(i): m for i, m in enumerate(convo)}
                ref.child(f"{user_id}/{session_id}").set(fixed_convo)
                print(f"[FIXED] {user_id}/{session_id}")
 