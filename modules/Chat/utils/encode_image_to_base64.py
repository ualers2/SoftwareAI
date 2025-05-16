
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################

def encode_image_to_base64(file_storage):
    return base64.b64encode(file_storage.read()).decode("utf-8")
