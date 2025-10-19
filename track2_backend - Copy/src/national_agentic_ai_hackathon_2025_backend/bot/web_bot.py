from national_agentic_ai_hackathon_2025_backend.schemas.user import User
from national_agentic_ai_hackathon_2025_backend.database.chat_history import ChatHistoryDB
from national_agentic_ai_hackathon_2025_backend.schemas.chat_history import ChatHistory, Message
from national_agentic_ai_hackathon_2025_backend.utils._helpers import _get_current_time
from national_agentic_ai_hackathon_2025_backend.database.user import UserDB
from national_agentic_ai_hackathon_2025_backend.handlers.workflow import WorkFlow
from national_agentic_ai_hackathon_2025_backend.context.global_context import GlobalContext
from national_agentic_ai_hackathon_2025_backend.context.chat_history import ChatHistoryContext
from national_agentic_ai_hackathon_2025_backend.context.user import UserContext
from national_agentic_ai_hackathon_2025_backend._debug import Logger
from national_agentic_ai_hackathon_2025_backend.context.coordinates import Coordinates
from pydantic import BaseModel

from typing import Optional

class ConnectionInfo(BaseModel):
    downlink: float
    effectiveType: str
    rtt: int

class BatteryInfo(BaseModel):
    level: int
    charging: bool

class DeviceStatus(BaseModel):
    connection: ConnectionInfo
    battery: BatteryInfo

class WebBot:
    def __init__(self, status: DeviceStatus) -> None:
        self.chat_db = ChatHistoryDB()
        self.user_db = UserDB()
        self.status = status

    async def execute_workflow(self, user: User, message: str, coordinates: Optional[Coordinates] = None):
        """
        Main entry point to process incoming web messages.
        Steps:
        1. Receive message from web interface
        2. Store message in history
        3. Retrieve or create user
        4. Route message to appropriate agent
        5. Return agent's response
        """
        try:
            if not message:
                Logger.error("No message provided to execute_workflow")
                return "No message provided"

            if not user or not user.userid:
                Logger.error("No user provided to execute_workflow")
                return "User authentication required"

            Logger.info(f"Received message from user {user.userid}: {message}")

            # Log incoming user message
            try:
                await self._log_user_message(user.phone_number, message, "text")
            except Exception as e:
                Logger.error(f"Error logging user message: {e}")

            # Fetch chat history for the user
            try:
                chat_history = await self.chat_db.get_chat_history_by_userid(user.userid)
                Logger.info(f"Fetched chat history for user {user.userid}")
            except Exception as e:
                Logger.error(f"Error fetching chat history for user {user.userid}: {e}")
                chat_history = None

            # Retrieve or create user
            try:
                updated_user = await self._get_or_create_user(user)
                if not updated_user:
                    Logger.error(f"Failed to create or retrieve user {user.userid}")
                    return "User authentication failed"
            except Exception as e:
                Logger.error(f"Error getting or creating user: {e}")
                return "User authentication failed"

            # Build global context
            try:
                global_context = GlobalContext(
                    user=self._get_user_context(updated_user),
                    chat_history=self._get_chat_history_context(user.phone_number, chat_history),
                    coordinates=coordinates
                )
            except Exception as e:
                Logger.error(f"Error building global context: {e}")
                return "Error processing request"

            # Process message through workflow
            try:
                wf = WorkFlow(self.status)
                response = await wf.execute_workflow(message, global_context)
                
                if not response:
                    Logger.error("Agent returned no result")
                    return "I'm sorry, I couldn't process your request at the moment."

                # Log the agent's response
                await self._log_agent_message(user.phone_number, response, "text")
                
                Logger.info(f"Successfully processed message for user {user.userid}")
                return response
                
            except Exception as e:
                Logger.error(f"Error processing message: {e}")
                return "I'm sorry, I encountered an error processing your message. Please try again later."

        except Exception as e:
            import traceback
            Logger.error(f"{__name__}> execute_workflow -> Unexpected error in execute_workflow: {e}")
            Logger.error(f"Traceback: {traceback.format_exc()}")
            return "I'm sorry, I encountered an unexpected error. Please try again later."

    async def _log_user_message(self, phone_number: str, raw_message: str, message_type: str):
        """Log user message to chat history."""
        try:
            message = Message(
                content=raw_message,
                sender="user",
                type=message_type,
                timestamp=_get_current_time()
            )
            await self.chat_db.append_message(phone_number, message)
            Logger.info(f"Logged user message for {phone_number}: {raw_message}")
        except Exception as e:
            Logger.error(f"Error logging user message: {e}")

    async def _log_agent_message(self, phone_number: str, raw_message: str, message_type: str):
        """Log agent message to chat history."""
        try:
            message = Message(
                content=raw_message,
                sender="agent",
                type=message_type,
                timestamp=_get_current_time()
            )
            await self.chat_db.append_message(phone_number, message)
            Logger.info(f"Logged agent message for {phone_number}: {raw_message}")
        except Exception as e:
            Logger.error(f"Error logging agent message: {e}")

    async def _get_or_create_user(self, user: User) -> Optional[User]:
        """Retrieve existing user or create a new one."""
        try:
            # Try to get user by ID first
            user_result = await self.user_db.get_user_by_id(user.userid)
            if user_result and user_result.get("success") and user_result.get("data"):
                user_data = user_result["data"]
                updated_user = User(**user_data)
                Logger.info(f"User found: {user.userid}")
                return updated_user

            # If not found by ID, try by phone number
            if user.phone_number:
                phone_result = await self.user_db.get_user_by_phone(user.phone_number)
                if phone_result and phone_result.get("success") and phone_result.get("data"):
                    user_data = phone_result["data"]
                    updated_user = User(**user_data)
                    Logger.info(f"User found by phone: {user.phone_number}")
                    return updated_user

            # Create new user
            
            create_result = await self.user_db.create_user(user)
            if create_result and create_result.get("success"):
                Logger.success(f"Created new user {user.userid}")
                return user
            else:
                Logger.error(f"Failed to create user {user.userid}: {create_result}")
                return None
        except Exception as e:
            Logger.error(f"Error retrieving or creating user {user.userid}: {e}")
            return None

    @staticmethod
    def _get_user_context(user: User) -> UserContext:
        """Convert User schema to UserContext safely."""
        return UserContext(
            phone_number=getattr(user, "phone_number", "") or "",
            username=getattr(user, "username", "") or "",
            address=getattr(user, "address", "") or "",
            email=getattr(user, "email", "") or "",
        )

    @staticmethod
    def _get_chat_history_context(phone_number: str, chat_history: ChatHistory) -> ChatHistoryContext:
        """Convert ChatHistory schema to ChatHistoryContext."""
        return ChatHistoryContext(
            phone_number=phone_number,
            messages=chat_history.messages if chat_history else [],
        )