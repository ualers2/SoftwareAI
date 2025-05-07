#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################
from typing_extensions import TypedDict
from agents import function_tool

def get_file_sha(repo, path, token):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}","Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["sha"]
    return None

class autouploadData(TypedDict):
    softwarepypath: List[str]
    repo_name: str
    repo_owner: str
    token: str
    
@function_tool
def autoupload(data: autouploadData):
    try:
        data_FINAL = data["data"]
        softwarepypath = data_FINAL["softwarepypath"]
        repo_owner = data_FINAL["repo_owner"] 
        repo_name = data_FINAL["repo_name"]
        token = data_FINAL["token"]
    except Exception as e:
        print(e)
        softwarepypath = data["softwarepypath"]
        repo_owner = data["repo_owner"] 
        repo_name = data["repo_name"]
        token = data["token"]

    print("autoupload Prestes a iniciar")
    results = []

    # 🧠 Detectar pasta base comum de todos os arquivos
    common_prefix = os.path.commonpath(softwarepypath)

    for softwarepy in softwarepypath:
        with open(softwarepy, "rb") as file:
            content = file.read()
            encoded_content = base64.b64encode(content).decode("utf-8")

        # 📁 Calcular o caminho relativo a partir da raiz comum
        relative_path = os.path.relpath(softwarepy, start=common_prefix)
        github_path = relative_path.replace("\\", "/")

        filename = os.path.basename(softwarepy)
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{github_path}"

        response = requests.get(url, headers={"Authorization": f"token {token}"})
        sha = response.json().get("sha") if response.status_code == 200 else None

        data = {
            "message": f"Update {filename}",
            "content": encoded_content,
            "branch": "main"
        }
        if sha:
            data["sha"] = sha

        put_response = requests.put(url, json=data, headers={"Authorization": f"token {token}"})
        if put_response.status_code in (200, 201):
            results.append({"status": "success", "message": f"Arquivo: {github_path} - Status: Sucesso ({put_response.status_code})"})
        else:
            results.append({"status": "error", "message": f"Erro ao enviar {github_path}: Status {put_response.status_code} - {put_response.text}"})

    return results
