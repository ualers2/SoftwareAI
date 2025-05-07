#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################
from typing_extensions import TypedDict
from agents import function_tool

class autoapprovepullrequestData(TypedDict):
    repo_owner: str
    repo_name: str
    pull_number: int
    githubtoken_aprove: str
    githubtoken_merge: str
    approval_message: str
    merge_message: str

@function_tool
def autoapprovepullrequest(data: autoapprovepullrequestData):
    try:
        data_FINAL = data["data"]
        repo_owner = data_FINAL["repo_owner"]
        repo_name = data_FINAL["repo_name"]
        pull_number = data_FINAL["pull_number"]
        githubtoken_aprove = data_FINAL["githubtoken_aprove"]
        githubtoken_merge = data_FINAL["githubtoken_merge"]
        approval_message = data_FINAL["approval_message"]
        merge_message = data_FINAL["merge_message"]
    except Exception as e:
        print(e)
        repo_owner = data["repo_owner"]
        repo_name = data["repo_name"]
        pull_number = data["pull_number"]
        githubtoken_aprove = data["githubtoken_aprove"]
        githubtoken_merge = data["githubtoken_merge"]
        approval_message = data["approval_message"]
        merge_message = data["merge_message"]
    pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pull_number}/reviews"
    headers = {
        "Authorization": f"token {githubtoken_aprove}",
        "Accept": "application/vnd.github.v3+json"
    }
    review_data = {
        "event": "APPROVE",
        "body": approval_message
    }
    response = requests.post(pr_url, json=review_data, headers=headers)
    if response.status_code == 200:
        print(f"Pull Request #{pull_number} aprovado com sucesso no repositório {repo_name} com a mensagem: '{approval_message}'")
    else:
        print(f"Falha ao aprovar o Pull Request. Status: {response.status_code}, Resposta: {response.json()}")
        return {"status": "error", "message": response.json()}
    headers = {
        "Authorization": f"token {githubtoken_merge}",
        "Accept": "application/vnd.github.v3+json"
    }
    merge_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pull_number}/merge"
    merge_data = {
        "commit_title": f"Merge PR #{pull_number}",
        "commit_message": merge_message,
        "merge_method": "merge"  # ou 'squash' ou 'rebase', se preferir outros métodos de merge
    }

    merge_response = requests.put(merge_url, json=merge_data, headers=headers)

    if merge_response.status_code == 200:
        print("Merge realizado com sucesso!")
        return {"status": "merged", "message": "Pull request foi mergeado com sucesso."}
    else:
        print(f"Erro ao fazer merge. Status: {merge_response.json()}")
        return {"status": "error", "message": merge_response.json()}





def autoapprovepullrequest1(
                repo_owner: str,
                repo_name: str,
                pull_number: int,
                githubtoken_aprove: str,
                githubtoken_merge: str,
                approval_message: str,
                merge_message: str
                ):
    
    pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pull_number}/reviews"
    headers = {
        "Authorization": f"token {githubtoken_aprove}",
        "Accept": "application/vnd.github.v3+json"
    }
    review_data = {
        "event": "APPROVE",
        "body": approval_message
    }
    
    response = requests.post(pr_url, json=review_data, headers=headers)
    
    if response.status_code == 200:
        print(f"Pull Request #{pull_number} aprovado com sucesso no repositório {repo_name} com a mensagem: '{approval_message}'")
            

    else:
        print(f"Falha ao aprovar o Pull Request. Status: {response.status_code}, Resposta: {response.json()}")
        return {"status": "error", "message": response.json()}


    headers = {
        "Authorization": f"token {githubtoken_merge}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Fazer o merge do pull request
    merge_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pull_number}/merge"
    merge_data = {
        "commit_title": f"Merge PR #{pull_number}",
        "commit_message": merge_message,
        "merge_method": "merge"  # ou 'squash' ou 'rebase', se preferir outros métodos de merge
    }

    merge_response = requests.put(merge_url, json=merge_data, headers=headers)

    if merge_response.status_code == 200:
        print("Merge realizado com sucesso!")
        return {"status": "merged", "message": "Pull request foi mergeado com sucesso."}
    else:
        print(f"Erro ao fazer merge. Status: {merge_response.json()}")
        return {"status": "error", "message": merge_response.json()}




