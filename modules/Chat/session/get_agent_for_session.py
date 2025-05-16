
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################

def get_agent_for_session(session_id, appcompany):
    # Recupera os dados do agente a partir do Firebase
    ref = db.reference(f'agents/{session_id}', app=appcompany)
    agent_data = ref.get()

    if agent_data:
        # Cria uma instância do agente a partir dos dados recuperados
        agent = Agent(
            name=agent_data.get("name"),
            instructions=agent_data.get("instructions"),
            model=agent_data.get("model")
        )
        return agent
    else:
        return None
