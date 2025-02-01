

tools_ByteManager = [
{"type": "file_search"},
{
    "type": "function",
    "function": {
        "name": "create_repo",
        "description": "Realiza A criacao do repositorio no github",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_name": {
                    "type": "string",
                    "description": "Nome do repositório no GitHub."
                },
                "description": {
                    "type": "string",
                    "description": "Descricao de 250 caracteres do projeto."
                },
                "token": {
                    "type": "string",
                    "description": "Token de autenticação do GitHub para realizar operações na API."
                }
            },
            "required": [
                "repo_name",
                "description",
                "token"
            ]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "autoupdaterepo",
        "description": "Realiza Melhorias no repositorio",
        "parameters": {
            "type": "object",
            "properties": {
                "repo_name": {
                    "type": "string",
                    "description": "Nome do repositório no GitHub."
                }
            },
            "required": [
                "repo_name"
            ]
        }
    }
}

]

                