
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Functions
from softwareai.CoreApp.SoftwareAI.Functions._init_functions_ import *
#########################################

def submit_output_test_software(function_name,
                                function_arguments,
                                tool_call,
                                threead_id,
                                client,
                                run
                                ):

    if function_name == 'test_software':
        args = json.loads(function_arguments)
        report = test_software(
            test_file_path=args['test_file_path'],
            repo_owner=args['repo_owner'],
            repo_name=args['repo_name'],
            branch_name=args['branch_name'],
            file_path=args['file_path'],
            token=args['token']
        )
        tool_call_id = tool_call.id  
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=threead_id,
            run_id=run.id,
            tool_outputs=[
                {
                    "tool_call_id": tool_call_id, 
                    "output": json.dumps(report)  
                }
            ]
        )

