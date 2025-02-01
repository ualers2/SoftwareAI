

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




class SoftwareDevelopment_SignalMaster:
    def __init__(self):
        pass

    ##############################################################################################
    def AI_SignalMaster(self, appfb, client, python_file_path, repo_name: str, branch_name: str, analisyspng=None):
        python_content = python_functions.analyze_file(python_file_path)
        """
        Nome da IA: SignalMaster \n
        Função: Desenvolvedor Pleno em Python \n
        Horario de trabalho: 1H
        
        :param analysis_txt_path: str \n
        :param output: path_to_py
        """   

        key = "AI_SignalMaster_Desenvolvedor_Pleno_de_Software_em_Python"
        nameassistant = "AI SignalMaster Desenvolvedor Pleno de Software em Python"
        model_select = "gpt-4o-mini-2024-07-18"

        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_list_for_code_interpreter_in_thread = None
        Upload_1_image_for_vision_in_thread = None
        vectorstore_in_assistant = None 
        vectorstore_in_Thread = None

        github_username, github_token = GithubKeys.SignalMaster_github_keys()

        key_openai = OpenAIKeysteste.keys()

        AI_SignalMaster, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionSignalMaster, nameassistant, model_select, tools_SignalMaster, vectorstore_in_assistant)
        
        
        mensaxgem = f"""melhore esse script em python\n
        script:\n
        {python_content}
        """
        format = 'Responda no formato JSON Exemplo: {"codigo": "import..."}'
        mensagem = mensaxgem + format
        response = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensagem,
                                                                agent_id=AI_SignalMaster, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_SignalMaster,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_SignalMaster
                                                                )


        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensaxgem, response, instructionsassistant, nameassistant)
        
        path_Software_Development_txt = os.getenv("PATH_SOFTWARE_DEVELOPMENT_TXT_ENV")
        python_functions.save_TXT(response, path_Software_Development_txt, "w")
        python_software_in_txt = python_functions.analyze_txt(path_Software_Development_txt)


        mensaxgem = f"""corrija todos os erros de sintaxe do codigo asseguir:\n
        {python_software_in_txt}\n
        caso nao tenha erros de sintaxe retorne o codigo 
        """
        format = 'Responda no formato JSON Exemplo: {"codigo": "import..."}'
        path_Software_Development_py = os.getenv("PATH_SOFTWARE_DEVELOPMENT_PY_ENV")
        mensagem = mensaxgem + format
        response = ResponseAgent.ResponseAgent_message_completions(mensagem, key_openai, "", True, True)
        codigo = response["codigo"]
        python_functions.save_python_code(codigo, path_Software_Development_py)


        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem, response, instructionsassistant, nameassistant)
        


        mensaxgem = f"""crie uma mensagem de commit para o pull request no github do codigo asseguir descrevendo as melhorias feitas:\n
        codigo melhorado:\n
        {codigo}\n
        codigo antigo:\n
        {python_content}
       
        """
        
        format = 'Responda no formato JSON Exemplo: {"mensagem": "mensagem de commit para o pull request..."}'
        mensagem = mensaxgem + format
        response = ResponseAgent.ResponseAgent_message_completions(mensagem, key_openai, "", True, True)
        commit_message = response["mensagem"]

        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem, response, instructionsassistant, nameassistant)
        

        title_prompt = f"""Crie um título para um pull request no GitHub com base no código e na mensagem de commit:
        código:
        {codigo}
        commit_message:
        {commit_message}
        """
        format = 'Responda no formato JSON Exemplo: {"nome_para_pr": "nome do pull request..."}'
        title_message = title_prompt + format
        response = ResponseAgent.ResponseAgent_message_completions(title_message, key_openai, "", True, True)
        pr_title = response.get("nome_para_pr", "Título do Pull Request")

        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(title_message, response, instructionsassistant, nameassistant)

        Software_Development_py = python_functions.analyze_txt(path_Software_Development_py)
        
        mensaxgem = f"""Realize melhorias no código e cria um pull request no repositório GitHub.\n
        repo_owner:\n
        A-I-O-R-G
        repo_name:\n
        {repo_name}\n
        branch_name:\n
        {branch_name}\n
        file_path:\n
        {path_Software_Development_py}\n
        commit_message:\n
        {commit_message}\n
        improvements:\n
        {Software_Development_py}\n
        pr_title:\n
        {pr_title}
        token:\n
        {github_token}
        """
        
        response = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensaxgem,
                                                                agent_id=AI_SignalMaster, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_SignalMaster,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_SignalMaster
                                                                )


        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensaxgem, response, instructionsassistant, nameassistant)
        




        #file_teste_path = CipherMind_Testing_in_Software_development.AI_CipherMind(script_version_1_path, path_doc)

        #github_username, github_password, github_tokenNexGenCoder = Github_functions.NexGenCoder_github_keys()
        #NexGenCoder_Testing_in_Software_development.AI_NexGenCoder(file_teste_path, repo_owner, repo_name, branch_name,  github_tokenNexGenCoder)




        return response







