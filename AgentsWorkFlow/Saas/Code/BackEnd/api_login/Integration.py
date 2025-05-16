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
    print(f"CodeFlaskBackEndapi_loginAgent: {input_data.FrontEndContent}")

              
def CodeFlaskBackEndapi_loginAgent(                                
                                session_id, 
                                appcompany,
                                path_ProjectWeb,
                                path_html,
                                path_js,
                                path_css,
                                doc_md,
                                Keys_path,
                                api_login

                      ):

    os.chdir(path_ProjectWeb)


    # session_id_CodeFlaskBackEndSprint9Agent = "teste_handoff_CodeFlaskBackEndSprint9Agent"
    # agent_, handoff_obj_CodeFlaskBackEndSprint9Agent = CodeFlaskBackEndSprint9Agent(session_id_CodeFlaskBackEndSprint9Agent, appcompany)

    Tools_Name_dict = Egetoolsv2(["autosave", "autogetlocalfilecontent"])

# {RECOMMENDED_PROMPT_PREFIX}\n
# ---

# Ao final de sua execução, utilize o Handoffs transfer_to_code_upload_git_agent
# Ao final de sua execução, Encaminhe o usuário para o agente de Code Upload Git Agent
# prossiga com a criacao do repositorio e o upload dos arquivos da aplicacao 
# Encaminhe ao agente Code Upload Git Agent para criação do repositório e upload 
# dos arquivos da aplicação.
# ---

# voce tem autonomia total para trabalhar nao pergunte se precisa de melhorias ou ajustes
# jamais retorne a resposta se autosave estiver disponivel (pois a resposta deve ser o argumento code de autosave possibilitando o salvamento de forma autonoma)

# ---


    agent_ids = ['api_login']
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
        # handoffs=[handoff_obj_CodeFlaskBackEndSprint8Agent],
    )




    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
    )
    return agent, handoff_obj