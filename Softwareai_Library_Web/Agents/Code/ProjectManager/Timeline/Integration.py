from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################

from modules.modules import *

from Agents.Code.FrontEnd.Index.Integration import CodeIndexFrontEnd


class doc_pre_project_Data(BaseModel):
    doc_pre_project: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: doc_pre_project_Data):
    print(f"CodeRequirementsAndTimeline: {input_data.doc_pre_project}")


def CodeRequirementsAndTimeline(
    WEBHOOK_URL,
    session_id,
    user_email,
    ):

    agent_codefrontend, handoff_obj_codeindexfrontEnd = CodeIndexFrontEnd(
        WEBHOOK_URL,
        session_id,
        user_email,
        )

   
    path_ProjectWeb = "/app/LocalProject"
    os.chdir(path_ProjectWeb)
    path_html = f"{path_ProjectWeb}/templates"
    path_js = f"{path_ProjectWeb}/static/js"
    path_css = f"{path_ProjectWeb}/static/css"
    doc_md = f"{path_ProjectWeb}/doc_md"

    githubtoken = os.getenv("github_username_Ualers")
    repo_owner = os.getenv("companyname")

    name_agent, model_agent, instruction_original, tools_agent  = get_settings_agents(path_metadata = os.path.join(os.path.dirname(__file__), "metadata.json"))
    instruction_formatado = format_instruction(instruction_original, locals())

    Tools_Name_dict = Egetoolsv2(list(tools_agent))
    agent = Agent(
        name=name_agent,
        instructions = f"""
{RECOMMENDED_PROMPT_PREFIX}
{instruction_formatado}
        """
        ,
        model=str(model_agent),
        tools=Tools_Name_dict,
        handoffs=[handoff_obj_codeindexfrontEnd],

    )

    




# ### 
# Sprint 15 (Dia 1 – Passo 15)
# **Objetivo:** Integração do login com verificação de sessão  
# **Tarefas:**
# - Após login bem-sucedido, redirecionar o usuário para o painel (`/dashboard`)
# - Criar uma verificação no backend para garantir que o usuário está autenticado antes de acessar o painel
# - Armazenar a sessão em cookie ou localStorage
# **Critério de conclusão:** Navegação segura e funcional pós-login

# ---

# ### Sprint 16 (Dia 1 – Passo 16)
# **Objetivo:** Carregar dados do usuário logado no painel  
# **Tarefas:**
# - Buscar dados do usuário via `/api/user-info` baseado na sessão atual
# - Exibir nome, email e plano na dashboard
# - Exibir botão “logout” funcional
# **Critério de conclusão:** Painel personalizado com dados reais

# ---

# ### Sprint 18 (Dia 1 – Passo 18)
# **Objetivo:** Logout funcional e seguro  
# **Tarefas:**
# - Criar endpoint `/api/logout` que limpa sessão ou token
# - Botão “logout” no painel redireciona para `/login`
# **Critério de conclusão:** Sessão encerrada com redirecionamento seguro

# ---

# ### Sprint 19 (Dia 2 – Passo 19)
# **Objetivo:** Página “Minhas configurações”  
# **Tarefas:**
# - Criar rota `/settings` protegida por login
# - Permitir ao usuário alterar email e senha
# - Salvar alterações no Firebase
# **Critério de conclusão:** Dados persistidos e confirmados

# ---

# ### Sprint 20 (Dia 2 – Passo 20)
# **Objetivo:** Permitir alteração de plano no painel  
# **Tarefas:**
# - Mostrar plano atual com opção “mudar plano”
# - Botão leva ao checkout novamente (com novo plano)
# - Ao finalizar compra, atualizar plano no Firebase
# **Critério de conclusão:** Upgrade/downgrade funcional via painel

# ---

# ### Sprint 21 (Dia 2 – Passo 21)
# **Objetivo:** Bloqueio automático de funcionalidades se assinatura expirar  
# **Tarefas:**
# - Verificar `expiration` em cada rota protegida
# - Se data for menor que `hoje`, redirecionar para `/plan/premium/checkout`
# **Critério de conclusão:** Segurança da cobrança mantida

# ---

# ### Sprint 22 (Dia 2 – Passo 22)
# **Objetivo:** Painel com componente funcional principal do app (ex: IA, vídeo, análise, etc.)  
# **Tarefas:**
# - Criar interface da funcionalidade central do app
# - Conectar com API (mesmo que mock inicialmente)
# **Critério de conclusão:** Core feature com visual e entrada funcional

# ---

# ### Sprint 23 (Dia 2 – Passo 23)
# **Objetivo:** Conectar componente central com backend real  
# **Tarefas:**
# - Conectar botão/ação principal à API real
# - Mostrar resultado da funcionalidade em tempo real no painel
# **Critério de conclusão:** Primeira função real do app funcionando

# ---

# ### Sprint 24 (Dia 2 – Passo 24)
# **Objetivo:** Histórico de uso (mínimo viável)  
# **Tarefas:**
# - Registrar ações do usuário em `/api/history`
# - Criar página ou aba “Histórico” no painel
# **Critério de conclusão:** Ações recentes acessíveis pelo usuário

# ---

# ### Sprint 25 (Dia 2 – Passo 25)
# **Objetivo:** Compartilhamento de resultados (mínimo viável)  
# **Tarefas:**
# - Gerar link único (ou copiar conteúdo)
# - Permitir compartilhamento manual (copiar para área de transferência)
# **Critério de conclusão:** Link de resultado funcional

# ---










    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=doc_pre_project_Data,
    )
    return agent, handoff_obj