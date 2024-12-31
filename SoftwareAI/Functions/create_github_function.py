
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################


def create_github_repo_and_upload(repo_name: str, 
                                repo_description: str,
                                setup_file_path: str,
                                requirements_file_path: str,
                                LICENSE_file_path: str,
                                pyproject_file_path: str,
                                readme_file_path: str,
                                PATH_SOFTWARE_DEVELOPMENT_init_ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_PY_ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_config_ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_services___init___ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV: str,
                                PATH_SOFTWARE_DEVELOPMENT_Example_ENV: str,

                                token: str
                                
                                ):
    repo_url = f"https://api.github.com/orgs/A-I-O-R-G/repos"

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    repo_data = {
        "name": repo_name,
        "description": repo_description,
        "private": False
    }
    response = requests.post(repo_url, json=repo_data, headers=headers)
    if response.status_code == 201:
        print(f"Repositório {repo_name} criado com sucesso na organização A-I-O-R-G!")
    else:
        print(f"Falha ao criar o repositório. Status: {response.status_code}, Resposta: {response.json()}")
        return {"status": "error", "message": response.json()}

    # URL para fazer upload dos arquivos
    repo_git_url = f"https://api.github.com/repos/A-I-O-R-G/{repo_name}/contents/"

    def upload_file_to_github(file_path, commit_message, pathgithub=""):
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as file:
            file_content = file.read()
            file_base64 = base64.b64encode(file_content).decode('utf-8')

        upload_data = {
            "message": commit_message,
            "content": file_base64
        }
        if pathgithub != "":
            file_url = repo_git_url + pathgithub + "/" + file_name
        else:
            file_url = repo_git_url + file_name

        upload_response = requests.put(file_url, json=upload_data, headers=headers)

        if upload_response.status_code == 201:
            print(f"Arquivo {file_name} carregado com sucesso no repositório.")
        else:
            try:
                print(f"Falha ao fazer upload do arquivo {file_name}. Status: {upload_response.status_code} {upload_response.content}")
            except:
                try:
                    print(f"Falha ao fazer upload do arquivo {file_name}. Status: {upload_response.status_code} {upload_response.json()}")
                except:
                    print(f"Falha ao fazer upload do arquivo {file_name}. Status: {upload_response.status_code} {upload_response.json}")


            return {"status": "error", "message": upload_response.json()}

    # Upload do arquivo README.md
    upload_file_to_github(readme_file_path, "Adicionando documentação")

    # Upload do arquivo setup.py
    upload_file_to_github(setup_file_path, "Adicionando setup.py")

    # Upload do arquivo requirements.txt
    upload_file_to_github(requirements_file_path, "Adicionando requirements.txt")

    # Upload do arquivo LICENSE.txt
    upload_file_to_github(LICENSE_file_path, "Adicionando LICENSE")

    # Upload do arquivo pyproject.toml
    upload_file_to_github(pyproject_file_path, "Adicionando pyproject.toml")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_init_ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_init_ENV", "CoreApp")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_PY_ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_PY_ENV", "CoreApp")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_config_ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_config_ENV", "CoreApp")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV", "CoreApp/utils")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV", "CoreApp/utils")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV", "CoreApp/modules")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV", "CoreApp/modules")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV", "CoreApp/modules")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_services___init___ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_services___init___ENV", "CoreApp/services")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV", "CoreApp/services")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV", "CoreApp/services")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV", "CoreApp/tests")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV", "CoreApp/tests")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV", "CoreApp/tests")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV", "CoreApp/tests")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV", "CoreApp/tests")

    # Upload do arquivo 
    upload_file_to_github(PATH_SOFTWARE_DEVELOPMENT_Example_ENV, "Adicionando PATH_SOFTWARE_DEVELOPMENT_Example_ENV", "CoreApp/Examples")





    # # Upload do CoreApp
    # upload_codes_to_github(f"{CoreApp_path}")


    # code_file_paths = os.listdir(CoreApp_path)
    # for code_file_path in code_file_paths:
    #     code_path = os.path.join(CoreApp_path, code_file_path)
    #     upload_file_to_github(code_path, "Adicionando código fonte")





    # Adicionando colaborador com permissões de administrador
    collaborator_url = f"https://api.github.com/repos/A-I-O-R-G/{repo_name}/collaborators/SignalMaster727"

    collaborator_data = {
        "permission": "admin"
    }

    collaborator_response = requests.put(collaborator_url, headers=headers, json=collaborator_data)

    if collaborator_response.status_code == 201 or collaborator_response.status_code == 204:
        print(f"Colaborador 'SignalMaster727' adicionado com sucesso com permissões de administrador.")
    else:
        print(f"Falha ao adicionar colaborador. Status: {collaborator_response.status_code}, Resposta: {collaborator_response.json()}")
        return {"status": "error", "message": collaborator_response.json()}


    # Adicionando colaborador com permissões de administrador
    collaborator_url = f"https://api.github.com/repos/A-I-O-R-G/{repo_name}/collaborators/NexGenCoder756"

    collaborator_data = {
        "permission": "admin"
    }

    collaborator_response = requests.put(collaborator_url, headers=headers, json=collaborator_data)

    if collaborator_response.status_code == 201 or collaborator_response.status_code == 204:
        print(f"Colaborador 'NexGenCoder756' adicionado com sucesso com permissões de administrador.")
    else:
        print(f"Falha ao adicionar colaborador. Status: {collaborator_response.status_code}, Resposta: {collaborator_response.json()}")
        return {"status": "error", "message": collaborator_response.json()}
    

    # Adicionando colaborador com permissões de administrador
    collaborator_url = f"https://api.github.com/repos/A-I-O-R-G/{repo_name}/collaborators/CloudArchitectt"

    collaborator_data = {
        "permission": "admin"
    }

    collaborator_response = requests.put(collaborator_url, headers=headers, json=collaborator_data)

    if collaborator_response.status_code == 201 or collaborator_response.status_code == 204:
        print(f"Colaborador 'CloudArchitectt' adicionado com sucesso com permissões de administrador.")
    else:
        print(f"Falha ao adicionar colaborador. Status: {collaborator_response.status_code}, Resposta: {collaborator_response.json()}")
        return {"status": "error", "message": collaborator_response.json()}

    return {"status": "success", "message": "Repositório, arquivos e colaborador adicionados com sucesso"}
