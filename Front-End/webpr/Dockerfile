## Dockerfile otimizado apenas para o serviço de landingpage

# Use uma imagem Node.js leve
FROM node:22-slim

# Diretório de trabalho
WORKDIR /app

# Copia apenas dependências para cache de camadas
COPY ./package*.json ./

# 4. Assegura que as devDependencies (incluindo o vite) sejam instaladas
#    Se seu build estiver setando NODE_ENV=production em algum lugar, force o dev:
ENV NODE_ENV=development
# Instala as dependências do front-end
RUN npm install --legacy-peer-deps
RUN npm install vite --save-dev
# RUN npm install @rollup/rollup-linux-x64-gnu 
RUN npm i --save-dev @types/node
RUN npm install @stripe/stripe-js

RUN npm install framer-motion axios react-icons

# 6. Coloca o binário local no PATH (para que 'vite' seja encontrado)
ENV PATH /app/node_modules/.bin:$PATH
# Copia todo o código da landingpage
COPY ./ ./