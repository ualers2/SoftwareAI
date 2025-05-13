# Dockerfile otimizado
FROM python:3.12-slim

# Definir onde o Playwright vai guardar seus binários (não dentro da layer de sistema)
ENV PLAYWRIGHT_BROWSERS_PATH=/playwright_cache

# Instalar dependências de SO 
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      curl git ffmpeg libglib2.0-0 libgl1-mesa-glx libnss3 \
      libatk1.0-0 libatk-bridge2.0-0 libcups2 libxcomposite1 \
      libxdamage1 libx11-dev libxss1 libasound2 libsecret-1-dev \
      libgdk-pixbuf2.0-dev libxkbfile-dev libdbus-glib-1-2 libgtk-3-0 \
      unzip wget jq ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Instalar Playwright e baixar deps
RUN pip install --no-cache-dir playwright \
 && playwright install --with-deps

WORKDIR /app

# Copiar e instalar requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . /app/
