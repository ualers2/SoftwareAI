Padrões de Contêineres (Front-End)
1. Padrões de Contêineres (Docker)

1.1. Dockerfile do Front-End (Vite/React)
ID: DEVOPS-DOCKER-FRONT
Palavras-Chave: dockerfile frontend react vite otimizacao
Regra: O Dockerfile do Front-End DEVE ser otimizado para a build estática do Vite, utilizando multi-stage build:

Stage 1 (Build): Usar uma imagem Node.js (ex: node:20-slim) para instalar dependências (npm install) e realizar a build (npm run build).

Stage 2 (Servidor): Usar uma imagem leve de servidor HTTP (ex: Nginx ou Caddy) para servir os arquivos estáticos gerados na etapa de build.

1.2. Docker Compose para Ambiente Local
ID: DEVOPS-COMPOSE-LOCAL
Palavras-Chave: docker-compose ambiente local frontend
Regra: O docker-compose.yml é o padrão para o desenvolvimento local. Ele DEVE orquestrar o serviço:

front: O contêiner Vite (Front-End).

Regra de Conexão: O Front-End DEVE usar o nome do serviço do Back-End definido no docker-compose (ex: http://web:8080/api) para a BASE_URL de desenvolvimento, e NUNCA localhost.