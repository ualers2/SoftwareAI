
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Functions
from softwareai.CoreApp.SoftwareAI.Functions._init_functions_ import *
#########################################


def submit_output_improve_code_and_create_pull_request(function_name,
                                function_arguments,
                                tool_call,
                                threead_id,
                                client,
                                run
                                ):


    if function_name == 'improve_code_and_create_pull_request':
        args = json.loads(function_arguments)
        result = improve_code_and_create_pull_request(
            repo_owner=args['repo_owner'],
            repo_name=args['repo_name'],
            branch_name=args['branch_name'],
            file_path=args['file_path'],
            commit_message=args['commit_message'],
            improvements=args['improvements'],
            pr_title=args['pr_title'],
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

