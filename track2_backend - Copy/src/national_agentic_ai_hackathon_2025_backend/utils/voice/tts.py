import io
from openai import OpenAI
from openai import OpenAIError, APIError, RateLimitError, APITimeoutError
from typing import Optional
from national_agentic_ai_hackathon_2025_backend._debug import Logger

class TextToSpeech:
    """Handles text to speech conversion"""

    def __init__(self):
        try:
            self.client = OpenAI()
            Logger.info("Successfully initialized TextToSpeech client")
        except Exception as e:
            Logger.error(f"{__name__}> __init__ -> Error initializing TextToSpeech client: {e}")
            raise RuntimeError(f"Failed to initialize TextToSpeech: {e}")
    
    async def convert_to_speech(self, text: str) -> Optional[bytes]:
        """Convert text to speech and return audio bytes"""
        try:
            if not text or not isinstance(text, str):
                Logger.warning(f"Invalid text provided for TTS conversion: {text}")
                return None
                
            if len(text.strip()) == 0:
                Logger.warning("Empty text provided for TTS conversion")
                return None
                
            # Limit text length to prevent API errors
            if len(text) > 4000:  # OpenAI TTS has character limits
                Logger.warning(f"Text too long for TTS ({len(text)} chars), truncating to 4000 chars")
                text = text[:4000]
            
            Logger.info(f"Converting text to speech ({len(text)} characters)")
            
            with self.client.audio.speech.with_streaming_response.create(
                model="tts-1",   # Using tts-1 for better compatibility
                voice="alloy",
                input=text
            ) as response:
                audio_buffer = io.BytesIO()
                chunk_count = 0
                for chunk in response.iter_bytes():   # stream audio chunks
                    audio_buffer.write(chunk)
                    chunk_count += 1
                    
                audio_bytes = audio_buffer.getvalue()
                Logger.info(f"Successfully converted text to speech ({len(audio_bytes)} bytes, {chunk_count} chunks)")
                return audio_bytes
                
        except RateLimitError as e:
            Logger.error(f"{__name__}> convert_to_speech -> Rate limit exceeded converting text to speech: {e}")
            return None
        except APIError as e:
            Logger.error(f"{__name__}> convert_to_speech -> API error converting text to speech: {e}")
            return None
        except APITimeoutError as e:
            Logger.error(f"{__name__}> convert_to_speech -> Timeout converting text to speech: {e}")
            return None
        except OpenAIError as e:
            Logger.error(f"{__name__}> convert_to_speech -> OpenAI error converting text to speech: {e}")
            return None
        except Exception as e:
            Logger.error(f"{__name__}> convert_to_speech -> Unexpected error converting text to speech: {e}")
            return None
