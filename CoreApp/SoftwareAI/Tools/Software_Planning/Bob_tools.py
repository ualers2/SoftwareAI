tools_Bob = [
    {"type": "file_search"},
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Retorna a data e hora atual no formato YYYY-MM-DD HH:MM:SS.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "autosave",
            "description": "Salva um codigo python em um caminho",
            "parameters": {
                "type": "object",
                "properties": {
                    "code": {
                        "type": "string",
                        "description": "codigo"
                    },
                    "path": {
                        "type": "string",
                        "description": "Caminho do codigo"
                    }
                },
                "required": ["code","path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "autoupload",
            "description": "Realiza o upload ou update de um arquivo",
            "parameters": {
                "type": "object",
                "properties": {
                    "softwarepypath": {
                        "type": "string",
                        "description": "caminho do arquivo"
                    },
                    "repo_name": {
                        "type": "string",
                        "description": "Nome do repositorio "
                    },
                    "token": {
                        "type": "string",
                        "description": "Token do github de que realiza o upload ou update"
                    }
                },
                "required": ["softwarepypath","repo_name","token"]
            }
        }
    }
]