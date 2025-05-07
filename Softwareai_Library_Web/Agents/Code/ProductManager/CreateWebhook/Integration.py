from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from modules.modules import *


# from Agents.Code.BackEnd.Sprint6.Integration import CodeFlaskBackEndSprint6Agent

class Data(BaseModel):
    Content: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: Data):
    print(f"CreateWebhook: {input_data.Content}")

              
def CreateWebhook(
                session_id, 
                appcompany,

            ):
   
    path_ProjectWeb = "/app/LocalProject"
    os.chdir(path_ProjectWeb)
    path_html = f"templates"
    path_js = f"static/js"
    path_css = f"static/css"
    doc_md = f"doc_md"
    path_Keys = f"Keys"

    dotenv_path= os.path.join("Keys", "keys.env")
    load_dotenv(dotenv_path=dotenv_path)

    STRIPE_WEBHOOK_EVENTS = os.getenv("STRIPE_WEBHOOK_EVENTS")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

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


    )

    
    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=Data,
    )
    return agent, handoff_obj