# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################


def load_env(env):
    """
    Method to load the .env file located in the two folders above the script.
    """
    # Caminho relativo para o .env
    script_dir = os.path.dirname(__file__)
    env_path = os.path.abspath(os.path.join(script_dir, env))
    print(env_path)
    # Carregar o arquivo .env se ele existir
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f".env carregado de: {env_path}")
    else:
        print(f"Erro: Arquivo environment.env não encontrado em {env_path}")


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

incrementar_versao_em_arquivo(os.path.abspath(os.path.join(os.path.dirname(__file__), "Changelog.env")))

load_env("Changelog.env")


version = os.getenv("version")
print(version)