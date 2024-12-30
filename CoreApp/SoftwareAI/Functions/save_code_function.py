
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################

def save_code(code_string, name_script, file_type, path):
    # Definir a extensão com base no tipo de arquivo
    extensions = {"html": ".html", "js": ".js", "css": ".css", "py": ".py"}
    if file_type not in extensions:
        raise ValueError("Tipo de arquivo inválido. Use 'html', 'js' ,'py' ou 'css'.")

    # Construir o caminho completo do arquivo
    full_path = os.path.join(path, f"{name_script}{extensions[file_type]}")

    # Garantir que o diretório existe
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    
    # Salvar o conteúdo no arquivo
    with open(full_path, 'w', encoding="utf-8") as file:
        file.write(code_string)

    return {"status": "success", "message": f"Arquivo salvo com sucesso em {full_path}"}
    