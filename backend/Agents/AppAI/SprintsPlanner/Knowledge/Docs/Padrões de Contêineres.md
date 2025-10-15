1. Padrões de Contêineres (Docker)

1.1. Dockerfile do Back-End (Flask)

ID: DEVOPS-DOCKER-BACK
Palavras-Chave: dockerfile backend flask python otimizacao
Regra: O Dockerfile do Back-End DEVE ser otimizado para o Python, utilizando multi-stage build (se possível) ou, no mínimo, um .dockerignore para excluir arquivos desnecessários (.git, __pycache__).

Etapas Cruciais:

Começar de uma imagem oficial de Python (ex: python:3.11-slim-buster).

Copiar requirements.txt e instalá-los antes de copiar o código-fonte (para aproveitar o cache do Docker).

Definir o ENTRYPOINT para executar o api.py ou um script de inicialização.

1.2. Docker Compose para Ambiente Local

ID: DEVOPS-COMPOSE-LOCAL
Palavras-Chave: docker-compose ambiente local postgres mongodb
Regra: O docker-compose.yml é o padrão para o desenvolvimento local. Ele DEVE orquestrar no mínimo três serviços:

web: O contêiner Flask (Back-End).

db: O contêiner PostgreSQL.

mongo: O contêiner MongoDB.

front: O contêiner Front-End (React/Vite) para simular o ambiente de produção.

Regra de Conexão: O Back-End DEVE usar os nomes dos serviços definidos no docker-compose (ex: postgres://user:pass@db:5432/app) e NUNCA localhost.