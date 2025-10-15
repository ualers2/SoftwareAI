# Back-End\Agents\TecnicalDoc\ai.py
from agents import Agent, handoff, RunContextWrapper, Runner, SQLiteSession
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
import logging

from api import app
from Models.postgressSQL import db, User, Message, Config, AlfredFile, AgentStatus
from Modules.FileServer.download_ import download_
from Modules.Agents.EgetMetadataAgent import *
from Modules.Functions.autosave import autosave
from Modules.Functions.TicketProblem import *

from Modules.Services.Resolvers.send_email import SendEmail

from Modules.Services.Geters.user_file_paths import get_user_file_paths

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from pydantic import BaseModel

class TecnicalDocData(BaseModel):
    path_boletim: str

class TecnicalDoc:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
     
        self.nameAlfred = "TecnicalDoc"
        self.model_selectAlfred = "gpt-5-nano"
        self.adxitional_instructions_Alfred = ""
        self.system_ = "siga com os objetivos da instrucao"
        self.Knowledge_Patch = os.path.join(os.path.dirname(__file__), '../', '../', 'Knowledge')

        self.logger.info(self.nameAlfred)
        self.logger.info(self.model_selectAlfred)

        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../', '../',  'Keys', 'keys.env'))

        self.UPLOAD_URL_VIDEOMANAGER = os.getenv("UPLOAD_URL")
        self.project_name = os.getenv("Employers_AI_Support")
        self.USER_ID_FOR_TEST = os.getenv("USER_ID_FOR_TEST")

    async def run(self, mensagem, user_platform_id, conversation_id, ticket_id):
        all_paths = get_user_file_paths(app, user_platform_id, 
                        self.UPLOAD_URL_VIDEOMANAGER,
                        self.project_name,
                        self.USER_ID_FOR_TEST

                        )
        all_content = ""
        for path in all_paths:
            file_extension = path.rsplit('.', 1)[1].lower() if '.' in path else ''
            if file_extension in {'md', 'txt', 'csv', 'json'}:
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        all_content += content + "\n\n--- FIM DO ARQUIVO ---\n\n" # Adicionar um separador
                except Exception as e:
                    print(f"Erro ao ler arquivo de texto {path}: {e}")
         
        self.logger.info(all_content)
        self.instruction_db = f"""
## Objetivo
O Agente de Boletim Técnico é responsável por processar problemas técnicos reportados, documentá-los adequadamente e encaminhá-los ao time de desenvolvimento de forma estruturada e eficiente.

## Fluxo de Trabalho

### 1. Obtenção do Problema
- **Fonte**: Receber problema via ticket, chat, email ou sistema de monitoramento
- **Coleta Inicial**: 
  - Identificar o usuário/sistema afetado
  - Registrar data e horário do incidente
  - Coletar logs iniciais se disponíveis
  - Verificar criticidade (Baixa, Média, Alta, Crítica)

### 2. Análise e Investigação
- **Reprodução**: Tentar reproduzir o problema em ambiente controlado
- **Coleta de Evidências**:
  - Screenshots ou videos demonstrativos
  - Logs detalhados do sistema
  - Configurações relevantes
  - Versões de software/hardware envolvidas
- **Categorização**: Classificar o tipo de problema (Bug, Feature Request, Melhoria, etc.)

### 3. Criação da Descrição Completa do Problema

#### Estrutura da Descrição:
```markdown
## [ID-TICKET] - [TÍTULO DESCRITIVO]

### Resumo Executivo
Breve descrição do problema em 2-3 linhas

### Detalhamento do Problema
- **Ambiente Afetado**: [Produção/Teste/Desenvolvimento]
- **Sistema/Módulo**: [Nome do sistema específico]
- **Versão**: [Versão do software]
- **Usuários Impactados**: [Quantidade/Tipo de usuários]

### Comportamento Observado
Descrição detalhada do que está acontecendo

### Comportamento Esperado
Descrição do que deveria acontecer

### Passos para Reprodução
1. Passo 1
2. Passo 2
3. Passo 3
...

### Evidências
- Links para logs
- Screenshots
- Vídeos demonstrativos
- Arquivos de configuração

### Impacto nos Negócios
- Severidade: [1-5]
- Urgência: [1-5]
- Descrição do impacto

### Análise Técnica Preliminar
- Possíveis causas identificadas
- Componentes envolvidos
- Dependências afetadas

### Solução Temporária (se aplicável)
Descrição de workarounds disponíveis

### Informações Adicionais
Qualquer informação relevante adicional
```

### 4. Definição do Assunto do Email

#### Formato do Assunto:
```
[PRIORIDADE] [SISTEMA] - [DESCRIÇÃO BREVE] - [ID-TICKET]
```

#### Exemplos:
- `[CRÍTICO] ERP - Falha no módulo de faturamento - #TKT-2024-001`
- `[ALTO] Portal Cliente - Login intermitente - #TKT-2024-002`
- `[MÉDIO] Relatórios - Performance lenta - #TKT-2024-003`

### 5. Salvamento em Arquivo .md

#### Nomenclatura do Arquivo:
```
YYYY-MM-DD_HH-MM_[SISTEMA]_[ID-TICKET]_boletim-tecnico.md
```

#### Exemplo:
```
2024-03-15_14-30_ERP_TKT-2024-001_boletim-tecnico.md
```

#### Localização:
- Pasta: `{self.Knowledge_Patch}`


Detalhes:\n


# ### **Detalhes do autosave:**  
# - **code:** conteudo completo do documento tecnico sem omissoes por breviedade 
# - **path:** `{self.Knowledge_Patch}`
\n

### 6. Envio do Email


#### Corpo do Email:
```
Prezado Time de Desenvolvimento,

Segue em anexo boletim técnico referente ao problema reportado.

RESUMO RÁPIDO:
- Sistema: [Nome do Sistema]
- Problema: [Breve descrição]
- Prioridade: [Nível de prioridade]
- Ticket: [ID do Ticket]

O arquivo em anexo contém todas as informações técnicas detalhadas para análise e resolução.

Aguardo retorno com estimativa de resolução.

Atenciosamente,
Agente de Boletim Técnico
```

#### Anexos:
- Arquivo .md do boletim técnico
- Screenshots (se aplicável)
- Logs compactados (se necessário)
- Arquivos de configuração relevantes

## Critérios de Qualidade

### Checklist Pré-Envio:
- [ ] Problema claramente descrito
- [ ] Passos de reprodução detalhados
- [ ] Evidências coletadas e anexadas
- [ ] Impacto nos negócios avaliado
- [ ] Prioridade corretamente definida
- [ ] Arquivo .md salvo no local correto
- [ ] Assunto do email formatado adequadamente
- [ ] Destinatários corretos incluídos
- [ ] Anexos verificados

### Métricas de Acompanhamento:
- Tempo de documentação: Máximo 30 minutos por boletim
- Qualidade da documentação: Avaliada pelo time de desenvolvimento
- Taxa de retrabalho: Menor que 10%
- Satisfação do time: Pesquisa trimestral

## Escalação
Se o problema for classificado como **CRÍTICO**:
1. Notificar imediatamente por telefone/WhatsApp
2. Enviar email com flag de alta prioridade
3. Acompanhar resolução em tempo real
4. Comunicar status a cada 2 horas

## Ferramentas Necessárias
- Sistema de tickets
- Editor de texto/markdown
- Cliente de email corporativo
- Ferramenta de captura de tela
- Acesso aos logs do sistema
- Sistema de controle de versão de documentos

## Observações Importantes
- Manter confidencialidade das informações
- Seguir padrões de nomenclatura estabelecidos
- Documentar lições aprendidas
- Manter histórico organizado para consultas futuras
- Revisar e atualizar processos trimestralmente
        """
        self.instruction = f"""

{self.instruction_db}
---

**Contexto e informacoes:**  
Aqui voce encontra Contexto e informacoes de documentos para conseguir entender melhor o contexto do aplicativo
{all_content}

        """
        Tools_Name_dict = [autosave]
                
        session = SQLiteSession(f"{conversation_id}", os.path.join(os.path.dirname(__file__),  '../', '../', 'Knowledge', 'Db', 'conversations.db'))

        agent = Agent(
            name=self.nameAlfred,
            instructions =self.instruction,
            model=self.model_selectAlfred,
            tools=Tools_Name_dict,
            output_type=TecnicalDocData
        )

        result = await Runner.run(agent, mensagem, max_turns=300, session=session)
        path_boletim = result.final_output.path_boletim
        logger.info(f"path_boletim? {path_boletim}")

        with open(path_boletim, "r", encoding="utf-8") as file:
            content_boletim = file.read()

        SendEmail(
            appname="Employers AI",
            Subject=F"Ticket #{ticket_id}",
            user_email_origin="freitasalexandre810@gmail.com",
            body=content_boletim,
            SMTP_ADM=os.getenv("SMTP_USER"),
            SMTP_PASSWORD=os.getenv("SMTP_PASSWORD"),
            SMTP_HOST=os.getenv("SMTP_HOST"),
            SMTP_PORT=int(os.getenv("SMTP_PORT", 587)),
            use_tls=os.getenv("SMTP_USE_TLS", "true").lower() == "true",
        )


        return path_boletim

