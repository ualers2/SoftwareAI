
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################


def format_instruction(instruction: str, context: dict) -> str:
    pattern = re.compile(r'\{(\w+)\}')
    def repl(match):
        var_name = match.group(1)
        if var_name in context:
            return str(context[var_name])
        else:
            raise KeyError(f"Variável '{var_name}' não encontrada no contexto.")
    return pattern.sub(repl, instruction)

