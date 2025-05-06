
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################

class OpenAIKeysinit:
    
    def _init_client_(key_api):
        client = OpenAI(
            api_key=key_api,
        )
        return client
