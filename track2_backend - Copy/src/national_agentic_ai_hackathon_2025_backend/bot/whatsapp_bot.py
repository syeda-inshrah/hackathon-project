from pywa_async import types
from national_agentic_ai_hackathon_2025_backend._debug import Logger
from national_agentic_ai_hackathon_2025_backend.database.user import UserDB
from national_agentic_ai_hackathon_2025_backend.database.chat_history import ChatHistoryDB
from national_agentic_ai_hackathon_2025_backend.handlers.whatsapp import WhatsappHandler
from national_agentic_ai_hackathon_2025_backend.context.chat_history import ChatHistoryContext, Message
from national_agentic_ai_hackathon_2025_backend.schemas.chat_history import ChatHistory
from national_agentic_ai_hackathon_2025_backend.context.user import UserContext
from national_agentic_ai_hackathon_2025_backend.context.global_context import GlobalContext
from national_agentic_ai_hackathon_2025_backend.utils._helpers import _get_current_time
from national_agentic_ai_hackathon_2025_backend.schemas.user import User
from national_agentic_ai_hackathon_2025_backend.handlers.workflow import WorkFlow
from typing import Optional


class WhatsappBot:
    def __init__(self):
        self.user_db = UserDB()
        self.chat_db = ChatHistoryDB()
        self.whatsapp_handler = WhatsappHandler()

    async def execute_workflow(self, message: types.Message, message_type: str):
        """
        Main entry point to process incoming WhatsApp messages.
        Steps:
        1. Receive message from WhatsApp
        2. Store message in history
        3. Retrieve or create customer
        4. Route message to appropriate agent
        5. Send agent's response back to WhatsApp and dashboard
        """
        try:
            if not message:
                Logger.error("No message provided to execute_workflow")
                return
                
            if not message_type or not isinstance(message_type, str):
                Logger.error(f"Invalid message type provided: {message_type}")
                return

            if message_type not in {"text", "audio", "voice"}:
                Logger.warning(f"Unsupported message type: {message_type}")
                try:
                    await message.reply("Unsupported message type.")
                except Exception as e:
                    Logger.error(f"Failed to send unsupported message type reply: {e}")
                return

            # Identify business
            try:
                buisness_number, phone_number = self.whatsapp_handler._get_phone_numbers(message)
                if not buisness_number or not phone_number:
                    Logger.error("Failed to extract phone numbers from message")
                    return
            except Exception as e:
                Logger.error(f"Error extracting phone numbers: {e}")
                return
                
            try:
                await message.mark_as_read()
            except Exception as e:
                Logger.warning(f"Failed to mark message as read: {e}")
                
            try:
                raw_message = await self.whatsapp_handler._get_raw_message(message, message_type)
                if not raw_message:
                    Logger.warning(f"Failed to extract message content for type: {message_type}")
                    return
            except Exception as e:
                Logger.error(f"Error extracting raw message: {e}")
                return
                
            Logger.info(f"Received message from {phone_number}: {raw_message}")
            Logger.debug(f"Raw message object: {message}")
            Logger.debug(f"Message metadata: {message.metadata if hasattr(message, 'metadata') else 'No metadata'}")

            # Fetch chat history
            try:
                chat_history = await self.chat_db.get_chat_history_by_phone(phone_number)
                Logger.info(f"Fetched chat history for {phone_number}")
                Logger.debug(f"Raw chat history: {chat_history}")
            except Exception as e:
                Logger.error(f"Error fetching chat history for {phone_number}: {e}")
                chat_history = None

            # save incoming user message
            try:
                await self._log_and_save_user_message(phone_number, raw_message, message_type)
            except Exception as e:
                Logger.error(f"Error logging user message: {e}")

            # Retrieve or create user
            try:
                user = await self._get_or_create_user(phone_number)
                if not user:
                    Logger.error(f"Failed to create or retrieve user for {phone_number}")
                    return
            except Exception as e:
                Logger.error(f"Error getting or creating user: {e}")
                return

            # Build global context
            try:
                global_context = GlobalContext(
                    user=self._get_user_context(user),
                    chat_history=self._get_chat_history_context(phone_number, chat_history),
                )
            except Exception as e:
                Logger.error(f"Error building global context: {e}")
                return

            # Process message
            try:
                await message.indicate_typing()
            except Exception as e:
                Logger.warning(f"Failed to indicate typing: {e}")
                
            try:
                wf = WorkFlow()
                response = await wf.execute_workflow(raw_message, global_context)
                
                if not response:
                    Logger.error("Agent returned no result")
                    return

                await self._log_agent_message(phone_number, response, message_type)
                await self.whatsapp_handler.send_whatsapp_message(phone_number, response, message_type)
            except Exception as e:
                Logger.error(f"Error sending agent response: {e}")

        except Exception as e:
            import traceback
            Logger.error(f"{__name__}> execute_workflow -> Unexpected error in execute_workflow: {e}")
            Logger.error(f"Traceback: {traceback.format_exc()}")
            try:
                # Try to send error message to user
                if 'phone_number' in locals():
                    await self.whatsapp_handler.send_whatsapp_message(
                        phone_number, 
                        "I'm sorry, I encountered an error processing your message. Please try again later.",
                        "text"
                    )
            except Exception as send_error:
                Logger.error(f"{__name__}> execute_workflow -> Failed to send error message to user: {send_error}")


    async def _log_and_save_user_message(self, phone_number: str, raw_message: str, message_type: str):
        message = Message(
            content=raw_message,
            sender="user",
            type=message_type,
            timestamp=_get_current_time()
        )
        await self.chat_db.append_message(phone_number, message)
        Logger.info(f"Logged user message for {phone_number}: {raw_message}")

    async def _log_agent_message(self, phone_number: str, raw_message: str, message_type: str):
        message = Message(
            content=raw_message,
            sender="agent",
            type=message_type,
            timestamp=_get_current_time()
        )
        await self.chat_db.append_message(phone_number, message)
        Logger.info(f"Logged agent message for {phone_number}: {raw_message}")

    async def _get_or_create_user(self, phone_number: str) -> Optional[User]:
        """Retrieve existing user or create a new one."""
        try:
            # Await the async method properly
            user_result = await self.user_db.get_user_by_phone(phone_number)
            if user_result and user_result.get("success") and user_result.get("data"):
                user_data = user_result["data"]
                user = User(**user_data)
                Logger.info(f"User found: {phone_number}")
                return user

            # Create new user
            new_user = User(
                phone_number=phone_number,
                platform="whatsapp",
                is_loggedin=True
            )
            create_result = await self.user_db.create_user(new_user)
            if create_result and create_result.get("success"):
                Logger.success(f"Created new user {phone_number}")
                return new_user
            else:
                Logger.error(f"Failed to create user {phone_number}: {create_result}")
                return None
        except Exception as e:
            Logger.error(f"Error retrieving or creating user {phone_number}: {e}")
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