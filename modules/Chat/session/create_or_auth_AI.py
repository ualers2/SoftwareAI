# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
def create_or_auth_AI(
    appcompany,
    client,
    key: str, 
    instructionsassistant: Optional[str] = None,
    nameassistant: Optional[str] = None, 
    model_select: Optional[str] = "gpt-4o-mini-2024-07-18", 
    tools: Optional[List] = [{"type": "file_search"},{"type": "code_interpreter"}],


    
    ):
    """ 
    :param key: this is the key that represents the agent in the database
        
    :param instructionsassistant: This argument is the instruction of the agent's behavior The maximum length is 256,000 characters.
    
    :param nameassistant: This argument is the name of the agent The maximum length is 256 characters.
    
    :param model_select: This argument is the AI model that the agent will use
        
    :param tools: This argument is the agent's tools  There can be a maximum of 128 tools per assistant. Tools can be of types code_interpreter, file_search, vectorstore, or function.
        
    :param vectorstore: This argument is the vector storage id desired when creating or authenticating the agent
    response_format: Optional[str] = "json_object",
    response_format: Optional[str] = "json_schema_TitleAndPreface",
    response_format: Optional[str] = "text",
    """

    
    try:
        ref1 = db.reference(f'ai_org_assistant_id/User_{key}', app=appcompany)
        data1 = ref1.get()
        assistant_iddb = data1['assistant_id']
        instructionsassistantdb = data1['instructionsassistant']
        nameassistantdb = data1['nameassistant']
        model_selectdb = data1['model_select']
    
        client.beta.assistants.update(
            assistant_id=str(assistant_iddb),
            instructions=instructionsassistant
        )
        ref1 = db.reference(f'ai_org_assistant_id', app=appcompany)
        controle_das_funcao2 = f"User_{key}"
        controle_das_funcao_info_2 = {
            "assistant_id": f'{assistant_iddb}',
            "instructionsassistant": f'{instructionsassistant}',
            "nameassistant": f'{nameassistantdb}',
            "model_select": f'{model_selectdb}',
            "tools": f'{tools}',
            "key": f'{key}',
        }
        ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)


        return str(assistant_iddb), str(instructionsassistantdb), str(nameassistantdb), str(model_selectdb)
    except Exception as err234:
    
        assistant = client.beta.assistants.create(
            name=nameassistant,
            instructions=instructionsassistant,
            model=model_select,
            tools=tools
        )


        ref1 = db.reference(f'ai_org_assistant_id', app=appcompany)
        controle_das_funcao2 = f"User_{key}"
        controle_das_funcao_info_2 = {
            "assistant_id": f'{assistant.id}',
            "instructionsassistant": f'{instructionsassistant}',
            "nameassistant": f'{nameassistant}',
            "model_select": f'{model_select}',
            "tools": f'{tools}',
            "key": f'{key}',
        }
        ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)
        return str(assistant.id), str(instructionsassistant), str(nameassistant), str(model_select)

