
import re
import os 
import shutil
import subprocess

os.chdir(os.path.join(os.path.dirname(__file__)))

import re
import shutil
import glob
import os

python_path = r"C:\Users\Media Cuts Studio\AppData\Local\Programs\Python\Python39\python.exe"

def incrementar_versao_em_arquivo(nome_arquivo):
    padrao = r'version\s*=\s*["\'](\d+)(?:\.(\d+))?(?:\.(\d+))?["\']'
    
    with open(nome_arquivo, "r", encoding="utf-8") as f:
        conteudo = f.read()

    match = re.search(padrao, conteudo)
    if match:
        major = int(match.group(1))
        minor = int(match.group(2) or 0)
        patch = int(match.group(3) or 0)

        # Incrementa o patch
        patch += 1
        if patch > 99:
            patch = 0
            minor += 1
            if minor > 99:
                minor = 0
                major += 1

        # Formata nova versão
        nova_versao = f'{major}.{minor}.{patch}'
        conteudo_atualizado = re.sub(padrao, f'version=\"{nova_versao}\"', conteudo)
        print(f"Nova versão: {nova_versao}")
    else:
        raise ValueError("Versão não encontrada no arquivo.")

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(conteudo_atualizado)


for folder in ["build", "dist"] + glob.glob("*.egg-info"):
    try:
        shutil.rmtree(folder)
    except Exception as e:
        print(f"Erro ao remover {folder}: {e}")

try:
    shutil.rmtree("dist")
except Exception as e:
    print(e)
    
try:
    shutil.rmtree("build")
except Exception as e:
    print(e)
    
try:
    shutil.rmtree("SoftwareAI.egg-info")
except Exception as e:
    print(e)

padrao = r'version="(\d+)\.(\d+)\.(\d+)"'
with open("setup.py", "r", encoding="utf-8") as f:
    conteudo = f.read()
match = re.search(padrao, conteudo)
if match:
    major, minor, patch = map(int, match.groups())
    versao = f'{major}.{minor}.{patch}'
    try:
        shutil.rmtree(f"softwareai_engine_library-{versao}")
    except Exception as e:
        print(e)

else:
    raise ValueError("Versão não encontrada no arquivo.")

incrementar_versao_em_arquivo("setup.py")



comand = [
"move",
"LICENSE.txt",
"LICENSE_HIDE.txt"
]
subprocess.run(comand, shell=True)



comand = [f"python", "setup.py", "sdist", "bdist_wheel"]
subprocess.run(comand, shell=True)


comand = [
"move",
"LICENSE_HIDE.txt",
"LICENSE.txt"
]
subprocess.run(comand, shell=True)

comand = [
"twine",
"upload",
"dist/*"
]
subprocess.run(comand, shell=True)






# comand = [
# "pip",
# "install",
# "--upgrade",
# "softwareai_engine_library"
# ]
# subprocess.run(comand, shell=True)
# subprocess.run(comand, shell=True)


for folder in ["build", "dist"] + glob.glob("*.egg-info"):
    try:
        shutil.rmtree(folder)
    except Exception as e:
        print(f"Erro ao remover {folder}: {e}")

try:
    shutil.rmtree("dist")
except Exception as e:
    print(e)
    
try:
    shutil.rmtree("build")
except Exception as e:
    print(e)
    
try:
    shutil.rmtree("SoftwareAI.egg-info")
except Exception as e:
    print(e)

import time
time.sleep(1)

