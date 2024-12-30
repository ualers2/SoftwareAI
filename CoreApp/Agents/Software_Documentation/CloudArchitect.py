

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






# SoftwareAI
class Software_Documentation:
    def __init__(self):
        pass

    def CloudArchitect_Software_Documentation_Type_Create(self, appfb, client, path_python_software, path_Analysis, path_Roadmap, path_Spreadsheet, path_Timeline, path_Preproject):

        python_software = python_functions.analyze_txt(path_python_software)

        Analysis = python_functions.analyze_txt(path_Analysis)

        Roadmap = python_functions.analyze_txt(path_Roadmap)

        Spreadsheet = python_functions.analyze_txt(path_Spreadsheet)

        Timeline = python_functions.analyze_txt(path_Timeline)

        Preproject = python_functions.analyze_txt(path_Preproject)

        key = "AI_CloudArchitect_Software_Documentation"
        nameassistant = "AI CloudArchitect Software Documentation"
        model_select = "gpt-4o-mini-2024-07-18"
        
        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_1_image_for_vision_in_thread = None
        Upload_list_for_code_interpreter_in_thread = None
        vectorstore_in_assistant = None
        vectorstore_in_Thread = None



        key_openai = OpenAIKeysteste.keys()
        # name_app = "appx"
        # appfb = FirebaseKeysinit._init_app_(name_app)
        # client = OpenAIKeysinit._init_client_(key_openai)

        AI_CloudArchitect, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionCloudArchitect, nameassistant, model_select, tools_CloudArchitect, vectorstore_in_assistant)
        
        #vector_store_id = Agent_files.auth_or_create_vectorstore("DocGitHubData")
        #AI_CloudArchitect = Agent_files_update.update_vectorstore_in_agent(AI_CloudArchitect, [vector_store_id])
        
        mensagem = f"""
        Crie a Documentacao para o github desse software com base no codigo do software e nas documentacoes\n
        Codigo Software:\n
        {python_software}\n
        Documentacao Analysis:\n
        {Analysis}\n
        Documentacao Roadmap:\n
        {Roadmap}\n
        Documentacao Spreadsheet:\n
        {Spreadsheet}\n
        Documentacao Timeline:\n
        {Timeline}\n
        Documentacao Preproject:\n
        {Preproject}\n
        """
        rregras = "Regras: NÃO use a function update_readme_to_github"
        mensagem_final = mensagem + rregras
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensagem_final,
                                                                agent_id=AI_CloudArchitect, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_CloudArchitect,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_CloudArchitect
                                                                )

        path_Documentacao = os.getenv("PATH_DOCUMENTACAO_ENV")
        print(response)

        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem_final, response, instructionsassistant, nameassistant)
        

        # # referencias = """remova as referencias a criacao da documentacao por exemplo:\n
        # #     ```json
        # #         {
        # #             "status_da_documentacao": "Documentação criada com sucesso.",
        # #             "secoes_documentadas": [
        # #                 "Introdução",
        # #                 "Funcionalidade",
        # #                 "Instalação",
        # #                 "Uso",
        # #                 "Referência de API",
        # #                 "Contribuição",
        # #                 "Licença"
        # #             ],
        # #             "observacoes": "A documentação deve ser mantida atualizada conforme novas funcionalidades "
        # #         }
        # #     ```
        # # """

        mensaxgem = f"""deixe essa documentacao do github asseguir no formato markdown: \n {response}"""
        format = 'Responda no formato JSON Exemplo: {"documentacao": "documentacao..."}'
        mensagem = mensaxgem + format
        response = ResponseAgent.ResponseAgent_message_completions(mensagem, key_openai, "", True, True)
        documentacao_corrigida = response["documentacao"]
        print(documentacao_corrigida)
        python_functions.save_TXT(documentacao_corrigida, path_Documentacao, "w")

        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem, response, instructionsassistant, nameassistant)
        
        self.diretorio_script = os.path.dirname(os.path.abspath(__file__))
        self.path_DocGitHubDataREADME = os.path.join(self.diretorio_script,  '../../../',  'CoreCompany', 'DocGitHubData', f"README{random.randint(30, 900)}.md")
        self.path_DocGitHubData = os.path.join(self.diretorio_script,  '../../../', 'CoreCompany', 'DocGitHubData')
        self.path_DocGitHubData_log = os.path.join(self.diretorio_script,  '../../../',  'CoreCompany', 'docs_uploaded.log')

        python_functions.save_TXT(documentacao_corrigida, self.path_DocGitHubDataREADME, "w")

        self.check_and_upload_docs(appfb, client)

        return path_Documentacao



    def CloudArchitect_Software_Documentation_Type_Update(self, appfb, client, repo_name, path_readme, code_python_software_old, code_path_python_software_new):

        
        Readme = python_functions.analyze_txt(path_readme)

        # python_software_old = python_functions.analyze_txt(code_python_software_old)

        # python_software_new = python_functions.analyze_txt(code_path_python_software_new)

        # Analysis = python_functions.analyze_txt(path_Analysis)

        # Roadmap = python_functions.analyze_txt(path_Roadmap)

        # Spreadsheet = python_functions.analyze_txt(path_Spreadsheet)

        # Timeline = python_functions.analyze_txt(path_Timeline)

        # Preproject = python_functions.analyze_txt(path_Preproject)

        key = "AI_CloudArchitect_Software_Documentation"
        nameassistant = "AI CloudArchitect Software Documentation"
        model_select = "gpt-4o-mini-2024-07-18"
        
        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_1_image_for_vision_in_thread = None
        Upload_list_for_code_interpreter_in_thread = None
        vectorstore_in_assistant = None
        vectorstore_in_Thread = None



        key_openai = OpenAIKeysteste.keys()
        # name_app = "appx"
        # appfb = FirebaseKeysinit._init_app_(name_app)
        # client = OpenAIKeysinit._init_client_(key_openai)


        AI_CloudArchitect, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionCloudArchitect, nameassistant, model_select, tools_CloudArchitect, vectorstore_in_assistant)

        # vector_store_id = Agent_files.auth_or_create_vectorstore("DocGitHubData")
        #AI_CloudArchitect = Agent_files_update.update_vectorstore_in_agent(AI_CloudArchitect, [vector_store_id])
        
        mensagem = f"""
        Atualize a Documentacao atual do github desse software com base no codigo do software antigo e o software novo \n
        Repo Name:\n
        {repo_name}\n
        Documentacao atual do github:\n
        {Readme}\n
        codigo python do software antigo :\n
        {code_python_software_old}
        codigo python do software novo :\n
        {code_path_python_software_new}\n

        """
        # Documentacao Analysis:\n
        # {Analysis}\n
        # Documentacao Roadmap:\n
        # {Roadmap}\n
        # Documentacao Spreadsheet:\n
        # {Spreadsheet}\n
        # Documentacao Timeline:\n
        # {Timeline}\n
        # Documentacao Preproject:\n
        # {Preproject}\n
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensagem,
                                                                agent_id=AI_CloudArchitect, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_CloudArchitect,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_CloudArchitect
                                                                )

        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem, response, instructionsassistant, nameassistant)
        
        path_Documentacao = os.getenv("PATH_DOCUMENTACAO_ENV")
        print(response)
        

        mensaxgem = f"""deixe essa documentacao do github asseguir aprensentavel ao publico: \n {response}"""
        
        # referencias = """remova as referencias a criacao da documentacao por exemplo:\n
        #     ```json
        #         {
        #             "status_da_documentacao": "Documentação criada com sucesso.",
        #             "secoes_documentadas": [
        #                 "Introdução",
        #                 "Funcionalidade",
        #                 "Instalação",
        #                 "Uso",
        #                 "Referência de API",
        #                 "Contribuição",
        #                 "Licença"
        #             ],
        #             "observacoes": "A documentação deve ser mantida atualizada conforme novas funcionalidades "
        #         }
        #     ```
        # """

        format = 'Responda no formato JSON Exemplo: {"documentacao_corrigida": "documentacao corrigida..."}'
        mensagem = mensaxgem + format
        response = ResponseAgent.ResponseAgent_message_completions(mensagem, key_openai, "", True, True)
        documentacao_corrigida = response["documentacao_corrigida"]
        print(documentacao_corrigida)
        python_functions.save_TXT(documentacao_corrigida, path_Documentacao, "w")

        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensagem, response, instructionsassistant, nameassistant)
        
        self.diretorio_script = os.path.dirname(os.path.abspath(__file__))
        self.path_DocGitHubDataREADME = os.path.join(self.diretorio_script, '../../../', 'CoreCompany', 'DocGitHubData', f"README{random.randint(30, 900)}.md")
        self.path_DocGitHubData = os.path.join(self.diretorio_script, '../../../', 'CoreCompany', 'DocGitHubData')
        self.path_DocGitHubData_log = os.path.join(self.diretorio_script, '../../../', 'CoreCompany', 'docs_uploaded.log')

        python_functions.save_TXT(documentacao_corrigida, self.path_DocGitHubDataREADME, "w")

        github_username, github_token = GithubKeys.CloudArchitect_github_keys()

        mensagem = f"""
        Atualiza o Readme do repositorio no github\n
        file_path_readme_improvements:\n
        {path_readme}\n
        repo_name:\n
        {repo_name}\n
        token:\n
        {github_token}\n

        """

        
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensagem,
                                                                agent_id=AI_CloudArchitect, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_CloudArchitect,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_CloudArchitect
                                                                )
        path_Documentacao = os.getenv("PATH_DOCUMENTACAO_ENV")
        print(response)
                                            
        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensaxgem, response, instructionsassistant, nameassistant)
        
        self.check_and_upload_docs(appfb, client)
        
        return path_Documentacao




    def read_uploaded_files(self):
        """Lê o arquivo de log e retorna um conjunto de arquivos já carregados"""
        if os.path.exists(self.path_DocGitHubData_log):
            with open(self.path_DocGitHubData_log, "r") as log:
                uploaded_files = {line.strip() for line in log.readlines()}
        else:
            uploaded_files = set()
        return uploaded_files

    def log_uploaded_file(self, file_name):
        """Registra um arquivo como carregado no arquivo de log"""
        with open(self.path_DocGitHubData_log, "a") as log:
            log.write(f"{file_name}\n")

    def check_and_upload_docs(self, app1, client,  name="DocGitHubData"):
        """Verifica novos arquivos .md e realiza o upload, registrando-os no log"""
        uploaded_files = self.read_uploaded_files()
        files = [f for f in os.listdir(self.path_DocGitHubData) if f.lower().endswith('.md')]
        new_files = [f for f in files if f not in uploaded_files]
        if new_files:
            for file in new_files:
                file_path = os.path.join(self.path_DocGitHubData, file)
                self.upload_to_vectorstore(app1, client, file_path, name)
                uploaded_files.add(file) 
                self.log_uploaded_file(file) 
            print(f"Novos arquivos carregados para {name}: {', '.join(new_files)}")
        else:
            print("Nenhum novo arquivo encontrado.")

    def upload_to_vectorstore(self, app1, client,  file_path, name):
 
        paths_to_upload  = [
            file_path
        ]

        vector_store_id = Agent_files.auth_or_create_vectorstore(app1, client, name, paths_to_upload, file_path)
        print(vector_store_id)
        print(paths_to_upload)
        print(file_path)
        

