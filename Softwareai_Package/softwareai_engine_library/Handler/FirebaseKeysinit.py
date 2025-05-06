
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
class FirebaseKeysinit:
    @staticmethod
    def _init_app_(name_app):
        module_path = "softwareai.CoreApp.KeysFirebase.keys"
        
        # Importa o módulo dinamicamente
        keys_module = importlib.import_module(module_path)

        # Verifica se o atributo (função ou classe) existe no módulo
        if hasattr(keys_module, name_app):
            # Obtém o atributo com base no nome dinâmico
            imported_name_app = getattr(keys_module, name_app)

            # Verifica se é uma função ou classe e chama ou instância
            if callable(imported_name_app):
                appfb = imported_name_app()  # Chama a função
            else:
                appfb = imported_name_app  # Atribui diretamente se for outro tipo (como uma classe)

            return appfb
        else:
            raise AttributeError(f"O módulo '{module_path}' não contém o atributo '{name_app}'.")
