# Back-End\Modules\Geters\pr_diff.py
import requests
from datetime import datetime, timedelta

def fetch_pr_diff_via_api(pr_api_url: str, token: str) -> str:
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'MediaCutsStudio-Automation',
    }
    response = requests.get(pr_api_url, headers=headers, timeout=120)
    response.raise_for_status()
    files = response.json()
    diff_parts = []
    for f in files:
        if 'patch' in f:
            diff_parts.append(f"--- {f['filename']}\n{f['patch']}")
    return "\n".join(diff_parts)
