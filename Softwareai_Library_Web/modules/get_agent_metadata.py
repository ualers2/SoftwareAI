from firebase_admin import credentials, db, initialize_app

# Função para buscar as metainformações dos agentes
def get_agent_metadata(agent_ids, appcompany):
    metadata = {}
    for agent_id in agent_ids:
        try:
            ref = db.reference(f"agents/{agent_id}/metadata", app=appcompany)
            metadata[agent_id] = ref.get()
        except Exception as e:
            metadata[agent_id] = {"error": str(e)}
    return metadata