

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


class Softwareanaysis:
    def __init__(self):
        pass

    ##############################################################################################
    def AI_SynthOperator(self, appfb, client,  path_Roadmap, cronograma_do_projeto, planilha, doc_Pre_Projeto):
        read_path_Roadmap = python_functions.analyze_txt(path_Roadmap)
        read_cronograma_do_projeto = python_functions.analyze_txt(cronograma_do_projeto)
        read_planilha = python_functions.analyze_txt(planilha)
        read_doc_Pre_Projeto = python_functions.analyze_txt(doc_Pre_Projeto)
        
        key = "AI_SynthOperator_Software_requirements_analyst"
        nameassistant = "AI SynthOperator Software requirements analyst"
        model_select = "gpt-4o-mini-2024-07-18"
        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None

        Upload_1_image_for_vision_in_thread = None
        vectorstore_in_assistant = None
        vectorstore_in_Thread = None
        Upload_list_for_code_interpreter_in_thread = None
        


        key_openai = OpenAIKeysteste.keys()
        # name_app = "appx"
        # appfb = FirebaseKeysinit._init_app_(name_app)
        # client = OpenAIKeysinit._init_client_(key_openai)


        AI_SynthOperator, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionSynthOperator, nameassistant, model_select, tools_SynthOperator, vectorstore_in_assistant)

        #AI_SynthOperator_Software_requirements_analyst = Agent_files_update.update_vectorstore_in_agent(AI_SynthOperator_Software_requirements_analyst, vector_store_id)

        mensaxgem = f"""
        Analise os quatro arquivos abaixo relacionados a um projeto de software \n
        Roadmap:\n
        {read_path_Roadmap}\n
        cronograma_do_projeto:\n
        {read_cronograma_do_projeto}\n
        planilha:\n
        {read_planilha}\n
        doc_Pre_Projeto:\n
        {read_doc_Pre_Projeto}\n

        """

        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensaxgem,
                                                                agent_id=AI_SynthOperator, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_SynthOperator,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructionSynthOperator
                                                                )


                                            
        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensaxgem, response, instructionsassistant, nameassistant)
        
        path__analise = os.getenv("PATH_ANALISE_ENV")
        python_functions.save_TXT(response, path__analise, "w")
        return str(path__analise)







