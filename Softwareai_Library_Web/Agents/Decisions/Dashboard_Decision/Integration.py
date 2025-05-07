from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from modules.modules import *


from Agents.Code.FrontEnd.Dashboard.CRM.Integration import DashboardCRM
from Agents.Code.FrontEnd.Dashboard.Scheduling.Integration import DashboardScheduling
from Agents.Code.FrontEnd.Dashboard.IA.Integration import DashboardAIAgent
from Agents.Code.FrontEnd.Dashboard.ReservationPlatform.Integration import DashboardReservationPlatformAgent
from Agents.Code.FrontEnd.Dashboard.Dashboard_Product_Performance_Agent.Integration import Dashboard_Product_Performance_Agent
from Agents.Code.FrontEnd.Dashboard.Dashboard_Learning_Management_Agent.Integration import Dashboard_Learning_Management_Agent
from Agents.Code.FrontEnd.Dashboard.Dashboard_Supply_Chain_Agent.Integration import Dashboard_Supply_Chain_Agent





class FrontEndData(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: FrontEndData):
    print(f"CodeFrontEndDecisionDashboard: {input_data.FrontEndContent}")

              
def CodeFrontEndDecisionDashboard(
                        session_id, 
                        appcompany,
                        path_ProjectWeb,
                        path_html,
                        path_js,
                        path_css,
                        doc_md,
                        Keys_path,
                    ):

    os.chdir(path_ProjectWeb)

    agent_, handoff_obj_dashboard_reservation_platform_agent = DashboardReservationPlatformAgent("", appcompany)
    agent_, handoff_obj_CodeFrontEndDashboardAISprint14Agent = DashboardAIAgent("", appcompany)
    agent_, handoff_obj_CodeFrontEndDashboardSchedulingSprint14 = DashboardScheduling("", appcompany)
    agent_, handoff_obj_CodeFrontEndDashboardCRMSprint14 = DashboardCRM("", appcompany)
    agent_, handoff_obj_Dashboard_Product_Performance_Agent = Dashboard_Product_Performance_Agent("", appcompany)
    agent_, handoff_obj_Dashboard_Learning_Management_Agent = Dashboard_Learning_Management_Agent("", appcompany)
    agent_, handoff_obj_Dashboard_Supply_Chain_Agent = Dashboard_Supply_Chain_Agent("", appcompany)
        

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
        handoffs=[
                handoff_obj_CodeFrontEndDashboardCRMSprint14,
                handoff_obj_CodeFrontEndDashboardAISprint14Agent,
                handoff_obj_CodeFrontEndDashboardSchedulingSprint14,
                handoff_obj_dashboard_reservation_platform_agent,
                handoff_obj_Dashboard_Product_Performance_Agent,
                handoff_obj_Dashboard_Learning_Management_Agent,
                handoff_obj_Dashboard_Supply_Chain_Agent

            ],

    )

    



    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
    )
    return agent, handoff_obj