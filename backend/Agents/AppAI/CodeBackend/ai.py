# Back-End\Agents\GitContextLayer\ai.py
from agents import Agent, Runner, ModelSettings
import logging
import os
from pydantic import BaseModel
from typing import List

import os
from agents import Agent, Runner, function_tool, SQLiteSession
import openai
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from openai import OpenAI

from typing_extensions import TypedDict, Any
from agents import Agent, ModelSettings, Runner, RunConfig, function_tool, FileSearchTool, WebSearchTool, Runner
from datetime import datetime
import requests
from agents.mcp import MCPServerStdio

from Functions.autosave.autosave import autosave
from Functions.autolistlocalproject.autolistlocalproject import autolistlocalproject
from Functions.retrieve_backend_context.retrieve_backend_context import retrieve_backend_context


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SprintsPlanner_logger")

class CodeBackEndAgentOutput(BaseModel):
  saved_files: List[str]                
      
class ReflectionAgentAgentOutput(BaseModel):
  should_retry: bool  
  suggested_changes: List[str]              
  confidence: float

class ReflectionData(TypedDict):
  task: str
  last_output: str
  history: List[str]
import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from pydantic import BaseModel
from agents import FunctionTool, RunContextWrapper

logger = logging.getLogger("sequentialthinking")
logging.basicConfig(level=logging.ERROR)


class ThoughtArgs(BaseModel):
    thought: str
    nextThoughtNeeded: bool
    thoughtNumber: int
    totalThoughts: int
    isRevision: Optional[bool] = None
    revisesThought: Optional[int] = None
    branchFromThought: Optional[int] = None
    branchId: Optional[str] = None
    needsMoreThoughts: Optional[bool] = None


class SequentialThinkingState:
    def __init__(self):
        self.thought_history: List[ThoughtArgs] = []
        self.branches: Dict[str, List[ThoughtArgs]] = {}
        self.lock = asyncio.Lock()

    def _format_thought(self, t: ThoughtArgs) -> str:
        header_parts = []
        if t.isRevision:
            header_parts.append("🔄 Revision")
        elif t.branchFromThought:
            header_parts.append("🌿 Branch")
        else:
            header_parts.append("💭 Thought")
        header = f"{header_parts[0]} {t.thoughtNumber}/{t.totalThoughts}"
        if t.isRevision and t.revisesThought:
            header += f" (revising thought {t.revisesThought})"
        if t.branchFromThought and t.branchId:
            header += f" (from thought {t.branchFromThought}, ID: {t.branchId})"
        body = t.thought
        width = max(len(header), len(body)) + 4
        border = "─" * width
        formatted = f"\n┌{border}┐\n│ {header.ljust(width-2)} │\n├{border}┤\n│ {body.ljust(width-2)} │\n└{border}┘"
        return formatted

    async def process(self, data: ThoughtArgs) -> Dict[str, Any]:
        async with self.lock:
            if data.thoughtNumber > data.totalThoughts:
                data.totalThoughts = data.thoughtNumber
            self.thought_history.append(data)
            if data.branchFromThought and data.branchId:
                if data.branchId not in self.branches:
                    self.branches[data.branchId] = []
                self.branches[data.branchId].append(data)
            formatted = self._format_thought(data)
            logger.error(formatted)
            return {
                "thoughtNumber": data.thoughtNumber,
                "totalThoughts": data.totalThoughts,
                "nextThoughtNeeded": data.nextThoughtNeeded,
                "branches": list(self.branches.keys()),
                "thoughtHistoryLength": len(self.thought_history),
            }


_state = SequentialThinkingState()


async def _on_invoke(ctx: RunContextWrapper[Any], args_json: str) -> str:
    parsed = ThoughtArgs.model_validate_json(args_json)
    result = await _state.process(parsed)
    return json.dumps(result, indent=2)


tool_sequentialthinking = FunctionTool(
    name="sequentialthinking",
    description=(
        "Ferramenta para pensamento sequencial/reflexivo. Aceita um objeto com os campos:"
        " thought, nextThoughtNeeded, thoughtNumber, totalThoughts, isRevision, revisesThought,"
        " branchFromThought, branchId, needsMoreThoughts"
    ),
    params_json_schema=ThoughtArgs.model_json_schema(),
    on_invoke_tool=_on_invoke,
)

# async def _sequential_thinking():
#     async with MCPServerStdio(
#         name="sequentialthinking",
#         params={
#             "command": "docker",
#             "args": [
#                 "run",
#                 "--rm",
#                 "-i",
#                 "mcp/sequentialthinking"
#             ],
#         },
#         client_session_timeout_seconds=45
#     ) as sequential_thinking:
#       return sequential_thinking
    
# async def _git_server(src):
#     async with MCPServerStdio(
#         name="git",
#         params={
#             "command": "docker",
#             "args": ["run", 
#                     "--rm", 
#                     "-i", 
#                     "--mount", 
#                     f"type=bind,src={src},dst={src}", 
#                     "mcp/git"
#                 ],
#         },
#         client_session_timeout_seconds=45
#     ) as git_:
#       return git_

async def CodeBackEndAgent(
      OPENAI_API_KEY,
      user_id,
      tipo_app,
      title,
      description,
      category,
      price,
      technologies,
      early_bonus,
      deadline,
      commit_language = 'pt',
      model = "gpt-5-nano",
      local_to_save = "./", 

  ):
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    os.makedirs(os.path.join(os.path.dirname(__file__), 'Sessions'), exist_ok=True)
    os.chdir(local_to_save)
    logger.info(f"CodeBackEndAgent Agent")
    name_chroma_store = "backend_skeleton"
    chroma_store = os.path.join(os.path.dirname(__file__), 'CodeKnowledge', 'chroma_store')

    total_usage = {
        "input": 0, "cached": 0, "reasoning": 0, "output": 0, "total": 0
    }
    logger.info(f"language {commit_language}")
    
    if commit_language == 'en':
        prompt_system_direct = f"""

        """

    elif commit_language == 'pt':
        prompt_system_direct = f"""
Você é um desenvolvedor backend sênior especializado em Python/Flask, 
responsável por implementar tarefas de backend de forma autônoma e eficiente.\n
# FLUXO DE TRABALHO OBRIGATÓRIO\n
1) ANÁLISE INICIAL (SEMPRE EXECUTAR PRIMEIRO)\n
  1.1 - Antes de qualquer implementação, você DEVE:
    Listar Estado Atual do Projeto
    {{
      "autolistlocalproject": {{
        "path_project": "{local_to_save}"
        "show_contents" True
      }}
    }}
    Objetivo: Mapear arquivos existentes, estrutura de diretórios e evitar conflitos.\n
  1.2 - sequentialthinking
    Use o pensamento sequencial para pensar e planejar o desenvolvimento 
  
---\n
2) DESENVOLVIMENTO E SALVAMENTO\n
  2.1 - Regras de Implementação\n
  Use o pensamento sequencial para cada codigo funcional e sem erros
  2.2 - Salvamento de Arquivos\n
  Para cada arquivo implementado:
  json{{
    "autosave": {{
      "code": "# Conteúdo completo do arquivo aqui\n# Inclua imports, docstrings, type hints\n\nfrom flask import Blueprint\n\nauth_bp = Blueprint('auth', __name__)\n\n@auth_bp.route('/login', methods=['POST'])\ndef login():\n    \"\"\"Endpoint de autenticação.\"\"\"\n    pass",
      "path": "{local_to_save}/app/routes/auth.py"
    }}
  }}
  \n
  2.3 - Regras de desing system\n
    Use nomenclatura clara e descritiva (snake_case para arquivos/funções)
    Implemente tratamento de erros com logging adequado
    Adicione docstrings em todas as funções/classes
    Siga padrões RESTful para APIs
    Use type hints (Python 3.10+)
    Valide inputs com Pydantic models\n

    Estrutura de Diretórios Padrão
    {local_to_save}/
    ├── app/
    │   ├── __init__.py
    │   ├── models/          # SQLAlchemy models
    │   ├── routes/          # Flask blueprints
    │   ├── schemas/         # Pydantic schemas
    │   ├── services/        # Business logic
    │   └── utils/           # Helpers
    ├── tasks/               # Celery tasks
    ├── config/              # Settings 
    ├── tests/               # Testes unitários
  2.4 - NUNCA FAÇA ISSO:\n
    Hardcode credenciais ou secrets
    Criar arquivos fora de {local_to_save}
    Sobrescrever arquivos sem verificar o conteúdo atual via autolistlocalproject\n
---\n
3) FORMATO DE RESPOSTA FINAL\n
  3.1 - Após concluir todas as etapas, retorne SOMENTE este JSON (sem texto adicional):
    json{{
      "analysis_summary": {{
        "existing_files": ["lista de arquivos encontrados no autolistlocalproject"],
      }},
      "implementation_details": {{
        "approach": "breve descrição da estratégia de implementação",
        "stack_decisions": ["Flask blueprints", "SQLAlchemy models", "Pydantic validation"]
      }},
      "saved_files": [
        "{local_to_save}/app/routes/auth.py",
        "{local_to_save}/manifest.json"
      ],
      "next_steps": [
        "Configurar variáveis de ambiente no .env",
        "Executar migrações do banco de dados"
      ]
    }}
    - o saved_files deve ser de arquivos salvos ou modificados

EXEMPLOS DE USO DAS FERRAMENTAS\n
Exemplo 1: Criar Endpoint de Autenticação
Sequência:
autolistlocalproject → Verificar se já existe app/routes/auth.py
sequentialthinking → pensamento em como implementar o app/routes/auth.py com blueprint de forma proativa e eficiente
autosave → Criar app/routes/auth.py com blueprint
sequentialthinking → pensamento em como desenvolver o  app/schemas/auth.py com Pydantic models de forma proativa e eficiente
autosave → Criar app/schemas/auth.py com Pydantic models
Exemplo 2: Implementar Model de Usuário
Sequência:
autolistlocalproject → Mapear models existentes
sequentialthinking → pensamento em como desenvolver o app/models/user.py com SQLAlchemy de forma proativa e eficiente
autosave → Criar app/models/user.py com SQLAlchemy
---\n
CHECKLIST PRÉ-RESPOSTA
Antes de enviar o JSON final, confirme:
 Executei autolistlocalproject?
 Consultei o pensamento sequencial para decisões importantes?
 Todos os arquivos foram salvos via autosave?
 O JSON de resposta está válido e completo?
        """
        
        user_content = f"""
## INFORMAÇÕES DO PROJETO
- Tipo: {tipo_app}
- Titulo: {title}
- Descrição: {description}
- Categoria: {category}
- Stack Tecnológica: {technologies}
- Preço Pago Pela Solucao: {price}
- Data Limite De Entrega: {deadline}
- Bonus Recebido Em Caso De Entrega Antecipada: {early_bonus}
- Diretório Base: {local_to_save}
    """
# ---\n
# Conhecimento de Ferramentas de operacoes git\n
# Registra alterações no staging area
# Entradas:
# repo_path(string): Caminho para o repositório Git
# message(string): Mensagem de confirmação
# Retorna: Confirmação com novo hash de commit
# git_add
# \n
# Registra alterações no repositório local\n
# Entradas:
# repo_path(string): Caminho para o repositório Git
# target(string): Ramificação de destino ou commit para comparar com
# Retorna: Saída diferente comparando o estado atual com o alvo
# git_commit
# \n
# Criar nova branch\n
# Entradas:
# repo_path(string): Caminho para o repositório Git
# max_count(número, opcional): Número máximo de confirmações a serem exibidas (padrão: 10)
# Retorna: Matriz de entradas de confirmação com hash, autor, data e mensagem
# git_create_branch
# ---\n
    imported_tools = [
                    autosave, 
                    autolistlocalproject,
                    tool_sequentialthinking
                  ]
    
    session = SQLiteSession("agent_session_backend_01", db_path=os.path.join(os.path.dirname(__file__), 'Sessions',  f"session_{user_id}.db"))
    
    # git_server = await _git_server(local_to_save)
    # sequential_thinking = await _sequential_thinking()
    async with MCPServerStdio(
        name="sequentialthinking",
        params={
            "command": "docker",
            "args": [
                "run",
                "--rm",
                "-i",
                "mcp/sequentialthinking"
            ],
        },
        client_session_timeout_seconds=45
    ) as sequential_thinking:
      agent = Agent(
          name="Agent Code BackEnd",
          instructions=prompt_system_direct,
          model=model,
          # mcp_servers=[
          #   sequential_thinking, 
          #   # git_server
          # ],
          output_type=CodeBackEndAgentOutput,
          model_settings=ModelSettings(
                                      tool_choice="sequentialthinking",
                                      include_usage=True
                                    ),
          tools=imported_tools
      )

      result = await Runner.run(
          agent, 
          user_content, 
          max_turns=300, 
          session=session,
          run_config=RunConfig(
                  model_settings=ModelSettings(
                  tool_choice="sequentialthinking",
                  include_usage=True,
                  parallel_tool_calls=True
                )
                ),
      )
      final_output = result.final_output
      saved_files = final_output.saved_files
    
      usage = result.context_wrapper.usage
      total_usage["input"] = usage.input_tokens
      total_usage["cached"] = usage.input_tokens_details.cached_tokens
      total_usage["reasoning"] = usage.output_tokens_details.reasoning_tokens
      total_usage["output"] = usage.output_tokens
      total_usage["total"] = usage.total_tokens

      logger.info(f"Agent Final Usage: {total_usage['total']} total tokens.")


      return total_usage["total"], saved_files







