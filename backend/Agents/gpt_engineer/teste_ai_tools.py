# Back-End\Agents\gpt_engineer\teste_ai.py
import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
import os
import logging


os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'keys.env'))

logger = logging.getLogger(__name__)

# Tool de teste
class AutosaveTool(BaseModel):
    """Tool para salvar código Python em arquivo"""
    code: str = Field(..., description="Código Python a ser salvo")
    path: str = Field(..., description="Caminho completo do arquivo onde o código será salvo")

def autosave(data: AutosaveTool) -> dict:
    """Função que salva o código, chamada pela tool do LLM"""
    try:
        os.makedirs(os.path.dirname(data.path), exist_ok=True)
        with open(data.path, 'w', encoding='utf-8') as f:
            f.write(data.code)
        logger.info(f"Arquivo salvo com sucesso: {data.path}")
        return {"status": "success", "file_path": data.path}
    except Exception as e:
        logger.error(f"Erro ao salvar arquivo {data.path}: {e}")
        return {"status": "error", "message": str(e)}

# Instancia LLM
llm = ChatOpenAI(
    model="gpt-5-nano",
    temperature=0,
    max_tokens=None,
    max_retries=2,
    streaming=False
)

# Bind da tool
llm_with_tools = llm.bind_tools([AutosaveTool])

# Prompt de teste
prompt = "Salve o seguinte código em ./teste.py:\nprint('Oi Mundo!')"

# Invoca o LLM
ai_msg = llm_with_tools.invoke(prompt)
print("Tool calls retornadas pelo LLM:", ai_msg.tool_calls)

# Executa as tool calls
for tool_call in getattr(ai_msg, "tool_calls", []):
    tool_name = tool_call.get("name")
    args = tool_call.get("args", {})
    if tool_name == "AutosaveTool":
        result = autosave(AutosaveTool(**args))
        print("Resultado da tool:", result)
