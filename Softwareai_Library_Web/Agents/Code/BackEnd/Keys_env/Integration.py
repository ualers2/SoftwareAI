from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from modules.modules import *


# from Decisions.Dashboard.Integration import CodeFrontEndDecisionDashboard

class FrontEndData(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[dict], input_data: FrontEndData):
    print(f"CodeFlaskBackEndSprint13Agent: {input_data.FrontEndContent}")
    # response = requests.post("http://localhost:5000/agent/refund", json={"input": input_data.reason})
    # reply = response.json().get("reply")
              
def CodeFlaskBackEndSprint13Agent(session_id, appcompany,
                                
                                ):
   
    path_ProjectWeb = "/app/LocalProject"
    os.chdir(path_ProjectWeb)
    path_html = f"templates"
    path_js = f"static/js"
    path_css = f"static/css"
    doc_md = f"doc_md"
    githubtoken = os.getenv("github_username_Ualers")
    repo_owner = os.getenv("companyname")
    STRIPE_SECRET_KEY=os.getenv("STRIPE_SECRET_KEY")
    NEXT_PUBLIC_STRIPE_PUB_KEY=os.getenv("NEXT_PUBLIC_STRIPE_PUB_KEY")
    # session_id_CodeFrontEndDecisionDashboard = "teste_handoff_CodeFrontEndDecisionDashboard"
    # agent_, handoff_obj_CodeFrontEndDecisionDashboard = CodeFrontEndDecisionDashboard(session_id_CodeFrontEndDecisionDashboard, appcompany)


    user_code_init_env = f'''
STRIPE_WEBHOOK_SECRET=
STRIPE_SECRET_KEY={STRIPE_SECRET_KEY}
STRIPE_PRODUCT_ID_Premium=
STRIPE_SUBSCRIPTION_PRICE_ID_Premium=
NEXT_PUBLIC_STRIPE_PUB_KEY={NEXT_PUBLIC_STRIPE_PUB_KEY}
gmail_usuario=
gmail_senha=
API_BASE_URL="http://127.0.0.1:5000"


    '''


# {RECOMMENDED_PROMPT_PREFIX}\n
# ---

# Ao final de sua execução, utilize o Handoffs transfer_to_code_front_end_dashboard_sprint_14_agent
# Ao final de sua execução, Encaminhe o usuário para o agente de Code Front End Dashboard Sprint 14 Agent
# prossiga com a criacao do dashboard da aplicacao 
# Encaminhe ao agente Code Front End Dashboard Sprint 14 Agent 
# ---

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
        # handoffs=[handoff_obj_CodeFrontEndDecisionDashboard],



    )



    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
    )
    return agent, handoff_obj