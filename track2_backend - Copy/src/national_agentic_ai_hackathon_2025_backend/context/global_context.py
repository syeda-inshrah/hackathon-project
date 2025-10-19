from pydantic import BaseModel
from national_agentic_ai_hackathon_2025_backend.context.user import UserContext
from national_agentic_ai_hackathon_2025_backend.context.chat_history import ChatHistoryContext
from national_agentic_ai_hackathon_2025_backend.context.coordinates import Coordinates
from typing import Optional

class GlobalContext(BaseModel):
    user: UserContext
    chat_history: ChatHistoryContext
    coordinates: Optional[Coordinates] = None