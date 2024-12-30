
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################

def execute_python_code(filename):
    try:
        result = subprocess.run(['python', filename], capture_output=True, text=True, check=True)
        return f"Saída padrão: {result.stdout.strip()}" if result.stdout else "Execução concluída sem saída."
    except subprocess.CalledProcessError as e:
        return f"Erro ao executar o código:\n{e.stderr.strip()}"
    except FileNotFoundError:
        return f"Erro: O arquivo '{filename}' não foi encontrado."
    except Exception as e:
        return f"Erro inesperado: {str(e)}"
