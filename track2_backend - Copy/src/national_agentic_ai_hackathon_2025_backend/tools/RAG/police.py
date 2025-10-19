from national_agentic_ai_hackathon_2025_backend.context.global_context import GlobalContext
from national_agentic_ai_hackathon_2025_backend.config import Config
from agents import FileSearchTool, RunContextWrapper

def police_facility_tool(wrapper: RunContextWrapper[GlobalContext]):
    vector_store_id = Config.get("POLICE_VECTOR_STORE_ID")
    return FileSearchTool(
        vector_store_ids=[vector_store_id],
        max_num_results=3,
        include_search_results=True,
    )