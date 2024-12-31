
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
            PATH_SOFTWARE_DEVELOPMENT_init_ENV=args['PATH_SOFTWARE_DEVELOPMENT_init_ENV'],
            PATH_SOFTWARE_DEVELOPMENT_PY_ENV=args['PATH_SOFTWARE_DEVELOPMENT_PY_ENV'],
            PATH_SOFTWARE_DEVELOPMENT_config_ENV=args['PATH_SOFTWARE_DEVELOPMENT_config_ENV'],
            PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV=args['PATH_SOFTWARE_DEVELOPMENT_utils___init___ENV'],
            PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV=args['PATH_SOFTWARE_DEVELOPMENT_utils_file_utils_ENV'],
            PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV=args['PATH_SOFTWARE_DEVELOPMENT_modules___init___ENV'],
            PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV=args['PATH_SOFTWARE_DEVELOPMENT_modules_module1_ENV'],
            PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV=args['PATH_SOFTWARE_DEVELOPMENT_modules_module2_ENV'],
            PATH_SOFTWARE_DEVELOPMENT_services___init___ENV=args['PATH_SOFTWARE_DEVELOPMENT_services___init___ENV'],
            PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV=args['PATH_SOFTWARE_DEVELOPMENT_services_service1_ENV'],
            PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV=args['PATH_SOFTWARE_DEVELOPMENT_services_service2_ENV'],
            PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV=args['PATH_SOFTWARE_DEVELOPMENT_tests___init___ENV'],
            PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV=args['PATH_SOFTWARE_DEVELOPMENT_tests_test_module1_ENV'],
            PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV=args['PATH_SOFTWARE_DEVELOPMENT_tests_test_module2_ENV'],
            PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV=args['PATH_SOFTWARE_DEVELOPMENT_tests_test_service1_ENV'],
            PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV=args['PATH_SOFTWARE_DEVELOPMENT_tests_test_service2_ENV'],
            PATH_SOFTWARE_DEVELOPMENT_Example_ENV=args['PATH_SOFTWARE_DEVELOPMENT_Example_ENV'],
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


