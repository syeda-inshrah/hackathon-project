from typing import Any, Dict, Optional, List
from national_agentic_ai_hackathon_2025_backend.database.base import DataBase
from national_agentic_ai_hackathon_2025_backend.schemas.chat_history import ChatHistory, Message

class ChatHistoryDB(DataBase):
    def __init__(self):
        super().__init__()
        self.table_name = "chat_history"

    async def create_chat_history(self, chat_history: ChatHistory) -> Dict[str, Any]:
        # Insert a new chat history record into the database using supabase.table
        data = chat_history.model_dump()
        try:
            result = self.supabase.table(self.table_name).insert(data).execute()
            return {"success": True, "data": result.data[0] if result.data else None}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def get_chat_history_by_phone(self, phone_number: str) -> Optional[ChatHistory]:
        """
        Retrieve chat history for a given phone number.
        Returns a ChatHistory object if found, otherwise None.
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq("phone_number", phone_number).execute()
            if result.data and len(result.data) > 0:
                item = result.data[0]
                messages = item.get("messages", [])
                if messages and isinstance(messages[0], dict):
                    item["messages"] = [Message(**m) if not isinstance(m, Message) else m for m in messages]
                return ChatHistory(**item)
            return None
        except Exception as e:
            return None
            
    async def get_chat_history_by_userid(self, user_id: str) -> Optional[ChatHistory]:
        """
        Retrieve chat history for a given user_id.
        Returns a ChatHistory object if found, otherwise None.
        """
        try:
            result = self.supabase.table(self.table_name).select("*").eq("user_id", user_id).execute()
            if result.data and len(result.data) > 0:
                item = result.data[0]
                messages = item.get("messages", [])
                if messages and isinstance(messages[0], dict):
                    item["messages"] = [Message(**m) if not isinstance(m, Message) else m for m in messages]
                return ChatHistory(**item)
            return None
        except Exception as e:
            return None

    async def append_message(
        self,
        phone_number: str,
        message: Message
    ) -> Optional[ChatHistory]:
        # Append a message to the chat history for a given phone number
        chat_history = await self.get_chat_history_by_phone(phone_number)
        if not chat_history:
            # Create new chat history if it doesn't exist
            chat_history = ChatHistory(
                phone_number=phone_number,
                messages=[message]
            )
            await self.create_chat_history(chat_history)
            return chat_history
        else:
            chat_history.messages.append(message)
            try:
                self.supabase.table(self.table_name).update(
                    {"messages": [m.dict() for m in chat_history.messages]}
                ).eq("phone_number", phone_number).execute()
            except Exception as e:
                pass
            return chat_history

    async def get_all_chat_histories(self) -> List[ChatHistory]:
        # Retrieve all chat histories using supabase.table
        try:
            result = self.supabase.table(self.table_name).select("*").execute()
            if result.data:
                return [ChatHistory(**item) for item in result.data]
            return []
        except Exception as e:
            return []

    async def delete_chat_history(self, phone_number: str) -> bool:
        # Delete chat history for a given phone number using supabase.table
        try:
            result = self.supabase.table(self.table_name).delete().eq("phone_number", phone_number).execute()
            return result.data is not None
        except Exception as e:
            return False