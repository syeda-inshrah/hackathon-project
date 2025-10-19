from pydantic import BaseModel

class GuidanceOutputType(BaseModel):
    response: str
    is_critical: bool