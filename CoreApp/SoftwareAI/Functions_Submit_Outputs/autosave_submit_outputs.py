
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Functions
from softwareai.CoreApp._init_functions_ import *
#########################################

def submit_output_autosave(function_name,
                                function_arguments,
                                tool_call,
                                threead_id,
                                client,
                                run
                                ):

    if function_name == 'autosave':
        args = json.loads(function_arguments)     
        result = autosave(
                code=args['code'],
                path=args['path']
                )

        try:
            run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=threead_id,
            run_id=run.id,
            tool_outputs=[{
            "tool_call_id": tool_call.id,
            "output": json.dumps(result)
            }]
            )
            print("Tool outputs submitted successfully.")
            return True
        except Exception as e:
            print("Failed to submit tool outputs:", e)

    # if function_name == 'autosave':
    #     args = json.loads(function_arguments)
    #     result = autosave(
    #         code=args['code'],
    #         path=args['path']
    #     )
    #     tool_call_id = tool_call.id
    #     client.beta.threads.runs.submit_tool_outputs(
    #         thread_id=threead_id,
    #         run_id=run.id,
    #         tool_outputs=[
    #             {
    #                 "tool_call_id": tool_call_id, 
    #                 "output": json.dumps(result)  
    #             }
    #         ]
    #     )