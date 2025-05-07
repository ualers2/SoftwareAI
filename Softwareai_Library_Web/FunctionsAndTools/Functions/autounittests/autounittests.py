import sys
import pytest
from typing_extensions import TypedDict
from agents import function_tool

class autounittestsData(TypedDict):
    test_file: str

@function_tool
def autounittests(data: autounittestsData) -> int:
    try:
        data_FINAL = data["data"]
        test_file = data_FINAL["test_file"]
    except Exception as e:
        print(e)
        test_file = data["test_file"]
    """
    Executa os testes do arquivo fornecido e retorna o código de saída do pytest.
    Código 0 indica que todos os testes passaram.
    """
    exit_code = pytest.main([test_file])
    if exit_code == 0:
        print("Todos os testes passaram.")
    else:
        print("Alguns testes falharam.")
    return exit_code

def autounittests1(test_file: str) -> int:
    """
    Executa os testes do arquivo fornecido e retorna o código de saída do pytest.
    Código 0 indica que todos os testes passaram.
    """
    exit_code = pytest.main([test_file])
    if exit_code == 0:
        print("Todos os testes passaram.")
    else:
        print("Alguns testes falharam.")
    return exit_code
