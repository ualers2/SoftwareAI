
import sys
import os


import struct
import re
import platform
import json
import ast
from firebase_admin import credentials, initialize_app, storage, db, delete_app
from datetime import datetime



from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


from typing import Optional, List, Union
from typing_extensions import override


class QListAgents(QThread):
    AgentSelector = Signal(str)
    messagesignal = Signal(str)
    def __init__(self):
        super().__init__()
        pass
        
    def run(self):
        paths_agents = self.init_paths_agents()
        self.messagesignal.emit("Searching\nfor Agents...")
        for path in paths_agents:
            agentss = os.listdir(path)
            for agent in agentss:
                if agent == "DocGitHubData":
                    pass
                elif agent == "docs_uploaded.log":
                    pass
                elif agent == "__pycache__":
                    pass
                else:
                    agentpath = os.path.join(path, agent)
                    with open(agentpath, 'r', encoding='latin-1') as file:
                        content = file.read()
                        matches = re.findall(r'key\s*[:=]\s*["\']?([^"\',\s]+)["\']?', content)
                        keyAssistant = matches[0]
                        if matches:
                            self.AgentSelector.emit(keyAssistant)
                        file.close()



    def init_paths_agents(self):
        paths_agents = [
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../CoreApp/Agents/Software_Requirements_Analysis')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../CoreApp/Agents/Software_Planning')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../CoreApp/Agents/Software_Documentation')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../CoreApp/Agents/Software_Development')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../CoreApp/Agents/Pre_Project')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../CoreApp/Agents/Company_Managers')),
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../CoreApp/Agents/Company_CEO')),
        ]
        return paths_agents


