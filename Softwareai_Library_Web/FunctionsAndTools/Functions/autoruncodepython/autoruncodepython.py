#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################
from typing_extensions import TypedDict
from agents import function_tool
import subprocess
import logging

# Configuração do logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class Data(TypedDict):
    script_name: str
    arguments: List[str]
    python_env: str

@function_tool
def autoruncodepython(data: Data):
    try:
        data_FINAL = data["data"]
        script_name = data_FINAL["script_name"]
        arguments = data_FINAL["arguments"]
        python_env = data_FINAL["python_env"]
        logger.info(f"Received data: script_name={script_name}, arguments={arguments}, python_env={python_env}")
    except Exception as eroo1:
        logger.error(f"Error extracting data: {eroo1}")
        script_name = data["script_name"]
        arguments = data["arguments"]
        python_env = data["python_env"]
        logger.info(f"Using provided data: script_name={script_name}, arguments={arguments}, python_env={python_env}")
    
    # Formatar o comando para executar o script Python com os argumentos fornecidos
    command = [python_env, script_name] + arguments
    logger.info(f"Executing command: {command}")
    
    try:
        # Executar o comando Python
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        logger.info(f"Script executed successfully. Output: {result.stdout}")
        return {"status": "success", "message": result.stdout}
    except subprocess.CalledProcessError as e:
        logger.error(f"Error executing script. Code: {e.returncode}, Error: {e.stderr}")
        return {"status": "error", "message": e.stderr}
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {"status": "error", "message": str(e)}
