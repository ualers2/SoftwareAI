
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Functions
from softwareai.CoreApp.SoftwareAI.Functions._init_functions_ import *
#########################################

def submit_output_add_projectmap_to_github(function_name,
                                function_arguments,
                                tool_call,
                                threead_id,
                                client,
                                run
                                ):


    if function_name == 'add_projectmap_to_github':
        args = json.loads(function_arguments)
        result = add_projectmap_to_github(
            timeline_file_path=args['timeline_file_path'],
            spreadsheet_file_path=args['spreadsheet_file_path'],
            pre_project_file_path=args['pre_project_file_path'],
            Roadmap_file_path=args['Roadmap_file_path'],
            analise_file_path=args['analise_file_path'],
            repo_name=args['repo_name'],
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


