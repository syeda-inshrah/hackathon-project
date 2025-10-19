from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
# from national_agentic_ai_hackathon_2025_backend.utils.wa_instance import wa
from national_agentic_ai_hackathon_2025_backend._debug import Logger, enable_verbose_logging
from national_agentic_ai_hackathon_2025_backend.utils.app_instance import app
from national_agentic_ai_hackathon_2025_backend.routes.chat import router

load_dotenv()
enable_verbose_logging()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)

@app.get("/", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify if the API is running.
    """
    return {
        "status": "healthy",
        "message": "WhatsApp Agent is running",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000) # set """reload = True""" for hot relod in development