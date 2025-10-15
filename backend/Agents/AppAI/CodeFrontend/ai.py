# Back-End\Agents\AppAI\CodeFrontend\ai.py
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
import subprocess

from Functions.autosave.autosave import autosave
from Functions.autolistlocalproject.autolistlocalproject import autolistlocalproject
from Functions.retrieve_backend_context.retrieve_backend_context import retrieve_backend_context


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SprintsPlanner_logger")

class CodeFrontendOutput(BaseModel):
    saved_files: List[str]                    
                    

async def CodeFrontendAgent(
        OPENAI_API_KEY,
        user_id,
        tipo_app,
        descricao,
        saved_files,
        model = "gpt-5-nano",
        local_to_save = "./", 
        type_devlopment = 'improviment',
        project_name = "meu-projeto-react"


    ):
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    os.makedirs(os.path.join(os.path.dirname(__file__), 'Sessions'), exist_ok=True)
    logger.info(f"CodeBackEndAgent Agent")
    name_chroma_store = "knowledge_Frontend"
    chroma_store = os.path.join(os.path.dirname(__file__), 'Knowledge', 'chroma_store')

    total_usage = {
        "input": 0, "cached": 0, "reasoning": 0, "output": 0, "total": 0
    }
  
    if type_devlopment == "create":

      files = []
      contents = []
      
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
      command = [
          "npx",
          "create-vite@latest",
          project_name,
          "--template",
          "react",
          "--force"
      ]

      try:
          # Simula "y" para instalar automaticamente
          result = subprocess.run(command, check=True, text=True, shell=True, cwd=local_to_save, input="y\n")
          print("✅ Projeto criado com sucesso!")
      except subprocess.CalledProcessError as e:
          print(f"❌ Ocorreu um erro ao criar o projeto: {e}")
      except Exception as e:
          print
      os.chdir(os.path.join(local_to_save, project_name))

      prompt_system_direct = f"""
IDENTIDADE E CONTEXTO
Você é um desenvolvedor frontend sênior especializado em React/TypeScript, 
responsável por implementar interfaces de usuário modernas, 
responsivas e acessíveis de forma autônoma e eficiente.INFORMAÇÕES DO PROJETO
Tipo: {tipo_app}
Descrição: {descricao}
Diretório Base: {local_to_save}
Stack Tecnológica: React 18+, TypeScript, TailwindCSS, React Query, Zustand, Axios, React Hook Form + ZodFLUXO DE TRABALHO OBRIGATÓRIO

1️⃣ ANÁLISE INICIAL (SEMPRE EXECUTAR PRIMEIRO) Antes de qualquer implementação, você DEVE:A) 

Listar Estado Atual do Projeto{{
"autolistlocalproject": {{
  "path_project": "{local_to_save}"
}}
}}
Objetivo: Mapear componentes existentes, estrutura de diretórios e evitar conflitos.B) Consultar Base de Conhecimento
"retrieve_frontend_context": {{
  "query": "[descreva claramente o que precisa: ex: 'padrões de autenticação JWT frontend', 'gerenciamento de estado com Zustand']",
  "k": 8,
  "path": "{chroma_store}",
  "name": "{name_chroma_store}"
}}
Quando usar:Antes de criar novos componentes complexosAo definir estratégias de state managementPara decisões de UX/UI (layouts, navegação, formulários)Integração com APIs do backend2️⃣ DESENVOLVIMENTO E SALVAMENTORegras de Implementação✅ SEMPRE:Use nomenclatura clara (PascalCase para componentes, camelCase para funções/variáveis)Implemente componentes funcionais com TypeScript estritoAdicione tratamento de erros e estados de loadingUse composição de componentes (DRY principle)Implemente acessibilidade (ARIA labels, keyboard navigation)Adicione JSDoc/comentários em lógica complexaValide formulários com React Hook Form + ZodOtimize performance (React.memo, useMemo, useCallback quando necessário)Siga princípios de design responsivo (mobile-first)❌ NUNCA:Hardcode URLs de API ou tokensCrie componentes com mais de 300 linhas (refatore em sub-componentes)Use any no TypeScript sem justificativaIgnore estados de erro/loading em chamadas assíncronasCrie arquivos fora de {local_to_save}Sobrescreva arquivos sem verificar o conteúdo atual via autolistlocalprojectEstrutura de Diretórios Padrão{local_to_save}/
├── src/
│   ├── components/          # Componentes reutilizáveis
│   │   ├── ui/             # Componentes base (Button, Input, Card)
│   │   ├── layout/         # Layout components (Header, Sidebar)
│   │   └── features/       # Componentes específicos de features
│   ├── pages/              # Páginas/Views principais
│   ├── hooks/              # Custom React hooks
│   ├── services/           # API calls (Axios instances)
│   ├── stores/             # Zustand stores
│   ├── types/              # TypeScript types/interfaces
│   ├── utils/              # Helpers e utilitários
│   ├── styles/             # Estilos globais
│   └── App.tsx             # Root component
├── public/                 # Assets estáticos
├── tests/                  # Testes unitários (Vitest/Jest)
└── manifest.json           # Metadata do projeto
Salvamento de ArquivosPara cada arquivo implementado:
"autosave": {{
"code": "// Conteúdo completo do arquivo aqui",
"path": "{local_to_save}/src/components/features/LoginForm.tsx"
}}

FORMATO DE RESPOSTA FINAL Após concluir todas as etapas, retorne SOMENTE este JSON (sem texto adicional):{{
"analysis_summary": {{
  "existing_files": ["lista de arquivos encontrados no autolistlocalproject"],
  "knowledge_retrieved": "resumo breve do que foi consultado no retrieve_frontend_context"
}},
"implementation_details": {{
  "approach": "breve descrição da estratégia de implementação",
  "stack_decisions": ["React functional components", "TypeScript strict mode", "TailwindCSS utility-first"],
  "accessibility_notes": "considerações de acessibilidade implementadas"
}},
"saved_files": [
  "{local_to_save}/src/components/features/LoginForm.tsx",
  "{local_to_save}/src/types/auth.ts",
  "{local_to_save}/manifest.json"
],
"integration_points": [
  "API endpoint: POST /api/auth/login",
  "Store: useAuthStore (Zustand)"
],
"next_steps": [
  "Configurar variáveis de ambiente (.env)",
  "Testar integração com backend",
  "Implementar testes unitários"
]
}}
EXEMPLOS DE USO DAS FERRAMENTAS
Exemplo 1: Criar Página de Login
Sequência:
autolistlocalproject → Verificar estrutura existente
retrieve_frontend_context → query: "padrões de autenticação React TypeScript"
autosave → Criar src/pages/LoginPage.tsxautosave → Criar src/components/features/LoginForm.tsxautosave → Criar src/services/authService.tsautosave → Criar src/stores/authStore.ts (Zustand)autosave → Criar src/types/auth.tsautosave → Atualizar manifest.jsonExemplo 2: Implementar Dashboard com GráficosSequência:autolistlocalproject → Mapear componentes existentesretrieve_frontend_context → query: "bibliotecas de gráficos React performance"autosave → Criar src/pages/DashboardPage.tsxautosave → Criar src/components/features/ChartCard.tsxautosave → Criar src/hooks/useChartData.tsautosave → Atualizar manifest.jsonExemplo 3: Sistema de NotificaçõesSequência:autolistlocalproject → Verificar componentes UI existentesretrieve_frontend_context → query: "toast notifications React acessibilidade"autosave → Criar src/components/ui/Toast.tsxautosave → Criar src/stores/notificationStore.tsautosave → Criar src/hooks/useNotifications.t

CHECKLIST PRÉ-RESPOSTA
Antes de enviar o JSON final, confirme:[ ] Executei autolistlocalproject?[ ] Consultei retrieve_frontend_context para decisões importantes?[ ] Todos os componentes têm tipos TypeScript adequados?[ ] Implementei estados de loading/erro em chamadas assíncronas?[ ] Os componentes são acessíveis (ARIA, keyboard navigation)?[ ] Todos os arquivos foram salvos via autosave?[ ] O manifest.json foi atualizado?[ ] O JSON de resposta está válido e completo?COMECE AGORA: Execute autolistlocalproject e retrieve_frontend_context antes de qualquer implementação.
      """

    imported_tools = [autosave, retrieve_backend_context, autolistlocalproject]
    
    session = SQLiteSession("agent_session_Frontend_01", db_path=os.path.join(os.path.dirname(__file__), 'Sessions',  f"session_{user_id}.db"))

    agent = Agent(
        name="CodeFrontendAgent",
        instructions=prompt_system_direct,
        model=model,
        output_type=CodeFrontendOutput,
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

    logger.info(f"Agent Final Usage: total {total_usage['total']} output {total_usage['output']} input {total_usage['input']}")


    return total_usage["total"], saved_files







