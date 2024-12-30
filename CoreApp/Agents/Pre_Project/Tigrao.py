

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



class Pre_Project_Document:
    def __init__(self):
        pass


    def AI_1_Pre_Project_Document_Writer(self, appfb, client, mensagem):
        """
        Nome da IA: Tigrao \n
        Função: Escritor de Documento Pre-Projeto De Software \n
        Horario de trabalho: 1H\n
        :param mensagem: str \n
        :param output: path_name_doc_Pre_Projeto
        """   

       

        key = "AI_Tigrao_Escritor_de_documento_Pre_Projeto"
        nameassistant = "AI Tigrao Escritor de documento Pre-Projeto"
        model_select = "gpt-4o-mini-2024-07-18"
        
        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_1_image_for_vision_in_thread = None
        Upload_list_for_code_interpreter_in_thread = None
        vectorstore_in_Thread = None
        vectorstore_in_agent = None

        key_openai = OpenAIKeysteste.keys()
        # name_app = "appx"
        # appfb = FirebaseKeysinit._init_app_(name_app)
        # client = OpenAIKeysinit._init_client_(key_openai)


        AI_Tigrao, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionTigrao, nameassistant, model_select, tools_Tigrao, vectorstore_in_agent)

        mensaxgem = f"crie um documento Pre-Projeto baseado nas informacoes asseguir: \n  {mensagem}"
        format = 'Responda no formato JSON Exemplo: {"doc_Pre_Projeto": "..."},{"name_doc_Pre_Projeto": "..."} '
        mensage3 = mensaxgem + format
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensage3,
                                                                agent_id=AI_Tigrao, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_Tigrao,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_Tigrao
                                                                )
                                                
         
                                            
        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensage3, response, instructionsassistant, nameassistant)
        
        
        #print(response)
        
        #python_functions.save_json(response, path_name_doc_Pre_Projeto)
        try:
            teste_dict = json.loads(response)
            documento_Pre_Projeto = teste_dict['doc_Pre_Projeto']
            print(documento_Pre_Projeto)
            
            name_doc_Pre_Projeto = teste_dict['name_doc_Pre_Projeto']
            path_name_doc_Pre_Projeto = os.getenv("PATH_NAME_DOC_PRE_PROJETO_ENV")
            path = os.path.dirname(path_name_doc_Pre_Projeto)
            novo_caminho = os.path.join(path, f"{name_doc_Pre_Projeto}.txt")
            print(name_doc_Pre_Projeto)
            python_functions.save_TXT(documento_Pre_Projeto, novo_caminho, "w")
            return novo_caminho
        except Exception as E:
            print(E)
            path_name_doc_Pre_Projeto = os.getenv("PATH_NAME_DOC_PRE_PROJETO_ENV")
            python_functions.save_TXT(response, path_name_doc_Pre_Projeto, "w")
            return path_name_doc_Pre_Projeto









