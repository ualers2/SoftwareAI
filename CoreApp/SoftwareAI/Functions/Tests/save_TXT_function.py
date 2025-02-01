
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################

def save_TXT(string, filexname, letra, path):
    # Construir o caminho completo do arquivo
    full_path = os.path.join(path, filexname)
    
    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Salvar o conteúdo no arquivo
    with open(full_path, letra, encoding="utf-8") as file:
        file.write(f'\n{string}')

    return {"status": "success", "message": f"Arquivo txt salvo com sucesso em {full_path}"}