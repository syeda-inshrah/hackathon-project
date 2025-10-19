from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from national_agentic_ai_hackathon_2025_backend.schemas.chat_history import Message

class ChatHistoryContext(BaseModel):
    phone_number: str
    messages: List[Message] = []
    formatted_messages: Optional[str] = None

    def set_message_limit(self, limit: int):
        self.generate_formatted_messages(limit=limit)
        return self.formatted_messages 

    def generate_formatted_messages(self, limit: int = 10) -> str:
        """
        Convert chat history into a readable block for system prompt.
        """
        if not self.messages:
            return ""

        lines = []
        
        for msg in self.messages[-limit:]:
            # Format time
            msg_time = datetime.fromisoformat(msg.timestamp)
            time_str = msg_time.strftime("%Y-%m-%d %H:%M")

            # Show content differently if not text
            if msg.type == "text":
                content_display = msg.content
            else:
                content_display = f"[{msg.type.upper()}] {msg.content}"

            # Capitalize sender
            sender_name = msg.sender.capitalize()

            lines.append(f"[{time_str}] {sender_name}: {content_display}")

        self.formatted_messages = (
            "\n---\n" +
            "**Chat History**\n"
            + "\n".join(lines) +
            "\n---\n"
        )

        return self.formatted_messages

    def __init__(self, **data):
        super().__init__(**data)
        self.generate_formatted_messages()
