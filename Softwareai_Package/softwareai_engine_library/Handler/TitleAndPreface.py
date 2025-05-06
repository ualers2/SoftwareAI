
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
import re
from pydantic import BaseModel
from firebase_admin import App
import importlib

class TitleAndPreface(BaseModel):
    title: str
    preface: str
