# Back-End\Agents\AppAI\SprintsSheduler\ai.py
from agents import Agent, Runner, ModelSettings, SQLiteSession
import logging
import os
from pydantic import BaseModel
from typing import List
from Modules.Helpers.EgetTools import Egetoolsv2

from Functions.task_sheduler.task_sheduler import task_sheduler
from Functions.autogetcurrenttime.autogetcurrenttime import autogetcurrenttime


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SprintsPlanner_logger")

class Output(BaseModel):
  total_de_tarefas_agendadas: str                     

async def SprintsShedulerAppAgent(
        OPENAI_API_KEY,
        user_id,
        ACCESS_TOKEN,
        user_content,
        BACKEND_URL,
        commit_language = 'pt',
        model = "gpt-5-nano",
    ):
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    logger.info(f"Sprints Sheduler App Agent")
    os.makedirs(os.path.join(os.path.dirname(__file__), 'Sessions'), exist_ok=True)
    total_usage = {
        "input": 0, "cached": 0, "reasoning": 0, "output": 0, "total": 0
    }
    logger.info(f"language {commit_language}")
    

    if commit_language == 'en':
        prompt_system_direct = f"""

        """

    elif commit_language == 'pt':
        prompt_system_direct = f"""

# IDENTIDADE E PAPEL
Você é um **Agente de Agendamento de Sprints Técnicas**, atuando como Engenheiro de Software Sênior.  
Seu papel é **receber um documento de sprints técnicas já definidas** e **agendar cada tarefa individualmente no backend**, usando **exatamente o conteúdo da tarefa**, incluindo nome, subtarefas e dependências.

---

## 🎯 OBJETIVO PRINCIPAL
- Ler o Markdown ou JSON contendo as sprints detalhadas
- Para cada tarefa, criar `SPRINT_OBJECTIVE` contendo:
  - Nome da tarefa
  - Todas as subtarefas listadas
  - Todas as dependências explícitas
  - O Objetivo listado
- Calcular `eta_str` baseado no horário da tarefa anterior, respeitando dependências
- Criar agendamentos individuais no backend usando `task_sheduler`

---

## 🔁 FLUXO DE TRABALHO

### ETAPA 1: CONSULTAR DOCUMENTO EXISTENTE
- Leia o plano de sprints fornecido (`Markdown` ou `JSON`) contendo:
  - Nome da sprint
  - Lista de tarefas e subtarefas
  - Dependências entre tarefas
  - Estimativa de horas
- **Não crie novas tarefas**, use somente as existentes no documento.

- **Importante:** cada `SPRINT_OBJECTIVE` deve conter **tudo que está na tarefa**, incluindo subtarefas e dependências, sem modificar ou resumir.

---

### ETAPA 2: OBTENÇÃO DO HORÁRIO INICIAL
- Obtenha o horário atual em **São Paulo** como referência para a primeira tarefa.

```json
{{
  "autogetcurrenttime": {{
    "timezone": "America/Sao_Paulo",
    "format": "%Y-%m-%d %H:%M:%S"
  }}
}}
````

---

### ETAPA 3: CALCULAR HORÁRIOS (`eta_str`)

* Para cada tarefa:

  * Somar o tempo estimado da tarefa anterior para definir `eta_str`
  * Respeitar dependências
  * Garantir **nenhuma sobreposição de horários**

---

### ETAPA 4: ENVIAR AGENDAMENTOS PARA O BACKEND

Para cada tarefa, gerar o JSON de execução usando `task_sheduler`:

```json
{{
  "task_sheduler": {{
    "BACKEND_URL": "{BACKEND_URL}",
    "ACCESS_TOKEN": "{ACCESS_TOKEN}",
    "EMPLOYER_CATEGORY": "desenvolvimento",
    "SPRINT_NAME": "nome da sprint",
    "SPRINT_OBJECTIVE": "conteúdo completo da tarefa + todas subtarefas + dependências conforme documento",
    "user_id": {user_id},
    "priority": "nível de prioridade (1-10)",
    "hours": "minutos estimados da tarefa",
    "lang": "pt",
    "eta_str": "data e hora de execução da tarefa (%Y-%m-%d %H:%M:%S)"
  }}
}}
```

⚠️ **Importante:**

* `SPRINT_OBJECTIVE` **deve refletir 100% do conteúdo original**, incluindo subtarefas e dependências
* `eta_str` calculado dinamicamente, sem sobreposição de horários

---

## 🧠 REGRAS FUNDAMENTAIS

✅ Sempre:

* Use **exatamente** nome + subtarefas + dependências da tarefa do documento
* Respeite dependências, sequência e prioridades
* Gere horários coerentes e progressivos
* Produza JSONs válidos para backend

❌ Nunca:

* Alterar objetivos, subtarefas ou dependências
* Criar tarefas extras
* Reutilizar horários

---

## 💡 SAÍDA ESPERADA

* JSONs individuais para cada tarefa com `SPRINT_OBJECTIVE` completo (título + subtarefas + dependências)
* Horários (`eta_str`) progressivos e coerentes
* Integração pronta com backend para execução automática


        """


    imported_tools = [task_sheduler, autogetcurrenttime]

    session = SQLiteSession("agent_session_SprintsSheduler_01", db_path=os.path.join(os.path.dirname(__file__), 'Sessions',  f"session_{user_id}.db"))

    agent = Agent(
        name="Agent Sprints Sheduler",
        instructions=prompt_system_direct,
        model=model,
        output_type=Output,
        model_settings=ModelSettings(include_usage=True),
        tools=imported_tools
    )
    result = await Runner.run(agent, user_content, max_turns=300, session=session)
    plan = result.final_output
    total_de_tarefas_agendadas = plan.total_de_tarefas_agendadas
    usage = result.context_wrapper.usage
    total_usage["input"] = usage.input_tokens
    total_usage["cached"] = usage.input_tokens_details.cached_tokens
    total_usage["reasoning"] = usage.output_tokens_details.reasoning_tokens
    total_usage["output"] = usage.output_tokens
    total_usage["total"] = usage.total_tokens

    logger.info(f"Agent Final Usage: {total_usage['total']} total tokens.")
    return total_usage["total"], total_de_tarefas_agendadas




























