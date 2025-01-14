# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################


def load_chagelog(repo_name):
    """
    Method to load the .env file located in the two folders above the script.
    """
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Work_Environment", f"{repo_name}", "SoftwareDevelopment", f"{repo_name}", "Changelog.env"))
    print(env_path)
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f".env carregado de: {env_path}")
    else:
        print(f"Erro: Arquivo  não encontrado em {env_path}")

def load_env(repo_name):
    """
    Method to load the .env file located in the two folders above the script.
    """
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "environment.env"))
    print(env_path)
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f".env carregado de: {env_path}")
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Work_Environment", f"{repo_name}"))

        file_paths = {


            "PATH_SOFTWARE_DEVELOPMENT_init_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "__init__.py"),
            "PATH_SOFTWARE_DEVELOPMENT_PY_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "main.py"),
            "PATH_SOFTWARE_DEVELOPMENT_TXT_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "main_software_save.txt"),
            "PATH_SOFTWARE_DEVELOPMENT_config_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "config.py"),

            "PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "utils", "__init__.py"),
            "PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "utils", "file_utils.py"),

            "PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "modules", "__init__.py"),
            "PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "modules", "module1.py"),
            "PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "modules", "module2.py"),

            "PATH_SOFTWARE_DEVELOPMENT_services___init___ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "services", "__init__.py"),
            "PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "services", "service1.py"),
            "PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "services", "service2.py"),

            "PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "tests", "__init__.py"),
            "PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "tests", "test_module1.py"),
            "PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "tests", "test_module2.py"),
            "PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "tests", "test_service1.py"),
            "PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "tests", "test_service2.py"),

            "PATH_SOFTWARE_DEVELOPMENT_Example_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "Examples", "Example.py"),

            "PATH_SOFTWARE_DEVELOPMENT_Requirements_ENV": os.path.join(base_path, "SoftwareDevelopment", "requirements.txt"),
            "PATH_SOFTWARE_DEVELOPMENT_SendToPip": os.path.join(base_path, "SoftwareDevelopment", "SendToPip.py"),
            "PATH_SOFTWARE_DEVELOPMENT_gitignore_ENV": os.path.join(base_path, "SoftwareDevelopment", ".gitignore"),
            "PATH_DOCUMENTACAO_ENV": os.path.join(base_path, "SoftwareDevelopment", "README.md"),
            "PATH_DOCUMENTACAO_LICENSE_ENV": os.path.join(base_path, "SoftwareDevelopment", "LICENSE.txt"),
            "PATH_DOCUMENTACAO_setup_ENV": os.path.join(base_path, "SoftwareDevelopment", "setup.py"),
            "PATH_pyproject": os.path.join(base_path, "SoftwareDevelopment", "pyproject.toml"),
            "PATH_NAME_DOC_PRE_PROJETO_ENV": os.path.join(base_path, "PreProject", "doc.txt"),
            "PATH_NOME_DO_CRONOGRAMA_ENV": os.path.join(base_path, "ScheduleAndSpreadsheet", "Schedule", "Schedule.txt"),
            "PATH_PLANILHA_PROJETO_ENV": os.path.join(base_path, "ScheduleAndSpreadsheet", "Spreadsheet", "Spreadsheet.txt"),
            "PATH_ROADMAP_ENV": os.path.join(base_path, "Roadmap", "Roadmap.txt"),
            "PATH_ANALISE_ENV": os.path.join(base_path, "AnalysisRequirements", "AnalysisRequirements.txt"),

            "PATH_Changelog": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "Changelog.env"),
        
        }
     
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "environment.txt")), "w") as file:
            for key, value in file_paths.items():
                file.write(f"{key}={value}\n")

       

    else:
        print(f"Erro: Arquivo environment.env não encontrado em {env_path}")


def create_env(variables, env):
    """
    Cria um arquivo .env com as variáveis fornecidas.
    Se o arquivo já existir, ele será sobrescrito.

    Args:
        variables (dict): Um dicionário com chave-valor representando as variáveis de ambiente.
    """
    with open(env, "w") as file:
        for key, value in variables.items():
            file.write(f"{key}={value}\n")
    return True

def incrementar_versao_em_arquivo(nome_arquivo):
    padrao = r'version="(\d+)\.(\d+)\.(\d+)"'
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()
    match = re.search(padrao, conteudo)
    if match:
        major, minor, patch = map(int, match.groups())
        patch += 1
        nova_versao = f'{major}.{minor}.{patch}'
        conteudo_atualizado = re.sub(padrao, f'version="{nova_versao}"', conteudo)  # Atualiza o conteúdo
        print(f"Nova versão: {nova_versao}")
    else:
        raise ValueError("Versão não encontrada no arquivo.")
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo_atualizado)

def init_env(repo_name):
    try:
        os.makedirs(os.path.abspath(os.path.join(os.path.dirname(__file__), "Work_Environment", f"{repo_name}", "SoftwareDevelopment", f"{repo_name}")))
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "Work_Environment", f"{repo_name}", "SoftwareDevelopment", f"{repo_name}", "Changelog.env")), "x") as file:
            file.write('version="0.0.0"')

        incrementar_versao_em_arquivo(os.path.abspath(os.path.join(os.path.dirname(__file__), "Work_Environment", f"{repo_name}", "SoftwareDevelopment", f"{repo_name}", "Changelog.env")))

        load_chagelog(repo_name)

        version = os.getenv("version")
        print(version)
    except Exception as e:
        print(e)
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Work_Environment", f"{repo_name}"))

    file_paths = {


        "PATH_SOFTWARE_DEVELOPMENT_init_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "__init__.py"),
        "PATH_SOFTWARE_DEVELOPMENT_PY_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "main.py"),
        "PATH_SOFTWARE_DEVELOPMENT_TXT_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "main_software_save.txt"),
        "PATH_SOFTWARE_DEVELOPMENT_config_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "config.py"),

        "PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "utils", "__init__.py"),
        "PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "utils", "file_utils.py"),

        "PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "modules", "__init__.py"),
        "PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "modules", "module1.py"),
        "PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "modules", "module2.py"),

        "PATH_SOFTWARE_DEVELOPMENT_services___init___ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "services", "__init__.py"),
        "PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "services", "service1.py"),
        "PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "services", "service2.py"),

        "PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "tests", "__init__.py"),
        "PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "tests", "test_module1.py"),
        "PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "tests", "test_module2.py"),
        "PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "tests", "test_service1.py"),
        "PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV": os.path.join(base_path, "SoftwareDevelopment",f"{repo_name}", "tests", "test_service2.py"),

        "PATH_SOFTWARE_DEVELOPMENT_Example_ENV": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "Examples", "Example.py"),
        "PATH_SOFTWARE_DEVELOPMENT_SendToPip": os.path.join(base_path, "SoftwareDevelopment", "SendToPip.py"),

        "PATH_SOFTWARE_DEVELOPMENT_Requirements_ENV": os.path.join(base_path, "SoftwareDevelopment", "requirements.txt"),
        "PATH_SOFTWARE_DEVELOPMENT_gitignore_ENV": os.path.join(base_path, "SoftwareDevelopment", ".gitignore"),
        "PATH_DOCUMENTACAO_ENV": os.path.join(base_path, "SoftwareDevelopment", "README.md"),
        "PATH_DOCUMENTACAO_LICENSE_ENV": os.path.join(base_path, "SoftwareDevelopment", "LICENSE.txt"),
        "PATH_DOCUMENTACAO_setup_ENV": os.path.join(base_path, "SoftwareDevelopment", "setup.py"),
        "PATH_pyproject": os.path.join(base_path, "SoftwareDevelopment", "pyproject.toml"),
        "PATH_NAME_DOC_PRE_PROJETO_ENV": os.path.join(base_path, "PreProject", "doc.txt"),
        "PATH_NOME_DO_CRONOGRAMA_ENV": os.path.join(base_path, "ScheduleAndSpreadsheet", "Schedule", "Schedule.txt"),
        "PATH_PLANILHA_PROJETO_ENV": os.path.join(base_path, "ScheduleAndSpreadsheet", "Spreadsheet", "Spreadsheet.txt"),
        "PATH_ROADMAP_ENV": os.path.join(base_path, "Roadmap", "Roadmap.txt"),
        "PATH_ANALISE_ENV": os.path.join(base_path, "AnalysisRequirements", "AnalysisRequirements.txt"),

        "PATH_Changelog": os.path.join(base_path, "SoftwareDevelopment", f"{repo_name}", "Changelog.env"),
        "PATH_Env": os.path.join(os.path.dirname(__file__), "environment.env"),
        "PATH_Envtxt": os.path.join(os.path.dirname(__file__), "environment.txt")
    }
    
    try:
        for path in file_paths.values():
            os.makedirs(os.path.dirname(path), exist_ok=True)
            if not os.path.exists(path):
                with open(path, "w") as file:
                    file.write("")  
        for key in list(os.environ.keys()):
            if key.endswith('_ENV'):
                del os.environ[key]                                                                                                                                                                     
        flag = create_env(file_paths, os.path.abspath(os.path.join(os.path.dirname(__file__), "environment.env")))
        load_env(repo_name)

        PATH_SOFTWARE_DEVELOPMENT_SendToPip = os.getenv("PATH_SOFTWARE_DEVELOPMENT_SendToPip")
        repo_namereplace = repo_name.replace("A-I-O-R-G/", "")
        with open(PATH_SOFTWARE_DEVELOPMENT_SendToPip, "w") as f:
            f.write(f"""


import re
import os 
import shutil
import subprocess


def incrementar_versao_em_arquivo(nome_arquivo):
    padrao = r'version="(\d+)\.(\d+)\.(\d+)"'
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()
    
    match = re.search(padrao, conteudo)
    if match:
        major, minor, patch = map(int, match.groups())
        patch += 1
        if patch > 99:  # Quando o patch chega a 100
            patch = 0
            minor += 1
            if minor > 99:  # Quando o minor chega a 100
                minor = 0
                major += 1
        nova_versao = f'{{major}}.{{minor:02}}.{{patch:02}}'  # Formata com dois dígitos
        conteudo_atualizado = re.sub(padrao, f'version="{{nova_versao}}"', conteudo)  # Atualiza o conteúdo
        print(f"Nova versão: {{nova_versao}}")
    else:
        raise ValueError("Versão não encontrada no arquivo.")
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo_atualizado)

try:
    shutil.rmtree("dist")
except Exception as e:
    print(e)
    
try:
    shutil.rmtree("build")
except Exception as e:
    print(e)
    
try:
    shutil.rmtree("{repo_namereplace}.egg-info")
except Exception as e:
    print(e)

padrao = r'version="(\d+)\.(\d+)\.(\d+)"'
with open("setup.py", "r", encoding="utf-8") as f:
    conteudo = f.read()
match = re.search(padrao, conteudo)
if match:
    major, minor, patch = map(int, match.groups())
    versao = f'{{major}}.{{minor}}.{{patch}}'
    try:
        shutil.rmtree(f"{repo_namereplace}-{{versao}}")
    except Exception as e:
        print(e)

else:
    raise ValueError("Versão não encontrada no arquivo.")

incrementar_versao_em_arquivo("setup.py")



comand = [
"python",
"setup.py",
"sdist",
"bdist_wheel"
]
subprocess.run(comand, shell=True)



comand = [
"twine",
"upload",
"dist/*"
]
subprocess.run(comand, shell=True)

            """)



    except Exception as e:
        print(e)