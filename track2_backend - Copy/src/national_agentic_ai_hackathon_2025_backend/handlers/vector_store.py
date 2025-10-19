from openai import OpenAI, RateLimitError, APIError, APITimeoutError, OpenAIError
from typing import Dict, Any, List, Optional
from national_agentic_ai_hackathon_2025_backend.config import Config
from national_agentic_ai_hackathon_2025_backend._debug import Logger


class VectorStoreManager:
    def __init__(self):
        """
        Initialize the OpenAI client and set up storage for vector stores.
        """
        try:
            self.client = Config.get_openai_client(sync=True)
            if not self.client:
                raise RuntimeError("Failed to initialize OpenAI client")
        except Exception as e:
            Logger.error(f"{__name__}> __init__ -> Error initializing VectorStoreManager: {e}")
            raise RuntimeError(f"Failed to initialize VectorStoreManager: {e}")

    # ---------- File Operations ----------
    def upload_file(self, file_name: str, content: bytes, purpose: str = "assistants") -> Dict[str, Any]:
        """
        Uploads a file to OpenAI (supports text and binary files).
        """
        try:
            if not file_name or not isinstance(file_name, str):
                raise ValueError("Invalid file name provided")
            if not content or not isinstance(content, bytes):
                raise ValueError("Invalid file content provided")
            if not purpose or not isinstance(purpose, str):
                raise ValueError("Invalid purpose provided")
                
            file_upload = self.client.files.create(
                file=(file_name, content),
                purpose=purpose,
            )
            Logger.info(f"Successfully uploaded file: {file_name}")
            return file_upload.to_dict()
        except RateLimitError as e:
            Logger.error(f"{__name__}> upload_file -> Rate limit exceeded uploading file {file_name}: {e}")
            raise RuntimeError(f"Rate limit exceeded: {e}")
        except APIError as e:
            Logger.error(f"{__name__}> upload_file -> API error uploading file {file_name}: {e}")
            raise RuntimeError(f"API error uploading file: {e}")
        except APITimeoutError as e:
            Logger.error(f"{__name__}> upload_file -> Timeout uploading file {file_name}: {e}")
            raise RuntimeError(f"Timeout uploading file: {e}")
        except OpenAIError as e:
            Logger.error(f"{__name__}> upload_file -> OpenAI error uploading file {file_name}: {e}")
            raise RuntimeError(f"OpenAI error uploading file: {e}")
        except Exception as e:
            Logger.error(f"{__name__}> upload_file -> Unexpected error uploading file {file_name}: {e}")
            raise RuntimeError(f"Unexpected error uploading file: {e}")

    def list_files(self) -> List[Dict[str, Any]]:
        """
        Lists all uploaded files.
        """
        try:
            files = self.client.files.list()
            file_list = [f.to_dict() for f in files.data]
            Logger.info(f"Successfully retrieved {len(file_list)} files")
            return file_list
        except RateLimitError as e:
            Logger.error(f"{__name__}> list_files -> Rate limit exceeded listing files: {e}")
            raise RuntimeError(f"Rate limit exceeded: {e}")
        except APIError as e:
            Logger.error(f"{__name__}> list_files -> API error listing files: {e}")
            raise RuntimeError(f"API error listing files: {e}")
        except APITimeoutError as e:
            Logger.error(f"{__name__}> list_files -> Timeout listing files: {e}")
            raise RuntimeError(f"Timeout listing files: {e}")
        except OpenAIError as e:
            Logger.error(f"{__name__}> list_files -> OpenAI error listing files: {e}")
            raise RuntimeError(f"OpenAI error listing files: {e}")
        except Exception as e:
            Logger.error(f"{__name__}> list_files -> Unexpected error listing files: {e}")
            raise RuntimeError(f"Unexpected error listing files: {e}")

    async def delete_file(self, file_id: str) -> Dict[str, Any]:
        """
        Deletes a file by ID.
        """
        try:
            if not file_id or not isinstance(file_id, str):
                raise ValueError("Invalid file ID provided")
                
            deleted = self.client.files.delete(file_id)
            Logger.info(f"Successfully deleted file: {file_id}")
            return deleted.to_dict()
        except RateLimitError as e:
            Logger.error(f"{__name__}> delete_file -> Rate limit exceeded deleting file {file_id}: {e}")
            raise RuntimeError(f"Rate limit exceeded: {e}")
        except APIError as e:
            Logger.error(f"{__name__}> delete_file -> API error deleting file {file_id}: {e}")
            raise RuntimeError(f"API error deleting file: {e}")
        except APITimeoutError as e:
            Logger.error(f"{__name__}> delete_file -> Timeout deleting file {file_id}: {e}")
            raise RuntimeError(f"Timeout deleting file: {e}")
        except OpenAIError as e:
            Logger.error(f"{__name__}> delete_file -> OpenAI error deleting file {file_id}: {e}")
            raise RuntimeError(f"OpenAI error deleting file: {e}")
        except Exception as e:
            Logger.error(f"{__name__}> delete_file -> Unexpected error deleting file {file_id}: {e}")
            raise RuntimeError(f"Unexpected error deleting file: {e}")
        
    # ---------- Vector Store Operations ----------
    def create_vector_store(self, name: str) -> Dict[str, Any]:
        """
        Creates a new vector store.
        """
        try:
            if not name or not isinstance(name, str):
                raise ValueError("Invalid vector store name provided")
                
            vector_store = self.client.vector_stores.create(name=name)
            Logger.info(f"Successfully created vector store: {name}")
            return vector_store.to_dict()
        except RateLimitError as e:
            Logger.error(f"{__name__}> create_vector_store -> Rate limit exceeded creating vector store {name}: {e}")
            raise RuntimeError(f"Rate limit exceeded: {e}")
        except APIError as e:
            Logger.error(f"{__name__}> create_vector_store -> API error creating vector store {name}: {e}")
            raise RuntimeError(f"API error creating vector store: {e}")
        except APITimeoutError as e:
            Logger.error(f"{__name__}> create_vector_store -> Timeout creating vector store {name}: {e}")
            raise RuntimeError(f"Timeout creating vector store: {e}")
        except OpenAIError as e:
            Logger.error(f"{__name__}> create_vector_store -> OpenAI error creating vector store {name}: {e}")
            raise RuntimeError(f"OpenAI error creating vector store: {e}")
        except Exception as e:
            Logger.error(f"{__name__}> create_vector_store -> Unexpected error creating vector store {name}: {e}")
            raise RuntimeError(f"Unexpected error creating vector store: {e}")

    def list_vector_stores(self) -> List[Dict[str, Any]]:
        """
        Lists all vector stores.
        """
        try:
            stores = self.client.vector_stores.list()
            store_list = [s.to_dict() for s in stores.data]
            Logger.info(f"Successfully retrieved {len(store_list)} vector stores")
            return store_list
        except RateLimitError as e:
            Logger.error(f"{__name__}> list_vector_stores -> Rate limit exceeded listing vector stores: {e}")
            raise RuntimeError(f"Rate limit exceeded: {e}")
        except APIError as e:
            Logger.error(f"{__name__}> list_vector_stores -> API error listing vector stores: {e}")
            raise RuntimeError(f"API error listing vector stores: {e}")
        except APITimeoutError as e:
            Logger.error(f"{__name__}> list_vector_stores -> Timeout listing vector stores: {e}")
            raise RuntimeError(f"Timeout listing vector stores: {e}")
        except OpenAIError as e:
            Logger.error(f"{__name__}> list_vector_stores -> OpenAI error listing vector stores: {e}")
            raise RuntimeError(f"OpenAI error listing vector stores: {e}")
        except Exception as e:
            Logger.error(f"{__name__}> list_vector_stores -> Unexpected error listing vector stores: {e}")
            raise RuntimeError(f"Unexpected error listing vector stores: {e}")

    def delete_vector_store(self, vector_store_id: str) -> Dict[str, Any]:
        """
        Deletes a vector store by ID.
        """
        try:
            if not vector_store_id or not isinstance(vector_store_id, str):
                raise ValueError("Invalid vector store ID provided")
                
            deleted = self.client.vector_stores.delete(vector_store_id)
            Logger.info(f"Successfully deleted vector store: {vector_store_id}")
            return deleted.to_dict()
        except RateLimitError as e:
            Logger.error(f"{__name__}> delete_vector_store -> Rate limit exceeded deleting vector store {vector_store_id}: {e}")
            raise RuntimeError(f"Rate limit exceeded: {e}")
        except APIError as e:
            Logger.error(f"{__name__}> delete_vector_store -> API error deleting vector store {vector_store_id}: {e}")
            raise RuntimeError(f"API error deleting vector store: {e}")
        except APITimeoutError as e:
            Logger.error(f"{__name__}> delete_vector_store -> Timeout deleting vector store {vector_store_id}: {e}")
            raise RuntimeError(f"Timeout deleting vector store: {e}")
        except OpenAIError as e:
            Logger.error(f"{__name__}> delete_vector_store -> OpenAI error deleting vector store {vector_store_id}: {e}")
            raise RuntimeError(f"OpenAI error deleting vector store: {e}")
        except Exception as e:
            Logger.error(f"{__name__}> delete_vector_store -> Unexpected error deleting vector store {vector_store_id}: {e}")
            raise RuntimeError(f"Unexpected error deleting vector store: {e}")

    # ---------- Vector Store Files ----------
    def add_file_to_vector_store(self, vector_store_id: str, file_id: str) -> Dict[str, Any]:
        """
        Indexes a file into a vector store.
        """
        try:
            if not vector_store_id or not isinstance(vector_store_id, str):
                raise ValueError("Invalid vector store ID provided")
            if not file_id or not isinstance(file_id, str):
                raise ValueError("Invalid file ID provided")
                
            indexed = self.client.vector_stores.files.create_and_poll(
                vector_store_id=vector_store_id,
                file_id=file_id,
            )
            Logger.info(f"Successfully added file {file_id} to vector store {vector_store_id}")
            return indexed.to_dict()
        except RateLimitError as e:
            Logger.error(f"{__name__}> add_file_to_vector_store -> Rate limit exceeded adding file {file_id} to vector store {vector_store_id}: {e}")
            raise RuntimeError(f"Rate limit exceeded: {e}")
        except APIError as e:
            Logger.error(f"{__name__}> add_file_to_vector_store -> API error adding file {file_id} to vector store {vector_store_id}: {e}")
            raise RuntimeError(f"API error adding file to vector store: {e}")
        except APITimeoutError as e:
            Logger.error(f"{__name__}> add_file_to_vector_store -> Timeout adding file {file_id} to vector store {vector_store_id}: {e}")
            raise RuntimeError(f"Timeout adding file to vector store: {e}")
        except OpenAIError as e:
            Logger.error(f"{__name__}> add_file_to_vector_store -> OpenAI error adding file {file_id} to vector store {vector_store_id}: {e}")
            raise RuntimeError(f"OpenAI error adding file to vector store: {e}")
        except Exception as e:
            Logger.error(f"{__name__}> add_file_to_vector_store -> Unexpected error adding file {file_id} to vector store {vector_store_id}: {e}")
            raise RuntimeError(f"Unexpected error adding file to vector store: {e}")

    def list_vector_store_files(self, vector_store_id: str) -> List[Dict[str, Any]]:
        """
        Lists files in a vector store.
        """
        try:
            if not vector_store_id or not isinstance(vector_store_id, str):
                raise ValueError("Invalid vector store ID provided")
                
            files = self.client.vector_stores.files.list(vector_store_id=vector_store_id)
            file_list = [f.to_dict() for f in files.data]
            Logger.info(f"Successfully retrieved {len(file_list)} files from vector store {vector_store_id}")
            return file_list
        except RateLimitError as e:
            Logger.error(f"{__name__}> list_vector_store_files -> Rate limit exceeded listing files in vector store {vector_store_id}: {e}")
            raise RuntimeError(f"Rate limit exceeded: {e}")
        except APIError as e:
            Logger.error(f"{__name__}> list_vector_store_files -> API error listing files in vector store {vector_store_id}: {e}")
            raise RuntimeError(f"API error listing files in vector store: {e}")
        except APITimeoutError as e:
            Logger.error(f"{__name__}> list_vector_store_files -> Timeout listing files in vector store {vector_store_id}: {e}")
            raise RuntimeError(f"Timeout listing files in vector store: {e}")
        except OpenAIError as e:
            Logger.error(f"{__name__}> list_vector_store_files -> OpenAI error listing files in vector store {vector_store_id}: {e}")
            raise RuntimeError(f"OpenAI error listing files in vector store: {e}")
        except Exception as e:
            Logger.error(f"{__name__}> list_vector_store_files -> Unexpected error listing files in vector store {vector_store_id}: {e}")
            raise RuntimeError(f"Unexpected error listing files in vector store: {e}")

    def remove_file_from_vector_store(self, vector_store_id: str, file_id: str) -> Dict[str, Any]:
        """
        Removes a file from a vector store.
        """
        try:
            if not vector_store_id or not isinstance(vector_store_id, str):
                raise ValueError("Invalid vector store ID provided")
            if not file_id or not isinstance(file_id, str):
                raise ValueError("Invalid file ID provided")
                
            removed = self.client.vector_stores.files.delete(
                vector_store_id=vector_store_id,
                file_id=file_id,
            )
            Logger.info(f"Successfully removed file {file_id} from vector store {vector_store_id}")
            return removed.to_dict()
        except RateLimitError as e:
            Logger.error(f"{__name__}> remove_file_from_vector_store -> Rate limit exceeded removing file {file_id} from vector store {vector_store_id}: {e}")
            raise RuntimeError(f"Rate limit exceeded: {e}")
        except APIError as e:
            Logger.error(f"{__name__}> remove_file_from_vector_store -> API error removing file {file_id} from vector store {vector_store_id}: {e}")
            raise RuntimeError(f"API error removing file from vector store: {e}")
        except APITimeoutError as e:
            Logger.error(f"{__name__}> remove_file_from_vector_store -> Timeout removing file {file_id} from vector store {vector_store_id}: {e}")
            raise RuntimeError(f"Timeout removing file from vector store: {e}")
        except OpenAIError as e:
            Logger.error(f"{__name__}> remove_file_from_vector_store -> OpenAI error removing file {file_id} from vector store {vector_store_id}: {e}")
            raise RuntimeError(f"OpenAI error removing file from vector store: {e}")
        except Exception as e:
            Logger.error(f"{__name__}> remove_file_from_vector_store -> Unexpected error removing file {file_id} from vector store {vector_store_id}: {e}")
            raise RuntimeError(f"Unexpected error removing file from vector store: {e}")

    def get_vector_store_id(self, name: str) -> Optional[str]:
        """
        Fetches the ID of a vector store by name.
        """
        try:
            if not name or not isinstance(name, str):
                Logger.warning(f"Invalid vector store name provided: {name}")
                return None
                
            response = self.list_vector_stores()
            for store in response:
                if store.get('name') == name:
                    Logger.info(f"Found vector store ID for name '{name}': {store.get('id')}")
                    return store.get('id')
            Logger.warning(f"No vector store found with name: {name}")
            return None
        except Exception as e:
            Logger.error(f"{__name__}> get_vector_store_id -> Error getting vector store ID for name '{name}': {e}")
            return None
        
    def delete_vector_store_with_files(self, vector_store_id: str) -> None:
        """
        Deletes a vector store along with all its indexed files.
        """
        try:
            if not vector_store_id or not isinstance(vector_store_id, str):
                raise ValueError("Invalid vector store ID provided")
                
            Logger.info(f"Starting deletion of vector store {vector_store_id} with all files")
            files = self.list_vector_store_files(vector_store_id)
            
            for file in files:
                try:
                    self.remove_file_from_vector_store(vector_store_id, file['id'])
                    self.delete_file(file['id'])
                except Exception as e:
                    Logger.warning(f"Error deleting file {file.get('id', 'unknown')}: {e}")
                    continue
                    
            self.delete_vector_store(vector_store_id)
            Logger.info(f"Successfully deleted vector store {vector_store_id} with all files")
        except Exception as e:
            Logger.error(f"{__name__}> delete_vector_store_with_files -> Error deleting vector store {vector_store_id} with files: {e}")
            raise RuntimeError(f"Error deleting vector store with files: {e}")