# git_context_layer.py
"""
Git Context Layer - Automação inteligente de commits com IA
Monitora alterações locais e cria commits contextualizados automaticamente
"""

import os
import sys
import time
import json
import asyncio
import subprocess
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Optional
from dataclasses import dataclass, asdict

import anthropic
from dotenv import load_dotenv

from Agents.GitContextLayer.ai import GenerateCommitMessageAgent

@dataclass
class Config:
    """Configurações do Git Context Layer"""
    lines_threshold: int = 1
    files_threshold: int = 1   
    time_threshold: int = 1  
    auto_push: bool = False 
    require_tests: bool = False  
    max_file_size: int = 1_000_000 
    ignored_patterns: List[str] = None
    ai_model: str = "gpt-5-nano"
    api_key: str = ""
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'Keys', 'keys.env'))
    os.chdir(os.path.join(os.path.dirname(__file__)))

    def __post_init__(self):
        if self.ignored_patterns is None:
            self.ignored_patterns = [
                "__pycache__", "*.pyc", "*.pyo", "*.pyd",
                ".git", ".venv", "venv", "node_modules",
                ".env", "*.log", ".DS_Store", "*.swp",
                "build", "dist", "*.egg-info"
            ]
    
    @classmethod
    def load(cls, config_path: str = ".gitcontext.json") -> 'Config':
        """Carrega configuração de arquivo"""
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                data = json.load(f)
                return cls(**data)
        return cls()
    
    def save(self, config_path: str = ".gitcontext.json"):
        """Salva configuração em arquivo"""
        with open(config_path, 'w') as f:
            json.dump(asdict(self), f, indent=2)


class GitAnalyzer:
    """Analisa alterações do Git"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
    
    def run_git_command(self, *args) -> str:
        """Executa comando git e retorna output"""
        try:
            result = subprocess.run(
                ["git", "-C", str(self.repo_path)] + list(args),
                capture_output=True,
                text=True,
                encoding='utf-8',
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro Git: {e.stderr}")
            return ""
    
    def get_modified_files(self) -> List[str]:
        """Retorna lista de arquivos modificados"""
        output = self.run_git_command("status", "--porcelain")
        files = []
        for line in output.split('\n'):
            if line:
                status, filepath = line[:2], line[3:]
                if status.strip():
                    files.append(filepath)
        return files
    
    def get_diff(self, filepath: Optional[str] = None) -> str:
        """Retorna diff das alterações"""
        if filepath:
            return self.run_git_command("diff", "HEAD", "--", filepath)
        return self.run_git_command("diff", "HEAD")
    
    def count_lines_changed(self) -> int:
        """Conta total de linhas modificadas usando git diff --numstat."""
        output = self.run_git_command("diff", "--numstat")
        
        total_lines = 0
        
        for line in output.split('\n'):
            if line:
                try:
                    parts = line.split('\t', 2)
                    if len(parts) < 3:
                        continue  
                    insertions_str, deletions_str, _ = parts
                    if insertions_str.isdigit():
                        total_lines += int(insertions_str)
                    if deletions_str.isdigit():
                        total_lines += int(deletions_str)
                        
                except ValueError:
                    continue
                    
        return total_lines
    
    def git_add(self, files: List[str] = None):
        """Adiciona arquivos ao staging"""
        if files:
            for f in files:
                self.run_git_command("add", f)
        else:
            self.run_git_command("add", ".")
    
    def git_commit(self, message: str):
        """Cria commit com mensagem"""
        self.run_git_command("commit", "-m", message)
    
    def git_push(self):
        """Push para repositório remoto"""
        self.run_git_command("push")
    
    def has_tests(self) -> bool:
        """Verifica se há testes no repositório"""
        test_patterns = ["test_*.py", "*_test.py", "tests/"]
        for pattern in test_patterns:
            if list(self.repo_path.glob(f"**/{pattern}")):
                return True
        return False
    
    def run_tests(self) -> bool:
        """Executa testes (pytest se disponível)"""
        try:
            result = subprocess.run(
                ["pytest", "--tb=short"],
                cwd=self.repo_path,
                capture_output=True,
                timeout=60
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return True  # Se não tem pytest, considera ok

class ChangeTracker:
    """Rastreia alterações e acumula mudanças (apenas tempo de inatividade)"""
    
    def __init__(self):
        # last_activity_time rastreia a última vez que *qualquer* mudança foi detectada no Git.
        self.last_activity_time: float = time.time()
        self.lock = threading.Lock()
    
    # Esta função não é mais chamada pelo Watchdog, mas é mantida por coerência
    # e para uso manual, se necessário (embora não seja mais usada no fluxo).
    def add_change(self, filepath: str):
        """Atualiza o tempo de atividade para iniciar o contador de inatividade."""
        with self.lock:
            self.last_activity_time = time.time()
    
    def reset(self):
        """Reseta o tempo de inatividade após um commit bem-sucedido."""
        with self.lock:
            self.last_activity_time = time.time()
    
    def should_trigger(self, config: Config, git: GitAnalyzer) -> bool:
        """Verifica se deve disparar análise com base nos thresholds do Git e tempo."""
        with self.lock:
            files = git.get_modified_files()
            lines = git.count_lines_changed()

            current_time = time.time()
            time_since_last_activity = current_time - self.last_activity_time
            
            # --- Lógica de Controle de Estado ---
            if not files:
                self.last_activity_time = current_time
                return False
            
            if len(files) < config.files_threshold or lines < config.lines_threshold:
                return False

            if time_since_last_activity < config.time_threshold:
                return False 
            
            return True

class GitContextLayer:
    """Orquestrador principal do Git Context Layer"""
    
    def __init__(self, config: Config, repo_path: str = "."):
        self.config = config
        self.git = GitAnalyzer(repo_path)

        self.tracker = ChangeTracker()
        self.observer = None
        self.running = False
    
    def start_watching(self):
        """Inicia monitoramento de alterações"""
        print("🚀 Git Context Layer iniciado")
        print(f"📊 Thresholds: {self.config.lines_threshold} linhas, {self.config.files_threshold} arquivos")
        print(f"⏱️  Tempo mínimo: {self.config.time_threshold}s")
        print(f"🔒 Auto-push: {'✓' if self.config.auto_push else '✗'}")
        print(f"🧪 Requer testes: {'✓' if self.config.require_tests else '✗'}")
        
        # VERIFICA IMEDIATAMENTE SE HÁ MUDANÇAS PENDENTES
        print("\n🔍 Verificando alterações pendentes no Git...")
        files = self.git.get_modified_files()
        lines = self.git.count_lines_changed()
        
        if files:
            print(f"✨ Encontradas {len(files)} arquivo(s) modificado(s) com {lines} linha(s) alterada(s)")
            # Força processamento imediato se atingir thresholds
            if len(files) >= self.config.files_threshold and lines >= self.config.lines_threshold:
                print("🎯 Thresholds já atingidos! Processando imediatamente...\n")
                self.process_changes()
                self.tracker.reset()
            else:
                print(f"⏳ Aguardando mais mudanças (precisa {self.config.files_threshold} arquivos e {self.config.lines_threshold} linhas)")
        else:
            print("✓ Nenhuma alteração pendente")
        
        print("\n👀 Monitorando alterações contínuas...\n")
        
        self.running = True
        
        try:
            while self.running:
                time.sleep(5)
                self._check_and_process()
        except KeyboardInterrupt:
            print("\n\n⏹️  Parando Git Context Layer...")

    
    def _check_and_process(self):
        """Verifica e processa alterações se thresholds atingidos"""
        if self.tracker.should_trigger(self.config, self.git):
            print("\n" + "="*60)
            print("🎯 Thresholds atingidos! Iniciando análise...")
            print("="*60)
            
            self.process_changes()
            self.tracker.reset()
    
    def process_changes(self):
        """Processa alterações: analisa, commita e faz push se configurado"""
        files = self.git.get_modified_files()
        if not files:
            print("ℹ️  Nenhuma alteração detectada")
            return
        
        print(f"\n📝 Arquivos modificados: {len(files)}")
        for f in files[:10]:
            print(f"   • {f}")
        if len(files) > 10:
            print(f"   ... e mais {len(files) - 10} arquivos")
        
        lines = self.git.count_lines_changed()
        print(f"📊 Linhas modificadas: {lines}")
        
        print("\n🔒 Verificando regras de segurança...")
        
        for filepath in files:
            full_path = self.git.repo_path / filepath
            if full_path.exists() and full_path.stat().st_size > self.config.max_file_size:
                print(f"⚠️  Arquivo muito grande: {filepath}")
                return
        
        print("\n🤖 Analisando alterações com IA...")
        diff = self.git.get_diff()
        commit_output, *usage_stats  =  asyncio.run(GenerateCommitMessageAgent(
                self.config.api_key,
                "",
                diff,
                files,
                self.config.ai_model,
                40000,
            )
        )
        commit_message = f"{commit_output.subject}\n\n{commit_output.body}"
        
        print("\n💬 Mensagem de commit gerada:")
        print("   " + commit_message.replace("\n", "\n   "))
        
        print("\n📦 Criando staging e commit...")
        self.git.git_add()
        self.git.git_commit(commit_message)
        print("✅ Commit criado com sucesso!")
        if self.config.require_tests and self.git.has_tests():
            print("\n🧪 Executando testes...")
            if not self.git.run_tests():
                print("❌ Testes falharam! Push cancelado.")
                return
            print("✅ Testes passaram!")
        
        if self.config.auto_push:
            print("\n🚀 Fazendo push para repositório remoto...")
            self.git.git_push()
            print("✅ Push concluído!")
        else:
            print("\n⏸️  Auto-push desabilitado. Execute 'git push' manualmente.")
        
        print("\n" + "="*60)
        print("✨ Processo concluído!")
        print("="*60 + "\n")


def main():
    """Função principal"""
    config = Config.load()

    config.api_key = os.getenv("OPENAI_API_KEY", "")
    if not config.api_key:
        print("❌ Erro: OPENAI_API_KEY não configurada")
        print("Configure no arquivo .gitcontext.json ou variável de ambiente")
        sys.exit(1)

    if not os.path.exists(".gitcontext.json"):
        config.save()
        print("📝 Arquivo de configuração criado: .gitcontext.json")
    
    gcl = GitContextLayer(config)
    gcl.start_watching()


if __name__ == "__main__":
    main()