# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
def send_to_webhook(WEBHOOK_URL, user, type, message):
    """Envia uma mensagem para o webhook."""
    try:
        # Envia o conteúdo da mensagem como JSON; ajuste se necessário
        requests.post(WEBHOOK_URL, json={str(user): {"type": type, "message": message}})
    except Exception as e:
        # Evita erro recursivo chamando a função original de print
        print(f"Erro ao enviar mensagem para webhook:{e}")
