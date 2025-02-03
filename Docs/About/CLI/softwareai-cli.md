# CLI do SoftwareAI (Interface de Linha de Comando)

## Visão Geral

A Interface de Linha de Comando (CLI) do SoftwareAI foi projetada para simplificar e automatizar diversas tarefas relacionadas ao gerenciamento e uso do framework SoftwareAI.

## Problemas Resolvidos

# 1. Gerenciamento de Configurações

#### Configuração de Banco de Dados da Empresa
- Configurar e armazenar credenciais de banco de dados da empresa de forma segura

##### Exemplo de Comando
```bash
softwareai-cli configure-db-company --namefordb "Nome do Banco de Dados" --databaseurl "https://database.url" --storagebucketurl "https://storage.bucket" --pathkey "/caminho/para/chave-firebase-admin-sdk.json"
```
#### Configuração de Banco de Dados do aplicativo
- Configurar facilmente conexões de banco de dados para aplicações gerenciadas

##### Exemplo de Comando
```bash
softwareai-cli configure-db-app --namefordb "Nome do Banco de Dados" --databaseurl "https://database.url" --storagebucketurl "https://storage.bucket" --pathkey "/caminho/para/chave-firebase-admin-sdk.json"
```
#

#### Integrações de APIs e Serviços
#### Configuração de Credenciais da OpenAI
- Configuração rápida para Credenciais da OpenAI
##### Exemplo de Comando
```bash
softwareai-cli configure-openai --name "Nome para Credenciais da OpenAI" --key "OpenAI-Key" 
```
#
#### Configuração de Credenciais da Hugging Face
- Configuração rápida para Chaves de API da Hugging Face
##### Exemplo de Comando
```bash
softwareai-cli configure-huggingface --name "Nome para Credenciais da Hugging Face" --key "Hugging-Face-Key" 
```
#
#### Configuração de Credenciais do Github
- Configuração rápida para Chaves de API dos agentes na plataforma Github
```bash
softwareai-cli configure-github-keys --name "Nome para Credenciais do Github" --github-username "Usuario do agente no github" --github-token "Chave do agente no github"
```

#

# 2. Geração Automatizada de Tools
- Criar uma tool para um agente com base em um arquivo de função e categoria 
```bash
softwareai-cli create-function --pathfunction "path/to/function.py" --for-agent "QuantumCore" --category "e.g Software_Development" --description-autogen-in-gpu "true" --cache-dir "D:/LLMModels"
```
- observe que ao definir a linha --description-autogen-in-gpu "true"
 voce habilita a criação de descrição usando o **Modelo de raciocínio DeepSeek-R1-Distill-Qwen-1.5B** para a funcao 
- para usar o modelo é preciso definir o local de armazenamento dos tensores com --cache-dir "D:/LLMModels"
#
# 
# 3. Inferencia via Api local
- Ao inves de solicitar agente de forma estatica podemos inferir via Api , ajudando em trabalhos de Multi-Agentes controlados por um lider

```bash
softwareai-cli select-agent-mode-api --name-agent "GearAssist" --category-agent "Software_Technical_Support" --local-execute-port "100"
```
#
#
# 4. Iniciando Servidor de controle de compania
- Aqui podemos iniciar de maneira absurdamente simples todos os scripts e agentes da compania 

```bash
softwareai-cli initialize-company --execute-multiples-agents "True" --names-agents ["GearAssist"] --category-agents ["Software_Technical_Support"] --agents-execute-port ["100"] --run-alfred "True" --path-to-inicializer-alfred "C:\Users\ualer\OneDrive\Área de Trabalho\init_alfred.py" --run-web-company "True"
```
### Argumentos: 
#### --execute-multiples-agents: 
- Valor str booleano que Define se voce quer executar multiplos agentes 
#### --names-agents:
- uma lista de str com os nomes de cada agente a ser executado com o modo execute-multiples-agents
#### --category-agents: 
- uma lista de str com as categorias de cada agente a ser executado com o modo execute-multiples-agents
#### --agents-execute-port: 
- uma lista de str com as portas de cada agente a ser executado em modo api e com o modo execute-multiples-agents
#### --run-alfred: 
- Valor str booleano que Define se voce quer executar o agente de supporte alfred
#### --path-to-inicializer-alfred: 
- caminho str onde esta o inicializador do alfred caso run-alfred seja definido
#### --run-web-company: 
- Valor str booleano que Define se voce quer executar a interface web da compania/framework


#