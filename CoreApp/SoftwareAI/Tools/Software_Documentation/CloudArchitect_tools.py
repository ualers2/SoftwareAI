tools_CloudArchitect = [
    {"type": "file_search"},
    {
        "type": "function",
        "function": {
            "name": "update_readme_to_github",
            "description": "Atualiza o Readme do repositorio no github",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path_readme_improvements": {
                        "type": "string",
                        "description": "O Caminho do readme melhorado"
                    },
                    "repo_name": {
                        "type": "string",
                        "description": "O nome do repositorio do github"
                    },
                    "token": {
                        "type": "string",
                        "description": "Token de autenticação do GitHub para realizar operações na API."
                    }

                },
                "required": [
                    "file_path_readme_improvements",
                    "repo_name",
                    "token"
                ]
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