from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import Optional
from national_agentic_ai_hackathon_2025_backend.schemas.user import User
from national_agentic_ai_hackathon_2025_backend.context.coordinates import Coordinates
from national_agentic_ai_hackathon_2025_backend.bot.web_bot import WebBot, DeviceStatus

router = APIRouter(tags=["Chat"])

class ChatPayload(BaseModel):
    user: User
    message: str
    status: DeviceStatus
    coordinates: Optional[Coordinates] = None

@router.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        print("\n🟩 Received Payload:", body)  # Debug print

        # Try to validate manually to see what fails
        try:
            payload = ChatPayload(**body)
        except ValidationError as e:
            print("\n🟥 VALIDATION ERROR:", e.errors())  # show which field failed
            return JSONResponse(content={"validation_error": e.errors()}, status_code=422)

        bot = WebBot(status=payload.status)
        result = await bot.execute_workflow(
            user=payload.user,
            message=payload.message,
            coordinates=payload.coordinates,
        )

        return result

    except Exception as e:
        import traceback
        print("Error in /chat route:", traceback.format_exc())
        return JSONResponse(content={"error": str(e)}, status_code=500)
