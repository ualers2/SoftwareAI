from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel

from modules.modules import *

from Agents.Code.ProjectManager.Timeline.Integration import CodeRequirementsAndTimeline

class doc_pre_project_Data(BaseModel):
    doc_pre_project: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: doc_pre_project_Data):
    print(f"doc_pre_project: {input_data.doc_pre_project}")


def CodePreProject(
        WEBHOOK_URL,
        session_id,
        user_email,

    ):

    agent_, handoff_obj_CodeRequirementsAndTimeline = CodeRequirementsAndTimeline(
        WEBHOOK_URL,
        session_id,
        user_email,

        )
   
    path_ProjectWeb = "/app/LocalProject"
    os.makedirs(path_ProjectWeb, exist_ok=True)
    os.chdir(path_ProjectWeb)
    path_html = f"{path_ProjectWeb}/templates"
    path_js = f"{path_ProjectWeb}/static/js"
    path_css = f"{path_ProjectWeb}/static/css"
    doc_md = f"{path_ProjectWeb}/doc_md"
    Keys_path = f"{path_ProjectWeb}/Keys"

    os.makedirs(Keys_path, exist_ok=True)
    os.makedirs(path_html, exist_ok=True)
    os.makedirs(path_js, exist_ok=True)
    os.makedirs(path_css, exist_ok=True)
    os.makedirs(doc_md, exist_ok=True)
    
    githubtoken = os.getenv("github_username_Ualers")
    repo_owner = os.getenv("companyname")

# ### 📦 autocreaterepo
# - **description:** Máximo 250 caracteres (resumo do projeto)
# - **githubtoken:** {githubtoken}
# - **private:** false
# - **repo_name:** nome do projeto slugificado
# - **repo_owner:** {repo_owner}

# ### 📦 autoupload
# - **repo_name:** nome do projeto 
# - **repo_owner:** {repo_owner}
# - **softwarepypath:** {doc_md}/nome-do-documento.md
# - **token:** {githubtoken}

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
        handoffs=[handoff_obj_CodeRequirementsAndTimeline],


    )

    

   
    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=doc_pre_project_Data,
    )
    return agent, handoff_obj