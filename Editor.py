import threading
import subprocess
import os
def initeditor():
    diretório_coreui = os.path.join(os.path.dirname(__file__), 'CoreUi', 'Editor')
    os.chdir(diretório_coreui)
    comando_terminal = ['python', 'main.py'] 
    subprocess.run(comando_terminal, shell=True)
initeditor()