
#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import *
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################


def run_tests(test_file_path):
    """Executa os testes no arquivo .py especificado e retorna o resultado detalhado."""
    try:
        # Executa os testes usando pytest e captura a saída
        result = subprocess.run(['pytest', test_file_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            # Testes foram executados com sucesso
            return {
                'output': result.stdout,
                'error': result.stderr,
                'success': True
            }
        else:
            # Houve falhas na execução dos testes
            return {
                'output': result.stdout,
                'error': result.stderr,
                'success': False
            }

    except Exception as e:
        # Captura qualquer exceção que possa ocorrer
        print(f"Ocorreu um erro ao executar os testes: {str(e)}")
        return {
            'output': None,
            'error': str(e),
            'success': False
        }

def generate_test_report(test_file_path):
    """Gera um relatório detalhado dos testes executados."""
    test_results = run_tests(test_file_path)
    
    report = {
        'test_file': test_file_path,
        'timestamp': datetime.now().isoformat(),
        'status': 'success' if test_results['success'] else 'failure'
    }
    
    if test_results['success']:
        report['details'] = test_results['output'] + test_results['error'] 
    else:
        report['details'] = test_results['error'] if test_results['error'] else test_results['output']
    
    return report

def save_test_report_to_pull_request(report, file_path, repo_owner, repo_name, branch_name, token):
    """Salva o relatório de teste em um pull request no GitHub."""

    file_pathRelatório = "Work_Environment/Create_Testing_in_Software_Development/Testing_in_Software.txt"
    with open(file_pathRelatório, 'w') as json_file:
        json.dump(report, json_file, indent=4)
    print(f"Relatório de teste salvo no arquivo {file_pathRelatório}")

    # Converta o relatório para JSON
    report_json = json.dumps(report, indent=4)

    # Verificar se o branch principal existe (ex: 'main')
    repo_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/heads/main"
    response = requests.get(repo_url, headers={'Authorization': f'token {token}'})

    if response.status_code == 404:  # Branch principal não existe
        print("Branch 'main' não encontrado. Criando branch 'main' a partir de um commit inicial.")

        # Criar um commit inicial vazio
        create_commit_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/commits"
        commit_data = {
            "message": "Initial commit",
            "tree": "",
            "parents": []
        }
        response = requests.post(create_commit_url, headers={'Authorization': f'token {token}'}, json=commit_data)
        if response.status_code != 201:
            print(f"Erro ao criar commit inicial: {response.content}")
            return
        commit_sha = response.json()['sha']

        # Criar o branch 'main' usando o commit inicial
        create_branch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs"
        branch_data = {
            "ref": "refs/heads/main",
            "sha": commit_sha
        }
        response = requests.post(create_branch_url, headers={'Authorization': f'token {token}'}, json=branch_data)
        if response.status_code != 201:
            print(f"Erro ao criar o branch 'main': {response.content}")
            return
        print("Branch 'main' criado com sucesso.")

    # Crie um novo branch baseado no branch principal
    response = requests.get(repo_url, headers={'Authorization': f'token {token}'})
    main_sha = response.json().get('object', {}).get('sha')

    if not main_sha:
        print("Erro ao obter SHA do branch principal.")
        return
    randomnumber = random.randint(1, 175)
    branch_name = f"{branch_name}_{randomnumber}"
    print(branch_name)
    new_branch_data = {
        "ref": f"refs/heads/{branch_name}",
        "sha": main_sha
    }
    create_branch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs"
    response = requests.post(create_branch_url, headers={'Authorization': f'token {token}'}, json=new_branch_data)
    if response.status_code != 201:
        print(f"Erro ao criar o branch: {response.content}")

        # Crie um novo branch baseado no branch principal
        response = requests.get(repo_url, headers={'Authorization': f'token {token}'})
        main_sha = response.json().get('object', {}).get('sha')

        if not main_sha:
            print("Erro ao obter SHA do branch principal.")
            return
        randomnumber = random.randint(1, 175)
        branch_name = f"{branch_name}_{randomnumber}"
        print(branch_name)
        new_branch_data = {
            "ref": f"refs/heads/{branch_name}",
            "sha": main_sha
        }
        create_branch_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs"
        response = requests.post(create_branch_url, headers={'Authorization': f'token {token}'}, json=new_branch_data)
        if response.status_code != 201:
            print(f"Erro ao criar o branch: {response.content}")
            return
        
    # Adicionar o arquivo ao novo branch
    create_file_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
    commit_message = f"Test software report {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    content_base64 = base64.b64encode(report_json.encode()).decode()

    file_data = {
        "message": commit_message,
        "content": content_base64,
        "branch": branch_name
    }

    response = requests.put(create_file_url, headers={'Authorization': f'token {token}'}, json=file_data)
    if response.status_code not in [201, 200]:
        print(f"Erro ao adicionar o arquivo: {response.content}")
        return

    # Criar um pull request para o branch criado
    prompt = f"""Crie um relatorio completo para o pull request com base nesses testes:\n
    {report_json}
      
    """
    formato = """Responda no formato JSON
    Exemplo:
    {"resposta": "resposta ..."}"""
    promptt = prompt + formato

    pullrequestsreport = ResponseAgent.ResponseAgent_message_completions(promptt, "", True)
    print(pullrequestsreport)
    try:
        resposta = pullrequestsreport["resposta"]
    except:
        resposta = pullrequestsreport

    create_pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    pr_data = {
        "title": "Test software report",
        "body": f"""{resposta} \n {report_json}""",
        "head": branch_name,
        "base": "main"
    }
    response = requests.post(create_pr_url, headers={'Authorization': f'token {token}'}, json=pr_data)
    if response.status_code == 201:
        print("Pull request criado com sucesso.")
    else:
        print(f"Erro ao criar o pull request: {response.content}")

def test_software(test_file_path, repo_owner, repo_name, branch_name, file_path, token):
    """Executa testes de software, gera um relatório detalhado e salva em um Pull Request no GitHub."""
    report = generate_test_report(test_file_path)
    save_test_report_to_pull_request(report, file_path, repo_owner, repo_name, branch_name, token)
    return report

def handle_test_software(test_file_path, repo_owner, repo_name, branch_name, file_path, token):
    """Função manipuladora para executar os testes e retornar o relatório."""
    report = test_software(test_file_path, repo_owner, repo_name, branch_name, file_path, token)
    return {"report": report}

def submit_test_results(client, thread_id, run_id, test_report, function_name):
    """
    Envia os resultados dos testes para a API da OpenAI usando a chamada de função.

    :param client: Instância do cliente da API da OpenAI
    :param thread_id: ID da thread em execução
    :param run_id: ID do run específico
    :param test_report: Dicionário contendo os resultados dos testes
    """
   
    function_data = {
        "thread_id": thread_id,
        "run_id": run_id,
        "test_report": test_report
    }

    response = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread_id,
        run_id=run_id,
        tool_output={
            "function_name": function_name,
            "arguments": json.dumps(function_data)
        }
    )

    if response.status == "success":
        print("Resultados dos testes enviados com sucesso.")
    else:
        print(f"Erro ao enviar resultados dos testes: {response}")
