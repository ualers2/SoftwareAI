import requests
import sys
import logging


# Configura o logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)  # ou INFO, WARNING etc.

# Cria um handler para a saída padrão (stdout)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# Formato dos logs
formatter = logging.Formatter(
    fmt='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

# Evita adicionar múltiplos handlers
if not logger.hasHandlers():
    logger.addHandler(handler)


# Dados da requisição
url = sys.argv[1]
api_key_Arg = sys.argv[2]
session_id = sys.argv[3]
user_email = sys.argv[4]
message = sys.argv[5]
name_project = sys.argv[6]

api_key = api_key_Arg.replace("Api Token: ", "").replace("Api Token:", "")
logger.info(f"api_key: {api_key}")

headers = {
    "X-API-KEY": api_key,
    "X-User-Email": user_email,
    "Content-Type": "application/json"
}

body = {
    "session_id": session_id,
    "user_email": user_email,
    "user_message": message,
    "name_project": name_project
}

# Enviando a requisição POST
response = requests.post(url, headers=headers, json=body)
logger.info(f"Status Code:{response.status_code}")
logger.info(f"Resposta da API:{response.json()}")

