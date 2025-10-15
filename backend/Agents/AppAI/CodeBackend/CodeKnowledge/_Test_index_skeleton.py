"""
Script: index_skeleton.py
Função: Indexar automaticamente todos os arquivos do esqueleto backend (core/, services/, routes/, etc)
para o vetor store Chroma (./chroma_store).

Requisitos:
    pip install openai openai-agents chromadb
Execução:
    python index_skeleton.py
"""

import os
import sys
import openai
import chromadb
from chromadb.config import Settings
from pathlib import Path

# Importa a função que você já tem
from _Test_embedings import build_or_update_index  # ajuste o caminho se necessário
from dotenv import load_dotenv

os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__),  '../',  '../',  '../',  '../', 'Keys', 'keys.env'))

# ---------- CONFIGURAÇÕES ----------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("❌ ERRO: variável OPENAI_API_KEY não definida.")
    sys.exit(1)

openai.api_key = OPENAI_API_KEY

# diretórios padrão do seu backend
TARGET_DIRS = ["Architectures/Stack1", 'Docs']

# extensões de código relevantes
ALLOWED_EXTS = [".py", ".json", ".yml", ".yaml", ".toml", ".md"]

# tamanho máximo por arquivo em bytes (para evitar binários ou logs enormes)
MAX_FILE_SIZE = 200_000  # ~200 KB

# diretório base
BASE_DIR = Path(__file__).resolve().parent


# ---------- FUNÇÃO PRINCIPAL ----------
def collect_files(base_dir: Path):
    """Percorre os diretórios alvo e retorna lista de arquivos válidos"""
    all_files = []
    for folder in TARGET_DIRS:
        path = base_dir / folder
        if not path.exists():
            print(f"⚠️  Diretório {folder}/ não encontrado, ignorando...")
            continue

        for root, _, files in os.walk(path):
            for f in files:
                full_path = Path(root) / f
                if full_path.suffix.lower() not in ALLOWED_EXTS:
                    continue
                if full_path.stat().st_size > MAX_FILE_SIZE:
                    print(f"⚠️  Ignorando arquivo muito grande: {full_path.name}")
                    continue
                if "__pycache__" in full_path.parts or f.startswith("."):
                    continue
                all_files.append(full_path)
    return all_files


def index_repository():
    """Percorre todos os arquivos e adiciona ao índice"""
    files = collect_files(BASE_DIR)
    if not files:
        print("❌ Nenhum arquivo encontrado para indexar.")
        return

    total_chunks = 0
    print(f"📂 Encontrados {len(files)} arquivos para indexar...")

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    continue
                doc_id = str(file_path.relative_to(BASE_DIR))
                build_or_update_index(doc_id, content)
                print(f"✅ Indexado: {doc_id}")
        except Exception as e:
            print(f"⚠️  Falha ao processar {file_path}: {e}")

    print("✅ Indexação concluída com sucesso!")
    print(f"🧠 Dados salvos no diretório: ./chroma_store")


if __name__ == "__main__":
    index_repository()
