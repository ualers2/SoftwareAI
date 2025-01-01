

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

    ##############################################################################################
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




        
        # path_Conhecimentos_python = r"C:\Users\ualer\Downloads\Saas do site\A-I-O-R-G\AI_Team_Software_Development\Conhecimentos_python_em_pdf"
        # name_for_vectorstore = "Conhecimentos_python_em_pdf"
        # file_path_Conhecimentos_python_em_pdf = [
        #     f"{path_Conhecimentos_python}/Automate the Boring Stuff with Python.pdf",
        #     f"{path_Conhecimentos_python}/Effective Python 2nd.pdf",
        #     f"{path_Conhecimentos_python}/Fluent Python.pdf",
        #     f"{path_Conhecimentos_python}/pep8-readthedocs-io-en-release-1.7.x.pdf",
        #     f"{path_Conhecimentos_python}/pep257-readthedocs-io-en-0.6.0.pdf",
        #     f"{path_Conhecimentos_python}/python_para_desenvolvedores.pdf",
        #     f"{path_Conhecimentos_python}/python-clean-code-best-practices-and-techniques-for-writing-clear-concise-and-maintainable-code-publishdrivenbsped.pdf",
        #     f"{path_Conhecimentos_python}/python-cookbook-3rd-edition-9781449357337-1449357334.pdf",
        #     f"{path_Conhecimentos_python}/python-type-checking-readthedocs-io-en-latest.pdf",
        # ]
        # list_file_id_Conhecimentos_python_em_pdf = Agent_files.auth_or_upload_multiple_files(name_for_vectorstore, file_path_Conhecimentos_python_em_pdf)
        # vector_store_id_conhecimentospython = Agent_files.auth_or_create_vector_store_with_multiple_files(name_for_vectorstore, list_file_id_Conhecimentos_python_em_pdf)


        # path_local = r"C:\Users\ualer\Downloads\Saas do site\Youtube Downloader (dev)"
        # youtube_downloader_software_name = "youtube_downloader"
        # file_path_youtube_downloader_software_in_company = [

        #     f"{path_local}/main.py",
        #     f"{path_local}/CoreApp/Securityclass.py",
        #     f"{path_local}/Update.py",
        #     f"{path_local}/Update_exe.py", f"{path_local}/Update_Update.py",
        #     f"{path_local}/YoutubeDownloader.py", f"{path_local}/Enviar_atualizacao.py",
        #     f"{path_local}/Convert_ui.py", f"{path_local}/uisave/UI_Convert.py",
        #     #f"{path_local}/uisave/latestchannelstreams.xml", f"{path_local}/uisave/main_window.xml",
        #     f"{path_local}/CoreApp/ui/latestchannelstreams_ui.py", f"{path_local}/CoreApp/ui/main_window_ui.py"

            
        # ]

        # path_localTwitch = r"C:\Users\ualer\Downloads\Saas do site\Twitch Downloader (dev)"
        # Twitch_downloader_software_name = "Twitch_downloader"
        # file_path_Twitch_downloader_software_in_company = [

        #     f"{path_localTwitch}/main.py",
        #     f"{path_localTwitch}/CoreApp/Securityclass.py",
        #     f"{path_localTwitch}/Update.py",
        #     f"{path_localTwitch}/Update_exe.py", f"{path_localTwitch}/Update_Update.py",
        #     f"{path_localTwitch}/TwitchDownloader.py", f"{path_localTwitch}/Enviar_atualizacao.py",
        #     f"{path_localTwitch}/Convert_ui.py", f"{path_localTwitch}/uisave/UI_Convert.py",
        #     #f"{path_localTwitch}/uisave/mode_all_vod_dialog.xml", f"{path_localTwitch}/uisave/login.xml", f"{path_localTwitch}/uisave/main_window.xml",
        #     f"{path_localTwitch}/CoreApp/ui/mode_all_vod_dialog_ui.py", f"{path_localTwitch}/CoreApp/ui/main_window_ui.py", f"{path_localTwitch}/CoreApp/ui/login_ui.py"
            
        # ]

        # vector_store_id_youtube_downloader_software = Agent_files.auth_or_create_vectorstore(youtube_downloader_software_name, file_path_youtube_downloader_software_in_company)
        
        # vector_store_id_Twitch_downloader_software = Agent_files.auth_or_create_vectorstore(Twitch_downloader_software_name, file_path_Twitch_downloader_software_in_company)
        


        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_1_image_for_vision_in_thread = None
        vectorstore_in_assistant = None
        vectorstore_in_Thread = None
        Upload_list_for_code_interpreter_in_thread = None

        github_username, github_token = GithubKeys.QuantumCore_github_keys()

        load_env("environment.env", repo_name)

        key_openai = OpenAIKeysteste.keys()

        AI_QuantumCore, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionQuantumCore, nameassistant, model_select, tools_QuantumCore, vectorstore_in_assistant)
        
        if UseVectorstoreToGenerateFiles == True:
            file_paths = [timeline_file_path, spreadsheet_file_path, pre_project_file_path, Roadmap_file_path, analysis_txt_path]
            AI_QuantumCore = Agent_files_update.del_all_and_upload_files_in_vectorstore(appfb, client, AI_QuantumCore, "QuantumCore_Work_Environment", file_paths)
            mensaxgem = f"""crie um script em python com base nos requisitos fornecidos no analysis e nos outros documentos que estao armazenados em QuantumCore_Work_Environment \n
            """

        else:
            
            read_timeline_file_path = python_functions.analyze_txt(timeline_file_path)
            read_spreadsheet_file_path = python_functions.analyze_txt(spreadsheet_file_path)
            read_pre_project_file_path = python_functions.analyze_txt(pre_project_file_path)
            read_Roadmap_file_path = python_functions.analyze_txt(Roadmap_file_path)
            read_analysis_txt_path = python_functions.analyze_txt(analysis_txt_path)

            mensaxgem = f"""crie um script em python com base nos requisitos fornecidos no analysis e nos outros documentos\n
            
            analysis\n
            {read_analysis_txt_path}\n
            timeline\n
            {read_timeline_file_path}\n
            spreadsheet\n
            {read_spreadsheet_file_path}\n
            preproject\n
            {read_pre_project_file_path}\n
            Roadmap\n
            {read_Roadmap_file_path}\n

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
        
                                            
        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensaxgem, response, instructionsassistant, nameassistant)
        
        path_Software_Development_txt =  os.getenv("PATH_SOFTWARE_DEVELOPMENT_TXT_ENV")
        python_functions.save_TXT(response, path_Software_Development_txt, "w")
        python_software_in_txt = python_functions.analyze_txt(path_Software_Development_txt)


        mensaxgem = f"""corrija todos os erros de sintaxe do codigo asseguir :\n
        {python_software_in_txt}
        """
        regras = "\ncaso nao haja erros de sintaxe retorne o codigo\n"
        format = 'Responda no formato JSON Exemplo: {"codigo": "import..."}'
        path_Software_Development_py = os.getenv("PATH_SOFTWARE_DEVELOPMENT_PY_ENV")
        mensagem = mensaxgem + regras + format
        response = ResponseAgent.ResponseAgent_message_completions(mensagem, key_openai, "", True, True)
        codigo = response["codigo"]
        python_functions.save_python_code(codigo, path_Software_Development_py)

        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem, response, instructionsassistant, nameassistant)
    

        mensaxgem = f"""crie uma descricao de 250 caracteres para o repositorio desse codigo no github:\n
        {codigo}
        """
        format = 'Responda no formato JSON Exemplo: {"descricao": "descricao..."}'
        mensagem = mensaxgem + format
        response = ResponseAgent.ResponseAgent_message_completions(mensagem, key_openai, "", True, True)
        repo_description = response["descricao"]


        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem, response, instructionsassistant, nameassistant)
        

        path_Software_Development_py = os.getenv("PATH_SOFTWARE_DEVELOPMENT_PY_ENV")
        path_Analysis = os.getenv("PATH_ANALISE_ENV")
        path_Roadmap = os.getenv("PATH_ROADMAP_ENV")
        path_Spreadsheet = os.getenv("PATH_PLANILHA_PROJETO_ENV")
        path_Timeline = os.getenv("PATH_NOME_DO_CRONOGRAMA_ENV")
        path_Preproject = os.getenv("PATH_NAME_DOC_PRE_PROJETO_ENV")
        path_DOCUMENTACAO_ENV = os.getenv("PATH_DOCUMENTACAO_ENV")
        

        readme_file_path = self.Software_Documentation.CloudArchitect_Software_Documentation_Type_Create(appfb, client, path_Software_Development_py, path_Analysis, path_Roadmap, path_Spreadsheet, path_Timeline, path_Preproject)
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

        requirements_file_path = os.getenv("PATH_SOFTWARE_DEVELOPMENT_Requirements_ENV")
        LICENSE_file_path = os.getenv("PATH_DOCUMENTACAO_LICENSE_ENV")
        setup_file_path = os.getenv("PATH_DOCUMENTACAO_setup_ENV")
        pyproject_file_path = os.getenv("PATH_pyproject")

        mensaxgem = f"""Cria um repositório no GitHub e realiza o upload do projeto Python.\n
        repo_name:\n
        {repo_name}\n
        repo_description:\n
        {repo_description}\n
        setup_file_path:\n
        {setup_file_path}
        requirements_file_path:\n
        {requirements_file_path}
        LICENSE_file_path:\n
        {LICENSE_file_path}
        pyproject_file_path:\n
        {pyproject_file_path}
        readme_file_path:\n
        {readme_file_path}\n
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
        save_code_old = codigo
        pr_number = 1
        branch_name = f"main_1"
        for i in range(2):
            branch_name = f"main_{i + 1}"
            

            path_Software_Development_py = os.getenv("PATH_SOFTWARE_DEVELOPMENT_PY_ENV")

            flag_improvements = self.SoftwareImprovements_DataWeaver.AI_DataWeaver_improvements(appfb, client, path_Software_Development_py)
            print(flag_improvements)

            flag_SoftwareDevelopment_SignalMaster = self.SoftwareDevelopment_SignalMaster.AI_SignalMaster(appfb, client, path_Software_Development_py, repo_name, branch_name)
            print(flag_SoftwareDevelopment_SignalMaster)

            flag_SoftwareDevelopment_NexGenCoder = self.SoftwareDevelopment_NexGenCoder.AI_NexGenCoder(appfb, client, repo_name, pr_number)
            print(flag_SoftwareDevelopment_NexGenCoder)
            
            
            path_python_software_new = python_functions.analyze_txt(path_Software_Development_py)

            readme_file_path_improvements = self.Software_Documentation.CloudArchitect_Software_Documentation_Type_Update(appfb, client, repo_name, path_DOCUMENTACAO_ENV, code_python_software_old, path_python_software_new)

            code_python_software_old = python_functions.analyze_txt(path_Software_Development_py)

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







