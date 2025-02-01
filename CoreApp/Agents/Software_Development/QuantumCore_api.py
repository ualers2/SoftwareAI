#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI All Paths 
from softwareai.CoreApp._init_paths_ import *
#########################################
# IMPORT SoftwareAI Instructions
from softwareai.CoreApp._init_Instructions_ import *
#########################################
# IMPORT SoftwareAI Tools
from softwareai.CoreApp._init_tools_ import *
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *
#########################################
# IMPORT SoftwareAI _init_environment_
from softwareai.CoreApp._init_environment_ import init_env
from flask import Flask, request, jsonify
import hmac
import hashlib
import requests
import urllib.parse
import json



app = Flask(__name__)
CORS(app)  
app.secret_key = os.urandom(24)  

github_username, github_token, GITHUB_WEBHOOK_SECRET = GithubKeys.QuantumCore_github_keys()

@app.route('/')
def index():
    return "None"


@app.route('/api/quantumcore_mode_api', methods=['POST'])
def quantumcore_mode_api():
    # Captura a assinatura enviada pelo GitHub
    signature = request.headers.get('X-Hub-Signature-256')
    if signature is None:
        return "Assinatura não encontrada", 400

    # Captura o payload bruto
    payload = request.data

    # Calcula a assinatura
    computed_signature = 'sha256=' + hmac.new(
        GITHUB_WEBHOOK_SECRET.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    # Logs para depuração
    Payloaddecode = payload.decode('utf-8', errors='ignore')
    print(f"Signature from GitHub: {signature}")
    print(f"Computed Signature: {computed_signature}")
    #print(f"Payload (decoded): {Payloaddecode}")

    # Valida a assinatura
    if not hmac.compare_digest(signature, computed_signature):
        return "Assinatura inválida", 403

    # Processa o JSON do payload
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return "Payload inválido", 400

    # Verifica se é um ping (zen)
    if 'zen' in data:
        return "Ping recebido", 200

    # Agora, verifica a presença de issue no payload
    if 'issue' in data:


        repo_full_name = data['repository']['full_name']
        owner, repo = repo_full_name.split('/')
        issue_number = data['issue']['number']
        issue_title = data['issue']['title']
        issue_body = data['issue']['body']
        issue_creator = data['issue']['user']['login']
        print(issue_body)


        companyname = "SoftwareAI-Company"
        key_openai = OpenAIKeysteste.keys()

        repo_name = repo
        name_app = "appx"

        appfb = FirebaseKeysinit._init_app_(name_app)
        client = OpenAIKeysinit._init_client_(key_openai)

        key = "AI_QuantumCore_Desenvolvedor_Pleno_de_Software_em_Python"
        nameassistant = "AI QuantumCore Desenvolvedor Pleno de Software em Python"
        model_select = "gpt-4o-mini-2024-07-18"


        Upload_1_file_in_thread = None
        Upload_1_file_in_message = None
        Upload_1_image_for_vision_in_thread = None
        vectorstore_in_assistant = None
        vectorstore_in_Thread = None
        Upload_list_for_code_interpreter_in_thread = None
        
        tools_QuantumCore = [
            {"type": "file_search"},
            {
                "type": "function",
                "function": {
                    "name": "autopullrequest",
                    "description": "cria um pull request no repositório GitHub.",
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
            },
            {
                "type": "function",
                "function": {
                    "name": "get_repo_structure",
                    "description": "Obtem o a estrutura do repositório GitHub.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "repo_name": {
                                "type": "string",
                                "description": "Nome do repositório no GitHub."
                            },
                            "repo_owner": {
                                "type": "string",
                                "description": "Nome do dono do repositório no GitHub."
                            },
                            "github_token": {
                                "type": "string",
                                "description": "Token de autenticacao "
                            },
                            "branch_name": {
                                "type": "string",
                                "description": "Nome da branch principal geralmente main."
                            }
                        },
                        "required": ["repo_name", "repo_owner", "github_token", "branch_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "autogetfilecontent",
                    "description": "Obtem o conteudo do arquivo em um repositório GitHub.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "repo_name": {
                                "type": "string",
                                "description": "Nome do repositório no GitHub."
                            },
                            "file_path": {
                                "type": "string",
                                "description": "Caminho relativo junto ao arquivo"
                            },
                            "branch_name": {
                                "type": "string",
                                "description": "Nome da branch principal geralmente main."
                            },
                            "companyname": {
                                "type": "string",
                                "description": "Nome da organizacao/compania"
                            },
                            "github_token": {
                                "type": "string",
                                "description": "Token de autenticacao "
                            }
                        },
                        "required": ["repo_name", "file_path", "branch_name", "companyname", "github_token"]
                    }
                }
            }
        ]
        
        instructionQuantumCore = f""" 
        Meu nome é **QuantumCore**, sou Desenvolvedor Pleno em Python na empresa **{companyname}**. Minha responsabilidade é aprimorar o código com qualidade, respeitando a estrutura existente do projeto.

        ### **Minhas Responsabilidades:**  

        1. **Analisar a Estrutura Completa do Projeto:**  
        - Acesso a toda a **estrutura do repositório** usando a função **get_repo_structure**, que retorna um dicionário com todos os arquivos e diretórios.  
        - Utilizo a função **autogetfilecontent** para acessar o **conteúdo completo de qualquer arquivo** conforme necessário.

        2. **Selecionar Arquivos Estratégicos para Melhoria:**  
        - **Tenho autonomia total** para escolher de **1 arquivo** que apresentem maior potencial de melhoria.  
        - A escolha é baseada na **análise da estrutura** e no **conteúdo dos arquivos**.

        3. **Analisar e Melhorar o Código:**  
        - Examino cuidadosamente o código e **identifico melhorias sem modificar a estrutura do programa**.  
        - As melhorias podem incluir:  
            - **Otimizações de desempenho**  
            - **Correções de bugs**  
            - **Refatorações seguras**  
            - **Implementação de novas funcionalidades**  
        - **Preservo a lógica e a organização original do código**.

        4. **Garantir o Retorno Completo do Código:**  
        - **É obrigatório retornar o código completo e atualizado**, com todas as melhorias implementadas.  
        - **Nunca** enviar apenas trechos de código ou mensagens de continuação.  
        - O código deve ser completo, claro e totalmente funcional.

        5. **Gerar Commit e Pull Request:**  
        - Crio automaticamente:  
            - Uma **Commit Message** clara e descritiva.  
            - Um **Título de PR** direto e objetivo.  
            - Uma **Descrição de PR** completa, explicando as melhorias.  
            - Um **Branch Name** claro e relacionado à melhoria principal.  
        - Utilizo a função **autopullrequest** para abrir um Pull Request com as melhorias aplicadas.

        6. **Manter a Qualidade do Código:**  
        - Garanto um código **limpo, legível e documentado**.  
        - Evito mudanças desnecessárias na lógica existente.  

        ---

        ### **Funções Disponíveis:**  
        - **get_repo_structure** → Retorna a estrutura completa do repositório.  
        - **autogetfilecontent** → Retorna o conteúdo completo de um arquivo específico.  
        - **autopullrequest** → Cria automaticamente um Pull Request com commit, título e descrição gerados.  

        Com esse fluxo de trabalho, asseguro melhorias eficientes, seguras e de alta qualidade, mantendo a integridade do projeto.
        """
            
        AI_QuantumCore, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(
                                                                                                            appfb, 
                                                                                                            client, 
                                                                                                            key, 
                                                                                                            instructionQuantumCore, 
                                                                                                            nameassistant, 
                                                                                                            model_select, 
                                                                                                            tools_QuantumCore
                                                                                                            )

        mensagem = f"""
        ### **Missão:** 
        Analisar automaticamente o repositório `{repo_name}` e implementar melhorias baseadas no problema descrito no `issue_body`. Escolha **1 arquivo estratégico** para modificação com base na descrição do problema ou, caso não seja especificado, utilize critérios próprios para decidir.

        **Detalhes da Issue:**
        - **Criador:** {issue_creator}
        - **Número:** {issue_number}
        - **Título:** {issue_title}
        - **Descrição:** {issue_body}

        ---

        ### **Fluxo de Trabalho Automatizado:**  

        1. **Obtenha a Estrutura Completa do Repositório:**  
        - Utilize a função **get_repo_structure** para acessar a **estrutura completa** do repositório.  
        - Identifique os arquivos mais relevantes com base na descrição do problema.


        2. **Selecione e Leia o Conteúdo dos Arquivos:**  
        - Selecione de **1 arquivo** com base em sua relevância.  
        - Utilize a função **autogetfilecontent** para obter o **conteúdo completo** desses arquivos.  
        

        3. **Implementação de Melhorias:**
        - **Analise o conteúdo** e identifique pontos de melhoria, incluindo:  
            - Otimização de desempenho.  
            - Correções de bugs.  
            - Refatoração para legibilidade e manutenção.  
            - Implementação de funcionalidades relacionadas ao problema.  
        - **Mantenha a estrutura geral e lógica do código inalteradas.**

        4. **Gere o Código Completo:**  
            - Gere e **retorne o código completo** com as melhorias implementadas.
            - **Garanta que o código seja funcional e compatível com o restante do projeto.**

        5. **Automatize o Pull Request:**  
        - **Crie automaticamente**:  
            - Uma **Commit Message** clara e descritiva.  
            - Um **Título do Pull Request (PR)** direto e objetivo.  
            - Uma **Descrição detalhada** explicando as melhorias.  
            - Um **Branch Name** relacionado à principal melhoria.  
        - Utilize a função **autopullrequest()** para abrir o PR.

        ---

        ### **Detalhes do Pull Request:**  
        - **Repo Owner:** {companyname}  
        - **Repo Name:** {repo_name}  
        - **Branch Name:** Defina um nome relacionado à melhoria aplicada.  
        - **File Path:** Caminho do arquivo a ser analisado (via **get_repo_structure**)  
        - **Commit Message:** Clara e descritiva.  
        - **Improvements:** **Código completo** com todas as melhorias.  
        - **PR Title:** Um título direto e objetivo.  
        - **Token de Autenticação:** {github_token}  


        ---

        ### **Detalhes do autogetfilecontent:**  
        - **Repo Name:** {repo_name}  
        - **File path:** Caminho do arquivo a ser analisado obtido atraves de get_repo_structure
        - **Branch Name:** main 
        - **Company name:** {companyname}  
        - **Github Token:** {github_token}  

        ---
        
        ### **Detalhes do get_repo_structure:**  
        - **Repo Name:** {repo_name}  
        - **Repo Owner:** {companyname}  
        - **Github Token:** {github_token}  
        - **Branch Name:** main  


        ---

        ### **Diretrizes para Geração Automática:**  

        #### **Commit Message:**  
        - **feat:** Para novas funcionalidades.  
        - Exemplo: **feat:** Adiciona autenticação de usuário com OAuth 2.0.  
        - **fix:** Para correções de bugs.  
        - Exemplo: **fix:** Corrige erro na autenticação via API.  
        - **refactor:** Para melhorias sem alteração de comportamento.  
        - Exemplo: **refactor:** Refatora classes para melhorar a legibilidade.

        #### **Título do PR:**  
        - Deve ser direto e refletir a principal melhoria.  
        - Exemplo: **Refatora autenticação de usuário**

        #### **Descrição do PR:**  
        - **Problema:** Explique o problema identificado.  
        - **Solução:** Detalhe as melhorias implementadas.  
        - **Impacto:** Informe como a mudança afeta o sistema.

        #### **Branch Name:**  
        - **feat/nome-da-funcionalidade**  
        - **fix/correcao-do-bug**  
        - **refactor/ajuste-no-codigo**  
        - Exemplo: **fix/authentication-error**

        ---


        ### **Regras Rígidas:**  
        - Sempre **retorne o código completo e atualizado** do arquivo modificado.  
        - Não envie respostas incompletas ou parciais.  
        - Preserve a lógica e a estrutura original do projeto.  
        """

        adxitional_instructions_QuantumCore = f"""
        """
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensagem,
                                                                agent_id=AI_QuantumCore, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_QuantumCore,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_QuantumCore,
                                                                streamflag=False
                                                                )


        # Retorna a resposta com o status da issue e outras informações
        response_message = {
            "issue_number": issue_number,
            "issue_title": issue_title,
            "issue_creator": issue_creator,
            "issue_body": issue_body
        }
        return jsonify(response_message), 200

if __name__ == '__main__':
    app.run(debug=True, port=101)
