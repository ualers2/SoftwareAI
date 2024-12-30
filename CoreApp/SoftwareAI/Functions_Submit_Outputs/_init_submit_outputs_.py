#from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs._submit_outputs import submit_output_
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.pegar_hora_submit_outputs import submit_output_pegar_hora

from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.create_github_repo_and_upload_submit_outputs import submit_output_create_github_repo_and_upload
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.get_current_datetime_submit_outputs import submit_output_get_current_datetime
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.improve_code_and_create_pull_request_submit_outputs import submit_output_improve_code_and_create_pull_request
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.test_software_submit_outputs import submit_output_test_software
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.add_project_map_submit_outputs import submit_output_add_projectmap_to_github
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.analyze_file_outputs import submit_output_analyze_file
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.save_TXT_outputs import submit_output_save_TXT
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.save_code_outputs import submit_output_save_code
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.execute_python_code_outputs import submit_output_execute_python_code
from softwareai.CoreApp.SoftwareAI.Functions_Submit_Outputs.update_readme_outputs import submit_output_update_readme

def _init_output_(function_name,
                function_arguments,
                tool_call,
                threead_id,
                client,
                run):
    
    functions_to_call = [
        submit_output_pegar_hora,
        submit_output_get_current_datetime,
        submit_output_create_github_repo_and_upload,
        submit_output_improve_code_and_create_pull_request,
        submit_output_test_software,
        submit_output_add_projectmap_to_github,
        submit_output_analyze_file,
        submit_output_save_TXT,
        submit_output_save_code,
        submit_output_execute_python_code,
        submit_output_update_readme
    ]
    
    for func in functions_to_call:
        if func == submit_output_get_current_datetime:
            flag = func(function_name, function_arguments, tool_call, threead_id, client, run)
            if flag:
                return True
        else:
            func(function_name, function_arguments, tool_call, threead_id, client, run)