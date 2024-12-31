

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





class Company_Managers:
        
    def AI_MatrixMinder_Company_Managers(self, mensaagem, Analysis_txt, file_path_py, Roadmap_txt, Documentation_md, Project_spreadsheet_txt):
        
        # Analysis_txt = python_functions.analyze_txt(Analysis_txt)
        # file_path_py = python_functions.analyze_txt(file_path_py)
        # Roadmap_txt = python_functions.analyze_txt(Roadmap_txt)
        # Documentation_md = python_functions.analyze_txt(Documentation_md)
        # Project_spreadsheet_txt = python_functions.analyze_txt(Project_spreadsheet_txt)



        """Nome da IA: MatrixMinder\n
            Função: Manager de Software"""    

        key = "AI_MatrixMinder_Manager_de_Software"
        nameassistant = "AI MatrixMinder Manager de Software"
        model_select = "gpt-4o-mini"
        
        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_1_image_for_vision_in_thread = None
        vectorstore_in_assistant = None
        
        Upload_list_for_code_interpreter_in_thread = None
        # Upload_list_for_code_interpreter_in_thread = [
        #     Analysis_txt,
        #     file_path_py,
        #     Roadmap_txt,
        #     Documentation_md,
        #     Project_spreadsheet_txt
        # ]

        MatrixMinderAnálxise = "MatrixMinderAnálise"
        file_path_MatrixMinderAnálise = [
            Analysis_txt,
            file_path_py,
            Roadmap_txt,
            Documentation_md,
            Project_spreadsheet_txt
        ]
        print(file_path_MatrixMinderAnálise)
        vector_store_id_MatrixMinderAnálise = Agent_files.auth_or_create_vectorstore(MatrixMinderAnálxise, file_path_MatrixMinderAnálise)
        vectorstore_in_Thread = vector_store_id_MatrixMinderAnálise

        AI_MatrixMinder = AutenticateAgent.create_or_auth_AI(key, instructionMatrixMinder, nameassistant, model_select, tools_MatrixMinder, vectorstore_in_assistant)

        mensaxgem = f"""
        decidir se oque foi solicitado na mensagem é uma atualizacao: {mensaagem}
        \n

        """
        AI_ByteManager_response = ResponseAgent.ResponseAgent_message_with_assistants(mensaxgem,
                                                                Upload_1_file_in_thread, Upload_1_file_in_message,
                                                                Upload_1_image_for_vision_in_thread, Upload_list_for_code_interpreter_in_thread,
                                                                vectorstore_in_Thread,
                                                                tools_MatrixMinder,  AI_MatrixMinder, model_select, adxitional_instructions_MatrixMinder, key)
        try:
            resposta = AI_ByteManager_response['resposta']
        except:
            resposta = AI_ByteManager_response

        print(resposta)


        return resposta







