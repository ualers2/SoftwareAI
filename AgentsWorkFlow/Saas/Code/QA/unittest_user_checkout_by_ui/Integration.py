from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################

from modules.modules import *

class Data(BaseModel):
    content: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: Data):
    print(f"unittest_user_checkout_by_ui: {input_data.content}")


def unittest_user_checkout_by_ui(session_id, appcompany,
                        path_ProjectWeb,
                        path_html,
                        path_js,
                        path_css,
                        doc_md,
                        Keys_path,
                        STRIPE_WEBHOOK_EVENTS,
                        STRIPE_SECRET_KEY,
                        API_BASE_URL,
                        firebase_json_path,
                        firebase_db_url,

                    ):

    agent_ids = ['unittest_user_checkout_by_ui']
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