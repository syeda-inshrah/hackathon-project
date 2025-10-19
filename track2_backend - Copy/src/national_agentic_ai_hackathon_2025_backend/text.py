import json
from national_agentic_ai_hackathon_2025_backend.handlers.vector_store import VectorStoreManager

def save_json_objects_to_vector_store(json_path: str, vector_store_name: str):
    manager = VectorStoreManager()

    # 1. Load JSON data
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 2. Ensure vector store exists
    vector_store_id = manager.get_vector_store_id(vector_store_name)
    if not vector_store_id:
        store = manager.create_vector_store(vector_store_name)
        vector_store_id = store["id"]

    # 3. Loop over each object in JSON and upload as separate file
    for idx, obj in enumerate(data, start=1):
        try:
            # Create a text representation of the object
            file_content = f"Query: {obj['querries']}\nAnswer: {obj['answer']}"
            file_name = f"entry_{idx}.txt"

            # Upload file to OpenAI
            uploaded_file = manager.upload_file(
                file_name=file_name,
                content=file_content.encode("utf-8"),
                purpose="assistants"
            )

            file_id = uploaded_file["id"]

            # Index file into vector store
            manager.add_file_to_vector_store(vector_store_id, file_id)
            print(f"✅ Saved object {idx} as {file_name} -> file_id {file_id}")

        except Exception as e:
            print(f"❌ Error saving object {idx}: {e}")

if __name__ == "__main__":
    save_json_objects_to_vector_store("data.json", "FAQs")
