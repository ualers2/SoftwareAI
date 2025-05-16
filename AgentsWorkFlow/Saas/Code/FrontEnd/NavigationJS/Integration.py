from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel

from modules.modules import *


class FrontEndData(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: FrontEndData):
    print(f"Navigation JS FrontEnd: {input_data.FrontEndContent}")
    # response = requests.post("http://localhost:5000/agent/refund", json={"input": input_data.reason})
    # reply = response.json().get("reply")
              
def CodeNavigationJSFrontEnd(
                        session_id, 
                        appcompany,
                        path_ProjectWeb,
                        path_html,
                        path_js,
                        path_css,
                        doc_md,
                        Keys_path,
                        checkout_payment_button,
                        checkout_payment_selected,
                    ):
   

    os.chdir(path_ProjectWeb)
    path_Keys = Keys_path


    agent_ids = ['NavigationJS']
    agents_metadata = EgetMetadataAgent(agent_ids)

    name = agents_metadata['NavigationJS']["name"]
    model = agents_metadata['NavigationJS']["model"]
    instruction = agents_metadata['NavigationJS']["instruction"]
    try:
        tools = agents_metadata['NavigationJS']["tools"]
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
        # handoffs=[handoff_obj_CodeDocumentationStaticjsAgent],
    )

    
    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
    )
    return agent, handoff_obj