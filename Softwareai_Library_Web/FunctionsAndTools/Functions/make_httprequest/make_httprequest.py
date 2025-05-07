from typing import Dict
import requests, logging
from agents import function_tool

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

@function_tool(
    strict_mode=False
)
def make_httprequest(
    method: str,
    url: str,
    headers: Dict[str, str],
    body: Dict[str, str]
):
    """
    Faz uma requisição HTTP.

    Args:
        method: Método HTTP (GET, POST, PUT, DELETE).
        url: URL de destino da requisição.
        headers: Dicionário de cabeçalhos HTTP.
        body: Dicionário que será serializado como JSON no corpo.
    """
    try:
        logger.info(f"Fazendo {method} para {url} • headers={headers} • body={body}")
        resp = requests.request(method, url, headers=headers, json=body)
        logger.info(f"Status: {resp.status_code}")
        return {
            "status": "success",
            "status_code": resp.status_code,
            "response": resp.text
        }
    except Exception as e:
        logger.error(f"Falha na requisição: {e}")
        return {
            "status": "error",
            "message": str(e)
        }
