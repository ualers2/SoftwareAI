# Documentação da API — Backend Flask

> Versão: baseada no arquivo `app.py` fornecido

---

## Sumário

1. Visão geral
2. Autenticação
3. Parâmetros comuns
4. Endpoints
   - `/` (GET)
   - `/api/login` (POST)
   - `/api/register` (POST)
   - `/api/health` (GET)
   - `/api/rate-limits` (GET)
   - `/api/settings` (GET, PUT)
   - `/api/test-connection/<service>` (POST)
   - `/api/logs` (GET)
   - `/api/logs/export` (GET)
   - `/api/pull-requests` (GET)
   - `/api/pull-requests/<pr_id>` (GET)
   - `/api/dashboard-data` (GET)
   - `/api/reprocess-pr/<pr_number>` (POST)
   - `/api/prai/gen` (POST)
   - `/api/force-deploy` (POST)
   - `/api/send-custom-webhook` (POST)
   - `/api/deployments` (GET)
5. Comportamentos assíncronos / background tasks
6. Modelos de dados / Respostas comuns
7. Logging e auditoria
8. Boas práticas para integração frontend
9. Exemplos de `curl`
10. Próximos passos sugeridos

---

## 1. Visão geral

API construída com Flask que integra PostgreSQL (SQLAlchemy) e MongoDB para logs. Fornece endpoints para autenticação, configuração de integrações (GitHub/OpenAI), health checks, listagem e reprocessamento de pull requests, deploys e logs.

> Observação: o código atual aceita `user_id` como query param ou no corpo JSON para a maioria dos endpoints — a autenticação JWT existe (Flask-JWT-Extended) mas muitos endpoints continuam dependendo do `user_id` passado explícita e/ou da função `resolve_user_identifier`.

---

## 2. Autenticação

- O projeto registra `JWTManager(app)`. Alguns endpoints usam `get_jwt_identity()` (ex.: `/api/force-deploy`, `/api/send-custom-webhook`) mas a maior parte dos endpoints continua exigindo `user_id` como query param ou dentro do JSON.
- **Header usado em alguns pontos:** Para _prai/gen_ o código busca `GitToken` no header `Bearer` (não é o padrão Authorization: Bearer ...).

**Nota importante:** o endpoint `/api/login` no código devolve o `access_token` como `user.password_hash` em vez de um JWT criado por `create_access_token`. Recomenda-se revisar isso por questões de segurança. A documentação abaixo descreve o comportamento atual e sugere remoção/ajuste.

---

## 3. Parâmetros comuns

- `user_id` — obrigatório na maioria dos endpoints. Pode ser enviado via query string (`?user_id=...`) ou no corpo JSON (`{ "user_id": ... }`). A função `resolve_user_identifier` é usada para transformar identificadores (email, id) no modelo `User` da aplicação.
- `limit`, `page`, `per_page` — usados para paginação (quando aplicável).
- `searchTerm` — parâmetro opcional para busca textual em endpoints como `/api/pull-requests` e `/api/logs`.

Cabeçalhos relevantes:
- `Content-Type: application/json`
- `Authorization: Bearer <JWT>` — usado em endpoints onde `get_jwt_identity()` é utilizado (sugestão: padronizar).
- `Bearer: <GitToken>` — header não padrão usado em `/api/prai/gen` (recomendado mover para `Authorization`).

---

## 4. Endpoints

> Abaixo cada endpoint com descrição, parâmetros, exemplos e status codes esperados.

### `GET /`
Retorna meta-informações básicas da API.

**Resposta 200**
```json
{
  "message": "Backend Flask - API Principal",
  "version": "2.0",
  "database": "PostgreSQL + MongoDB",
  "status": "running"
}
```

---

### `POST /api/login`
Autenticação do usuário.

**Payload** (JSON):
```json
{ "email": "usuario@example.com", "password": "senha" }
```

**Comportamento atual:**
- Resolve o usuário com `resolve_user_identifier`.
- Verifica senha com `user.check_password(password)`.
- Atualiza `user.last_seen` e grava log de ação.
- **Retorna `access_token` contendo `user.password_hash` (isso é um comportamento inseguro e não-padrão).**

**Respostas**:
- `200` — login bem-sucedido: `{"message": "Bem-vindo, ...", "access_token": "...", "user_id": <id>}`
- `401` — credenciais inválidas
- `404` — usuário não encontrado
- `200` (no exceção) — retorna mensagem de erro genérica no código atual (recomenda-se ajustar para `500`)

---

### `POST /api/register`
Cria um novo usuário.

**Payload**:
```json
{ "email": "novo@exemplo.com", "password": "senha" }
```

**Respostas**:
- `201` — criado com sucesso: `{"message": "Usuário criado com sucesso", "user_id": ...}`
- `400` — email ou senha ausente / usuário já existe
- `500` — erro interno ao salvar

---

### `GET /api/health`
Verifica saúde do sistema (Postgres, MongoDB, GitHub/OpenAI se tokens configurados). Requer `user_id`.

**Query / Body**: `user_id` (requerido)

**Resposta** (exemplo):
```json
{
  "status": "ok",
  "timestamp": "2025-09-24T12:00:00Z",
  "postgres_connected": true,
  "mongodb_connected": true,
  "github_token_configured": true,
  "openai_token_configured": false,
  "github_api_reachable": true,
  "openai_api_reachable": false
}
```

**Códigos**: `200` (ok) ou `503` quando `status` != 'ok'.

---

### `GET /api/rate-limits`
Retorna limites (rate limits) para GitHub/OpenAI se tokens disponíveis. Requer `user_id`.

**Resposta**: JSON com blocos `github` e `openai` e `timestamp`.

---

### `GET /api/settings`
Recupera configurações do sistema (valores mascarados no retorno). Requer `user_id`.

**Resposta**:
```json
{
  "githubToken": "<masked>",
  "githubSecret": "<masked>",
  "repositoryName": "meu/repo",
  "openaiApiKey": "<masked>",
  "webhookUrl": "https://...",
  "autoProcessPRs": true,
  "enableLogging": true,
  "logLevel": "INFO"
}
```

---

### `PUT /api/settings`
Atualiza as configurações do sistema. Requer `user_id`.

**Payload**: qualquer combinação dos campos apresentados em GET `/api/settings`.

**Respostas**:
- `200` sucesso
- `400` payload ausente
- `500` erro interno

---

### `POST /api/test-connection/<service>`
Testa conexão com serviços externos: `github` ou `openai`. Requer `user_id`.

- `service=github` → usa `settings.github_token` e faz `GET https://api.github.com/user`.
- `service=openai` → usa `settings.openai_api_key` e faz `GET https://api.openai.com/v1/models`.

**Respostas**: `200` sucesso, `400` se token não configurado ou erro da API, `500` erro de requisição.

---

### `GET /api/logs`
Lista logs do usuário a partir do MongoDB.

**Query params**:
- `user_id` (requerido)
- `level` (opcional, ex: `INFO`, `ERROR`, `all`)
- `searchTerm` (opcional)
- `limit` (opcional, default `200`)

**Retorno**: array de objetos de log adaptados com campos `id`, `timestamp`, `level`, `action`, `details`, `prNumber`, `user`, `user_id`.

---

### `GET /api/logs/export`
Exporta logs filtrados em `.txt`. Requer `user_id`.

**Query params**: `user_id`, `level`, `searchTerm`.

**Resposta**: `text/plain` com `Content-Disposition: attachment; filename=logs-{user_id}.txt`.

---

### `GET /api/pull-requests`
Lista PRs processados.

**Query params**:
- `user_id` (requerido)
- `searchTerm` (opcional)
- `limit` (opcional, default 50)
- `page` (opcional, default 1)

**Retorno**: lista paginada de PRs com campos como `id`, `number`, `title`, `status`, `processedAt`, `githubUrl`, `author`, `aiGeneratedContent`, `originalDiff`, `errorMessage`.

---

### `GET /api/pull-requests/<pr_id>`
Detalhes de um PR específico. Requer `user_id`.

**Retorno**: objeto com informações detalhadas e tentativa de buscar dados no GitHub se `GITHUB_TOKEN` estiver configurado.

---

### `GET /api/dashboard-data`
Agrupa dados para o dashboard (estatísticas de PRs, uptime, últimas atividades). Requer `user_id`.

**Retorno**: objeto com `stats` (totalPRs, successfulPRs, failedPRs, pendingPRs, uptime, lastActivity) e `recentActivity` (lista).

---

### `POST /api/reprocess-pr/<int:pr_number>`
Inicia reprocessamento de um PR. Requer `user_id`.

**Comportamento**: dispara `process_pull_request` em uma thread separada e retorna `202 Accepted` com `message: Processing started`.

**Observações**:
- O processo roda em background; não há espera pela conclusão.
- Parâmetros adicionais: `redo_merge` (query param).

---

### `POST /api/prai/gen`
Dispara processamento de PR via endpoint público.

**Cabeçalho**: `Bearer: <GitToken>` (não padrão)
**Payload**:
```json
{ "repository": "meu/repo", "pr_number": 123 }
```

**Comportamento**: inicia `process_pull_request` em thread e retorna texto `Processamento do Pull Request iniciado` com código `202`.

---

### `POST /api/force-deploy`
Dispara deploy forçado. Usa `get_jwt_identity()` para identificar usuário (espera JWT).

**Payload**:
```json
{ "source": "manual_trigger" }
```

**Comportamento**: inicia `deploy_containers_internal` em thread e retorna `202` com dados do disparador.

---

### `POST /api/send-custom-webhook`
Recebe um payload JSON e processa em background (thread) via `process_webhook_internal`.

**Retorno**: `200` com mensagem `Webhook processed` se payload válido.

---

### `GET /api/deployments`
Lista registros de deploys (model `Deployment`). Paginação via `page` e `per_page`.

**Retorno**: objeto com `deployments` (lista) e `pagination`.

---

## 5. Comportamentos assíncronos / background tasks

Vários endpoints disparam ações em threads Python (`threading.Thread(...).start()`) e retornam `202` imediatamente. Isto inclui:
- `/api/reprocess-pr/<pr_number>`
- `/api/prai/gen`
- `/api/force-deploy`
- `/api/send-custom-webhook`

**Recomendações**:
- Considerar mover para um worker (Celery / RQ / Background Tasks) para melhor observabilidade, retries e resiliência.
- Registrar um `deployment_id` / `process_id` retornado ao cliente para consultar status posteriormente.

---

## 6. Modelos de dados / Respostas comuns

### Log (retorno adaptado)
```json
{
  "id": "<mongo_id>",
  "timestamp": "2025-09-24T12:00:00Z",
  "level": "INFO",
  "action": "prs_listed",
  "details": { "message": "..." },
  "prNumber": 123,
  "user": 1,
  "user_id": 1
}
```

### PullRequest (resposta resumida)
```json
{
  "id": "<id>",
  "number": 12,
  "title": "Corrige bug X",
  "status": "completed",
  "processedAt": "2025-09-24T12:00:00Z",
  "githubUrl": "https://github.com/meu/repo/pull/12",
  "author": "autor",
  "aiGeneratedContent": "...",
  "originalDiff": "...",
  "errorMessage": null
}
```

---

## 7. Logging e auditoria

- A aplicação registra ações com `log_action(logs_collection, action, details, user=...)` e salva registros em MongoDB (`logs_collection`).
- Eventos importantes listados no código: `login_success`, `login_failed`, `settings_updated`, `prs_listed`, `health_check`, `rate_limits_checked`, etc.

---

## 8. Boas práticas para integração frontend

- Padronizar autenticação: usar `Authorization: Bearer <JWT>` e modificar `/api/login` para gerar um JWT real com `create_access_token()`.
- Evitar envio de `password_hash` como token.
- Criar endpoint que retorne `process_id` ao disparar trabalhos em background para consultar status.
- Padronizar header `Authorization` para `prai/gen` em vez de `Bearer` no topo.
- Tratar erros HTTP corretamente (`500` para erros internos em vez de `200` com mensagem de erro).

---

## 9. Exemplos `curl`

**Login**
```bash
curl -X POST https://api.seudominio.com/api/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","password":"senha"}'
```

**Checar health**
```bash
curl "https://api.seudominio.com/api/health?user_id=1"
```

**Listar PRs**
```bash
curl "https://api.seudominio.com/api/pull-requests?user_id=1&limit=20&page=1"
```

**Reprocessar PR (inicia background)**
```bash
curl -X POST "https://api.seudominio.com/api/reprocess-pr/123?user_id=1"
```

---

## 10. Próximos passos sugeridos

1. Corrigir `/api/login` para retornar JWT real com `create_access_token()` e usar `JWTManager` consistentemente.
2. Padronizar header `Authorization` e remover uso de `Bearer` custom.
3. Substituir `threading.Thread` por um sistema de filas (Celery/RQ) para jobs longos.
4. Adicionar endpoints de status para jobs em background (`/api/jobs/<id>`).
5. Gerar especificação OpenAPI / Swagger (posso gerar já um `openapi.yaml` a partir deste código).

---

**Se quiser, eu gero automaticamente:**
- um arquivo OpenAPI (YAML) inicial; ou
- uma collection do Postman; ou
- exemplos TypeScript/React para consumo desses endpoints.

