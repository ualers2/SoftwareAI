#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Functions
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################


class Agent_files_update:
    """
    Offers utilities to update an assistant's vector store configuration, including
    updating tool resources and refreshing uploaded files.
    """

    def update_vectorstore_in_agent(client, assistant_id: str, vector_store_id: list, toolswithfunction:list):
        """
        Updates the vector store IDs for an assistant's file search tool.

        Parameters:
        ----------
        assistant_id (str): The ID of the assistant to update.
        vector_store_id (List[str]): A list of vector store IDs to set for the assistant.

        Returns:
        -------
        str: The updated assistant ID.

        Raises:
        -------
        Exception: If there is an error updating the assistant.

        Example:
        --------
        >>> assistant_id = '12345'
        >>> vector_store_id = ['store1', 'store2']
        >>> updated_assistant_id = update_vectorstore_in_agent(assistant_id, vector_store_id)
        >>> print(updated_assistant_id)
        '12345'

        Note:
        -----
        - This function assumes that the `client` object is properly configured with the necessary credentials to interact with the assistant management API.
        """
        try:
            assistant = client.beta.assistants.update(
                assistant_id=assistant_id,
                tools=toolswithfunction,
                tool_resources={"file_search": {"vector_store_ids": vector_store_id}},
            )
            return assistant.id
        except Exception as e:
            raise Exception(f"Error updating assistant: {e}")

    def del_all_and_upload_files_in_vectorstore(appfb, client, AI: str, name_for_vectorstore: str, file_paths: list, toolswithfunction: list):
        """
        Deletes all existing files from a specified vector store and uploads a new set of files.
        Afterwards, updates the assistant's configuration with the refreshed vector store ID.

        Parameters:
        ----------
        appfb: Firebase app reference for database operations.
        client: OpenAI client instance for vector store operations.
        AI (str): Assistant ID to update.
        name_for_vectorstore (str): Name of the target vector store.
        file_paths (list): List of file paths to upload.
        toolswithfunction (list): List of tool definitions for the assistant.

        Returns:
        -------
        str: Updated assistant ID.
        """
        vector_store_id = Agent_files.auth_vectorstoreAdvanced(app1=appfb, client=client, name_for_vectorstore=name_for_vectorstore)
        lista = client.beta.vector_stores.files.list(vector_store_id)
        ids = [file.id for file in lista.data]
        print(ids)
        for id in ids:
            deleted_vector_store_file = client.beta.vector_stores.files.delete(
                vector_store_id=vector_store_id,
                file_id=id
            )
            print(deleted_vector_store_file)

        vector_store_id = Agent_files.auth_vectorstoreAdvanced(app1=appfb, client=client, name_for_vectorstore=name_for_vectorstore, file_paths=file_paths)
        AI = Agent_files_update.update_vectorstore_in_agent(client, AI, [vector_store_id], toolswithfunction)
        return AI


