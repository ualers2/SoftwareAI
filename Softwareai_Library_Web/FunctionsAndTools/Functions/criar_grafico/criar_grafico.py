import matplotlib.pyplot as plt
from typing_extensions import TypedDict, Any , Union
from agents import Agent, ModelSettings, function_tool, FileSearchTool, WebSearchTool, Runner

def criar_grafico1(tipo, dados, titulo="", xlabel="", ylabel="", salvar_em=None):
    """
    Cria e opcionalmente salva gráficos de linha, barra ou pizza.

    Args:
        tipo (str): Tipo de gráfico ('linha', 'barra', 'pizza').
        dados (dict): Dados para o gráfico.
        titulo (str): Título do gráfico.
        xlabel (str): Rótulo do eixo X (linha/barra).
        ylabel (str): Rótulo do eixo Y (linha/barra).
        legenda (list): Legenda opcional (linha/barra).
        salvar_em (str): Caminho do arquivo para salvar (ex: 'grafico.png'). Se None, exibe o gráfico.
    """
    plt.figure(figsize=(8, 5))

    if tipo == 'linha':
        plt.plot(dados['x'], dados['y'], marker='o')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    elif tipo == 'barra':
        plt.bar(dados['x'], dados['y'])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

    elif tipo == 'pizza':
        plt.pie(dados['valores'], labels=dados['labels'], autopct='%1.1f%%', startangle=90)
        plt.axis('equal')

    else:
        raise ValueError("Tipo de gráfico não suportado. Use 'linha', 'barra' ou 'pizza'.")

    plt.title(titulo)

    plt.tight_layout()

    if salvar_em:
        plt.savefig(salvar_em, dpi=300)
        print(f"Gráfico salvo em: {salvar_em}")
        plt.close()
    else:
        plt.show()


class DadosGraficoLinhaOuBarra(TypedDict):
    x: list[str]
    y: list[float]

class criar_graficoData(TypedDict):
    tipo: str
    dados: Union[DadosGraficoLinhaOuBarra]
    titulo: str
    xlabel: str
    ylabel: str
    salvar_em: str
    

@function_tool
def criar_grafico(data: criar_graficoData) -> str:
    """
    Cria e opcionalmente salva gráficos de linha, barra ou pizza.

    Args:
        tipo (str): Tipo de gráfico ('linha', 'barra', 'pizza').
        dados (dict): Dados para o gráfico.
        titulo (str): Título do gráfico.
        xlabel (str): Rótulo do eixo X (linha/barra).
        ylabel (str): Rótulo do eixo Y (linha/barra).
        salvar_em (str): Caminho do arquivo para salvar (ex: 'grafico.png'). Se None, exibe o gráfico.
    """
    try:
        data_FINAL = data["data"]
        tipo = data_FINAL["tipo"]
        dados = data_FINAL["dados"]
        titulo = data_FINAL["titulo"]
        xlabel = data_FINAL["xlabel"]
        ylabel = data_FINAL["ylabel"]
        salvar_em = data_FINAL["salvar_em"]
    except Exception as eroo1:
        print(eroo1)
        tipo = data["tipo"]
        dados = data["dados"]
        titulo = data["titulo"]
        xlabel = data["xlabel"]
        ylabel = data["ylabel"]
        salvar_em = data["salvar_em"]
    plt.figure(figsize=(8, 5))
    if tipo == 'linha':
        plt.plot(dados['x'], dados['y'], marker='o')
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
    elif tipo == 'barra':
        plt.bar(dados['x'], dados['y'])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
    elif tipo == 'pizza':
        plt.pie(dados['valores'], labels=dados['labels'], autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
    else:
        raise ValueError("Tipo de gráfico não suportado. Use 'linha', 'barra' ou 'pizza'.")
    plt.title(titulo)
    plt.tight_layout()
    if salvar_em:
        plt.savefig(salvar_em, dpi=300)
        print(f"Gráfico salvo em: {salvar_em}")
        plt.close()
    else:
        plt.show()
    return f"Tipo {tipo} de gráfico criado com sucesso"




























