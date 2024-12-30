
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *




class QProcessCreateVectorStoreByUser(QThread):
    vectorsignal = Signal(str)
    ModalSucess = Signal(str)
    ModalInfo = Signal(str)

    def __init__(self,
                selected_files,
                app1,
                client
            ):
        
        self.selected_files = selected_files
        self.app1 = app1
        self.client = client
        super().__init__()

    def run(self):
        name_for_vectorstore = "VectorStoreByUser1"
        self.ModalInfo.emit(f"Naming the vector store {name_for_vectorstore}")
        file_paths = self.selected_files
        try:
            ref1 = db.reference(f'ai_org_vector_store/User_{name_for_vectorstore}', app=self.app1)
            data1 = ref1.get()
            vector_store_id = data1['vector_store_id']
            self.ModalInfo.emit(f"Vector store already exists")
            for update1newfiles in file_paths:
                self.ModalInfo.emit(f"Uploading the to the vector store")

                update1newfile = open(update1newfiles, "rb")
                self.client.beta.vector_stores.files.upload(
                    vector_store_id=vector_store_id, file=update1newfile
                )
                self.ModalSucess.emit(f"Uploaded to the vector store")
                
            self.ModalSucess.emit(f"Vector store authenticated successfully")
            self.vectorsignal.emit(str(vector_store_id)) 

        except Exception as err:
            print(err)
            self.ModalInfo.emit(f"Vector store does not exist creating..")
            vector_store = self.client.beta.vector_stores.create(name=name_for_vectorstore)
            self.ModalSucess.emit(f"Vector store has been created {vector_store.id}")

            
            self.ModalInfo.emit(f"Uploading files to vector storage")

            file_streams = [open(path, "rb") for path in file_paths]
            self.client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id=vector_store.id, files=file_streams
            )
            self.ModalSucess.emit(f"Uploaded to the vector store")

            self.ModalInfo.emit(f"Storing Vector Store in firebase")
            ref1 = db.reference(f'ai_org_vector_store', app=self.app1)
            controle_das_funcao2 = f"User_{name_for_vectorstore}"
            controle_das_funcao_info_2 = {
                "name_for_vectorstore": f'{name_for_vectorstore}',
                "vector_store_id": f'{vector_store.id}'
            }
            ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)
            self.ModalSucess.emit(f"Vector Store was stored on Firebase")
            self.ModalSucess.emit(f"Vector store authenticated successfully")
            self.vectorsignal.emit(vector_store.id)  
