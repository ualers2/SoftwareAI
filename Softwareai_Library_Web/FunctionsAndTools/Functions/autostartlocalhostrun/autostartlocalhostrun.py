#!/usr/bin/env python3
"""
Função para iniciar um túnel localhost.run para expor uma aplicação local via URL pública.
"""

import subprocess
import re
import logging
from typing_extensions import TypedDict
from agents import function_tool

# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

class LocalhostRunData(TypedDict):
    port: int

@function_tool
def autostartlocalhostrun(data: LocalhostRunData):
    port = data.get("port", 5000)

    cmd = ['ssh', '-R', f'80:127.0.0.1:{port}', 'ssh.localhost.run']
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        url = None
        while True:
            line = process.stdout.readline()
            if not line:
                break
            logger.debug(line.strip())  # para depuração
            match = re.search(r'(https://[a-zA-Z0-9.-]+\.lhr\.life)', line)
            if match:
                url = match.group(1)
                break

        if url:
            logger.info(f"🚀 URL pública criada: {url}")
            return {
                "url": url,
                "status": "success",
            }
        else:
            logger.warning("⚠️ Não foi possível obter a URL pública.")
            return {
                "status": "error",
                "message": "Não foi possível obter a URL pública."
            }

    except Exception as e:
        logger.exception("❌ Erro ao iniciar túnel localhost.run:")
        return {
            "status": "error",
            "message": str(e)
        }
