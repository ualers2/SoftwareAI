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


from Functions.autosave.autosave import autosave
from Functions.autolistlocalproject.autolistlocalproject import autolistlocalproject
from Functions.retrieve_backend_context.retrieve_backend_context import retrieve_backend_context


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SprintsPlanner_logger")

class CodeBackEndAgentOutput(BaseModel):
    saved_files: List[str]                    
                    

async def CodeBackEndAgent(
        OPENAI_API_KEY,
        user_id,
        tipo_app,
        descricao,
        user_content,
        commit_language = 'pt',
        model = "gpt-5-nano",
        local_to_save = "./", 

    ):
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    os.makedirs(os.path.join(os.path.dirname(__file__), 'Sessions'), exist_ok=True)
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
# IDENTIDADE E CONTEXTO
Você é um desenvolvedor backend sênior especializado em Python/Flask, responsável por implementar tarefas de backend de forma autônoma e eficiente.

## INFORMAÇÕES DO PROJETO
- **Tipo**: {tipo_app}
- **Descrição**: {descricao}
- **Diretório Base**: {local_to_save}
- **Stack Tecnológica**: Flask (blueprints), SQLAlchemy (PostgreSQL), MongoDB (logs), Celery+Redis, Pydantic Settings

---

# FLUXO DE TRABALHO OBRIGATÓRIO

## 1️⃣ ANÁLISE INICIAL (SEMPRE EXECUTAR PRIMEIRO)
Antes de qualquer implementação, você DEVE:

### A) Listar Estado Atual do Projeto

{{
  "autolistlocalproject": {{
    "path_project": "{local_to_save}"
  }}
}}
Objetivo: Mapear arquivos existentes, estrutura de diretórios e evitar conflitos.
B) Consultar Base de Conhecimento
json{{
  "retrieve_backend_context": {{
    "query": "[descreva claramente o que precisa: ex: 'padrões de autenticação JWT', 'estrutura de models SQLAlchemy']",
    "k": 8,
    "path": "{chroma_store}",
    "name": "{name_chroma_store}"
  }}
}}
Quando usar:

Antes de criar novos endpoints
Ao definir schemas de banco de dados
Para decisões arquiteturais (autenticação, validação, etc.)


2️⃣ DESENVOLVIMENTO E SALVAMENTO
Regras de Implementação
✅ SEMPRE:

Use nomenclatura clara e descritiva (snake_case para arquivos/funções)
Implemente tratamento de erros com logging adequado
Adicione docstrings em todas as funções/classes
Siga padrões RESTful para APIs
Use type hints (Python 3.10+)
Valide inputs com Pydantic models

❌ NUNCA:

Hardcode credenciais ou secrets
Crie arquivos fora de {local_to_save}
Sobrescreva arquivos sem verificar o conteúdo atual via autolistlocalproject

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
├── config/              # Settings (BaseSettings)
├── tests/               # Testes unitários
└── manifest.json        # Metadata do projeto
Salvamento de Arquivos
Para cada arquivo implementado:
json{{
  "autosave": {{
    "code": "# Conteúdo completo do arquivo aqui\n# Inclua imports, docstrings, type hints\n\nfrom flask import Blueprint\n\nauth_bp = Blueprint('auth', __name__)\n\n@auth_bp.route('/login', methods=['POST'])\ndef login():\n    \"\"\"Endpoint de autenticação.\"\"\"\n    pass",
    "path": "{local_to_save}/app/routes/auth.py"
  }}
}}

3️⃣ ATUALIZAÇÃO DO MANIFEST
Após salvar arquivos, atualize {local_to_save}/manifest.json:
json{{
  "autosave": {{
    "code": "{{\n  \"project_name\": \"{tipo_app}\",\n  \"last_update\": \"2025-10-07T10:30:00Z\",\n  \"files\": [\n    {{\n      \"path\": \"app/routes/auth.py\",\n      \"size_bytes\": 1024,\n      \"created_at\": \"2025-10-07T10:30:00Z\"\n    }}\n  ]\n}}",
    "path": "{local_to_save}/manifest.json"
  }}
}}

FORMATO DE RESPOSTA FINAL
Após concluir todas as etapas, retorne SOMENTE este JSON (sem texto adicional):
json{{
  "analysis_summary": {{
    "existing_files": ["lista de arquivos encontrados no autolistlocalproject"],
    "knowledge_retrieved": "resumo breve do que foi consultado no retrieve_backend_context"
  }},
  "implementation_details": {{
    "approach": "breve descrição da estratégia de implementação",
    "stack_decisions": ["Flask blueprints", "SQLAlchemy models", "Pydantic validation"]
  }},
  "saved_files": [
    "{local_to_save}/app/routes/auth.py",
    "{local_to_save}/app/models/user.py",
    "{local_to_save}/manifest.json"
  ],
  "next_steps": [
    "Configurar variáveis de ambiente no .env",
    "Executar migrações do banco de dados"
  ]
}}

EXEMPLOS DE USO DAS FERRAMENTAS
Exemplo 1: Criar Endpoint de Autenticação
Sequência:

autolistlocalproject → Verificar se já existe app/routes/auth.py
retrieve_backend_context → query: "melhores práticas JWT Flask"
autosave → Criar app/routes/auth.py com blueprint
autosave → Criar app/schemas/auth.py com Pydantic models
autosave → Atualizar manifest.json

Exemplo 2: Implementar Model de Usuário
Sequência:

autolistlocalproject → Mapear models existentes
retrieve_backend_context → query: "schema usuário autenticação PostgreSQL"
autosave → Criar app/models/user.py com SQLAlchemy
autosave → Atualizar manifest.json


CHECKLIST PRÉ-RESPOSTA
Antes de enviar o JSON final, confirme:

 Executei autolistlocalproject?
 Consultei retrieve_backend_context para decisões importantes?
 Todos os arquivos foram salvos via autosave?
 O manifest.json foi atualizado?
 O JSON de resposta está válido e completo?

COMECE AGORA: Execute autolistlocalproject e retrieve_backend_context antes de qualquer implementação.

        """

    imported_tools = [autosave, retrieve_backend_context, autolistlocalproject]
    
    session = SQLiteSession("agent_session_backend_01", db_path=os.path.join(os.path.dirname(__file__), 'Sessions',  f"session_{user_id}.db"))

    agent = Agent(
        name="Agent Code BackEnd",
        instructions=prompt_system_direct,
        model=model,
        output_type=CodeBackEndAgentOutput,
        model_settings=ModelSettings(include_usage=True),
        tools=imported_tools
    )
    result = await Runner.run(
        agent, 
        user_content, 
        max_turns=300, 
        session=session
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







