# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################


def load_env():
    """
    Method to load the .env file located in the two folders above the script.
    """
    # Caminho relativo para o .env
    script_dir = os.path.dirname(__file__)
    env_path = os.path.abspath(os.path.join(script_dir, "environment.env"))
    print(env_path)
    # Carregar o arquivo .env se ele existir
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f".env carregado de: {env_path}")
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

def init_env(repo_name):
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Work_Environment", f"{repo_name}"))
    file_paths = {


        "PATH_SOFTWARE_DEVELOPMENT_init_ENV": os.path.join(base_path, "SoftwareDevelopment", "CoreApp", "__init__.py"),
        "PATH_SOFTWARE_DEVELOPMENT_PY_ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "main.py"),
        "PATH_SOFTWARE_DEVELOPMENT_TXT_ENV": os.path.join(base_path, "SoftwareDevelopment", "CoreApp", "main_software_save.txt"),
        "PATH_SOFTWARE_DEVELOPMENT_config_ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "config.py"),

        "PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "utils", "__init__.py"),
        "PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "utils", "file_utils.py"),

        "PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "modules", "__init__.py"),
        "PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "modules", "module1.py"),
        "PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "modules", "module2.py"),

        "PATH_SOFTWARE_DEVELOPMENT_services___init___ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "services", "__init__.py"),
        "PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "services", "service1.py"),
        "PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "services", "service2.py"),

        "PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "tests", "__init__.py"),
        "PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "tests", "test_module1.py"),
        "PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "tests", "test_module2.py"),
        "PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "tests", "test_service1.py"),
        "PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV": os.path.join(base_path, "SoftwareDevelopment","CoreApp", "tests", "test_service2.py"),

        "PATH_SOFTWARE_DEVELOPMENT_Example_ENV": os.path.join(base_path, "SoftwareDevelopment", "CoreApp", "Examples", "Example.py"),

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
        "PATH_CoreApp": os.path.join(base_path, "SoftwareDevelopment", "CoreApp")
    
    }
    for path in file_paths.values():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            with open(path, "w") as file:
                file.write("")  
    for key in list(os.environ.keys()):
        if key.endswith('_ENV'):
            del os.environ[key]                                                                                                                                                                     
    flag = create_env(file_paths, os.path.abspath(os.path.join(os.path.dirname(__file__), "environment.env")))
    load_env()



    PATH_SOFTWARE_DEVELOPMENT_init_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_init_ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_init_ENV, "w") as file:
        file.write("###init###")

    PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV, "w") as file:
        file.write("###init###")

    PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV, "w") as file:
        file.write("###init###")


    PATH_SOFTWARE_DEVELOPMENT_services___init___ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_services___init___ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_services___init___ENV, "w") as file:
        file.write("###init###")


    PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV, "w") as file:
        file.write("###init###")


    PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV, "w") as file:
        file.write("###init###")


    PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV, "w") as file:
        file.write("###init###")


    PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV, "w") as file:
        file.write("###init###")


    PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV, "w") as file:
        file.write("###init###")


    PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV, "w") as file:
        file.write("###init###")


    PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV, "w") as file:
        file.write("###init###")


    PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV, "w") as file:
        file.write("###init###")


    PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV, "w") as file:
        file.write("###init###")


    PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV, "w") as file:
        file.write("###init###")


    PATH_SOFTWARE_DEVELOPMENT_Example_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_Example_ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_Example_ENV, "w") as file:
        file.write("###init###")


    PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV, "w") as file:
        file.write("###init###")

    PATH_SOFTWARE_DEVELOPMENT_config_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_config_ENV")
    with open(PATH_SOFTWARE_DEVELOPMENT_config_ENV, "w") as file:
        file.write("###init###")
