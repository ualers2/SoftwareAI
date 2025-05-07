from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from modules.modules import *


class inputdata(BaseModel):
  input_data_Content: str

async def on_handoff(ctx: RunContextWrapper[dict], input_data: inputdata):
    print(f"CodeUploadGit: {input_data.input_data_Content}")
    # response = requests.post("http://localhost:5000/agent/refund", json={"input": input_data.reason})
    # reply = response.json().get("reply")
              
def CodeUploadGit(session_id, appcompany):
   
    path_ProjectWeb = "/app/LocalProject"
    os.chdir(path_ProjectWeb)
    path_html = f"{path_ProjectWeb}/templates"
    path_js = f"{path_ProjectWeb}/static/js"
    path_css = f"{path_ProjectWeb}/static/css"
    doc_md = f"{path_ProjectWeb}/doc_md"

    githubtoken = os.getenv("github_username_Ualers")
    repo_owner = os.getenv("companyname")

# ### 📥 `autoupload`  
#   - repo_name: nome do projeto armazenado no historico de conversas
#   - repo_owner: {repo_owner}  
#   - softwarepypath: {path_html}/checkout.html e {path_js}/checkout-payment-button.js (no caso de 2 arquivos utilize a ferramenta 1 vez para cada arquivo)
#   - token: {githubtoken}

# ###📦 autogetlocalfilecontent  
# Para obter o conteúdo **completo** do arquivo index para que seja possivel o desenvolvimento das modificacoes
# autogetlocalfilecontent:
# - preferred_name: "index.html"
# - fallback_names: ["index.html"]
# - search_dir: {path_html}

# ### 📦 autocreaterepo
# Para Criar o Repositorio do projeto no git
# autocreaterepo:
# - **description:** Máximo 250 caracteres (resumo do projeto)
# - **githubtoken:** {githubtoken}
# - **private:** false
# - **repo_name:** nome do projeto slugificado
# - **repo_owner:** {repo_owner}

# ###📦 autolistlocalproject  
# Para obter os caminhos dos arquivos e seus conteudos do projeto local (no nosso caso precisamos apenas dos caminhos para usar em autoupload)
# autolistlocalproject:
# - path_project: {path_ProjectWeb}

# ### 📦 autoupload
# - **repo_name:** nome do projeto 
# - **repo_owner:** {repo_owner}
# - **softwarepypath:** a lista de caminhos dos arquivos a ser enviado
# - **token:** {githubtoken}



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
        # handoffs=[handoff_obj_CodeUploadGit],

    )


    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=inputdata,
    )
    return agent, handoff_obj