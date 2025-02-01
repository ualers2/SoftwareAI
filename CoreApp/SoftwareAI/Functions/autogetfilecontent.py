import requests

def autogetfilecontent(repo_name, file_path, branch_name, companyname, github_token):

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