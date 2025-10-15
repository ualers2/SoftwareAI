### 🧠 Diretrizes de tecnologia:
**Banco de dados:** PostgreSQL para dados, MongoDB Para logs
**Back End:** Flask + blueprint para api
**Front End:** Vite + React
**Filas e Agendamentos:** Celery + Redis
**Autenticação/Autorização:** Funcao propria do sistema que verifica se o usuario esta registrado no sistema, nao há necessidade de jwt
**Pagamentos:** Stripe (planos, subscriptions, webhooks)
**Observabilidade:** logs MongoDB centralizados, deploy com CI/CD via Git Actions
