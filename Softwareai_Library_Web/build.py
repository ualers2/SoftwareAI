import subprocess
import os

os.chdir(os.path.join(os.path.dirname(__file__)))
# Adiciona o caminho do Docker Compose
os.environ["PATH"] += r";C:\Program Files\Docker\Docker\resources\bin"

def executar_comando(comando):
    """Executa um comando sem abrir um novo terminal (funciona dentro do contêiner)."""
    subprocess.run(comando, shell=True)


# executar_comando("docker-compose up --build")

executar_comando("docker-compose build library_agents_watcher")

executar_comando("docker-compose up -d library_agents_watcher")

executar_comando("docker-compose build library_tools_watcher")

executar_comando("docker-compose up -d library_tools_watcher")

# executar_comando("docker-compose build agent_library_hub")

# executar_comando("docker-compose up -d agent_library_hub")

# executar_comando("docker-compose build agent_library_webhook")

# executar_comando("docker-compose up -d agent_library_webhook")
