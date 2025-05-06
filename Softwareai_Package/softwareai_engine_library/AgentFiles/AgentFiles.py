#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################


class Agent_files:
    """
    Provides methods to authenticate, create, and manage vector stores for agents,
    including uploading files, retrieving stored file lists, and setting up new or existing stores.
    """

    def auth_vectorstoreAdvanced(app1, client, name_for_vectorstore, file_paths=None):
        """
        Uploads multiple files to an existing Vector Store or creates a new one if it doesn't exist.

        Parameters:
        - name_for_vectorstore (str): The name of the vector store.
        - file_paths (list): A list of file paths to be uploaded.

        Returns:
        - str: The ID of the created or updated vector store.

        Raises:
        - Exception: If there is an error during the upload process.

        Example:
        ```python
        example of how to use the auth_vectorstoreAdvanced function...
        ```

        Note:
        - This function handles both existing and new vector stores based on the existence of the vector store with the given name.
        - It uses the `beta` API endpoint for uploading files and handling batch uploads.
        - If the vector store does not exist, it creates a new one and updates the database reference accordingly.
        """


        try:
            ref1 = db.reference(f'ai_org_vector_store/User_{name_for_vectorstore}', app=app1)
            data1 = ref1.get()
            vector_store_id = data1['vector_store_id']
            if file_paths is not None:
                for file in file_paths:
                    update1newfile = open(file, "rb")
                    client.beta.vector_stores.files.upload(
                        vector_store_id=vector_store_id, file=update1newfile
                    )
            return str(vector_store_id)
        except Exception as err:
            print(err)
            vector_store = client.beta.vector_stores.create(name=name_for_vectorstore)
            if file_paths is not None:
                file_streams = [open(path, "rb") for path in file_paths]
                client.beta.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=vector_store.id, files=file_streams
                )
            ref1 = db.reference(f'ai_org_vector_store', app=app1)
            controle_das_funcao2 = f"User_{name_for_vectorstore}"
            controle_das_funcao_info_2 = {
                "name_for_vectorstore": f'{name_for_vectorstore}',
                "vector_store_id": f'{vector_store.id}'
            }
            ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)
            return vector_store.id

    def auth_or_upload_multiple_files(app1, client, name_for: str, list_files_path: list):
        """
        This function attempts to retrieve a list of file IDs from the database under the key 'auth_or_upload_multiple_files/User_{name_for}'.

        Parameters:
        -----------
        name_for : str
            The name associated with the user's data in the database.
        list_files_path : list
            A list of file paths that need to be uploaded.

        Returns:
        --------
        list
            A list of file IDs if the data retrieval is successful, otherwise, it uploads the files and returns the list of file IDs.

        Raises:
        -------
        Exception
            If there is an error during the retrieval or upload process.

        Example:
        --------
        ```python
        file_paths = ['file1.txt', 'file2.txt']
        file_ids = auth_or_upload_multiple_files('user123', file_paths)
        print(file_ids)  # Output: [file_id1, file_id2]
        ```

        Note:
        -----
        - This function uses the `db.reference` method to interact with the Firebase Realtime Database.
        - If the data for the specified user does not exist, it creates a new entry with the list of file IDs.
        - It handles exceptions that may occur during the database operations.
        """
        
        try:
            ref1 = db.reference(f'auth_or_upload_multiple_files/User_{name_for}', app=app1)
            data1 = ref1.get()
            list_return = data1['list']
            return list(list_return)
        except:
            lista_de_file_id = []
            for file in list_files_path:
                message_file = client.files.create(
                    file=open(file, "rb"), purpose="assistants"
                )
                lista_de_file_id.append(message_file.id)

            ref1 = db.reference(f'auth_or_upload_multiple_files', app=app1)
            controle_das_funcao2 = f"User_{name_for}"
            controle_das_funcao_info_2 = {
                "list": lista_de_file_id,
            }
            ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)
            return lista_de_file_id

    def auth_or_create_vector_store_with_multiple_files(app1, client, name_for_vectorstore: str, file_ids: list): 
        """
        This function creates or retrieves an existing vector store based on the provided name and a list of file IDs.

        Parameters:
        - name_for_vectorstore (str): The name of the vector store to be created or retrieved.
        - file_ids (list): A list of file IDs to be added to the vector store.

        Returns:
        - str: The ID of the vector store.

        Raises:
        - Exception: If there is an error during the creation or retrieval process.

        Example:
        >>> auth_or_create_vector_store_with_multiple_files("my_vectorstore", ["file1.txt", "file2.txt"])
        'vs_abc123'

        Note:
        - The function uses Firebase Firestore to manage vector stores and their associated file batches.
        - It checks if a vector store with the given name already exists. If it does, it retrieves its ID; otherwise, it creates a new one.
        - It adds the specified file IDs to the vector store using batch operations.
        """
        try:
            ref1 = db.reference(f'auth_or_create_vector_store_with_multiple_files/User_{name_for_vectorstore}', app=app1)
            data1 = ref1.get()
            vector_store_return = data1['vectorstore']
            return str(vector_store_return)
        except:
            vector_store = client.beta.vector_stores.create(name=name_for_vectorstore)
            client.beta.vector_stores.file_batches.create_and_poll(
                vector_store_id=vector_store.id,
                file_ids=file_ids
            )
            ref1 = db.reference(f'auth_or_create_vector_store_with_multiple_files', app=app1)
            controle_das_funcao2 = f"User_{name_for_vectorstore}"
            controle_das_funcao_info_2 = {
                "vectorstore": vector_store.id,
            }
            ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)

            return vector_store.id

    def auth_or_create_vectorstore(app1, client, name_for_vectorstore: str, file_paths=None, updatenewfiles=None):
        """
        Authenticates with the database or creates a new vector store based on the provided name.

        Parameters:
        -----------
        name_for_vectorstore (str): The name of the vector store to authenticate or create.
        file_paths (list of str, optional): A list of file paths to upload to the vector store.
        update1newfiles (str, optional): The path to an updated file to upload to the vector store.

        Returns:
        --------
        str: The ID of the authenticated or created vector store.

        Raises:
        -------
        Exception: If there is an error during authentication or creation.

        Example:
        --------
        vector_store_id = auth_or_create_vectorstore("my_vector_store", file_paths=["path/to/file1.txt", "path/to/file2.txt"])
        print(vector_store_id)

        Note:
        -----
        - This function handles both authentication and creation of a vector store.
        - It uploads files to the vector store if specified.
        - It stores the vector store ID in the database after successful creation.
        """
        try:
            ref1 = db.reference(f'ai_org_vector_store/User_{name_for_vectorstore}', app=app1)
            data1 = ref1.get()
            vector_store_id = data1['vector_store_id']
            if updatenewfiles:
                for file in updatenewfiles:
                    update1newfile = open(file, "rb")
                    client.beta.vector_stores.files.upload(
                        vector_store_id=vector_store_id, file=update1newfile
                    )
            return str(vector_store_id)
        except Exception as err1:
            print(err1)
            vector_store = client.beta.vector_stores.create(name=name_for_vectorstore)
            if updatenewfiles:
                for file in updatenewfiles:
                    update1newfile = open(file, "rb")
                    client.beta.vector_stores.files.upload(
                        vector_store_id=vector_store.id, file=update1newfile
                    )
            elif file_paths:
                file_streams = [open(path, "rb") for path in file_paths]
                client.beta.vector_stores.file_batches.upload_and_poll(
                    vector_store_id=vector_store.id, files=file_streams
                )
                
            ref1 = db.reference(f'ai_org_vector_store', app=app1)
            controle_das_funcao2 = f"User_{name_for_vectorstore}"
            controle_das_funcao_info_2 = {
                "name_for_vectorstore": f'{name_for_vectorstore}',
                "vector_store_id": f'{vector_store.id}'
            }
            ref1.child(controle_das_funcao2).set(controle_das_funcao_info_2)
            return vector_store.id
