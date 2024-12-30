

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





class software_improvements:
    def __init__(self):
        pass

    def AI_DataWeaver_improvements(self, appfb, client, file_path):
        """
        Nome da IA: DataWeaver \n
        Função: ideas for software improvements \n
        Horario de trabalho: 1H
        
        :param file_path: str \n
        :param repo_name: str \n
        :param branch_name: str \n
        
        :param output: path_to_py
        """   


        python_content = python_functions.analyze_file(file_path) 

        key = "AI_DataWeaver_ideas_for_software_improvements"
        nameassistant = "AI DataWeaver ideas for software improvements"
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


        # path_localYoutube = r"C:\Users\ualer\Downloads\Saas do site\Youtube Downloader (dev)"
        # path_localTwitch = r"C:\Users\ualer\Downloads\Saas do site\Twitch Downloader (dev)"
        # all_software_name = "All_Software_in_company"
        # file_path_all_software_in_company = [

        #     f"{path_localTwitch}/main_Twitch_Downloader.py",
        #     f"{path_localTwitch}/CoreApp/Securityclass_Twitch_Downloader.py",
        #     f"{path_localTwitch}/Update_Twitch_Downloader.py",
        #     f"{path_localTwitch}/Update_exe_Twitch_Downloader.py", f"{path_localTwitch}/Update_Update_Twitch_Downloader.py",
        #     f"{path_localTwitch}/TwitchDownloader.py", f"{path_localTwitch}/Enviar_atualizacao_Twitch_Downloader.py",
        #     f"{path_localTwitch}/Convert_ui_Twitch_Downloader.py", f"{path_localTwitch}/uisave/UI_Convert_Twitch_Downloader.py",
        #     #f"{path_localTwitch}/uisave/mode_all_vod_dialog.xml", f"{path_localTwitch}/uisave/login.xml", f"{path_localTwitch}/uisave/main_window.xml",
        #     f"{path_localTwitch}/CoreApp/ui/mode_all_vod_dialog_ui_Twitch_Downloader.py",
        #     f"{path_localTwitch}/CoreApp/ui/main_window_ui_Twitch_Downloader.py", f"{path_localTwitch}/CoreApp/ui/login_ui_Twitch_Downloader.py",
           
        #     f"{path_localYoutube}/main_Youtube_Downloader.py",
        #     f"{path_localYoutube}/CoreApp/Securityclass_Youtube_Downloader.py",
        #     f"{path_localYoutube}/Update_Youtube_Downloader.py",
        #     f"{path_localYoutube}/Update_exe_Youtube_Downloader.py", f"{path_localYoutube}/Update_Update_Youtube_Downloader.py",
        #     f"{path_localYoutube}/YoutubeDownloader.py", f"{path_localYoutube}/Enviar_atualizacao_Youtube_Downloader.py",
        #     f"{path_localYoutube}/Convert_ui_Youtube_Downloader.py", f"{path_localYoutube}/uisave/UI_Convert_Youtube_Downloader.py",
        #     #f"{path_local}/uisave/latestchannelstreams.xml", f"{path_local}/uisave/main_window.xml",
        #     f"{path_localYoutube}/CoreApp/ui/latestchannelstreams_ui_Youtube_Downloader.py", f"{path_localYoutube}/CoreApp/ui/main_window_ui_Youtube_Downloader.py"

        # ]

        # vector_store_id_all_software_in_company = Agent_files.auth_or_create_vectorstore(all_software_name, file_path_all_software_in_company)


        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_list_for_code_interpreter_in_thread = None
        Upload_1_image_for_vision_in_thread = None
        vectorstore_in_assistant = None #[vector_store_id_all_software_in_company]
        vectorstore_in_Thread = None

        github_username, github_token = GithubKeys.SignalMaster_github_keys()

        key_openai = OpenAIKeysteste.keys()
        # name_app = "appx"
        # appfb = FirebaseKeysinit._init_app_(name_app)
        # client = OpenAIKeysinit._init_client_(key_openai)

        
        AI_DataWeaver, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionDataWeaver, nameassistant, model_select, tools_DataWeaver, vectorstore_in_assistant)
        
        
        mensaxgem = f"""melhore esse script em python com novas funcionalidades \n
        script:\n
        {python_content}
        """
        format = 'Responda no formato JSON Exemplo: {"codigo": "import..."}'
        mensagem = mensaxgem + format
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensagem,
                                                                agent_id=AI_DataWeaver, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_DataWeaver,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_CloudArchitect
                                                                )
        print(response)

        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem, response, instructionsassistant, nameassistant)

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



        #flagAI_SignalMaster = SoftwareDevelopment_SignalMaster.AI_SignalMaster(path_Software_Development_py, repo_name, branch_name)
       



        return path_Software_Development_py