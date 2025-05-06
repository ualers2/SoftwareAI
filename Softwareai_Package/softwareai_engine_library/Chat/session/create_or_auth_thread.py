# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
def create_or_auth_thread(
                        client,
                        appcompany,
                        file_ids_to_upload: Optional[List] = None,
                        code_interpreter_in_thread: Optional[List] = None,
                        user_id: Optional[str] = None
                        
                        ):

            
        try:
            ref1 = db.reference(f'ai_org_thread_Id/User_{user_id}', app=appcompany)
            data1 = ref1.get()
            thread_Id = data1['thread_id']
            print(thread_Id)
            # try:
            #     vector_store_id = data1['vector_store_id']

            #     if file_ids_to_upload is not None:
            #         batch = client.vector_stores.file_batches.create_and_poll(
            #             vector_store_id=vector_store_id,
            #             file_ids=file_ids_to_upload
            #         )

            #         client.beta.threads.update(
            #             thread_id=str(thread_Id),
            #             tool_resources={
            #                 "file_search": {
            #                 "vector_store_ids": [vector_store_id]
            #                 }
            #             }
            #         )

            # except Exception as err2342z:
            #     print(f"err2342z {err2342z}")
                
            return str(thread_Id)
        except Exception as err234z:
            # print(err234z)
            # tool_resources = {}
            # if file_ids_to_upload is not None:
            #     vector_store = client.vector_stores.create(
            #         name=f"{user_id}",
            #         file_ids=file_ids_to_upload
            #     )

            #     tool_resources["file_search"] = {"vector_store_ids": [vector_store.id]}
            #     thread = client.beta.threads.create(
            #         tool_resources=tool_resources
            #     )
            #     ref1 = db.reference(f'ai_org_thread_Id', app=appcompany)
            #     controle_das_funcao2 = f"User_{user_id}"
            #     controle_das_funcao_info_2 = {
            #         "thread_id": f'{thread.id}',
            #         "user_id": f'{user_id}',
            #         "vector_store_id": f"{vector_store.id}"
            #     }
            #     ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)

            #     return str(thread.id)

            # else:
                thread = client.beta.threads.create()
                ref1 = db.reference(f'ai_org_thread_Id', app=appcompany)
                controle_das_funcao2 = f"User_{user_id}"
                controle_das_funcao_info_2 = {
                    "thread_id": f'{thread.id}',
                    "user_id": f'{user_id}',

                }
                ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)

                return str(thread.id)
