

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
from softwareai.CoreApp._init_Instructions_ import *
#########################################
# IMPORT SoftwareAI Tools
from softwareai.CoreApp._init_tools_ import *
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *
#########################################



class Pre_Project_Document:
    def __init__(self):
        pass


    def AI_1_Pre_Project_Document_Writer(self, appfb, client, mensagem, repo_name):

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
        
        github_username, github_token = GithubKeys.Tigrao_github_keys()

        AI_Tigrao, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionTigrao, nameassistant, model_select, tools_Tigrao, vectorstore_in_agent)

        mensaxgem = f"""
        Crie o documento Pre-Projeto do projeto, salve e realize o upload no GitHub (usando autosave e autoupload) Baseie-se nas informacoes asseguir: \n  {mensagem}
        repo_name: \n
        {repo_name}\n
        token: \n
        {github_token}\n


        regra: em autoupload utilize o seguinte caminho relativo para o Dcumento Pre-Projeto: AppMap/PreProject/doc.txt
        """
        mensage3 = mensaxgem 
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
        
        path_name_doc_Pre_Projeto = os.getenv("PATH_NAME_DOC_PRE_PROJETO_ENV")
        return path_name_doc_Pre_Projeto







