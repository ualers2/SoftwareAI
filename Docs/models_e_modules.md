# Documentação Técnica — Models e Modules

> Documento gerado a partir dos arquivos fornecidos no diretório `Back-End`.

---

## Sumário

1. Models (MongoDB & PostgreSQL)
   - Visão geral
   - Modelos MongoDB
   - Modelos PostgreSQL (SQLAlchemy)
   - Exemplos JSON
   - Recomendações e índices

2. Modules (Geters, Resolvers, Savers, Updaters)
   - Arquitetura e responsabilidade
   - Geters
   - Resolvers
   - Savers
   - Updaters
   - Fluxos comuns e pontos de falha

3. Boas práticas e próximos passos

---

# 1. MODELS

### Visão geral
Os *models* representam duas camadas de persistência usadas pela aplicação:
- **MongoDB**: coleções para logs, trilhas de auditoria e registros de saúde do sistema (mais orientado a events/logs/telemetria).
- **PostgreSQL (SQLAlchemy)**: entidades relacionais para usuários, pull requests, deployments e configurações do sistema.


## 1.1 Modelos MongoDB (arquivo: `Modules/Models/MongoDB.py`)

### `Log` (coleção `logs`)
- **Campos principais**:
  - `timestamp` (datetime) — data UTC do evento
  - `action` (str) — nome da ação (e.g. `login_success`)
  - `details` (dict) — payload livre com informações/contexto
  - `user` / `user_id` (int|string) — referência ao usuário
  - `level` (str) — `INFO`, `WARNING`, `ERROR` etc.

- **Métodos utilitários**:
  - `create(action, details, user, level)` → insere e retorna `inserted_id`.
  - `find_all(limit)` → retorna lista ordenada por timestamp desc.
  - `find_by_user(user)` → retorna logs do usuário.

**Uso típico**: armazenar eventos de auditoria e operações internas que não exigem consistência relacional rígida.


### `AuditTrail` (coleção `audit_trail`)
- **Campos**:
  - `entity` (str) — nome da entidade auditada
  - `action` (str) — ação realizada (create/update/delete/…)
  - `user` — identificador do ator
  - `metadata` (dict) — dados adicionais
  - `timestamp` (datetime)

- **Métodos**:
  - `create(entity, action, user, metadata)` → insere e retorna `inserted_id`.
  - `find_by_entity(entity)` → retorna entradas por entidade ordenadas.

**Uso típico**: auditoria explícita para rastreabilidade de mudanças sensíveis.


## 1.2 Modelos PostgreSQL (arquivo: `Models/postgreSQL.py`)
> Usando SQLAlchemy (`db = SQLAlchemy()`)

### `User` (tabela `users`)
- **Campos**:
  - `id` (int, PK)
  - `user_id` (int, FK -> users.id?) — campo de relação ambígua no modelo atual (cuidado com recursividade)
  - `email` (str, unique)
  - `username` (str, unique, opcional)
  - `password_hash` (str)
  - `is_admin` (bool)
  - `created_at` (datetime)

- **Métodos**:
  - `set_password(password)` — cria `password_hash` via `bcrypt`
  - `check_password(password)` — valida senha

**Observações**: `user_id` como FK para `users.id` pode indicar um owner/manager; revisar se necessário para evitar loop.


### `PullRequest` (tabela `pull_requests`)
- **Campos**:
  - `id`, `user_id` (FK)
  - `author` (str)
  - `pr_number` (int, unique)
  - `title`, `body`, `ai_generated_content`, `original_diff` (text)
  - `status` (str) — `pending`, `processing`, `completed`, `error`
  - `diff_url` (str)
  - `created_at`, `updated_at`
  - `processed_by` (str)
  - `error_message` (str)

**Uso**: histórico dos PRs processados pelo agente; `pr_number` é chave única por repositório no código atual (mas repository não está no modelo — atenção se houver multi-repo).


### `Deployment` (tabela `deployments`)
- **Campos**: `id`, `user_id`, `status` (`pending`, `in_progress`, `completed`, `failed`), `triggered_by`, `source`, `created_at`, `completed_at`, `error_message`.

**Uso**: registrar tentativas de deploy e seu status.


### `SystemHealth` (tabela `system_health`)
- **Campos**: `id`, `user_id`, `postgres_status` (bool), `mongodb_status` (bool), `github_status`, `openai_status`, `last_check`.

**Uso**: armazenar checks de saúde periódicos; o código também registra um documento no Mongo (coleção `system_health`).


### `SystemSettings` (tabela `system_settings`)
- **Campos**: `id`, `user_id`, `github_token`, `github_secret`, `repository_name`, `openai_api_key`, `webhook_url`, `auto_process_prs`, `enable_logging`, `log_level`, `updated_at`.

**Uso**: configurações por usuário para integrações externas.


## 1.3 Exemplos JSON (respostas típicas)

**PullRequest (resumo)**
```json
{
  "id": 12,
  "number": 345,
  "title": "Corrige bug X",
  "status": "completed",
  "processedAt": "2025-09-24T12:00:00Z",
  "author": "autor",
  "aiGeneratedContent": "..."
}
```

**Log (documento Mongo)**
```json
{
  "timestamp": "2025-09-24T12:00:00Z",
  "action": "pr_process",
  "details": { "message": "Preview...", "pr_number": 345 },
  "user": 1,
  "level": "INFO"
}
```


## 1.4 Recomendações e índices
- Criar índice em `PullRequest.pr_number` e, idealmente, em combinação com `repository` (se multi-repo for necessário).
- Índices em `system_settings.user_id`, `system_health.user_id` e `deployments.user_id`.
- No Mongo: índice TTL para logs se for necessário expirar entradas; índices em `user_id` e `timestamp`.
- Rever FK `user_id` em User (possível campo redundante/confuso).

---

# 2. MODULES

### Visão geral
Os módulos seguem uma separação de responsabilidades:
- **Geters**: funções de leitura/consultas (Mongo e GitHub diffs)
- **Resolvers**: lógicas de resolução e processos de alto nível (processamento de PRs, verificação de assinatura, resolução de usuário)
- **Savers**: funções que persistem eventos de logs, auditorias, saúde no MongoDB
- **Updaters**: funções que atualizam recursos externos (GitHub PR body, merge)

Essa organização facilita testes unitários e substituição de implementações (ex.: substituir `requests` por client assíncrono).


## 2.1 GETERS
Arquivo(s): `Modules/Geters/logs.py`, `Modules/Geters/pr_diff.py`

### `get_recent_logs(user_id=None, limit=10)`
- Retorna lista de logs adaptados com `timestamp` ISO e `prNumber` normalizado.
- Filtra por `user_id` se fornecido.
- Erros comuns: import incorreto de `logs_collection` (checar path) ou documentos com timestamps não-datetime.

### `get_logs_by_user(user, limit=50)`
- Recupera logs diretamente por campo `user`.

### `get_audit_trail(entity=None, limit=50)`
- Recupera documentos da coleção `audit_trail`.

### `fetch_pr_diff_via_api(pr_api_url: str, token: str) -> str` (em `pr_diff.py`)
- Faz `GET` no endpoint de arquivos do PR (`/pulls/{num}/files`) e concatena `patch` para gerar um diff textual.
- Levanta exceções (`response.raise_for_status()`) em caso de erro HTTP.
- *Observação*: usa header `Authorization: token <token>` (GitHub).


## 2.2 RESOLVERS
Arquivos: `Modules/Resolvers/pr_process.py`, `user_identifier.py`, `verify_signature.py`

### `user_identifier.resolve_user_identifier(identifier)`
- Aceita id numérico, email (string com `@`) ou string representando id.
- Retorna instância `User` ou `None`.

### `verify_signature.verify_signature(GITHUB_SECRET, req)`
- Valida header `X-Hub-Signature-256` usando HMAC-SHA256.
- Retorna `True` se assinatura válida; registra warnings em casos de formato/algoritmo incorretos.

### `pr_process.process_pull_request(...)`
- Fluxo principal para processar PRs:
  1. Monta URLs do PR e files
  2. Chama `fetch_pr_diff_via_api` para obter diff
  3. Executa `PrGen(...)` (AI) para gerar título e conteúdo (via `asyncio.run`)
  4. Atualiza PR via `update_pr_body`
  5. Opcionalmente chama `merge_pull_request`
  6. Insere log no Mongo (`logs_collection.insert_one`) e cria registro em PostgreSQL (`PullRequest`)

- **Pontos críticos**:
  - Usa `asyncio.run(PrGen(...))` — cuidado com event loop já em execução (em servidores async isso pode quebrar).
  - Erros em chamada à GitHub API são capturados como `requests.exceptions.RequestException`.
  - Falta tratamento de transações/rollback para o caso de falha após inserir log.


## 2.3 SAVERS
Arquivos: `Modules/Savers/log_action.py`, `log_audit.py`, `log_system_health.py`

### `log_action(logs_collection, action, details=None, user=None, level='info')`
- Normaliza `details` (garante dict), adiciona `message` quando ausente, normaliza `user`/`user_id`, transforma `level` para uppercase.
- Insere documento em `logs_collection` e retorna `inserted_id`.
- Também printa um log via `logger.info` com timestamp e detalhes.

### `log_audit(entity, action, user=None, metadata=None)`
- Registra entrada na coleção `audit_trail`.

### `log_system_health(user_id, health_status: dict)`
- Persiste um documento estruturado em `system_health` no Mongo contendo flags e o `details`.


## 2.4 UPDATERS
Arquivos: `Modules/Updaters/pr_body.py`, `pr_merge.py`

### `update_pr_body(GITHUB_TOKEN, pr_api_url, title, new_body)`
- Faz `PATCH` no endpoint do PR para atualizar `title` e `body`. Levanta exceção em caso de erro HTTP.

### `merge_pull_request(GITHUB_TOKEN, repo_name, pr_number)`
- Faz `PUT` em `/pulls/{pr_number}/merge` com payload de merge.
- Loga sucesso ou falha; não lança exceção por padrão — retorna `None`.


## 2.5 Fluxos comuns e pontos de falha

- **Processamento de PR**: depende de rede (GitHub), do serviço AI (`Agents.PrSumary.ai.PrGen`) e da consistência do DB. Falhas em cada etapa precisam ser tratadas para evitar registros inconsistentes.
- **Assincronismo**: uso de `threading.Thread` no `app.py` + `asyncio.run` dentro de threads pode funcionar, mas há risco quando adaptado para servidores ASGI/uvicorn. Considere centralizar lógicas assíncronas e background workers (Celery, RQ).
- **Erros silenciosos**: alguns `except Exception` apenas logam e não propagam — isso dificulta rastreio e retry. Preferir logs com `level='error'` e retorno de erro padronizado quando aplicável.

---

# 3. BOAS PRÁTICAS E PRÓXIMOS PASSOS

1. **Documentar contratos de dados** (ex.: JSON schemas) para entradas/saídas dos endpoints e para documentos Mongo.
2. **Padronizar autenticação**: usar JWT retornado por `create_access_token` e header `Authorization: Bearer <token>` em todos os endpoints. Remover o uso de `password_hash` como token.
3. **Adicionar testes unitários** para:
   - `resolve_user_identifier` com múltiplos formatos
   - `fetch_pr_diff_via_api` (mockando requests)
   - `process_pull_request` (usar DB de teste e mocks para GitHub/AI)
4. **Adicionar índice nos campos mais consultados** (DB e Mongo) e revisar unicidade de `pr_number` em cenários multi-repositório.
5. **Substituir background threads por fila** (Celery/RQ) para jobs longos — facilita retries e observabilidade.
6. **Melhorar tratamento de erros** nos resolvers (`raise` quando necessário, ou retornar objeto erro padronizado) e adicionar métricas.
