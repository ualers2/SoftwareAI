from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from modules.modules import *

from AgentsWorkFlow.Saas.Code.FrontEnd.Dashboard.CRM.Integration import DashboardCRM
from AgentsWorkFlow.Saas.Code.FrontEnd.Dashboard.Scheduling.Integration import DashboardScheduling
from AgentsWorkFlow.Saas.Code.FrontEnd.Dashboard.IA.Integration import DashboardAIAgent
from AgentsWorkFlow.Saas.Code.FrontEnd.Dashboard.ReservationPlatform.Integration import DashboardReservationPlatformAgent
from AgentsWorkFlow.Saas.Code.FrontEnd.Dashboard.Dashboard_Product_Performance_Agent.Integration import Dashboard_Product_Performance_Agent
from AgentsWorkFlow.Saas.Code.FrontEnd.Dashboard.Dashboard_Learning_Management_Agent.Integration import Dashboard_Learning_Management_Agent
from AgentsWorkFlow.Saas.Code.FrontEnd.Dashboard.Dashboard_Supply_Chain_Agent.Integration import Dashboard_Supply_Chain_Agent



class Data(BaseModel):
    Content: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: Data):
    print(f"CodeFrontEndDecisionDashboard: {input_data.Content}")


              
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


    agent_, handoff_obj_dashboard_reservation_platform_agent = DashboardReservationPlatformAgent(
                                "", 
                                "",
                                path_ProjectWeb,
                                path_html,
                                path_js,
                                path_css,
                                doc_md,
                                Keys_path,


                            )
    agent_, handoff_obj_CodeFrontEndDashboardAISprint14Agent = DashboardAIAgent(
                                "", 
                                "",
                                path_ProjectWeb,
                                path_html,
                                path_js,
                                path_css,
                                doc_md,
                                Keys_path,


                            )
    agent_, handoff_obj_CodeFrontEndDashboardSchedulingSprint14 = DashboardScheduling(
                                "", 
                                "",
                                path_ProjectWeb,
                                path_html,
                                path_js,
                                path_css,
                                doc_md,
                                Keys_path,


                            )
    agent_, handoff_obj_CodeFrontEndDashboardCRMSprint14 = DashboardCRM(
                                "", 
                                "",
                                path_ProjectWeb,
                                path_html,
                                path_js,
                                path_css,
                                doc_md,
                                Keys_path,

                            )
    agent_, handoff_obj_Dashboard_Product_Performance_Agent = Dashboard_Product_Performance_Agent(
                                "", 
                                "",
                                path_ProjectWeb,
                                path_html,
                                path_js,
                                path_css,
                                doc_md,
                                Keys_path,


                            )
    agent_, handoff_obj_Dashboard_Learning_Management_Agent = Dashboard_Learning_Management_Agent(
                                "", 
                                "",
                                path_ProjectWeb,
                                path_html,
                                path_js,
                                path_css,
                                doc_md,
                                Keys_path,


                            )
    agent_, handoff_obj_Dashboard_Supply_Chain_Agent = Dashboard_Supply_Chain_Agent(
                                "", 
                                "",
                                path_ProjectWeb,
                                path_html,
                                path_js,
                                path_css,
                                doc_md,
                                Keys_path,


                            )
        
    agent_ids = ['Dashboard_Decision']
    agents_metadata = EgetMetadataAgent(agent_ids)

    name = agents_metadata['Dashboard_Decision']["name"]
    model = agents_metadata['Dashboard_Decision']["model"]
    instruction = agents_metadata['Dashboard_Decision']["instruction"]

    instruction_formatado = format_instruction(instruction, locals())
    try:
        tools_TypeProject = agents_metadata['Dashboard_Decision']["tools"]
        Tools_Name_dict = Egetoolsv2(list(tools_TypeProject))
        agent = Agent(
            name=str(name),
            instructions=f"""
{RECOMMENDED_PROMPT_PREFIX}\n
{instruction_formatado}        
            """,
            model=str(model),
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
    except:
                
        agent = Agent(
            name=str(name),
            instructions=f"""
{RECOMMENDED_PROMPT_PREFIX}\n
{instruction_formatado}        
            """,
            model=str(model),
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
        input_type=Data,
    )
    return agent, handoff_obj