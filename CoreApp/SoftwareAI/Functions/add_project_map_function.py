
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

def add_projectmap_to_github(
                            timeline_file_path: str,
                            spreadsheet_file_path: str,
                            pre_project_file_path: str,
                            Roadmap_file_path: str,
                            analise_file_path: str,
                            repo_name: str,
                            token: str
                        ):
    def reconhecer_e_upar_spreadsheet_and_timeline_file_path(directory):
            
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                with open(file_path, "rb") as file:
                    content = file.read()
                    encoded_content = base64.b64encode(content).decode("utf-8")

                relative_path = os.path.relpath(file_path, start=directory)  
                github_path = relative_path.replace("\\", "/")  

                url = f"https://api.github.com/repos/A-I-O-R-G/{repo_name}/contents/AppMap/SpreadsheetAndTimeline/{github_path}"

                response = requests.get(url, headers={"Authorization": f"token {token}"})
                sha = response.json().get("sha") if response.status_code == 200 else None

                data = {
                    "message": f"Add {filename}",
                    "content": encoded_content,
                    "branch": "main"
                }
                if sha:
                    data["sha"] = sha 

                response = requests.put(url, json=data, headers={"Authorization": f"token {token}"})
                print(f"Arquivo: {github_path} - Status: {response.status_code} ")
    
    def reconhecer_e_upar_pre_project_file_path(directory):
            
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                with open(file_path, "rb") as file:
                    content = file.read()
                    encoded_content = base64.b64encode(content).decode("utf-8")

                relative_path = os.path.relpath(file_path, start=directory)  
                github_path = relative_path.replace("\\", "/")  

                url = f"https://api.github.com/repos/A-I-O-R-G/{repo_name}/contents/AppMap/PreProject/{github_path}"

                response = requests.get(url, headers={"Authorization": f"token {token}"})
                sha = response.json().get("sha") if response.status_code == 200 else None

                data = {
                    "message": f"Add {filename}",
                    "content": encoded_content,
                    "branch": "main"
                }
                if sha:
                    data["sha"] = sha 

                response = requests.put(url, json=data, headers={"Authorization": f"token {token}"})
                print(f"Arquivo: {github_path} - Status: {response.status_code} ")
    
    def reconhecer_e_upar_Roadmap(directory):
            
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                with open(file_path, "rb") as file:
                    content = file.read()
                    encoded_content = base64.b64encode(content).decode("utf-8")

                relative_path = os.path.relpath(file_path, start=directory)  
                github_path = relative_path.replace("\\", "/")  

                url = f"https://api.github.com/repos/A-I-O-R-G/{repo_name}/contents/AppMap/RoadMap/{github_path}"

                response = requests.get(url, headers={"Authorization": f"token {token}"})
                sha = response.json().get("sha") if response.status_code == 200 else None

                data = {
                    "message": f"Add {filename}",
                    "content": encoded_content,
                    "branch": "main"
                }
                if sha:
                    data["sha"] = sha 

                response = requests.put(url, json=data, headers={"Authorization": f"token {token}"})
                print(f"Arquivo: {github_path} - Status: {response.status_code} ")
    
    def reconhecer_e_upar_analise_file_path(directory):
            
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                with open(file_path, "rb") as file:
                    content = file.read()
                    encoded_content = base64.b64encode(content).decode("utf-8")

                relative_path = os.path.relpath(file_path, start=directory)  
                github_path = relative_path.replace("\\", "/")  

                url = f"https://api.github.com/repos/A-I-O-R-G/{repo_name}/contents/AppMap/Analisys/{github_path}"

                response = requests.get(url, headers={"Authorization": f"token {token}"})
                sha = response.json().get("sha") if response.status_code == 200 else None

                data = {
                    "message": f"Add {filename}",
                    "content": encoded_content,
                    "branch": "main"
                }
                if sha:
                    data["sha"] = sha 

                response = requests.put(url, json=data, headers={"Authorization": f"token {token}"})
                print(f"Arquivo: {github_path} - Status: {response.status_code} ")
    

    reconhecer_e_upar_spreadsheet_and_timeline_file_path(os.path.dirname(timeline_file_path))
    
    reconhecer_e_upar_spreadsheet_and_timeline_file_path(os.path.dirname(spreadsheet_file_path))
    
    reconhecer_e_upar_pre_project_file_path(os.path.dirname(pre_project_file_path))
    
    reconhecer_e_upar_Roadmap(os.path.dirname(Roadmap_file_path))
    
    reconhecer_e_upar_analise_file_path(os.path.dirname(analise_file_path))
    return {"status": "success", "message": "Arquivos, adicionados com sucesso ao repositorio"}

