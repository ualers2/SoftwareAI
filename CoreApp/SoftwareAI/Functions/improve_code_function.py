

#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import *
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################

def improve_code_and_create_pull_request(
                                        repo_owner: str,
                                        repo_name: str, 
                                        branch_name: str,
                                        file_path: str, 
                                        commit_message: str, 
                                        improvements: str,
                                        pr_title: str, 
                                        token: str
                                        ):
    """
    Realiza melhorias no código e cria um pull request no repositório GitHub dentro de uma organização.
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Verificar se a branch principal existe (ex: 'main')
    repo_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches/main"
    response = requests.get(repo_url, headers=headers)
    
    if response.status_code == 404:  # Branch principal não existe
        print("Branch 'main' não encontrada. Criando a branch 'main' a partir de um commit inicial.")
        # Criar um commit inicial vazio
        create_commit_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/commits"
        commit_data = {
            "message": "Initial commit",
            "tree": "",  # Crie um commit com uma árvore vazia
            "parents": []
        }
        response = requests.post(create_commit_url, headers=headers, json=commit_data)
        if response.status_code != 201:
            print(f"Erro ao criar o commit inicial: {response.content}")
            return
        commit_sha = response.json()['sha']

        # Criar a branch 'main' usando o commit inicial
        create_branch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs"
        branch_data = {
            "ref": "refs/heads/main",
            "sha": commit_sha
        }
        response = requests.post(create_branch_url, headers=headers, json=branch_data)
        if response.status_code != 201:
            print(f"Erro ao criar a branch 'main': {response.content}")
            return
        print("Branch 'main' criada com sucesso.")

    # Obter SHA do branch principal
    response = requests.get(repo_url, headers=headers)
    main_sha = response.json().get('commit', {}).get('sha')
    if not main_sha:
        print("Erro ao obter SHA do branch principal.")
        return

    # Criar uma nova branch baseada no branch principal
    new_branch_data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": main_sha
    }
    create_branch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs"
    response = requests.post(create_branch_url, headers=headers, json=new_branch_data)
    if response.status_code != 201:
        print(f"Erro ao criar o branch: {response.content}")
        return

    # Verificar se o arquivo já existe no branch principal
    file_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}?ref=main"
    response = requests.get(file_url, headers=headers)
    file_sha = None
    if response.status_code == 200:
        file_sha = response.json().get('sha')  # Obter SHA do arquivo existente

    # Adicionar ou atualizar o arquivo no novo branch
    name_filepath = os.path.basename(file_path)
    file_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{name_filepath}"
    improved_content_base64 = base64.b64encode(improvements.encode()).decode()
    
    # Verificar se o arquivo já existe para obter o SHA
    response = requests.get(file_url, headers=headers, params={"ref": branch_name})
    if response.status_code == 200:
        file_sha = response.json().get("sha")  # SHA do arquivo existente
    else:
        file_sha = None  # Arquivo novo, sem SHA

    # Dados para a requisição PUT
    file_data = {
        "message": commit_message,
        "content": improved_content_base64,
        "branch": branch_name
    }
    if file_sha:
        file_data["sha"] = file_sha  # Incluir o SHA para atualização

    response = requests.put(file_url, headers=headers, json=file_data)
    if response.status_code not in [201, 200]:
        print(f"Erro ao adicionar o arquivo: {response.content}")
        return

    # Criar o pull request
    pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    pr_data = {
        "title": pr_title,
        "body": commit_message,
        "head": branch_name,
        "base": "main"  # Supondo que a branch principal seja 'main'
    }
    pr_response = requests.post(pr_url, json=pr_data, headers=headers)
    if pr_response.status_code == 201:
        print("Pull request criado com sucesso!")
        return {"status": "success", "message": "Pull request criado com sucesso", "pull_request_url": pr_response.json()['html_url']}
    else:
        print(f"Erro ao criar o pull request: {pr_response.content}")
        return {"status": "error", "message": pr_response.json()}


