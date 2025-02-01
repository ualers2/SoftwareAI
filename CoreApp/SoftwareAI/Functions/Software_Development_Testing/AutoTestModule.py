import subprocess
import os
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

def AutoTestModule(file_path):
    """
    Analisa um arquivo Python (.py) usando Unittest, Pytest, Pylint, Flake8 e MyPy.

    Parâmetros:
        file_path (str): Caminho para o arquivo Python a ser analisado.

    Retorna:
        dict: Um dicionário contendo os resultados de cada ferramenta.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    if not file_path.endswith('.py'):
        raise ValueError("O arquivo fornecido não é um arquivo .py")

    results = {
        "unittest": {},
        "pytest": {},
        "pylint": {},
        "flake8": {},
        "mypy": {}
    }
    def Unittest():
        # Unittest
        print("Executando Unittest...")
        unittest_result = subprocess.run(
            ['python', '-m', 'unittest', file_path],
            capture_output=True,
            text=True
        )
        results['unittest'] = {
            "stdout": unittest_result.stdout.strip(),
            "stderr": unittest_result.stderr.strip(),
            "returncode": unittest_result.returncode
        }

    def Pytest():
        # Pytest
        print("Executando Pytest...")
        pytest_result = subprocess.run(
            ['pytest', file_path],
            capture_output=True,
            text=True
        )
        results['pytest'] = {
            "stdout": pytest_result.stdout.strip(),
            "stderr": pytest_result.stderr.strip(),
            "returncode": pytest_result.returncode
        }
    
    def Pylint():
        # Pylint
        print("Executando Pylint...")
        pylint_result = subprocess.run(
            ['pylint', file_path],
            capture_output=True,
            text=True
        )
        results['pylint'] = {
            "stdout": pylint_result.stdout.strip(),
            "stderr": pylint_result.stderr.strip(),
            "returncode": pylint_result.returncode
        }
    
    def Flake8():
        # Flake8
        print("Executando Flake8...")
        flake8_result = subprocess.run(
            ['flake8', file_path],
            capture_output=True,
            text=True
        )
        results['flake8'] = {
            "stdout": flake8_result.stdout.strip(),
            "stderr": flake8_result.stderr.strip(),
            "returncode": flake8_result.returncode
        }
    
    def MyPy():
        # MyPy
        print("Executando MyPy...")
        mypy_result = subprocess.run(
            ['mypy', file_path],
            capture_output=True,
            text=True
        )
        results['mypy'] = {
            "stdout": mypy_result.stdout.strip(),
            "stderr": mypy_result.stderr.strip(),
            "returncode": mypy_result.returncode
        }

    with ThreadPoolExecutor(max_workers=9) as executor:
        futures = {
            executor.submit(Unittest): "unittest",
            executor.submit(Pytest): "pytest",
            executor.submit(Pylint): "pylint",
            executor.submit(Flake8): "flake8",
            executor.submit(MyPy): "mypy"
        }

        for future in as_completed(futures):
            result_key = futures[future]
            try:
                future.result()  
            except Exception as e:
                print(f"Ocorreu um erro ao executar {result_key}: {e}")

    return json.dumps(results, indent=4)
