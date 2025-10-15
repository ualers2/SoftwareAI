2. Padrões de Integração Contínua (CI/CD)
2.1. Arquivo de Deploy (deploy.yml)
ID: DEVOPS-CI-DEPLOY
Palavras-Chave: ci/cd github actions deploy.yml
Regra: O pipeline de CI/CD (localizado em .github/workflows/deploy.yml) DEVE ter, no mínimo, as seguintes etapas antes de qualquer deploy:

Build do Back-End: Instalar dependências e garantir que o Dockerfile possa ser construído.

Testes: Executar os testes unitários (TEST-PY-TOOL) na camada de Resolvers e Geters/Savers.

Lint/Formatação: Garantir que o código siga os padrões de formatação (ex: black para Python).

2.2. Migrações de Banco de Dados
ID: DEVOPS-DB-MIGRATIONS
Palavras-Chave: migracao banco dados flask alembic flyway
Regra: Toda alteração no Models/postgreSQL/ DEVE ser acompanhada de um script de migração (ex: usando Alembic para Flask-SQLAlchemy).
Requisito de CI/CD: O pipeline DEVE rodar as migrações automaticamente ANTES de iniciar a nova versão do Back-End. NUNCA permitir que juniores alterem o banco de dados de produção manualmente.