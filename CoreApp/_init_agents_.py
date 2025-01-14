from softwareai.CoreApp.Agents.Company_CEO.ByteManager import ByteManager

from softwareai.CoreApp.Agents.Software_Planning.Bob import Gerente_de_projeto
from softwareai.CoreApp.Agents.Software_Documentation.CloudArchitect import Software_Documentation
from softwareai.CoreApp.Agents.Software_Planning.Dallas import Equipe_De_Solucoes
from softwareai.CoreApp.Agents.Software_Development.DataWeaver import software_improvements
from softwareai.CoreApp.Agents.Company_Managers.AI_MatrixMinder_Company_Managers import Company_Managers
from softwareai.CoreApp.Agents.Software_Development.QuantumCore import SoftwareDevelopment
from softwareai.CoreApp.Agents.Software_Development.SignalMaster import SoftwareDevelopment_SignalMaster
from softwareai.CoreApp.Agents.Software_Requirements_Analysis.SynthOperator import Softwareanaysis
from softwareai.CoreApp.Agents.Pre_Project.Tigrao import Pre_Project_Document
from softwareai.CoreApp.Agents.Software_Development.NexGenCoder import SoftwareDevelopment_NexGenCoder

class AgentInitializer:
    _agents = {}

    @classmethod
    def initialize_agents(cls):
        """Initializes all agents and stores them in the _agents dictionary."""
        cls._agents['Gerente_de_projeto'] = Gerente_de_projeto()

        cls._agents['Company_Managers'] = Company_Managers() 
        cls._agents['Pre_Project_Document'] = Pre_Project_Document() 
        cls._agents['Software_Documentation'] = Software_Documentation()
        cls._agents['Equipe_De_Solucoes'] = Equipe_De_Solucoes()
        cls._agents['Softwareanaysis'] = Softwareanaysis()
        cls._agents['software_improvements'] = software_improvements()
        cls._agents['SoftwareDevelopment_SignalMaster'] = SoftwareDevelopment_SignalMaster()
        cls._agents['SoftwareDevelopment_NexGenCoder'] = SoftwareDevelopment_NexGenCoder()
        cls._agents['SoftwareDevelopment'] = SoftwareDevelopment(
            cls._agents['Software_Documentation'],
            cls._agents['software_improvements'],
            cls._agents['SoftwareDevelopment_SignalMaster'],
            cls._agents['SoftwareDevelopment_NexGenCoder']
        )
        cls._agents['ByteManager'] = ByteManager(
            cls._agents['Company_Managers'],
            cls._agents['Pre_Project_Document'],
            cls._agents['Gerente_de_projeto'],
            cls._agents['Equipe_De_Solucoes'],
            cls._agents['Softwareanaysis'],
            cls._agents['SoftwareDevelopment'],
            cls._agents['Software_Documentation'],
        )

        
    @classmethod
    def get_agent(cls, agent_name):
        """Returns an agent instance by name."""
        return cls._agents.get(agent_name)

AgentInitializer.initialize_agents()