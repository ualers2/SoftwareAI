

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
from softwareai.CoreApp._init_environment_ import load_env




class SoftwareDevelopment:
    def __init__(self, Software_Documentation,
                SoftwareImprovements_DataWeaver,
                SoftwareDevelopment_SignalMaster,
                SoftwareDevelopment_NexGenCoder):
        
        self.Software_Documentation = Software_Documentation
        self.SoftwareImprovements_DataWeaver = SoftwareImprovements_DataWeaver
        self.SoftwareDevelopment_SignalMaster = SoftwareDevelopment_SignalMaster
        self.SoftwareDevelopment_NexGenCoder = SoftwareDevelopment_NexGenCoder

    def AI_QuantumCore(
                    self,
                    appfb, client, repo_name,
                    timeline_file_path,
                    spreadsheet_file_path,
                    pre_project_file_path,
                    Roadmap_file_path,
                    analysis_txt_path,
                    UseVectorstoreToGenerateFiles = True
                    ):


        key = "AI_QuantumCore_Desenvolvedor_Pleno_de_Software_em_Python"
        nameassistant = "AI QuantumCore Desenvolvedor Pleno de Software em Python"
        model_select = "gpt-4o-mini-2024-07-18"
        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_1_image_for_vision_in_thread = None
        vectorstore_in_assistant = None
        vectorstore_in_Thread = None
        Upload_list_for_code_interpreter_in_thread = None

        github_username, github_token = GithubKeys.QuantumCore_github_keys()

        load_env(repo_name)

        key_openai = OpenAIKeysteste.keys()

        AI_QuantumCore, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionQuantumCore, nameassistant, model_select, tools_QuantumCore, vectorstore_in_assistant)

        


        if UseVectorstoreToGenerateFiles == True:
            file_paths = [os.path.abspath(os.path.join(os.path.dirname(__file__), "../../", f"projectstructure.txt")), timeline_file_path, spreadsheet_file_path, pre_project_file_path, Roadmap_file_path, analysis_txt_path]
            AI_QuantumCore = Agent_files_update.del_all_and_upload_files_in_vectorstore(appfb, client, AI_QuantumCore, "QuantumCore_Work_Environment", file_paths)
            mensagem = """Crie, salve automaticamente (usando autosave) um script main.py completo em Python com base nos nas informacoes do projeto fornecidos e armazenados em QuantumCore_Work_Environment

            Certifique-se de que o script:

            1. **Integre as informações** dos arquivos de forma lógica e coesa, combinando os requisitos de maneira eficiente.
            2. **Utilize boas práticas de programação** em Python, incluindo modularidade, tratamento de erros e documentação detalhada.
            3. **Inclua comentários explicativos** em todo o código para facilitar a compreensão e manutenção.
            4. **Garanta que o script seja funcional e executável** como um programa independente.

            ### Etapas a serem seguidas:
            1. **Criação e Salvamento:**
            - Desenvolva o script Python com base nos requisitos fornecidos.
            - Salve o script no diretório apropriado utilizando a função `autosave`.

            2. **Execução e Teste:**
            - Após salvar o script, execute-o automaticamente utilizando a função `execute_py` para verificar se ele atende aos requisitos e funciona corretamente.
            - Analise o resultado da execução para confirmar que o comportamento do script corresponde às expectativas.

            ### Objetivo Principal:
            O script deve atender a todos os requisitos especificados nos arquivos mencionados, adaptando a estrutura e a lógica conforme necessário para garantir clareza, eficiência e funcionalidade.

            Lembre-se de priorizar a qualidade do código e validar os resultados após a execução."""

        adxitional_instructions_QuantumCore = f"""
        estrutura do projeto esta armazenada em projectstructure.txt
        os caminho para salvar o main  {os.getenv('PATH_SOFTWARE_DEVELOPMENT_PY_ENV')}
        """
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensagem,
                                                                agent_id=AI_QuantumCore, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_QuantumCore,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_QuantumCore
                                                                )
        

        
                                            
        
                                            
        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem, response, instructionsassistant, nameassistant)


        if UseVectorstoreToGenerateFiles == True:
            file_paths = [os.getenv('PATH_SOFTWARE_DEVELOPMENT_PY_ENV'), os.path.abspath(os.path.join(os.path.dirname(__file__), "../../", f"environment.txt")), os.path.abspath(os.path.join(os.path.dirname(__file__), "../../", f"projectstructure.txt")), timeline_file_path, spreadsheet_file_path, pre_project_file_path, Roadmap_file_path, analysis_txt_path]
            AI_QuantumCore = Agent_files_update.del_all_and_upload_files_in_vectorstore(appfb, client, AI_QuantumCore, "QuantumCore_Work_Environment", file_paths)
            mensagem = f"""
            Siga os passos de desenvolvimento:
            1) Crie, salve automaticamente (usando autosave) o `setup.py` do projeto com base no `main.py`
            2) Crie, salve automaticamente (usando autosave) o `pyproject.toml` do projeto com base no  `main.py`
            3) Crie, salve automaticamente (usando autosave) o `LICENSE.txt` do projeto com base no `main.py`


            """

        adxitional_instructions_QuantumCore = f"""
        estrutura do projeto esta armazenada em projectstructure.txt
        todos os caminhos para salvar estao em environment.txt 
        """
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensagem,
                                                                agent_id=AI_QuantumCore, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_QuantumCore,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_QuantumCore
                                                                )
         
        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem, response, instructionsassistant, nameassistant)


        PATH_SOFTWARE_DEVELOPMENT_PY_ENV =  os.getenv("PATH_SOFTWARE_DEVELOPMENT_PY_ENV")
        read_PY = python_functions.analyze_txt(PATH_SOFTWARE_DEVELOPMENT_PY_ENV)

        path_Software_Development_py = os.getenv("PATH_SOFTWARE_DEVELOPMENT_PY_ENV")
        path_Analysis = os.getenv("PATH_ANALISE_ENV")
        path_Roadmap = os.getenv("PATH_ROADMAP_ENV")
        path_Spreadsheet = os.getenv("PATH_PLANILHA_PROJETO_ENV")
        path_Timeline = os.getenv("PATH_NOME_DO_CRONOGRAMA_ENV")
        path_Preproject = os.getenv("PATH_NAME_DOC_PRE_PROJETO_ENV")
        path_DOCUMENTACAO_ENV = os.getenv("PATH_DOCUMENTACAO_ENV")
        

        readme_file_path = self.Software_Documentation.CloudArchitect_Software_Documentation_Type_Create(appfb, client, path_Software_Development_py, path_Analysis, path_Roadmap, path_Spreadsheet, path_Timeline, path_Preproject, repo_name)
        #code_file_paths = [path_Software_Development_py]
        PATH_SOFTWARE_DEVELOPMENT_init_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_init_ENV")
        PATH_SOFTWARE_DEVELOPMENT_PY_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_PY_ENV")
        PATH_SOFTWARE_DEVELOPMENT_config_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_config_ENV")
        PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV")
        PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV")
        PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV")
        PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV")
        PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV")
        PATH_SOFTWARE_DEVELOPMENT_services___init___ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_services___init___ENV")
        PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV")
        PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV")
        PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV")
        PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV")
        PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV")
        PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV")
        PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV")
        PATH_SOFTWARE_DEVELOPMENT_Example_ENV = os.getenv("PATH_SOFTWARE_DEVELOPMENT_Example_ENV")
        PATH_Changelog = os.getenv("PATH_Changelog")
        PATH_SOFTWARE_DEVELOPMENT_SendToPip = os.getenv("PATH_SOFTWARE_DEVELOPMENT_SendToPip")
        requirements_file_path = os.getenv("PATH_SOFTWARE_DEVELOPMENT_Requirements_ENV")
        LICENSE_file_path = os.getenv("PATH_DOCUMENTACAO_LICENSE_ENV")
        setup_file_path = os.getenv("PATH_DOCUMENTACAO_setup_ENV")
        pyproject_file_path = os.getenv("PATH_pyproject")


        


        mensaxgem = f"""Realize o upload do projeto Python\n
        repo_name:\n
        {repo_name}\n
        setup_file_path:\n
        {setup_file_path}
        requirements_file_path:\n
        {requirements_file_path}
        LICENSE_file_path:\n
        {LICENSE_file_path}
        pyproject_file_path:\n
        {pyproject_file_path}
        PATH_SOFTWARE_DEVELOPMENT_init_ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_init_ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_PY_ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_PY_ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_config_ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_config_ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_services___init___ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_services___init___ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV}\n
        PATH_SOFTWARE_DEVELOPMENT_Example_ENV:\n
        {PATH_SOFTWARE_DEVELOPMENT_Example_ENV}\n
        PATH_Changelog:\n
        {PATH_Changelog}\n
        PATH_SOFTWARE_DEVELOPMENT_SendToPip:
        {PATH_SOFTWARE_DEVELOPMENT_SendToPip}\n
        token:\n
        {github_token}\n
        """
        #format = 'Responda no formato JSON Exemplo: {"nome": "nome..."}'
        #mensagem = mensaxgem + format
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensaxgem,
                                                                agent_id=AI_QuantumCore, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_QuantumCore,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_QuantumCore
                                                                )
        
        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensaxgem, response, instructionsassistant, nameassistant)
        
        
        print(response)

        mensaxgem = f"""Realiza o upload dos arquivos do projeto, incluindo documentação, timeline, roadmap e análises.\n
        repo_name:\n
        {repo_name}\n
        timeline_file_path:\n
        {timeline_file_path}\n
        spreadsheet_file_path:\n
        {spreadsheet_file_path}\n
        pre_project_file_path:\n
        {pre_project_file_path}\n
        Roadmap_file_path:\n
        {Roadmap_file_path}\n
        analise_file_path:\n
        {analysis_txt_path}\n
        token:\n
        {github_token}\n
        """
        #format = 'Responda no formato JSON Exemplo: {"nome": "nome..."}'
        #mensagem = mensaxgem + format
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensaxgem,
                                                                agent_id=AI_QuantumCore, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_QuantumCore,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_QuantumCore
                                                                )
        print(response)
        
        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensaxgem, response, instructionsassistant, nameassistant)
        
        code_python_software_old = python_functions.analyze_txt(os.getenv("PATH_SOFTWARE_DEVELOPMENT_PY_ENV"))
        # save_code_old = read_PY
        # pr_number = 1
        # branch_name = f"main_1"
        # for i in range(2):
        #     branch_name = f"main_{i + 1}"
            

        #     path_Software_Development_py = os.getenv("PATH_SOFTWARE_DEVELOPMENT_PY_ENV")

        #     flag_improvements = self.SoftwareImprovements_DataWeaver.AI_DataWeaver_improvements(appfb, client, path_Software_Development_py)
        #     print(flag_improvements)

        #     flag_SoftwareDevelopment_SignalMaster = self.SoftwareDevelopment_SignalMaster.AI_SignalMaster(appfb, client, path_Software_Development_py, repo_name, branch_name)
        #     print(flag_SoftwareDevelopment_SignalMaster)

        #     flag_SoftwareDevelopment_NexGenCoder = self.SoftwareDevelopment_NexGenCoder.AI_NexGenCoder(appfb, client, repo_name, pr_number)
        #     print(flag_SoftwareDevelopment_NexGenCoder)
            
            
        #     path_python_software_new = python_functions.analyze_txt(path_Software_Development_py)

        #     readme_file_path_improvements = self.Software_Documentation.CloudArchitect_Software_Documentation_Type_Update(appfb, client, repo_name, path_DOCUMENTACAO_ENV, code_python_software_old, path_python_software_new)

        #     code_python_software_old = python_functions.analyze_txt(path_Software_Development_py)
        return repo_name




        # mensaxgem = f"""crie um nome para a branch de 10 caracteres do pull request do repositorio no github:\n
        # repositorio:\n
        # {repo_name}\n
        # repo_description:\n
        # {repo_description}\n
        # """
        # format = 'Responda no formato JSON Exemplo: {"branch_name": "branch name..."}'
        # mensagem = mensaxgem + format
        # response = ResponseAgent.ResponseAgent_message_completions(mensagem, "", True)
        # branch_name = response["branch_name"]
        # repo_owner = "A-I-O-R-G"

        # flagAI_DataWeaver_improvements = software_improvements.AI_DataWeaver_improvements(path_Software_Development_py, repo_name, branch_name)
        # print(flagAI_DataWeaver_improvements)


        # file_teste_path = CipherMind_Testing_in_Software_development.AI_CipherMind(script_version_1_path, path_doc)

        # github_username, github_password, github_tokenNexGenCoder = Github_functions.NexGenCoder_github_keys()
        # NexGenCoder_Testing_in_Software_development.AI_NexGenCoder(file_teste_path, repo_owner, repo_name, branch_name,  github_tokenNexGenCoder)
        # flagquantumcore_review_pr = quantumcore_review_pr(repo_owner, repo_name, pr_number)
        # print(flagquantumcore_review_pr)


        # return response

    def QuantumCoreUpdate(
                    self,
                    appfb, client, repo_name,
                    UseVectorstoreToGenerateFiles = True
                    ):


        key = "AI_QuantumCore_Desenvolvedor_Pleno_de_Software_em_Python"
        nameassistant = "AI QuantumCore Desenvolvedor Pleno de Software em Python"
        model_select = "gpt-4o-mini-2024-07-18"

        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_1_image_for_vision_in_thread = None
        vectorstore_in_assistant = None
        vectorstore_in_Thread = None
        Upload_list_for_code_interpreter_in_thread = None
        onlyrepo_name = repo_name.replace("A-I-O-R-G/", "")
        load_env(onlyrepo_name)
        
        key_openai = OpenAIKeysteste.keys()

        github_username, github_token = GithubKeys.QuantumCore_github_keys()

        AI_QuantumCore, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionQuantumCore, nameassistant, model_select, tools_QuantumCore, vectorstore_in_assistant)

        
        branch_name = "main"  # Substitua pelo branch correto, se necessário

        
        AnalysisRequirements = self.get_file_content(repo_name, "AppMap/Analisys/AnalysisRequirements.txt", branch_name)
        PreProject = self.get_file_content(repo_name, "AppMap/PreProject/doc.txt", branch_name)
        RoadMap = self.get_file_content(repo_name, "AppMap/RoadMap/Roadmap.txt", branch_name)
        Schedule = self.get_file_content(repo_name, "AppMap/SpreadsheetAndTimeline/Schedule.txt", branch_name)
        Spreadsheet = self.get_file_content(repo_name, "AppMap/SpreadsheetAndTimeline/Spreadsheet.txt", branch_name)
        main = self.get_file_content(repo_name, f"{onlyrepo_name}/main.py", branch_name)
        config = self.get_file_content(repo_name, f"{onlyrepo_name}/config.py", branch_name)
        setup = self.get_file_content(repo_name, f"setup.py", branch_name)
        pyproject = self.get_file_content(repo_name, f"pyproject.toml", branch_name)


        Changelog = self.get_file_content(repo_name, f"{onlyrepo_name}/Changelog.env", branch_name)

        python_functions.save_TXT(AnalysisRequirements, os.getenv("PATH_ANALISE_ENV"), 'w')
        python_functions.save_TXT(PreProject, os.getenv("PATH_NAME_DOC_PRE_PROJETO_ENV"), 'w')
        python_functions.save_TXT(RoadMap, os.getenv("PATH_ROADMAP_ENV"), 'w')
        python_functions.save_TXT(Spreadsheet, os.getenv("PATH_PLANILHA_PROJETO_ENV"), 'w')
        python_functions.save_TXT(Schedule, os.getenv("PATH_NOME_DO_CRONOGRAMA_ENV"), 'w')
        python_functions.save_TXT(main, os.getenv("PATH_SOFTWARE_DEVELOPMENT_PY_ENV"), 'w')
        python_functions.save_TXT(config, os.getenv("PATH_SOFTWARE_DEVELOPMENT_config_ENV"), 'w')
        python_functions.save_TXT(setup, os.getenv("PATH_DOCUMENTACAO_setup_ENV"), 'w')
        python_functions.save_TXT(pyproject, os.getenv("PATH_pyproject"), 'w')
        
        python_functions.save_TXT(Changelog, os.getenv("PATH_Changelog"), 'w')


        if UseVectorstoreToGenerateFiles == True:
            file_paths = [os.path.abspath(os.path.join(os.path.dirname(__file__), "../../", f"environment.txt")), os.getenv("PATH_ANALISE_ENV"), os.getenv("PATH_NAME_DOC_PRE_PROJETO_ENV"), os.getenv("PATH_ROADMAP_ENV"), os.getenv("PATH_PLANILHA_PROJETO_ENV"), os.getenv("PATH_NOME_DO_CRONOGRAMA_ENV")]
            AI_QuantumCore = Agent_files_update.del_all_and_upload_files_in_vectorstore(appfb, client, AI_QuantumCore, "QuantumCore_Work_Environment", file_paths)
            mensaxgem = f"""Crie melhorias, salve e realize o upload no GitHub (usando autosave e autoupload) das melhorias para o arquivo `main.py` no repositório `{repo_name}`. 
            Baseie-se nos arquivos armazenados em `QuantumCore_Work_Environment` para implementar melhorias no código\n
            token: {github_token}
            regra adicional: use execute_py para verificar se o codigo criado com as melhorias nao tem erros 
            """
       

        adxitional_instructions_QuantumCore = f"""
        estrutura do projeto esta armazenada em environment.txt
        
        """
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensaxgem,
                                                                agent_id=AI_QuantumCore, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_QuantumCore,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_QuantumCore
                                                                )
        print(response)
        print(total_tokens)
        Agent_destilation.DestilationResponseAgent(mensaxgem, response, instructionsassistant, nameassistant)
        return response







    def get_file_content(self, repo_name, file_path, branch_name):

        github_username, github_token = GithubKeys.QuantumCore_github_keys()

        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
  

        file_url = f"https://api.github.com/repos/{repo_name}/contents/{file_path}?ref={branch_name}"
        response = requests.get(file_url, headers=headers)
        
        if response.status_code == 200:
            file_data = response.json()
            import base64
            content = base64.b64decode(file_data['content']).decode('utf-8')
            return content
        else:
            print(f"Erro ao acessar {file_path}. Status: {response.status_code}  {response.content}")
            return None
        








