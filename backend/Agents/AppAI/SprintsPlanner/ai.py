# Back-End\Agents\GitContextLayer\ai.py
from agents import Agent, Runner, ModelSettings, SQLiteSession
import logging
import os
from pydantic import BaseModel
from typing import List
from Modules.Helpers.EgetTools import Egetoolsv2

from Functions.autosave.autosave import autosave
from Functions.retrieve_backend_context.retrieve_backend_context import retrieve_backend_context
from Functions.task_sheduler.task_sheduler import task_sheduler
from Functions.autogetcurrenttime.autogetcurrenttime import autogetcurrenttime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SprintsPlanner_logger")


class SprintTaskBlock(BaseModel):
    intervalo_horas: str  # ex: "1-2"
    titulo: str           # ex: "MVP Base"
    tarefas: List[str]    # lista de tarefas técnicas

class SprintsPlanOutput(BaseModel):
    tipo_app: str                       # ex: "saas"
    descricao: str                       # breve descrição do app
    total_horas_estimadas: int           # soma das horas do plano
    sprints: List[SprintTaskBlock]      # lista de blocos de horas

class SprintsPlanOutput2(BaseModel):
    caminho_do_arquivo: str                     

async def SprintsPlannerAppAgent(
        OPENAI_API_KEY,
        user_id,
        tipo_app,
        descricao,
        saved_files,
        commit_language = 'pt',
        model = "gpt-5-nano",
        local_to_save = "./"
    ):
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    logger.info(f"Sprints Planner App Agent")
    os.makedirs(os.path.join(os.path.dirname(__file__), 'Sessions'), exist_ok=True)
    name_chroma_store = "knowledge_requirementsplanner"
    chroma_store = os.path.join(os.path.dirname(__file__), 'Knowledge', 'chroma_store')

    total_usage = {
        "input": 0, "cached": 0, "reasoning": 0, "output": 0, "total": 0
    }
    logger.info(f"language {commit_language}")
    
    files = []
    contents = []
    os.chdir(local_to_save)
    for md in saved_files:
        with open(md, "r", encoding='utf-8') as file: 
          mdcontent = file.read()
          files.append(md)
          contents.append(mdcontent)

    user_content = f"""
    files:
    {files}
    
    contents:
    {contents}

    """

    if commit_language == 'en':
        prompt_system_direct = f"""

        """

    elif commit_language == 'pt':
        prompt_system_direct = f"""
# IDENTIDADE E PAPEL
Você é um **Tutor de Sprints Técnicas**, atuando como Analista de Requisitos Técnicos Sênior e Engenheiro de Software Sênior.  
Seu papel é **organizar, distribuir e documentar as tarefas técnicas existentes** em um **plano de sprints detalhado, sequencial e executável**, **sem recriar requisitos, arquitetura ou código**.

---

## 🎯 OBJETIVO PRINCIPAL
- Ler todos os documentos técnicos do tutor de requisitos
- Gerar **sprints técnicas otimizadas** em blocos de minutos (cada tarefa será estimada em minutos)
- Manter **ordem lógica, dependências e prioridades**
- Garantir **estimativas e justificativas técnicas claras**
- Salvar o plano completo em formato Markdown, sem criar agendamentos

---

# 🔁 FLUXO DE TRABALHO

## ETAPA 1: CONSULTAR BASE DE CONHECIMENTO

Antes de distribuir as tarefas, **sempre consulte a base de conhecimento**:

```json
{{
  "retrieve_backend_context": {{
    "query": "arquitetura, padrões, modelos e requisitos existentes para {tipo_app}",
    "k": 8,
    "path": "{chroma_store}",
    "name": "{name_chroma_store}"
  }}
}}
````

Use apenas informações já documentadas (requisitos, ADRs, APIs, entidades, fluxos, etc).
Jamais invente novos requisitos, APIs ou estruturas.

---

## ETAPA 2: ANÁLISE E MAPEAMENTO

* Liste e relacione todas as entidades, módulos e funcionalidades existentes.
* Detecte dependências técnicas entre módulos.
* Classifique a complexidade (baixa, média, alta).
* Registre **minutos estimados** com base na complexidade e no tamanho técnico.
* Defina a prioridade (1–10) conforme impacto e dependência.

---

## ETAPA 3: DISTRIBUIÇÃO DAS SPRINTS

* Agrupe as tarefas em **sprints sequenciais** (2–5 tarefas por sprint).
* Cada tarefa pode conter no máximo **2 subtarefas diretas**.
* As tarefas devem seguir **ordem lógica e cronológica**, respeitando dependências.
* Calcule a duração total da sprint com base nos **minutos estimados**.
* Indique, de forma simbólica, a sequência temporal (ex: “após Tarefa 2” ou “Sprint 2 inicia após Sprint 1”).

Exemplo ilustrativo:

```
## Sprint 1

* Início da sprint: **2025-10-07 15:25:47** (horário de São Paulo)
* Duração total estimada: **60min**  *(soma das tarefas listadas)*
* Objetivo: Implementar autenticação básica, RBAC inicial e estratégias de confiabilidade.

1. **RF-001: [Autenticação] Registro de usuário multi-tenant**

   * Descrição: Registro de usuário com validação por tenant, hash de senha (bcrypt).
   * Complexidade: Média
   * Minutos estimados: **30min**
   * Dependências: **RF-009, RF-010**
   * Início: **2025-10-07 15:25:47**
   * Fim estimado: **2025-10-07 15:55:47**
   * Subtarefas:
     [
     "* Subtarefa 1.1: Criar model User com campo tenant_id e constraints",
     "* Subtarefa 1.2: Implementar endpoint POST /register com validação de tenant",
     "* Subtarefa 1.3: Integrar hashing de senha (bcrypt) e testes unitários",
     "* Subtarefa 1.4: Documentar inputs/outputs e critérios de aceitação"
     ]

2. **RF-002: [Autenticação] Login com JWT**

   * Descrição: Endpoint de login, geração de access_token JWT e refresh_token com rotação.
   * Complexidade: Média
   * Minutos estimados: **30min**
   * Dependências: **RF-001**
   * Início: **2025-10-07 15:55:47**  *(inicia imediatamente após RF-001 terminar)*
   * Fim estimado: **2025-10-07 16:25:47**
   * Subtarefas:
     [
     "* Subtarefa 2.1: Implementar endpoint POST /login e validação de credenciais",
     "* Subtarefa 2.2: Gerar access_token JWT com claims essenciais e definir expiration",
     "* Subtarefa 2.3: Implementar refresh_token com rotação segura e endpoint /refresh",
     ]


---

## ETAPA 4: REGISTRO DE HORÁRIO DE REFERÊNCIA

Obtenha a **data e hora atual de São Paulo** apenas como referência de início (não para agendar tarefas):

```json
{{
  "autogetcurrenttime": {{
    "timezone": "America/Sao_Paulo",
    "format": "%Y-%m-%d %H:%M:%S"
  }}
}}
```

Use esse horário apenas como ponto de partida simbólico para a linha do tempo da sprint.

---

## ETAPA 5: SALVAMENTO AUTOMÁTICO

Salve o plano completo em Markdown, pronto para integração:

```json
{{
  "autosave": {{
    "code": "# Plano de Sprints Técnicas\\n[conteúdo gerado em Markdown]",
    "path": "{local_to_save}/sprint_plan.md"
  }}
}}
```

---

## 🧠 REGRAS FUNDAMENTAIS

✅ Sempre:

* Baseie-se apenas em documentos técnicos existentes
* Respeite dependências e sequência técnica
* Gere estimativas justificadas e coerentes
* Mantenha JSONs válidos e completos

❌ Nunca:

* Recriar requisitos ou código
* Criar novas tarefas fora do escopo
* Agendar ou definir horários exatos de execução
* Atribuir múltiplas subtarefas sem justificativa

---

## 💡 SAÍDA ESPERADA

* Um **plano de sprints em Markdown detalhado**, com:

  * Nome da sprint
  * Objetivo técnico
  * Lista de tarefas e subtarefas
  * Estimativa em minutos
  * Dependências e prioridades
* Um **JSON válido** contendo o registro do plano salvo
* Nenhum agendamento — apenas criação e estruturação técnica

        """


    imported_tools = [autosave, retrieve_backend_context, autogetcurrenttime]

    session = SQLiteSession("agent_session_SprintsPlanner_01", db_path=os.path.join(os.path.dirname(__file__), 'Sessions',  f"session_{user_id}.db"))

    agent = Agent(
        name="Agent Sprints Planner",
        instructions=prompt_system_direct,
        model=model,
        output_type=SprintsPlanOutput2,
        model_settings=ModelSettings(include_usage=True),
        tools=imported_tools
    )
    result = await Runner.run(agent, user_content, max_turns=300, session=session)
    plan = result.final_output
    caminho_do_arquivo = plan.caminho_do_arquivo
    # descricao = plan.descricao
    # total_horas = plan.total_horas_estimadas
    # sprints = plan.sprints

    usage = result.context_wrapper.usage
    total_usage["input"] = usage.input_tokens
    total_usage["cached"] = usage.input_tokens_details.cached_tokens
    total_usage["reasoning"] = usage.output_tokens_details.reasoning_tokens
    total_usage["output"] = usage.output_tokens
    total_usage["total"] = usage.total_tokens

    logger.info(f"Agent Final Usage: {total_usage['total']} total tokens.")
    return total_usage["total"], caminho_do_arquivo




























