from agents import Agent, handoff, RunContextWrapper
import json
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from AgentsWorkFlow.Saas.Code.ProjectManager.PreProject.Integration import CodePreProject

# path_APPCOMPANY = "/app/Keys/appcompany.json"
# with open(path_APPCOMPANY) as f:
#     firebase_credentials_APPCOMPANY = json.load(f)

# credt1 = credentials.Certificate(firebase_credentials_APPCOMPANY)
# appcompany = initialize_app(credt1, {
#    'storageBucket': 'aicompanydata1.appspot.com',
#    'databaseURL': 'https://aicompanydata1-default-rtdb.europe-west1.firebasedatabase.app'
# }, name='appcompany')
 
from modules.modules import *



def TriageAgent(
    session_id,
    user_email,
    path_ProjectWeb,
    path_html,
    path_js,
    path_css,
    doc_md,
    path_Keys,

    ):
    agent_codepreproject, handoff_obj_codepreproject = CodePreProject(
        session_id,
        user_email,
        path_ProjectWeb,
        path_html,
        path_js,
        path_css,
        doc_md,
        path_Keys,
        )

    agent_ids = ['TypeProject']
    agents_metadata = EgetMetadataAgent(agent_ids)

    name_TypeProject = agents_metadata['TypeProject']["name"]
    model_TypeProject = agents_metadata['TypeProject']["model"]
    instruction_TypeProject = agents_metadata['TypeProject']["instruction"]
    try:
        tools_TypeProject = agents_metadata['TypeProject']["tools"]
        Tools_Name_dict = Egetoolsv2(list(tools_TypeProject))
            
        TypeProject_agent = Agent(
            name=str(name_TypeProject),
            instructions=f"""
{RECOMMENDED_PROMPT_PREFIX}\n
{instruction_TypeProject}        
            """,
            model=str(model_TypeProject),
            tools=Tools_Name_dict,
            handoffs=[handoff_obj_codepreproject],

        )
    except:
        TypeProject_agent = Agent(
            name=str(name_TypeProject),
            instructions=f"""
{RECOMMENDED_PROMPT_PREFIX}\n
{instruction_TypeProject}        
            """,
            model=str(model_TypeProject),
            handoffs=[handoff_obj_codepreproject],

        )

    return TypeProject_agent
