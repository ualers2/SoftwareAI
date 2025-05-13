from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel

from modules.modules import *

STRIPE_WEBHOOK_EVENTS = None
STRIPE_SECRET_KEY = None
API_BASE_URL = None

class Data(BaseModel):
    Content: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: Data):

    print(f"CreateWebhook: {input_data.Content}")


              
def CreateWebhook(session_id, appcompany,
                        path_ProjectWeb,
                        path_html,
                        path_js,
                        path_css,
                        doc_md,
                        Keys_path,
                    ):

    os.chdir(path_ProjectWeb)

    path_Keys = Keys_path

    agent_ids = ['CreateWebhook']
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
        instructions=f"""
{RECOMMENDED_PROMPT_PREFIX}\n
{instruction_formatado}        
        """,
        model=str(model),
        tools=Tools_Name_dict,
    )




    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=Data,
    )
    return agent, handoff_obj