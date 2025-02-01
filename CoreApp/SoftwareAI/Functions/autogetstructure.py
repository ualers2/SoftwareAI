import requests

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
