from national_agentic_ai_hackathon_2025_backend._debug import Logger
import tempfile
import aiohttp
import os
from openai import OpenAI
from openai import OpenAIError, APIError, RateLimitError, APITimeoutError
from typing import Optional

class AudioProcessor:
    """Handles audio processing for voice messages"""
    
    def __init__(self, openai_client: OpenAI):
        try:
            if not openai_client or not isinstance(openai_client, OpenAI):
                raise ValueError("Invalid OpenAI client provided")
            self.client = openai_client
            Logger.info("Successfully initialized AudioProcessor")
        except Exception as e:
            Logger.error(f"{__name__}> __init__ -> Error initializing AudioProcessor: {e}")
            raise RuntimeError(f"Failed to initialize AudioProcessor: {e}")
    
    async def download_audio(self, audio_url: str, access_token: str) -> Optional[str]:
        """Download audio file from URL"""
        try:
            if not audio_url or not isinstance(audio_url, str):
                Logger.warning(f"Invalid audio URL provided: {audio_url}")
                return None
                
            if not access_token or not isinstance(access_token, str):
                Logger.warning(f"Invalid access token provided")
                return None
                
            headers = {
                "Authorization": f"Bearer {access_token}"
            }
            
            Logger.info(f"Downloading audio from URL: {audio_url[:50]}...")
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                async with session.get(audio_url, headers=headers) as response:
                    if response.status == 200:
                        # Create temporary file
                        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ogg')
                        try:
                            audio_data = await response.read()
                            if len(audio_data) == 0:
                                Logger.warning("Downloaded audio file is empty")
                                return None
                                
                            temp_file.write(audio_data)
                            temp_file.close()
                            Logger.info(f"Successfully downloaded audio file: {temp_file.name} ({len(audio_data)} bytes)")
                            return temp_file.name
                        except Exception as e:
                            Logger.error(f"Error writing audio data to temp file: {e}")
                            temp_file.close()
                            if os.path.exists(temp_file.name):
                                os.unlink(temp_file.name)
                            return None
                    else:
                        Logger.error(f"Download failed. Status: {response.status}")
                        try:
                            error_text = await response.text()
                            Logger.error(f"Response: {error_text}")
                        except:
                            Logger.error("Could not read error response")
                        return None
        except aiohttp.ClientError as e:
            Logger.error(f"{__name__}> download_audio -> Network error downloading audio: {e}")
            return None
        except Exception as e:
            Logger.error(f"{__name__}> download_audio -> Unexpected error downloading audio: {e}")
            return None

    async def download_audio_from_message(self, message) -> Optional[str]:
        """Download audio file from pywa Message object"""
        try:
            if not message:
                Logger.warning("Invalid message object provided")
                return None
                
            # Get the media URL from the message
            try:
                media_url = await message.audio.get_media_url()
                if not media_url:
                    Logger.warning("No media URL found in message")
                    return None
            except Exception as e:
                Logger.error(f"Error getting media URL from message: {e}")
                return None
            
            # Get the access token from config
            from national_agentic_ai_hackathon_2025_backend.config import Config
            access_token = Config.get("WHATSAPP_ACCESS_TOKEN")
            
            if not access_token:
                Logger.error("WHATSAPP_ACCESS_TOKEN not found in configuration")
                return None
            
            # Download the audio file
            return await self.download_audio(media_url, access_token)
            
        except Exception as e:
            Logger.error(f"{__name__}> download_audio_from_message -> Error downloading audio from message: {e}")
            return None

    async def convert_to_text(self, audio_file: str) -> Optional[str]:
        """Convert audio to text using Whisper"""
        try:
            if not audio_file or not isinstance(audio_file, str):
                Logger.warning(f"Invalid audio file path provided: {audio_file}")
                return None
                
            if not os.path.exists(audio_file):
                Logger.warning(f"Audio file does not exist: {audio_file}")
                return None
                
            # Check file size (Whisper has limits)
            file_size = os.path.getsize(audio_file)
            if file_size == 0:
                Logger.warning(f"Audio file is empty: {audio_file}")
                return None
                
            if file_size > 25 * 1024 * 1024:  # 25MB limit for Whisper
                Logger.warning(f"Audio file too large for Whisper ({file_size} bytes): {audio_file}")
                return None
            
            Logger.info(f"Converting audio to text: {audio_file} ({file_size} bytes)")
            
            with open(audio_file, "rb") as file:
                response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=file
                )
                
            if not response or not response.text:
                Logger.warning("Whisper returned empty transcription")
                return None
                
            Logger.info(f"Successfully transcribed audio: {len(response.text)} characters")
            return response.text
            
        except RateLimitError as e:
            Logger.error(f"{__name__}> convert_to_text -> Rate limit exceeded converting audio to text: {e}")
            return None
        except APIError as e:
            Logger.error(f"{__name__}> convert_to_text -> API error converting audio to text: {e}")
            return None
        except APITimeoutError as e:
            Logger.error(f"{__name__}> convert_to_text -> Timeout converting audio to text: {e}")
            return None
        except OpenAIError as e:
            Logger.error(f"{__name__}> convert_to_text -> OpenAI error converting audio to text: {e}")
            return None
        except Exception as e:
            Logger.error(f"{__name__}> convert_to_text -> Unexpected error converting audio to text: {e}")
            return None