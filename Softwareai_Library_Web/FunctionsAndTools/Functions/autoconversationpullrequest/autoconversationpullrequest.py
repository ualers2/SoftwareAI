#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################
from typing_extensions import TypedDict
from agents import function_tool

class autoconversationissueData(TypedDict):
    owner: str
    repo: str
    response_message: str
    issue_number: int
    github_token: str

@function_tool
def autoconversationissue(data: autoconversationissueData):
    try:
        data_FINAL = data["data"]
        owner = data_FINAL["owner"]
        repo = data_FINAL["repo"]
        response_message = data_FINAL["response_message"]
        issue_number = data_FINAL["issue_number"]
        github_token = data_FINAL["github_token"]
    except Exception as e:
        print(e)
        owner = data["owner"]
        repo = data["repo"]
        response_message = data["response_message"]
        issue_number = data["issue_number"]
        github_token = data["github_token"]
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
    print(url)
    headers = {"Authorization": f"Bearer {github_token}", "Accept": "application/vnd.github+json"}
    payload_resposta = {"body": response_message}
    resposta_api = requests.post(url, headers=headers, json=payload_resposta)
    print(resposta_api.status_code)
    print(resposta_api)
    if resposta_api.status_code in [200, 201]:
        response = f"Comentário respondido com sucesso!"
    else:
        response = f"Falha ao responder comentário:{resposta_api.content}"
    print(response)
    return response
