
# softwareai-pip-library

[![Version](https://img.shields.io/badge/version-1.0.23-blue)]
[![Status](https://img.shields.io/badge/status-Stable-green)]
[![License](https://img.shields.io/badge/license-Apache_2.0-green)]

Biblioteca Python para criação e orquestração de agentes de IA especializados em tarefas de desenvolvimento de software:

- Autenticação e gerenciamento de agentes  
- Chat com histórico de conversas e streaming de respostas  
- Ferramentas integradas (busca em arquivos, interpretador de código, vetores semânticos, funções Python)  
- Armazenamento de metadados e histórico em Firebase  
- Destilação de respostas (salva inputs, outputs e instruções em JSON/JSONL)  
- Envio de resultados para webhooks  
- Cálculo de custo de tokens de entrada/saída  

## Índice

- [Recursos](#recursos)  
- [Instalação](#instalação)  
- [Exemplo rápido](#exemplo-rápido)  
- [Documentação](#documentação)  
- [Contribuição](#contribuição)  
- [Licença](#licença)  

## Recursos

- Inicializa e autentica agentes de IA junto à API OpenAI  
- Gerencia vetor stores e arquivos (upload, atualização, listagem)  
- Cria sessões de chat com ferramentas (arquivo, interpretador, vetores, funções)  
- Processa respostas em streaming e armazena histórico  
- Envia eventos de workflow para webhooks  
- Modula cálculo de custo por tokens  

## Instalação

```bash
pip install softwareai-engine-library
````

Requisitos: Python ≥ 3.7

## Exemplo rápido

```python
from softwareai_engine_library.Handler.OpenAIKeysinit import OpenAIKeysinit
from softwareai_engine_library.Handler.FirebaseKeysinit import FirebaseKeysinit
from softwareai_engine_library.AutenticateAgent.AuthAgent import AutenticateAgent
from softwareai_engine_library.Chat.session.create_or_auth_AI import create_or_auth_AI
from softwareai_engine_library.Chat.stream.process_stream import process_stream
import asyncio

# 1) Inicializa clientes
openai_client = OpenAIKeysinit._init_client_("SEU_OPENAI_API_KEY")

# 2) Cria ou autentica um agente de IA
assistant_id, _, _, _ = create_or_auth_AI(
    appcompany=firebase_app,
    client=openai_client,
    key="usuario123",
    instructionsassistant="Você é um assistente especializado em refatoração de código.",
    nameassistant="RefactorBot",
    model_select="gpt-4o-mini-2024-07-18",
    tools=[{"type": "file_search"}, {"type": "code_interpreter"}]
)

```

## Documentação

* Detalhes de todos os módulos e funções: [MODULES\_DETAILS.md](./MODULES_DETAILS.md)
* Informações extras: [MODULES\_DETAILS2.md](./MODULES_DETAILS2.md)

## Contribuição

Pull requests e issues são muito bem-vindos!
Por favor, siga as diretrizes de estilo e adicione testes quando possível.

## Licença

Este projeto está sob a licença Apache 2.0. Veja [LICENSE.txt](LICENSE.txt).
