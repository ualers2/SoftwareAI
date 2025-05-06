
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################

def init_fb(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)

    path_APPCOMPANY = os.getenv("FIREBASE_CREDENTIALS_PATH_APPCOMPANY")
    with open(path_APPCOMPANY) as f:
        firebase_credentials_APPCOMPANY = json.load(f)

    path_APPFB = os.getenv("FIREBASE_CREDENTIALS_PATH_APPFB")
    with open(path_APPFB) as f:
        firebase_credentials_APPFB = json.load(f)

    return firebase_credentials_APPCOMPANY, firebase_credentials_APPFB