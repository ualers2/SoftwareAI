
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Functions
from softwareai.CoreApp._init_functions_ import *
#########################################

tool_outputs = []
def submit_output_checkcommentspr(function_name,
                                function_arguments,
                                tool_call,
                                threead_id,
                                client,
                                run
                                ):
    global tool_outputs
    
    if function_name == 'autocheckcommentspr':
        args = json.loads(function_arguments)
        result = autocheckcommentspr(
            OWNER=args['OWNER'],
            REPO=args['REPO'],
            PR_NUMBER=args['PR_NUMBER'],
            github_token=args['github_token']
        )
        tool_outputs.append({
        "tool_call_id": tool_call.id,
        "output": json.dumps(result)
        })
        
        # Submit all tool outputs at once after collecting them in a list
        if tool_outputs:
            try:
                run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=threead_id,
                run_id=run.id,
                tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
                tool_outputs = []
                return True
            except Exception as e:
                print("Failed to submit tool outputs:", e)
        else:
            print("No tool outputs to submit.")
