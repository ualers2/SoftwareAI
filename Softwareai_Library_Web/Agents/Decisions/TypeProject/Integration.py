from agents import Agent, handoff, RunContextWrapper
import json
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from modules.modules import *
from Agents.Code.ProjectManager.PreProject.Integration import CodePreProject

# path_APPCOMPANY = "/app/Keys/appcompany.json"
# with open(path_APPCOMPANY) as f:
#     firebase_credentials_APPCOMPANY = json.load(f)

# credt1 = credentials.Certificate(firebase_credentials_APPCOMPANY)
# appcompany = initialize_app(credt1, {
#    'storageBucket': 'aicompanydata1.appspot.com',
#    'databaseURL': 'https://aicompanydata1-default-rtdb.europe-west1.firebasedatabase.app'
# }, name='appcompany')
 

def TriageAgent(
    WEBHOOK_URL,
    session_id,
    user_email,
    ):
    agent_codepreproject, handoff_obj_codepreproject = CodePreProject(
        WEBHOOK_URL,
        session_id,
        user_email,

        )

    name_agent, model_agent, instruction_original, tools_agent  = get_settings_agents(path_metadata = os.path.join(os.path.dirname(__file__), "metadata.json"))
    instruction_formatado = format_instruction(instruction_original, locals())

    Tools_Name_dict = Egetoolsv2(list(tools_agent))
    agent = Agent(
        name=name_agent,
        instructions = f"""
{RECOMMENDED_PROMPT_PREFIX}
{instruction_formatado}
        """
        ,
        model=str(model_agent),
        tools=Tools_Name_dict,
        handoffs=[handoff_obj_codepreproject],

    )


    return agent
