# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
def get_api_key():
    return request.headers.get('X-API-KEY')
