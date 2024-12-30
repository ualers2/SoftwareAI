
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Functions
from softwareai.CoreApp.SoftwareAI.Functions._init_functions_ import *
#########################################

tool_outputs = []
def submit_output_update_readme(function_name,
                                function_arguments,
                                tool_call,
                                threead_id,
                                client,
                                run
                                ):

    # if function_name == 'update_readme_to_github':
    #     args = json.loads(function_arguments)
    #     report = update_readme_to_github(
    #         file_path_readme_improvements=args['file_path_readme_improvements'],
    #         repo_name=args['repo_name'],
    #         token=args['token']
    #     )
    #     tool_call_id = tool_call.id  
    #     client.beta.threads.runs.submit_tool_outputs(
    #         thread_id=threead_id,
    #         run_id=run.id,
    #         tool_outputs=[
    #             {
    #                 "tool_call_id": tool_call_id, 
    #                 "output": json.dumps(report)  
    #             }
    #         ]
    #     )

    global tool_outputs
    if function_name == 'update_readme_to_github':
        args = json.loads(function_arguments)
        resultado = update_readme_to_github(
            file_path_readme_improvements=args['file_path_readme_improvements'],
            repo_name=args['repo_name'],
            token=args['token']
        )
        tool_outputs.append({
        "tool_call_id": tool_call.id,
        "output": json.dumps(resultado)  
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