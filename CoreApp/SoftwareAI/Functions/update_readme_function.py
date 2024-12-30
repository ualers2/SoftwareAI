
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################


def get_file_sha(repo, path, token):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["sha"]
    return None

def update_readme_to_github(
                            file_path_readme_improvements: str,
                            repo_name: str,
                            token: str
                        ):
    
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=r"C:\Users\Media Cuts Studio\Desktop\Saas do site\Projetos de codigo aberto\SoftwareAI\CoreApp\ambiente.env")

    file_path_readme_improvements_teste = os.getenv("PATH_DOCUMENTACAO_ENV")
    directory = os.path.dirname(file_path_readme_improvements_teste)

    with open(file_path_readme_improvements_teste, "rb") as file:
        content = file.read()
        encoded_content = base64.b64encode(content).decode("utf-8")

    relative_path = os.path.relpath(file_path_readme_improvements_teste, start=directory)  
    filename = os.path.basename(file_path_readme_improvements_teste)
    github_path = relative_path.replace("\\", "/")  

    url = f"https://api.github.com/repos/A-I-O-R-G/{repo_name}/contents/{github_path}"

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
        return {"status": "success", "message": f"Arquivo: {github_path} - Status: Sucesso ({put_response.status_code})"}
    else:
        return {"status": "success", "message": f"Erro ao enviar {github_path}: Status {put_response.status_code} - {put_response.text}"}

    

