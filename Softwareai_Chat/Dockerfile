FROM python:3.12-slim-bullseye

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    jq \
    libffi-dev \
    build-essential \
    gcc \
    g++ \
    linux-headers-amd64 \
    libssl-dev \
 && rm -rf /var/lib/apt/lists/*

# Baixar e instalar o Ngrok
RUN curl -s -o /tmp/ngrok.tgz https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz && \
    tar -xzf /tmp/ngrok.tgz -C /usr/local/bin && \
    rm /tmp/ngrok.tgz

# Definir diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar os arquivos do projeto
COPY . /app
