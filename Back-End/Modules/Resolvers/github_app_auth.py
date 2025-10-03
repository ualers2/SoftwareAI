import jwt
import time
import requests
import os
import logging
from cryptography.hazmat.primitives import serialization
from flask import current_app

logger = logging.getLogger(__name__)

INSTALLATION_TOKEN_CACHE = {}


def get_installation_token(app_id: str, private_key_content: str, installation_id: str) -> str:
    """
    Gera um JWT e o usa para obter um Token de Acesso à Instalação do GitHub.

    Args:
        app_id: O ID do GitHub App.
        private_key_content: O conteúdo da chave privada do App (formato PEM).
        installation_id: O ID da instalação para o qual gerar o token.

    Returns:
        O Installation Access Token de curta duração, ou None em caso de falha.
    """
    try:
        # 1. Carregar a Chave Privada do App
        # A chave privada deve estar no formato bytes
        private_key = serialization.load_pem_private_key(
            private_key_content.encode('utf-8'),
            password=None
        )

        # 2. Gerar o JSON Web Token (JWT)
        now = int(time.time())
        
        payload = {
            # Emitido em (Issued at time) - 60 segundos de desvio
            'iat': now - 60,
            # Expiração (Expiration time) - 5 minutos (máx. 10 minutos)
            'exp': now + 300, 
            # ID do App (Issuer)
            'iss': app_id 
        }
        
        # Gerar o JWT assinado com a chave privada
        jwt_token = jwt.encode(
            payload,
            private_key,
            algorithm='RS256'
        )
        
        # 3. Trocar o JWT por um Token de Acesso à Instalação
        url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
        
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.post(url, headers=headers)
        response.raise_for_status() # Lança exceção para status 4xx/5xx
        
        data = response.json()
        access_token = data.get("token")
        
        return access_token
    
    except requests.exceptions.HTTPError as e:
        logger.error(f"Erro HTTP ao obter o token de instalação: {e} - Resposta: {e.response.text}")
        return None
    except Exception as e:
        logger.error(f"Erro ao gerar ou obter o token de instalação: {e}")
        return None

# Função auxiliar para garantir que a chave privada seja carregada com segurança
def load_private_key(private_key_path: str) -> str:
    """Carrega o conteúdo da chave privada do App a partir do caminho do arquivo."""
    if not private_key_path or not os.path.exists(private_key_path):
        logger.error(f"Caminho da chave privada inválido ou arquivo não encontrado: {private_key_path}")
        return None
    try:
        with open(private_key_path, "r") as f:
            # Retorna o conteúdo como uma string, para ser passado para get_installation_token
            return f.read()
    except Exception as e:
        logger.error(f"Erro ao ler o arquivo da chave privada: {e}")
        return None


def get_cached_installation_token(app_id: str, private_key_content: str, installation_id: str) -> str:
    """
    Obtém um token de acesso de instalação usando cache para evitar a regeneração desnecessária.
    O token do GitHub App dura 1 hora. O cache pode ser configurado para 50 minutos (3000 segundos) para segurança.
    """
    cache_key = str(installation_id)
    cached_data = INSTALLATION_TOKEN_CACHE.get(cache_key)
    
    # Verifica o cache
    if cached_data and cached_data['expires_at'] > time.time():
        return cached_data['token']

    # Gera um novo token
    token = get_installation_token(app_id, private_key_content, installation_id)
    
    if token:
        # Define a expiração do cache para 50 minutos (3000 segundos), pois o token real expira em 3600s
        INSTALLATION_TOKEN_CACHE[cache_key] = {
            'token': token,
            'expires_at': time.time() + 3000
        }
        return token
    return None