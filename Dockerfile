# Dockerfile otimizado
FROM python:3.12-slim

# Definir onde o Playwright vai guardar seus binários (não dentro da layer de sistema)
ENV PLAYWRIGHT_BROWSERS_PATH=/playwright_cache



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
    libgl1 \
    libglib2.0-0 \
    libssl-dev \
 && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y \
 curl \
 gnupg \
 ca-certificates \ 
 nginx \
 git \
 libglib2.0-0 \
 libgl1-mesa-glx \
 libnss3 \
 libxcomposite1 \
 libxdamage1 \
 nodejs \ 
 npm \
 libatk1.0-0 \
 libatk-bridge2.0-0 \
 libcups2 \
 libatspi2.0-0 \
 libx11-dev \
 libxkbfile-dev \
 libsecret-1-dev \
 libnss3-dev \
 libgdk-pixbuf2.0-dev \
 libxss1 \
 libappindicator3-1 \
 libasound2 \
 libglib2.0-0 \
 libgl1-mesa-glx \
 wget \
 curl \
 gnupg2 \
 unzip \
 libgbm-dev \
 libgconf-2-4 \
 ca-certificates \
 libatk-bridge2.0-0 \
 libgtk-3-0 \
 libdbus-glib-1-2\
 --no-install-recommends


# Instalar Playwright e baixar deps
RUN pip install --no-cache-dir playwright \
 && playwright install --with-deps

WORKDIR /app

# Copiar e instalar requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade softwareai-engine-library

# Copiar código
COPY . /app/
