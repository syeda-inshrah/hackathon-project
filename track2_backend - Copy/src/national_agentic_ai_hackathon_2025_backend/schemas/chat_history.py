from typing import Literal, Optional, List
from pydantic import BaseModel

class Message(BaseModel):
    content: str
    sender: Literal["user", "agent"]
    type: Literal["text", "audio"] = "text"
    timestamp: Optional[str] = None

class ChatHistory(BaseModel):
    phone_number: str
    messages: List[Message] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
