from typing_extensions import TypedDict
import requests
import base64
from agents import function_tool


class autogetfilecontentData(TypedDict):
    repo_name: str
    file_path: str
    branch_name: str
    companyname: str
    github_token: str
    

@function_tool
def autogetfilecontent(data: autogetfilecontentData):
    try:
        data_FINAL = data["data"]
        repo_name = data_FINAL["repo_name"]
        file_path = data_FINAL["file_path"]
        branch_name = data_FINAL["branch_name"]
        companyname = data_FINAL["companyname"]
        github_token = data_FINAL["github_token"]
    except Exception as eroo1:
        print(eroo1)
        repo_name = data["repo_name"]
        file_path = data["file_path"]
        branch_name = data["branch_name"]
        companyname = data["companyname"]
        github_token = data["github_token"]
    print("autogetfilecontent Prestes a iniciar")
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    file_url = f"https://api.github.com/repos/{companyname}/{repo_name}/contents/{file_path}?ref={branch_name}"
    response = requests.get(file_url, headers=headers)
    if response.status_code == 200:
        file_data = response.json()
        import base64
        content = base64.b64decode(file_data['content']).decode('utf-8')
        return content
    else:
        print(f"Erro ao acessar {file_path}. Status: {response.status_code}  {response.content}")
        return None
    

def autogetfilecontent1(repo_name, file_path, branch_name, companyname, github_token):

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }


    file_url = f"https://api.github.com/repos/{companyname}/{repo_name}/contents/{file_path}?ref={branch_name}"
    response = requests.get(file_url, headers=headers)
    
    if response.status_code == 200:
        file_data = response.json()
        import base64
        content = base64.b64decode(file_data['content']).decode('utf-8')
        return content
    else:
        print(f"Erro ao acessar {file_path}. Status: {response.status_code}  {response.content}")
        return None