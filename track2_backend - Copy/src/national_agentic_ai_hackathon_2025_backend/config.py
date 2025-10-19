import os
from dotenv import load_dotenv
from national_agentic_ai_hackathon_2025_backend._debug import Logger
from openai import AsyncOpenAI
from typing import Optional

load_dotenv()

class Config:
    """Manages application configuration"""
    sender_email = os.environ.get("SENDER_EMAIL")
    app_password = os.environ.get("APP_PASSWORD")
    
    @classmethod
    def get_openai_client(cls, sync: bool = False):
        """Get OpenAI client with proper error handling"""
        try:
            api_key = cls.get("OPENAI_API_KEY")
            
            if not api_key:
                Logger.warning("OPENAI_API_KEY missing; skipping OpenAI client setup")
                return None
            
            if not isinstance(api_key, str) or len(api_key.strip()) == 0:
                Logger.warning("OPENAI_API_KEY is empty or invalid")
                return None
            
            if sync:
                from openai import OpenAI
                Logger.info("Using OpenAI API key for sync client")
                return OpenAI(api_key=api_key)
            else:    
                return AsyncOpenAI(
                    api_key=api_key,
                    base_url="https://api.openai.com/v1"
                )
        except Exception as e:
            Logger.error(f"{__name__}> get_openai_client -> Error creating OpenAI client: {e}")
            return None

    @classmethod
    def get(cls, key: str, default: str = None) -> Optional[str]:
        """Get configuration value with validation"""
        try:
            if not key or not isinstance(key, str):
                Logger.warning(f"Invalid configuration key: {key}")
                return default
                
            value = os.environ.get(key, default)
            return value
        except Exception as e:
            Logger.error(f"{__name__}> get -> Error getting configuration value for key '{key}': {e}")
            return default
    
    @classmethod
    def get_required(cls, key: str) -> str:
        """Get required configuration value, raise error if missing"""
        value = cls.get(key)
        if value is None:
            raise ValueError(f"Required configuration '{key}' is not set")
        return value
    
    @classmethod
    def validate_required_configs(cls, required_keys: list) -> bool:
        """Validate that all required configuration keys are set"""
        missing_keys = []
        for key in required_keys:
            if not cls.get(key):
                missing_keys.append(key)
        
        if missing_keys:
            Logger.error(f"{__name__}> validate_required_configs -> Missing required configuration keys: {missing_keys}")
            return False
        
        Logger.info("All required configuration keys are present")
        return True