import threading
import subprocess
import os
def initchat():
    diretório_coreui = os.path.join(os.path.dirname(__file__), 'CoreUi', 'Chat')
    os.chdir(diretório_coreui)  # Mudando para o diretório 
    comando_terminal = ['python', 'main.py']  # Executando main.py dentro do diretório 
    subprocess.Popen(comando_terminal, shell=True)
initchat()