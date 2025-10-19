import httpx
from pywa_async import WhatsApp
from national_agentic_ai_hackathon_2025_backend.utils.app_instance import app
from national_agentic_ai_hackathon_2025_backend.config import Config
from national_agentic_ai_hackathon_2025_backend._debug import Logger

# Global variable to hold the WhatsApp instance
wa = None

def create_wa_instance():
    """Create a new WhatsApp instance with current config values"""
    global wa
    try:
        config_data = {
            "phone_id": Config.get("WHATSAPP_PHONE_NO_ID"),
            "callback_url": Config.get("SERVER_BASE_URL"),
            "verify_token": Config.get("WHATSAPP_VERIFY_TOKEN", "whatsap-agent-sdk-sepcial-for-me"),
            "app_id": Config.get("WHATSAPP_APP_ID"),
            "business_account_id": Config.get("WHATSAPP_BUSINESS_ACCOUNT_ID")
        }
        Logger.debug(f"Raw WhatsApp config data: {config_data}")
        
        return WhatsApp(
            phone_id=Config.get("WHATSAPP_PHONE_NO_ID"),
            token=Config.get("WHATSAPP_ACCESS_TOKEN"),
            server=app,
            callback_url=Config.get("SERVER_BASE_URL"),
            verify_token=Config.get("WHATSAPP_VERIFY_TOKEN", "whatsap-agent-sdk-sepcial-for-me"),
            app_id=Config.get("WHATSAPP_APP_ID"),
            app_secret=Config.get("WHATSAPP_APP_SECRET"),
            business_account_id=Config.get("WHATSAPP_BUSINESS_ACCOUNT_ID"),
            validate_updates=True,
            continue_handling=False,
            webhook_endpoint="/webhook",
            webhook_challenge_delay=30,
            skip_duplicate_updates=True,
            # session=httpx.Client()
        )
    except Exception as e:
        Logger.error(f"Error creating WhatsApp instance: {e}")
        return None
    
# Initialize the WhatsApp instance
wa = create_wa_instance()
if wa:
    Logger.success("WhatsApp instance created successfully")
else:
    Logger.error("Failed to create WhatsApp instance")

from national_agentic_ai_hackathon_2025_backend.utils.whatsapp_essentials import *