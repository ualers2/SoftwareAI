import requests

def EgetMetadataAgent(agent_ids = ['PreProject']):
    base_url = 'https://softwareai-library-hub.rshare.io/api/agent-metadata/'
    agent_ids_str = ','.join(agent_ids)
    
    try:
        response = requests.get(base_url + agent_ids_str)
        response.raise_for_status()  # Garante que o código de status é 200
        metadata = response.json()
        
        agents_data = {}  # Dicionário para armazenar os dados de cada agente
        
        # Itera sobre os dados de cada agente
        for agent_id in agent_ids:
            if agent_id in metadata and metadata[agent_id] is not None:
                agent_info = metadata[agent_id]
                name = agent_info.get("name")
                model = agent_info.get("model")
                instruction = agent_info.get("instruction")
                tools = agent_info.get("tools")
                
                agents_data[agent_id] = {
                    'name': name,
                    'model': model,
                    'instruction': instruction,
                    'tools': tools
                }
            else:
                print(f"Agente {agent_id} não encontrado ou metadado está ausente.")
        
        return agents_data
    
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar metadados: {e}")
        return {}

# # Exemplo de uso
# agent_ids = ['PreProject']
# agents_metadata = EgetMetadataAgent(agent_ids)

# # Acessando os dados de cada agente diretamente com o nome do agente
# if 'PreProject' in agents_metadata:
#     name_PreProject = agents_metadata['PreProject']["name"]
#     model_PreProject = agents_metadata['PreProject']["model"]
#     instruction_PreProject = agents_metadata['PreProject']["instruction"]
#     tools_PreProject = agents_metadata['PreProject']["tools"]

#     print(f"PreProject:")
#     print(f"  Name: {name_PreProject}")
#     print(f"  Model: {model_PreProject}")
#     print(f"  Instruction: {instruction_PreProject}")
#     print(f"  Tools: {tools_PreProject}")