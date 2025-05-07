import sys
import pytest
import firebase_admin
from firebase_admin import credentials, db, delete_app
from typing_extensions import TypedDict
from agents import function_tool

class Data(TypedDict):
    firebase_json_path: str
    firebase_db_url: str
    code: str

@function_tool
def exec_test_code(data: Data) -> dict:
    """
    Executa o código Selenium gerado e captura falhas.
    O código deve definir um dict chamado `result = {"status": "...", "details": "..."}`.
    """
    import traceback, sys
    local = {}
    # Inicializa Firebase
    cred = credentials.Certificate(data["firebase_json_path"])
    app_instance = firebase_admin.initialize_app(cred, {
        "databaseURL": data["firebase_db_url"]
    }, name="app_instance")
    try:
        exec(data.get("code"), {"app_instance": app_instance}, local)

        return local.get("result", {"status":"unknown","details":"`result` não definido"})
    except Exception as e:
        return {"status":"failed","details":traceback.format_exc()}


