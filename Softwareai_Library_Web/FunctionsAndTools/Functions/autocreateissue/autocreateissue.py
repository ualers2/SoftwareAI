#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################
from typing_extensions import TypedDict, Any , Union
from agents import Agent, ModelSettings, function_tool, FileSearchTool, WebSearchTool, Runner


class autocreateissueData(TypedDict):
    repo_owner: str
    repo_name: str
    issue_title: str
    issue_body: str
    githubtoken: str
    

@function_tool
def autocreateissue(data: autocreateissueData):
    try:
        data_FINAL = data["data"]
        repo_owner = data_FINAL["repo_owner"]
        repo_name = data_FINAL["repo_name"]
        issue_title = data_FINAL["issue_title"]
        issue_body = data_FINAL["issue_body"]
        githubtoken = data_FINAL["githubtoken"]
    except Exception as eroo1:
        print(eroo1)
        repo_owner = data["repo_owner"]
        repo_name = data["repo_name"]
        issue_title = data["issue_title"]
        issue_body = data["issue_body"]
        githubtoken = data["githubtoken"]
    issue_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    headers = {
        "Authorization": f"token {githubtoken}",
        "Accept": "application/vnd.github.v3+json"
    }
    issue_data = {
        "title": issue_title,
        "body": issue_body
    }
    response = requests.post(issue_url, json=issue_data, headers=headers)
    if response.status_code == 201:
        print(f"Issue '{issue_title}' criada com sucesso no repositório {repo_name}")
        return {"status": "success", "message": f"Issue '{issue_title}' criada com sucesso"}
    else:
        print(f"Falha ao criar a issue. Status: {response.status_code}, Resposta: {response.json()}")
        return {"status": "error", "message": response.json()}



def autocreateissue(
                repo_owner: str,
                repo_name: str,
                issue_title: str,
                issue_body: str,
                githubtoken: str
                ):
    issue_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    headers = {
        "Authorization": f"token {githubtoken}",
        "Accept": "application/vnd.github.v3+json"
    }
    issue_data = {
        "title": issue_title,
        "body": issue_body
    }
    
    response = requests.post(issue_url, json=issue_data, headers=headers)
    
    if response.status_code == 201:
        print(f"Issue '{issue_title}' criada com sucesso no repositório {repo_name}")
        return {"status": "success", "message": f"Issue '{issue_title}' criada com sucesso"}
    else:
        print(f"Falha ao criar a issue. Status: {response.status_code}, Resposta: {response.json()}")
        return {"status": "error", "message": response.json()}






