from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel

from modules.modules import *



from AgentsWorkFlow.Saas.Code.FrontEnd.Checkout.Integration import CodeCheckoutFrontEnd
from AgentsWorkFlow.Saas.Code.FrontEnd.Index.Integration import CodeIndexFrontEnd
from AgentsWorkFlow.Saas.Code.FrontEnd.Login.Integration import CodeLoginFrontEnd
from AgentsWorkFlow.Saas.Decisions.Dashboard_Decision.Integration import CodeFrontEndDecisionDashboard

class Data(BaseModel):
    Content: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: Data):
    print(f"Code Review FrontEnd Html Agent: {input_data.Content}")

def CodeReviewFrontEndHtmlAgent(                                
                                session_id, 
                                appcompany,
                                path_ProjectWeb,
                                path_html,
                                path_js,
                                path_css,
                                doc_md,
                                Keys_path,
                                script_base_login_js,
                                checkout_payment_button,
                                checkout_payment_selected,
                      ):

    os.chdir(path_ProjectWeb)


    agent_, handoff_obj_CodeFrontEndDecisionDashboard = CodeFrontEndDecisionDashboard(
                        session_id, 
                        appcompany,
                        path_ProjectWeb,
                        path_html,
                        path_js,
                        path_css,
                        doc_md,
                        Keys_path,
                    )
    agent_, handoff_obj_CodeCheckoutFrontEnd = CodeCheckoutFrontEnd(
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
                    )
    agent_, handoff_obj_CodeLoginFrontEnd = CodeLoginFrontEnd(                                
                                session_id, 
                                appcompany,
                                path_ProjectWeb,
                                path_html,
                                path_js,
                                path_css,
                                doc_md,
                                Keys_path,
                                script_base_login_js,
                      )
    agent_, handoff_obj_CodeIndexFrontEnd= CodeIndexFrontEnd(
                        session_id, 
                        appcompany,
                        path_ProjectWeb,
                        path_html,
                        path_js,
                        path_css,
                        doc_md,
                        Keys_path,
                    )


    agent_ids = ['CodeReview_FrontEnd_Html']
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
        instructions=f"""{RECOMMENDED_PROMPT_PREFIX}\n
        {instruction_formatado}        
        """,
        model=str(model),
        tools=Tools_Name_dict,
        handoffs=[
          handoff_obj_CodeFrontEndDecisionDashboard,
          handoff_obj_CodeCheckoutFrontEnd,
          handoff_obj_CodeLoginFrontEnd,
          handoff_obj_CodeIndexFrontEnd
        ]
    )



    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=Data,
    )
    return agent, handoff_obj