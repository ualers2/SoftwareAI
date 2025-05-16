# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
def save_agent_for_session(session_id, agent, appcompany):
    # Converte o agente em um formato serializável (por exemplo, um dicionário)
    agent_data = {
        "name": agent.name,
        "instructions": agent.instructions,
        "model": agent.model,
    }
    
    # Salva o agente no Firebase Realtime Database
    ref = db.reference(f'agents/{session_id}', app=appcompany)
    ref.set(agent_data)
