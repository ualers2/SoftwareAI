import firebase_admin
from firebase_admin import credentials, db, delete_app
from typing import List, Dict, Any
from typing_extensions import TypedDict
from agents import function_tool

class FetchMetadataInput(TypedDict):
    firebase_json_path: str
    firebase_db_url: str
    agent_ids: List[str]

@function_tool
def fetch_agent_metadata(data: FetchMetadataInput) -> Dict[str, Any]:
    """
    Busca os metadados de diversos agentes no Firebase Realtime Database.
    
    Parâmetros esperados em `data`:
    - firebase_json_path: caminho para o JSON de credenciais do Firebase.
    - firebase_db_url: URL do database do Firebase.
    - agent_ids: lista de IDs de agentes cujos metadados serão buscados.
    
    Retorna um dicionário no formato:
    {
        "agent_id_1": { ... metadados ... },
        "agent_id_2": { ... metadados ... },
        ...
    }
    """
    app_instance = None
    try:
        # Inicializa o app Firebase
        cred = credentials.Certificate(data["firebase_json_path"])
        app_instance = firebase_admin.initialize_app(cred, {
            "databaseURL": data["firebase_db_url"]
        })
        
        results: Dict[str, Any] = {}
        for agent_id in data["agent_ids"]:
            # Monta referência no Realtime Database
            ref = db.reference(f'agents/{agent_id}/metadata', app=app_instance)
            metadata = ref.get()
            results[agent_id] = metadata
        
        return {
            "success": True,
            "metadata": results
        }
    
    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Erro ao buscar metadados: {e}"
        }
    
    finally:
        # Cleanup
        if app_instance:
            delete_app(app_instance)
