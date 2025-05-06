#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################


def valid(GITHUB_WEBHOOK_SECRET_CodeReview, signature, payload):
    computed_signature = 'sha256=' + hmac.new(
        GITHUB_WEBHOOK_SECRET_CodeReview.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    Payloaddecode = payload.decode('utf-8', errors='ignore')
    print(f"Signature from GitHub: {signature}")
    print(f"Computed Signature: {computed_signature}")

    if not hmac.compare_digest(signature, computed_signature):
        return "Assinatura inválida", 403

    try:
        data = json.loads(payload)
        return data
    except json.JSONDecodeError:
        return "Payload inválido", 400