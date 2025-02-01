
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################


def create_repo(repo_name: str, 
                description:str,
                token: str
                ):
    repo_url = "https://api.github.com/orgs/A-I-O-R-G/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    repo_data = {
        "name": repo_name,
        "description": description,
        "private": False
    }
    
    response = requests.post(repo_url, json=repo_data, headers=headers)
    
    if response.status_code == 201:
        print(f"Repositório {repo_name} criado com sucesso na organização A-I-O-R-G!")
        
        colaboradores = [
            "CloudArchitectt", "TigraoEscritor", "NexGenCoder756",
            "SignalMaster727", "QuantummCore", "BobGerenteDeProjeto",
            "DallasEquipeDeSolucoes"
        ]
        
        for colaborador in colaboradores:
            collaborator_url = f"https://api.github.com/repos/A-I-O-R-G/{repo_name}/collaborators/{colaborador}"
            collaborator_data = {"permission": "admin"}
            
            collaborator_response = requests.put(collaborator_url, headers=headers, json=collaborator_data)
            
            if collaborator_response.status_code in [201, 204]:
                print(f"Colaborador {colaborador} adicionado com sucesso com permissões de administrador.")
            else:
                print(f"Falha ao adicionar {colaborador}. Status: {collaborator_response.status_code}, Resposta: {collaborator_response.json()}")
        
        return {"status": "success", "message": f"Repositório {repo_name} criado com sucesso na organização A-I-O-R-G!"}
    
    else:
        print(f"Falha ao criar o repositório. Status: {response.status_code}, Resposta: {response.json()}")
        return {"status": "error", "message": response.json()}
