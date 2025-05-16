from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel

from modules.modules import *

   
class doc_pre_project_Data(BaseModel):
    doc_pre_project: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: doc_pre_project_Data):
    print(f"doc_pre_project: {input_data.doc_pre_project}")


def CodePreProject(
        session_id,
        user_email,
        path_ProjectWeb,
        path_html,
        path_js,
        path_css,
        doc_md,
        Keys_path,
    ):

    os.makedirs(path_ProjectWeb, exist_ok=True)
    os.chdir(path_ProjectWeb)


    os.makedirs(Keys_path, exist_ok=True)
    os.makedirs(path_html, exist_ok=True)
    os.makedirs(path_js, exist_ok=True)
    os.makedirs(path_css, exist_ok=True)
    os.makedirs(doc_md, exist_ok=True)

    agent_ids = ['PreProject']
    agents_metadata = EgetMetadataAgent(agent_ids)

    name = agents_metadata['PreProject']["name"]
    model = agents_metadata['PreProject']["model"]
    instruction = agents_metadata['PreProject']["instruction"]
    tools = agents_metadata['PreProject']["tools"]

    instruction_formatado = format_instruction(instruction, locals())

    Tools_Name_dict = Egetoolsv2(list(tools))
    agent = Agent(
        name=str(name),
        instructions=f"""
        {instruction_formatado}        
        """,
        model=str(model),
        tools=Tools_Name_dict,
        # handoffs=[handoff_obj_CodeRequirementsAndTimeline],
    )

    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=doc_pre_project_Data,
    )
    return agent, handoff_obj