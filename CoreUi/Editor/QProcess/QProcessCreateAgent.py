
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *



class QProcessCreateAgent(QThread):
    ModalSucess = Signal(str)
    ModalInfo = Signal(str)
    finishedqthread = Signal()
    def __init__(self,
                KeyInFirebase_AgentCreate,
                ModelSelect_AgentCreate,
                Vectorstoreinassistant_AgentCreate,
                VectorstoreinThread_AgentCreate,
                Upload1fileinThread_AgentCreate,
                Upload1fileinmessage_AgentCreate,
                Upload1imageforvisioninThread_AgentCreate,
                Uploadlistfileforcodeinterpreterinthread_AgentCreate,
                Promptmain_AgentCreate,
                PromptRules_AgentCreate,
                PromptExample_AgentCreate,
                NameAgent_AgentCreate,
                category_target,
                namefunction_agentcreate,
                AgentToolsAgentCreate,
                InstructionAgentCreate,
                FunctionPythonAgentCreate,
                AditionalInstructionsAgentCreate,
                FunctionPythonOutputAgentCreate,
                UseVectorstoreToGenerateFiles,
                ArgsCreatetextedit,
                CurrentArgs_AgentCreate,
                StorageAgentCompletions_AgentCreate,
                StorageAgentOutput_AgentCreate,
                StoreFormatJsonAndJsonl_AgentCreate,
                AgentKeysGithubName,
                AgentKeysOpenAIName,
                AgentKeyOpenAI,
                name_app
            ):
        
        super().__init__()

        self.KeyInFirebase_AgentCreate = KeyInFirebase_AgentCreate
        self.ModelSelect_AgentCreate = ModelSelect_AgentCreate
        self.Vectorstoreinassistant_AgentCreate = Vectorstoreinassistant_AgentCreate
        self.VectorstoreinThread_AgentCreate = VectorstoreinThread_AgentCreate
        self.Upload1fileinThread_AgentCreate = Upload1fileinThread_AgentCreate
        self.Upload1fileinmessage_AgentCreate = Upload1fileinmessage_AgentCreate
        self.Upload1imageforvisioninThread_AgentCreate = Upload1imageforvisioninThread_AgentCreate
        self.Uploadlistfileforcodeinterpreterinthread_AgentCreate = Uploadlistfileforcodeinterpreterinthread_AgentCreate
        self.Promptmain_AgentCreate = Promptmain_AgentCreate
        self.PromptRules_AgentCreate = PromptRules_AgentCreate
        self.PromptExample_AgentCreate = PromptExample_AgentCreate
        self.NameAgent_AgentCreate = NameAgent_AgentCreate
        self.AgentCategory_AgentCreate = category_target
        self.namefunction_agentcreate = namefunction_agentcreate
        self.AgentToolsAgentCreate = AgentToolsAgentCreate
        self.InstructionAgentCreate = InstructionAgentCreate
        self.FunctionPythonAgentCreate = FunctionPythonAgentCreate
        self.AditionalInstructionsAgentCreate = AditionalInstructionsAgentCreate
        self.FunctionPythonOutputAgentCreate = FunctionPythonOutputAgentCreate
        self.UseVectorstoreToGenerateFiles = UseVectorstoreToGenerateFiles
        self.ArgsCreatetextedit = ArgsCreatetextedit
        self.CurrentArgs_AgentCreate = CurrentArgs_AgentCreate

        self.StorageAgentCompletions_AgentCreate = StorageAgentCompletions_AgentCreate
        self.StorageAgentOutput_AgentCreate = StorageAgentOutput_AgentCreate
        self.StoreFormatJsonAndJsonl_AgentCreate = StoreFormatJsonAndJsonl_AgentCreate
        self.AgentKeysGithubName = AgentKeysGithubName
        self.AgentKeysOpenAIName = AgentKeysOpenAIName
        self.AgentKeyOpenAI = AgentKeyOpenAI
        self.name_app = name_app

        self._stop_flag = False
        self.cancelled = False

    def run(self):

        KeyInFirebase_AgentCreate = self.KeyInFirebase_AgentCreate
        ModelSelect_AgentCreate = self.ModelSelect_AgentCreate
        if self.Vectorstoreinassistant_AgentCreate.strip():
            Vectorstoreinassistant_AgentCreate = [self.Vectorstoreinassistant_AgentCreate]
        else:
            Vectorstoreinassistant_AgentCreate = None

        if self.VectorstoreinThread_AgentCreate.strip():
            VectorstoreinThread_AgentCreate = [self.VectorstoreinThread_AgentCreate]
        else:
            VectorstoreinThread_AgentCreate = None


        if self.Upload1fileinThread_AgentCreate.strip():
            Upload1fileinThread_AgentCreate = self.Upload1fileinThread_AgentCreate
        else:
            Upload1fileinThread_AgentCreate = None


        if self.Upload1fileinmessage_AgentCreate.strip():
            Upload1fileinmessage_AgentCreate = self.Upload1fileinmessage_AgentCreate
        else:
            Upload1fileinmessage_AgentCreate = None


        if self.Upload1imageforvisioninThread_AgentCreate.strip():
            Upload1imageforvisioninThread_AgentCreate = self.Upload1imageforvisioninThread_AgentCreate
        else:
            Upload1imageforvisioninThread_AgentCreate = None


        if self.Uploadlistfileforcodeinterpreterinthread_AgentCreate.strip():
            Uploadlistfileforcodeinterpreterinthread_AgentCreate = [self.Uploadlistfileforcodeinterpreterinthread_AgentCreate]
        else:
            Uploadlistfileforcodeinterpreterinthread_AgentCreate = None

        Promptmain_AgentCreate = self.Promptmain_AgentCreate
        PromptRules_AgentCreate = self.PromptRules_AgentCreate
        PromptExample_AgentCreate = self.PromptExample_AgentCreate
        NameAgent_AgentCreate = self.NameAgent_AgentCreate
        category_target = self.AgentCategory_AgentCreate
        UseVectorstoreToGenerateFiles = self.UseVectorstoreToGenerateFiles

        self.AgentToolsAgentCreate_()

        time.sleep(1.5)

        self.InstructionAgentCreate_()

        time.sleep(1.5)

        self.FunctionPythonAgentCreate_()

        time.sleep(1.5)

        self.FunctionPythonOutputAgentCreate_()


        time.sleep(1.5)

        print("z")

        
        print("1")

        if self.ArgsCreatetextedit == None:
            processandoargs_str = f""
        else:
            argslist =  self.ArgsCreatetextedit.split(", ")
            processandoargs = []
            for arg in argslist:
                if self.CurrentArgs_AgentCreate == "txt":
                    processandoargs.append(f"            read_path_{arg} = python_functions.analyze_txt(self.{arg})")  # Note a indentação
                elif self.CurrentArgs_AgentCreate == "py":
                    processandoargs.append(f"            read_path_{arg} = python_functions.analyze_file(self.{arg})")

                elif self.CurrentArgs_AgentCreate == "agent":
                    processandoargs.append(f"")

            processandoargs_str = "\n".join(processandoargs)

            if self.CurrentArgs_AgentCreate == "agent":
                processandoargs_strx = ""

            elif self.CurrentArgs_AgentCreate == "txt":
                argslistx =  self.ArgsCreatetextedit.split(", ")
                processandoargsx = []
                for argx in argslistx:
                    processandoargsx.append(f"            {{read_path_{argx}}}") 
                processandoargs_strx = "\n".join(processandoargsx)

            elif self.CurrentArgs_AgentCreate == "py":
                argslistx =  self.ArgsCreatetextedit.split(", ")
                processandoargsx = []
                for argx in argslistx:
                    processandoargsx.append(f"            {{read_path_{argx}}}") 
                processandoargs_strx = "\n".join(processandoargsx)


        if self.CurrentArgs_AgentCreate == "agent":

            vectorstorecode = F'''

        {NameAgent_AgentCreate}, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(app{self.name_app}, client, key, instruction{NameAgent_AgentCreate}, nameassistant, model_select, tools_{NameAgent_AgentCreate}, vectorstore_in_assistant)
            
        mensagem = f"""
{Promptmain_AgentCreate}
{processandoargs_strx}
            """

        


            '''

        else:

            vectorstorecode = F'''

        if UseVectorstoreToGenerateFiles == True:
            name_for_vectorstore = key
            file_paths = [{', '.join([f'f"{{self.{arg.strip()}}}"' for arg in self.ArgsCreatetextedit.split(',')])}]
            vector_store_id = Agent_files.auth_vectorstoreAdvanced(app{self.name_app}, client, name_for_vectorstore, file_paths)

            {NameAgent_AgentCreate}, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(app{self.name_app}, client, key, instruction{NameAgent_AgentCreate}, nameassistant, model_select, tools_{NameAgent_AgentCreate}, vectorstore_in_assistant)

            {NameAgent_AgentCreate} = Agent_files_update.update_vectorstore_in_agent(client, {NameAgent_AgentCreate}, [vector_store_id])

            mensagem = f"""
    {Promptmain_AgentCreate}
            """

        else:
    
{processandoargs_str}

            {NameAgent_AgentCreate}, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(app{self.name_app}, client, key, instruction{NameAgent_AgentCreate}, nameassistant, model_select, tools_{NameAgent_AgentCreate}, vectorstore_in_assistant)
            
            mensagem = f"""
{Promptmain_AgentCreate}
{processandoargs_strx}
            """

        


            '''
        
        print('1')
        # instruction  = self.InstructionAgentCreate
        # name_app = self.name_app
        # app = FirebaseKeysinit._init_app_(name_app)
        # client = OpenAIKeysinit._init_client_(self.AgentKeyOpenAI)
        # assistant_id, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(app1=app, 

        print("2")
        PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/Agents/{category_target}'))
        file_path = os.path.join(PATH_caminho, f"{NameAgent_AgentCreate}.py")


        try:
            AgentKeysGithub = f"github_username, github_token = GithubKeys{self.AgentKeysGithubName[0]}.{self.AgentKeysGithubName[0]}_github_keys()"
        except Exception as err2:
            AgentKeysGithub = f"github_username, github_token = None, None"

    


        if self.StorageAgentOutput_AgentCreate:
            config_output = f""" 
        date = datetime.now().strftime('%Y-%m-%d')
        output_path_jsonl = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/Destilation/{NameAgent_AgentCreate}/Jsonl/DestilationAgent{{date}}.jsonl'))
        output_path_json = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/Destilation/{NameAgent_AgentCreate}/Json/DestilationAgent{{date}}.json'))
        os.makedirs(output_path_json, exist_ok=True)
        os.makedirs(output_path_jsonl, exist_ok=True)
            """

            codeStorageAgentOutput = """
        datasetjson = {
            "input": mensage_final.strip(),
            "output": response.strip()
        }
        datasetjsonl = {
            "messages": [
                {"role": "system", "content": f"{instructionsassistant}"},
                {"role": "user", "content": f"{mensage_final.strip()}"},
                {"role": "assistant", "content": f"{response.strip()}"}
            ]
        }
                    



        finaloutputjson = os.path.join(output_path_json, f"DestilationDateTime_{date.replace('-', '_').replace(':', '_')}.json")
        with open(finaloutputjson, 'a', encoding='utf-8') as json_file:
            json.dump(datasetjson, json_file, indent=4, ensure_ascii=False)
        
        finaloutputjsonl = os.path.join(output_path_jsonl, f"DestilationDateTime_{date.replace('-', '_').replace(':', '_')}.jsonl")
        with open(finaloutputjsonl, 'a', encoding='utf-8') as json_file:
            json_file.write(json.dumps(datasetjsonl, ensure_ascii=False) + "\\n")
        

        print(f"Dataset salvo")


            """

            codeStorageAgentOutputFinal = config_output + codeStorageAgentOutput
        
        else:
            codeStorageAgentOutputFinal = ""

        if self.ArgsCreatetextedit == None:
            argsclass = ""
            nome_da_class = f"class {NameAgent_AgentCreate}:\n    def __init__(self):\n    pass"
            nome_da_funcao = f"    def {NameAgent_AgentCreate}_{KeyInFirebase_AgentCreate}(self, mensagem):"
        else:
            argslistclass =  self.ArgsCreatetextedit.split(", ")
            processandoargsclass = []
            for arg in argslistclass:
                processandoargsclass.append(f"        self.{arg} = {arg}") 

            argsclass = "\n".join(processandoargsclass)
            nome_da_class = f"class {NameAgent_AgentCreate}:\n    def __init__(self, {self.ArgsCreatetextedit}):"
            nome_da_funcao = f"    def {NameAgent_AgentCreate}_{KeyInFirebase_AgentCreate}(self, mensagemUserorAgent):"


        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(F'''
#################The agent was created with SoftwareAI#################


# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#################
# IMPORT SoftwareAI All Paths 
from softwareai.CoreApp._init_paths_ import *
#################
# IMPORT SoftwareAI Instructions
from softwareai.CoreApp.SoftwareAI.Instructions._init_Instructions_ import *
#################
# IMPORT SoftwareAI Tools
from softwareai.CoreApp.SoftwareAI.Tools._init_tools_ import *
#################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *
######################################################################


{nome_da_class}
{argsclass}
{nome_da_funcao}
        key = "{KeyInFirebase_AgentCreate}"
        nameassistant = "{NameAgent_AgentCreate}"
        model_select = "{ModelSelect_AgentCreate}"
        UseVectorstoreToGenerateFiles = {UseVectorstoreToGenerateFiles}
        Upload_1_file_in_thread = {Upload1fileinThread_AgentCreate}
        Upload_1_file_in_message = {Upload1fileinmessage_AgentCreate}
        Upload_1_image_for_vision_in_thread = {Upload1imageforvisioninThread_AgentCreate}
        vectorstore_in_assistant = {Vectorstoreinassistant_AgentCreate}
        vectorstore_in_Thread = {VectorstoreinThread_AgentCreate}
        Upload_list_for_code_interpreter_in_thread = {Uploadlistfileforcodeinterpreterinthread_AgentCreate}
        {AgentKeysGithub}
        key_openai = OpenAIKeys{self.AgentKeysOpenAIName[0]}.keys()
        name_app = "{self.name_app}"
        app{self.name_app} = FirebaseKeysinit._init_app_(name_app)
        client = OpenAIKeysinit._init_client_(key_openai)

        
        {vectorstorecode}
        
        exemplo = f""" 
        {PromptExample_AgentCreate}
        """
        
        regras = f""" 
        {PromptRules_AgentCreate}
        
        """
        mensage_final = mensagem + exemplo + regras
        
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                        mensagem=mensage_final,
                                                                        agent_id={NameAgent_AgentCreate},
                                                                        key=key,
                                                                        app1=app{self.name_app},
                                                                        client=client, 
                                                                        tools=tools_{NameAgent_AgentCreate}, 
                                                                        model_select=model_select,
                                                                        aditional_instructions=adxitional_instructions_{NameAgent_AgentCreate}
                                                                    )

                                            
                                                                        
                                
        {codeStorageAgentOutputFinal}

        return response
            ''')
            file.close()

        self.ModalInfo.emit("Agent Created !!, Configuring launchers")

        time.sleep(1.5)

        self.ModalInfo.emit("Launcher Tools Configured !!")

        self.insert_init_tools_()

        time.sleep(1.5)

        self.insert_init_functions_()

        self.ModalInfo.emit("Launcher Functions Configured !!")

        time.sleep(1.5)

        self.insert_init_submit_outputs_()

        self.ModalInfo.emit("Launcher Functions Outputs Configured !!")

        time.sleep(1.5)

        self.insert_init_Instructions_()

        self.ModalInfo.emit("Launcher Instructions Configured !!")

        time.sleep(1.5)

        self.insert_import_init_agents_()

        self.ModalInfo.emit("Agente inicializer Configured !!")

        time.sleep(1.5)

        self.ModalSucess.emit("The agent was created with SoftwareAI !!")


        # ref1 = db.reference(f'ai_org_assistant_id', app=appx)
        # controle_das_funcao2 = f"User_{KeyInFirebase_AgentCreate}"
        # controle_das_funcao_info_2 = {
        #     "assistant_id": f'{assistant_id}',
        #     "instructionsassistant": f'{instructionsassistant}',
        #     "nameassistant": f'{nameassistant}',
        #     "model_select": f'{model_select}',
        #     "tools": [{"type": "file_search"}],
        #     "key": f'{KeyInFirebase_AgentCreate}',
        # }
        # ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)


        self.finishedqthread.emit()




    def insert_init_tools_(self):
        with open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/SoftwareAI/Tools')), f"_init_tools_.py"), 'r+', encoding='utf-8') as file:
            content = file.read()
            if f"{self.AgentCategory_AgentCreate}.{self.NameAgent_AgentCreate}_tools" not in content:
                
                file.write(F'''
from softwareai.CoreApp.SoftwareAI.Tools.{self.AgentCategory_AgentCreate}.{self.NameAgent_AgentCreate}_tools import *
                ''')
                file.close()

    def insert_init_functions_(self):
        with open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/SoftwareAI/Functions')), f"_init_functions_.py"), 'r+', encoding='utf-8') as file:
            content = file.read()
            if f"{self.namefunction_agentcreate}_function" not in content:

                file.write(F'''
from softwareai.CoreApp.SoftwareAI.Functions.{self.namefunction_agentcreate}_function import *
                ''')
                file.close()

    def insert_init_submit_outputs_(self):

        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../CoreApp/SoftwareAI/Functions_Submit_Outputs'))
        init_file_path = os.path.join(base_path, '_init_submit_outputs_.py')
        new_function_name = f"submit_output_{self.namefunction_agentcreate}"
        with open(init_file_path, 'r+', encoding='utf-8') as file:
            content = file.read()
            if new_function_name not in content:
                updated_content = content.replace(
                    "functions_to_call = [",
                    f"functions_to_call = [\n        {new_function_name},"
                )
                file.seek(0)
                file.write(updated_content)
                file.truncate()
            else:
                print("Função já está na lista.")
        with open(init_file_path, 'r+', encoding='utf-8') as file:
            content = file.read()
            new_import = f"from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.{self.namefunction_agentcreate}_submit_outputs import submit_output_{self.namefunction_agentcreate}\n"
            if new_import not in content:
                file.seek(0)
                file.write(new_import + content)
                file.truncate()

    def insert_init_Instructions_(self):
        with open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/SoftwareAI/Instructions')), f"_init_Instructions_.py"), 'r+', encoding='utf-8') as file:
            content = file.read()
            if f"{self.AgentCategory_AgentCreate}.{self.NameAgent_AgentCreate}" not in content:

                file.write(F'''
from softwareai.CoreApp.SoftwareAI.Instructions.{self.AgentCategory_AgentCreate}.{self.NameAgent_AgentCreate} import *
                ''')
                file.close()
        
    def insert_import_init_agents_(self):

        
        new_import = f"from softwareai.CoreApp.Agents.{self.AgentCategory_AgentCreate}.{self.NameAgent_AgentCreate} import {self.NameAgent_AgentCreate}_{self.KeyInFirebase_AgentCreate}\n"
        file_path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp')), f"_init_agents_.py")
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        content = content.replace(f"\nfrom softwareai.CoreApp.Agents.{self.AgentCategory_AgentCreate}.{self.NameAgent_AgentCreate} import {self.NameAgent_AgentCreate}_{self.KeyInFirebase_AgentCreate}", "")
        first_import_end = content.find('\n', content.find('from ')) + 1
        updated_content = content[:first_import_end] + new_import + content[first_import_end:]
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(updated_content)


        if self.CurrentArgs_AgentCreate == "agent":
            argslistcls =  self.ArgsCreatetextedit.split(", ")
            argscls = []
            for arg in argslistcls:
                argscls.append(f"            cls._agents['{arg}'],") 
            argscls = "\n".join(argscls)
            agent_initializer_entry = (
                f"        cls._agents['{self.NameAgent_AgentCreate}'] = {self.NameAgent_AgentCreate}_{self.KeyInFirebase_AgentCreate}(\n{argscls}\n)\n"
            )
        else:

            agent_initializer_entry = (
                f"        cls._agents['{self.NameAgent_AgentCreate}'] = {self.NameAgent_AgentCreate}_{self.KeyInFirebase_AgentCreate}()\n"
            )
        with open(os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp')), f"_init_agents_.py"), 'r+', encoding='utf-8') as file:
            content = file.read()

            # Adicionar a importação se não existir
            if new_import not in content:
                file.seek(0)
                file.write(new_import + content)
                file.truncate()
            else:
                print(f"Importação para já está presente.")

            # Adicionar a inicialização dentro do método `initialize_agents`
            if agent_initializer_entry not in content:
                # Localizar o início do método `initialize_agents`
                initialize_start = content.find("def initialize_agents(cls):")
                if initialize_start != -1:
                    # Localizar onde termina as inicializações existentes
                    insert_pos = content.find("cls._agents", initialize_start)
                    end_of_initializations = content.find("\n", insert_pos) + 1

                    # Inserir a inicialização no local correto
                    updated_content = (
                        content[:end_of_initializations]
                        + agent_initializer_entry
                        + content[end_of_initializations:]
                    )
                    file.seek(0)
                    file.write(updated_content)
                    file.truncate()



    def FunctionPythonOutputAgentCreate_(self):
        if self.FunctionPythonOutputAgentCreate.strip():

            PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/SoftwareAI/Functions_Submit_Outputs'))
            file_path = os.path.join(PATH_caminho, f"{self.namefunction_agentcreate}_submit_outputs.py")
            with open(file_path, 'w', encoding='utf-8') as file:
               
                file.write(f'''

#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Functions
from softwareai.CoreApp.SoftwareAI.Functions._init_functions_ import *
#########################################
tool_outputs = []
{self.FunctionPythonOutputAgentCreate}

                ''')
                file.close()

                self.ModalInfo.emit("Function Python Output Agent Created !!")

    def AgentToolsAgentCreate_(self):
        if self.AgentToolsAgentCreate.strip():

            PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/SoftwareAI/Tools/{self.AgentCategory_AgentCreate}'))
            file_path = os.path.join(PATH_caminho, f"{self.NameAgent_AgentCreate}_tools.py")
            with open(file_path, 'w', encoding='utf-8') as file:
                
                file.write(f'''

tools_{self.NameAgent_AgentCreate} = [
{self.AgentToolsAgentCreate}
]

                ''')
                file.close()
                self.ModalInfo.emit("Agent Tools Created !!")

    def InstructionAgentCreate_(self):

        if self.InstructionAgentCreate.strip():
            if self.AditionalInstructionsAgentCreate.strip():
                AditionalInstructionsAgentCreate = f"""\"\"\" {self.AditionalInstructionsAgentCreate}\"\"\""""
            else:
                AditionalInstructionsAgentCreate = "None"

            PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/SoftwareAI/Instructions/{self.AgentCategory_AgentCreate}'))
            file_path = os.path.join(PATH_caminho, f"{self.NameAgent_AgentCreate}.py")
            with open(file_path, 'w', encoding='utf-8') as file:
                content = self.InstructionAgentCreate
                file.write(F'''
instruction{self.NameAgent_AgentCreate} = \"\"\" 
{content}
\"\"\"
adxitional_instructions_{self.NameAgent_AgentCreate} = {AditionalInstructionsAgentCreate}

                ''')
                file.close()
                self.ModalInfo.emit("Instruction Agent Created !!")

    def FunctionPythonAgentCreate_(self):
                
        if self.FunctionPythonAgentCreate.strip():

            PATH_caminho = os.path.abspath(os.path.join(os.path.dirname(__file__), f'../../../CoreApp/SoftwareAI/Functions'))
            file_path = os.path.join(PATH_caminho, f"{self.namefunction_agentcreate}_function.py")
            with open(file_path, 'w', encoding='utf-8') as file:
                content = self.FunctionPythonAgentCreate
                file.write(f'''

{content}

                ''')
                file.close()
                self.ModalInfo.emit("Function Python Agent Created !!")



    def cancel(self):
        self.finishedqthread.emit()
