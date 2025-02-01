import typer
import os
from typing import Dict
import ast
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time
import re
import subprocess

def extract_function_arguments(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        file_content = file.read()
    
    tree = ast.parse(file_content)
    function_args = {}

    for node in ast.walk(tree):
        print(node)
        if isinstance(node, ast.FunctionDef):
            arg_names = [arg.arg for arg in node.args.args]
            function_args[node.name] = arg_names
    
    return function_args

app = typer.Typer()

# Configurações de Chaves
@app.command()
def configure_db_company(
    namefordb: str = typer.Option(..., help="Nome para banco de dados."),
    databaseurl: str = typer.Option(..., help="URL do banco de dados."),
    storagebucketurl: str = typer.Option(..., help="URL do bucket de armazenamento."),
    pathkey: str = typer.Option(..., help="Caminho + arquivo com a Chave do banco de dados da companhia.")
    ):
        
    """
    Configura as credenciais do banco de dados da companhia.
    """

    file_Pathkey = os.path.join(pathkey)
    contentkey = None
    with open(file_Pathkey, 'r', encoding='utf-8') as file:
        contentkey = file.read()
        file.close()



    PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'CoreApp/KeysFirebase'))
    file_path = os.path.join(PATH_caminho, f"keys.py")


    namefilter = namefordb.replace(" ", "_")

    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(F'''
                
def keys_{namefilter}():
    key = {contentkey}
    credt = credentials.Certificate(key)
    app_{namefilter} = initialize_app(credt, {{
            'storageBucket': '{storagebucketurl}',
            'databaseURL': '{databaseurl}'
    }}, name='{namefilter}')
    return app_{namefilter}

        ''')
        file.close()



    # Lógica para armazenar ou validar a chave do banco de dados da companhia
    typer.echo(f"Chave do banco de dados da companhia Salva em: {file_path}")


@app.command()
def configure_db_app(
    namefordb: str = typer.Option(..., help="Nome para banco de dados."),
    databaseurl: str = typer.Option(..., help="URL do banco de dados."),
    storagebucketurl: str = typer.Option(..., help="URL do bucket de armazenamento."),
    pathkey: str = typer.Option(..., help="Caminho + arquivo com a Chave do banco de dados do app a ser governado.")
    ):
    """
    Configura as credenciais do banco de dados do aplicativo.
    """

    file_Pathkey = os.path.join(pathkey)
    contentkey = None
    with open(file_Pathkey, 'r', encoding='utf-8') as file:
        contentkey = file.read()
        file.close()

    PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'CoreApp/KeysFirebase'))
    file_path = os.path.join(PATH_caminho, f"keys.py")

    namefilter = namefordb.replace(" ", "_")

    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(F'''
                
def keys_{namefilter}():
    key = {contentkey}
    credt = credentials.Certificate(key)
    app_{namefilter} = initialize_app(credt, {{
            'storageBucket': '{storagebucketurl}',
            'databaseURL': '{databaseurl}'
    }}, name='{namefilter}')
    return app_{namefilter}

        ''')
        file.close()

    typer.echo(f"Chave do banco de dados do aplicativ Salva em: {file_path}")

@app.command()
def configure_openai(
    name: str = typer.Option(..., help="Nome para Chave da OpenAI."),
    key: str = typer.Option(..., help="Chave da OpenAI.")
    ):
    """
    Configura a chave de acesso da OpenAI.
    """

    PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'CoreApp/KeysOpenAI'))
    file_path = os.path.join(PATH_caminho, f"keys.py")

    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(F'''

class OpenAI_Keys_{name.replace(" ", "_")}:
    def keys():
        companyname = "{name.replace(" ", "_")}"
        str_key = "{key.replace(" ", "")}"
        return str_key
    


        ''')
        file.close()

    typer.echo(f"Chave da OpenAI Salva em: {file_path}")

@app.command()
def configure_huggingface(
                        name: str = typer.Option(..., help="Nome para Chave da Hugging Face."), 
                        key: str = typer.Option(..., help="Chave da Hugging Face.")
                        
                    ):
    """
    Configura a chave de acesso da Hugging Face.
    """

    PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'CoreApp/KeysHuggingFace'))
    file_path = os.path.join(PATH_caminho, f"keys.py")

    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(F'''

class HugKeys_{name.replace(" ", "_")}:
    def hug_{name.replace(" ", "_")}_keys():
        token = "{key}"
        return token

        ''')
        file.close()

    typer.echo(f"Chave da Hugging Face Salva em: {file_path}")

@app.command()
def configure_github_keys(
                        name: str = typer.Option(..., help="Nome para Chave do github."), 
                        github_username: str = typer.Option(..., help="Usuario do agente no github"),
                        github_token: str = typer.Option(..., help="Chave do agente no github")
                        
                    ):


    PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'CoreApp/KeysGitHub'))
    file_path = os.path.join(PATH_caminho, f"keys.py")

    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(F'''


class GithubKeys_{name.replace(" ", "_")}:
    def {name.replace(" ", "_")}_github_keys():
        github_username = "{github_username}"
        github_token = "{github_token}"
        return github_username, github_token


        ''')
        file.close()

    typer.echo(f"Chave do Github Salva em: {file_path}")




# Automatização da criacao de tools para agentes softwareai 
@app.command()
def create_function(
                pathfunction: str = typer.Option(..., help="Caminho + arquivo da função."),
                category: str = typer.Option(..., help="Categoria da função."),
                description_autogen_in_gpu: str = typer.Option(..., help="true"),
                cache_dir: str = typer.Option(..., help="D:/LLMModels"),
                ):
    """
    Cria uma nova função de maneira automatizada com base na descrição fornecida.
    """
    name = os.path.basename(pathfunction)
    name_filtrer = name.replace(" ", "_").replace(".py", "")
    category_filtrer = category.replace(" ", "_")
    
    #### Create tools  #### 
    args = extract_function_arguments(pathfunction)
    for function_name, arguments in args.items():
        def create_tool_file(tool_name, function_arguments, description="Descrição da função."):
            """Cria um arquivo de definição de tools baseado nos argumentos da função."""
            tools_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'CoreApp', 'SoftwareAI', 'Tools', f"{category_filtrer}"))
            os.makedirs(tools_dir, exist_ok=True)
            file_path = os.path.join(tools_dir, f"{tool_name}.py")
            # Criar propriedades baseadas nos argumentos da função
            properties = {arg: {"type": "string", "description": f"Descrição do argumento {arg}."} for arg in function_arguments}
            
            if description_autogen_in_gpu:
                with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'CoreApp', 'SoftwareAI', 'Functions', f"{category_filtrer}", f"{name_filtrer}.py" )), "r", encoding="utf-8") as f:
                    contentcode = f.read()
                    f.close()

                def autocreatedescription(code):

                    
                    model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
                    max_new_tokens = 1900

                    input_text = f""" 
                Create a description for the code function arguments

                code:
                {code}

                    """

                    # Carregar o modelo e o tokenizer
                    model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        torch_dtype="auto",
                        device_map="auto",
                        cache_dir=cache_dir
                    )
                    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)

                    # Preparar a entrada
                    messages = [{"role": "user", "content": f"{input_text}"}]
                    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

                    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

                    # Inicializar variáveis
                    input_ids = model_inputs['input_ids']
                    generated_ids = input_ids
                    num_generated_tokens = 0

                    # Variável para armazenar o texto após a segunda ocorrência
                    text_after_second_think = None
                    found_second_think = False

                    # Variável para acumular texto gerado no streaming
                    current_text = ""

                    # Gerar texto em "streaming"
                    while num_generated_tokens < max_new_tokens:
                        # Gerar um token de cada vez
                        outputs = model.generate(
                            generated_ids,
                            max_length=generated_ids.shape[1] + 1,  # Apenas um token adicional
                            do_sample=True,
                            top_k=50,
                            top_p=0.95,
                            temperature=0.7,
                            pad_token_id=tokenizer.eos_token_id
                        )
                        
                        # Atualizar a sequência gerada
                        generated_ids = outputs[:, :generated_ids.shape[1] + 1]
                        generated_token = generated_ids[0, -1].item()
                        
                        # Mostrar o token gerado
                        generated_text = tokenizer.decode(generated_ids[0, -1:], skip_special_tokens=True)
                        print(generated_text, end='', flush=True)
                        
                        # Acumular texto até a segunda ocorrência de </think>
                        current_text += generated_text

                        # Verificar se o token gerado é o final (EOS)
                        if generated_token == tokenizer.eos_token_id:
                            
                            break

                    matches = list(re.finditer(r"</think>\n", current_text))
                    #print(len(matches))
                    if len(matches) == 1:
                        start_index = matches[0].end()
                        text_after_second_think = current_text[start_index:]
                        return text_after_second_think


                description_DeepSeek_R1 = autocreatedescription(contentcode)

                description = description_DeepSeek_R1
                # Criar propriedades baseadas nos argumentos da função
                properties = {arg: {"type": "string", "description": f"Descrição do argumento {arg}."} for arg in function_arguments}
                
                
            required_args = function_arguments

            # Criar o conteúdo do arquivo
            tool_content = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "required": required_args
                    }
                }
            }
            
            
            # Escrever no arquivo
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f"tools_{tool_name} = [\n")
                file.write(json.dumps(tool_content, indent=4))
                file.write("\n]\n")

        create_tool_file(tool_name=function_name, function_arguments=arguments)
        break

    ################################ 

    #### Create init functions  #### 
    with open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), f'CoreApp')), f"_init_functions_.py"), 'r+', encoding='utf-8') as file:
        content = file.read()
        if f"from softwareai.CoreApp.SoftwareAI.Functions.{category_filtrer}.{name_filtrer}" not in content:
            file.write(F'''
from softwareai.CoreApp.SoftwareAI.Functions.{category_filtrer}.{name_filtrer} import *
            ''')
            file.close()

    ################################ 
    



    #### Create init tools #### 
    with open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), f'CoreApp' )), f"_init_tools_.py"), 'r+', encoding='utf-8') as file:
        content = file.read()
        if f"{category_filtrer}.{name_filtrer}" not in content:
            
            file.write(F'''
from softwareai.CoreApp.SoftwareAI.Tools.{category_filtrer}.{name_filtrer} import *
            ''')
            file.close()

    ################################ 



    #### Create Submit Output #### 
    PATH_caminho_Submit_Output = os.path.abspath(os.path.join(os.path.dirname(__file__), f'CoreApp', 'SoftwareAI', 'Functions_Submit_Outputs', f'{category_filtrer}'))
    os.makedirs(PATH_caminho_Submit_Output, exist_ok=True)
    file_path_Submit_Output = os.path.join(PATH_caminho_Submit_Output, f'{name_filtrer}.py')
    with open(file_path_Submit_Output, 'x', encoding='utf-8') as file:
        file.write(F'''

#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI Functions
from softwareai.CoreApp._init_functions_ import *
#########################################

tool_outputs = []
def submit_output_{name_filtrer}(function_name,
                                function_arguments,
                                tool_call,
                                threead_id,
                                client,
                                run,
                                appfb,
                                appproduct
                                ):

    global tool_outputs
    
    # Mapear funções pelo nome
    functions_map = {{
        "{name_filtrer}": {name_filtrer},

    }}

    # Obter a função correspondente
    target_function = functions_map.get(function_name)
    if not target_function:
        print(f"Função {{function_name}} não encontrada.")
        return False

    # Inspecionar os argumentos da função
    function_signature = inspect.signature(target_function)
    function_parameters = function_signature.parameters

    # Preparar argumentos para chamada
    args = json.loads(function_arguments)
    call_arguments = {{}}

    # Adicionar parâmetros obrigatórios 
    if "appcompany" in function_parameters:
        call_arguments["appcompany"] = appfb
    if "appfb" in function_parameters:
        call_arguments["appfb"] = appfb
    if "appproduct" in function_parameters:
        call_arguments["appproduct"] = appproduct
    if "app_product" in function_parameters:
        call_arguments["app_product"] = appproduct
        
    # Adicionar outros argumentos do JSON somente se estiverem na assinatura da função
    for arg_name, arg_value in args.items():
        if arg_name in function_parameters:
            call_arguments[arg_name] = arg_value

    try:
        # Chamar a função com os argumentos preparados
        result = target_function(**call_arguments)

        # Submeter o resultado
        tool_call_id = tool_call.id
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=threead_id,
            run_id=run.id,
            tool_outputs=[
                {{
                    "tool_call_id": tool_call_id,
                    "output": json.dumps(result),
                }}
            ]
        )
        print("Tool outputs submitted successfully.")
        return True

    except Exception as e:
        print(f"Erro ao executar  {{function_name}}: {{e}}")
        
        ''')
        file.close()
   
    ################################ 


    #### Create init submit outputs  #### 
    new_function_name = f"submit_output_{name_filtrer}"
    with open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), 'CoreApp')), '_init_submit_outputs_.py'), 'r+', encoding='utf-8') as file:
        content = file.read()
        if new_function_name not in content:
            updated_content = content.replace(
                "functions_to_call = [",
                f"functions_to_call = [\n        {new_function_name},"
            )
            file.seek(0)
            file.write(updated_content)
            file.truncate()
        else:
            print("Função já está na lista.")
    with open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), 'CoreApp')), '_init_submit_outputs_.py'), 'r+', encoding='utf-8') as file:
        content = file.read()
        new_import = f"from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.{category_filtrer}.{name_filtrer} import submit_output_{name_filtrer}\n"
        if new_import not in content:
            file.seek(0)
            file.write(new_import + content)
            file.truncate()

    ################################ 

    
    file_path_tool = os.path.abspath(os.path.join(os.path.dirname(__file__), 'CoreApp', 'SoftwareAI', 'Tools', f"{category_filtrer}", f"{name_filtrer}.py"))
    typer.echo(f"\nTool criada e salva em: {file_path_tool}")






# Agente Selecionado Em Modo API
@app.command()
def select_agent_mode_api(
    name_agent: str = typer.Option(..., help="Nome do agente a ser executado"),
    category_agent: str = typer.Option(..., help="Nome da Categoria do agente a ser executado"),
    local_execute_port: str = typer.Option(..., help="A porta onde o agente sera consultado"), 
    ):

    name_agent_filter = name_agent.replace(" ", "_").replace(".py", "")
    category_agent_filter = category_agent.replace(" ", "_")


    # Caminho do arquivo
    diretorio = os.path.join(
        os.path.dirname(__file__),
        'CoreApp',
        'Agents',
        f"{category_agent_filter}",
        f'{name_agent_filter}_api.py'
    )
    with open(diretorio, 'r') as arquivo:
        conteudo = arquivo.readlines()

    # Modifica a porta na linha contendo app.run
    for i, linha in enumerate(conteudo):
        if "if __name__ == '__main__':" in linha:
            # Procura a linha com app.run na sequência
            for j in range(i + 1, len(conteudo)):
                if "app.run" in conteudo[j]:
                    conteudo[j] = f"    app.run(port={local_execute_port})\n"
                    break
            break

    # Escreve de volta no arquivo
    with open(diretorio, 'w') as arquivo:
        arquivo.writelines(conteudo)

    print(f"A porta foi alterada para {local_execute_port}")
            
    comando_terminal = ['start', f'"{name_agent}"', 'cmd', '/K', f'python "{diretorio}"']
    subprocess.Popen(' '.join(comando_terminal), shell=True)
    print(f"Executando {name_agent} em http://127.0.0.1:100")



if __name__ == "__main__":
    app()
