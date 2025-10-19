from pydantic import BaseModel
from national_agentic_ai_hackathon_2025_backend.utils._helpers import _generate_random_id
from typing import Literal

class OrchestratorOutputType(BaseModel):
    case_id: str = _generate_random_id(4)
    request_type: Literal["medical", "police", "catastrophic"]
    request_text: str
    timestamp: str