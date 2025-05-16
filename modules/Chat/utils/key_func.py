# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################

from softwareai_engine_library.Chat.utils.get_api_key import get_api_key

def key_func():
    api_key = get_api_key()
    return api_key if api_key else get_remote_address()
