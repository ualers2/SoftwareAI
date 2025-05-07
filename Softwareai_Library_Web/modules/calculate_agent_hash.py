import os
import hashlib

def calculate_agent_hash(agent_path: str) -> str:
    """
    Gera SHA256 do conteúdo de definição do agente: metadata.yaml/json e arquivo de instruções.
    """
    sha256 = hashlib.sha256()
    for root, _, files in os.walk(agent_path):
        for fname in sorted(files):
            if fname.endswith(('.md', '.py', '.json', '.yaml', '.yml')):
                full = os.path.join(root, fname)
                with open(full, 'rb') as f:
                    while chunk := f.read(8192):
                        sha256.update(chunk)
    return sha256.hexdigest()