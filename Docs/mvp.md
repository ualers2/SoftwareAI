
Inicio - 20:05 04/07/2025
**Tempo Gasto Planejamento de requisitos :** 1 a 2,3 horas (04/07/2025 a noite)


subistitua o Firebase por os seguintes Databases

PostgreSQL: Dados estruturados 
MongoDB: Logs 

---

### [x]**Requisitos de Frontend com React para o Backend de IA**

Aqui estão os requisitos e as abordagens recomendadas para construir seu frontend usando React:

### **1. Estrutura e Ferramentas do Projeto**

* **Framework:** **React**.
* **Construção Rápida:** Utilize o **Vite** para iniciar o projeto. Ele oferece uma experiência de desenvolvimento extremamente rápida e otimizada.
    * **Comando Inicial:** `npm create vite@latest my-ai-frontend -- --template react-ts` (para TypeScript, recomendado para projetos maiores) ou `npm create vite@latest my-ai-frontend -- --template react` (para JavaScript).
* **Gerenciamento de Pacotes:** `npm` ou `yarn`.
* **Estilização:**
    * **Opção Simples:** CSS puro ou módulos CSS para escopo local.
    * **Opção Produtiva:** Um framework de UI como **Tailwind CSS** (para utilitários CSS) ou **Chakra UI / Material UI** (para componentes prontos e estilização rápida). Para um frontend simples, Tailwind CSS é uma ótima pedida por sua flexibilidade e leveza.
* **Roteamento:** **React Router DOM** para navegação entre as diferentes seções do seu aplicativo (ex: Monitoramento de PRs, Logs, Configurações).
* **Gerenciamento de Estado (Opcional para Início, mas útil):**
    * **Context API do React:** Suficiente para compartilhar estados entre componentes de forma simples no início.
    * **TanStack Query (React Query):** Excelente para gerenciar estados de dados assíncronos (dados do backend), caching e revalidação, simplificando muito a interação com a API.

### **2. Componentes e Funcionalidades Essenciais**

#### **2.1. Visualização e Monitoramento de PRs**

* **Página `Dashboard` ou `PRsView`:**
    * **Tabela/Lista de PRs Processados:** Exibir em formato de tabela as informações principais de cada PR.
        * **Colunas:** `Número do PR`, `Título`, `Status` (Ex: "Gerado", "Erro na IA", "Atualizado no GitHub"), `Data/Hora do Processamento`, `Link GitHub`.
        * **Integração Backend:** Um endpoint GET no seu Flask para `/api/processed-prs` que retorne uma lista JSON dos PRs processados (você precisará persistir esses dados, talvez em um DB simples ou em um arquivo JSON no backend).
    * **Componente `PRDetail`:** Ao clicar em um PR na lista, abrir uma visualização detalhada.
        * **Exibição de Diffs:** Mostrar o `diff_content` original. Considere usar uma biblioteca como `react-diff-viewer` (ou similar) para uma visualização amigável de diffs.
        * **Corpo do PR Gerado:** Exibir o `pr_content` gerado pela IA.
        * **Corpo Atual do PR (GitHub):** Uma chamada à API do GitHub (via seu backend) para obter o corpo atual do PR no GitHub para comparação.
        * **Logs Específicos:** Filtrar e exibir os logs relacionados àquele `pr_number` específico.

#### **2.2. Interação e Controle**

* **Página `Actions` ou `ControlsView`:**
    * **Botão "Re-processar PR":**
        * Um campo de entrada para o `Número do PR`.
        * Ao clicar, envia uma requisição POST para um novo endpoint no seu Flask (ex: `/api/reprocess-pr/<pr_number>`) que internamente chame `process_pull_request`.
        * **Feedback:** Mostrar feedback de carregamento e sucesso/erro.
    * **Botão "Forçar Deploy":**
        * Um botão simples que envia uma requisição POST para seu endpoint `/webhook` ou `/webhook/legacy`.
        * **Confirmação:** Um modal de confirmação antes de disparar, dada a criticidade da operação.
        * **Feedback:** Indicação de que o deploy foi iniciado.
* **Visualizador de Logs em Tempo Real (ou quase):**
    * **Página `LogsView`:** Um componente que faz requisições periódicas (long-polling ou WebSockets, se for avançar) para um endpoint no seu Flask (ex: `/api/logs`) que retorne os logs mais recentes.
    * **Funcionalidades:** `Auto-scroll`, `Filtro por nível` (INFO, ERROR), `Filtro por texto`.

#### **2.3. Gerenciamento de Configurações (Apenas para Administradores)**

* **Página `SettingsView`:**
    * **Formulários Seguros:** Campos para `GITHUB_TOKEN`, `repo_name`, `GITHUB_SECRET`.
        * **Não Exibir Secrets Completos:** Exiba apenas os primeiros/últimos caracteres de tokens e secrets.
        * **Atualização Via Backend:** As atualizações devem ser enviadas para um endpoint POST seguro no seu backend (ex: `/api/update-settings`) que sobrescreva as variáveis no `.env` ou em um DB.
        * **Recarregamento:** Recomendar reiniciar o backend após alterações críticas.

### **3. Requisitos de Segurança no Frontend**

* **Autenticação Simples:** Para o MVP, você pode usar uma autenticação de usuário/senha armazenada em uma variável de ambiente no backend.
    * **Fluxo:** Tela de login -> envia credenciais para um endpoint `/api/login` -> backend retorna um token (JWT) -> frontend armazena o token (local storage) -> envia o token em cada requisição autenticada no cabeçalho `Authorization: Bearer <token>`.
* **HTTPS:** Essencial em produção para proteger a comunicação entre frontend e backend.
* **Validação de Formulários:** Use bibliotecas como `Formik` ou `React Hook Form` com `Yup` para validação robusta de entradas.

### **4. Experiência do Usuário (UX)**

* **Componentes de UI:** Utilize bibliotecas como **Ant Design**, **Chakra UI** ou **Material UI** para componentes pré-construídos (botões, tabelas, modais, formulários) que garantam uma aparência limpa e profissional com pouco esforço.
* **Feedback Visual:** Utilize `loaders` para operações em andamento, mensagens de `toast` para sucesso e erro, e `modals` para confirmações críticas.

---

Ao seguir esses requisitos, você terá um frontend React que não só visualiza o que sua IA está fazendo, mas também oferece controle direto e valioso sobre as operações do seu backend, tudo de uma maneira segura e intuitiva.





















#













-----

Excelente\! Ter os mockups do frontend é um passo fundamental para visualizarmos as interações e, a partir delas, definir os requisitos do backend. Analisei seu componente `Controls.jsx` (ou `.tsx`) e identifiquei os seguintes endpoints e funcionalidades que seu backend Flask precisará fornecer, usando **Firebase Realtime Database** para persistência e **segurança como prioridade**.

-----

### **Requisitos de Backend Flask com Firebase Realtime DB para o Componente `Controls`**

Vamos detalhar cada endpoint, suas responsabilidades, e como o Firebase Realtime Database se encaixa.

### **1. Configuração Básica do Backend (Flask)**

  * **Firebase Admin SDK:**
      * **Instalação:** `pip install firebase-admin`
      * **Inicialização:** No seu `app.py` (ou onde sua aplicação Flask é inicializada), configure o Firebase SDK. Você precisará de uma **chave de conta de serviço (Service Account Key)** do Firebase.
        ```python
        import firebase_admin
        from firebase_admin import credentials, db
        import os

        # Certifique-se de que o caminho para sua chave de serviço esteja correto
        # Pode ser uma variável de ambiente ou um arquivo no sistema
        SERVICE_ACCOUNT_KEY_PATH = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY_PATH') 
        DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL') 

        cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
        firebase_admin.initialize_app(cred, {
            'databaseURL': DATABASE_URL
        })
        # Você pode obter uma referência ao DB root para usar em outras funções
        firebase_db_ref = db.reference('/') 
        ```
  * **CORS:** Habilite CORS para o domínio do seu frontend.
      * **Instalação:** `pip install flask-cors`
      * **Configuração:**
        ```python
        from flask_cors import CORS
        # ...
        app = Flask(__name__)
        CORS(app) # Permite todas as origens por padrão para desenvolvimento
        # Em produção, especifique as origens permitidas: CORS(app, resources={r"/api/*": {"origins": "https://seu-dominio-frontend.com"}})
        ```
  * **Autenticação JWT (JSON Web Token):**
      * Para proteger os endpoints da UI, você precisará de um sistema de autenticação.
      * **Instalação:** `pip install Flask-JWT-Extended`
      * **Endpoint de Login:** Um endpoint (`/api/login`) para receber credenciais e, se válidas, gerar um JWT.
      * **Decorador de Proteção:** Usar `@jwt_required()` nas rotas que precisam de autenticação.
      * **Tokens:** O frontend deve enviar este token no cabeçalho `Authorization: Bearer <token>`.

-----

### **2. Endpoints da API para o Componente `Controls`**

#### **2.1. Health Check do Sistema**

  * **Endpoint:** `GET /api/health`
  * **Função do Frontend:** `testSystemHealth()`
  * **Requisitos de Backend:**
      * **Autenticação:** Opcional, mas recomendado para evitar abusos.
      * **Lógica:**
          * Verificar a conexão com o Firebase Realtime Database.
          * Verificar se o `GITHUB_TOKEN` e o `GITHUB_SECRET` estão configurados (não necessariamente válidos no GitHub, mas presentes).
          * (Opcional) Tentar uma requisição simples à API do GitHub e OpenAI para verificar conectividade e credenciais.
          * (Opcional) Verificar o status de algum worker (e.g., Celery) se você tiver um.
      * **Resposta:** JSON com `status: "ok"` ou `status: "error"` e detalhes adicionais.
        ```json
        {
            "status": "ok",
            "firebase_connected": true,
            "github_token_configured": true,
            "openai_api_reachable": true,
            "message": "System is operating normally."
        }
        ```

#### **2.2. Reprocessar Pull Request**

  * **Endpoint:** `POST /api/reprocess-pr/<int:pr_number>`
  * **Função do Frontend:** `handleReprocessPR(prNumber)`
  * **Requisitos de Backend:**
      * **Autenticação:** **Obrigatório**. Apenas usuários autenticados devem poder disparar isso.
      * **Parâmetros:** Receber o `pr_number` na URL.
      * **Lógica:**
          * Buscar os dados necessários do PR no GitHub usando a API (e.g., `pulls/<pr_number>`). Isso incluirá o `diff_url`, `title`, `body`.
          * Reutilizar a lógica existente da sua função `process_pull_request` no `webhook.py`. Você pode refatorá-la para ser uma função interna que pode ser chamada tanto pelo webhook quanto por este novo endpoint.
          * A chamada deve ser **assíncrona/não bloqueante** (como você já está fazendo com `threading.Thread`) para evitar timeouts no frontend.
      * **Resposta:** JSON com `message: "Processing started"` e `pr_number`, status `202 Accepted`.

#### **2.3. Disparar Deploy Forçado**

  * **Endpoint:** `POST /api/force-deploy`
  * **Função do Frontend:** `handleForceDeploy()`
  * **Requisitos de Backend:**
      * **Autenticação:** **Obrigatório** e fortemente recomendado para administradores apenas.
      * **Lógica:**
          * Reutilizar a lógica da sua função `main()` ou `deploy_containers()` existente.
          * Similar ao reprocessamento de PR, a chamada deve ser **assíncrona/não bloqueante**.
          * **Não use o endpoint `/webhook` diretamente** para o deploy manual, pois ele espera a verificação de assinatura do GitHub. Crie um endpoint dedicado (`/api/force-deploy`) que chame sua lógica de deploy internamente.
      * **Corpo da Requisição (opcional):** O frontend envia um payload simples (`{ action: 'force_deploy', source: 'manual_trigger' }`). O backend pode usar isso para logs.
      * **Resposta:** JSON com `message: "Deploy initiated"`, status `202 Accepted`.

#### **2.4. Enviar Webhook Customizado**

  * **Endpoint:** `POST /api/send-custom-webhook` (ou `/webhook/custom` para diferenciar do GitHub)
  * **Função do Frontend:** `handleCustomWebhook()`
  * **Requisitos de Backend:**
      * **Autenticação:** **Obrigatório**.
      * **Corpo da Requisição:** Receber o payload JSON customizado diretamente do frontend.
      * **Lógica:**
          * Validar se o `payload` é um JSON válido.
          * Chamar a sua lógica principal de webhook (ex: `webhookgenpr` ou `webhook`) com este payload.
          * **Importante:** Este endpoint **NÃO** deve tentar verificar a assinatura `X-Hub-Signature-256`, pois o payload virá do seu frontend, não do GitHub. Se o seu `webhookgenpr` ou `webhook` requerem assinatura, você precisará de uma função interna separada que processe o payload sem a verificação, e que seja chamada tanto por este endpoint quanto pelo webhook do GitHub (após a verificação de assinatura).
      * **Resposta:** JSON com `message: "Webhook processed"` ou erro, status `200 OK` ou `400 Bad Request`.

#### **2.5. Monitoramento de Rate Limits**

  * **Endpoint:** `GET /api/rate-limits`
  * **Função do Frontend:** (Não está no código enviado, mas as "Quick Actions" o implicam).
  * **Requisitos de Backend:**
      * **Autenticação:** Recomendado.
      * **Lógica:** Fazer requisições à API do GitHub ([https://api.github.com/rate\_limit](https://www.google.com/search?q=https://api.github.com/rate_limit)) e à API da OpenAI (se disponível) para obter os dados de limite de taxa.
      * **Resposta:** JSON com os limites e usos atuais.
        ```json
        {
            "github": {
                "limit": 5000,
                "remaining": 4847,
                "reset": 1720233600 # Timestamp
            },
            "openai": {
                "limit": 1000,
                "remaining": 142,
                "reset": 1720233600
            }
        }
        ```

### **3. Persistência de Dados (Firebase Realtime Database)**

Para as "Quick Actions" e a visualização de histórico de PRs, você precisará persistir dados.

  * **Estrutura de Dados (Exemplo):**
    ```json
    {
      "processed_prs": {
        "pr_71": {
          "pr_number": 71,
          "title": "Implementação da Automação de PRs",
          "status": "success",
          "processed_at": "2025-07-04T21:58:09Z",
          "github_url": "https://github.com/SoftwareAI-Company/MediaCutsStudio/pull/71",
          "generated_body": "## Descrição...\n## Mudanças Principais...",
          "diff_content_summary": "resumo do diff (não armazene o diff completo se for muito grande)",
          "logs": {
            "log_id_1": { "timestamp": "...", "level": "INFO", "message": "..." },
            "log_id_2": { "timestamp": "...", "level": "ERROR", "message": "..." }
          }
        },
        "pr_72": { ... }
      },
      "system_events": {
        "deploy_123": {
          "type": "deploy",
          "initiated_by": "admin_user",
          "timestamp": "2025-07-04T22:05:00Z",
          "status": "success",
          "details": "Deploy completo da main."
        }
      },
      "settings": {
        "github_token": "ghp_...",
        "repo_name": "SoftwareAI-Company/MediaCutsStudio",
        "openai_model": "gpt-4.1-nano"
      }
    }
    ```
  * **Operações no Firebase:**
      * **Escrita:**
          * Quando um PR é processado (sucesso ou falha), salve os detalhes em `/processed_prs/pr_<number>`.
          * Quando um deploy é disparado, salve um registro em `/system_events`.
      * **Leitura:**
          * Endpoint `/api/processed-prs` (para a tela de histórico) leria de `/processed_prs`.
          * Endpoint `/api/system-status` (para o dashboard) leria de `/system_events` para o último deploy.
          * Endpoint `/api/settings` leria de `/settings` (para a tela de configurações).
      * **Atualização:** Endpoint `/api/update-settings` atualizará os nós em `/settings`.

### **4. Considerações de Segurança Adicionais no Backend**

  * **Variáveis de Ambiente:** Todos os tokens (GitHub, OpenAI, Firebase Service Account Key) e secrets devem ser carregados de variáveis de ambiente (`.env`) e **nunca** codificados diretamente.
  * **Validação de Entrada:** Sempre valide e sanitize as entradas recebidas do frontend (ex: `pr_number` deve ser um número inteiro, `customPayload` deve ser um JSON válido).
  * **Logs Detalhados:** Continue a usar o logger para registrar todas as ações, requisições recebidas e respostas do backend, especialmente para depuração e auditoria.

Com esses requisitos, você terá um backend robusto em Flask com Firebase Realtime Database para suportar as funcionalidades do seu componente `Controls` do seu frontend React.



-----

Perfeito\! Esse componente `Dashboard.tsx` (ou `.jsx`) nos dá uma visão clara das **estatísticas do sistema** e da **atividade recente**. Para preencher esses dados, seu backend Flask com Firebase Realtime Database precisará de alguns endpoints e uma estrutura de dados robusta.

-----




### **Requisitos de Backend Flask com Firebase Realtime DB para o Componente `Dashboard`**

Para suportar o `Dashboard` do frontend, o backend precisará expor dois endpoints principais, que buscarão e agregarão dados do Firebase.

### **1. Estrutura de Dados no Firebase Realtime Database**

Para o dashboard, precisamos de dados persistidos que reflitam o estado atual e o histórico do sistema. A estrutura no Firebase deve permitir consultas eficientes para as estatísticas e a atividade recente.

#### **1.1. Coleção `prs_data` (ou `processed_prs`)**

Essa coleção armazenará os dados detalhados de cada PR processado pela IA.

```json
{
  "prs_data": {
    "PR_1234": {
      "pr_number": 1234,
      "title": "Feature: Nova autenticação de usuário",
      "status": "success",          // "success", "error", "pending"
      "processed_at": "2025-07-04T10:30:00Z", // Timestamp ISO 8601
      "github_url": "https://github.com/org/repo/pull/1234",
      "generated_body": "## Descrição...\n## Mudanças Principais...",
      "ai_feedback": "A descrição gerada foi completa.", // Opcional: feedback da IA ou sistema
      "error_message": null,         // Preenchido se status for "error"
      "tokens_consumed": 41000       // Opcional: para métricas
    },
    "PR_1235": {
      "pr_number": 1235,
      "title": "Bugfix: Correção de validação de formulário",
      "status": "error",
      "processed_at": "2025-07-04T09:45:00Z",
      "github_url": "https://github.com/org/repo/pull/1235",
      "generated_body": null,
      "ai_feedback": null,
      "error_message": "Erro ao conectar com a API do GitHub para obter diff.",
      "tokens_consumed": 0
    },
    "PR_1236": {
      "pr_number": 1236,
      "title": "WIP: Melhoria de performance",
      "status": "pending",
      "processed_at": "2025-07-04T11:00:00Z",
      "github_url": "https://github.com/org/repo/pull/1236",
      "generated_body": null,
      "ai_feedback": null,
      "error_message": null,
      "tokens_consumed": 0
    }
  }
}
```

#### **1.2. Coleção `system_activity`**

Essa coleção registrará eventos gerais do sistema, como deploys, inicializações, e erros críticos que não estão diretamente ligados a um PR.

```json
{
  "system_activity": {
    "activity_1": {
      "id": "uuid_gerado_ou_timestamp",
      "type": "pr_processed", // "pr_processed", "deploy", "error", "system_start"
      "message": "PR #1234 processado com sucesso.",
      "timestamp": "2025-07-04T10:30:00Z",
      "status": "success", // "success", "error", "warning"
      "related_pr_number": 1234 // Opcional: para vincular a um PR
    },
    "activity_2": {
      "id": "uuid_gerado_ou_timestamp_2",
      "type": "deploy",
      "message": "Deploy iniciado via frontend.",
      "timestamp": "2025-07-04T10:20:00Z",
      "status": "success"
    },
    "activity_3": {
      "id": "uuid_gerado_ou_timestamp_3",
      "type": "error",
      "message": "Erro crítico no servidor: Firebase indisponível.",
      "timestamp": "2025-07-04T09:00:00Z",
      "status": "error"
    }
  }
}
```

### **2. Endpoints do Backend Flask**

Para o componente `Dashboard`, precisaremos de um endpoint que agregue os dados das duas coleções acima.

#### **2.1. Endpoint de Dashboard Data**

  * **Endpoint:** `GET /api/dashboard-data`
  * **Função do Frontend:** `fetchDashboardData()`
  * **Requisitos de Backend:**
      * **Autenticação:** **Obrigatório**. Somente usuários autenticados devem acessar as estatísticas do sistema.
      * **Lógica de Agregação:**
        1.  **Obter `SystemStats`:**
              * Leia todos os PRs de `/prs_data`.
              * **`totalPRs`**: Contagem total de entradas em `prs_data`.
              * **`successfulPRs`**: Contagem de PRs com `status: "success"`.
              * **`failedPRs`**: Contagem de PRs com `status: "error"`.
              * **`pendingPRs`**: Contagem de PRs com `status: "pending"` (ou PRs sem `generated_body` e sem `error_message` se você não tiver um status "pending" explícito).
              * **`uptime`**: Para simular o uptime, você precisará de uma forma de registrar o **início da aplicação Flask**.
                  * Ao iniciar o Flask, salve um timestamp (e.g., `system_start_time`) em uma variável global ou em uma entrada no Firebase (`/system_info/start_time`).
                  * No endpoint, calcule a diferença entre o tempo atual e `system_start_time` e formate-o como "Xd Yh Zm".
              * **`lastActivity`**: Leia a entrada mais recente de `/system_activity` e formate a diferença de tempo (ex: "2 minutos atrás").
        2.  **Obter `RecentActivity`:**
              * Leia as N (ex: 5-10) entradas mais recentes de `/system_activity`.
              * O Firebase permite ordenar e limitar consultas (`.order_by_child('timestamp').limit_to_last(N)`).
              * Mapeie os dados do Firebase para a estrutura `RecentActivity` esperada pelo frontend (`id`, `type`, `message`, `timestamp`, `status`). Certifique-se de que o `timestamp` seja formatado de forma amigável ou que o frontend possa formatá-lo.
      * **Resposta:** JSON contendo os dois objetos (`SystemStats` e `RecentActivity[]`).
        ```json
        {
            "stats": {
                "totalPRs": 45,
                "successfulPRs": 38,
                "failedPRs": 5,
                "pendingPRs": 2,
                "uptime": "2d 14h 32m",
                "lastActivity": "2 minutos atrás"
            },
            "recentActivity": [
                {
                    "id": "1",
                    "type": "pr_processed",
                    "message": "PR #1234 processado com sucesso",
                    "timestamp": "2 min atrás",
                    "status": "success"
                },
                {
                    "id": "2",
                    "type": "deploy",
                    "message": "Deploy realizado automaticamente",
                    "timestamp": "15 min atrás",
                    "status": "success"
                }
                // ... mais atividades
            ]
        }
        ```

### **3. Lógica de Persistência (Escrita no Firebase)**

Além dos endpoints de leitura, seu backend precisará **gravar dados no Firebase** sempre que um evento relevante ocorrer.

  * **Processamento de PR (`PrGen` e `webhookgenpr`):**
      * Sempre que um PR for processado (sucesso ou erro), o resultado deve ser salvo em `/prs_data/PR_<pr_number>`.
      * Também registre um evento correspondente em `/system_activity` (ex: `type: "pr_processed"`, `status: "success"/"error"`).
  * **Eventos de Deploy:**
      * Sempre que um deploy for iniciado (seja por webhook ou manualmente via `/api/force-deploy`), registre um evento em `/system_activity` (ex: `type: "deploy"`, `status: "success"` (inicialmente), `message: "Deploy iniciado"`).
      * Você pode adicionar um estágio "in\_progress" e depois "success" ou "error" para deploys mais complexos.
  * **Outros Erros Críticos:**
      * Qualquer erro significativo no backend (falha de conexão com a API do GitHub/OpenAI, erro de configuração) deve ser registrado em `/system_activity` com `type: "error"` e `status: "error"`.

### **4. Considerações de Implementação**

  * **Timestamps:** Salve todos os timestamps em formato **ISO 8601 (UTC)** no Firebase (e.g., `YYYY-MM-DDTHH:MM:SSZ`). O frontend pode então formatá-los para "X minutos atrás".
  * **`uptime`:** Para um uptime mais preciso, considere usar uma solução de monitoramento externa ou persistir o `system_start_time` no Firebase de forma robusta, talvez atualizando-o apenas no primeiro boot ou após um restart manual.
  * **Segurança (Regras do Firebase):** Defina **regras de segurança** no Firebase para proteger seus dados. Por exemplo, apenas seu backend (com a chave de serviço) deve ter permissão de escrita, e a leitura pode ser restrita a usuários autenticados.

Com esses requisitos, seu backend Flask estará apto a alimentar o `Dashboard` com dados precisos e atualizados, proporcionando uma visão abrangente do desempenho do seu sistema de IA.





-----

Ótimo\! O componente `Logs.tsx` é crucial para a depuração e monitoramento do sistema. Ele apresenta funcionalidades avançadas de filtragem, busca, auto-refresh e exportação, o que significa que o backend precisará ser bastante flexível no fornecimento de dados de log.

-----

### **Requisitos de Backend Flask com Firebase Realtime DB para o Componente `Logs`**

Para que o componente `Logs` funcione perfeitamente, o backend Flask precisará fornecer um endpoint de logs robusto, e a estrutura de dados no Firebase deve ser otimizada para consultas de logs.

### **1. Estrutura de Dados no Firebase Realtime Database**

A coleção `system_activity` que definimos para o Dashboard já é um bom começo. Para os logs, podemos aprimorá-la ou criar uma nova, `logs`, que seja mais granular. Dado o seu `LogEntry` interface, a coleção `logs` parece mais apropriada.

#### **1.1. Coleção `logs`**

Esta coleção armazenará todas as entradas de log geradas pela aplicação, permitindo consultas e filtragens.

```json
{
  "logs": {
    "log_uuid_1": {
      "timestamp": "2025-07-04T14:35:22Z", // Sempre ISO 8601 UTC
      "level": "INFO",                 // "INFO", "WARNING", "ERROR"
      "message": "PR #1234 processado com sucesso. Conteúdo gerado pela IA.",
      "source": "pr_processor",        // Módulo ou componente que gerou o log (e.g., "webhook_handler", "pr_processor", "github_api", "ai_service", "main")
      "prNumber": 1234                 // Opcional: Para logs relacionados a PRs específicos
    },
    "log_uuid_2": {
      "timestamp": "2025-07-04T14:34:15Z",
      "level": "INFO",
      "message": "Iniciando processamento do PR #1234",
      "source": "webhook_handler",
      "prNumber": 1234
    },
    // ... mais logs
    "log_uuid_n": {
      "timestamp": "2025-07-04T14:15:22Z",
      "level": "ERROR", 
      "message": "Falha na conexão com a OpenAI API: Request timeout",
      "source": "ai_service"
    }
  }
}
```

  * **Chaves dos Logs (`log_uuid_1`):** Use IDs únicos e ordenáveis. Firebase gera chaves automaticamente que são ordenáveis por tempo se você usar `push()`. Isso é ideal para logs, pois eles são naturalmente baseados em tempo.
  * **`timestamp`:** Essencial para ordenação e filtragem por data. Use o formato ISO 8601 e UTC.

### **2. Endpoints do Backend Flask**

#### **2.1. Endpoint para Buscar Logs**

  * **Endpoint:** `GET /api/logs`
  * **Função do Frontend:** `fetchLogs()`
  * **Requisitos de Backend:**
      * **Autenticação:** **Obrigatório**. Logs são informações sensíveis.
      * **Parâmetros de Consulta (Query Parameters):**
          * `level`: String opcional (e.g., "INFO", "WARNING", "ERROR", "all").
          * `searchTerm`: String opcional para busca de texto.
          * `limit`: Inteiro opcional para limitar o número de logs retornados (útil para performance, ex: `?limit=100`).
          * `start_at_timestamp`: String opcional (ISO 8601) para buscar logs a partir de um determinado timestamp (útil para auto-refresh e paginação).
      * **Lógica de Busca e Filtragem:**
        1.  **Conectividade Firebase:** Acesse a referência `db.reference('/logs')`.
        2.  **Ordenação:** Os logs devem ser retornados em ordem cronológica reversa (mais recentes primeiro). Use `.order_by_key().limit_to_last(limit)` para buscar os mais recentes (se as chaves forem timestamps ou geradas por `push()`).
        3.  **Filtragem por Nível:**
              * Se `level` for fornecido e não for "all", o backend precisará filtrar os logs após recebê-los do Firebase (Firebase Realtime DB não tem filtragem direta por campos arbitrários em consultas complexas sem indexação específica). Você pode usar `orderByChild('level')` se você tiver um índice para isso e o nível for o *único* filtro, mas para múltiplos filtros é melhor buscar e filtrar na aplicação Flask.
        4.  **Filtragem por Termo de Busca (`searchTerm`):**
              * Isso precisará ser feito **no backend Flask** após obter os logs do Firebase, pois o Firebase Realtime DB não suporta buscas de texto complexas dentro de strings. Itere sobre os logs e verifique se `message`, `source` ou `prNumber` (convertido para string) contêm o `searchTerm`.
        5.  **Limitação e Paginação:**
              * Use o `limit` para controlar o volume de dados. Para "auto-refresh", o frontend pode simplesmente buscar os X logs mais recentes. Para navegação de histórico, implemente um cursor baseado em `timestamp` ou `key`.
      * **Resposta:** JSON contendo uma lista de objetos `LogEntry`.
        ```json
        [
            {
                "id": "log_uuid_1",
                "timestamp": "2025-07-04T14:35:22Z",
                "level": "INFO",
                "message": "PR #1234 processado com sucesso. Conteúdo gerado pela IA.",
                "source": "pr_processor",
                "prNumber": 1234
            },
            // ... logs mais antigos
        ]
        ```

#### **2.2. Endpoint para Exportar Logs (Opcional, se o volume for grande)**

  * **Endpoint:** `GET /api/logs/export`
  * **Função do Frontend:** `exportLogs()`
  * **Requisitos de Backend:**
      * **Autenticação:** **Obrigatório**.
      * **Parâmetros de Consulta:** Os mesmos de `/api/logs` (`level`, `searchTerm`), mas provavelmente sem `limit` (ou com um limite muito alto) para exportar todos os logs relevantes.
      * **Lógica:**
          * Obtenha os logs do Firebase com base nos filtros.
          * Formate-os em um formato de texto plano ou CSV.
          * Retorne o conteúdo como um anexo de arquivo.
      * **Resposta:** Um arquivo de texto (`Content-Type: text/plain`) ou CSV (`Content-Type: text/csv`).

### **3. Lógica de Persistência (Escrita de Logs no Firebase)**

A parte mais importante para o funcionamento desta tela é garantir que *todos os eventos relevantes* na sua aplicação Flask sejam registrados no Firebase.

  * **Integração do Logger Flask com Firebase:**
      * A melhor abordagem é criar um **handler de logging customizado** no Flask que envie os logs para o Firebase Realtime Database.
      * Isso garante que cada `app.logger.info()`, `app.logger.error()`, etc., seja persistido.
      * **Exemplo Simplificado de um Handler:**
        ```python
        import logging
        from firebase_admin import db

        class FirebaseHandler(logging.Handler):
            def __init__(self, ref_path='/logs'):
                super().__init__()
                self.db_ref = db.reference(ref_path)

            def emit(self, record):
                try:
                    log_entry = {
                        "timestamp": self.format(record.created), # Converte timestamp para ISO
                        "level": record.levelname,
                        "message": self.format(record.msg, *record.args), # Formata a mensagem com args
                        "source": record.name, # Nome do logger (e.g., "PrGen_logger", "webhook_handler")
                        # Adicionar prNumber se puder ser inferido do contexto (ex: via extras no log)
                    }
                    if hasattr(record, 'prNumber') and record.prNumber is not None:
                        log_entry['prNumber'] = record.prNumber
                    
                    self.db_ref.push(log_entry) # Firebase gera uma chave única e ordenável
                except Exception as e:
                    print(f"Erro ao enviar log para o Firebase: {e}")

        # Configuração da aplicação Flask
        # ...
        from flask import Flask
        app = Flask(__name__)

        # Adicione o handler customizado ao logger da sua aplicação
        firebase_handler = FirebaseHandler()
        # Defina o formato para timestamps ISO 8601
        firebase_handler.setFormatter(logging.Formatter('%(asctime)sZ', '%Y-%m-%dT%H:%M:%S'))
        app.logger.addHandler(firebase_handler)
        app.logger.setLevel(logging.INFO) # Define o nível mínimo de logs a serem enviados
        ```
      * **Enriquecimento de Logs:** Para incluir `prNumber` nos logs, você precisará passar essa informação quando logar. Ex: `app.logger.info("Processando PR #%s", pr_number, extra={'prNumber': pr_number})`.

### **4. Considerações de Performance e Escalabilidade**

  * **Volume de Logs:** Se o volume de logs for muito alto, buscar todos os logs do Firebase a cada 5 segundos pode ser ineficiente.
      * **Paginação/Limitação:** O frontend já tem um `limit`, use-o no backend.
      * **Realtime Updates (Avançado):** Para "tempo real" verdadeiro, considere usar a funcionalidade de WebSockets (ex: Flask-SocketIO) e a capacidade de Realtime Updates do Firebase. O backend escutaria as mudanças no Firebase e enviaria apenas os novos logs para o frontend. Isso é mais complexo, mas muito eficiente.
  * **Indexação do Firebase:** Para buscas eficientes no Firebase (especialmente `orderByChild` e `equalTo`), você precisará configurar índices em seu `firebase.rules`. Para `timestamp` e `level`, isso pode ser útil.
    ```json
    {
      "rules": {
        "logs": {
          ".read": "auth != null", // Apenas usuários autenticados podem ler
          ".write": "auth.token.admin == true", // Apenas admins podem escrever (ou via service account)
          ".indexOn": ["timestamp", "level"] // Otimiza buscas por timestamp e nível
        }
      }
    }
    ```






-----

Fantástico\! O componente `PullRequests.tsx` é o coração da interface para monitorar o trabalho da sua IA. Ele oferece uma tabela interativa com funcionalidades de busca e visualização detalhada, o que exige um endpoint de backend bem estruturado para fornecer todos esses dados.

-----

### **Requisitos de Backend Flask com Firebase Realtime DB para o Componente `PullRequests`**

Para que o componente `PullRequests` liste, filtre e exiba detalhes dos PRs, seu backend Flask precisará de um endpoint que busque informações da sua base de dados do Firebase.

### **1. Estrutura de Dados no Firebase Realtime Database**

A coleção `prs_data` que definimos para o Dashboard já atende bem à interface `PullRequest` do frontend. Vamos revisitar a estrutura para garantir que todos os campos estejam presentes e sejam adequados para consulta.

#### **1.1. Coleção `prs_data` (Revisada)**

Essa coleção deve armazenar todos os dados detalhados de cada Pull Request processado pela IA.

```json
{
  "prs_data": {
    "PR_1234": { // Chave para cada PR, pode ser o número do PR ou um UUID
      "pr_number": 1234,         // int: Número do PR no GitHub
      "title": "Adicionar nova funcionalidade de autenticação", // string: Título do PR
      "status": "success",       // string: "success", "error", "pending"
      "processed_at": "2024-01-15T14:30:00Z", // string (ISO 8601 UTC): Data/hora do processamento
      "github_url": "https://github.com/user/repo/pull/1234", // string: URL do PR no GitHub
      "author": "developer1",    // string: Autor do PR no GitHub
      "ai_generated_content": "## Resumo...\nEste PR adiciona...", // string: Conteúdo gerado pela IA (Markdown)
      "original_diff": "diff --git a/auth.py b/auth.py\n+...", // string: O diff completo do PR
      "error_message": null,     // string | null: Mensagem de erro, se o status for "error"
      "webhook_id": "uuid_do_webhook", // Opcional: ID do webhook que disparou o processo
      "repo_full_name": "user/repo",   // Opcional: Nome completo do repositório
      "commits_sha": ["sha1", "sha2"]  // Opcional: SHAs dos commits envolvidos
    },
    "PR_1233": {
      "pr_number": 1233,
      "title": "Corrigir bug no sistema de logs",
      "status": "error",
      "processed_at": "2024-01-15T13:15:00Z",
      "github_url": "https://github.com/user/repo/pull/1233",
      "author": "developer2",
      "ai_generated_content": "",
      "original_diff": "diff --git a/logger.py b/logger.py\n-...",
      "error_message": "Token do GitHub inválido",
      "webhook_id": "uuid_do_webhook_2",
      "repo_full_name": "user/repo"
    }
  }
}
```

  * **`id` no frontend:** O `id` na sua interface `PullRequest` (ex: "1", "2") pode ser simplesmente a chave do Firebase para o PR (e.g., "PR\_1234"). Se você usar o `pr_number` como chave principal no Firebase (como no exemplo `PR_1234`), a recuperação é direta. Se você usar UUIDs aleatórios, precisará garantir que o `pr_number` esteja sempre presente no objeto.
  * **`processed_at`:** Mantenha no formato **ISO 8601 (UTC)**. O frontend pode convertê-lo para o formato local (`toLocaleString`).
  * **`ai_generated_content` e `original_diff`:** Estes campos podem ser grandes. O Firebase Realtime Database suporta strings grandes, mas esteja atento ao volume de dados transferido se você planeja carregar muitos PRs de uma vez.

### **2. Endpoints do Backend Flask**

Para o componente `PullRequests`, precisaremos de um endpoint que possa listar todos os PRs processados e, idealmente, um para buscar os detalhes de um único PR, caso o volume de dados seja grande.

#### **2.1. Endpoint para Listar Pull Requests**

  * **Endpoint:** `GET /api/pull-requests`
  * **Função do Frontend:** `fetchPRs()`
  * **Requisitos de Backend:**
      * **Autenticação:** **Obrigatório**. A lista de PRs e seus detalhes são informações sensíveis.

      * **Parâmetros de Consulta (Query Parameters):**

          * `searchTerm`: String opcional para buscar por `number`, `title` ou `author`.
          * `limit`: Inteiro opcional para limitar o número de PRs retornados (para paginação ou para carregar apenas os mais recentes).
          * `orderBy`: String opcional para ordenar os resultados (e.g., "processedAt", "pr\_number").
          * `orderDirection`: String opcional para a direção da ordenação ("asc" ou "desc").

      * **Lógica de Busca e Filtragem:**

        1.  **Conectividade Firebase:** Acesse a referência `db.reference('/prs_data')`.
        2.  **Ordenação:** Para carregar os mais recentes primeiro, use `.order_by_child('processed_at').limit_to_last(limit)`. Firebase retorna em ordem crescente por padrão para `limit_to_last`, então você pode precisar inverter a ordem no Flask.
        3.  **Filtragem por Termo de Busca (`searchTerm`):**
              * Como no caso dos logs, a busca por `title`, `author` ou `pr_number` (convertido para string) precisará ser feita **no backend Flask** após obter os dados do Firebase. O Firebase Realtime DB não oferece busca de texto completa em campos de string.
              * Recupere todos os PRs (ou um número limitado para pesquisa) e então filtre na aplicação Flask.
        4.  **Estrutura da Resposta:** Mapeie os dados do Firebase para a estrutura `PullRequest` esperada pelo frontend.

      * **Resposta:** JSON contendo uma lista de objetos `PullRequest`.

        ```json
        [
            {
                "id": "PR_1234",
                "number": 1234,
                "title": "Adicionar nova funcionalidade de autenticação",
                "status": "success",
                "processedAt": "2024-01-15T14:30:00Z",
                "githubUrl": "https://github.com/user/repo/pull/1234",
                "author": "developer1",
                "aiGeneratedContent": "## Resumo...\nEste PR adiciona uma nova funcionalidade de autenticação...",
                "originalDiff": "diff --git a/auth.py b/auth.py\n+def authenticate_user():...",
                "errorMessage": null
            },
            {
                "id": "PR_1233",
                "number": 1233,
                "title": "Corrigir bug no sistema de logs",
                "status": "error",
                "processedAt": "2024-01-15T13:15:00Z",
                "githubUrl": "https://github.com/user/repo/pull/1233",
                "author": "developer2",
                "aiGeneratedContent": "",
                "originalDiff": "diff --git a/logger.py b/logger.py\n-...",
                "errorMessage": "Token do GitHub inválido"
            }
        ]
        ```

#### **2.2. Endpoint para Buscar um Pull Request Específico (Opcional, mas recomendado para grandes `originalDiff`/`aiGeneratedContent`)**

Se `aiGeneratedContent` ou `originalDiff` forem muito grandes e você não quiser carregar todos eles na lista inicial, pode criar um endpoint para buscar um único PR.

  * **Endpoint:** `GET /api/pull-requests/<pr_id>` (onde `pr_id` é a chave do Firebase, e.g., "PR\_1234")
  * **Lógica de Frontend:** A `Dialog` no frontend precisaria chamar este endpoint quando `setSelectedPR` for acionado.
  * **Requisitos de Backend:**
      * **Autenticação:** **Obrigatório**.
      * **Lógica:**
        1.  Acesse a referência `db.reference(f'/prs_data/{pr_id}')`.
        2.  Recupere o objeto PR.
        3.  Retorne o objeto `PullRequest`.

### **3. Lógica de Persistência (Escrita no Firebase)**

A integração mais crítica aqui é o processo de **gravação dos dados do PR no Firebase** após a IA concluir seu trabalho. Isso deve ser feito pelos módulos do backend que orquestram o processamento do PR.

  * **No Módulo de Processamento de PR (e.g., `PrGen`):**
      * Após a IA gerar o conteúdo para o PR (ou falhar), o resultado completo deve ser salvo no Firebase.
      * Exemplo de como o backend pode persistir isso:
        ```python
        from firebase_admin import db
        import datetime

        def save_pr_data_to_firebase(pr_number, title, status, github_url, author, ai_content, original_diff, error_msg=None):
            pr_ref = db.reference(f'/prs_data/PR_{pr_number}')
            data = {
                "pr_number": pr_number,
                "title": title,
                "status": status,
                "processed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "github_url": github_url,
                "author": author,
                "ai_generated_content": ai_content,
                "original_diff": original_diff,
                "error_message": error_msg
            }
            pr_ref.set(data) # ou .update(data) se quiser atualizar parcialmente
            # Considere também registrar um log em /logs ou /system_activity aqui!
            print(f"Dados do PR #{pr_number} salvos no Firebase.")

        # Exemplo de uso após processamento bem-sucedido
        # save_pr_data_to_firebase(1234, "Adicionar auth", "success", "...", "dev1", "Conteúdo...", "Diff...")

        # Exemplo de uso após falha
        # save_pr_data_to_firebase(1233, "Corrigir bug", "error", "...", "dev2", "", "Diff...", "Token inválido")
        ```
  * **Gatilhos de Webhook:** O `webhookgenpr` será o principal ponto de entrada. Ele deve orquestrar a obtenção do diff, o envio para a IA e, finalmente, a persistência de *todos* os dados do PR (incluindo o diff original e o conteúdo gerado pela IA) no Firebase.

### **4. Considerações de Performance e Segurança**

  * **Indexação do Firebase:** Para buscas eficientes e ordenação por `processed_at`, `pr_number`, `status`, etc., você precisará configurar índices em seu `firebase.rules`:
    ```json
    {
      "rules": {
        "prs_data": {
          ".read": "auth != null",
          ".write": "auth.token.admin == true", // ou via service account
          ".indexOn": ["processed_at", "pr_number", "status", "author"]
        }
      }
    }
    ```
  * **Tamanho do Payload:** Se `ai_generated_content` e `original_diff` forem muito grandes, carregar todos eles para cada linha da tabela pode tornar a resposta lenta. Considere buscar apenas os campos `id`, `number`, `title`, `status`, `processedAt`, `githubUrl`, `author` para a tabela, e carregar `ai_generated_content` e `original_diff` separadamente na `Dialog` de detalhes (usando o endpoint `/api/pull-requests/<pr_id>` sugerido).
      * Se for seguir essa rota, o `fetchPRs` inicial buscaria apenas um subconjunto de campos, e a função `setSelectedPR` na verdade dispararia uma nova chamada ao backend para obter os detalhes completos do PR selecionado.
  * **Tratamento de Dados Sensíveis:** O `originalDiff` pode conter informações sensíveis do código. Garanta que apenas usuários autorizados possam acessá-lo.








-----

O componente `Settings.tsx` é a interface de configuração para o seu sistema de IA, permitindo que os administradores gerenciem parâmetros cruciais como credenciais de API, comportamento do processamento de PRs e configurações de logging. Isso exige um backend robusto para **armazenamento seguro**, **recuperação** e **atualização** dessas configurações.

-----

### **Requisitos de Backend Flask com Firebase Realtime DB para o Componente `Settings`**

Para suportar o componente `Settings`, o backend Flask precisará de funcionalidades para:

1.  **Armazenar e recuperar** as configurações do sistema de forma segura.
2.  **Atualizar** as configurações com base nas entradas do usuário.
3.  **Testar a conectividade** com serviços externos (GitHub e OpenAI) usando as credenciais fornecidas.

### **1. Estrutura de Dados no Firebase Realtime Database**

As configurações do sistema são geralmente únicas para a aplicação. Podemos armazená-las em um nó dedicado, por exemplo, `/system_settings`.

#### **1.1. Coleção/Nó `system_settings`**

Este nó armazenará um único objeto contendo todas as configurações da aplicação.

```json
{
  "system_settings": {
    "github_token": "ghp_full_token_string",
    "github_secret": "full_webhook_secret_string",
    "repository_name": "user/repo-name",
    "openai_api_key": "sk-full_openai_key_string",
    "webhook_url": "https://your-domain.com/api/webhook",
    "auto_process_prs": true,
    "enable_logging": true,
    "log_level": "INFO" // Ou "DEBUG", "WARNING", "ERROR"
  }
}
```

  * **Segurança:** É crucial que estes tokens e chaves **NÃO SEJAM ACESSÍVEIS DIRETAMENTE PELO CLIENTE (FRONTEND)**. O backend deve ser o único a ter acesso às chaves completas.
      * Quando o frontend solicita as configurações, o backend deve enviar apenas as versões mascaradas dos tokens, como você já implementou (`substring(0, 4)}...${data.githubToken.slice(-4)}`).
      * Quando o frontend envia configurações, se os campos de token contiverem a versão mascarada, o backend deve **ignorar a atualização** desses campos ou ter uma lógica para detectar se o usuário realmente digitou um novo token (ou seja, se a string não contém "...") antes de tentar atualizar. Caso contrário, o frontend deve enviar apenas os novos valores de token quando forem alterados, e não a string mascarada.

### **2. Endpoints do Backend Flask**

#### **2.1. Endpoint para Recuperar Configurações**

  * **Endpoint:** `GET /api/settings`
  * **Função do Frontend:** `fetchSettings()`
  * **Requisitos de Backend:**
      * **Autenticação:** **Obrigatório**. Apenas administradores devem ser capazes de ver as configurações.
      * **Lógica:**
        1.  Acesse a referência `db.reference('/system_settings')`.
        2.  Recupere o objeto de configurações.
        3.  Antes de enviar ao frontend, **mascare** os campos sensíveis (`githubToken`, `githubSecret`, `openaiApiKey`).
            ```python
            # Exemplo de mascaramento no Flask
            settings_data = db.reference('/system_settings').get()
            if settings_data:
                # Crie uma cópia para mascarar sem alterar os dados originais no DB
                display_settings = settings_data.copy() 
                for key in ['github_token', 'github_secret', 'openai_api_key']:
                    if key in display_settings and display_settings[key]:
                        token = display_settings[key]
                        display_settings[key] = f"{token[:4]}...{token[-4:]}"
                return jsonify(display_settings)
            return jsonify({}), 404
            ```
      * **Resposta:** JSON contendo as configurações, com tokens mascarados.

#### **2.2. Endpoint para Salvar/Atualizar Configurações**

  * **Endpoint:** `PUT /api/settings`
  * **Função do Frontend:** `saveSettings()`
  * **Requisitos de Backend:**
      * **Autenticação:** **Obrigatório**. Apenas administradores devem ser capazes de modificar as configurações.
      * **Corpo da Requisição:** O backend deve esperar um payload JSON que corresponda à interface `SystemSettings` (com as chaves convertidas para `snake_case` para Python, se necessário).
      * **Lógica:**
        1.  Obtenha os dados do corpo da requisição (`request.json`).
        2.  **Tratamento de Tokens Mascarados:** Antes de salvar, verifique se os campos de token (e.g., `githubToken`) contêm o padrão de mascaramento (`...`). Se contiverem, significa que o usuário não alterou o token, e você deve **manter o valor existente no banco de dados** para esse campo específico, em vez de salvar a string mascarada.
            ```python
            # Exemplo de lógica de salvamento
            new_settings_data = request.json
            current_settings = db.reference('/system_settings').get() or {}

            for key in ['github_token', 'github_secret', 'openai_api_key']:
                frontend_value = new_settings_data.get(key)
                # Se o valor do frontend está mascarado, não atualize o campo do DB
                if frontend_value and '...' in frontend_value:
                    new_settings_data[key] = current_settings.get(key) # Usa o valor do DB

            # Converte chaves de camelCase para snake_case se necessário
            db_data = {
                'github_token': new_settings_data.get('githubToken'),
                'github_secret': new_settings_data.get('githubSecret'),
                'repository_name': new_settings_data.get('repositoryName'),
                'openai_api_key': new_settings_data.get('openaiApiKey'),
                'webhook_url': new_settings_data.get('webhookUrl'),
                'auto_process_prs': new_settings_data.get('autoProcessPRs'),
                'enable_logging': new_settings_data.get('enableLogging'),
                'log_level': new_settings_data.get('logLevel')
            }
            db.reference('/system_settings').update(db_data)
            ```
        3.  **Validação:** Valide os dados recebidos (e.g., se `repositoryName` não está vazio, se `logLevel` é um valor válido).
        4.  **Persistência:** Atualize o nó `system_settings` no Firebase. Use `set()` se quiser sobrescrever tudo ou `update()` para atualizar campos específicos. `update()` é geralmente mais seguro.
      * **Resposta:** Um JSON de sucesso como `{"status": "success", "message": "Settings updated"}` com status `200 OK`.

#### **2.3. Endpoints para Testar Conexões**

  * **Endpoint:** `POST /api/test-connection/<service>` (onde `<service>` é `github` ou `openai`)
  * **Função do Frontend:** `testConnection("github")` ou `testConnection("openai")`
  * **Requisitos de Backend:**
      * **Autenticação:** **Obrigatório**.
      * **Lógica:**
        1.  Recupere as credenciais completas (`githubToken`, `openaiApiKey`) do Firebase (ou de variáveis de ambiente/configuração interna) – **NÃO USE as credenciais mascaradas recebidas do frontend**.
        2.  **Para GitHub:** Tente fazer uma requisição simples à API do GitHub (e.g., obter informações do usuário associado ao token, ou listar um repositório conhecido).
              * Você pode usar a biblioteca `PyGithub` (`github.Github(token)`) para isso.
              * Exemplo: `g = Github(github_token); g.get_user().login`
        3.  **Para OpenAI:** Tente fazer uma requisição simples à API da OpenAI (e.g., uma chamada de modelo de baixo custo como `gpt-3.5-turbo` com uma mensagem trivial).
              * Você pode usar a biblioteca `openai` (`openai.OpenAI(api_key=openai_api_key)`).
              * Exemplo: `client = OpenAI(api_key=openai_api_key); client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}])`
        4.  Capture quaisquer exceções (erros de autenticação, rede, etc.).
      * **Resposta:**
          * Sucesso: `{"status": "success", "message": "Connection OK"}` com status `200 OK`.
          * Falha: `{"status": "error", "message": "Detailed error description"}` com status `400 Bad Request` ou `500 Internal Server Error`, dependendo da natureza da falha.

### **3. Considerações Adicionais**

  * **Variáveis de Ambiente:** Para produção, **NÃO armazene tokens e chaves secretas diretamente no Firebase ou em arquivos de configuração**. Use **variáveis de ambiente** ou um serviço de gerenciamento de segredos (como Google Secret Manager, AWS Secrets Manager, etc.). O Firebase Realtime DB pode ser usado para armazenar configurações *não sensíveis* ou apenas referências aos segredos. Se você persistir no Firebase, garanta que suas regras de segurança (`firebase.rules`) sejam extremamente restritivas para `/system_settings`.
    ```json
    {
      "rules": {
        "system_settings": {
          ".read": "auth.token.admin == true", // Apenas admins podem ler
          ".write": "auth.token.admin == true" // Apenas admins podem escrever
        }
      }
    }
    ```
  * **Reinicialização do Sistema:** Como o frontend menciona que algumas mudanças "requerem reinicialização do sistema", seu backend Flask precisará de um mecanismo para que essas configurações sejam recarregadas dinamicamente ou para que o processo seja reiniciado (o que é mais complexo e geralmente feito por fora da aplicação, via um orquestrador como `systemd`, Docker Compose, Kubernetes, etc.).
      * Para **`logLevel`** e **`enableLogging`**, o Python `logging` module pode ter seu nível alterado em tempo de execução.
      * Para **tokens de API** e **nomes de repositórios**, a aplicação precisaria recarregar esses valores em tempo de execução ou ser reiniciada.
