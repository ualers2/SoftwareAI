
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Functions
from softwareai.CoreApp._init_functions_ import *
#########################################

def submit_output_create_repo(function_name,
                                function_arguments,
                                tool_call,
                                threead_id,
                                client,
                                run
                                ):


    if function_name == 'create_repo':
        args = json.loads(function_arguments)
        result = create_repo(
            repo_name=args['repo_name'],
            description=args['description'],
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


