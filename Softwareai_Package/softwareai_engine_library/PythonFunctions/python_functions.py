


# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
class python_functions:

    def ignore_python_code(text: str, replacement: str = "[CODE ON THE BOARD]") -> str:
        padrão = r"```python\n[\s\S]*?```"
        texto_limpo = re.sub(padrão, replacement, text, flags=re.DOTALL)
        texto_limpo = re.sub(r'\n{3,}', '\n\n', texto_limpo)
        return texto_limpo.strip()


    def format_message(message):
        patternbash = r"^\s*```bash\n([\s\S]*?)```"
        highlight_pattern = r'`(.*?)`'
        title_pattern = r'### (.+?):'
        title_pattern2 = r'(###\s.*)'
        numberbeforcepoint_pattern = r'(\d+\.)'
        list_pattern = r'(\s{3}-\s.*)'
        minititulo_pattern = r'\*\*(.*?)\*\*'
        list_with_phrase_pattern = r"(\d+\.\s?\*\*`.*?`(?:\*\*)?\s*):\s*(.*)"

        # # Substitui blocos de código por HTML estilizado
        # message = re.sub(
        #     code_pattern,
        #     lambda m: (
        #         '<div style="position: relative; background-color: #1E1E1E; color: #D4D4D4; padding: 12px; border-radius: 8px; '
        #         'border: 1px solid #3C3C3C; font-family: Consolas, \'Courier New\', monospace; font-size: 14px; overflow: auto;">'
        #         '<div style="position: absolute; top: 8px; right: 8px; background-color: #022740; '
        #         'color: #FFFFFF; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 12px;">'
        #         f'<b>#Python Code With {len(m.group(1).splitlines())} Lines</b>'
        #         '</div>'
        #         '<pre style="margin: 0; padding: 0; white-space: pre-wrap; background-color: #1E1E1E; color: #D4D4D4;">' +
        #         ''.join(
        #             f'{line}\n'
        #             for i, line in enumerate(m.group(1).splitlines())
        #         ).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>") +
        #         '</pre>'
        #         '</div>'
        #     ),
        #     message,
        #     flags=re.DOTALL
        # )


        message = python_functions.ignore_python_code(message)

        message = re.sub(
            list_with_phrase_pattern,
            lambda m: (
                f'<li style="background-color: #F7F7F7; color: #000000; padding: 8px 12px; '
                f'border-radius: 6px; margin: 6px 0;"><b>' + m.group(1).replace("\n", "").replace("**", "").replace(":", "-").strip() + '</b>:<span style="color: #3b302c;">' + m.group(2).replace("\n", "").strip() + '</span></li>'
            ),
            message
        )
        message = re.sub(
            highlight_pattern,
            lambda m: (
                f'<span style="background-color: #F7F7F7; color: #000000; padding: 2px 4px; '
                f'border-radius: 3px;"><b>{m.group(1)}</b></span>'
            ),
            message
        )
        message = re.sub(
            minititulo_pattern,
            lambda m: (
                f'<span style="background-color: #F7F7F7; color: #022740; padding: 2px 4px; '
                f'border-radius: 3px;"><b>{m.group(1)}</b></span>'
            ),
            message
        )
        message = re.sub(
            numberbeforcepoint_pattern,
            lambda m: (
                f'<span style="background-color: #F7F7F7; color: #243096; padding: 2px 4px; '
                f'border-radius: 3px;"><b>{m.group(1).replace(".", ")")}</b></span>'
            ),
            message
        )
        message = re.sub(
            list_pattern,
            lambda m: (
                f'<span style="color: #1a0e03; padding: 2px 4px; '
                f'border-radius: 3px;">     {m.group(1)}</span>'
            ),
            message
        )
        message = re.sub(
            title_pattern,
            lambda m: (
                f'<h3 style="background-color: #F7F7F7; color: #000000; margin: 5px 0; font-size: 1.2em;"><b>{m.group(1)}</b></h3>'
            ),
            message
        )
        message = re.sub(
            title_pattern2,
            lambda m: (
                f'<h3 style="background-color: #F7F7F7; color: #000000; margin: 5px 0; font-size: 1.2em;"><b>{m.group(1).replace("### ", "")}</b></h3>'
            ),
            message
        )
        message = re.sub( 
            patternbash, 
            lambda m: ( 
                '<pre style="margin: 0; padding: 0; white-space: pre-wrap; background-color: #F7F7F7; color: #0e0042;"><b>' +
                ''.join(
                    f'{line}'
                    for i, line in enumerate(m.group(1).splitlines())
                ).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "") +
                '</b></pre>'
                '</div>'
                ), message, flags=re.MULTILINE,
            )
        message = message.replace("\n", "<br>")
        return message








    def ignore_python_code(text: str, replacement: str = "[CODE ON THE BOARD]") -> str:
        padrão = r"```python\n[\s\S]*?```"
        texto_limpo = re.sub(padrão, replacement, text, flags=re.DOTALL)
        texto_limpo = re.sub(r'\n{3,}', '\n\n', texto_limpo)
        return texto_limpo.strip()


    def create_env(variables, env):
        """
        Cria um arquivo .env com as variáveis fornecidas.
        Se o arquivo já existir, ele será sobrescrito.

        Args:
            variables (dict): Um dicionário com chave-valor representando as variáveis de ambiente.
        """
        with open(env, "w") as file:
            for key, value in variables.items():
                file.write(f"{key}={value}\n")
        return True

    def update_multiple_env_variables(updates, env):
        # Lê o conteúdo atual do .env
        with open(env, "r") as file:
            lines = file.readlines()
        
        # Abre o .env para escrita e modifica as linhas conforme necessário
        with open(env, "w") as file:
            for line in lines:
                # Extrai a chave de cada linha no .env
                key = line.split("=")[0]
                
                # Verifica se a chave precisa ser atualizada
                if key in updates:
                    file.write(f"{key}={updates[key]}\n")
                else:
                    file.write(line)
        return True

    def update_env_variable(key, value):
        """
        Update the environment variable `key` with the given `value`.

        Parameters:
        ----------
        key (str): The name of the environment variable to update.
        value (str): The new value for the environment variable.

        Returns:
        -------
        None
        """
        with open(".env", "r") as file:
            lines = file.readlines()
        
        # Modifies the line that contains the environment variable
        with open(".env", "w") as file:
            for line in lines:
                if line.startswith(key + "="):
                    file.write(f"{key}={value}\n")
                else:
                    file.write(line)

    def execute_python_code_created(filename):
        """
        Execute the Python code stored in the specified file.

        Parameters:
        ----------
        filename (str): The name of the Python file to execute.

        Returns:
        -------
        str: The standard output of the executed script.
        """
        try:
            result = subprocess.run(['python', filename], capture_output=True, text=True)
            return f"Saída padrão: {result.stdout}"
        except Exception as e:
            pass

    def save_data_frame_planilha(planilha_json, path_nome_da_planilha):
        """
        Save the data frame to a CSV file.

        Parameters:
        ----------
        planilha_json (dict): The dictionary representing the data frame.
        path_nome_da_planilha (str): The path where the CSV file will be saved.

        Returns:
        -------
        None
        """
        df = pd.DataFrame(planilha_json)
        df.to_csv(path_nome_da_planilha, index=False)

    def save_python_code(code_string, name_script):
        """
        Save the provided Python code string to a file.

        Parameters:
        ----------
        code_string (str): The Python code to save.
        name_script (str): The name of the file where the code will be saved.

        Returns:
        -------
        None
        """
        with open(name_script, 'w', encoding="utf-8") as file:
            file.write(code_string)

    def save_csv(dataframe, path_nome_do_cronograma):
        """
        Salva o DataFrame em um arquivo CSV no caminho especificado.

        :param dataframe: O DataFrame a ser salvo.
        :param path_nome_do_cronograma: O caminho e nome do arquivo CSV onde o DataFrame será salvo.
        """
        try:
            dataframe.to_csv(path_nome_do_cronograma, index=False, encoding='utf-8')
            print(f"Arquivo salvo com sucesso em: {path_nome_do_cronograma}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo CSV: {e}")


    def save_TXT(string, filexname, letra):
        """
        Save a string to a text file.

        Parameters:
        - string (str): The content to be saved.
        - filexname (str): The path to the output text file.
        - letra (str): The mode in which to open the file ('a' for append, 'w' for write).

        Returns:
        - None
        """
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filexname), exist_ok=True)
        
        # Save the content to the file
        with open(filexname, letra, encoding="utf-8") as file:
            file.write(f'{string}')


    def save_json(string, filexname):
        """
        Save a JSON string to a JSON file.

        Parameters:
        - string (dict): The dictionary to be saved as JSON.
        - filexname (str): The path to the output JSON file.

        Returns:
        - None
        """
        with open(filexname, 'w', encoding='utf-8') as json_file:
            json.dump(string, json_file, ensure_ascii=False, indent=4)
        print("JSON salvo em 'documento_pre_projeto.json'")


    def delete_all_lines_in_txt(filepath):
        """
        Delete all lines from a text file.

        Parameters:
        - filepath (str): The path to the text file.

        Returns:
        - None
        """
        with open(filepath, 'w') as file:
            pass  


    def move_arquivos(a, b):
        """
        Move files from one directory to another.

        Parameters:
        - a (str): The source directory.
        - b (str): The destination directory.

        Returns:
        - None
        """
        pasta1 = os.listdir(a)
        for arquivo in pasta1:
            caminho_arquivo_origem = os.path.join(a, arquivo)
            caminho_arquivo_destino = os.path.join(b, arquivo)
            shutil.move(caminho_arquivo_origem, caminho_arquivo_destino)
            print(f'{arquivo} movido para {b}')


    def executar_agentes(mensagem, name_for_script, nome_agente):
        """
        Execute an agent script using Python.

        Parameters:
        - mensagem (str): The message to be passed to the agent.
        - name_for_script (str): The name of the agent script.
        - nome_agente (str): The name of the agent.

        Returns:
        - None
        """
        comando_terminal = ['start', 'python', f'{nome_agente}.py', mensagem, name_for_script]
        subprocess.Popen(comando_terminal, shell=True)


    def analyze_txt_0(file):
        """
        Read the last line of a text file.

        Parameters:
        - file (str): The path to the text file.

        Returns:
        - str: The last line of the text file.
        """
        with open(file, 'r') as file:
            linhas = file.readlines()
            ultima_linha = linhas[-1].strip()
            return ultima_linha


    def analyze_file(file_path):
        """
        Read the entire content of a file.

        Parameters:
        - file_path (str): The path to the file.

        Returns:
        - str: The content of the file.
        """
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return content
        except:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    return content
            except:
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        content = file.read()
                        return content
                except UnicodeDecodeError:
                    return None


    def analyze_txt(file_path):
        """
        Read the entire content of a text file.

        Parameters:
        - file_path (str): The path to the text file.

        Returns:
        - str: The content of the file.
        """
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                return content
        except:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    return content
            except:
                try:
                    with open(file_path, 'r', encoding='latin-1') as file:
                        content = file.read()
                        return content
                except UnicodeDecodeError:
                    try:
                        file_path = file_path.replace(" ", "").replace("\n", "")
                        with open(file_path, 'r', ) as file:
                            content = file.read()
                            return content
                    except UnicodeDecodeError:
                        pass


    def analyze_csv(file_path):
        """
        Read the contents of a CSV file.

        Parameters:
        - file_path (str): The path to the CSV file.

        Returns:
        - list: A list of lists containing the rows of the CSV file.
        """
        import csv
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)


    def analyze_json(file_path):
        """
        Load a JSON file and print its contents.

        Parameters:
        - file_path (str): The path to the JSON file.

        Returns:
        - dict: The loaded JSON data.
        """
        import json
        with open(file_path, 'r') as file:
            data = json.load(file)
        print(f"Dados JSON: {data}")
        