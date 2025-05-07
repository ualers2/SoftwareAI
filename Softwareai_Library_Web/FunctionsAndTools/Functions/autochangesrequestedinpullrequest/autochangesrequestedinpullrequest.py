#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################
from typing_extensions import TypedDict
from agents import function_tool

class autochangesrequestedinpullrequestData(TypedDict):
    repo: str
    file_update: str
    new_content: str
    branch: str
    commit_message: str
    github_token: str

@function_tool
def autochangesrequestedinpullrequest(data: autochangesrequestedinpullrequestData):
    try:
        data_FINAL = data["data"]
        repo = data_FINAL["repo"]
        file_update = data_FINAL["file_update"]
        new_content = data_FINAL["new_content"]
        branch = data_FINAL["branch"]
        commit_message = data_FINAL["commit_message"]
        github_token = data_FINAL["github_token"]
    except Exception as e:
        print(e)
        repo = data["repo"]
        file_update = data["file_update"]
        new_content = data["new_content"]
        branch = data["branch"]
        commit_message = data["commit_message"]
        github_token = data["github_token"]
    url = f"https://api.github.com/repos/{repo}/contents/{file_update}?ref={branch}"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_info = response.json()
    else:
        print("Erro ao obter informações do arquivo:", response.status_code, response.content)
    sha = file_info.get("sha")
    if not sha:
        print("Não foi possível obter o SHA do arquivo.")
    url = f"https://api.github.com/repos/{repo}/contents/{file_update}"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }
    content_b64 = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
    payload = {
        "message": commit_message,
        "content": content_b64,
        "sha": sha,
        "branch": branch
    }
    response = requests.put(url, headers=headers, json=payload)
    
    if response.status_code in (200, 201):
        print("Arquivo atualizado com sucesso!")
    else:
        print("Erro ao atualizar o arquivo:", response.status_code, response.content)
        sys.exit(1)

    return "Arquivo atualizado com sucesso!"

def autochangesrequestedinpullrequest1(
        repo,
        file_update, 
        new_content, 
        branch,
        commit_message, 
        github_token
    ): 

    # Cria um novo commit para as mudanças requeridas traves do comentario 
    
    url = f"https://api.github.com/repos/{repo}/contents/{file_update}?ref={branch}"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_info = response.json()
    else:
        print("Erro ao obter informações do arquivo:", response.status_code, response.content)

    sha = file_info.get("sha")
    if not sha:
        print("Não foi possível obter o SHA do arquivo.")
        
    url = f"https://api.github.com/repos/{repo}/contents/{file_update}"
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }
    content_b64 = base64.b64encode(new_content.encode("utf-8")).decode("utf-8")
    payload = {
        "message": commit_message,
        "content": content_b64,
        "sha": sha,
        "branch": branch
    }
    
    response = requests.put(url, headers=headers, json=payload)
    
    if response.status_code in (200, 201):
        print("Arquivo atualizado com sucesso!")
    else:
        print("Erro ao atualizar o arquivo:", response.status_code, response.content)
        sys.exit(1)

    return "Arquivo atualizado com sucesso!"
