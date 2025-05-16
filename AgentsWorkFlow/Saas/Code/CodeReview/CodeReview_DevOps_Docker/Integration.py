from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel

from modules.modules import *


from AgentsWorkFlow.Saas.Code.DevOps.DockerFile.Integration import CodeDockerFileAgent
from AgentsWorkFlow.Saas.Code.DevOps.DockerBuild.Integration import CodeDockerBuildAgent
from AgentsWorkFlow.Saas.Code.DevOps.DockerCompose.Integration import CodeDockerComposeAgent
from AgentsWorkFlow.Saas.Code.DevOps.RequirementsTxt.Integration import CodeRequirementstxtAgent




class Data(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: Data):
    print(f"CodeReview_DevOps_Docker: {input_data.FrontEndContent}")

def CodeReview_DevOps_Docker(session_id, appcompany,
                        path_ProjectWeb,
                        path_html,
                        path_js,
                        path_css,
                        doc_md,
                        Keys_path,
                        docker_file,
                        docker_compose,
                        dockerbuild
                    ):

    os.chdir(path_ProjectWeb)
    agent, _CodeDockerFileAgent = CodeDockerFileAgent(session_id, appcompany,
                                    path_ProjectWeb,
                                    path_html,
                                    path_js,
                                    path_css,
                                    doc_md,
                                    Keys_path,
                                    docker_file
                        )
    agent, _CodeDockerComposeAgent = CodeDockerComposeAgent(session_id, appcompany,
                        path_ProjectWeb,
                        path_html,
                        path_js,
                        path_css,
                        doc_md,
                        Keys_path,
                        docker_compose
                    )
    agent, _CodeDockerBuildAgent = CodeDockerBuildAgent(session_id, appcompany,
                        path_ProjectWeb,
                        path_html,
                        path_js,
                        path_css,
                        doc_md,
                        Keys_path,
                        dockerbuild
                    )
    agent, _CodeRequirementstxtAgent = CodeRequirementstxtAgent(session_id, appcompany,
                        path_ProjectWeb,
                        path_html,
                        path_js,
                        path_css,
                        doc_md,
                        Keys_path,
                    )
    agent_ids = ['CodeReview_DevOps_Docker']
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
        handoffs=[_CodeDockerFileAgent,
                  _CodeDockerComposeAgent,
                  _CodeDockerBuildAgent,
                  _CodeRequirementstxtAgent,


                  
                ],
    )



    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=Data,
    )
    return agent, handoff_obj