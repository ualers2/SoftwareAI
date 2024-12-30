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
    }
]