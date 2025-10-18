from typing_extensions import TypedDict, Any
from agents import Agent, ModelSettings, function_tool, FileSearchTool, WebSearchTool, Runner
from datetime import datetime
import requests

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
        return {"status": "success", "message": f"Repositório {repo_name} criado com sucesso na organização {repo_owner}"}
    else:
        print(f"Falha ao criar o repositório. Status: {response.status_code}, Resposta: {response.json()}")
        return {"status": "error", "message": response.json()}