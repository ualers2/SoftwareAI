#########################################
# IMPORT SoftwareAI Agents
from softwareai.CoreApp._init_agents_ import AgentInitializer
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################

byte_manager = AgentInitializer.get_agent('ByteManager') 
mensagem = "solicito um script para Análise técnica da criptomoeda dogecoin"
owner_response = byte_manager.AI_1_ByteManager_Company_Owners(mensagem)
print(owner_response)
