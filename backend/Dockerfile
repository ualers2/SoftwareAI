FROM python:3.11-slim

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

RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
