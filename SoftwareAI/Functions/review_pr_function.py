

#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import *
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################

def merge_pull_request(repo_owner: str, repo_name: str, pr_number: int, token: str):
    """
    Faz o merge de um pull request aprovado com a branch principal.
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Obter as informações do PR
    pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    pr_response = requests.get(pr_url, headers=headers)

    if pr_response.status_code != 200:
        print(f"Erro ao buscar PR. Status: {pr_response.status_code}")
        return {"status": "error", "message": pr_response.json()}

    pr_data = pr_response.json()

    # Verificar se o pull request foi aprovado
    if pr_data['mergeable'] is False:
        return {"status": "error", "message": "Pull request não está pronto para merge."}

    # Fazer o merge do pull request
    merge_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/merge"
    merge_data = {
        "commit_title": f"Merge PR #{pr_number}: {pr_data['title']}",
        "commit_message": "Merge realizado automaticamente pelo QuantumCore.",
        "merge_method": "merge"  # ou 'squash' ou 'rebase', se preferir outros métodos de merge
    }

    merge_response = requests.put(merge_url, json=merge_data, headers=headers)

    if merge_response.status_code == 200:
        print("Merge realizado com sucesso!")
        return {"status": "merged", "message": "Pull request foi mergeado com sucesso."}
    else:
        print(f"Erro ao fazer merge. Status: {merge_response.status_code}")
        return {"status": "error", "message": merge_response.json()}
    
def quantumcore_review_pr(repo_owner: str, repo_name: str, pr_number: int):
    """
    QuantumCore analisa o pull request e decide se aprova ou solicita mais melhorias.
    """

    instructionQuantumCore = """ 
    Seu nome é QuantumCore, você é um Desenvolvedor Pleno em Python na empresa urobotsoftware. Sua principal responsabilidade é desenvolver software de alta qualidade com base nos requisitos fornecidos pelo Analista de Requisitos de Software e nos padrões de software já existentes na empresa, que foram upados via vectorstore.

    ### Responsabilidades:

    1. **Recepção do Arquivo:**
    - Receber e revisar o arquivo contendo a análise de requisitos de software, que inclui tanto os requisitos funcionais quanto os não funcionais.
    - Assegurar-se de que todos os requisitos estejam claramente documentados e que não existam ambiguidades que possam impactar o desenvolvimento.

    2. **Análise de Requisitos:**
    - Compreender detalhadamente todos os requisitos especificados no documento, incluindo funcionalidades, desempenho, segurança, escalabilidade e outras características críticas do software a ser desenvolvido.
    - Utilizar o **vectorstore** para verificar os padrões já implementados em softwares anteriores da empresa, assegurando a consistência com os requisitos e boas práticas internas.
    - Identificar áreas que necessitem de esclarecimento ou detalhamento adicional e comunicar-se proativamente com o Analista de Requisitos de Software.

    3. **Planejamento do Desenvolvimento:**
    - Dividir os requisitos em tarefas de desenvolvimento claras e gerenciáveis, priorizando-as conforme a complexidade e dependências.
    - Estabelecer um cronograma detalhado para o desenvolvimento das funcionalidades, alinhando-o com o cronograma do projeto fornecido e garantindo a alocação eficiente do tempo e recursos.
    - Selecionar as tecnologias, frameworks e bibliotecas Python mais adequadas para o desenvolvimento, levando em consideração o que já foi utilizado e validado pela empresa, conforme armazenado no **vectorstore**.

    4. **Implementação do Software:**
    - Desenvolver o software de acordo com os requisitos funcionais e não funcionais, aplicando boas práticas de programação Python, incluindo Clean Code, modularidade, reutilização de código e aderência a padrões de codificação (PEP 8).
    - Consultar o **vectorstore** para reutilizar módulos ou padrões existentes, sempre que aplicável, garantindo consistência e eficiência.
    - Implementar testes unitários e de integração para garantir a robustez e qualidade do software durante todo o ciclo de desenvolvimento.
    - Utilizar controle de versão (Git) de maneira eficiente.

    5. **Documentação do Código:**
    - Documentar o código desenvolvido de forma clara e concisa, e manter consistência com a documentação de projetos anteriores, conforme os padrões armazenados no **vectorstore**.
    - Criar e manter documentação técnica abrangente, incluindo arquivos README (.md) e outros documentos relevantes.

    6. **Colaboração com Outros Membros da Equipe:**
    - Trabalhar em colaboração com o Analista de Requisitos, Testadores de Software e outros desenvolvedores, assegurando a aderência aos padrões internos.

    7. **Entrega do Software:**
    - Preparar o software para entrega, incluindo builds finais, criação de pacotes Python e configuração do ambiente de produção, automatizando o processo sempre que possível.

    8. **Resolução de Problemas:**
    - Identificar, diagnosticar e resolver problemas ou bugs durante o desenvolvimento, propondo melhorias baseadas em soluções anteriores armazenadas no **vectorstore**.

    9. **Criação e Upload no GitHub:**
    - Criar um repositório no GitHub para o projeto.
    - Fazer o upload da documentação (.md) e dos arquivos de código Python para o repositório recém-criado, assegurando que a estrutura do repositório esteja organizada e a documentação esteja atualizada.

    ### Formato de Resposta:

    Responda no formato JSON conforme o exemplo abaixo:
    ```json
    {
        "status_do_desenvolvimento": "Progresso conforme o planejado",
        "tarefas_completas": [
            "Implementação da funcionalidade de autenticação de usuários",
            "Criação de testes unitários para o módulo de autenticação",
            "Documentação do código para a funcionalidade de autenticação"
        ],
        "pendencias": [
            "Clarificação necessária para o requisito de segurança adicional",
            "Aprovação do design da API pelo Analista de Requisitos"
        ],
        "proximas_tarefas": [
            "Início da integração com o sistema de pagamentos",
            "Teste de desempenho para a funcionalidade de processamento de pedidos"
        ],
        "observacoes": "Nenhum impedimento significativo até o momento. Desenvolvimento dentro do prazo."
    }
    """
    key = "AI_QuantumCore_Desenvolvedor_Pleno_de_Software_em_Python"
    nameassistant = "AI QuantumCore Desenvolvedor Pleno de Software em Python"
    model_select = "gpt-4o-mini-2024-07-18"
    adxitional_instructions = None
    tools=[
        {"type": "file_search"},
        {
            "type": "function",
            "function": {
                "name": "create_github_repo_and_upload",
                "description": "Cria um repositório no GitHub e realiza o upload da documentação (.md) e do código Python.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "repo_name": {
                            "type": "string",
                            "description": "Nome do repositório a ser criado no GitHub."
                        },
                        "repo_description": {
                            "type": "string",
                            "description": "Descrição do repositório."
                        },
                        "readme_file_path": {
                            "type": "string",
                            "description": "Caminho do arquivo .md (README) a ser carregado no repositório."
                        },
                        "code_file_paths": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            },
                            "description": "Lista de caminhos dos arquivos de código Python a serem carregados no repositório."
                        },
                        "token": {
                            "type": "string",
                            "description": "Token de autenticação do GitHub para realizar operações na API."
                        }
                    },
                    "required": ["repo_name", "repo_description", "readme_file_path", "code_file_paths", "token"]
                }
            }
        }
    ]

    Upload_1_file_in_thread = None
    Upload_1_file_in_message = None
    Upload_1_image_for_vision_in_thread = None
    vectorstore_in_assistant = None
    vectorstore_in_Thread = None

    github_username, github_token = Github_functions.QuantumCore_github_keys()


    
    AI_QuantumCore = AutenticateAgent.create_or_auth_AI(key, instructionQuantumCore, nameassistant, model_select, tools, vectorstore_in_assistant)
    
    

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Buscar informações do pull request
    pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"
    pr_response = requests.get(pr_url, headers=headers)

    if pr_response.status_code != 200:
        print(f"Erro ao buscar PR. Status: {pr_response.status_code}")
        return {"status": "error", "message": pr_response.json()}

    pr_data = pr_response.json()

    # Analisar o código no pull request
    code_url = pr_data['commits_url']
    commits_response = requests.get(code_url, headers=headers)
    if commits_response.status_code != 200:
        print(f"Erro ao buscar commits. Status: {commits_response.status_code}")
        return {"status": "error", "message": commits_response.json()}

    commits_data = commits_response.json()
    improvements = ""
    
    # Iterar pelos commits e realizar a análise
    for commit in commits_data:
        commit_message = commit['commit']['message']
        commit_url = commit['url']

        # Fazer a análise de melhoria via QuantumCore
        analysis_message = f"""
        Analisar este commit e decidir se o código está adequado ou se requer melhorias:
        Commit: {commit_message}
        URL: {commit_url}
        """
        response = ResponseAgent.ResponseAgent_message_with_assistants(analysis_message, Upload_1_file_in_thread, Upload_1_file_in_message, Upload_1_image_for_vision_in_thread, vectorstore_in_Thread, tools, AI_QuantumCore, model_select, adxitional_instructions, key)
        print(response)
        
        mensaxgem = f""" com base nessa analize responda a decisao de aprovar ou rejeitar o pull request 
        {response}\n
        caso a decisao seja rejeitar pull request sugira melhorias e motivos da rejeicao 
        """
        format = 'Responda a decisao de sim ou nao no formato JSON Exemplo: {"decisao": "sim ou nao..."}'
        mensagem = mensaxgem + format
        response = ResponseAgent.ResponseAgent_message_completions(mensagem, "", True)
        JSONformat = response["decisao"]
        if JSONformat == "sim":
            pass
        else:
            improvements += JSONformat

    if improvements:
        print("QuantumCore encontrou melhorias necessárias.")
        return {
            "status": "improvement_needed",
            "message": improvements
        }
    else:
        review_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/reviews"
        review_data = {
            "body": f"""Aprovado por QuantumCore.\n 
                    {response}
            """,
            "event": "APPROVE"
        }
        review_response = requests.post(review_url, json=review_data, headers=headers)
        if review_response.status_code == 200:
            print("Pull request aprovado com sucesso!")
            resultado = merge_pull_request(repo_owner, repo_name, pr_number, github_token)
            return {"status": "approved", "message": f"Pull request aprovado com sucesso. {resultado}"}
        else:
            print(f"Erro ao aprovar o PR. Status: {review_response.status_code}")
            return {"status": "error", "message": review_response.json()}
    



