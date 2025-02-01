NexGenCoder_tools = [
    {"type": "file_search"},
    {
        "type": "function",
        "function": {
            "name": "AutoTestModule",
            "description": "Analisa um arquivo Python (.py) usando Unittest, Pytest, Pylint, Flake8 e MyPy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Caminho Do arquivo para teste"
                    }
                },
                "required": ["file_path"]
            }
        }
    }



]