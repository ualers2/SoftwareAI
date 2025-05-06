# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
def generate_api_key(subscription_plan):
    prefix_map = {
        "free": "apikey-free",
        "premium": "apikey-premium",
    }
    prefix = prefix_map.get(subscription_plan.lower(), "apikey-default")
    unique_part = secrets.token_urlsafe(32)
    api_key = f"{prefix}-{unique_part}"
    return api_key
