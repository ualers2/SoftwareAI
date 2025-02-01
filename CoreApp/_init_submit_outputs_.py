
# from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.pegar_hora_submit_outputs import submit_output_pegar_hora

# from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.upload_project_py_submit_outputs import submit_output_upload_project_py
# from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.get_current_datetime_submit_outputs import submit_output_get_current_datetime
# from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.improve_code_and_create_pull_request_submit_outputs import submit_output_improve_code_and_create_pull_request
# from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.test_software_submit_outputs import submit_output_test_software
# from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.add_project_map_submit_outputs import submit_output_add_projectmap_to_github
# from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.analyze_file_outputs import submit_output_analyze_file
# from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.save_TXT_outputs import submit_output_save_TXT
# from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.save_code_outputs import submit_output_save_code
# from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.execute_py_outputs import submit_output_execute_py
# from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.update_readme_outputs import submit_output_update_readme
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.autosave_submit_outputs import submit_output_autosave
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.autoupload_submit_outputs import submit_output_autoupload
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.create_repo_submit_outputs import submit_output_create_repo
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.autopullrequest import submit_output_autopullrequest
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.autoupdaterepo import submit_output_autoupdaterepo
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.autogetstructure import submit_output_get_repo_structure
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.autogetfilecontent import submit_output_autogetfilecontent
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.autocheckcommentspr import submit_output_checkcommentspr
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.Software_Support.TicketProblem import submit_output_TicketProblem
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.Software_Technical_Support.AutoGetLoggerUser import submit_output_AutoGetLoggerUser
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.Software_Development_Testing.AutoTestModule import submit_output_AutoTestModule

from firebase_admin import App
from typing import Optional

import inspect
from typing import Optional

def _init_output_(function_name,
                  function_arguments,
                  tool_call,
                  threead_id,
                  client,
                  run,
                  appfb,
                  OpenAIKeysinit,
                  OpenAIKeysteste,
                  GithubKeys,
                  python_functions,
                  Agent_files_update,
                  AutenticateAgent,
                  ResponseAgent,
                  app_product: Optional[App] = None):
    

    functions_to_call = [
        
        submit_output_autosave,
        submit_output_autoupload,
        submit_output_create_repo,
        submit_output_autopullrequest,
        submit_output_autoupdaterepo,
        submit_output_get_repo_structure,
        submit_output_autogetfilecontent,
        submit_output_checkcommentspr,
        submit_output_TicketProblem,
        submit_output_AutoGetLoggerUser,
        submit_output_AutoTestModule,
    ]

    # Dicionário com todos os argumentos disponíveis
    available_args = {
        "function_name": function_name,
        "function_arguments": function_arguments,
        "tool_call": tool_call,
        "threead_id": threead_id,
        "client": client,
        "run": run,
        "appfb": appfb,             
        "OpenAIKeysteste": OpenAIKeysteste,
        "OpenAIKeysinit": OpenAIKeysinit,
        "GithubKeys": GithubKeys,
        "python_functions": python_functions,
        "Agent_files_update": Agent_files_update,
        "AutenticateAgent": AutenticateAgent,
        "ResponseAgent": ResponseAgent,
        "appproduct": app_product,  # Incluindo o sinônimo
        "app_product": app_product  # Garantia para nomes alternativos
    }

    for func in functions_to_call:
        # Obter assinatura da função e os parâmetros necessários
        func_signature = inspect.signature(func)
        func_parameters = func_signature.parameters

        # Construir dicionário de argumentos para a função atual
        func_args = {}
        missing_args = []

        for param_name, param in func_parameters.items():
            if param_name in available_args:
                func_args[param_name] = available_args[param_name]
            elif param.default == inspect.Parameter.empty:
                missing_args.append(param_name)

        # Reportar se há argumentos obrigatórios ausentes
        if missing_args:
            print(f"Erro: {func.__name__} faltando argumentos obrigatórios: {missing_args}")
            continue

        # Chamar a função
        try:
            flag = func(**func_args)
            if flag:
                return True
        except Exception as e:
            print(f"Erro ao Chamar a função {func.__name__}: {e}")

    return False
