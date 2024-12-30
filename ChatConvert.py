import threading
import subprocess
import os

def initchatconvert():
    # Definindo o diretório correto (onde está o )
    diretório_coreui = os.path.join(os.path.dirname(__file__), 'CoreUi', 'Chat')
    os.chdir(diretório_coreui)  # Mudando para o diretório 

    comando_terminal = ['python', 'Convert.py']  # Executando main.py dentro do diretório 
    subprocess.run(comando_terminal, shell=True)
initchatconvert()