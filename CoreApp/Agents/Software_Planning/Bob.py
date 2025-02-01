

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





class Gerente_de_projeto:
    def __init__(self):
        pass

    ##############################################################################################
    def Bob_Gerente_de_projeto(self, appfb, client, path_name_doc_Pre_Projeto, repo_name, UseVectorstoreToGenerateFiles = True):

        key = "AI_Bob_Gerente_de_Projeto"
        nameassistant = "AI Bob Gerente de Projeto"
        model_select = "gpt-4o-mini-2024-07-18"
        
        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_1_image_for_vision_in_thread = None
        vectorstore_in_assistant = None
        vectorstore_in_Thread = None
        Upload_list_for_code_interpreter_in_thread = None

        
        key_openai = OpenAIKeysteste.keys()

        github_username, github_token = GithubKeys.BobGerenteDeProjeto_github_keys()
        
        path_nome_do_cronograma = os.getenv("PATH_NOME_DO_CRONOGRAMA_ENV")
        

        AI_Bob, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionBob, nameassistant, model_select, tools_Bob, vectorstore_in_assistant)
        if UseVectorstoreToGenerateFiles == True:
            file_paths = [os.path.abspath(os.path.join(os.path.dirname(__file__), "../../", f"environment.txt")), path_name_doc_Pre_Projeto]
            AI_Bob = Agent_files_update.del_all_and_upload_files_in_vectorstore(appfb, client, AI_Bob, "Bob_Work_Environment", file_paths)

        
        mensagem = f"""
        Crie o cronograma do projeto, salve e realize o upload no GitHub (usando autosave e autoupload) Baseie-se no documento pre projeto armazenado em `Bob_Work_Environment`
        repo_name: \n
        {repo_name}\n
        token: \n
        {github_token}\n


        regra: em autoupload utilize o seguinte caminho relativo para o cronograma AppMap/SpreadsheetAndTimeline
        """

        adxitional_instructions_Bob = f"""
        estrutura do projeto esta armazenada em environment.txt
        """
               
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensagem,
                                                                agent_id=AI_Bob, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_Bob,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_Bob
                                                                )
    
                                            
        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem, response, instructionsassistant, nameassistant)
        

        if UseVectorstoreToGenerateFiles == True:
            file_paths = [path_name_doc_Pre_Projeto, path_nome_do_cronograma]
            AI_Bob = Agent_files_update.del_all_and_upload_files_in_vectorstore(appfb, client, AI_Bob, "Bob_Work_Environment", file_paths)
            mensagem = f"""
            Crie o planilha do projeto, salve e realize o upload no GitHub (usando autosave e autoupload) Baseie-se no documento pre projeto e cronograma armazenado em `Bob_Work_Environment`
            repo_name: \n
            {repo_name}\n
            token: \n
            {github_token}\n
            """


        adxitional_instructions_Bob = f"""
        estrutura do projeto esta armazenada em environment.txt
        """

        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensagem,
                                                                agent_id=AI_Bob, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_Bob,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_Bob
                                                                )
    
                                            
        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem, response, instructionsassistant, nameassistant)
        



        return os.getenv("PATH_PLANILHA_PROJETO_ENV"), path_nome_do_cronograma, path_name_doc_Pre_Projeto



