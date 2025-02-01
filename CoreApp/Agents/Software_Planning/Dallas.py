

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




class Equipe_De_Solucoes:
    def __init__(self):
        pass

    def Dallas_Equipe_De_Solucoes_Roadmap(self, appfb, client, cronograma_do_projeto, planilha_json, doc_Pre_Projeto, repo_name, UseVectorstoreToGenerateFiles = True):

        key = "AI_Dallas_Equipe_de_Solucoes"
        nameassistant = "AI Dallas Equipe de Solucoes"
        model_select = "gpt-4o-mini-2024-07-18"

        
        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_1_image_for_vision_in_thread = None
        vectorstore_in_assistant = None
        vectorstore_in_Thread = None
        Upload_list_for_code_interpreter_in_thread = None


        key_openai = OpenAIKeysteste.keys()


        github_username, github_token = GithubKeys.DallasEquipeDeSolucoes_github_keys()

        AI_Dallas, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionDallas, nameassistant, model_select, tools_Dallas, vectorstore_in_assistant)

        if UseVectorstoreToGenerateFiles == True:
            file_paths = [os.path.abspath(os.path.join(os.path.dirname(__file__), "../../", f"environment.txt")), cronograma_do_projeto, planilha_json, doc_Pre_Projeto]
            AI_Dallas = Agent_files_update.del_all_and_upload_files_in_vectorstore(appfb, client, AI_Dallas, "Dallas_Work_Environment", file_paths)
            mensagem = f"""
            Planeje o Roadmap do projeto, salve e realize o upload no GitHub (usando autosave e autoupload) Baseie-se no documento Cronograma,Planilha e Documento Pre Projeto armazenado em `Dallas_Work_Environment`\n
            repo_name: \n
            {repo_name}\n
            token: \n
            {github_token}\n
             
            """

        adxitional_instructions_Dallas = f"""
        estrutura do projeto esta armazenada em environment.txt
        """
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensagem,
                                                                agent_id=AI_Dallas, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_Dallas,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_Dallas
                                                                )
    
        path_Roadmap = os.getenv("PATH_ROADMAP_ENV")
                 
        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem, response, instructionsassistant, nameassistant)
        
        return str(path_Roadmap), str(cronograma_do_projeto), str(planilha_json), str(doc_Pre_Projeto)
        

