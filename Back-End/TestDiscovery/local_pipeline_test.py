import os
import hmac
import hashlib
import time
import subprocess
import shutil
import logging
from flask import Flask, request, abort
from dotenv import load_dotenv

# Configura logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv("keys.env")
app = Flask(__name__)
repo_name = os.getenv('repo_name', '')
GITHUB_SECRET = os.getenv('GITHUB_SECRET', '')
GITHUB_TOKEN = os.getenv('GH_TOKEN', '')
repo_path = os.getenv('repo_path', '')
SoftwareAI_path = "SoftwareAI"
new_name_for_html = os.getenv('new_name_for_html', '')
new_name_for_js = os.getenv('new_name_for_js', '')
new_name_for_css = os.getenv('new_name_for_css', '')

def checkout_or_create_branch(branch_name, repo_path):
    try:
        # Tenta fazer checkout da branch existente
        subprocess.run(['git', 'checkout', branch_name], cwd=repo_path, check=True)
        print(f"Switched to existing branch: {branch_name}")
    except subprocess.CalledProcessError:
        # Se a branch não existe, cria uma nova
        subprocess.run(['git', 'checkout', '-b', branch_name], cwd=repo_path, check=True)
        print(f"Created and switched to new branch: {branch_name}")

def rename_single_html(dist_dir, new_name):
    src = os.path.join(dist_dir, 'index.html')
    dst = os.path.join(dist_dir, new_name)
    if os.path.exists(src):
        os.rename(src, dst)
        logger.info(f'Renomeado index.html → {new_name}')
    else:
        logger.error(f'HTML não encontrado em {src}')


def rename_single_css(assets_dir, new_name):
    # Encontra o primeiro arquivo .css e renomeia
    for fname in os.listdir(assets_dir):
        if fname.endswith('.css'):
            src = os.path.join(assets_dir, fname)
            dst = os.path.join(assets_dir, new_name)
            try:
                os.rename(src, dst)
                logger.info(f'Renomeado {fname} → {new_name}')
                return True
            except Exception as e:
                logger.error(f'Erro ao renomear CSS: {e}')
                return False
    logger.error(f'Nenhum arquivo .css encontrado em {assets_dir}')
    return False


def rename_single_js(assets_dir, new_name):
    for fname in os.listdir(assets_dir):
        if fname.endswith('.js'):
            src = os.path.join(assets_dir, fname)
            dst = os.path.join(assets_dir, new_name)
            try:
                os.rename(src, dst)
                logger.info(f'Renomeado {fname} → {new_name}')
                return True
            except Exception as e:
                logger.error(f'Erro ao renomear JS: {e}')
                return False
    logger.error(f'Nenhum arquivo .js encontrado em {assets_dir}')
    return False

# Remove diretório antigo
if os.path.exists(repo_path):
    logger.info(f"Removendo repositório existente em {repo_path}")
    shutil.rmtree(repo_path)
    shutil.rmtree(repo_path)

# Clona repositório
clone_url = f"https://{GITHUB_TOKEN}@github.com/{repo_name}.git"
logger.info(f"Clonando repositório: {clone_url}")
subprocess.run(["git", "clone", clone_url, repo_path], check=True)

time.sleep(5)

# Instala dependências (opcional)
logger.info("Instalando dependências do projeto...")
result_install = subprocess.run(
    ["npm", "install"], cwd=repo_path, capture_output=True, text=True
)
if result_install.returncode != 0:
    logger.error("Erro ao instalar dependências:")
    logger.error(result_install.stderr)
   
# Executa o comando de build
logger.info("Disparando npm run build do Vite + React...")
result_build = subprocess.run(
    ["npm", "run", "build"], cwd=repo_path, capture_output=True, text=True
)
if result_build.returncode != 0:
    logger.error("Erro durante o build do projeto:")
    logger.error(result_build.stderr)
   
logger.info("Build concluído com sucesso!")

time.sleep(5)

dist_path = os.path.join("/app", repo_path, 'dist')
assets_path = os.path.join("/app", dist_path, 'assets')

rename_single_html(dist_path, new_name_for_html)
rename_single_css(assets_path, new_name_for_css)
rename_single_js(assets_path, new_name_for_js)

clone_url2 = f"https://{GITHUB_TOKEN}@github.com/SoftwareAI-Company/SoftwareAI.git"
subprocess.run(['git', 'clone', clone_url2, SoftwareAI_path], check=True)

static_js_path = os.path.join(SoftwareAI_path, 'static', 'js')
static_css_path = os.path.join(SoftwareAI_path, 'static', 'css')
templates_path = os.path.join(SoftwareAI_path, 'templates')

shutil.move(os.path.join(assets_path, new_name_for_js), os.path.join(static_js_path, new_name_for_js))
shutil.move(os.path.join(assets_path, new_name_for_css), os.path.join(static_css_path, new_name_for_css))
shutil.move(os.path.join(dist_path, new_name_for_html), os.path.join(templates_path, new_name_for_html))

# Commit ..e PR
subprocess.run(['git', 'config', '--global', "user.email", '"mediacutsstudio@gmail.com"'], cwd=SoftwareAI_path, check=True)
subprocess.run(['git', 'config', '--global', "user.name", 'ualers2'], cwd=SoftwareAI_path, check=True)

subprocess.run(['git', 'init'], cwd=SoftwareAI_path, check=True)
subprocess.run(['git', 'remote', 'set-url', ' origin', 'https://github.com/SoftwareAI-Company/SoftwareAI.git'], cwd=SoftwareAI_path, check=True)

subprocess.run(['git', 'checkout', 'main'], cwd=SoftwareAI_path, check=True)
subprocess.run(['git', 'pull', 'origin', 'main'], cwd=SoftwareAI_path, check=True)
checkout_or_create_branch('auto/update-assets', SoftwareAI_path)

try:
    subprocess.run(['gh', 'auth', 'status'], check=True)
except subprocess.CalledProcessError:
    subprocess.run(['gh', 'auth', 'login', '--with-token'],
                   input=f'{GITHUB_TOKEN}\n'.encode(),
                   env=os.environ.copy(), check=True)

subprocess.run(['git', 'add', '.'], cwd=SoftwareAI_path, check=True)
subprocess.run(['git', 'commit', '-m', 'feat: atualização automática de arquivos estáticos e template'], cwd=SoftwareAI_path, check=True)
subprocess.run(['git', 'push', 'origin', 'auto/update-assets'], cwd=SoftwareAI_path, check=True)
subprocess.run([
    'gh', 'pr', 'create', '--base', 'main', '--head', 'auto/update-assets', '--title', 'Atualização de arquivos estáticos', '--body', 'Atualiza JS, CSS e HTML template após build.'
], cwd=SoftwareAI_path, check=True)

logger.info("Deploy concluído com sucesso.")