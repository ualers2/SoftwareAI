
tools_Alfred = [
    {"type": "file_search"},
    {
        "type": "function",
        "function": {
            "name": "OpenSupportTicketProblem",
            "description": "Salva o ticket de problema no banco de dados ",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_email": {
                        "type": "string",
                        "description": "gmaiil do usuario"
                    },
                    "issue_description": {
                        "type": "string",
                        "description": "Descrição do problema"
                    }
                },
                "required": ["user_email", 'issue_description']
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "GearAssist_Technical_Support",
            "description": "GearAssist é um agente tecnico de suporte construido com softwareai, uma ferramenta avançada de rastreamento e resolução de problemas técnicos de software .",
            "parameters": {
                "type": "object",
                "properties": {
                    "Ticketid": {
                        "type": "string",
                        "description": "Ticket id do problema"
                    }
                },
                "required": ["Ticketid"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "CloseSupportTicketProblem",
            "description": "Fecha o ticket de problema no banco de dados ",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticketid": {
                        "type": "string",
                        "description": "Ticket id a ser fechado"
                    }
                },
                "required": ["ticketid"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "RecordCSAT",
            "description": "Antes de fechar o ticket de problema realizamos a coleta de Pontuação de Satisfação do Cliente com notas de 1 a 5 (CSAT) ",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticketid": {
                        "type": "string",
                        "description": "Ticket id"
                    },
                    "csat_score": {
                        "type": "string",
                        "description": "Satisfação do Cliente"
                    }
                },
                "required": ["ticketid", "csat_score"]
            }
        }
    }

    
]

