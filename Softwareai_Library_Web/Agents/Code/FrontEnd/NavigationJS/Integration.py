from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from modules.modules import *


# from Agents.Code.BackEnd.Sprint6.Integration import CodeFlaskBackEndSprint6Agent

class FrontEndData(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[dict], input_data: FrontEndData):
    print(f"Navigation JS FrontEnd: {input_data.FrontEndContent}")
    # response = requests.post("http://localhost:5000/agent/refund", json={"input": input_data.reason})
    # reply = response.json().get("reply")
              
def CodeNavigationJSFrontEnd(session_id, appcompany):
   
    path_ProjectWeb = "/app/LocalProject"
    os.chdir(path_ProjectWeb)
    path_html = f"{path_ProjectWeb}/templates"
    path_js = f"{path_ProjectWeb}/static/js"
    path_css = f"{path_ProjectWeb}/static/css"
    doc_md = f"{path_ProjectWeb}/doc_md"

    githubtoken = os.getenv("github_username_Ualers")
    repo_owner = os.getenv("companyname")
    # session_id_CodeFlaskBackEndSprint6Agent = "teste_handoff_CodeFlaskBackEndSprint6Agent"
    # agent_, handoff_obj_CodeFlaskBackEndSprint6Agent = CodeFlaskBackEndSprint6Agent(session_id_CodeFlaskBackEndSprint6Agent, appcompany)


# ### 📥 autoupload  
#   - repo_name: nome do projeto armazenado no historico de conversas
#   - repo_owner: {repo_owner}  
#   - softwarepypath: {path_html}/checkout.html e {path_js}/checkout-payment-button.js (no caso de 2 arquivos utilize a ferramenta 1 vez para cada arquivo)
#   - token: {githubtoken}

# ### 1️⃣ Executar `autogetstructure`  
# Para compreender onde estao os arquivos mencionados com base na **estrutura completa de diretórios e arquivos** do repositório retornados pela ferramenta.
# autogetstructure:
# - branch_name: main
# - repo_name:  nome do projeto armazenado no historico de conversa
# - repo_owner: {repo_owner}
# - github_token: {githubtoken}
# - path: pasta a ser procurada (caso queira obter todas a estrutura de pasta basta deixar assim "")

# ### 2️⃣ Executar `autogetfilecontent`  
# Para obter o conteúdo **completo** do arquivo mencionado (Se mencionado mais de um execute a ferramenta na quantidade dos arquivos mencionados nos Objetivos)
# autogetfilecontent:
# - branch_name: main
# - repo_name:  nome do projeto armazenado no historico de conversa
# - companyname: {repo_owner}
# - file_path: <caminho/relativo/para/arquivo.extencao>
# - github_token: {githubtoken}

# {RECOMMENDED_PROMPT_PREFIX}\n
# ---

# Ao final de sua execução, utilize o Handoffs transfer_to_code_initial_flask_back_end_agent.
# Ao final de sua execução, Encaminhe o usuário para o agente de Code Initial Flask BackEnd Agent
# prossiga com a geração do código BackEnd específico para a aplicacao 
# voce tem autonomia total para trabalhar nao pergunte se precisa de melhorias ou ajustes
# jamais retorne a resposta se autosave estiver disponivel (pois a resposta deve ser o argumento code de autosave possibilitando o salvamento de forma autonoma)

# ---

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
        # handoffs=[handoff_obj_CodeFlaskBackEndSprint6Agent],



    )

    
    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
    )
    return agent, handoff_obj