
# Passos para Construir Agent softwareai
- importe as dependencias softwareai
- construia uma classe com o nome do agente, no construtor _init_ voce pode passar outras Classes de agentes que o agente tem acesso
- definir a funcao de personalidade do agente
- 




                                       
# Personalidade 
- Cada agente pode ter mais de 1 Personalidade
- isso significa que podemos ter o mesmo agente com mesmos nomes com variacoes finais de nome: 
- `quantumcore desenvolvimento python`, `quantumcore desenvolvimento backend python com foco em api `
- os 2 agentes tem o mesmo nome sao o mesmo agente ,pertencem a mesma classe, porem com variacoes de "Personalidade" 

Primeiro importamos as dependencias 
```python


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
# IMPORT SoftwareAI _init_environment_
from softwareai.CoreApp._init_environment_ import init_env

```

Definindo A classe Com nome do agente e o construtor init com outros agentes que o agente tem acesso , pode ser nenhum
```python

class GearAssist:
    def __init__(self
                ):
        pass

```

Adicionamos o agente na sua respectiva classe  
```python

    def GearAssist_Technical_Support(self, 
                                        mensagem,
                                        appfb,
                                        vectorstore_in_assistant = None,
                                        vectorstore_in_Thread = None,
                                        Upload_1_file_in_thread = None,
                                        Upload_1_file_in_message = None,
                                        Upload_1_image_for_vision_in_thread = None,
                                        Upload_list_for_code_interpreter_in_thread = None
                                        
                                        ):

        key = "GearAssist_Technical_Support"
        nameassistant = "GearAssist Technical Support"
        model_select = "gpt-4o-mini-2024-07-18"

        key_openai = OpenAIKeysteste.keys()
        client = OpenAIKeysinit._init_client_(key_openai)

        github_username, github_token = GithubKeys.ByteManagerCompanyOwner_github_keys()

        GearAssist_Technical_Support, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appfb, client, key, instructionByteManager, nameassistant, model_select, tools_ByteManager, vectorstore_in_assistant)

        mensaxgem = """
        """  
        mensaxgemfinal = mensaxgem + f"mensagem:\n{mensagem}"
        
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensaxgemfinal,
                                                                agent_id=GearAssist_Technical_Support, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_ByteManager,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_ByteManager
                                                                )
                                                
                
        print(response)
        try:
            teste_dict = json.loads(response)
        except:
            teste_dict = response





```

