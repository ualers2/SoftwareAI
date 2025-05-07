from typing_extensions import TypedDict, List
import requests
import base64
from agents import function_tool
import os


class Data(TypedDict):
    search_dir: str
    preferred_name: str
    fallback_names: List[str]
    

@function_tool
def autogetlocalfilecontent(data: Data):
    try:
        data_FINAL = data["data"]
        search_dir = data_FINAL["search_dir"]
        preferred_name = data_FINAL["preferred_name"]
        fallback_names = data_FINAL["fallback_names"]
    except Exception as eroo1:
        print(eroo1)
        search_dir = data["search_dir"]
        preferred_name = data["preferred_name"]
        fallback_names = data["fallback_names"]
    print("autogetlocalfilecontent Prestes a iniciar")
    """
    Busca o conteúdo de um arquivo local dentro de um diretório, com preferência por um nome específico.

    Args:
        search_dir (str): Diretório base para iniciar a busca.
        preferred_name (str): Nome preferido do arquivo.
        fallback_names (list): Lista de nomes alternativos a serem procurados caso o preferido não seja encontrado.

    Returns:
        dict: {
            'file_path': caminho completo do arquivo encontrado,
            'content': conteúdo do arquivo como string
        }
        ou erro:
        dict: { 'error': 'mensagem de erro' }
    """
    if fallback_names is None:
        fallback_names = ["preplanejamento.md", "planejamento.md", "plano.md"]

    if not os.path.exists(search_dir):
        return {"error": f"Diretório '{search_dir}' não encontrado."}

    # Busca por arquivos
    for root, dirs, files in os.walk(search_dir):
        if preferred_name in files:
            path = os.path.join(root, preferred_name)
            with open(path, 'r', encoding='utf-8') as f:
                return {'file_path': path, 'content': f.read()}

    # Tenta nomes alternativos
    for root, dirs, files in os.walk(search_dir):
        for alt_name in fallback_names:
            if alt_name in files:
                path = os.path.join(root, alt_name)
                with open(path, 'r', encoding='utf-8') as f:
                    return {'file_path': path, 'content': f.read()}

    return {"error": "Nenhum arquivo de planejamento encontrado."}