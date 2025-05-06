# from softwareai_engine_library.FunctionsAndTools.Functions.autounittests.Submit_Outputs.autounittests import submit_output_autounittests
# from softwareai_engine_library.FunctionsAndTools.Functions.autosave.Submit_Outputs.autosave_submit_outputs import submit_output_autosave
# from softwareai_engine_library.FunctionsAndTools.Functions.autoupload.Submit_Outputs.autoupload_submit_outputs import submit_output_autoupload
# from softwareai_engine_library.FunctionsAndTools.Functions.autocreaterepo.Submit_Outputs.autocreaterepo import submit_output_autocreaterepo
# from softwareai_engine_library.FunctionsAndTools.Functions.autopullrequest.Submit_Outputs.autopullrequest import submit_output_autopullrequest
# from softwareai_engine_library.FunctionsAndTools.Functions.autogetstructure.Submit_Outputs.autogetstructure import submit_output_get_repo_structure
# from softwareai_engine_library.FunctionsAndTools.Functions.autogetfilecontent.Submit_Outputs.autogetfilecontent import submit_output_autogetfilecontent
# from softwareai_engine_library.FunctionsAndTools.Functions.autochangesrequestedinpullrequest.Submit_Outputs.autochangesrequestedinpullrequest import submit_output_autochangesrequestedinpullrequest
# from softwareai_engine_library.FunctionsAndTools.Functions.autoconversationpullrequest.Submit_Outputs.autoconversationissuespullrequest import submit_output_autoconversationissuespullrequest
# from softwareai_engine_library.FunctionsAndTools.Functions.autocreateissue.Submit_Outputs.autocreateissue import submit_output_autocreateissue
# from softwareai_engine_library.FunctionsAndTools.Functions.autoapprovepullrequest.Submit_Outputs.autoapprovepullrequest import submit_output_autoapprovepullrequest
# from softwareai_engine_library.FunctionsAndTools.Functions.send_to_webhook_func.Submit_Outputs.send_to_webhook_func import submit_output_send_to_webhook_func
# from softwareai_engine_library.FunctionsAndTools.Functions.criar_grafico.Submit_Outputs.criar_grafico import submit_output_criar_grafico


# from firebase_admin import App
# from typing import Optional
# import inspect
# # /api/submit-tool-output
# def _init_output_(function_name,
#                   function_arguments,
#                   tool_call,
#                   threead_id,
#                   client,
#                   run,
#                   appfb,
#                 ):
                    

#     functions_to_call = [
#         submit_output_criar_grafico,
#         submit_output_send_to_webhook_func,
#         submit_output_autoapprovepullrequest,
#         submit_output_autounittests,
#         submit_output_autocreateissue,
#         submit_output_autosave,
#         submit_output_autoupload,
#         submit_output_autocreaterepo,
#         submit_output_autopullrequest,
#         submit_output_get_repo_structure,
#         submit_output_autogetfilecontent,
#         submit_output_autochangesrequestedinpullrequest,
#         submit_output_autoconversationissuespullrequest
#     ]

#     # Dicionário com todos os argumentos disponíveis
#     available_args = {
#         "function_name": function_name,
#         "function_arguments": function_arguments,
#         "tool_call": tool_call,
#         "threead_id": threead_id,
#         "client": client,
#         "run": run,
#         "appfb": appfb,             
#     }

#     for func in functions_to_call:
#         # Obter assinatura da função e os parâmetros necessários
#         func_signature = inspect.signature(func)
#         func_parameters = func_signature.parameters

#         # Construir dicionário de argumentos para a função atual
#         func_args = {}
#         missing_args = []

#         for param_name, param in func_parameters.items():
#             if param_name in available_args:
#                 func_args[param_name] = available_args[param_name]
#             elif param.default == inspect.Parameter.empty:
#                 missing_args.append(param_name)

#         # Reportar se há argumentos obrigatórios ausentes
#         if missing_args:
#             print(f"Erro: {func.__name__} faltando argumentos obrigatórios: {missing_args}")
#             continue

#         # Chamar a função
#         try:
#             flag = func(**func_args)
#             if flag:
#                 return True
#         except Exception as e:
#             print(f"Erro ao Chamar a função {func.__name__}: {e}")

#     return False
