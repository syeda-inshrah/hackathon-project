from pydantic import BaseModel
from typing import Literal, Optional

class User(BaseModel):
    userid: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_loggedin: Optional[bool] = None
    phone_number: Optional[str] = None
    platform: Literal["website", "whatsapp", "mobile"]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None