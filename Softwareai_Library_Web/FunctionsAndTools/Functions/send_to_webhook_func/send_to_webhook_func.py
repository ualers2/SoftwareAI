#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################
from typing_extensions import TypedDict
from agents import function_tool

class send_to_webhookData(TypedDict):
    user: str
    type: str
    message: str
    cor: str

@function_tool
def send_to_webhook_func(data: send_to_webhookData):
    try:
        data_FINAL = data["data"]
        user = data_FINAL["user"]
        type = data_FINAL["type"]
        message = data_FINAL["message"]
        cor = data_FINAL["cor"]
    except Exception as e:
        print(e)
        user = data["user"]
        type = data["type"]
        message = data["message"]
        cor = data["cor"]
    """Envia uma mensagem para o webhook."""
    WEBHOOK_URL = "https://ace-tahr-41.rshare.io/webhook"
    try:
        # Envia o conteúdo da mensagem como JSON; ajuste se necessário
        requests.post(WEBHOOK_URL, json={str(user): {"type": type, "message": message}})
        return True
    except Exception as e:
        # Evita erro recursivo chamando a função original de print
        print(f"Erro ao enviar mensagem para webhook:{e}")

def send_to_webhook_func1(
    user: str,
    type: str,
    message: str,
    cor: str
    ):
    """Envia uma mensagem para o webhook."""
    WEBHOOK_URL = "https://ace-tahr-41.rshare.io/webhook"
    try:
        # Envia o conteúdo da mensagem como JSON; ajuste se necessário
        requests.post(WEBHOOK_URL, json={str(user): {"type": type, "message": message}})
        return True
    except Exception as e:
        # Evita erro recursivo chamando a função original de print
        print(f"Erro ao enviar mensagem para webhook:{e}")
