# Back-End\Modules\Updaters\pr_body.py
import requests
from datetime import datetime, timedelta
def update_pr_body(GITHUB_TOKEN, pr_api_url, title, new_body):
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'title': title, # Manter o título existente
        'body': new_body
    }
    response = requests.patch(pr_api_url, headers=headers, json=data)
    response.raise_for_status()
    print(f"Corpo do Pull Request atualizado para {pr_api_url}")
