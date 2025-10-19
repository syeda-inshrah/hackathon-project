from national_agentic_ai_hackathon_2025_backend.utils.wa_instance import wa
from national_agentic_ai_hackathon_2025_backend._debug import Logger
from pywa_async import types

class WhatsappHandler:
    async def send_whatsapp_message(self, to: str, message: str, message_type: str = "text"):
        """Send a WhatsApp message."""
        try:
            Logger.info(f"Sending WhatsApp {message_type} to {to}...")
            Logger.debug(f"Raw message content: {message}")
            if message_type == "text":
                resp = await wa.send_message(to, message, preview_url=True)
            elif message_type in ["audio", "voice"]:
                from national_agentic_ai_hackathon_2025_backend.utils.voice.tts import TextToSpeech
                tts = TextToSpeech()
                audio_data = await tts.convert_to_speech(message)
                Logger.debug(f"Audio data size: {len(audio_data)} bytes")
                resp = await wa.send_audio(to, audio_data)  # Send the audio data
            else:
                Logger.error(f"Unsupported message type: {message_type}")
                return
            Logger.info(f"WhatsApp send {message_type} to {resp.to_user.wa_id}")
            Logger.debug(f"Full WhatsApp response: {resp}")
        except Exception as e:
            Logger.error(f"Failed to send WhatsApp message to {to}: {e}")

    async def _get_raw_message(self, message: types.Message, message_type: str) -> str:
        """
        Extract the raw message content based on its type.
        """
        if message_type == "text":
            return message.text
        elif message_type in ["audio", "voice"]:
            return await self._transcribe_audio_message(message)
        else:
            return f"[{message_type.upper()} MESSAGE]"

    @staticmethod
    async def send_whatsapp_text(to: str, message: str):
        """Send a WhatsApp text message."""
        try:
            return await wa.send_message(to, message, preview_url=True)
        except Exception as e:
            Logger.error(f"Failed to send WhatsApp text to {to}: {e}")

    @staticmethod
    async def send_whatsapp_audio(to: str, audio_bytes: bytes):
        """Send a WhatsApp audio message."""
        try:
            return await wa.send_audio(to, audio_bytes)
        except Exception as e:
            Logger.error(f"Failed to send WhatsApp audio to {to}: {e}")

    @staticmethod
    def _get_phone_numbers(message: types.Message) -> tuple[str, str]:
        """Extract the business's And User's WhatsApp number from the message context."""
        return (message.metadata.display_phone_number, message.from_user.wa_id)

    @staticmethod
    async def _transcribe_audio_message(message) -> str:
        """Transcribe audio message to text using OpenAI Whisper."""
        try:
            # Import here to avoid circular imports
            from national_agentic_ai_hackathon_2025_backend.utils.voice.audio import AudioProcessor
            from national_agentic_ai_hackathon_2025_backend.config import Config
            from openai import OpenAI
            
            Logger.info(f"Transcribing audio message from {message.from_user.wa_id}")
            
            # Initialize OpenAI client if not already done
            client = OpenAI(api_key=Config.get("OPENAI_API_KEY"))
            audio_processor = AudioProcessor(client)
            
            # Download the audio file
            audio_file = await audio_processor.download_audio_from_message(message)
            if not audio_file:
                Logger.error("Failed to download audio file")
                return "[AUDIO MESSAGE - Download Failed]"
            
            # Transcribe to text
            text = await audio_processor.convert_to_text(audio_file)
            if not text:
                Logger.error("Failed to transcribe audio")
                return "[AUDIO MESSAGE - Transcription Failed]"
            
            # Clean up temporary file
            import os
            if os.path.exists(audio_file):
                os.unlink(audio_file)
            
            Logger.info(f"Successfully transcribed audio: {text}")
            Logger.debug(f"Raw transcription result: {text}")
            return text
            
        except Exception as e:
            Logger.error(f"Error transcribing audio message: {e}")
            return "[AUDIO MESSAGE - Processing Error]"
