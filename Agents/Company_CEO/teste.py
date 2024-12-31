

#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI All Paths 
from softwareai.CoreApp._init_paths_ import *
#########################################
# IMPORT SoftwareAI Instructions
from softwareai.CoreApp.SoftwareAI.Instructions._init_Instructions_ import *
#########################################
# IMPORT SoftwareAI Tools
from softwareai.CoreApp.SoftwareAI.Tools._init_tools_ import *
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *
#########################################
# IMPORT SoftwareAI _init_environment_
from softwareai.CoreApp._init_environment_ import init_env


UseVectorstoreToGenerateFiles = True
nameassistant = "teste"
key = "teste"
model_select = "gpt-4o-mini-2024-07-18"

path_name_doc_Pre_Projeto = r"D:\Save disk C\Saas do site\Projetos de codigo aberto\SoftwareAI\requirements.txt" #os.getenv("PATH_NAME_DOC_PRE_PROJETO_ENV")

key_openai = OpenAIKeysteste.keys()
name_app = "appx"
appfb = FirebaseKeysinit._init_app_(name_app)
client = OpenAIKeysinit._init_client_(key_openai)


if UseVectorstoreToGenerateFiles == True:
def del_all_and_upload_files_in_vectorstore(appfb, client, AI:str, name_for_vectorstore:str, file_paths:list, )

    name_for_vectorstore = key
    file_paths = [path_name_doc_Pre_Projeto]
    vector_store_id = Agent_files.auth_vectorstoreAdvanced(app1=appfb, client=client, name_for_vectorstore=name_for_vectorstore, file_paths=file_paths)
    ai, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionByteManager, nameassistant, model_select, tools_ByteManager)

    lista = client.beta.vector_stores.files.list(vector_store_id)
    ids = [file.id for file in lista.data]
    print(ids)
    for id in ids:
        deleted_vector_store_file = client.beta.vector_stores.files.delete(
            vector_store_id=vector_store_id,
            file_id=id
        )
        print(deleted_vector_store_file)

    vector_store_id = Agent_files.auth_vectorstoreAdvanced(app1=appfb, client=client, name_for_vectorstore=name_for_vectorstore, file_paths=file_paths)
    ai = Agent_files_update.update_vectorstore_in_agent(client, ai, [vector_store_id])


##def delvectorstorefiles(client, assistant_id: str, vector_store_id: str)