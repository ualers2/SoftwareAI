
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Functions
from softwareai.CoreApp.SoftwareAI.Functions._init_functions_ import *
#########################################

def submit_output_create_github_repo_and_upload(function_name,
                                function_arguments,
                                tool_call,
                                threead_id,
                                client,
                                run
                                ):


    if function_name == 'create_github_repo_and_upload':
        args = json.loads(function_arguments)
        result = create_github_repo_and_upload(
            repo_name=args['repo_name'],
            repo_description=args['repo_description'],
            setup_file_path=args['setup_file_path'],
            requirements_file_path=args['requirements_file_path'],
            LICENSE_file_path=args['LICENSE_file_path'],
            pyproject_file_path=args['pyproject_file_path'],
            
            readme_file_path=args['readme_file_path'],
            CoreApp_path=args['CoreApp_path'],
            token=args['token']
        )
        tool_call_id = tool_call.id
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=threead_id,
            run_id=run.id,
            tool_outputs=[
                {
                    "tool_call_id": tool_call_id, 
                    "output": json.dumps(result)  
                }
            ]
        )


