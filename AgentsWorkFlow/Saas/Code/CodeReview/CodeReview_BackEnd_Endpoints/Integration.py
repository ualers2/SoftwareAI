from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel

from modules.modules import *




class Data(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: Data):
    print(f"CodeBackendEndpointscodereviewAgent: {input_data.FrontEndContent}")

def CodeBackendEndpointscodereviewAgent(session_id, appcompany,
                        path_ProjectWeb,
                        path_html,
                        path_js,
                        path_css,
                        doc_md,
                        Keys_path,
                        index_,
                        login,
                        dashboard,
                        checkout,
                        checkout_sucess,
                        api_create_checkout,
                        api_register,
                        api_login,
                        webhook,



                    ):

    os.chdir(path_ProjectWeb)

    agent_ids = ['CodeReview_BackEnd_Endpoints']
    agents_metadata = EgetMetadataAgent(agent_ids)

    name = agents_metadata[f'{agent_ids[0]}']["name"]
    model = agents_metadata[f'{agent_ids[0]}']["model"]
    instruction = agents_metadata[f'{agent_ids[0]}']["instruction"]
    try:
      tools = agents_metadata[f'{agent_ids[0]}']["tools"]
      Tools_Name_dict = Egetoolsv2(list(tools))
    except:
      pass

    instruction_formatado = format_instruction(instruction, locals())

    agent = Agent(
        name=str(name),
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}\n
        {instruction_formatado}        
        """,
        model=str(model),
        tools=Tools_Name_dict,
        # handoffs=[handoff_obj_CodeDocumentationModulesAgent],
    )



    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=Data,
    )
    return agent, handoff_obj