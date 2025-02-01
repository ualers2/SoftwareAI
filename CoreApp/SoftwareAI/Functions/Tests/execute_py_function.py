
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################

def execute_py(filepath):
    """
    Execute the Python code stored in the specified file.

    Parameters:
    ----------
    filepath (str): The name of the Python file to execute.

    Returns:
    -------
    str: The standard output of the executed script.
    """
    try:
        result = subprocess.run(
            ['python', filepath], 
            capture_output=True, 
            text=True, 
            check=True, 
            timeout=60  # Define o tempo limite de execução
        )
        return f"Saída padrão: {result.stdout.strip()}" if result.stdout else "Execução concluída sem saída."
    except subprocess.TimeoutExpired:
        return f"Erro: O script excedeu o tempo limite de 60 segundos e foi interrompido."
    except subprocess.CalledProcessError as e:
        return f"Erro ao executar o código:\n{e.stderr.strip()}"
    except FileNotFoundError:
        return f"Erro: O arquivo '{filepath}' não foi encontrado."
    except Exception as e:
        return f"Erro inesperado: {str(e)}"