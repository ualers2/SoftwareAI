# Back-End\Modules\Updaters\pr_merge.py

import asyncio
import requests
import logging
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def merge_pull_request(
        GITHUB_TOKEN, 
        repo_name, 
        pr_number,
        
    ):
    merge_url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}/merge"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        "merge_method": "merge",  # Pode ser "merge", "squash" ou "rebase"
        "commit_title": f"Auto-merge PR #{pr_number}",
        "commit_message": "Merge automático realizado pelo agente"
    }
    response = requests.put(merge_url, headers=headers, json=data)
    
    if response.status_code == 200:
        logger.info(f"PR #{pr_number} mesclado com sucesso.")
    else:
        logger.error(f"Falha ao tentar mergear PR #{pr_number}: {response.text}")
