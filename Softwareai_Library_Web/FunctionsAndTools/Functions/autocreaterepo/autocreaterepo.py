#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################
from typing_extensions import TypedDict, Any , Union
from agents import Agent, ModelSettings, function_tool, FileSearchTool, WebSearchTool, Runner

class autocreaterepoData(TypedDict):
    repo_owner: str
    repo_name: str
    description: str
    githubtoken: str
    private: bool

@function_tool
def autocreaterepo(data: autocreaterepoData):
    try:
        data_FINAL = data["data"]
        repo_owner = data_FINAL["repo_owner"]
        repo_name = data_FINAL["repo_name"]
        description = data_FINAL["description"]
        githubtoken = data_FINAL["githubtoken"]
        private = data_FINAL["private"]
    except Exception as eroo1:
        print(eroo1)
        repo_owner = data["repo_owner"]
        repo_name = data["repo_name"]
        description = data["description"]
        githubtoken = data["githubtoken"]
        private = data["private"]
    repo_url = f"https://api.github.com/orgs/{repo_owner}/repos"
    headers = {
        "Authorization": f"token {githubtoken}",
        "Accept": "application/vnd.github.v3+json"
    }
    repo_data = {
        "name": repo_name,
        "description": description,
        "private": private
    }
    response = requests.post(repo_url, json=repo_data, headers=headers)
    if response.status_code == 201:
        print(f"Repositório {repo_name} criado com sucesso na organização {repo_owner}")
        colaboradores = [
            "CloudArchitectt", "TigraoEscritor", "NexGenCoder756",
            "SignalMaster727", "QuantummCore", "BobGerenteDeProjeto",
            "DallasEquipeDeSolucoes"
        ]
        for colaborador in colaboradores:
            collaborator_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/collaborators/{colaborador}"
            collaborator_data = {"permission": "admin"}
            collaborator_response = requests.put(collaborator_url, headers=headers, json=collaborator_data)
            if collaborator_response.status_code in [201, 204]:
                print(f"Colaborador {colaborador} adicionado com sucesso com permissões de administrador.")
            else:
                print(f"Falha ao adicionar {colaborador}. Status: {collaborator_response.status_code}, Resposta: {collaborator_response.json()}")
        return {"status": "success", "message": f"Repositório {repo_name} criado com sucesso na organização {repo_owner}"}
    else:
        print(f"Falha ao criar o repositório. Status: {response.status_code}, Resposta: {response.json()}")
        return {"status": "error", "message": response.json()}


def autocreaterepo1(
                repo_owner: str,
                repo_name: str, 
                description:str,
                githubtoken: str,
                private: bool,
                
                ):
    repo_url = f"https://api.github.com/orgs/{repo_owner}/repos"
    headers = {
        "Authorization": f"token {githubtoken}",
        "Accept": "application/vnd.github.v3+json"
    }
    repo_data = {
        "name": repo_name,
        "description": description,
        "private": private
    }
    
    response = requests.post(repo_url, json=repo_data, headers=headers)
    
    if response.status_code == 201:
        print(f"Repositório {repo_name} criado com sucesso na organização {repo_owner}")
        
        colaboradores = [
            "CloudArchitectt", "TigraoEscritor", "NexGenCoder756",
            "SignalMaster727", "QuantummCore", "BobGerenteDeProjeto",
            "DallasEquipeDeSolucoes"
        ]
        
        for colaborador in colaboradores:
            collaborator_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/collaborators/{colaborador}"
            collaborator_data = {"permission": "admin"}
            
            collaborator_response = requests.put(collaborator_url, headers=headers, json=collaborator_data)
            
            if collaborator_response.status_code in [201, 204]:
                print(f"Colaborador {colaborador} adicionado com sucesso com permissões de administrador.")
            else:
                print(f"Falha ao adicionar {colaborador}. Status: {collaborator_response.status_code}, Resposta: {collaborator_response.json()}")
        
        return {"status": "success", "message": f"Repositório {repo_name} criado com sucesso na organização {repo_owner}"}
    
    else:
        print(f"Falha ao criar o repositório. Status: {response.status_code}, Resposta: {response.json()}")
        return {"status": "error", "message": response.json()}
