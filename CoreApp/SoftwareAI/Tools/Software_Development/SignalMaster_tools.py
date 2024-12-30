
tools_SignalMaster = [
    {"type": "file_search"},
    {
        "type": "function",
        "function": {
            "name": "improve_code_and_create_pull_request",
            "description": "Realiza melhorias no código e cria um pull request no repositório GitHub.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_owner": {
                        "type": "string",
                        "description": "Nome do dono do repositório no GitHub."
                    },
                    "repo_name": {
                        "type": "string",
                        "description": "Nome do repositório no GitHub."
                    },
                    "branch_name": {
                        "type": "string",
                        "description": "Nome da branch onde o código será atualizado."
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Caminho do arquivo no repositório."
                    },
                    "commit_message": {
                        "type": "string",
                        "description": "Mensagem de commit descrevendo as melhorias."
                    },
                    "improvements": {
                        "type": "string",
                        "description": "Novo código melhorado."
                    },
                    "pr_title": {
                        "type": "string",
                        "description": "Titulo do Pull request."
                    },
                    "token": {
                        "type": "string",
                        "description": "Token de autenticação do GitHub."
                    }
                },
                "required": ["repo_owner", "repo_name", "branch_name", "file_path", "commit_message", "improvements", "pr_title",  "token"]
            }
        }
    }

]

