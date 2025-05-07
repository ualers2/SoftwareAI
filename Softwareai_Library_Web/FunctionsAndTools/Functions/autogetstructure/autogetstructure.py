from typing_extensions import TypedDict
import requests
import base64
from agents import function_tool

def get_repo_structure(repo_name, repo_owner, github_token, branch_name, path=""):
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Adiciona autenticação apenas se o token for informado
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}?ref={branch_name}"
    response = requests.get(url, headers=headers)
    structure = {}
    
    if response.status_code == 200:
        items = response.json()
        for item in items:
            if item['type'] == 'dir':
                structure[item['name']] = get_repo_structure(repo_name, repo_owner, github_token, branch_name, item['path'])
            else:
                structure[item['name']] = item['path']
    else:
        print(f"Erro ao acessar {path}. Status: {response.status_code} {response.content}")
    return structure


class FunctionData(TypedDict):
    repo_name: str
    repo_owner: str
    branch_name: str
    github_token: str
    path: str
    

@function_tool
def autogetstructure(data: FunctionData):
    try:
        data_FINAL = data["data"]
        repo_name = data_FINAL["repo_name"]
        repo_owner = data_FINAL["repo_owner"]
        branch_name = data_FINAL["branch_name"]
        github_token = data_FINAL["github_token"]
        path = data_FINAL["path"]
    except Exception as eroo1:
        print(eroo1)
        repo_name = data["repo_name"]
        repo_owner = data["repo_owner"]
        branch_name = data["branch_name"]
        github_token = data["github_token"]
        path = data["path"]
    print("autogetstructure Prestes a iniciar")
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    # Se path estiver vazio, acessa a raiz do repositório
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents"
    if path:
        url += f"/{path}"
    url += f"?ref={branch_name}"

    response = requests.get(url, headers=headers)
    structure = {}
    if response.status_code == 200:
        items = response.json()
        for item in items:
            if item['type'] == 'dir':
                structure[item['name']] = get_repo_structure(
                    repo_name, repo_owner, github_token, branch_name, item['path']
                )
            else:
                structure[item['name']] = item['path']
    else:
        print(f"Erro ao acessar {path or 'raiz'}. Status: {response.status_code} {response.content}")
    return structure