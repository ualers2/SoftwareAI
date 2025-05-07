FROM python:3.9-slim

# Instalar dependências necessárias
RUN apt-get update && \
    apt-get install -y ca-certificates curl jq && \
    update-ca-certificates

# Baixar e instalar o Ngrok
RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt update && apt install -y ngrok

# Definir diretório de trabalho
WORKDIR /app

# Copiar dependências do Python e instalar
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt


# Copiar todos os arquivos do projeto
COPY . /app
