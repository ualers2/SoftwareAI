"""
File Overview: diffprocessor.py

Este módulo substitui toda a lógica manual de parsing e aplicação de diffs.
Agora utiliza a biblioteca `unidiff` para leitura e análise detalhada dos patches
e delega a aplicação real para o `git apply --3way`, garantindo máxima compatibilidade
com o comportamento nativo do Git.

Principais recursos:
- Leitura de diffs padrão (unified format) usando `unidiff`.
- Validação básica dos blocos de alteração.
- Aplicação real do patch usando `git apply --3way` com fallback seguro.
- Logs estruturados para auditoria e debugging.

Dependências:
- unidiff (pip install unidiff)
- git instalado no sistema
"""

import subprocess
import logging
from pathlib import Path
from unidiff import PatchSet

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[diff] %(message)s")


class DiffProcessor:
    """
    Classe de alto nível para leitura, análise e aplicação de diffs.
    Usa o `unidiff` para parsing e `git apply` para a aplicação real.
    """

    def __init__(self, diff_path="", diff_content=False, f=""):
        if diff_content == False:
            self.diff_path = Path(diff_path)
            if not self.diff_path.exists():
                raise FileNotFoundError(f"Arquivo de diff não encontrado: {self.diff_path}")
            self.patchset = None
        elif diff_content == True:    
            self.patchset = PatchSet(f)

    def parse(self):
        """Lê e analisa o diff usando `unidiff`."""
        with open(self.diff_path, "r", encoding="utf-8") as f:
            self.patchset = PatchSet(f)
        logger.info(f"Diff carregado com {len(self.patchset)} arquivos modificados.")
        return self.patchset

    def summary(self):
        """Retorna um resumo textual das mudanças contidas no diff."""
        if not self.patchset:
            self.parse()

        summary_lines = []
        for patched_file in self.patchset:
            added = sum(1 for h in patched_file for l in h if l.is_added)
            removed = sum(1 for h in patched_file for l in h if l.is_removed)
            summary_lines.append(
                f"{patched_file.path}: +{added} / -{removed} linhas"
            )
        return "\n".join(summary_lines)

    def validate(self):
        """Valida se os arquivos referenciados existem antes de aplicar."""
        if not self.patchset:
            self.parse()

        problems = []
        for patched_file in self.patchset:
            if not Path(patched_file.path).exists() and not patched_file.is_added_file:
                problems.append(f"Arquivo não encontrado: {patched_file.path}")
        if problems:
            logger.warning("⚠️  Problemas de validação encontrados:\n" + "\n".join(problems))
        else:
            logger.info("✅ Todos os arquivos do diff foram validados com sucesso.")
        return problems

    def apply(self, repo_path: str = "."):
        """
        Aplica o diff usando `git apply --3way`.
        Caso falhe, tenta fallback com `--reject` (gera .rej com falhas).
        """
        repo = Path(repo_path)
        if not repo.exists():
            raise FileNotFoundError(f"Repositório não encontrado: {repo_path}")

        try:
            logger.info("Tentando aplicar patch com git apply --3way ...")
            subprocess.run(
                ["git", "apply", "--3way", '--ignore-whitespace', str(self.diff_path)],
                cwd=repo,
                check=True,
                text=True,
                capture_output=True,
            )
            logger.info("✅ Patch aplicado com sucesso (modo 3-way).")
        except subprocess.CalledProcessError as e:
            logger.warning("⚠️  Falha no modo 3-way, tentando fallback com --reject...")
            reject_proc = subprocess.run(
                ["git", "apply", "--reject", str(self.diff_path)],
                cwd=repo,
                text=True,
                capture_output=True,
            )
            if reject_proc.returncode == 0:
                logger.info("✅ Patch parcialmente aplicado (arquivos .rej gerados).")
            else:
                logger.error(f"❌ Erro ao aplicar patch:\n{reject_proc.stderr}")
                raise RuntimeError("Falha ao aplicar patch.") from e
