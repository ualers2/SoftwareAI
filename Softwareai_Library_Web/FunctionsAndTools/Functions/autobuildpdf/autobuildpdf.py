import os
import json
import markdown
import pdfkit
import chardet
import html
import re
from unidecode import unidecode  # Importando a biblioteca unidecode

from datetime import datetime
import os
import json
import markdown
import pdfkit
import chardet
import html
import re
from unidecode import unidecode  # Importando a biblioteca unidecode
from typing_extensions import TypedDict, Any
from agents import Agent, ModelSettings, function_tool, FileSearchTool, WebSearchTool, Runner



def generate_watermark(document_type: str) -> str:
    """
    Gera HTML e CSS para uma marca d'água com o tipo do documento no canto superior esquerdo.

    Parâmetros:
        document_type (str): Texto a ser exibido, ex: "Pré-Projeto".

    Retorna:
        str: HTML + CSS para a marca d'água.
    """
    return f"""
    <style>
        .watermark-box {{
            position: fixed;
            top: 20px;
            left: -50px;
            transform: rotate(-45deg);
            background-color: #d0d0d0;
            color: #111;
            font-family: Arial, sans-serif;
            font-weight: bold;
            padding: 10px 40px;
            z-index: 9999;
            box-shadow: 0 0 5px rgba(0,0,0,0.2);
            opacity: 0.7;
            font-size: 18px;
        }}
    </style>
    <div class="watermark-box">{html.escape(document_type)}</div>
    """

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def read_file_with_correct_encoding(file_path):
    encoding = detect_encoding(file_path)
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()

def load_theme(theme_path: str):
    """
    Carrega um arquivo JSON de tema e retorna as propriedades CSS.

    Parâmetros:
        theme_path (str): Caminho para o arquivo .json do tema.

    Retorna:
        dict: Propriedades CSS extraídas do arquivo de tema.
    """
    if not os.path.isfile(theme_path):
        raise FileNotFoundError(f"Arquivo de tema não encontrado: {theme_path}")
    
    with open(theme_path, 'r', encoding='utf-8') as f:
        theme_data = json.load(f)

    css = theme_data.get('css', {})
    return css

def generate_css(css_properties: dict) -> str:
    """
    Gera o conteúdo CSS a partir das propriedades fornecidas, com suporte a seletores.
    
    Parâmetros:
        css_properties (dict): Dicionário com seletores e suas regras.
    
    Retorna:
        str: Código CSS gerado.
    """
    css_content = ""
    for selector, rules in css_properties.items():
        css_content += f"{selector} {{\n"
        for prop, value in rules.items():
            css_content += f"  {prop}: {value};\n"
        css_content += "}\n"
    return f"<style>{css_content}</style>"

def clean_invalid_characters(text: str) -> str:
    """
    Substitui caracteres inválidos e acentuados por letras sem acento, usando unidecode.
    
    Parâmetros:
        text (str): Texto a ser limpo.
    
    Retorna:
        str: Texto com caracteres inválidos e acentuados substituídos.
    """
    # Remover caracteres não ASCII (não válidos)
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', text)
    
    # Substituir acentos e caracteres especiais por suas versões sem acento
    return unidecode(cleaned_text)

class autobuildpdfData(TypedDict):
    input_md_content: str
    output_pdf_path: str
    theme_name: str

@function_tool
def autobuildpdf(data: autobuildpdfData):
    try:
        data_FINAL = data["data"]
        input_md_content = data_FINAL["input_md_content"]
        output_pdf_path = data_FINAL["output_pdf_path"]
        theme_name = data_FINAL["theme_name"]
    except Exception as eroo1:
        print(eroo1)
        input_md_content = data["input_md_content"]
        output_pdf_path = data["output_pdf_path"]
        theme_name = data["theme_name"]
    md_content_ = input_md_content
    md_content = clean_invalid_characters(md_content_)
    html_content = markdown.markdown(md_content, extensions=['extra', 'toc'])
    generation_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    footer_html = f"""
    <div style="text-align: center; font-size: 10px; color: gray; margin-top: 50px;">
        Document generated via auto build pdf in {generation_date}.
    </div>
    """
    
    if theme_name:
        theme_path = os.path.join("themes", f"{theme_name}.json")
        css_properties = load_theme(theme_path)
        css_style = generate_css(css_properties)
        html_content = f"""
        <html>
            <head>{css_style}</head>
            <body>{html_content}{footer_html}</body>
        </html>
        """
    else:
        html_content = f"<html><body>{html_content}{footer_html}</body></html>"
    pdfkit.from_string(html_content, output_pdf_path)
    print(f"PDF gerado com sucesso em: {output_pdf_path}")


def autobuildpdfv1(input_md_content: str, output_pdf_path: str = None, theme_name: str = None):

    md_content_ = input_md_content
    md_content = clean_invalid_characters(md_content_)

    # Extensões: 'toc' para sumário, 'extra' para suporte ampliado de markdown
    html_content = markdown.markdown(md_content, extensions=['extra', 'toc'])

    # Footer com data
    generation_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    footer_html = f"""
    <div style="text-align: center; font-size: 10px; color: gray; margin-top: 50px;">
        Document generated via auto build pdf in {generation_date}.
    </div>
    """

    # Se houver tema
    if theme_name:
        theme_path = os.path.join("themes", f"{theme_name}.json")
        css_properties = load_theme(theme_path)


        css_style = generate_css(css_properties)

        html_content = f"""
        <html>
            <head>{css_style}</head>
            <body>{html_content}{footer_html}</body>
        </html>
        """
    else:
        html_content = f"<html><body>{html_content}{footer_html}</body></html>"

    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_string(html_content, output_pdf_path, configuration=config)
    print(f"PDF gerado com sucesso em: {output_pdf_path}")

# # Exemplo de uso:
# autobuildpdf("docs/pre-projeto.md", 
#               theme_name="DarkMode",
# )
