import os
from typing_extensions import TypedDict, Any , Union
from agents import Agent, ModelSettings, function_tool, FileSearchTool, WebSearchTool, Runner


def listar_arquivos(pasta, ignorar_ocultos=True):
    caminhos_arquivos = []
    for root, dirs, files in os.walk(pasta):
        if ignorar_ocultos:
            # Ignora diretórios ocultos
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            files = [f for f in files if not f.startswith('.')]
        for nome_arquivo in files:
            caminho_completo = os.path.join(root, nome_arquivo)
            caminhos_arquivos.append(caminho_completo)
    return caminhos_arquivos

def ler_conteudos_arquivos(caminhos_arquivos):
    conteudos = []
    for caminho in caminhos_arquivos:
        try:
            with open(caminho, 'r', encoding='utf-8') as arquivo:
                conteudo = arquivo.read()
        except UnicodeDecodeError:
            # Caso o arquivo não seja texto ou não seja UTF-8, ignora ou trata como quiser
            conteudo = "[ARQUIVO BINÁRIO OU COM CODIFICAÇÃO DESCONHECIDA]"
        conteudos.append(conteudo)
    return conteudos

class FunctionData(TypedDict):
    path_project: str

@function_tool
def autolistlocalproject(data: FunctionData):
    try:
        data_FINAL = data["data"]
        path_project = data_FINAL["path_project"]
    except Exception as eroo1:
        print(eroo1)
        path_project = data["path_project"]
    caminhos_arquivos = listar_arquivos(path_project)
    conteudos_arquivos = ler_conteudos_arquivos(caminhos_arquivos)
    data = {
        "paths": caminhos_arquivos,
        "contents": conteudos_arquivos,
    }
    return data