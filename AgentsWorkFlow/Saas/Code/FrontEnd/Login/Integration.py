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
    print(f"CodeLoginFrontEnd: {input_data.FrontEndContent}")
    # response = requests.post("http://localhost:5000/agent/refund", json={"input": input_data.reason})
    # reply = response.json().get("reply")
              
def CodeLoginFrontEnd(                                
                                session_id, 
                                appcompany,
                                path_ProjectWeb,
                                path_html,
                                path_js,
                                path_css,
                                doc_md,
                                Keys_path,
                                script_base_login_js,

                      ):

    os.chdir(path_ProjectWeb)
    path_Keys = Keys_path

    agent_ids = ['Login']
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
        {instruction_formatado}        
        """,
        model=str(model),
        tools=Tools_Name_dict,
        # handoffs=[handoff_obj_CodeCheckoutFrontEnd],
    )

    
    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
        tool_name_override="code_login_front_end_agent"
    )
    return agent, handoff_obj