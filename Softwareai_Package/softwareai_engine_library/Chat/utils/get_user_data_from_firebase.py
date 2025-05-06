
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################

def get_user_data_from_firebase(email, appcompany):
    """
    Função que obtém os dados do usuário no Firebase Realtime Database
    a partir da chave da API, na referência 'Users_Control_Panel'.
    """

    ref = db.reference(f'users/{email}', app=appcompany)
    user_data = ref.get()  # Obtém os dados do usuário com a chave especificada
    return user_data
