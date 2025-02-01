# IMPORT SoftwareAI _init_environment_
from softwareai.CoreApp._init_environment_ import init_env
# IMPORT SoftwareAI Agents
from softwareai.CoreApp.Agents.Software_Development.QuantumCore import QuantumCoreUpdate
#########################################


def autoupdaterepo(
                repo_name,
                client,
                appfb,
                OpenAIKeysteste,
                GithubKeys,
                python_functions,
                Agent_files_update,
                AutenticateAgent,
                ResponseAgent,
                ):
    
    init_env(repo_name)

    Melhorias = QuantumCoreUpdate(
                repo_name,
                client,
                appfb,
                OpenAIKeysteste,
                GithubKeys,
                python_functions,
                Agent_files_update,
                AutenticateAgent,
                ResponseAgent,
            )