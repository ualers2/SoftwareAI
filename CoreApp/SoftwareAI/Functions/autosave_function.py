
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################

def autosave(code, path):
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
        with open(path, 'w', encoding="utf-8") as file:
            file.write(code)
        return True
    except Exception as e:
        print(e)
        with open(path, 'x', encoding="utf-8") as file:
            file.write(code)
        return True