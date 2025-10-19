from supabase import create_client, Client
from national_agentic_ai_hackathon_2025_backend.config import Config

class DataBase:
    def __init__(self):
        self._connect_to_db()

    def _connect_to_db(self):
        config = Config()
        self.supabase: Client = create_client(config.get("SUPABASE_URL"), config.get("SUPABASE_SERVICE_ROLE_KEY"))