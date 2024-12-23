
#########################################
# IMPORT SoftwareAI Core
from ..._init_core_ import *
#########################################
# IMPORT SoftwareAI Libs 
from ..._init_libs_ import *
#########################################
# IMPORT SoftwareAI All Paths 
from ..._init_paths_ import *
#########################################
# IMPORT SoftwareAI Instructions
from ...SoftwareAI.Instructions._init_Instructions_ import *
#########################################
# IMPORT SoftwareAI Tools
from ...SoftwareAI.Tools._init_tools_ import *
#########################################

class Softwareanaysis:
    def __init__(self):
        pass

    ##############################################################################################
    def AI_SynthOperator(self, path_Roadmap, cronograma_do_projeto, planilha, doc_Pre_Projeto):
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
        
        AI_SynthOperator_Software_requirements_analyst = AutenticateAgent.create_or_auth_AI(key, instructionSynthOperator, nameassistant, model_select, tools_SynthOperator, vectorstore_in_assistant)

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

        response = ResponseAgent.ResponseAgent_message_with_assistants(mensaxgem,
                                                                        Upload_1_file_in_thread,
                                                                        Upload_1_file_in_message,
                                                                        Upload_1_image_for_vision_in_thread, 
                                                                        Upload_list_for_code_interpreter_in_thread,
                                                                        vectorstore_in_Thread,
                                                                        tools_SynthOperator, 
                                                                        AI_SynthOperator_Software_requirements_analyst, 
                                                                        model_select,
                                                                        adxitional_instructionSynthOperator, key)

        path__analise = os.getenv("PATH_ANALISE_ENV")
        python_functions.save_TXT(response, path__analise, "w")
        return str(path__analise)







