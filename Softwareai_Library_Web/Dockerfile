FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install openai-agents
RUN pip install --no-cache-dir --upgrade softwareai-engine-library
 
# Copiar todos os arquivos do projeto
COPY . /app


