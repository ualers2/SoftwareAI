#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################
from typing_extensions import TypedDict, Any
from agents import Agent, ModelSettings, function_tool, FileSearchTool, WebSearchTool, Runner

class AutosaveData(TypedDict):
   code: str
   path: str

@function_tool
def autosave(data: AutosaveData):
   """
   Save the provided Python code string to a file.

   Parameters:
   ----------
   code (str): The Python code to save.
   path (str): The name of the file where the code will be saved.

   Returns:
   -------
   None
   """
   try:
      data_FINAL = data["data"]
      code = data_FINAL["code"]
      path = data_FINAL["path"]
   except Exception as eroo1:
      print(eroo1)
      code = data["code"]
      path = data["path"]
   print("autosave Prestes a iniciar")
   try:
      print(f"autosave {path}")
      with open(path, 'w', encoding="utf-8") as file:
         file.write(code)

      data_return = {
         "status": "success", 
         "file_path": path,
      }


      return data_return
   
   
   except Exception as e:
      print(e)
      with open(path, 'x', encoding="utf-8") as file:
         file.write(code)

      data_return = {
         "status": "success", 
         "file_path": path,
      }


      return data_return