
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################

def analyze_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                return content
        except:
            try:
                with open(file_path, 'r', encoding='latin-1') as file:
                    content = file.read()
                    return content
            except UnicodeDecodeError:
                return None