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
    print(f"CodeFlaskBackEnd_basic_endpointsAgent: {input_data.FrontEndContent}")

def CodeFlaskBackEnd_basic_endpointsAgent(
    session_id, 
    appcompany,
    path_ProjectWeb,
    path_html,
    path_js,
    path_css,
    doc_md,
    Keys_path,
    basic_endpoints
  ):
    # Trocar para o diretório do projeto
    os.chdir(path_ProjectWeb)


    # Carrega metadados do agente básico
    agent_ids = ['basic_endpoints']
    agents_metadata = EgetMetadataAgent(agent_ids)

    name = agents_metadata['basic_endpoints']["name"]
    model = agents_metadata['basic_endpoints']["model"]
    instruction = agents_metadata['basic_endpoints']["instruction"]
    try:
        tools = agents_metadata['basic_endpoints']["tools"]
        Tools_Name_dict = Egetoolsv2(list(tools))
    except KeyError:
        Tools_Name_dict = {}

    # Garante que 'prefix' esteja disponível para formatação
    prefix = RECOMMENDED_PROMPT_PREFIX

    # Formata a instrução substituindo placeholders pelas variáveis do contexto
    instruction_formatado = format_instruction(instruction, locals())

    # Cria o agente com instruções formatadas
    agent = Agent(
        name=str(name),
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}\n{instruction_formatado}""",
        model=str(model),
        tools=Tools_Name_dict,
        # handoffs=[handoff_obj_CodeFlaskBackEndSprint7Agent],
    )

    # Define o handoff para front-end
    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
    )
    return agent, handoff_obj
