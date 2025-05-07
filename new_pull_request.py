import os
import git
import time
from requests.auth import HTTPBasicAuth
import base64

import zipfile
import requests
from dotenv import load_dotenv

os.chdir(os.path.join(os.path.dirname(__file__)))

# headers = {
#     "Authorization": f"token {token}",
#     "Accept": "application/vnd.github.v3+json"
# }
# colaboradores = [
#     "CloudArchitectt", "TigraoEscritor", "NexGenCoder756",
#     "SignalMaster727", "QuantummCore", "BobGerenteDeProjeto",
#     "DallasEquipeDeSolucoes"
# ]

# for colaborador in colaboradores:
#     collaborator_url = f"https://api.github.com/repos/{repo_name}/collaborators/{colaborador}"
#     collaborator_data = {"permission": "admin"}
    
#     collaborator_response = requests.put(collaborator_url, headers=headers, json=collaborator_data)
    
#     if collaborator_response.status_code in [201, 204]:
#         print(f"Colaborador {colaborador} adicionado com sucesso com permissões de administrador.")
#     else:
#         print(f"Falha ao adicionar {colaborador}. Status: {collaborator_response.status_code}, Resposta: {collaborator_response.json()}")

import os
import time
import base64
import requests
from dotenv import load_dotenv

# Configurações iniciais
main_branch = "main"
new_branch = f"pr-{int(time.time())}"  # nome da branch criada dinamicamente

load_dotenv("keys.env")
token = os.getenv("github_token")
repo_name = os.getenv("repo_name")
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# Função para carregar regras do .gitignore
def load_gitignore(directory):
    gitignore_path = os.path.join(directory, ".gitignore")
    ignored_paths = set()
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignored_paths.add(os.path.normpath(line))
    return ignored_paths

# Função para verificar se um arquivo/diretório deve ser ignorado
def is_ignored(file_path, base_directory, ignored_paths):
    rel_path = os.path.relpath(file_path, start=base_directory)
    for pattern in ignored_paths:
        if rel_path.startswith(pattern):
            return True
    return False

# Cria uma nova branch a partir da branch main
def create_new_branch():
    # Obtém o SHA da última commit da branch main
    ref_url = f"https://api.github.com/repos/{repo_name}/git/ref/heads/{main_branch}"
    r = requests.get(ref_url, headers=headers)
    if r.status_code != 200:
        print("Erro ao obter referência da branch main:", r.status_code, r.json())
        exit(1)
    main_sha = r.json()["object"]["sha"]

    # Cria a nova branch
    create_branch_url = f"https://api.github.com/repos/{repo_name}/git/refs"
    payload = {
        "ref": f"refs/heads/{new_branch}",
        "sha": main_sha
    }
    r = requests.post(create_branch_url, json=payload, headers=headers)
    if r.status_code not in [200, 201]:
        print("Erro ao criar nova branch:", r.status_code, r.json())
        exit(1)
    print(f"Nova branch criada: {new_branch}")

# Função para enviar os arquivos para a branch especificada
def upload_files_to_github(branch, directorys=None, file_path_request=None):
    if file_path_request is not None:
        file_directory = os.path.dirname(file_path_request)
        file_name = os.path.basename(file_path_request)
        file_directory_final = os.path.abspath(file_directory)
        with open(file_path_request, "rb") as file:
            content = file.read()
        encoded_content = base64.b64encode(content).decode("utf-8")

        relative_path = os.path.relpath(file_path_request, start=file_directory_final).replace("\\", "/")
        url = f"https://api.github.com/repos/{repo_name}/contents/{relative_path}"
        
        # Verifica se o arquivo já existe na branch de destino
        params = {"ref": branch}
        response = requests.get(url, headers=headers, params=params)
        sha = response.json().get("sha") if response.status_code == 200 else None

        data = {
            "message": f"Add {file_name}",
            "content": encoded_content,
            "branch": branch
        }
        if sha:
            data["sha"] = sha

        put_response = requests.put(url, json=data, headers=headers)
        print(f"Arquivo: {relative_path} - Status: {put_response.status_code}")
        time.sleep(1)

    elif file_path_request is None:

        for directory in directorys:
            directory = os.path.abspath(directory)
            ignored_paths = load_gitignore(directory)  # Carrega as regras do .gitignore

            for dirpath, dirnames, filenames in os.walk(directory):
                if is_ignored(dirpath, directory, ignored_paths):
                    print(f"Ignorando diretório: {dirpath}")
                    continue
                
                for filename in filenames:
                    # Ignorar arquivos temporários ou de log
                    if filename.endswith(".log") or filename == "DumpStack.log.tmp":
                        print(f"Ignorando arquivo temporário ou de log: {filename}")
                        continue

                    file_path = os.path.join(dirpath, filename)
                    if is_ignored(file_path, directory, ignored_paths):
                        print(f"Ignorando arquivo: {file_path}")
                        continue  

                    with open(file_path, "rb") as file:
                        content = file.read()
                    encoded_content = base64.b64encode(content).decode("utf-8")

                    relative_path = os.path.relpath(file_path, start=directory).replace("\\", "/")
                    url = f"https://api.github.com/repos/{repo_name}/contents/{relative_path}"
                    
                    # Verifica se o arquivo já existe na branch de destino
                    params = {"ref": branch}
                    response = requests.get(url, headers=headers, params=params)
                    sha = response.json().get("sha") if response.status_code == 200 else None

                    data = {
                        "message": f"Add {filename}",
                        "content": encoded_content,
                        "branch": branch
                    }
                    if sha:
                        data["sha"] = sha

                    put_response = requests.put(url, json=data, headers=headers)
                    print(f"Arquivo: {relative_path} - Status: {put_response.status_code}")
                    time.sleep(1)

# Cria a nova branch para o pull request
create_new_branch()

# Determina o diretório atual para envio dos arquivos
diretorio_script = os.path.dirname(os.path.abspath(__file__))
app_diretorio_script = os.path.join(diretorio_script)
file_path_to_upload = os.path.join(diretorio_script, "library_hub_app.py")


upload_files_to_github(directorys=[app_diretorio_script], branch=new_branch)


title = """
First stable version of the Softwareai Chat
"""

body = """


#63
#51
#42
#28
#18
#10


"""

# Cria um pull request da nova branch para a branch main
pr_url = f"https://api.github.com/repos/{repo_name}/pulls"
pr_payload = {
    "title": title,
    "body": f"{body}",
    "head": new_branch,
    "base": main_branch
}
pr_response = requests.post(pr_url, json=pr_payload, headers=headers)
if pr_response.status_code in [200, 201]:
    print("Pull Request criado com sucesso.")
else:
    print("Erro ao criar Pull Request:", pr_response.status_code, pr_response.json())
